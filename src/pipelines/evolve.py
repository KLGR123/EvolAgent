import os
from tqdm import tqdm
from openai import OpenAI
from typing import Tuple, Optional, List
# from concurrent.futures import ThreadPoolExecutor, as_completed TODO add concurrent

from .base import BasePipeline
from ..nodes import CriticNode, TestNode, DevNode, PlanNode


class EvolvePipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )

    def _forward(self, 
        task: str, 
        model: str = "o4-mini",
    ) -> Tuple[str, str]: # TODO better logging, supporting concurrent
        """
        Forward the task, sample one trajectory.
        """
        self.task = task

        self.plan_node = PlanNode(model=model)
        self.dev_node = DevNode(model=model)
        self.test_node = TestNode(model=model)
        self.critic_node = CriticNode(model=model)
        
        self.plan_node._init_prompt(task=task)
        self.critic_node._init_prompt(task=task)

        description = None
        reason = None
        
        while True:
            plan, reason = self.plan_node(content=description, name="dev")
            print("Plan-Plan: ", plan)
            print("Plan-Reason: ", reason)
            print("-"*50)
            if "END" in plan:
                break
            
            self.dev_node._init_prompt(plan=plan)
            self.test_node._init_prompt(plan=plan)

            feedback, code_output = None, None
            while True:
                code, description = self.dev_node(content=(feedback, code_output), name="test")
                print("Dev-Description: ", description)
                if "END" in code:
                    print("Dev: END")
                    break

                feedback, code_output = self.test_node(content=code, name="dev")
                print("Test-Feedback: ", feedback)
                print("\n")
        
        history = self.plan_node.export_history(past_n=4)
        answer = reason
        return history, answer

    def __call__(self, # TODO better logging, supporting concurrent
        task: str,
        models: List[str] = ["o4-mini", "gpt-4o", "gpt-4o-mini"], 
    ) -> str:
        """
        Evolve the task, use three parallel trajectories and judge them with the critic node.
        """
        histories, answers = [], []
                
        for model in tqdm(models):
            print(f"Pipeline: {model} started")
            history, answer = self._forward(task, model)
            histories.append(history)
            answers.append(answer)
            print(f"Pipeline: {model} completed")

        final_answer, reason = self.critic_node(histories=histories, answers=answers)
        print("Critic-Reason: ", reason)
        print("\n")
        return final_answer

    def learn(self) -> None: # TODO contrastive learning, leveraging failed trajectories
        """
        Learn from the past experiences, save the successful experiences to the long-term memory.
        """ 
        self._save_plan_episodic()
        self._save_dev_episodic()
        print("Pipeline: Successfully saved the experiences to the long-term memory.")
    
    def _summarize_task(self, task: str) -> str:
        response = self.client.chat.completions.create(
            model = "o4-mini",
            messages = [{"role": "user", "content": f"Summarize the task into a title within 15 words: {task}"}],
            max_tokens = 1000,
            temperature = 0.1,
        )
        return response.choices[0].message.content # type: ignore

    def _save_plan_episodic(self) -> None:
        title = self._summarize_task(self.task)
        history = self.plan_node.export_history()
        content = f"### {title}\n\n```\n{history}\n```\n"
        self.plan_memory.add_episodic(content)

    def _save_dev_episodic(self, remove_code: bool = True) -> None:
        title = self._summarize_task(self.task)
        code = self.dev_node.export_final_code()
        if remove_code:
            content = f"### {title}\n\n{self.task}\n\n"
        else:
            content = f"### {title}\n\n{self.task}\n\n```python\n{code}\n```\n\n"
        self.dev_memory.add_episodic(content)

    def clear_episodic(self) -> None:
        self.plan_memory.clear_episodic()
        self.dev_memory.clear_episodic()