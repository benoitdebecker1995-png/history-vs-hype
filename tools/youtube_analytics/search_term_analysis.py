"""
Search Term Analysis Tool

Analyzes YouTube search terms driving traffic to each video, identifies
title-search mismatches, high-value terms, cross-video overlap, and
untapped description keywords.

Data sources:
  - analytics.db (videos table for metadata)
  - _search_terms.json (cached search term data)
  - YouTube Analytics API (fresh fetch via --fetch)

Usage:
    python -m tools.youtube_analytics.search_term_analysis --report      # Full report
    python -m tools.youtube_analytics.search_term_analysis --fetch       # Fetch fresh data
    python -m tools.youtube_analytics.search_term_analysis --cached      # Report from cache
    python -m tools.youtube_analytics.search_term_analysis --video ID    # Single video
    python -m tools.youtube_analytics.search_term_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/SEARCH-TERM-ANALYSIS.md
"""

import sys
import json
import sqlite3
import argparse
import re
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
SEARCH_TERMS_JSON = Path(__file__).parent / '_search_terms.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'SEARCH-TERM-ANALYSIS.md'


# =========================================================================
# DATA LOADING
# =========================================================================

def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table (long-form only)."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        rows = store.videos(min_duration_seconds=61)  # preserve old `> 60`

    keep = ('video_id', 'title', 'published_at', 'duration_seconds',
            'views', 'watch_time_minutes', 'topic_type', 'subscribers_gained')
    result = {r['video_id']: {k: r[k] for k in keep} for r in rows}

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


def load_search_terms_from_json() -> Dict[str, List[dict]]:
    """Load search term data from the JSON cache file."""
    if not SEARCH_TERMS_JSON.exists():
        logger.warning("No search terms JSON found at %s", SEARCH_TERMS_JSON)
        return {}

    with open(SEARCH_TERMS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info("Loaded search terms for %d videos from JSON cache", len(data))
    return data


def save_search_terms_json(data: Dict[str, List[dict]]) -> None:
    """Save search term data to JSON cache."""
    with open(SEARCH_TERMS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Saved search terms for %d videos to %s", len(data), SEARCH_TERMS_JSON)


# =========================================================================
# API FETCH
# =========================================================================

# Top-N search terms kept per video. Applied by the API for the single-video
# helper below, and by hand after grouping in the batched fetch.
SEARCH_TERMS_PER_VIDEO = 25


def fetch_search_terms_for_video(analytics, video_id: str) -> List[dict]:
    """Fetch search terms driving traffic to a specific video."""
    try:
        response = analytics.reports().query(
            ids='channel==MINE',
            startDate='2024-01-01',
            endDate='2026-12-31',
            metrics='views,estimatedMinutesWatched',
            dimensions='insightTrafficSourceDetail',
            filters=f'video=={video_id};insightTrafficSourceType==YT_SEARCH',
            maxResults=SEARCH_TERMS_PER_VIDEO,
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


def fetch_all_search_terms(video_ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
    """
    Fetch search terms for all videos from YouTube Analytics API.

    Args:
        video_ids: Specific video IDs to fetch. If None, fetches all from DB.

    Returns:
        Dict mapping video_id -> list of search term dicts.
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    if video_ids is None:
        metadata = load_video_metadata()
        video_ids = list(metadata.keys())

    logger.info("Fetching search terms for %d videos from API...", len(video_ids))

    # ⚠ This loop CANNOT be batched — do not "optimise" it into one request.
    # Its siblings (geography_analysis, traffic_analysis) were collapsed from 58
    # round-trips to 1 on 2026-07-30 via analytics_batch.query_grouped_by_video.
    # The same change was attempted here and the API rejects it:
    #     dimensions='video,insightTrafficSourceDetail'
    #     -> HTTP 400 badRequest, "The query is not supported."
    # insightTrafficSourceDetail cannot be broken down by video; it is only
    # available filtered to a single video at a time. So the per-video loop is
    # the supported shape, not an oversight.
    result = {}

    for i, vid_id in enumerate(video_ids):
        terms = fetch_search_terms_for_video(analytics, vid_id)
        if terms:
            result[vid_id] = terms
        if (i + 1) % 10 == 0:
            logger.info("  Fetched %d/%d videos", i + 1, len(video_ids))
        time.sleep(0.1)

    logger.info("Fetched search terms for %d videos (%d had search traffic)",
                len(video_ids), len(result))
    return result


# =========================================================================
# TEXT UTILITIES
# =========================================================================

def tokenize(text: str) -> set:
    """Tokenize text into a set of lowercase alphanumeric words."""
    if not text:
        return set()
    return set(re.findall(r'[a-z0-9]+', text.lower()))


def token_overlap_ratio(text_a: str, text_b: str) -> float:
    """
    Compute token overlap ratio between two strings.

    Returns the fraction of tokens in text_b that appear in text_a.
    A low ratio means the search term is very different from the title.
    """
    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)
    if not tokens_b:
        return 1.0
    overlap = tokens_a & tokens_b
    return len(overlap) / len(tokens_b)


# =========================================================================
# ANALYSIS FUNCTIONS
# =========================================================================

def find_title_search_mismatches(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    overlap_threshold: float = 0.3,
) -> List[dict]:
    """
    Find videos where top search terms differ significantly from the title.

    A mismatch means the audience is searching for something different than
    what the title advertises — an opportunity for retitling or description
    optimization.

    Args:
        search_data: video_id -> list of search term dicts
        metadata: video_id -> video metadata dict
        overlap_threshold: below this ratio = mismatch (0.0 - 1.0)

    Returns:
        List of mismatch dicts sorted by views (descending).
    """
    mismatches = []

    for vid_id, terms in search_data.items():
        if not terms:
            continue
        meta = metadata.get(vid_id)
        if not meta:
            continue

        title = meta.get('title', '')
        top_term = terms[0]  # Highest-views search term

        overlap = token_overlap_ratio(title, top_term['term'])

        if overlap <= overlap_threshold:
            mismatches.append({
                'video_id': vid_id,
                'title': title,
                'top_search_term': top_term['term'],
                'term_views': top_term['views'],
                'overlap_ratio': overlap,
                'total_search_views': sum(t['views'] for t in terms),
            })

    mismatches.sort(key=lambda x: x['term_views'], reverse=True)
    return mismatches


def find_high_value_terms(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    min_views: int = 3,
) -> List[dict]:
    """
    Find search terms with highest watch time per view (= best audience fit).

    High min/view means the searcher found what they wanted and watched longer.

    Args:
        search_data: video_id -> list of search term dicts
        metadata: video_id -> video metadata dict
        min_views: minimum views to include (filters noise)

    Returns:
        List of high-value term dicts sorted by avg_min_per_view descending.
    """
    term_agg: Dict[str, dict] = defaultdict(lambda: {
        'total_views': 0,
        'total_watch_time': 0.0,
        'video_ids': set(),
    })

    for vid_id, terms in search_data.items():
        for t in terms:
            key = t['term'].lower().strip()
            agg = term_agg[key]
            agg['total_views'] += t['views']
            agg['total_watch_time'] += t['watch_time_minutes']
            agg['video_ids'].add(vid_id)

    results = []
    for term, agg in term_agg.items():
        if agg['total_views'] < min_views:
            continue
        avg_min = agg['total_watch_time'] / agg['total_views']
        results.append({
            'term': term,
            'total_views': agg['total_views'],
            'total_watch_time': round(agg['total_watch_time'], 1),
            'avg_min_per_view': round(avg_min, 2),
            'video_count': len(agg['video_ids']),
        })

    results.sort(key=lambda x: x['avg_min_per_view'], reverse=True)
    return results


def find_cross_video_terms(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    min_videos: int = 2,
) -> List[dict]:
    """
    Find search terms that appear across multiple videos.

    These represent audience bridge opportunities — topics where viewers
    cross over between videos.

    Args:
        search_data: video_id -> list of search term dicts
        metadata: video_id -> video metadata dict
        min_videos: minimum number of videos the term must appear in

    Returns:
        List of cross-video term dicts sorted by video_count then total_views.
    """
    term_agg: Dict[str, dict] = defaultdict(lambda: {
        'total_views': 0,
        'total_watch_time': 0.0,
        'videos': [],
    })

    for vid_id, terms in search_data.items():
        meta = metadata.get(vid_id, {})
        title = meta.get('title', vid_id)
        for t in terms:
            key = t['term'].lower().strip()
            agg = term_agg[key]
            agg['total_views'] += t['views']
            agg['total_watch_time'] += t['watch_time_minutes']
            agg['videos'].append({
                'video_id': vid_id,
                'title': title,
                'views': t['views'],
            })

    results = []
    for term, agg in term_agg.items():
        # Deduplicate videos (same video could theoretically appear twice)
        unique_vids = {v['video_id'] for v in agg['videos']}
        if len(unique_vids) < min_videos:
            continue
        results.append({
            'term': term,
            'total_views': agg['total_views'],
            'total_watch_time': round(agg['total_watch_time'], 1),
            'video_count': len(unique_vids),
            'videos': agg['videos'],
        })

    results.sort(key=lambda x: (-x['video_count'], -x['total_views']))
    return results


def find_untapped_terms(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    min_views: int = 3,
) -> List[dict]:
    """
    Find search terms driving traffic that aren't in the video title.

    These are candidates for description optimization — adding these keywords
    to descriptions could boost search visibility.

    Args:
        search_data: video_id -> list of search term dicts
        metadata: video_id -> video metadata dict
        min_views: minimum views for the term to be included

    Returns:
        List of untapped term dicts sorted by views descending.
    """
    results = []

    for vid_id, terms in search_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue
        title = meta.get('title', '')
        title_tokens = tokenize(title)

        for t in terms:
            if t['views'] < min_views:
                continue
            term_tokens = tokenize(t['term'])
            # If fewer than half the term tokens appear in the title, it's untapped
            if not term_tokens:
                continue
            overlap = len(title_tokens & term_tokens) / len(term_tokens)
            if overlap < 0.5:
                results.append({
                    'video_id': vid_id,
                    'title': title,
                    'search_term': t['term'],
                    'views': t['views'],
                    'watch_time_minutes': round(t['watch_time_minutes'], 1),
                    'overlap': round(overlap, 2),
                })

    results.sort(key=lambda x: x['views'], reverse=True)
    return results


def aggregate_terms_by_topic(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> Dict[str, List[dict]]:
    """
    Aggregate search terms by topic type (territorial, ideological, general).

    Shows what terms drive traffic for each content category.

    Returns:
        Dict mapping topic_type -> list of aggregated term dicts.
    """
    topic_terms: Dict[str, Dict[str, dict]] = defaultdict(
        lambda: defaultdict(lambda: {'views': 0, 'watch_time': 0.0, 'videos': 0})
    )

    for vid_id, terms in search_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue
        topic_type = meta.get('topic_type') or 'general'

        for t in terms:
            key = t['term'].lower().strip()
            agg = topic_terms[topic_type][key]
            agg['views'] += t['views']
            agg['watch_time'] += t['watch_time_minutes']
            agg['videos'] += 1

    result = {}
    for topic_type, terms_dict in sorted(topic_terms.items()):
        sorted_terms = sorted(
            [{'term': k, **v} for k, v in terms_dict.items()],
            key=lambda x: x['views'],
            reverse=True,
        )
        result[topic_type] = sorted_terms[:20]  # Top 20 per topic

    return result


def get_top_terms_channel_wide(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    limit: int = 30,
) -> List[dict]:
    """
    Get top search terms across the entire channel.

    Returns:
        List of aggregated term dicts sorted by total views.
    """
    term_agg: Dict[str, dict] = defaultdict(lambda: {
        'total_views': 0,
        'total_watch_time': 0.0,
        'video_ids': set(),
    })

    for vid_id, terms in search_data.items():
        for t in terms:
            key = t['term'].lower().strip()
            agg = term_agg[key]
            agg['total_views'] += t['views']
            agg['total_watch_time'] += t['watch_time_minutes']
            agg['video_ids'].add(vid_id)

    results = []
    for term, agg in term_agg.items():
        views = agg['total_views']
        watch = agg['total_watch_time']
        results.append({
            'term': term,
            'total_views': views,
            'total_watch_time': round(watch, 1),
            'avg_min_per_view': round(watch / views, 2) if views > 0 else 0,
            'video_count': len(agg['video_ids']),
        })

    results.sort(key=lambda x: x['total_views'], reverse=True)
    return results[:limit]


# =========================================================================
# SINGLE VIDEO REPORT
# =========================================================================

def single_video_report(
    video_id: str,
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate a search term report for a single video."""
    terms = search_data.get(video_id)
    meta = metadata.get(video_id)

    if not terms:
        return f"No search term data found for {video_id}"

    lines = []
    title = meta.get('title', video_id) if meta else video_id
    lines.append(f"# Search Terms: {title}")
    lines.append("")

    if meta:
        lines.append(f"- **Topic type:** {meta.get('topic_type', 'unknown')}")
        lines.append(f"- **Total views:** {meta.get('views', 'N/A'):,}")
        lines.append("")

    total_search_views = sum(t['views'] for t in terms)
    lines.append(f"## Search Terms ({total_search_views:,} search views)")
    lines.append("")
    lines.append("| # | Search Term | Views | Watch Time (min) | Avg Min/View |")
    lines.append("|---|-------------|------:|-----------------:|------------:|")

    for i, t in enumerate(terms, 1):
        avg = t['watch_time_minutes'] / t['views'] if t['views'] > 0 else 0
        lines.append(
            f"| {i} | {t['term']} | {t['views']:,} | {t['watch_time_minutes']:.1f} | {avg:.2f} |"
        )

    # Check title overlap
    if meta:
        lines.append("")
        lines.append("## Title Overlap Analysis")
        lines.append("")
        title_tokens = tokenize(title)
        for t in terms[:5]:
            overlap = token_overlap_ratio(title, t['term'])
            status = "MATCH" if overlap > 0.3 else "MISMATCH"
            lines.append(f"- **{status}** ({overlap:.0%} overlap): \"{t['term']}\" ({t['views']} views)")

    return "\n".join(lines)


# =========================================================================
# FULL REPORT
# =========================================================================

def generate_report(
    search_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate the full SEARCH-TERM-ANALYSIS.md report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Count unique terms
    all_terms = set()
    for terms in search_data.values():
        for t in terms:
            all_terms.add(t['term'].lower().strip())

    videos_with_data = len(search_data)

    lines = [
        "# Search Term Analysis",
        "",
        f"**Generated:** {now}",
        f"**Videos analyzed:** {videos_with_data} | **Unique search terms:** {len(all_terms)}",
        "",
    ]

    # ── Section 1: Top Search Terms ──
    lines.append("## 1. Top Search Terms (Channel-Wide)")
    lines.append("")

    top_terms = get_top_terms_channel_wide(search_data, metadata, limit=30)
    if top_terms:
        lines.append("| # | Search Term | Total Views | Avg Min/View | Videos |")
        lines.append("|---|-------------|------------:|------------:|-------:|")
        for i, t in enumerate(top_terms, 1):
            lines.append(
                f"| {i} | {t['term']} | {t['total_views']:,} | "
                f"{t['avg_min_per_view']:.2f} | {t['video_count']} |"
            )
    else:
        lines.append("*No search term data available.*")
    lines.append("")

    # ── Section 2: Title-Search Mismatches ──
    lines.append("## 2. Title-Search Mismatches")
    lines.append("")
    lines.append("Videos where people search something different than the title suggests.")
    lines.append("Low overlap ratio = audience expects different content than the title promises.")
    lines.append("")

    mismatches = find_title_search_mismatches(search_data, metadata)
    if mismatches:
        lines.append("| Video Title | Top Search Term | Term Views | Overlap |")
        lines.append("|-------------|-----------------|----------:|---------:|")
        for m in mismatches[:15]:
            lines.append(
                f"| {m['title'][:50]} | {m['top_search_term']} | "
                f"{m['term_views']:,} | {m['overlap_ratio']:.0%} |"
            )
        lines.append("")
        lines.append("**Action:** Consider retitling or updating descriptions to match search intent.")
    else:
        lines.append("*No significant mismatches found.*")
    lines.append("")

    # ── Section 3: High-Value Terms ──
    lines.append("## 3. High-Value Terms (Best Audience Fit)")
    lines.append("")
    lines.append("Terms with highest watch time per view — searchers found what they wanted.")
    lines.append("")

    high_value = find_high_value_terms(search_data, metadata, min_views=3)
    if high_value:
        lines.append("| # | Search Term | Views | Avg Min/View | Videos |")
        lines.append("|---|-------------|------:|------------:|-------:|")
        for i, t in enumerate(high_value[:20], 1):
            lines.append(
                f"| {i} | {t['term']} | {t['total_views']:,} | "
                f"{t['avg_min_per_view']:.2f} | {t['video_count']} |"
            )
    else:
        lines.append("*Not enough data (need terms with 3+ views).*")
    lines.append("")

    # ── Section 4: Cross-Video Terms ──
    lines.append("## 4. Cross-Video Terms")
    lines.append("")
    lines.append("Terms appearing across 2+ videos — audience bridge opportunities.")
    lines.append("")

    cross_video = find_cross_video_terms(search_data, metadata, min_videos=2)
    if cross_video:
        lines.append("| Search Term | Videos | Total Views | Avg Min/View |")
        lines.append("|-------------|-------:|------------:|------------:|")
        for t in cross_video[:20]:
            avg = t['total_watch_time'] / t['total_views'] if t['total_views'] > 0 else 0
            lines.append(
                f"| {t['term']} | {t['video_count']} | "
                f"{t['total_views']:,} | {avg:.2f} |"
            )
        lines.append("")

        # Show which videos share the top cross-video terms
        lines.append("### Cross-Video Details (Top 5)")
        lines.append("")
        for t in cross_video[:5]:
            lines.append(f"**\"{t['term']}\"** ({t['total_views']:,} views across {t['video_count']} videos)")
            for v in sorted(t['videos'], key=lambda x: x['views'], reverse=True):
                lines.append(f"  - {v['title'][:60]} ({v['views']} views)")
            lines.append("")
    else:
        lines.append("*No terms found across multiple videos.*")
    lines.append("")

    # ── Section 5: Untapped Description Keywords ──
    lines.append("## 5. Untapped Description Keywords")
    lines.append("")
    lines.append("Terms driving traffic but NOT in video titles — add to descriptions for SEO.")
    lines.append("")

    untapped = find_untapped_terms(search_data, metadata, min_views=3)
    if untapped:
        lines.append("| Search Term | Video Title | Views | Watch Time | Title Overlap |")
        lines.append("|-------------|-------------|------:|-----------:|--------------:|")
        for t in untapped[:20]:
            lines.append(
                f"| {t['search_term']} | {t['title'][:45]} | "
                f"{t['views']:,} | {t['watch_time_minutes']:.1f} min | {t['overlap']:.0%} |"
            )
    else:
        lines.append("*No untapped terms found with 3+ views.*")
    lines.append("")

    # ── Section 6: Search Terms by Topic Type ──
    lines.append("## 6. Search Terms by Topic Type")
    lines.append("")
    lines.append("What terms work for territorial vs ideological vs general videos?")
    lines.append("")

    by_topic = aggregate_terms_by_topic(search_data, metadata)
    if by_topic:
        for topic_type, terms in by_topic.items():
            total_views = sum(t['views'] for t in terms)
            lines.append(f"### {topic_type.title()} ({total_views:,} search views)")
            lines.append("")
            lines.append("| # | Search Term | Views | Watch Time (min) |")
            lines.append("|---|-------------|------:|-----------------:|")
            for i, t in enumerate(terms[:10], 1):
                lines.append(
                    f"| {i} | {t['term']} | {t['views']:,} | {t['watch_time']:.1f} |"
                )
            lines.append("")
    else:
        lines.append("*No topic type data available.*")
    lines.append("")

    # ── Interpreted Findings ──
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = _generate_findings(
        top_terms, mismatches, high_value, cross_video, untapped, by_topic
    )
    for f in findings:
        lines.append(f"- {f}")
    lines.append("")

    return "\n".join(lines)


def _generate_findings(
    top_terms: List[dict],
    mismatches: List[dict],
    high_value: List[dict],
    cross_video: List[dict],
    untapped: List[dict],
    by_topic: Dict[str, List[dict]],
) -> List[str]:
    """Generate actionable bullet-point findings from the analysis."""
    findings = []

    # Top terms insight
    if top_terms:
        top = top_terms[0]
        findings.append(
            f"**Top search driver:** \"{top['term']}\" ({top['total_views']:,} views, "
            f"{top['avg_min_per_view']:.1f} min/view across {top['video_count']} video(s))."
        )

    # Mismatches insight
    if mismatches:
        count = len(mismatches)
        top_m = mismatches[0]
        findings.append(
            f"**{count} title-search mismatch(es) detected.** Biggest: \"{top_m['title'][:40]}\" "
            f"— audience searches \"{top_m['top_search_term']}\" instead ({top_m['term_views']:,} views). "
            f"Consider retitling or description update."
        )
    else:
        findings.append("**No significant title-search mismatches** — titles align well with search intent.")

    # High-value terms insight
    if high_value:
        best = high_value[0]
        findings.append(
            f"**Highest-value search term:** \"{best['term']}\" ({best['avg_min_per_view']:.1f} avg min/view). "
            f"Searchers who find this term watch longest — double down on this topic area."
        )

    # Cross-video insight
    if cross_video:
        findings.append(
            f"**{len(cross_video)} term(s) bridge multiple videos.** "
            f"These represent core audience interests. Use for playlist grouping and end-screen links."
        )
    else:
        findings.append(
            "**No cross-video search terms found** — videos are serving distinct audiences. "
            "Consider creating content clusters to build audience overlap."
        )

    # Untapped terms
    if untapped:
        top_u = untapped[0]
        findings.append(
            f"**{len(untapped)} untapped keyword(s)** driving traffic without title presence. "
            f"Top opportunity: \"{top_u['search_term']}\" ({top_u['views']:,} views to "
            f"\"{top_u['title'][:35]}\"). Add to description."
        )

    # Topic type insight
    if by_topic:
        topic_views = {
            t: sum(term['views'] for term in terms)
            for t, terms in by_topic.items()
        }
        if topic_views:
            best_topic = max(topic_views, key=topic_views.get)
            findings.append(
                f"**{best_topic.title()} videos attract the most search traffic** "
                f"({topic_views[best_topic]:,} views). "
                f"Prioritize search-optimized titles for this topic type."
            )

    return findings


# =========================================================================
# CLI
# =========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze YouTube search terms driving traffic to videos.",
        prog="python -m tools.youtube_analytics.search_term_analysis",
    )
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch fresh search term data from YouTube Analytics API')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached data only (skip API fetch)')
    parser.add_argument('--report', action='store_true',
                        help='Generate the full analysis report')
    parser.add_argument('--video', type=str, default=None,
                        help='Analyze a single video by ID')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress non-error output')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    # Default: if no action specified, generate report from cache
    if not args.fetch and not args.report and not args.video:
        args.report = True
        args.cached = True

    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata found in analytics.db. Run backfill first.")
        sys.exit(1)

    # Load or fetch search term data
    if args.fetch:
        video_ids = [args.video] if args.video else None
        search_data = fetch_all_search_terms(video_ids)
        if search_data:
            # Merge with existing cache
            existing = load_search_terms_from_json()
            existing.update(search_data)
            save_search_terms_json(existing)
            search_data = existing
        else:
            logger.warning("No search term data fetched. Using cache if available.")
            search_data = load_search_terms_from_json()
    else:
        search_data = load_search_terms_from_json()

    if not search_data:
        logger.error("No search term data available. Run with --fetch first.")
        sys.exit(1)

    # Single video report
    if args.video:
        report = single_video_report(args.video, search_data, metadata)
        print(report)
        return

    # Full report
    if args.report:
        report = generate_report(search_data, metadata)

        # Ensure output directory exists
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info("Report saved to %s", REPORT_PATH)
        print(f"Report saved to {REPORT_PATH}")
        print(f"  Videos with search data: {len(search_data)}")
        all_terms = set()
        for terms in search_data.values():
            for t in terms:
                all_terms.add(t['term'].lower().strip())
        print(f"  Unique search terms: {len(all_terms)}")


if __name__ == '__main__':
    main()
