from string import Template
from typing import Dict, Optional, Tuple

from .base import BaseNode
from ..memory import Memory


class PlanNode(BaseNode):
    """
    PlanNode is a node that generates the next plan.
    It uses the procedural, semantic, episodic memories, the task and the history to generate the next plan.
    """

    def __init__(self, model: str = "o4-mini", past_n: int = 10):
        super().__init__(
            role="planner",
            model=model
        )
        self.memory = Memory("planner")
        self.past_n = past_n

    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.task = task
        self.procedural: Template = self.memory.get_procedural()

        try:
            self.episodic: str = self.memory.get_episodic(query=self.task) # TODO: augment task description
        except Exception as e:
            self.logger.warning(f"Failed to get episodic memory for {self.role} node: {str(e)}")
            self.episodic = ""

        self.init_prompt: str = self.procedural.safe_substitute(
            episodic=self.episodic,
            task=self.task
        )
        self._init_counter()

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, str], bool]:
        """
        Generate the next plan.
        """
        if h:
            self.logger.debug(f"{self.role} received history from {h['role']}")
            self.add_history(h=h)

        prompt = Template(self.init_prompt).safe_substitute(history=self.export_history(past_n=self.past_n))
        response = self.forward(prompt=prompt)
        h = self.parse_response(response)
        self.add_history(h=h)

        is_end = (h["plan"] == "<END>" or "<END>" in h["plan"])
        return h, is_end


if __name__ == "__main__":
    plan_node = PlanNode()
    plan_node._init_prompt(task="I want to learn about the history of the world")
    print(plan_node.export_history())