"""
Evolutionary Pipeline for EvolAgent.

This module implements the core evolutionary algorithm pipeline that orchestrates
multiple agent nodes to solve complex tasks through iterative planning, development,
testing, and criticism.
"""

import os
import gc
import random
import weakref
from tqdm import tqdm
from openai import OpenAI
from typing import Tuple, Optional, List, Dict, Any

from .base import BasePipeline
from ..nodes import CriticNode, TestNode, DevNode, PlanNode
from ..utils.config import config

from ..utils.timer import timer
from ..utils.logger import get_logger
from ..utils.manager import workspace_manager
from ..utils.logger import get_task_logger, get_html_task_logger


class EvolvePipeline(BasePipeline):
    """
    Multi-agent evolutionary pipeline for complex task solving.
    
    This pipeline orchestrates multiple AI agents (planner, developer, tester, critic)
    to solve tasks through an evolutionary approach with multiple parallel trajectories
    and critic-based selection of the best solution.
    """

    def __init__(self):
        """Initialize the evolutionary pipeline with resource management."""
        super().__init__()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.logger = get_logger("agent.pipeline")
        
        # Weak reference to active nodes to prevent memory leaks
        self._active_nodes = weakref.WeakSet()
        
        # Log initialization configuration
        self._log_initialization()

    def _log_initialization(self) -> None:
        """Log pipeline initialization configuration."""
        self.logger.info("EvolvePipeline initialized with configuration:")
        self.logger.info(f"Max dev-test iterations: {config.get('pipeline.max_dev_test_iterations', 50)}")
        self.logger.info(f"Max parallel tasks: {config.get('runtime.parallel_workers', 3)}")
        
        models = config.get('models.default_models', ['o4-mini'])
        temperatures = config.get('models.temperature', 0.7)
        
        self.logger.info(f"Default models: {models}")
        self.logger.info(f"Temperature configuration: {temperatures}")
        
        # Validate temperature configuration
        self._validate_temperature_config(models, temperatures)

    def _validate_temperature_config(self, models: List[str], temperatures) -> None:
        """
        Validate that temperature configuration matches models configuration.
        
        Args:
            models: List of model names
            temperatures: Temperature configuration (single value or list)
        """
        if isinstance(temperatures, list):
            if len(temperatures) != len(models):
                warning_msg = (
                    f"Temperature list length ({len(temperatures)}) does not match "
                    f"models list length ({len(models)}). This may cause issues with "
                    f"temperature assignment. Models: {models}, Temperatures: {temperatures}"
                )
                self.logger.warning(warning_msg)
                
                # Suggest fix
                if len(temperatures) < len(models):
                    self.logger.warning(f"Consider adding {len(models) - len(temperatures)} more temperature values")
                else:
                    self.logger.warning(f"Consider removing {len(temperatures) - len(models)} temperature values")
            else:
                self.logger.info("Temperature configuration validated successfully")
                for i, (model, temp) in enumerate(zip(models, temperatures)):
                    self.logger.debug(f"Model {i}: {model} -> Temperature: {temp}")
        else:
            self.logger.info(f"Using single temperature value {temperatures} for all models")

    def _create_agent_nodes(self, model: str, model_index: int) -> Tuple[PlanNode, DevNode, TestNode]:
        """
        Create fresh agent nodes for each task execution.
        
        This ensures complete isolation between tasks and prevents state leakage.
        
        Args:
            model: Model identifier for the agents
            model_index: Index of the model in the default_models list
            
        Returns:
            Tuple of (planner, developer, tester) nodes
        """
        self.logger.debug(f"Creating fresh agent nodes for model: {model} (index: {model_index})")
        
        # Create nodes with configured history lengths and model index
        planner = PlanNode(
            model=model, 
            past_n=config.get('nodes.plan_history_length', 8),
            model_index=model_index
        )
        developer = DevNode(
            model=model, 
            past_n=config.get('nodes.dev_history_length', 8),
            model_index=model_index
        )
        tester = TestNode(
            model=model, 
            past_n=config.get('nodes.test_history_length', 8),
            model_index=model_index
        )
        
        # Track nodes with weak references for automatic cleanup
        self._active_nodes.add(planner)
        self._active_nodes.add(developer)
        self._active_nodes.add(tester)
        
        self.logger.debug(f"Created agent nodes for model: {model} (index: {model_index})")
        return planner, developer, tester

    def _cleanup_agent_nodes(self, *nodes) -> None:
        """
        Clean up agent node resources and release memory.
        
        Args:
            *nodes: Variable number of node instances to clean up
        """
        for node in nodes:
            if node:
                try:
                    # Clear node history
                    if hasattr(node, 'history'):
                        node.history.clear()
                    
                    # Clean up node-specific resources
                    if hasattr(node, 'dev_trajectory'):
                        node.dev_trajectory.clear()
                    
                    # Memory cleanup is handled by the Memory class itself
                    # OpenAI client cleanup is handled by the client pool
                        
                except Exception as e:
                    self.logger.warning(f"Error cleaning up node {type(node).__name__}: {e}")

    @timer()
    def _execute_single_trajectory(self, 
        task: str, 
        model: str,
        task_id: Optional[str] = None,
        model_index: int = 0,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Execute a single evolutionary trajectory for the given task.
        
        This method orchestrates the complete planning-development-testing cycle
        for one model trajectory.
        
        Args:
            task: Task description to solve
            model: Model identifier
            task_id: Optional task identifier for workspace isolation
            model_index: Index of the model in the parallel execution
            
        Returns:
            Tuple of (execution_history, development_trajectory)
        """
        self.task = task
        self.logger.info(f"Starting trajectory execution for model: {model}")

        # Initialize task loggers
        task_logger = get_task_logger(task_id, model, model_index) if task_id else None
        html_logger = get_html_task_logger(
            task_id, model, 
            task_logger.get_base_dir() if task_logger else None, 
            model_index
        ) if task_id else None

        # Create fresh agent nodes for isolation
        planner, developer, tester = self._create_agent_nodes(model, model_index)
        
        try:
            # Initialize planner with task
            planner._init_prompt(task=task)
            self.logger.debug(f"Planner initialized for task: {task[:500] if len(task) > 500 else task}...")

            # Log planner initialization
            self._log_planner_initialization(task_logger, html_logger, planner, task)

            # Execute planning-development cycles
            execution_history, dev_trajectory = self._execute_planning_cycles(
                planner, developer, tester, task_logger, html_logger
            )
            
            # Store nodes for potential learning (weak references prevent memory leaks)
            self.planner = planner
            self.developer = developer
            self.tester = tester
            
            self.logger.info(f"Trajectory execution completed for model: {model}")
            return execution_history, dev_trajectory
            
        except Exception as e:
            self.logger.error(f"Error in trajectory execution for model {model}: {e}")
            self._cleanup_agent_nodes(planner, developer, tester)
            raise
        finally:
            # Force garbage collection to release memory
            gc.collect()

    def _log_planner_initialization(self, task_logger, html_logger, planner, task) -> None:
        """Log planner initialization to various loggers."""
        if task_logger:
            episodic_examples = getattr(planner, 'episodic', '') or ''
            task_logger.log_planner_start(task, episodic_examples)
        
        if html_logger:
            episodic_examples = getattr(planner, 'episodic', '') or ''
            html_logger.log_planner_start(task, episodic_examples)

    def _execute_planning_cycles(self, planner, developer, tester, task_logger, html_logger) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Execute the main planning-development-testing cycles with timeout protection.
        
        Returns:
            Tuple of (execution_history, development_trajectory)
        """
        next_code = None
        plan_iteration = 0
        max_plan_iterations = config.get('pipeline.max_plan_iterations', 10)
        
        while True:
            plan_iteration += 1
            self.logger.debug(f"Plan iteration {plan_iteration}")
            
            # Check for planning timeout
            if plan_iteration > max_plan_iterations:
                self.logger.warning(f"Planning exceeded maximum iterations ({max_plan_iterations}), forcing completion")
                is_plan_complete = True
            
            # Generate next plan
            next_plan, is_plan_complete = planner(h=next_code)
            self.logger.info("Plan generated: %s...", next_plan['plan'][:200])
            self.logger.debug("Plan description: %s...", next_plan['description'][:200])
            
            # Log planner history
            self._log_planner_history(task_logger, html_logger, planner)
            
            if is_plan_complete:
                self.logger.info("Plan marked as complete with <END>")
                break
            
            # Initialize development and testing nodes for current plan
            developer._init_prompt(plan=next_plan["plan"])
            tester._init_prompt(plan=next_plan["plan"])
            self.logger.debug("Developer and tester nodes initialized for current plan")

            # Execute development-testing cycle
            next_code = self._execute_development_cycle(
                next_plan, developer, tester, task_logger, html_logger
            )
        
        # Extract results
        execution_history = planner.export_history(past_n=config.get('nodes.critic_length', 5))
        dev_trajectory = developer.dev_trajectory
        
        return execution_history, dev_trajectory

    def _log_planner_history(self, task_logger, html_logger, planner) -> None:
        """Log planner history to various loggers."""
        if task_logger:
            planner_history = planner.export_history()
            task_logger.log_planner_history(planner_history)
            
        if html_logger:
            planner_history = planner.export_history()
            html_logger.log_planner_history(planner_history)

    def _execute_development_cycle(self, plan, developer, tester, task_logger, html_logger) -> Dict[str, Any]:
        """
        Execute the development-testing cycle for a single plan.
        
        Args:
            plan: Current plan dictionary
            developer: Developer node instance
            tester: Tester node instance
            task_logger: Task logger instance
            html_logger: HTML logger instance
            
        Returns:
            Final code result from the development cycle
        """
        # Get episodic examples and log developer plan start
        episodic_examples = getattr(developer, 'episodic', '')
        current_plan_index = self._log_developer_plan_start(
            task_logger, html_logger, plan, episodic_examples
        )

        next_feedback = None
        dev_test_iteration = 0
        max_iterations = config.get('pipeline.max_dev_test_iterations', 50)
        emergency_limit = config.get('pipeline.emergency_break_iterations', 55)
        
        while True:
            dev_test_iteration += 1
            self.logger.debug(f"Dev-test iteration {dev_test_iteration}")
            
            # Add timeout feedback if approaching limits
            if dev_test_iteration > max_iterations and next_feedback is not None:
                next_feedback = self._add_timeout_feedback(next_feedback, dev_test_iteration)
                
            # Generate code
            next_code, is_code_complete = developer(h=next_feedback)
            self.logger.debug("Developer generated code description: %s...", next_code['description'][:200])
            
            if is_code_complete:
                self.logger.info("Developer marked task as complete with <END>")
                break

            # Test code and get feedback
            next_feedback = tester(h=next_code)
            self.logger.debug("Tester feedback: %s...", next_feedback['feedback'][:200])
            
            # Log execution details
            self._log_code_execution(
                html_logger, current_plan_index, next_code, next_feedback, dev_test_iteration
            )
            
            # Emergency break to prevent infinite loops
            if dev_test_iteration > emergency_limit:
                self.logger.warning("Forcing termination due to excessive iterations")
                next_code = self._create_emergency_termination_response()
                break
        
        # Log final development history
        self._log_developer_history(task_logger, html_logger, current_plan_index, developer)
        
        return next_code

    def _log_developer_plan_start(self, task_logger, html_logger, plan, episodic_examples) -> Optional[int]:
        """Log the start of a new development plan."""
        current_plan_index = None
        
        if task_logger:
            current_plan_index = task_logger.log_developer_plan(
                plan["plan"], 
                plan.get("description", ""),
                episodic_examples
            )
        
        if html_logger:
            current_plan_index = html_logger.log_developer_plan(
                plan["plan"], 
                plan.get("description", ""),
                episodic_examples
            )
            
        return current_plan_index

    def _add_timeout_feedback(self, feedback: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """Add timeout warning to feedback."""
        self.logger.warning(f"Exceeded maximum iterations ({config.get('pipeline.max_dev_test_iterations', 50)})")
        self.logger.info("Adding timeout feedback message to encourage reflection")
        
        feedback["feedback"] += (
            f"\nATTENTION: The development cycle has reached {iteration} attempts, which is excessive. "
            "Please reconsider your approach. If the task is impossible, terminate with <END> and explain why."
        )
        return feedback

    def _log_code_execution(self, html_logger, plan_index, code_result, feedback, iteration) -> None:
        """Log code execution details to HTML logger."""
        if html_logger and plan_index:
            html_logger.log_developer_code_execution(
                plan_index=plan_index,
                code=code_result.get('code', ''),
                code_output=feedback.get('code_output', ''),
                iteration=iteration
            )
            html_logger.log_tester_feedback(
                code=code_result.get('code', ''),
                code_output=feedback.get('code_output', ''),
                feedback=feedback.get('feedback', '')
            )

    def _create_emergency_termination_response(self) -> Dict[str, Any]:
        """Create emergency termination response."""
        return {
            "role": "developer",
            "code": "print('The task is too complex for me to handle. Please provide a simpler task.')",
            "description": "The task is too complex for me to handle. Please provide a simpler task."
        }

    def _log_developer_history(self, task_logger, html_logger, plan_index, developer) -> None:
        """Log developer history after development cycle completion."""
        if task_logger and plan_index:
            dev_history = developer.export_history()
            task_logger.log_developer_history(plan_index, dev_history)
            
        if html_logger and plan_index:
            dev_history = developer.export_history()
            html_logger.log_developer_history(plan_index, dev_history)

    @timer()
    def __call__(self,
        task: str,
        models: Optional[List[str]] = None,
        task_id: Optional[str] = None,
        true_answer: Optional[str] = None,
    ) -> str:
        """
        Execute the evolutionary algorithm with multiple parallel trajectories.
        
        This is the main entry point that orchestrates multiple model trajectories,
        evaluates them using a critic node, and returns the best solution.
        
        Args:
            task: Task description to solve
            models: List of models to use (defaults to config.default_models)
            task_id: Optional task identifier for workspace isolation
            true_answer: Optional true answer for comparison in results
            
        Returns:
            Final answer selected by the critic node
        """
        # Initialize parameters
        if models is None:
            models = config.get('models.default_models', ['o4-mini'])

        if task_id is None:
            import uuid
            task_id = str(uuid.uuid4())[:8]
            
        # Store true_answer for later use in critic results
        self.true_answer = true_answer
            
        self.logger.info(f"Starting evolutionary task solving with {len(models)} models (task_id: {task_id})")
        self.logger.debug("Task: %s...", task[:200])
        self.logger.debug(f"Models: {models}")
        
        # Execute task within isolated workspace context
        with workspace_manager.isolated_workspace(task_id) as workspace_path:
            self.logger.info(f"Using isolated workspace: {workspace_path}")
            
            # Initialize critic with random model selection
            critic = self._initialize_critic(models, task)
            
            # Execute parallel trajectories
            execution_results = self._execute_parallel_trajectories(
                task, models, task_id, workspace_path
            )
            
            try:
                # Evaluate trajectories and select best solution
                final_answer = self._evaluate_and_select_best(
                    critic, execution_results, models, task_id
                )
                
                # Store results for learning
                self._store_execution_results(execution_results)
                
                self.logger.info(f"Evolutionary task solving completed successfully (task_id: {task_id})")
                return final_answer
                
            finally:
                # Clean up critic node
                self._cleanup_agent_nodes(critic)
                gc.collect()

    def _initialize_critic(self, models: List[str], task: str) -> CriticNode:
        """Initialize and configure the critic node."""
        # Randomly select a model and its index for the critic
        critic_model_index = random.randint(0, len(models) - 1)
        critic = CriticNode(model=models[critic_model_index], model_index=critic_model_index)
        critic._init_prompt(task=task)
        return critic

    def _execute_parallel_trajectories(self, 
        task: str, 
        models: List[str], 
        task_id: str, 
        workspace_path: str
    ) -> List[Dict[str, Any]]:
        """Execute multiple parallel trajectories and collect results."""
        execution_results = []
        
        for i, model in enumerate(tqdm(models, desc="Executing trajectories")):
            self.logger.info(f"Starting trajectory {i+1}/{len(models)} with model: {model}")
            
            # Execute single trajectory
            history, dev_trajectory = self._execute_single_trajectory(task, model, task_id, i)
            
            # Store execution result
            execution_result = {
                'model': model,
                'history': history,
                'dev_trajectory': dev_trajectory,
                'index': i
            }
            execution_results.append(execution_result)
            
            self.logger.info(f"Completed trajectory {i+1}/{len(models)} with model: {model}")
            
            # Clear workspace between executions (except last one)
            if i < len(models) - 1:
                self._clear_workspace_files(workspace_path)
                self.logger.debug("Cleared workspace files for next trajectory")
            
            # Periodic memory cleanup
            gc.collect()
        
        return execution_results

    def _evaluate_and_select_best(self, 
        critic: CriticNode, 
        execution_results: List[Dict[str, Any]], 
        models: List[str], 
        task_id: str
    ) -> str:
        """Evaluate trajectories using critic and select the best solution."""
        self.logger.info("All trajectories completed, starting critic evaluation")
        
        # Extract histories for critic evaluation
        histories = [result['history'] for result in execution_results]
        
        # Critic evaluation
        final_answer, reason, best_id = critic(histories=histories)
        
        self.logger.info("Critic evaluation completed")
        self.logger.debug("Critic reasoning: %s...", reason[:200] if len(reason) > 200 else reason)
        self.logger.info(f"Selected best trajectory: {best_id} (model: {models[best_id]})")
        
        # Save critic results
        self._save_critic_results(task_id, critic.model, final_answer, reason, best_id, self.true_answer)
        
        return final_answer

    def _save_critic_results(self, 
        task_id: str, 
        critic_model: str, 
        final_answer: str, 
        reason: str, 
        best_id: int,
        true_answer: str = None
    ) -> None:
        """Save critic evaluation results."""
        from ..utils.logger import HTMLTaskLogger
        
        HTMLTaskLogger.save_critic_result_static(
            task_id=task_id,
            critic_model=critic_model,
            final_answer=final_answer,
            reason=reason,
            best_model_index=best_id,
            true_answer=true_answer
        )

    def _store_execution_results(self, execution_results: List[Dict[str, Any]]) -> None:
        """Store execution results for potential learning."""
        if execution_results:
            # Find the best trajectory based on critic selection
            best_result = execution_results[getattr(self, 'best_id', 0)]
            self.best_id = best_result['index']
            self.execution_results = execution_results

    def learn(self) -> None: # TODO contrastive learning, leveraging failed trajectories
        """
        Learn from the past experiences, save the successful experiences to the long-term memory.
        Only saves the best path as determined by the critic node.
        """ 
        if hasattr(self, 'best_id'):
            self.logger.info(f"Learning from best path (index {self.best_id})")

            self.best_history = self.execution_results[self.best_id]['history']
            self.best_model = self.execution_results[self.best_id]['model']

            self._save_plan_episodic()
            self._save_dev_episodic()

            self.logger.info("Successfully saved the best path experiences to the long-term memory")
            
            # Clean up execution_results after saving episodic memories
            if hasattr(self, 'execution_results'):
                del self.execution_results
                
        else:
            self.logger.warning("No valid execution paths found for learning")
    
    def _summarize_task(self, task: str) -> str:
        """Summarize task into a concise title using configured parameters."""
        try:
            prompt_template = config.get('task.summarize_task_prompt', 
                                       "Summarize the task into a title within {max_words} words: {task}")
            prompt = prompt_template.format(
                max_words=config.get('task.max_title_words', 15),
                task=task
            )
            
            response = self.client.chat.completions.create(
                model=config.get('models.summarize_model', 'o4-mini'),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get('models.summarize_max_tokens', 500),
                temperature=config.get('models.summarize_temperature', 0.3),
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
            prompt_template = config.get('task.use_cases_prompt', 
                                       "Generate use cases for plan: {plan} and code: {code}")
            prompt = prompt_template.format(plan=plan, code=code)

            response = self.client.chat.completions.create(
                model=config.get('models.summarize_model', 'o4-mini'),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get('models.summarize_max_tokens', 500),
                temperature=config.get('models.summarize_temperature', 0.3),
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
            history = self.best_history
            content = f"### {title}\n\n**TASK**: {self.task}\n\n```\n{history}\n```"
            
            plan_node = PlanNode(model=self.best_model, model_index=self.best_id)
            plan_node.memory.add_episodic(content)
            self.logger.info(f"Plan episodic memory saved successfully: {title}")
                
        except Exception as e:
            self.logger.error(f"Failed to save plan episodic memory: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    def _save_dev_episodic(self) -> None:
        """
        Save development episodic memory with improved code/text separation.
        Now that we have better RAG handling, we should include code by default.
        """
        try:
            dev_trajectory = self.execution_results[self.best_id]['dev_trajectory']
            self.logger.info(f"Processing {len(dev_trajectory)} plan-code pairs for episodic memory")
            
            successful_saves = 0
            failed_saves = 0
            
            for i, trajectory_item in enumerate(dev_trajectory):
                try:
                    # Handle both dict and tuple formats for backward compatibility
                    if isinstance(trajectory_item, dict):
                        plan = trajectory_item["plan"]
                        code = trajectory_item["code"]
                    else:
                        plan, code = trajectory_item
                    
                    # Create more specific title to avoid conflicts
                    title = f"Development Step {i+1}: {self._summarize_task(plan)}"
                    use_cases = self._summarize_use_cases(plan=plan, code=code)
                    
                    # Ensure proper template variable substitution
                    content = f"### {title}\n\n**Description**: {plan}\n\n**Use Cases**:\n{use_cases}\n\n```\n{code}\n```"
                    
                    self.logger.debug(f"Dev episodic memory content created: {title}")
                    
                    dev_node = DevNode(model=self.best_model, model_index=self.best_id)
                    dev_node.memory.add_episodic(content)
                    successful_saves += 1
                    
                except Exception as e:
                    failed_saves += 1
                    self.logger.error(f"Failed to save dev episodic memory item {i+1}: {e}")
                    continue  # Continue with next item even if this one fails
            
            self.logger.info(f"Dev episodic memory save completed: {successful_saves} successful, {failed_saves} failed")
                
        except Exception as e:
            self.logger.error(f"Failed to save dev episodic memory: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    def _clear_workspace_files(self, workspace_path: str) -> None:
        """
        Clear all files in the workspace directory while keeping the directory itself.
        
        Args:
            workspace_path: Path to the workspace directory
        """
        try:
            from pathlib import Path
            import shutil
            
            workspace = Path(workspace_path)
            if workspace.exists() and workspace.is_dir():
                # Remove all files and subdirectories
                for item in workspace.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                
                self.logger.debug(f"Cleared all files from workspace: {workspace_path}")
            else:
                self.logger.warning(f"Workspace directory does not exist: {workspace_path}")
                
        except Exception as e:
            self.logger.error(f"Failed to clear workspace files {workspace_path}: {e}")

    def clear_episodic(self) -> None:
        """Clear all episodic memories."""
        try:
            # Create temporary nodes to access memory
            temp_plan_node = PlanNode(model="o4-mini", model_index=0)
            temp_dev_node = DevNode(model="o4-mini", model_index=0)
            
            temp_plan_node.memory.clear_episodic()
            temp_dev_node.memory.clear_episodic()
            
            # Clean up temporary nodes
            self._cleanup_agent_nodes(temp_plan_node, temp_dev_node)
            
            self.logger.info("All episodic memories cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memories: {e}")

    def __del__(self):
        """Destructor to clean up resources."""
        try:
            # Clean up possible residual node references
            if hasattr(self, 'planner'):
                self._cleanup_agent_nodes(self.planner)
            if hasattr(self, 'developer'):
                self._cleanup_agent_nodes(self.developer)
            if hasattr(self, 'tester'):
                self._cleanup_agent_nodes(self.tester)
        except:
            pass