import os
import re
import json
import uuid
import tiktoken
import json_repair
from openai import OpenAI
from string import Template
from typing import Any, Dict, List, Literal, Optional
from dotenv import load_dotenv

from ..config import config
from ..utils.logger import get_logger

load_dotenv()


class BaseNode:
    """
    BaseNode is the base class for all the nodes.
    It provides the basic functionality for all the nodes.
    """

    def __init__(self, 
        name: str,
        model: str
    ):
        """
        Initialize the node with configuration and logging.
        """

        self.name: str = name
        self.model: str = model
        self.logger = get_logger(f"evolagent.node.{name}")
        
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        self.init_prompt: str = ""
        self.history: List[str] = []
        self._last_history_token_counts = 0
        
        self.logger.debug(f"Initialized {name} node with model {model}")

    def _is_token_limit_exceeded(self, h: str) -> bool:
        """
        Check if the history is too long using configured limits.
        """
        token_counts = len(self.encoding.encode(h))
        limit_exceeded = self._last_history_token_counts + token_counts > config.max_history_tokens
        
        if limit_exceeded:
            self.logger.warning(f"Token limit approaching: {self._last_history_token_counts + token_counts} > {config.max_history_tokens}")
        
        return limit_exceeded
    
    def _add_history(self, content: str, name: Literal["plan", "dev", "test", "critic", "task"]) -> None:
        """
        Add the history to the node with token tracking.
        """
        h = f"{name}: {content}"
        if self._is_token_limit_exceeded(h):
            self.logger.warning(f"History token limit exceeded, attempting maintenance")
            self._maintain_history(h)
        else:
            self.history.append(h)
            self._last_history_token_counts += len(self.encoding.encode(h))
            self.logger.debug(f"Added history entry from {name}: {content[:100]}... (tokens: {len(self.encoding.encode(h))})")

    def _maintain_history(self, h: str) -> None: # TODO compress the history, Mem0 style 
        """
        Maintain the history when token limit is exceeded.
        Achieved by either removing the oldest history or compressing the history.
        """
        self.logger.error(f"History token limit exceeded for {self.name} node")
        raise ValueError("Token limit exceeded - history compression not yet implemented")

    def _forward(self, prompt: str) -> str:
        """
        Forward the prompt to the LLM API with error handling and logging.
        """
        try:
            self.logger.debug(f"Sending prompt to {self.model}: {prompt[:200]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=64000,
                timeout=config.api_timeout,
                extra_headers={
                    'x-ms-client-request-id': "evolagent-"+str(uuid.uuid4()),
                }
            )
            
            if hasattr(response, "error"):
                self.logger.error(f"API returned error: {response.error['message']}")
                raise Exception(response.error['message'])
            
            result = response.choices[0].message.content or ""
            self.logger.debug(f"Received response from {self.model}: {result[:200]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"API call failed for {self.model}: {str(e)}")
            raise

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the JSON response from the API response with enhanced error handling.
        """
        self.logger.debug(f"Parsing JSON response: {response[:200]}...")
        
        json_pattern = r'```json\s*\n?(.*?)\n?```'
        matches = re.findall(json_pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            json_content = matches[0].strip()
            self.logger.debug("Found JSON in code block")
        else:
            json_content = response.strip()
            self.logger.debug("Using entire response as JSON")
            
        try:
            parsed_json = json_repair.loads(json_content)
            self.logger.debug("JSON parsed successfully")
            return parsed_json
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing failed for {self.name}: {str(e)}")
            self.logger.debug(f"Failed JSON content: {json_content}")
            raise json.JSONDecodeError(f"{self.name}: JSON parsing failed, {str(e)}", json_content, e.pos)

    def __call__(self) -> None:
        """
        One single call for the node.
        """
        pass

    def export_history(self, past_n: Optional[int] = None) -> str:
        """
        Export the history to a string with conversation markers for better model understanding.
        """
        history_to_export = self.history if past_n is None else self.history[-past_n:]
        
        if not history_to_export:
            return ""
        
        # Add conversation markers to enhance model understanding of dialogue structure
        formatted_history = []
        for entry in history_to_export:
            formatted_entry = f"<|im_start|>{entry}<|im_end|>"
            formatted_history.append(formatted_entry)
        
        return "\n".join(formatted_history)

    def export_prompt(self) -> str:
        """
        Export the whole prompt with the history.
        """

        return Template(self.init_prompt).safe_substitute(
            history="", 
            code="",
            code_output=""
        )

    def __repr__(self):
        return f"Node(name={self.name}, model={self.model})"

    def __str__(self):
        return f"Node(name={self.name}, model={self.model})"


if __name__ == '__main__':
    llm = BaseNode(
        name="base", 
        model="anthropic.claude-sonnet-4-20250514-v1:0"
    )
    print(llm.export_prompt())
    print(llm)
