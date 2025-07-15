from copy import deepcopy
from string import Template
from typing import Literal, Optional, Tuple

from .base import BaseNode

from ..memory import Memory


class DevNode(BaseNode):
    """
    DevNode is a node that develops the code.
    It uses the procedural, semantic, episodic memories, the task and the history to develop the code.
    """

    def __init__(self, model: str = "anthropic.claude-sonnet-4-20250514-v1:0"):
        super().__init__(
            name="dev", 
            model=model
        )
        self.memory = Memory("dev")
        self.last_code: str = ""

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()
        self.semantic: str = self.memory.get_semantic(query=self.plan)
        self.episodic: str = self.memory.get_episodic(query=self.plan)
        self.init_prompt: str = self.procedural.safe_substitute(
            semantic=self.semantic, 
            episodic=self.episodic,
            plan=self.plan
        )

        def _init_counter() -> None:
            """
            Initialize the token counter for the node.
            The counter is used to check if the prompt is too long.
            """

            _ = Template(self.init_prompt).substitute(history=self.export_history())
            self._last_history_token_counts = len(self.encoding.encode(_))

        _init_counter()
        self._add_history(content=self.plan, name="plan")

    def __call__(self, 
        content: Tuple[Optional[str], Optional[str]] = (None, None), # TODO: feedback and code_output
        name: Optional[Literal["plan", "dev", "test"]] = "test"
    ) -> Tuple[str, str]:
        """
        Develop the code.
        The history is the last 4 history.
        """

        if content[0] is not None and content[1] is not None and name is not None:
            self._add_history(content=content[0], name=name)
            self._add_history(content=content[1], name=name)

        prompt = Template(self.init_prompt).substitute(
            history=self.export_history(past_n=4) # TODO 2 code 1 code output 1 feedback?
        )
        response = self._forward(prompt=prompt)

        next_code = self._parse_json_response(response)["code"] # type: ignore
        description = self._parse_json_response(response)["description"] # type: ignore

        if "END" not in next_code:
            self.last_code = deepcopy(next_code)

        self._add_history(content=next_code, name="dev")
        return next_code, description

    def export_final_code(self) -> str:
        return self.last_code