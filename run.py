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
            # task_list = get_all_task_ids_by_level(split=split)
            task_done = [
                "11af4e1a-5f45-467d-9aeb-46f4bb0bf034",
                "1f975693-876d-457b-a649-393859e79bf3",
                "27d5d136-8563-469e-92bf-fd103c28b57c",
                "2d83110e-a098-4ebb-9987-066c06fa42d0",
                "389793a7-ca17-4e82-81cb-2b3a2391b4b9",
                "3f57289b-8c60-48be-bd80-01f8099ca449",
                "4b650a35-8529-4695-89ed-8dc7a500a498",
                "305ac316-eef6-4446-960a-92d80d542f82",
                "50ec8903-b81f-4257-9450-1085afd2c319",
                "5188369a-3bbe-43d8-8b94-11558f909a08",
                "5a0c1adf-205e-4841-a666-7c3ef95def9d",
                "5cfb274c-0207-4aa7-9575-6ac0bd95d9b2",
                "6f37996b-2ac7-44b0-8e68-6d28256631b4",
                "7bd855d8-463d-4ed5-93ca-5fe35145f733",
                "8e867cd7-cff9-4e6c-867a-ff5ddc2550be",
                "99c9cc74-fdc8-46c6-8f8d-3ce2d3bfeea3",
                "a3fbeb63-0e8c-4a11-bff6-0e3b484c3e9c",
                "bda648d7-d618-4883-88f4-3466eabd860e",
                "c714ab3a-da30-4603-bacd-d008800188b9",
                "cffe0e32-c9a6-4c52-9877-78ceb4aaa9fb",
                "dc28cf18-6431-458b-83ef-64b3ce566c10",
                "f918266a-b3e0-4914-865d-4faa564f1aef",
                "935e2cff-ae78-4218-b3f5-115589b19dae",
                "50ad0280-0819-4bd9-b275-5de32d3b5bcb",
                "0ff53813-3367-4f43-bcbd-3fd725c1bf4b",
                "076c8171-9b3b-49b9-a477-244d2a532826",
                "08c0b6e9-1b43-4c2e-ae55-4e3fce2c2715",
                "0a65cb96-cb6e-4a6a-8aae-c1084f613456",
                "366e2f2b-8632-4ef2-81eb-bc3877489217",
                "14569e28-c88c-43e4-8c32-097d35b9a67d",
                "32102e3e-d12a-4209-9163-7b3a104efe5d",
                "33d8ea3b-6c6b-4ff1-803d-7e270dea8a57",
                "4d0aa727-86b1-406b-9b33-f870dd14a4a5",
                "f0f46385-fc03-4599-b5d3-f56496c3e69f",
                "544b7f0c-173a-4377-8d56-57b36eb26ddf",
                "54612da3-fd56-4941-80f4-5eb82330de25",
                "65638e28-7f37-4fa7-b7b9-8c19bb609879",
                "65da0822-a48a-4a68-bbad-8ed1b835a834",
                "67e8878b-5cef-4375-804e-e6291fdbe78a",
                "7cc4acfa-63fd-4acc-a1a1-e8e529e0a97f",
                "87c610df-bef7-4932-b950-1d83ef4e282b",
                "a26649c6-1cb2-470a-871e-6910c64c3e53",
                "b9763138-c053-4832-9f55-86200cb1f99c",
                "3ff6b7a9-a5bd-4412-ad92-0cd0d45c0fee",
                "3627a8be-a77f-41bb-b807-7e1bd4c0ebdf",
                "ad37a656-079a-49f9-a493-7b739c9167d1",
                "73c1b9fe-ee1d-4cf4-96ca-35c08f97b054",
                "d8152ad6-e4d5-4c12-8bb7-8d57dc10c6de",
                "dd3c7503-f62a-4bd0-9f67-1b63b94194cc",
                "e4e91f1c-1dcd-439e-9fdd-cb976f5293fd",
                "e9a2c537-8232-4c3f-85b0-b52de6bcba99",
                "ded28325-3447-4c56-860f-e497d6fb3577",
                "e961a717-6b25-4175-8a68-874d28190ee4",
                "42576abe-0deb-4869-8c63-225c2d75a95a",
                "5d0080cb-90d7-4712-bc33-848150e917d3",
                "3cef3a44-215e-4aed-8e3b-b1e3f08063b7",
                "c365c1c7-a3db-4d5e-a9a1-66f56eae7865",
                "e0c10771-d627-4fd7-9694-05348e54ee36",
                "56db2318-640f-477a-a82f-bc93ad13e882",
                "4fc2f1ae-8625-45b5-ab34-ad4433bc21f8",
                "9d191bce-651d-4746-be2d-7ef8ecadb9c2",
                "a0068077-79f4-461a-adfe-75c1a4148545",
                "b816bfce-3d80-4913-a07d-69b752ce6377",
                "e1fc63a2-da7a-432f-be78-7c4a95598703",
                "6b078778-0b90-464d-83f6-59511c811b01",
                "7619a514-5fa8-43ef-9143-83b66a43d7a4",
                "7dd30055-0198-452e-8c25-f73dbe27dcb8",
                "edd4d4f2-1a58-45c4-b038-67337af4e029",
                "d1af70ea-a9a4-421a-b9cc-94b5e02f1788",
                "f3917a3d-1d17-4ee2-90c5-683b072218fe",
                "f46b4380-207e-4434-820b-f32ce04ae2a4",
                "08f3a05f-5947-4089-a4c4-d4bcfaa6b7a0",
                "08cae58d-4084-4616-b6dd-dd6534e4825b",
                "851e570a-e3de-4d84-bcfa-cc85578baa59",
                "da52d699-e8d2-4dc5-9191-a2199e0b6a9b",
                "65afbc8a-89ca-4ad5-8d62-355bb401f61d",
                "e29834fd-413a-455c-a33e-c3915b07401c",
                "ec09fa32-d03f-4bf8-84b0-1f16922c3ae4",
                "cabe07ed-9eca-40ea-8ead-410ef5e83f91",
                "17b5a6a3-bc87-42e8-b0fb-6ab0781ef2cc",
                "2a649bb1-795f-4a01-b3be-9a01868dae73",
                "04a04a9b-226c-43fd-b319-d5e89743676f",
                "a1e91b78-d3d8-4675-bb8d-62741b4b68a6",
                "b7f857e4-d8aa-4387-af2a-0e844df5b9d8",
                "d700d50d-c707-4dca-90dc-4528cddd0c80",
                "840bfca7-4f7b-481a-8794-c560c340185d",
                "71345b0a-9c7d-4b50-b2bf-937ec5879845",
                "0bdb7c40-671d-4ad1-9ce3-986b159c0ddc",
                "ebbc1f13-d24d-40df-9068-adcf735b4240",
                "0a3cd321-3e76-4622-911b-0fda2e5d6b1a",
                "db4fd70a-2d37-40ea-873f-9433dc5e301f",
                "2b3ef98c-cc05-450b-a719-711aee40ac65",
                "c61d22de-5f6c-4958-a7f6-5e9707bd3466",
                "b2c257e0-3ad7-4f05-b8e3-d9da973be36e",
                "114d5fd0-e2ae-4b6d-a65a-870da2d19c08",
                "f2feb6a4-363c-4c09-a804-0db564eafd68",
                "9b54f9d9-35ee-4a14-b62f-d130ea00317f",
                "50f58759-7bd6-406f-9b0d-5692beb2a926",
                "dc22a632-937f-4e6a-b72f-ba0ff3f5ff97",
            ]
            task_list = [
                "676e5e31-a554-4acc-9286-b60d90a92d26",
                "0383a3ee-47a7-41a4-b493-519bdefe0488",
                "7d4a7d1d-cac6-44a8-96e8-ea9584a70825",
                "e142056d-56ab-4352-b091-b56054bd1359",
                "d0633230-7067-47a9-9dbf-ee11e0a2cdd6",
                "023e9d44-96ae-4eed-b912-244ee8c3b994",
                "20194330-9976-4043-8632-f8485c6c71b2",
                "48eb8242-1099-4c26-95d4-ef22b002457a",
                "853c8244-429e-46ca-89f2-addf40dfb2bd",
                "1dcc160f-c187-48c2-b68e-319bd4354f3d",
                "e2d69698-bc99-4e85-9880-67eaccd66e6c",
                "8131e2c0-0083-4265-9ce7-78c2d568425d",
                "872bfbb1-9ccf-49f6-8c5f-aa22818ccd66",
                "8d46b8d6-b38a-47ff-ac74-cda14cf2d19b",
                "ad2b4d70-9314-4fe6-bfbe-894a45f6055f",
                "c3a79cfe-8206-451f-aca8-3fec8ebe51d3",
                "3da89939-209c-4086-8520-7eb734e6b4ef",
                "46719c30-f4c3-4cad-be07-d5cb21eee6bb",
                "4b6bb5f7-f634-410e-815d-e673ab7f8632",
                "72e110e7-464c-453c-a309-90a95aed6538",
                "7673d772-ef80-4f0f-a602-1bf4485c9b43",
                "9318445f-fe6a-4e1b-acbf-c68228c9906a",
                "cca530fc-4052-43b2-b130-b30968d8aa44",
                "d5141ca5-e7a0-469f-bf3e-e773507c86e2",
                "0b260a57-3f3a-4405-9f29-6d7a1012dbfb",
                "0e9e85b8-52b9-4de4-b402-5f635ab9631f",
                "16d825ff-1623-4176-a5b5-42e0f5c2b0ac",
                "42d4198c-5895-4f0a-b0c0-424a66465d83",
                "4d51c4bf-4b0e-4f3d-897b-3f6687a7d9f2",
                "624cbf11-6a41-4692-af9c-36b3e5ca3130",
                "6359a0b1-8f7b-499b-9336-840f9ab90688",
                "708b99c5-e4a7-49cb-a5cf-933c8d46470d",
                "7a4a336d-dcfa-45a0-b014-824c7619e8de",
                "8b3379c0-0981-4f5b-8407-6444610cb212",
                "8f80e01c-1296-4371-9486-bb3d68651a60",
                "a7feb290-76bb-4cb7-8800-7edaf7954f2f",
                "bfcd99e1-0690-4b53-a85c-0174a8629083",
                "c8b7e059-c60d-472e-ad64-3b04ae1166dc",
                "df6561b2-7ee5-4540-baab-5095f742716a",
                "ecbc4f94-95a3-4cc7-b255-6741a458a625",
                "00d579ea-0889-4fd9-a771-2c8d79835c8d",
                "384d0dd8-e8a4-4cfe-963c-d37f256e7662",
                "5f982798-16b9-4051-ab57-cfc7ebdb2a91",
                "72c06643-a2fa-4186-aa5c-9ec33ae9b445",
                "983bba7c-c092-455f-b6c9-7857003d48fc",
                "bec74516-02fc-48dc-b202-55e78d0e17cf",
                "c526d8d6-5987-4da9-b24c-83466fa172f3",
                "56137764-b4e0-45b8-9c52-1866420c3df5", # wrong
                "b415aba4-4b68-4fc6-9b89-2c812e55a3e1", # wrong
                "0bb3b44a-ede5-4db5-a520-4e844b0079c5", # wrong
                "9f41b083-683e-4dcf-9185-ccfeaa88fa45", # wrong
                "05407167-39ec-4d3a-a234-73a9120c325d", # wrong
                "7b5377b0-3f38-4103-8ad2-90fe89864c04", # wrong
                "ed58682d-bc52-4baa-9eb0-4eb81e1edacc", # wrong
                "cca70ce6-1952-45d2-acd4-80c903b0bc49", # wrong
                "2dfc4c37-fec1-4518-84a7-10095d30ad75", # wrong
                "b4cc024b-3f5e-480e-b96a-6656493255b5", # wrong
                "de9887f5-ead8-4727-876f-5a4078f8598c", # wrong
                "a56f1527-3abf-41d6-91f8-7296d6336c3f", # wrong
                "e8cb5b03-41e0-4086-99e5-f6806cd97211", # wrong
                "0512426f-4d28-49f0-be77-06d05daec096", # wrong
                "5b2a14e8-6e59-479c-80e3-4696e8980152", # wrong
                "9e1fc53b-46ff-49a1-9d05-9e6faac34cc5", # wrong
                "a0c07678-e491-4bbc-8f0b-07405144218f", # wrong
                "23dd907f-1261-4488-b21c-e9185af91d5e", # wrong
            ]
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
            parallel_workers = config.get('runtime.parallel_workers', 3)
        
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
                    task_timeout = config.get('runtime.task_timeout_seconds', 7200)  # 2 hours default
                    result = future.result(timeout=task_timeout)
                    results.append(result)
                    completed_count += 1
                    self.logger.info(f"Completed task {completed_count}/{len(task_list)} - {task_id}: {result.get('is_correct', 'N/A')}")
                    
                    # Periodic garbage collection
                    if completed_count % 5 == 0:
                        collected = gc.collect()
                        self.logger.debug(f"Periodic GC: freed {collected} objects")
                        
                except TimeoutError:
                    task_timeout = config.get('runtime.task_timeout_seconds', 7200)
                    self.logger.error(f"Task {task_id} timed out after {task_timeout} seconds")
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