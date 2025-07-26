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
        role: str,
        model: str
    ):
        """
        Initialize the node with configuration and logging.
        """

        self.role: str = role
        self.model: str = model
        self.logger = get_logger(f"evolagent.node.{role}")

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        self.init_prompt: str = ""
        self.history: List[Dict[str, str]] = []
        self._last_history_token_counts = 0
    
        self.logger.debug(f"Initialized {role} node with model {model}")

    def _init_counter(self) -> None:
        """
        Initialize the token counter for the node.
        The counter is used to check if the prompt is too long.
        """

        _ = Template(self.init_prompt).safe_substitute(
            history=self.export_history(),
        )
        self._last_history_token_counts = len(self.encoding.encode(_))
    
    def _is_token_limit_exceeded(self, h: Dict[str, str]) -> bool:
        """
        Check if the history is too long using configured limits.
        """

        token_counts = len(self.encoding.encode(str(h)))
        limit_exceeded = self._last_history_token_counts + token_counts > config.max_history_tokens
        
        if limit_exceeded:
            self.logger.warning(f"Token limit approaching: {self._last_history_token_counts + token_counts} > {config.max_history_tokens}")
        
        return limit_exceeded
    
    def add_history(self, h: Dict[str, str]) -> None:
        """
        Add the history to the node with token tracking.
        """

        if self._is_token_limit_exceeded(h):
            self._maintain_history(h)
        else:
            self.history.append(h)
            self._last_history_token_counts += len(self.encoding.encode(str(h)))
            self.logger.debug(f"Added history entry from {h['role']}, with {len(self.encoding.encode(str(h)))} tokens")

    def _maintain_history(self, h: Dict[str, str]) -> None:
        """
        Maintain the history when token limit is exceeded.
        Achieved by either removing the oldest history or compressing the history.
        """

        self.logger.error(f"History token limit exceeded for {self.role} node")
        raise ValueError("Token limit exceeded - history compression not yet implemented")

    def forward(self, prompt: str) -> str:
        """
        Forward the prompt to the LLM API with error handling and logging.
        """

        try:
            self.logger.debug("Sending prompt to %s: %s...", self.model, prompt[:200] if len(prompt) > 200 else prompt)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.max_tokens,
                timeout=config.api_timeout,
                extra_headers={
                    'x-ms-client-request-id': "evolagent-"+str(uuid.uuid4()),
                }
            )
            
            if hasattr(response, "error"):
                self.logger.error(f"API returned error: {response.error['message']}")
                raise Exception(response.error['message'])
            
            result = response.choices[0].message.content or ""
            self.logger.debug("Received response from %s: %s...", self.model, result[:200])
            return result
            
        except Exception as e:
            self.logger.error(f"API call failed for {self.model}: {str(e)}")
            raise

    def parse_response(self, response: str) -> Dict[str, str]:
        """
        Parse the JSON response from the API response with enhanced error handling.
        """

        self.logger.debug("Parsing JSON response: %s...", response[:200])
        
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
            self.logger.debug("JSON parsed successfully using json_repair")
            
            # Check if 'role' field exists and matches expected role
            if "role" not in parsed_json:
                self.logger.warning(f"Missing 'role' field in response, setting to {self.role}")
                parsed_json["role"] = self.role
            elif parsed_json["role"] != self.role:
                self.logger.warning(f"Role mismatch: got '{parsed_json['role']}', expected '{self.role}', correcting it")
                parsed_json["role"] = self.role

            return parsed_json

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing failed for {self.role}: {str(e)}")
            self.logger.debug("Failed JSON content: %s", json_content)
            raise json.JSONDecodeError(f"{self.role}: JSON parsing failed, {str(e)}", json_content, e.pos)

    def __call__(self, h: Dict[str, str]) -> Dict[str, str]:
        """
        One single call for the node.
        """
        self.logger.debug(f"{self.role} received history from {h['role']}")
        self.add_history(h=h)

        prompt = Template(self.init_prompt).safe_substitute(history=self.export_history(past_n=self.past_n))
        response = self.forward(prompt=prompt)
        h = self.parse_response(response)
        self.add_history(h=h)
        return h

    def export_history(self, past_n: Optional[int] = None) -> str:
        """
        Export the history to a string with pretty format.

        Args:
            past_n: Optional[int], the number of history to export. If None, export all history.

        Returns:
            str, the history to export.
        """

        history_to_export = self.history[-past_n:] if past_n is not None and past_n > 0 else self.history

        def format_dict(d: Dict[str, str]) -> str:
            items = list(d.items())
            items.sort(key=lambda x: (0 if x[0] == "role" else 1))
            lines = ["{"]
            for k, v in items:
                lines.append(f'    "{k}": {repr(v)},')
            lines.append("}")
            return "\n".join(lines)

        if not history_to_export:
            return ""

        return "\n".join(format_dict(h) for h in history_to_export)

    def export_prompt(self) -> str:
        """
        Export the whole prompt with the history.
        """

        return Template(self.init_prompt).safe_substitute(
            history=self.export_history()
        )

    def __repr__(self):
        return f"Node(role={self.role}, model={self.model})"

    def __str__(self):
        return f"Node(role={self.role}, model={self.model})"


if __name__ == '__main__':
    llm = BaseNode(
        role="base", 
        model="anthropic.claude-sonnet-4-20250514-v1:0"
    )
    print(llm.export_prompt())
    print(llm)
