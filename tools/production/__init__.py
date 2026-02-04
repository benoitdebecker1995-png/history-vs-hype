"""
Production Tools Module

Provides script parsing and entity extraction for the v1.5 Production Acceleration pipeline.

Components:
- ScriptParser: Parses markdown scripts into structured sections
- EntityExtractor: Extracts named entities (places, people, documents, dates, organizations)
- Section: Dataclass representing a parsed script section
- Entity: Dataclass representing an extracted entity

Usage:
    from tools.production import ScriptParser, EntityExtractor, Section, Entity

    parser = ScriptParser()
    extractor = EntityExtractor()

    sections = parser.parse_file('path/to/script.md')
    entities = extractor.extract_from_sections(sections)
"""

from .parser import ScriptParser, Section
from .entities import EntityExtractor, Entity

__all__ = ['ScriptParser', 'Section', 'EntityExtractor', 'Entity']
