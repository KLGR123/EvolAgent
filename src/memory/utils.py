"""
Memory utilities for EvolAgent.

This module provides embedding models, search result structures, and content processing
utilities for the memory system.
"""

import os
import re
import time
import tiktoken
import requests
import threading
import numpy as np
from deprecated import deprecated
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Any, Tuple
from fastembed import SparseTextEmbedding, SparseEmbedding
from openai import OpenAI

from ..utils.config import config

load_dotenv()


@dataclass
class SearchResult:
    """
    Structure for storing search results from memory retrieval.
    
    Attributes:
        id: Unique identifier for the result
        score: Relevance score from the search
        payload: Additional metadata
        text: Main text content
        code: Optional associated code block
    """
    id: str
    score: float
    payload: Dict[str, Any]
    text: str
    code: Optional[str] = None


class DenseEmbeddingModel:
    """
    Singleton dense embedding model using OpenAI's embedding API.
    Provides thread-safe text embedding with automatic retries and error handling.
    """
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls, model_name: str = "text-embedding-3-large"):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DenseEmbeddingModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, model_name: str = "text-embedding-3-large", dimension: int = None):
        """
        Initialize the dense embedding model.
        
        Args:
            model_name: OpenAI embedding model name
            dimension: Optional dimension limit for embeddings (None for full dimension)
        """
        # Only initialize once, even if __init__ is called multiple times
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.base_url = os.getenv("OPENAI_BASE_URL")
                    if self.base_url:
                        self.base_url = self.base_url.rstrip('/')
                    self.api_key = os.getenv("OPENAI_API_KEY")
                    self.model_name = model_name
                    self.dimension = dimension
                    # Initialize OpenAI client
                    if self.base_url:
                        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, max_retries=3)
                    else:
                        self.client = OpenAI(api_key=self.api_key, max_retries=3)
                    self._initialized = True

    @deprecated("Use embed_with_openai_sdk instead")
    def embed(self, texts: Union[str, List[str]], max_retries: int = 3, retry_delay: float = 1.0) -> List[List[float]]:
        """
        Generate dense embeddings for input texts.
        
        Args:
            texts: Single text or list of texts to embed
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries (exponential backoff)
            
        Returns:
            List of embedding vectors
            
        Raises:
            Exception: If all retry attempts fail
        """
        texts = [texts] if isinstance(texts, str) else texts
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": texts,
            "model": self.model_name
        }
        
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    f"{self.base_url}/embeddings",
                    json=payload,
                    headers=headers,
                    timeout=600
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("error"):
                    raise Exception(result["error"])

                embeddings = [item["embedding"] for item in result["data"]]

                # Cache dimension on first successful call
                if self.dimension is None and embeddings:
                    self.dimension = len(embeddings[0])
                    
                return embeddings
                
            except requests.RequestException as e:
                last_exception = e
                if attempt < max_retries:
                    print(f"Dense embedding API call failed on attempt {attempt + 1}/{max_retries + 1}: {e}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise Exception(f"Dense embedding API call failed after {max_retries + 1} attempts: {e}")
        
        # This line should never be reached, but included for type checking
        raise Exception(f"Dense embedding API call failed after {max_retries + 1} attempts: {last_exception}")

    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate dense embeddings using OpenAI SDK (alternative method).
        
        Args:
            texts: Single text or list of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            Exception: If embedding generation fails
        """
        if isinstance(texts, str):
            texts = [texts]
            
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=texts,
                encoding_format="float"
            )
            
            if hasattr(response, "error"):
                raise Exception(response.error)
                
            embeddings = [x.embedding for x in response.data]
            
            # Apply dimension limit if specified
            if self.dimension is not None:
                embeddings = [emb[:self.dimension] for emb in embeddings]
            
            # Cache dimension on first successful call
            if self.dimension is None and embeddings:
                self.dimension = len(embeddings[0])
                
            return embeddings
            
        except Exception as e:
            raise Exception(f"Dense embedding API call failed: {e}")
    
    def _normalize_l2(self, x: List[float]) -> List[float]:
        """
        Apply L2 normalization to a vector.
        
        Args:
            x: Input vector
            
        Returns:
            L2 normalized vector
        """
        x = np.array(x)
        if x.ndim == 1:
            norm = np.linalg.norm(x)
            if norm == 0:
                return x.tolist()
            return (x / norm).tolist()
        else:
            norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
            return np.where(norm == 0, x, (x / norm)).tolist()


class SparseEmbeddingModel:
    """
    Singleton sparse embedding model using FastEmbed.
    Provides efficient sparse vector representations for text retrieval.
    """
    
    _instance = None
    _lock = threading.Lock()
    _model = None
    _model_name = None
    
    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SparseEmbeddingModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, model_name: str = None):
        """
        Initialize the sparse embedding model.
        
        Args:
            model_name: FastEmbed sparse model name
        """
        if model_name is None:
            # Try to get from config using both methods for compatibility
            try:
                model_name = getattr(config, 'default_sparse_model', None)
                if model_name is None:
                    model_name = config.get('models.default_sparse_model', 'prithivida/Splade_PP_en_v1')
            except (AttributeError, KeyError):
                model_name = config.get('models.default_sparse_model', 'prithivida/Splade_PP_en_v1')
            
        # Only initialize the model once, even if __init__ is called multiple times
        if self._model is None or self._model_name != model_name:
            with self._lock:
                if self._model is None or self._model_name != model_name:
                    try:
                        self._model = SparseTextEmbedding(model_name=model_name)
                        self._model_name = model_name
                    except Exception as e:
                        raise Exception(f"Sparse embedding model {model_name} initialization failed: {e}")
        
    def embed(self, documents: Union[str, List[str]]) -> List[SparseEmbedding]:
        """
        Generate sparse embeddings for input documents.
        
        Args:
            documents: Single document or list of documents to embed
            
        Returns:
            List of sparse embeddings
            
        Raises:
            Exception: If embedding generation fails
        """
        try:
            if self._model is None:
                raise Exception("Sparse embedding model not initialized")
                
            if isinstance(documents, str):
                documents = [documents]
                
            sparse_embeddings = list(self._model.embed(documents))
            return sparse_embeddings
            
        except Exception as e:
            print(f"Sparse embedding failed: {e}")
            raise e


def split_content_blocks(content: str) -> List[Dict[str, str]]:
    """
    Split markdown content into structured blocks separating text from code.
    
    This function processes markdown content and extracts text descriptions
    along with associated code blocks for better indexing and retrieval.
    
    Args:
        content: Markdown content to split
        
    Returns:
        List of dictionaries with 'text' and 'code' keys
    """
    # Split content by markdown headers (### level)
    blocks = re.split(r'(?=^### )', content, flags=re.MULTILINE)
    result_blocks = []
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Extract code blocks from the current block
        code_pattern = r'```(?:\w+)?\n?(.*?)\n?```'
        code_matches = re.findall(code_pattern, block, re.DOTALL)
        
        # Remove code blocks from text to get clean description
        text_without_code = re.sub(code_pattern, '', block, flags=re.DOTALL)
        text_without_code = re.sub(r'\n\s*\n\s*\n+', '\n\n', text_without_code).strip()
        
        # Combine all code blocks
        combined_code = '\n\n'.join(code_matches) if code_matches else None
        
        result_blocks.append({
            'text': text_without_code,
            'code': combined_code
        })
    
    return result_blocks


def validate_token_length(text: str, max_tokens: int = 8192) -> Tuple[bool, int]:
    """
    Validate if text is within token limit using tiktoken.
    
    Args:
        text: Text to validate
        max_tokens: Maximum allowed tokens
        
    Returns:
        Tuple of (is_within_limit, actual_token_count)
    """
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        token_count = len(encoding.encode(text))
        return token_count <= max_tokens, token_count
    except Exception as e:
        # Fallback to character-based approximation
        approx_tokens = len(text) // 4  # Rough approximation
        return approx_tokens <= max_tokens, approx_tokens


def truncate_text_to_tokens(text: str, max_tokens: int = 8192) -> str:
    """
    Truncate text to fit within token limit.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum allowed tokens
        
    Returns:
        Truncated text that fits within the token limit
    """
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode(text)
        
        if len(tokens) <= max_tokens:
            return text
        
        # Truncate and decode back
        truncated_tokens = tokens[:max_tokens]
        return encoding.decode(truncated_tokens)
        
    except Exception as e:
        # Fallback to character-based truncation
        approx_char_limit = max_tokens * 4
        if len(text) <= approx_char_limit:
            return text
        return text[:approx_char_limit]