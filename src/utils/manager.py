"""
Workspace Manager.

Provides isolated workspace environments for parallel task execution
by creating separate workspace directories for each task.

Features:
- Isolated workspace for each task
- Thread-safe workspace management
- Context manager for isolated workspace
- Global workspace manager instance
- Convenient context manager for isolated workspace
- Get current workspace path and task ID
"""

import os
import shutil
import threading
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Generator
from .config import config
from ..utils.logger import get_logger


# Thread-local storage for current task workspace
_local = threading.local()

class WorkspaceManager:
    """
    Manages isolated workspace directories for parallel task execution.
    Creates separate workspace directories for each task to avoid conflicts.
    Each task gets its own workspace_{task_id}/ directory.
    """
    
    def __init__(self):
        self.logger = get_logger("workspace")
        self.base_workspace = config.get('environment.workspace_dir', 'workspace')
        self.active_workspaces = {}
        self._lock = threading.Lock()
    
    def _create_task_workspace(self, task_id: str) -> str:
        """
        Create a task-specific workspace directory.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Path to the task workspace directory
        """

        workspace_dir = f"workspace_{task_id}"
        workspace_path = Path(workspace_dir)
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.debug(f"Created task workspace: {workspace_path.absolute()}")
        return str(workspace_path.absolute())
    
    def _cleanup_task_workspace(self, workspace_path: str) -> None:
        """
        Remove task workspace directory and all its contents.
        
        Args:
            workspace_path: Path to task workspace directory
        """
        try:
            if os.path.exists(workspace_path):
                shutil.rmtree(workspace_path)
                self.logger.debug(f"Cleaned up task workspace: {workspace_path}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup task workspace {workspace_path}: {e}")
    
    @contextmanager
    def isolated_workspace(self, task_id: str) -> Generator[str, None, None]:
        """
        Context manager providing isolated workspace for a task.
        
        Creates a task-specific workspace directory and cleans up afterward.
        Fully thread-safe for parallel task execution.
        
        Args:
            task_id: Unique identifier for the task
            
        Yields:
            Path to the isolated workspace directory
        """
        workspace_path = None
        
        try:
            # Create task-specific workspace directory
            workspace_path = self._create_task_workspace(task_id)
            
            # Track active workspace (thread-safe)
            with self._lock:
                self.active_workspaces[task_id] = workspace_path
            
            # Store in thread-local storage for access by interpreter
            _local.task_id = task_id
            _local.workspace_path = workspace_path
            
            self.logger.info(f"Isolated workspace ready for task {task_id}: {workspace_path}")
            yield workspace_path
            
        finally:
            try:
                with self._lock:
                    if task_id in self.active_workspaces:
                        del self.active_workspaces[task_id]
                
                if hasattr(_local, 'task_id'):
                    delattr(_local, 'task_id')
                if hasattr(_local, 'workspace_path'):
                    delattr(_local, 'workspace_path')
                
                if workspace_path:
                    self._cleanup_task_workspace(workspace_path)
                
                self.logger.info(f"Cleaned up isolated workspace for task {task_id}")
                
            except Exception as cleanup_error:
                self.logger.error(f"Error during workspace cleanup for task {task_id}: {cleanup_error}")
    
    def get_current_workspace(self) -> Optional[str]:
        """
        Get the current thread's isolated workspace path.
        
        Returns:
            Path to current workspace or None if not in isolated context
        """
        return getattr(_local, 'workspace_path', None)
    
    def get_current_task_id(self) -> Optional[str]:
        """
        Get the current thread's task ID.
        
        Returns:
            Current task ID or None if not in isolated context
        """
        return getattr(_local, 'task_id', None)
    
    def cleanup_all(self) -> None:
        """
        Emergency cleanup of all active task workspaces.
        Should only be used in case of unexpected shutdown.
        """
        with self._lock:
            self.logger.warning("Performing emergency cleanup of all workspaces")
            
            for task_id, workspace_path in list(self.active_workspaces.items()):
                try:
                    self._cleanup_task_workspace(workspace_path)
                    self.logger.info(f"Emergency cleanup completed for task {task_id}")
                except Exception as e:
                    self.logger.error(f"Emergency cleanup failed for task {task_id}: {e}")
            
            self.active_workspaces.clear()


workspace_manager = WorkspaceManager()   