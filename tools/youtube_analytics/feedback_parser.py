"""
Feedback Parser Module

Back-compat shim over tools.post_publish.PostPublishStore. The legacy
public surface is preserved:

    from feedback_parser import parse_analysis_file, find_analysis_files, backfill_all

`parse_analysis_file` returns a legacy dict (avg_retention as PERCENT, field
name `ctr`, error-dict on failure) — distinct from patterns.py's contract
(fraction, ctr_percent, None-on-failure). The unification of the two
contracts will happen in Phase 3 when each caller is migrated to import
PostPublishReport directly.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

from tools.logging_config import get_logger
from tools.post_publish import (
    PostPublishMalformedError,
    PostPublishMissingError,
    PostPublishReport,
    PostPublishStore,
)

logger = get_logger(__name__)


def _report_to_feedback_dict(report: PostPublishReport) -> Dict[str, Any]:
    """Convert a PostPublishReport to the legacy feedback_parser dict shape.

    Note the contract preserved here vs. patterns.py:
      - `avg_retention` is a PERCENT (28.1), not a fraction.
      - Field name is `ctr` (not `ctr_percent`).
      - `parsed_at` is set to NOW at conversion time (matches old behaviour).
      - `filepath` (not `source_file`) holds the source path as a string.
    """
    return {
        'video_id': report.video_id,
        'parsed_at': datetime.now(timezone.utc).isoformat(),
        'filepath': str(report.source_path),
        'avg_retention': report.avg_retention_pct,
        'final_retention': report.final_retention_pct,
        'ctr': report.ctr_percent,
        'impressions': report.impressions,
        'views': report.views,
        'subscribers_gained': report.subscribers_gained,
        'observations': report.observations,
        'actionable': report.actionable,
        'drop_points': report.drop_points,
        'biggest_drop_position': report.biggest_drop_position,
        'discovery': report.discovery,
    }


def parse_analysis_file(filepath: str) -> Dict[str, Any]:
    """Parse one POST-PUBLISH-ANALYSIS file into the legacy feedback dict shape.

    Returns the dict on success, or {'error': msg, 'filepath': filepath} on
    failure — preserving the historical contract that callers branch on
    `'error' in result`.
    """
    try:
        report = PostPublishStore().load(Path(filepath))
    except PostPublishMissingError:
        return {'error': 'File not found', 'filepath': filepath}
    except PostPublishMalformedError as exc:
        return {'error': str(exc), 'filepath': filepath}
    return _report_to_feedback_dict(report)


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
        parsed = parse_analysis_file(str(filepath))

        if 'error' in parsed:
            logger.warning("Parse error for %s: %s", filename, parsed['error'])
            results['errors'] += 1
            results['details'].append({
                'file': filename,
                'status': 'error',
                'message': parsed['error']
            })
            continue

        video_id = parsed['video_id']

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
            'biggest_drop_position': parsed['biggest_drop_position'],
            'observations': parsed['observations'],
            'actionable': parsed['actionable'],
            'discovery': parsed.get('discovery', {})
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
        result = parse_analysis_file(args.target)
        print(json.dumps(result, indent=2))
