"""
Growth Data Foundation — YouTube Analytics API Backfill

Pulls all long-form video data directly from YouTube APIs into analytics.db.
This is the data foundation for v5.2 Growth Engine (Phases 56-59).

Three data sources:
  1. YouTube Data API v3 — video metadata (title, publish date, duration, tags)
  2. YouTube Analytics API v2 — per-video metrics (views, retention, subs, watch time)
  3. YouTube Analytics API v2 — per-video traffic sources (search, suggested, browse)

Schema: analytics.db with 3 tables (videos, traffic_sources, daily_channel)
  - PRAGMA user_version tracks schema version
  - All migrations are atomic (transaction-wrapped)

Usage:
    python -m tools.youtube_analytics.growth_data                # Full backfill
    python -m tools.youtube_analytics.growth_data --refresh      # Update existing data
    python -m tools.youtube_analytics.growth_data --video VIDEO_ID  # Single video

Dependencies:
    - google-api-python-client, google-auth-oauthlib (YouTube API)
    - tools.youtube_analytics.auth (OAuth2)
"""

import re
import sys
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, date, timezone, timedelta
from typing import Dict, List, Any, Optional

from tools.logging_config import get_logger
from tools.youtube_analytics.auth import get_authenticated_service

logger = get_logger(__name__)

DB_PATH = Path(__file__).parent / 'analytics.db'
CURRENT_SCHEMA_VERSION = 1
MIN_DURATION_SECONDS = 180  # 3+ minutes = long-form


# =========================================================================
# DATABASE SCHEMA
# =========================================================================

SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS videos (
    video_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    published_at TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    tags TEXT,  -- JSON array

    -- Metrics from YouTube Analytics API
    views INTEGER DEFAULT 0,
    watch_time_minutes REAL DEFAULT 0,
    avg_view_duration_seconds INTEGER DEFAULT 0,
    avg_view_percentage REAL DEFAULT 0,  -- retention as percentage (e.g. 35.3)
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    subscribers_gained INTEGER DEFAULT 0,
    subscribers_lost INTEGER DEFAULT 0,

    -- CTR (from Analytics API)
    impressions INTEGER,
    ctr_percent REAL,

    -- Classification
    topic_type TEXT DEFAULT 'general',
    angles TEXT,  -- JSON array

    -- Tracking
    fetched_at TEXT NOT NULL,
    metrics_fetched_at TEXT
);

CREATE TABLE IF NOT EXISTS traffic_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    source_type TEXT NOT NULL,  -- YT_SEARCH, RELATED_VIDEO, SUBSCRIBER, etc.
    views INTEGER DEFAULT 0,
    watch_time_minutes REAL DEFAULT 0,
    fetched_at TEXT NOT NULL,
    UNIQUE(video_id, source_type)
);

CREATE TABLE IF NOT EXISTS daily_channel (
    day TEXT PRIMARY KEY,
    views INTEGER DEFAULT 0,
    watch_time_minutes REAL DEFAULT 0,
    avg_view_duration_seconds INTEGER DEFAULT 0,
    subscribers_gained INTEGER DEFAULT 0,
    subscribers_lost INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    fetched_at TEXT NOT NULL
);
"""


def _get_db(db_path: Path = None) -> sqlite3.Connection:
    """Get database connection with row factory and WAL mode."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Create or migrate schema. Atomic — rolls back on failure."""
    current = conn.execute("PRAGMA user_version").fetchone()[0]

    if current >= CURRENT_SCHEMA_VERSION:
        return

    try:
        conn.executescript(SCHEMA_V1)
        conn.execute(f"PRAGMA user_version = {CURRENT_SCHEMA_VERSION}")
        conn.commit()
        logger.info("Schema initialized to version %d", CURRENT_SCHEMA_VERSION)
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Schema migration failed: {e}") from e


# =========================================================================
# DATA API — VIDEO METADATA
# =========================================================================

def fetch_all_video_ids() -> List[str]:
    """Fetch all video IDs from channel via YouTube Data API v3."""
    yt = get_authenticated_service('youtube', 'v3')
    all_ids = []
    next_page = None

    while True:
        resp = yt.search().list(
            part='id',
            forMine=True,
            type='video',
            maxResults=50,
            pageToken=next_page,
            order='date'
        ).execute()

        all_ids.extend(item['id']['videoId'] for item in resp.get('items', []))
        next_page = resp.get('nextPageToken')
        if not next_page:
            break

    logger.info("Found %d total videos on channel", len(all_ids))
    return all_ids


def fetch_video_metadata(video_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch metadata for videos via Data API v3. Filters to long-form only.

    Returns list of dicts with: id, title, published_at, duration_seconds, tags
    """
    yt = get_authenticated_service('youtube', 'v3')
    longform = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        resp = yt.videos().list(
            part='contentDetails,snippet',
            id=','.join(batch)
        ).execute()

        for item in resp.get('items', []):
            dur = item['contentDetails']['duration']
            m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur)
            if not m:
                continue

            secs = (int(m.group(1) or 0) * 3600 +
                    int(m.group(2) or 0) * 60 +
                    int(m.group(3) or 0))

            if secs < MIN_DURATION_SECONDS:
                continue

            snippet = item['snippet']
            longform.append({
                'id': item['id'],
                'title': snippet['title'],
                'published_at': snippet['publishedAt'],
                'duration_seconds': secs,
                'tags': json.dumps(snippet.get('tags', [])),
            })

    logger.info("Found %d long-form videos (3+ min)", len(longform))
    return longform


# =========================================================================
# ANALYTICS API — PER-VIDEO METRICS
# =========================================================================

def fetch_video_metrics_bulk(video_ids: List[str]) -> Dict[str, Dict]:
    """
    Fetch metrics for specific videos via Analytics API v2.

    Uses per-video filter to ensure we get data for all long-form videos,
    not just the top 200 by views (which mixes in shorts).

    Args:
        video_ids: List of video IDs to fetch metrics for

    Returns dict keyed by video_id with metrics.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    result = {}
    metrics_str = ','.join([
        'views', 'estimatedMinutesWatched', 'averageViewDuration',
        'averageViewPercentage', 'subscribersGained',
        'likes', 'comments', 'shares',
    ])

    for vid in video_ids:
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=date.today().isoformat(),
                metrics=metrics_str,
                filters=f'video=={vid}',
            ).execute()

            rows = resp.get('rows', [])
            if not rows:
                continue

            headers = [h['name'] for h in resp.get('columnHeaders', [])]
            data = dict(zip(headers, rows[0]))

            result[vid] = {
                'views': int(data.get('views', 0)),
                'watch_time_minutes': float(data.get('estimatedMinutesWatched', 0)),
                'avg_view_duration_seconds': int(data.get('averageViewDuration', 0)),
                'avg_view_percentage': float(data.get('averageViewPercentage', 0)),
                'subscribers_gained': int(data.get('subscribersGained', 0)),
                'likes': int(data.get('likes', 0)),
                'comments': int(data.get('comments', 0)),
                'shares': int(data.get('shares', 0)),
            }
        except Exception as e:
            logger.warning("Metrics fetch failed for %s: %s", vid, e)

    logger.info("Fetched metrics for %d / %d videos", len(result), len(video_ids))
    return result


def fetch_video_ctr_bulk() -> Dict[str, Dict]:
    """
    Fetch CTR/impressions for all videos via Analytics API.

    Returns dict keyed by video_id with impressions and ctr_percent.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    try:
        resp = analytics.reports().query(
            ids='channel==MINE',
            startDate='2014-01-01',
            endDate=date.today().isoformat(),
            metrics='views,videoThumbnailImpressions,videoThumbnailImpressionsClickRate',
            dimensions='video',
            sort='-views',
            maxResults=200  # API limit for video dimension
        ).execute()
    except Exception as e:
        logger.warning("CTR bulk fetch failed (expected for some channels): %s", e)
        return {}

    headers = [h['name'] for h in resp.get('columnHeaders', [])]
    result = {}

    for row in resp.get('rows', []):
        data = dict(zip(headers, row))
        vid = data['video']
        impressions = data.get('videoThumbnailImpressions')
        ctr_rate = data.get('videoThumbnailImpressionsClickRate')

        if impressions is not None and ctr_rate is not None:
            result[vid] = {
                'impressions': int(impressions),
                'ctr_percent': round(float(ctr_rate) * 100, 2),
            }

    logger.info("Fetched CTR for %d videos", len(result))
    return result


# =========================================================================
# ANALYTICS API — TRAFFIC SOURCES
# =========================================================================

def fetch_traffic_sources_per_video(video_ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Fetch traffic source breakdown per video.

    The Analytics API doesn't support video+trafficSource combined dimension
    in a single query, so we fetch per-video. To manage quota, we batch
    up to 50 video IDs per filter.

    Returns dict keyed by video_id with list of {source_type, views, watch_time_minutes}.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    result = {}

    for vid in video_ids:
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=date.today().isoformat(),
                metrics='views,estimatedMinutesWatched',
                dimensions='insightTrafficSourceType',
                filters=f'video=={vid}',
            ).execute()

            headers = [h['name'] for h in resp.get('columnHeaders', [])]
            sources = []
            for row in resp.get('rows', []):
                data = dict(zip(headers, row))
                sources.append({
                    'source_type': data['insightTrafficSourceType'],
                    'views': int(data.get('views', 0)),
                    'watch_time_minutes': float(data.get('estimatedMinutesWatched', 0)),
                })
            result[vid] = sources

        except Exception as e:
            logger.warning("Traffic source fetch failed for %s: %s", vid, e)
            result[vid] = []

    logger.info("Fetched traffic sources for %d videos", len(result))
    return result


# =========================================================================
# ANALYTICS API — DAILY CHANNEL METRICS
# =========================================================================

def fetch_daily_channel_metrics(days: int = 90) -> List[Dict]:
    """Fetch daily channel-level metrics for the last N days."""
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    start = (date.today() - timedelta(days=days)).isoformat()
    end = date.today().isoformat()

    resp = analytics.reports().query(
        ids='channel==MINE',
        startDate=start,
        endDate=end,
        metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes',
        dimensions='day',
        sort='day'
    ).execute()

    headers = [h['name'] for h in resp.get('columnHeaders', [])]
    rows = []
    for row in resp.get('rows', []):
        data = dict(zip(headers, row))
        rows.append({
            'day': data['day'],
            'views': int(data.get('views', 0)),
            'watch_time_minutes': float(data.get('estimatedMinutesWatched', 0)),
            'avg_view_duration_seconds': int(data.get('averageViewDuration', 0)),
            'subscribers_gained': int(data.get('subscribersGained', 0)),
            'subscribers_lost': int(data.get('subscribersLost', 0)),
            'likes': int(data.get('likes', 0)),
        })

    logger.info("Fetched %d days of channel metrics", len(rows))
    return rows


# =========================================================================
# TOPIC CLASSIFICATION
# =========================================================================

TOPIC_RULES = {
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'sovereignty',
                     'bir tawil', 'essequibo', 'bermeja', 'gibraltar', 'treaty', 'icj',
                     'disappear', 'islands', 'wall', 'divided', 'cyprus', 'kashmir',
                     'ukraine', 'taiwan', 'china sea', 'morocco', 'map', 'ceuta',
                     'melilla', 'belize', 'guatemala', 'guyana', 'venezuela',
                     'somaliland', 'chagos', 'turkey', 'greece'],
    'ideological': ['myth', 'dark ages', 'flat earth', 'propaganda', 'narrative',
                    'debunk', 'fact-check', 'lie', 'misconception', 'hero',
                    'weaponized', 'christmas', 'sol invictus', 'stalin', 'putin',
                    'communism', 'crusade'],
    'colonial': ['colonial', 'colony', 'empire', 'independence', 'decolonization',
                 'protectorate', 'french control', 'stock exchange', 'emptied',
                 'haiti', 'condor', 'coup', 'cia'],
    'legal': ['constitution', 'statute', 'legislation', 'referendum', 'clause',
              'article', 'court', 'ruling', 'legal', 'loophole', 'provision',
              'vichy', 'recopilación', 'wuchale'],
    'factcheck': ['fact-check', 'fact check', 'claims', 'checking', 'fuentes', 'vance'],
}


def classify_title(title: str) -> str:
    """Classify a video title into a topic type."""
    if not title:
        return 'general'
    t = title.lower()
    for topic, keywords in TOPIC_RULES.items():
        if any(kw in t for kw in keywords):
            return topic
    return 'general'


# =========================================================================
# DATABASE STORAGE
# =========================================================================

def store_videos(conn: sqlite3.Connection, videos: List[Dict],
                 metrics: Dict[str, Dict], ctr_data: Dict[str, Dict]) -> int:
    """Store video metadata + metrics in analytics.db. Returns count stored."""
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    for v in videos:
        vid = v['id']
        m = metrics.get(vid, {})
        c = ctr_data.get(vid, {})
        topic = classify_title(v['title'])

        conn.execute("""
            INSERT OR REPLACE INTO videos (
                video_id, title, published_at, duration_seconds, tags,
                views, watch_time_minutes, avg_view_duration_seconds,
                avg_view_percentage, likes, comments, shares,
                subscribers_gained, subscribers_lost,
                impressions, ctr_percent,
                topic_type, fetched_at, metrics_fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vid, v['title'], v['published_at'], v['duration_seconds'], v['tags'],
            m.get('views', 0), m.get('watch_time_minutes', 0),
            m.get('avg_view_duration_seconds', 0), m.get('avg_view_percentage', 0),
            m.get('likes', 0), m.get('comments', 0), m.get('shares', 0),
            m.get('subscribers_gained', 0), 0,  # subscribers_lost not available per-video
            c.get('impressions'), c.get('ctr_percent'),
            topic, now, now if m else None
        ))
        stored += 1

    conn.commit()
    logger.info("Stored %d videos", stored)
    return stored


def store_traffic_sources(conn: sqlite3.Connection,
                          traffic: Dict[str, List[Dict]]) -> int:
    """Store per-video traffic source data. Returns count stored."""
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    for vid, sources in traffic.items():
        for src in sources:
            conn.execute("""
                INSERT OR REPLACE INTO traffic_sources
                (video_id, source_type, views, watch_time_minutes, fetched_at)
                VALUES (?, ?, ?, ?, ?)
            """, (vid, src['source_type'], src['views'],
                  src['watch_time_minutes'], now))
            stored += 1

    conn.commit()
    logger.info("Stored %d traffic source records", stored)
    return stored


def store_daily_metrics(conn: sqlite3.Connection, days: List[Dict]) -> int:
    """Store daily channel metrics. Returns count stored."""
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    for d in days:
        conn.execute("""
            INSERT OR REPLACE INTO daily_channel
            (day, views, watch_time_minutes, avg_view_duration_seconds,
             subscribers_gained, subscribers_lost, likes, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (d['day'], d['views'], d['watch_time_minutes'],
              d['avg_view_duration_seconds'], d['subscribers_gained'],
              d['subscribers_lost'], d['likes'], now))
        stored += 1

    conn.commit()
    logger.info("Stored %d daily metrics", stored)
    return stored


# =========================================================================
# ORCHESTRATOR
# =========================================================================

def run_backfill(db_path: Path = None, refresh: bool = False,
                 single_video: str = None) -> Dict[str, Any]:
    """
    Full backfill pipeline: metadata → metrics → CTR → traffic → daily.

    Args:
        db_path: Override database path (for testing)
        refresh: If True, re-fetch all data even if present
        single_video: If set, only backfill this video ID

    Returns:
        Results dict with counts and any errors
    """
    conn = _get_db(db_path)
    ensure_schema(conn)

    results = {
        'videos_stored': 0,
        'traffic_records': 0,
        'daily_records': 0,
        'errors': [],
    }

    try:
        # Step 1: Get video IDs and metadata
        logger.info("Step 1: Fetching video metadata from Data API")
        if single_video:
            video_ids = [single_video]
        else:
            video_ids = fetch_all_video_ids()

        videos = fetch_video_metadata(video_ids)

        if not videos:
            results['errors'].append("No long-form videos found")
            return results

        longform_ids = [v['id'] for v in videos]

        # Step 2: Fetch metrics per video
        logger.info("Step 2: Fetching per-video metrics from Analytics API (%d videos)", len(longform_ids))
        metrics = fetch_video_metrics_bulk(longform_ids)

        # Step 3: Fetch CTR in bulk
        logger.info("Step 3: Fetching CTR data from Analytics API")
        ctr_data = fetch_video_ctr_bulk()

        # Step 4: Store videos + metrics
        logger.info("Step 4: Storing videos and metrics")
        results['videos_stored'] = store_videos(conn, videos, metrics, ctr_data)

        # Step 5: Fetch traffic sources per video
        logger.info("Step 5: Fetching traffic sources per video (%d videos)", len(longform_ids))
        traffic = fetch_traffic_sources_per_video(longform_ids)
        results['traffic_records'] = store_traffic_sources(conn, traffic)

        # Step 6: Fetch daily channel metrics (90 days)
        logger.info("Step 6: Fetching daily channel metrics (90 days)")
        daily = fetch_daily_channel_metrics(days=90)
        results['daily_records'] = store_daily_metrics(conn, daily)

    except Exception as e:
        results['errors'].append(f"Pipeline error: {e}")
        logger.error("Backfill failed: %s", e, exc_info=True)
    finally:
        conn.close()

    return results


# =========================================================================
# QUERY HELPERS (for downstream phases)
# =========================================================================

def get_all_videos(db_path: Path = None) -> List[Dict]:
    """Get all videos sorted by views descending."""
    conn = _get_db(db_path)
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM videos ORDER BY views DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_video_traffic(video_id: str, db_path: Path = None) -> List[Dict]:
    """Get traffic source breakdown for a video."""
    conn = _get_db(db_path)
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM traffic_sources WHERE video_id = ? ORDER BY views DESC",
        (video_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_daily_metrics(days: int = 30, db_path: Path = None) -> List[Dict]:
    """Get recent daily channel metrics."""
    conn = _get_db(db_path)
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM daily_channel ORDER BY day DESC LIMIT ?",
        (days,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_videos_by_topic(topic_type: str, db_path: Path = None) -> List[Dict]:
    """Get all videos of a specific topic type, sorted by views."""
    conn = _get_db(db_path)
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM videos WHERE topic_type = ? ORDER BY views DESC",
        (topic_type,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =========================================================================
# CLI
# =========================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Backfill analytics.db from YouTube APIs for growth analysis.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.growth_data              Full backfill
  python -m tools.youtube_analytics.growth_data --refresh    Re-fetch all data
  python -m tools.youtube_analytics.growth_data --video XYZ  Single video only

Output: tools/youtube_analytics/analytics.db
  - videos table: metadata + metrics + CTR + topic classification
  - traffic_sources table: per-video traffic source breakdown
  - daily_channel table: 90 days of channel-level metrics
        """
    )
    parser.add_argument(
        '--refresh', action='store_true',
        help='Re-fetch all data even if already present'
    )
    parser.add_argument(
        '--video', metavar='VIDEO_ID',
        help='Backfill a single video only'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true",
                          help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true",
                          help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    logger.info("Growth Data Backfill")
    logger.info("Database: %s", DB_PATH)

    result = run_backfill(
        refresh=args.refresh,
        single_video=args.video
    )

    print("=" * 60)
    print("Growth Data Backfill Complete")
    print("=" * 60)
    print(f"  Videos stored:      {result['videos_stored']}")
    print(f"  Traffic records:    {result['traffic_records']}")
    print(f"  Daily metrics:      {result['daily_records']}")

    if result['errors']:
        print(f"\n  Errors ({len(result['errors'])}):")
        for err in result['errors']:
            print(f"    - {err}")
        sys.exit(1)

    print()
    sys.exit(0)
