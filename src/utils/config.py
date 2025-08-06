"""
Configuration management for EvolAgent.

This module provides a centralized configuration manager that reads all settings
from config.yaml without any hardcoded hyperparameters.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class ConfigManager:
    """
    Configuration manager that loads all settings from config.yaml.
    No hardcoded hyperparameters - everything comes from the YAML file.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = Path(config_path)
        self._config_data = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config_data = yaml.safe_load(f) or {}
                
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.config_path}: {e}")
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'models.default_models')
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Dictionary containing the section data
        """
        return self._config_data.get(section, {})
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value (runtime only, not saved to file).
        
        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split('.')
        config_section = self._config_data
        
        for k in keys[:-1]:
            if k not in config_section:
                config_section[k] = {}
            config_section = config_section[k]
        
        config_section[keys[-1]] = value
    
    def has(self, key: str) -> bool:
        """
        Check if configuration key exists.
        
        Args:
            key: Configuration key in dot notation
            
        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None


# Global configuration instance
config = ConfigManager() 