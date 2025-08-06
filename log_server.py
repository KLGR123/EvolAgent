from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory
from typing import Dict, List, Any, Optional

app = Flask(__name__)


class LogServer:
    """
    Log server for Agent
    """
    
    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = Path(logs_dir)
    
    def get_task_list(self) -> List[Dict[str, Any]]:
        """
        Get all task list
        """
        tasks = []
        if not self.logs_dir.exists():
            return tasks
        
        for task_dir in self.logs_dir.iterdir():
            if task_dir.is_dir() and task_dir.name.startswith("log_"):
                task_id = task_dir.name[4:]  # remove "log_" prefix
                
                # get all models in the task
                models = []
                critic_exists = False
                
                for item in task_dir.iterdir():
                    if item.is_dir():
                        # check if there is a task_log.html file
                        task_log_path = item / "task_log.html"
                        if task_log_path.exists():
                            models.append({
                                "name": item.name,
                                "path": str(task_log_path.relative_to(self.logs_dir))
                            })
                    elif item.name == "critic.html":
                        critic_exists = True
                
                if models or critic_exists:
                    tasks.append({
                        "task_id": task_id,
                        "models": models,
                        "has_critic": critic_exists,
                        "critic_path": f"log_{task_id}/critic.html" if critic_exists else None
                    })
        
        return sorted(tasks, key=lambda x: x["task_id"])
    
    def get_html_content(self, file_path: str) -> Optional[str]:
        """
        Get HTML file content
        """
        full_path = self.logs_dir / file_path
        if full_path.exists() and full_path.suffix == '.html':
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Failed to read file {full_path}: {e}")
                return None
        return None

# create log server instance
log_server = LogServer()

@app.route('/')
def index():
    """
    Main page
    """
    return render_template('index.html')

@app.route('/api/tasks')
def get_tasks():
    """
    Get task list API
    """
    tasks = log_server.get_task_list()
    return jsonify(tasks)

@app.route('/api/html/<path:file_path>')
def get_html_content(file_path):
    """
    Get HTML content API
    """
    content = log_server.get_html_content(file_path)
    if content:
        return jsonify({"content": content})
    else:
        return jsonify({"error": "File not found or read failed"}), 404

@app.route('/logs/<path:filename>')
def serve_logs(filename):
    """
    Serve log files directly
    """
    return send_from_directory(log_server.logs_dir, filename)

if __name__ == '__main__':
    # create templates directory
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    print("Agent log server is starting...")
    print("Visit http://localhost:5000 to view logs")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5002) 