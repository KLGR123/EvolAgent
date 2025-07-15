from string import Template
from typing import List, Tuple

from .base import BaseNode
from ..memory import Memory


class CriticNode(BaseNode):
    """
    CriticNode is a node that criticizes the answers from the plan and dev nodes.
    No memory is used.
    """

    def __init__(self, model: str = "o4-mini"):
        super().__init__(
            name="critic", 
            model=model
        )
    
    def _init_prompt(self, task: str) -> None:
        """
        Initialize the prompt for the node, with the task.
        """

        self.task = task
        self.procedural: Template = Memory("critic").get_procedural()
        self.init_prompt: str = self.procedural.safe_substitute(task=self.task)

        def _init_counter() -> None:
            _ = Template(self.init_prompt).substitute(
                history_0="",
                history_1="",
                history_2="",
                answer_0="",
                answer_1="",
                answer_2=""
            )
            self._last_history_token_counts = len(self.encoding.encode(_))

        _init_counter()
        # self._add_history(content=self.task, name="task")

    def __call__(self, histories: List[str], answers: List[str]) -> Tuple[str, str]:
        """
        Criticize the answers from the plan and dev nodes.
        Current the critic node only supports 3 trajectories.
        """

        assert len(histories) == len(answers) == 3, "CriticNode only supports 3 trajectories."
        prompt = Template(self.init_prompt).substitute(
            history_0=histories[0],
            history_1=histories[1],
            history_2=histories[2],
            answer_0=answers[0],
            answer_1=answers[1],
            answer_2=answers[2]
        )
        response = self._forward(prompt=prompt)

        final_answer = self._parse_json_response(response)["final_answer"] # type: ignore
        reason = self._parse_json_response(response)["reason"] # type: ignore
        return final_answer, reason


if __name__ == "__main__":
    critic = CriticNode()
    critic._init_prompt(task="What is 10298412.121 + 123198005.12 equal to?")
    print(critic.export_prompt())