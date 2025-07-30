import os
import hashlib
import threading
from string import Template
from typing import Literal, Optional
from qdrant_client import QdrantClient

from .retrieve import Retriever
from .utils import split_content_blocks
from ..config import config
from ..utils.logger import ComponentLoggers


class Memory:
    """
    Long-term Memory for the node with configuration-driven initialization.
    """

    _shared_client: Optional[QdrantClient] = None
    _semantic_loaded: dict[str, bool] = {}
    _semantic_lock = threading.Lock()  # Thread lock for semantic loading
    _client_lock = threading.Lock()  # Thread lock for client initialization
    _episodic_loaded: dict[str, bool] = {}
    _episodic_lock = threading.Lock()  # Thread lock for episodic loading

    def __init__(self, role: Literal["planner", "developer", "tester", "critic"]):
        """
        Initialize the memory for the node.
        """

        self.role = role
        self.logger = ComponentLoggers.get_memory_logger()
        
        # Thread-safe Qdrant client initialization
        with Memory._client_lock:
            if Memory._shared_client is None:
                qdrant_path = config.qdrant_persist_path
                self.logger.info(f"Initializing Qdrant client at path: {qdrant_path}")
                Memory._shared_client = QdrantClient(path=qdrant_path)

        self.client = Memory._shared_client
        if self.role in ["planner", "developer"]:
            self.semantic_retriever = Retriever(client=self.client, role=role, type="semantic")
        if self.role in ["planner", "developer"]:  # Both planner and developer need episodic memory
            self.episodic_retriever = Retriever(client=self.client, role=role, type="episodic")
        
        self.logger.debug(f"Initialized Memory for {role}")
        if self.role in ["planner", "developer"]:
            self._add_semantic()
            self._add_episodic()

    def get_procedural(self) -> Template:
        """
        Get the procedural prompt for the node.
        """

        with open(f"src/memory/{self.role}/procedural.md", "r") as f:
            return Template(f.read())

    def get_semantic(self, query: Optional[str] = None) -> str:
        """
        Get the semantic facts for the node.
        """

        if len(os.listdir(f"src/memory/{self.role}/semantic")) == 0:
            return ""

        if query is None:
            semantic = []

            for file in os.listdir(f"src/memory/{self.role}/semantic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.role}/semantic/{file}", "r") as f:
                        semantic.append(f.read())

            return "\n\n".join(semantic)
        else:
            self.logger.debug(f"Searching semantic memory for: {query[:100]}...")
            hits = self.semantic_retriever.search(query,
                method=config.search_method,
                score_threshold=config.score_threshold, 
                limit=config.semantic_search_limit
            )
            self.logger.debug(f"Found {len(hits)} semantic results")

            combined_results = []

            for hit in hits:
                result = hit.text
                if hit.code:  # If code exists, append it
                    result += f"\n\n```\n{hit.code}\n```"

                combined_results.append(result)

            return "\n\n".join(combined_results)

    def get_episodic(self, query: Optional[str] = None) -> str:
        """
        Get the episodic for the node.
        """

        if len(os.listdir(f"src/memory/{self.role}/episodic")) == 0:
            return ""

        if query is None:
            episodic = []

            for file in os.listdir(f"src/memory/{self.role}/episodic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.role}/episodic/{file}", "r") as f:
                        episodic.append(f.read())
                        
            return "\n\n".join(episodic)
        else:
            self.logger.debug(f"Searching episodic memory for: {query[:100]}...")
            hits = self.episodic_retriever.search(query, 
                method=config.search_method,
                score_threshold=config.score_threshold, 
                limit=config.episodic_search_limit
            )
            self.logger.debug(f"Found {len(hits)} episodic results")

            combined_results = []

            for hit in hits:
                result = hit.text
                if hit.code:
                    result += f"\n\n```\n{hit.code}\n```"

                combined_results.append(result)

            return "\n\n".join(combined_results)

    def _add_semantic(self) -> None:
        """
        Add the semantic memory with code/text separation for better retrieval.
        Use content hash as ID to avoid duplicates.
        Thread-safe implementation.
        """
    
        with Memory._semantic_lock:
            if Memory._semantic_loaded.get(self.role, False):
                self.logger.debug(f"Semantic content already loaded for {self.role}, skipping")
                return
             
            semantic_payloads = []

            if not os.path.exists(f"src/memory/{self.role}/semantic"):
                self.logger.debug(f"No semantic content found for {self.role}")
                Memory._semantic_loaded[self.role] = True
                return
            
            for file in os.listdir(f"src/memory/{self.role}/semantic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.role}/semantic/{file}", "r") as f:
                        md_content = f.read()
                        content_blocks = split_content_blocks(md_content)
                        
                        for block_data in content_blocks:
                            text = block_data['text'].strip()
                            code = block_data['code']
                            
                            if text:  # Only add blocks with meaningful text content
                                semantic_payloads.append({"text": text, "code": code})
            
            if semantic_payloads:
                self.semantic_retriever.add(
                    payloads=semantic_payloads, 
                )
                # mark as loaded
                Memory._semantic_loaded[self.role] = True
            else:
                self.logger.debug(f"No semantic content found for {self.role}")
                # even if there is no content, mark as loaded to avoid repeated checks for empty directories
                Memory._semantic_loaded[self.role] = True

    def _clear_semantic(self) -> None:
        """
        Clear the semantic memory.
        Thread-safe implementation.
        """
        with Memory._semantic_lock:
            self.semantic_retriever.delete_all()
            # reset loading state, allowing re-loading
            Memory._semantic_loaded[self.role] = False

    def _add_episodic(self) -> None:
        """
        Add the episodic memory with code/text separation for better retrieval.
        """
    
        with Memory._episodic_lock:
            if Memory._episodic_loaded.get(self.role, False):
                self.logger.debug(f"Episodic content already loaded for {self.role}, skipping")
                return
             
            episodic_payloads = []

            if not os.path.exists(f"src/memory/{self.role}/episodic"):
                self.logger.debug(f"No episodic content found for {self.role}")
                Memory._episodic_loaded[self.role] = True
                return
            
            for file in os.listdir(f"src/memory/{self.role}/episodic"):
                if file.endswith(".md"):
                    with open(f"src/memory/{self.role}/episodic/{file}", "r") as f:
                        md_content = f.read()
                        content_blocks = split_content_blocks(md_content)
                        
                        for block_data in content_blocks:
                            text = block_data['text'].strip()
                            code = block_data['code']
                            
                            if text:  # Only add blocks with meaningful text content
                                # Use content hash of text (not including code) as ID to avoid duplicates
                                episodic_payloads.append({"text": text, "code": code})
            
            if episodic_payloads:
                self.episodic_retriever.add(
                    payloads=episodic_payloads, 
                )
                # mark as loaded
                Memory._episodic_loaded[self.role] = True
            else:
                self.logger.debug(f"No episodic content found for {self.role}")
                # even if there is no content, mark as loaded to avoid repeated checks for empty directories
                Memory._episodic_loaded[self.role] = True

    def add_episodic(self, text: str) -> None:
        """
        Add the episodic memory with code/text separation for better retrieval.
        """
        import uuid
        from datetime import datetime

        episodic_dir = f"src/memory/{self.role}/episodic"
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
            payloads = []
            
            for i, block_data in enumerate(content_blocks):
                block_text = block_data['text'].strip()
                block_code = block_data['code']
                
                if block_text:  # Only add blocks with meaningful text content
                    payloads.append({"text": block_text, "code": block_code})
            
            if payloads:
                self.logger.info(f"Adding {len(payloads)} episodic blocks to {self.role} memory")
                self.episodic_retriever.add(payloads=payloads)
        else:
            # Fallback for content that doesn't have clear structure
            self.logger.debug("Using fallback episodic storage for unstructured content")
            self.episodic_retriever.add(payloads=[{"text": text, "code": None}])

    def clear_episodic(self) -> None:
        """
        Clear the episodic memory with logging.
        """
        import shutil

        self.logger.info(f"Clearing episodic memory for {self.role}")
        try:
            self.episodic_retriever.delete_all()
            episodic_dir = f"src/memory/{self.role}/episodic"
            if os.path.exists(episodic_dir):
                shutil.rmtree(episodic_dir)
                os.makedirs(episodic_dir, exist_ok=True)
            self.logger.debug(f"Episodic memory cleared successfully for {self.role}")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memory for {self.role}: {e}")

    def __repr__(self) -> str:
        return f"Memory(role={self.role})"