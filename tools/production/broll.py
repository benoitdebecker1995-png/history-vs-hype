"""
B-Roll Generation Module

Converts extracted entities into actionable shot lists with source suggestions.
Generates production-ready B-roll checklists matching existing B-ROLL-DOWNLOAD-LINKS.md format.

Purpose: Enable users to generate B-roll checklists from parsed scripts in <30 seconds
instead of 2-4 hours manual work.

Usage:
    from tools.production import BRollGenerator, Shot

    generator = BRollGenerator(project_name="14-chagos-islands-2025")
    shots = generator.generate(entities, sections)
    checklist_md = generator.generate_checklist(entities, sections)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date
from .entities import Entity

# Type checking import
try:
    from .parser import Section
except ImportError:
    Section = None


@dataclass
class Shot:
    """A B-roll shot derived from an extracted entity."""
    entity: str                          # Entity text
    visual_type: str                     # map, primary_source_document, portrait, etc.
    priority: int                        # 1=Critical, 2=High, 3=Nice-to-have
    source_urls: List[str] = field(default_factory=list)  # Download/search URLs
    diy_instructions: Optional[str] = None  # Creation steps for maps/graphics
    section_references: List[str] = field(default_factory=list)  # Script sections needing this


# Keywords for visual type classification
MARITIME_KEYWORDS = ['gulf', 'ocean', 'sea', 'strait', 'bay', 'harbor', 'harbour', 'naval', 'maritime']
TERRITORY_KEYWORDS = ['island', 'archipelago', 'territory', 'region', 'peninsula', 'border', 'frontier']


def classify_visual_type(entity: Entity) -> str:
    """
    Classify entity into visual type for B-roll planning.

    Args:
        entity: Entity object with text and entity_type

    Returns:
        Visual type string: 'map', 'primary_source_document', 'portrait',
        'historical_photo', 'timeline_graphic', 'strategic_map', 'logo_or_building'
    """
    entity_lower = entity.text.lower()

    # Document entities -> primary source documents
    if entity.entity_type == 'document':
        return 'primary_source_document'

    # Place entities with maritime context -> strategic maps
    if entity.entity_type == 'place':
        if any(kw in entity_lower for kw in MARITIME_KEYWORDS):
            return 'strategic_map'
        # Territory context -> general map
        if any(kw in entity_lower for kw in TERRITORY_KEYWORDS):
            return 'map'
        # City/landmark -> historical photo
        return 'historical_photo'

    # Person entities -> portraits
    if entity.entity_type == 'person':
        return 'portrait'

    # Date entities -> timeline graphics
    if entity.entity_type == 'date':
        return 'timeline_graphic'

    # Organization entities -> logo or building photos
    if entity.entity_type == 'organization':
        return 'logo_or_building'

    # Default fallback
    return 'historical_photo'
