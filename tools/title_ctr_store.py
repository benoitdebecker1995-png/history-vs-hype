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
from typing import Dict

from tools.logging_config import get_logger

logger = get_logger(__name__)


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
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Fetch the latest non-zero CTR snapshot per video, joined with title.
        # Subquery picks MAX snapshot_date per video WHERE ctr_percent > 0.
        cursor.execute(
            """
            SELECT vp.video_id, vp.title, cs.ctr_percent
            FROM video_performance vp
            JOIN ctr_snapshots cs ON cs.video_id = vp.video_id
            WHERE cs.ctr_percent > 0
              AND vp.title IS NOT NULL
              AND cs.snapshot_date = (
                  SELECT MAX(cs2.snapshot_date)
                  FROM ctr_snapshots cs2
                  WHERE cs2.video_id = vp.video_id
                    AND cs2.ctr_percent > 0
              )
            """
        )
        rows = cursor.fetchall()
        conn.close()

    except sqlite3.Error as e:
        logger.debug("CTR DB read failed (%s): %s — using static scores", db_path, e)
        return {}

    if not rows:
        return {}

    # Group by detected pattern
    pattern_ctrs: Dict[str, list] = {}
    for row in rows:
        title = row["title"]
        ctr = row["ctr_percent"]
        if not title:
            continue
        pattern = detect_pattern(title)
        pattern_ctrs.setdefault(pattern, []).append(ctr)

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
