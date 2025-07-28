"""
HTML Task Logger for EvolAgent

Provides enhanced HTML logging with role-based conversations, 
code highlighting, and formatted output display.
"""

import os
import json
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from ..config import config


class HTMLTaskLogger:
    """
    Manages HTML-based logging for a specific task and model combination.
    
    Features:
    - Role-based conversation display
    - Python code syntax highlighting  
    - Formatted code output display
    - Responsive web design
    
    Directory structure: logs/log_{task_id}/{model_name}/
    """
    
    def __init__(self, task_id: str, model: str, base_dir: Optional[Path] = None):
        self.task_id = task_id
        self.model = model
        self.model_safe = model.replace(":", "_").replace("/", "_")  # Safe filename
        
        if base_dir is not None:
            # Use provided directory (from TaskLogger)
            self.base_dir = base_dir
        else:
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
        
        # Store conversation history for HTML rendering
        self.conversations = []
    
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
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return html.escape(text)
    
    def _highlight_python_code(self, code: str) -> str:
        """Apply basic Python syntax highlighting using CSS classes."""
        # Escape HTML first
        code = self._escape_html(code)
        
        # Basic keyword highlighting (you can extend this)
        keywords = [
            'def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 
            'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'pass',
            'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'None', 
            'True', 'False', 'print', 'len', 'range', 'str', 'int', 'float',
            'list', 'dict', 'tuple', 'set'
        ]
        
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            code = code.replace(f' {keyword} ', f' <span class="keyword">{keyword}</span> ')
            code = code.replace(f'\n{keyword} ', f'\n<span class="keyword">{keyword}</span> ')
            code = code.replace(f'({keyword} ', f'(<span class="keyword">{keyword}</span> ')
            if code.startswith(f'{keyword} '):
                code = f'<span class="keyword">{keyword}</span> ' + code[len(keyword) + 1:]
        
        # Highlight strings (basic implementation)
        # This is a simplified approach - you might want to use a proper syntax highlighter
        lines = code.split('\n')
        highlighted_lines = []
        
        for line in lines:
            # Highlight single quotes
            if "'" in line:
                parts = line.split("'")
                for i in range(1, len(parts), 2):  # Every odd index is inside quotes
                    parts[i] = f'<span class="string">\'{parts[i]}\'</span>'
                    parts[i] = parts[i].replace("'", "")  # Remove extra quotes
                line = "'".join(parts)
            
            # Highlight double quotes
            if '"' in line:
                parts = line.split('"')
                for i in range(1, len(parts), 2):  # Every odd index is inside quotes
                    parts[i] = f'<span class="string">"{parts[i]}"</span>'
                    parts[i] = parts[i].replace('"', "")  # Remove extra quotes
                line = '"'.join(parts)
            
            highlighted_lines.append(line)
        
        return '\n'.join(highlighted_lines)
    
    def _format_code_output(self, output: str) -> str:
        """Format code output with proper styling."""
        if not output.strip():
            return '<div class="output-empty">No output</div>'
        
        escaped_output = self._escape_html(output)
        
        # Check if it looks like an error
        if any(keyword in output.lower() for keyword in ['error', 'exception', 'traceback']):
            return f'<div class="output-error">{escaped_output}</div>'
        
        # Check if it contains warnings
        elif 'warning' in output.lower():
            return f'<div class="output-warning">{escaped_output}</div>'
        
        # Regular output
        return f'<div class="output-success">{escaped_output}</div>'
    
    def _get_html_template(self) -> str:
        """Get the base HTML template with CSS styling."""
        return '''<!DOCTYPE html>
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
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
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
        
        .timestamp {{
            color: #657786;
            font-size: 0.85em;
        }}
        
        .conversation-content {{
            padding: 25px;
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
        
        .output-section {{
            margin: 20px 0;
        }}
        
        .output-header {{
            background: #f8f9fa;
            padding: 12px 18px;
            border-left: 4px solid #007bff;
            font-weight: 600;
            color: #495057;
            margin-bottom: 10px;
            border-radius: 4px 4px 0 0;
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
        }}
        
        .output-success {{
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }}
        
        .output-error {{
            color: #721c24;
            background-color: #f8d7da;
            border-color: #f5c6cb;
        }}
        
        .output-warning {{
            color: #856404;
            background-color: #fff3cd;
            border-color: #ffeaa7;
        }}
        
        .output-empty {{
            color: #6c757d;
            font-style: italic;
        }}
        
        .section {{
            margin: 25px 0;
        }}
        
        .section-title {{
            font-size: 1.4em;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #3498db;
        }}
        
        .text-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #6c5ce7;
            margin: 15px 0;
        }}
        
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #7f8c8d;
            border-top: 1px solid #e1e8ed;
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
                padding: 20px;
            }}
            
            .code-block {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>EvolAgent Task Log</h1>
            <div class="meta">
                <div><strong>Task ID:</strong> {task_id}</div>
                <div><strong>Model:</strong> {model}</div>
                <div><strong>Start Time:</strong> {start_time}</div>
            </div>
        </div>
        
        {content}
        
        <div class="footer">
            <p>Generated by EvolAgent HTML Logger - {generation_time}</p>
        </div>
    </div>
</body>
</html>'''
    
    def _write_html(self, filename: str, content: str) -> None:
        """Write content to an HTML file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing HTML log file {filepath}: {e}")
    
    def _write_json(self, filename: str, data: Dict[str, Any]) -> None:
        """Write data to a JSON file with error handling."""
        try:
            filepath = self.base_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing JSON log file {filepath}: {e}")
    
    def add_conversation(self, role: str, title: str, content: str, 
                        code: str = None, code_output: str = None, 
                        metadata: Dict[str, Any] = None) -> None:
        """Add a conversation entry to the log."""
        conversation = {
            'role': role,
            'title': title,
            'content': content,
            'code': code,
            'code_output': code_output,
            'metadata': metadata or {},
            'timestamp': datetime.now()
        }
        self.conversations.append(conversation)
        self._update_html_log()
    
    def _render_conversation(self, conv: Dict[str, Any]) -> str:
        """Render a single conversation to HTML."""
        role_class = f"role-{conv['role'].lower()}"
        timestamp_str = conv['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        html_parts = []
        html_parts.append(f'''
        <div class="conversation">
            <div class="conversation-header">
                <div class="role-badge {role_class}">{conv['role']}</div>
                <div class="timestamp">{timestamp_str}</div>
            </div>
            <div class="conversation-content">
                <div class="section">
                    <div class="section-title">{self._escape_html(conv['title'])}</div>
        ''')
        
        # Add main content
        if conv['content']:
            html_parts.append(f'''
                    <div class="text-content">
                        {self._escape_html(conv['content']).replace(chr(10), '<br>')}
                    </div>
            ''')
        
        # Add code block if present
        if conv['code']:
            highlighted_code = self._highlight_python_code(conv['code'])
            html_parts.append(f'''
                    <div class="code-block">
                        <div class="code-header">
                            <span class="code-label">Python Code</span>
                            <span class="code-lang">python</span>
                        </div>
                        <div class="code-content">{highlighted_code}</div>
                    </div>
            ''')
        
        # Add code output if present
        if conv['code_output']:
            formatted_output = self._format_code_output(conv['code_output'])
            html_parts.append(f'''
                    <div class="output-section">
                        <div class="output-header">Execution Output</div>
                        <div class="output-content {formatted_output.split('"')[1] if 'class="' in formatted_output else ''}">{formatted_output}</div>
                    </div>
            ''')
        
        html_parts.append('''
                </div>
            </div>
        </div>
        ''')
        
        return ''.join(html_parts)
    
    def _update_html_log(self) -> None:
        """Update the main HTML log file with all conversations."""
        # Render all conversations
        conversations_html = ''.join([
            self._render_conversation(conv) for conv in self.conversations
        ])
        
        # Add summary statistics
        summary_html = f'''
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-value">{len(self.conversations)}</div>
                <div class="stat-label">Conversation Count</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len([c for c in self.conversations if c['code']])}</div>
                <div class="stat-label">Code Block Count</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{(datetime.now() - self.start_time).total_seconds():.1f}s</div>
                <div class="stat-label">Execution Time</div>
            </div>
        </div>
        '''
        
        # Generate complete HTML
        full_html = self._get_html_template().format(
            task_id=self.task_id,
            model=self.model,
            start_time=self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            content=summary_html + conversations_html,
            generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        self._write_html("task_log.html", full_html)
    
    def log_planner_start(self, task: str, episodic_examples: str = "") -> None:
        """Log planner initialization with task and episodic examples."""
        content = f"Task Description:\n{task}\n\n"
        if episodic_examples:
            content += f"Retrieved Episodic Memory Examples:\n{episodic_examples}"
        else:
            content += "No Episodic Memory Examples Retrieved"
        
        self.add_conversation(
            role="planner",
            title="Planner Initialization",
            content=content,
            metadata={
                "task": task,
                "episodic_examples": episodic_examples
            }
        )
    
    def log_planner_history(self, history: str) -> None:
        """Update planner log with current history."""
        # Parse the history string to extract the latest plan
        latest_plan = self._extract_latest_plan(history)
        
        self.add_conversation(
            role="planner", 
            title="Latest Planning Update",
            content=f"Current Plan:\n{latest_plan}" if latest_plan else "No plan available yet"
        )
    
    def _extract_latest_plan(self, history: str) -> str:
        """Extract the latest plan from the history string."""
        if not history.strip():
            return ""
        
        try:
            # Split history by dictionary blocks (each starts with '{' and ends with '}')
            blocks = []
            current_block = []
            brace_count = 0
            
            for line in history.split('\n'):
                line = line.strip()
                if line == '{':
                    if current_block:
                        blocks.append('\n'.join(current_block))
                    current_block = [line]
                    brace_count = 1
                elif line == '}' and brace_count > 0:
                    current_block.append(line)
                    blocks.append('\n'.join(current_block))
                    current_block = []
                    brace_count = 0
                elif brace_count > 0:
                    current_block.append(line)
            
            # Find the last block that contains a plan from planner role
            for block in reversed(blocks):
                if '"role": \'planner\'' in block and '"plan":' in block:
                    # Extract plan content
                    lines = block.split('\n')
                    for line in lines:
                        if '"plan":' in line:
                            # Extract the plan content between quotes
                            plan_part = line.split('"plan":', 1)[1].strip()
                            if plan_part.endswith(','):
                                plan_part = plan_part[:-1]
                            # Remove outer quotes and unescape
                            if plan_part.startswith("'") and plan_part.endswith("'"):
                                plan_content = plan_part[1:-1]
                            elif plan_part.startswith('"') and plan_part.endswith('"'):
                                plan_content = plan_part[1:-1]
                            else:
                                plan_content = plan_part
                            return plan_content.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
            
            return "No plan found in history"
            
        except Exception as e:
            # If parsing fails, return a safe fallback
            return f"Error parsing plan history: {str(e)}"
    
    def log_developer_plan(self, plan: str, plan_description: str = "") -> int:
        """Log a new developer plan and return the plan index."""
        self.developer_plan_count += 1
        plan_index = self.developer_plan_count
        
        content = f"Plan Content:\n{plan}\n\n"
        if plan_description:
            content += f"Plan Description:\n{plan_description}"
        
        self.add_conversation(
            role="developer",
            title=f"Development Plan #{plan_index}",
            content=content,
            metadata={
                "plan_index": plan_index,
                "plan": plan,
                "plan_description": plan_description
            }
        )
        
        return plan_index
    
    def log_developer_history(self, plan_index: int, history: str) -> None:
        """Update developer log with history for a specific plan."""
        # Removed: No longer adding Development History to the HTML log
        pass
    
    def log_developer_code_execution(self, plan_index: int, code: str, 
                                   code_output: str, iteration: int = None) -> None:
        """Log developer code execution with syntax highlighting."""
        title = f"Code Execution - Plan #{plan_index}"
        if iteration is not None:
            title += f" (Iteration {iteration})"
        
        self.add_conversation(
            role="developer",
            title=title,
            content="Executing development phase code:",
            code=code,
            code_output=code_output,
            metadata={
                "plan_index": plan_index,
                "iteration": iteration
            }
        )
    
    def log_tester_feedback(self, code: str, code_output: str, feedback: str) -> None:
        """Log tester feedback with code and output."""
        self.add_conversation(
            role="tester",
            title="Tester Feedback",
            content=f"Tester Feedback:\n{feedback}",
            code=code,
            code_output=code_output
        )
    
    def log_critic_result(self, final_answer: str, reason: str, best_model_index: int) -> None:
        """Log critic final decision and reasoning."""
        content = f"""**Final Answer:**
{final_answer}

**Reasoning Process:**
{reason}

**Task Summary:**
- Task completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Total execution time: {(datetime.now() - self.start_time).total_seconds():.2f} seconds
- Selected best model index: {best_model_index}"""
        
        self.add_conversation(
            role="critic",
            title="🏆 Critic Final Decision",
            content=content,
            metadata={
                "final_answer": final_answer,
                "reason": reason,
                "best_model_index": best_model_index,
                "execution_time": (datetime.now() - self.start_time).total_seconds()
            }
        )
        
        # Save critic result to task_id root directory
        critic_data = {
            "task_id": self.task_id,
            "critic_model": self.model,
            "final_answer": final_answer,
            "reason": reason,
            "best_model_index": best_model_index,
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": (datetime.now() - self.start_time).total_seconds()
        }
        
        # Save to log_{task_id} directory instead of model subdirectory
        task_dir = Path(f"logs/log_{self.task_id}")
        task_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON format
        try:
            critic_json_path = task_dir / "critic.json"
            with open(critic_json_path, 'w', encoding='utf-8') as f:
                json.dump(critic_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing critic JSON file: {e}")
        
        # HTML format critic report
        critic_html = self._get_html_template().format(
            task_id=self.task_id,
            model=f"Critic ({self.model})",
            start_time=self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            content=f'''
            <div class="conversation">
                <div class="conversation-header">
                    <div class="role-badge role-critic">CRITIC</div>
                    <div class="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                <div class="conversation-content">
                    <div class="section">
                        <div class="section-title">Final Decision Result</div>
                        <div class="text-content">
                            <strong>Best Model Index:</strong> {best_model_index}<br><br>
                            <strong>Final Answer:</strong><br>
                            {self._escape_html(final_answer).replace(chr(10), '<br>')}<br><br>
                            <strong>Reasoning Process:</strong><br>
                            {self._escape_html(reason).replace(chr(10), '<br>')}
                        </div>
                        <div class="summary-stats">
                            <div class="stat-card">
                                <div class="stat-value">{best_model_index}</div>
                                <div class="stat-label">Best Model Index</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">{(datetime.now() - self.start_time).total_seconds():.1f}s</div>
                                <div class="stat-label">Total Execution Time</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ''',
            generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        try:
            critic_html_path = task_dir / "critic.html"
            with open(critic_html_path, 'w', encoding='utf-8') as f:
                f.write(critic_html)
        except Exception as e:
            print(f"Error writing critic HTML file: {e}")
    
    def log_task_summary(self, task: str, models: List[str], total_plans: int) -> None:
        """Create a task summary with overview information."""
        content = f"""**Task Description:**
{task}

**Models Used:**
{chr(10).join(f'• {model}' for model in models)}

**Execution Statistics:**
• Total models: {len(models)}
• Total plans generated: {total_plans}
• Total conversations: {len(self.conversations)}"""
        
        self.add_conversation(
            role="system",
            title="📊 Task Summary",
            content=content,
            metadata={
                "task": task,
                "models": models,
                "total_plans": total_plans,
                "total_conversations": len(self.conversations)
            }
        )


class HTMLTaskLoggerManager:
    """Manages HTMLTaskLogger instances for different task_id and model combinations."""
    
    def __init__(self):
        self.loggers: Dict[str, Dict[str, HTMLTaskLogger]] = {}
    
    def get_logger(self, task_id: str, model: str, base_dir: Optional[Path] = None) -> HTMLTaskLogger:
        """Get or create an HTMLTaskLogger for the specified task_id and model."""
        if task_id not in self.loggers:
            self.loggers[task_id] = {}
        
        # If base_dir is provided, always create a new logger to ensure correct directory
        if base_dir is not None:
            return HTMLTaskLogger(task_id, model, base_dir)
        
        # Otherwise use the cached logger
        if model not in self.loggers[task_id]:
            self.loggers[task_id][model] = HTMLTaskLogger(task_id, model, base_dir)
        
        return self.loggers[task_id][model]
    
    def cleanup_task(self, task_id: str) -> None:
        """Clean up loggers for a completed task."""
        if task_id in self.loggers:
            del self.loggers[task_id]


# Global HTML logger manager instance
html_task_logger_manager = HTMLTaskLoggerManager()


def get_html_task_logger(task_id: str, model: str, base_dir: Optional[Path] = None) -> HTMLTaskLogger:
    """Convenient function to get an HTML task logger."""
    return html_task_logger_manager.get_logger(task_id, model, base_dir) 