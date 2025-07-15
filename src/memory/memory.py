import os
import re
import hashlib
from string import Template
from typing import Literal, Optional
from qdrant_client import QdrantClient

from .retrieve import Retriever


class Memory:
    """
    Long-term Memory for the node.
    """
    _shared_client: Optional[QdrantClient] = None # TODO local client, remote client supporting concurrent

    def __init__(self, name: Literal["plan", "dev", "test", "critic"]):
        self.name = name
        if Memory._shared_client is None:
            Memory._shared_client = QdrantClient(path=os.getenv("QDRANT_PERSIST_PATH"))

        self.client = Memory._shared_client
        self.semantic_retriever = Retriever(client=self.client, name=name, type="semantic")
        self.episodic_retriever = Retriever(client=self.client, name=name, type="episodic")
        self._add_semantic()

    def get_procedural(self) -> Template:
        """
        Get the procedural prompt for the node.
        """
        with open(f"src/memory/{self.name}/procedural.md", "r") as f:
            return Template(f.read())

    def get_semantic(self, query: Optional[str] = None, augment: bool = False) -> str:
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
            hits = self.semantic_retriever.search(query, limit=3, augment=augment)
            return "\n\n".join([hit.text for hit in hits])

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
            hits = self.episodic_retriever.search(query, limit=3) # TODO limit refinement
            return "\n\n".join([hit.text for hit in hits])

    def _add_semantic(self) -> None:
        """
        Add the semantic memory.
        Use content hash as ID to avoid duplicates.
        """
        semantic_blocks = []
        semantic_ids = []
        
        for file in os.listdir(f"src/memory/{self.name}/semantic"):
            if file.endswith(".md"):
                with open(f"src/memory/{self.name}/semantic/{file}", "r") as f:
                    md_content = f.read()
                    blocks = re.split(r'(?=^### )', md_content, flags=re.MULTILINE)
                    for block in blocks:
                        block = block.strip()
                        if block:
                            # Use content hash as ID to avoid duplicates
                            content_hash = hashlib.md5(block.encode('utf-8')).hexdigest()
                            semantic_blocks.append(block)
                            semantic_ids.append(content_hash)
        
        if semantic_blocks:
            self.semantic_retriever.add(texts=semantic_blocks, ids=semantic_ids)

    def _clear_semantic(self) -> None:
        """
        Clear the semantic memory.
        """
        self.semantic_retriever.delete_all()

    def add_episodic(self, text: str) -> None: # TODO selective modes: header + description only; w. code
        """
        Add the episodic memory.
        """
        import uuid
        from datetime import datetime

        episodic_dir = f"src/memory/{self.name}/episodic"
        os.makedirs(episodic_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.md"
        filepath = os.path.join(episodic_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        self.episodic_retriever.add(texts=[text], ids=[content_hash])

    def clear_episodic(self) -> None:
        """
        Clear the episodic memory.
        """
        import shutil

        self.episodic_retriever.delete_all()
        episodic_dir = f"src/memory/{self.name}/episodic"
        if os.path.exists(episodic_dir):
            shutil.rmtree(episodic_dir)
            os.makedirs(episodic_dir, exist_ok=True)