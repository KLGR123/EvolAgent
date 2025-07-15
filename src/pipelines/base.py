from typing import Tuple
from ..memory import Memory


class BasePipeline:
    def __init__(self):
        self.plan_memory = Memory("plan")
        self.dev_memory = Memory("dev")

    def _forward(self, task: str, model: str = "o4-mini") -> Tuple[str, str]:
        return "", ""

    def __call__(self, task: str) -> None:
        pass

    def __repr__(self) -> str:
        return f"Pipeline(plan_memory={self.plan_memory}, dev_memory={self.dev_memory})"