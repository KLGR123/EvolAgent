"""
History Maintainer for EvolAgent Nodes

Provides intelligent history maintenance with dual-fallback mechanism:
1. Semantic compression of history items
2. Removal of oldest items if compression is insufficient

Features:
- Accurate token counting
- Compression state tracking
- Configuration-driven parameters
- Thread-safe operations
"""

import os
import uuid
import threading
import tiktoken
from copy import deepcopy
from string import Template
from typing import Dict, List, Set, Optional, Tuple, Any
from openai import OpenAI

from ..config import config
from ..utils.logger import get_logger
from .code_compressor import code_compressor


class HistoryMaintainer:
    """
    Thread-safe history maintainer with intelligent compression and fallback mechanisms.
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
        self.logger = get_logger(f"evolagent.history_maintainer.{role}")
        
        # Compression state tracking
        self._compressed_items: Set[int] = set()
        self._compression_templates: Dict[str, Template] = {}
        self._compress_lock = threading.Lock()
        
        # Load compression templates
        self._load_compression_templates()
    
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
        with self._compress_lock:
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
                    'x-ms-client-request-id': f"evolagent-compress-{uuid.uuid4()}"
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
        with self._compress_lock:
            self._compressed_items.clear()
            self.logger.debug("Compression state reset")
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics."""
        return {
            "compressed_items_count": len(self._compressed_items),
            "compressed_items": list(self._compressed_items),
            "templates_loaded": list(self._compression_templates.keys())
        } 