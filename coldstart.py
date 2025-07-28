import os
import sys
import time
import signal
import atexit
from typing import Literal
from concurrent.futures import ThreadPoolExecutor, as_completed

from main import TASK_ID_LIST
from src.utils.scorer import question_scorer, check_close_call
from src.utils.loader import get_task_from_coldstart
from src.pipelines import EvolvePipeline
from src.config import config
from src.utils.logger import get_logger, TaskLogger
from src.utils.workspace_manager import cleanup_all_workspaces

# Global flag to prevent multiple cleanup attempts
_cleanup_in_progress = False

TASK_ID_LIST = [
    "codestart_12",    
    "codestart_11",
    "codestart_13",    
    "codestart_1",
    "codestart_2",
    "codestart_3",
    "codestart_4",
    "codestart_5",
    "codestart_6",
    "codestart_7",
    "codestart_8",
    "codestart_9",
    "codestart_10",
]

def main(task_id: str, 
    pipeline: EvolvePipeline, 
    split: Literal["validation", "test"]
) -> dict:
    """
    Run the pipeline for the whole GAIA dataset with enhanced logging.
    """
    with TaskLogger(task_id) as task_logger:
        task_logger.info(f"Starting task execution: {task_id}")
        
        task_info = get_task_from_coldstart(task_id, split)
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


def cleanup_handler(signum=None, frame=None):
    """Handle cleanup on program termination."""
    global _cleanup_in_progress
    
    # Avoid multiple cleanup attempts
    if _cleanup_in_progress:
        return
    
    _cleanup_in_progress = True
    logger = get_logger(__name__)
    logger.info("Received termination signal, cleaning up workspaces...")
    
    try:
        cleanup_all_workspaces()
        logger.info("Cleanup completed, exiting...")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
    finally:
        os._exit(1)  # Force exit


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Starting EvolAgent main execution")
    logger.info(f"Configuration loaded: max_parallel_tasks={config.max_parallel_tasks}")

    # Register cleanup handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, cleanup_handler)  # Termination
    atexit.register(cleanup_all_workspaces)  # Normal exit

    pipeline = EvolvePipeline()
    
    # Use ThreadPoolExecutor for parallel task execution with configured limits
    max_workers = config.max_parallel_tasks
    results = []
    
    logger.info(f"Processing {len(TASK_ID_LIST)} tasks with {max_workers} parallel workers")
    
    executor = None
    try:
        executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Submit all tasks to the executor
        future_to_task_id = {
            executor.submit(main, task_id, pipeline, "validation"): task_id 
            for task_id in TASK_ID_LIST
        }
        
        # Collect results as they complete with timeout for interruption
        for future in as_completed(future_to_task_id, timeout=None):
            task_id = future_to_task_id[future]
            try:
                result = future.result(timeout=1.0)  # Short timeout to allow interruption
                results.append(result)
                logger.info(f"Completed task {task_id}: {result.get('is_correct', 'N/A')}")
            except Exception as exc:
                logger.error(f"Task {task_id} generated an exception: {exc}")
        
        # Summary statistics
        if results:
            total_tasks = len(results)
            correct_tasks = sum(1 for r in results if r.get('is_correct', False))
            success_rate = correct_tasks / total_tasks * 100
            logger.info(f"Final Summary: {correct_tasks}/{total_tasks} tasks completed successfully ({success_rate:.1f}%)")
        
            logger.info("Check Episodic Memories!")
            # pipeline.clear_episodic()
            logger.info("EvolAgent execution completed")
    
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        if executor:
            logger.info("Shutting down executor...")
            executor.shutdown(wait=False)  # Don't wait for completion
        cleanup_all_workspaces()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error during execution: {e}")
        if executor:
            executor.shutdown(wait=False)
        cleanup_all_workspaces()
        raise
    finally:
        # Final cleanup to ensure all temporary workspaces are removed
        if executor:
            try:
                executor.shutdown(wait=True)
            except:
                pass
        cleanup_all_workspaces()
        logger.info("Workspace cleanup completed")