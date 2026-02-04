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


# Topic detection keywords
TOPIC_KEYWORDS = {
    'holocaust': ['holocaust', 'nazi', 'hitler', 'concentration', 'genocide', 'auschwitz', 'treblinka'],
    'legal': ['treaty', 'icj', 'court', 'ruling', 'verdict', 'judgment', 'lawsuit', 'legal', 'jurisdiction'],
    'medieval': ['medieval', 'crusade', 'knight', 'feudal', 'dark ages', 'byzantine', 'carolingian'],
    'colonial': ['colonial', 'empire', 'independence', 'decolonization', 'mandate', 'protectorate'],
}

# Archive hierarchy by topic category
ARCHIVE_HIERARCHY = {
    'holocaust': [
        ('Yad Vashem', 'https://www.yadvashem.org/archive/search'),
        ('USHMM', 'https://collections.ushmm.org/search/'),
        ('Wikimedia Commons', 'https://commons.wikimedia.org/w/index.php?search={query}'),
    ],
    'legal': [
        ('ICJ Cases', 'https://www.icj-cij.org/search'),
        ('UK National Archives', 'https://discovery.nationalarchives.gov.uk/results/r?_q={query}'),
        ('UN Digital Library', 'https://digitallibrary.un.org/search?ln=en&p={query}'),
    ],
    'colonial': [
        ('UK National Archives', 'https://discovery.nationalarchives.gov.uk/results/r?_q={query}'),
        ('Library of Congress', 'https://www.loc.gov/search/?q={query}'),
        ('Wikimedia Commons', 'https://commons.wikimedia.org/w/index.php?search={query}'),
    ],
    'medieval': [
        ('British Library', 'https://www.bl.uk/catalogues-and-collections/digital-collections'),
        ('Wikimedia Commons', 'https://commons.wikimedia.org/w/index.php?search={query}'),
        ('Library of Congress', 'https://www.loc.gov/search/?q={query}'),
    ],
    'general': [
        ('Wikimedia Commons', 'https://commons.wikimedia.org/w/index.php?search={query}'),
        ('Library of Congress', 'https://www.loc.gov/search/?q={query}'),
        ('Internet Archive', 'https://archive.org/search?query={query}'),
    ],
}

# DIY instructions templates
DIY_INSTRUCTIONS = {
    'map': """1. Visit https://www.mapchart.net/world.html
2. Click regions to highlight (use different colors for emphasis)
3. Add labels for key locations
4. Add range circles or arrows if showing military/strategic reach
5. Screenshot or export as PNG
6. Optional: Add legend/title in Canva or PowerPoint""",

    'strategic_map': """1. Visit https://www.mapchart.net/world.html
2. Highlight strategic location (primary color)
3. Add range circles from location to show reach/proximity
4. Mark relevant countries/regions in secondary colors
5. Add shipping routes or strategic connections (arrows)
6. Screenshot and add annotations in Canva""",

    'timeline_graphic': """1. Open Canva or PowerPoint
2. Use timeline template or create horizontal line
3. Add date markers with labels
4. Use consistent color scheme (match channel branding)
5. Keep text minimal (dates + short labels only)
6. Export as PNG (1920x1080 or 3840x2160)""",

    'quote_card': """1. Open Canva
2. Search "quote card" templates
3. Use aged paper/document texture for historical quotes
4. Font: Serif (Times New Roman, Garamond) for formal documents
5. Include source attribution at bottom
6. Export as PNG (1920x1080 or 3840x2160)""",
}


def detect_topic_category(entities: List[Entity]) -> str:
    """
    Detect topic category from entity keywords.

    Args:
        entities: List of Entity objects

    Returns:
        Topic category: 'holocaust', 'legal', 'medieval', 'colonial', 'general'
    """
    # Aggregate all entity text
    all_text = ' '.join(e.text.lower() for e in entities)

    # Check each topic's keywords
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in all_text for kw in keywords):
            return topic

    return 'general'


def get_wikimedia_search_url(search_term: str) -> str:
    """Generate Wikimedia Commons search URL."""
    from urllib.parse import quote
    return f"https://commons.wikimedia.org/w/index.php?search={quote(search_term)}"


def get_archive_search_url(search_term: str) -> str:
    """Generate Internet Archive search URL."""
    from urllib.parse import quote
    return f"https://archive.org/search?query={quote(search_term)}"


def get_mapchart_url() -> str:
    """Static URL for MapChart.net world map editor."""
    return "https://www.mapchart.net/world.html"


def get_loc_search_url(search_term: str) -> str:
    """Generate Library of Congress search URL."""
    from urllib.parse import quote
    return f"https://www.loc.gov/search/?q={quote(search_term)}"


def get_source_urls(entity: Entity, visual_type: str, topic: str) -> List[str]:
    """
    Get source URLs for an entity based on visual type and topic.

    Args:
        entity: Entity object
        visual_type: Visual type classification
        topic: Topic category (holocaust, legal, colonial, etc.)

    Returns:
        List of up to 3 source URLs (search URLs, not fabricated file paths)
    """
    urls = []

    # For maps, always include MapChart first
    if visual_type in ['map', 'strategic_map']:
        urls.append(get_mapchart_url())

    # Get topic-specific archives
    archives = ARCHIVE_HIERARCHY.get(topic, ARCHIVE_HIERARCHY['general'])

    # Add top 2-3 archive search URLs
    for archive_name, url_template in archives[:3]:
        if '{query}' in url_template:
            url = url_template.format(query=entity.text.replace(' ', '+'))
        else:
            url = url_template
        urls.append(url)

    # Return top 3 URLs
    return urls[:3]


def assign_priority(entity: Entity, visual_type: str) -> int:
    """
    Assign priority to an entity based on mentions and visual type.

    Args:
        entity: Entity object with mentions count
        visual_type: Visual type classification

    Returns:
        Priority: 1 (Critical), 2 (High), 3 (Nice-to-have)
    """
    # Documents with 3+ mentions -> Priority 1
    if visual_type == 'primary_source_document' and entity.mentions >= 3:
        return 1

    # Maps with 5+ mentions -> Priority 1
    if visual_type in ['map', 'strategic_map'] and entity.mentions >= 5:
        return 1

    # Portraits with 5+ mentions -> Priority 1
    if visual_type == 'portrait' and entity.mentions >= 5:
        return 1

    # Timeline graphics, logos -> Priority 2
    if visual_type in ['timeline_graphic', 'logo_or_building']:
        return 2

    # High-mention items (3-4 mentions) -> Priority 2
    if entity.mentions >= 3:
        return 2

    # Everything else -> Priority 3
    return 3
