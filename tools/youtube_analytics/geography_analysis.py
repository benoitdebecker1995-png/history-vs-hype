"""
Geography Analysis Tool

Analyzes geographic distribution of viewers and correlates with video content types
(topic type, retention, subscriber conversion).

Data sources:
  - analytics.db (videos table for metadata)
  - _geography_data.json (pre-fetched geography data)
  - YouTube Analytics API (fresh fetch via --fetch)

Usage:
    python -m tools.youtube_analytics.geography_analysis --report      # Full report
    python -m tools.youtube_analytics.geography_analysis --fetch       # Fetch fresh data
    python -m tools.youtube_analytics.geography_analysis --cached      # Report from cache only
    python -m tools.youtube_analytics.geography_analysis --video ID    # Single video
    python -m tools.youtube_analytics.geography_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/GEOGRAPHY-ANALYSIS.md
"""

import sys
import json
import time
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean
from typing import Dict, List, Any, Optional
from collections import defaultdict

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
GEOGRAPHY_JSON = Path(__file__).parent / '_geography_data.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'GEOGRAPHY-ANALYSIS.md'

# ISO 3166-1 alpha-2 to friendly name (top countries likely to appear)
COUNTRY_NAMES = {
    'US': 'United States', 'GB': 'United Kingdom', 'CA': 'Canada',
    'DE': 'Germany', 'AU': 'Australia', 'IN': 'India', 'FR': 'France',
    'NL': 'Netherlands', 'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark',
    'FI': 'Finland', 'IE': 'Ireland', 'NZ': 'New Zealand', 'BE': 'Belgium',
    'AT': 'Austria', 'CH': 'Switzerland', 'PL': 'Poland', 'IT': 'Italy',
    'ES': 'Spain', 'PT': 'Portugal', 'BR': 'Brazil', 'MX': 'Mexico',
    'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia', 'PE': 'Peru',
    'JP': 'Japan', 'KR': 'South Korea', 'PH': 'Philippines', 'SG': 'Singapore',
    'MY': 'Malaysia', 'ID': 'Indonesia', 'TH': 'Thailand', 'VN': 'Vietnam',
    'ZA': 'South Africa', 'NG': 'Nigeria', 'KE': 'Kenya', 'EG': 'Egypt',
    'TR': 'Turkey', 'RU': 'Russia', 'UA': 'Ukraine', 'RO': 'Romania',
    'GR': 'Greece', 'CZ': 'Czechia', 'HU': 'Hungary', 'HR': 'Croatia',
    'RS': 'Serbia', 'BG': 'Bulgaria', 'SK': 'Slovakia', 'SI': 'Slovenia',
    'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia', 'IS': 'Iceland',
    'IL': 'Israel', 'SA': 'Saudi Arabia', 'AE': 'UAE', 'PK': 'Pakistan',
    'BD': 'Bangladesh', 'LK': 'Sri Lanka', 'HK': 'Hong Kong', 'TW': 'Taiwan',
    'BZ': 'Belize', 'GT': 'Guatemala', 'HT': 'Haiti', 'DO': 'Dominican Republic',
    'JM': 'Jamaica', 'TT': 'Trinidad & Tobago', 'GI': 'Gibraltar',
    'XK': 'Kosovo', 'BA': 'Bosnia & Herzegovina', 'MK': 'North Macedonia',
    'AL': 'Albania', 'ME': 'Montenegro', 'CY': 'Cyprus', 'MT': 'Malta',
}

# Core anglophone countries (baseline audience)
ANGLOPHONE = {'US', 'GB', 'CA', 'AU', 'NZ', 'IE'}


# =========================================================================
# DATA LOADING
# =========================================================================

def load_geography_from_json() -> Dict[str, Any]:
    """Load geography data from the JSON cache file."""
    if not GEOGRAPHY_JSON.exists():
        logger.warning("No geography JSON found at %s", GEOGRAPHY_JSON)
        return {}

    with open(GEOGRAPHY_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    video_count = len([k for k in data if k != '_channel_level'])
    logger.info("Loaded geography data for %d videos from JSON cache", video_count)
    return data


def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    conn = sqlite3.connect(str(ANALYTICS_DB))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT video_id, title, published_at, duration_seconds,
               views, watch_time_minutes, avg_view_percentage,
               topic_type, impressions, ctr_percent,
               subscribers_gained
        FROM videos
        WHERE duration_seconds > 60
    """)
    rows = cur.fetchall()
    conn.close()

    result = {}
    for row in rows:
        result[row['video_id']] = dict(row)

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


# =========================================================================
# API FETCH
# =========================================================================

def fetch_geography_api(video_ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
    """
    Fetch geography data from YouTube Analytics API for each video.

    Args:
        video_ids: Specific video IDs to fetch. If None, fetches all from DB.

    Returns:
        Dict mapping video_id -> list of country dicts.
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    if video_ids is None:
        metadata = load_video_metadata()
        video_ids = list(metadata.keys())

    logger.info("Fetching geography data for %d videos from API...", len(video_ids))
    result = {}

    for i, vid_id in enumerate(video_ids):
        try:
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate='2024-01-01',
                endDate='2026-12-31',
                metrics='views,estimatedMinutesWatched,subscribersGained',
                dimensions='country',
                filters=f'video=={vid_id}'
            ).execute()

            countries = []
            for row in response.get('rows', []):
                countries.append({
                    'country': row[0],
                    'views': int(row[1]),
                    'watch_time_minutes': float(row[2]),
                    'subscribers_gained': int(row[3]),
                })

            result[vid_id] = countries

            if (i + 1) % 10 == 0:
                logger.info("  Fetched %d/%d videos", i + 1, len(video_ids))

            time.sleep(0.1)

        except Exception as e:
            logger.warning("Failed to fetch geography for %s: %s", vid_id, e)

    logger.info("Fetched geography data for %d videos", len(result))
    return result


def fetch_channel_level_geography() -> List[dict]:
    """Fetch channel-level geography (no video filter)."""
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    try:
        response = analytics.reports().query(
            ids='channel==MINE',
            startDate='2024-01-01',
            endDate='2026-12-31',
            metrics='views,estimatedMinutesWatched,subscribersGained',
            dimensions='country',
        ).execute()

        countries = []
        for row in response.get('rows', []):
            countries.append({
                'country': row[0],
                'views': int(row[1]),
                'watch_time_minutes': float(row[2]),
                'subscribers_gained': int(row[3]),
            })

        logger.info("Fetched channel-level geography: %d countries", len(countries))
        return countries

    except Exception as e:
        logger.error("Failed to fetch channel-level geography: %s", e)
        return []


def save_geography_json(video_data: Dict[str, List[dict]], channel_data: List[dict]) -> None:
    """Save geography data to JSON cache."""
    combined = dict(video_data)
    combined['_channel_level'] = channel_data

    with open(GEOGRAPHY_JSON, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2)
    logger.info("Saved geography data to %s", GEOGRAPHY_JSON)


# =========================================================================
# HELPERS
# =========================================================================

def country_name(code: str) -> str:
    """Get friendly country name from ISO code."""
    return COUNTRY_NAMES.get(code, code)


def compute_herfindahl(countries: List[dict]) -> float:
    """
    Compute Herfindahl-Hirschman Index for geographic concentration.

    HHI = sum of (share_i)^2 where share is fraction (0-1).
    Range: 0 (infinitely spread) to 1 (all from one country).
    """
    total = sum(c['views'] for c in countries)
    if total == 0:
        return 0.0

    return sum((c['views'] / total) ** 2 for c in countries)


def compute_international_pct(countries: List[dict]) -> float:
    """Percentage of views from non-anglophone countries."""
    total = sum(c['views'] for c in countries)
    if total == 0:
        return 0.0

    intl = sum(c['views'] for c in countries if c['country'] not in ANGLOPHONE)
    return (intl / total) * 100


# =========================================================================
# ANALYSIS ENGINE
# =========================================================================

def analyze_country_mix_by_topic(
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> Dict[str, dict]:
    """
    Analyze which countries watch which topic types.

    Returns dict: topic_type -> {
        'count': N,
        'total_views': N,
        'country_views': {country: views},
        'top_countries': [(country, pct), ...],
        'international_pct': float,
    }
    """
    topics: Dict[str, dict] = defaultdict(lambda: {
        'count': 0,
        'total_views': 0,
        'country_views': defaultdict(int),
    })

    for vid_id, countries in geo_data.items():
        if vid_id == '_channel_level':
            continue
        meta = metadata.get(vid_id)
        if not meta:
            continue

        topic = meta.get('topic_type') or 'unknown'
        t = topics[topic]
        t['count'] += 1

        for c in countries:
            t['country_views'][c['country']] += c['views']
            t['total_views'] += c['views']

    result = {}
    for topic, t in topics.items():
        total = t['total_views']
        if total == 0:
            continue

        sorted_countries = sorted(
            t['country_views'].items(), key=lambda x: x[1], reverse=True
        )
        top_countries = [
            (code, (views / total) * 100)
            for code, views in sorted_countries[:10]
        ]

        intl_views = sum(
            v for code, v in t['country_views'].items() if code not in ANGLOPHONE
        )

        result[topic] = {
            'count': t['count'],
            'total_views': total,
            'top_countries': top_countries,
            'international_pct': (intl_views / total) * 100 if total > 0 else 0,
        }

    return result


def analyze_geographic_concentration(
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    Compute Herfindahl index per video and rank by concentration.

    Returns list of dicts sorted by HHI descending.
    """
    videos = []
    for vid_id, countries in geo_data.items():
        if vid_id == '_channel_level':
            continue
        meta = metadata.get(vid_id)
        if not meta:
            continue

        total_views = sum(c['views'] for c in countries)
        if total_views < 10:
            continue

        hhi = compute_herfindahl(countries)
        intl_pct = compute_international_pct(countries)

        # Find top country
        top = max(countries, key=lambda c: c['views']) if countries else None
        top_country = top['country'] if top else 'N/A'
        top_pct = (top['views'] / total_views * 100) if top and total_views > 0 else 0

        videos.append({
            'video_id': vid_id,
            'title': meta.get('title', vid_id),
            'topic_type': meta.get('topic_type', 'unknown'),
            'total_views': total_views,
            'hhi': hhi,
            'international_pct': intl_pct,
            'top_country': top_country,
            'top_country_pct': top_pct,
            'num_countries': len(countries),
        })

    videos.sort(key=lambda x: x['hhi'], reverse=True)
    return videos


def find_geographic_monopolies(
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    threshold: float = 30.0,
) -> List[dict]:
    """
    Find videos where a single non-US/UK country accounts for >threshold% of views.

    These represent geographic monopoly opportunities — topics that resonate
    strongly in specific countries.
    """
    monopolies = []
    for vid_id, countries in geo_data.items():
        if vid_id == '_channel_level':
            continue
        meta = metadata.get(vid_id)
        if not meta:
            continue

        total_views = sum(c['views'] for c in countries)
        if total_views < 20:
            continue

        for c in countries:
            # Skip US and UK (expected baseline)
            if c['country'] in ('US', 'GB'):
                continue

            pct = (c['views'] / total_views) * 100
            if pct >= threshold:
                monopolies.append({
                    'video_id': vid_id,
                    'title': meta.get('title', vid_id),
                    'topic_type': meta.get('topic_type', 'unknown'),
                    'total_views': total_views,
                    'country': c['country'],
                    'country_name': country_name(c['country']),
                    'country_views': c['views'],
                    'country_pct': pct,
                    'subs_gained': c.get('subscribers_gained', 0),
                })

    monopolies.sort(key=lambda x: x['country_pct'], reverse=True)
    return monopolies


def correlate_geography_retention(
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> dict:
    """
    Correlate international audience percentage with retention.

    Returns summary stats for high-international vs low-international videos.
    """
    video_stats = []
    for vid_id, countries in geo_data.items():
        if vid_id == '_channel_level':
            continue
        meta = metadata.get(vid_id)
        if not meta:
            continue

        avg_view_pct = meta.get('avg_view_percentage')
        if avg_view_pct is None:
            continue

        total_views = sum(c['views'] for c in countries)
        if total_views < 20:
            continue

        intl_pct = compute_international_pct(countries)
        video_stats.append({
            'video_id': vid_id,
            'title': meta.get('title', vid_id),
            'international_pct': intl_pct,
            'avg_view_percentage': avg_view_pct,
            'views': total_views,
        })

    if len(video_stats) < 4:
        return {'error': 'Insufficient data', 'n': len(video_stats)}

    # Split into high/low international
    video_stats.sort(key=lambda x: x['international_pct'])
    mid = len(video_stats) // 2
    low_intl = video_stats[:mid]
    high_intl = video_stats[mid:]

    # Compute Pearson correlation manually (avoid scipy dependency)
    n = len(video_stats)
    x = [v['international_pct'] for v in video_stats]
    y = [v['avg_view_percentage'] for v in video_stats]
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    std_x = (sum((xi - mean_x) ** 2 for xi in x) / n) ** 0.5
    std_y = (sum((yi - mean_y) ** 2 for yi in y) / n) ** 0.5
    correlation = cov / (std_x * std_y) if std_x > 0 and std_y > 0 else 0

    return {
        'n': n,
        'correlation': correlation,
        'low_international': {
            'count': len(low_intl),
            'avg_intl_pct': mean([v['international_pct'] for v in low_intl]),
            'avg_retention': mean([v['avg_view_percentage'] for v in low_intl]),
        },
        'high_international': {
            'count': len(high_intl),
            'avg_intl_pct': mean([v['international_pct'] for v in high_intl]),
            'avg_retention': mean([v['avg_view_percentage'] for v in high_intl]),
        },
    }


def country_subscriber_conversion(
    geo_data: Dict[str, List[dict]],
) -> List[dict]:
    """
    Compute subscribers_gained per view by country (channel-level).

    Uses channel-level data if available, otherwise aggregates per-video.
    """
    channel_data = geo_data.get('_channel_level', [])

    if channel_data:
        source = channel_data
    else:
        # Aggregate from per-video data
        agg: Dict[str, dict] = defaultdict(lambda: {
            'views': 0, 'watch_time_minutes': 0.0, 'subscribers_gained': 0,
        })
        for vid_id, countries in geo_data.items():
            if vid_id == '_channel_level':
                continue
            for c in countries:
                a = agg[c['country']]
                a['views'] += c['views']
                a['watch_time_minutes'] += c['watch_time_minutes']
                a['subscribers_gained'] += c.get('subscribers_gained', 0)

        source = [
            {'country': code, **vals}
            for code, vals in agg.items()
        ]

    result = []
    for c in source:
        views = c['views']
        if views < 10:
            continue

        subs = c.get('subscribers_gained', 0)
        result.append({
            'country': c['country'],
            'country_name': country_name(c['country']),
            'views': views,
            'watch_time_minutes': c['watch_time_minutes'],
            'subscribers_gained': subs,
            'sub_rate': (subs / views * 100) if views > 0 else 0,
            'avg_watch_per_view': c['watch_time_minutes'] / views if views > 0 else 0,
        })

    result.sort(key=lambda x: x['views'], reverse=True)
    return result


# =========================================================================
# SINGLE VIDEO REPORT
# =========================================================================

def single_video_report(
    video_id: str,
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate a detailed geography report for a single video."""
    countries = geo_data.get(video_id)
    meta = metadata.get(video_id)

    if not countries:
        return f"No geography data found for {video_id}"

    lines = []
    title = meta.get('title', video_id) if meta else video_id
    lines.append(f"# Geography Breakdown: {title}")
    lines.append("")

    if meta:
        lines.append(f"- **Topic type:** {meta.get('topic_type', 'unknown')}")
        dur = meta.get('duration_seconds', 0)
        lines.append(f"- **Duration:** {dur // 60}m {dur % 60}s")
        lines.append(f"- **Total views:** {meta.get('views', 'N/A'):,}")
        lines.append(f"- **Avg retention:** {meta.get('avg_view_percentage', 'N/A')}%")
        lines.append("")

    total = sum(c['views'] for c in countries)
    hhi = compute_herfindahl(countries)
    intl_pct = compute_international_pct(countries)

    lines.append(f"**HHI:** {hhi:.4f} | **International %:** {intl_pct:.1f}% | **Countries:** {len(countries)}")
    lines.append("")
    lines.append("| # | Country | Views | % | Watch Time (hr) | Subs | Sub Rate |")
    lines.append("|---|---------|------:|--:|----------------:|-----:|---------:|")

    sorted_countries = sorted(countries, key=lambda c: c['views'], reverse=True)
    for rank, c in enumerate(sorted_countries[:20], 1):
        pct = (c['views'] / total * 100) if total > 0 else 0
        wt_hr = c['watch_time_minutes'] / 60
        subs = c.get('subscribers_gained', 0)
        sub_rate = (subs / c['views'] * 100) if c['views'] > 0 else 0
        lines.append(
            f"| {rank} | {country_name(c['country'])} ({c['country']}) "
            f"| {c['views']:,} | {pct:.1f}% | {wt_hr:.1f} "
            f"| {subs} | {sub_rate:.2f}% |"
        )

    return "\n".join(lines)


# =========================================================================
# FULL REPORT
# =========================================================================

def generate_full_report(
    geo_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate the complete geography analysis report."""
    video_count = len([k for k in geo_data if k != '_channel_level'])
    now = datetime.now().strftime('%Y-%m-%d')

    lines = []
    lines.append("# Geography Analysis")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {video_count}")
    lines.append("")

    # ---- Section 1: Channel Country Mix ----
    lines.append("## 1. Channel Country Mix (Overall)")
    lines.append("")

    channel_countries = geo_data.get('_channel_level', [])
    if not channel_countries:
        # Aggregate from per-video
        agg: Dict[str, dict] = defaultdict(lambda: {
            'views': 0, 'watch_time_minutes': 0.0, 'subscribers_gained': 0,
        })
        for vid_id, countries in geo_data.items():
            if vid_id == '_channel_level':
                continue
            for c in countries:
                a = agg[c['country']]
                a['views'] += c['views']
                a['watch_time_minutes'] += c['watch_time_minutes']
                a['subscribers_gained'] += c.get('subscribers_gained', 0)
        channel_countries = [
            {'country': code, **vals} for code, vals in agg.items()
        ]

    channel_countries.sort(key=lambda c: c['views'], reverse=True)
    grand_total = sum(c['views'] for c in channel_countries)

    if grand_total > 0:
        lines.append("| # | Country | Views | % | Watch Time (hr) | Subs Gained | Sub Rate |")
        lines.append("|---|---------|------:|--:|----------------:|------------:|---------:|")
        for rank, c in enumerate(channel_countries[:20], 1):
            pct = c['views'] / grand_total * 100
            wt_hr = c['watch_time_minutes'] / 60
            subs = c.get('subscribers_gained', 0)
            sub_rate = (subs / c['views'] * 100) if c['views'] > 0 else 0
            lines.append(
                f"| {rank} | {country_name(c['country'])} ({c['country']}) "
                f"| {c['views']:,} | {pct:.1f}% | {wt_hr:.1f} "
                f"| {subs} | {sub_rate:.2f}% |"
            )

        # Summary stats
        anglophone_views = sum(
            c['views'] for c in channel_countries if c['country'] in ANGLOPHONE
        )
        lines.append("")
        lines.append(f"**Anglophone share:** {anglophone_views / grand_total * 100:.1f}% "
                      f"({anglophone_views:,} / {grand_total:,})")
        lines.append(f"**International share:** "
                      f"{(grand_total - anglophone_views) / grand_total * 100:.1f}%")
        lines.append(f"**Total countries:** {len(channel_countries)}")
    else:
        lines.append("*No channel-level geography data available.*")

    lines.append("")

    # ---- Section 2: Country Mix by Topic Type ----
    lines.append("## 2. Country Mix by Topic Type")
    lines.append("")

    topic_mix = analyze_country_mix_by_topic(geo_data, metadata)
    if topic_mix:
        lines.append("| Topic | Videos | Views | Top Country | % | 2nd Country | % | International % |")
        lines.append("|-------|-------:|------:|-------------|--:|-------------|--:|----------------:|")

        for topic in sorted(topic_mix.keys()):
            t = topic_mix[topic]
            top = t['top_countries']
            top1 = f"{country_name(top[0][0])}" if len(top) > 0 else "N/A"
            top1_pct = top[0][1] if len(top) > 0 else 0
            top2 = f"{country_name(top[1][0])}" if len(top) > 1 else "N/A"
            top2_pct = top[1][1] if len(top) > 1 else 0

            lines.append(
                f"| {topic} | {t['count']} | {t['total_views']:,} "
                f"| {top1} | {top1_pct:.1f}% | {top2} | {top2_pct:.1f}% "
                f"| {t['international_pct']:.1f}% |"
            )
    else:
        lines.append("*No topic-type data available.*")

    lines.append("")

    # ---- Section 3: Geographic Concentration ----
    lines.append("## 3. Geographic Concentration (Herfindahl Index)")
    lines.append("")
    lines.append("HHI ranges from 0 (infinitely spread) to 1 (all from one country). "
                 "Higher = more concentrated audience.")
    lines.append("")

    concentration = analyze_geographic_concentration(geo_data, metadata)
    if concentration:
        # Most concentrated
        lines.append("### Most Concentrated (highest HHI)")
        lines.append("")
        lines.append("| Video | Topic | Views | HHI | Top Country | Top % | Countries |")
        lines.append("|-------|-------|------:|----:|-------------|------:|----------:|")
        for v in concentration[:10]:
            lines.append(
                f"| {v['title'][:45]}{'...' if len(v['title']) > 45 else ''} "
                f"| {v['topic_type']} | {v['total_views']:,} | {v['hhi']:.4f} "
                f"| {country_name(v['top_country'])} | {v['top_country_pct']:.1f}% "
                f"| {v['num_countries']} |"
            )

        lines.append("")
        lines.append("### Most Spread (lowest HHI)")
        lines.append("")
        lines.append("| Video | Topic | Views | HHI | Top Country | Top % | Countries |")
        lines.append("|-------|-------|------:|----:|-------------|------:|----------:|")
        for v in concentration[-10:]:
            lines.append(
                f"| {v['title'][:45]}{'...' if len(v['title']) > 45 else ''} "
                f"| {v['topic_type']} | {v['total_views']:,} | {v['hhi']:.4f} "
                f"| {country_name(v['top_country'])} | {v['top_country_pct']:.1f}% "
                f"| {v['num_countries']} |"
            )

        # Summary
        if len(concentration) >= 2:
            avg_hhi = mean([v['hhi'] for v in concentration])
            avg_countries = mean([v['num_countries'] for v in concentration])
            lines.append("")
            lines.append(f"**Average HHI:** {avg_hhi:.4f} | "
                          f"**Average countries per video:** {avg_countries:.0f}")
    else:
        lines.append("*Insufficient data for concentration analysis.*")

    lines.append("")

    # ---- Section 4: Geographic Monopoly Opportunities ----
    lines.append("## 4. Geographic Monopoly Opportunities")
    lines.append("")
    lines.append("Videos where a single non-US/UK country accounts for >30% of views. "
                 "These indicate topics with strong regional resonance.")
    lines.append("")

    monopolies = find_geographic_monopolies(geo_data, metadata)
    if monopolies:
        lines.append("| Video | Country | Country Views | % of Total | Total Views | Subs |")
        lines.append("|-------|---------|-------------:|----------:|-----------:|-----:|")
        for m in monopolies:
            lines.append(
                f"| {m['title'][:45]}{'...' if len(m['title']) > 45 else ''} "
                f"| {m['country_name']} ({m['country']}) "
                f"| {m['country_views']:,} | {m['country_pct']:.1f}% "
                f"| {m['total_views']:,} | {m['subs_gained']} |"
            )
    else:
        lines.append("*No geographic monopolies found (no non-US/UK country >30% for any video).*")

    lines.append("")

    # ---- Section 5: Country Subscriber Conversion ----
    lines.append("## 5. Country-Subscriber Conversion")
    lines.append("")

    conversions = country_subscriber_conversion(geo_data)
    if conversions:
        # Top 20 by views
        lines.append("### By Volume (top 20 countries)")
        lines.append("")
        lines.append("| # | Country | Views | Watch Time (hr) | Subs Gained | Sub Rate | Avg Min/View |")
        lines.append("|---|---------|------:|----------------:|------------:|---------:|-------------:|")
        for rank, c in enumerate(conversions[:20], 1):
            wt_hr = c['watch_time_minutes'] / 60
            lines.append(
                f"| {rank} | {c['country_name']} ({c['country']}) "
                f"| {c['views']:,} | {wt_hr:.1f} "
                f"| {c['subscribers_gained']} | {c['sub_rate']:.2f}% "
                f"| {c['avg_watch_per_view']:.1f} |"
            )

        # Top converters (min 50 views)
        high_conv = [c for c in conversions if c['views'] >= 50]
        high_conv.sort(key=lambda x: x['sub_rate'], reverse=True)
        if high_conv:
            lines.append("")
            lines.append("### Best Converting Countries (min 50 views)")
            lines.append("")
            lines.append("| Country | Views | Subs Gained | Sub Rate | Avg Min/View |")
            lines.append("|---------|------:|------------:|---------:|-------------:|")
            for c in high_conv[:15]:
                lines.append(
                    f"| {c['country_name']} ({c['country']}) "
                    f"| {c['views']:,} | {c['subscribers_gained']} "
                    f"| {c['sub_rate']:.2f}% | {c['avg_watch_per_view']:.1f} |"
                )
    else:
        lines.append("*No subscriber conversion data available.*")

    lines.append("")

    # ---- Section 6: Geography-Retention Correlation ----
    lines.append("## 6. Geography-Retention Correlation")
    lines.append("")

    retention_corr = correlate_geography_retention(geo_data, metadata)
    if 'error' in retention_corr:
        lines.append(f"*{retention_corr['error']} (n={retention_corr['n']})*")
    else:
        r = retention_corr['correlation']
        lines.append(f"**Pearson r:** {r:.3f} (n={retention_corr['n']})")
        lines.append("")

        strength = "negligible"
        if abs(r) > 0.5:
            strength = "strong"
        elif abs(r) > 0.3:
            strength = "moderate"
        elif abs(r) > 0.1:
            strength = "weak"

        direction = "positive" if r > 0 else "negative"
        lines.append(f"Correlation between international audience % and retention is "
                      f"**{strength} {direction}**.")
        lines.append("")

        lo = retention_corr['low_international']
        hi = retention_corr['high_international']
        lines.append("| Group | Videos | Avg International % | Avg Retention % |")
        lines.append("|-------|-------:|--------------------:|----------------:|")
        lines.append(
            f"| Low international | {lo['count']} "
            f"| {lo['avg_intl_pct']:.1f}% | {lo['avg_retention']:.1f}% |"
        )
        lines.append(
            f"| High international | {hi['count']} "
            f"| {hi['avg_intl_pct']:.1f}% | {hi['avg_retention']:.1f}% |"
        )

    lines.append("")

    # ---- Section 7: Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = []

    # Finding 1: Channel geographic profile
    if grand_total > 0 and channel_countries:
        top3 = channel_countries[:3]
        top3_str = ", ".join(
            f"{country_name(c['country'])} ({c['views'] / grand_total * 100:.0f}%)"
            for c in top3
        )
        findings.append(f"- **Core audience:** {top3_str}")

        anglophone_pct = anglophone_views / grand_total * 100 if grand_total > 0 else 0
        if anglophone_pct > 70:
            findings.append(
                f"- **Heavily anglophone** ({anglophone_pct:.0f}%). "
                "International expansion potential exists if topics with regional "
                "resonance are prioritized."
            )
        else:
            findings.append(
                f"- **Solid international mix** ({100 - anglophone_pct:.0f}% non-anglophone). "
                "Content resonates beyond English-speaking markets."
            )

    # Finding 2: Monopoly insights
    if monopolies:
        unique_countries = set(m['country'] for m in monopolies)
        findings.append(
            f"- **Geographic monopolies detected** in {len(monopolies)} videos "
            f"across {len(unique_countries)} countries. "
            "Consider creating follow-up content targeting these regions."
        )

    # Finding 3: Retention correlation
    if 'error' not in retention_corr:
        r = retention_corr['correlation']
        if abs(r) > 0.2:
            if r > 0:
                findings.append(
                    "- **More international audiences correlate with higher retention** "
                    f"(r={r:.2f}). International viewers may be more invested in niche topics."
                )
            else:
                findings.append(
                    "- **More international audiences correlate with lower retention** "
                    f"(r={r:.2f}). Language barrier or cultural relevance gap may affect engagement."
                )
        else:
            findings.append(
                f"- **No meaningful link between international audience and retention** (r={r:.2f}). "
                "Geographic spread does not predict engagement quality."
            )

    # Finding 4: Conversion insights
    if conversions:
        high_conv_countries = [c for c in conversions if c['views'] >= 50 and c['sub_rate'] > 1.0]
        if high_conv_countries:
            best = max(high_conv_countries, key=lambda c: c['sub_rate'])
            findings.append(
                f"- **Highest subscriber conversion:** {best['country_name']} "
                f"({best['sub_rate']:.2f}% sub rate, n={best['views']}). "
                "Topics resonating with this audience are strong growth levers."
            )

    # Finding 5: Topic geography patterns
    if topic_mix:
        most_intl = max(topic_mix.items(), key=lambda x: x[1]['international_pct'])
        least_intl = min(topic_mix.items(), key=lambda x: x[1]['international_pct'])
        if most_intl[0] != least_intl[0]:
            findings.append(
                f"- **Most international topic:** {most_intl[0]} "
                f"({most_intl[1]['international_pct']:.0f}% non-anglophone). "
                f"**Most anglophone:** {least_intl[0]} "
                f"({least_intl[1]['international_pct']:.0f}% non-anglophone)."
            )

    if findings:
        lines.extend(findings)
    else:
        lines.append("- *Insufficient data for interpreted findings. Run --fetch to collect data.*")

    lines.append("")
    return "\n".join(lines)


# =========================================================================
# MAIN
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Geography Analysis Tool for History vs Hype YouTube channel"
    )
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch fresh geography data from YouTube Analytics API')
    parser.add_argument('--cached', action='store_true',
                        help='Use only cached data (no API calls)')
    parser.add_argument('--report', action='store_true',
                        help='Generate full geography analysis report')
    parser.add_argument('--video', type=str, default=None,
                        help='Analyze a single video by ID')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress info logging')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not any([args.fetch, args.cached, args.report, args.video]):
        args.report = True

    metadata = load_video_metadata()

    # Fetch mode
    if args.fetch:
        video_ids = [args.video] if args.video else None
        video_data = fetch_geography_api(video_ids)
        channel_data = fetch_channel_level_geography()
        save_geography_json(video_data, channel_data)

        # Merge with existing cache
        existing = load_geography_from_json()
        existing.update(video_data)
        if channel_data:
            existing['_channel_level'] = channel_data
        save_geography_json(
            {k: v for k, v in existing.items() if k != '_channel_level'},
            existing.get('_channel_level', [])
        )
        geo_data = existing
    else:
        geo_data = load_geography_from_json()

    if not geo_data:
        logger.error("No geography data available. Run with --fetch first.")
        sys.exit(1)

    # Single video mode
    if args.video:
        report = single_video_report(args.video, geo_data, metadata)
        print(report)
        return

    # Report mode
    if args.report or args.cached:
        report = generate_full_report(geo_data, metadata)

        # Write to file
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report written to %s", REPORT_PATH)

        # Also print summary to stdout
        video_count = len([k for k in geo_data if k != '_channel_level'])
        print(f"Geography analysis complete: {video_count} videos analyzed")
        print(f"Report saved to: {REPORT_PATH}")


if __name__ == '__main__':
    main()
