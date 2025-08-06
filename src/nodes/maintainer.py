"""
History Maintainer for Agent Nodes.

Provides intelligent history maintenance with dual-fallback mechanism:
1. Semantic compression of history items
2. Removal of oldest items if compression is insufficient

Features:
- Accurate token counting
- Compression state tracking
- Configuration-driven parameters
"""

import re
import ast
import json
import uuid
import tiktoken
from copy import deepcopy
from openai import OpenAI
from string import Template
from typing import Dict, List, Set, Optional, Tuple, Any

from ..config import config
from ..utils.logger import get_logger


class CodeCompressor:
    """
    Intelligent compressor for code and code output fields.
    """
    
    def __init__(self):
        self.logger = get_logger("code_compressor")
    
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


class HistoryMaintainer:
    """
    History maintainer with intelligent compression and fallback mechanisms.
    """
    
    def __init__(self, role: str, client: OpenAI, encoding: tiktoken.Encoding):
        """
        Initialize the history maintainer.
        
        Args:
            role: Node role (planner, developer, tester, critic)
            client: OpenAI client instance
            encoding: Tiktoken encoding for token counting
        """
        self.role = role
        self.client = client
        self.encoding = encoding
        self.logger = get_logger("history_maintainer")
        
        # Compression state tracking
        self._compressed_items: Set[int] = set()
        self._compression_templates: Dict[str, Template] = {}
        
        # Load compression templates
        self._load_compression_templates()
        self.code_compressor = CodeCompressor() 
    
    def _load_compression_templates(self) -> None:
        """Load unified compression template for all roles."""
        # Critic nodes don't need compression templates due to their simple usage pattern
        if self.role == "critic":
            self.logger.debug("Skipping compression template loading for critic node")
            return
        
        # Unified template that works for all text compression scenarios
        unified_template = Template("""
You are an expert content compressor. Your task is to create a concise summary that preserves all critical information while significantly reducing length.

**Context for reference**: $reference

**Content to compress**: $target

**Compression guidelines**:
- Preserve key facts, decisions, and outcomes
- Remove redundant explanations and verbose descriptions  
- Eliminate filler words and unnecessary elaboration
- Maintain technical accuracy and essential details
- Use concise, clear language

Return only the compressed result without additional explanation.
""".strip())
        
        # Use the same template for all roles - modern LLMs are smart enough to adapt
        for role in ["planner", "developer", "tester"]:
            self._compression_templates[role] = unified_template
        
        self.logger.debug("Loaded unified compression template for all roles")
    
    def maintain_history(self, history: List[Dict[str, str]], current_token_count: int) -> Tuple[List[Dict[str, str]], int]:
        """
        Maintain history using dual-fallback mechanism.
        
        Args:
            history: Current history list
            current_token_count: Current token count
            
        Returns:
            Tuple of (maintained_history, new_token_count)
        """
        if current_token_count <= config.max_history_tokens:
            return history, current_token_count
        
        # Critic nodes rarely need history maintenance due to their simple usage pattern
        if self.role == "critic":
            self.logger.debug("Critic node history maintenance skipped - critics typically have minimal history")
            return history, current_token_count
            
        self.logger.info(f"History maintenance triggered: {current_token_count} > {config.max_history_tokens}")
        
        # Deep copy to avoid modifying original
        working_history = deepcopy(history)
        working_token_count = current_token_count
        
        # Phase 1: Semantic compression
        working_history, working_token_count = self._compress_history(
            working_history, working_token_count
        )
        
        # Phase 2: Fallback removal if still over limit
        if working_token_count > config.max_history_tokens:
            working_history, working_token_count = self._remove_old_history(
                working_history, working_token_count
            )
        
        # Reset compression tracking if history structure changed significantly
        if len(working_history) != len(history):
            self._compressed_items.clear()
        
        self.logger.info(f"History maintenance completed: {working_token_count} tokens, {len(working_history)} items")
        return working_history, working_token_count
    
    def _compress_history(self, history: List[Dict[str, str]], token_count: int) -> Tuple[List[Dict[str, str]], int]:
        """
        Compress history items semantically.
        
        Args:
            history: History to compress
            token_count: Current token count
            
        Returns:
            Tuple of (compressed_history, new_token_count)
        """
        if not history:
            return history, token_count
            
        attempts = 0
        max_attempts = config.compression_max_attempts
        
        while (token_count > config.max_history_tokens 
               and attempts < max_attempts):
            
            compressed_any = False
            
            # Find uncompressed items to compress
            for i, history_item in enumerate(history):
                if i in self._compressed_items:
                    continue
                    
                if token_count <= config.max_history_tokens:
                    break
                
                # Try to compress this item
                original_tokens = len(self.encoding.encode(str(history_item)))
                compressed_item = self._compress_single_item(history_item)
                
                if compressed_item:
                    new_tokens = len(self.encoding.encode(str(compressed_item)))
                    token_saved = original_tokens - new_tokens
                    
                    if token_saved > config.compression_min_savings:
                        # Apply compression
                        history[i] = compressed_item
                        token_count -= token_saved
                        self._compressed_items.add(i)
                        compressed_any = True
                        
                        self.logger.debug(f"Compressed history item {i}, saved {token_saved} tokens")
                    else:
                        # Mark as attempted but not beneficial
                        self._compressed_items.add(i)
                        self.logger.debug(f"Compression of item {i} not beneficial, skipping")
                else:
                    # Mark as failed
                    self._compressed_items.add(i)
            
            if not compressed_any:
                # No more items can be compressed effectively
                break
                
            attempts += 1
        
        self.logger.debug(f"Compression phase completed after {attempts} attempts: {token_count} tokens")
        return history, token_count
    
    def _compress_single_item(self, history_item: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Compress a single history item.
        
        Args:
            history_item: History item to compress
            
        Returns:
            Compressed item or None if compression failed
        """
        try:
            # Determine what to compress based on the item content
            compress_target, reference_key = self._determine_compression_target(history_item)
            if not compress_target:
                return None
            
            # Get the appropriate compression template
            item_role = history_item.get('role', self.role)
            compress_template = self._compression_templates.get(item_role, self._compression_templates[self.role])
            
            # Perform compression
            target_key, target_content = next(iter(compress_target.items()))
            reference_content = history_item.get(reference_key, "")
            
            # Use specialized compression for code and output fields
            if target_key == 'code':
                compressed_content = code_compressor.compress_code(
                    target_content, 
                    target_reduction=config.code_target_reduction
                )
            elif target_key == 'code_output':
                compressed_content = code_compressor.compress_output(
                    target_content, 
                    max_length=config.output_max_length
                )
            else:
                # Use LLM compression for text fields
                compressed_content = self._llm_compress(
                    compress_template, reference_content, target_content
                )
            
            if compressed_content and len(compressed_content) < len(target_content):
                # Create compressed item
                compressed_item = deepcopy(history_item)
                compressed_item[target_key] = compressed_content
                return compressed_item
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to compress history item: {e}")
            return None
    
    def _determine_compression_target(self, history_item: Dict[str, str]) -> Tuple[Optional[Dict[str, str]], str]:
        """
        Determine what field to compress and what to use as reference.
        
        Args:
            history_item: History item to analyze
            
        Returns:
            Tuple of (target_dict, reference_key) or (None, "")
        """
        # Priority order for compression targets - code and output first (they consume most tokens)
        compression_candidates = [
            ('code', '', config.compression_min_length),           # Code compression (highest priority)
            ('code_output', '', config.compression_min_length // 2),  # Output compression (shorter threshold)
            ('description', 'code', config.compression_min_length),
            ('description', 'plan', config.compression_min_length),
            ('feedback', 'code_output', config.compression_min_length),
            # ('reason', 'final_answer', config.compression_min_length),
            ('plan', '', config.compression_min_length * 2),  # Plans can be longer
        ]
        
        for target_key, reference_key, min_length in compression_candidates:
            if (target_key in history_item 
                and len(history_item[target_key]) > min_length):
                
                # Use reference key if it exists, otherwise empty string
                ref_key = reference_key if reference_key in history_item else ''
                return {target_key: history_item[target_key]}, ref_key
        
        return None, ""
    
    def _llm_compress(self, template: Template, reference: str, target: str) -> Optional[str]:
        """
        Use LLM to compress content.
        
        Args:
            template: Compression prompt template
            reference: Reference content for context
            target: Content to compress
            
        Returns:
            Compressed content or None if failed
        """
        try:
            # Prepare messages
            system_prompt = (
                "You are a content compression expert. Your task is to create concise summaries "
                "that preserve all critical information while reducing length. "
                "Focus on key facts, decisions, and outcomes."
            )
            
            user_prompt = template.safe_substitute(
                reference=reference[:config.compression_reference_max_length],
                target=target
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Calculate target length for compression
            target_max_tokens = max(
                config.compression_min_output_tokens,
                min(len(target) // config.compression_target_ratio, config.compression_max_output_tokens)
            )
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=config.compression_model,
                messages=messages,
                max_tokens=target_max_tokens,
                temperature=config.compression_temperature,
                timeout=config.compression_timeout,
                extra_headers={
                    'x-ms-client-request-id': f"agent-compress-{uuid.uuid4()}"
                }
            )
            
            compressed_content = response.choices[0].message.content
            if compressed_content:
                return compressed_content.strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"LLM compression failed: {e}")
            return None
    
    def _remove_old_history(self, history: List[Dict[str, str]], token_count: int) -> Tuple[List[Dict[str, str]], int]:
        """
        Remove oldest history items as fallback mechanism.
        
        Args:
            history: History to trim
            token_count: Current token count
            
        Returns:
            Tuple of (trimmed_history, new_token_count)
        """
        if not history:
            return history, token_count
            
        removed_count = 0
        target_token_count = int(config.max_history_tokens * config.removal_target_ratio)
        
        while (history and token_count > target_token_count 
               and removed_count < config.removal_max_items):
            
            # Remove oldest item
            removed_item = history.pop(0)
            removed_tokens = len(self.encoding.encode(str(removed_item)))
            token_count -= removed_tokens
            removed_count += 1
            
            # Adjust compression tracking indices
            self._compressed_items = {i-1 for i in self._compressed_items if i > 0}
            
            self.logger.debug(f"Removed oldest history item, freed {removed_tokens} tokens")
        
        if removed_count > 0:
            self.logger.info(f"Removed {removed_count} oldest history items as fallback")
        
        return history, token_count
    
    def reset_compression_state(self) -> None:
        """Reset compression state tracking."""
        self._compressed_items.clear()
        self.logger.debug("Compression state reset")
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics."""
        return {
            "compressed_items_count": len(self._compressed_items),
            "compressed_items": list(self._compressed_items),
            "templates_loaded": list(self._compression_templates.keys())
        } 