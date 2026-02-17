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
from cross_checker import CrossChecker
from legal_annotator import LegalAnnotator
from surprise_detector import SurpriseDetector


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
    """Cross-check translation against independent sources."""
    # Read translated JSON input
    if not args.file:
        print("ERROR: --file required (path to translated JSON output)", file=sys.stderr)
        return 1

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            translation_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Translation file not found: {args.file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in translation file: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read translation file: {str(e)}", file=sys.stderr)
        return 1

    # Extract sections from translation data
    sections = translation_data.get('sections', [])
    if not sections:
        print("ERROR: No sections found in translation file", file=sys.stderr)
        return 1

    # Validate language
    if not args.language:
        print("ERROR: --language required (e.g., french, spanish, german)", file=sys.stderr)
        return 1

    # Initialize cross-checker
    checker = CrossChecker()

    if checker.error:
        print(f"ERROR: CrossChecker initialization failed: {checker.error}", file=sys.stderr)
        return 1

    # Progress callback
    def on_progress(current, total, clause_id):
        print(f"Cross-checking clause {current}/{total}... ({clause_id})", file=sys.stderr)

    # Run cross-check
    print(f"Cross-checking {len(sections)} clauses...", file=sys.stderr)

    results = checker.check_document(
        sections=sections,
        source_language=args.language,
        on_progress=on_progress
    )

    if 'error' in results:
        if results.get('skipped', False):
            # Backend unavailable - not a fatal error, just inform
            print(f"WARNING: {results['error']}", file=sys.stderr)
            return 0
        else:
            print(f"ERROR: Cross-check failed: {results['error']}", file=sys.stderr)
            return 1

    # Format output
    if args.json:
        # JSON output
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # Markdown report
        report = checker.format_report(results)
        print(report)

    summary = results['summary']
    print(f"\nCross-check complete. {summary['discrepancies_found']} discrepancies found.", file=sys.stderr)
    return 0


def cmd_annotate(args):
    """Annotate legal/technical terms."""
    # Read translated JSON input
    if not args.file:
        print("ERROR: --file required (path to translated JSON output)", file=sys.stderr)
        return 1

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            translation_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Translation file not found: {args.file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in translation file: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read translation file: {str(e)}", file=sys.stderr)
        return 1

    # Extract sections from translation data
    sections = translation_data.get('sections', [])
    if not sections:
        print("ERROR: No sections found in translation file", file=sys.stderr)
        return 1

    # Validate language
    if not args.language:
        print("ERROR: --language required (e.g., french, spanish, german)", file=sys.stderr)
        return 1

    # Initialize annotator
    annotator = LegalAnnotator()

    if annotator.error:
        print(f"ERROR: LegalAnnotator initialization failed: {annotator.error}", file=sys.stderr)
        return 1

    # Progress callback
    def on_progress(current, total, clause_id):
        print(f"Annotating clause {current}/{total}... ({clause_id})", file=sys.stderr)

    # Run annotation
    print(f"Annotating {len(sections)} clauses...", file=sys.stderr)

    results = annotator.annotate_document(
        sections=sections,
        source_language=args.language,
        document_context=args.context,
        on_progress=on_progress
    )

    if 'error' in results:
        print(f"ERROR: Annotation failed: {results['error']}", file=sys.stderr)
        return 1

    # Format output
    if args.json:
        # JSON output
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # Markdown report with footnotes
        report = "# Legal Term Annotations\n\n"
        report += f"**Total Annotations:** {results['total_annotations']}\n"
        report += f"**Mistranslation Flags:** {results['mistranslation_flags']}\n\n"

        for section in results['sections']:
            report += f"## {section.get('heading', section.get('id', 'Unknown'))}\n\n"

            # Show translation
            report += "### Translation\n"
            report += f"{section.get('translation', 'N/A')}\n\n"

            # Show footnotes
            if section.get('footnotes'):
                report += "### Annotations\n\n"
                for i, footnote in enumerate(section['footnotes'], 1):
                    report += f"{i}. {footnote}\n\n"

        print(report)

    print(f"\nAnnotation complete. {results['total_annotations']} terms annotated.", file=sys.stderr)
    return 0


def cmd_full(args):
    """Complete translation pipeline: detect + translate + crosscheck + annotate + surprise."""
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
    print("Step 1/5: Detecting structure...", file=sys.stderr)
    detector = StructureDetector()
    structure = detector.detect_structure(text, args.type)

    if 'error' in structure:
        print(f"ERROR: Structure detection failed: {structure['error']}", file=sys.stderr)
        return 1

    print(f"  Detected {structure['section_count']} sections", file=sys.stderr)

    # Dry run - show plan without executing
    if args.dry_run:
        print("\n# Full Pipeline Plan (Dry Run)\n", file=sys.stderr)
        print(f"**Source Language:** {args.language}", file=sys.stderr)
        print(f"**Detected Type:** {structure['detected_type']}", file=sys.stderr)
        print(f"**Section Count:** {structure['section_count']}\n", file=sys.stderr)

        print("## Pipeline Steps:\n", file=sys.stderr)
        print(f"1. Translate: {structure['section_count']} API calls (Claude)", file=sys.stderr)

        if not args.skip_crosscheck:
            print(f"2. Cross-check: {structure['section_count']} comparisons (DeepL/Google)", file=sys.stderr)
        else:
            print("2. Cross-check: SKIPPED", file=sys.stderr)

        if not args.skip_annotate:
            print(f"3. Annotate: {structure['section_count']} legal term analyses (Claude)", file=sys.stderr)
        else:
            print("3. Annotate: SKIPPED", file=sys.stderr)

        if not args.skip_surprise and (args.narrative or args.narrative_file):
            print(f"4. Surprise: {structure['section_count']} clause analyses (Claude)", file=sys.stderr)
        else:
            print("4. Surprise: SKIPPED", file=sys.stderr)

        print("5. Format: Split-screen markdown output", file=sys.stderr)

        print("\nTo proceed, remove --dry-run flag", file=sys.stderr)
        return 0

    # Step 2: Translate
    print("\nStep 2/5: Translating...", file=sys.stderr)
    translator = Translator()

    if translator.error:
        print(f"ERROR: Translator initialization failed: {translator.error}", file=sys.stderr)
        return 1

    def on_translate_progress(current, total, clause_id):
        print(f"  Translating clause {current}/{total}... ({clause_id})", file=sys.stderr)

    translation_result = translator.translate_document(
        sections=structure['sections'],
        source_language=args.language,
        full_text=text,
        document_context=args.context,
        on_progress=on_translate_progress
    )

    if 'error' in translation_result:
        print(f"ERROR: Translation failed: {translation_result['error']}", file=sys.stderr)
        return 1

    print(f"  Translation complete ({translation_result['clause_count']} clauses)", file=sys.stderr)

    # Step 3: Cross-check (optional)
    crosscheck_results = None
    if not args.skip_crosscheck:
        print("\nStep 3/5: Cross-checking...", file=sys.stderr)
        checker = CrossChecker()

        if checker.error:
            print(f"WARNING: CrossChecker initialization failed: {checker.error}", file=sys.stderr)
            print("  Skipping cross-check step", file=sys.stderr)
        else:
            def on_check_progress(current, total, clause_id):
                print(f"  Checking clause {current}/{total}... ({clause_id})", file=sys.stderr)

            crosscheck_results = checker.check_document(
                sections=translation_result['sections'],
                source_language=args.language,
                on_progress=on_check_progress
            )

            if 'error' in crosscheck_results:
                if crosscheck_results.get('skipped', False):
                    print(f"WARNING: {crosscheck_results['error']}", file=sys.stderr)
                    print("  Skipping cross-check step", file=sys.stderr)
                    crosscheck_results = None
                else:
                    print(f"ERROR: Cross-check failed: {crosscheck_results['error']}", file=sys.stderr)
                    return 1
            else:
                summary = crosscheck_results['summary']
                print(f"  Cross-check complete ({summary['discrepancies_found']} discrepancies)", file=sys.stderr)
    else:
        print("\nStep 3/5: Cross-checking SKIPPED", file=sys.stderr)

    # Step 4: Annotate (optional)
    annotation_results = None
    if not args.skip_annotate:
        print("\nStep 4/5: Annotating legal terms...", file=sys.stderr)
        annotator = LegalAnnotator()

        if annotator.error:
            print(f"WARNING: LegalAnnotator initialization failed: {annotator.error}", file=sys.stderr)
            print("  Skipping annotation step", file=sys.stderr)
        else:
            def on_annotate_progress(current, total, clause_id):
                print(f"  Annotating clause {current}/{total}... ({clause_id})", file=sys.stderr)

            annotation_results = annotator.annotate_document(
                sections=translation_result['sections'],
                source_language=args.language,
                document_context=args.context,
                on_progress=on_annotate_progress
            )

            if 'error' in annotation_results:
                print(f"ERROR: Annotation failed: {annotation_results['error']}", file=sys.stderr)
                return 1

            print(f"  Annotation complete ({annotation_results['total_annotations']} terms)", file=sys.stderr)
    else:
        print("\nStep 4/5: Annotation SKIPPED", file=sys.stderr)

    # Step 5: Surprise detection (optional)
    surprise_results = None
    if not args.skip_surprise:
        # Check for narrative
        narrative = None
        if args.narrative and args.narrative_file:
            print("ERROR: Cannot specify both --narrative and --narrative-file", file=sys.stderr)
            return 1
        elif args.narrative:
            narrative = args.narrative
        elif args.narrative_file:
            try:
                with open(args.narrative_file, 'r', encoding='utf-8') as f:
                    narrative = f.read().strip()
            except Exception as e:
                print(f"ERROR: Failed to read narrative file: {str(e)}", file=sys.stderr)
                return 1

        if narrative:
            print("\nStep 5/5: Detecting surprise clauses...", file=sys.stderr)
            detector_obj = SurpriseDetector()

            if detector_obj.error:
                print(f"WARNING: SurpriseDetector initialization failed: {detector_obj.error}", file=sys.stderr)
                print("  Skipping surprise detection step", file=sys.stderr)
            else:
                def on_surprise_progress(current, total, clause_id):
                    print(f"  Analyzing clause {current}/{total}... ({clause_id})", file=sys.stderr)

                # Use annotated sections if available, otherwise use translated sections
                sections_for_surprise = annotation_results['sections'] if annotation_results else translation_result['sections']

                surprise_results = detector_obj.detect_surprises(
                    sections=sections_for_surprise,
                    narrative=narrative,
                    source_language=args.language,
                    document_context=args.context,
                    on_progress=on_surprise_progress
                )

                if 'error' in surprise_results:
                    print(f"ERROR: Surprise detection failed: {surprise_results['error']}", file=sys.stderr)
                    return 1

                print(f"  Surprise detection complete ({surprise_results['surprise_count']} surprises)", file=sys.stderr)
        else:
            print("\nStep 5/5: Surprise detection SKIPPED (no --narrative provided)", file=sys.stderr)
    else:
        print("\nStep 5/5: Surprise detection SKIPPED", file=sys.stderr)

    # Format output
    print("\nFormatting output...", file=sys.stderr)
    formatter = Formatter()

    # Merge surprise data into sections if available
    sections_to_format = annotation_results['sections'] if annotation_results else translation_result['sections']

    if surprise_results:
        detector_obj = SurpriseDetector()
        sections_to_format = detector_obj.update_sections_with_surprises(
            sections_to_format,
            surprise_results['surprises']
        )

    # Format with surprise markers
    output_lines = []
    for section in sections_to_format:
        # Section heading
        heading = section.get('heading', section.get('id', 'Unknown'))
        output_lines.append(f"## {heading}\n")

        # Original
        output_lines.append("### Original")
        output_lines.append(f"> {section.get('original', '')}\n")

        # Translation
        output_lines.append("### Translation")
        output_lines.append(f"{section.get('translation', '')}\n")

        # Surprise marker (if present)
        surprise = section.get('surprise')
        if surprise and surprise.get('severity'):
            severity = surprise['severity'].upper()
            script_beat = surprise.get('script_beat', '')
            output_lines.append(f"> **SURPRISE ({severity}):** {script_beat}\n")

        # Notes (if present)
        notes = section.get('notes', [])
        if notes and any(notes):
            output_lines.append("**Notes:**")
            for i, note in enumerate(notes, 1):
                if note and note.strip():
                    output_lines.append(f"{i}. {note}")
            output_lines.append("")

        # Annotations (if present)
        annotations = section.get('annotations', [])
        if annotations:
            output_lines.append("**Legal Terms:**")
            for i, ann in enumerate(annotations, 1):
                term = ann.get('term', '')
                definition = ann.get('definition', '')
                output_lines.append(f"{i}. **{term}**: {definition}")
            output_lines.append("")

        output_lines.append("---\n")

    output = '\n'.join(output_lines)

    # Append cross-check report if available
    if crosscheck_results:
        output += "\n\n---\n\n"
        output += checker.format_report(crosscheck_results)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\nPipeline complete. Output written to: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: Failed to write output file: {str(e)}", file=sys.stderr)
            return 1
    else:
        # Print to stdout
        print(output)

    # Summary
    print("\n=== Pipeline Summary ===", file=sys.stderr)
    print(f"Translated: {translation_result['clause_count']} clauses", file=sys.stderr)
    if crosscheck_results:
        summary = crosscheck_results['summary']
        print(f"Cross-checked: {summary['discrepancies_found']} discrepancies found", file=sys.stderr)
    if annotation_results:
        print(f"Annotated: {annotation_results['total_annotations']} legal terms", file=sys.stderr)
    if surprise_results:
        print(f"Surprises: {surprise_results['surprise_count']} found ({surprise_results['by_severity']['major']} major, {surprise_results['by_severity']['notable']} notable, {surprise_results['by_severity']['minor']} minor)", file=sys.stderr)

    return 0


def cmd_surprise(args):
    """Run surprise clause detection on translated output."""
    # Validate narrative input
    narrative = None
    if args.narrative and args.narrative_file:
        print("ERROR: Cannot specify both --narrative and --narrative-file", file=sys.stderr)
        return 1
    elif args.narrative:
        narrative = args.narrative
    elif args.narrative_file:
        try:
            with open(args.narrative_file, 'r', encoding='utf-8') as f:
                narrative = f.read().strip()
        except FileNotFoundError:
            print(f"ERROR: Narrative file not found: {args.narrative_file}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"ERROR: Failed to read narrative file: {str(e)}", file=sys.stderr)
            return 1
    else:
        print("ERROR: Either --narrative or --narrative-file required", file=sys.stderr)
        return 1

    if not narrative:
        print("ERROR: Narrative cannot be empty", file=sys.stderr)
        return 1

    # Read translated JSON input
    if not args.file:
        print("ERROR: --file required (path to translated JSON output)", file=sys.stderr)
        return 1

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            translation_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Translation file not found: {args.file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in translation file: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read translation file: {str(e)}", file=sys.stderr)
        return 1

    # Extract sections from translation data
    sections = translation_data.get('sections', [])
    if not sections:
        print("ERROR: No sections found in translation file", file=sys.stderr)
        return 1

    # Validate language
    if not args.language:
        print("ERROR: --language required (e.g., french, spanish, german)", file=sys.stderr)
        return 1

    # Initialize detector
    detector = SurpriseDetector()

    if detector.error:
        print(f"ERROR: Detector initialization failed: {detector.error}", file=sys.stderr)
        return 1

    # Progress callback
    def on_progress(current, total, clause_id):
        print(f"Analyzing clause {current}/{total}... ({clause_id})", file=sys.stderr)

    # Run detection
    print(f"Analyzing {len(sections)} clauses against narrative...", file=sys.stderr)

    results = detector.detect_surprises(
        sections=sections,
        narrative=narrative,
        source_language=args.language,
        document_context=args.context,
        on_progress=on_progress
    )

    if 'error' in results:
        print(f"ERROR: Surprise detection failed: {results['error']}", file=sys.stderr)
        return 1

    # Format output
    if args.json:
        # JSON output
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # Markdown report
        report = detector.format_report(results)
        print(report)

    print(f"\nAnalysis complete. {results['surprise_count']} surprises found.", file=sys.stderr)
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

    # crosscheck subcommand
    crosscheck_parser = subparsers.add_parser('crosscheck', help='Cross-check translation against independent sources')
    crosscheck_parser.add_argument('--file', required=True, help='Translated JSON file (from translate --format json)')
    crosscheck_parser.add_argument('--language', required=True, help='Source language (french, spanish, german, etc.)')
    crosscheck_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # annotate subcommand
    annotate_parser = subparsers.add_parser('annotate', help='Annotate legal/technical terms')
    annotate_parser.add_argument('--file', required=True, help='Translated JSON file (from translate --format json)')
    annotate_parser.add_argument('--language', required=True, help='Source language (french, spanish, german, etc.)')
    annotate_parser.add_argument('--context', help='Optional document context for better annotation')
    annotate_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # surprise subcommand
    surprise_parser = subparsers.add_parser('surprise', help='Detect surprise clauses')
    surprise_parser.add_argument('--file', required=True, help='Translated JSON file (from translate --format json)')
    surprise_parser.add_argument('--language', required=True, help='Source language (french, spanish, german, etc.)')
    surprise_parser.add_argument('--narrative', help='Inline narrative baseline (what people commonly believe)')
    surprise_parser.add_argument('--narrative-file', help='Read narrative from file')
    surprise_parser.add_argument('--context', help='Optional document context')
    surprise_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # full pipeline subcommand
    full_parser = subparsers.add_parser('full', help='Complete pipeline (detect + translate + crosscheck + annotate + surprise)')
    full_parser.add_argument('text', nargs='?', help='Document text or "-" for stdin')
    full_parser.add_argument('--file', help='Read from file')
    full_parser.add_argument('--language', required=True, help='Source language (french, spanish, german, latin, etc.)')
    full_parser.add_argument('--type', help='Override document type')
    full_parser.add_argument('--context', help='Document context for better translation')
    full_parser.add_argument('--output', help='Write output to file (default: stdout)')
    full_parser.add_argument('--narrative', help='Narrative baseline for surprise detection')
    full_parser.add_argument('--narrative-file', help='Read narrative from file')
    full_parser.add_argument('--skip-crosscheck', action='store_true', help='Skip cross-checking step')
    full_parser.add_argument('--skip-annotate', action='store_true', help='Skip annotation step')
    full_parser.add_argument('--skip-surprise', action='store_true', help='Skip surprise detection step')
    full_parser.add_argument('--dry-run', action='store_true', help='Show plan without executing')

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
    elif args.command == 'full':
        return cmd_full(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
