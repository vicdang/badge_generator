# -*- coding: utf-8 -*-
"""
Centralized Configuration Manager

Authors: Vic Dang
Purpose: Unified configuration loading, validation, and management
"""

import json
import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional

LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CONFIG_FILE = PROJECT_ROOT / 'config' / 'config.ini'
POSITIONS_FILE = PROJECT_ROOT / 'config' / 'positions.json'


class ConfigManager:
    """Manages application configuration with validation and caching"""

    # Singleton instance
    _instance = None
    _config = None
    _positions = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._load_config()
            self._load_positions()
            self._initialized = True

    @classmethod
    def reset(cls):
        """Reset singleton instance (useful for testing)"""
        cls._instance = None
        cls._config = None
        cls._positions = None

    def _load_config(self):
        """Load configuration from INI file"""
        try:
            self._config = ConfigParser()
            if CONFIG_FILE.exists():
                self._config.read(str(CONFIG_FILE))
                LOGGER.info(f"Loaded config from {CONFIG_FILE}")
            else:
                LOGGER.warning(f"Config file not found: {CONFIG_FILE}")
        except Exception as e:
            LOGGER.error(f"Failed to load config: {e}")
            self._config = ConfigParser()

    def _load_positions(self):
        """Load positions mapping from JSON file"""
        try:
            self._positions = {}
            if POSITIONS_FILE.exists():
                with open(POSITIONS_FILE, 'r', encoding='utf-8') as f:
                    self._positions = json.load(f)
                LOGGER.info(f"Loaded positions from {POSITIONS_FILE}")
            else:
                LOGGER.warning(f"Positions file not found: {POSITIONS_FILE}")
        except Exception as e:
            LOGGER.error(f"Failed to load positions: {e}")
            self._positions = {}

    def get(self, section: str, key: str, default: Any = None, fallback: Any = None) -> Any:
        """
        Get configuration value with validation
        
        :param section: config section name
        :param key: config key name
        :param default: default value if not found
        :param fallback: fallback value (for backward compatibility)
        :return: configuration value
        """
        try:
            if self._config.has_option(section, key):
                return self._config.get(section, key)
        except Exception as e:
            LOGGER.warning(f"Error reading {section}.{key}: {e}")
        
        return fallback if fallback is not None else default

    def get_int(self, section: str, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        try:
            if self._config.has_option(section, key):
                return self._config.getint(section, key)
        except Exception as e:
            LOGGER.warning(f"Error reading int {section}.{key}: {e}")
        return default

    def get_float(self, section: str, key: str, default: float = 0.0) -> float:
        """Get float configuration value"""
        try:
            if self._config.has_option(section, key):
                return self._config.getfloat(section, key)
        except Exception as e:
            LOGGER.warning(f"Error reading float {section}.{key}: {e}")
        return default

    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        try:
            if self._config.has_option(section, key):
                return self._config.getboolean(section, key)
        except Exception as e:
            LOGGER.warning(f"Error reading bool {section}.{key}: {e}")
        return default

    def get_section(self, section: str) -> Dict[str, str]:
        """Get entire config section as dictionary"""
        try:
            if self._config.has_section(section):
                return dict(self._config.items(section))
        except Exception as e:
            LOGGER.warning(f"Error reading section {section}: {e}")
        return {}

    def get_all_sections(self) -> Dict[str, Dict[str, str]]:
        """Get all configuration sections"""
        result = {}
        try:
            for section in self._config.sections():
                result[section] = self.get_section(section)
        except Exception as e:
            LOGGER.warning(f"Error reading all sections: {e}")
        return result

    def set(self, section: str, key: str, value: Any):
        """Set configuration value (in memory only)"""
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, str(value))

    def save(self, filepath: Path = None):
        """Save configuration to file"""
        try:
            target_file = filepath or CONFIG_FILE
            with open(target_file, 'w') as f:
                self._config.write(f)
            LOGGER.info(f"Config saved to {target_file}")
        except Exception as e:
            LOGGER.error(f"Failed to save config: {e}")

    def reload(self):
        """Reload configuration from file"""
        self._load_config()
        self._load_positions()
        LOGGER.info("Configuration reloaded")

    # Convenience methods for common config values

    def get_image_paths(self) -> Dict[str, Path]:
        """Get all image directory paths"""
        paths = {
            'source': self._expand_path(self.get('general', 'src_path', 'images/source/')),
            'output': self._expand_path(self.get('general', 'des_path', 'images/output/')),
            'temp': self._expand_path(self.get('general', 'tmp_path', 'images/temp/')),
            'templates': self._expand_path(self.get('general', 'template_path', 'images/templates/')),
        }
        return paths

    def get_crawler_config(self) -> Dict[str, Any]:
        """Get crawler configuration"""
        return {
            'base_url': self.get('crawler', 'base_url', ''),
            'workers': self.get_int('crawler', 'workers', 5),
            'timeout': self.get_int('crawler', 'timeout', 30),
            'enabled': self.get_bool('crawler', 'enabled', False),
        }

    def get_badge_config(self) -> Dict[str, Any]:
        """Get badge generation configuration"""
        return {
            'template': self.get('template', 'filename', ''),
            'width': self.get_int('template', 'width', 1024),
            'height': self.get_int('template', 'height', 768),
            'font': self.get('general', 'base_font', 'Arial'),
            'text_size': self.get_int('general', 'base_text_size', 32),
        }

    def get_position(self, position_code: str) -> Optional[str]:
        """Get full position name from position code"""
        return self._positions.get(position_code)

    @staticmethod
    def _expand_path(path_str: str) -> Path:
        """Expand relative path to absolute path based on project root"""
        path = Path(path_str)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path
