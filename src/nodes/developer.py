from copy import deepcopy
from string import Template
from typing import Dict, List, Optional, Tuple

from .base import BaseNode
from ..memory import Memory


class DevNode(BaseNode):
    """
    DevNode is a node that develops the code.
    It uses the procedural, semantic, episodic memories, the task and the history to develop the code.
    """

    def __init__(self, model: str = "anthropic.claude-sonnet-4-20250514-v1:0", past_n: int = 4):
        super().__init__(
            role="developer", 
            model=model
        )
        self.memory = Memory("developer")
        self.past_n = past_n
        self.plan_code_trajectory = []

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt for the node.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()
        self.history: List[Dict[str, str]] = []

        try:
            self.semantic: str = self.memory.get_semantic(query=self.plan)
        except Exception as e:
            self.logger.warning(f"Failed to get semantic memory for {self.role} node: {str(e)}")
            self.semantic = ""

        try:
            self.episodic: str = self.memory.get_episodic(query=self.plan)
        except Exception as e:
            self.logger.warning(f"Failed to get episodic memory for {self.role} node: {str(e)}")
            self.episodic = ""

        self.init_prompt: str = self.procedural.safe_substitute(
            semantic=self.semantic, 
            episodic=self.episodic,
            plan=self.plan
        )
        self._init_counter()

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, str], bool]:
        """
        Develop the code.
        """
        if h:
            self.logger.debug(f"{self.role} received history from {h['role']}")
            self.add_history(h=h)

        prompt = Template(self.init_prompt).safe_substitute(
            history=self.export_history(past_n=self.past_n)
        )
        response = self.forward(prompt=prompt)
        h = self.parse_response(response)
        self.add_history(h=h)

        code = deepcopy(h["code"])
        is_end = (code == "<END>" or "<END>" in code)
        
        # Record all plan-code pairs during development, not just at the end
        if code and code != "<END>":
            self.plan_code_trajectory.append({
                "plan": self.plan,
                "code": code,
            })

        return h, is_end

    def export_plan_code_trajectory(self) -> List[Dict[str, str]]:
        """
        Export the plan code trajectory.
        """
        return self.plan_code_trajectory