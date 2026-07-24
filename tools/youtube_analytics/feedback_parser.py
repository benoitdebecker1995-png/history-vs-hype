"""
Feedback Parser Module

Backfill CLI over tools.post_publish.PostPublishStore: parses post-publish
reports and stores their feedback sections in the performance database.

    from feedback_parser import find_analysis_files, backfill_all

The legacy dict dialect (`avg_retention` as PERCENT, field name `ctr`) was
deleted 2026-07-01 — its numeric fields had no live readers, and killing the
dialect ends the fraction-vs-percent divergence with patterns.py (ADR-0005).
Consumers read `PostPublishReport` attributes directly.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

from tools.logging_config import get_logger
from tools.post_publish import (
    PostPublishMalformedError,
    PostPublishMissingError,
    PostPublishStore,
)

logger = get_logger(__name__)


def find_analysis_files(project_root: Path) -> List[Path]:
    """Return all post-publish report paths under project_root, sorted.

    Thin shim over PostPublishStore.discover().
    """
    return PostPublishStore(project_root=project_root).discover()



def backfill_all(project_root: Path, force: bool = False) -> Dict[str, Any]:
    """
    Process all POST-PUBLISH-ANALYSIS files and store in database.

    Args:
        project_root: Path to project root directory
        force: If True, re-parse files that already have feedback stored

    Returns:
        Dict with processed/skipped/errors counts and details list
    """
    try:
        from tools.discovery.performance_tracker import PerformanceTracker
        db = PerformanceTracker.connect()
    except ImportError:
        return {
            'error': 'PerformanceTracker not available',
            'processed': 0,
            'skipped': 0,
            'errors': 1
        }

    results = {
        'processed': 0,
        'skipped': 0,
        'errors': 0,
        'details': []
    }

    files = find_analysis_files(project_root)
    total = len(files)

    logger.info("Found %d analysis files to process", total)

    for i, filepath in enumerate(files, 1):
        filename = filepath.name
        logger.debug("[%d/%d] Parsing: %s...", i, total, filename)

        # Parse file
        try:
            report = PostPublishStore().load(filepath)
        except (PostPublishMissingError, PostPublishMalformedError) as exc:
            logger.warning("Parse error for %s: %s", filename, exc)
            results['errors'] += 1
            results['details'].append({
                'file': filename,
                'status': 'error',
                'message': str(exc)
            })
            continue

        video_id = report.video_id

        # Check if already has feedback (unless force=True)
        if not force and db.has_feedback(video_id):
            logger.debug("SKIP %s (already has feedback)", filename)
            results['skipped'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'skipped'
            })
            continue

        # Store in database
        feedback_data = {
            'biggest_drop_position': report.biggest_drop_position,
            'observations': report.observations,
            'actionable': report.actionable,
            'discovery': report.discovery
        }

        store_result = db.store_video_feedback(video_id, feedback_data)

        if 'error' in store_result:
            logger.warning("Store error for %s: %s", filename, store_result['error'])
            results['errors'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'error',
                'message': store_result['error']
            })
        elif store_result.get('status') == 'no_match':
            logger.debug("SKIP %s (video not in performance table)", filename)
            results['skipped'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'no_match'
            })
        else:
            logger.debug("OK: %s", filename)
            results['processed'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'success'
            })

    db.close()

    logger.info("Complete: %d processed, %d skipped, %d errors",
                results['processed'], results['skipped'], results['errors'])

    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Parse POST-PUBLISH-ANALYSIS markdown files into structured data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.feedback_parser path/to/POST-PUBLISH-ANALYSIS.md
  python -m tools.youtube_analytics.feedback_parser backfill
  python -m tools.youtube_analytics.feedback_parser backfill --force""",
    )
    parser.add_argument(
        "target",
        help="Path to a POST-PUBLISH-ANALYSIS.md file, or 'backfill' to process all files",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-process files that have already been stored (only applies to backfill mode)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    if args.target == 'backfill':
        project_root = Path(__file__).parent.parent.parent
        result = backfill_all(project_root, force=args.force)
        sys.exit(0 if result['errors'] == 0 else 1)
    else:
        from dataclasses import asdict
        try:
            report = PostPublishStore().load(Path(args.target))
        except (PostPublishMissingError, PostPublishMalformedError) as exc:
            print(json.dumps({'error': str(exc), 'filepath': args.target}, indent=2))
        else:
            print(json.dumps(asdict(report), indent=2, default=str))
