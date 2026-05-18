"""
Traffic Source Analysis Tool

Analyzes traffic source patterns and correlates them with video content types
(topic type, title pattern, duration, publication day).

Data sources:
  - analytics.db (videos table for metadata, traffic_sources table for cached data)
  - _traffic_sources.json (pre-fetched traffic source data)
  - YouTube Analytics API (fresh fetch via --fetch)

Usage:
    python -m tools.youtube_analytics.traffic_analysis --report      # Full report
    python -m tools.youtube_analytics.traffic_analysis --fetch       # Fetch fresh data
    python -m tools.youtube_analytics.traffic_analysis --video ID    # Single video
    python -m tools.youtube_analytics.traffic_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md
"""

import sys
import json
import sqlite3
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone, date
from statistics import mean, stdev
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
TRAFFIC_JSON = Path(__file__).parent / '_traffic_sources.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'TRAFFIC-SOURCE-ANALYSIS.md'

# Friendly names for traffic source types
SOURCE_LABELS = {
    'YT_SEARCH': 'YouTube Search',
    'RELATED_VIDEO': 'Suggested/Related',
    'SUBSCRIBER': 'Subscribers (Home)',
    'EXT_URL': 'External URLs',
    'NOTIFICATION': 'Notifications',
    'NO_LINK_OTHER': 'Direct/Other',
    'YT_CHANNEL': 'Channel Page',
    'YT_OTHER_PAGE': 'Other YT Pages',
    'PLAYLIST': 'Playlists',
    'SHORTS_CONTENT_LINKS': 'Shorts Links',
    'ANNOTATION': 'Annotations/Cards',
    'END_SCREEN': 'End Screens',
    'HASHTAGS': 'Hashtags',
    'CAMPAIGN_CARD': 'Campaign Cards',
    'PROMOTED': 'Promoted',
}

# Major sources to focus on (the rest are lumped as "Other")
MAJOR_SOURCES = [
    'YT_SEARCH', 'RELATED_VIDEO', 'SUBSCRIBER', 'EXT_URL',
    'NOTIFICATION', 'YT_CHANNEL', 'PLAYLIST', 'SHORTS_CONTENT_LINKS',
]

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# =========================================================================
# CLASSIFIERS
# =========================================================================

def classify_title_pattern(title: str) -> str:
    """Classify title into pattern categories matching title_scorer.py."""
    t = title.lower().strip()

    if " vs " in t or " versus " in t:
        return "versus"
    if " | " in t or ":" in t:
        return "colon"
    if t.startswith("how ") or t.startswith("why "):
        return "how_why"
    if (t.endswith("?") or t.startswith("what ") or t.startswith("who ")
            or t.startswith("where ") or t.startswith("when ")
            or t.startswith("did ") or t.startswith("was ")
            or t.startswith("were ")):
        return "question"
    return "declarative"


def classify_duration_bucket(seconds: int) -> str:
    """Bucket video duration for analysis."""
    if seconds < 300:
        return "short (<5m)"
    if seconds < 600:
        return "medium (5-10m)"
    if seconds < 900:
        return "long (10-15m)"
    return "very_long (15m+)"


# =========================================================================
# DATA LOADING
# =========================================================================

def load_traffic_from_json() -> Dict[str, List[dict]]:
    """Load traffic source data from the JSON cache file."""
    if not TRAFFIC_JSON.exists():
        logger.warning("No traffic sources JSON found at %s", TRAFFIC_JSON)
        return {}

    with open(TRAFFIC_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info("Loaded traffic data for %d videos from JSON cache", len(data))
    return data


def load_traffic_from_db() -> Dict[str, List[dict]]:
    """Load traffic source data from analytics.db traffic_sources table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        rows = store.traffic_sources()

    result: Dict[str, List[dict]] = defaultdict(list)
    for row in rows:
        result[row['video_id']].append({
            'source_type': row['source_type'],
            'views': row['views'],
            'watch_time_minutes': row['watch_time_minutes'],
        })

    logger.info("Loaded traffic data for %d videos from analytics.db", len(result))
    return dict(result)


def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found")
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    keep = ('video_id', 'title', 'published_at', 'duration_seconds',
            'views', 'watch_time_minutes', 'avg_view_percentage',
            'topic_type', 'impressions', 'ctr_percent', 'subscribers_gained')
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        rows = store.videos(min_duration_seconds=61)  # preserve old `> 60`

    result = {}
    for row in rows:
        vid = {k: row[k] for k in keep}
        # Enrich with derived fields
        vid['title_pattern'] = classify_title_pattern(vid['title'] or '')
        vid['duration_bucket'] = classify_duration_bucket(vid['duration_seconds'] or 0)

        # Parse publication day
        try:
            pub_date = datetime.fromisoformat(vid['published_at'].replace('Z', '+00:00'))
            vid['pub_day'] = DAY_NAMES[pub_date.weekday()]
        except (ValueError, AttributeError):
            vid['pub_day'] = 'Unknown'

        result[vid['video_id']] = vid

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


def merge_traffic_data(json_data: Dict, db_data: Dict) -> Dict[str, List[dict]]:
    """Merge traffic data from JSON and DB, preferring JSON (more recent)."""
    merged = dict(db_data)
    merged.update(json_data)  # JSON overwrites DB
    return merged


# =========================================================================
# API FETCH
# =========================================================================

def fetch_traffic_sources_api(video_ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
    """
    Fetch traffic source data from YouTube Analytics API.

    Args:
        video_ids: Specific video IDs to fetch. If None, fetches all from DB.

    Returns:
        Dict mapping video_id -> list of traffic source dicts.
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    if video_ids is None:
        metadata = load_video_metadata()
        video_ids = list(metadata.keys())

    logger.info("Fetching traffic sources for %d videos from API...", len(video_ids))
    result = {}

    for i, vid_id in enumerate(video_ids):
        try:
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate='2024-01-01',
                endDate='2026-12-31',
                metrics='views,estimatedMinutesWatched',
                dimensions='insightTrafficSourceType',
                filters=f'video=={vid_id}'
            ).execute()

            sources = []
            for row in response.get('rows', []):
                sources.append({
                    'source_type': row[0],
                    'views': int(row[1]),
                    'watch_time_minutes': float(row[2]),
                })

            result[vid_id] = sources
            if (i + 1) % 10 == 0:
                logger.info("  Fetched %d/%d videos", i + 1, len(video_ids))

        except Exception as e:
            logger.warning("Failed to fetch traffic for %s: %s", vid_id, e)

    logger.info("Fetched traffic data for %d videos", len(result))
    return result


def fetch_search_terms_api(video_id: str) -> List[dict]:
    """Fetch search terms driving traffic to a specific video."""
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    try:
        response = analytics.reports().query(
            ids='channel==MINE',
            startDate='2024-01-01',
            endDate='2026-12-31',
            metrics='views,estimatedMinutesWatched',
            dimensions='insightTrafficSourceDetail',
            filters=f'video=={video_id};insightTrafficSourceType==YT_SEARCH',
            maxResults=25,
            sort='-views'
        ).execute()

        terms = []
        for row in response.get('rows', []):
            terms.append({
                'term': row[0],
                'views': int(row[1]),
                'watch_time_minutes': float(row[2]),
            })
        return terms

    except Exception as e:
        logger.warning("Failed to fetch search terms for %s: %s", video_id, e)
        return []


def save_traffic_json(data: Dict[str, List[dict]]) -> None:
    """Save traffic data to JSON cache and to analytics.db."""
    # Save JSON
    with open(TRAFFIC_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("Saved traffic data to %s", TRAFFIC_JSON)

    # Upsert into analytics.db
    if not ANALYTICS_DB.exists():
        return

    now = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(str(ANALYTICS_DB))
    cur = conn.cursor()

    for vid_id, sources in data.items():
        for s in sources:
            cur.execute("""
                INSERT INTO traffic_sources (video_id, source_type, views, watch_time_minutes, fetched_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(video_id, source_type) DO UPDATE SET
                    views = excluded.views,
                    watch_time_minutes = excluded.watch_time_minutes,
                    fetched_at = excluded.fetched_at
            """, (vid_id, s['source_type'], s['views'], s['watch_time_minutes'], now))

    conn.commit()
    conn.close()
    logger.info("Upserted traffic data into analytics.db")


# =========================================================================
# ANALYSIS ENGINE
# =========================================================================

def compute_source_percentages(sources: List[dict]) -> Dict[str, float]:
    """Compute percentage of views from each source for a single video."""
    total = sum(s['views'] for s in sources)
    if total == 0:
        return {}

    pcts = {}
    for s in sources:
        pcts[s['source_type']] = (s['views'] / total) * 100
    return pcts


def compute_source_watch_efficiency(sources: List[dict]) -> Dict[str, float]:
    """Compute avg watch time per view for each source (minutes)."""
    result = {}
    for s in sources:
        if s['views'] > 0:
            result[s['source_type']] = s['watch_time_minutes'] / s['views']
    return result


def analyze_by_group(
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    group_key: str,
) -> Dict[str, dict]:
    """
    Aggregate traffic sources by a grouping key (topic_type, title_pattern, etc.)

    Returns dict: group_value -> {
        'count': int,
        'total_views': int,
        'source_pcts': {source_type: avg_pct},
        'source_views': {source_type: total_views},
        'avg_watch_efficiency': {source_type: avg_min_per_view},
    }
    """
    groups: Dict[str, dict] = defaultdict(lambda: {
        'count': 0,
        'total_views': 0,
        'source_views': defaultdict(int),
        'source_watch_time': defaultdict(float),
        'pct_lists': defaultdict(list),
    })

    for vid_id, sources in traffic_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        group_val = meta.get(group_key, 'unknown')
        if not group_val:
            group_val = 'unknown'

        g = groups[group_val]
        g['count'] += 1

        total_views = sum(s['views'] for s in sources)
        g['total_views'] += total_views

        pcts = compute_source_percentages(sources)
        for source_type, pct in pcts.items():
            g['pct_lists'][source_type].append(pct)

        for s in sources:
            g['source_views'][s['source_type']] += s['views']
            g['source_watch_time'][s['source_type']] += s['watch_time_minutes']

    # Compute averages
    result = {}
    for group_val, g in groups.items():
        source_pcts = {}
        for source_type, pct_list in g['pct_lists'].items():
            source_pcts[source_type] = mean(pct_list)

        avg_watch_eff = {}
        for source_type in g['source_views']:
            views = g['source_views'][source_type]
            if views > 0:
                avg_watch_eff[source_type] = g['source_watch_time'][source_type] / views

        result[group_val] = {
            'count': g['count'],
            'total_views': g['total_views'],
            'source_pcts': dict(source_pcts),
            'source_views': dict(g['source_views']),
            'avg_watch_efficiency': avg_watch_eff,
        }

    return result


def rank_videos_by_source(
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    source_type: str,
) -> List[dict]:
    """Rank videos by percentage of traffic from a specific source."""
    ranked = []
    for vid_id, sources in traffic_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        pcts = compute_source_percentages(sources)
        total_views = sum(s['views'] for s in sources)
        source_views = sum(s['views'] for s in sources if s['source_type'] == source_type)

        ranked.append({
            'video_id': vid_id,
            'title': meta.get('title', ''),
            'topic_type': meta.get('topic_type', 'general'),
            'total_views': total_views,
            'source_views': source_views,
            'source_pct': pcts.get(source_type, 0),
        })

    ranked.sort(key=lambda x: x['source_pct'], reverse=True)
    return ranked


def compute_channel_traffic_mix(traffic_data: Dict[str, List[dict]]) -> Dict[str, dict]:
    """Compute overall channel traffic source mix (totals and averages)."""
    total_views_by_source: Dict[str, int] = defaultdict(int)
    total_watch_by_source: Dict[str, float] = defaultdict(float)
    grand_total = 0

    for sources in traffic_data.values():
        for s in sources:
            total_views_by_source[s['source_type']] += s['views']
            total_watch_by_source[s['source_type']] += s['watch_time_minutes']
            grand_total += s['views']

    result = {}
    for source_type in total_views_by_source:
        views = total_views_by_source[source_type]
        watch = total_watch_by_source[source_type]
        result[source_type] = {
            'views': views,
            'pct': (views / grand_total * 100) if grand_total > 0 else 0,
            'watch_time_minutes': watch,
            'avg_watch_per_view': watch / views if views > 0 else 0,
        }

    return dict(sorted(result.items(), key=lambda x: x[1]['views'], reverse=True))


# =========================================================================
# SINGLE VIDEO REPORT
# =========================================================================

def single_video_report(
    video_id: str,
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate a detailed report for a single video."""
    sources = traffic_data.get(video_id)
    meta = metadata.get(video_id)

    if not sources:
        return f"No traffic source data found for {video_id}"

    lines = []
    title = meta.get('title', video_id) if meta else video_id
    lines.append(f"# Traffic Source Breakdown: {title}")
    lines.append("")

    if meta:
        lines.append(f"- **Topic type:** {meta.get('topic_type', 'unknown')}")
        lines.append(f"- **Title pattern:** {meta.get('title_pattern', 'unknown')}")
        dur = meta.get('duration_seconds', 0)
        lines.append(f"- **Duration:** {dur // 60}m {dur % 60}s")
        lines.append(f"- **Total views:** {meta.get('views', 'N/A'):,}")
        lines.append(f"- **Published:** {meta.get('published_at', 'N/A')[:10]} ({meta.get('pub_day', '?')})")
        lines.append("")

    total = sum(s['views'] for s in sources)
    lines.append(f"## Traffic Sources ({total:,} views total)")
    lines.append("")
    lines.append("| Source | Views | % | Watch Time (min) | Avg Min/View |")
    lines.append("|--------|------:|--:|----------------:|------------:|")

    sorted_sources = sorted(sources, key=lambda s: s['views'], reverse=True)
    for s in sorted_sources:
        label = SOURCE_LABELS.get(s['source_type'], s['source_type'])
        pct = (s['views'] / total * 100) if total > 0 else 0
        avg_wt = s['watch_time_minutes'] / s['views'] if s['views'] > 0 else 0
        lines.append(
            f"| {label} | {s['views']:,} | {pct:.1f}% | {s['watch_time_minutes']:,.0f} | {avg_wt:.1f} |"
        )

    lines.append("")

    # Diagnosis
    pcts = compute_source_percentages(sources)
    search_pct = pcts.get('YT_SEARCH', 0)
    suggested_pct = pcts.get('RELATED_VIDEO', 0)
    sub_pct = pcts.get('SUBSCRIBER', 0)

    lines.append("## Diagnosis")
    lines.append("")
    if search_pct > 40:
        lines.append("- **Search-driven** — This video gets most traffic from YouTube Search. "
                      "Optimize description with target keywords.")
    elif suggested_pct > 40:
        lines.append("- **Algorithm-driven** — This video is being recommended by YouTube. "
                      "Strong signal for similar content.")
    elif sub_pct > 40:
        lines.append("- **Subscriber-driven** — Mostly reaching existing subscribers. "
                      "Limited new audience discovery.")
    else:
        lines.append("- **Mixed traffic** — No dominant single source. Balanced distribution.")

    return "\n".join(lines)


# =========================================================================
# FULL REPORT GENERATION
# =========================================================================

def _format_source_table(
    groups: Dict[str, dict],
    focus_sources: List[str],
    sort_by: Optional[str] = None,
) -> str:
    """Format a markdown table showing source percentages by group."""
    headers = ["Group", "n"]
    for src in focus_sources:
        headers.append(SOURCE_LABELS.get(src, src)[:15])
    headers.append("Total Views")

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")

    items = sorted(groups.items(),
                   key=lambda x: x[1].get('total_views', 0) if sort_by is None
                   else x[1]['source_pcts'].get(sort_by, 0),
                   reverse=True)

    for group_val, data in items:
        row = [f"**{group_val}**", str(data['count'])]
        for src in focus_sources:
            pct = data['source_pcts'].get(src, 0)
            row.append(f"{pct:.1f}%")
        row.append(f"{data['total_views']:,}")
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def generate_full_report(
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate the complete traffic source analysis report."""

    # Filter to only videos we have both traffic and metadata for
    common_ids = set(traffic_data.keys()) & set(metadata.keys())
    filtered_traffic = {k: v for k, v in traffic_data.items() if k in common_ids}

    if not filtered_traffic:
        return "# Traffic Source Analysis\n\nNo data available. Run with --fetch to pull from API."

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines = []

    lines.append("# Traffic Source Analysis")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {len(filtered_traffic)}")
    lines.append("")

    # ---- Section 1: Channel Traffic Mix ----
    lines.append("## 1. Channel Traffic Mix (Overall)")
    lines.append("")
    channel_mix = compute_channel_traffic_mix(filtered_traffic)
    grand_total = sum(v['views'] for v in channel_mix.values())

    lines.append("| Source | Views | % of Total | Watch Time (hr) | Avg Min/View |")
    lines.append("|--------|------:|----------:|---------------:|------------:|")
    for source_type, data in channel_mix.items():
        label = SOURCE_LABELS.get(source_type, source_type)
        hours = data['watch_time_minutes'] / 60
        lines.append(
            f"| {label} | {data['views']:,} | {data['pct']:.1f}% "
            f"| {hours:,.1f} | {data['avg_watch_per_view']:.1f} |"
        )
    lines.append("")

    # Key insight
    top_source = next(iter(channel_mix))
    top_pct = channel_mix[top_source]['pct']
    lines.append(f"**Key insight:** {SOURCE_LABELS.get(top_source, top_source)} "
                 f"drives {top_pct:.0f}% of all views. ", )

    # Find highest watch time efficiency
    best_eff_source = max(channel_mix.items(), key=lambda x: x[1]['avg_watch_per_view'])
    lines.append(
        f"**Best engagement source:** {SOURCE_LABELS.get(best_eff_source[0], best_eff_source[0])} "
        f"({best_eff_source[1]['avg_watch_per_view']:.1f} min/view avg)."
    )
    lines.append("")

    # ---- Section 2: Traffic by Topic Type ----
    lines.append("## 2. Traffic Sources by Topic Type")
    lines.append("")
    lines.append("Which content types attract which traffic sources?")
    lines.append("")

    topic_groups = analyze_by_group(filtered_traffic, metadata, 'topic_type')
    focus = ['YT_SEARCH', 'RELATED_VIDEO', 'SUBSCRIBER', 'EXT_URL', 'NOTIFICATION']
    lines.append(_format_source_table(topic_groups, focus))
    lines.append("")

    # Insights
    lines.append("### Insights")
    lines.append("")
    for topic, data in sorted(topic_groups.items(), key=lambda x: x[1]['total_views'], reverse=True):
        search_pct = data['source_pcts'].get('YT_SEARCH', 0)
        suggested_pct = data['source_pcts'].get('RELATED_VIDEO', 0)
        sub_pct = data['source_pcts'].get('SUBSCRIBER', 0)

        if search_pct > suggested_pct and search_pct > sub_pct:
            driver = f"Search-driven ({search_pct:.0f}%)"
            tip = "Optimize descriptions and tags for search keywords"
        elif suggested_pct > search_pct and suggested_pct > sub_pct:
            driver = f"Algorithm-driven ({suggested_pct:.0f}%)"
            tip = "YouTube is recommending these — create more related content"
        elif sub_pct > search_pct and sub_pct > suggested_pct:
            driver = f"Subscriber-driven ({sub_pct:.0f}%)"
            tip = "Limited new audience reach — improve title/thumbnail for Browse"
        else:
            driver = "Mixed traffic"
            tip = "No dominant source — balanced distribution"

        lines.append(f"- **{topic}** (n={data['count']}): {driver}. {tip}.")
    lines.append("")

    # ---- Section 3: Traffic by Title Pattern ----
    lines.append("## 3. Traffic Sources by Title Pattern")
    lines.append("")
    title_groups = analyze_by_group(filtered_traffic, metadata, 'title_pattern')
    lines.append(_format_source_table(title_groups, focus))
    lines.append("")

    # ---- Section 4: Search vs Browse Optimization ----
    lines.append("## 4. Search vs Browse Optimization")
    lines.append("")
    lines.append("Videos ranked by Search dependency (higher = more search-driven):")
    lines.append("")

    search_ranked = rank_videos_by_source(filtered_traffic, metadata, 'YT_SEARCH')
    lines.append("| # | Title | Topic | Search % | Suggested % | Views |")
    lines.append("|---|-------|-------|--------:|----------:|------:|")
    for i, v in enumerate(search_ranked[:15], 1):
        pcts = compute_source_percentages(filtered_traffic[v['video_id']])
        suggested_pct = pcts.get('RELATED_VIDEO', 0)
        title_short = v['title'][:50] + ('...' if len(v['title']) > 50 else '')
        lines.append(
            f"| {i} | {title_short} | {v['topic_type']} "
            f"| {v['source_pct']:.1f}% | {suggested_pct:.1f}% | {v['total_views']:,} |"
        )
    lines.append("")

    # Search vs algorithm quadrant
    lines.append("### Search/Algorithm Quadrant")
    lines.append("")
    lines.append("Classifying each video by its primary traffic driver:")
    lines.append("")

    quadrants = {'search_driven': [], 'algorithm_driven': [], 'subscriber_driven': [], 'mixed': []}
    for vid_id, sources in filtered_traffic.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue
        pcts = compute_source_percentages(sources)
        search = pcts.get('YT_SEARCH', 0)
        suggested = pcts.get('RELATED_VIDEO', 0)
        subs = pcts.get('SUBSCRIBER', 0)

        if search >= 30 and search > suggested and search > subs:
            quadrants['search_driven'].append(meta['title'][:45])
        elif suggested >= 30 and suggested > search and suggested > subs:
            quadrants['algorithm_driven'].append(meta['title'][:45])
        elif subs >= 30 and subs > search and subs > suggested:
            quadrants['subscriber_driven'].append(meta['title'][:45])
        else:
            quadrants['mixed'].append(meta['title'][:45])

    for q_name, q_label in [
        ('search_driven', 'Search-Driven (>30% from YT Search)'),
        ('algorithm_driven', 'Algorithm-Driven (>30% from Suggested)'),
        ('subscriber_driven', 'Subscriber-Driven (>30% from Subscribers)'),
        ('mixed', 'Mixed Traffic (no dominant source)'),
    ]:
        lines.append(f"**{q_label}** ({len(quadrants[q_name])} videos):")
        if quadrants[q_name]:
            for title in quadrants[q_name][:8]:
                lines.append(f"  - {title}")
        else:
            lines.append("  - (none)")
        lines.append("")

    # ---- Section 5: Traffic by Duration ----
    lines.append("## 5. Traffic Sources by Video Duration")
    lines.append("")
    dur_groups = analyze_by_group(filtered_traffic, metadata, 'duration_bucket')
    lines.append(_format_source_table(dur_groups, focus))
    lines.append("")

    # ---- Section 6: Traffic by Publication Day ----
    lines.append("## 6. Traffic Sources by Publication Day")
    lines.append("")
    day_groups = analyze_by_group(filtered_traffic, metadata, 'pub_day')
    lines.append(_format_source_table(day_groups, ['YT_SEARCH', 'RELATED_VIDEO', 'SUBSCRIBER']))
    lines.append("")

    # ---- Section 7: Watch Time Efficiency by Source ----
    lines.append("## 7. Watch Time Efficiency by Source")
    lines.append("")
    lines.append("Which traffic sources deliver the most engaged viewers?")
    lines.append("")

    lines.append("| Source | Avg Min/View | Total Hours | Interpretation |")
    lines.append("|--------|------------:|----------:|----------------|")
    for source_type, data in channel_mix.items():
        label = SOURCE_LABELS.get(source_type, source_type)
        hours = data['watch_time_minutes'] / 60
        eff = data['avg_watch_per_view']
        if eff > 3:
            interp = "High engagement"
        elif eff > 1:
            interp = "Moderate engagement"
        else:
            interp = "Low engagement (bouncing)"
        lines.append(f"| {label} | {eff:.1f} | {hours:,.1f} | {interp} |")
    lines.append("")

    # ---- Section 8: Actionable Recommendations ----
    lines.append("## 8. Actionable Recommendations")
    lines.append("")

    # Generate data-driven recommendations
    recs = _generate_recommendations(topic_groups, channel_mix, quadrants, filtered_traffic, metadata)
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. {rec}")
    lines.append("")

    # ---- Footer ----
    lines.append("---")
    lines.append(f"*Generated by `traffic_analysis.py` on {now}. "
                 f"Data covers {len(filtered_traffic)} long-form videos.*")

    return "\n".join(lines)


def _generate_recommendations(
    topic_groups: Dict[str, dict],
    channel_mix: Dict[str, dict],
    quadrants: Dict[str, list],
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[str]:
    """Generate data-driven recommendations from the analysis."""
    recs = []

    # Recommendation 1: Topic-specific SEO
    for topic, data in sorted(topic_groups.items(), key=lambda x: x[1]['total_views'], reverse=True):
        search_pct = data['source_pcts'].get('YT_SEARCH', 0)
        if search_pct > 25:
            recs.append(
                f"**{topic.title()} videos are search-dependent** ({search_pct:.0f}% from Search). "
                f"For {topic} topics: front-load the target keyword in title, "
                f"use the keyword 3+ times in description, add related long-tail tags."
            )
            break

    # Recommendation 2: Algorithm gap
    suggested_pct = channel_mix.get('RELATED_VIDEO', {}).get('pct', 0)
    if suggested_pct < 20:
        recs.append(
            f"**Suggested/Related traffic is only {suggested_pct:.0f}%** (healthy channels get 30-50%). "
            f"To increase: create content that relates to popular existing videos, "
            f"use end screens linking to thematically similar videos, optimize thumbnails for Browse."
        )

    # Recommendation 3: Subscriber dependency
    sub_pct = channel_mix.get('SUBSCRIBER', {}).get('pct', 0)
    if sub_pct > 30:
        recs.append(
            f"**{sub_pct:.0f}% of traffic comes from subscribers** — high dependency on existing audience. "
            f"New videos need stronger titles/thumbnails to break into Browse/Search."
        )
    elif sub_pct < 10:
        recs.append(
            f"**Only {sub_pct:.0f}% from subscribers** — low subscriber engagement. "
            f"Consider notification CTAs and community posts to activate existing subscribers."
        )

    # Recommendation 4: External traffic
    ext_pct = channel_mix.get('EXT_URL', {}).get('pct', 0)
    if ext_pct > 10:
        ext_eff = channel_mix.get('EXT_URL', {}).get('avg_watch_per_view', 0)
        recs.append(
            f"**External traffic is {ext_pct:.0f}%** with {ext_eff:.1f} min/view. "
            f"Identify and cultivate these referral sources (Reddit, forums, social media)."
        )

    # Recommendation 5: Search-driven winners
    if quadrants.get('search_driven'):
        n_search = len(quadrants['search_driven'])
        recs.append(
            f"**{n_search} videos are search-driven.** These are evergreen assets. "
            f"Review their titles and descriptions annually to maintain search ranking. "
            f"Consider creating follow-up content on the same search terms."
        )

    # Recommendation 6: Best engagement source
    if channel_mix:
        best = max(
            [(k, v) for k, v in channel_mix.items() if v['views'] > 10],
            key=lambda x: x[1]['avg_watch_per_view'],
            default=None,
        )
        if best:
            label = SOURCE_LABELS.get(best[0], best[0])
            recs.append(
                f"**{label} delivers the highest engagement** "
                f"({best[1]['avg_watch_per_view']:.1f} min/view). "
                f"Viewers from this source watch longer — "
                f"prioritize strategies that increase this traffic type."
            )

    return recs


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Analyze YouTube traffic source patterns by content type.'
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full report to channel-data/patterns/')
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch fresh data from YouTube Analytics API')
    parser.add_argument('--video', type=str, default=None,
                        help='Single video ID for detailed breakdown')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress info logging')
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not args.report and not args.fetch and not args.video:
        args.report = True

    # Load metadata
    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata found in analytics.db. Run backfill first.")
        sys.exit(1)

    # Fetch or load traffic data
    if args.fetch:
        logger.info("Fetching fresh traffic data from YouTube Analytics API...")
        video_ids = [args.video] if args.video else None
        fresh_data = fetch_traffic_sources_api(video_ids)
        if fresh_data:
            # Merge with existing
            existing = load_traffic_from_json()
            existing.update(fresh_data)
            save_traffic_json(existing)
            traffic_data = existing
        else:
            logger.warning("No data fetched. Falling back to cache.")
            traffic_data = merge_traffic_data(load_traffic_from_json(), load_traffic_from_db())
    else:
        traffic_data = merge_traffic_data(load_traffic_from_json(), load_traffic_from_db())

    if not traffic_data:
        logger.error("No traffic source data available. Run with --fetch to pull from API.")
        sys.exit(1)

    logger.info("Traffic data: %d videos. Metadata: %d videos.", len(traffic_data), len(metadata))

    # Single video mode
    if args.video:
        report = single_video_report(args.video, traffic_data, metadata)
        print(report)
        return

    # Full report mode
    if args.report:
        report = generate_full_report(traffic_data, metadata)

        # Save to file
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        # Also print to stdout
        print(report)


if __name__ == '__main__':
    main()
