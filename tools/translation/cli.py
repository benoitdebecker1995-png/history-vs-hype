"""
Translation Pipeline CLI

Unified command-line interface for document translation pipeline.

After refactor (Phase 42.1), this CLI is split into two tiers:

STANDALONE (no API key, no LLM):
    python tools/translation/cli.py detect --file document.txt
    python tools/translation/cli.py detect "Article 1\nText here"
    cat document.txt | python tools/translation/cli.py detect -
    python tools/translation/cli.py smoketest

REPLACED BY /translate SLASH COMMAND (requires Claude Code):
    translate   -> Use: /translate [project] --file [document] --language [language]
    crosscheck  -> Use: /translate [project] (included in step 3 of /translate)
    annotate    -> Use: /translate [project] (included in step 4 of /translate)
    surprise    -> Use: /translate [project] --narrative "..." (step 5 of /translate)

Subcommands:
    detect      - Detect document structure (pure Python, works standalone)
    smoketest   - Pipeline health check (pure Python, no credentials needed)
    translate   - REDIRECTS to /translate slash command
    crosscheck  - REDIRECTS to /translate slash command
    annotate    - REDIRECTS to /translate slash command
    surprise    - REDIRECTS to /translate slash command
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

from .structure_detector import StructureDetector
from .formatter import Formatter
from .smoke_test import run_smoke_test


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
    """Detect document structure (pure Python, works without API key)."""
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
    """Redirect to /translate slash command."""
    print("ERROR: The 'translate' subcommand has been replaced by the /translate slash command.")
    print("Run: /translate [project] --file [document] --language [language]")
    print("This provides the same functionality through Claude Code's native LLM integration.")
    print("No API key needed — Claude Code handles all LLM calls natively.")
    sys.exit(1)


def cmd_crosscheck(args):
    """Redirect to /translate slash command."""
    print("ERROR: The 'crosscheck' subcommand has been replaced by the /translate slash command.")
    print("Cross-checking is integrated into Step 3 of /translate.")
    print("Run: /translate [project] --file [document] --language [language]")
    print("This provides the same functionality through Claude Code's native LLM integration.")
    sys.exit(1)


def cmd_annotate(args):
    """Redirect to /translate slash command."""
    print("ERROR: The 'annotate' subcommand has been replaced by the /translate slash command.")
    print("Legal annotation is integrated into Step 4 of /translate.")
    print("Run: /translate [project] --file [document] --language [language]")
    print("This provides the same functionality through Claude Code's native LLM integration.")
    sys.exit(1)


def cmd_surprise(args):
    """Redirect to /translate slash command."""
    print("ERROR: The 'surprise' subcommand has been replaced by the /translate slash command.")
    print("Surprise detection is integrated into Step 5 of /translate (use --narrative flag).")
    print("Run: /translate [project] --file [document] --language [language] --narrative \"expected narrative\"")
    print("This provides the same functionality through Claude Code's native LLM integration.")
    sys.exit(1)


def cmd_smoketest(args):
    """Run end-to-end pipeline smoke test (pure Python, no API key needed)."""
    return run_smoke_test()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Translation Pipeline CLI\n\nStandalone commands: detect, smoketest\nLLM commands (use /translate instead): translate, crosscheck, annotate, surprise',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # detect subcommand (standalone, pure Python)
    detect_parser = subparsers.add_parser('detect', help='Detect document structure (works without API key)')
    detect_parser.add_argument('text', nargs='?', help='Document text or "-" for stdin')
    detect_parser.add_argument('--file', help='Read from file')
    detect_parser.add_argument('--type', help='Override document type (legal_code, treaty, decree, book, letter, other)')
    detect_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # translate subcommand (redirects to /translate)
    translate_parser = subparsers.add_parser('translate', help='REPLACED: Use /translate slash command instead')
    translate_parser.add_argument('text', nargs='?', help='(ignored)')
    translate_parser.add_argument('--file', help='(ignored)')
    translate_parser.add_argument('--language', help='(ignored)')

    # crosscheck subcommand (redirects to /translate)
    crosscheck_parser = subparsers.add_parser('crosscheck', help='REPLACED: Use /translate slash command instead (step 3)')
    crosscheck_parser.add_argument('--file', help='(ignored)')
    crosscheck_parser.add_argument('--language', help='(ignored)')

    # annotate subcommand (redirects to /translate)
    annotate_parser = subparsers.add_parser('annotate', help='REPLACED: Use /translate slash command instead (step 4)')
    annotate_parser.add_argument('--file', help='(ignored)')
    annotate_parser.add_argument('--language', help='(ignored)')
    annotate_parser.add_argument('--context', help='(ignored)')

    # surprise subcommand (redirects to /translate)
    surprise_parser = subparsers.add_parser('surprise', help='REPLACED: Use /translate --narrative instead (step 5)')
    surprise_parser.add_argument('--file', help='(ignored)')
    surprise_parser.add_argument('--language', help='(ignored)')
    surprise_parser.add_argument('--narrative', help='(ignored)')
    surprise_parser.add_argument('--narrative-file', help='(ignored)')
    surprise_parser.add_argument('--context', help='(ignored)')

    # smoketest subcommand (standalone, pure Python)
    subparsers.add_parser(
        'smoketest',
        help='Pipeline health check (no API key needed)'
    )

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
    elif args.command == 'smoketest':
        return cmd_smoketest(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
