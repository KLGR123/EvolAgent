from string import Template
from typing import Optional, Literal, Tuple

from .base import BaseNode
from ..utils import interpret_code
from ..memory import Memory


class TestNode(BaseNode):
    """
    TestNode is a node that tests the code.
    It uses the code, the plan and the history to test the code.
    """

    def __init__(self, model: str = "claude-3-7-sonnet-v1"):
        super().__init__(
            name="test",
            model=model
        )
        self.memory = Memory("test")

    def _interpret(self, code: str) -> None:
        """
        Interpret the code.
        """
        self.code = code
        self.code_output = interpret_code(code)

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()
        self.semantic: str = self.memory.get_semantic(query=self.plan)
        self.episodic: str = self.memory.get_episodic(query=self.plan)

        self.init_prompt = self.procedural.safe_substitute(
            semantic=self.semantic, 
            episodic=self.episodic,
            plan=self.plan,
        )

        def _init_counter() -> None:
            """
            Initialize the token counter for the node.
            The counter is used to check if the prompt is too long.
            """

            _ = Template(self.init_prompt).substitute(
                history=self.export_history(),
                code="",
                code_output=""
            )
            self._last_history_token_counts = len(self.encoding.encode(_))

        _init_counter()
        self._add_history(content=self.plan, name="plan")

    def __call__(self, 
        content: str,
        name: Literal["plan", "dev", "test"] = "dev"
    ) -> Tuple[str, str]:
        """
        Test the code.
        The history is the last 5 history.
        """

        self._add_history(content=content, name=name)
        self._interpret(code=content)

        prompt = Template(self.init_prompt).substitute(
            history=self.export_history(past_n=6), # TODO adaptive history length
            code=self.code,
            code_output=self.code_output
        )
        response = self._forward(prompt=prompt)
        feedback = self._parse_json_response(response)["feedback"] # type: ignore
        
        self._add_history(content=self.code_output, name="test")
        self._add_history(content=feedback, name="test")
        
        return feedback, self.code_output