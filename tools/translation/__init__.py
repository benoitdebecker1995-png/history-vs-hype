"""
Translation Pipeline Package

Clause-by-clause document translation via Claude Code, structure detection,
and split-screen formatted output for Untranslated Evidence series.

LLM calls are handled by Claude Code natively via the /translate slash command.
Python modules are pure data processors (no Anthropic SDK required).
"""

__version__ = "0.2.0"

from .structure_detector import StructureDetector
from .translator import TranslationDataBuilder
from .formatter import Formatter

__all__ = ['StructureDetector', 'TranslationDataBuilder', 'Formatter']
