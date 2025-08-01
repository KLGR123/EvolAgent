import os
import sys
import time
import signal
import atexit
import threading
import gc
from typing import Literal
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set environment variable to ensure matplotlib uses non-GUI backend
os.environ['MPLBACKEND'] = 'Agg'

# Set matplotlib backend to non-GUI before any other matplotlib imports
import matplotlib
matplotlib.use('Agg')  # Use Anti-Grain Geometry backend (no GUI)

from main import TASK_ID_LIST
from src.utils.scorer import llm_scorer, question_scorer, check_close_call
from src.utils.loader import get_task_from_coldstart
from src.pipelines import EvolvePipeline
from src.config import config
from src.utils.logger import get_logger, TaskLogger
from src.utils.workspace_manager import cleanup_all_workspaces
from src.nodes.base import cleanup_openai_clients
from src.memory.memory import Memory

# 全局清理状态标志
_cleanup_in_progress = False
_cleanup_lock = threading.Lock()

TASK_ID_LIST = ["webshaper_"+str(i) for i in range(50)]
# TASK_ID_LIST =["3", "4"]

def single_run(task_id: str, 
    split: Literal["validation", "test"]
) -> dict:
    """
    Run the pipeline for the whole GAIA dataset with enhanced logging and resource management.
    """
    pipeline = None
    try:
        pipeline = EvolvePipeline()
        with TaskLogger(task_id) as task_logger:
            task_logger.info(f"Starting task execution: {task_id}")
            
            task_info = get_task_from_coldstart(task_id, "webshaper")
            task_logger.info(f"Loaded task: {task_info['question'][:200]}...")
            task_logger.debug(f"Full task info: {task_info}")
            
            start_time = time.time()
            
            # Use configured models instead of hardcoded list with task_id for workspace isolation
            answer = pipeline(
                task=task_info["question"], 
                models=config.default_models,
                task_id=task_id
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            task_logger.info(f"Task execution completed in {execution_time:.2f}s")

            if split == "test":
                result = {
                    "answer": answer,
                    "task_id": task_id,
                    "execution_time": execution_time
                }
                task_logger.info(f"Test result: {result}")
                return result
            
            # is_correct = question_scorer(answer, task_info["true_answer"])
            is_correct = llm_scorer(task_info["question"],answer, task_info["true_answer"])
            is_close = check_close_call(answer, task_info["true_answer"], is_correct)
            
            if is_correct:
                task_logger.info("Task answered correctly, triggering learning")
                pipeline.learn()
            else:
                task_logger.info(f"Task answered incorrectly. Answer: {answer}, Expected: {task_info['true_answer']}")
                
            result = {
                "answer": answer,
                "true_answer": task_info["true_answer"],
                "is_correct": is_correct,
                "is_close": is_close,
                "task_id": task_id,
                "execution_time": execution_time
            }
            task_logger.info(f"Validation result: {result}")
            return result
            
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error in single_run task execution for {task_id}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "answer": "Error occurred during task execution",
            "task_id": task_id,
            "is_correct": False,
            "error": str(e)
        }
    finally:
        # 清理pipeline资源
        if pipeline and hasattr(pipeline, '__del__'):
            try:
                pipeline.__del__()
            except:
                pass
        # 强制垃圾回收
        gc.collect()


def comprehensive_cleanup():
    """
    执行全面的资源清理。
    """
    global _cleanup_in_progress
    
    with _cleanup_lock:
        if _cleanup_in_progress:
            return
        _cleanup_in_progress = True
    
    logger = get_logger(__name__)
    logger.info("Starting comprehensive resource cleanup...")
    
    try:
        # 1. 清理工作区
        cleanup_all_workspaces()
        logger.info("Workspaces cleaned up")
        
        # 2. 清理OpenAI客户端连接
        cleanup_openai_clients()
        logger.info("OpenAI clients cleaned up")
        
        # 3. 清理Qdrant连接
        Memory._cleanup_shared_client()
        logger.info("Qdrant connections cleaned up")
        
        # 4. 清理其他可能的资源
        try:
            import subprocess
            import psutil
            
            # Clean up any child processes
            current_process = psutil.Process(os.getpid())
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    logger.info(f"Terminating child process: {child.pid}")
                    child.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Wait for children to terminate
            if children:
                psutil.wait_procs(children, timeout=3)
                logger.info(f"Terminated {len(children)} child processes")
                
        except (ImportError, Exception) as e:
            logger.warning(f"Process cleanup skipped: {e}")
        
        # 5. 强制垃圾回收
        collected = gc.collect()
        logger.info(f"Garbage collection freed {collected} objects")
        
        # 6. 清理线程资源
        active_threads = threading.active_count()
        if active_threads > 1:  # Main thread + others
            logger.info(f"Warning: {active_threads} threads still active")
            for thread in threading.enumerate():
                if thread != threading.current_thread():
                    logger.debug(f"Active thread: {thread.name}")
        
        logger.info("Comprehensive cleanup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during comprehensive cleanup: {e}")
        import traceback
        logger.error(f"Cleanup traceback: {traceback.format_exc()}")


def cleanup_handler(signum=None, frame=None):
    """Handle cleanup on program termination with improved resource management."""
    logger = get_logger(__name__)
    logger.info(f"Received termination signal {signum}, performing cleanup...")
    
    try:
        comprehensive_cleanup()
        logger.info("Cleanup completed, exiting gracefully...")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        import traceback
        logger.error(f"Cleanup traceback: {traceback.format_exc()}")
    finally:
        # Use sys.exit instead of os._exit to allow proper cleanup
        sys.exit(1)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Starting EvolAgent single_run execution")
    logger.info(f"Configuration loaded: max_parallel_tasks={config.max_parallel_tasks}")

    # Register cleanup handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, cleanup_handler)  # Termination
    atexit.register(comprehensive_cleanup)  # Normal exit
    
    # Use ThreadPoolExecutor for parallel task execution with configured limits
    max_workers = config.max_parallel_tasks
    results = []
    
    logger.info(f"Processing {len(TASK_ID_LIST)} tasks with {max_workers} parallel workers")
    
    executor = None
    futures = []
    try:
        executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="EvolAgent-Worker"
        )
        
        # Submit all tasks to the executor
        future_to_task_id = {}
        for task_id in TASK_ID_LIST:
            future = executor.submit(single_run, task_id, "validation")
            future_to_task_id[future] = task_id
            futures.append(future)
        
        logger.info(f"Submitted {len(futures)} tasks to executor")
        
        # Collect results as they complete with proper timeout handling
        completed_count = 0
        for future in as_completed(future_to_task_id, timeout=None):
            task_id = future_to_task_id[future]
            try:
                # Use longer timeout to avoid premature cancellation
                result = future.result(timeout=600)  # 10 minutes per task
                results.append(result)
                completed_count += 1
                logger.info(f"Completed task {completed_count}/{len(TASK_ID_LIST)} - {task_id}: {result.get('is_correct', 'N/A')}")
                
                # 定期强制垃圾回收以释放内存
                if completed_count % 5 == 0:
                    collected = gc.collect()
                    logger.debug(f"Periodic GC: freed {collected} objects")
                    
            except TimeoutError:
                logger.error(f"Task {task_id} timed out after 10 minutes")
                future.cancel()
                results.append({
                    "task_id": task_id,
                    "is_correct": False,
                    "error": "Timeout"
                })
            except Exception as exc:
                logger.error(f"Task {task_id} generated an exception: {exc}")
                import traceback
                logger.error(f"Exception traceback: {traceback.format_exc()}")
                results.append({
                    "task_id": task_id,
                    "is_correct": False,
                    "error": str(exc)
                })
        
        # Summary statistics
        if results:
            total_tasks = len(results)
            correct_tasks = sum(1 for r in results if r.get('is_correct', False))
            success_rate = correct_tasks / total_tasks * 100
            logger.info(f"Final Summary: {correct_tasks}/{total_tasks} tasks completed successfully ({success_rate:.1f}%)")
            
            # 详细统计
            error_tasks = sum(1 for r in results if 'error' in r)
            timeout_tasks = sum(1 for r in results if r.get('error') == 'Timeout')
            logger.info(f"Error breakdown: {error_tasks} errors ({timeout_tasks} timeouts)")
        
        logger.info("Check Episodic Memories!")
        # pipeline.clear_episodic()
        logger.info("EvolAgent execution completed")
    
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        # Cancel all pending futures
        for future in futures:
            if not future.done():
                logger.info(f"Cancelling task: {future_to_task_id.get(future, 'unknown')}")
                future.cancel()
        
        if executor:
            logger.info("Shutting down executor...")
            executor.shutdown(wait=False, cancel_futures=True)
            
        comprehensive_cleanup()
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unexpected error during execution: {e}")
        import traceback
        logger.error(f"Exception traceback: {traceback.format_exc()}")
        
        # Cancel all pending futures on error
        for future in futures:
            if not future.done():
                future.cancel()
        
        if executor:
            executor.shutdown(wait=False, cancel_futures=True)
            
        comprehensive_cleanup()
        raise
        
    finally:
        # Final cleanup to ensure all temporary workspaces are removed
        if executor:
            try:
                logger.info("Final executor shutdown...")
                executor.shutdown(wait=True, cancel_futures=True)
            except Exception as cleanup_error:
                logger.error(f"Error during executor shutdown: {cleanup_error}")
        
        comprehensive_cleanup()
        logger.info("All cleanup completed, program ending")