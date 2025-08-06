"""
Interpreter for Python code.

Features:
- Interpret Python code in a sandboxed environment
- Automatically install packages from requirements.txt
- Handle workspace paths
- Provide a backward-compatible function interface
- Support for matplotlib backend
- Support for code execution timeout
"""

import io
import os
import re
import gc
import sys
import ast
import threading
import subprocess
import importlib
import contextlib
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class InterpreterConfig:
    """Interpreter configuration class"""
    timeout: int = 5000
    auto_install_packages: bool = True
    matplotlib_backend: str = 'Agg'
    max_output_length: Optional[int] = None
    requirements_file: str = "requirements.txt"


class PackageManager:
    """Package manager, responsible for package installation and caching"""
    
    def __init__(self):
        self._install_lock = threading.Lock()
        self._installed_cache = set()
        self._builtin_modules = self._get_builtin_modules()
    
    def _get_builtin_modules(self) -> set:
        """Get the list of Python built-in and standard library modules"""

        return {
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
    
    def is_installed(self, package_name: str) -> bool:
        """Check if a package is installed, with caching mechanism"""
        
        if package_name in self._installed_cache:
            return True
        
        try:
            importlib.import_module(package_name)
            self._installed_cache.add(package_name)
            return True
        except ImportError:
            return False
    
    def install_package(self, package_name: str) -> bool:
        """Thread-safe package installation"""

        with self._install_lock:
            # double-check pattern
            if self.is_installed(package_name):
                return True
            
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_name],
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                self._installed_cache.add(package_name)
                return True
            except subprocess.CalledProcessError:
                return False
    
    def ensure_packages(self, 
        packages: List[str], 
        requirements_file: str = "requirements.txt"
    ) -> Tuple[List[str], List[str]]:
        """Ensure packages are installed

        Args:
            packages: List of package names to install
            requirements_file: Path to the requirements.txt file

        Returns:
            Tuple of (successfully installed packages, failed packages)
        """
        
        # filter out built-in modules
        external_packages = [pkg for pkg in packages if pkg not in self._builtin_modules]
        
        # load packages from requirements.txt
        req_packages = self._load_requirements(requirements_file)
        all_packages = list(set(external_packages + req_packages))
        
        installed = []
        failed = []
        
        for package in all_packages:
            if not self.is_installed(package):
                print(f"Package '{package}' is not installed, installing...")
                if self.install_package(package):
                    installed.append(package)
                    self._update_requirements(package, requirements_file)
                    print(f"Successfully installed: {package}")
                else:
                    failed.append(package)
                    print(f"Installation failed: {package}")
        
        return installed, failed
    
    def _load_requirements(self, requirements_file: str) -> List[str]:
        """Load packages from requirements.txt"""
        
        packages = []
        try:
            if os.path.exists(requirements_file):
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # extract package name (ignore version specifiers)
                            package_name = re.split(r'[>=<~!]', line)[0].strip()
                            packages.append(package_name)
        except Exception as e:
            print(f"Could not read {requirements_file}: {e}")
        return packages
    
    def _update_requirements(self, package_name: str, requirements_file: str) -> bool:
        """Update requirements.txt file"""
        
        try:
            content = ""
            if os.path.exists(requirements_file):
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # check if package exists
            lines = content.strip().split('\n')
            existing_packages = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    package = re.split(r'[>=<~!]', line)[0].strip()
                    existing_packages.append(package)
            
            # if package does not exist, add it
            if package_name not in existing_packages:
                if content and not content.endswith('\n'):
                    content += '\n'
                content += f"{package_name}\n"
                
                with open(requirements_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            return False
        except Exception as e:
            print(f"Error updating {requirements_file}: {e}")
            return False


class CodeParser:
    """Code parser, responsible for extracting import statements"""
    
    @staticmethod
    def extract_imports(code: str) -> List[str]:
        """Extract import statements from code"""
        
        import_names = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top_level = alias.name.split('.')[0]
                        import_names.append(top_level)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        top_level = node.module.split('.')[0]
                        import_names.append(top_level)
                
                elif isinstance(node, ast.Call):
                    # handle dynamic imports
                    if (isinstance(node.func, ast.Name) and 
                        node.func.id in ['__import__', 'importlib.import_module'] and
                        node.args and isinstance(node.args[0], ast.Constant)):
                        module_name = node.args[0].value
                        if isinstance(module_name, str):
                            top_level = module_name.split('.')[0]
                            import_names.append(top_level)
        
        except SyntaxError:
            pass  # return empty list on syntax error
        
        return list(set(import_names))  # deduplicate


class ExecutionEnvironment:
    """Execution environment manager"""
    
    def __init__(self, config: InterpreterConfig):
        self.config = config
        self._original_backend = None
        self._original_sys_path = None
        self._original_cwd = None
    
    def __enter__(self):
        """Enter execution environment"""
        
        self._setup_matplotlib()
        self._setup_paths()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit execution environment, restore original state"""
        
        self._restore_paths()
        self._restore_matplotlib()
        gc.collect()
    
    def _setup_matplotlib(self):
        """Setup matplotlib backend"""
        
        try:
            import matplotlib
            self._original_backend = matplotlib.get_backend()
            matplotlib.use(self.config.matplotlib_backend, force=True)
        except ImportError:
            pass
    
    def _restore_matplotlib(self):
        """Restore matplotlib backend"""
        
        if self._original_backend:
            try:
                import matplotlib
                matplotlib.use(self._original_backend)
            except:
                pass
    
    def _setup_paths(self):
        """Setup execution path"""
        
        self._original_sys_path = sys.path.copy()
        self._original_cwd = os.getcwd()
        
        current_dir = os.path.abspath('.')
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        os.chdir(current_dir)
    
    def _restore_paths(self):
        """Restore execution path"""
        
        if self._original_sys_path is not None:
            sys.path.clear()
            sys.path.extend(self._original_sys_path)
        if self._original_cwd is not None:
            os.chdir(self._original_cwd)
    
    def create_globals(self) -> Dict[str, Any]:
        """Create isolated execution global environment"""
        
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
        
        # add essential built-in functions
        essential_builtins = [
            'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 
            'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 
            'delattr', 'dir', 'help', 'abs', 'max', 'min', 'sum', 'any', 'all', 
            'sorted', 'reversed', 'enumerate', 'zip', 'map', 'filter', 'open',
            'chr', 'ord', 'hex', 'oct', 'bin', 'round', 'pow', 'divmod', 'complex', 
            'bytes', 'bytearray', 'memoryview', 'slice', 'property', 'super', 
            'object', 'classmethod', 'staticmethod', 'frozenset', 'vars', 'locals', 
            'globals', 'eval', 'exec', 'compile', 'callable', 'hash', 'id', 'repr', 
            'ascii', 'format'
        ]
        
        import builtins
        for name in essential_builtins:
            if hasattr(builtins, name):
                execution_globals[name] = getattr(builtins, name)
        
        # add safe special functions
        execution_globals['input'] = self._safe_input
        execution_globals['breakpoint'] = self._safe_breakpoint
        execution_globals['exit'] = exit
        
        # add essential modules
        essential_modules = [
            'sys', 'os', 're', 'json', 'datetime', 'time', 'math', 'random',
            'pathlib', 'collections', 'itertools', 'functools', 'typing', 'copy',
            'hashlib', 'base64', 'struct', 'array', 'bisect', 'heapq', 'weakref',
            'gc', 'inspect', 'traceback', 'argparse', 'logging', 'platform',
            'shutil', 'tempfile', 'glob', 'csv', 'string', 'warnings'
        ]
        
        for module_name in essential_modules:
            try:
                module = importlib.import_module(module_name)
                execution_globals[module_name] = module
            except ImportError:
                pass
        
        execution_globals['os'].environ.update(os.environ)
        return execution_globals
    
    def _safe_input(self, prompt=""):
        """Safe input function, avoid blocking in non-interactive environment"""
        print(f"[INPUT REQUESTED] {prompt}")
        return ""
    
    def _safe_breakpoint(self, *args, **kwargs):
        """Safe breakpoint function"""
        print("[BREAKPOINT REQUESTED] Debugging is not available in this environment")
        return None


class PythonInterpreter:
    """Python interpreter main class"""
    
    def __init__(self, config: Optional[InterpreterConfig] = None):
        self.config = config or InterpreterConfig()
        self.package_manager = PackageManager()
        self.code_parser = CodeParser()
        
    def execute(self, code: str, auto_install_packages: Optional[List[str]] = None) -> str:
        """
        Execute Python code, return execution result
        
        Args:
            code: Python code to execute
            auto_install_packages: Additional packages to install
            
        Returns:
            Execution result string
        """

        processed_code = self._process_workspace_paths(code)
        
        # extract imported packages
        import_names = self.code_parser.extract_imports(processed_code)
        if auto_install_packages:
            import_names.extend(auto_install_packages)
        
        # ensure packages are installed
        results = []
        if import_names and self.config.auto_install_packages:
            installed, failed = self.package_manager.ensure_packages(
                import_names, self.config.requirements_file
            )
            
            if failed:
                results.append(f"Warning: Failed to install packages: {', '.join(failed)}")
            if installed:
                results.append(f"Automatically installed packages: {', '.join(installed)}")
        
        # execute code in isolated environment
        with ExecutionEnvironment(self.config) as env:
            stdout_content, stderr_content = self._execute_in_environment(
                processed_code, env
            )
        
        # organize output results
        if stdout_content:
            results.append("Code Output: \n")
            results.append(stdout_content.rstrip())
        
        if stderr_content:
            results.append("Error/Warning: \n")
            results.append(stderr_content.rstrip())
        
        result = "\n".join(results)
        return result
    
    def _process_workspace_paths(self, code: str) -> str:
        """Process workspace paths"""
        
        try:
            from .manager import workspace_manager
            
            current_workspace = workspace_manager.get_current_workspace()
            current_task_id = workspace_manager.get_current_task_id()
            
            if current_task_id and current_workspace:
                task_workspace_name = f"workspace_{current_task_id}"
                
                # replace workspace paths in various forms
                code = code.replace('workspace/', f'{task_workspace_name}/')
                code = code.replace('workspace\\', f'{task_workspace_name}\\')
                code = code.replace('"workspace"', f'"{task_workspace_name}"')
                code = code.replace("'workspace'", f"'{task_workspace_name}'")
                
                print(f"[WORKSPACE] Using task-specific workspace: {task_workspace_name}")
        
        except ImportError:
            pass
        
        return code
    
    def _execute_in_environment(self, code: str, env: ExecutionEnvironment) -> Tuple[str, str]:
        """Execute code in isolated environment"""

        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        execution_globals = env.create_globals()
        
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
            try:
                # determine code type and execute
                import_names = self.code_parser.extract_imports(code)
                has_imports = len(import_names) > 0
                
                if has_imports:
                    # contains import statements, use exec
                    exec(code, execution_globals, {})
                    if 'result' in execution_globals:
                        print(f"result = {repr(execution_globals['result'])}")
                else:
                    # try to execute as expression
                    try:
                        ast.parse(code, mode='eval')
                        result = eval(code, execution_globals, {})
                        if result is not None:
                            print(repr(result))
                    except SyntaxError:
                        # not an expression, execute as statement
                        exec(code, execution_globals, {})
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
                
                # provide friendly error hints
                self._print_error_hints(e)
        
        return output_buffer.getvalue(), error_buffer.getvalue()
    
    def _print_error_hints(self, error: Exception):
        """Print error hints"""

        error_type = type(error).__name__
        
        if "ModuleNotFoundError" in error_type:
            print("\nHint: If you're getting a ModuleNotFoundError, the package might need to be installed.")
            print("The interpreter will automatically install packages from requirements.txt and those you import.")

        elif "PermissionError" in error_type:
            print("\nHint: Permission error - check file/directory permissions.")

        elif "FileNotFoundError" in error_type:
            print("\nHint: File not found - check if the file path is correct.")


config = InterpreterConfig(timeout=5000)
python_interpreter = PythonInterpreter(config)