#!/usr/bin/env python3
"""
EvolAgent Runner - Modern CLI interface for running experiments.

This module provides a unified entry point for running EvolAgent experiments
on different datasets with configurable parameters.
"""

import os
import sys
import time
import signal
import atexit
import argparse
import threading
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set matplotlib backend before any imports
os.environ['MPLBACKEND'] = 'Agg'
import matplotlib
matplotlib.use('Agg')

from src.utils.scorer import question_scorer, llm_scorer, check_close_call
from src.utils.loader import get_task_from_gaia, get_task_from_coldstart, get_all_task_ids_by_level
from src.pipelines import EvolvePipeline
from src.utils.config import config
from src.utils.logger import get_logger
from src.utils.manager import workspace_manager
from src.nodes.base import OPENAI_CLIENT_POOL
from src.memory.memory import Memory


class ExperimentRunner:
    """
    Modern experiment runner with comprehensive resource management and configuration.
    """
    
    def __init__(self):
        self.logger = get_logger("evolagent.runner")
        self._cleanup_in_progress = False
        self._cleanup_lock = threading.Lock()
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._cleanup_handler)
        signal.signal(signal.SIGTERM, self._cleanup_handler)
        atexit.register(self._comprehensive_cleanup)
        
    def _cleanup_handler(self, signum=None, frame=None):
        """Handle cleanup on program termination."""
        self.logger.info(f"Received termination signal {signum}, performing cleanup...")
        try:
            self._comprehensive_cleanup()
            self.logger.info("Cleanup completed, exiting gracefully...")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            import traceback
            self.logger.error(f"Cleanup traceback: {traceback.format_exc()}")
        finally:
            sys.exit(1)
    
    def _comprehensive_cleanup(self):
        """Comprehensive resource cleanup."""
        with self._cleanup_lock:
            if self._cleanup_in_progress:
                return
            self._cleanup_in_progress = True
        
        self.logger.info("Starting comprehensive resource cleanup...")
        
        try:
            # Clean up workspaces
            workspace_manager.cleanup_all()
            self.logger.info("Workspaces cleaned up")
            
            # Clean up OpenAI clients
            OPENAI_CLIENT_POOL.cleanup()
            self.logger.info("OpenAI clients cleaned up")
            
            # Clean up Qdrant connections
            Memory._cleanup_shared_client()
            self.logger.info("Qdrant connections cleaned up")
            
            # Process cleanup
            self._cleanup_processes()
            
            # Force garbage collection
            collected = gc.collect()
            self.logger.info(f"Garbage collection freed {collected} objects")
            
            # Thread monitoring
            active_threads = threading.active_count()
            if active_threads > 1:
                self.logger.info(f"Warning: {active_threads} threads still active")
                for thread in threading.enumerate():
                    if thread != threading.current_thread():
                        self.logger.debug(f"Active thread: {thread.name}")
            
            self.logger.info("Comprehensive cleanup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during comprehensive cleanup: {e}")
            import traceback
            self.logger.error(f"Cleanup traceback: {traceback.format_exc()}")
    
    def _cleanup_processes(self):
        """Clean up child processes."""
        try:
            import psutil
            current_process = psutil.Process(os.getpid())
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    self.logger.info(f"Terminating child process: {child.pid}")
                    child.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if children:
                psutil.wait_procs(children, timeout=3)
                self.logger.info(f"Terminated {len(children)} child processes")
                
        except (ImportError, Exception) as e:
            self.logger.warning(f"Process cleanup skipped: {e}")
    
    def _get_task_list(self, dataset: str, split: str, max_tasks: Optional[int] = None) -> List[str]:
        """Get task list based on dataset and configuration."""
        if dataset == "gaia":
            task_list = get_all_task_ids_by_level(split=split)
        elif dataset == "coldstart":
            task_list = [f"webshaper_{i}" for i in range(50)]
        else:
            raise ValueError(f"Unknown dataset: {dataset}")
        
        if max_tasks and max_tasks > 0:
            task_list = task_list[:max_tasks]
            
        return task_list
    
    def _run_single_task(self, task_id: str, dataset: str, split: str) -> Dict[str, Any]:
        """Run a single task with proper error handling and resource management."""
        pipeline = None
        try:
            pipeline = EvolvePipeline()
            self.logger.info(f"Starting task execution: {task_id}")
            
            # Load task based on dataset
            if dataset == "gaia":
                task_info = get_task_from_gaia(task_id, split)
                scorer_func = question_scorer
            elif dataset == "coldstart":
                task_info = get_task_from_coldstart(task_id, "webshaper")
                scorer_func = llm_scorer
            else:
                raise ValueError(f"Unknown dataset: {dataset}")
            
            self.logger.info(f"Loaded task: {task_info['question'][:200]}...")
            self.logger.debug(f"Full task info: {task_info}")
            
            start_time = time.time()
            
            # Execute task
            answer = pipeline(
                task=task_info["question"], 
                models=config.get('models.default_models', ['o4-mini']),
                task_id=task_id
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            self.logger.info(f"Task execution completed in {execution_time:.2f}s")

            # Handle test split
            if split == "test":
                return {
                    "answer": answer,
                    "task_id": task_id,
                    "execution_time": execution_time
                }
            
            # Evaluate answer
            if dataset == "gaia":
                is_correct = scorer_func(answer, task_info["true_answer"])
            else:  # coldstart
                is_correct = scorer_func(task_info["question"], answer, task_info["true_answer"])
                
            is_close = check_close_call(answer, task_info["true_answer"], is_correct)
            
            # Learn from correct answers
            if is_correct:
                self.logger.info("Task answered correctly, triggering learning")
                pipeline.learn()
            else:
                self.logger.info(f"Task answered incorrectly. Answer: {answer}, Expected: {task_info['true_answer']}")
                
            result = {
                "answer": answer,
                "true_answer": task_info["true_answer"],
                "is_correct": is_correct,
                "is_close": is_close,
                "task_id": task_id,
                "execution_time": execution_time
            }
            self.logger.info(f"Validation result: {result}")
            return result
                
        except Exception as e:
            self.logger.error(f"Error in task execution for {task_id}: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "answer": "Error occurred during task execution",
                "task_id": task_id,
                "is_correct": False,
                "error": str(e)
            }
        finally:
            if pipeline and hasattr(pipeline, '__del__'):
                try:
                    pipeline.__del__()
                except:
                    pass
            gc.collect()
    
    def run_experiment(self, dataset: str, split: str, max_tasks: Optional[int] = None, 
                      parallel_workers: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Run experiment with specified parameters.
        
        Args:
            dataset: Dataset to run ("gaia" or "coldstart")
            split: Data split ("validation" or "test")
            max_tasks: Maximum number of tasks to run (None for all)
            parallel_workers: Number of parallel workers (None for config default)
            
        Returns:
            List of task results
        """
        # Get task list
        task_list = self._get_task_list(dataset, split, max_tasks)
        
        # Set parallel workers
        if parallel_workers is None:
            parallel_workers = config.get('runtime.parallel_workers', config.get('pipeline.max_parallel_tasks', 3))
        
        self.logger.info(f"Starting {dataset} experiment with {len(task_list)} tasks")
        self.logger.info(f"Using {parallel_workers} parallel workers")
        self.logger.info(f"Split: {split}")
        
        results = []
        executor = None
        futures = []
        
        try:
            executor = ThreadPoolExecutor(
                max_workers=parallel_workers,
                thread_name_prefix=f"EvolAgent-{dataset.title()}-Worker"
            )
            
            # Submit all tasks
            future_to_task_id = {}
            for task_id in task_list:
                future = executor.submit(self._run_single_task, task_id, dataset, split)
                future_to_task_id[future] = task_id
                futures.append(future)
            
            self.logger.info(f"Submitted {len(futures)} tasks to executor")
            
            # Collect results
            completed_count = 0
            for future in as_completed(future_to_task_id, timeout=None):
                task_id = future_to_task_id[future]
                try:
                    result = future.result(timeout=10000)  # 10000 seconds per task
                    results.append(result)
                    completed_count += 1
                    self.logger.info(f"Completed task {completed_count}/{len(task_list)} - {task_id}: {result.get('is_correct', 'N/A')}")
                    
                    # Periodic garbage collection
                    if completed_count % 5 == 0:
                        collected = gc.collect()
                        self.logger.debug(f"Periodic GC: freed {collected} objects")
                        
                except TimeoutError:
                    self.logger.error(f"Task {task_id} timed out after 10000 seconds")
                    future.cancel()
                    results.append({
                        "task_id": task_id,
                        "is_correct": False,
                        "error": "Timeout"
                    })
                except Exception as exc:
                    self.logger.error(f"Task {task_id} generated an exception: {exc}")
                    import traceback
                    self.logger.error(f"Exception traceback: {traceback.format_exc()}")
                    results.append({
                        "task_id": task_id,
                        "is_correct": False,
                        "error": str(exc)
                    })
            
            # Summary statistics
            self._print_summary(results)
            return results
        
        except KeyboardInterrupt:
            self.logger.info("Execution interrupted by user")
            self._cancel_futures(futures, future_to_task_id)
            if executor:
                executor.shutdown(wait=False, cancel_futures=True)
            self._comprehensive_cleanup()
            sys.exit(0)
            
        except Exception as e:
            self.logger.error(f"Unexpected error during execution: {e}")
            import traceback
            self.logger.error(f"Exception traceback: {traceback.format_exc()}")
            self._cancel_futures(futures, future_to_task_id)
            if executor:
                executor.shutdown(wait=False, cancel_futures=True)
            self._comprehensive_cleanup()
            raise
            
        finally:
            if executor:
                try:
                    self.logger.info("Final executor shutdown...")
                    executor.shutdown(wait=True, cancel_futures=True)
                except Exception as cleanup_error:
                    self.logger.error(f"Error during executor shutdown: {cleanup_error}")
            self._comprehensive_cleanup()
    
    def _cancel_futures(self, futures: List, future_to_task_id: Dict):
        """Cancel all pending futures."""
        for future in futures:
            if not future.done():
                self.logger.info(f"Cancelling task: {future_to_task_id.get(future, 'unknown')}")
                future.cancel()
    
    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print experiment summary statistics."""
        if not results:
            self.logger.warning("No results to summarize")
            return
            
        total_tasks = len(results)
        correct_tasks = sum(1 for r in results if r.get('is_correct', False))
        success_rate = correct_tasks / total_tasks * 100
        self.logger.info(f"Final Summary: {correct_tasks}/{total_tasks} tasks completed successfully ({success_rate:.1f}%)")
        
        # Detailed statistics
        error_tasks = sum(1 for r in results if 'error' in r)
        timeout_tasks = sum(1 for r in results if r.get('error') == 'Timeout')
        self.logger.info(f"Error breakdown: {error_tasks} errors ({timeout_tasks} timeouts)")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI interface."""
    parser = argparse.ArgumentParser(
        description="EvolAgent - Multi-Agent AI System for Complex Task Solving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --dataset gaia --split validation --max-tasks 10\n"
            "  %(prog)s --dataset coldstart --parallel-workers 2\n"
            "  %(prog)s --dataset gaia --split test --max-tasks 5"
        )
    )
    
    parser.add_argument(
        '--dataset', 
        choices=['gaia', 'coldstart'],
        default=config.get('runtime.dataset', 'gaia'),
        help='Dataset to run experiments on (default: %(default)s)'
    )
    
    parser.add_argument(
        '--split',
        choices=['validation', 'test'],
        default=config.get('runtime.split', 'validation'),
        help='Data split to use (default: %(default)s)'
    )
    
    parser.add_argument(
        '--max-tasks',
        type=int,
        default=config.get('runtime.max_tasks'),
        help='Maximum number of tasks to run (default: all tasks)'
    )
    
    parser.add_argument(
        '--parallel-workers',
        type=int,
        default=config.get('runtime.parallel_workers'),
        help='Number of parallel workers (default: %(default)s)'
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=config.get('logging.level', 'INFO'),
        help='Logging level (default: %(default)s)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='EvolAgent 1.0.0'
    )
    
    return parser


def main():
    """Main entry point for the CLI interface."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Update config if custom config file provided
    if args.config:
        if not args.config.exists():
            print(f"Error: Configuration file not found: {args.config}")
            sys.exit(1)
        # Would need to implement config reloading here
        print(f"Using custom configuration: {args.config}")
    
    # Initialize runner and execute experiment
    runner = ExperimentRunner()
    
    try:
        results = runner.run_experiment(
            dataset=args.dataset,
            split=args.split,
            max_tasks=args.max_tasks,
            parallel_workers=args.parallel_workers
        )
        
        runner.logger.info("Experiment completed successfully")
        runner.logger.info("Check episodic memories for learned experiences!")
        
    except Exception as e:
        runner.logger.error(f"Experiment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 