"""
Task Logger for EvolAgent

Provides real-time logging of node activities organized by task_id and model.
Creates readable logs in markdown format for easy inspection.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from ..config import config


class TaskLogger:
    """
    Manages real-time logging for a specific task and model combination.
    
    Directory structure: logs/log_{task_id}/{model_name}/
    """
    
    def __init__(self, task_id: str, model: str):
        self.task_id = task_id
        self.model = model
        self.model_safe = model.replace(":", "_").replace("/", "_")  # Safe filename
        
        # Handle duplicate model names by adding suffix
        base_log_dir = Path(f"logs/log_{task_id}")
        model_dir_name = self._get_unique_model_dir_name(base_log_dir, self.model_safe)
        
        # Create directory structure
        self.base_dir = base_log_dir / model_dir_name
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Track developer plan iterations
        self.developer_plan_count = 0
        
        # Initialize timestamp
        self.start_time = datetime.now()
    
    def _get_unique_model_dir_name(self, base_log_dir: Path, model_safe: str) -> str:
        """
        Get a unique directory name for the model, adding suffix if needed.
        
        Args:
            base_log_dir: Base log directory path
            model_safe: Safe model name for directory
            
        Returns:
            Unique directory name (e.g., "o4-mini", "o4-mini_2", "o4-mini_3")
        """
        original_name = model_safe
        counter = 2  # Start from 2 since first instance has no suffix
        
        # Check if directory already exists
        while (base_log_dir / model_safe).exists():
            model_safe = f"{original_name}_{counter}"
            counter += 1
        
        return model_safe
    
    def get_base_dir(self) -> Path:
        """Get the base directory path for this logger."""
        return self.base_dir
    
    def _write_markdown(self, filename: str, content: str) -> None:
        """Write content to a markdown file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing log file {filepath}: {e}")
    
    def _write_json(self, filename: str, data: Dict[str, Any]) -> None:
        """Write data to a JSON file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing JSON log file {filepath}: {e}")
    
    def log_planner_start(self, task: str, episodic_examples: str = "") -> None:
        """
        Log planner initialization with task and episodic examples.
        
        Args:
            task: The task description
            episodic_examples: Episodic memory examples retrieved
        """
        content = f"""# Planner Log - {self.model}

**Task ID:** {self.task_id}  
**Model:** {self.model}  
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Task Description
```
{task}
```

## Episodic Memory Examples Retrieved
```
{episodic_examples if episodic_examples else 'No episodic examples retrieved'}
```

## Planning History
*(This section will be updated as planning progresses)*

"""
        self._write_markdown("planner.md", content)
    
    def log_planner_history(self, history: str) -> None:
        """
        Update planner log with current history.
        
        Args:
            history: Current planner history
        """
        # Read existing content and update history section
        filepath = self.base_dir / "planner.md"
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the history section
                history_section = f"""## Planning History
```
{history}
```

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                # Find and replace the history section
                if "## Planning History" in content:
                    lines = content.split('\n')
                    new_lines = []
                    skip_section = False
                    
                    for line in lines:
                        if line.startswith("## Planning History"):
                            skip_section = True
                            new_lines.append(history_section)
                            break
                        elif not skip_section:
                            new_lines.append(line)
                    
                    content = '\n'.join(new_lines)
                else:
                    content += history_section
                
                self._write_markdown("planner.md", content)
        except Exception as e:
            print(f"Error updating planner history log: {e}")
    
    def log_developer_plan(self, plan: str, plan_description: str = "", episodic_examples: str = "") -> int:
        """
        Log a new developer plan and return the plan index.
        
        Args:
            plan: The plan content
            plan_description: Optional plan description
            episodic_examples: Optional episodic memory examples
            
        Returns:
            Plan index for this iteration
        """
        self.developer_plan_count += 1
        plan_index = self.developer_plan_count
        
        content = f"""# Developer Plan #{plan_index} - {self.model}

**Task ID:** {self.task_id}  
**Model:** {self.model}  
**Plan Index:** {plan_index}  
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Plan Content
```
{plan}
```

## Plan Description
```
{plan_description if plan_description else 'No description provided'}
```

## Retrieved Episodic Memory Examples
```
{episodic_examples if episodic_examples else 'No Episodic Memory Examples Retrieved'}
```

## Development History
*(This section will be updated as development progresses)*

"""
        filename = f"developer_plan_{plan_index:02d}.md"
        self._write_markdown(filename, content)
        return plan_index
    
    def log_developer_history(self, plan_index: int, history: str) -> None:
        """
        Update developer log with history for a specific plan.
        
        Args:
            plan_index: The plan iteration index
            history: Developer history for this plan
        """
        filename = f"developer_plan_{plan_index:02d}.md"
        filepath = self.base_dir / filename
        
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the history section
                history_section = f"""## Development History
```
{history}
```

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                # Find and replace the history section
                if "## Development History" in content:
                    lines = content.split('\n')
                    new_lines = []
                    skip_section = False
                    
                    for line in lines:
                        if line.startswith("## Development History"):
                            skip_section = True
                            new_lines.append(history_section)
                            break
                        elif not skip_section:
                            new_lines.append(line)
                    
                    content = '\n'.join(new_lines)
                else:
                    content += history_section
                
                self._write_markdown(filename, content)
        except Exception as e:
            print(f"Error updating developer history log for plan {plan_index}: {e}")
    
    def log_critic_result(self, final_answer: str, reason: str, best_model_index: int) -> None:
        """
        Log critic final decision and reasoning.
        
        Args:
            final_answer: The final answer chosen by critic
            reason: Critic's reasoning for the choice
            best_model_index: Index of the best model chosen
        """
        content = f"""# Critic Result - {self.model}

**Task ID:** {self.task_id}  
**Critic Model:** {self.model}  
**Best Model Index:** {best_model_index}  
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Final Answer
```
{final_answer}
```

## Reasoning
```
{reason}
```

## Summary
- **Task completed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total execution time:** {(datetime.now() - self.start_time).total_seconds():.2f} seconds
- **Selected best model index:** {best_model_index}
"""
        
        # Save critic files to task root directory instead of model subdirectory
        task_dir = Path(f"logs/log_{self.task_id}")
        task_dir.mkdir(parents=True, exist_ok=True)
        
        # Write markdown to task root directory
        try:
            critic_md_path = task_dir / "critic.md"
            with open(critic_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing critic markdown file {critic_md_path}: {e}")
        
        # Also save as JSON for programmatic access
        critic_data = {
            "task_id": self.task_id,
            "critic_model": self.model,
            "final_answer": final_answer,
            "reason": reason,
            "best_model_index": best_model_index,
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": (datetime.now() - self.start_time).total_seconds()
        }
        
        # Write JSON to task root directory
        try:
            critic_json_path = task_dir / "critic.json"
            with open(critic_json_path, 'w', encoding='utf-8') as f:
                json.dump(critic_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing critic JSON file {critic_json_path}: {e}")
    
    def log_task_summary(self, task: str, models: List[str], total_plans: int) -> None:
        """
        Create a task summary file with overview information.
        
        Args:
            task: Original task description
            models: List of models used
            total_plans: Total number of plans generated
        """
        content = f"""# Task Summary - {self.task_id}

**Task ID:** {self.task_id}  
**Start Time:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}  
**End Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Duration:** {(datetime.now() - self.start_time).total_seconds():.2f} seconds

## Task Description
```
{task}
```

## Models Used
{chr(10).join(f'- {model}' for model in models)}

## Execution Statistics
- **Total models:** {len(models)}
- **Total plans generated:** {total_plans}
- **Log files created:** {len(list(self.base_dir.glob('*.md')))}

## Log Files
{chr(10).join(f'- {f.name}' for f in sorted(self.base_dir.glob('*.md')))}
"""
        # Save in parent directory for task-level overview
        parent_dir = self.base_dir.parent
        summary_path = parent_dir / "task_summary.md"
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing task summary: {e}")


class TaskLoggerManager:
    """
    Manages TaskLogger instances for different task_id and model combinations.
    """
    
    def __init__(self):
        self.loggers: Dict[str, TaskLogger] = {}  # Use single dict with composite key
        self.model_counters: Dict[str, Dict[str, int]] = {}  # Track model usage per task
    
    def get_logger(self, task_id: str, model: str, model_index: Optional[int] = None) -> TaskLogger:
        """
        Get or create a TaskLogger for the specified task_id and model.
        
        Args:
            task_id: Task identifier
            model: Model name
            model_index: Optional model index for duplicate models
            
        Returns:
            TaskLogger instance
        """
        # Initialize counters for this task if needed
        if task_id not in self.model_counters:
            self.model_counters[task_id] = {}
        
        # Generate unique key based on task_id, model, and occurrence index
        if model_index is not None:
            # Use provided index (from pipeline)
            unique_key = f"{task_id}_{model}_{model_index}"
        else:
            # Auto-increment counter for this model in this task
            if model not in self.model_counters[task_id]:
                self.model_counters[task_id][model] = 0
            else:
                self.model_counters[task_id][model] += 1
            
            unique_key = f"{task_id}_{model}_{self.model_counters[task_id][model]}"
        
        # Create logger if it doesn't exist
        if unique_key not in self.loggers:
            self.loggers[unique_key] = TaskLogger(task_id, model)
        
        return self.loggers[unique_key]
    
    def cleanup_task(self, task_id: str) -> None:
        """
        Clean up loggers for a completed task.
        
        Args:
            task_id: Task identifier to clean up
        """
        # Remove all loggers for this task
        keys_to_remove = [key for key in self.loggers.keys() if key.startswith(f"{task_id}_")]
        for key in keys_to_remove:
            del self.loggers[key]
        
        # Clean up counters
        if task_id in self.model_counters:
            del self.model_counters[task_id]


# Global logger manager instance
task_logger_manager = TaskLoggerManager()


def get_task_logger(task_id: str, model: str, model_index: Optional[int] = None) -> TaskLogger:
    """
    Convenient function to get a task logger.
    
    Args:
        task_id: Task identifier
        model: Model name
        model_index: Optional model index for duplicate models
        
    Returns:
        TaskLogger instance
    """
    return task_logger_manager.get_logger(task_id, model, model_index) 