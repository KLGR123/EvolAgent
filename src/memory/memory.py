import os
import re
import hashlib
from string import Template
from typing import Literal, Optional
from qdrant_client import QdrantClient

from .retrieve import Retriever
from .utils import split_content_blocks
from ..config import config
from ..utils.logger import get_logger, ComponentLoggers


class Memory:
    """
    Long-term Memory for the node with configuration-driven initialization.
    """
    _shared_client: Optional[QdrantClient] = None # TODO local client, remote client supporting concurrent

    def __init__(self, name: Literal["plan", "dev", "test", "critic"]):
        self.name = name
        self.logger = ComponentLoggers.get_memory_logger()
        
        if Memory._shared_client is None:
            qdrant_path = os.getenv("QDRANT_PERSIST_PATH") or config.qdrant_persist_path
            self.logger.info(f"Initializing Qdrant client at path: {qdrant_path}")
            Memory._shared_client = QdrantClient(path=qdrant_path)

        self.client = Memory._shared_client
        self.semantic_retriever = Retriever(client=self.client, name=name, type="semantic")
        self.episodic_retriever = Retriever(client=self.client, name=name, type="episodic")
        
        self.logger.debug(f"Initialized Memory for {name}")
        self._add_semantic()

    def get_procedural(self) -> Template:
        """
        Get the procedural prompt for the node.
        """
        with open(f"src/memory/{self.name}/procedural.md", "r") as f:
            return Template(f.read())

    def get_semantic(self, query: Optional[str] = None) -> str:
        """
        Get the semantic facts for the node.
        """
        if len(os.listdir(f"src/memory/{self.name}/semantic")) == 0:
            return ""
        if query is None:
            semantic = []
            for file in os.listdir(f"src/memory/{self.name}/semantic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.name}/semantic/{file}", "r") as f:
                        semantic.append(f.read())
            return "\n\n".join(semantic)
        else:
            self.logger.debug(f"Searching semantic memory for: {query[:100]}...")
            hits = self.semantic_retriever.search(query, limit=config.semantic_search_limit)
            self.logger.debug(f"Found {len(hits)} semantic results")
            
            # Combine text and code for the final output
            combined_results = []
            for hit in hits:
                result = hit.text
                if hit.code:  # If code exists, append it
                    result += f"\n\n```python\n{hit.code}\n```"
                combined_results.append(result)
            return "\n\n".join(combined_results)

    def get_episodic(self, query: Optional[str] = None) -> str:
        """
        Get the episodic for the node.
        """
        if len(os.listdir(f"src/memory/{self.name}/episodic")) == 0:
            return ""
        if query is None:
            episodic = []
            for file in os.listdir(f"src/memory/{self.name}/episodic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.name}/episodic/{file}", "r") as f:
                        episodic.append(f.read())
            return "\n\n".join(episodic)
        else:
            self.logger.debug(f"Searching episodic memory for: {query[:100]}...")
            hits = self.episodic_retriever.search(query, limit=config.episodic_search_limit)
            self.logger.debug(f"Found {len(hits)} episodic results")
            
            # Combine text and code for the final output
            combined_results = []
            for hit in hits:
                result = hit.text
                if hit.code:  # If code exists, append it
                    result += f"\n\n```python\n{hit.code}\n```"
                combined_results.append(result)
            return "\n\n".join(combined_results)

    def _add_semantic(self) -> None:
        """
        Add the semantic memory with code/text separation for better retrieval.
        Use content hash as ID to avoid duplicates.
        """
        semantic_texts = []
        semantic_codes = []
        semantic_ids = []
        
        for file in os.listdir(f"src/memory/{self.name}/semantic"):
            if file.endswith(".md"):
                with open(f"src/memory/{self.name}/semantic/{file}", "r") as f:
                    md_content = f.read()
                    # Use the new split_content_blocks function for better separation
                    content_blocks = split_content_blocks(md_content)
                    
                    for block_data in content_blocks:
                        text = block_data['text'].strip()
                        code = block_data['code']
                        
                        if text:  # Only add blocks with meaningful text content
                            # Use content hash of text (not including code) as ID to avoid duplicates
                            content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                            semantic_texts.append(text)
                            semantic_codes.append(code)
                            semantic_ids.append(content_hash)
        
        if semantic_texts:
            self.logger.info(f"Adding {len(semantic_texts)} semantic blocks to {self.name} memory")
            self.semantic_retriever.add(
                texts=semantic_texts, 
                ids=semantic_ids, 
                codes=semantic_codes
            )
        else:
            self.logger.debug(f"No semantic content found for {self.name}")

    def _clear_semantic(self) -> None:
        """
        Clear the semantic memory.
        """
        self.semantic_retriever.delete_all()

    def add_episodic(self, text: str) -> None:
        """
        Add the episodic memory with code/text separation for better retrieval.
        """
        import uuid
        from datetime import datetime

        episodic_dir = f"src/memory/{self.name}/episodic"
        os.makedirs(episodic_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.md"
        filepath = os.path.join(episodic_dir, filename)
        
        self.logger.debug(f"Saving episodic memory to: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        # Use content splitting for better indexing
        content_blocks = split_content_blocks(text)
        
        # If there are multiple blocks, process each separately
        if content_blocks:
            texts = []
            codes = []
            ids = []
            
            for i, block_data in enumerate(content_blocks):
                block_text = block_data['text'].strip()
                block_code = block_data['code']
                
                if block_text:  # Only add blocks with meaningful text content
                    # Create unique ID for each block within this episodic entry
                    block_hash = hashlib.md5(f"{text}_{i}_{block_text}".encode('utf-8')).hexdigest()
                    texts.append(block_text)
                    codes.append(block_code)
                    ids.append(block_hash)
            
            if texts:
                self.logger.info(f"Adding {len(texts)} episodic blocks to {self.name} memory")
                self.episodic_retriever.add(texts=texts, ids=ids, codes=codes)
        else:
            # Fallback for content that doesn't have clear structure
            self.logger.debug("Using fallback episodic storage for unstructured content")
            content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            self.episodic_retriever.add(texts=[text], ids=[content_hash], codes=[None])

    def clear_episodic(self) -> None:
        """
        Clear the episodic memory with logging.
        """
        import shutil

        self.logger.info(f"Clearing episodic memory for {self.name}")
        try:
            self.episodic_retriever.delete_all()
            episodic_dir = f"src/memory/{self.name}/episodic"
            if os.path.exists(episodic_dir):
                shutil.rmtree(episodic_dir)
                os.makedirs(episodic_dir, exist_ok=True)
            self.logger.debug(f"Episodic memory cleared successfully for {self.name}")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memory for {self.name}: {e}")

    def __repr__(self) -> str:
        return f"Memory(name={self.name})"