from string import Template
from typing import Dict, List, Tuple

from .base import BaseNode
from ..utils import interpret_code
from ..config import config
from ..memory import Memory


class TestNode(BaseNode):
    """
    TestNode is a node that tests the code.
    It uses the code, the plan and the history to test the code.
    """

    def __init__(self, model: str = "claude-3-7-sonnet-v1", past_n: int = 4):
        super().__init__(
            role="tester",
            model=model
        )
        self.memory = Memory("tester")
        self.past_n = past_n

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()
        self.history: List[Dict[str, str]] = []

        self.init_prompt = self.procedural.safe_substitute(
            plan=self.plan,
        )
        self._init_counter()

    def __call__(self, h: Dict[str, str]) -> Tuple[str, str]:
        """
        Test the code.
        """

        self.logger.debug(f"{self.role} received history from {h['role']}")
        code_output = interpret_code(h["code"])

        # max_len = config.max_code_output_length
        # if len(code_output) > max_len:
        #     half = max_len // 2
        #     code_output = f"{code_output[:half]}...(truncated)...{code_output[-half:]}"
        # else:
        #     code_output = code_output

        prompt = Template(self.init_prompt).safe_substitute(
            history=self.export_history(past_n=self.past_n),
            code=h["code"],
            code_output=code_output
        )
        h["code_output"] = code_output
        self.add_history(h=h)

        response = self.forward(prompt=prompt)
        h = self.parse_response(response)
        self.add_history(h=h)
        h["code_output"] = code_output
        return h