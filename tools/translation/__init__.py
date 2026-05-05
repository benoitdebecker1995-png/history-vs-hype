"""
Translation Pipeline Package

Clause-by-clause document translation via Claude Code, structure detection,
and split-screen formatted output for Untranslated Evidence series.

LLM calls are handled by Claude Code natively via the /translate slash command.
Python modules are pure data processors (no Anthropic SDK required).
"""

__version__ = "0.2.0"

from .pipeline import DocumentTranslationPipeline, StructureDetector, CrossChecker, LegalAnnotator, SurpriseDetector, Formatter
from .translator import TranslationDataBuilder

__all__ = ['DocumentTranslationPipeline', 'StructureDetector', 'TranslationDataBuilder', 'Formatter']
