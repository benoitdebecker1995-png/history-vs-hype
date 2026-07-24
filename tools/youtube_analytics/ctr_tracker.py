"""
CTR / View Velocity Tracker — Periodic Snapshot Comparison

Takes snapshots of video view counts from the YouTube Analytics API,
stores them in keywords.db (ctr_snapshots table), and compares against
the most recent previous snapshot to flag significant changes.

Also fetches real CTR (click-through rate) and impression data from the
YouTube Analytics API and stores them alongside view counts, automatically
keeping the title_ctr_store -> title_scorer -> greenlight chain up to date.

Flags:
  - View velocity dropped >50% (algorithm pullback)
  - View velocity increased >100% (momentum / double-down candidate)
  - Videos with zero new views since last snapshot (dead weight)

Usage:
    python -m tools.youtube_analytics.ctr_tracker              # Snapshot + report
    python -m tools.youtube_analytics.ctr_tracker --report-only  # Compare existing only

Output: stdout summary report + CTR update summary
Storage: tools/discovery/keywords.db (ctr_snapshots table)
"""

import sys
import sqlite3
import argparse
from pathlib import Path
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Dict, List, Tuple, Optional

from tools.logging_config import get_logger, setup_logging
from tools.youtube_analytics.auth import get_authenticated_service
from tools.youtube_analytics.growth_data import fetch_all_video_ids, fetch_video_metadata
from tools.title_ctr_store import get_pattern_ctr_from_db

logger = get_logger(__name__)

DB_PATH = Path(__file__).parent.parent / 'discovery' / 'keywords.db'


# =========================================================================
# DATABASE
# =========================================================================

def _get_db() -> sqlite3.Connection:
    """Get connection to keywords.db with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def get_previous_snapshot(conn: sqlite3.Connection,
                          before_date: str) -> Dict[str, dict]:
    """
    Get the most recent snapshot before the given date.

    Returns dict keyed by video_id with {view_count, snapshot_date}.
    """
    # Find the most recent snapshot date before today
    row = conn.execute(
        "SELECT MAX(snapshot_date) FROM ctr_snapshots WHERE snapshot_date < ? AND is_valid = 1",
        (before_date,)
    ).fetchone()

    prev_date = row[0] if row else None
    if not prev_date:
        return {}

    rows = conn.execute(
        "SELECT video_id, view_count, ctr_percent, impression_count, snapshot_date "
        "FROM ctr_snapshots WHERE snapshot_date = ? AND is_valid = 1",
        (prev_date,)
    ).fetchall()

    return {r['video_id']: dict(r) for r in rows}


def get_latest_snapshot(conn: sqlite3.Connection) -> Dict[str, dict]:
    """Get the most recent snapshot (any date)."""
    row = conn.execute(
        "SELECT MAX(snapshot_date) FROM ctr_snapshots WHERE is_valid = 1"
    ).fetchone()

    latest_date = row[0] if row else None
    if not latest_date:
        return {}

    rows = conn.execute(
        "SELECT video_id, view_count, ctr_percent, impression_count, snapshot_date "
        "FROM ctr_snapshots WHERE snapshot_date = ? AND is_valid = 1",
        (latest_date,)
    ).fetchall()

    return {r['video_id']: dict(r) for r in rows}


def get_two_most_recent_snapshots(conn: sqlite3.Connection
                                  ) -> Tuple[Dict[str, dict], Dict[str, dict], str, str]:
    """
    Get the two most recent snapshot dates and their data.

    Returns (latest_data, previous_data, latest_date, previous_date).
    """
    dates = conn.execute(
        "SELECT DISTINCT snapshot_date FROM ctr_snapshots "
        "WHERE is_valid = 1 ORDER BY snapshot_date DESC LIMIT 2"
    ).fetchall()

    if len(dates) < 2:
        latest = get_latest_snapshot(conn)
        latest_date = dates[0][0] if dates else 'none'
        return latest, {}, latest_date, 'none'

    latest_date = dates[0][0]
    prev_date = dates[1][0]

    latest_rows = conn.execute(
        "SELECT video_id, view_count, ctr_percent, impression_count, snapshot_date "
        "FROM ctr_snapshots WHERE snapshot_date = ? AND is_valid = 1",
        (latest_date,)
    ).fetchall()

    prev_rows = conn.execute(
        "SELECT video_id, view_count, ctr_percent, impression_count, snapshot_date "
        "FROM ctr_snapshots WHERE snapshot_date = ? AND is_valid = 1",
        (prev_date,)
    ).fetchall()

    latest_data = {r['video_id']: dict(r) for r in latest_rows}
    prev_data = {r['video_id']: dict(r) for r in prev_rows}

    return latest_data, prev_data, latest_date, prev_date


def store_snapshot(conn: sqlite3.Connection, video_id: str,
                   views: int, snapshot_date: str,
                   ctr_percent: float = 0.0,
                   impression_count: int = 0) -> None:
    """Store a single video snapshot with optional CTR data.

    Args:
        conn: Database connection.
        video_id: YouTube video ID.
        views: Current view count.
        snapshot_date: Date string (YYYY-MM-DD).
        ctr_percent: CTR percentage from Analytics API (default 0.0 when unavailable).
        impression_count: Thumbnail impression count from Analytics API (default 0).
    """
    conn.execute(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, "
        " is_late_entry, recorded_at) "
        "VALUES (?, ?, ?, ?, ?, 0, ?)",
        (video_id, snapshot_date, ctr_percent, impression_count, views, snapshot_date)
    )


# =========================================================================
# API FETCH
# =========================================================================

REACH_JOB_REPORT_TYPE = 'channel_reach_basic_a1'


def _dedup_reports_by_interval(reports: list) -> list:
    """One report per reporting interval — the newest generated — newest date first.

    YouTube regenerates reach reports for the same day, so `reports` can hold
    several objects sharing a (startTime, endTime) interval. The aggregation loop
    SUMS impressions across whatever it's given, so feeding it duplicates double-
    counts: observed 2026-07 when #59's 30-day rolling impressions (20,919) came
    out ABOVE its lifetime Studio total (10,925) — physically impossible. Keep
    only the report with the latest createTime per interval before windowing.
    """
    by_interval: Dict[tuple, dict] = {}
    for r in reports:
        key = (r.get('startTime', ''), r.get('endTime', ''))
        prev = by_interval.get(key)
        if prev is None or r.get('createTime', '') > prev.get('createTime', ''):
            by_interval[key] = r
    return sorted(by_interval.values(), key=lambda r: r.get('endTime', ''), reverse=True)


def _load_studio_lifetime() -> Tuple[Dict[str, dict], Optional["date"]]:
    """Return ({video_id: {impressions}}, export_date) from the latest Studio
    import, or ({}, None) if none exists.

    Wired to the Studio importer (studio_ctr_imports/rows) once that lands. Until
    then it returns empty, so the lifetime comparison in take_snapshot skips
    gracefully while the internal invariants (non-negative, CTR range) still run.
    """
    try:
        from tools.youtube_analytics.store import AnalyticsStore
        with AnalyticsStore.open() as store:
            if hasattr(store, "latest_studio_lifetime"):
                return store.latest_studio_lifetime()
    except Exception as e:  # importer/table not present yet — skip, don't fail
        logger.debug("No Studio lifetime source available: %s", e)
    return {}, None


@dataclass
class ValidationResult:
    """Outcome of validating a rolling CTR map before it is snapshotted."""
    ok: bool
    failures: List[str]          # hard invariant breaches — abort the snapshot
    unverified: List[str]        # video_ids with no lifetime reference to check
    warnings: List[str]          # non-fatal (e.g. stale Studio export skipped)


def validate_rolling_against_lifetime(
    rolling: Dict[str, dict],
    lifetime: Dict[str, dict],
    *,
    studio_as_of: "date",
    reporting_window_end: "date",
) -> ValidationResult:
    """Hard-guard the rolling CTR map before it is written.

    The invariant that matters: rolling (≤30-day) impressions can never exceed
    lifetime impressions. When it does, the collector is double-counting (the
    2026-07 regression: #59 rolling 20,919 > lifetime 10,925). Integer counts,
    so no tolerance.

    The lifetime comparison is OPPORTUNISTIC — Studio exports are manual. It runs
    only when `studio_as_of >= reporting_window_end` (an older export can be
    legitimately overtaken by newer reporting and must not raise a false alarm);
    otherwise it is skipped with a warning. Videos absent from `lifetime` are
    reported `unverified`, never assumed valid or invalid.

    Internal invariants (always checked, no lifetime needed): non-negative
    impressions, CTR in [0, 100].
    """
    failures: List[str] = []
    unverified: List[str] = []
    warnings: List[str] = []

    for vid, d in rolling.items():
        imp = d.get('impression_count', 0)
        ctr = d.get('ctr_percent', 0.0)
        if imp < 0:
            failures.append(f"{vid}: negative impressions ({imp})")
        if not (0.0 <= ctr <= 100.0):
            failures.append(f"{vid}: CTR out of range ({ctr})")

    if studio_as_of < reporting_window_end:
        warnings.append(
            f"Studio export ({studio_as_of}) predates reporting window end "
            f"({reporting_window_end}); skipping lifetime comparison."
        )
    else:
        for vid, d in rolling.items():
            life = lifetime.get(vid)
            if life is None:
                unverified.append(vid)
                continue
            r_imp = d.get('impression_count', 0)
            l_imp = life.get('impression_count', life.get('impressions', 0))
            if r_imp > l_imp:
                failures.append(
                    f"{vid}: rolling impressions {r_imp} > lifetime {l_imp} "
                    "(collector double-count)"
                )

    return ValidationResult(
        ok=not failures, failures=failures, unverified=unverified, warnings=warnings,
    )


def fetch_ctr_from_reach_reports(video_ids: set) -> Dict[str, dict]:
    """
    Fetch CTR data from YouTube Reporting API reach reports.

    Downloads the most recent bulk CSV reports (channel_reach_basic_a1), each
    covering one day, and aggregates the 30 most recent (see report_list[:30]
    below) into an impression-weighted CTR per video. This is a ROLLING ~30-DAY
    figure, NOT lifetime — it moves as the window slides, so downstream must not
    treat it as a stable cumulative number.

    Returns dict of {video_id: {ctr_percent, impression_count}}.
    Returns empty dict if no reports are available yet.
    """
    import csv
    import io

    try:
        reporting = get_authenticated_service('youtubereporting', 'v1')
    except Exception as e:
        logger.warning("Could not connect to Reporting API: %s", e)
        return {}

    # Find the reach report job
    jobs = reporting.jobs().list().execute()
    reach_job = None
    for j in jobs.get('jobs', []):
        if j['reportTypeId'] == REACH_JOB_REPORT_TYPE:
            reach_job = j
            break

    if not reach_job:
        logger.warning("No reach report job found. Create one with: "
                       "reporting.jobs().create(body={'reportTypeId': '%s', "
                       "'name': 'CTR Reach Report'})", REACH_JOB_REPORT_TYPE)
        return {}

    # List available reports, dedup by interval, sort newest date first
    reports = reporting.jobs().reports().list(jobId=reach_job['id']).execute()
    report_list = _dedup_reports_by_interval(reports.get('reports', []))

    if not report_list:
        logger.info("No reach reports available yet (job created recently, "
                     "reports generate within 24-48h)")
        return {}

    # Download the most recent reports (up to 30 days for aggregation)
    # Each report covers one day of data
    impressions_by_video: Dict[str, int] = {}
    clicks_by_video: Dict[str, int] = {}
    reports_downloaded = 0

    for report in report_list[:30]:
        try:
            url = report['downloadUrl']
            response = reporting._http.request(url)
            if response[0].status != 200:
                logger.warning("Failed to download report: HTTP %d", response[0].status)
                continue

            content = response[1].decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))

            for row in reader:
                vid = row.get('video_id', '')
                if vid not in video_ids:
                    continue

                imps = int(row.get('video_thumbnail_impressions', 0))
                ctr_rate = float(row.get('video_thumbnail_impressions_ctr', 0))

                impressions_by_video[vid] = impressions_by_video.get(vid, 0) + imps
                # Accumulate clicks (impressions * ctr) for weighted average
                clicks = int(round(imps * ctr_rate))
                clicks_by_video[vid] = clicks_by_video.get(vid, 0) + clicks

            reports_downloaded += 1
        except Exception as e:
            logger.warning("Error processing report: %s", e)
            continue

    logger.info("Downloaded %d reach reports, found CTR for %d videos",
                reports_downloaded, len(impressions_by_video))

    # Compute weighted average CTR per video
    ctr_map: Dict[str, dict] = {}
    for vid in impressions_by_video:
        total_imps = impressions_by_video[vid]
        total_clicks = clicks_by_video.get(vid, 0)

        if total_imps > 0:
            ctr_pct = round((total_clicks / total_imps) * 100, 2)
        else:
            ctr_pct = 0.0

        ctr_map[vid] = {
            'ctr_percent': ctr_pct,
            'impression_count': total_imps,
        }

    return ctr_map


def fetch_view_counts(video_ids: List[str]) -> Dict[str, int]:
    """
    Fetch current view counts via YouTube Data API v3 (statistics).

    Batches 50 at a time. Much faster than Analytics API per-video queries.

    Returns dict of {video_id: view_count}.
    """
    yt = get_authenticated_service('youtube', 'v3')
    result = {}

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        resp = yt.videos().list(
            part='statistics',
            id=','.join(batch)
        ).execute()

        for item in resp.get('items', []):
            stats = item.get('statistics', {})
            result[item['id']] = int(stats.get('viewCount', 0))

    logger.info("Fetched view counts for %d / %d videos", len(result), len(video_ids))
    return result


# =========================================================================
# SNAPSHOT + COMPARISON
# =========================================================================

def take_snapshot() -> Tuple[int, str]:
    """
    Take a new snapshot: fetch all video IDs, get view counts + CTR, store.

    Fetches real CTR and impression data from the YouTube Analytics API for
    each long-form video. Videos where CTR is unavailable still get view_count
    snapshots with ctr_percent=0. Individual video API errors do not abort the run.

    Returns (count_stored, snapshot_date).
    """
    today = date.today().isoformat()
    conn = _get_db()

    # Check if we already have a snapshot for today
    existing = conn.execute(
        "SELECT COUNT(*) FROM ctr_snapshots WHERE snapshot_date = ?",
        (today,)
    ).fetchone()[0]

    if existing > 0:
        logger.warning("Snapshot already exists for %s (%d rows). Skipping.",
                        today, existing)
        conn.close()
        return existing, today

    # Fetch video IDs and metadata (long-form only)
    logger.info("Fetching video catalog from YouTube API...")
    all_ids = fetch_all_video_ids()
    videos = fetch_video_metadata(all_ids)
    longform_ids = [v['id'] for v in videos]

    if not longform_ids:
        logger.error("No long-form videos found")
        conn.close()
        return 0, today

    # Fetch view counts via Data API (fast batch)
    logger.info("Fetching view counts for %d long-form videos...", len(longform_ids))
    view_counts = fetch_view_counts(longform_ids)

    # Fetch CTR metrics from Reporting API bulk reports
    logger.info("Fetching CTR from Reporting API reach reports...")
    ctr_map = fetch_ctr_from_reach_reports(set(longform_ids))

    # Guard: never write a snapshot that fails the invariants. Validate BEFORE
    # any insert so the "today already exists" guard can't lock a broken snapshot
    # in place (a partial insert would block the next clean run).
    lifetime, studio_as_of_raw = _load_studio_lifetime()
    # latest_studio_lifetime returns exported_at as a stored string; the validator
    # compares dates, so coerce here at the seam.
    try:
        studio_as_of = date.fromisoformat(studio_as_of_raw) if studio_as_of_raw else date.today()
    except (TypeError, ValueError):
        studio_as_of = date.today()
    validation = validate_rolling_against_lifetime(
        ctr_map, lifetime,
        studio_as_of=studio_as_of,
        reporting_window_end=date.today(),
    )
    for w in validation.warnings:
        logger.warning("CTR validation: %s", w)
    if not validation.ok:
        for f in validation.failures:
            logger.error("CTR validation FAILED: %s", f)
        logger.error("Aborting snapshot for %s — no rows written.", today)
        conn.close()
        return 0, today

    # Store snapshots with CTR data where available
    stored = 0
    for vid, views in view_counts.items():
        ctr_data = ctr_map.get(vid, {})
        store_snapshot(
            conn, vid, views, today,
            ctr_percent=ctr_data.get('ctr_percent', 0.0),
            impression_count=ctr_data.get('impression_count', 0),
        )
        stored += 1

    conn.commit()
    conn.close()

    logger.info("Stored %d video snapshots for %s", stored, today)

    # End-of-run summary
    ctr_fetched = len(ctr_map)
    ctr_total = len(longform_ids)
    pattern_scores = get_pattern_ctr_from_db(str(DB_PATH))

    if pattern_scores:
        scores_str = ", ".join(f"{k}={v}" for k, v in sorted(pattern_scores.items()))
        print(f"CTR updated for {ctr_fetched}/{ctr_total} videos. "
              f"Title scorer now using DB-enriched scores: {scores_str}")
    else:
        print(f"CTR updated for {ctr_fetched}/{ctr_total} videos. "
              f"Title scorer using static scores (insufficient DB data).")

    if ctr_fetched == 0:
        print("Note: Reporting API reach reports may take 24-48h to generate after job creation.")

    return stored, today


def compare_snapshots(latest: Dict[str, dict], previous: Dict[str, dict]
                      ) -> Dict[str, List[dict]]:
    """
    Compare two snapshots and flag significant changes.

    Returns dict with keys:
      - 'velocity_drop': videos where view velocity dropped >50%
      - 'velocity_surge': videos where view velocity increased >100%
      - 'dead_weight': videos with zero new views
      - 'all': all videos with computed velocity
    """
    if not previous:
        return {'velocity_drop': [], 'velocity_surge': [],
                'dead_weight': [], 'all': []}

    # We need a THIRD snapshot (the one before previous) to compare velocities.
    # Without it, we can only compute velocity = latest_views - previous_views.
    # That's the primary metric.
    results = {
        'velocity_drop': [],
        'velocity_surge': [],
        'dead_weight': [],
        'all': [],
    }

    # Compute velocity for each video present in both snapshots
    common_ids = set(latest.keys()) & set(previous.keys())

    for vid in common_ids:
        curr_views = latest[vid]['view_count']
        prev_views = previous[vid]['view_count']
        velocity = curr_views - prev_views

        entry = {
            'video_id': vid,
            'current_views': curr_views,
            'previous_views': prev_views,
            'velocity': velocity,
        }
        results['all'].append(entry)

        if velocity == 0:
            results['dead_weight'].append(entry)

    # Sort all by velocity descending
    results['all'].sort(key=lambda x: x['velocity'], reverse=True)

    # For velocity_drop / velocity_surge, we need the snapshot BEFORE previous
    # to compute velocity change. Pull from DB.
    conn = _get_db()
    prev_date = next(iter(previous.values()), {}).get('snapshot_date')
    if prev_date:
        older = get_previous_snapshot(conn, prev_date)
        if older:
            for vid in common_ids:
                if vid not in older:
                    continue

                old_views = older[vid]['view_count']
                prev_views = previous[vid]['view_count']
                curr_views = latest[vid]['view_count']

                old_velocity = prev_views - old_views
                new_velocity = curr_views - prev_views

                if old_velocity > 0:
                    pct_change = ((new_velocity - old_velocity) / old_velocity) * 100

                    entry = {
                        'video_id': vid,
                        'current_views': curr_views,
                        'old_velocity': old_velocity,
                        'new_velocity': new_velocity,
                        'pct_change': pct_change,
                    }

                    if pct_change <= -50:
                        results['velocity_drop'].append(entry)
                    elif pct_change >= 100:
                        results['velocity_surge'].append(entry)

    conn.close()

    # Sort flags by magnitude
    results['velocity_drop'].sort(key=lambda x: x['pct_change'])
    results['velocity_surge'].sort(key=lambda x: x['pct_change'], reverse=True)

    return results


# =========================================================================
# TITLE LOOKUP
# =========================================================================

def get_video_titles(video_ids: List[str]) -> Dict[str, str]:
    """Look up video titles from analytics.db, falling back to API."""
    from tools.youtube_analytics.growth_data import DB_PATH as ANALYTICS_DB
    from tools.youtube_analytics.store import AnalyticsStore

    if not ANALYTICS_DB.exists() or not video_ids:
        return {}
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        return {vid: r['title'] for vid, r in store.videos_by_id(video_ids).items()}


# =========================================================================
# REPORT
# =========================================================================

def print_report(results: Dict[str, List[dict]],
                 latest_date: str, prev_date: str) -> None:
    """Print the comparison report to stdout."""
    # Collect all video IDs for title lookup
    all_ids = list({e['video_id'] for e in results['all']})
    titles = get_video_titles(all_ids) if all_ids else {}

    def title(vid: str) -> str:
        t = (titles.get(vid, vid))[:50]
        # Replace non-ASCII chars that crash Windows cp1252 console
        return t.encode('ascii', errors='replace').decode('ascii')

    print()
    print("=" * 70)
    print(f"  VIEW VELOCITY REPORT")
    print(f"  Comparing: {prev_date} -> {latest_date}")
    print("=" * 70)

    # Velocity surge
    surges = results['velocity_surge']
    if surges:
        print(f"\n  MOMENTUM (velocity up >100%) [{len(surges)} videos]")
        print("  " + "-" * 66)
        for e in surges[:10]:
            print(f"  +{e['pct_change']:>6.0f}%  vel {e['old_velocity']:>6} -> {e['new_velocity']:>6}  {title(e['video_id'])}")
    else:
        print("\n  MOMENTUM: none")

    # Velocity drop
    drops = results['velocity_drop']
    if drops:
        print(f"\n  ALGORITHM PULLBACK (velocity down >50%) [{len(drops)} videos]")
        print("  " + "-" * 66)
        for e in drops[:10]:
            print(f"  {e['pct_change']:>7.0f}%  vel {e['old_velocity']:>6} -> {e['new_velocity']:>6}  {title(e['video_id'])}")
    else:
        print("\n  ALGORITHM PULLBACK: none")

    # Dead weight
    dead = results['dead_weight']
    if dead:
        print(f"\n  DEAD WEIGHT (0 new views) [{len(dead)} videos]")
        print("  " + "-" * 66)
        for e in dead[:10]:
            print(f"    {e['current_views']:>8} total views  {title(e['video_id'])}")
        if len(dead) > 10:
            print(f"    ... and {len(dead) - 10} more")
    else:
        print("\n  DEAD WEIGHT: none")

    # Top movers
    all_sorted = results['all']
    if all_sorted:
        top_n = min(10, len(all_sorted))
        print(f"\n  TOP {top_n} BY VIEW VELOCITY")
        print("  " + "-" * 66)
        print(f"  {'Velocity':>10}  {'Total Views':>12}  {'Title'}")
        print("  " + "-" * 66)
        for e in all_sorted[:top_n]:
            print(f"  {e['velocity']:>+10,}  {e['current_views']:>12,}  {title(e['video_id'])}")

    total_velocity = sum(e['velocity'] for e in all_sorted)
    print(f"\n  Total velocity (all {len(all_sorted)} videos): {total_velocity:+,} views")
    print()


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Track view velocity across snapshots.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Examples:
  python -m tools.youtube_analytics.ctr_tracker              Take snapshot + report
  python -m tools.youtube_analytics.ctr_tracker --report-only  Compare existing snapshots

Scheduled execution (Windows Task Scheduler):
  schtasks /Create /TN "HistoryVsHype\CTRTracker" ^
    /TR "cmd /c cd /D \"D:\History vs Hype\" && python -m tools.youtube_analytics.ctr_tracker >> logs\ctr_tracker.log 2>&1" ^
    /SC WEEKLY /D MON /ST 09:00 /F

The scheduled task runs weekly on Monday at 09:00. OAuth token auto-refreshes
as long as the task runs at least once every 6 months. If the token expires,
run `python -m tools.youtube_analytics.auth` interactively to re-authorize.
        """
    )
    parser.add_argument(
        '--report-only', action='store_true',
        help='Only compare existing snapshots, do not fetch new data'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true",
                           help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true",
                           help="Only show errors on stderr")

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    conn = _get_db()

    if args.report_only:
        logger.info("Report-only mode: comparing existing snapshots")
        latest, previous, latest_date, prev_date = get_two_most_recent_snapshots(conn)
        conn.close()

        if not latest:
            print("No snapshots found. Run without --report-only first.")
            sys.exit(1)

        if not previous:
            print(f"Only one snapshot found ({latest_date}). Need at least 2 to compare.")
            sys.exit(1)

        results = compare_snapshots(latest, previous)
        print_report(results, latest_date, prev_date)
    else:
        # Take snapshot
        logger.info("Taking view count snapshot...")
        stored, today = take_snapshot()
        print(f"Snapshot: {stored} videos recorded for {today}")

        # Compare with previous
        conn = _get_db()
        latest_data = {}
        rows = conn.execute(
            "SELECT video_id, view_count, ctr_percent, impression_count, snapshot_date "
            "FROM ctr_snapshots WHERE snapshot_date = ? AND is_valid = 1",
            (today,)
        ).fetchall()
        latest_data = {r['video_id']: dict(r) for r in rows}

        previous = get_previous_snapshot(conn, today)
        conn.close()

        if not previous:
            print("First snapshot taken. Run again tomorrow to see velocity comparison.")
            sys.exit(0)

        prev_date = next(iter(previous.values()))['snapshot_date']
        results = compare_snapshots(latest_data, previous)
        print_report(results, today, prev_date)

    sys.exit(0)


if __name__ == '__main__':
    main()
