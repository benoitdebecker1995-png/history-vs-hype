"""
Script Parser Module

Parses markdown scripts into structured sections for downstream production tools.
Extracts headings, content, word counts, and section types.

Usage:
    from tools.production import ScriptParser, Section

    parser = ScriptParser()
    sections = parser.parse_file('video-projects/_IN_PRODUCTION/1-somaliland-2025/SCRIPT.md')

    for section in sections:
        print(f'{section.heading}: {section.word_count} words')
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional


@dataclass
class Section:
    """A parsed section from a script file."""
    heading: str           # H2 heading text (or "Untitled" for headerless scripts)
    content: str           # Full text content of section
    word_count: int        # Word count for timing estimation (spoken words only)
    start_line: int        # Line number where section starts
    section_type: str      # 'intro', 'body', 'conclusion' (inferred by position)


class ScriptParser:
    """
    Parses markdown script files into structured sections.

    Handles:
    - YAML frontmatter stripping
    - H2 (##) header detection
    - B-roll marker exclusion from word counts
    - Section type inference (intro/body/conclusion)
    """

    # Regex patterns
    H2_PATTERN = re.compile(r'^##\s+(.+)$', re.MULTILINE)
    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
    COMMENT_PATTERN = re.compile(r'<!--.*?-->', re.DOTALL)
    CODE_BLOCK_PATTERN = re.compile(r'```.*?```', re.DOTALL)

    # B-roll and annotation markers to exclude from word count
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
    ]

    def parse_file(self, path: Path) -> List[Section]:
        """
        Parse a script file into sections.

        Args:
            path: Path to the markdown script file

        Returns:
            List of Section objects
        """
        path = Path(path)

        # Read file with encoding fallback for Windows
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = path.read_text(encoding='cp1252')

        return self.parse_text(text)

    def parse_text(self, text: str) -> List[Section]:
        """
        Parse script text into sections.

        Args:
            text: Raw markdown script text

        Returns:
            List of Section objects
        """
        # Strip frontmatter if present
        _, clean_text = self._extract_frontmatter(text)

        # Strip comments and code blocks for parsing
        parsing_text = self.COMMENT_PATTERN.sub('', clean_text)
        parsing_text = self.CODE_BLOCK_PATTERN.sub('', parsing_text)

        # Split into sections
        sections = self._split_sections(parsing_text)

        # Infer section types
        sections = self._infer_section_types(sections)

        return sections

    def _extract_frontmatter(self, text: str) -> Tuple[dict, str]:
        """
        Extract and strip YAML frontmatter from text.

        Args:
            text: Raw script text

        Returns:
            Tuple of (frontmatter_dict, remaining_text)
            frontmatter_dict is empty if no frontmatter found
        """
        match = self.FRONTMATTER_PATTERN.match(text)
        if match:
            frontmatter_text = match.group(0)
            remaining = text[match.end():]
            # Basic frontmatter parsing (key: value)
            frontmatter = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line and not line.strip().startswith('---'):
                    key, _, value = line.partition(':')
                    frontmatter[key.strip()] = value.strip()
            return frontmatter, remaining
        return {}, text

    def _split_sections(self, text: str) -> List[Section]:
        """
        Split text into sections based on H2 headers.

        Args:
            text: Clean script text (no frontmatter)

        Returns:
            List of Section objects
        """
        lines = text.split('\n')
        sections = []

        # Find all H2 header positions
        header_positions = []
        for i, line in enumerate(lines):
            match = self.H2_PATTERN.match(line)
            if match:
                header_positions.append((i, match.group(1).strip()))

        # If no headers, treat entire text as single section
        if not header_positions:
            content = text.strip()
            word_count = self._count_spoken_words(content)
            return [Section(
                heading="Untitled",
                content=content,
                word_count=word_count,
                start_line=1,
                section_type='body'
            )]

        # Build sections from headers
        for idx, (line_num, heading) in enumerate(header_positions):
            # Determine end of this section
            if idx + 1 < len(header_positions):
                end_line = header_positions[idx + 1][0]
            else:
                end_line = len(lines)

            # Extract content (excluding the header line itself)
            section_lines = lines[line_num + 1:end_line]
            content = '\n'.join(section_lines).strip()

            # Count spoken words
            word_count = self._count_spoken_words(content)

            sections.append(Section(
                heading=heading,
                content=content,
                word_count=word_count,
                start_line=line_num + 1,  # 1-indexed
                section_type='body'  # Will be updated by _infer_section_types
            ))

        return sections

    def _count_spoken_words(self, content: str) -> int:
        """
        Count spoken words in content, excluding B-roll markers and formatting.

        Args:
            content: Section content text

        Returns:
            Word count of spoken content only
        """
        # Remove B-roll and annotation markers
        clean = content
        for pattern in self.MARKER_PATTERNS:
            clean = pattern.sub('', clean)

        # Remove markdown formatting
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)  # **bold**
        clean = re.sub(r'\*([^*]+)\*', r'\1', clean)      # *italic*
        clean = re.sub(r'!\[.*?\]\(.*?\)', '', clean)     # Images
        clean = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', clean)  # Links
        clean = re.sub(r'^#+\s+', '', clean, flags=re.MULTILINE)  # Headers
        clean = re.sub(r'^\|.*\|$', '', clean, flags=re.MULTILINE)  # Tables
        clean = re.sub(r'^---+$', '', clean, flags=re.MULTILINE)  # Horizontal rules
        clean = re.sub(r'^\s*[-*]\s+', '', clean, flags=re.MULTILINE)  # List markers

        # Remove any remaining bracketed content (likely markers we missed)
        clean = re.sub(r'\[[^\]]+\]', '', clean)

        # Count words
        words = clean.split()
        return len(words)

    def _infer_section_types(self, sections: List[Section]) -> List[Section]:
        """
        Infer section types based on position and heading keywords.

        Args:
            sections: List of sections with type='body'

        Returns:
            Sections with updated types
        """
        if not sections:
            return sections

        # Keywords that indicate section type
        intro_keywords = ['opening', 'hook', 'intro', 'introduction']
        conclusion_keywords = ['conclusion', 'end', 'closing', 'outro', 'end card']

        for i, section in enumerate(sections):
            heading_lower = section.heading.lower()

            # Check for intro keywords
            if any(kw in heading_lower for kw in intro_keywords):
                section.section_type = 'intro'
            # Check for conclusion keywords
            elif any(kw in heading_lower for kw in conclusion_keywords):
                section.section_type = 'conclusion'
            # Position-based fallback
            elif i == 0:
                section.section_type = 'intro'
            elif i == len(sections) - 1:
                section.section_type = 'conclusion'
            else:
                section.section_type = 'body'

        return sections


if __name__ == "__main__":
    import sys

    # Check for flags
    broll_mode = '--broll' in sys.argv
    editguide_mode = '--edit-guide' in sys.argv
    if broll_mode:
        sys.argv.remove('--broll')
    if editguide_mode:
        sys.argv.remove('--edit-guide')

    if len(sys.argv) < 2:
        print("Usage: python parser.py <script.md> [--broll] [--edit-guide]")
        print("  --broll: Generate B-roll checklist")
        print("  --edit-guide: Generate EDITING-GUIDE.md with timing")
        sys.exit(1)

    from pathlib import Path
    import os

    # Add project root to path for imports to work
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    from tools.production import EntityExtractor, BRollGenerator

    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"File not found: {script_path}")
        sys.exit(1)

    parser = ScriptParser()
    extractor = EntityExtractor()

    sections = parser.parse_file(script_path)
    entities = extractor.extract_from_sections(sections)

    # B-roll mode: generate checklist and exit
    if broll_mode:
        # Extract project name from path (e.g., "14-chagos-islands-2025")
        project_name = script_path.parent.name
        generator = BRollGenerator(project_name=project_name)
        checklist = generator.generate_checklist(entities, sections)
        print(checklist)
        sys.exit(0)

    # Edit guide mode: generate edit guide and exit
    if editguide_mode:
        from tools.production import EditGuideGenerator
        # Set stdout to UTF-8 encoding for unicode characters
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        project_name = script_path.parent.name
        broll_gen = BRollGenerator(project_name=project_name)
        shots = broll_gen.generate(entities, sections)
        editguide_gen = EditGuideGenerator(project_name=project_name)
        guide = editguide_gen.generate_edit_guide(sections, shots, entities)
        print(guide)
        sys.exit(0)

    # Default mode: entity summary
    print(f"\n=== SECTIONS ({len(sections)}) ===")
    total_words = 0
    for i, section in enumerate(sections, 1):
        print(f"{i}. {section.heading} ({section.section_type})")
        print(f"   Words: {section.word_count} | Line: {section.start_line}")
        total_words += section.word_count

    print(f"\nTotal words: {total_words}")
    print(f"Est. runtime: {total_words / 150:.1f} min @ 150 WPM")

    print(f"\n=== ENTITIES ({len(entities)}) ===")
    for etype in ['document', 'place', 'person', 'date', 'organization']:
        typed = [e for e in entities if e.entity_type == etype]
        if typed:
            print(f"\n{etype.upper()}S ({len(typed)}):")
            for e in sorted(typed, key=lambda x: -x.mentions)[:5]:
                print(f"  - {e.text} ({e.mentions}x)")
