"""
Refactored logging system for EvolAgent.

This module provides a simplified, efficient logging system with HTML and markdown
output capabilities while maintaining the same output structure and functionality.
"""

import json
import html
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from .config import config


class LoggerManager:
    """
    Centralized logger manager with singleton pattern.
    Handles both file and console logging with configuration-based setup.
    """
    
    _loggers = {}
    _configured = False
    
    @classmethod
    def setup_logging(cls) -> None:
        """Setup logging configuration based on config settings."""
        if cls._configured:
            return
        
        # Create log directory
        log_file_path = Path(config.get('logging.file_path', 'logs/agent.log'))
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, config.get('logging.level', 'INFO').upper()))
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Setup formatter
        formatter = logging.Formatter(
            config.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=config.get('logging.max_file_size', 10485760),
            backupCount=config.get('logging.backup_count', 5),
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, config.get('logging.level', 'INFO').upper()))
        root_logger.addHandler(file_handler)
        
        # Console handler if enabled
        if config.get('logging.console_output', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(getattr(logging, config.get('logging.level', 'INFO').upper()))
            root_logger.addHandler(console_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger with the specified name."""
        if not cls._configured:
            cls.setup_logging()
        
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger
        
        return cls._loggers[name]


class BaseTaskLogger:
    """
    Base class for task-specific logging with common functionality.
    Handles directory creation, file operations, and model naming.
    """
    
    def __init__(self, task_id: str, model: str, base_dir: Optional[Path] = None):
        self.task_id = task_id
        self.model = model
        self.model_safe = self._sanitize_model_name(model)
        
        # Setup directory structure
        if base_dir is not None:
            self.base_dir = base_dir
        else:
            base_log_dir = Path(f"logs/log_{task_id}")
            model_dir_name = self._get_unique_model_dir_name(base_log_dir, self.model_safe)
            self.base_dir = base_log_dir / model_dir_name
            
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tracking variables
        self.developer_plan_count = 0
        self.start_time = datetime.now()
    
    def _sanitize_model_name(self, model: str) -> str:
        """Convert model name to filesystem-safe format."""
        return model.replace(":", "_").replace("/", "_").replace(".", "_")
    
    def _get_unique_model_dir_name(self, base_log_dir: Path, model_safe: str) -> str:
        """Generate unique directory name for the model."""
        original_name = model_safe
        counter = 2
        
        while (base_log_dir / model_safe).exists():
            model_safe = f"{original_name}_{counter}"
            counter += 1
        
        return model_safe
    
    def _write_file(self, filename: str, content: str, format_type: str = "text") -> None:
        """Write content to file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing {format_type} file {filename}: {e}")
    
    def _write_json(self, filename: str, data: Dict[str, Any]) -> None:
        """Write JSON data to file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing JSON file {filename}: {e}")
    
    def get_base_dir(self) -> Path:
        """Get the base directory path for this logger."""
        return self.base_dir


class MarkdownTaskLogger(BaseTaskLogger):
    """
    Task logger that outputs structured markdown files.
    Maintains the original output format and file structure.
    """
    
    def log_planner_start(self, task: str, episodic_examples: str = "") -> None:
        """Log the start of planning phase."""
        content = f"""# Planner Initialization

## Task
{task}

## Episodic Examples
{episodic_examples if episodic_examples else "No episodic examples available."}

## Start Time
{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        self._write_file("planner_init.md", content, "markdown")
    
    def log_planner_history(self, history: str) -> None:
        """Log planner execution history."""
        content = f"""# Planner History

## Execution History
```
{history}
```

## Updated Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self._write_file("planner_history.md", content, "markdown")
    
    def log_developer_plan(self, plan: str, plan_description: str = "", episodic_examples: str = "") -> int:
        """Log developer plan and return plan index."""
        self.developer_plan_count += 1
        
        content = f"""# Developer Plan {self.developer_plan_count:02d}

## Plan
{plan}

## Description
{plan_description if plan_description else "No description provided."}

## Episodic Examples
{episodic_examples if episodic_examples else "No episodic examples available."}

## Created Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        filename = f"developer_plan_{self.developer_plan_count:02d}.md"
        self._write_file(filename, content, "markdown")
        return self.developer_plan_count
    
    def log_developer_history(self, plan_index: int, history: str) -> None:
        """Log developer execution history."""
        content = f"""# Developer History - Plan {plan_index:02d}

## Execution History
```
{history}
```

## Updated Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        filename = f"developer_history_{plan_index:02d}.md"
        self._write_file(filename, content, "markdown")
    
    def log_critic_result(self, final_answer: str, reason: str, best_model_index: int) -> None:
        """Log critic evaluation results."""
        content = f"""# Critic Evaluation Result

## Final Answer
{final_answer}

## Reasoning
{reason}

## Best Model Index
{best_model_index}

## Evaluation Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self._write_file("critic.md", content, "markdown")
        
        # Also save as JSON for programmatic access
        critic_data = {
            "final_answer": final_answer,
            "reason": reason,
            "best_model_index": best_model_index,
            "evaluation_time": datetime.now().isoformat()
        }
        self._write_json("critic.json", critic_data)


class HTMLTaskLogger(BaseTaskLogger):
    """
    Task logger that outputs rich HTML files with syntax highlighting.
    Provides enhanced visualization while maintaining compatibility.
    """
    
    def __init__(self, task_id: str, model: str, base_dir: Optional[Path] = None, model_index: Optional[int] = None):
        super().__init__(task_id, model, base_dir)
        self.conversations = []
        self.model_index = model_index
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return html.escape(text)
    
    def _highlight_python_code(self, code: str) -> str:
        """Apply basic Python syntax highlighting."""
        if not code.strip():
            return code
            
        # Simple syntax highlighting (can be enhanced with pygments if needed)
        highlighted = self._escape_html(code)
        
        # Highlight keywords
        keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'return', 'print']
        for keyword in keywords:
            highlighted = highlighted.replace(
                f' {keyword} ', 
                f' <span class="keyword">{keyword}</span> '
            )
            highlighted = highlighted.replace(
                f'\n{keyword} ', 
                f'\n<span class="keyword">{keyword}</span> '
            )
        
        return highlighted
    
    def _format_code_output(self, output: str) -> str:
        """Format code execution output for display."""
        if not output.strip():
            return "No output"
        
        # Escape HTML and preserve formatting
        formatted = self._escape_html(output)
        
        # Highlight error messages
        if "Error" in formatted or "Exception" in formatted:
            formatted = f'<span class="error">{formatted}</span>'
        
        return formatted
    
    def _get_html_template(self) -> str:
        """Get the HTML template with embedded CSS."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EvolAgent Task Log - {task_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .conversation {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .role-header {{
            padding: 15px 20px;
            font-weight: bold;
            color: white;
        }}
        .planner {{ background-color: #28a745; }}
        .developer {{ background-color: #007bff; }}
        .tester {{ background-color: #ffc107; color: #333; }}
        .critic {{ background-color: #dc3545; }}
        .content {{
            padding: 20px;
        }}
        .code {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .keyword {{ color: #0000ff; font-weight: bold; }}
        .error {{ color: #dc3545; font-weight: bold; }}
        .output {{
            background-color: #f1f3f4;
            border-left: 4px solid #28a745;
            padding: 10px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>EvolAgent Task Execution Log</h1>
        <p>Task ID: {task_id} | Model: {model} | Started: {start_time}</p>
    </div>
    
    <div class="conversations">
        {conversations}
    </div>
</body>
</html>"""
    
    def add_conversation(self, role: str, title: str, content: str, 
                        code: str = None, code_output: str = None, 
                        metadata: Dict[str, Any] = None) -> None:
        """Add a conversation entry to the log."""
        conversation = {
            "role": role,
            "title": title,
            "content": content,
            "code": code,
            "code_output": code_output,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.conversations.append(conversation)
        self._update_html_log()
    
    def _render_conversation(self, conv: Dict[str, Any]) -> str:
        """Render a single conversation entry to HTML."""
        role = conv["role"]
        title = conv["title"]
        content = conv["content"]
        code = conv.get("code", "")
        code_output = conv.get("code_output", "")
        timestamp = conv.get("timestamp", "")
        
        html_content = f"""
        <div class="conversation">
            <div class="role-header {role}">
                {role.title()}: {title}
            </div>
            <div class="content">
                <div>{self._escape_html(content)}</div>
        """
        
        if code:
            html_content += f"""
                <div class="code">
                    {self._highlight_python_code(code)}
                </div>
            """
        
        if code_output:
            html_content += f"""
                <div class="output">
                    {self._format_code_output(code_output)}
                </div>
            """
        
        html_content += f"""
                <div class="timestamp">
                    {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </div>
        """
        
        return html_content
    
    def _update_html_log(self) -> None:
        """Update the HTML log file with current conversations."""
        conversations_html = "\n".join(
            self._render_conversation(conv) for conv in self.conversations
        )
        
        full_html = self._get_html_template().format(
            task_id=self.task_id,
            model=self.model,
            start_time=self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            conversations=conversations_html
        )
        
        self._write_file("task_log.html", full_html, "HTML")
    
    def log_planner_start(self, task: str, episodic_examples: str = "") -> None:
        """Log planner initialization."""
        content = f"Task: {task}\n\nEpisodic Examples:\n{episodic_examples if episodic_examples else 'None'}"
        self.add_conversation("planner", "Initialization", content)
    
    def log_planner_history(self, history: str) -> None:
        """Log planner execution history."""
        self.add_conversation("planner", "Execution History", history)
    
    def log_developer_plan(self, plan: str, plan_description: str = "", episodic_examples: str = "") -> int:
        """Log developer plan."""
        self.developer_plan_count += 1
        content = f"Plan: {plan}\n\nDescription: {plan_description}\n\nEpisodic Examples:\n{episodic_examples if episodic_examples else 'None'}"
        self.add_conversation("developer", f"Plan {self.developer_plan_count:02d}", content)
        return self.developer_plan_count
    
    def log_developer_code_execution(self, plan_index: int, code: str, 
                                   code_output: str, iteration: int = None) -> None:
        """Log developer code execution."""
        title = f"Code Execution - Plan {plan_index:02d}"
        if iteration:
            title += f" (Iteration {iteration})"
        
        self.add_conversation("developer", title, "Code execution result:", code, code_output)
    
    def log_tester_feedback(self, code: str, code_output: str, feedback: str) -> None:
        """Log tester feedback."""
        self.add_conversation("tester", "Code Testing", feedback, code, code_output)
    
    def log_critic_result(self, final_answer: str, reason: str, best_model_index: int) -> None:
        """Log critic evaluation results."""
        content = f"Final Answer: {final_answer}\n\nReasoning: {reason}\n\nBest Model Index: {best_model_index}"
        self.add_conversation("critic", "Final Evaluation", content)
        
        # Save static result
        self.save_critic_result_to_task_root(final_answer, reason, best_model_index)
    
    def save_critic_result_to_task_root(self, final_answer: str, reason: str, best_model_index: int) -> None:
        """Save critic result to task root directory."""
        task_root = self.base_dir.parent
        
        # HTML format
        html_content = f"""<!DOCTYPE html>
<html><head><title>Critic Result</title></head>
<body>
<h1>Critic Evaluation Result</h1>
<h2>Final Answer</h2>
<p>{self._escape_html(final_answer)}</p>
<h2>Reasoning</h2>
<p>{self._escape_html(reason)}</p>
<h2>Best Model Index</h2>
<p>{best_model_index}</p>
</body></html>"""
        
        # JSON format
        json_data = {
            "final_answer": final_answer,
            "reason": reason,
            "best_model_index": best_model_index,
            "evaluation_time": datetime.now().isoformat()
        }
        
        try:
            with open(task_root / "critic.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            with open(task_root / "critic.json", 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving critic result: {e}")
    
    @staticmethod
    def save_critic_result_static(task_id: str, critic_model: str, final_answer: str, 
                                 reason: str, best_model_index: int, start_time: datetime = None) -> None:
        """Static method to save critic results without logger instance."""
        task_root = Path(f"logs/log_{task_id}")
        task_root.mkdir(parents=True, exist_ok=True)
        
        # Create basic HTML
        html_content = f"""<!DOCTYPE html>
<html><head><title>Critic Result - {task_id}</title></head>
<body>
<h1>Critic Evaluation Result</h1>
<p><strong>Task ID:</strong> {task_id}</p>
<p><strong>Critic Model:</strong> {critic_model}</p>
<h2>Final Answer</h2>
<p>{html.escape(final_answer)}</p>
<h2>Reasoning</h2>
<p>{html.escape(reason)}</p>
<h2>Best Model Index</h2>
<p>{best_model_index}</p>
<p><strong>Evaluation Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body></html>"""
        
        # Create JSON data
        json_data = {
            "task_id": task_id,
            "critic_model": critic_model,
            "final_answer": final_answer,
            "reason": reason,
            "best_model_index": best_model_index,
            "evaluation_time": datetime.now().isoformat()
        }
        
        try:
            with open(task_root / "critic.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            with open(task_root / "critic.json", 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving static critic result: {e}")


class LoggerManagerSingleton:
    """
    Singleton manager for task loggers to avoid duplication and manage resources efficiently.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.markdown_loggers = {}
            cls._instance.html_loggers = {}
            cls._instance.model_counters = {}
        return cls._instance
    
    def get_markdown_logger(self, task_id: str, model: str, model_index: Optional[int] = None) -> MarkdownTaskLogger:
        """Get or create a markdown task logger."""
        key = self._generate_logger_key(task_id, model, model_index)
        
        if key not in self.markdown_loggers:
            self.markdown_loggers[key] = MarkdownTaskLogger(task_id, model)
        
        return self.markdown_loggers[key]
    
    def get_html_logger(self, task_id: str, model: str, base_dir: Optional[Path] = None, 
                       model_index: Optional[int] = None) -> HTMLTaskLogger:
        """Get or create an HTML task logger."""
        # Always create new logger if base_dir is provided
        if base_dir is not None:
            return HTMLTaskLogger(task_id, model, base_dir, model_index)
        
        key = self._generate_logger_key(task_id, model, model_index)
        
        if key not in self.html_loggers:
            self.html_loggers[key] = HTMLTaskLogger(task_id, model, None, model_index)
        
        return self.html_loggers[key]
    
    def _generate_logger_key(self, task_id: str, model: str, model_index: Optional[int] = None) -> str:
        """Generate unique key for logger identification."""
        if model_index is not None:
            return f"{task_id}_{model}_{model_index}"
        
        # Auto-increment counter
        if task_id not in self.model_counters:
            self.model_counters[task_id] = {}
        
        if model not in self.model_counters[task_id]:
            self.model_counters[task_id][model] = 0
        else:
            self.model_counters[task_id][model] += 1
        
        return f"{task_id}_{model}_{self.model_counters[task_id][model]}"
    
    def cleanup_task(self, task_id: str) -> None:
        """Clean up loggers for a completed task."""
        # Remove markdown loggers
        keys_to_remove = [key for key in self.markdown_loggers.keys() if key.startswith(f"{task_id}_")]
        for key in keys_to_remove:
            del self.markdown_loggers[key]
        
        # Remove HTML loggers
        keys_to_remove = [key for key in self.html_loggers.keys() if key.startswith(f"{task_id}_")]
        for key in keys_to_remove:
            del self.html_loggers[key]
        
        # Remove counters
        if task_id in self.model_counters:
            del self.model_counters[task_id]


# Global singleton instances
_logger_manager = LoggerManagerSingleton()


# Public API functions for backward compatibility
def get_logger(name: str) -> logging.Logger:
    """Get a standard logger instance."""
    return LoggerManager.get_logger(name)


def get_task_logger(task_id: str, model: str, model_index: Optional[int] = None) -> MarkdownTaskLogger:
    """Get a markdown task logger instance."""
    return _logger_manager.get_markdown_logger(task_id, model, model_index)


def get_html_task_logger(task_id: str, model: str, base_dir: Optional[Path] = None, 
                        model_index: Optional[int] = None) -> HTMLTaskLogger:
    """Get an HTML task logger instance."""
    return _logger_manager.get_html_logger(task_id, model, base_dir, model_index)