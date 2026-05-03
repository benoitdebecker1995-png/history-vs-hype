"""
First-Week Velocity Analysis Tool

Analyzes first-48-hour and first-7-day view velocity for each video to identify
algorithmic push patterns, optimal publication timing, and whether early
performance predicts lifetime success.

Data sources:
  - analytics.db (videos table for metadata)
  - _velocity_data.json (cached daily metrics for first 7 days)
  - YouTube Analytics API (fresh fetch via --fetch)

Usage:
    python -m tools.youtube_analytics.velocity_analysis --report      # Full report
    python -m tools.youtube_analytics.velocity_analysis --fetch       # Fetch fresh data
    python -m tools.youtube_analytics.velocity_analysis --cached      # Use cache only
    python -m tools.youtube_analytics.velocity_analysis --video ID    # Single video
    python -m tools.youtube_analytics.velocity_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/VELOCITY-ANALYSIS.md
"""

import sys
import json
import sqlite3
import argparse
import time
from pathlib import Path
from datetime import datetime, timedelta, timezone
from statistics import mean, stdev
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
VELOCITY_JSON = Path(__file__).parent / '_velocity_data.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'VELOCITY-ANALYSIS.md'

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# =========================================================================
# DATA LOADING
# =========================================================================

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
               views, watch_time_minutes, topic_type, subscribers_gained
        FROM videos
        WHERE duration_seconds > 60
    """)
    rows = cur.fetchall()
    conn.close()

    result = {}
    for row in rows:
        vid = dict(row)

        # Parse publication day
        try:
            pub_date = datetime.fromisoformat(vid['published_at'].replace('Z', '+00:00'))
            vid['pub_day'] = DAY_NAMES[pub_date.weekday()]
            vid['pub_date_obj'] = pub_date
        except (ValueError, AttributeError, TypeError):
            vid['pub_day'] = 'Unknown'
            vid['pub_date_obj'] = None

        result[vid['video_id']] = vid

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


def load_velocity_cache() -> Dict[str, dict]:
    """Load cached velocity data from JSON."""
    if not VELOCITY_JSON.exists():
        logger.warning("No velocity cache found at %s", VELOCITY_JSON)
        return {}

    with open(VELOCITY_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info("Loaded velocity data for %d videos from cache", len(data))
    return data


def save_velocity_cache(data: Dict[str, dict]) -> None:
    """Save velocity data to JSON cache."""
    with open(VELOCITY_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("Saved velocity data for %d videos to %s", len(data), VELOCITY_JSON)


# =========================================================================
# API FETCH
# =========================================================================

def fetch_velocity_data(
    metadata: Dict[str, dict],
    video_ids: Optional[List[str]] = None,
) -> Dict[str, dict]:
    """
    Fetch daily metrics for the first 7 days after publish for each video.

    Args:
        metadata: Video metadata dict (needs published_at).
        video_ids: Specific video IDs to fetch. If None, fetches all.

    Returns:
        Dict mapping video_id -> {publish_date, daily: [{day, views, watch_time, subs}]}
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    if video_ids is None:
        video_ids = list(metadata.keys())

    now = datetime.now(timezone.utc)
    result = {}

    logger.info("Fetching velocity data for %d videos from API...", len(video_ids))

    for i, vid_id in enumerate(video_ids):
        meta = metadata.get(vid_id)
        if not meta or not meta.get('published_at'):
            logger.debug("Skipping %s: no published_at", vid_id)
            continue

        # Parse publish date
        try:
            pub_dt = datetime.fromisoformat(meta['published_at'].replace('Z', '+00:00'))
        except (ValueError, TypeError):
            logger.debug("Skipping %s: unparseable published_at", vid_id)
            continue

        pub_date_str = pub_dt.strftime('%Y-%m-%d')
        # End date is 7 days after publish, but not beyond today
        end_dt = min(pub_dt + timedelta(days=7), now)
        end_date_str = end_dt.strftime('%Y-%m-%d')

        # Skip if published today (no data yet)
        if pub_date_str == end_date_str:
            logger.debug("Skipping %s: published today, no data yet", vid_id)
            continue

        try:
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate=pub_date_str,
                endDate=end_date_str,
                metrics='views,estimatedMinutesWatched,subscribersGained',
                dimensions='day',
                filters=f'video=={vid_id}'
            ).execute()

            daily = []
            for row in response.get('rows', []):
                daily.append({
                    'day': row[0],
                    'views': int(row[1]),
                    'watch_time': float(row[2]),
                    'subs': int(row[3]),
                })

            # Sort by day
            daily.sort(key=lambda x: x['day'])

            result[vid_id] = {
                'publish_date': pub_date_str,
                'daily': daily,
            }

            if (i + 1) % 10 == 0:
                logger.info("  Fetched %d/%d videos", i + 1, len(video_ids))

            time.sleep(0.1)

        except Exception as e:
            logger.warning("Failed to fetch velocity for %s: %s", vid_id, e)

    logger.info("Fetched velocity data for %d videos", len(result))
    return result


# =========================================================================
# ANALYSIS ENGINE
# =========================================================================

def compute_velocity_metrics(daily_data: List[dict]) -> dict:
    """
    Compute velocity metrics from daily view data.

    Returns dict with day1_views, day2_views, total_48h, total_7day,
    day1_pct_of_7day, daily_breakdown.
    """
    if not daily_data:
        return {
            'day1_views': 0,
            'day2_views': 0,
            'total_48h': 0,
            'total_7day': 0,
            'day1_pct_of_7day': 0.0,
            'daily_breakdown': [],
        }

    day1_views = daily_data[0]['views'] if len(daily_data) >= 1 else 0
    day2_views = daily_data[1]['views'] if len(daily_data) >= 2 else 0
    total_48h = day1_views + day2_views
    total_7day = sum(d['views'] for d in daily_data)
    day1_pct = (day1_views / total_7day * 100) if total_7day > 0 else 0.0

    return {
        'day1_views': day1_views,
        'day2_views': day2_views,
        'total_48h': total_48h,
        'total_7day': total_7day,
        'day1_pct_of_7day': day1_pct,
        'daily_breakdown': [d['views'] for d in daily_data],
    }


def classify_velocity_curve(daily_data: List[dict]) -> str:
    """
    Classify the velocity curve shape.

    Returns:
        "front_loaded" - >60% of views came in first 2 days
        "delayed_push" - any day after day 2 has more views than day 1
        "steady" - roughly even distribution
    """
    if not daily_data or len(daily_data) < 2:
        return "insufficient_data"

    total = sum(d['views'] for d in daily_data)
    if total == 0:
        return "no_views"

    day1 = daily_data[0]['views']
    day2 = daily_data[1]['views'] if len(daily_data) >= 2 else 0
    first_48h_pct = (day1 + day2) / total * 100

    # Check for delayed push: any day after day 2 exceeds day 1
    later_days = daily_data[2:]
    has_delayed_spike = any(d['views'] > max(day1, 1) for d in later_days)

    if has_delayed_spike:
        return "delayed_push"
    elif first_48h_pct > 60:
        return "front_loaded"
    else:
        return "steady"


def analyze_velocity_by_topic(
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> Dict[str, dict]:
    """
    Group velocity metrics by topic type.

    Returns dict: topic -> {count, avg_day1, avg_48h, avg_7day, videos}
    """
    groups: Dict[str, list] = defaultdict(list)

    for vid_id, vel in velocity_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue
        topic = meta.get('topic_type') or 'unknown'
        metrics = compute_velocity_metrics(vel['daily'])
        groups[topic].append({
            'vid_id': vid_id,
            'title': meta.get('title', ''),
            'lifetime_views': meta.get('views', 0),
            **metrics,
        })

    result = {}
    for topic, videos in sorted(groups.items(), key=lambda x: len(x[1]), reverse=True):
        result[topic] = {
            'count': len(videos),
            'avg_day1': mean(v['day1_views'] for v in videos),
            'avg_48h': mean(v['total_48h'] for v in videos),
            'avg_7day': mean(v['total_7day'] for v in videos),
            'videos': videos,
        }

    return result


def analyze_velocity_by_day(
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> Dict[str, dict]:
    """
    Group velocity metrics by publication day of week.

    Returns dict: day_name -> {count, avg_day1, avg_48h}
    """
    groups: Dict[str, list] = defaultdict(list)

    for vid_id, vel in velocity_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue
        pub_day = meta.get('pub_day', 'Unknown')
        metrics = compute_velocity_metrics(vel['daily'])
        groups[pub_day].append(metrics)

    result = {}
    for day, metrics_list in groups.items():
        result[day] = {
            'count': len(metrics_list),
            'avg_day1': mean(m['day1_views'] for m in metrics_list),
            'avg_48h': mean(m['total_48h'] for m in metrics_list),
            'avg_7day': mean(m['total_7day'] for m in metrics_list),
        }

    return result


def correlate_velocity_lifetime(
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> dict:
    """
    Correlate 48h velocity with lifetime views.

    Returns dict with correlation coefficient, data points, and interpretation.
    """
    points = []
    for vid_id, vel in velocity_data.items():
        meta = metadata.get(vid_id)
        if not meta or not meta.get('views'):
            continue
        metrics = compute_velocity_metrics(vel['daily'])
        if metrics['total_48h'] > 0:
            points.append({
                'vid_id': vid_id,
                'title': meta.get('title', ''),
                'total_48h': metrics['total_48h'],
                'lifetime_views': meta['views'],
                'ratio': meta['views'] / metrics['total_48h'] if metrics['total_48h'] > 0 else 0,
            })

    if len(points) < 3:
        return {
            'correlation': None,
            'n': len(points),
            'interpretation': 'Insufficient data for correlation.',
            'points': points,
        }

    # Pearson correlation
    x = [p['total_48h'] for p in points]
    y = [p['lifetime_views'] for p in points]
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denom_x = sum((xi - mean_x) ** 2 for xi in x) ** 0.5
    denom_y = sum((yi - mean_y) ** 2 for yi in y) ** 0.5

    if denom_x == 0 or denom_y == 0:
        r = 0.0
    else:
        r = numerator / (denom_x * denom_y)

    # Interpretation
    if abs(r) > 0.7:
        interp = f"Strong {'positive' if r > 0 else 'negative'} correlation (r={r:.3f}). 48h velocity is a strong predictor of lifetime views."
    elif abs(r) > 0.4:
        interp = f"Moderate {'positive' if r > 0 else 'negative'} correlation (r={r:.3f}). 48h velocity is a moderate predictor."
    elif abs(r) > 0.2:
        interp = f"Weak {'positive' if r > 0 else 'negative'} correlation (r={r:.3f}). 48h velocity is a weak predictor."
    else:
        interp = f"No meaningful correlation (r={r:.3f}). 48h velocity does not predict lifetime views."

    # Sort by ratio (lifetime / 48h) descending — "overperformers"
    points.sort(key=lambda p: p['ratio'], reverse=True)

    return {
        'correlation': r,
        'n': n,
        'interpretation': interp,
        'points': points,
        'avg_multiplier': mean(p['ratio'] for p in points),
    }


def find_delayed_pushes(
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    Find videos that got an algorithmic push on days 3-7
    (any day after day 2 has more views than day 1).

    Returns list of dicts with video info and spike details.
    """
    pushes = []

    for vid_id, vel in velocity_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        daily = vel['daily']
        if len(daily) < 3:
            continue

        day1_views = daily[0]['views']
        if day1_views == 0:
            continue

        # Check days 3-7 for spikes above day 1
        for idx, day_data in enumerate(daily[2:], start=3):
            if day_data['views'] > day1_views:
                metrics = compute_velocity_metrics(daily)
                pushes.append({
                    'vid_id': vid_id,
                    'title': meta.get('title', ''),
                    'topic_type': meta.get('topic_type', 'unknown'),
                    'day1_views': day1_views,
                    'spike_day': idx,
                    'spike_views': day_data['views'],
                    'spike_ratio': day_data['views'] / day1_views,
                    'total_7day': metrics['total_7day'],
                    'lifetime_views': meta.get('views', 0),
                    'daily_breakdown': [d['views'] for d in daily],
                })
                break  # Only record first spike per video

    # Sort by spike ratio descending
    pushes.sort(key=lambda p: p['spike_ratio'], reverse=True)
    return pushes


# =========================================================================
# SINGLE VIDEO REPORT
# =========================================================================

def single_video_report(
    video_id: str,
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> str:
    """Generate a detailed velocity report for a single video."""
    lines = []

    meta = metadata.get(video_id, {})
    title = meta.get('title', video_id)
    lines.append(f"# Velocity Report: {title}")
    lines.append("")

    vel = velocity_data.get(video_id)
    if not vel:
        lines.append("No velocity data available for this video. Run with --fetch.")
        return "\n".join(lines)

    daily = vel['daily']
    metrics = compute_velocity_metrics(daily)
    curve = classify_velocity_curve(daily)

    lines.append(f"**Published:** {vel['publish_date']}")
    lines.append(f"**Curve type:** {curve}")
    lines.append(f"**Lifetime views:** {meta.get('views', 'N/A'):,}")
    lines.append("")

    # Daily breakdown table
    lines.append("## Daily Breakdown")
    lines.append("")
    lines.append("| Day | Date | Views | Watch Time (min) | Subs Gained |")
    lines.append("|-----|------|------:|----------------:|----------:|")

    for idx, d in enumerate(daily, 1):
        lines.append(
            f"| Day {idx} | {d['day']} | {d['views']:,} "
            f"| {d['watch_time']:.1f} | {d['subs']} |"
        )
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Day 1 views:** {metrics['day1_views']:,}")
    lines.append(f"- **Day 2 views:** {metrics['day2_views']:,}")
    lines.append(f"- **48h total:** {metrics['total_48h']:,}")
    lines.append(f"- **7-day total:** {metrics['total_7day']:,}")
    lines.append(f"- **Day 1 as % of week:** {metrics['day1_pct_of_7day']:.1f}%")

    if meta.get('views') and metrics['total_48h'] > 0:
        multiplier = meta['views'] / metrics['total_48h']
        lines.append(f"- **Lifetime / 48h ratio:** {multiplier:.1f}x")

    return "\n".join(lines)


# =========================================================================
# FULL REPORT GENERATION
# =========================================================================

def generate_full_report(
    velocity_data: Dict[str, dict],
    metadata: Dict[str, dict],
) -> str:
    """Generate the complete velocity analysis report."""

    # Filter to videos with both velocity and metadata
    common_ids = set(velocity_data.keys()) & set(metadata.keys())
    filtered_vel = {k: v for k, v in velocity_data.items() if k in common_ids}

    if not filtered_vel:
        return ("# First-Week Velocity Analysis\n\n"
                "No data available. Run with --fetch to pull from API.")

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines = []

    lines.append("# First-Week Velocity Analysis")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {len(filtered_vel)}")
    lines.append("")

    # ------------------------------------------------------------------
    # Section 1: Velocity Summary
    # ------------------------------------------------------------------
    lines.append("## 1. Velocity Summary")
    lines.append("")
    lines.append("| # | Title | Day 1 | Day 2 | 48h Total | 7-Day Total | Day1 % of Week | Curve Type |")
    lines.append("|---|-------|------:|------:|----------:|----------:|-------------:|-----------|")

    # Build per-video metrics
    all_metrics = []
    for vid_id, vel in filtered_vel.items():
        meta = metadata[vid_id]
        metrics = compute_velocity_metrics(vel['daily'])
        curve = classify_velocity_curve(vel['daily'])
        all_metrics.append({
            'vid_id': vid_id,
            'title': meta.get('title', vid_id),
            'topic_type': meta.get('topic_type', 'unknown'),
            'pub_day': meta.get('pub_day', 'Unknown'),
            'lifetime_views': meta.get('views', 0),
            'curve': curve,
            **metrics,
        })

    # Sort by 48h total descending
    all_metrics.sort(key=lambda m: m['total_48h'], reverse=True)

    for i, m in enumerate(all_metrics, 1):
        title_short = m['title'][:45] + ('...' if len(m['title']) > 45 else '')
        lines.append(
            f"| {i} | {title_short} | {m['day1_views']:,} | {m['day2_views']:,} "
            f"| {m['total_48h']:,} | {m['total_7day']:,} "
            f"| {m['day1_pct_of_7day']:.0f}% | {m['curve']} |"
        )
    lines.append("")

    # ------------------------------------------------------------------
    # Section 2: Velocity Curve Types
    # ------------------------------------------------------------------
    lines.append("## 2. Velocity Curve Types")
    lines.append("")
    lines.append("| Type | Count | Avg 48h Views | Avg 7-Day Views | Avg Lifetime Views |")
    lines.append("|------|------:|-------------:|---------------:|------------------:|")

    curve_groups: Dict[str, list] = defaultdict(list)
    for m in all_metrics:
        curve_groups[m['curve']].append(m)

    for curve_type in ['front_loaded', 'steady', 'delayed_push', 'insufficient_data', 'no_views']:
        vids = curve_groups.get(curve_type, [])
        if not vids:
            continue
        avg_48h = mean(v['total_48h'] for v in vids)
        avg_7d = mean(v['total_7day'] for v in vids)
        avg_lt = mean(v['lifetime_views'] for v in vids)
        lines.append(
            f"| {curve_type} | {len(vids)} | {avg_48h:,.0f} | {avg_7d:,.0f} | {avg_lt:,.0f} |"
        )
    lines.append("")

    # Interpretation
    if 'delayed_push' in curve_groups and 'front_loaded' in curve_groups:
        dp_avg = mean(v['lifetime_views'] for v in curve_groups['delayed_push'])
        fl_avg = mean(v['lifetime_views'] for v in curve_groups['front_loaded'])
        if dp_avg > fl_avg:
            lines.append(
                f"**Insight:** Delayed-push videos average {dp_avg:,.0f} lifetime views "
                f"vs {fl_avg:,.0f} for front-loaded. Algorithm pushes signal long-term success."
            )
        else:
            lines.append(
                f"**Insight:** Front-loaded videos average {fl_avg:,.0f} lifetime views "
                f"vs {dp_avg:,.0f} for delayed-push. Early momentum matters for this channel."
            )
    lines.append("")

    # ------------------------------------------------------------------
    # Section 3: Velocity by Topic Type
    # ------------------------------------------------------------------
    lines.append("## 3. Velocity by Topic Type")
    lines.append("")

    topic_vel = analyze_velocity_by_topic(filtered_vel, metadata)

    lines.append("| Topic | n | Avg Day 1 | Avg 48h | Avg 7-Day |")
    lines.append("|-------|--:|--------:|---------:|--------:|")

    for topic, data in sorted(topic_vel.items(), key=lambda x: x[1]['avg_48h'], reverse=True):
        lines.append(
            f"| {topic} | {data['count']} | {data['avg_day1']:,.0f} "
            f"| {data['avg_48h']:,.0f} | {data['avg_7day']:,.0f} |"
        )
    lines.append("")

    # ------------------------------------------------------------------
    # Section 4: Velocity by Publication Day
    # ------------------------------------------------------------------
    lines.append("## 4. Velocity by Publication Day")
    lines.append("")

    day_vel = analyze_velocity_by_day(filtered_vel, metadata)

    lines.append("| Day | n | Avg Day 1 | Avg 48h | Avg 7-Day |")
    lines.append("|-----|--:|--------:|---------:|--------:|")

    # Sort by day of week (Mon-Sun)
    for day_name in DAY_NAMES:
        data = day_vel.get(day_name)
        if not data:
            continue
        lines.append(
            f"| {day_name} | {data['count']} | {data['avg_day1']:,.0f} "
            f"| {data['avg_48h']:,.0f} | {data['avg_7day']:,.0f} |"
        )
    # Handle Unknown
    if 'Unknown' in day_vel:
        data = day_vel['Unknown']
        lines.append(
            f"| Unknown | {data['count']} | {data['avg_day1']:,.0f} "
            f"| {data['avg_48h']:,.0f} | {data['avg_7day']:,.0f} |"
        )
    lines.append("")

    # Best/worst day
    valid_days = {k: v for k, v in day_vel.items() if k != 'Unknown' and v['count'] >= 2}
    if valid_days:
        best_day = max(valid_days.items(), key=lambda x: x[1]['avg_48h'])
        worst_day = min(valid_days.items(), key=lambda x: x[1]['avg_48h'])
        lines.append(
            f"**Best velocity day:** {best_day[0]} ({best_day[1]['avg_48h']:,.0f} avg 48h views, n={best_day[1]['count']})"
        )
        lines.append(
            f"**Worst velocity day:** {worst_day[0]} ({worst_day[1]['avg_48h']:,.0f} avg 48h views, n={worst_day[1]['count']})"
        )
    lines.append("")

    # ------------------------------------------------------------------
    # Section 5: Delayed Algorithm Pushes
    # ------------------------------------------------------------------
    lines.append("## 5. Delayed Algorithm Pushes")
    lines.append("")
    lines.append("Videos where YouTube pushed views on days 3-7 (spike > day 1):")
    lines.append("")

    pushes = find_delayed_pushes(filtered_vel, metadata)

    if pushes:
        lines.append("| # | Title | Topic | Day 1 | Spike Day | Spike Views | Spike/Day1 | Lifetime |")
        lines.append("|---|-------|-------|------:|--------:|----------:|--------:|--------:|")

        for i, p in enumerate(pushes, 1):
            title_short = p['title'][:40] + ('...' if len(p['title']) > 40 else '')
            lines.append(
                f"| {i} | {title_short} | {p['topic_type']} "
                f"| {p['day1_views']:,} | Day {p['spike_day']} "
                f"| {p['spike_views']:,} | {p['spike_ratio']:.1f}x "
                f"| {p['lifetime_views']:,} |"
            )
        lines.append("")

        # Show daily sparkline for top 3
        lines.append("### Daily View Curves (Top Delayed Pushes)")
        lines.append("")
        for p in pushes[:3]:
            breakdown = " -> ".join(str(v) for v in p['daily_breakdown'])
            lines.append(f"- **{p['title'][:50]}**: {breakdown}")
        lines.append("")
    else:
        lines.append("*No delayed algorithm pushes detected.*")
        lines.append("")

    # ------------------------------------------------------------------
    # Section 6: 48h Velocity -> Lifetime Views Correlation
    # ------------------------------------------------------------------
    lines.append("## 6. 48h Velocity -> Lifetime Views Correlation")
    lines.append("")
    lines.append("Does early performance predict long-term success?")
    lines.append("")

    corr = correlate_velocity_lifetime(filtered_vel, metadata)
    lines.append(f"**Pearson r:** {corr['correlation']:.3f}" if corr['correlation'] is not None else "**Pearson r:** N/A")
    lines.append(f"**n:** {corr['n']}")
    lines.append(f"**Interpretation:** {corr['interpretation']}")
    lines.append("")

    if corr.get('avg_multiplier'):
        lines.append(f"**Average lifetime/48h multiplier:** {corr['avg_multiplier']:.1f}x")
        lines.append("")

    # Show biggest overperformers (high lifetime/48h ratio)
    if corr['points']:
        lines.append("### Overperformers (Highest Lifetime / 48h Ratio)")
        lines.append("")
        lines.append("Videos that far exceeded their 48h trajectory:")
        lines.append("")
        lines.append("| # | Title | 48h Views | Lifetime Views | Ratio |")
        lines.append("|---|-------|--------:|--------------:|------:|")

        for i, p in enumerate(corr['points'][:10], 1):
            title_short = p['title'][:45] + ('...' if len(p['title']) > 45 else '')
            lines.append(
                f"| {i} | {title_short} | {p['total_48h']:,} "
                f"| {p['lifetime_views']:,} | {p['ratio']:.1f}x |"
            )
        lines.append("")

    # ------------------------------------------------------------------
    # Section 7: Interpreted Findings
    # ------------------------------------------------------------------
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = _generate_findings(all_metrics, curve_groups, day_vel, pushes, corr)
    for finding in findings:
        lines.append(f"- {finding}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(
        f"*Generated by `velocity_analysis.py` on {now}. "
        f"Data covers {len(filtered_vel)} long-form videos.*"
    )

    return "\n".join(lines)


def _generate_findings(
    all_metrics: list,
    curve_groups: Dict[str, list],
    day_vel: Dict[str, dict],
    pushes: list,
    corr: dict,
) -> List[str]:
    """Generate actionable findings from the analysis."""
    findings = []

    # Finding 1: Dominant curve type
    if curve_groups:
        dominant = max(curve_groups.items(), key=lambda x: len(x[1]))
        total = sum(len(v) for v in curve_groups.values())
        pct = len(dominant[1]) / total * 100
        findings.append(
            f"**{pct:.0f}% of videos are {dominant[0]}** ({len(dominant[1])}/{total}). "
            f"This is the channel's typical velocity pattern."
        )

    # Finding 2: 48h benchmark
    if all_metrics:
        median_48h = sorted(m['total_48h'] for m in all_metrics)[len(all_metrics) // 2]
        mean_48h = mean(m['total_48h'] for m in all_metrics)
        findings.append(
            f"**48h benchmark:** median {median_48h:,} views, mean {mean_48h:,.0f} views. "
            f"Videos exceeding {median_48h * 2:,} in 48h are outperformers."
        )

    # Finding 3: Best publication day
    valid_days = {k: v for k, v in day_vel.items() if k != 'Unknown' and v['count'] >= 2}
    if valid_days:
        best = max(valid_days.items(), key=lambda x: x[1]['avg_48h'])
        worst = min(valid_days.items(), key=lambda x: x[1]['avg_48h'])
        if best[1]['avg_48h'] > 0 and worst[1]['avg_48h'] > 0:
            ratio = best[1]['avg_48h'] / worst[1]['avg_48h']
            findings.append(
                f"**Publication day matters:** {best[0]} gets {ratio:.1f}x more 48h views "
                f"than {worst[0]} (n={best[1]['count']} vs n={worst[1]['count']})."
            )

    # Finding 4: Delayed pushes
    if pushes:
        findings.append(
            f"**{len(pushes)} videos got delayed algorithm pushes** (day 3-7 spike). "
            f"This suggests YouTube tested and then promoted these videos."
        )
        # Check if delayed push videos have higher lifetime views
        push_ids = {p['vid_id'] for p in pushes}
        push_lt = [m['lifetime_views'] for m in all_metrics if m['vid_id'] in push_ids]
        non_push_lt = [m['lifetime_views'] for m in all_metrics if m['vid_id'] not in push_ids]
        if push_lt and non_push_lt:
            push_avg = mean(push_lt)
            non_avg = mean(non_push_lt)
            if push_avg > non_avg:
                findings.append(
                    f"**Delayed-push videos average {push_avg:,.0f} lifetime views** "
                    f"vs {non_avg:,.0f} for non-pushed videos ({push_avg / non_avg:.1f}x)."
                )

    # Finding 5: Correlation
    if corr.get('correlation') is not None:
        r = corr['correlation']
        if abs(r) > 0.5:
            findings.append(
                f"**48h velocity predicts lifetime success** (r={r:.3f}). "
                f"Invest in launch-day promotion (community posts, social sharing)."
            )
        elif abs(r) < 0.3:
            findings.append(
                f"**48h velocity does NOT predict lifetime success** (r={r:.3f}). "
                f"Evergreen search traffic matters more than launch-day spikes."
            )

    # Finding 6: Top performer
    if all_metrics:
        top = all_metrics[0]  # Already sorted by 48h desc
        findings.append(
            f"**Fastest launch:** \"{top['title'][:50]}\" with {top['total_48h']:,} views in 48h."
        )

    return findings


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Analyze first-48h and first-7-day view velocity patterns.'
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full report to channel-data/patterns/')
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch fresh data from YouTube Analytics API')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached data only (skip API)')
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

    # Fetch or load velocity data
    if args.fetch:
        logger.info("Fetching fresh velocity data from YouTube Analytics API...")
        video_ids = [args.video] if args.video else None
        fresh_data = fetch_velocity_data(metadata, video_ids)
        if fresh_data:
            # Merge with existing cache
            existing = load_velocity_cache()
            existing.update(fresh_data)
            save_velocity_cache(existing)
            velocity_data = existing
        else:
            logger.warning("No data fetched. Falling back to cache.")
            velocity_data = load_velocity_cache()
    else:
        velocity_data = load_velocity_cache()

    if not velocity_data:
        logger.error("No velocity data available. Run with --fetch to pull from API.")
        sys.exit(1)

    logger.info("Velocity data: %d videos. Metadata: %d videos.",
                len(velocity_data), len(metadata))

    # Single video mode
    if args.video:
        report = single_video_report(args.video, velocity_data, metadata)
        print(report)
        return

    # Full report mode (--report or --cached both generate report)
    if args.report or args.cached:
        report = generate_full_report(velocity_data, metadata)

        # Save to file
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        # Also print to stdout
        print(report)


if __name__ == '__main__':
    main()
