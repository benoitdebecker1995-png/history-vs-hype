"""
Translation Pipeline Package

Clause-by-clause document translation with Claude API, structure detection,
and split-screen formatted output for Untranslated Evidence series.
"""

__version__ = "0.1.0"

from .structure_detector import StructureDetector
from .translator import Translator
from .formatter import Formatter

__all__ = ['StructureDetector', 'Translator', 'Formatter']
