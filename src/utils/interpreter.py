

import io
import contextlib
import subprocess
import sys
import os
import importlib
import ast
import re
import threading
import gc
from typing import List, Optional

# 线程安全的包安装锁
_package_install_lock = threading.Lock()
_installed_packages = set()  # 缓存已安装的包，避免重复检查

def extract_import_names(code: str) -> List[str]:
    """
    Extract all import names from the code, return a list of module names.
    """
    import_names = []
    
    try:
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # get the top level package name
                    top_level = alias.name.split('.')[0]
                    import_names.append(top_level)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # get the top level package name
                    top_level = node.module.split('.')[0]
                    import_names.append(top_level)
    except SyntaxError:
        # if the code has syntax error, return an empty list
        pass
    
    return list(set(import_names))  # remove duplicates


def is_package_installed(package_name: str) -> bool:
    """
    Check if the package is installed with caching.
    """
    if package_name in _installed_packages:
        return True
        
    try:
        importlib.import_module(package_name)
        _installed_packages.add(package_name)
        return True
    except ImportError:
        return False


def install_package(package_name: str) -> bool: # TODO conflicts dealing when not pip install package name
    """
    Install the package with thread-safe locking.
    """
    with _package_install_lock:
        # 双重检查：在获得锁后再次检查包是否已安装
        if is_package_installed(package_name):
            return True
            
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            _installed_packages.add(package_name)
            return True
        except subprocess.CalledProcessError:
            return False


def update_requirements_txt(package_name: str, requirements_path: str = "requirements.txt") -> bool:
    """
    Add the package name to the requirements.txt file.
    """
    try:
        # read the existing requirements.txt content
        if os.path.exists(requirements_path):
            with open(requirements_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # check if the package already exists
        lines = content.strip().split('\n')
        existing_packages = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # extract the package name (ignore the version number)
                package = re.split(r'[>=<~!]', line)[0].strip()
                existing_packages.append(package)
        
        # if the package does not exist, add it to the file
        if package_name not in existing_packages:
            if content and not content.endswith('\n'):
                content += '\n'
            content += f"{package_name}\n"
            
            with open(requirements_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        return False  # the package already exists
        
    except Exception as e:
        print(f"Error updating requirements.txt: {e}")
        return False


def get_python_builtin_modules():
    """
    Get a comprehensive list of Python built-in and standard library modules.
    """
    return {
        # Built-in modules
        'builtins', 'sys', 'os', 'time', 'datetime', 'json', 're', 'math', 
        'random', 'collections', 'itertools', 'functools', 'typing', 'pathlib',
        'urllib', 'http', 'socket', 'threading', 'multiprocessing', 'subprocess',
        'io', 'contextlib', 'ast', 'importlib', 'pickle', 'copy', 'hashlib',
        'base64', 'binascii', 'struct', 'array', 'bisect', 'heapq', 'weakref',
        'gc', 'inspect', 'dis', 'code', 'codeop', 'traceback', 'pdb', 'profile',
        'pstats', 'timeit', 'argparse', 'configparser', 'logging', 'getpass',
        'curses', 'platform', 'shutil', 'tempfile', 'glob', 'fnmatch', 'filecmp',
        'tarfile', 'zipfile', 'gzip', 'bz2', 'lzma', 'csv', 'xml', 'html',
        'email', 'mimetypes', 'base64', 'quopri', 'uu', 'binascii', 'unicodedata',
        'stringprep', 'readline', 'rlcompleter', 'sqlite3', 'zlib', 'mailbox',
        'calendar', 'decimal', 'fractions', 'statistics', 'wave', 'chunk',
        'colorsys', 'imghdr', 'sndhdr', 'ossaudiodev', 'audioop', 'hmac',
        'secrets', 'ssl', 'ftplib', 'poplib', 'imaplib', 'smtplib', 'telnetlib',
        'uuid', 'socketserver', 'xmlrpc', 'ipaddress', 'queue', 'sched',
        'mutex', 'enum', 'signal', 'errno', 'ctypes', 'mmap', 'winreg',
        'winsound', 'msvcrt', 'fcntl', 'pipes', 'posix', 'pwd', 'spwd', 'grp',
        'crypt', 'termios', 'tty', 'pty', 'syslog', 'operator', 'keyword',
        'token', 'tokenize', 'symbol', 'textwrap', 'string', 'unicodedata',
        'warnings', 'site', 'user', 'encodings', 'codecs', '__future__',
        'abc', 'numbers', 'cmath', 'locale', 'gettext', 'doctest', 'unittest',
        'pprint', 'reprlib', 'difflib', 'linecache', 'tkinter', 'turtle',
        'idle', 'pydoc', 'asyncio', 'concurrent', 'test', 'lib2to3',
        'distutils', 'pkgutil', 'modulefinder', 'runpy', 'compileall',
        'py_compile', 'zipapp', 'venv', 'ensurepip'
    }


def interpret_code(code: str, auto_install_packages: Optional[List[str]] = None) -> str:
    """
    Execute Python code in a thread-safe isolated environment with proper resource cleanup.
    
    Args:
        code: The Python code to execute.
        auto_install_packages: Optional list of package names, these packages will be automatically installed if they do not exist.
    
    Returns:
        The string of the execution result.
    """
    # Set matplotlib backend to non-GUI to prevent GUI window creation in threads
    # 仅在当前线程中设置，避免全局污染
    original_backend = None
    try:
        import matplotlib
        original_backend = matplotlib.get_backend()
        matplotlib.use('Agg', force=True)  # Use Anti-Grain Geometry backend (no GUI)
    except ImportError:
        pass  # matplotlib not installed, skip
    
    # Import workspace_manager here to avoid circular imports
    try:
        from .workspace_manager import workspace_manager
        
        # Replace workspace/ paths with task-specific workspace paths
        current_workspace = workspace_manager.get_current_workspace()
        current_task_id = workspace_manager.get_current_task_id()
        
        if current_task_id and current_workspace:
            # Replace workspace/ with workspace_{task_id}/
            task_workspace_name = f"workspace_{current_task_id}"
            
            # Use string replacement instead of regex to avoid escape issues
            # Replace various forms of workspace paths
            code = code.replace('workspace/', f'{task_workspace_name}/')
            code = code.replace('workspace\\', f'{task_workspace_name}\\')  # Windows paths
            code = code.replace('"workspace"', f'"{task_workspace_name}"')
            code = code.replace("'workspace'", f"'{task_workspace_name}'")
            
            print(f"[WORKSPACE] Using task-specific workspace: {task_workspace_name}")
        
    except ImportError:
        # If workspace_manager is not available, continue with original code
        pass
    
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    result_parts = []
    
    # extract the import statements from the code
    import_names = extract_import_names(code)
    
    # if auto_install_packages is specified, merge it with import_names
    if auto_install_packages:
        import_names.extend(auto_install_packages)
        import_names = list(set(import_names))  # remove duplicates
    
    # Get comprehensive built-in modules list
    builtin_modules = get_python_builtin_modules()
    
    # check and install missing packages (thread-safe)
    installed_packages = []
    for package_name in import_names:
        # Skip built-in modules and standard library
        if package_name in builtin_modules:
            continue
            
        if not is_package_installed(package_name):
            print(f"Package '{package_name}' is not installed, installing...")
            if install_package(package_name):
                installed_packages.append(package_name)
                update_requirements_txt(package_name)
                print(f"Successfully installed and added to requirements.txt: {package_name}")
            else:
                print(f"Installation failed: {package_name}")
    
    if installed_packages:
        result_parts.append(f"Automatically installed packages: {', '.join(installed_packages)}")
    
    # 保存原始的 sys.path，避免全局污染
    original_sys_path = sys.path.copy()
    original_cwd = os.getcwd()
    
    try:
        # Get the absolute path of the current working directory
        current_dir = os.path.abspath('.')
        
        # 临时添加到 sys.path，在 finally 中恢复
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Set working directory
        os.chdir(current_dir)
        
        # Create a completely isolated execution environment
        execution_globals = {
            '__name__': '__main__',
            '__file__': '<string>',
            '__builtins__': __builtins__,
            '__package__': None,
            '__spec__': None,
            '__annotations__': {},
            '__loader__': None,
            '__cached__': None,
        }
        
        # Add essential built-in functions without importing everything
        essential_builtins = ['print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'delattr', 'dir', 'help', 'abs', 'max', 'min', 'sum', 'any', 'all', 'sorted', 'reversed', 'enumerate', 'zip', 'map', 'filter', 'open', 'input']
        import builtins
        for name in essential_builtins:
            if hasattr(builtins, name):
                execution_globals[name] = getattr(builtins, name)
        
        # Pass through environment variables (important for API keys, etc.)
        execution_globals['os'] = os
        
        # Import commonly used modules into the execution environment
        essential_modules = ['sys', 'os', 're', 'json', 'datetime', 'time', 'math', 'random']
        for module_name in essential_modules:
            try:
                module = importlib.import_module(module_name)
                execution_globals[module_name] = module
            except ImportError:
                pass
        
        # Handle input() function in non-interactive environment
        def safe_input(prompt=""):
            """Safe input function that doesn't block in non-interactive environment"""
            print(f"[INPUT REQUESTED] {prompt}")
            return ""  # Return empty string by default
        
        execution_globals['input'] = safe_input
        
        # redirect stdout and stderr to capture the output
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
            try:
                # Check if the code is a simple expression first
                try:
                    # Try to parse as expression first
                    ast.parse(code, mode='eval')
                    # If successful, it's a simple expression, use eval
                    result = eval(code, execution_globals, {})  # 使用独立的 locals
                    if result is not None:
                        print(repr(result))
                except SyntaxError:
                    # Not a simple expression, execute as statement
                    exec(code, execution_globals, {})  # 使用独立的 locals
                    
                    # Check if there's a 'result' variable in the execution globals
                    if 'result' in execution_globals:
                        print(f"result = {repr(execution_globals['result'])}")
                
            except KeyboardInterrupt:
                print("Code execution was interrupted by user")
            except SystemExit as e:
                print(f"Code execution called sys.exit({e.code})")
            except Exception as e:
                print(f"Execution error: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
    
    finally:
        # 恢复原始状态，避免全局污染
        sys.path.clear()
        sys.path.extend(original_sys_path)
        os.chdir(original_cwd)
        
        # 恢复 matplotlib backend
        if original_backend:
            try:
                import matplotlib
                matplotlib.use(original_backend)
            except:
                pass
        
        # 强制垃圾回收，清理执行环境
        gc.collect()
    
    # get the captured output
    stdout_content = output_buffer.getvalue()
    stderr_content = error_buffer.getvalue()
    
    # add the output TODO better logging
    if stdout_content:
        result_parts.append("Code Output:")
        result_parts.append(stdout_content.rstrip())
    
    if stderr_content:
        result_parts.append("Error/Warning:")
        result_parts.append(stderr_content.rstrip())
    
    return "\n".join(result_parts)


if __name__ == "__main__":
    # test code
    test_code = '''
import pandas as pd
import math
import random

print("Hello, World!")
print(math.sqrt(16))
'''
    
    result = interpret_code(test_code, auto_install_packages=['requests', 'pandas'])
    print(result)