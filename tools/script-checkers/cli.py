"""
Script Quality Checker CLI

Main command-line interface for running script quality checks.
Orchestrates all checkers and outputs results in markdown or JSON format.

Usage:
    python cli.py SCRIPT_PATH [OPTIONS]

    Options:
        --stumble          Run stumble checker only
        --scaffolding      Run scaffolding checker only
        --all              Run all available checkers (default)
        --json             Output JSON instead of Markdown
        --no-annotate      Summary only, no annotated script

    Examples:
        python cli.py script.md
        python cli.py script.md --stumble
        python cli.py script.md --all --json
        python cli.py script.md --scaffolding --no-annotate

Exit codes:
    0 = No errors
    1 = Warnings only
    2 = Errors found

Dependencies:
    - spacy (for stumble checker)
    - en_core_web_sm model (install: python -m spacy download en_core_web_sm)
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

    Args:
        text: Script text to analyze
        config: Configuration object
        checker_flags: Dictionary of {checker_name: should_run}

    Returns:
        Dictionary of {checker_name: result}
    """
    results = {}

    # SCRIPT-03: Stumble Test
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

    # SCRIPT-04: Scaffolding Counter
    if checker_flags.get('scaffolding', False):
        from checkers.scaffolding import ScaffoldingChecker
        checker = ScaffoldingChecker(config)
        results['scaffolding'] = checker.check(text)

    return results


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
  python cli.py script.md --stumble          # Only stumble test
  python cli.py script.md --scaffolding      # Only scaffolding counter
  python cli.py script.md --json             # JSON output
  python cli.py script.md --no-annotate      # Summary only

Exit codes:
  0 = No issues
  1 = Warnings found
  2 = Errors found
        """
    )

    parser.add_argument('script_path', help='Path to script file (.md or .txt)')
    parser.add_argument('--stumble', action='store_true', help='Run stumble checker only')
    parser.add_argument('--scaffolding', action='store_true', help='Run scaffolding checker only')
    parser.add_argument('--all', action='store_true', help='Run all checkers (default)')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of Markdown')
    parser.add_argument('--no-annotate', action='store_true', help='Summary only, no annotated script')

    args = parser.parse_args()

    # Determine which checkers to run
    checker_flags = {}

    if args.all or not (args.stumble or args.scaffolding):
        # Default: run all checkers
        checker_flags = {'stumble': True, 'scaffolding': True}
    else:
        # Run selected checkers
        if args.stumble:
            checker_flags['stumble'] = True
        if args.scaffolding:
            checker_flags['scaffolding'] = True

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

    # Initialize config
    config = Config()

    # Run checkers
    results = run_checkers(script, config, checker_flags)

    # Format output
    if args.json:
        output = OutputFormatter.format_json(results)
    else:
        include_annotated = not args.no_annotate
        output = OutputFormatter.format_full_report(script, results, include_annotated)

    # Print results
    print(output)

    # Exit with appropriate code
    exit_code = determine_exit_code(results)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
