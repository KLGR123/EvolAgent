from string import Template
from typing import Dict, Optional

from .base import BaseNode
from ..memory import Memory
from ..utils import python_interpreter


class TestNode(BaseNode):
    """
    TestNode interprets the code and tests the code.
    It leverages the procedural memories only, the plan and the history to test the code.
    """

    def __init__(self, model: str = "o4-mini", past_n: int = 4, model_index: Optional[int] = None):
        super().__init__(
            role="tester",
            model=model,
            model_index=model_index
        )
        self.memory: Memory = Memory("tester")
        self.past_n: int = past_n

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt with the plan.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()
        self.init_prompt = self.procedural.safe_substitute(
            plan=self.plan,
        )
        self._init_counter()

    def __call__(self, h: Dict[str, str]) -> Dict[str, str]:
        """
        Test the code based on code interpretation.
        Pass code output to the developer node.

        Args:
            h: Dict[str, str], the history from the previous node.

        Returns:
            Dict[str, str]
        """

        code_output: str = python_interpreter.execute(h["code"])

        prompt = Template(self.init_prompt).safe_substitute(
            history=self.export_history(past_n=self.past_n),
            code=h["code"],
            code_output=code_output
        )
        h["code_output"] = code_output
        self.add_history(h=h)

        response = self.forward(prompt=prompt)
        h = self._parse_response(response)
        
        self.add_history(h=h)
        h["code_output"] = code_output
        return h