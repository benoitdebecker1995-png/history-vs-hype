"""
Script Quality Checker CLI

Main command-line interface for running script quality checks.
Orchestrates all checkers and outputs results in markdown or JSON format.

Usage:
    python cli.py SCRIPT_PATH [OPTIONS]

    Options:
        --stumble          Run stumble checker only
        --scaffolding      Run scaffolding checker only
        --repetition       Run repetition checker only
        --flow             Run flow checker only
        --pacing           Run pacing analysis (sentence variance, readability, entity density)
        --all              Run all available checkers (default)
        --json             Output JSON instead of Markdown
        --no-annotate      Summary only, no annotated script
        --verbose          Show full section-by-section breakdown (used with --pacing)

        --voice            Apply learned voice patterns to script
        --show-voice-changes   Show what voice modifications were made
        --voice-patterns PATH  Path to voice-patterns.json (default: auto-detect)
        --rebuild-voice    Rebuild voice-patterns.json from all script+transcript pairs

    Examples:
        python cli.py script.md
        python cli.py script.md --flow --repetition
        python cli.py script.md --pacing --verbose
        python cli.py script.md --all --json
        python cli.py script.md --scaffolding --no-annotate
        python cli.py script.md --voice --show-voice-changes
        python cli.py --rebuild-voice

Exit codes:
    0 = No errors
    1 = Warnings only
    2 = Errors found

Dependencies:
    - spacy (for stumble checker)
    - en_core_web_sm model (install: python -m spacy download en_core_web_sm)
    - srt (for voice pattern corpus analysis)
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

from config import Config
from output import OutputFormatter


def read_script_file(filepath: str) -> str:
    """
    Read script file and return content.

    Supports .md and .txt files. Strips markdown formatting for analysis
    but preserves original for output.

    Args:
        filepath: Path to script file

    Returns:
        Script content as string

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Script file not found: {filepath}")

    content = path.read_text(encoding='utf-8')

    if not content.strip():
        raise ValueError(f"Script file is empty: {filepath}")

    return content


def run_checkers(text: str, config: Config, checker_flags: Dict[str, bool]) -> Dict[str, Any]:
    """
    Run selected checkers on text.

    Checkers run in logical order:
    1. Flow (check definitions and transitions first)
    2. Repetition (check content issues)
    3. Stumble (check delivery complexity)
    4. Scaffolding (check delivery phrases)

    Args:
        text: Script text to analyze
        config: Configuration object
        checker_flags: Dictionary of {checker_name: should_run}

    Returns:
        Dictionary of {checker_name: result} in execution order
    """
    results = {}

    # SCRIPT-02: Flow Analysis (check definitions before content)
    if checker_flags.get('flow', False):
        try:
            from checkers.flow import FlowChecker
            checker = FlowChecker(config)
            results['flow'] = checker.check(text)
        except RuntimeError as e:
            # spaCy model not installed
            print(f"ERROR: {e}", file=sys.stderr)
            print("Install with: python -m spacy download en_core_web_sm", file=sys.stderr)
            sys.exit(3)

    # SCRIPT-01: Repetition Detection (content issues)
    if checker_flags.get('repetition', False):
        from checkers.repetition import RepetitionChecker
        checker = RepetitionChecker(config)
        results['repetition'] = checker.check(text)

    # SCRIPT-03: Stumble Test (delivery complexity)
    if checker_flags.get('stumble', False):
        try:
            from checkers.stumble import StumbleChecker
            checker = StumbleChecker(config)
            results['stumble'] = checker.check(text)
        except RuntimeError as e:
            # spaCy model not installed
            print(f"ERROR: {e}", file=sys.stderr)
            print("Install with: python -m spacy download en_core_web_sm", file=sys.stderr)
            sys.exit(3)

    # SCRIPT-04: Scaffolding Counter (delivery phrases)
    if checker_flags.get('scaffolding', False):
        from checkers.scaffolding import ScaffoldingChecker
        checker = ScaffoldingChecker(config)
        results['scaffolding'] = checker.check(text)

    # SCRIPT-05: Pacing Analysis (section-level complexity and rhythm)
    if checker_flags.get('pacing', False):
        try:
            from checkers.pacing import PacingChecker
            checker = PacingChecker(config)
            results['pacing'] = checker.check(text)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(3)
        except ImportError as e:
            print(f"WARNING: Pacing checker unavailable: {e}", file=sys.stderr)
            print("Install with: pip install textstat", file=sys.stderr)

    return results


def format_voice_changes(changes: list) -> str:
    """
    Format voice pattern changes for display.

    Args:
        changes: List of change dictionaries from pattern applier

    Returns:
        Formatted markdown string showing changes
    """
    if not changes:
        return "## Voice Pattern Changes Applied\n\nNo changes made.\n\n---\n"

    output = ["## Voice Pattern Changes Applied\n"]

    # Separate substitutions and removals
    substitutions = [c for c in changes if c['type'] == 'substitution']
    removals = [c for c in changes if c['type'] == 'removal']

    if substitutions:
        output.append("**Substitutions:**")
        for sub in substitutions:
            output.append(f"- \"{sub['original']}\" -> \"{sub['replacement']}\" ({sub['count']} times)")
        output.append("")

    if removals:
        output.append("**Phrases Removed:**")
        for rem in removals:
            output.append(f"- \"{rem['phrase']}\" ({rem['count']} times)")
        output.append("")

    total_mods = sum(c['count'] for c in changes)
    output.append(f"**Total modifications:** {total_mods}\n")
    output.append("---\n")

    return "\n".join(output)


def determine_exit_code(results: Dict[str, Any]) -> int:
    """
    Determine exit code based on checker results.

    Args:
        results: Checker results

    Returns:
        0 = no issues or all 'ok'
        1 = warnings only
        2 = errors found
    """
    has_warnings = False
    has_errors = False

    for checker_name, data in results.items():
        # Check pacing verdict (PASS/NEEDS WORK/FAIL)
        if checker_name == 'pacing':
            pacing_verdict = data.get('stats', {}).get('verdict', '')
            if pacing_verdict == 'FAIL':
                has_errors = True
            elif pacing_verdict == 'NEEDS WORK':
                has_warnings = True
            continue

        severity = data.get('stats', {}).get('severity', 'ok')

        if severity == 'error':
            has_errors = True
        elif severity in ('warning', 'medium', 'high'):
            has_warnings = True

        # Check individual issues
        for issue in data.get('issues', []):
            issue_severity = issue.get('severity', 'ok')
            if issue_severity == 'error':
                has_errors = True
            elif issue_severity in ('warning', 'medium', 'high'):
                has_warnings = True

    if has_errors:
        return 2
    elif has_warnings:
        return 1
    else:
        return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Check script quality for teleprompter delivery',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py script.md                    # Run all checkers
  python cli.py script.md --flow             # Only flow analysis
  python cli.py script.md --repetition       # Only repetition detection
  python cli.py script.md --stumble          # Only stumble test
  python cli.py script.md --scaffolding      # Only scaffolding counter
  python cli.py script.md --pacing           # Only pacing analysis
  python cli.py script.md --pacing --verbose # Pacing with full section breakdown
  python cli.py script.md --json             # JSON output
  python cli.py script.md --no-annotate      # Summary only

Exit codes:
  0 = No issues
  1 = Warnings found
  2 = Errors found
        """
    )

    parser.add_argument('script_path', nargs='?', help='Path to script file (.md or .txt)')
    parser.add_argument('--flow', action='store_true', help='Run flow checker only')
    parser.add_argument('--repetition', action='store_true', help='Run repetition checker only')
    parser.add_argument('--stumble', action='store_true', help='Run stumble checker only')
    parser.add_argument('--scaffolding', action='store_true', help='Run scaffolding checker only')
    parser.add_argument('--pacing', action='store_true', help='Run pacing analysis (sentence variance, readability, entity density)')
    parser.add_argument('--all', action='store_true', help='Run all checkers (default)')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of Markdown')
    parser.add_argument('--no-annotate', action='store_true', help='Summary only, no annotated script')
    parser.add_argument('--verbose', action='store_true', help='Show full section-by-section breakdown (used with --pacing)')

    # Voice pattern flags
    parser.add_argument('--voice', action='store_true', help='Apply learned voice patterns to script')
    parser.add_argument('--show-voice-changes', action='store_true', help='Show what voice pattern changes were made')
    parser.add_argument('--voice-patterns', type=str, default=None, help='Path to voice-patterns.json (default: auto-detect)')
    parser.add_argument('--rebuild-voice', action='store_true', help='Rebuild voice-patterns.json from all available script+transcript pairs')

    args = parser.parse_args()

    # Handle --rebuild-voice (exits after completion)
    if args.rebuild_voice:
        # Determine projects directory
        if args.script_path:
            # Use script path's parent to find video-projects
            script_dir = Path(args.script_path).parent
            projects_dir = script_dir / '../../video-projects'
        else:
            # Try to find video-projects relative to cli.py
            cli_dir = Path(__file__).parent
            projects_dir = cli_dir / '../../video-projects'

        projects_dir = projects_dir.resolve()
        output_path = Path(__file__).parent / 'voice-patterns.json'

        if not projects_dir.exists():
            print(f"ERROR: Projects directory not found: {projects_dir}", file=sys.stderr)
            print("Provide a script path from your video project, or ensure video-projects/ is in expected location", file=sys.stderr)
            sys.exit(1)

        try:
            from voice import build_pattern_library
        except ImportError as e:
            print("ERROR: srt library not installed. Required for corpus analysis.", file=sys.stderr)
            print("Install with: pip install srt", file=sys.stderr)
            print("See: VOICE-SETUP.md for details", file=sys.stderr)
            sys.exit(1)

        print(f"Rebuilding voice patterns from: {projects_dir}")
        patterns = build_pattern_library(projects_dir, output_path)

        # Print summary
        meta = patterns.get('metadata', {})
        patterns_data = patterns.get('patterns', {})

        videos_analyzed = meta.get('videos_analyzed', 0)
        subs = len(patterns_data.get('word_substitutions', []))
        anti = len(patterns_data.get('anti_patterns', []))

        print(f"\nAnalyzed {videos_analyzed} videos")
        print(f"Found {subs} substitution patterns")
        print(f"Found {anti} anti-patterns")
        print(f"\nPatterns saved to: {output_path}")

        sys.exit(0)

    # Require script_path for all other operations
    if not args.script_path:
        print("ERROR: script_path is required (unless using --rebuild-voice)", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Determine which checkers to run
    checker_flags = {}

    if args.all or not (args.flow or args.repetition or args.stumble or args.scaffolding or args.pacing):
        # Default: run all checkers
        checker_flags = {
            'flow': True,
            'repetition': True,
            'stumble': True,
            'scaffolding': True,
            'pacing': True
        }
    else:
        # Run selected checkers
        if args.flow:
            checker_flags['flow'] = True
        if args.repetition:
            checker_flags['repetition'] = True
        if args.stumble:
            checker_flags['stumble'] = True
        if args.scaffolding:
            checker_flags['scaffolding'] = True
        if args.pacing:
            checker_flags['pacing'] = True

    # Read script file
    try:
        script = read_script_file(args.script_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("No content to check", file=sys.stderr)
        sys.exit(0)

    # Apply voice patterns if requested (BEFORE checkers)
    voice_changes = []
    if args.voice:
        from voice import apply_voice_patterns

        patterns_path = None
        if args.voice_patterns:
            patterns_path = Path(args.voice_patterns)

        try:
            script, voice_changes = apply_voice_patterns(
                script,
                patterns_path=patterns_path,
                show_changes=args.show_voice_changes
            )
        except FileNotFoundError:
            print("WARNING: No voice patterns found. Run corpus analysis first to build voice-patterns.json", file=sys.stderr)
            print("See: VOICE-SETUP.md for setup instructions", file=sys.stderr)

    # Initialize config
    config = Config()

    # Run checkers
    results = run_checkers(script, config, checker_flags)

    # Format output
    if args.json:
        output = OutputFormatter.format_json(results)
    else:
        # Check if only pacing was run (special formatting)
        if 'pacing' in results and len(results) == 1:
            # Pacing-only output
            output = OutputFormatter.format_pacing_report(
                results['pacing'],
                verbose=getattr(args, 'verbose', False)
            )
        else:
            # Standard multi-checker report
            include_annotated = not args.no_annotate
            output = OutputFormatter.format_full_report(script, results, include_annotated)

            # Append pacing report if pacing was run alongside other checkers
            if 'pacing' in results:
                pacing_output = OutputFormatter.format_pacing_report(
                    results['pacing'],
                    verbose=getattr(args, 'verbose', False)
                )
                output = output + "\n\n" + pacing_output

    # Prepend voice changes if requested
    if args.show_voice_changes and voice_changes:
        voice_output = format_voice_changes(voice_changes)
        output = voice_output + output

    # Print results
    print(output)

    # Exit with appropriate code
    exit_code = determine_exit_code(results)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
