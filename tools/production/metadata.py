"""
Metadata Draft Generation Module

Generates METADATA-DRAFT.md files from parsed scripts with auto-generated titles,
descriptions, chapters, and tags. Applies documentary tone filtering to reject
clickbait patterns.

Purpose: Reduce YouTube publishing prep from 30+ minutes to <1 minute by automating
metadata generation from script content.

Usage:
    from tools.production import MetadataGenerator

    generator = MetadataGenerator(project_name="14-chagos-islands-2025")
    metadata = generator.generate_metadata_draft(sections, entities, timings)
"""

import os
import re
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple
from .parser import Section
from .entities import Entity
from .editguide import SectionTiming, format_time
from .title_generator import generate_title_candidates, format_title_candidates, TitleMaterialExtractor
from tools.title_scorer import CLICKBAIT_PATTERNS, ALLOWED_ACRONYMS

# Title constraints
MAX_TITLE_LENGTH = 70
TARGET_TITLE_LENGTH = (60, 70)
TARGET_TAG_COUNT = (15, 20)

# ---------------------------------------------------------------------------
# Citation extraction patterns (META-01)
# ---------------------------------------------------------------------------
# Pattern 1: "According to Chris Wickham in The Inheritance of Rome, page 147"
_CITATION_PATTERN_ACCORDING_TO = re.compile(
    r'(?:According to|per)\s+'
    r'([A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Za-z]+)*)\s+'
    r'in\s+[*"]?([A-Z][^,\n"*]{3,80}?)[*"]?,\s*'
    r'(?:pages?|pp?\.?)\s*(\d+)',
    re.IGNORECASE,
)
# Pattern 2: "Harris's *Ancient Literacy*, p. 23"
_CITATION_PATTERN_POSSESSIVE = re.compile(
    r"([A-Z][a-z]+(?:'s)?)\s+"
    r'[*"]([A-Z][^"*\n]{3,60})[*"][,\s]+'
    r'(?:pages?|pp?\.?)\s*(\d+)',
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Thumbnail pattern → concept templates (META-02)
# ---------------------------------------------------------------------------
THUMBNAIL_PATTERNS = {
    'territorial': ['split_map_conflict', 'document_on_map', 'geo_plus_evidence'],
    'ideological': ['myth_vs_reality', 'document_reveal', 'timeline_contrast'],
    'political_fact_check': ['document_on_map', 'quote_vs_reality', 'map_timeline'],
    'general': ['split_map_conflict', 'document_on_map', 'geo_plus_evidence'],
}


@dataclass
class TitleVariant:
    """
    A generated title variant with focus description.

    DEPRECATED: Replaced by ranked scored candidates from title_generator.
    Kept for backward compatibility with any external references.
    """
    variant: str        # 'A', 'B', 'C'
    title: str          # Title text
    focus: str          # What this variant emphasizes
    length: int         # Character count


class MetadataGenerator:
    """
    Generates METADATA-DRAFT.md files from parsed scripts.

    Produces documentary-tone titles, descriptions with document lists,
    chapters from section timings, and entity-based tags.
    """

    def __init__(self, project_name: str = "Untitled", db_path: Optional[str] = None):
        """
        Initialize the metadata generator.

        Args:
            project_name: Project identifier (e.g., "14-chagos-islands-2025")
            db_path:      Optional path to keywords.db for DB-enriched title scoring.
                          If None, auto-resolves to tools/discovery/keywords.db when present.
        """
        self.project_name = project_name
        # Auto-resolve db_path to the standard keywords.db location if not provided
        if db_path is None:
            default_db = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "tools", "discovery", "keywords.db",
            )
            if os.path.exists(default_db):
                db_path = default_db
        self._db_path = db_path

    def generate_metadata_draft(
        self,
        sections: List[Section],
        entities: List[Entity],
        timings: List[SectionTiming]
    ) -> str:
        """
        Generate complete METADATA-DRAFT.md matching existing format.

        Args:
            sections: List of Section objects from ScriptParser
            entities: List of Entity objects from EntityExtractor
            timings: List of SectionTiming objects from EditGuideGenerator

        Returns:
            Complete markdown string in YOUTUBE-METADATA.md format
        """
        # Generate components
        title_candidates = self._generate_title_variants(sections, entities)
        title_section = format_title_candidates(title_candidates)
        description = self._generate_description(sections, entities)
        chapters = self._generate_chapters(timings)
        tags = self._generate_tags(entities, sections)

        # Build complete metadata document
        md = [
            f"# YouTube Metadata: {self.project_name}",
            "",
            title_section,
            "",
            "---",
            "",
            "## Description",
            "",
            "```",
            description,
            "```",
            "",
            "---",
            "",
            "## Chapters",
            "",
            "```",
            chapters,
            "```",
            "",
            "---",
            "",
            "## Tags",
            "",
            "```",
            tags,
            "```",
            "",
            "---",
            "",
            "## Thumbnail Concepts",
            "",
            "[PLACEHOLDER: To be added manually based on video content]",
            "",
            "---",
            "",
            "## VidIQ Research Notes",
            "",
            "[PLACEHOLDER: Add VidIQ keyword research here]",
        ]

        return '\n'.join(md)

    def _generate_title_variants(
        self,
        sections: List[Section],
        entities: List[Entity]
    ) -> List[dict]:
        """
        Generate ranked scored title candidates from the full script.

        Delegates to generate_title_candidates() from title_generator.py,
        which extracts material from the full script (not just the opening hook)
        and auto-scores every candidate via title_scorer.score_title().

        Args:
            sections: Script sections
            entities: Extracted entities (unused — title_generator re-extracts
                      from sections for position-weighted scoring)

        Returns:
            List of scored candidate dicts sorted by score descending.
            Each dict has: title, score, grade, pattern, penalties, hard_rejects, ...
        """
        if not sections:
            # Fallback: return a single minimal candidate for empty input
            return [{
                "title": "Untitled Video",
                "score": 0,
                "grade": "F",
                "pattern": "unknown",
                "penalties": [],
                "hard_rejects": [],
            }]

        return generate_title_candidates(
            sections=sections,
            topic_type=None,
            db_path=self._db_path,
        )

    def _extract_hook(self, text: str) -> str:
        """Extract first 2-3 sentences from opening text."""
        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Take first 2-3 sentences
        hook_sentences = sentences[:3] if len(sentences) >= 3 else sentences
        hook = ' '.join(hook_sentences)

        # Clean up
        hook = hook.replace('\n', ' ')
        hook = re.sub(r'\s+', ' ', hook)

        # Strip markers
        for pattern in [r'\[.*?\]', r'\*\*\[.*?\]\*\*']:
            hook = re.sub(pattern, '', hook)

        return hook.strip()

    def _generate_mechanism_title(
        self,
        hook: str,
        top_places: List[Entity],
        entities: List[Entity]
    ) -> TitleVariant:
        """Generate mechanism-focused title (Variant A)."""
        # Try to extract main topic from places
        if top_places:
            place = top_places[0].text
            # Try to find problem/paradox in hook
            if 'but' in hook.lower() or 'yet' in hook.lower() or 'however' in hook.lower():
                # Extract contradiction
                parts = re.split(r'\bbut\b|\byet\b|\bhowever\b', hook, maxsplit=1, flags=re.IGNORECASE)
                if len(parts) == 2:
                    problem = parts[1].strip()[:40]
                    title = f"{place}: {problem}"
                else:
                    title = f"Why {place}'s Status Remains Disputed"
            else:
                title = f"How {place} Became a Territorial Dispute"
        else:
            # Fallback to generic mechanism
            title = "The Historical Dispute That Created This Crisis"

        # Apply tone filter and truncate
        title = self._apply_tone_filter(title)
        title = self._truncate_title(title)

        return TitleVariant('A', title, 'Mechanism-focused', len(title))

    def _generate_document_title(
        self,
        hook: str,
        top_documents: List[Entity],
        entities: List[Entity]
    ) -> TitleVariant:
        """Generate document-focused title (Variant B)."""
        if top_documents:
            doc = top_documents[0].text

            # Extract date if present
            dates = [e for e in entities if e.entity_type == 'date']
            if dates:
                date_text = dates[0].text
                title = f"The {date_text} {doc} That Changed Everything"
            else:
                title = f"The {doc}: What It Actually Says"
        else:
            # Fallback to document angle without specific doc
            title = "The Document That Shaped This Dispute"

        # Apply tone filter and truncate
        title = self._apply_tone_filter(title)
        title = self._truncate_title(title)

        return TitleVariant('B', title, 'Document/evidence focus', len(title))

    def _generate_paradox_title(
        self,
        hook: str,
        top_places: List[Entity],
        entities: List[Entity]
    ) -> TitleVariant:
        """Generate paradox/curiosity-focused title (Variant C)."""
        if top_places:
            place = top_places[0].text

            # Look for paradoxical elements in hook
            if 'gave back' in hook.lower() or 'returned' in hook.lower():
                title = f"Why They Gave Back {place} (But Kept Control)"
            elif 'unclaimed' in hook.lower() or 'nobody wants' in hook.lower():
                title = f"The Land Nobody Wants to Claim: {place}"
            elif 'deport' in hook.lower() or 'removed' in hook.lower():
                title = f"They Deported Everyone From {place}. Here's Why."
            else:
                title = f"{place}'s Disputed Status, Explained"
        else:
            # Fallback to generic paradox
            title = "The Territorial Paradox That Still Hasn't Been Resolved"

        # Apply tone filter and truncate
        title = self._apply_tone_filter(title)
        title = self._truncate_title(title)

        return TitleVariant('C', title, 'Paradox/status-focused', len(title))

    def _apply_tone_filter(self, title: str) -> str:
        """
        Apply documentary tone filter to reject clickbait patterns.

        Removes/replaces:
        - Clickbait phrases
        - Excessive punctuation
        - All-caps emphasis (except acronyms)

        Args:
            title: Raw title text

        Returns:
            Filtered title text
        """
        # Check for clickbait patterns
        for pattern in CLICKBAIT_PATTERNS:
            if pattern.lower() in title.lower():
                # Replace with neutral version
                title = re.sub(re.escape(pattern), '', title, flags=re.IGNORECASE)

        # Remove excessive punctuation
        title = re.sub(r'[!?]{2,}', '', title)
        title = re.sub(r'\.{3,}', '', title)

        # Fix all-caps words (except acronyms)
        words = title.split()
        filtered_words = []
        for word in words:
            # Skip if it's an allowed acronym
            if word.upper() in ALLOWED_ACRONYMS:
                filtered_words.append(word.upper())
            # Convert all-caps to title case
            elif word.isupper() and len(word) > 2:
                filtered_words.append(word.capitalize())
            else:
                filtered_words.append(word)

        title = ' '.join(filtered_words)

        # Clean up spacing
        title = re.sub(r'\s+', ' ', title)
        title = title.strip()

        return title

    def _truncate_title(self, title: str) -> str:
        """Truncate title to MAX_TITLE_LENGTH, preserving word boundaries."""
        if len(title) <= MAX_TITLE_LENGTH:
            return title

        # Truncate at word boundary
        truncated = title[:MAX_TITLE_LENGTH]
        last_space = truncated.rfind(' ')

        if last_space > 0:
            truncated = truncated[:last_space]

        return truncated.rstrip('.,;:')

    def _extract_citations(self, sections: List[Section]) -> List[str]:
        """
        Extract academic citation strings from script sections.

        Finds two patterns:
          1. "According to X in Y, page N" / "per X in Y, page N"
          2. "X's *Y*, p. N"

        Returns:
            Deduplicated list of formatted strings: "Author, *Title*, p. N"
        """
        full_text = " ".join(s.content for s in sections)
        citations: List[str] = []
        seen: Set[str] = set()

        for pattern in [_CITATION_PATTERN_ACCORDING_TO, _CITATION_PATTERN_POSSESSIVE]:
            for m in pattern.finditer(full_text):
                author = m.group(1).strip()
                # Strip possessive 's suffix if present (e.g., "Harris's" → "Harris")
                if author.endswith("'s"):
                    author = author[:-2]
                book = m.group(2).strip()
                page = m.group(3).strip()
                citation = f"{author}, *{book}*, p. {page}"
                key = citation.lower()
                if key not in seen:
                    seen.add(key)
                    citations.append(citation)

        return citations

    def _generate_description(
        self,
        sections: List[Section],
        entities: List[Entity],
        timings: List[SectionTiming] = None,
        material: Optional[dict] = None,
    ) -> str:
        """
        Generate YouTube description with SEO first line, auto-extracted citations,
        chapters, and warning block for missing elements.

        The description ALWAYS outputs content — missing elements produce ⚠️ warnings
        appended at the end, but never hard-block the output.

        Args:
            sections:  Script sections
            entities:  Extracted entities
            timings:   SectionTiming list for chapter generation (None = no chapters)
            material:  Optional pre-computed TitleMaterialExtractor dict

        Returns:
            Complete description string
        """
        if timings is None:
            timings = []

        lines: List[str] = []
        warnings: List[str] = []

        # ------------------------------------------------------------------
        # 1. SEO first line — keyword-rich, NOT "In this video"
        # ------------------------------------------------------------------
        # Detect topic type for phrasing
        try:
            from tools.youtube_analytics.performance import classify_topic_type
            # Build a rough "title" from primary entity + first section heading
            first_section_text = sections[0].content[:200] if sections else ""
            raw_topic = classify_topic_type(description=first_section_text)
        except Exception:
            raw_topic = "general"

        topic_verb_map = {
            "territorial": "territorial history of",
            "ideological": "myth-busting analysis of",
            "political_fact_check": "fact-check of",
            "general": "primary-source analysis of",
        }
        topic_verb = topic_verb_map.get(raw_topic, "primary-source analysis of")

        # Get primary entity: try material, then entities, then first section heading
        primary_entity = None
        if material is not None:
            for ent, _w in material.get("entities", []):
                if hasattr(ent, "entity_type") and ent.entity_type != "date" and len(ent.text) >= 3:
                    primary_entity = ent.text
                    break
        if primary_entity is None:
            for ent in entities:
                if hasattr(ent, "entity_type") and ent.entity_type != "date" and len(ent.text) >= 3:
                    primary_entity = ent.text
                    break
        if primary_entity is None and sections:
            # Fall back: extract first capitalized word/phrase from first section content
            caps_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b', sections[0].content)
            if caps_match:
                primary_entity = caps_match.group(1)

        if primary_entity:
            seo_line = f"{primary_entity} — a {topic_verb} {primary_entity} using primary sources and academic research."
        else:
            seo_line = f"A {topic_verb} this topic using primary sources and academic research."
            warnings.append("SEO first line keyword unclear — verify primary keyword")

        lines.append(seo_line)
        lines.append("")

        # ------------------------------------------------------------------
        # 2. Video summary (2-3 sentences from section headings)
        # ------------------------------------------------------------------
        if sections:
            heading_names = [s.heading for s in sections[:4] if s.heading and s.heading.lower() not in ("intro", "introduction", "conclusion", "outro", "body")]
            if heading_names:
                summary = "This video covers: " + ", ".join(heading_names[:3]) + "."
                lines.append(summary)
                lines.append("")

        lines.append("—")
        lines.append("")

        # ------------------------------------------------------------------
        # 3. Key documents section
        # ------------------------------------------------------------------
        documents = [e for e in entities if e.entity_type == 'document']
        if documents:
            lines.append("📜 KEY DOCUMENTS REFERENCED:")
            for doc in sorted(documents, key=lambda x: x.mentions, reverse=True)[:5]:
                lines.append(f"• {doc.text}")
            lines.append("")

        # ------------------------------------------------------------------
        # 4. Auto-extracted citations
        # ------------------------------------------------------------------
        citations = self._extract_citations(sections)
        if citations:
            lines.append("📚 SOURCES:")
            for cite in citations:
                lines.append(f"• {cite}")
            lines.append("")
        else:
            lines.append("📚 SOURCES:")
            lines.append("[Add academic sources from script]")
            lines.append("")
            warnings.append("No source citations found in script — add academic source references")

        lines.append("—")
        lines.append("")

        # ------------------------------------------------------------------
        # 5. Chapters (if timings provided)
        # ------------------------------------------------------------------
        if timings:
            chapters = self._generate_chapters(timings)
            if chapters:
                lines.append("⏱️ CHAPTERS:")
                lines.append(chapters)
                lines.append("")
        else:
            warnings.append("No timestamps — run EditGuideGenerator to generate SectionTiming data")

        # ------------------------------------------------------------------
        # 6. Related videos placeholder
        # ------------------------------------------------------------------
        lines.append("🌍 MORE FROM HISTORY VS HYPE:")
        lines.append("[Related video links]")
        lines.append("")

        lines.append("—")
        lines.append("")

        # ------------------------------------------------------------------
        # 7. Hashtags from top entities
        # ------------------------------------------------------------------
        hashtags = self._generate_hashtags(entities)
        lines.append(hashtags)

        # ------------------------------------------------------------------
        # 8. Warning block (appended, never hard-blocks)
        # ------------------------------------------------------------------
        if warnings:
            lines.append("")
            lines.append("⚠️ MISSING ELEMENTS:")
            for w in warnings:
                lines.append(f"• {w}")

        return '\n'.join(lines)

    def _generate_thumbnail_concepts(
        self,
        material: dict,
        entities: List[Entity],
        topic_type: Optional[str] = None,
    ) -> str:
        """
        Generate 3 script-grounded thumbnail concepts with thumbnail_checker badges.

        Args:
            material:    Output of TitleMaterialExtractor.extract_from_sections()
            entities:    Entity list (for fallback lookups)
            topic_type:  Optional override. When None, auto-detects from material.

        Returns:
            Formatted markdown string with 3 **Concept A/B/C** blocks, each with
            a ✅/⚠️ badge (score/100) from thumbnail_checker, and Issues line if any.
        """
        from tools.preflight.thumbnail_checker import check_thumbnail

        # Auto-detect topic type from material entities if not supplied
        if topic_type is None:
            try:
                from tools.youtube_analytics.performance import classify_topic_type
                # Build a small text from top entities to guess topic
                entity_names = " ".join(
                    ent.text for ent, _w in material.get("entities", [])[:5]
                    if hasattr(ent, "text")
                )
                topic_type = classify_topic_type(description=entity_names) or "general"
            except Exception:
                topic_type = "general"

        # Normalize to known keys
        patterns_for_topic = THUMBNAIL_PATTERNS.get(topic_type, THUMBNAIL_PATTERNS["general"])

        concept_labels = ["A", "B", "C"]
        concept_names = {
            'split_map_conflict': 'Split-Map Conflict',
            'document_on_map': 'Document on Map',
            'geo_plus_evidence': 'Geo + Evidence',
            'myth_vs_reality': 'Myth vs Reality',
            'document_reveal': 'Document Reveal',
            'timeline_contrast': 'Timeline Contrast',
            'quote_vs_reality': 'Quote vs Reality',
            'map_timeline': 'Map Timeline',
        }

        output_lines: List[str] = []

        for label, pattern in zip(concept_labels, patterns_for_topic):
            concept_text = self._fill_template(pattern, material, entities)
            result = check_thumbnail(concept_text)
            badge = "✅" if result['verdict'] == 'PASS' else "⚠️"
            score = result['score']
            display_name = concept_names.get(pattern, pattern.replace('_', ' ').title())

            output_lines.append(
                f"**Concept {label}** {badge} ({score}/100) — {display_name}"
            )
            output_lines.append(concept_text)
            if result.get('issues'):
                output_lines.append("Issues: " + ", ".join(result['issues'][:3]))
            output_lines.append("")

        return "\n".join(output_lines)

    def _fill_template(
        self,
        pattern: str,
        material: dict,
        entities: List[Entity],
    ) -> str:
        """
        Fill a thumbnail pattern template with script-specific extracted values.

        Falls back to neutral defaults when material is sparse.
        Always includes map/geographic signal and "No face, no text overlay."
        so thumbnail_checker can score correctly.
        """
        # Extract primary values from material
        primary_place = "the disputed region"
        primary_doc = None
        primary_number = None

        for ent, _w in material.get("entities", []):
            if hasattr(ent, "entity_type") and ent.entity_type == "place" and len(ent.text) >= 3:
                primary_place = ent.text
                break

        # Fallback: try non-date entity for place
        if primary_place == "the disputed region":
            for ent, _w in material.get("entities", []):
                if hasattr(ent, "entity_type") and ent.entity_type != "date" and len(ent.text) >= 3:
                    primary_place = ent.text
                    break

        docs = material.get("documents", [])
        if docs:
            doc_ent, _w = docs[0]
            primary_doc = doc_ent.text if hasattr(doc_ent, "text") else str(doc_ent)

        numbers = material.get("numbers", [])
        if numbers:
            primary_number = numbers[0][0]

        doc_str = primary_doc or "primary source document"

        if pattern == 'split_map_conflict':
            base = f"Map of {primary_place} split down the middle. "
            if primary_number:
                base += f"Dividing line at {primary_number}. "
            base += "Warm (gold/red) vs cool (blue) color halves. No face, no text overlay."
            return base

        elif pattern == 'document_on_map':
            return (
                f"{doc_str} overlaid on faded map of {primary_place}. "
                "Document edges visible, handwritten text legible. "
                "Rich color on document, faded blue map background. "
                "No face, no text overlay."
            )

        elif pattern == 'geo_plus_evidence':
            return (
                f"Map of {primary_place} split between two territories. "
                f"Document fragment ({doc_str}) as corner overlay. "
                "Warm amber and cool blue opposing halves. "
                "No face, no text overlay."
            )

        elif pattern == 'myth_vs_reality':
            return (
                f"Split map: left half faded and grey (myth), right half bright and detailed (reality). "
                f"Geographic overlay of {primary_place}. "
                "Bold contrast between washed-out and vivid halves. "
                "No face, no text overlay."
            )

        elif pattern == 'document_reveal':
            return (
                f"{doc_str} partially unfolded on a map background of {primary_place}. "
                "Document reveals highlighted text. Geographic split visible behind. "
                "Red and gold color contrast. No face, no text overlay."
            )

        elif pattern == 'timeline_contrast':
            return (
                f"Two-panel split on map of {primary_place}: "
                "left panel faded historical (myth era), right panel sharp modern (reality). "
                "Blue-to-amber color gradient across the split. "
                "No face, no text overlay."
            )

        elif pattern == 'quote_vs_reality':
            return (
                f"Map of {primary_place} as background. "
                f"Document ({doc_str}) in foreground with key passage visible. "
                "Dark dramatic background, document brightly lit. "
                "No face, no text overlay."
            )

        elif pattern == 'map_timeline':
            return (
                f"Map of {primary_place} with timeline overlay. "
                "Geographic boundaries clearly visible. "
                "Red dividing line shows territorial change. "
                "No face, no text overlay."
            )

        else:
            # Generic fallback
            return (
                f"Map of {primary_place} showing geographic context. "
                "High-contrast colors, clear boundary lines. "
                "No face, no text overlay."
            )

    def _generate_hashtags(self, entities: List[Entity]) -> str:
        """Generate hashtag string from top entities."""
        # Get top entities across all types
        top_entities = sorted(entities, key=lambda x: x.mentions, reverse=True)[:8]

        hashtags = []
        for entity in top_entities:
            # Convert entity text to hashtag format
            tag = entity.text.replace(' ', '')
            tag = re.sub(r'[^\w]', '', tag)
            if tag and len(tag) > 2:
                hashtags.append(f"#{tag}")

        return ' '.join(hashtags) if hashtags else "#History #Geopolitics"

    def _generate_chapters(self, timings: List[SectionTiming]) -> str:
        """
        Generate chapter timestamps from section timings.

        Args:
            timings: List of SectionTiming objects

        Returns:
            Chapters text (MM:SS format)
        """
        if not timings:
            return "0:00 Introduction"

        lines = []
        for timing in timings:
            timestamp = format_time(timing.start_time)
            lines.append(f"{timestamp} {timing.section.heading}")

        return '\n'.join(lines)

    def _generate_tags(
        self,
        entities: List[Entity],
        sections: List[Section]
    ) -> str:
        """
        Generate comma-separated tag string.

        Primary: Entity names (places, people, documents) - deduplicated
        Secondary: Broader topic terms from section headings

        Args:
            entities: Extracted entities
            sections: Script sections

        Returns:
            Comma-separated tag string (15-20 tags)
        """
        tags: List[str] = []
        seen: Set[str] = set()

        # Primary: Entity names (prioritize by mentions, filter by type and length)
        sorted_entities = sorted(entities, key=lambda x: x.mentions, reverse=True)

        for entity in sorted_entities:
            # Use entity text as tag
            tag = entity.text.strip()
            tag_normalized = tag.lower()

            # Skip if:
            # - Too short (less than 3 chars)
            # - Too long (more than 50 chars - likely a sentence fragment)
            # - Contains parentheses or brackets (likely metadata)
            # - Already seen
            if (len(tag) < 3 or len(tag) > 50 or
                '(' in tag or ')' in tag or '[' in tag or ']' in tag or
                tag_normalized in seen):
                continue

            # Skip date entities that are just years
            if entity.entity_type == 'date' and tag.isdigit():
                if len(tag) != 4:  # Skip unless it's a year
                    continue

            tags.append(tag)
            seen.add(tag_normalized)

            if len(tags) >= 15:
                break

        # Secondary: Broader terms from section headings (only if needed)
        if len(tags) < 10:
            for section in sections[:5]:
                # Extract key terms from headings
                heading_words = section.heading.split()
                for word in heading_words:
                    # Clean up word
                    word = word.strip('.,;:()[]')

                    # Skip common words and short words
                    if (word.lower() in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'act', 'section'] or
                        len(word) < 4):
                        continue

                    word_normalized = word.lower()
                    if word_normalized not in seen:
                        tags.append(word)
                        seen.add(word_normalized)

                    if len(tags) >= 20:
                        break

                if len(tags) >= 20:
                    break

        # Ensure we have at least some tags
        if len(tags) < 5:
            fallback_tags = ['History', 'Geopolitics', 'Documentary', 'International Relations']
            for fallback in fallback_tags:
                if fallback.lower() not in seen:
                    tags.append(fallback)
                    seen.add(fallback.lower())
                if len(tags) >= 10:
                    break

        return ', '.join(tags[:20])


if __name__ == "__main__":
    # Simple test
    print("MetadataGenerator module loaded successfully")

    # Test tone filter
    gen = MetadataGenerator("test")

    test_titles = [
        "The SHOCKING Truth About Chagos",
        "You Won't BELIEVE What Britain Did",
        "The ICJ Ruling That Changed Everything"
    ]

    for title in test_titles:
        filtered = gen._apply_tone_filter(title)
        print(f"Original: {title}")
        print(f"Filtered: {filtered}")
        print()
