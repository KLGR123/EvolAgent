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
import platform
import shutil
import tempfile
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path


@dataclass
class WebBrowsingConfig:
    """Web browsing specific configuration"""
    headless: bool = True
    window_size: str = "1920,1080"
    chrome_args: List[str] = field(default_factory=lambda: [
        "--headless",
        "--no-sandbox", 
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--remote-debugging-port=9222"
    ])
    implicit_wait: int = 10
    page_load_timeout: int = 30
    script_timeout: int = 30
    enable_logging: bool = False
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


@dataclass
class InterpreterConfig:
    """Interpreter configuration class"""
    timeout: int = 5000
    auto_install_packages: bool = True
    matplotlib_backend: str = 'Agg'
    max_output_length: Optional[int] = None
    requirements_file: str = "requirements.txt"
    web_browsing: WebBrowsingConfig = field(default_factory=WebBrowsingConfig)
    enable_web_browsing_env: bool = True


class PackageManager:
    """Package manager, responsible for package installation and caching"""
    
    def __init__(self):
        self._install_lock = threading.Lock()
        self._installed_cache = set()
        self._builtin_modules = self._get_builtin_modules()
        self._web_browsing_packages = {
            'selenium': ['webdriver-manager', 'beautifulsoup4', 'requests'],
            'crawl4ai': ['aiohttp', 'playwright'],
            'playwright': ['playwright-stealth'],
            'requests': ['urllib3', 'certifi'],
            'beautifulsoup4': ['lxml', 'html5lib']
        }
    
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
        
        # Add web browsing dependencies
        extended_packages = self._expand_web_browsing_packages(external_packages)
        
        # load packages from requirements.txt
        req_packages = self._load_requirements(requirements_file)
        all_packages = list(set(extended_packages + req_packages))
        
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
        
        # Special handling for selenium webdriver setup
        if any(pkg in packages for pkg in ['selenium']):
            self._setup_selenium_environment()
        
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
    
    def _expand_web_browsing_packages(self, packages: List[str]) -> List[str]:
        """Expand web browsing packages with their dependencies"""
        
        expanded = packages.copy()
        
        for package in packages:
            if package in self._web_browsing_packages:
                expanded.extend(self._web_browsing_packages[package])
                print(f"Adding dependencies for {package}: {self._web_browsing_packages[package]}")
        
        return list(set(expanded))
    
    def _setup_selenium_environment(self):
        """Setup selenium-specific environment and webdrivers"""
        
        try:
            # Try to setup Chrome webdriver
            self._setup_chrome_webdriver()
        except Exception as e:
            print(f"Warning: Failed to setup Chrome webdriver: {e}")
    
    def _setup_chrome_webdriver(self):
        """Setup Chrome webdriver using webdriver-manager"""
        
        try:
            # Install webdriver-manager if not present
            if not self.is_installed('webdriver-manager'):
                if self.install_package('webdriver-manager'):
                    print("Successfully installed webdriver-manager")
            
            # Try to initialize webdriver manager
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            # Download and cache the chromedriver
            driver_path = ChromeDriverManager().install()
            print(f"ChromeDriver installed at: {driver_path}")
            
            # Set environment variable for chromedriver path
            os.environ['CHROMEDRIVER_PATH'] = driver_path
            
        except ImportError:
            print("Warning: webdriver-manager not available, manual chromedriver setup may be required")
        except Exception as e:
            print(f"Warning: ChromeDriver setup failed: {e}")


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
        self._original_env_vars = {}
    
    def __enter__(self):
        """Enter execution environment"""
        
        self._setup_matplotlib()
        self._setup_paths()
        if self.config.enable_web_browsing_env:
            self._setup_web_browsing_environment()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit execution environment, restore original state"""
        
        self._restore_paths()
        self._restore_matplotlib()
        if self.config.enable_web_browsing_env:
            self._restore_web_browsing_environment()
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
    
    def _setup_web_browsing_environment(self):
        """Setup environment for web browsing tools like selenium"""
        
        web_env_vars = {
            # Display environment for headless browsing
            'DISPLAY': ':99',
            # Chrome/Chromium configuration
            'CHROME_BIN': self._find_chrome_binary(),
            'CHROME_PATH': self._find_chrome_binary(),
            # Disable GPU for headless Chrome
            'CHROME_ARGS': ' '.join(self.config.web_browsing.chrome_args),
            # Webdriver manager configuration
            'WDM_LOG_LEVEL': '0',
            'WDM_PRINT_FIRST_LINE': 'False',
            'WDM_LOCAL': '1',
            # Selenium configuration
            'SELENIUM_MANAGER_LOG_LEVEL': '0',
            # Playwright configuration
            'PLAYWRIGHT_BROWSERS_PATH': str(Path.home() / '.cache' / 'ms-playwright'),
            # User agent
            'USER_AGENT': self.config.web_browsing.user_agent,
            # Timeout configurations
            'WEB_DRIVER_TIMEOUT': str(self.config.web_browsing.page_load_timeout),
            'IMPLICIT_WAIT': str(self.config.web_browsing.implicit_wait),
        }
        
        # Store original values and set new ones
        for key, value in web_env_vars.items():
            if key in os.environ:
                self._original_env_vars[key] = os.environ[key]
            else:
                self._original_env_vars[key] = None
            
            if value:
                os.environ[key] = value
                if self.config.web_browsing.enable_logging:
                    print(f"[WEB_ENV] Set {key}={value}")
    
    def _restore_web_browsing_environment(self):
        """Restore original web browsing environment variables"""
        
        for key, original_value in self._original_env_vars.items():
            if original_value is None:
                # Remove the key if it wasn't originally set
                if key in os.environ:
                    del os.environ[key]
            else:
                # Restore original value
                os.environ[key] = original_value
    
    def _find_chrome_binary(self) -> str:
        """Find Chrome binary path on the system"""
        
        chrome_paths = []
        
        if platform.system() == "Darwin":  # macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        elif platform.system() == "Linux":
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
                "/snap/bin/chromium",
            ]
        elif platform.system() == "Windows":
            chrome_paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe",
            ]
        
        # Check which chrome binary exists
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        
        # Try using shutil.which
        chrome_names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
        for name in chrome_names:
            path = shutil.which(name)
            if path:
                return path
        
        # Default fallback
        return "/usr/bin/google-chrome"
    
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
        
        # Pre-import modules that are mentioned in the code
        import_names = self.code_parser.extract_imports(code)
        for module_name in import_names:
            try:
                if module_name not in execution_globals:
                    module = importlib.import_module(module_name)
                    execution_globals[module_name] = module
            except ImportError:
                # Module might not be installed, but exec will handle the error
                pass
        
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
            try:
                # Always use exec for consistency and to handle all import scenarios
                exec(code, execution_globals, execution_globals)
                
                # Check if there's a result variable to display
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
        error_msg = str(error).lower()
        
        # Web browsing specific errors
        if "timeoutexception" in error_type.lower():
            print("\nHint: Selenium TimeoutException - Element not found")
            print("Suggestion: Increase wait time, check element locators, confirm page is loaded correctly")
            print("Try: Add longer wait time or use more robust element locator strategies")
            print("Example: WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'element_id')))")
        
        elif "webdriverexception" in error_type.lower():
            print("\nHint: WebDriver Exception - Browser driver problem")
            print("Suggestion: Check Chrome/ChromeDriver version compatibility, confirm headless mode configuration")
            print("Try: Update webdriver-manager or manually specify driver path")
            print("Environment variable CHROMEDRIVER_PATH is automatically set")
        
        elif "sessionnotcreatedexception" in error_type.lower():
            print("\nHint: WebDriver Session Creation Failed")
            print("Suggestion: Check if Chrome browser is installed, check ChromeDriver version compatibility")
            print("Try: pip install --upgrade selenium webdriver-manager")
        
        elif "nosuchelementexception" in error_type.lower():
            print("\nHint: No Such Element Exception - Page element not found")
            print("Suggestion: Check if element locator is correct, check if page is fully loaded")
            print("Try: Use explicit wait: WebDriverWait(driver, 10).until(...)")
        
        elif "selenium" in error_msg or "webdriver" in error_msg:
            print("\nHint: Selenium Related Errors")
            print("Suggestion: Confirm selenium and related dependencies are correctly installed, check browser environment configuration")
            print("Web browsing environment is automatically configured, including Chrome path and environment variables")
        
        elif "crawl4ai" in error_msg:
            print("\nHint: Crawl4AI Related Errors")
            print("Suggestion: Confirm crawl4ai and its dependencies are correctly installed")
            print("Try: pip install crawl4ai aiohttp playwright")
        
        elif "playwright" in error_msg:
            print("\nHint: Playwright Related Errors")
            print("Suggestion: Confirm playwright is correctly installed and downloaded the browser")
            print("Try: pip install playwright && playwright install")
        
        elif "requests" in error_msg and ("connection" in error_msg or "timeout" in error_msg):
            print("\nHint: Network Connection Error")
            print("Suggestion: Check network connection, increase timeout, use retry mechanism")
            print("Try: Add headers and timeout parameters")
        
        # General errors
        elif "ModuleNotFoundError" in error_type:
            print("\nHint: Module Not Found Error - Package may need to be installed")
            print("The interpreter will automatically install requirements.txt and imported packages")
            print("Web browsing related dependencies will be automatically added")

        elif "PermissionError" in error_type:
            print("\nHint: Permission Error - Check file/directory permissions")

        elif "FileNotFoundError" in error_type:
            print("\nHint: File Not Found Error - Check file path is correct")
        
        elif "connectionerror" in error_msg or "httperror" in error_msg:
            print("\nHint: HTTP Connection Error")
            print("Suggestion: Check network connection, check if target website is accessible, check if proxy is needed")
        
        # Add web browsing troubleshooting info
        if any(term in error_msg for term in ['selenium', 'webdriver', 'chrome', 'browser']):
            print("\n[WEB BROWSING TROUBLESHOOTING]")
            print("1. Chrome path is automatically detected and set")
            print("2. Environment variables are configured for headless mode")
            print("3. ChromeDriver is automatically downloaded and managed")
            print("4. If there are still problems, check if Chrome is installed")


class BrowserDetector:
    """Browser and WebDriver detection utilities"""
    
    @staticmethod
    def detect_chrome() -> Dict[str, Any]:
        """Detect Chrome installation and version"""
        
        result = {
            'installed': False,
            'path': None,
            'version': None,
            'error': None
        }
        
        try:
            # Find Chrome binary
            chrome_paths = []
            
            if platform.system() == "Darwin":  # macOS
                chrome_paths = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Chromium.app/Contents/MacOS/Chromium",
                ]
            elif platform.system() == "Linux":
                chrome_paths = [
                    "/usr/bin/google-chrome",
                    "/usr/bin/google-chrome-stable",
                    "/usr/bin/chromium",
                    "/usr/bin/chromium-browser",
                ]
            elif platform.system() == "Windows":
                chrome_paths = [
                    "C:\\Program Files\\Google Chrome\\Application\\chrome.exe",
                    "C:\\Program Files (x86)\\Google Chrome\\Application\\chrome.exe",
                ]
            
            # Check existing paths
            for path in chrome_paths:
                if os.path.exists(path):
                    result['installed'] = True
                    result['path'] = path
                    break
            
            # Try using shutil.which if not found
            if not result['installed']:
                chrome_names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
                for name in chrome_names:
                    path = shutil.which(name)
                    if path:
                        result['installed'] = True
                        result['path'] = path
                        break
            
            # Get version if found
            if result['installed'] and result['path']:
                try:
                    version_cmd = [result['path'], '--version']
                    version_output = subprocess.check_output(
                        version_cmd, stderr=subprocess.DEVNULL, timeout=10
                    ).decode('utf-8').strip()
                    result['version'] = version_output
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    result['version'] = 'Unknown'
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    @staticmethod
    def detect_webdriver() -> Dict[str, Any]:
        """Detect WebDriver availability"""
        
        result = {
            'selenium_installed': False,
            'webdriver_manager_installed': False,
            'chromedriver_available': False,
            'chromedriver_path': None,
            'error': None
        }
        
        try:
            # Check selenium installation
            try:
                import selenium
                result['selenium_installed'] = True
            except ImportError:
                pass
            
            # Check webdriver-manager installation
            try:
                import webdriver_manager
                result['webdriver_manager_installed'] = True
            except ImportError:
                pass
            
            # Check chromedriver availability
            if result['webdriver_manager_installed']:
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    driver_path = ChromeDriverManager().install()
                    result['chromedriver_available'] = True
                    result['chromedriver_path'] = driver_path
                except Exception as e:
                    result['error'] = f"ChromeDriver setup failed: {e}"
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    @classmethod
    def get_web_browsing_status(cls) -> Dict[str, Any]:
        """Get complete web browsing environment status"""
        
        chrome_info = cls.detect_chrome()
        webdriver_info = cls.detect_webdriver()
        
        return {
            'chrome': chrome_info,
            'webdriver': webdriver_info,
            'ready_for_selenium': (
                chrome_info['installed'] and 
                webdriver_info['selenium_installed'] and 
                webdriver_info['chromedriver_available']
            ),
            'system': platform.system(),
            'recommendations': cls._get_recommendations(chrome_info, webdriver_info)
        }
    
    @staticmethod
    def _get_recommendations(chrome_info: Dict, webdriver_info: Dict) -> List[str]:
        """Get recommendations for improving web browsing setup"""
        
        recommendations = []
        
        if not chrome_info['installed']:
            recommendations.append("Install Google Chrome or Chromium browser")
        
        if not webdriver_info['selenium_installed']:
            recommendations.append("Install selenium: pip install selenium")
        
        if not webdriver_info['webdriver_manager_installed']:
            recommendations.append("Install webdriver-manager: pip install webdriver-manager")
        
        if not webdriver_info['chromedriver_available']:
            recommendations.append("ChromeDriver setup failed - check Chrome version compatibility")
        
        if chrome_info.get('error'):
            recommendations.append(f"Chrome detection error: {chrome_info['error']}")
        
        if webdriver_info.get('error'):
            recommendations.append(f"WebDriver setup error: {webdriver_info['error']}")
        
        return recommendations


# Enhanced configuration with browser detection
def create_enhanced_config(enable_browser_detection: bool = True) -> InterpreterConfig:
    """Create enhanced interpreter configuration with browser detection"""
    
    config = InterpreterConfig(timeout=5000)
    
    if enable_browser_detection:
        browser_status = BrowserDetector.get_web_browsing_status()
        
        # Update Chrome path if detected
        if browser_status['chrome']['installed']:
            config.web_browsing.chrome_args = [
                "--headless",
                "--no-sandbox", 
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--remote-debugging-port=9222",
                f"--user-agent={config.web_browsing.user_agent}"
            ]
        
        # Enable logging if setup is not ready
        if not browser_status['ready_for_selenium']:
            config.web_browsing.enable_logging = True
            print("[BROWSER DETECTION] Web browsing setup incomplete:")
            for rec in browser_status['recommendations']:
                print(f"  - {rec}")
    
    return config


# Default configuration instances
config = create_enhanced_config()
python_interpreter = PythonInterpreter(config)