"""Canonical valid-latest-CTR reads over keywords.db `ctr_snapshots`.

ONE place that encodes "the current CTR observation for a video":

  * `is_valid = 1` — quarantined snapshots (the 2026-07-13/07-23 collector
    double-count rows) are excluded, never silently consumed.
  * exactly ONE row per video — the latest `snapshot_date`, tie-broken by
    highest `id`, so duplicate rows on the same date never multiply a video's
    weight in downstream averages.

Origin (ADR-0017, 2026-07-23 audit): six consumers each re-implemented "latest
CTR per video" against `ctr_snapshots`. Only `growth_data`'s fallback got it
right; the other five omitted the `is_valid` filter and/or the per-video dedup,
so invalid double-counted rows won `MAX(snapshot_date)` and leaked into title
scoring (509 rows / 275 videos, 36 invalid). This module is that one correct
query, factored out; callers route through it instead of hand-rolling SQL.

Read-only, stdlib `sqlite3` only. Never raises: returns `{}` / `None` on any
DB error, matching the repo's read-side error contract.
"""

import sqlite3
from typing import Any, Dict, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

_COLUMNS = "video_id, ctr_percent, impression_count, view_count, snapshot_date"


def _predicate(require_ctr: bool, require_impressions: bool) -> str:
    """Fixed, literal column guards (no caller-supplied SQL — never interpolated
    from untrusted input)."""
    parts = []
    if require_ctr:
        parts.append("ctr_percent > 0")
    if require_impressions:
        parts.append("impression_count > 0")
    return "".join(f" AND {p}" for p in parts)


def latest_valid_ctr_by_video(
    conn: sqlite3.Connection,
    *,
    require_ctr: bool = False,
    require_impressions: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Latest valid CTR snapshot for EVERY video, one row each.

    Returns ``{video_id: {ctr_percent, impression_count, view_count,
    snapshot_date}}``. Empty dict on any error.
    """
    pred = _predicate(require_ctr, require_impressions)
    sql = f"""
        SELECT {_COLUMNS}
        FROM ctr_snapshots s
        WHERE s.is_valid = 1{pred}
          AND s.id = (
              SELECT x.id FROM ctr_snapshots x
              WHERE x.video_id = s.video_id AND x.is_valid = 1{pred}
              ORDER BY x.snapshot_date DESC, x.id DESC
              LIMIT 1
          )
    """
    try:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        out: Dict[str, Dict[str, Any]] = {}
        for row in cur.fetchall():
            rec = dict(zip(cols, row))
            out[rec["video_id"]] = rec
        return out
    except sqlite3.Error as e:
        logger.debug("latest_valid_ctr_by_video failed: %s", e)
        return {}


def latest_valid_ctr_for(
    conn: sqlite3.Connection,
    video_id: str,
    *,
    after_date: Optional[str] = None,
    require_ctr: bool = True,
    require_impressions: bool = False,
) -> Optional[Dict[str, Any]]:
    """Latest valid CTR snapshot for ONE video (optionally on/after ``after_date``).

    Returns a ``{ctr_percent, impression_count, view_count, snapshot_date, ...}``
    dict, or ``None`` if there is no qualifying valid row / on error.
    """
    pred = _predicate(require_ctr, require_impressions)
    sql = f"SELECT {_COLUMNS} FROM ctr_snapshots WHERE video_id = ? AND is_valid = 1{pred}"
    params: list = [video_id]
    if after_date:
        sql += " AND snapshot_date >= ?"
        params.append(after_date)
    sql += " ORDER BY snapshot_date DESC, id DESC LIMIT 1"
    try:
        cur = conn.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return None
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, row))
    except sqlite3.Error as e:
        logger.debug("latest_valid_ctr_for(%s) failed: %s", video_id, e)
        return None


def d28_for(
    conn: sqlite3.Connection,
    video_id: str,
    published_date: str,
    *,
    traffic_source: str = "ALL",
) -> Dict[str, Any]:
    """First-28-day impressions for one video, from `impressions_daily`.

    This is the pre-registered breakout metric (BREAKOUT-HYPOTHESES.md, H3). It
    must NOT be computed from `ctr_snapshots.impression_count`, which is a sliding
    ~30-report-day sum ending ~D-3 and therefore answers a different question
    entirely — for a video older than a month it does not contain the launch
    window at all.

    `published_date` is 'YYYY-MM-DD'. The window is [published, published+27]
    inclusive.

    ALWAYS check `complete`. A partial window is a real number about an unfinished
    period, and comparing it to a threshold as though it were final is how a video
    gets called a win before its window closes. Returns `days_covered` so callers
    can say so out loud.

    Completeness is measured against REPORT COVERAGE, not against this video's own
    rows. A day on which a video got zero impressions produces no CSV row at all,
    so counting the video's rows would mean a quiet video could never read as
    complete — the exact error that made a fully-covered window look like 24/28.
    """
    empty = {
        "video_id": video_id, "impressions": 0, "clicks": 0, "ctr_percent": 0.0,
        "days_covered": 0, "days_with_data": 0, "complete": False,
        "window_start": published_date, "window_end": None,
    }
    try:
        from datetime import date as _date, timedelta as _td
        start = _date.fromisoformat(published_date)
    except (TypeError, ValueError):
        logger.debug("d28_for(%s): unparseable published_date %r", video_id, published_date)
        return empty

    end = start + _td(days=27)
    try:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(impressions), 0), COALESCE(SUM(clicks), 0),
                   COUNT(DISTINCT metric_date)
              FROM impressions_daily
             WHERE video_id = ? AND traffic_source = ?
               AND metric_date >= ? AND metric_date <= ?
            """,
            (video_id, traffic_source, start.isoformat(), end.isoformat()),
        ).fetchone()
        # Report coverage across ALL videos — the denominator for completeness.
        covered = conn.execute(
            """
            SELECT COUNT(DISTINCT metric_date) FROM impressions_daily
             WHERE metric_date >= ? AND metric_date <= ?
            """,
            (start.isoformat(), end.isoformat()),
        ).fetchone()[0]
    except sqlite3.Error as e:
        logger.debug("d28_for(%s) failed: %s", video_id, e)
        return empty

    impressions, clicks, days_with_data = (row or (0, 0, 0))
    return {
        "video_id": video_id,
        "impressions": impressions,
        "clicks": clicks,
        "ctr_percent": round(clicks / impressions * 100, 2) if impressions else 0.0,
        "days_covered": covered,            # report-days we hold for this window
        "days_with_data": days_with_data,   # days this video actually appeared
        "complete": covered >= 28,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
    }


def d28_impressions_by_video(
    conn: sqlite3.Connection,
    published: Dict[str, str],
    *,
    traffic_source: str = "ALL",
) -> Dict[str, Dict[str, Any]]:
    """`d28_for` across a {video_id: published_date} map. Complete windows only
    should be used for baselines — filter on `complete` at the call site so the
    exclusion is visible rather than buried here."""
    return {
        vid: d28_for(conn, vid, pub, traffic_source=traffic_source)
        for vid, pub in published.items()
    }


def latest_valid_snapshot_date(
    conn: sqlite3.Connection, *, require_ctr: bool = True
) -> Optional[str]:
    """Most recent VALID snapshot date (YYYY-MM-DD), or None.

    Used for freshness/staleness reporting so a quarantined later date never
    masquerades as fresh data.
    """
    pred = _predicate(require_ctr, False)
    try:
        row = conn.execute(
            f"SELECT MAX(snapshot_date) FROM ctr_snapshots WHERE is_valid = 1{pred}"
        ).fetchone()
        return row[0] if row and row[0] else None
    except sqlite3.Error as e:
        logger.debug("latest_valid_snapshot_date failed: %s", e)
        return None
