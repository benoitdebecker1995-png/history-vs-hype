"""
Production Tools Module

Provides script parsing and entity extraction for the v1.5 Production Acceleration pipeline.

Components:
- ScriptParser: Parses markdown scripts into structured sections
- EntityExtractor: Extracts named entities (places, people, documents, dates, organizations)
- BRollGenerator: Generates B-roll shot lists from entities
- EditGuideGenerator: Generates timing-aware edit guides with shot breakdowns
- MetadataGenerator: Generates METADATA-DRAFT.md with titles, descriptions, chapters, tags
- Section: Dataclass representing a parsed script section
- Entity: Dataclass representing an extracted entity
- Shot: Dataclass representing a B-roll shot
- SectionTiming: Dataclass representing section timing information

Usage:
    from tools.production import ScriptParser, EntityExtractor, BRollGenerator
    from tools.production import Section, Entity, Shot

    parser = ScriptParser()
    extractor = EntityExtractor()
    broll_gen = BRollGenerator(project_name="14-chagos-islands-2025")

    sections = parser.parse_file('path/to/script.md')
    entities = extractor.extract_from_sections(sections)
    checklist = broll_gen.generate_checklist(entities, sections)
"""

from .parser import ScriptParser, Section
from .entities import EntityExtractor, Entity
from .broll import BRollGenerator, Shot
from .editguide import EditGuideGenerator, SectionTiming
from .metadata import MetadataGenerator

__all__ = [
    'ScriptParser', 'Section',
    'EntityExtractor', 'Entity',
    'BRollGenerator', 'Shot',
    'EditGuideGenerator', 'SectionTiming',
    'MetadataGenerator'
]
