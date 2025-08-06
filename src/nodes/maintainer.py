"""
History Maintainer for Agent Nodes.

This module provides history maintenance functionality including compression
and removal strategies for managing conversation history within token limits.
"""

import re
from typing import Dict, List, Optional, Tuple, Any

from ..utils.config import config
from ..utils.logger import get_logger


class HistoryMaintainer:
    """
    Manages conversation history maintenance through compression and removal.
    
    Provides token-aware history management to keep conversations within
    configured limits while preserving important context.
    """
    
    def __init__(self):
        """Initialize the history maintainer."""
        self.logger = get_logger("history_maintainer")
        self.client = None  # Will be set by the node that uses this maintainer
    
    def compress_code(self, code: str, target_reduction: float = None) -> Optional[str]:
        """
        Compress code while preserving functionality and readability.
        
        Uses specialized compression techniques for code including:
        - Comment removal and optimization
        - Whitespace normalization
        - Variable name shortening (when safe)
        
        Args:
            code: Original code string
            target_reduction: Target reduction ratio (0.5 = 50% reduction)
            
        Returns:
            Compressed code or None if compression failed
        """
        compression_min_length = config.get('compression.compression_min_length', 100)
        if not code or len(code) < compression_min_length:
            return None
            
        try:
            # Remove excessive whitespace and comments
            lines = code.split('\n')
            compressed_lines = []
            
            for line in lines:
                # Remove comments but preserve docstrings
                if line.strip().startswith('#'):
                    continue
                    
                # Normalize whitespace
                compressed_line = re.sub(r'\s+', ' ', line.strip())
                if compressed_line:
                    compressed_lines.append(compressed_line)
            
            compressed = '\n'.join(compressed_lines)
            
            # Calculate compression ratio
            original_length = len(code)
            compressed_length = len(compressed)
            
            if compressed_length < original_length * 0.8:  # At least 20% reduction
                self.logger.debug(f"Code compressed: {original_length} -> {compressed_length} chars")
                return compressed
            
            return None
            
        except Exception as e:
            self.logger.error(f"Code compression failed: {e}")
            return None
    
    def compress_text(self, 
                     text: str, 
                     target_reduction: float = None,
                     max_length: int = None,
                     reference: str = "") -> Optional[str]:
        """
        Compress text content using LLM-based summarization.
        
        Uses the configured compression model to intelligently summarize
        text while preserving key information and context.
        
        Args:
            text: Original text to compress
            target_reduction: Target reduction ratio (0.5 = 50% reduction)
            max_length: Maximum length for compressed text
            reference: Reference text for context-aware compression
            
        Returns:
            Compressed text or None if compression failed
        """
        compression_min_length = config.get('compression.compression_min_length', 100)
        if not text or len(text) < compression_min_length:
            return None
            
        if not self.client:
            self.logger.warning("No client available for text compression")
            return None
            
        try:
            # Build compression prompt
            prompt_parts = [
                "Compress the following text while preserving key information and context:",
                f"Original text: {text}"
            ]
            
            if reference:
                compression_reference_max_length = config.get('compression.compression_reference_max_length', 500)
                prompt_parts.append(f"Reference context: {reference[:compression_reference_max_length]}")
            
            if target_reduction:
                prompt_parts.append(f"Target: Reduce length by approximately {target_reduction*100:.0f}%")
            
            if max_length:
                prompt_parts.append(f"Maximum length: {max_length} characters")
            
            prompt_parts.extend([
                "Requirements:",
                "- Preserve essential information and meaning",
                "- Use concise, clear language", 
                "- Maintain logical flow and structure",
                "- Remove redundant or less important details"
            ])
            
            prompt = "\n".join(prompt_parts)
            
            # Calculate token limits
            compression_min_output_tokens = config.get('compression.compression_min_output_tokens', 50)
            compression_target_ratio = config.get('compression.compression_target_ratio', 3)
            compression_max_output_tokens = config.get('compression.compression_max_output_tokens', 1000)
            
            max_tokens = max(
                compression_min_output_tokens,
                min(len(text) // compression_target_ratio, compression_max_output_tokens)
            )
            
            # Call compression API
            response = self.client.chat.completions.create(
                model=config.get('compression.model', 'gpt-4.1'),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=config.get('compression.temperature', 0.1),
                timeout=config.get('compression.timeout', 600),
            )
            
            compressed = response.choices[0].message.content
            if compressed and len(compressed) < len(text):
                compression_ratio = len(compressed) / len(text)
                self.logger.debug(f"Text compressed: {len(text)} -> {len(compressed)} chars (ratio: {compression_ratio:.2f})")
                return compressed.strip()
                
            return None
            
        except Exception as e:
            self.logger.error(f"Text compression failed: {e}")
            return None
    
    def maintain_history(self, history: List[Dict[str, Any]], 
                        current_tokens: int) -> Tuple[List[Dict[str, Any]], int]:
        """
        Maintain conversation history within token limits.
        
        Uses a combination of compression and selective removal to keep
        history within configured token limits while preserving important context.
        
        Args:
            history: List of conversation entries
            current_tokens: Current token count
            
        Returns:
            Tuple of (maintained_history_list, new_token_count)
        """
        max_history_tokens = config.get('nodes.max_history_tokens', 184320)
        
        if not history:
            return history
        
        # Check if maintenance is needed
        if current_tokens <= max_history_tokens:
            return history
        
        self.logger.info(f"History maintenance triggered: {current_tokens} > {max_history_tokens}")
        
        # Create working copy
        working_history = history.copy()
        working_token_count = current_tokens
        
        # Phase 1: Compression
        if working_token_count > max_history_tokens:
            working_history, working_token_count = self._compress_history_entries(
                working_history, working_token_count
            )
        
        # Phase 2: Selective removal if still over limit
        if working_token_count > max_history_tokens:
            working_history, working_token_count = self._remove_history_entries(
                working_history, working_token_count
            )
        
        self.logger.info(f"History maintenance completed: {len(history)} -> {len(working_history)} entries, "
                        f"{current_tokens} -> {working_token_count} tokens")
        
        return working_history, working_token_count
    
    def _compress_history_entries(self, history: List[Dict[str, Any]], 
                                 current_tokens: int) -> Tuple[List[Dict[str, Any]], int]:
        """Compress individual history entries to reduce token count."""
        max_history_tokens = config.get('nodes.max_history_tokens', 184320)
        compression_max_attempts = config.get('compression.compression_max_attempts', 10)
        
        compressed_history = []
        token_count = current_tokens
        max_attempts = compression_max_attempts
        attempts = 0
        
        while (token_count > max_history_tokens 
               and attempts < max_attempts 
               and compressed_history != history):
            
            attempts += 1
            compressed_history = []
            entries_compressed = 0
            
            for entry in history:
                compressed_entry = self._compress_single_entry(entry.copy())
                compressed_history.append(compressed_entry)
                
                if compressed_entry != entry:
                    entries_compressed += 1
            
            # Recalculate token count (simplified estimation)
            if token_count <= max_history_tokens:
                break
                
            # Estimate token savings (rough approximation)
            if entries_compressed > 0:
                compression_min_savings = config.get('compression.compression_min_savings', 1000)
                estimated_savings = entries_compressed * compression_min_savings
                token_count -= estimated_savings
                if estimated_savings > compression_min_savings:
                    self.logger.debug(f"Compression attempt {attempts}: {entries_compressed} entries compressed")
            
            history = compressed_history
        
        return compressed_history, token_count
    
    def _compress_single_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Compress a single history entry based on its content."""
        
        # Define compression priorities and thresholds for different field types
        compression_min_length = config.get('compression.compression_min_length', 100)
        
        compression_targets = [
            ('code', '', compression_min_length),           # Code compression (highest priority)
            ('code_output', '', compression_min_length // 2),  # Output compression (shorter threshold)
            ('description', 'code', compression_min_length),
            ('description', 'plan', compression_min_length),
            ('feedback', 'code_output', compression_min_length),
            # ('reason', 'final_answer', compression_min_length),
            ('plan', '', compression_min_length * 2),  # Plans can be longer
        ]
        
        for field, reference_field, min_length in compression_targets:
            if field in entry and len(str(entry[field])) >= min_length:
                reference = str(entry.get(reference_field, "")) if reference_field else ""
                
                if field == 'code':
                    # Use specialized code compression
                    code_target_reduction = config.get('compression.code_target_reduction', 0.5)
                    compressed = self.compress_code(
                        entry[field], 
                        target_reduction=code_target_reduction
                    )
                else:
                    # Use text compression
                    output_max_length = config.get('compression.output_max_length', 500)
                    compression_reference_max_length = config.get('compression.compression_reference_max_length', 500)
                    compressed = self.compress_text(
                        entry[field],
                        reference=reference[:compression_reference_max_length],
                        max_length=output_max_length
                    )
                
                if compressed:
                    entry[field] = compressed
                    
        return entry
    
    def _remove_history_entries(self, history: List[Dict[str, Any]], 
                               current_tokens: int) -> Tuple[List[Dict[str, Any]], int]:
        """Remove less important history entries to meet token limits."""
        
        if len(history) <= 2:  # Keep at least recent entries
            return history, current_tokens
        
        max_history_tokens = config.get('nodes.max_history_tokens', 184320)
        removal_target_ratio = config.get('compression.removal_target_ratio', 0.8)
        removal_max_items = config.get('compression.removal_max_items', 10)
        
        # Target token count (80% of limit to provide buffer)
        target_token_count = int(max_history_tokens * removal_target_ratio)
        
        # Remove entries from middle of history (preserve recent and oldest)
        removed_count = 0
        working_history = history.copy()
        
        while (current_tokens > target_token_count 
               and len(working_history) > 2 
               and removed_count < removal_max_items):
            
            # Remove from middle (keep first and last few entries)
            middle_index = len(working_history) // 2
            removed_entry = working_history.pop(middle_index)
            removed_count += 1
            
            # Estimate token reduction (simplified)
            estimated_tokens = len(str(removed_entry)) // 4  # Rough token estimation
            current_tokens -= estimated_tokens
        
        if removed_count > 0:
            self.logger.debug(f"Removed {removed_count} history entries to meet token limits")
        
        return working_history, current_tokens 