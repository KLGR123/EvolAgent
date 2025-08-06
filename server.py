"""
EvolAgent Log Server

A Flask-based web server for viewing and analyzing EvolAgent experiment logs.
Provides a web interface to browse task execution logs, model comparisons, and critic evaluations.
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from flask import Flask, render_template, jsonify, request, send_from_directory, abort
from werkzeug.exceptions import NotFound

from src.utils.config import config


class EvolAgentLogServer:
    """
    Modern log server for EvolAgent experiment results.
    
    Provides web-based visualization and analysis of task execution logs,
    including model trajectories, critic evaluations, and performance metrics.
    """
    
    def __init__(self, logs_dir: str = None):
        """
        Initialize the log server.
        
        Args:
            logs_dir: Directory containing experiment logs (defaults to config value)
        """
        self.logs_dir = Path(logs_dir or config.get('logging.folder_path', 'logs'))
        self.app = self._create_flask_app()
        
    def _create_flask_app(self) -> Flask:
        """Create and configure Flask application."""
        app = Flask(__name__)
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        
        # Register routes
        self._register_routes(app)
        
        return app
    
    def _register_routes(self, app: Flask) -> None:
        """Register all Flask routes."""
        
        @app.route('/')
        def index():
            """Main dashboard page."""
            return render_template('index.html')
        
        @app.route('/api/tasks')
        def get_tasks():
            """Get list of all experiment tasks."""
            try:
                tasks = self.get_task_list()
                return jsonify({
                    'success': True,
                    'data': tasks,
                    'count': len(tasks)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @app.route('/api/task/<task_id>')
        def get_task_details(task_id: str):
            """Get detailed information about a specific task."""
            try:
                task_info = self.get_task_details(task_id)
                if task_info:
                    return jsonify({
                        'success': True,
                        'data': task_info
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Task not found'
                    }), 404
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @app.route('/api/html/<path:file_path>')
        def get_html_content(file_path: str):
            """Get HTML content for log visualization."""
            try:
                content = self.get_html_content(file_path)
                if content:
                    return jsonify({
                        'success': True,
                        'content': content
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'File not found or inaccessible'
                    }), 404
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @app.route('/logs/<path:filename>')
        def serve_logs(filename: str):
            """Serve log files directly."""
            try:
                return send_from_directory(self.logs_dir, filename)
            except FileNotFoundError:
                abort(404)
        
        @app.route('/api/stats')
        def get_statistics():
            """Get overall experiment statistics."""
            try:
                stats = self.get_experiment_statistics()
                return jsonify({
                    'success': True,
                    'data': stats
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def get_task_list(self) -> List[Dict[str, Any]]:
        """
        Get comprehensive list of all experiment tasks.
        
        Returns:
            List of task dictionaries with metadata
        """
        tasks = []
        
        if not self.logs_dir.exists():
            return tasks
        
        for task_dir in self.logs_dir.iterdir():
            if not (task_dir.is_dir() and task_dir.name.startswith("log_")):
                continue
                
            task_id = task_dir.name[4:]  # Remove "log_" prefix
            
            # Analyze task directory structure
            models = []
            critic_data = None
            task_metadata = {
                'created_time': None,
                'total_models': 0,
                'has_critic': False
            }
            
            # Process model directories
            for item in task_dir.iterdir():
                if item.is_dir():
                    task_log_path = item / "task_log.html"
                    if task_log_path.exists():
                        model_info = {
                            "name": item.name,
                            "path": str(task_log_path.relative_to(self.logs_dir)),
                            "created_time": datetime.fromtimestamp(
                                task_log_path.stat().st_mtime
                            ).isoformat() if task_log_path.exists() else None
                        }
                        models.append(model_info)
                
                elif item.name == "critic.html":
                    task_metadata['has_critic'] = True
                    critic_data = {
                        'path': f"log_{task_id}/critic.html",
                        'created_time': datetime.fromtimestamp(
                            item.stat().st_mtime
                        ).isoformat()
                    }
                    
                    # Try to read critic JSON for additional metadata
                    critic_json_path = task_dir / "critic.json"
                    if critic_json_path.exists():
                        try:
                            with open(critic_json_path, 'r', encoding='utf-8') as f:
                                critic_json_data = json.load(f)
                                critic_data.update({
                                    'best_model_index': critic_json_data.get('best_model_index'),
                                    'evaluation_time': critic_json_data.get('evaluation_time')
                                })
                        except Exception:
                            pass  # Continue without critic metadata
            
            task_metadata['total_models'] = len(models)
            
            # Set task creation time to earliest model time
            if models:
                creation_times = [m['created_time'] for m in models if m['created_time']]
                if creation_times:
                    task_metadata['created_time'] = min(creation_times)
            
            # Only include tasks with content
            if models or task_metadata['has_critic']:
                tasks.append({
                    "task_id": task_id,
                    "models": sorted(models, key=lambda x: x['created_time'] or ''),
                    "critic": critic_data,
                    "metadata": task_metadata
                })
        
        # Sort by creation time (newest first)
        return sorted(tasks, key=lambda x: x['metadata']['created_time'] or '', reverse=True)
    
    def get_task_details(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Detailed task information or None if not found
        """
        task_dir = self.logs_dir / f"log_{task_id}"
        if not task_dir.exists():
            return None
        
        # Get basic task info from task list
        tasks = self.get_task_list()
        task_info = next((t for t in tasks if t['task_id'] == task_id), None)
        
        if not task_info:
            return None
        
        # Add detailed analysis
        task_info['analysis'] = {
            'total_files': sum(1 for _ in task_dir.rglob('*') if _.is_file()),
            'directory_size': sum(f.stat().st_size for f in task_dir.rglob('*') if f.is_file()),
            'model_performance': self._analyze_model_performance(task_dir)
        }
        
        return task_info
    
    def _analyze_model_performance(self, task_dir: Path) -> Dict[str, Any]:
        """Analyze model performance from log files."""
        # This could be expanded to parse actual performance metrics
        # from log files, execution times, etc.
        return {
            'execution_completed': True,
            'has_errors': False,
            'metrics': {}
        }
    
    def get_html_content(self, file_path: str) -> Optional[str]:
        """
        Safely retrieve HTML content from log files.
        
        Args:
            file_path: Relative path to HTML file
            
        Returns:
            HTML content or None if not accessible
        """
        # Sanitize file path to prevent directory traversal
        safe_path = Path(file_path).resolve()
        full_path = (self.logs_dir / file_path).resolve()
        
        # Ensure the resolved path is within logs directory
        try:
            full_path.relative_to(self.logs_dir.resolve())
        except ValueError:
            return None  # Path traversal attempt
        
        if not (full_path.exists() and full_path.suffix == '.html'):
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {full_path}: {e}")
            return None
    
    def get_experiment_statistics(self) -> Dict[str, Any]:
        """
        Get overall experiment statistics.
        
        Returns:
            Dictionary with experiment statistics
        """
        tasks = self.get_task_list()
        
        total_models = sum(t['metadata']['total_models'] for t in tasks)
        tasks_with_critic = sum(1 for t in tasks if t['metadata']['has_critic'])
        
        # Calculate time range
        creation_times = [
            t['metadata']['created_time'] 
            for t in tasks 
            if t['metadata']['created_time']
        ]
        
        time_range = None
        if creation_times:
            time_range = {
                'earliest': min(creation_times),
                'latest': max(creation_times)
            }
        
        return {
            'total_tasks': len(tasks),
            'total_models': total_models,
            'tasks_with_critic': tasks_with_critic,
            'completion_rate': tasks_with_critic / len(tasks) if tasks else 0,
            'time_range': time_range,
            'average_models_per_task': total_models / len(tasks) if tasks else 0
        }
    
    def run(self, host: str = '0.0.0.0', port: int = 5002, debug: bool = False) -> None:
        """
        Start the log server.
        
        Args:
            host: Host address to bind to
            port: Port number to use
            debug: Enable Flask debug mode
        """
        # Ensure templates directory exists
        templates_dir = Path("templates")
        templates_dir.mkdir(exist_ok=True)
        
        print(f"🚀 EvolAgent Log Server starting...")
        print(f"📁 Logs directory: {self.logs_dir.absolute()}")
        print(f"🌐 Server URL: http://localhost:{port}")
        print(f"📊 Found {len(self.get_task_list())} experiment tasks")
        print("Press Ctrl+C to stop the server")
        
        try:
            self.app.run(debug=debug, host=host, port=port)
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")


def main():
    """Main entry point for the log server."""
    parser = argparse.ArgumentParser(
        description="EvolAgent Log Server - Web interface for experiment logs"
    )
    parser.add_argument(
        '--logs-dir', 
        type=str, 
        help="Directory containing experiment logs (default: from config)"
    )
    parser.add_argument(
        '--host', 
        type=str, 
        default='0.0.0.0',
        help="Host address to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=5002,
        help="Port number to use (default: 5002)"
    )
    parser.add_argument(
        '--debug', 
        action='store_true',
        help="Enable Flask debug mode"
    )
    
    args = parser.parse_args()
    
    # Create and run server
    server = EvolAgentLogServer(logs_dir=args.logs_dir)
    server.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main() 