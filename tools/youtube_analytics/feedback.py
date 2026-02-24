#!/usr/bin/env python3
"""
Feedback CLI - Query and analyze past video performance insights

Provides backfill, query, and pattern extraction commands for feedback data.

Usage:
    python feedback.py backfill                  Import all analysis files
    python feedback.py backfill --force          Re-import all (overwrite)
    python feedback.py query --topic territorial Show territorial insights
    python feedback.py query --video VIDEO_ID   Show specific video feedback
    python feedback.py patterns                  Display success/failure patterns
    python feedback.py patterns --markdown       Save patterns report

Dependencies:
    - feedback_parser.py for backfill
    - feedback_queries.py for query and patterns
    - KeywordDB for database access
"""

import sys
import argparse
from pathlib import Path

# Project root (3 levels up from tools/youtube_analytics/)
project_root = Path(__file__).parent.parent.parent

try:
    from .feedback_parser import backfill_all
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False

try:
    from .feedback_queries import (
        get_insights_for_topic,
        get_insights_preamble,
        generate_patterns_report,
        format_patterns_markdown,
        format_patterns_terminal,
        format_query_terminal,
        format_query_markdown
    )
    QUERIES_AVAILABLE = True
except ImportError:
    QUERIES_AVAILABLE = False

try:
    from tools.discovery.database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False


def cmd_backfill(args):
    """Process all POST-PUBLISH-ANALYSIS files and store in database."""
    if not PARSER_AVAILABLE:
        print("ERROR: feedback_parser module not available")
        return 2

    print("Starting backfill of POST-PUBLISH-ANALYSIS files...")
    print()

    result = backfill_all(project_root, force=args.force)

    if 'error' in result:
        print(f"ERROR: {result['error']}")
        return 2

    # Summary already printed by backfill_all
    return 0 if result['errors'] == 0 else 1


def cmd_query(args):
    """Query insights by topic or video."""
    if not QUERIES_AVAILABLE or not DATABASE_AVAILABLE:
        print("ERROR: Required modules not available")
        return 2

    # Determine query type
    if args.video:
        # Single video query
        db = KeywordDB()
        result = db.get_video_feedback(args.video)
        db.close()

        if 'error' in result:
            print(f"ERROR: {result['error']}")
            if result['error'] == 'not_found':
                print()
                print("Video has no feedback stored yet.")
                print("Run 'python feedback.py backfill' to import analysis files.")
            return 1

        # Format output
        if args.markdown:
            output = format_query_markdown(result)
            # Save to project folder or channel-data
            output_path = project_root / 'channel-data' / f"FEEDBACK-{args.video}.md"
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Saved to: {output_path}")
        else:
            print(format_query_terminal(result))

    elif args.topic:
        # Topic query
        command_context = args.metric if args.metric else 'script'
        result = get_insights_for_topic(args.topic, command=command_context, limit=10)

        if result['count'] == 0:
            print(f"No feedback data found for topic: {args.topic}")
            print()
            print("Run 'python feedback.py backfill' to import analysis files.")
            return 1

        # Format output
        if args.markdown:
            output = format_query_markdown(result)
            filename = f"FEEDBACK-{args.topic.upper()}"
            if args.metric:
                filename += f"-{args.metric.upper()}"
            filename += ".md"
            output_path = project_root / 'channel-data' / filename
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Saved to: {output_path}")
        else:
            print(format_query_terminal(result))

    else:
        print("ERROR: Must specify --topic or --video")
        return 2

    return 0


def cmd_patterns(args):
    """Generate success/failure pattern report."""
    if not QUERIES_AVAILABLE:
        print("ERROR: feedback_queries module not available")
        return 2

    print("Generating patterns report...")
    print()

    report = generate_patterns_report()

    # Check if any data available
    success_count = report['success'].get('video_count', 0)
    failure_count = report['failure'].get('video_count', 0)

    if success_count == 0 and failure_count == 0:
        print("No feedback data found for pattern extraction.")
        print()
        print("Run 'python feedback.py backfill' to import analysis files.")
        return 1

    # Format output
    if args.markdown:
        output = format_patterns_markdown(report)
        output_path = project_root / 'channel-data' / 'patterns' / 'FEEDBACK-PATTERNS.md'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')
        print(f"Saved to: {output_path}")
    else:
        print(format_patterns_terminal(report))

    return 0


def main():
    """CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description='Feedback Analysis - Query insights and extract patterns from past videos',
        epilog="""
Examples:
  python feedback.py backfill                          Import all analysis files
  python feedback.py backfill --force                  Re-import all (overwrite existing)
  python feedback.py query --topic territorial         Show territorial video insights
  python feedback.py query --video VIDEO_ID            Show specific video feedback
  python feedback.py query --topic territorial --metric retention  Filter by metric
  python feedback.py query --topic territorial --markdown  Save as markdown report
  python feedback.py patterns                          Show success/failure patterns
  python feedback.py patterns --markdown               Save patterns report
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Backfill subcommand
    backfill_parser = subparsers.add_parser('backfill', help='Import all POST-PUBLISH-ANALYSIS files')
    backfill_parser.add_argument('--force', action='store_true',
                                 help='Re-parse all files, overwriting existing feedback')

    # Query subcommand
    query_parser = subparsers.add_parser('query', help='Query insights by topic or video')
    query_parser.add_argument('--topic', type=str,
                             help='Topic type (territorial, ideological, legal, colonial, general)')
    query_parser.add_argument('--video', type=str,
                             help='YouTube video ID')
    query_parser.add_argument('--metric', type=str, choices=['retention', 'ctr', 'discovery'],
                             help='Filter insights by metric type')
    query_parser.add_argument('--markdown', action='store_true',
                             help='Output as markdown report (saves to channel-data/)')

    # Patterns subcommand
    patterns_parser = subparsers.add_parser('patterns', help='Extract success/failure patterns')
    patterns_parser.add_argument('--markdown', action='store_true',
                                help='Save as markdown report (saves to channel-data/patterns/)')

    args = parser.parse_args()

    # Route to subcommand handlers
    if args.command == 'backfill':
        exit_code = cmd_backfill(args)
    elif args.command == 'query':
        exit_code = cmd_query(args)
    elif args.command == 'patterns':
        exit_code = cmd_patterns(args)
    else:
        parser.print_help()
        exit_code = 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
