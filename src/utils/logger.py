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
    
    def log_developer_plan(self, plan: str, plan_description: str = "", semantic_examples: str = "", episodic_examples: str = "") -> int:
        """Log developer plan and return plan index."""
        self.developer_plan_count += 1
        
        content = f"""# Developer Plan {self.developer_plan_count:02d}

## Plan
{plan}

## Description
{plan_description if plan_description else "No description provided."}

{"## Semantic Examples\n"+semantic_examples if semantic_examples else None}

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
        """Apply enhanced Python syntax highlighting."""
        if not code.strip():
            return code
            
        # Enhanced syntax highlighting
        highlighted = self._escape_html(code)
        
        # Highlight Python keywords
        keywords = [
            'def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 
            'try', 'except', 'finally', 'return', 'yield', 'break', 'continue',
            'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False', 'with', 'as',
            'pass', 'lambda', 'global', 'nonlocal', 'raise', 'assert', 'del'
        ]
        
        # Apply keyword highlighting with word boundaries
        import re
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            highlighted = re.sub(pattern, f'<span class="keyword">{keyword}</span>', highlighted)
        
        # Highlight function definitions
        highlighted = re.sub(r'\bdef\s+(\w+)', r'<span class="keyword">def</span> <span class="function">\1</span>', highlighted)
        highlighted = re.sub(r'\bclass\s+(\w+)', r'<span class="keyword">class</span> <span class="function">\1</span>', highlighted)
        
        # Highlight strings
        highlighted = re.sub(r'(["\'])((?:\\.|(?!\1)[^\\])*?)\1', r'<span class="string">\1\2\1</span>', highlighted)
        highlighted = re.sub(r'(["\']){3}(.*?)\1{3}', r'<span class="string">\1\1\1\2\1\1\1</span>', highlighted, flags=re.DOTALL)
        
        # Highlight numbers
        highlighted = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="number">\1</span>', highlighted)
        
        # Highlight comments
        highlighted = re.sub(r'(#.*?)(?=\n|$)', r'<span class="comment">\1</span>', highlighted)
        
        return highlighted
    
    def _format_code_output(self, output: str) -> str:
        """Format code execution output for display."""
        if not output.strip():
            return '<span class="output-empty">No output</span>'
        
        # Escape HTML and preserve formatting
        formatted = self._escape_html(output)
        
        return formatted
    
    def _detect_output_type(self, output: str) -> str:
        """Detect the type of output to apply appropriate styling."""
        if not output.strip():
            return "output-empty"
        
        output_lower = output.lower()
        if any(error in output_lower for error in ['error', 'exception', 'traceback', 'failed']):
            return "output-error"
        elif any(warning in output_lower for warning in ['warning', 'warn', 'deprecated']):
            return "output-warning"
        elif any(success in output_lower for success in ['success', 'completed', 'passed', 'ok']):
            return "output-success"
        else:
            return ""
    
    def _format_content_text(self, content: str) -> str:
        """Format content text with proper paragraphs and line breaks."""
        if not content:
            return ""
        
        # Escape HTML first
        escaped = self._escape_html(content)
        
        # Split into paragraphs and format
        paragraphs = escaped.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Replace single line breaks with <br> within paragraphs
                formatted_para = para.replace('\n', '<br>')
                formatted_paragraphs.append(f'<p>{formatted_para}</p>')
        
        return '\n'.join(formatted_paragraphs)
    
    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata dictionary for display."""
        if not metadata:
            return ""
        
        formatted_items = []
        for key, value in metadata.items():
            escaped_key = self._escape_html(str(key))
            escaped_value = self._escape_html(str(value))
            formatted_items.append(f'<strong>{escaped_key}:</strong> {escaped_value}')
        
        return '<br>'.join(formatted_items)
    
    def _get_html_template(self) -> str:
        """Get the HTML template with embedded CSS."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EvolAgent Task Log - {task_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f7fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e1e8ed;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
            color: #1a73e8;
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
            color: #5f6368;
        }}
        
        .conversation {{
            background: white;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        .conversation-header {{
            padding: 20px 25px;
            border-bottom: 1px solid #e1e8ed;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .role-badge {{
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .role-planner {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .role-developer {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}
        
        .role-tester {{
            background: #e8f5e8;
            color: #388e3c;
        }}
        
        .role-critic {{
            background: #fff3e0;
            color: #f57c00;
        }}
        
        .conversation-title {{
            font-size: 1.1em;
            font-weight: 500;
            color: #333;
        }}
        
        .timestamp {{
            color: #657786;
            font-size: 0.85em;
        }}
        
        .conversation-content {{
            padding: 25px;
        }}
        
        .content-text {{
            margin-bottom: 20px;
            line-height: 1.7;
            color: #333;
        }}
        
        .content-text p {{
            margin-bottom: 12px;
        }}
        
        .code-block {{
            background: #1e1e1e;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            overflow-x: auto;
            position: relative;
        }}
        
        .code-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }}
        
        .code-label {{
            color: #ffd700;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .code-lang {{
            color: #888;
            font-size: 0.8em;
        }}
        
        .code-content {{
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
            color: #f8f8f2;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        
        .keyword {{
            color: #ff79c6;
            font-weight: bold;
        }}
        
        .string {{
            color: #f1fa8c;
        }}
        
        .comment {{
            color: #6272a4;
            font-style: italic;
        }}
        
        .number {{
            color: #bd93f9;
        }}
        
        .function {{
            color: #50fa7b;
        }}
        
        .output-section {{
            margin: 20px 0;
        }}
        
        .output-header {{
            background: #f8f9fa;
            padding: 12px 18px;
            border-left: 4px solid #007bff;
            font-weight: 600;
            color: #495057;
            margin-bottom: 0;
            border-radius: 4px 4px 0 0;
            border: 1px solid #dee2e6;
            border-bottom: none;
        }}
        
        .output-content {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-top: none;
            border-radius: 0 0 4px 4px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            line-height: 1.4;
            white-space: pre-wrap;
            word-break: break-word;
            color: #495057;
        }}
        
        .output-success {{
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }}
        
        .output-success .output-header {{
            background-color: #d4edda;
            border-left-color: #28a745;
            border-color: #c3e6cb;
        }}
        
        .output-error {{
            color: #721c24;
            background-color: #f8d7da;
            border-color: #f5c6cb;
        }}
        
        .output-error .output-header {{
            background-color: #f8d7da;
            border-left-color: #dc3545;
            border-color: #f5c6cb;
        }}
        
        .output-warning {{
            color: #856404;
            background-color: #fff3cd;
            border-color: #ffeaa7;
        }}
        
        .output-warning .output-header {{
            background-color: #fff3cd;
            border-left-color: #ffc107;
            border-color: #ffeaa7;
        }}
        
        .output-empty {{
            color: #6c757d;
            font-style: italic;
        }}
        
        .metadata {{
            background: #f1f3f4;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 0.9em;
            border-left: 3px solid #4285f4;
        }}
        
        .metadata-title {{
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        
        .metadata-content {{
            color: #5f6368;
        }}
        
        .scroll-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .scroll-to-top:hover {{
            background: #1557b0;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .conversation-content {{
                padding: 15px;
            }}
            
            .conversation-header {{
                padding: 15px;
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 EvolAgent Task Execution Log</h1>
            <div class="meta">
                <strong>Task ID:</strong> {task_id} | 
                <strong>Model:</strong> {model} | 
                <strong>Started:</strong> {start_time}
            </div>
        </div>
        
        <div class="conversations">
            {conversations}
        </div>
        
        <button class="scroll-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑</button>
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
        metadata = conv.get("metadata", {})
        
        # Format timestamp
        try:
            formatted_timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_timestamp = timestamp or "Unknown time"
        
        # Format content with proper line breaks and paragraphs
        formatted_content = self._format_content_text(content)
        
        html_content = f"""
        <div class="conversation">
            <div class="conversation-header">
                <div>
                    <span class="role-badge role-{role}">{role}</span>
                    <span class="conversation-title">{self._escape_html(title)}</span>
                </div>
                <div class="timestamp">{formatted_timestamp}</div>
            </div>
            <div class="conversation-content">
                <div class="content-text">{formatted_content}</div>
        """
        
        if code:
            html_content += f"""
                <div class="code-block">
                    <div class="code-header">
                        <span class="code-label">📝 Code</span>
                        <span class="code-lang">Python</span>
                    </div>
                    <div class="code-content">{self._highlight_python_code(code)}</div>
                </div>
            """
        
        if code_output:
            output_type = self._detect_output_type(code_output)
            html_content += f"""
                <div class="output-section {output_type}">
                    <div class="output-header">📄 Output</div>
                    <div class="output-content">{self._format_code_output(code_output)}</div>
                </div>
            """
        
        if metadata:
            html_content += f"""
                <div class="metadata">
                    <div class="metadata-title">📊 Metadata</div>
                    <div class="metadata-content">{self._format_metadata(metadata)}</div>
                </div>
            """
        
        html_content += """
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
    
    def log_developer_plan(self, plan: str, plan_description: str = "", semantic_examples: str = "", episodic_examples: str = "") -> int:
        """Log developer plan."""
        self.developer_plan_count += 1
        content = f"Plan: {plan}\n\nDescription: {plan_description}\n\nSemantic Examples:\n{semantic_examples if semantic_examples else 'None'}\n\nEpisodic Examples:\n{episodic_examples if episodic_examples else 'None'}"
        self.add_conversation("developer", f"Plan {self.developer_plan_count:02d}", content)
        return self.developer_plan_count
    
    def log_developer_code_execution(self, plan_index: int, code: str, 
                                   code_output: str, iteration: int = None) -> None:
        """Log developer code execution."""
        title = f"Code Execution - Plan {plan_index:02d}"
        if iteration:
            title += f" (Iteration {iteration})"
        
        self.add_conversation("developer", title, "Code execution result:", code, code_output)
    
    def log_developer_history(self, plan_index: int, history: str) -> None:
        """Log developer execution history."""
        title = f"Developer History - Plan {plan_index:02d}"
        self.add_conversation("developer", title, history)
    
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
        
        # Use the same modern HTML template as the static method
        # Extract task_id from path
        task_id = task_root.name.replace("log_", "")
        
        # Use the static method to ensure consistency
        HTMLTaskLogger.save_critic_result_static(
            task_id=task_id,
            critic_model=self.model,
            final_answer=final_answer,
            reason=reason,
            best_model_index=best_model_index
        )
    
    @staticmethod
    def save_critic_result_static(task_id: str, critic_model: str, final_answer: str, 
                                 reason: str, best_model_index: int, true_answer: str = None, 
                                 start_time: datetime = None) -> None:
        """Static method to save critic results without logger instance."""
        task_root = Path(f"logs/log_{task_id}")
        task_root.mkdir(parents=True, exist_ok=True)
        
        # Create modern HTML with beautiful styling
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Critic Evaluation Result - {task_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
            animation: slideUp 0.6s ease-out;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .header {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
        }}
        
        .header::before {{
            content: '🎯';
            font-size: 4em;
            display: block;
            margin-bottom: 10px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .meta-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .meta-card .label {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .meta-card .value {{
            font-size: 1.1em;
            color: #333;
            font-weight: 500;
        }}
        
        .section {{
            margin-bottom: 35px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .section-icon {{
            font-size: 1.5em;
            margin-right: 12px;
        }}
        
        .section-title {{
            font-size: 1.4em;
            font-weight: 600;
            color: #333;
        }}
        
        .answer-box {{
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .answer-text {{
            font-size: 2em;
            font-weight: bold;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .reasoning-box {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 25px;
            line-height: 1.8;
            color: #495057;
        }}
        
        .best-model {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
        }}
        
        .best-model .index {{
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 5px;
        }}
        
        .best-model .label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .footer {{
            background: #f1f3f4;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        .timestamp {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 15px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 30px 20px;
            }}
            
            .meta-info {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            
            .footer {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Critic Evaluation Result</h1>
            <div class="subtitle">AI Agent Performance Assessment</div>
        </div>
        
        <div class="content">
            <div class="meta-info">
                <div class="meta-card">
                    <div class="label">Task ID</div>
                    <div class="value">{html.escape(task_id)}</div>
                </div>
                <div class="meta-card">
                    <div class="label">Critic Model</div>
                    <div class="value">{html.escape(critic_model)}</div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="section-icon">🎯</span>
                    <span class="section-title">Final Answer</span>
                </div>
                <div class="answer-box">
                    <div class="answer-text">{html.escape(final_answer)}</div>
                </div>
            </div>
            
            {f'''<div class="section">
                <div class="section-header">
                    <span class="section-icon">✅</span>
                    <span class="section-title">True Answer</span>
                </div>
                <div class="answer-box" style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);">
                    <div class="answer-text">{html.escape(true_answer)}</div>
                </div>
            </div>''' if true_answer is not None else ''}
            
            <div class="section">
                <div class="section-header">
                    <span class="section-icon">🤔</span>
                    <span class="section-title">Reasoning</span>
                </div>
                <div class="reasoning-box">
                    {html.escape(reason)}
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="section-icon">🏆</span>
                    <span class="section-title">Best Model Selection</span>
                </div>
                <div class="best-model">
                    <div class="index">#{best_model_index}</div>
                    <div class="label">Selected Model Index</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="timestamp">
                <span>⏰</span>
                <span>Evaluation completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        # Create JSON data
        json_data = {
            "task_id": task_id,
            "critic_model": critic_model,
            "final_answer": final_answer,
            "true_answer": true_answer,
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