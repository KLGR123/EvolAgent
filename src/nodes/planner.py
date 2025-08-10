from string import Template
from typing import Dict, Optional, Tuple

from .base import BaseNode
from ..memory import Memory


class PlanNode(BaseNode):
    """
    PlanNode generates the next plan, a.k.a. subintent of the task.
    It leverages the procedural, semantic, episodic memories, the task and the history to generate the next plan.
    """

    def __init__(self, model: str = "o4-mini", past_n: int = 10, model_index: Optional[int] = None):
        super().__init__(
            role="planner",
            model=model,
            model_index=model_index
        )
        self.memory: Memory = Memory("planner")
        self.past_n: int = past_n

    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt with the task.
        """

        self.task = task
        self.procedural: Template = self.memory.get_procedural()

        try:
            self.episodic: str = self.memory.get_episodic(query=self.task)
            self.logger.debug(f"Episodic memory is loaded.")
        except Exception as e:
            self.logger.warning(f"Failed to get episodic memory: {str(e)}")
            self.episodic = ""

        self.init_prompt: str = self.procedural.safe_substitute(
            episodic=self.episodic,
            task=self.task
        )
        self._init_counter()

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, str], bool]:
        """
        Generate the next plan, a.k.a. subintent of the task.
        
        Args:
            h: Optional[Dict[str, str]], the history from the previous node.

        Returns:
            Tuple[Dict[str, str], bool], the history and a boolean indicating if the plan is complete.
        """
            
        if h:
            self.logger.debug(f"Received history from {h['role']}")
            self.add_history(h=h)

        prompt = Template(self.init_prompt).safe_substitute(
            history=self.export_history(past_n=self.past_n)
        )
        response = self.forward(prompt=prompt)
        h = self._parse_response(response)
        self.add_history(h=h)

        is_end = (h["plan"] == "<END>" or "<END>" in h["plan"])
        return h, is_end