"""
Translation Pipeline CLI

Unified command-line interface for document translation with structure detection,
Claude-based clause-by-clause translation, and split-screen formatted output.

Usage:
    python tools/translation/cli.py detect --file document.txt
    python tools/translation/cli.py detect "Article 1\nText here"
    cat document.txt | python tools/translation/cli.py detect -

    python tools/translation/cli.py translate --file doc.txt --language french
    python tools/translation/cli.py translate "text" --language spanish --context "1940 statute"
    cat doc.txt | python tools/translation/cli.py translate - --language french --output translation.md

Subcommands:
    detect      - Detect document structure (preview before translating)
    translate   - Full translation pipeline (detect + translate + format)
    crosscheck  - Cross-check translation (Plan 40-02)
    annotate    - Annotate legal terms (Plan 40-02)
    surprise    - Detect surprise clauses (Plan 40-03)
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from structure_detector import StructureDetector
from translator import Translator
from formatter import Formatter


def read_input(text_arg: Optional[str], file_path: Optional[str]) -> dict:
    """
    Read document text from stdin, file, or argument.

    Returns:
        {'text': str} on success
        {'error': msg} on failure
    """
    if text_arg == '-':
        # Read from stdin
        try:
            text = sys.stdin.read()
        except Exception as e:
            return {'error': f'Failed to read stdin: {str(e)}'}
    elif file_path:
        # Read from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            return {'error': f'File not found: {file_path}'}
        except Exception as e:
            return {'error': f'Failed to read file: {str(e)}'}
    elif text_arg:
        # Use text argument directly
        text = text_arg
    else:
        return {'error': 'No input provided. Use --file, stdin (-), or provide text as argument'}

    # Validate
    if not text or not text.strip():
        return {'error': 'Input text is empty'}

    if len(text.strip()) < 10:
        return {'error': 'Input text too short (< 10 characters)'}

    return {'text': text.strip()}


def cmd_detect(args):
    """Detect document structure."""
    # Read input
    input_result = read_input(args.text, args.file)
    if 'error' in input_result:
        print(f"ERROR: {input_result['error']}", file=sys.stderr)
        return 1

    text = input_result['text']

    # Detect structure
    detector = StructureDetector()
    result = detector.detect_structure(text, args.type)

    if 'error' in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        return 1

    # Output
    if args.json:
        # JSON output
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Markdown output
        print(f"# Document Structure Detection\n")
        print(f"**Detected Type:** {result['detected_type']}")
        print(f"**Document Type:** {result['document_type']}")
        print(f"**Section Count:** {result['section_count']}")
        print(f"**Has Preamble:** {result['has_preamble']}\n")

        print("## Sections Detected\n")
        for section in result['sections']:
            print(f"### {section['heading']}")
            print(f"- **ID:** {section['id']}")
            print(f"- **Lines:** {section['start_line']}-{section['end_line']}")
            body_preview = section['body'][:100] + '...' if len(section['body']) > 100 else section['body']
            print(f"- **Preview:** {body_preview}\n")

    return 0


def cmd_translate(args):
    """Full translation pipeline."""
    # Read input
    input_result = read_input(args.text, args.file)
    if 'error' in input_result:
        print(f"ERROR: {input_result['error']}", file=sys.stderr)
        return 1

    text = input_result['text']

    # Validate language
    if not args.language:
        print("ERROR: --language required (e.g., french, spanish, german, latin)", file=sys.stderr)
        return 1

    # Detect structure
    detector = StructureDetector()
    structure = detector.detect_structure(text, args.type)

    if 'error' in structure:
        print(f"ERROR: Structure detection failed: {structure['error']}", file=sys.stderr)
        return 1

    # Dry run - show plan without translating
    if args.dry_run:
        print("# Translation Plan (Dry Run)\n", file=sys.stderr)
        print(f"**Source Language:** {args.language}", file=sys.stderr)
        print(f"**Detected Type:** {structure['detected_type']}", file=sys.stderr)
        print(f"**Section Count:** {structure['section_count']}", file=sys.stderr)
        print(f"**Estimated API Calls:** {structure['section_count']}\n", file=sys.stderr)

        print("## Sections to Translate:\n", file=sys.stderr)
        for i, section in enumerate(structure['sections'], 1):
            print(f"{i}. {section['heading']} ({len(section['body'])} chars)", file=sys.stderr)

        print("\nTo proceed with translation, remove --dry-run flag", file=sys.stderr)
        return 0

    # Initialize translator
    translator = Translator()

    if translator.error:
        print(f"ERROR: Translator initialization failed: {translator.error}", file=sys.stderr)
        return 1

    # Progress callback
    def on_progress(current, total, clause_id):
        print(f"Translating clause {current}/{total}... ({clause_id})", file=sys.stderr)

    # Translate
    print(f"Starting translation of {structure['section_count']} sections...", file=sys.stderr)

    translation_result = translator.translate_document(
        sections=structure['sections'],
        source_language=args.language,
        full_text=text,
        document_context=args.context,
        on_progress=on_progress
    )

    if 'error' in translation_result:
        print(f"ERROR: Translation failed: {translation_result['error']}", file=sys.stderr)
        return 1

    # Format output
    formatter = Formatter()

    if args.format == 'json':
        # JSON output
        metadata = {
            'document_name': args.file or 'Untitled',
            'source_language': args.language,
            'model': translation_result['model'],
            'clause_count': translation_result['clause_count']
        }
        output = formatter.format_json(translation_result['sections'], metadata)
    else:
        # Markdown output (default)
        output = formatter.format_paired(translation_result['sections'], output_format='markdown')

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\nTranslation complete. Output written to: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: Failed to write output file: {str(e)}", file=sys.stderr)
            return 1
    else:
        # Print to stdout
        print(output)

    print(f"\nTranslation complete. {translation_result['clause_count']} clauses translated.", file=sys.stderr)
    return 0


def cmd_crosscheck(args):
    """Placeholder for Plan 40-02."""
    print("Cross-checking will be available after Plan 40-02 is complete.", file=sys.stderr)
    print("This feature will compare Claude translations against DeepL/Google Translate.", file=sys.stderr)
    return 0


def cmd_annotate(args):
    """Placeholder for Plan 40-02."""
    print("Legal term annotation will be available after Plan 40-02 is complete.", file=sys.stderr)
    print("This feature will annotate terms with no direct English equivalent.", file=sys.stderr)
    return 0


def cmd_surprise(args):
    """Placeholder for Plan 40-03."""
    print("Surprise clause detection will be available after Plan 40-03 is complete.", file=sys.stderr)
    print("This feature will identify clauses that contradict common narratives.", file=sys.stderr)
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Translation Pipeline - Document translation with structure detection',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # detect subcommand
    detect_parser = subparsers.add_parser('detect', help='Detect document structure')
    detect_parser.add_argument('text', nargs='?', help='Document text or "-" for stdin')
    detect_parser.add_argument('--file', help='Read from file')
    detect_parser.add_argument('--type', help='Override document type (legal_code, treaty, decree, book, letter, other)')
    detect_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # translate subcommand
    translate_parser = subparsers.add_parser('translate', help='Translate document')
    translate_parser.add_argument('text', nargs='?', help='Document text or "-" for stdin')
    translate_parser.add_argument('--file', help='Read from file')
    translate_parser.add_argument('--language', required=True, help='Source language (french, spanish, german, latin, etc.)')
    translate_parser.add_argument('--type', help='Override document type')
    translate_parser.add_argument('--context', help='Document context for better translation (e.g., "1940 French statute")')
    translate_parser.add_argument('--output', help='Write output to file (default: stdout)')
    translate_parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    translate_parser.add_argument('--dry-run', action='store_true', help='Show plan without translating')

    # Placeholder subcommands
    crosscheck_parser = subparsers.add_parser('crosscheck', help='Cross-check translation (Plan 40-02)')
    annotate_parser = subparsers.add_parser('annotate', help='Annotate legal terms (Plan 40-02)')
    surprise_parser = subparsers.add_parser('surprise', help='Detect surprise clauses (Plan 40-03)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command handler
    if args.command == 'detect':
        return cmd_detect(args)
    elif args.command == 'translate':
        return cmd_translate(args)
    elif args.command == 'crosscheck':
        return cmd_crosscheck(args)
    elif args.command == 'annotate':
        return cmd_annotate(args)
    elif args.command == 'surprise':
        return cmd_surprise(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
