import os
import random
from tqdm import tqdm
from openai import OpenAI
from typing import Tuple, Optional, List

from .base import BasePipeline
from ..nodes import CriticNode, TestNode, DevNode, PlanNode
from ..config import config
from ..utils.logger import log_execution_time, ComponentLoggers


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
        self.logger.info(f"Max dev-test iterations: {config.max_dev_test_iterations}")
        self.logger.info(f"Max parallel tasks: {config.max_parallel_tasks}")
        self.logger.info(f"Default models: {config.default_models}")

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
                'planner': PlanNode(model=model, past_n=config.plan_history_length),
                'developer': DevNode(model=model, past_n=config.dev_history_length),
                'tester': TestNode(model=model, past_n=config.test_history_length)
            }
        else:
            self.logger.debug(f"Reusing existing node pool for model: {model}")
        
        pool = self._node_pools[model]
        return pool['planner'], pool['developer'], pool['tester']

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
        self.logger.debug(f"Plan node initialized for task: {task[:500] if len(task) > 500 else task}...")

        next_code = None
        plan_iteration = 0
        
        while True:
            plan_iteration += 1
            self.logger.debug(f"Plan iteration {plan_iteration}")
            
            next_plan, is_end = self.plan_node(h=next_code)
            self.plan_node.save_logs_to_file()  # save plan node prompt and history to log file
            self.logger.info("Plan generated: %s...", next_plan['plan'][:200])
            self.logger.debug("Plan description: %s...", next_plan['description'][:200])
            
            if is_end:
                self.logger.info("Plan marked as complete with <END>")
                break
            
            self.dev_node._init_prompt(plan=next_plan["plan"])
            self.test_node._init_prompt(plan=next_plan["plan"])
            self.logger.debug("Dev and test nodes initialized for current plan")

            next_feedback = None
            dev_test_iteration = 0
            
            while True:
                dev_test_iteration += 1
                self.logger.debug(f"Dev-test iteration {dev_test_iteration}")
                
                # Check iteration limit and add timeout feedback if exceeded
                if dev_test_iteration > config.max_dev_test_iterations:
                    self.logger.warning(f"Exceeded maximum iterations ({config.max_dev_test_iterations})")
                    self.logger.info("Adding timeout feedback message to encourage reflection")
                    
                    next_feedback["feedback"] += (
                        f"\nATTENTION: The development cycle has reached {dev_test_iteration} attempts, which is excessive. "
                        "Please reconsider your approach. If the task is impossible, terminate with <END> and explain why."
                    )
                    
                next_code, is_end = self.dev_node(h=next_feedback)
                self.dev_node.save_logs_to_file()  # save dev node prompt and history to log file
                self.logger.debug("Dev generated code description: %s...", next_code['description'][:200])
                
                if is_end:
                    self.logger.info("Dev marked task as complete with <END>")
                    break

                next_feedback = self.test_node(h=next_code)
                self.test_node.save_logs_to_file()  # save test node prompt and history to log file
                self.logger.debug("Test feedback: %s...", next_feedback['feedback'][:200])
                
                # Double check after test feedback to prevent infinite loops
                if dev_test_iteration > config.emergency_break_iterations:
                    self.logger.warning("Forcing termination due to excessive iterations")
                    next_code = {
                        "role": "developer",
                        "code": "print('The task is too complex for me to handle. Please provide a simpler task.')",
                        "description": "The task is too complex for me to handle. Please provide a simpler task."
                    }
                    break
        
        history = self.plan_node.export_history(past_n=config.critic_length)
        self.logger.info(f"Forward pass completed for model: {self.plan_node.model}")
        return history

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
        self.logger.debug("Task: %s...", task[:200])
        self.logger.debug(f"Models: {models}")
        
        # Use a random model for critic
        self.critic_node = CriticNode(model=models[random.randint(0, len(models) - 1)])
        self.critic_node._init_prompt(task=task)
        
        histories = []
        self.execution_paths = [] # Store all execution paths for potential learning
                
        for i, model in enumerate(tqdm(models, desc="Processing models")):
            self.logger.info(f"Starting execution path {i+1}/{len(models)} with model: {model}")
            
            history = self._forward(task, model)
            histories.append(history)
            
            # Store the complete execution context for this path
            execution_path = {
                'model': model,
                'history': history,
                'plan_node': self.plan_node,
                'dev_node': self.dev_node,
                'index': i
            }
            self.execution_paths.append(execution_path)
            self.logger.info(f"Completed execution path {i+1}/{len(models)} with model: {model}")

        self.logger.info("All execution paths completed, starting critic evaluation")
        final_answer, reason, best_id = self.critic_node(histories=histories)
        self.critic_node.save_logs_to_file()  # save critic node prompt and history to log file
        
        self.logger.info("Critic evaluation completed")
        self.logger.debug("Critic reason: %s...", reason[:200] if len(reason) > 500 else reason)
        self.logger.info(f"Best member index: {best_id} (model: {models[best_id]})")
        
        # Store the best path information for learning
        self.best_id = best_id
        
        self.logger.info(f"Task evolution completed successfully")
        return final_answer

    def learn(self) -> None: # TODO contrastive learning, leveraging failed trajectories
        """
        Learn from the past experiences, save the successful experiences to the long-term memory.
        Only saves the best path as determined by the critic node.
        """ 
        if hasattr(self, 'best_id') and hasattr(self, 'execution_paths'):
            best_path = self.execution_paths[self.best_id]
            self.best_plan_node: PlanNode = best_path['plan_node']
            self.best_dev_node: DevNode = best_path['dev_node']
            
            self.logger.info(f"Learning from best path (index {self.best_id}, model: {best_path['model']})")
            self._save_plan_episodic()
            self._save_dev_episodic()

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

    def _summarize_use_cases(self, plan: str, code: str) -> str:
        """Generate use cases for the given plan and code implementation."""
        try:
            prompt = f"""Based on the following plan and code implementation, generate 6-8 practical use cases in the exact format shown below. Each use case should be a specific, real-world application scenario that demonstrates when and why someone would use this solution.

PLAN: {plan}

CODE: {code}

Generate use cases following this exact format:
- [Specific use case description for a particular domain/scenario]
- [Another specific use case for a different application area]
- [Continue with practical, real-world applications]

Requirements:
1. Each use case should start with a dash (-)
2. Focus on specific, practical applications
3. Cover diverse domains (business, research, automation, analysis, etc.)
4. Be concise but descriptive
5. Avoid generic descriptions - be specific about the application
6. Generate 6-8 use cases total

Example format:
- Financial report analysis and automated data extraction for accounting workflows
- Scientific research data processing and statistical analysis for academic publications
- E-commerce inventory management and product catalog automation
- Social media content monitoring and sentiment analysis for marketing teams"""

            response = self.client.chat.completions.create(
                model="o4-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get('summarize_max_tokens', 500),
                temperature=config.get('summarize_temperature', 0.3),
            )
            
            use_cases = response.choices[0].message.content or "- General automation and data processing tasks"
            
            # Clean up the response to ensure proper formatting
            lines = use_cases.strip().split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('-'):
                    line = '- ' + line
                if line:
                    formatted_lines.append(line)
            
            result = '\n'.join(formatted_lines)
            self.logger.debug(f"Use cases generated: {len(formatted_lines)} items")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to generate use cases: {e}")
            return "- General automation and data processing tasks\n- Custom scripting and workflow optimization"

    def _save_plan_episodic(self) -> None:
        """Save plan episodic memory with task summary and execution history."""
        try:
            title = self._summarize_task(self.task)
            history = self.best_plan_node.export_history()
            content = f"### {title}\n\n**TASK**: {self.task}\n\n```\n{history}\n```"
            self.plan_memory.add_episodic(content)
            self.logger.debug(f"Plan episodic memory saved: {title}")
        except Exception as e:
            self.logger.error(f"Failed to save plan episodic memory: {e}")

    def _save_dev_episodic(self) -> None:
        """
        Save development episodic memory with improved code/text separation.
        Now that we have better RAG handling, we should include code by default.
        """
        try:
            plan_code_trajectory = self.best_dev_node.export_plan_code_trajectory()
            for plan, code in plan_code_trajectory:
                title = self._summarize_task(plan)
                use_cases = self._summarize_use_cases(plan=plan, code=code)
                content = f"### {title}\n\n**Description**: {plan}\n\n**Use Cases**:\n{use_cases}\n\n```\n{code}\n```"
                self.logger.debug(f"Dev episodic memory saved: {title}")
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