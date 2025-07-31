import os
import sys
import time
import signal
import atexit
import threading
import multiprocessing
import gc
from typing import Literal
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set environment variable to ensure matplotlib uses non-GUI backend
os.environ['MPLBACKEND'] = 'Agg'

# Set matplotlib backend to non-GUI before any other matplotlib imports
import matplotlib
matplotlib.use('Agg')  # Use Anti-Grain Geometry backend (no GUI)

from src.utils.scorer import question_scorer, check_close_call
from src.utils.loader import get_task_from_gaia, get_all_task_ids_by_level
from src.pipelines import EvolvePipeline
from src.config import config
from src.utils.logger import get_logger, TaskLogger
from src.utils.workspace_manager import cleanup_all_workspaces
from src.nodes.base import cleanup_openai_clients
from src.memory.memory import Memory

# 全局清理状态标志
_cleanup_in_progress = False
_cleanup_lock = threading.Lock()

# TASK_ID_LIST = get_all_task_ids_by_level(split="validation")

TASK_DONE = [
    # "11af4e1a-5f45-467d-9aeb-46f4bb0bf034",
    # "1f975693-876d-457b-a649-393859e79bf3",
    # "27d5d136-8563-469e-92bf-fd103c28b57c",
    # "2d83110e-a098-4ebb-9987-066c06fa42d0",
    # "389793a7-ca17-4e82-81cb-2b3a2391b4b9",
    # "3f57289b-8c60-48be-bd80-01f8099ca449",
    # "4b650a35-8529-4695-89ed-8dc7a500a498",
    # "305ac316-eef6-4446-960a-92d80d542f82",
    # "50ec8903-b81f-4257-9450-1085afd2c319",
    # "5188369a-3bbe-43d8-8b94-11558f909a08",
    # "5a0c1adf-205e-4841-a666-7c3ef95def9d",
    # "5cfb274c-0207-4aa7-9575-6ac0bd95d9b2",
    # "6f37996b-2ac7-44b0-8e68-6d28256631b4",
    # "7bd855d8-463d-4ed5-93ca-5fe35145f733",
    # "8e867cd7-cff9-4e6c-867a-ff5ddc2550be",
    # "99c9cc74-fdc8-46c6-8f8d-3ce2d3bfeea3",
    # "a3fbeb63-0e8c-4a11-bff6-0e3b484c3e9c",
    # "b415aba4-4b68-4fc6-9b89-2c812e55a3e1", # wrong
    # "bda648d7-d618-4883-88f4-3466eabd860e",
    # "c714ab3a-da30-4603-bacd-d008800188b9",
    # "cffe0e32-c9a6-4c52-9877-78ceb4aaa9fb",
    # "dc28cf18-6431-458b-83ef-64b3ce566c10",
    # "ec09fa32-d03f-4bf8-84b0-1f16922c3ae4", # wrong
    # "f918266a-b3e0-4914-865d-4faa564f1aef",
    # "935e2cff-ae78-4218-b3f5-115589b19dae",
    # "50ad0280-0819-4bd9-b275-5de32d3b5bcb",
    # "0ff53813-3367-4f43-bcbd-3fd725c1bf4b",
    # "076c8171-9b3b-49b9-a477-244d2a532826",
    # "08c0b6e9-1b43-4c2e-ae55-4e3fce2c2715",
    # "0a65cb96-cb6e-4a6a-8aae-c1084f613456",
    # "366e2f2b-8632-4ef2-81eb-bc3877489217",
    # "14569e28-c88c-43e4-8c32-097d35b9a67d",
    # "32102e3e-d12a-4209-9163-7b3a104efe5d",
    # "33d8ea3b-6c6b-4ff1-803d-7e270dea8a57",
    # "4d0aa727-86b1-406b-9b33-f870dd14a4a5",
    # "f0f46385-fc03-4599-b5d3-f56496c3e69f",
    # "544b7f0c-173a-4377-8d56-57b36eb26ddf",
    # "54612da3-fd56-4941-80f4-5eb82330de25",
    # "65638e28-7f37-4fa7-b7b9-8c19bb609879",
    # "65da0822-a48a-4a68-bbad-8ed1b835a834",
    # "67e8878b-5cef-4375-804e-e6291fdbe78a",
    # "7cc4acfa-63fd-4acc-a1a1-e8e529e0a97f",
    # "87c610df-bef7-4932-b950-1d83ef4e282b",
    # "9f41b083-683e-4dcf-9185-ccfeaa88fa45", # wrong
    # "a26649c6-1cb2-470a-871e-6910c64c3e53",
    # "b9763138-c053-4832-9f55-86200cb1f99c",
]

TASK_ID_LIST = [
    "3627a8be-a77f-41bb-b807-7e1bd4c0ebdf",
    "3ff6b7a9-a5bd-4412-ad92-0cd0d45c0fee", # correct already, rerun
    "73c1b9fe-ee1d-4cf4-96ca-35c08f97b054",
    "ad37a656-079a-49f9-a493-7b739c9167d1",
    "b7f857e4-d8aa-4387-af2a-0e844df5b9d8",
    "d8152ad6-e4d5-4c12-8bb7-8d57dc10c6de",
    "dd3c7503-f62a-4bd0-9f67-1b63b94194cc",
    "e0c10771-d627-4fd7-9694-05348e54ee36",
    "e4e91f1c-1dcd-439e-9fdd-cb976f5293fd",
    "e9a2c537-8232-4c3f-85b0-b52de6bcba99",
    "ded28325-3447-4c56-860f-e497d6fb3577",
    "0bb3b44a-ede5-4db5-a520-4e844b0079c5",
    "56db2318-640f-477a-a82f-bc93ad13e882",
    "e961a717-6b25-4175-8a68-874d28190ee4",
    "42576abe-0deb-4869-8c63-225c2d75a95a",
    "4fc2f1ae-8625-45b5-ab34-ad4433bc21f8",
    "5d0080cb-90d7-4712-bc33-848150e917d3",
    "65afbc8a-89ca-4ad5-8d62-355bb401f61d",
    "9d191bce-651d-4746-be2d-7ef8ecadb9c2",
    "a0068077-79f4-461a-adfe-75c1a4148545",
    "a1e91b78-d3d8-4675-bb8d-62741b4b68a6",
    "b816bfce-3d80-4913-a07d-69b752ce6377",
    "cabe07ed-9eca-40ea-8ead-410ef5e83f91",
    "3cef3a44-215e-4aed-8e3b-b1e3f08063b7",
    "840bfca7-4f7b-481a-8794-c560c340185d",
    "e1fc63a2-da7a-432f-be78-7c4a95598703",
    "c365c1c7-a3db-4d5e-a9a1-66f56eae7865",
    "b4cc024b-3f5e-480e-b96a-6656493255b5",
    "05407167-39ec-4d3a-a234-73a9120c325d",
    "17b5a6a3-bc87-42e8-b0fb-6ab0781ef2cc",
    "2dfc4c37-fec1-4518-84a7-10095d30ad75",
    "56137764-b4e0-45b8-9c52-1866420c3df5",
    "6b078778-0b90-464d-83f6-59511c811b01",
    "7619a514-5fa8-43ef-9143-83b66a43d7a4",
    "7b5377b0-3f38-4103-8ad2-90fe89864c04",
    "7dd30055-0198-452e-8c25-f73dbe27dcb8",
    "a56f1527-3abf-41d6-91f8-7296d6336c3f",
    "ed58682d-bc52-4baa-9eb0-4eb81e1edacc",
    "edd4d4f2-1a58-45c4-b038-67337af4e029",
    "2a649bb1-795f-4a01-b3be-9a01868dae73",
    "71345b0a-9c7d-4b50-b2bf-937ec5879845",
    "d1af70ea-a9a4-421a-b9cc-94b5e02f1788",
    "e29834fd-413a-455c-a33e-c3915b07401c",
    "f3917a3d-1d17-4ee2-90c5-683b072218fe",
    "f46b4380-207e-4434-820b-f32ce04ae2a4",
    "04a04a9b-226c-43fd-b319-d5e89743676f",
    "08f3a05f-5947-4089-a4c4-d4bcfaa6b7a0",
    "cca70ce6-1952-45d2-acd4-80c903b0bc49",
    "d700d50d-c707-4dca-90dc-4528cddd0c80",
    "08cae58d-4084-4616-b6dd-dd6534e4825b",
    "e8cb5b03-41e0-4086-99e5-f6806cd97211",
    "0512426f-4d28-49f0-be77-06d05daec096",
    "676e5e31-a554-4acc-9286-b60d90a92d26",
    "851e570a-e3de-4d84-bcfa-cc85578baa59",
    "da52d699-e8d2-4dc5-9191-a2199e0b6a9b",
    "de9887f5-ead8-4727-876f-5a4078f8598c",
    "5b2a14e8-6e59-479c-80e3-4696e8980152",
    "0bdb7c40-671d-4ad1-9ce3-986b159c0ddc",
    "ebbc1f13-d24d-40df-9068-adcf735b4240",

    "9e1fc53b-46ff-49a1-9d05-9e6faac34cc5",
    "a0c07678-e491-4bbc-8f0b-07405144218f",
    "0383a3ee-47a7-41a4-b493-519bdefe0488",
    "23dd907f-1261-4488-b21c-e9185af91d5e",
    "7d4a7d1d-cac6-44a8-96e8-ea9584a70825",
    "dc22a632-937f-4e6a-b72f-ba0ff3f5ff97",
    "e142056d-56ab-4352-b091-b56054bd1359",
    "d0633230-7067-47a9-9dbf-ee11e0a2cdd6",
    "2b3ef98c-cc05-450b-a719-711aee40ac65",
    "db4fd70a-2d37-40ea-873f-9433dc5e301f",
    "0a3cd321-3e76-4622-911b-0fda2e5d6b1a",
    "023e9d44-96ae-4eed-b912-244ee8c3b994",
    "c61d22de-5f6c-4958-a7f6-5e9707bd3466",
    "20194330-9976-4043-8632-f8485c6c71b2",
    "48eb8242-1099-4c26-95d4-ef22b002457a",
    "853c8244-429e-46ca-89f2-addf40dfb2bd",
    "b2c257e0-3ad7-4f05-b8e3-d9da973be36e",
    "1dcc160f-c187-48c2-b68e-319bd4354f3d",
    "114d5fd0-e2ae-4b6d-a65a-870da2d19c08",
    "e2d69698-bc99-4e85-9880-67eaccd66e6c",
    "f2feb6a4-363c-4c09-a804-0db564eafd68",
    "8131e2c0-0083-4265-9ce7-78c2d568425d",
    "872bfbb1-9ccf-49f6-8c5f-aa22818ccd66",
    "8d46b8d6-b38a-47ff-ac74-cda14cf2d19b",
    "ad2b4d70-9314-4fe6-bfbe-894a45f6055f",
    "c3a79cfe-8206-451f-aca8-3fec8ebe51d3",
    "3da89939-209c-4086-8520-7eb734e6b4ef",
    "9b54f9d9-35ee-4a14-b62f-d130ea00317f",
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
    "50f58759-7bd6-406f-9b0d-5692beb2a926",
    "5f982798-16b9-4051-ab57-cfc7ebdb2a91",
    "72c06643-a2fa-4186-aa5c-9ec33ae9b445",
    "983bba7c-c092-455f-b6c9-7857003d48fc",
    "bec74516-02fc-48dc-b202-55e78d0e17cf",
    "c526d8d6-5987-4da9-b24c-83466fa172f3"
]


def main(task_id: str, 
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
            
            task_info = get_task_from_gaia(task_id, split)
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
            
            is_correct = question_scorer(answer, task_info["true_answer"])
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
        logger.error(f"Error in main task execution for {task_id}: {e}")
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
    logger.info("Starting EvolAgent main execution")
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
            future = executor.submit(main, task_id, "validation")
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