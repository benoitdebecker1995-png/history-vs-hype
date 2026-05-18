"""
End Screen Analysis Tool

Analyzes end screen performance by combining YouTube Analytics API card/annotation
metrics with traffic source data. Falls back gracefully to traffic-source-only
analysis when API metrics are unavailable.

Data sources:
  - YouTube Analytics API (card/annotation metrics via --fetch)
  - _traffic_sources.json (end screen traffic already fetched by traffic_analysis)
  - _endscreen_data.json (cached card/annotation metrics from this tool)
  - analytics.db (videos table for metadata)

Usage:
    python -m tools.youtube_analytics.endscreen_analysis --report      # Full report
    python -m tools.youtube_analytics.endscreen_analysis --fetch       # Fetch card metrics
    python -m tools.youtube_analytics.endscreen_analysis --cached      # Skip API, cache only
    python -m tools.youtube_analytics.endscreen_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/ENDSCREEN-ANALYSIS.md
"""

import sys
import json
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
TRAFFIC_JSON = Path(__file__).parent / '_traffic_sources.json'
ENDSCREEN_JSON = Path(__file__).parent / '_endscreen_data.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'ENDSCREEN-ANALYSIS.md'

# Traffic source types that represent end screen / annotation traffic
ENDSCREEN_SOURCE_TYPES = {'END_SCREEN', 'ANNOTATION', 'CAMPAIGN_CARD'}

# Metric sets to try in order (YouTube Analytics API is inconsistent)
METRIC_SETS = [
    {
        'name': 'cards',
        'metrics': 'cardClickRate,cardImpressions,cardClicks,cardTeaserImpressions,cardTeaserClicks',
        'fields': ['card_click_rate', 'card_impressions', 'card_clicks',
                   'card_teaser_impressions', 'card_teaser_clicks'],
    },
    {
        'name': 'annotations',
        'metrics': 'annotationClickThroughRate,annotationImpressions,annotationClicks',
        'fields': ['annotation_ctr', 'annotation_impressions', 'annotation_clicks'],
    },
]


# =========================================================================
# DATA LOADING
# =========================================================================

def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        rows = store.videos(min_duration_seconds=61)  # preserve old `> 60`

    result = {r['video_id']: {
        'video_id': r['video_id'], 'title': r['title'],
        'topic_type': r['topic_type'], 'views': r['views'],
        'duration_seconds': r['duration_seconds'],
    } for r in rows}

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


def load_traffic_sources() -> Dict[str, List[dict]]:
    """Load traffic source data from the JSON cache file."""
    if not TRAFFIC_JSON.exists():
        logger.warning("No traffic sources JSON found at %s", TRAFFIC_JSON)
        return {}

    with open(TRAFFIC_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info("Loaded traffic data for %d videos from JSON cache", len(data))
    return data


def load_endscreen_cache() -> Dict[str, dict]:
    """Load cached end screen / card metrics."""
    if not ENDSCREEN_JSON.exists():
        logger.info("No endscreen cache found at %s", ENDSCREEN_JSON)
        return {}

    with open(ENDSCREEN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info("Loaded endscreen cache for %d videos", len(data))
    return data


def save_endscreen_cache(data: Dict[str, dict]) -> None:
    """Save end screen / card metrics to JSON cache."""
    with open(ENDSCREEN_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("Saved endscreen data to %s", ENDSCREEN_JSON)


# =========================================================================
# API FETCH
# =========================================================================

def fetch_card_metrics(video_ids: Optional[List[str]] = None) -> Dict[str, dict]:
    """
    Fetch card/annotation metrics from YouTube Analytics API.

    Tries multiple metric sets because YouTube frequently changes
    which metrics are available. Returns whatever data is obtainable.

    Args:
        video_ids: Specific video IDs to fetch. If None, fetches all from DB.

    Returns:
        Dict mapping video_id -> dict of available metrics.
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    if video_ids is None:
        metadata = load_video_metadata()
        video_ids = list(metadata.keys())

    logger.info("Fetching end screen / card metrics for %d videos...", len(video_ids))

    # Determine which metric set works by testing the first video
    working_metric_set = None
    for metric_set in METRIC_SETS:
        if not video_ids:
            break
        try:
            test_response = analytics.reports().query(
                ids='channel==MINE',
                startDate='2024-01-01',
                endDate='2026-12-31',
                metrics=metric_set['metrics'],
                filters=f'video=={video_ids[0]}'
            ).execute()
            working_metric_set = metric_set
            logger.info("Using metric set '%s': %s",
                        metric_set['name'], metric_set['metrics'])
            break
        except Exception as e:
            logger.warning("Metric set '%s' not available: %s",
                           metric_set['name'], e)

    if working_metric_set is None:
        logger.warning(
            "No card/annotation metrics available from the YouTube Analytics API. "
            "This is common — YouTube deprecated annotation metrics and card metrics "
            "may require specific API access. Falling back to traffic source data."
        )
        return {}

    result = {}
    fields = working_metric_set['fields']

    for i, vid_id in enumerate(video_ids):
        try:
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate='2024-01-01',
                endDate='2026-12-31',
                metrics=working_metric_set['metrics'],
                filters=f'video=={vid_id}'
            ).execute()

            rows = response.get('rows', [])
            if rows:
                row = rows[0]
                entry = {
                    'metric_set': working_metric_set['name'],
                    'fetched_at': datetime.now(timezone.utc).isoformat(),
                }
                for j, field_name in enumerate(fields):
                    if j < len(row):
                        entry[field_name] = row[j]
                result[vid_id] = entry

            if (i + 1) % 10 == 0:
                logger.info("  Fetched %d/%d videos", i + 1, len(video_ids))

        except Exception as e:
            logger.warning("Failed to fetch card metrics for %s: %s", vid_id, e)

    logger.info("Fetched card/annotation data for %d videos", len(result))
    return result


# =========================================================================
# ANALYSIS — TRAFFIC SOURCE BASED (primary / fallback)
# =========================================================================

def extract_endscreen_traffic(
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    Extract end screen / annotation traffic from traffic source data.

    Returns list of dicts with video_id, title, topic_type, total_views,
    endscreen_views, endscreen_watch_minutes, endscreen_pct.
    """
    results = []

    for vid_id, sources in traffic_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        total_views = sum(s['views'] for s in sources)
        if total_views == 0:
            continue

        es_views = 0
        es_minutes = 0.0
        for s in sources:
            if s['source_type'] in ENDSCREEN_SOURCE_TYPES:
                es_views += s['views']
                es_minutes += s.get('watch_time_minutes', 0.0)

        results.append({
            'video_id': vid_id,
            'title': meta.get('title', vid_id),
            'topic_type': meta.get('topic_type', 'unknown'),
            'total_views': meta.get('views', total_views),
            'traffic_total_views': total_views,
            'endscreen_views': es_views,
            'endscreen_watch_minutes': round(es_minutes, 1),
            'endscreen_pct': round(es_views / total_views * 100, 2) if total_views else 0.0,
        })

    results.sort(key=lambda x: x['endscreen_views'], reverse=True)
    return results


def compute_endscreen_ctr(endscreen_cache: Dict[str, dict]) -> List[dict]:
    """
    Compute end screen / card CTR from cached API data.

    Returns sorted list of dicts with video_id and CTR metrics.
    Only useful if card/annotation metrics were successfully fetched.
    """
    results = []

    for vid_id, data in endscreen_cache.items():
        metric_set = data.get('metric_set', '')
        entry = {'video_id': vid_id, 'metric_set': metric_set}

        if metric_set == 'cards':
            impressions = data.get('card_impressions', 0)
            clicks = data.get('card_clicks', 0)
            entry['impressions'] = impressions
            entry['clicks'] = clicks
            entry['ctr'] = round(clicks / impressions * 100, 2) if impressions else 0.0
            # Also include teaser metrics
            entry['teaser_impressions'] = data.get('card_teaser_impressions', 0)
            entry['teaser_clicks'] = data.get('card_teaser_clicks', 0)
        elif metric_set == 'annotations':
            impressions = data.get('annotation_impressions', 0)
            clicks = data.get('annotation_clicks', 0)
            entry['impressions'] = impressions
            entry['clicks'] = clicks
            entry['ctr'] = data.get('annotation_ctr', 0.0)
        else:
            continue

        results.append(entry)

    results.sort(key=lambda x: x.get('ctr', 0), reverse=True)
    return results


def analyze_by_topic(
    endscreen_traffic: List[dict],
) -> List[dict]:
    """
    Aggregate end screen traffic by topic_type.

    Returns list of dicts with topic, count, avg_endscreen_views,
    avg_endscreen_pct, total_endscreen_views.
    """
    topic_groups: Dict[str, List[dict]] = defaultdict(list)

    for entry in endscreen_traffic:
        topic = entry.get('topic_type', 'unknown') or 'unknown'
        topic_groups[topic].append(entry)

    results = []
    for topic, entries in topic_groups.items():
        es_views_list = [e['endscreen_views'] for e in entries]
        es_pct_list = [e['endscreen_pct'] for e in entries]

        results.append({
            'topic': topic,
            'count': len(entries),
            'total_endscreen_views': sum(es_views_list),
            'avg_endscreen_views': round(mean(es_views_list), 1) if es_views_list else 0,
            'avg_endscreen_pct': round(mean(es_pct_list), 2) if es_pct_list else 0,
        })

    results.sort(key=lambda x: x['avg_endscreen_pct'], reverse=True)
    return results


def estimate_endscreen_value(
    endscreen_traffic: List[dict],
) -> dict:
    """
    Estimate the total value of end screen traffic across the channel.

    Returns dict with total views from end screens, percentage of all traffic,
    total watch time, and average per video.
    """
    total_es_views = sum(e['endscreen_views'] for e in endscreen_traffic)
    total_es_minutes = sum(e['endscreen_watch_minutes'] for e in endscreen_traffic)
    total_all_views = sum(e['traffic_total_views'] for e in endscreen_traffic)
    videos_with_es = sum(1 for e in endscreen_traffic if e['endscreen_views'] > 0)
    total_videos = len(endscreen_traffic)

    return {
        'total_endscreen_views': total_es_views,
        'total_all_views': total_all_views,
        'endscreen_pct_of_all': round(
            total_es_views / total_all_views * 100, 2
        ) if total_all_views else 0.0,
        'total_endscreen_watch_minutes': round(total_es_minutes, 1),
        'videos_with_endscreen_traffic': videos_with_es,
        'total_videos': total_videos,
        'avg_endscreen_views_per_video': round(
            total_es_views / total_videos, 1
        ) if total_videos else 0,
    }


# =========================================================================
# REPORT GENERATION
# =========================================================================

def generate_report(
    endscreen_traffic: List[dict],
    topic_analysis: List[dict],
    value_estimate: dict,
    card_metrics: List[dict],
    metadata: Dict[str, dict],
    card_data_available: bool,
) -> str:
    """Generate the full markdown report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    if card_data_available:
        availability = (
            "Card/annotation metrics fetched via YouTube Analytics API. "
            "Traffic source data also available."
        )
    else:
        availability = (
            "Card/annotation metrics **not available** from YouTube Analytics API "
            "(common — YouTube deprecated annotation metrics in 2017 and card metrics "
            "require specific API access). Analysis uses traffic source data "
            "(END_SCREEN / ANNOTATION source types) as primary data source."
        )

    lines = [
        "# End Screen Analysis",
        f"**Generated:** {now}",
        f"**Data availability:** {availability}",
        "",
    ]

    # ---- Section 1: End Screen Traffic Volume ----
    lines.append("## 1. End Screen Traffic Volume")
    lines.append("")

    v = value_estimate
    lines.append(
        f"End screens generated **{v['total_endscreen_views']:,}** views "
        f"out of **{v['total_all_views']:,}** total traffic-source views "
        f"(**{v['endscreen_pct_of_all']}%** of all traffic)."
    )
    lines.append("")
    lines.append(f"- Videos with end screen traffic: "
                 f"**{v['videos_with_endscreen_traffic']}** / {v['total_videos']}")
    lines.append(f"- Total watch time from end screens: "
                 f"**{v['total_endscreen_watch_minutes']:,.1f}** minutes")
    lines.append(f"- Average end screen views per video: "
                 f"**{v['avg_endscreen_views_per_video']:.1f}**")
    lines.append("")

    # ---- Section 2: End Screen Performance by Video ----
    lines.append("## 2. End Screen Performance by Video")
    lines.append("")

    # Only show videos that have any end screen traffic, plus top videos by total
    videos_with_es = [e for e in endscreen_traffic if e['endscreen_views'] > 0]

    if videos_with_es:
        lines.append(
            f"**{len(videos_with_es)} videos** received traffic from end screens:"
        )
        lines.append("")
        lines.append("| # | Title | End Screen Views | % of Traffic | "
                      "Watch Min | Topic |")
        lines.append("|---|-------|-----------------|-------------|"
                      "----------|-------|")

        for i, entry in enumerate(videos_with_es[:30], 1):
            title = entry['title']
            if len(title) > 50:
                title = title[:47] + "..."
            lines.append(
                f"| {i} | {title} | {entry['endscreen_views']:,} | "
                f"{entry['endscreen_pct']:.1f}% | "
                f"{entry['endscreen_watch_minutes']:.1f} | "
                f"{entry['topic_type'] or 'unknown'} |"
            )

        lines.append("")
    else:
        lines.append("No videos have recorded end screen traffic in the traffic "
                      "source data.")
        lines.append("")

    # Also show top videos WITHOUT end screen traffic for context
    videos_no_es = [e for e in endscreen_traffic if e['endscreen_views'] == 0]
    if videos_no_es and videos_with_es:
        top_no_es = sorted(videos_no_es, key=lambda x: x['total_views'], reverse=True)[:5]
        lines.append(f"**Top videos with zero end screen traffic** "
                      f"({len(videos_no_es)} videos total):")
        lines.append("")
        for entry in top_no_es:
            title = entry['title']
            if len(title) > 60:
                title = title[:57] + "..."
            lines.append(f"- {title} ({entry['total_views']:,} views)")
        lines.append("")

    # ---- Section 3: End Screen by Topic Type ----
    lines.append("## 3. End Screen by Topic Type")
    lines.append("")

    if topic_analysis:
        lines.append("| Topic | Videos | Total ES Views | Avg ES Views | "
                      "Avg % of Traffic |")
        lines.append("|-------|--------|---------------|-------------|"
                      "----------------|")

        for t in topic_analysis:
            lines.append(
                f"| {t['topic']} | {t['count']} | "
                f"{t['total_endscreen_views']:,} | "
                f"{t['avg_endscreen_views']:.1f} | "
                f"{t['avg_endscreen_pct']:.2f}% |"
            )

        lines.append("")
    else:
        lines.append("Insufficient data for topic-level analysis.")
        lines.append("")

    # ---- Section 4: Card / Annotation Metrics ----
    lines.append("## 4. Card/Annotation Metrics")
    lines.append("")

    if card_metrics:
        lines.append(
            f"Card/annotation data available for **{len(card_metrics)} videos**:"
        )
        lines.append("")

        # Determine column headers based on metric set
        sample_set = card_metrics[0].get('metric_set', 'cards')
        if sample_set == 'cards':
            lines.append("| # | Video | Card Impressions | Card Clicks | "
                          "Card CTR | Teaser Imp | Teaser Clicks |")
            lines.append("|---|-------|-----------------|------------|"
                          "---------|------------|---------------|")

            for i, cm in enumerate(card_metrics[:30], 1):
                vid_id = cm['video_id']
                title = metadata.get(vid_id, {}).get('title', vid_id)
                if len(title) > 40:
                    title = title[:37] + "..."
                lines.append(
                    f"| {i} | {title} | {cm.get('impressions', 0):,} | "
                    f"{cm.get('clicks', 0):,} | {cm.get('ctr', 0):.2f}% | "
                    f"{cm.get('teaser_impressions', 0):,} | "
                    f"{cm.get('teaser_clicks', 0):,} |"
                )
        else:
            lines.append("| # | Video | Impressions | Clicks | CTR |")
            lines.append("|---|-------|------------|--------|-----|")

            for i, cm in enumerate(card_metrics[:30], 1):
                vid_id = cm['video_id']
                title = metadata.get(vid_id, {}).get('title', vid_id)
                if len(title) > 50:
                    title = title[:47] + "..."
                lines.append(
                    f"| {i} | {title} | {cm.get('impressions', 0):,} | "
                    f"{cm.get('clicks', 0):,} | {cm.get('ctr', 0):.2f}% |"
                )

        lines.append("")
    else:
        lines.append(
            "Card/annotation metrics are **not available** from the YouTube "
            "Analytics API. This is expected for most channels — YouTube "
            "deprecated annotation metrics and card-level metrics require "
            "specific API access that may not be enabled."
        )
        lines.append("")
        lines.append(
            "To get end screen performance data, use YouTube Studio directly: "
            "Analytics > Reach > End screen element click rate."
        )
        lines.append("")

    # ---- Section 5: Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    total_es = value_estimate['total_endscreen_views']
    total_all = value_estimate['total_all_views']
    es_pct = value_estimate['endscreen_pct_of_all']
    vids_with = value_estimate['videos_with_endscreen_traffic']
    total_vids = value_estimate['total_videos']

    if total_es == 0:
        lines.append(
            "- **No end screen traffic detected.** Either end screens are not "
            "configured on videos, or traffic from end screens is below the "
            "reporting threshold in the YouTube Analytics API."
        )
        lines.append(
            "- **Recommendation:** Add end screen elements (subscribe button + "
            "best-for-viewer video) to all videos. Even at small scale, end "
            "screens compound — each end screen click is a free impression."
        )
    else:
        lines.append(
            f"- End screens account for **{es_pct:.1f}%** of total traffic "
            f"({total_es:,} / {total_all:,} views). "
        )

        if es_pct < 1.0:
            lines.append(
                "  This is below the typical 2-5% benchmark for channels "
                "with optimized end screens."
            )
            lines.append(
                "- **Low-hanging fruit:** End screen optimization has minimal "
                "effort and guaranteed upside. Even a 1% improvement means "
                f"~{total_all // 100:,} additional views at current traffic levels."
            )
        elif es_pct < 3.0:
            lines.append(
                "  This is in the low-to-average range. There is room to improve "
                "by testing different end screen video suggestions."
            )
        else:
            lines.append(
                "  This is a healthy end screen traffic rate. Maintain current "
                "end screen strategy."
            )

        if vids_with < total_vids * 0.5:
            lines.append(
                f"- **Coverage gap:** Only {vids_with}/{total_vids} videos "
                f"({vids_with / total_vids * 100:.0f}%) have end screen traffic. "
                f"Ensure all videos have end screen elements configured."
            )

    lines.append("")
    lines.append("### Actionable Recommendations")
    lines.append("")
    lines.append("1. **Add end screens to every video** — subscribe button + "
                 "\"best for viewer\" algorithm-picked video.")
    lines.append("2. **Place end screens at a natural pause** — not mid-sentence. "
                 "Script a brief outro (\"If you want to see how this played out...\").")
    lines.append("3. **Use end screen to chain related content** — territorial "
                 "dispute videos should link to other territorial disputes.")
    lines.append("4. **Check YouTube Studio** for end screen element click rate "
                 "(Analytics > Reach) — this data is more granular than what the "
                 "API provides.")
    lines.append("5. **Monitor end screens in playlists** — playlist viewers "
                 "auto-advance, making end screens less critical but still "
                 "useful for non-playlist traffic.")
    lines.append("")

    return "\n".join(lines)


# =========================================================================
# MAIN
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='End Screen Analysis — card metrics + traffic source data'
    )
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch card/annotation metrics from YouTube Analytics API')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached data only, skip API calls')
    parser.add_argument('--report', action='store_true',
                        help='Generate markdown report')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress info logging')
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not args.report and not args.fetch:
        args.report = True

    # Load video metadata
    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata found in analytics.db. Run backfill first.")
        sys.exit(1)

    # ---- Fetch or load card/annotation metrics ----
    endscreen_cache: Dict[str, dict] = {}
    card_data_available = False

    if args.fetch and not args.cached:
        logger.info("Fetching card/annotation metrics from YouTube Analytics API...")
        fresh_data = fetch_card_metrics()
        if fresh_data:
            # Merge with existing cache
            existing = load_endscreen_cache()
            existing.update(fresh_data)
            save_endscreen_cache(existing)
            endscreen_cache = existing
            card_data_available = True
        else:
            logger.info(
                "No card/annotation metrics available from API. "
                "Will analyze using traffic source data instead."
            )
            endscreen_cache = load_endscreen_cache()
            card_data_available = bool(endscreen_cache)
    else:
        endscreen_cache = load_endscreen_cache()
        card_data_available = bool(endscreen_cache)

    # ---- Load traffic source data (always needed as fallback / primary) ----
    traffic_data = load_traffic_sources()
    if not traffic_data:
        logger.warning(
            "No traffic source data found. Run "
            "'python -m tools.youtube_analytics.traffic_analysis --fetch' first."
        )
        if not card_data_available:
            logger.error(
                "No data available at all (no card metrics, no traffic sources). "
                "Cannot generate report."
            )
            sys.exit(1)

    logger.info(
        "Data loaded: %d videos in metadata, %d in traffic sources, "
        "%d with card metrics.",
        len(metadata), len(traffic_data), len(endscreen_cache),
    )

    # ---- Run analysis ----
    endscreen_traffic = extract_endscreen_traffic(traffic_data, metadata)
    topic_analysis = analyze_by_topic(endscreen_traffic)
    value_estimate = estimate_endscreen_value(endscreen_traffic)
    card_metrics = compute_endscreen_ctr(endscreen_cache) if endscreen_cache else []

    logger.info(
        "Analysis complete: %d videos analyzed, %d with end screen traffic, "
        "%d with card metrics.",
        len(endscreen_traffic),
        value_estimate['videos_with_endscreen_traffic'],
        len(card_metrics),
    )

    # ---- Generate report ----
    if args.report or not args.fetch:
        report = generate_report(
            endscreen_traffic=endscreen_traffic,
            topic_analysis=topic_analysis,
            value_estimate=value_estimate,
            card_metrics=card_metrics,
            metadata=metadata,
            card_data_available=card_data_available,
        )

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        print(report)

    elif args.fetch:
        # Fetch-only mode — just print summary
        print(f"Fetched card metrics for {len(endscreen_cache)} videos.")
        print(f"Traffic source data covers {len(traffic_data)} videos.")
        es_count = sum(
            1 for e in endscreen_traffic if e['endscreen_views'] > 0
        )
        print(f"Videos with end screen traffic: {es_count}")


if __name__ == '__main__':
    main()
