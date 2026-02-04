"""
Entity Extraction Module

Extracts named entities from script text using hybrid regex + optional spaCy approach.
Detects documents, places, people, dates, and organizations for downstream B-roll planning.

Usage:
    from tools.production import EntityExtractor, Entity

    extractor = EntityExtractor()  # Regex-only (no dependencies)
    extractor = EntityExtractor(use_spacy=True)  # Enhanced with spaCy NER

    entities = extractor.extract(text)
    entities = extractor.extract_from_sections(sections)
"""

import re
from dataclasses import dataclass, field
from typing import List, Set, Dict, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import Section


@dataclass
class Entity:
    """A named entity extracted from script text."""
    text: str              # Entity text as found in script
    entity_type: str       # 'place', 'person', 'document', 'date', 'organization'
    mentions: int          # Number of times mentioned
    positions: List[int]   # Line numbers where mentioned
    normalized: str        # Lowercase, normalized form for deduplication


# Domain-specific keyword dictionaries (following classifiers.py pattern)
DOCUMENT_KEYWORDS = [
    'treaty', 'act', 'order', 'agreement', 'accord', 'convention', 'protocol',
    'ruling', 'resolution', 'declaration', 'memo', 'constitution', 'law',
    'opinion', 'report', 'charter', 'statute', 'ordinance', 'proclamation',
    'mandate', 'covenant', 'memorandum', 'directive', 'code'
]

PLACE_INDICATORS = [
    'island', 'islands', 'peninsula', 'gulf', 'ocean', 'sea', 'strait',
    'bay', 'coast', 'river', 'lake', 'mountain', 'valley', 'desert',
    'archipelago', 'territory', 'region', 'province', 'state', 'county',
    'district', 'zone', 'border', 'frontier', 'harbor', 'harbour', 'port'
]

ORG_KEYWORDS = [
    'union', 'court', 'council', 'organization', 'organisation', 'committee',
    'commission', 'assembly', 'parliament', 'congress', 'senate', 'agency',
    'authority', 'administration', 'ministry', 'department', 'office',
    'federation', 'league', 'alliance', 'coalition', 'bloc'
]

TITLE_KEYWORDS = [
    'prime minister', 'president', 'foreign minister', 'premier', 'king',
    'queen', 'emperor', 'sultan', 'shah', 'general', 'admiral', 'colonel',
    'ambassador', 'secretary', 'minister', 'governor', 'mayor', 'chairman',
    'chairperson', 'director', 'chief', 'commander', 'judge'
]

# Known organizations (abbreviations and full names)
KNOWN_ORGS = {
    'UN': 'United Nations',
    'AU': 'African Union',
    'EU': 'European Union',
    'ICJ': 'International Court of Justice',
    'NATO': 'North Atlantic Treaty Organization',
    'UNGA': 'UN General Assembly',
    'UNESCO': 'UNESCO',
    'WHO': 'World Health Organization',
    'IMF': 'International Monetary Fund',
    'WTO': 'World Trade Organization',
    'ICC': 'International Criminal Court',
    'ECHR': 'European Court of Human Rights',
    'OPEC': 'OPEC',
    'BRICS': 'BRICS',
    'ASEAN': 'ASEAN',
    'OAS': 'Organization of American States',
    'FCDO': 'Foreign, Commonwealth and Development Office',
}

# Common country/place names for detection
KNOWN_PLACES = {
    'Africa', 'Asia', 'Europe', 'America', 'Americas', 'Antarctica',
    'Britain', 'UK', 'United Kingdom', 'England', 'Scotland', 'Wales', 'Ireland',
    'France', 'Germany', 'Italy', 'Spain', 'Portugal', 'Netherlands', 'Belgium',
    'Russia', 'Soviet Union', 'USSR', 'China', 'Japan', 'India', 'Pakistan',
    'United States', 'USA', 'US', 'Canada', 'Mexico', 'Brazil', 'Argentina',
    'Egypt', 'Ethiopia', 'Kenya', 'Somalia', 'Somaliland', 'Djibouti', 'Eritrea',
    'Israel', 'Palestine', 'Iran', 'Iraq', 'Syria', 'Turkey', 'Saudi Arabia',
    'Australia', 'New Zealand', 'Indonesia', 'Malaysia', 'Singapore',
    'Mauritius', 'Seychelles', 'Madagascar', 'Diego Garcia', 'Chagos',
    'London', 'Paris', 'Berlin', 'Rome', 'Moscow', 'Beijing', 'Washington',
    'Persian Gulf', 'Red Sea', 'Indian Ocean', 'Mediterranean', 'Atlantic',
    'Gulf of Aden', 'Horn of Africa', 'Middle East', 'South Asia', 'East Africa',
    'Lancaster House', 'Berbera', 'Burao', 'Hargeisa'
}

# Month names for date detection
MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# B-roll and script markers to strip before entity extraction
MARKER_PATTERNS = [
    re.compile(r'\*\*\[.*?\]\*\*'),           # **[ON-CAMERA]**, **[VO]**, etc.
    re.compile(r'\[B-ROLL:.*?\]'),             # [B-ROLL: ...]
    re.compile(r'\[MAP:.*?\]'),                # [MAP: ...]
    re.compile(r'\[DOCUMENT.*?\]'),            # [DOCUMENT ...] or [DOCUMENT DISPLAY: ...]
    re.compile(r'\[TEXT ON SCREEN:.*?\]'),     # [TEXT ON SCREEN: ...]
    re.compile(r'\[NEWS.*?\]'),                # [NEWS FOOTAGE: ...] or [NEWS: ...]
    re.compile(r'\[QUOTE.*?\]'),               # [QUOTE ON SCREEN: ...]
    re.compile(r'\[PRIMARY SOURCE.*?\]'),      # [PRIMARY SOURCE READOUT]
    re.compile(r'\[TALKING HEAD\]'),           # [TALKING HEAD]
    re.compile(r'\[CAVEAT\]'),                 # [CAVEAT]
    re.compile(r'\[STAKES.*?\]'),              # [STAKES - 0:25]
    re.compile(r'\[AUTHORITY.*?\]'),           # [AUTHORITY MARKER - 0:30]
    re.compile(r'\[PAYOFF.*?\]'),              # [PAYOFF - 0:35]
    re.compile(r'\[RETURN TO EXTREMES\]'),     # [RETURN TO EXTREMES]
    re.compile(r'\[VO\]'),                     # [VO]
    re.compile(r'\[ON-CAMERA\]'),              # [ON-CAMERA]
]

# False positive person names to filter out
PERSON_BLOCKLIST = {
    'king head', 'talking head', 'primary source', 'text on screen',
    'document display', 'on camera', 'reading', 'quote', 'visual',
    'priority', 'pacing', 'word count', 'ignition', 'retention',
    'causal clarity', 'steelman', 'ending', 'spoken', 'delivery',
    'changes', 'from', 'the object', 'that phrase'
}


class EntityExtractor:
    """
    Extracts named entities from script text.

    Uses hybrid approach:
    - Regex patterns for domain-specific entities (always available)
    - Optional spaCy NER for enhanced coverage (requires spaCy installation)
    """

    def __init__(self, use_spacy: bool = False):
        """
        Initialize the entity extractor.

        Args:
            use_spacy: If True, use spaCy NER for enhanced extraction.
                       Falls back to regex-only if spaCy unavailable.
        """
        self.use_spacy = use_spacy
        self._nlp = None  # Lazy load spaCy

    @property
    def nlp(self):
        """Lazy-load spaCy model (following flow.py pattern)."""
        if self._nlp is None:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm")
            except (ImportError, OSError) as e:
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm"
                ) from e
        return self._nlp

    def _strip_markers(self, text: str) -> str:
        """Strip B-roll markers from text before entity extraction."""
        clean = text
        for pattern in MARKER_PATTERNS:
            clean = pattern.sub(' ', clean)
        return clean

    def extract(self, text: str, base_line: int = 1) -> List[Entity]:
        """
        Extract entities from text.

        Args:
            text: Script text to analyze
            base_line: Starting line number for position tracking

        Returns:
            List of Entity objects
        """
        entities_dict: Dict[str, Entity] = {}

        # Strip markers before extraction
        clean_text = self._strip_markers(text)

        # Extract with regex patterns (always available)
        self._extract_documents(clean_text, base_line, entities_dict)
        self._extract_dates(clean_text, base_line, entities_dict)
        self._extract_places(clean_text, base_line, entities_dict)
        self._extract_organizations(clean_text, base_line, entities_dict)
        self._extract_people(clean_text, base_line, entities_dict)

        # Enhance with spaCy if requested and available
        if self.use_spacy:
            try:
                self._extract_with_spacy(clean_text, base_line, entities_dict)
            except RuntimeError:
                pass  # Graceful fallback to regex-only

        return list(entities_dict.values())

    def extract_from_sections(self, sections: List['Section']) -> List[Entity]:
        """
        Extract entities from multiple sections and merge.

        Args:
            sections: List of Section objects from ScriptParser

        Returns:
            Merged list of Entity objects with aggregated counts
        """
        all_entities: Dict[str, Entity] = {}

        for section in sections:
            section_entities = self.extract(section.content, section.start_line)

            for entity in section_entities:
                if entity.normalized in all_entities:
                    # Merge with existing
                    existing = all_entities[entity.normalized]
                    existing.mentions += entity.mentions
                    existing.positions.extend(entity.positions)
                    # Keep the longer/more complete text version
                    if len(entity.text) > len(existing.text):
                        existing.text = entity.text
                else:
                    all_entities[entity.normalized] = entity

        return list(all_entities.values())

    def _normalize(self, text: str) -> str:
        """Normalize entity text for deduplication."""
        # Lowercase, strip 'the ', collapse whitespace
        normalized = text.lower().strip()
        if normalized.startswith('the '):
            normalized = normalized[4:]
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized

    def _add_entity(
        self,
        entities_dict: Dict[str, Entity],
        text: str,
        entity_type: str,
        line: int
    ):
        """Add or update an entity in the dictionary."""
        normalized = self._normalize(text)
        if not normalized or len(normalized) < 2:
            return

        # Filter out known false positives for person entities
        if entity_type == 'person' and normalized in PERSON_BLOCKLIST:
            return

        if normalized in entities_dict:
            entities_dict[normalized].mentions += 1
            if line not in entities_dict[normalized].positions:
                entities_dict[normalized].positions.append(line)
            # Keep longer text version
            if len(text) > len(entities_dict[normalized].text):
                entities_dict[normalized].text = text
        else:
            entities_dict[normalized] = Entity(
                text=text,
                entity_type=entity_type,
                mentions=1,
                positions=[line],
                normalized=normalized
            )

    def _get_line_number(self, text: str, char_pos: int, base_line: int) -> int:
        """Convert character position to line number."""
        return base_line + text[:char_pos].count('\n')

    def _extract_documents(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Extract document entities (treaties, acts, rulings, etc.)."""
        # Pattern for formal document names
        # e.g., "British Somaliland Independence Act 1960"
        doc_suffix = '|'.join(DOCUMENT_KEYWORDS)
        pattern = re.compile(
            rf'(?:the\s+)?([A-Z][A-Za-z\s\-\']+(?:{doc_suffix})\s*(?:of\s+)?\d{{4}}?)',
            re.IGNORECASE
        )

        for match in pattern.finditer(text):
            doc_text = match.group(1).strip()
            # Clean up the text
            doc_text = re.sub(r'\s+', ' ', doc_text)
            line = self._get_line_number(text, match.start(), base_line)
            self._add_entity(entities_dict, doc_text, 'document', line)

        # Also detect documents by explicit patterns
        explicit_patterns = [
            r'(?:the\s+)?([A-Z][A-Za-z\s\-\']+(?:Act|Treaty|Order|Agreement|Accord|Convention|Resolution|Declaration|Constitution|Ruling|Protocol|Memorandum|MOU))\s*(?:\(|\,|\.|$)',
            r'(?:ICJ|UN|AU)\s+(?:Advisory\s+)?(?:Opinion|Report|Resolution)\s*(?:\(?\d{4}\)?)?',
        ]

        for pat in explicit_patterns:
            for match in re.finditer(pat, text):
                doc_text = match.group(0).strip().rstrip('.,()').strip()
                if len(doc_text) > 5:
                    line = self._get_line_number(text, match.start(), base_line)
                    self._add_entity(entities_dict, doc_text, 'document', line)

    def _extract_dates(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Extract date entities."""
        months_pattern = '|'.join(MONTHS)

        # Full dates: "June 26, 1960" or "26th June 1960"
        patterns = [
            rf'({months_pattern})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(\d{{4}})',
            rf'(\d{{1,2}})(?:st|nd|rd|th)?\s+({months_pattern}),?\s+(\d{{4}})',
            rf'({months_pattern})\s+(\d{{4}})',  # "June 1960"
        ]

        for pat in patterns:
            for match in re.finditer(pat, text):
                date_text = match.group(0).strip()
                line = self._get_line_number(text, match.start(), base_line)
                self._add_entity(entities_dict, date_text, 'date', line)

        # Standalone years in context (e.g., "in 1960", "by 1991")
        year_pattern = r'(?:in|by|since|until|from|after|before|during)\s+(\d{4})'
        for match in re.finditer(year_pattern, text, re.IGNORECASE):
            year = match.group(1)
            if 1800 <= int(year) <= 2100:
                line = self._get_line_number(text, match.start(), base_line)
                self._add_entity(entities_dict, year, 'date', line)

    def _extract_places(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Extract place entities."""
        # Known places
        for place in KNOWN_PLACES:
            # Word boundary match
            pattern = re.compile(rf'\b{re.escape(place)}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                matched_text = match.group(0)
                line = self._get_line_number(text, match.start(), base_line)
                self._add_entity(entities_dict, matched_text, 'place', line)

        # Places with geographic indicators
        # e.g., "Chagos Archipelago", "Gulf of Aden"
        indicators = '|'.join(PLACE_INDICATORS)
        patterns = [
            rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+({indicators})',  # Name + indicator
            rf'({indicators})\s+of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # indicator of Name
        ]

        for pat in patterns:
            for match in re.finditer(pat, text, re.IGNORECASE):
                place_text = match.group(0).strip()
                line = self._get_line_number(text, match.start(), base_line)
                self._add_entity(entities_dict, place_text, 'place', line)

    def _extract_organizations(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Extract organization entities."""
        # Known organization abbreviations
        for abbrev, full_name in KNOWN_ORGS.items():
            pattern = re.compile(rf'\b{re.escape(abbrev)}\b')
            for match in pattern.finditer(text):
                line = self._get_line_number(text, match.start(), base_line)
                self._add_entity(entities_dict, abbrev, 'organization', line)

        # "The [Adjective] [Org word]" pattern
        # e.g., "the African Union", "the United Nations"
        org_words = '|'.join(ORG_KEYWORDS)
        pattern = re.compile(
            rf'(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+({org_words})',
            re.IGNORECASE
        )
        for match in pattern.finditer(text):
            org_text = match.group(0).strip()
            if not org_text.lower().startswith('the '):
                org_text = org_text
            line = self._get_line_number(text, match.start(), base_line)
            self._add_entity(entities_dict, org_text, 'organization', line)

    def _extract_people(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Extract person entities."""
        # Titled individuals
        # e.g., "Prime Minister Netanyahu", "President Wilson"
        titles = '|'.join(TITLE_KEYWORDS)
        pattern = re.compile(
            rf'({titles})\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            re.IGNORECASE
        )
        for match in pattern.finditer(text):
            person_text = match.group(0).strip()
            line = self._get_line_number(text, match.start(), base_line)
            self._add_entity(entities_dict, person_text, 'person', line)

        # Named individuals in context (Name + verb patterns)
        # e.g., "Chen Yi sent", "Ramgoolam signed"
        person_verb_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:sent|signed|wrote|said|announced|declared|ruled|found|stated|argued|claimed)'
        for match in re.finditer(person_verb_pattern, text):
            # Filter out common non-person words
            name = match.group(1).strip()
            if name.lower() not in ['the', 'this', 'that', 'they', 'which', 'britain', 'france', 'mauritius', 'somalia']:
                if name not in KNOWN_PLACES:
                    line = self._get_line_number(text, match.start(), base_line)
                    self._add_entity(entities_dict, name, 'person', line)

        # Specific scholars/judges mentioned with context
        scholar_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)[\'s]*\s+(?:analysis|conclusion|argument|ruling|opinion|report|finding)'
        for match in re.finditer(scholar_pattern, text):
            name = match.group(1).strip()
            if name.lower() not in ['the', 'their', 'his', 'her', 'its', 'this']:
                if name not in KNOWN_PLACES and name not in KNOWN_ORGS:
                    line = self._get_line_number(text, match.start(), base_line)
                    self._add_entity(entities_dict, name, 'person', line)

    def _extract_with_spacy(
        self,
        text: str,
        base_line: int,
        entities_dict: Dict[str, Entity]
    ):
        """Enhance extraction with spaCy NER."""
        doc = self.nlp(text)

        type_mapping = {
            'PERSON': 'person',
            'GPE': 'place',      # Geopolitical entities
            'LOC': 'place',      # Locations
            'ORG': 'organization',
            'DATE': 'date',
            'NORP': 'organization',  # Nationalities, religious, political groups
        }

        for ent in doc.ents:
            if ent.label_ in type_mapping:
                entity_type = type_mapping[ent.label_]
                line = self._get_line_number(text, ent.start_char, base_line)
                self._add_entity(entities_dict, ent.text, entity_type, line)
