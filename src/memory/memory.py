import os
import gc
import atexit
import threading
from string import Template
from typing import Literal, Optional
from qdrant_client import QdrantClient

from ..config import config
from .retrieve import Retriever
from ..utils.logger import get_logger
from .utils import split_content_blocks


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
    _active_retrievers = []  # Track active retriever instances

    def __init__(self, role: Literal["planner", "developer", "tester", "critic"]):
        """
        Initialize the memory for the node.
        """

        self.role = role
        self.logger = get_logger("agent.memory")
        
        # Thread-safe Qdrant client initialization
        with Memory._client_lock:
            if Memory._shared_client is None:
                qdrant_path = config.qdrant_persist_path
                self.logger.info(f"Initializing Qdrant client at path: {qdrant_path}")
                try:
                    Memory._shared_client = QdrantClient(path=qdrant_path)
                    # 注册清理函数，确保程序退出时正确关闭连接
                    atexit.register(Memory._cleanup_shared_client)
                except Exception as e:
                    self.logger.error(f"Failed to initialize Qdrant client: {e}")
                    raise

        self.client = Memory._shared_client
        
        # 初始化retriever实例，并跟踪它们以便后续清理
        if self.role in ["planner", "developer"]:
            self.semantic_retriever = Retriever(client=self.client, role=role, type="semantic")
            Memory._active_retrievers.append(self.semantic_retriever)
            
        if self.role in ["planner", "developer"]:  # Both planner and developer need episodic memory
            self.episodic_retriever = Retriever(client=self.client, role=role, type="episodic")
            Memory._active_retrievers.append(self.episodic_retriever)
        
        self.logger.debug(f"Initialized Memory for {role}")
        if self.role in ["planner", "developer"]:
            self._add_semantic()
            self._add_episodic()

    @classmethod
    def _cleanup_shared_client(cls):
        """
        清理共享的Qdrant客户端连接。
        """
        if cls._shared_client is not None:
            try:
                # 清理活跃的retriever引用
                cls._active_retrievers.clear()
                
                # 关闭Qdrant客户端连接
                if hasattr(cls._shared_client, 'close'):
                    cls._shared_client.close()
                cls._shared_client = None
                
                # 强制垃圾回收
                gc.collect()
                
            except Exception as e:
                # 在清理过程中不抛出异常
                pass

    def get_procedural(self) -> Template:
        """
        Get the procedural prompt for the node.
        """

        with open(f"src/memory/{self.role}/procedural.md", "r") as f:
            return Template(f.read())

    def get_semantic(self, query: Optional[str] = None) -> str:
        """
        Get the semantic facts for the node with enhanced error handling.
        """

        semantic_path = f"src/memory/{self.role}/semantic"
        
        if not os.path.exists(semantic_path) or len(os.listdir(semantic_path)) == 0:
            return ""

        if query is None:
            semantic = []

            for file in os.listdir(semantic_path):
                if file.endswith(".md"):
                    try:
                        with open(f"{semantic_path}/{file}", "r") as f:
                            semantic.append(f.read())
                    except Exception as e:
                        self.logger.warning(f"Failed to read semantic file {file}: {e}")

            return "\n\n".join(semantic)
        else:
            try:
                self.logger.debug(f"Searching semantic memory for: {query[:100]}...")
                if not hasattr(self, 'semantic_retriever'):
                    self.logger.warning("Semantic retriever not available for this role")
                    return ""
                    
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
            except Exception as e:
                self.logger.error(f"Error in semantic search: {e}")
                return ""

    def get_episodic(self, query: Optional[str] = None) -> str:
        """
        Get the episodic for the node with enhanced error handling.
        """

        episodic_path = f"src/memory/{self.role}/episodic"
        
        if not os.path.exists(episodic_path) or len(os.listdir(episodic_path)) == 0:
            return ""

        if query is None:
            episodic = []

            for file in os.listdir(episodic_path):
                if file.endswith(".md"):
                    try:
                        with open(f"{episodic_path}/{file}", "r") as f:
                            episodic.append(f.read())
                    except Exception as e:
                        self.logger.warning(f"Failed to read episodic file {file}: {e}")
                        
            return "\n\n".join(episodic)
        else:
            try:
                self.logger.debug(f"Searching episodic memory for: {query[:100]}...")
                if not hasattr(self, 'episodic_retriever'):
                    self.logger.warning("Episodic retriever not available for this role")
                    return ""
                    
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
            except Exception as e:
                self.logger.error(f"Error in episodic search: {e}")
                return ""

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

            semantic_path = f"src/memory/{self.role}/semantic"
            if not os.path.exists(semantic_path):
                self.logger.debug(f"No semantic content found for {self.role}")
                Memory._semantic_loaded[self.role] = True
                return
            
            try:
                for file in os.listdir(semantic_path):
                    if file.endswith(".md"):
                        try:
                            with open(f"{semantic_path}/{file}", "r") as f:
                                md_content = f.read()
                                content_blocks = split_content_blocks(md_content)
                                
                                for block_data in content_blocks:
                                    text = block_data['text'].strip()
                                    code = block_data['code']
                                    
                                    if text:  # Only add blocks with meaningful text content
                                        semantic_payloads.append({"text": text, "code": code})
                        except Exception as e:
                            self.logger.warning(f"Failed to process semantic file {file}: {e}")
                
                if semantic_payloads and hasattr(self, 'semantic_retriever'):
                    self.semantic_retriever.add(
                        payloads=semantic_payloads, 
                    )
                    # mark as loaded
                    Memory._semantic_loaded[self.role] = True
                    self.logger.debug(f"Added {len(semantic_payloads)} semantic blocks for {self.role}")
                else:
                    self.logger.debug(f"No semantic content found for {self.role}")
                    # even if there is no content, mark as loaded to avoid repeated checks for empty directories
                    Memory._semantic_loaded[self.role] = True
                    
            except Exception as e:
                self.logger.error(f"Error adding semantic memory for {self.role}: {e}")
                Memory._semantic_loaded[self.role] = True  # 标记为已加载，避免重复尝试

    def _clear_semantic(self) -> None:
        """
        Clear the semantic memory.
        Thread-safe implementation.
        """
        with Memory._semantic_lock:
            try:
                if hasattr(self, 'semantic_retriever'):
                    self.semantic_retriever.delete_all()
                # reset loading state, allowing re-loading
                Memory._semantic_loaded[self.role] = False
            except Exception as e:
                self.logger.error(f"Error clearing semantic memory for {self.role}: {e}")

    def _add_episodic(self) -> None:
        """
        Add the episodic memory with code/text separation for better retrieval.
        """
    
        with Memory._episodic_lock:
            if Memory._episodic_loaded.get(self.role, False):
                self.logger.debug(f"Episodic content already loaded for {self.role}, skipping")
                return
             
            episodic_payloads = []

            episodic_path = f"src/memory/{self.role}/episodic"
            if not os.path.exists(episodic_path):
                self.logger.debug(f"No episodic content found for {self.role}")
                Memory._episodic_loaded[self.role] = True
                return
            
            try:
                for file in os.listdir(episodic_path):
                    if file.endswith(".md"):
                        try:
                            with open(f"{episodic_path}/{file}", "r") as f:
                                md_content = f.read()
                                content_blocks = split_content_blocks(md_content)
                                
                                for block_data in content_blocks:
                                    text = block_data['text'].strip()
                                    code = block_data['code']
                                    
                                    if text:  # Only add blocks with meaningful text content
                                        # Use content hash of text (not including code) as ID to avoid duplicates
                                        episodic_payloads.append({"text": text, "code": code})
                        except Exception as e:
                            self.logger.warning(f"Failed to process episodic file {file}: {e}")
                
                if episodic_payloads and hasattr(self, 'episodic_retriever'):
                    self.episodic_retriever.add(
                        payloads=episodic_payloads, 
                    )
                    # mark as loaded
                    Memory._episodic_loaded[self.role] = True
                    self.logger.debug(f"Added {len(episodic_payloads)} episodic blocks for {self.role}")
                else:
                    self.logger.debug(f"No episodic content found for {self.role}")
                    # even if there is no content, mark as loaded to avoid repeated checks for empty directories
                    Memory._episodic_loaded[self.role] = True
                    
            except Exception as e:
                self.logger.error(f"Error adding episodic memory for {self.role}: {e}")
                Memory._episodic_loaded[self.role] = True  # 标记为已加载，避免重复尝试

    def add_episodic(self, text: str) -> None:
        """
        Add the episodic memory with code/text separation for better retrieval.
        """
        import uuid
        from datetime import datetime

        try:
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
            if content_blocks and hasattr(self, 'episodic_retriever'):
                payloads = []
                
                for i, block_data in enumerate(content_blocks):
                    block_text = block_data['text'].strip()
                    block_code = block_data['code']
                    
                    if block_text:  # Only add blocks with meaningful text content
                        payloads.append({"text": block_text, "code": block_code})
                
                if payloads:
                    self.logger.info(f"Adding {len(payloads)} episodic blocks to {self.role} memory")
                    self.episodic_retriever.add(payloads=payloads)
            elif hasattr(self, 'episodic_retriever'):
                # Fallback for content that doesn't have clear structure
                self.logger.debug("Using fallback episodic storage for unstructured content")
                self.episodic_retriever.add(payloads=[{"text": text, "code": None}])
            else:
                self.logger.warning("Episodic retriever not available for this role")
                
        except Exception as e:
            self.logger.error(f"Failed to add episodic memory: {e}")

    def clear_episodic(self) -> None:
        """
        Clear the episodic memory with logging.
        """
        import shutil

        self.logger.info(f"Clearing episodic memory for {self.role}")
        try:
            if hasattr(self, 'episodic_retriever'):
                self.episodic_retriever.delete_all()
                
            episodic_dir = f"src/memory/{self.role}/episodic"
            if os.path.exists(episodic_dir):
                shutil.rmtree(episodic_dir)
                os.makedirs(episodic_dir, exist_ok=True)
                
            # 重置加载状态
            with Memory._episodic_lock:
                Memory._episodic_loaded[self.role] = False
                
            self.logger.debug(f"Episodic memory cleared successfully for {self.role}")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memory for {self.role}: {e}")

    def cleanup(self):
        """
        清理当前Memory实例的资源。
        """
        try:
            # 从活跃列表中移除retriever引用
            if hasattr(self, 'semantic_retriever') and self.semantic_retriever in Memory._active_retrievers:
                Memory._active_retrievers.remove(self.semantic_retriever)
            if hasattr(self, 'episodic_retriever') and self.episodic_retriever in Memory._active_retrievers:
                Memory._active_retrievers.remove(self.episodic_retriever)
                
            # 清理retriever实例
            if hasattr(self, 'semantic_retriever'):
                del self.semantic_retriever
            if hasattr(self, 'episodic_retriever'):
                del self.episodic_retriever
                
        except Exception as e:
            self.logger.warning(f"Error during memory cleanup: {e}")

    def __repr__(self) -> str:
        return f"Memory(role={self.role})"
        
    def __del__(self):
        """
        Destructor to ensure proper cleanup.
        """

        try:
            self.cleanup()
        except:
            pass