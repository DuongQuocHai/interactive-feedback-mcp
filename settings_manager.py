# Settings Manager for Tkinter version
# Equivalent to QSettings functionality
import os
import json
import hashlib
from typing import Any, Optional, Dict
from pathlib import Path

class SettingsManager:
    """Settings manager equivalent to QSettings for cross-platform compatibility"""
    
    def __init__(self, organization: str, application: str):
        self.organization = organization
        self.application = application
        self.settings_dir = self._get_settings_dir()
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self.settings = self._load_settings()
    
    def _get_settings_dir(self) -> str:
        """Get platform-specific settings directory"""
        if os.name == 'nt':  # Windows
            base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
        elif os.name == 'posix':  # macOS/Linux
            if os.uname().sysname == 'Darwin':  # macOS
                base_dir = os.path.expanduser('~/Library/Preferences')
            else:  # Linux
                base_dir = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        else:
            base_dir = os.path.expanduser('~')
        
        settings_dir = os.path.join(base_dir, self.organization, self.application)
        os.makedirs(settings_dir, exist_ok=True)
        return settings_dir
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def beginGroup(self, group: str):
        """Begin a settings group (context manager)"""
        return SettingsGroup(self, group)
    
    def setValue(self, key: str, value: Any):
        """Set a value in the current group"""
        if not hasattr(self, '_current_group'):
            self._current_group = 'default'
        
        if self._current_group not in self.settings:
            self.settings[self._current_group] = {}
        
        self.settings[self._current_group][key] = value
        self._save_settings()
    
    def value(self, key: str, default: Any = None, type: type = None) -> Any:
        """Get a value from the current group"""
        if not hasattr(self, '_current_group'):
            self._current_group = 'default'
        
        if self._current_group not in self.settings:
            return default
        
        value = self.settings[self._current_group].get(key, default)
        
        if type and value is not None:
            try:
                return type(value)
            except (ValueError, TypeError):
                return default
        
        return value
    
    def get_project_group_name(self, project_dir: str) -> str:
        """Get project-specific group name"""
        basename = os.path.basename(os.path.normpath(project_dir))
        full_hash = hashlib.md5(project_dir.encode('utf-8')).hexdigest()[:8]
        return f"{basename}_{full_hash}"

class SettingsGroup:
    """Context manager for settings groups"""
    
    def __init__(self, settings_manager: SettingsManager, group: str):
        self.settings_manager = settings_manager
        self.group = group
        self.original_group = None
    
    def __enter__(self):
        self.original_group = getattr(self.settings_manager, '_current_group', 'default')
        self.settings_manager._current_group = self.group
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.settings_manager._current_group = self.original_group

def get_project_settings_group(project_dir: str) -> str:
    """Get project-specific settings group name"""
    basename = os.path.basename(os.path.normpath(project_dir))
    full_hash = hashlib.md5(project_dir.encode('utf-8')).hexdigest()[:8]
    return f"{basename}_{full_hash}"

