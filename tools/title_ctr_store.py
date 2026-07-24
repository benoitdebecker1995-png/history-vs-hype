"""
Title CTR Store — DB-backed pattern CTR lookup for title scorer.

Reads real CTR data from keywords.db (ctr_snapshots JOIN video_performance)
and converts per-pattern average CTR percentages into 0-100 scores
matching the title_scorer.py scale.

CTR-to-score calibration:
    score = min(100, max(0, int(ctr_percent * 17)))
    3.8% CTR -> 64 (matches static declarative baseline of 65)

Usage:
    from tools.title_ctr_store import get_pattern_ctr_from_db

    scores = get_pattern_ctr_from_db("tools/discovery/keywords.db")
    # {'declarative': 64, 'versus': 79, ...}
"""

import sqlite3
from typing import Dict, Optional

from tools.discovery.ctr_reads import (
    latest_valid_ctr_by_video,
    latest_valid_snapshot_date,
)
from tools.logging_config import get_logger

logger = get_logger(__name__)


def get_latest_snapshot_date(db_path: str) -> Optional[str]:
    """Return the most recent non-zero ctr_snapshots date (YYYY-MM-DD), or None.

    Used by title_scorer to report how stale the live-CTR data behind a DB-enriched
    score is. Returns None on any DB error / missing table — never raises.
    """
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        logger.debug("latest snapshot date lookup failed (%s): %s", db_path, e)
        return None
    try:
        return latest_valid_snapshot_date(conn, require_ctr=True)
    finally:
        conn.close()


def get_pattern_ctr_from_db(db_path: str, min_sample: int = 3) -> Dict[str, int]:
    """
    Query keywords.db for real CTR data grouped by title pattern.

    For each video in video_performance, takes the latest non-zero CTR snapshot,
    classifies the title into a pattern using detect_pattern(), groups by pattern,
    and converts the average CTR% to a 0-100 score.

    Args:
        db_path: Path to keywords.db (or compatible SQLite DB)
        min_sample: Minimum number of videos required for a pattern to be included.
                    Patterns with fewer samples are excluded (not statistically reliable).

    Returns:
        Dict mapping pattern name -> score (0-100).
        Returns empty dict if DB is missing, has no data, or any sqlite3.Error occurs.

    Score calibration:
        score = min(100, max(0, int(ctr_percent * 17)))
        This maps 3.8% CTR -> 64, close to the static declarative baseline of 65.
    """
    # Import here to avoid circular import at module load time.
    # title_ctr_store imports detect_pattern from title_scorer.
    # title_scorer will import get_pattern_ctr_from_db from title_ctr_store.
    # This is safe: the lazy import breaks the potential import cycle since
    # title_ctr_store never calls score_title().
    try:
        from tools.title_scorer import detect_pattern
    except ImportError as e:
        logger.warning("Could not import detect_pattern: %s", e)
        return {}

    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        logger.debug("CTR DB open failed (%s): %s — using static scores", db_path, e)
        return {}
    try:
        # Canonical valid-latest CTR per video (is_valid=1, one row per video —
        # excludes quarantined snapshots and same-date duplicates). See ADR-0017.
        latest = latest_valid_ctr_by_video(conn, require_ctr=True)
        titles = {
            r[0]: r[1]
            for r in conn.execute(
                "SELECT video_id, title FROM video_performance WHERE title IS NOT NULL"
            )
        }
    except sqlite3.Error as e:
        logger.debug("CTR DB read failed (%s): %s — using static scores", db_path, e)
        return {}
    finally:
        conn.close()

    if not latest:
        return {}

    # Group by detected pattern — exactly one observation per video.
    pattern_ctrs: Dict[str, list] = {}
    for video_id, rec in latest.items():
        title = titles.get(video_id)
        if not title:
            continue
        pattern = detect_pattern(title)
        pattern_ctrs.setdefault(pattern, []).append(rec["ctr_percent"])

    # Filter by min_sample, compute averages, convert to scores
    result: Dict[str, int] = {}
    for pattern, ctrs in pattern_ctrs.items():
        if len(ctrs) < min_sample:
            logger.debug(
                "Pattern '%s' has only %d samples (need %d) — excluded",
                pattern, len(ctrs), min_sample
            )
            continue
        avg_ctr = sum(ctrs) / len(ctrs)
        score = min(100, max(0, int(avg_ctr * 17)))
        result[pattern] = score
        logger.debug(
            "Pattern '%s': n=%d, avg_ctr=%.2f%%, score=%d",
            pattern, len(ctrs), avg_ctr, score
        )

    return result
