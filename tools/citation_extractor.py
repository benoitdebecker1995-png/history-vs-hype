#!/usr/bin/env python3
"""
NotebookLM Citation Extractor

Parses NotebookLM chat output and extracts citations into VERIFIED-RESEARCH.md-compatible format.
Replaces the Phase 14 PowerShell script with a cross-platform Python tool.

Usage:
    python citation_extractor.py INPUT_FILE [--output FILE] [--format detailed|compact] [--stats-only]
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def parse_citations(content: str) -> List[Dict]:
    """
    Parse NotebookLM output and extract citations.

    Supports multiple citation formats:
    - Pattern A: [1] markers with source legend at bottom (most common)
    - Pattern B: SOURCES: section with numbered list
    - Pattern C: Inline parenthetical citations

    Returns:
        List of dicts with keys: claim, source, page, citation_num, status
    """
    citations = []

    # Extract claims with [N] markers
    # Pattern handles both: "claim text [1]." and "claim text. [1]"
    claim_pattern = re.compile(r'([^.!?\n]+?)\s*\[(\d+)\][.!?]?')
    claims = {}
    for match in claim_pattern.finditer(content):
        claim_text = match.group(1).strip()
        citation_num = match.group(2)
        if citation_num not in claims:
            claims[citation_num] = []
        claims[citation_num].append(claim_text)

    # Pattern A: Source legend at bottom
    # Format: [1] Author, Book Title, p. 45
    # or: [1] Author, Book Title, page 45
    # or: [1] Author, Book Title, pp. 45-46
    legend_pattern = re.compile(
        r'\[(\d+)\]\s+([^,]+),\s+"?([^,"]+)"?,?\s+(?:p\.?|page|pp\.?)\s*(\d+(?:-\d+)?)',
        re.IGNORECASE
    )

    sources = {}
    for match in legend_pattern.finditer(content):
        citation_num = match.group(1)
        author = match.group(2).strip()
        title = match.group(3).strip()
        page = match.group(4).strip()
        sources[citation_num] = {
            'author': author,
            'title': title,
            'page': page
        }

    # If Pattern A found sources, combine with claims
    if sources:
        for citation_num, claim_list in claims.items():
            if citation_num in sources:
                source_info = sources[citation_num]
                for claim_text in claim_list:
                    citations.append({
                        'claim': claim_text,
                        'source': f"{source_info['author']}, {source_info['title']}",
                        'page': source_info['page'],
                        'citation_num': citation_num,
                        'status': 'NEEDS REVIEW'
                    })

    # Pattern B: SOURCES: section with numbered list
    # Format: 1. Author, "Book Title" (Year), p. 45
    # or: 1. Author, "Book Title", p. 45
    if not citations:
        sources_section = re.search(
            r'SOURCES?:?\s*\n((?:\d+\.\s+.+\n?)+)',
            content,
            re.IGNORECASE | re.MULTILINE
        )

        if sources_section:
            sources_text = sources_section.group(1)
            # Pattern: N. Author Name. "Book Title" (year), p. XX
            # Author goes up to period before quote, title in quotes, page after p./pp./page
            source_pattern = re.compile(
                r'(\d+)\.\s+(.+?)\.\s+"([^"]+)".*?(?:p\.?|pp\.?|page)\s*(\d+(?:-\d+)?)',
                re.IGNORECASE
            )

            sources_b = {}
            for match in source_pattern.finditer(sources_text):
                citation_num = match.group(1)
                author = match.group(2).strip()
                title = match.group(3).strip()
                page = match.group(4).strip()
                sources_b[citation_num] = {
                    'author': author,
                    'title': title,
                    'page': page
                }

            # Combine with claims
            for citation_num, claim_list in claims.items():
                if citation_num in sources_b:
                    source_info = sources_b[citation_num]
                    for claim_text in claim_list:
                        citations.append({
                            'claim': claim_text,
                            'source': f"{source_info['author']}, {source_info['title']}",
                            'page': source_info['page'],
                            'citation_num': citation_num,
                            'status': 'NEEDS REVIEW'
                        })

    # Pattern C: Inline parenthetical citations
    # Format: Some claim text (Author, Year, p. 45).
    if not citations:
        inline_pattern = re.compile(
            r'([^.!?\n]+)\s*\(([^,]+),\s*\d{4},\s*(?:p\.?|page)\s*(\d+(?:-\d+)?)\)',
            re.IGNORECASE
        )

        for match in inline_pattern.finditer(content):
            claim_text = match.group(1).strip()
            author = match.group(2).strip()
            page = match.group(3).strip()

            citations.append({
                'claim': claim_text,
                'source': author,
                'page': page,
                'citation_num': 'inline',
                'status': 'NEEDS REVIEW'
            })

    return citations


def extract_citations(input_path: str) -> Dict[str, Any]:
    """
    Read input file and extract citations.

    Returns:
        Dict with status, citations, count, and warnings on success
        Dict with error on failure
    """
    try:
        path = Path(input_path)

        # File not found check
        if not path.exists():
            return {'error': f'File not found: {input_path}'}

        # Read file with UTF-8, fallback to latin-1
        content = ''
        encoding_used = 'utf-8'
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding='latin-1')
                encoding_used = 'latin-1'
            except Exception as e:
                return {'error': f'Failed to read file: {e}'}

        # Empty file check
        if not content.strip():
            return {'error': 'Input file is empty'}

        # Parse citations
        citations = parse_citations(content)

        # No citations found check
        if not citations:
            return {'error': 'No citations found. Check that the file contains NotebookLM output with [1], [2] citation markers or a SOURCES: section.'}

        # Collect warnings
        warnings = []
        if encoding_used != 'utf-8':
            warnings.append(f'Used {encoding_used} encoding (UTF-8 failed)')

        # Check for unreferenced sources or missing sources
        citation_nums = {c['citation_num'] for c in citations if c['citation_num'] != 'inline'}

        return {
            'status': 'success',
            'citations': citations,
            'count': len(citations),
            'warnings': warnings
        }

    except Exception as e:
        return {'error': f'Unexpected error: {e}'}


def write_extractions(citations: list, output_path: Path, input_filename: str):
    """Write extractions to markdown file in VERIFIED-RESEARCH.md format."""

    # Build header
    header = f"""# NotebookLM Citation Extractions

**Extracted from:** {input_filename}
**Extraction date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total claims extracted:** {len(citations)}

---

## Instructions

1. Review each extracted claim
2. Verify claim accuracy against the original source
3. Confirm page numbers are correct
4. Update status: VERIFIED / UNVERIFIABLE / PARTIALLY TRUE
5. Copy verified claims to `01-VERIFIED-RESEARCH.md`

---

"""

    # Build claim sections
    claims_text = ""
    for i, citation in enumerate(citations, 1):
        claims_text += f"""### Claim {i}

**Claim:** {citation['claim']}
**Source:** {citation['source']}, p. {citation['page']}
**Status:** {citation['status']}

**Verification:**
- [ ] Verify claim accuracy against source
- [ ] Confirm page number
- [ ] Update status: VERIFIED / UNVERIFIABLE / PARTIALLY TRUE
- [ ] Copy to 01-VERIFIED-RESEARCH.md when verified

---

"""

    # Write to file
    output_path.write_text(header + claims_text, encoding='utf-8')


def write_extractions_compact(citations: list, output_path: Path, input_filename: str):
    """Write extractions in compact table format."""

    header = f"""# NotebookLM Citation Extractions (Compact)

**Extracted from:** {input_filename}
**Extraction date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total claims extracted:** {len(citations)}

---

| # | Claim | Source | Page | Status |
|---|-------|--------|------|--------|
"""

    rows = ""
    for i, citation in enumerate(citations, 1):
        claim = citation['claim'][:80] + '...' if len(citation['claim']) > 80 else citation['claim']
        rows += f"| {i} | {claim} | {citation['source']} | {citation['page']} | {citation['status']} |\n"

    output_path.write_text(header + rows, encoding='utf-8')


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Extract citations from NotebookLM chat output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python citation_extractor.py nlm-output.txt
  python citation_extractor.py nlm-output.txt --output extractions.md
  python citation_extractor.py nlm-output.txt --format compact
  python citation_extractor.py nlm-output.txt --stats-only
        """
    )

    parser.add_argument(
        'input',
        help='Path to file with pasted NotebookLM output'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: NOTEBOOKLM-EXTRACTIONS.md in same directory as input)'
    )
    parser.add_argument(
        '--format',
        choices=['detailed', 'compact'],
        default='detailed',
        help='Output format: detailed (full checklist) or compact (table)'
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Print extraction statistics without writing file'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Extract citations
    result = extract_citations(args.input)

    # Handle errors
    if 'error' in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Print stats
    citations = result['citations']
    print(f"Extracted {result['count']} citations from {args.input}")

    # Print warnings
    if result['warnings']:
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    # Stats only mode
    if args.stats_only:
        sources = {c['source'] for c in citations}
        print(f"Unique sources: {len(sources)}")
        return

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        input_path = Path(args.input)
        output_path = input_path.parent / 'NOTEBOOKLM-EXTRACTIONS.md'

    # Write extractions
    if args.format == 'compact':
        write_extractions_compact(citations, output_path, Path(args.input).name)
    else:
        write_extractions(citations, output_path, Path(args.input).name)

    print(f"\nExtractions written to: {output_path}")
    print("\nNext steps:")
    print("1. Review each claim in the extractions file")
    print("2. Verify against original sources")
    print("3. Copy verified claims to 01-VERIFIED-RESEARCH.md")


if __name__ == '__main__':
    main()
