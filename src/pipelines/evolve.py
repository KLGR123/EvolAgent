import os
import random
import threading
import weakref
import gc
from tqdm import tqdm
from openai import OpenAI
from typing import Tuple, Optional, List

from .base import BasePipeline
from ..nodes import CriticNode, TestNode, DevNode, PlanNode
from ..config import config
from ..utils.logger import log_execution_time, ComponentLoggers
from ..utils.workspace_manager import isolated_workspace
from ..utils.task_logger import get_task_logger
from ..utils.html_logger import get_html_task_logger, HTMLTaskLogger


class EvolvePipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.logger = ComponentLoggers.get_pipeline_logger()
        
        # 移除共享节点池，改为每次创建新实例以确保线程安全
        self._node_creation_lock = threading.Lock()
        
        # 使用弱引用来跟踪活跃的节点，避免内存泄漏
        self._active_nodes = weakref.WeakSet()
        
        # Initialize configuration
        self.logger.info("EvolvePipeline initialized with configuration:")
        self.logger.info(f"Max dev-test iterations: {config.max_dev_test_iterations}")
        self.logger.info(f"Max parallel tasks: {config.max_parallel_tasks}")
        self.logger.info(f"Default models: {config.default_models}")

    def _create_fresh_nodes(self, model: str) -> Tuple[PlanNode, DevNode, TestNode]:
        """
        为每个任务创建全新的节点实例，确保完全的隔离性。
        
        Args:
            model: Model identifier
            
        Returns:
            Tuple of (plan_node, dev_node, test_node)
        """
        with self._node_creation_lock:
            self.logger.debug(f"Creating fresh nodes for model: {model}")
            
            plan_node = PlanNode(model=model, past_n=config.plan_history_length)
            dev_node = DevNode(model=model, past_n=config.dev_history_length)
            test_node = TestNode(model=model, past_n=config.test_history_length)
            
            # 使用弱引用跟踪，当节点被垃圾回收时自动移除
            self._active_nodes.add(plan_node)
            self._active_nodes.add(dev_node)
            self._active_nodes.add(test_node)
            
            self.logger.debug(f"Created fresh nodes for model: {model}")
            return plan_node, dev_node, test_node

    def _cleanup_nodes(self, *nodes):
        """
        清理节点资源，释放内存。
        """
        for node in nodes:
            if node:
                try:
                    # 清理节点历史
                    if hasattr(node, 'history'):
                        node.history.clear()
                    
                    # 清理特定节点的资源
                    if hasattr(node, 'plan_code_trajectory'):
                        node.plan_code_trajectory.clear()
                    
                    # 清理内存相关资源
                    if hasattr(node, 'memory'):
                        # 不直接删除memory，但可以清理其缓存
                        pass
                        
                    # 清理OpenAI客户端可能的缓存
                    if hasattr(node, 'client'):
                        # OpenAI客户端通常不需要显式清理，但可以设置为None
                        pass
                        
                except Exception as e:
                    self.logger.warning(f"Error cleaning up node {type(node).__name__}: {e}")

    @log_execution_time()
    def _forward(self, 
        task: str, 
        model: str = "o4-mini",
        task_id: Optional[str] = None,
        model_index: int = 0,
    ) -> str:
        """
        Forward the task, sample one trajectory using fresh nodes with proper cleanup.
        """

        self.task = task
        self.logger.info(f"Starting forward pass for model: {model}")

        # Get task loggers for this model with unique index
        task_logger = get_task_logger(task_id, model, model_index) if task_id else None
        html_logger = get_html_task_logger(task_id, model, task_logger.get_base_dir() if task_logger else None, model_index) if task_id else None

        # 创建全新的节点实例，确保线程安全
        plan_node, dev_node, test_node = self._create_fresh_nodes(model)
        
        try:
            # Initialize nodes for this task
            plan_node._init_prompt(task=task)
            self.logger.debug(f"Plan node initialized for task: {task[:500] if len(task) > 500 else task}...")

            # Log planner initialization
            if task_logger:
                episodic_examples = getattr(plan_node, 'episodic', '') or ''
                task_logger.log_planner_start(task, episodic_examples)
            
            if html_logger:
                episodic_examples = getattr(plan_node, 'episodic', '') or ''
                html_logger.log_planner_start(task, episodic_examples)

            next_code = None
            plan_iteration = 0
            
            while True:
                plan_iteration += 1
                self.logger.debug(f"Plan iteration {plan_iteration}")
                
                next_plan, is_end = plan_node(h=next_code)
                self.logger.info("Plan generated: %s...", next_plan['plan'][:200])
                self.logger.debug("Plan description: %s...", next_plan['description'][:200])
                
                # Log planner history after plan generation
                if task_logger:
                    planner_history = plan_node.export_history()
                    task_logger.log_planner_history(planner_history)
                    
                if html_logger:
                    planner_history = plan_node.export_history()
                    html_logger.log_planner_history(planner_history)
                
                if is_end:
                    self.logger.info("Plan marked as complete with <END>")
                    break
                
                dev_node._init_prompt(plan=next_plan["plan"])
                test_node._init_prompt(plan=next_plan["plan"])
                self.logger.debug("Dev and test nodes initialized for current plan")

                # Log developer plan start
                current_plan_index = None
                if task_logger:
                    current_plan_index = task_logger.log_developer_plan(
                        next_plan["plan"], 
                        next_plan.get("description", "")
                    )
                
                if html_logger:
                    current_plan_index = html_logger.log_developer_plan(
                        next_plan["plan"], 
                        next_plan.get("description", "")
                    )

                next_feedback = None
                dev_test_iteration = 0
                
                while True:
                    dev_test_iteration += 1
                    self.logger.debug(f"Dev-test iteration {dev_test_iteration}")
                    
                    # Check iteration limit and add timeout feedback if exceeded
                    if dev_test_iteration > config.max_dev_test_iterations and next_feedback is not None:
                        self.logger.warning(f"Exceeded maximum iterations ({config.max_dev_test_iterations})")
                        self.logger.info("Adding timeout feedback message to encourage reflection")
                        
                        next_feedback["feedback"] += (
                            f"\nATTENTION: The development cycle has reached {dev_test_iteration} attempts, which is excessive. "
                            "Please reconsider your approach. If the task is impossible, terminate with <END> and explain why."
                        )
                        
                    next_code, is_end = dev_node(h=next_feedback)
                    self.logger.debug("Dev generated code description: %s...", next_code['description'][:200])
                    
                    if is_end:
                        self.logger.info("Dev marked task as complete with <END>")
                        break

                    next_feedback = test_node(h=next_code)
                    self.logger.debug("Test feedback: %s...", next_feedback['feedback'][:200])
                    
                    # Log code execution to HTML logger
                    if html_logger and current_plan_index:
                        html_logger.log_developer_code_execution(
                            plan_index=current_plan_index,
                            code=next_code.get('code', ''),
                            code_output=next_feedback.get('code_output', ''),
                            iteration=dev_test_iteration
                        )
                        html_logger.log_tester_feedback(
                            code=next_code.get('code', ''),
                            code_output=next_feedback.get('code_output', ''),
                            feedback=next_feedback.get('feedback', '')
                        )
                    
                    # Double check after test feedback to prevent infinite loops
                    if dev_test_iteration > config.emergency_break_iterations:
                        self.logger.warning("Forcing termination due to excessive iterations")
                        next_code = {
                            "role": "developer",
                            "code": "print('The task is too complex for me to handle. Please provide a simpler task.')",
                            "description": "The task is too complex for me to handle. Please provide a simpler task."
                        }
                        break
                
                # Log developer history after dev-test cycle completion
                if task_logger and current_plan_index:
                    dev_history = dev_node.export_history()
                    task_logger.log_developer_history(current_plan_index, dev_history)
                    
                if html_logger and current_plan_index:
                    dev_history = dev_node.export_history()
                    html_logger.log_developer_history(current_plan_index, dev_history)
            
            history = plan_node.export_history(past_n=config.critic_length)
            self.logger.info(f"Forward pass completed for model: {plan_node.model}")
            
            # Store nodes for potential learning (使用弱引用避免内存泄漏)
            self.plan_node = plan_node
            self.dev_node = dev_node
            self.test_node = test_node
            
            return history
            
        except Exception as e:
            self.logger.error(f"Error in forward pass for model {model}: {e}")
            # 发生异常时确保清理资源
            self._cleanup_nodes(plan_node, dev_node, test_node)
            raise
        finally:
            # 强制垃圾回收以释放内存
            gc.collect()

    @log_execution_time()
    def __call__(self,
        task: str,
        models: Optional[List[str]] = None,
        task_id: Optional[str] = None,
    ) -> str:
        """
        Evolve the task, use multiple parallel trajectories and judge them with the critic node.
        
        Args:
            task: Task description to solve
            models: List of models to use (defaults to config.default_models)
            task_id: Optional task identifier for workspace isolation
            
        Returns:
            Final answer from the critic node
        """

        if models is None:
            models = config.default_models

        if task_id is None:
            import uuid
            task_id = str(uuid.uuid4())[:8]
            
        self.logger.info(f"Starting task evolution with {len(models)} models (task_id: {task_id})")
        self.logger.debug("Task: %s...", task[:200])
        self.logger.debug(f"Models: {models}")
        
        # Execute task within shared isolated workspace context
        with isolated_workspace(task_id) as workspace_path:
            self.logger.info(f"Using shared isolated workspace: {workspace_path}")
            
            # Initialize critic 
            critic_node = CriticNode(model=models[random.randint(0, len(models) - 1)])
            critic_node._init_prompt(task=task)
            
            histories = []
            # 使用更轻量级的存储方式，避免保存完整的节点引用
            execution_results = []
                    
            try:
                for i, model in enumerate(tqdm(models, desc="Processing models")):
                    self.logger.info(f"Starting execution path {i+1}/{len(models)} with model: {model}")
                    
                    history = self._forward(task, model, task_id, i)
                    histories.append(history)
                    
                    # 只存储必要的信息，避免内存泄漏
                    execution_result = {
                        'model': model,
                        'history': history,
                        'index': i
                    }
                    execution_results.append(execution_result)
                    
                    self.logger.info(f"Completed execution path {i+1}/{len(models)} with model: {model}")
                    
                    # Clear workspace files after each model execution (except the last one)
                    if i < len(models) - 1:
                        self._clear_workspace_files(workspace_path)
                        self.logger.debug(f"Cleared workspace files for next model")
                    
                    # 强制垃圾回收以及时释放内存
                    gc.collect()

                self.logger.info("All execution paths completed, starting critic evaluation")
                final_answer, reason, best_id = critic_node(histories=histories)
                
                self.logger.info("Critic evaluation completed")
                self.logger.debug("Critic reason: %s...", reason[:200] if len(reason) > 500 else reason)
                self.logger.info(f"Best member index: {best_id} (model: {models[best_id]})")
                
                # Log critic result with separate loggers to avoid contaminating model logs
                critic_task_logger = get_task_logger(task_id, f"critic_{critic_node.model}")
                critic_task_logger.log_critic_result(final_answer, reason, best_id)
                
                # Save critic result to task root directory without contaminating any model's conversation history
                critic_html_logger = HTMLTaskLogger(task_id, f"critic_{critic_node.model}")
                critic_html_logger.save_critic_result_to_task_root(final_answer, reason, best_id)
                
                # Store the best path information for learning
                self.best_id = best_id
                self.execution_results = execution_results  # 使用轻量级存储
                
                self.logger.info(f"Task evolution completed successfully (task_id: {task_id})")
                return final_answer
                
            finally:
                # 清理critic节点
                self._cleanup_nodes(critic_node)
                # 强制垃圾回收
                gc.collect()

    def learn(self) -> None: # TODO contrastive learning, leveraging failed trajectories
        """
        Learn from the past experiences, save the successful experiences to the long-term memory.
        Only saves the best path as determined by the critic node.
        """ 
        if hasattr(self, 'best_id') and hasattr(self, 'best_plan_node') and hasattr(self, 'best_dev_node'):
            self.logger.info(f"Learning from best path (index {self.best_id})")
            self._save_plan_episodic()
            self._save_dev_episodic()

            self.logger.info("Successfully saved the best path experiences to the long-term memory")
            
            # 清理学习后的引用
            if hasattr(self, 'best_plan_node'):
                del self.best_plan_node
            if hasattr(self, 'best_dev_node'):
                del self.best_dev_node
            if hasattr(self, 'execution_results'):
                del self.execution_results
                
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
            if not hasattr(self, 'plan_node'):
                self.logger.warning("No plan node available for episodic saving")
                return
                
            title = self._summarize_task(self.task)
            history = self.plan_node.export_history()
            content = f"### {title}\n\n**TASK**: {self.task}\n\n```\n{history}\n```"
            
            # 使用plan_node的memory
            if hasattr(self.plan_node, 'memory'):
                self.plan_node.memory.add_episodic(content)
                self.logger.info(f"Plan episodic memory saved successfully: {title}")
            else:
                self.logger.warning("Plan node does not have memory attribute")
                
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
            if not hasattr(self, 'dev_node'):
                self.logger.warning("No dev node available for episodic saving")
                return
                
            plan_code_trajectory = self.dev_node.export_plan_code_trajectory()
            self.logger.info(f"Processing {len(plan_code_trajectory)} plan-code pairs for episodic memory")
            
            successful_saves = 0
            failed_saves = 0
            
            for i, trajectory_item in enumerate(plan_code_trajectory):
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
                    
                    # 使用dev_node的memory
                    if hasattr(self.dev_node, 'memory'):
                        self.dev_node.memory.add_episodic(content)
                        successful_saves += 1
                    else:
                        self.logger.warning("Dev node does not have memory attribute")
                        failed_saves += 1
                    
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
            # 创建临时节点来访问memory
            temp_plan_node = PlanNode(model="o4-mini")
            temp_dev_node = DevNode(model="o4-mini")
            
            temp_plan_node.memory.clear_episodic()
            temp_dev_node.memory.clear_episodic()
            
            # 清理临时节点
            self._cleanup_nodes(temp_plan_node, temp_dev_node)
            
            self.logger.info("All episodic memories cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear episodic memories: {e}")

    def __del__(self):
        """清理资源的析构函数"""
        try:
            # 清理可能残留的节点引用
            if hasattr(self, 'plan_node'):
                self._cleanup_nodes(self.plan_node)
            if hasattr(self, 'dev_node'):
                self._cleanup_nodes(self.dev_node)
            if hasattr(self, 'test_node'):
                self._cleanup_nodes(self.test_node)
        except:
            pass  # 析构函数中不应该抛出异常