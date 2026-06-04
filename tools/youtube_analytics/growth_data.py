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
CURRENT_SCHEMA_VERSION = 2
MIN_DURATION_SECONDS = 180  # 3+ minutes = long-form

# Pre-channel personal/test uploads (2014) that pass the long-form duration
# filter but are not History vs Hype content. They skew retention-cliff and
# algorithm-reach tables. Excluded at fetch so the purge survives every refresh.
EXCLUDED_VIDEO_IDS = {
    '-EFfYT190ew',  # "vikinghordekamp Ksa oostende Essen (2005)"
    'exDA-YSe-nc',  # "vikinghordekamp Title2"
}


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

# Phase 60: retention curves, search terms, subscribed status
SCHEMA_V2 = """
CREATE TABLE IF NOT EXISTS retention_curves (
    video_id TEXT NOT NULL,
    elapsed_ratio REAL NOT NULL,         -- 0.00..1.00 (typically 100 buckets)
    audience_watch_ratio REAL NOT NULL,  -- 0..1+ (1.0 = 100% retained)
    relative_performance REAL,           -- vs similar videos (nullable)
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (video_id, elapsed_ratio)
);

CREATE TABLE IF NOT EXISTS search_terms (
    video_id TEXT NOT NULL,
    term TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    watch_time_minutes REAL DEFAULT 0,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (video_id, term)
);

CREATE TABLE IF NOT EXISTS subscribed_status (
    video_id TEXT NOT NULL,
    status TEXT NOT NULL,                -- 'SUBSCRIBED' or 'UNSUBSCRIBED'
    views INTEGER DEFAULT 0,
    watch_time_minutes REAL DEFAULT 0,
    avg_view_percentage REAL DEFAULT 0,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (video_id, status)
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
    """Create or migrate schema. Atomic — rolls back on failure.

    Migration ladder (idempotent):
      v0 -> v1: SCHEMA_V1 (videos, traffic_sources, daily_channel)
      v1 -> v2: SCHEMA_V2 (retention_curves, search_terms, subscribed_status)
    """
    current = conn.execute("PRAGMA user_version").fetchone()[0]

    if current >= CURRENT_SCHEMA_VERSION:
        return

    try:
        if current < 1:
            conn.executescript(SCHEMA_V1)
            logger.info("Schema migrated to version 1")
        if current < 2:
            conn.executescript(SCHEMA_V2)
            logger.info("Schema migrated to version 2 (retention_curves, search_terms, subscribed_status)")
        conn.execute(f"PRAGMA user_version = {CURRENT_SCHEMA_VERSION}")
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Schema migration failed: {e}") from e


# =========================================================================
# DATA API — VIDEO METADATA
# =========================================================================

def fetch_all_video_ids() -> List[str]:
    """Fetch all video IDs from channel via YouTube Data API v3.

    Uses the canonical "uploads playlist" pattern: channels.list(mine=True)
    to resolve the authenticated channel, then playlistItems.list on its
    uploads playlist. This is more reliable than search.list(forMine=True),
    which suffers from search-index propagation lag and can return 0 items
    for recently-published or recently-updated videos.

    Raises no exception when the token has no associated channel — logs a
    clear error and returns []. Callers that need to distinguish "no
    channel" from "empty channel" should check this log line.
    """
    yt = get_authenticated_service('youtube', 'v3')

    # Resolve the authenticated channel's uploads playlist ID.
    ch_resp = yt.channels().list(part='contentDetails', mine=True).execute()
    items = ch_resp.get('items', [])
    if not items:
        logger.error(
            "channels.list(mine=True) returned 0 channels — the OAuth token "
            "is not associated with any YouTube channel. Most likely cause: "
            "the token was minted against the wrong Google account during a "
            "recent re-auth, or the Brand Account grant was revoked. Fix: "
            "delete %s and re-run; the browser will prompt for re-auth — "
            "select the Google account that owns the History vs Hype channel.",
            "tools/youtube_analytics/credentials/token.json",
        )
        return []
    uploads_playlist_id = items[0]['contentDetails']['relatedPlaylists']['uploads']

    # Paginate uploads playlist for every video ID.
    all_ids: List[str] = []
    page = None
    while True:
        resp = yt.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=page,
        ).execute()
        all_ids.extend(item['contentDetails']['videoId'] for item in resp.get('items', []))
        page = resp.get('nextPageToken')
        if not page:
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
            if item['id'] in EXCLUDED_VIDEO_IDS:
                continue

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


def fetch_video_ctr_bulk(video_ids: Optional[List[str]] = None) -> Dict[str, Dict]:
    """
    Fetch CTR/impressions for videos via Analytics API.

    Tries the bulk path (dimensions=video) first. If that fails with 400
    "not supported", falls back to per-video queries (filters=video==<id>).

    For some channels (including this one as of 2026-05), the metric
    `videoThumbnailImpressions` is not exposed via the Analytics API at all
    — both bulk and per-video return the same "not supported" error. In
    that case CTR is owned by `tools.youtube_analytics.ctr_tracker`, which
    pulls reach reports from the YouTube *Reporting* API (a different
    endpoint) and writes to keywords.db.ctr_snapshots. We detect that
    condition and skip the per-video loop instead of spamming 60 identical
    400s, leaving CTR columns NULL in analytics.db.

    Args:
        video_ids: IDs to query in the per-video fallback. If None, only
            the bulk path is attempted.

    Returns dict keyed by video_id with impressions and ctr_percent.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    end = date.today().isoformat()
    bulk_unsupported = False

    try:
        resp = analytics.reports().query(
            ids='channel==MINE',
            startDate='2014-01-01',
            endDate=end,
            metrics='views,videoThumbnailImpressions,videoThumbnailImpressionsClickRate',
            dimensions='video',
            sort='-views',
            maxResults=200  # API limit for video dimension
        ).execute()

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

        if result:
            logger.info("Fetched CTR for %d videos (bulk)", len(result))
            return result
        logger.info("Bulk CTR query returned no rows — trying per-video fallback")
    except Exception as e:
        msg = str(e)
        if 'not supported' in msg.lower():
            bulk_unsupported = True
            logger.warning(
                "CTR metric not supported via Analytics API for this channel. "
                "Run `python -m tools.youtube_analytics.ctr_tracker` to populate "
                "CTR via the Reporting API instead. Skipping per-video fallback."
            )
        else:
            logger.warning("CTR bulk fetch failed, falling back to per-video: %s", e)

    if bulk_unsupported or not video_ids:
        return {}

    # Probe with the first video — if it returns "not supported", the metric
    # isn't enabled for this channel and the remaining N-1 calls will all fail
    # the same way. Stop early.
    result = {}
    for i, vid in enumerate(video_ids):
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=end,
                metrics='videoThumbnailImpressions,videoThumbnailImpressionsClickRate',
                filters=f'video=={vid}',
            ).execute()
            rows = resp.get('rows', [])
            if not rows:
                continue
            headers = [h['name'] for h in resp.get('columnHeaders', [])]
            data = dict(zip(headers, rows[0]))
            impressions = data.get('videoThumbnailImpressions')
            ctr_rate = data.get('videoThumbnailImpressionsClickRate')
            if impressions is not None and ctr_rate is not None:
                result[vid] = {
                    'impressions': int(impressions),
                    'ctr_percent': round(float(ctr_rate) * 100, 2),
                }
        except Exception as e:
            if i == 0 and 'not supported' in str(e).lower():
                logger.warning(
                    "Per-video CTR also not supported. Use ctr_tracker (Reporting "
                    "API) instead. Aborting CTR fetch."
                )
                return {}
            logger.warning("Per-video CTR fetch failed for %s: %s", vid, e)

    logger.info("Fetched CTR for %d / %d videos (per-video fallback)", len(result), len(video_ids))
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
# ANALYTICS API — RETENTION CURVES (per-video, 100 buckets)
# =========================================================================

def fetch_retention_curves(video_ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Fetch audience retention curves per video.

    Uses audienceType==ORGANIC to match retention.py's existing convention —
    filters out external traffic which skews curves. Returns up to 100 buckets
    per video (elapsedVideoTimeRatio 0.00..1.00).

    One API call per video. Returns dict keyed by video_id with list of
    {elapsed_ratio, audience_watch_ratio, relative_performance}.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    end = date.today().isoformat()
    result: Dict[str, List[Dict]] = {}

    for vid in video_ids:
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=end,
                metrics='audienceWatchRatio,relativeRetentionPerformance',
                dimensions='elapsedVideoTimeRatio',
                filters=f'video=={vid};audienceType==ORGANIC',
                maxResults=200,
                sort='elapsedVideoTimeRatio',
            ).execute()

            points = []
            for row in resp.get('rows', []):
                points.append({
                    'elapsed_ratio': float(row[0]),
                    'audience_watch_ratio': float(row[1]),
                    'relative_performance': float(row[2]) if len(row) > 2 and row[2] is not None else None,
                })
            if points:
                result[vid] = points
        except Exception as e:
            logger.warning("Retention curve fetch failed for %s: %s", vid, e)

    logger.info("Fetched retention curves for %d / %d videos", len(result), len(video_ids))
    return result


def store_retention_curves(curves: Dict[str, List[Dict]]) -> int:
    """Store retention curves via AnalyticsStore. Returns point count stored."""
    from tools.youtube_analytics.store import AnalyticsStore
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for vid, points in curves.items():
            for p in points:
                store.upsert_retention_point(
                    video_id=vid,
                    elapsed_ratio=p['elapsed_ratio'],
                    audience_watch_ratio=p['audience_watch_ratio'],
                    relative_performance=p['relative_performance'],
                    fetched_at=now,
                )
                stored += 1
        store.commit()

    logger.info("Stored %d retention curve points", stored)
    return stored


# =========================================================================
# ANALYTICS API — SEARCH TERMS (per-video YT_SEARCH detail)
# =========================================================================

def fetch_search_terms_per_video(video_ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Fetch top search queries driving traffic per video.

    One API call per video. Returns up to 25 terms per video, sorted by views.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    end = date.today().isoformat()
    result: Dict[str, List[Dict]] = {}

    for vid in video_ids:
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=end,
                metrics='views,estimatedMinutesWatched',
                dimensions='insightTrafficSourceDetail',
                filters=f'video=={vid};insightTrafficSourceType==YT_SEARCH',
                maxResults=25,
                sort='-views',
            ).execute()

            terms = []
            for row in resp.get('rows', []):
                terms.append({
                    'term': row[0],
                    'views': int(row[1]),
                    'watch_time_minutes': float(row[2]),
                })
            if terms:
                result[vid] = terms
        except Exception as e:
            logger.warning("Search term fetch failed for %s: %s", vid, e)

    total_terms = sum(len(v) for v in result.values())
    logger.info("Fetched %d search terms across %d / %d videos", total_terms, len(result), len(video_ids))
    return result


def store_search_terms(terms: Dict[str, List[Dict]]) -> int:
    """Store per-video search terms via AnalyticsStore. Returns row count stored."""
    from tools.youtube_analytics.store import AnalyticsStore
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for vid, term_rows in terms.items():
            for t in term_rows:
                store.upsert_search_term(
                    video_id=vid,
                    term=t['term'],
                    views=t['views'],
                    watch_time_minutes=t['watch_time_minutes'],
                    fetched_at=now,
                )
                stored += 1
        store.commit()

    logger.info("Stored %d search term rows", stored)
    return stored


# =========================================================================
# ANALYTICS API — SUBSCRIBED STATUS (per-video sub vs non-sub split)
# =========================================================================

def fetch_subscribed_status_per_video(video_ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Fetch view/retention split by subscribed status per video.

    Returns up to 2 rows per video: SUBSCRIBED and UNSUBSCRIBED.
    Tells you whether the algorithm is amplifying to new audience (UNSUBSCRIBED
    share high = good for reach) or recycling existing subs.
    """
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    end = date.today().isoformat()
    result: Dict[str, List[Dict]] = {}

    for vid in video_ids:
        try:
            resp = analytics.reports().query(
                ids='channel==MINE',
                startDate='2014-01-01',
                endDate=end,
                metrics='views,estimatedMinutesWatched,averageViewPercentage',
                dimensions='subscribedStatus',
                filters=f'video=={vid}',
            ).execute()

            rows_out = []
            for row in resp.get('rows', []):
                rows_out.append({
                    'status': row[0],
                    'views': int(row[1]),
                    'watch_time_minutes': float(row[2]),
                    'avg_view_percentage': float(row[3]),
                })
            if rows_out:
                result[vid] = rows_out
        except Exception as e:
            logger.warning("Subscribed status fetch failed for %s: %s", vid, e)

    logger.info("Fetched subscribed-status for %d / %d videos", len(result), len(video_ids))
    return result


def store_subscribed_status(status_data: Dict[str, List[Dict]]) -> int:
    """Store per-video subscribed-status rows via AnalyticsStore. Returns count."""
    from tools.youtube_analytics.store import AnalyticsStore
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for vid, rows in status_data.items():
            for r in rows:
                store.upsert_subscribed_status(
                    video_id=vid,
                    status=r['status'],
                    views=r['views'],
                    watch_time_minutes=r['watch_time_minutes'],
                    avg_view_percentage=r['avg_view_percentage'],
                    fetched_at=now,
                )
                stored += 1
        store.commit()

    logger.info("Stored %d subscribed-status rows", stored)
    return stored


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

def store_videos(videos: List[Dict],
                 metrics: Dict[str, Dict], ctr_data: Dict[str, Dict]) -> int:
    """Store video metadata + metrics via AnalyticsStore. Returns count stored."""
    from tools.youtube_analytics.store import AnalyticsStore, VideoRow
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for v in videos:
            vid = v['id']
            m = metrics.get(vid, {})
            c = ctr_data.get(vid, {})
            topic = classify_title(v['title'])

            store.upsert_video(VideoRow(
                video_id=vid,
                title=v['title'],
                published_at=v['published_at'],
                duration_seconds=v['duration_seconds'],
                fetched_at=now,
                tags=v['tags'],
                views=m.get('views', 0),
                watch_time_minutes=m.get('watch_time_minutes', 0),
                avg_view_duration_seconds=m.get('avg_view_duration_seconds', 0),
                avg_view_percentage=m.get('avg_view_percentage', 0),
                likes=m.get('likes', 0),
                comments=m.get('comments', 0),
                shares=m.get('shares', 0),
                subscribers_gained=m.get('subscribers_gained', 0),
                # subscribers_lost not available per-video — VideoRow default 0
                impressions=c.get('impressions'),
                ctr_percent=c.get('ctr_percent'),
                topic_type=topic,
                metrics_fetched_at=now if m else None,
            ))
            stored += 1
        store.commit()

    logger.info("Stored %d videos", stored)
    return stored


def store_traffic_sources(traffic: Dict[str, List[Dict]]) -> int:
    """Store per-video traffic source data via AnalyticsStore. Returns count stored.

    Uses AnalyticsStore.upsert_traffic_source — the seam introduced in
    ADR-0004 stage 3.1. All three growth_data writers (store_videos,
    store_traffic_sources, store_daily_metrics) now route through the
    store.
    """
    from tools.youtube_analytics.store import AnalyticsStore
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for vid, sources in traffic.items():
            for src in sources:
                store.upsert_traffic_source(
                    video_id=vid,
                    source_type=src['source_type'],
                    views=src['views'],
                    watch_time_minutes=src['watch_time_minutes'],
                    fetched_at=now,
                )
                stored += 1
        store.commit()

    logger.info("Stored %d traffic source records", stored)
    return stored


def store_daily_metrics(days: List[Dict]) -> int:
    """Store daily channel metrics via AnalyticsStore. Returns count stored."""
    from tools.youtube_analytics.store import AnalyticsStore
    now = datetime.now(timezone.utc).isoformat()
    stored = 0

    with AnalyticsStore.open() as store:
        for d in days:
            store.upsert_daily_metric(
                day=d['day'],
                views=d['views'],
                watch_time_minutes=d['watch_time_minutes'],
                avg_view_duration_seconds=d['avg_view_duration_seconds'],
                subscribers_gained=d['subscribers_gained'],
                subscribers_lost=d['subscribers_lost'],
                likes=d['likes'],
                fetched_at=now,
            )
            stored += 1
        store.commit()

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
        'retention_points': 0,
        'search_term_rows': 0,
        'subscribed_status_rows': 0,
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
        ctr_data = fetch_video_ctr_bulk(longform_ids)

        # Step 4: Store videos + metrics
        logger.info("Step 4: Storing videos and metrics")
        results['videos_stored'] = store_videos(videos, metrics, ctr_data)

        # Step 5: Fetch traffic sources per video
        logger.info("Step 5: Fetching traffic sources per video (%d videos)", len(longform_ids))
        traffic = fetch_traffic_sources_per_video(longform_ids)
        results['traffic_records'] = store_traffic_sources(traffic)

        # Step 6: Fetch daily channel metrics (90 days)
        logger.info("Step 6: Fetching daily channel metrics (90 days)")
        daily = fetch_daily_channel_metrics(days=90)
        results['daily_records'] = store_daily_metrics(daily)

        # Step 7: Retention curves per video
        logger.info("Step 7: Fetching retention curves (%d videos)", len(longform_ids))
        curves = fetch_retention_curves(longform_ids)
        results['retention_points'] = store_retention_curves(curves)

        # Step 8: Search terms per video
        logger.info("Step 8: Fetching search terms per video (%d videos)", len(longform_ids))
        terms = fetch_search_terms_per_video(longform_ids)
        results['search_term_rows'] = store_search_terms(terms)

        # Step 9: Subscribed-status split per video
        logger.info("Step 9: Fetching subscribed-status split (%d videos)", len(longform_ids))
        sub_status = fetch_subscribed_status_per_video(longform_ids)
        results['subscribed_status_rows'] = store_subscribed_status(sub_status)

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
    print(f"  Retention points:   {result['retention_points']}")
    print(f"  Search term rows:   {result['search_term_rows']}")
    print(f"  Sub-status rows:    {result['subscribed_status_rows']}")

    if result['errors']:
        print(f"\n  Errors ({len(result['errors'])}):")
        for err in result['errors']:
            print(f"    - {err}")
        sys.exit(1)

    print()
    sys.exit(0)
