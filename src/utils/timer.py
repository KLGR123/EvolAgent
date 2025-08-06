import time
import logging
from typing import Optional, Callable
from functools import wraps

from .logger import get_logger


def timer(logger: Optional[logging.Logger] = None) -> Callable:
    """
    Decorator to log function execution time.
    
    Args:
        logger: Logger instance, defaults to function's module logger if not provided
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func_logger = logger or get_logger(func.__module__)
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            func_logger.debug(
                f"Function {func.__name__} completed successfully in {execution_time:.2f}s"
            )
            return result         
        return wrapper
    return decorator