"""
Configuration loader for scoring rules and caption presets.
Loads TOML files from config directory.
"""

import toml
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Determine if running as bundled executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running as script
    BASE_DIR = Path(__file__).parent.parent.parent

# Config files are bundled with executable
CONFIG_DIR = BASE_DIR / "config"

# Data directories can be set by launcher (for executable)
# or default to BASE_DIR (for development)
DATA_DIR = Path(os.environ.get('APP_DATA_DIR', BASE_DIR / "data"))
MODELS_DIR = Path(os.environ.get('APP_MODELS_DIR', BASE_DIR / "models"))
LOGS_DIR = Path(os.environ.get('APP_LOGS_DIR', BASE_DIR / "logs"))


class Config:
    """Global configuration manager."""

    def __init__(self):
        self.scoring_rules = self._load_scoring_rules()
        self.caption_presets = self._load_caption_presets()

    def _load_scoring_rules(self) -> Dict[str, Any]:
        """Load scoring rules from TOML file."""
        path = CONFIG_DIR / "scoring_rules.toml"
        if not path.exists():
            raise FileNotFoundError(f"Scoring rules not found at {path}")
        return toml.load(path)

    def _load_caption_presets(self) -> Dict[str, Any]:
        """Load caption presets from TOML file."""
        path = CONFIG_DIR / "caption_presets.toml"
        if not path.exists():
            raise FileNotFoundError(f"Caption presets not found at {path}")
        return toml.load(path)

    def get_caption_preset(self, preset_name: str = "academic") -> Dict[str, Any]:
        """Get a specific caption preset by name."""
        if preset_name not in self.caption_presets:
            raise ValueError(f"Unknown preset: {preset_name}. Available: {list(self.caption_presets.keys())}")
        return self.caption_presets[preset_name]


# Global config instance
config = Config()
