from string import Template
from typing import List, Tuple
import random

from .base import BaseNode
from ..memory import Memory


class CriticNode(BaseNode):
    """
    CriticNode is a node that criticizes the answers from the plan and dev nodes.
    No memory is used.
    """

    def __init__(self, model: str = "o4-mini"):
        super().__init__(
            role="critic", 
            model=model
        )
    
    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt for the node, with the task.
        """

        self.task = task
        self.procedural: Template = Memory("critic").get_procedural()
        self.init_prompt: str = self.procedural.safe_substitute(task=self.task)

    def __call__(self, histories: List[str]) -> Tuple[str, str, int]:
        """
        Criticize the answers from the plan and dev nodes.
        Current the critic node only supports 3 trajectories.
        
        Returns:
            Tuple of (final_answer, reason, best_id)
        """

        try: 
            assert len(histories) == 3, "CriticNode only supports 3 trajectories."
        except AssertionError:
            raise ValueError(f"CriticNode only supports 3 trajectories. Got {len(histories)}.")
        
        prompt = Template(self.init_prompt).safe_substitute(
            history_0=histories[0],
            history_1=histories[1],
            history_2=histories[2],
        )
        response = self.forward(prompt=prompt)

        parsed_response = self.parse_response(response)
        final_answer = parsed_response["final_answer"] 
        reason = parsed_response["reason"] 

        try:
            best_id = int(parsed_response.get("best_id", 0))
            if best_id not in [0, 1, 2]:
                best_id = random.randint(0, 2)
        except (ValueError, TypeError):
            best_id = random.randint(0, 2)

        self.logger.info(f"CriticNode selected best member index: {best_id}")
        return final_answer, reason, best_id


if __name__ == "__main__":
    critic = CriticNode()
    critic._init_prompt(task="What is 10298412.121 + 123198005.12 equal to?")
    print(critic.export_prompt())