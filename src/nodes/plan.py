from string import Template
from typing import Literal, Optional, Tuple
from qdrant_client import QdrantClient

from .base import BaseNode
from ..memory import Memory


class PlanNode(BaseNode):
    """
    PlanNode is a node that generates the next plan.
    It uses the procedural, semantic, episodic memories, the task and the history to generate the next plan.
    """

    def __init__(self, model: str = "o4-mini"):
        super().__init__(
            name="plan",
            model=model
        )
        self.memory = Memory("plan")

    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.task = task
        self.procedural: Template = self.memory.get_procedural()
        self.semantic: str = self.memory.get_semantic(query=self.task)
        self.episodic: str = self.memory.get_episodic(query=self.task)
        self.init_prompt: str = self.procedural.safe_substitute(
            semantic=self.semantic, 
            episodic=self.episodic,
            task=self.task
        )

        def _init_counter() -> None:
            """
            Initialize the token counter for the node.
            The counter is used to check if the prompt is too long.
            """

            _ = Template(self.init_prompt).substitute(history=self.export_history())
            self._last_history_token_counts = len(self.encoding.encode(_))

        _init_counter()
        self._add_history(content=self.task, name="task")

    def __call__(self, 
        content: Optional[str] = None, 
        name: Optional[Literal["plan", "dev", "test"]] = "dev"
    ) -> Tuple[str, str]:
        """
        Generate the next plan.
        """

        if content is not None and name is not None:
            self._add_history(content=content, name=name)

        prompt = Template(self.init_prompt).substitute(history=self.export_history(past_n=10)) # TODO adaptive history length
        response = self._forward(prompt=prompt)

        next_plan = self._parse_json_response(response)["plan"] # type: ignore
        reason = self._parse_json_response(response)["reason"] # type: ignore

        self._add_history(content=next_plan, name="plan")
        return next_plan, reason


if __name__ == "__main__":
    plan_node = PlanNode()
    plan_node._init_prompt(task="I want to learn about the history of the world")
    print(plan_node.export_history())