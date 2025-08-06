from string import Template
from typing import List, Tuple
import random

from .base import BaseNode
from ..memory import Memory


class CriticNode(BaseNode):
    """
    CriticNode is a node that criticizes the answers from the plan and dev nodes.
    It is used to select the best trajectory from the plan and dev nodes.
    No memory is used for the critic node.
    """

    def __init__(self, model: str = "o4-mini"):
        super().__init__(
            role="critic", 
            model=model
        )
    
    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt with the task.
        """

        self.task = task
        self.procedural: Template = Memory("critic").get_procedural()
        self.init_prompt: str = self.procedural.safe_substitute(task=self.task)

    def __call__(self, histories: List[str]) -> Tuple[str, str, int]:
        """
        Criticize the answers from the plan and dev nodes.
        Current the critic node only supports 3 trajectories.
        
        Args:
            histories: List[str], the histories from the plan and dev nodes.

        Returns:
            Tuple of (final_answer, reason, best_id)
        """

        if len(histories) != 3:
            raise ValueError(f"{self.role} only supports 3 trajectories. Got {len(histories)}.")
        
        trajectory_mapping = {f"history_{idx}": history for idx, history in enumerate(histories)}
        prompt = Template(self.init_prompt).safe_substitute(**trajectory_mapping)
        
        response = self.forward(prompt=prompt)
        parsed_response = self._parse_response(response)

        final_answer = parsed_response.get("final_answer", "N/A")
        reason = parsed_response.get("reason", "N/A")

        try:
            best_id = int(parsed_response.get("best_id", 0))
            if best_id not in [0, 1, 2]:
                self.logger.warning(f"Selected best member index: {best_id} is not in [0, 1, 2].")
                best_id = random.randint(0, 2)

        except (ValueError, TypeError):
            self.logger.warning(f"Selected best member index: {parsed_response.get('best_id', 'N/A')} is not valid.")
            best_id = random.randint(0, 2)

        self.logger.info(f"Selected best member index: {best_id}")
        return final_answer, reason, best_id