"""
Split-Screen Edit Guide Generator (PROD-01, PROD-02, PROD-03)

Generates editor-ready split-screen guides for document walkthrough videos.
Integrates Phase 40 translation output + Phase 39 archive lookup to produce
clause-by-clause timing estimates, transition markers, and asset sourcing.

Design:
- Per-clause timing breakdown (context, read, translate, explain, connect)
- Section-level totals with cumulative running times
- Hybrid transition markers (explicit switches + ratio guidance)
- Auto-sourced assets from archive lookup + manual placeholders
- Surprise markers (MAJOR/NOTABLE only) for editor emphasis

Usage:
    python tools/production/split_screen_guide.py --translation PATH --script PATH --output PATH
"""

import os
import sys
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


# Fixed words-per-minute rate for timing calculations
WPM = 150

# Pause times for visual processing (seconds)
READ_PAUSE = 2.5
TRANSLATE_PAUSE = 2.5


class SplitScreenGuide:
    """
    Generate split-screen edit guides for document walkthrough videos.

    Combines:
    - Translation output (clause structure, surprises)
    - Script (word counts per section)
    - Archive lookup results (document URLs)

    Produces:
    - Clause-by-clause timing breakdowns
    - Section-level totals and cumulative running times
    - Transition markers (explicit + ratio guidance)
    - Asset checklist (auto-sourced + manual creation needed)
    - Surprise emphasis flags for editor
    """

    def __init__(self):
        """Initialize guide generator."""
        pass

    def generate_guide(self, translation_file: str, script_file: Optional[str] = None,
                      output_path: Optional[str] = None, archive_results: Optional[Dict] = None,
                      project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate complete split-screen edit guide.

        Args:
            translation_file: Path to formatted translation output (TRAN-05 format)
            script_file: Optional path to script file (for precise word counts)
            output_path: Optional output path (defaults to translation file directory)
            archive_results: Optional archive lookup results dict
            project_name: Optional project name (extracted from path if not provided)

        Returns:
            {
                'guide_path': str,
                'total_duration': int,  # seconds
                'total_duration_str': str,  # "25 min 30 sec"
                'clause_count': int,
                'section_count': int,
                'assets_auto_sourced': int,
                'assets_needed': int,
                'surprise_count': {'major': int, 'notable': int}
            }

            Or {'error': msg} on failure
        """
        # Validate inputs
        if not os.path.exists(translation_file):
            return {'error': f'Translation file not found: {translation_file}'}

        if script_file and not os.path.exists(script_file):
            return {'error': f'Script file not found: {script_file}'}

        # Parse translation file
        translation_data = self._parse_translation(translation_file)
        if 'error' in translation_data:
            return translation_data

        # Parse script file if provided
        script_data = None
        if script_file:
            script_data = self._parse_script(script_file)
            # Script errors are non-fatal - fall back to translation-only timing
            if isinstance(script_data, dict) and 'error' in script_data:
                script_data = None

        # Extract project name
        if not project_name:
            project_name = self._extract_project_name(translation_file)

        # Calculate clause timing
        clause_timings = self._calculate_clause_timings(
            translation_data['sections'],
            script_data
        )

        # Calculate section totals
        section_totals = self._calculate_section_totals(clause_timings, translation_data['sections'])

        # Generate transition markers
        transitions = self._generate_transitions(clause_timings, section_totals)

        # Collect assets
        assets = self._collect_assets(translation_data, archive_results)

        # Identify surprises
        surprises = self._extract_surprises(translation_data['sections'])

        # Build guide markdown
        guide_content = self._build_guide(
            project_name=project_name,
            document_name=translation_data.get('document_name', 'Unknown Document'),
            language=translation_data.get('source_language', 'Unknown'),
            clause_timings=clause_timings,
            section_totals=section_totals,
            transitions=transitions,
            assets=assets,
            surprises=surprises,
            total_duration=section_totals[-1]['cumulative_end'] if section_totals else 0
        )

        # Determine output path
        if not output_path:
            translation_dir = os.path.dirname(translation_file)
            output_path = os.path.join(translation_dir, 'SPLIT-SCREEN-EDIT-GUIDE.md')

        # Write guide
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(guide_content)
        except Exception as e:
            return {'error': f'Failed to write guide: {str(e)}'}

        # Calculate totals for return
        total_seconds = section_totals[-1]['cumulative_end'] if section_totals else 0
        total_minutes = total_seconds // 60
        total_remainder = total_seconds % 60

        return {
            'guide_path': output_path,
            'total_duration': total_seconds,
            'total_duration_str': f"{total_minutes} min {total_remainder} sec",
            'clause_count': len(clause_timings),
            'section_count': len(section_totals),
            'assets_auto_sourced': assets['auto_sourced_count'],
            'assets_needed': len(assets['manual_needed']),
            'surprise_count': {
                'major': len([s for s in surprises if s['severity'] == 'major']),
                'notable': len([s for s in surprises if s['severity'] == 'notable'])
            }
        }

    def _parse_translation(self, file_path: str) -> Dict[str, Any]:
        """
        Parse formatted translation file.

        Returns:
            {
                'document_name': str,
                'source_language': str,
                'sections': List[Dict]  # Each: {id, heading, original, translation, surprise}
            }
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Failed to read translation file: {str(e)}'}

        # Extract metadata from header
        doc_name_match = re.search(r'# Translation: (.+)', content)
        lang_match = re.search(r'\*\*Source Language:\*\* (.+)', content)

        document_name = doc_name_match.group(1) if doc_name_match else 'Unknown Document'
        source_language = lang_match.group(1) if lang_match else 'Unknown'

        # Parse sections
        sections = []
        section_pattern = r'## (.+?)\n\n### Original\n\n((?:> .+\n?)+)\n### Translation\n\n(.+?)(?:\n\n---\n\*\*Notes:\*\*\n((?:\d+\. .+\n?)+))?\n\n'

        for match in re.finditer(section_pattern, content, re.DOTALL):
            heading = match.group(1).strip()
            original = match.group(2).strip()
            translation = match.group(3).strip()
            notes = match.group(4).strip() if match.group(4) else None

            # Remove blockquote markers from original
            original_text = re.sub(r'^> ', '', original, flags=re.MULTILINE)

            # Extract section ID from heading (e.g., "Article 1" -> "article-1")
            section_id = heading.lower().replace(' ', '-').replace(':', '')

            # Check for surprise markers in notes or nearby content
            surprise = None
            if notes:
                if 'MAJOR SURPRISE' in notes or 'MAJOR:' in notes:
                    surprise = {'severity': 'major'}
                elif 'NOTABLE SURPRISE' in notes or 'NOTABLE:' in notes:
                    surprise = {'severity': 'notable'}

            sections.append({
                'id': section_id,
                'heading': heading,
                'original': original_text,
                'translation': translation,
                'notes': notes,
                'surprise': surprise
            })

        if not sections:
            return {'error': 'No sections found in translation file. Check format.'}

        return {
            'document_name': document_name,
            'source_language': source_language,
            'sections': sections
        }

    def _parse_script(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse script file to extract word counts per section.

        Returns:
            {
                'sections': {
                    'section-id': {
                        'context_words': int,
                        'explain_words': int,
                        'connect_words': int
                    }
                }
            }

            Or None on failure
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            return {
                'error': f'Failed to read file: {file_path}',
                'module': 'split_screen_guide',
                'operation': '_parse_script',
                'details': str(e)
            }

        # Simple word count extraction - this is a rough estimate
        # Script structure may vary, so we count all words in proximity to section headings
        sections = {}

        # Find sections matching article/section headings
        section_pattern = r'##+ (Article \d+|Section \d+).+?\n\n(.+?)(?=\n##|\Z)'

        for match in re.finditer(section_pattern, content, re.DOTALL):
            heading = match.group(1).strip()
            section_content = match.group(2).strip()
            section_id = heading.lower().replace(' ', '-')

            # Count words
            word_count = len(section_content.split())

            # Rough split: 30% context, 40% explain, 30% connect
            sections[section_id] = {
                'context_words': int(word_count * 0.3),
                'explain_words': int(word_count * 0.4),
                'connect_words': int(word_count * 0.3)
            }

        return {'sections': sections} if sections else None

    def _extract_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        # Look for pattern like "37-vichy-statut-juifs-2026"
        parts = file_path.split(os.sep)
        for part in reversed(parts):
            if re.match(r'\d+-[\w-]+-\d{4}', part):
                return part
        return 'Unknown Project'

    def _calculate_clause_timings(self, sections: List[Dict],
                                  script_data: Optional[Dict]) -> List[Dict]:
        """
        Calculate timing breakdown for each clause.

        Returns list of clause timing dicts with:
        - clause_id, heading
        - context_sec, read_sec, translate_sec, explain_sec, connect_sec
        - total_sec
        - context_words, read_words, translate_words, explain_words, connect_words
        """
        timings = []

        for section in sections:
            section_id = section['id']
            original = section['original']
            translation = section['translation']

            # Count words in original and translation
            read_words = len(original.split())
            translate_words = len(translation.split())

            # Get script word counts if available
            if script_data and section_id in script_data['sections']:
                script_section = script_data['sections'][section_id]
                context_words = script_section['context_words']
                explain_words = script_section['explain_words']
                connect_words = script_section['connect_words']
            else:
                # Fallback estimates based on document complexity
                context_words = max(30, read_words // 3)
                explain_words = max(25, translate_words // 2)
                connect_words = max(15, translate_words // 4)

            # Calculate time segments (at 150 WPM + pauses)
            context_sec = int((context_words / WPM) * 60)
            read_sec = int((read_words / WPM) * 60) + READ_PAUSE
            translate_sec = int((translate_words / WPM) * 60) + TRANSLATE_PAUSE
            explain_sec = int((explain_words / WPM) * 60)
            connect_sec = int((connect_words / WPM) * 60)

            total_sec = context_sec + read_sec + translate_sec + explain_sec + connect_sec

            timings.append({
                'clause_id': section_id,
                'heading': section['heading'],
                'context_sec': context_sec,
                'read_sec': read_sec,
                'translate_sec': translate_sec,
                'explain_sec': explain_sec,
                'connect_sec': connect_sec,
                'total_sec': total_sec,
                'context_words': context_words,
                'read_words': read_words,
                'translate_words': translate_words,
                'explain_words': explain_words,
                'connect_words': connect_words,
                'surprise': section.get('surprise')
            })

        return timings

    def _calculate_section_totals(self, clause_timings: List[Dict],
                                  sections: List[Dict]) -> List[Dict]:
        """
        Calculate section-level totals with cumulative running times.

        Groups clauses into sections (every 5 clauses or natural groupings).

        Returns list of section total dicts with:
        - section_name, clause_range, duration_sec
        - cumulative_start, cumulative_end
        - talking_head_ratio, document_ratio
        """
        if not clause_timings:
            return []

        # Group clauses into sections of ~5 clauses each
        section_size = 5
        section_totals = []
        cumulative = 0

        for i in range(0, len(clause_timings), section_size):
            section_clauses = clause_timings[i:i+section_size]

            # Calculate total duration for this section
            section_duration = sum(c['total_sec'] for c in section_clauses)

            # Determine clause range
            first_clause = section_clauses[0]['heading']
            last_clause = section_clauses[-1]['heading']
            clause_range = f"{first_clause} - {last_clause}" if len(section_clauses) > 1 else first_clause

            # Calculate visual ratios
            # Context, explain, connect = talking head
            # Read, translate = split-screen document display
            talking_head_sec = sum(c['context_sec'] + c['explain_sec'] + c['connect_sec']
                                  for c in section_clauses)
            document_sec = sum(c['read_sec'] + c['translate_sec'] for c in section_clauses)

            talking_head_ratio = int((talking_head_sec / section_duration) * 100) if section_duration else 50
            document_ratio = 100 - talking_head_ratio

            section_totals.append({
                'section_name': f"Section {len(section_totals) + 1}",
                'clause_range': clause_range,
                'duration_sec': section_duration,
                'cumulative_start': cumulative,
                'cumulative_end': cumulative + section_duration,
                'talking_head_ratio': talking_head_ratio,
                'document_ratio': document_ratio
            })

            cumulative += section_duration

        return section_totals

    def _generate_transitions(self, clause_timings: List[Dict],
                             section_totals: List[Dict]) -> Dict[str, Any]:
        """
        Generate transition markers (explicit key switches + ratio guidance).

        Returns:
            {
                'explicit': List[str],  # Timestamped transition markers
                'ratio_guidance': List[str]  # Section-level ratio notes
            }
        """
        explicit = []
        ratio_guidance = []

        # Generate explicit transition markers for first clause of each section
        current_time = 0
        for i, clause in enumerate(clause_timings):
            # Mark transitions at start of each clause
            if i == 0 or i % 5 == 0:  # Section boundaries
                timestamp = self._format_timestamp(current_time + clause['context_sec'])
                explicit.append(f"[{timestamp}] SWITCH TO SPLIT-SCREEN for {clause['heading']} reading")

                timestamp = self._format_timestamp(current_time + clause['context_sec'] + clause['read_sec'] + clause['translate_sec'])
                explicit.append(f"[{timestamp}] RETURN TO TALKING HEAD for significance explanation")

            current_time += clause['total_sec']

        # Generate ratio guidance for each section
        for section in section_totals:
            start_ts = self._format_timestamp(section['cumulative_start'])
            end_ts = self._format_timestamp(section['cumulative_end'])

            ratio_guidance.append(
                f"{section['section_name']}: {section['clause_range']} "
                f"({start_ts} - {end_ts})\n"
                f"Visual Ratio: {section['talking_head_ratio']}% talking head, "
                f"{section['document_ratio']}% split-screen document display"
            )

        return {
            'explicit': explicit[:10],  # Limit to first 10 transitions to avoid clutter
            'ratio_guidance': ratio_guidance
        }

    def _collect_assets(self, translation_data: Dict,
                       archive_results: Optional[Dict]) -> Dict[str, Any]:
        """
        Collect asset requirements (auto-sourced + manual creation needed).

        Returns:
            {
                'auto_sourced': List[Dict],  # {name, url, archive}
                'manual_needed': List[str],  # Asset descriptions
                'auto_sourced_count': int
            }
        """
        auto_sourced = []
        manual_needed = []

        # Auto-source document scans from archive results
        if archive_results and 'archives' in archive_results:
            for archive in archive_results['archives'][:3]:  # Top 3 archives
                auto_sourced.append({
                    'name': f"Document scan from {archive['name']}",
                    'url': archive['search_url'],
                    'archive': archive['name']
                })

        # Add manual placeholders for context visuals
        # These are document-type dependent - using generic placeholders
        manual_needed.extend([
            "[NEEDED] - Map showing geographic context",
            "[NEEDED] - Photo of document signing/issuance location",
            "[NEEDED] - Timeline showing document creation context"
        ])

        return {
            'auto_sourced': auto_sourced,
            'manual_needed': manual_needed,
            'auto_sourced_count': len(auto_sourced)
        }

    def _extract_surprises(self, sections: List[Dict]) -> List[Dict]:
        """
        Extract MAJOR and NOTABLE surprises for editor emphasis.

        Returns list of surprise dicts with:
        - clause_id, heading, severity, timestamp (will be calculated during build)
        """
        surprises = []

        for section in sections:
            surprise = section.get('surprise')
            if surprise and surprise.get('severity') in ['major', 'notable']:
                surprises.append({
                    'clause_id': section['id'],
                    'heading': section['heading'],
                    'severity': surprise['severity'],
                    'section': section
                })

        return surprises

    def _build_guide(self, project_name: str, document_name: str, language: str,
                    clause_timings: List[Dict], section_totals: List[Dict],
                    transitions: Dict, assets: Dict, surprises: List[Dict],
                    total_duration: int) -> str:
        """Build complete guide markdown."""

        # Header
        total_min = total_duration // 60
        total_sec = total_duration % 60

        lines = [
            f"# SPLIT-SCREEN EDIT GUIDE: {document_name}\n",
            f"**Project:** {project_name}",
            f"**Document:** {document_name}",
            f"**Language:** {language}",
            f"**Estimated Runtime:** {total_min} min {total_sec} sec",
            f"**Date Created:** {datetime.now().strftime('%Y-%m-%d')}\n",
            "---\n",
            "## OVERVIEW\n",
            "**Visual Format:** Split-screen throughout walkthrough",
            "- LEFT panel: Original language text",
            "- RIGHT panel: English translation",
            "- Talking head: Context, explanations, connections\n",
            f"**Total Sections:** {len(section_totals)}",
            f"**Total Clauses:** {len(clause_timings)}\n",
            "---\n"
        ]

        # Section breakdowns
        for i, section_total in enumerate(section_totals):
            section_start = section_total['cumulative_start']
            section_end = section_total['cumulative_end']
            section_duration = section_total['duration_sec']

            section_min = section_duration // 60
            section_sec = section_duration % 60

            lines.append(f"## {section_total['section_name']}: {section_total['clause_range']}\n")
            lines.append(f"**Section Duration:** {section_min} min {section_sec} sec "
                        f"({self._format_timestamp(section_start)} - {self._format_timestamp(section_end)})")
            lines.append(f"**Visual Ratio:** {section_total['talking_head_ratio']}% talking head, "
                        f"{section_total['document_ratio']}% split-screen document display\n")

            # Find clauses in this section
            section_clause_count = len([c for c in clause_timings
                                       if clause_timings.index(c) >= i * 5
                                       and clause_timings.index(c) < (i + 1) * 5])

            # Add clause details
            current_time = section_start
            for j in range(i * 5, min((i + 1) * 5, len(clause_timings))):
                clause = clause_timings[j]
                clause_end = current_time + clause['total_sec']

                lines.append(f"\n### {clause['heading']} ({self._format_timestamp(current_time)} - {self._format_timestamp(clause_end)})\n")
                lines.append("**TIMING BREAKDOWN:**")
                lines.append(f"- Context setup (talking head): {self._format_duration(clause['context_sec'])} ({clause['context_words']} words)")
                lines.append(f"- Read original (split-screen LEFT): {self._format_duration(clause['read_sec'])} ({clause['read_words']} words + {READ_PAUSE:.1f} sec pause)")
                lines.append(f"- Translate (split-screen RIGHT): {self._format_duration(clause['translate_sec'])} ({clause['translate_words']} words + {TRANSLATE_PAUSE:.1f} sec pause)")
                lines.append(f"- Explain significance (talking head): {self._format_duration(clause['explain_sec'])} ({clause['explain_words']} words)")
                lines.append(f"- Connect to myth (talking head): {self._format_duration(clause['connect_sec'])} ({clause['connect_words']} words)\n")

                lines.append("**VISUAL STAGING:**\n")
                lines.append(f"[{self._format_timestamp(current_time)} - {self._format_timestamp(current_time + clause['context_sec'])}] TALKING HEAD")
                lines.append("Script: [Context setup paragraph]")
                lines.append("Camera: Medium shot, calm delivery\n")

                current_time += clause['context_sec']
                lines.append(f"[{self._format_timestamp(current_time)} - {self._format_timestamp(current_time + clause['read_sec'])}] SWITCH TO SPLIT-SCREEN")
                lines.append("LEFT panel: Original text")
                lines.append("RIGHT panel: (Blank during reading)")
                lines.append("Script: [Read original]")
                lines.append("Visual cue: Fade in LEFT panel, hold\n")

                current_time += clause['read_sec']
                lines.append(f"[{self._format_timestamp(current_time)} - {self._format_timestamp(current_time + clause['translate_sec'])}] REVEAL TRANSLATION")
                lines.append("LEFT panel: (Remains visible)")
                lines.append("RIGHT panel: Fade in English translation")
                lines.append("Script: [Read translation]")
                lines.append("Visual cue: Highlight key phrase on RIGHT panel\n")

                current_time += clause['translate_sec']
                lines.append(f"[{self._format_timestamp(current_time)} - {self._format_timestamp(current_time + clause['explain_sec'])}] RETURN TO TALKING HEAD")
                lines.append("Script: [Explain significance paragraph]")
                lines.append("Camera: Lean forward slightly for emphasis\n")

                current_time += clause['explain_sec']
                lines.append(f"[{self._format_timestamp(current_time)} - {self._format_timestamp(current_time + clause['connect_sec'])}] TALKING HEAD (continued)")
                lines.append("Script: [Connect to myth paragraph]")
                lines.append("Camera: Return to medium shot\n")

                current_time += clause['connect_sec']

                # Asset note
                lines.append("**ASSETS NEEDED:**")
                lines.append(f"- {clause['heading']} original text: From translation output")
                lines.append(f"- {clause['heading']} translation: From translation output\n")

                lines.append("---\n")

        # Surprise markers section
        if surprises:
            lines.append("\n## SURPRISE MARKERS (Editor Emphasis)\n")

            major_surprises = [s for s in surprises if s['severity'] == 'major']
            notable_surprises = [s for s in surprises if s['severity'] == 'notable']

            if major_surprises:
                lines.append("### MAJOR SURPRISES (Must highlight)\n")
                for surprise in major_surprises:
                    # Find timing for this clause
                    clause_timing = next((c for c in clause_timings if c['clause_id'] == surprise['clause_id']), None)
                    if clause_timing:
                        clause_index = clause_timings.index(clause_timing)
                        # Calculate timestamp
                        timestamp = sum(c['total_sec'] for c in clause_timings[:clause_index])

                        lines.append(f"**{surprise['heading']} ({self._format_timestamp(timestamp)}):**")
                        lines.append("⚠️ Contradicts common narrative")
                        lines.append("Suggestion: Slow zoom on key phrase, extended hold on translation, consider highlight box or underline animation\n")

            if notable_surprises:
                lines.append("### NOTABLE SURPRISES (Worth highlighting)\n")
                for surprise in notable_surprises:
                    clause_timing = next((c for c in clause_timings if c['clause_id'] == surprise['clause_id']), None)
                    if clause_timing:
                        clause_index = clause_timings.index(clause_timing)
                        timestamp = sum(c['total_sec'] for c in clause_timings[:clause_index])

                        lines.append(f"**{surprise['heading']} ({self._format_timestamp(timestamp)}):**")
                        lines.append("📍 Adds important nuance")
                        lines.append("Suggestion: Brief hold on key phrase, no need for animation\n")

            lines.append("---\n")

        # Asset checklist
        lines.append("\n## ASSET CHECKLIST\n")

        if assets['auto_sourced']:
            lines.append("### Auto-Sourced (From Archive Lookup)")
            for asset in assets['auto_sourced']:
                lines.append(f"- [ ] {asset['name']}: {asset['url']}")
            lines.append("")

        if assets['manual_needed']:
            lines.append("### Manual Creation Needed")
            for asset in assets['manual_needed']:
                lines.append(f"- [ ] {asset}")
            lines.append("")

        lines.append("---\n")

        # Pacing notes
        lines.append("\n## PACING NOTES\n")
        if section_totals:
            first_section = section_totals[0]
            first_min = first_section['duration_sec'] // 60
            lines.append(f"**First {first_min} minutes ({first_section['clause_range']}):** Establish format, build viewer trust")
            lines.append("- Ensure split-screen reveals are smooth")
            lines.append("- Don't rush translations - allow processing time\n")

            if len(section_totals) > 2:
                middle_section = section_totals[len(section_totals)//2]
                lines.append(f"**Middle section ({middle_section['clause_range']}):** Maintain rhythm")
                lines.append("- Pattern is established, can move faster through non-surprise clauses")
                if major_surprises:
                    lines.append(f"- Major surprise at {major_surprises[0]['heading']} - spend extra time\n")
                else:
                    lines.append("")

            if len(section_totals) > 1:
                final_section = section_totals[-1]
                lines.append(f"**Final section ({final_section['clause_range']}):** Build to synthesis")
                lines.append("- Set up synthesis section by foreshadowing contradictions\n")

        lines.append("---\n")

        return '\n'.join(lines)

    def _format_timestamp(self, seconds: int) -> str:
        """Format seconds as MM:SS timestamp."""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def _format_duration(self, seconds: int) -> str:
        """Format seconds as readable duration."""
        if seconds < 60:
            return f"{seconds} sec"
        minutes = seconds // 60
        secs = seconds % 60
        if secs == 0:
            return f"{minutes} min"
        return f"{minutes}:{secs:02d}"


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate split-screen edit guide for document walkthrough videos')
    parser.add_argument('--translation', required=True, help='Path to formatted translation file')
    parser.add_argument('--script', help='Optional path to script file')
    parser.add_argument('--output', help='Optional output path (defaults to translation directory)')
    parser.add_argument('--project', help='Optional project name')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    generator = SplitScreenGuide()
    result = generator.generate_guide(
        translation_file=args.translation,
        script_file=args.script,
        output_path=args.output,
        project_name=args.project
    )

    if 'error' in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Split-screen edit guide generated successfully!")
    print(f"Location: {result['guide_path']}")
    print(f"Total duration: {result['total_duration_str']}")
    print(f"Clauses: {result['clause_count']}")
    print(f"Sections: {result['section_count']}")
    print(f"Assets auto-sourced: {result['assets_auto_sourced']}")
    print(f"Assets needing manual creation: {result['assets_needed']}")
    print(f"Major surprises: {result['surprise_count']['major']}")
    print(f"Notable surprises: {result['surprise_count']['notable']}")


if __name__ == '__main__':
    main()
