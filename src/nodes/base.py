import os
import json
import uuid
import atexit
import tiktoken
import threading
from copy import deepcopy
from openai import OpenAI
from dotenv import load_dotenv
from string import Template
from contextlib import contextmanager
from typing import Dict, List, Optional

from ..utils.config import config
from ..utils.logger import get_logger
from ..utils import parse_llm_response
from .maintainer import HistoryMaintainer

load_dotenv()


class OpenAIClientPool:
    """
    OpenAI client pool, providing thread-safe client management.
    Using singleton pattern to ensure a global unique instance.
    """
    
    _instance: Optional['OpenAIClientPool'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'OpenAIClientPool':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._clients: Dict[int, OpenAI] = {}
                    cls._instance._pool_lock = threading.Lock()
                    cls._instance._config = {
                        'api_key': os.getenv("OPENAI_API_KEY"),
                        'base_url': os.getenv("OPENAI_BASE_URL"),
                        'max_retries': 3
                    }
        return cls._instance
    
    def get_client(self) -> OpenAI:
        """
        Get the OpenAI client instance for the current thread.
        If the current thread doesn't have a client, create a new one.
        
        Returns:
            OpenAI: The OpenAI client instance for the current thread
        """
        
        thread_id = threading.get_ident()
        
        with self._pool_lock:
            if thread_id not in self._clients:
                self._clients[thread_id] = OpenAI(**self._config)
            return self._clients[thread_id]
    
    def cleanup(self) -> None:
        """
        Clean up all the client connections, release resources.
        Usually called when the program exits.
        """
        with self._pool_lock:
            for client in self._clients.values():
                try:
                    if hasattr(client, '_client') and hasattr(client._client, 'close'):
                        client._client.close()
                except Exception as e:
                    print(f"Error cleaning up OpenAI client: {e}")
            self._clients.clear()
    
    @contextmanager
    def client_context(self):
        """
        Context manager, providing safe access to the client.
        
        Usage:
            with openai_pool.client_context() as client:
                response = client.chat.completions.create(...)
        """
        client = self.get_client()
        try:
            yield client
        except Exception as e:
            raise e
    
    def get_pool_stats(self) -> Dict[str, int]:
        """
        Get the connection pool statistics.
        
        Returns:
            Dict[str, int]: A dictionary containing the number of active connections and thread IDs
        """
        with self._pool_lock:
            return {
                'active_connections': len(self._clients),
                'thread_ids': list(self._clients.keys())
            }


# Global client pool instance and cleanup function
OPENAI_CLIENT_POOL = OpenAIClientPool()
atexit.register(OPENAI_CLIENT_POOL.cleanup)


class BaseNode:
    """
    BaseNode creates a node for the LLM API.
    It is used to create all the nodes.

    Usage:
        node = BaseNode(role="developer", model="gpt-4o-mini")
        node("What is the capital of France?")
        node.clear()
    """

    def __init__(self, 
        role: str,
        model: str
    ):
        """
        Initialize the node with configuration and logging.

        Args:
            role: The role of the node, which is used to determine the type of the node.
            model: The model to use for the node.
        """

        self.role: str = role
        self.model: str = model
        self.logger = get_logger(f"agent.node.{role.lower()}")
        self.client = OPENAI_CLIENT_POOL.get_client()
        
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        except Exception:
            self.encoding = tiktoken.get_encoding("cl100k_base")
            
        self.init_prompt: str = ""
        self.history: List[Dict[str, str]] = []
        self._last_history_tokens = 0
        
        self.history_maintainer = HistoryMaintainer()
        self.history_maintainer.client = self.client
        self.logger.debug(f"Initialized {role} node with model {model}")

    def _init_counter(self) -> None:
        """
        Initialize the token counter for the node.
        The counter is used to check if the prompt is too long.
        """

        _ = Template(self.init_prompt).safe_substitute(
            history=self.export_history(),
        )
        self._last_history_tokens = len(self.encoding.encode(_))
    
    def add_history(self, h: Dict[str, str]) -> None:
        """
        Add the history to the node with token tracking and intelligent history maintenance.

        Args:
            h: The history to add, a dictionary with "role" and other fields, 
            like "plan", "code", "description", "feedback", etc.
        """

        history_copy = deepcopy(h)
        self.history.append(history_copy)
        
        new_tokens = len(self.encoding.encode(str(history_copy)))
        self._last_history_tokens += new_tokens
        
        max_history_tokens = config.get('nodes.max_history_tokens', 184320)
        if self._last_history_tokens > max_history_tokens:
            self.logger.warning(f"Token limit exceeded: {self._last_history_tokens} > {max_history_tokens}")
            self.logger.info("Executing history maintenance")

            maintained_history, new_token_count = self.history_maintainer.maintain_history(
                self.history, self._last_history_tokens
            )
            self.history = maintained_history
            self._last_history_tokens = new_token_count
            
        self.logger.debug(f"Added history entry from {history_copy['role']}, current tokens: {self._last_history_tokens}")

    def forward(self, prompt: str) -> str:
        """
        Forward the prompt to the LLM API with error handling and logging.

        Args:
            prompt: The prompt to forward, a string.

        Returns:
            The response from the LLM API, a string.
        """

        try:
            self.logger.debug(f"{self.role} forward sending prompt to {self.model}: {prompt[:200]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                            max_tokens=config.get('models.max_tokens', 32000),
            timeout=config.get('timeout.api_timeout', 800),
            temperature=config.get('models.temperature', 0.7),
                extra_headers={
                    'x-ms-client-request-id': "evolagent-"+str(uuid.uuid4()),
                },
                extra_body={
                    'erp': 'liujiarun.1'
                }
            )
            
            if hasattr(response, "error"):
                self.logger.error(f"{self.role} forward returned error: {response.error['message']}")
                raise Exception(response.error['message'])
            
            result = response.choices[0].message.content
            self.logger.debug(f"{self.role} forward received response from {self.model}: {result[:200]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"{self.role} forward failed for {self.model}: {str(e)}")
            raise

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        One single call for the node.
        It will add the history from the caller to the node, forward the prompt to the LLM API, 
        parse the response, and add the history from the node to the caller.

        Args:
            h: The history to add, a dictionary with "role" and other fields, 
            like "plan", "code", "description", "feedback", etc.

        Returns:
            The parsed JSON, a dictionary.
        """
        if h:
            self.logger.debug(f"{self.role} received history from {h['role']}")
            self.add_history(h=h)

        prompt = Template(self.init_prompt).safe_substitute(
            history=self.export_history(past_n=self.past_n)
        )
        response = self.forward(prompt=prompt)
        h = self._parse_response(response)
        self.add_history(h=h)
        return h

    def _parse_response(self, response: str) -> Dict[str, str]:
        """
        Parse the response from the LLM API.
        """
        return parse_llm_response(response, self.role, self.logger)

    @staticmethod
    def _format_dict(d: Dict[str, str]) -> str: 
        """
        Format the history to a string with pretty format
        """

        items = list(d.items())
        items.sort(key=lambda x: (0 if x[0] == "role" else 1))
        lines = ["{"]
        for k, v in items:
            lines.append(f'    "{k}": {repr(v)},')
        lines.append("}")
        return "\n".join(lines)

    def export_history(self, past_n: Optional[int] = None) -> str:
        """
        Export the history to a string with pretty format.
        Used when prompt is generated, so that the LLM can see the history.

        Args:
            past_n: Optional[int], the last n history to export. If None, export all history.

        Returns:
            str, the formatted history.
        """

        if not self.history:
            return ""

        if past_n is not None and past_n > 0:
            history_to_export = self.history[-past_n:]
        else:
            history_to_export = self.history

        history_str = "\n".join(self._format_dict(h) for h in history_to_export)
        return history_str

    def clear(self):
        """
        Clear the node state, release memory.
        Do not directly close client, it is shared and will be handled in the global cleanup function.
        """

        self.history.clear()
        self._last_history_tokens = 0
        self.history_maintainer.reset_compression_state()
        
    def __repr__(self):
        return f"Node(role={self.role}, model={self.model})"

    def __str__(self):
        return f"Node(role={self.role}, model={self.model})"