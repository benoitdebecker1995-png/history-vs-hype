"""
nlm_ingest.py — NotebookLM output ingestion for History vs Hype research workflow.

Extracts structured claims from raw NotebookLM chat output, generates a markdown
review checklist for the user to approve/reject/edit each claim, then writes
approved claims into the project's 01-VERIFIED-RESEARCH.md file.

Usage (via /research --ingest slash command):

    Step 1 — Parse & extract:
        from nlm_ingest import ingest
        result = ingest(input_text="<NLM output>", project_path="video-projects/...")

    Step 2 — User edits the review file (checks [x] or leaves [ ])

    Step 3 — Apply approved claims:
        from nlm_ingest import apply_review
        result = apply_review(
            review_path="path/to/_NLM-REVIEW-2026-02-20.md",
            verified_research_path="path/to/01-VERIFIED-RESEARCH.md"
        )

All public functions return a dict. On error: {'error': str}.
No exceptions are raised from public API.
"""

import re
import os
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# NLMParser
# ---------------------------------------------------------------------------

class NLMParser:
    """
    Parse raw NotebookLM output into claim-candidate chunks.

    Handles two input formats:
    - Structured: bullet points with inline citations
    - Freeform: paragraphs mixing claims with discussion
    """

    # Citation pattern variants
    _CITATION_PATTERNS = [
        # Author (Year, p. 45) or Author (2020, pp. 45-46)
        r'\b[A-Z][a-zA-Z\-]+\s+\(\d{4},\s*pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\)',
        # [Source N, p. 23] or [Source 3, pp. 12-15]
        r'\[Source\s+\d+,\s*pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\]',
        # page 45 or pages 45-46
        r'\bpages?\s+\d+(?:\s*[-–]\s*\d+)?\b',
        # p. 142 or pp. 142-143 (standalone)
        r'\bpp?\.\s*\d+(?:\s*[-–]\s*\d+)?\b',
        # "on page 142" — Allen argues on page 142
        r'\bon\s+page\s+\d+\b',
        # (p.45) or (pp. 45-46) in parentheses
        r'\(\s*pp?\.\s*\d+(?:\s*[-–]\s*\d+)?\s*\)',
    ]

    _CITATION_RE = re.compile(
        '|'.join(_CITATION_PATTERNS),
        re.IGNORECASE
    )

    # Sentence boundary: period/question/exclamation followed by space+capital
    _SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')

    def parse(self, text: str) -> dict:
        """
        Parse raw NLM text into claim-candidate chunks.

        Returns:
            {
                'chunks': [
                    {
                        'text': str,
                        'citation': str,
                        'source_ref': str,
                        'line_number': int
                    }
                ],
                'parse_stats': {
                    'total_lines': int,
                    'chunks_found': int,
                    'citation_coverage': float  # 0.0–1.0
                }
            }
        """
        if not text or not text.strip():
            return {
                'chunks': [],
                'parse_stats': {
                    'total_lines': 0,
                    'chunks_found': 0,
                    'citation_coverage': 0.0,
                }
            }

        lines = text.splitlines()
        total_lines = len(lines)
        chunks = []

        # First pass: try to detect structured (bullet) format
        structured_chunks = self._parse_structured(lines)

        # Second pass: parse as freeform if structured yielded nothing
        if structured_chunks:
            chunks = structured_chunks
        else:
            chunks = self._parse_freeform(text, lines)

        # Compute citation coverage
        chunks_with_citation = sum(
            1 for c in chunks if c.get('citation') and c['citation'].strip()
        )
        coverage = chunks_with_citation / len(chunks) if chunks else 0.0

        return {
            'chunks': chunks,
            'parse_stats': {
                'total_lines': total_lines,
                'chunks_found': len(chunks),
                'citation_coverage': round(coverage, 2),
            }
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_structured(self, lines: list) -> list:
        """
        Parse bullet-point / structured NLM output.

        A "structured" line starts with '-', '*', '•', or a digit+'.'.
        Returns list of chunk dicts, or empty list if format not detected.
        """
        bullet_re = re.compile(r'^\s*[-*•]\s+|^\s*\d+\.\s+')
        chunks = []

        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            # Only process bullet lines for structured extraction
            if not bullet_re.match(line):
                continue

            # Remove bullet marker
            text_body = bullet_re.sub('', line).strip()
            if not text_body:
                continue

            citation, source_ref = self._extract_citation_info(text_body)
            chunks.append({
                'text': text_body,
                'citation': citation,
                'source_ref': source_ref,
                'line_number': line_number,
            })

        return chunks

    def _parse_freeform(self, text: str, lines: list) -> list:
        """
        Parse freeform paragraph NLM output by splitting on sentence boundaries
        near citation markers.
        """
        chunks = []
        # Split on sentence boundaries
        sentences = self._SENTENCE_SPLIT_RE.split(text)

        # Track approximate line numbers
        current_pos = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                current_pos += len(sentence)
                continue

            # Only keep sentences that contain citation markers or
            # at least look like substantive claims (length > 40)
            has_citation = bool(self._CITATION_RE.search(sentence))
            if not has_citation and len(sentence) < 60:
                current_pos += len(sentence)
                continue

            # Approximate line number from character position
            approx_line = text[:current_pos].count('\n') + 1

            citation, source_ref = self._extract_citation_info(sentence)
            chunks.append({
                'text': sentence,
                'citation': citation,
                'source_ref': source_ref,
                'line_number': approx_line,
            })

            current_pos += len(sentence)

        return chunks

    def _extract_citation_info(self, text: str) -> tuple:
        """
        Extract citation string and source reference from a chunk of text.

        Returns: (citation_str, source_ref_str)
        """
        matches = list(self._CITATION_RE.finditer(text))
        if not matches:
            return ('', '')

        # Collect all citation fragments
        citation_parts = [m.group(0) for m in matches]
        citation = '; '.join(citation_parts)

        # Extract source reference: look for Author name before first match
        first_match_start = matches[0].start()
        prefix = text[:first_match_start].strip()
        # Source ref = last word-sequence before the citation (often the author name)
        author_re = re.compile(r'([A-Z][a-zA-Z\-]+(?: [A-Z][a-zA-Z\-]+)?)\s*$')
        author_match = author_re.search(prefix)
        source_ref = author_match.group(1) if author_match else ''

        return (citation, source_ref)


# ---------------------------------------------------------------------------
# ClaimExtractor
# ---------------------------------------------------------------------------

class ClaimExtractor:
    """
    Categorize claim-candidate chunks by type and assign confidence levels.
    """

    _STATISTIC_KEYWORDS = re.compile(
        r'\b(\d+\.?\d*\s*%|GDP|population|rate|percent|million|billion|'
        r'thousand|grew|growth|decline|increased|decreased|doubled|halved|'
        r'ratio|average|median|per capita|annual|output)\b',
        re.IGNORECASE
    )

    _QUOTE_KEYWORDS = re.compile(
        r'["\u201c\u201d]|'
        r'\b(said|wrote|argued|stated|noted|claimed|observed|'
        r'declared|concluded|asserted|described|explained)\b',
        re.IGNORECASE
    )

    _EVENT_KEYWORDS = re.compile(
        r'\b(\d{4}|century|era|decade|war|treaty|battle|revolution|'
        r'coup|invasion|occupation|independence|colonization|'
        r'annexation|partition|agreement|accord|pact)\b',
        re.IGNORECASE
    )

    _DEFINITION_KEYWORDS = re.compile(
        r'\b(defined as|means|refers to|is called|known as|'
        r'understood as|described as|term|concept|denotes|signifies)\b',
        re.IGNORECASE
    )

    # Confidence: high = author + page, medium = one of those, low = neither
    _PAGE_RE = re.compile(r'\bpp?\.\s*\d+|\bpage\s+\d+', re.IGNORECASE)
    _AUTHOR_RE = re.compile(r'[A-Z][a-z]+\s*\(\d{4}|According to [A-Z]|[A-Z][a-z]+ argues', re.IGNORECASE)

    def extract_claims(self, chunks: list) -> dict:
        """
        Categorize chunks and assign confidence.

        Args:
            chunks: list of chunk dicts from NLMParser.parse()

        Returns:
            {
                'claims': [
                    {
                        'id': int,
                        'text': str,
                        'type': str,          # statistic|quote|event|definition|claim
                        'citation': str,
                        'confidence': str     # high|medium|low
                    }
                ],
                'by_type': {
                    'statistic': int,
                    'quote': int,
                    'event': int,
                    'definition': int,
                    'claim': int,
                }
            }
        """
        claims = []
        by_type = {
            'statistic': 0,
            'quote': 0,
            'event': 0,
            'definition': 0,
            'claim': 0,
        }

        for idx, chunk in enumerate(chunks, start=1):
            text = chunk.get('text', '')
            citation = chunk.get('citation', '')

            claim_type = self._categorize(text)
            confidence = self._confidence(text, citation)

            claims.append({
                'id': idx,
                'text': text,
                'type': claim_type,
                'citation': citation,
                'confidence': confidence,
            })
            by_type[claim_type] += 1

        return {
            'claims': claims,
            'by_type': by_type,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _categorize(self, text: str) -> str:
        """Assign a category using keyword heuristics (order matters)."""
        # Quote check first — most specific
        if self._QUOTE_KEYWORDS.search(text):
            return 'quote'
        # Definition
        if self._DEFINITION_KEYWORDS.search(text):
            return 'definition'
        # Statistic
        if self._STATISTIC_KEYWORDS.search(text):
            return 'statistic'
        # Event
        if self._EVENT_KEYWORDS.search(text):
            return 'event'
        # General claim
        return 'claim'

    def _confidence(self, text: str, citation: str) -> str:
        """Determine citation confidence."""
        combined = text + ' ' + citation
        has_page = bool(self._PAGE_RE.search(combined))
        has_author = bool(self._AUTHOR_RE.search(combined))

        if has_page and has_author:
            return 'high'
        if has_page or has_author:
            return 'medium'
        return 'low'


# ---------------------------------------------------------------------------
# ReviewGenerator
# ---------------------------------------------------------------------------

class ReviewGenerator:
    """
    Create a markdown checklist file for user review of extracted claims.
    """

    _TYPE_ORDER = ['statistic', 'quote', 'event', 'definition', 'claim']
    _TYPE_LABELS = {
        'statistic': 'Statistics',
        'quote': 'Quotes',
        'event': 'Events',
        'definition': 'Definitions',
        'claim': 'General Claims',
    }

    def generate_review_file(
        self,
        claims: list,
        output_path: str,
        verified_research_path: str = ''
    ) -> dict:
        """
        Write a markdown review file grouping claims by type.

        Args:
            claims: list of claim dicts from ClaimExtractor.extract_claims()
            output_path: where to write the review file
            verified_research_path: shown in header for user reference

        Returns:
            {'path': str, 'claim_count': int} or {'error': str}
        """
        if not claims:
            return {'error': 'No claims to review — extraction produced empty list'}

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        except Exception as e:
            return {'error': f'Could not create directory for review file: {e}'}

        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        target_label = verified_research_path or '01-VERIFIED-RESEARCH.md'

        lines = [
            f'# NLM Claim Review - {timestamp}',
            '',
            '**Instructions:** Review each claim below. For each claim:',
            '- `[x]` = APPROVE (will be written to VERIFIED-RESEARCH.md)',
            '- `[ ]` = REJECT (will be skipped)',
            '- Edit the text/citation directly to correct before approving',
            '',
            f'**Target file:** {target_label}',
            '',
            '---',
            '',
        ]

        # Group by type
        by_type: dict[str, list] = {t: [] for t in self._TYPE_ORDER}
        for claim in claims:
            claim_type = claim.get('type', 'claim')
            if claim_type not in by_type:
                claim_type = 'claim'
            by_type[claim_type].append(claim)

        for type_key in self._TYPE_ORDER:
            type_claims = by_type[type_key]
            if not type_claims:
                continue

            label = self._TYPE_LABELS[type_key]
            lines.append(f'## {label} ({len(type_claims)} claim{"s" if len(type_claims) != 1 else ""})')
            lines.append('')

            for claim in type_claims:
                claim_id = claim.get('id', '?')
                text = claim.get('text', '').strip()
                citation = claim.get('citation', '').strip()
                confidence = claim.get('confidence', 'low')

                # Truncate very long claim text for the checkbox line
                short_text = text if len(text) <= 120 else text[:117] + '...'

                lines.append(f'- [ ] **[{claim_id}]** {short_text}')
                if citation:
                    lines.append(f'  - Citation: {citation}')
                else:
                    lines.append('  - Citation: (none found — add manually if needed)')
                lines.append(f'  - Confidence: {confidence}')
                if len(text) > 120:
                    lines.append(f'  - Full text: {text}')
                lines.append('')

        # Footer
        lines += [
            '---',
            '',
            f'*Generated by nlm_ingest.py at {timestamp}*',
            f'*Run `/research --apply-review {output_path}` when done*',
        ]

        content = '\n'.join(lines)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            return {'error': f'Could not write review file: {e}'}

        return {
            'path': output_path,
            'claim_count': len(claims),
        }


# ---------------------------------------------------------------------------
# ReviewReader
# ---------------------------------------------------------------------------

class ReviewReader:
    """
    Parse a user-edited review file to determine which claims were approved.
    """

    # Match: - [x] **[ID]** text  (case-insensitive x)
    _APPROVED_RE = re.compile(
        r'^\s*-\s+\[x\]\s+\*\*\[(\d+)\]\*\*\s+(.*)',
        re.IGNORECASE
    )
    # Match: - [ ] **[ID]** text
    _REJECTED_RE = re.compile(
        r'^\s*-\s+\[\s*\]\s+\*\*\[(\d+)\]\*\*\s+(.*)',
    )
    # Match citation line: "  - Citation: ..."
    _CITATION_LINE_RE = re.compile(r'^\s{2,}-\s+Citation:\s+(.*)')
    # Match type line from section header: ## Statistics, ## Quotes, etc.
    _SECTION_RE = re.compile(
        r'^##\s+(Statistics|Quotes|Events|Definitions|General Claims)',
        re.IGNORECASE
    )

    _LABEL_TO_TYPE = {
        'statistics': 'statistic',
        'quotes': 'quote',
        'events': 'event',
        'definitions': 'definition',
        'general claims': 'claim',
    }

    def read_approvals(self, review_path: str) -> dict:
        """
        Read a review markdown file and return approved claims.

        Returns:
            {
                'approved': [
                    {
                        'id': int,
                        'text': str,
                        'citation': str,
                        'type': str
                    }
                ],
                'rejected_count': int,
                'approved_count': int
            }
            or {'error': str}
        """
        if not os.path.isfile(review_path):
            return {'error': f'Review file not found: {review_path}'}

        try:
            with open(review_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return {'error': f'Could not read review file: {e}'}

        approved = []
        rejected_count = 0
        current_type = 'claim'
        i = 0

        while i < len(lines):
            line = lines[i]

            # Track current section type
            section_match = self._SECTION_RE.match(line)
            if section_match:
                label = section_match.group(1).lower()
                current_type = self._LABEL_TO_TYPE.get(label, 'claim')
                i += 1
                continue

            # Check for approved claim
            approved_match = self._APPROVED_RE.match(line)
            if approved_match:
                claim_id = int(approved_match.group(1))
                text = approved_match.group(2).strip()

                # Look ahead for citation on the very next indented line
                citation = ''
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    cit_match = self._CITATION_LINE_RE.match(next_line)
                    if cit_match:
                        cit_value = cit_match.group(1).strip()
                        # Skip placeholder "none found" citations
                        if 'none found' not in cit_value.lower():
                            citation = cit_value
                        j += 1
                    elif next_line.strip().startswith('-') or next_line.strip() == '':
                        break
                    else:
                        j += 1

                approved.append({
                    'id': claim_id,
                    'text': text,
                    'citation': citation,
                    'type': current_type,
                })
                i += 1
                continue

            # Check for rejected claim
            rejected_match = self._REJECTED_RE.match(line)
            if rejected_match:
                rejected_count += 1
                i += 1
                continue

            i += 1

        return {
            'approved': approved,
            'rejected_count': rejected_count,
            'approved_count': len(approved),
        }


# ---------------------------------------------------------------------------
# VerifiedResearchWriter
# ---------------------------------------------------------------------------

class VerifiedResearchWriter:
    """
    Append approved claims to a project's 01-VERIFIED-RESEARCH.md file.

    Maps claim types to known section headings. Falls back to an
    "INGESTED CLAIMS (Unsorted)" section at the end of the file.
    """

    # Section-heading candidates per claim type (first match wins)
    _SECTION_MAP = {
        'statistic': [
            'KEY STATISTICS',
            'ECONOMIC DATA',
            'VERIFIED NUMBERS',
            'STATISTICS',
            'DATA',
        ],
        'quote': [
            'VERIFIED QUOTES',
            'KEY QUOTES',
            'QUOTES',
        ],
        'event': [
            'TIMELINE',
            'KEY EVENTS',
            'EVENTS',
            'CHRONOLOGY',
        ],
        'definition': [
            'DEFINITIONS',
            'GLOSSARY',
            'TERMS',
        ],
        'claim': [
            'CLAIMS TO VERIFY',
            'VERIFIED CLAIMS',
            'CLAIMS',
        ],
    }

    _FALLBACK_SECTION = 'INGESTED CLAIMS (Unsorted)'

    def write_claims(
        self,
        claims: list,
        verified_research_path: str
    ) -> dict:
        """
        Write approved claims into sections of VERIFIED-RESEARCH.md.

        Args:
            claims: list of approved claim dicts (from ReviewReader)
            verified_research_path: absolute or relative path to the file

        Returns:
            {'written': int, 'sections_updated': list, 'path': str}
            or {'error': str}
        """
        if not os.path.isfile(verified_research_path):
            return {
                'error': (
                    f'VERIFIED-RESEARCH.md not found: {verified_research_path}. '
                    'Run /research --new first to set up the project.'
                )
            }

        if not claims:
            return {'error': 'No approved claims to write'}

        try:
            with open(verified_research_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Could not read VERIFIED-RESEARCH.md: {e}'}

        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        written = 0
        sections_updated = []

        for claim in claims:
            text = claim.get('text', '').strip()
            citation = claim.get('citation', '').strip()
            claim_type = claim.get('type', 'claim')

            if not text:
                continue

            # Build the claim block in VERIFIED-RESEARCH format
            short_summary = text[:60].rstrip() + ('...' if len(text) > 60 else '')
            block_lines = [
                f'',
                f'### {short_summary}',
                f'- **Status:** \u2705 VERIFIED (via NLM ingestion)',
                f'- **Claim:** {text}',
            ]
            if citation:
                block_lines.append(f'- **Source:** {citation}')
            block_lines.append(f'- **Ingested:** {today}')
            block = '\n'.join(block_lines) + '\n'

            # Find insertion point
            section_heading, content = self._insert_into_section(
                content, claim_type, block
            )
            sections_updated.append(section_heading)
            written += 1

        # Deduplicate section list while preserving order
        seen = set()
        unique_sections = []
        for s in sections_updated:
            if s not in seen:
                seen.add(s)
                unique_sections.append(s)

        try:
            with open(verified_research_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            return {'error': f'Could not write VERIFIED-RESEARCH.md: {e}'}

        return {
            'written': written,
            'sections_updated': unique_sections,
            'path': verified_research_path,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _insert_into_section(
        self,
        content: str,
        claim_type: str,
        block: str
    ) -> tuple:
        """
        Find the best matching section heading and insert block after it.

        Returns (section_name_used, updated_content).
        """
        candidates = self._SECTION_MAP.get(claim_type, [])

        for candidate in candidates:
            # Search for "## CANDIDATE" heading (case-insensitive)
            pattern = re.compile(
                r'^(##\s+' + re.escape(candidate) + r'[^\n]*)\n',
                re.IGNORECASE | re.MULTILINE
            )
            match = pattern.search(content)
            if match:
                # Insert block right after the heading line
                insert_pos = match.end()
                content = content[:insert_pos] + block + content[insert_pos:]
                return (candidate, content)

        # No matching section found — use / create fallback section
        fallback_heading = f'\n## {self._FALLBACK_SECTION}\n'
        if self._FALLBACK_SECTION.lower() in content.lower():
            # Append after existing fallback section heading
            pattern = re.compile(
                r'^(##\s+' + re.escape(self._FALLBACK_SECTION) + r'[^\n]*)\n',
                re.IGNORECASE | re.MULTILINE
            )
            match = pattern.search(content)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + block + content[insert_pos:]
                return (self._FALLBACK_SECTION, content)

        # Create the fallback section at the very end
        content = content.rstrip('\n') + '\n' + fallback_heading + block
        return (self._FALLBACK_SECTION, content)


# ---------------------------------------------------------------------------
# CLI orchestration functions
# ---------------------------------------------------------------------------

def ingest(
    input_text: str = None,
    input_file: str = None,
    project_path: str = None,
) -> dict:
    """
    Full ingestion flow: parse NLM output, extract claims, generate review file.

    Call this from the /research --ingest slash command.

    Args:
        input_text: raw NLM output text (pasted directly)
        input_file: path to a .txt/.md file containing NLM output
        project_path: path to project folder (must contain _research/ subfolder or it will be created)

    Returns:
        {
            'review_path': str,
            'claim_count': int,
            'by_type': dict,
            'parse_stats': dict,
        }
        or {'error': str}
    """
    # 1. Read input
    if input_text:
        text = input_text
    elif input_file:
        if not os.path.isfile(input_file):
            return {'error': f'Input file not found: {input_file}'}
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            return {'error': f'Could not read input file: {e}'}
    else:
        return {'error': 'Provide either input_text or input_file'}

    if not text.strip():
        return {'error': 'Input text is empty'}

    # 2. Determine project path
    if not project_path:
        project_path = os.getcwd()

    research_dir = os.path.join(project_path, '_research')

    # 3. Parse
    parser = NLMParser()
    parse_result = parser.parse(text)
    chunks = parse_result.get('chunks', [])
    parse_stats = parse_result.get('parse_stats', {})

    if not chunks:
        return {
            'error': (
                'No claim chunks extracted from NLM output. '
                'The text may be too short or lack recognizable citation patterns.'
            )
        }

    # 4. Extract claims
    extractor = ClaimExtractor()
    extract_result = extractor.extract_claims(chunks)
    claims = extract_result.get('claims', [])
    by_type = extract_result.get('by_type', {})

    # 5. Generate review file
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M')
    review_filename = f'_NLM-REVIEW-{timestamp}.md'
    review_path = os.path.join(research_dir, review_filename)

    # Try to find the VERIFIED-RESEARCH.md path for reference in review header
    vr_candidates = [
        os.path.join(project_path, '01-VERIFIED-RESEARCH.md'),
        os.path.join(project_path, '01-VERIFIED-RESEARCH.md'),
    ]
    vr_path_hint = ''
    for candidate in vr_candidates:
        if os.path.isfile(candidate):
            vr_path_hint = candidate
            break

    generator = ReviewGenerator()
    gen_result = generator.generate_review_file(
        claims=claims,
        output_path=review_path,
        verified_research_path=vr_path_hint,
    )

    if 'error' in gen_result:
        return gen_result

    return {
        'review_path': gen_result['path'],
        'claim_count': gen_result['claim_count'],
        'by_type': by_type,
        'parse_stats': parse_stats,
    }


def apply_review(
    review_path: str,
    verified_research_path: str,
) -> dict:
    """
    Apply approved claims from a reviewed file to VERIFIED-RESEARCH.md.

    Call this from the /research --apply-review slash command.

    Args:
        review_path: path to the _NLM-REVIEW-*.md file the user edited
        verified_research_path: path to the project's 01-VERIFIED-RESEARCH.md

    Returns:
        {
            'written': int,
            'approved_count': int,
            'rejected_count': int,
            'sections_updated': list,
            'path': str,
        }
        or {'error': str}
    """
    # 1. Read approvals from review file
    reader = ReviewReader()
    read_result = reader.read_approvals(review_path)

    if 'error' in read_result:
        return read_result

    approved = read_result.get('approved', [])
    rejected_count = read_result.get('rejected_count', 0)
    approved_count = read_result.get('approved_count', 0)

    if not approved:
        return {
            'error': (
                f'No approved claims found in {review_path}. '
                'Check [x] next to claims you want to approve, then re-run.'
            )
        }

    # 2. Write approved claims
    writer = VerifiedResearchWriter()
    write_result = writer.write_claims(
        claims=approved,
        verified_research_path=verified_research_path,
    )

    if 'error' in write_result:
        return write_result

    return {
        'written': write_result['written'],
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'sections_updated': write_result['sections_updated'],
        'path': write_result['path'],
    }
