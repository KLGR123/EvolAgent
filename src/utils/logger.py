import logging
import logging.handlers
from typing import Optional
from pathlib import Path

from ..config import config


class EvolAgentLogger:
    """
    Centralized logger for the EvolAgent system.
    """
    
    _loggers = {}
    _configured = False
    
    @classmethod
    def setup_logging(cls) -> None:
        """Setup logging configuration based on config settings."""
        if cls._configured:
            return
        
        # Create logs directory if it doesn't exist
        log_file_path = Path(config.log_file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, config.log_level.upper()))
        
        # Clear any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(config.log_format)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=config.log_file_path,
            maxBytes=config.log_max_file_size,
            backupCount=config.log_backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, config.log_level.upper()))
        root_logger.addHandler(file_handler)
        
        # Console handler
        if config.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(getattr(logging, config.log_level.upper()))
            root_logger.addHandler(console_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger with the given name.
        
        Args:
            name: Logger name (typically __name__ or module name)
            
        Returns:
            Logger instance
        """
        if not cls._configured:
            cls.setup_logging()
        
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger
        
        return cls._loggers[name]


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return EvolAgentLogger.get_logger(name)


# Context manager for task-specific logging
class TaskLogger:
    """Context manager for task-specific logging with automatic task ID tracking."""
    
    def __init__(self, task_id: str, logger: Optional[logging.Logger] = None):
        self.task_id = task_id
        self.logger = logger or get_logger("task")
        self.original_filter = None
    
    def __enter__(self):
        # Add task ID to log records
        class TaskFilter(logging.Filter):
            def __init__(self, task_id):
                self.task_id = task_id
                super().__init__()
            
            def filter(self, record):
                record.task_id = self.task_id
                return True
        
        self.task_filter = TaskFilter(self.task_id)
        self.logger.addFilter(self.task_filter)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.task_filter:
            self.logger.removeFilter(self.task_filter)


# Performance logging decorator
def log_execution_time(logger: Optional[logging.Logger] = None):
    """
    Decorator to log function execution time.
    
    Args:
        logger: Logger instance (defaults to function's module logger)
    """
    import time
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func_logger = logger or get_logger(func.__module__)
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                func_logger.info(
                    f"Function {func.__name__} completed successfully in {execution_time:.2f}s"
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                func_logger.error(
                    f"Function {func.__name__} failed after {execution_time:.2f}s: {str(e)}"
                )
                raise
                
        return wrapper
    return decorator


# Specialized loggers for different components
class ComponentLoggers:
    """Factory class for component-specific loggers."""
    
    @staticmethod
    def get_pipeline_logger() -> logging.Logger:
        return get_logger("evolagent.pipeline")
    
    @staticmethod
    def get_memory_logger() -> logging.Logger:
        return get_logger("evolagent.memory")
    
    @staticmethod
    def get_node_logger() -> logging.Logger:
        return get_logger("evolagent.node")
    
    @staticmethod
    def get_retriever_logger() -> logging.Logger:
        return get_logger("evolagent.retriever")
    
    @staticmethod
    def get_config_logger() -> logging.Logger:
        return get_logger("evolagent.config")


# Initialize logging on import
EvolAgentLogger.setup_logging()


if __name__ == "__main__":
    # Test logging functionality
    test_logger = get_logger("test")
    test_logger.info("Testing logging system")
    test_logger.debug("Debug message")
    test_logger.warning("Warning message")
    test_logger.error("Error message")
    
    # Test task logger
    with TaskLogger("test_task_123") as task_log:
        task_log.info("Task-specific log message")
    
    print("Logging test completed") 