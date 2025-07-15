import os
import re
import json
import uuid
import tiktoken
from openai import OpenAI
from string import Template
from typing import Any, Dict, List, Literal, Optional
from dotenv import load_dotenv

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
        Initialize the node.
        """

        self.name: str = name
        self.model: str = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        self.init_prompt: str = ""
        self.history: List[str] = []
        self._last_history_token_counts = 0

    def _is_token_limit_exceeded(self, h: str) -> bool:
        """
        Check if the history is too long.
        """

        token_counts = len(self.encoding.encode(h))
        return self._last_history_token_counts + token_counts > 199999
    
    def _add_history(self, content: str, name: Literal["plan", "dev", "test", "critic", "task"]) -> None:
        """
        Add the history to the node.
        """

        h = f"{name}: {content}"
        if self._is_token_limit_exceeded(h):
            self._maintain_history(h)
        else:
            self.history.append(h)
            self._last_history_token_counts += len(self.encoding.encode(h))

    def _maintain_history(self, h: str) -> None: # TODO compress the history, Mem0 style 
        """
        Maintain the history
        Achieved by either removing the oldest history or compressing the history.
        """
        raise ValueError("Token limit exceeded")

    def _forward(self, prompt: str) -> str:
        """
        Forward the prompt to the LLM api.
        """
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [{"role": "user", "content": prompt}],
            max_tokens = 64000,
            extra_headers = {
                'x-ms-client-request-id': "evolagent-"+str(uuid.uuid4()),
            }
        )
        return response.choices[0].message.content # type: ignore

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the JSON response from the api response.
        """
        json_pattern = r'```json\s*\n?(.*?)\n?```'
        matches = re.findall(json_pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            json_content = matches[0].strip()
        else:
            json_content = response.strip()
        try:
            parsed_json = json.loads(json_content)
            return parsed_json
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"{self.name}: JSON parsing failed, {str(e)}", json_content, e.pos)

    def __call__(self) -> None:
        """
        One single call for the node.
        """
        pass

    def export_history(self, past_n: Optional[int] = None) -> str:
        """
        Export the history to a string.
        """

        if past_n is None:
            return "\n".join(self.history)
        else:
            return "\n".join(self.history[-past_n:])

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
