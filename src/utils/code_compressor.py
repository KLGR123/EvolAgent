"""
Code and Output Compressor for EvolAgent

Specialized compression for code and code_output fields which are typically
the largest token consumers in history.
"""

import re
import ast
import json
from typing import Optional, Dict, Any, List
from textwrap import dedent

from ..config import config
from ..utils.logger import get_logger


class CodeCompressor:
    """
    Intelligent compressor for code and code output fields.
    """
    
    def __init__(self):
        self.logger = get_logger("evolagent.code_compressor")
    
    def compress_code(self, code: str, target_reduction: float = 0.5) -> Optional[str]:
        """
        Compress Python code while preserving functionality.
        
        Args:
            code: Original code string
            target_reduction: Target reduction ratio (0.5 = 50% reduction)
            
        Returns:
            Compressed code or None if compression failed
        """
        if not code or len(code) < config.compression_min_length:
            return None
            
        try:
            # Multi-stage compression pipeline
            compressed = code
            
            # Stage 1: Syntax-level compression
            compressed = self._compress_syntax(compressed)
            
            # Stage 2: Semantic compression (if still too long)
            if len(compressed) > len(code) * (1 - target_reduction):
                compressed = self._compress_semantically(compressed)
            
            # Stage 3: Structure-based compression (if still too long)  
            if len(compressed) > len(code) * (1 - target_reduction):
                compressed = self._compress_structure(compressed)
            
            # Only return if we achieved meaningful compression
            if len(compressed) < len(code) * 0.8:  # At least 20% reduction
                self.logger.debug(f"Code compressed: {len(code)} -> {len(compressed)} chars")
                return compressed
                
            return None
            
        except Exception as e:
            self.logger.error(f"Code compression failed: {e}")
            return None
    
    def _compress_syntax(self, code: str) -> str:
        """Stage 1: Syntax-level compression (safe, preserves functionality)."""
        
        # Remove excessive whitespace
        lines = code.split('\n')
        compressed_lines = []
        
        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace
            if line.strip():  # Skip empty lines
                # Preserve indentation but minimize it
                indent = len(line) - len(line.lstrip())
                content = line.strip()
                
                # Skip single-line comments unless they seem important
                if content.startswith('#'):
                    if any(keyword in content.lower() for keyword in ['todo', 'fixme', 'important', 'note']):
                        compressed_lines.append(' ' * indent + content)
                    # Skip other comments
                    continue
                
                compressed_lines.append(' ' * indent + content)
        
        # Remove docstrings (but keep the first one if it's short)
        result = '\n'.join(compressed_lines)
        result = self._remove_docstrings(result)
        
        return result
    
    def _remove_docstrings(self, code: str) -> str:
        """Remove docstrings while preserving the first one if it's concise."""
        try:
            tree = ast.parse(code)
            
            # Find docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    if (node.body and 
                        isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and 
                        isinstance(node.body[0].value.value, str)):
                        
                        docstring = node.body[0].value.value
                        # Keep short, informative docstrings
                        if len(docstring) > 100:
                            # Replace with summary
                            lines = code.split('\n')
                            for i, line in enumerate(lines):
                                if f'"""' in line or f"'''" in line:
                                    # Find the end of docstring
                                    end_i = i
                                    for j in range(i + 1, len(lines)):
                                        if '"""' in lines[j] or "'''" in lines[j]:
                                            end_i = j
                                            break
                                    
                                    # Replace docstring with summary
                                    indent = ' ' * (len(lines[i]) - len(lines[i].lstrip()))
                                    summary = f'{indent}"""Function implementation"""'
                                    lines[i:end_i+1] = [summary]
                                    break
                            
                            code = '\n'.join(lines)
            
            return code
            
        except:
            # If AST parsing fails, fall back to regex
            return re.sub(r'"""[\s\S]*?"""', '"""Implementation"""', code)
    
    def _compress_semantically(self, code: str) -> str:
        """Stage 2: Semantic compression using patterns and structure."""
        
        # Replace common verbose patterns
        patterns = [
            # Exception handling simplification
            (r'except Exception as e:\s*print\(.*?\)\s*raise', 'except Exception as e: raise'),
            
            # Logging simplification  
            (r'logger\.debug\(.*?\)', ''),
            (r'logger\.info\([^)]*"[^"]*"[^)]*\)', ''),
            
            # Verbose variable assignments
            (r'(\w+)\s*=\s*\1\.strip\(\)\.lower\(\)', r'\1 = \1.strip().lower()'),
            
            # List comprehension opportunities
            (r'result\s*=\s*\[\]\s*for\s+(\w+)\s+in\s+([^:]+):\s*result\.append\(([^)]+)\)', 
             r'result = [\3 for \1 in \2]'),
        ]
        
        compressed = code
        for pattern, replacement in patterns:
            compressed = re.sub(pattern, replacement, compressed, flags=re.MULTILINE | re.DOTALL)
        
        return compressed
    
    def _compress_structure(self, code: str) -> str:
        """Stage 3: Structure-based compression (more aggressive, may change logic)."""
        
        try:
            tree = ast.parse(code)
            
            # Extract key structural information
            functions = []
            classes = []
            imports = []
            main_logic = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extract function signature and key operations
                    args = [arg.arg for arg in node.args.args]
                    signature = f"def {node.name}({', '.join(args)}):"
                    
                    # Analyze function body for key operations
                    key_ops = self._extract_key_operations(node)
                    functions.append(f"{signature}\n    # {key_ops}")
                
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append(f"class {node.name}: # Methods: {', '.join(methods)}")
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.unparse(node))
            
            # Reconstruct compressed version
            compressed_parts = []
            
            if imports:
                compressed_parts.extend(imports[:5])  # Limit imports
            
            if classes:
                compressed_parts.extend(classes)
            
            if functions:
                compressed_parts.extend(functions)
            
            return '\n'.join(compressed_parts)
            
        except:
            # Fallback: extract just the function/class signatures
            lines = code.split('\n')
            key_lines = []
            
            for line in lines:
                stripped = line.strip()
                if (stripped.startswith('def ') or 
                    stripped.startswith('class ') or
                    stripped.startswith('import ') or
                    stripped.startswith('from ')):
                    key_lines.append(line)
            
            return '\n'.join(key_lines) if key_lines else code
    
    def _extract_key_operations(self, func_node: ast.FunctionDef) -> str:
        """Extract key operations from a function."""
        operations = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    operations.append(f"calls {node.func.id}")
                elif isinstance(node.func, ast.Attribute):
                    operations.append(f"uses {node.func.attr}")
        
        return ', '.join(operations[:3])  # Top 3 operations
    
    def compress_output(self, output: str, max_length: int = 500) -> Optional[str]:
        """
        Compress code output intelligently based on content type.
        
        Args:
            output: Original output string
            max_length: Maximum length for compressed output
            
        Returns:
            Compressed output or None if no compression needed
        """
        if not output or len(output) <= max_length:
            return None
        
        try:
            # Detect output type and apply appropriate compression
            if self._is_json_output(output):
                return self._compress_json_output(output, max_length)
            elif self._is_dataframe_output(output):
                return self._compress_dataframe_output(output, max_length)  
            elif self._is_error_output(output):
                return self._compress_error_output(output, max_length)
            elif self._is_log_output(output):
                return self._compress_log_output(output, max_length)
            else:
                return self._compress_generic_output(output, max_length)
                
        except Exception as e:
            self.logger.error(f"Output compression failed: {e}")
            return self._compress_generic_output(output, max_length)
    
    def _is_json_output(self, output: str) -> bool:
        """Check if output looks like JSON."""
        stripped = output.strip()
        return (stripped.startswith('{') and stripped.endswith('}')) or \
               (stripped.startswith('[') and stripped.endswith(']'))
    
    def _is_dataframe_output(self, output: str) -> bool:
        """Check if output looks like pandas DataFrame."""
        return any(marker in output for marker in [
            'DataFrame', 'columns:', 'dtype:', 'Index:', 'Shape:'
        ])
    
    def _is_error_output(self, output: str) -> bool:
        """Check if output contains error information."""
        return any(marker in output.lower() for marker in [
            'error:', 'exception:', 'traceback', 'failed:', 'errno'
        ])
    
    def _is_log_output(self, output: str) -> bool:
        """Check if output looks like log messages."""
        return any(marker in output.upper() for marker in [
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        ])
    
    def _compress_json_output(self, output: str, max_length: int) -> str:
        """Compress JSON output."""
        try:
            # Try to parse and reformat compactly
            data = json.loads(output)
            
            if isinstance(data, dict):
                # Show structure with sample values
                keys = list(data.keys())[:5]  # First 5 keys
                sample = {k: f"<{type(data[k]).__name__}>" for k in keys}
                if len(data) > 5:
                    sample['...'] = f"({len(data)-5} more keys)"
                return f"JSON object: {json.dumps(sample, separators=(',', ':'))}"
            
            elif isinstance(data, list):
                # Show list structure
                if len(data) > 3:
                    sample = data[:2] + [f"... {len(data)-2} more items"]
                    return f"JSON array[{len(data)}]: {json.dumps(sample, separators=(',', ':'))}"
                
            return json.dumps(data, separators=(',', ':'))[:max_length]
            
        except:
            return output[:max_length] + "..."
    
    def _compress_dataframe_output(self, output: str, max_length: int) -> str:
        """Compress pandas DataFrame output."""
        lines = output.split('\n')
        
        # Extract key information
        shape_info = next((line for line in lines if 'shape' in line.lower()), '')
        column_info = next((line for line in lines if 'columns' in line.lower()), '')
        dtype_info = next((line for line in lines if 'dtype' in line.lower()), '')
        
        # Build compact summary
        summary_parts = []
        if shape_info:
            summary_parts.append(shape_info.strip())
        if column_info:
            summary_parts.append(column_info.strip()[:100])
        if dtype_info:
            summary_parts.append(dtype_info.strip()[:50])
        
        # Add sample data (first few lines)
        data_lines = [line for line in lines[:10] if line.strip() and 
                     not any(keyword in line.lower() for keyword in ['shape', 'columns', 'dtype'])]
        
        summary = f"DataFrame Info: {' | '.join(summary_parts)}\nSample:\n" + '\n'.join(data_lines[:3])
        
        return summary[:max_length]
    
    def _compress_error_output(self, output: str, max_length: int) -> str:
        """Compress error output, keeping essential information."""
        lines = output.split('\n')
        
        # Keep error type and message
        error_lines = []
        traceback_lines = []
        
        for line in lines:
            if any(keyword in line for keyword in ['Error:', 'Exception:', 'Failed']):
                error_lines.append(line.strip())
            elif 'File "' in line and 'line' in line:
                # Keep file and line info but compress path
                traceback_lines.append(line.strip())
        
        # Build compressed error
        result_parts = []
        
        if error_lines:
            result_parts.append("ERROR: " + " | ".join(error_lines[:2]))
        
        if traceback_lines:
            result_parts.append("AT: " + " -> ".join(traceback_lines[-2:]))  # Last 2 locations
        
        return '\n'.join(result_parts)[:max_length]
    
    def _compress_log_output(self, output: str, max_length: int) -> str:
        """Compress log output, prioritizing warnings and errors."""
        lines = output.split('\n')
        
        # Categorize log lines
        errors = [line for line in lines if 'ERROR' in line.upper()]
        warnings = [line for line in lines if 'WARNING' in line.upper()]
        infos = [line for line in lines if 'INFO' in line.upper()]
        
        # Build compressed log
        compressed_parts = []
        
        if errors:
            compressed_parts.append(f"ERRORS({len(errors)}): " + " | ".join(errors[:2]))
        
        if warnings:
            compressed_parts.append(f"WARNINGS({len(warnings)}): " + " | ".join(warnings[:2]))
        
        if infos and len(compressed_parts) == 0:  # Only if no errors/warnings
            compressed_parts.append(f"INFO({len(infos)}): " + " | ".join(infos[:3]))
        
        result = '\n'.join(compressed_parts)
        return result[:max_length] if result else self._compress_generic_output(output, max_length)
    
    def _compress_generic_output(self, output: str, max_length: int) -> str:
        """Generic compression: keep beginning and end."""
        if len(output) <= max_length:
            return output
        
        # Smart truncation: keep beginning and end
        keep_length = max_length // 2 - 20  # Reserve space for separator
        
        beginning = output[:keep_length].rsplit('\n', 1)[0]  # Don't cut mid-line
        ending = output[-keep_length:].split('\n', 1)[-1]   # Don't cut mid-line
        
        # Count omitted lines
        omitted_lines = output[len(beginning):-len(ending)].count('\n')
        
        return f"{beginning}\n... ({omitted_lines} lines omitted) ...\n{ending}"


# Global instance
code_compressor = CodeCompressor() 