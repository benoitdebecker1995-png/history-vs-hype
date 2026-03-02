"""
Translation Output Formatter (TRAN-05)

Formats translated sections as paired original/translation markdown suitable for
split-screen video display. Supports footnote annotations for legal terms.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class Formatter:
    """
    Format translated sections for split-screen display and video production.

    Output formats:
    - markdown: Clause-by-clause paired original/translation with footnotes
    - json: Machine-readable structured output
    """

    def __init__(self):
        """Initialize formatter."""
        pass

    def format_paired(self, sections: List[Dict], output_format: str = 'markdown') -> str:
        """
        Format translated sections as paired original/translation.

        Args:
            sections: List of section dicts with keys:
                - 'id': Section identifier (e.g., 'article-1')
                - 'heading': Section heading (e.g., 'Article 1')
                - 'original': Original language text
                - 'translation': English translation
                - 'footnotes': Optional list of footnote strings
            output_format: 'markdown' or 'json'

        Returns:
            Formatted string (markdown or JSON)
            Or {'error': msg} on failure

        Markdown format:
            ## Article 1: [heading]

            ### Original (Language)
            > [original text, blockquoted]

            ### Translation
            [English translation text]

            ---
            **Notes:**
            1. [footnote]
            2. [footnote]
        """
        if not sections:
            return {'error': 'No sections provided'}

        if output_format == 'json':
            return json.dumps({'sections': sections}, indent=2, ensure_ascii=False)

        # Markdown format
        output_lines = []

        for section in sections:
            if 'error' in section:
                output_lines.append(f"ERROR in {section.get('id', 'unknown')}: {section['error']}\n")
                continue

            # Section heading
            heading = section.get('heading', section.get('id', 'Unknown'))
            output_lines.append(f"## {heading}\n")

            # Original text (blockquoted)
            original = section.get('original', '')
            if original:
                output_lines.append("### Original\n")
                # Blockquote each line
                original_lines = original.split('\n')
                for line in original_lines:
                    output_lines.append(f"> {line}")
                output_lines.append("")

            # Translation
            translation = section.get('translation', '')
            if translation:
                output_lines.append("### Translation\n")
                output_lines.append(translation)
                output_lines.append("")

            # Footnotes (if any)
            footnotes = section.get('footnotes') or section.get('notes')
            if footnotes:
                output_lines.append("---")
                output_lines.append("**Notes:**\n")
                for i, note in enumerate(footnotes, 1):
                    output_lines.append(f"{i}. {note}")
                output_lines.append("")

            # Add spacing between sections
            output_lines.append("")

        return '\n'.join(output_lines)

    def format_summary(self, sections: List[Dict], metadata: Dict) -> str:
        """
        Generate summary header for translation document.

        Args:
            sections: List of translated sections
            metadata: Dict with keys:
                - 'document_name': Document name
                - 'source_language': Source language
                - 'model': Translation model used
                - 'translation_date': Optional date (defaults to now)

        Returns:
            Markdown summary header
        """
        if not metadata:
            return {'error': 'Metadata required for summary'}

        lines = []

        # Title
        doc_name = metadata.get('document_name', 'Untitled Document')
        lines.append(f"# Translation: {doc_name}\n")

        # Metadata table
        lines.append("## Document Information\n")
        lines.append(f"**Source Language:** {metadata.get('source_language', 'Unknown')}")
        lines.append(f"**Section Count:** {len(sections)}")

        translation_date = metadata.get('translation_date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))
        lines.append(f"**Translation Date:** {translation_date}")

        model = metadata.get('model', 'Unknown')
        lines.append(f"**Translation Model:** {model}")

        if metadata.get('version'):
            lines.append(f"**Tool Version:** {metadata['version']}")

        lines.append("")

        # Section list
        lines.append("## Sections Translated\n")
        for section in sections:
            section_id = section.get('id', 'unknown')
            heading = section.get('heading', section_id)
            lines.append(f"- {heading}")

        lines.append("")
        lines.append("---\n")

        return '\n'.join(lines)

    def format_json(self, sections: List[Dict], metadata: Dict) -> str:
        """
        Format translation as JSON for machine consumption.

        Args:
            sections: List of translated sections
            metadata: Translation metadata

        Returns:
            JSON string with metadata and sections
        """
        if not sections:
            return {'error': 'No sections provided'}

        output = {
            'metadata': metadata,
            'sections': sections,
            'section_count': len(sections)
        }

        return json.dumps(output, indent=2, ensure_ascii=False)

    def format_split_screen(self, section: Dict, side: str = 'left') -> Dict[str, Any]:
        """
        Format single section for split-screen video editing.

        Args:
            section: Section dict with original and translation
            side: 'left' (original) or 'right' (translation) or 'both'

        Returns:
            Dict with formatted text for video overlay
            Keys: 'heading', 'text', 'side'
        """
        if not section:
            return {'error': 'Section required'}

        heading = section.get('heading', '')
        original = section.get('original', '')
        translation = section.get('translation', '')

        if side == 'left':
            return {
                'heading': heading,
                'text': original,
                'side': 'left',
                'language': 'original'
            }
        elif side == 'right':
            return {
                'heading': heading,
                'text': translation,
                'side': 'right',
                'language': 'english'
            }
        else:  # both
            return {
                'heading': heading,
                'original': original,
                'translation': translation,
                'side': 'both'
            }
