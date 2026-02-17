"""
Document Discovery CLI

Unified command-line interface for translation gap checking, document structure assessment,
and archive lookup.

Usage:
    python tools/document_discovery/cli.py gap "Statut des Juifs 1940"
    python tools/document_discovery/cli.py structure "Document name" --type legal_code --sections 10
    python tools/document_discovery/cli.py archive "Document name" --language french
    python tools/document_discovery/cli.py gap "query" --json

Subcommands:
    gap      - Check for translation gaps (DISC-01)
    structure - Assess document structure and estimate video length (DISC-02)
    archive  - Locate digitized originals across archives (DISC-03)

All commands support --json flag for machine-readable output.
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from gap_checker import GapChecker
from structure_assessor import StructureAssessor
from archive_lookup import ArchiveLookup


def format_markdown_gap(result: dict) -> str:
    """Format gap check result as markdown."""
    if 'error' in result:
        return f"ERROR: {result['error']}"

    lines = []
    lines.append(f"# Translation Gap Check: {result['query']}\n")

    lines.append("## Qualification Criteria\n")
    lines.append(result['qualification_criteria'])
    lines.append("")

    lines.append("## Search URLs by Category\n")

    current_category = None
    for search in result['searches']:
        if search['category'] != current_category:
            current_category = search['category']
            lines.append(f"\n### {current_category}\n")

        lines.append(f"**{search['description']}**")
        lines.append(f"{search['search_url']}")
        lines.append("")

    lines.append("## Instructions\n")
    lines.append(result['instructions'])
    lines.append("")

    return "\n".join(lines)


def format_markdown_structure(result: dict) -> str:
    """Format structure assessment result as markdown."""
    if 'error' in result:
        return f"ERROR: {result['error']}"

    lines = []
    lines.append(f"# Document Structure Assessment: {result['document_name']}\n")

    lines.append("## Document Information\n")
    lines.append(f"**Type:** {result['document_type']}")
    lines.append(f"**Section Count:** {result['section_count']}")
    lines.append(f"**Structure Template:** {result['structure_template']}")
    lines.append("")

    lines.append("## Video Length Estimates\n")

    lines.append("### Full Document Coverage")
    full_est = result['length_estimate_full']
    lines.append(f"**Total:** {full_est['estimated_minutes']} minutes")
    lines.append(f"- Intro: {full_est['breakdown']['intro']} min")
    lines.append(f"- Content: {full_est['breakdown']['content']} min")
    lines.append(f"- Conclusion: {full_est['breakdown']['conclusion']} min")
    lines.append("")

    lines.append("### Excerpt Coverage (User-Selected Sections)")
    excerpt_est = result['length_estimate_excerpt']
    lines.append(f"**Per Section:** {excerpt_est['per_section_minutes']} minutes")
    lines.append(f"- {excerpt_est['note']}")
    lines.append("")

    lines.append("## Scope Options\n")
    lines.append(result['scope_options'])
    lines.append("")

    lines.append("---\n")
    lines.append(result['outline'])

    return "\n".join(lines)


def format_markdown_archive(result: dict) -> str:
    """Format archive lookup result as markdown."""
    if 'error' in result:
        return f"ERROR: {result['error']}"

    lines = []
    lines.append(f"# Archive Lookup: {result['query']}\n")

    lines.append("## Priority Note\n")
    lines.append(result['priority_note'])
    lines.append("")

    lines.append(f"## Archives ({result['language']})\n")

    current_category = None
    for archive in result['archives']:
        if archive['category'] != current_category:
            current_category = archive['category']
            lines.append(f"\n### {current_category}\n")

        lines.append(f"**{archive['name']}**")
        lines.append(f"{archive['description']}")
        lines.append(f"{archive['search_url']}")
        lines.append("")

    return "\n".join(lines)


def cmd_gap(args):
    """Execute gap check command."""
    gc = GapChecker()
    result = gc.check_gap(args.query)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_markdown_gap(result))

    # Exit code: 0 on success, 1 on error
    return 0 if 'error' not in result else 1


def cmd_structure(args):
    """Execute structure assessment command."""
    sa = StructureAssessor()

    # Parse section names if provided
    section_names = None
    if args.section_names:
        section_names = args.section_names.split(',')

    result = sa.assess(
        document_name=args.query,
        description=args.description,
        document_type=args.type,
        section_count=args.sections,
        section_names=section_names
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_markdown_structure(result))

    return 0 if 'error' not in result else 1


def cmd_archive(args):
    """Execute archive lookup command."""
    al = ArchiveLookup()
    result = al.lookup(args.query, language=args.language)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_markdown_archive(result))

    return 0 if 'error' not in result else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Document Discovery Toolkit - Translation gaps, structure, and archives',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check for translation gaps
  python tools/document_discovery/cli.py gap "Statut des Juifs 1940"

  # Assess legal document structure
  python tools/document_discovery/cli.py structure "Statut des Juifs 1940" --type legal_code --sections 10

  # Assess book structure
  python tools/document_discovery/cli.py structure "Brevisima relacion" --type book --sections 16

  # Excerpt-based estimation
  python tools/document_discovery/cli.py structure "Document" --type treaty --sections 29 --scope excerpt

  # Find archives
  python tools/document_discovery/cli.py archive "Statut des Juifs 1940" --language french

  # JSON output
  python tools/document_discovery/cli.py gap "query" --json
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Gap checker subcommand
    parser_gap = subparsers.add_parser('gap', help='Check for translation gaps')
    parser_gap.add_argument('query', help='Document description (e.g., "Statut des Juifs 1940")')
    parser_gap.add_argument('--json', action='store_true', help='Output as JSON')

    # Structure assessor subcommand
    parser_structure = subparsers.add_parser('structure', help='Assess document structure')
    parser_structure.add_argument('query', help='Document name')
    parser_structure.add_argument('--description', help='Optional description or location info')
    parser_structure.add_argument('--type', default='other',
                                 choices=['legal_code', 'treaty', 'book', 'letter', 'decree', 'other'],
                                 help='Document type (default: other)')
    parser_structure.add_argument('--sections', type=int, default=1,
                                 help='Number of sections/articles/chapters (default: 1)')
    parser_structure.add_argument('--section-names', help='Comma-separated section names')
    parser_structure.add_argument('--json', action='store_true', help='Output as JSON')

    # Archive lookup subcommand
    parser_archive = subparsers.add_parser('archive', help='Locate digitized originals')
    parser_archive.add_argument('query', help='Document description')
    parser_archive.add_argument('--language', help='Language hint (french, spanish, german, latin, etc.)')
    parser_archive.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate handler
    if args.command == 'gap':
        return cmd_gap(args)
    elif args.command == 'structure':
        return cmd_structure(args)
    elif args.command == 'archive':
        return cmd_archive(args)


if __name__ == '__main__':
    sys.exit(main())
