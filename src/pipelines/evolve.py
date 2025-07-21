import os
from tqdm import tqdm
from openai import OpenAI
from typing import Tuple, Optional, List
# from concurrent.futures import ThreadPoolExecutor, as_completed TODO add concurrent

from .base import BasePipeline
from ..nodes import CriticNode, TestNode, DevNode, PlanNode
from ..config import config
from ..utils.logger import get_logger, log_execution_time, ComponentLoggers


class EvolvePipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.logger = ComponentLoggers.get_pipeline_logger()
        
        # Create reusable node pools for different models
        self._node_pools = {}
        
        # Initialize configuration
        self.logger.info("EvolvePipeline initialized with configuration:")
        self.logger.info(f"  Max dev-test iterations: {config.max_dev_test_iterations}")
        self.logger.info(f"  Max parallel tasks: {config.max_parallel_tasks}")
        self.logger.info(f"  Default models: {config.default_models}")

    def _get_or_create_nodes(self, model: str) -> Tuple[PlanNode, DevNode, TestNode]:
        """
        Get or create reusable node instances for a specific model.
        
        Args:
            model: Model identifier
            
        Returns:
            Tuple of (plan_node, dev_node, test_node)
        """
        if model not in self._node_pools:
            self.logger.debug(f"Creating new node pool for model: {model}")
            self._node_pools[model] = {
                'plan': PlanNode(model=model),
                'dev': DevNode(model=model),
                'test': TestNode(model=model)
            }
        else:
            self.logger.debug(f"Reusing existing node pool for model: {model}")
        
        pool = self._node_pools[model]
        return pool['plan'], pool['dev'], pool['test']

    def _reset_node_states(self, plan_node: PlanNode, dev_node: DevNode, test_node: TestNode):
        """
        Reset node states for reuse while preserving the model configurations.
        """
        # Clear history but preserve memory and model configurations
        plan_node.history.clear()
        dev_node.history.clear()
        test_node.history.clear()
        
        # Reset token counters
        plan_node._last_history_token_counts = 0
        dev_node._last_history_token_counts = 0
        test_node._last_history_token_counts = 0

    @log_execution_time()
    def _forward(self, 
        task: str, 
        model: str = "o4-mini",
    ) -> Tuple[str, str]:
        """
        Forward the task, sample one trajectory using reusable nodes.
        """
        self.task = task
        self.logger.info(f"Starting forward pass for model: {model}")

        # Get or create reusable nodes for this model
        self.plan_node, self.dev_node, self.test_node = self._get_or_create_nodes(model)
        
        # Reset node states for clean execution
        self._reset_node_states(self.plan_node, self.dev_node, self.test_node)
        
        # Initialize nodes for this task
        self.plan_node._init_prompt(task=task)
        self.logger.debug(f"Plan node initialized for task: {task[:100]}...")

        description = None
        reason = None
        plan_iteration = 0
        
        while True:
            plan_iteration += 1
            self.logger.debug(f"Plan iteration {plan_iteration}")
            
            plan, reason = self.plan_node(content=description, name="dev")
            self.logger.info(f"Plan generated: {plan[:200]}...")
            self.logger.debug(f"Plan reason: {reason[:200]}...")
            
            if "<END>" in plan:
                self.logger.info("Plan marked as complete with <END>")
                break
            
            self.dev_node._init_prompt(plan=plan)
            self.test_node._init_prompt(plan=plan)
            self.logger.debug("Dev and test nodes initialized for current plan")

            feedback, code_output = None, None
            dev_test_iteration = 0
            
            while True:
                dev_test_iteration += 1
                self.logger.debug(f"Dev-test iteration {dev_test_iteration}")
                
                # Check iteration limit and add timeout feedback if exceeded
                if dev_test_iteration > config.max_dev_test_iterations:
                    from src.memory.utils import get_timeout_feedback_message
                    timeout_message = get_timeout_feedback_message(dev_test_iteration)
                    self.logger.warning(f"Exceeded maximum iterations ({config.max_dev_test_iterations})")
                    self.logger.info("Adding timeout feedback message to encourage reflection")
                    feedback = timeout_message
                    code_output = "Iteration limit exceeded"
                    
                code, description = self.dev_node(content=(feedback, code_output), name="test")
                self.logger.debug(f"Dev generated code description: {description[:200]}...")
                
                if "<END>" in code:
                    self.logger.info("Dev marked task as complete with <END>")
                    break

                feedback, code_output = self.test_node(content=code, name="dev")
                self.logger.debug(f"Test feedback: {feedback[:200]}...")
                
                # Double check after test feedback to prevent infinite loops
                if dev_test_iteration > config.emergency_break_iterations:
                    self.logger.error("EMERGENCY BREAK: Forcing termination due to excessive iterations")
                    break
        
        history = self.plan_node.export_history(past_n=config.dev_history_length)
        answer = reason
        
        self.logger.info(f"Forward pass completed for model: {self.plan_node.model}")
        self.logger.debug(f"Final answer: {answer[:200]}...")
        
        return history, answer

    @log_execution_time()
    def __call__(self,
        task: str,
        models: Optional[List[str]] = None, 
    ) -> str:
        """
        Evolve the task, use multiple parallel trajectories and judge them with the critic node.
        
        Args:
            task: Task description to solve
            models: List of models to use (defaults to config.default_models)
            
        Returns:
            Final answer from the critic node
        """
        if models is None:
            models = config.default_models
            
        self.logger.info(f"Starting task evolution with {len(models)} models")
        self.logger.debug(f"Task: {task[:200]}...")
        self.logger.debug(f"Models: {models}")
        
        self.critic_node = CriticNode(model=models[0])  # Use first model for critic
        self.critic_node._init_prompt(task=task)
        
        histories, answers = [], []
        # Store all execution paths for potential learning
        self.execution_paths = []
                
        for i, model in enumerate(tqdm(models, desc="Processing models")):
            self.logger.info(f"Starting execution path {i+1}/{len(models)} with model: {model}")
            
            history, answer = self._forward(task, model)
            histories.append(history)
            answers.append(answer)
            
            # Store the complete execution context for this path
            execution_path = {
                'model': model,
                'history': history,
                'answer': answer,
                'plan_node': self.plan_node,
                'dev_node': self.dev_node,
                'index': i
            }
            self.execution_paths.append(execution_path)
            self.logger.info(f"Completed execution path {i+1}/{len(models)} with model: {model}")

        self.logger.info("All execution paths completed, starting critic evaluation")
        final_answer, reason, best_member_index = self.critic_node(histories=histories, answers=answers)
        
        self.logger.info(f"Critic evaluation completed")
        self.logger.debug(f"Critic reason: {reason[:500]}...")
        self.logger.info(f"Best member index: {best_member_index} (model: {models[best_member_index]})")
        
        # Store the best path information for learning
        self.best_member_index = best_member_index
        
        self.logger.info(f"Task evolution completed successfully")
        return final_answer

    def learn(self) -> None: # TODO contrastive learning, leveraging failed trajectories
        """
        Learn from the past experiences, save the successful experiences to the long-term memory.
        Only saves the best path as determined by the critic node.
        """ 
        if hasattr(self, 'best_member_index') and hasattr(self, 'execution_paths'):
            best_path = self.execution_paths[self.best_member_index]
            
            # Temporarily set the nodes to the best path for saving
            original_plan_node = getattr(self, 'plan_node', None)
            original_dev_node = getattr(self, 'dev_node', None)
            
            self.plan_node = best_path['plan_node']
            self.dev_node = best_path['dev_node']
            
            self.logger.info(f"Learning from best path (index {self.best_member_index}, model: {best_path['model']})")
            self._save_plan_episodic()
            self._save_dev_episodic()
            
            # Restore original nodes if they existed
            if original_plan_node:
                self.plan_node = original_plan_node
            if original_dev_node:
                self.dev_node = original_dev_node
                
            self.logger.info("Successfully saved the best path experiences to the long-term memory")
        else:
            self.logger.warning("No valid execution paths found for learning")
    
    def _summarize_task(self, task: str) -> str:
        """Summarize task into a concise title using configured parameters."""
        try:
            response = self.client.chat.completions.create(
                model="o4-mini",
                messages=[{"role": "user", "content": f"Summarize the task into a title within {config.get('task.max_title_words', 15)} words: {task}"}],
                max_tokens=config.summarize_max_tokens,
                temperature=config.summarize_temperature,
            )
            summary = response.choices[0].message.content or "Unknown Task"
            self.logger.debug(f"Task summarized: '{summary}'")
            return summary
        except Exception as e:
            self.logger.error(f"Failed to summarize task: {e}")
            return "Task Summary Failed"

    def _save_plan_episodic(self) -> None:
        """Save plan episodic memory with task summary and execution history."""
        try:
            title = self._summarize_task(self.task)
            history = self.plan_node.export_history()
            content = f"### {title}\n\n```\n{history}\n```\n"
            self.plan_memory.add_episodic(content)
            self.logger.debug(f"Plan episodic memory saved: {title}")
        except Exception as e:
            self.logger.error(f"Failed to save plan episodic memory: {e}")

    def _save_dev_episodic(self, include_code: bool = True) -> None:
        """
        Save development episodic memory with improved code/text separation.
        Now that we have better RAG handling, we should include code by default.
        """
        try:
            title = self._summarize_task(self.task)
            code = self.dev_node.export_final_code()
            
            if include_code and code:
                # Create structured content that our new splitting function can handle properly
                content = f"### {title}\n\n**Task Description:**\n{self.task}\n\n**Implementation:**\n\n```python\n{code}\n```"
                self.logger.debug(f"Dev episodic memory saved with code: {title}")
            else:
                content = f"### {title}\n\n**Task Description:**\n{self.task}"
                self.logger.debug(f"Dev episodic memory saved without code: {title}")
            
            self.dev_memory.add_episodic(content)
        except Exception as e:
            self.logger.error(f"Failed to save dev episodic memory: {e}")

    def clear_episodic(self) -> None:
        """Clear all episodic memories."""
        try:
            self.plan_memory.clear_episodic()
            self.dev_memory.clear_episodic()
            self.logger.info("All episodic memories cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memories: {e}")