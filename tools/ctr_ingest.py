"""
CTR Ingestion Tool — bridges CROSS-VIDEO-SYNTHESIS.md to keywords.db.

Reads per-video CTR from the manually-maintained synthesis table and writes
it into the ctr_snapshots table via KeywordDB.add_ctr_snapshot(). This
populates the DB so title_ctr_store.py can compute live pattern scores.

The title matching between synthesis table and video_performance is done via
case-insensitive LIKE on the first 40 characters of the title. Unmatched
titles are logged at WARNING level.

Usage:
    python -m tools.ctr_ingest                               # Default paths
    python -m tools.ctr_ingest --synthesis path/to/file.md  # Custom path
    python -m tools.ctr_ingest --dry-run                     # Preview only
    python -m tools.ctr_ingest --verbose                     # Verbose logging
"""

from pathlib import Path
from typing import Dict, Any

from tools.logging_config import get_logger
from tools.retitle_audit import _parse_synthesis_table

logger = get_logger(__name__)

# Default path to the synthesis file, relative to repo root
_DEFAULT_SYNTHESIS = Path("channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md")

# Snapshot date for all historical CTR entries (data collection date)
_SNAPSHOT_DATE = "2026-02-23"


def ingest_synthesis_ctr(
    synthesis_path: Path,
    db,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Read CROSS-VIDEO-SYNTHESIS.md master table and store CTR to keywords.db.

    Resolves video_ids by matching titles against video_performance.title using
    case-insensitive LIKE on a 40-character prefix. Videos without CTR data or
    without a matching video_id are skipped gracefully.

    Args:
        synthesis_path: Path to CROSS-VIDEO-SYNTHESIS.md
        db:             KeywordDB instance (already connected)
        dry_run:        If True, skip writes and return preview counts

    Returns:
        {
          'written':    int,   # Rows inserted into ctr_snapshots
          'skipped':    int,   # Videos with no CTR data (n/a)
          'unmatched':  int,   # Videos with CTR but no matching video_id
          'errors':     list,  # Error strings from failed inserts
          'would_write': int,  # (dry_run only) How many would be written
        }
    """
    videos = _parse_synthesis_table(synthesis_path)
    logger.info("Parsed %d videos from synthesis table", len(videos))

    written = 0
    skipped = 0
    unmatched = 0
    errors = []
    would_write = 0

    for video in videos:
        title = video.get("title", "").strip()
        ctr = video.get("ctr")
        impressions = video.get("impressions")
        views = video.get("views") or 0

        # Skip videos with no CTR data
        if ctr is None:
            logger.debug("Skipping '%s' — no CTR data", title)
            skipped += 1
            continue

        # Resolve video_id by title matching
        video_id = _lookup_video_id(db, title)
        if video_id is None:
            logger.warning("No video_performance match for title: '%s'", title)
            unmatched += 1
            continue

        would_write += 1

        if dry_run:
            logger.info(
                "[DRY RUN] Would write: video_id=%s title='%s' ctr=%.2f%% imp=%s",
                video_id,
                title,
                ctr,
                impressions,
            )
            continue

        result = db.add_ctr_snapshot(
            video_id=video_id,
            ctr_percent=ctr,
            impression_count=impressions or 0,
            view_count=views,
            snapshot_date=_SNAPSHOT_DATE,
            is_late_entry=True,
        )

        if "error" in result:
            logger.error(
                "Failed to write snapshot for '%s' (video_id=%s): %s",
                title,
                video_id,
                result["error"],
            )
            errors.append(f"{title}: {result['error']}")
        else:
            logger.info(
                "Wrote ctr_snapshot: video_id=%s title='%s' ctr=%.2f%%",
                video_id,
                title,
                ctr,
            )
            written += 1

    summary = {
        "written": written,
        "skipped": skipped,
        "unmatched": unmatched,
        "errors": errors,
        "would_write": would_write if dry_run else written,
    }

    if dry_run:
        summary["written"] = 0

    logger.info(
        "Ingest complete: written=%d skipped=%d unmatched=%d errors=%d",
        summary["written"],
        skipped,
        unmatched,
        len(errors),
    )
    return summary


def _lookup_video_id(db, title: str) -> str | None:
    """
    Look up video_id by matching title against video_performance table.

    Uses LIKE on the first 40 characters, case-insensitive. Returns the
    first match found, or None if no match.

    Args:
        db:    KeywordDB instance
        title: Title string from synthesis table

    Returns:
        video_id string if matched, None otherwise
    """
    if not title:
        return None

    # Use first 40 chars for LIKE match — handles minor formatting differences
    prefix = title[:40].replace("'", "''")

    try:
        cursor = db._conn.cursor()
        cursor.execute(
            "SELECT video_id FROM video_performance WHERE title LIKE ? COLLATE NOCASE LIMIT 1",
            (f"%{prefix}%",),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
    except Exception as exc:
        logger.warning("DB lookup error for title '%s': %s", title, exc)

    return None


def main() -> None:
    """CLI entry point for CTR ingestion."""
    import argparse
    from tools.discovery.database import KeywordDB
    from tools.logging_config import setup_logging

    parser = argparse.ArgumentParser(
        description="Ingest CTR data from CROSS-VIDEO-SYNTHESIS.md into keywords.db"
    )
    parser.add_argument(
        "--synthesis",
        type=Path,
        default=_DEFAULT_SYNTHESIS,
        help=f"Path to CROSS-VIDEO-SYNTHESIS.md (default: {_DEFAULT_SYNTHESIS})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be written without modifying the DB",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Only show errors")
    args = parser.parse_args()

    setup_logging(verbose=args.verbose, quiet=args.quiet)

    if not args.synthesis.exists():
        print(f"ERROR: Synthesis file not found: {args.synthesis}")
        raise SystemExit(1)

    db = KeywordDB()
    result = ingest_synthesis_ctr(args.synthesis, db, dry_run=args.dry_run)
    db.close()

    mode = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{mode}CTR Ingest Summary")
    print("=" * 40)
    if args.dry_run:
        print(f"  Would write:  {result['would_write']}")
    else:
        print(f"  Written:      {result['written']}")
    print(f"  Skipped:      {result['skipped']}  (no CTR data)")
    print(f"  Unmatched:    {result['unmatched']}  (title not in video_performance)")
    if result["errors"]:
        print(f"  Errors:       {len(result['errors'])}")
        for err in result["errors"]:
            print(f"    - {err}")
    print()


if __name__ == "__main__":
    main()
