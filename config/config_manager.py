#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager for ClipForge
Handles application configuration persistence and management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _get_config_directory(self) -> Path:
        """Get the configuration directory path"""
        documents_path = Path.home() / "Documents"
        config_dir = documents_path / "ClipForge" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values"""
        documents_path = Path.home() / "Documents"
        default_output_path = documents_path / "ClipForge" / "clips"
        
        return {
            "output_path": str(default_output_path),
            "last_duration": 30,
            "available_durations": [15, 20, 30, 45, 60, 90, 120],
            "window_size": {"width": 800, "height": 600},
            "window_position": {"x": 100, "y": 100},
            "theme": "default",
            "auto_create_folders": True,
            "overwrite_existing": False
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default config to ensure all keys exist
                    default_config = self._get_default_config()
                    default_config.update(config)
                    return default_config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                return self._get_default_config()
        else:
            # Create default config file
            config = self._get_default_config()
            self._save_config(config)
            return config
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value and save"""
        self.config[key] = value
        return self._save_config(self.config)
    
    def get_output_path(self) -> str:
        """Get the output path for clips"""
        return self.get("output_path")
    
    def set_output_path(self, path: str) -> bool:
        """Set the output path for clips"""
        return self.set("output_path", path)
    
    def get_last_duration(self) -> int:
        """Get the last selected duration"""
        return self.get("last_duration", 30)
    
    def set_last_duration(self, duration: int) -> bool:
        """Set the last selected duration"""
        return self.set("last_duration", duration)
    
    def get_available_durations(self) -> list:
        """Get available duration options"""
        return self.get("available_durations", [15, 20, 30, 45, 60, 90, 120])
    
    def get_window_size(self) -> Dict[str, int]:
        """Get window size configuration"""
        return self.get("window_size", {"width": 800, "height": 600})
    
    def set_window_size(self, width: int, height: int) -> bool:
        """Set window size configuration"""
        return self.set("window_size", {"width": width, "height": height})
    
    def get_window_position(self) -> Dict[str, int]:
        """Get window position configuration"""
        return self.get("window_position", {"x": 100, "y": 100})
    
    def set_window_position(self, x: int, y: int) -> bool:
        """Set window position configuration"""
        return self.set("window_position", {"x": x, "y": y})
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self.config = self._load_config()
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        self.config = self._get_default_config()
        return self._save_config(self.config) 