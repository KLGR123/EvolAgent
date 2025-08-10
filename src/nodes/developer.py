from copy import deepcopy
from string import Template
from typing import Dict, List, Optional, Tuple

from .base import BaseNode
from ..memory import Memory


class DevNode(BaseNode):
    """
    DevNode develops the code based on the plan, a.k.a. subintent of the task.
    It leverages the procedural, semantic, episodic memories, the task and the history to develop the code.
    """

    def __init__(self, model: str = "o4-mini", past_n: int = 4, model_index: Optional[int] = None):
        super().__init__(
            role="developer", 
            model=model,
            model_index=model_index
        )
        self.memory: Memory = Memory("developer")
        self.past_n: int = past_n
        self._dev_trajectory: List[Dict[str, str]] = []

    def _init_prompt(self, plan: str) -> None:
        """
        Initialize the prompt with the plan.
        """

        self.plan = plan
        self.procedural: Template = self.memory.get_procedural()

        try:
            self.semantic: str = self.memory.get_semantic(query=self.plan)
            self.logger.debug(f"Semantic memory is loaded.")
        except Exception as e:
            self.logger.warning(f"Failed to get semantic memory: {str(e)}")
            self.semantic = ""

        try:
            self.episodic: str = self.memory.get_episodic(query=self.plan)
            self.logger.debug(f"Episodic memory is loaded.")
        except Exception as e:
            self.logger.warning(f"Failed to get episodic memory: {str(e)}")
            self.episodic = ""

        self.init_prompt: str = self.procedural.safe_substitute(
            semantic=self.semantic, 
            episodic=self.episodic,
            plan=self.plan
        )
        self._init_counter()

    def __call__(self, h: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, str], bool]:
        """
        Develop the code based on the plan, a.k.a. subintent of the task.
        
        Args:
            h: Optional[Dict[str, str]], the history from the previous node.

        Returns:
            Tuple[Dict[str, str], bool], the history and a boolean indicating if the code is complete.
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
        
        code = deepcopy(h["code"]) if h["code"] else ""
        is_end = (code == "<END>" or "<END>" in code)

        if not is_end:
            self.logger.debug(f"Developed code: {code}")
            self._dev_trajectory.append({
                "plan": deepcopy(self.plan),
                "code": code,
            })

        return h, is_end

    @property
    def dev_trajectory(self) -> List[Dict[str, str]]:
        """
        Export the (plan, code) trajectory for learning.
        The trajectory is a list of dictionaries, each containing a plan and code.
        """
        return self._dev_trajectory