from copy import deepcopy
import os
import re
import json
import uuid
import tiktoken
import json_repair
import threading
import weakref
from openai import OpenAI
from string import Template
from typing import Any, Dict, List, Literal, Optional
from dotenv import load_dotenv

from ..config import config
from ..utils.logger import get_logger
from ..utils import HistoryMaintainer

load_dotenv()

# 全局OpenAI客户端池，线程安全
_client_pool = {}
_client_pool_lock = threading.Lock()


def get_shared_openai_client() -> OpenAI:
    """
    获取共享的OpenAI客户端实例，线程安全，避免重复创建连接。
    """
    thread_id = threading.get_ident()
    
    with _client_pool_lock:
        if thread_id not in _client_pool:
            _client_pool[thread_id] = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
                max_retries=3,
            )
        return _client_pool[thread_id]


def cleanup_openai_clients():
    """
    清理OpenAI客户端池，释放连接资源。
    """
    with _client_pool_lock:
        for client in _client_pool.values():
            try:
                # 关闭HTTP连接
                if hasattr(client, '_client') and hasattr(client._client, 'close'):
                    client._client.close()
            except:
                pass
        _client_pool.clear()


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

        # 使用共享的OpenAI客户端以减少连接数
        self.client = get_shared_openai_client()
        
        # 使用线程安全的tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        except Exception:
            # 备用编码器
            self.encoding = tiktoken.get_encoding("cl100k_base")
            
        self.init_prompt: str = ""
        self.history: List[Dict[str, str]] = []
        self._last_history_token_counts = 0
        
        # Initialize history maintainer
        self.history_maintainer = HistoryMaintainer(
            role=self.role,
            client=self.client,
            encoding=self.encoding
        )
        
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
    
    def add_history(self, h: Dict[str, str]) -> None:
        """
        Add the history to the node with token tracking and intelligent history maintenance.
        """
        # 深拷贝以避免外部修改影响内部状态
        history_copy = deepcopy(h)
        self.history.append(history_copy)
        
        # Update token count
        new_tokens = len(self.encoding.encode(str(history_copy)))
        self._last_history_token_counts += new_tokens
        
        # Check if maintenance is needed
        if self._last_history_token_counts > config.max_history_tokens:
            self.logger.warning(f"Token limit exceeded: {self._last_history_token_counts} > {config.max_history_tokens}")
            self.logger.info("Executing intelligent history maintenance")
            
            # Use history maintainer for intelligent maintenance
            maintained_history, new_token_count = self.history_maintainer.maintain_history(
                self.history, self._last_history_token_counts
            )
            
            # Update history and token count
            self.history = maintained_history
            self._last_history_token_counts = new_token_count
            
        self.logger.debug(f"Added history entry from {history_copy['role']}, current tokens: {self._last_history_token_counts}")

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
                temperature=config.temperature,
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

            if not isinstance(parsed_json, dict):
                if isinstance(parsed_json, list):
                    parsed_json = parsed_json[0]
                    self.logger.debug("Parsed a list of dicts, taking the first one")
                else:
                    self.logger.error(f"Invalid JSON format: {parsed_json}")
                    print(parsed_json)  # TODO: remove this
                    raise ValueError("Invalid JSON format")
            
            # Check if 'role' field exists and matches expected role
            if "role" not in parsed_json:
                self.logger.warning(f"Missing 'role' field in response, setting to {self.role}")
                parsed_json["role"] = self.role
            elif parsed_json["role"] != self.role:
                self.logger.warning(f"Role mismatch: got '{parsed_json['role']}', expected '{self.role}', correcting it")
                parsed_json["role"] = self.role

            # Validate and provide default values for required fields based on role
            self._validate_and_fix_required_fields(parsed_json)

            return parsed_json

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing failed for {self.role}: {str(e)}")
            self.logger.debug("Failed JSON content: %s", json_content)
            raise json.JSONDecodeError(f"{self.role}: JSON parsing failed, {str(e)}", json_content, e.pos)

    def _validate_and_fix_required_fields(self, parsed_json: Dict[str, str]) -> None:
        """
        Validate and provide default values for required fields based on node role.
        """

        if self.role == "developer":
            if "code" not in parsed_json:
                self.logger.warning("Missing 'code' field in developer response, setting empty code")
                parsed_json["code"] = "No code provided, please regenerate"
            if "description" not in parsed_json:
                self.logger.warning("Missing 'description' field in developer response, setting empty description")
                parsed_json["description"] = f"Response generated by {self.role} node"
        elif self.role == "planner":
            if "plan" not in parsed_json:
                self.logger.warning("Missing 'plan' field in planner response, setting empty plan")
                parsed_json["plan"] = ""
            if "description" not in parsed_json:
                self.logger.warning("Missing 'description' field in planner response, setting empty description")
                parsed_json["description"] = f"Response generated by {self.role} node"
        elif self.role == "tester":
            if "feedback" not in parsed_json:
                self.logger.warning("Missing 'feedback' field in tester response, setting default feedback")
                parsed_json["feedback"] = "No specific feedback provided"
            if "code_output" not in parsed_json:
                pass
                # self.logger.warning("Missing 'code_output' field in tester response, setting empty output")
                # parsed_json["code_output"] = ""
        elif self.role == "critic":
            if "final_answer" not in parsed_json:
                self.logger.warning("Missing 'final_answer' field in critic response, setting empty answer")
                parsed_json["final_answer"] = ""
            if "reason" not in parsed_json:
                self.logger.warning("Missing 'reason' field in critic response, setting default reason")
                parsed_json["reason"] = "No reasoning provided"

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        One single call for the node.
        """
        if h:
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

    def clear(self):
        """
        清理节点状态，释放内存。
        """
        self.history.clear()
        self._last_history_token_counts = 0
        
        # Reset history maintainer state
        self.history_maintainer.reset_compression_state()
        
        # 不直接关闭client，因为它是共享的
        # self.client 将在全局清理函数中处理

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
