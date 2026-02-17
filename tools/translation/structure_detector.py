"""
Document Structure Detector (TRAN-01 component)

Auto-detects article/clause boundaries in legal documents across multiple languages.
Supports French, Spanish, German, Latin legal/treaty texts with fallback to paragraph splitting.
"""

import re
from typing import Dict, Any, List, Optional


class StructureDetector:
    """
    Detect article/clause structure in legal and historical documents.

    Supports:
    - French legal: Article N, Art. N, ARTICLE N
    - Spanish legal: Artículo N, Art. N
    - German legal: Artikel N, § N
    - Latin/treaty: Articulus N
    - Generic: Section N, Chapter N, Clause N
    - Roman numerals: I., II., III., etc.
    """

    # Article marker patterns by language
    ARTICLE_PATTERNS = [
        # French
        r'^(Article\s+\d+)',
        r'^(Art\.\s*\d+)',
        r'^(ARTICLE\s+\d+)',
        # Spanish
        r'^(Artículo\s+\d+)',
        r'^(Articulo\s+\d+)',  # without accent
        # German
        r'^(Artikel\s+\d+)',
        r'^(§\s*\d+)',
        # Latin
        r'^(Articulus\s+\d+)',
        # Generic English
        r'^(Section\s+\d+)',
        r'^(Chapter\s+\d+)',
        r'^(Clause\s+\d+)',
        # Roman numerals (at line start)
        r'^([IVXLCDM]+\.?\s)',
    ]

    def __init__(self):
        """Initialize structure detector."""
        # Compile patterns
        self.compiled_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE)
                                  for p in self.ARTICLE_PATTERNS]

    def detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect article/clause boundaries in document text.

        Args:
            text: Raw document text
            document_type: Optional type hint (legal_code, treaty, decree, book, letter, other)

        Returns:
            Dict with keys:
            - 'document_type': User override if provided, else auto-detected
            - 'detected_type': Auto-detected document type
            - 'sections': List of section dicts with id, heading, body, start_line, end_line
            - 'section_count': Number of sections detected
            - 'has_preamble': Whether preamble text exists before first article
            - 'raw_text': Original input text

            Or {'error': msg} on failure
        """
        if not text or not text.strip():
            return {'error': 'Document text cannot be empty'}

        text = text.strip()
        lines = text.split('\n')

        # Try to find article markers
        article_positions = self._find_article_markers(lines)

        if article_positions:
            # Article-based structure detected
            sections = self._extract_article_sections(lines, article_positions)
            detected_type = self._infer_document_type(article_positions, text)
            has_preamble = article_positions[0]['line_num'] > 0
        else:
            # Fall back to paragraph-based splitting
            sections = self._extract_paragraph_sections(text)
            detected_type = 'other'
            has_preamble = False

        # Extract preamble if exists
        if has_preamble:
            preamble_text = '\n'.join(lines[:article_positions[0]['line_num']]).strip()
            if preamble_text:
                preamble_section = {
                    'id': 'preamble',
                    'heading': 'Preamble',
                    'body': preamble_text,
                    'start_line': 0,
                    'end_line': article_positions[0]['line_num'] - 1
                }
                sections.insert(0, preamble_section)

        # Optional integration with Phase 39 structure assessor for video length estimates
        timing_estimates = None
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent / 'document_discovery'))
            from structure_assessor import StructureAssessor
            assessor = StructureAssessor()
            timing_estimates = assessor.TIMING_ESTIMATES.get(detected_type or 'other')
        except (ImportError, Exception):
            # Phase 39 not available - continue without timing estimates
            pass

        result = {
            'document_type': document_type if document_type else detected_type,
            'detected_type': detected_type,
            'sections': sections,
            'section_count': len(sections),
            'has_preamble': has_preamble,
            'raw_text': text
        }

        if timing_estimates:
            result['timing_estimates'] = timing_estimates

        return result

    def _find_article_markers(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Find all article marker positions in document.

        Returns:
            List of dicts with 'line_num', 'marker_text', 'pattern_index'
        """
        markers = []

        for line_num, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Try each pattern
            for pattern_idx, pattern in enumerate(self.compiled_patterns):
                match = pattern.match(line_stripped)
                if match:
                    markers.append({
                        'line_num': line_num,
                        'marker_text': match.group(1).strip(),
                        'pattern_index': pattern_idx,
                        'full_line': line_stripped
                    })
                    break  # Only match first pattern

        return markers

    def _extract_article_sections(self, lines: List[str], markers: List[Dict]) -> List[Dict]:
        """
        Extract sections based on detected article markers.

        Returns:
            List of section dicts
        """
        sections = []

        for i, marker in enumerate(markers):
            # Determine section boundaries
            start_line = marker['line_num']

            if i + 1 < len(markers):
                # End at next marker
                end_line = markers[i + 1]['line_num'] - 1
            else:
                # Last section goes to end
                end_line = len(lines) - 1

            # Extract heading (marker line itself)
            heading = lines[start_line].strip()

            # Extract body (lines after heading until next marker)
            body_lines = []
            for line_num in range(start_line + 1, end_line + 1):
                line = lines[line_num].strip()
                if line:  # Skip empty lines
                    body_lines.append(line)

            body = '\n'.join(body_lines)

            # Generate section ID
            section_id = self._generate_section_id(marker['marker_text'], i + 1)

            sections.append({
                'id': section_id,
                'heading': heading,
                'body': body,
                'start_line': start_line,
                'end_line': end_line
            })

        return sections

    def _extract_paragraph_sections(self, text: str) -> List[Dict]:
        """
        Fall back to paragraph-based splitting when no article markers found.

        Returns:
            List of section dicts (one per paragraph)
        """
        # Split on double newlines
        paragraphs = re.split(r'\n\s*\n', text)

        sections = []
        line_counter = 0

        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue

            para_lines = para.split('\n')
            start_line = line_counter
            end_line = line_counter + len(para_lines) - 1
            line_counter = end_line + 2  # Account for blank line

            sections.append({
                'id': f'paragraph-{i + 1}',
                'heading': f'Paragraph {i + 1}',
                'body': para,
                'start_line': start_line,
                'end_line': end_line
            })

        return sections

    def _generate_section_id(self, marker_text: str, section_num: int) -> str:
        """
        Generate section ID from marker text.

        Examples:
            'Article 1' -> 'article-1'
            'Art. 5' -> 'article-5'
            '§ 12' -> 'section-12'
            'I.' -> 'article-1'
        """
        marker_lower = marker_text.lower()

        # Extract number if present
        num_match = re.search(r'\d+', marker_text)
        if num_match:
            num = num_match.group()
        else:
            num = str(section_num)

        # Determine prefix
        if 'article' in marker_lower or 'art.' in marker_lower or 'articulo' in marker_lower:
            prefix = 'article'
        elif 'section' in marker_lower or '§' in marker_text:
            prefix = 'section'
        elif 'chapter' in marker_lower:
            prefix = 'chapter'
        elif 'clause' in marker_lower:
            prefix = 'clause'
        else:
            # Roman numeral or other
            prefix = 'article'

        return f'{prefix}-{num}'

    def _infer_document_type(self, markers: List[Dict], full_text: str) -> str:
        """
        Infer document type from detected structure.

        Returns:
            One of: legal_code, treaty, decree, book, letter, other
        """
        marker_count = len(markers)

        # Check for treaty keywords
        if any(word in full_text.lower() for word in ['treaty', 'convention', 'protocol', 'agreement']):
            return 'treaty'

        # Check for decree/statute keywords
        if any(word in full_text.lower() for word in ['decree', 'statute', 'law', 'loi', 'statut']):
            return 'legal_code'

        # Check for book/chapter structure
        if any('chapter' in m['marker_text'].lower() for m in markers):
            return 'book'

        # Default to legal_code if has articles
        if marker_count > 0:
            return 'legal_code'

        return 'other'
