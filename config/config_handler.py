"""
Configuration file handling
"""

import json
import os
from typing import Dict, Any

class ConfigHandler:
    def __init__(self, config_path: str = 'config/config.json'):
        """
        Initialize configuration handler
        :param config_path: Path to config file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        :return: Dictionary with configuration
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Config file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in config file {self.config_path}")

    def get_shopify_config(self) -> Dict[str, str]:
        """Get Shopify-specific configuration"""
        return self.config.get('shopify', {})

    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        return self.config.get('app', {})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot notation
        :param key: Key in dot notation (e.g., 'shopify.api_key')
        :param default: Default value if key not found
        :return: Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k)
            if value is None:
                return default
        return value