"""
Base Checker Class for Script Quality Checkers

All checkers inherit from BaseChecker and implement:
- check(text: str) -> dict  # Returns {issues: [], stats: {}}
- name property
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseChecker(ABC):
    """Abstract base class for all script quality checkers"""

    def __init__(self, config):
        """
        Initialize checker with configuration.

        Args:
            config: Config object with threshold settings
        """
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        """Return checker name"""
        pass

    @abstractmethod
    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text and return issues.

        Args:
            text: Script text to analyze

        Returns:
            Dictionary with:
                - issues: List of issue dictionaries
                - stats: Dictionary of statistics
        """
        pass


__all__ = ['BaseChecker']
