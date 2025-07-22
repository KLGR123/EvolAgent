"""
Configuration management module for EvolAgent.
Provides centralized access to all system configurations.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """
    Configuration manager that loads and provides access to system settings.
    """
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent.parent / "config.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot notation key.
        
        Args:
            key: Configuration key in dot notation (e.g., 'pipeline.max_dev_test_iterations')
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., 'pipeline', 'memory')
            
        Returns:
            Dictionary containing the section configuration
        """
        return self._config.get(section, {})
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    # Convenience properties for frequently accessed configurations
    @property
    def max_dev_test_iterations(self) -> int:
        return self.get('pipeline.max_dev_test_iterations', 50)
    
    @property
    def max_parallel_tasks(self) -> int:
        return self.get('pipeline.max_parallel_tasks', 3)
    
    @property
    def emergency_break_iterations(self) -> int:
        return self.get('pipeline.emergency_break_iterations', 55)
    
    @property
    def max_tokens_per_chunk(self) -> int:
        return self.get('memory.max_tokens_per_chunk', 8192)
    
    @property
    def semantic_search_limit(self) -> int:
        return self.get('memory.semantic_search_limit', 3)
    
    @property
    def episodic_search_limit(self) -> int:
        return self.get('memory.episodic_search_limit', 3)
    
    @property
    def score_threshold(self) -> float:
        return self.get('memory.score_threshold', 0.35)
    
    @property
    def default_embedding_model(self) -> str:
        return self.get('models.default_embedding_model', 'text-embedding-3-large')
    
    @property
    def embedding_dimension(self) -> int:
        return self.get('models.embedding_dimension', 3072)
    
    @property
    def default_models(self) -> list:
        return self.get('models.default_models', [
            "o4-mini",
            "anthropic.claude-sonnet-4-20250514-v1:0", 
            "anthropic.claude-opus-4-20250514-v1:0"
        ])
    
    @property
    def max_history_tokens(self) -> int:
        return self.get('nodes.max_history_tokens', 199999)
    
    @property
    def adaptive_history_length(self) -> int:
        return self.get('nodes.adaptive_history_length', 10)
    
    @property
    def dev_history_length(self) -> int:
        return self.get('nodes.dev_history_length', 4)
    
    @property
    def test_history_length(self) -> int:
        return self.get('nodes.test_history_length', 6)
    
    @property
    def workspace_dir(self) -> str:
        return self.get('environment.workspace_dir', 'workspace')
    
    @property
    def qdrant_persist_path(self) -> str:
        return self.get('environment.qdrant_persist_path', './qdrant_data')
    
    @property
    def log_level(self) -> str:
        return self.get('logging.level', 'INFO')
    
    @property
    def log_format(self) -> str:
        return self.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    @property
    def log_file_path(self) -> str:
        return self.get('logging.file_path', 'logs/evolagent.log')
    
    @property
    def log_max_file_size(self) -> int:
        return self.get('logging.max_file_size', 10485760)
    
    @property
    def log_backup_count(self) -> int:
        return self.get('logging.backup_count', 5)
    
    @property
    def console_output(self) -> bool:
        return self.get('logging.console_output', True)
    
    @property
    def api_timeout(self) -> int:
        return self.get('timeout.api_timeout', 30)
    
    @property
    def max_retries(self) -> int:
        return self.get('timeout.max_retries', 3)
    
    @property
    def retry_delay(self) -> float:
        return self.get('timeout.retry_delay', 1.0)
    
    @property
    def summarize_max_tokens(self) -> int:
        return self.get('task.summarize_max_tokens', 1000)
    
    @property
    def summarize_temperature(self) -> float:
        return self.get('task.summarize_temperature', 0.1)

    @property
    def max_tokens(self) -> int:
        return self.get('models.max_tokens', 32000)

# Global configuration instance
config = Config()


if __name__ == "__main__":
    # Test configuration loading
    print("Configuration loaded successfully!")
    print(f"Max dev test iterations: {config.max_dev_test_iterations}")
    print(f"Default models: {config.default_models}")
    print(f"Log level: {config.log_level}") 