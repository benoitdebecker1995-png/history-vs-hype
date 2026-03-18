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
from .title_generator import generate_title_candidates, format_title_candidates


# Clickbait patterns to reject (from VIDIQ-CHANNEL-DNA-FILTER.md)
CLICKBAIT_PATTERNS = [
    'SHOCKING', 'You won\'t believe', 'You won\'t BELIEVE',
    'This will BLOW your mind', 'What THEY don\'t want you to know',
    'INSANE', 'MIND-BLOWING', 'EXPOSED', 'The TRUTH About',
    'DESTROYED by Facts', 'What IT Really Means', 'How THIS Changed',
    'Top 10', '5 Reasons Why', '3 Things You Didn\'t Know',
    'LIED About', 'The Truth They HID'
]

# Allowed acronyms (can be all-caps without being clickbait)
ALLOWED_ACRONYMS = [
    'ICJ', 'UN', 'CIA', 'AU', 'EU', 'NATO', 'UNESCO', 'WHO',
    'IMF', 'USSR', 'UK', 'US', 'USA', 'WTO', 'ICC', 'ECHR',
    'OPEC', 'BRICS', 'ASEAN', 'OAS', 'FCDO', 'BIOT', 'PDF',
    'DIY', 'GPS', 'GDP', 'CEO', 'FBI', 'NSA', 'NASA'
]

# Title constraints
MAX_TITLE_LENGTH = 70
TARGET_TITLE_LENGTH = (60, 70)
TARGET_TAG_COUNT = (15, 20)


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

    def _generate_description(
        self,
        sections: List[Section],
        entities: List[Entity]
    ) -> str:
        """
        Generate YouTube description.

        Includes:
        - Opening hook (rephrased for reading)
        - KEY DOCUMENTS section
        - SOURCES section
        - Hashtags from top entities

        Args:
            sections: Script sections
            entities: Extracted entities

        Returns:
            Description text
        """
        lines = []

        # Opening hook (first 2-3 sentences, rephrased)
        if sections:
            hook = self._extract_hook(sections[0].content)
            # Rephrase for reading (remove verbal markers)
            hook = hook.replace('Here\'s', 'This video shows')
            hook = hook.replace('We\'ll', 'The video will')
            hook = hook.replace('Let me', 'This video will')
            lines.append(hook)
            lines.append("")

        lines.append("—")
        lines.append("")

        # KEY DOCUMENTS section
        documents = [e for e in entities if e.entity_type == 'document']
        if documents:
            lines.append("📜 KEY DOCUMENTS REFERENCED:")
            for doc in sorted(documents, key=lambda x: x.mentions, reverse=True)[:5]:
                lines.append(f"• {doc.text}")
            lines.append("")

        # SOURCES section (placeholder - would need source extraction)
        lines.append("📚 SOURCES:")
        lines.append("[PLACEHOLDER: Add academic sources from script]")
        lines.append("")

        lines.append("—")
        lines.append("")

        # Related videos placeholder
        lines.append("🌍 MORE ON [TOPIC TYPE]:")
        lines.append("[PLACEHOLDER: Related video links]")
        lines.append("")

        lines.append("—")
        lines.append("")

        # Hashtags from top entities
        hashtags = self._generate_hashtags(entities)
        lines.append(hashtags)

        return '\n'.join(lines)

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
