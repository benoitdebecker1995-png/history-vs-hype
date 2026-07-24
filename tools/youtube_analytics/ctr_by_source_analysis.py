"""
CTR by Traffic Source Analysis Tool

Correlates overall video CTR with traffic source mix to identify which
traffic sources are associated with higher-CTR videos.

YouTube Analytics does NOT provide per-source CTR (impressions are video-level
only). This tool works around that limitation by:
  1. Parsing CTR from POST-PUBLISH-ANALYSIS files (manually entered from Studio)
  2. Loading traffic source view shares from _traffic_sources.json / analytics.db
  3. Correlating: do high-CTR videos get a different source mix than low-CTR ones?

Key question: should we optimize titles for Search (front-load keywords) or
Browse/Suggested (curiosity gap)?

Usage:
    python -m tools.youtube_analytics.ctr_by_source_analysis              # default: generate report
    python -m tools.youtube_analytics.ctr_by_source_analysis --report     # explicit report
    python -m tools.youtube_analytics.ctr_by_source_analysis --cached     # same as default (no API)
    python -m tools.youtube_analytics.ctr_by_source_analysis --verbose    # debug logging
    python -m tools.youtube_analytics.ctr_by_source_analysis --quiet      # suppress info

Output:
    channel-data/patterns/CTR-BY-SOURCE-ANALYSIS.md
"""

import argparse
import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median, stdev
from typing import Dict, List, Optional, Tuple

from tools.logging_config import get_logger, setup_logging
from tools.post_publish import PostPublishStore

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
TRAFFIC_JSON = Path(__file__).parent / '_traffic_sources.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'CTR-BY-SOURCE-ANALYSIS.md'

# Friendly names for traffic source types (shared with traffic_analysis.py)
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
}

# Sources to report individually; everything else is lumped as "Other"
MAJOR_SOURCES = [
    'YT_SEARCH', 'RELATED_VIDEO', 'SUBSCRIBER', 'EXT_URL',
    'NOTIFICATION', 'YT_CHANNEL',
]

# CTR tier thresholds
HIGH_CTR_THRESHOLD = 4.0   # >= 4% is "high"
LOW_CTR_THRESHOLD = 3.0    # <  3% is "low"


# =========================================================================
# CLASSIFIERS
# =========================================================================

def classify_title_pattern(title: str) -> str:
    """Classify title into the canonical structural taxonomy (ADR-0009).

    Delegates to tools.title_features.pattern. Was a local copy that had drifted
    from title_scorer (treated `|` as colon, lacked the_x_that, used broad
    question-word prefixes); now unified on the canonical logic.
    """
    from tools.title_features import pattern
    return pattern(title)


def classify_topic_type(topic_type: Optional[str]) -> str:
    """Normalize topic_type, falling back to 'unknown'."""
    if not topic_type:
        return "unknown"
    return topic_type.strip().lower()


# =========================================================================
# DATA LOADING: CTR from POST-PUBLISH-ANALYSIS files
# =========================================================================

def _extract_ctr_from_content(text: str) -> Optional[float]:
    """
    Extract the best CTR value from a POST-PUBLISH-ANALYSIS file.

    Looks for patterns like:
      - CTR History table rows: | 2026-02-23 | 3.8% | ...
      - **CTR:** 3.5%
      - CTR: 3.5%
      - CTR|3.5%

    Takes the LAST non-zero CTR value found (most recent snapshot).
    """
    ctr_values: list[float] = []

    # Pattern 1: CTR History table rows — | date | X.XX% | impressions | views |
    for m in re.finditer(
        r'\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*(\d+\.?\d*)\s*%', text
    ):
        val = float(m.group(1))
        if val > 0:
            ctr_values.append(val)

    # Pattern 2: **CTR:** X.XX% or CTR: X.XX%
    for m in re.finditer(r'CTR[:\*]*\s*(\d+\.?\d*)\s*%', text):
        val = float(m.group(1))
        if val > 0:
            ctr_values.append(val)

    # Pattern 3: CTR Trend line — (X.XX% -> Y.YY%, ...)
    for m in re.finditer(r'CTR Trend.*?(\d+\.?\d*)\s*%\s*->\s*(\d+\.?\d*)\s*%', text):
        val = float(m.group(2))  # take the "after" value
        if val > 0:
            ctr_values.append(val)

    if not ctr_values:
        return None

    # Return the last (most recent) non-zero value
    return ctr_values[-1]


def load_ctr_from_analyses() -> Dict[str, float]:
    """
    Scan all post-publish reports and extract video_id -> CTR mapping.

    Returns only videos with valid (non-zero) CTR data. CTR extraction
    stays local because this module catches CTR Trend patterns the store
    doesn't expose (e.g. "CTR Trend: 2.1% -> 3.4%" picks up the post-trend
    value). Discovery + video_id resolution route through PostPublishStore.
    """
    ctr_map: Dict[str, float] = {}
    files_scanned = 0
    files_with_ctr = 0

    for report in PostPublishStore(project_root=PROJECT_ROOT).discover_and_load_all():
        files_scanned += 1

        try:
            text = report.source_path.read_text(encoding='utf-8', errors='replace')
        except OSError as e:
            logger.warning("Cannot read %s: %s", report.source_path, e)
            continue

        ctr = _extract_ctr_from_content(text)
        if ctr is not None:
            ctr_map[report.video_id] = ctr
            files_with_ctr += 1
            logger.debug(
                "CTR %.2f%% for %s from %s",
                ctr, report.video_id, report.source_path.name,
            )

    logger.info(
        "Scanned %d POST-PUBLISH files, found CTR data for %d videos",
        files_scanned, files_with_ctr,
    )
    return ctr_map


# =========================================================================
# DATA LOADING: Traffic sources
# =========================================================================

def load_traffic_from_json() -> Dict[str, List[dict]]:
    """Load traffic source data from the JSON cache file."""
    if not TRAFFIC_JSON.exists():
        logger.warning("No traffic sources JSON at %s", TRAFFIC_JSON)
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
    try:
        with AnalyticsStore.open(ANALYTICS_DB) as store:
            rows = store.traffic_sources()
    except sqlite3.OperationalError as e:
        logger.warning("Cannot read traffic_sources table: %s", e)
        return {}

    result: Dict[str, List[dict]] = defaultdict(list)
    for row in rows:
        result[row['video_id']].append({
            'source_type': row['source_type'],
            'views': row['views'],
            'watch_time_minutes': row['watch_time_minutes'],
        })

    logger.info("Loaded traffic data for %d videos from analytics.db", len(result))
    return dict(result)


def merge_traffic_data(
    json_data: Dict[str, List[dict]],
    db_data: Dict[str, List[dict]],
) -> Dict[str, List[dict]]:
    """Merge traffic data from JSON and DB, preferring JSON (more recent)."""
    merged = dict(db_data)
    merged.update(json_data)
    return merged


def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found")
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    try:
        with AnalyticsStore.open(ANALYTICS_DB) as store:
            rows = store.videos(min_duration_seconds=61)  # preserve old `> 60`
    except sqlite3.OperationalError as e:
        logger.warning("Cannot read videos table: %s", e)
        return {}

    result = {}
    for row in rows:
        vid = dict(row)
        vid['title_pattern'] = classify_title_pattern(vid['title'] or '')
        vid['topic_type'] = classify_topic_type(vid.get('topic_type'))
        result[vid['video_id']] = vid

    logger.info("Loaded metadata for %d long-form videos from analytics.db", len(result))
    return result


# =========================================================================
# ANALYSIS ENGINE
# =========================================================================

def compute_source_view_share(sources: List[dict]) -> Dict[str, float]:
    """
    For a single video, compute the percentage of views from each source.

    Returns: {source_type: percentage} where percentages sum to ~100.
    """
    total = sum(s['views'] for s in sources)
    if total == 0:
        return {}

    shares: Dict[str, float] = {}
    for s in sources:
        shares[s['source_type']] = (s['views'] / total) * 100.0
    return shares


def _bucket_source(source_type: str) -> str:
    """Map a source type to a major bucket or 'Other'."""
    if source_type in MAJOR_SOURCES:
        return source_type
    return 'OTHER'


def compute_bucketed_shares(sources: List[dict]) -> Dict[str, float]:
    """Compute view share with minor sources lumped into 'Other'."""
    total = sum(s['views'] for s in sources)
    if total == 0:
        return {}

    buckets: Dict[str, int] = defaultdict(int)
    for s in sources:
        buckets[_bucket_source(s['source_type'])] += s['views']

    return {k: (v / total) * 100.0 for k, v in buckets.items()}


def correlate_source_share_with_ctr(
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> dict:
    """
    Split videos into CTR tiers and compare traffic source mix.

    Returns dict with keys:
      - 'high': {'count', 'avg_ctr', 'source_shares'}
      - 'mid':  same
      - 'low':  same
      - 'all':  same
      - 'correlation_pairs': list of (ctr, source_type, share_pct) for scatter
    """
    tiers: Dict[str, dict] = {
        tier: {'ctrs': [], 'share_lists': defaultdict(list)}
        for tier in ('high', 'mid', 'low', 'all')
    }
    correlation_pairs: list[Tuple[float, str, float]] = []

    for vid_id, ctr in ctr_map.items():
        if vid_id not in traffic_data:
            continue

        shares = compute_bucketed_shares(traffic_data[vid_id])
        if not shares:
            continue

        # Determine tier
        if ctr >= HIGH_CTR_THRESHOLD:
            tier = 'high'
        elif ctr < LOW_CTR_THRESHOLD:
            tier = 'low'
        else:
            tier = 'mid'

        for t in (tier, 'all'):
            tiers[t]['ctrs'].append(ctr)
            for source, pct in shares.items():
                tiers[t]['share_lists'][source].append(pct)

        for source, pct in shares.items():
            correlation_pairs.append((ctr, source, pct))

    result = {}
    for tier, data in tiers.items():
        if not data['ctrs']:
            result[tier] = {'count': 0, 'avg_ctr': 0, 'median_ctr': 0, 'source_shares': {}}
            continue

        source_shares = {}
        for source, pct_list in data['share_lists'].items():
            source_shares[source] = {
                'mean': mean(pct_list),
                'n': len(pct_list),
            }

        result[tier] = {
            'count': len(data['ctrs']),
            'avg_ctr': mean(data['ctrs']),
            'median_ctr': median(data['ctrs']),
            'source_shares': source_shares,
        }

    result['correlation_pairs'] = correlation_pairs
    return result


def analyze_by_title_pattern(
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> Dict[str, dict]:
    """
    Group videos by title pattern, compute avg source mix and CTR per group.

    Returns: {pattern: {count, avg_ctr, source_shares: {source: mean_pct}}}
    """
    groups: Dict[str, dict] = defaultdict(lambda: {
        'ctrs': [],
        'share_lists': defaultdict(list),
    })

    for vid_id, sources in traffic_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        pattern = meta['title_pattern']
        shares = compute_bucketed_shares(sources)
        if not shares:
            continue

        ctr = ctr_map.get(vid_id)
        if ctr is not None:
            groups[pattern]['ctrs'].append(ctr)

        for source, pct in shares.items():
            groups[pattern]['share_lists'][source].append(pct)

    result = {}
    for pattern, data in groups.items():
        source_shares = {
            source: mean(pct_list)
            for source, pct_list in data['share_lists'].items()
        }
        result[pattern] = {
            'count': len(data['share_lists'].get('SUBSCRIBER', [])),
            'count_with_ctr': len(data['ctrs']),
            'avg_ctr': mean(data['ctrs']) if data['ctrs'] else None,
            'source_shares': source_shares,
        }

    return result


def analyze_by_topic_type(
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> Dict[str, dict]:
    """
    Group videos by topic type, compute avg source mix and CTR per group.

    Returns: {topic: {count, avg_ctr, source_shares}}
    """
    groups: Dict[str, dict] = defaultdict(lambda: {
        'ctrs': [],
        'share_lists': defaultdict(list),
    })

    for vid_id, sources in traffic_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        topic = meta['topic_type']
        shares = compute_bucketed_shares(sources)
        if not shares:
            continue

        ctr = ctr_map.get(vid_id)
        if ctr is not None:
            groups[topic]['ctrs'].append(ctr)

        for source, pct in shares.items():
            groups[topic]['share_lists'][source].append(pct)

    result = {}
    for topic, data in groups.items():
        source_shares = {
            source: mean(pct_list)
            for source, pct_list in data['share_lists'].items()
        }
        result[topic] = {
            'count': len(data['share_lists'].get('SUBSCRIBER', [])),
            'count_with_ctr': len(data['ctrs']),
            'avg_ctr': mean(data['ctrs']) if data['ctrs'] else None,
            'source_shares': source_shares,
        }

    return result


def compute_search_ctr_correlation(
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
) -> Optional[Tuple[float, int]]:
    """
    Compute Pearson-like correlation between search view share and CTR.

    Returns (r, n) or None if insufficient data.
    """
    pairs: list[Tuple[float, float]] = []

    for vid_id, ctr in ctr_map.items():
        if vid_id not in traffic_data:
            continue
        shares = compute_bucketed_shares(traffic_data[vid_id])
        search_pct = shares.get('YT_SEARCH', 0.0)
        pairs.append((search_pct, ctr))

    if len(pairs) < 5:
        return None

    n = len(pairs)
    x_vals = [p[0] for p in pairs]
    y_vals = [p[1] for p in pairs]
    x_mean = mean(x_vals)
    y_mean = mean(y_vals)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    denom_x = sum((x - x_mean) ** 2 for x in x_vals) ** 0.5
    denom_y = sum((y - y_mean) ** 2 for y in y_vals) ** 0.5

    if denom_x == 0 or denom_y == 0:
        return (0.0, n)

    r = numerator / (denom_x * denom_y)
    return (r, n)


# =========================================================================
# REPORT GENERATION
# =========================================================================

def _source_label(source_type: str) -> str:
    """Human-readable label for a traffic source type."""
    return SOURCE_LABELS.get(source_type, source_type.replace('_', ' ').title())


def _fmt_pct(val: Optional[float]) -> str:
    """Format a percentage value, handling None."""
    if val is None:
        return "n/a"
    return f"{val:.1f}%"


def _fmt_ctr(val: Optional[float]) -> str:
    """Format a CTR value."""
    if val is None:
        return "n/a"
    return f"{val:.2f}%"


def _sorted_sources() -> list[str]:
    """Return major sources in a consistent display order."""
    return MAJOR_SOURCES + ['OTHER']


def generate_report(
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate the full markdown report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    n_ctr = len(ctr_map)
    n_traffic = len(traffic_data)

    # Count videos with BOTH CTR and traffic data
    both = set(ctr_map.keys()) & set(traffic_data.keys())
    n_both = len(both)

    lines: list[str] = []
    lines.append("# CTR by Traffic Source Analysis")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos with CTR data:** {n_ctr}")
    lines.append(f"**Videos with traffic data:** {n_traffic}")
    lines.append(f"**Videos with both:** {n_both}")
    lines.append("")
    lines.append("## Methodology Note")
    lines.append("")
    lines.append(
        "YouTube Analytics does not provide per-source CTR. Impressions are "
        "only available at the video level, not broken down by traffic source. "
        "This analysis correlates **overall video CTR** (from YouTube Studio, "
        "parsed from POST-PUBLISH-ANALYSIS files) with **traffic source view "
        "shares** (from YouTube Analytics API) to identify patterns."
    )
    lines.append("")
    lines.append(
        "The key question: do videos with higher CTR get their views from "
        "different sources than low-CTR videos?"
    )
    lines.append("")

    # ---- Section 1: CTR vs Source Correlation ----
    tier_data = correlate_source_share_with_ctr(ctr_map, traffic_data, metadata)

    lines.append("## 1. CTR vs Traffic Source Correlation")
    lines.append("")

    if n_both < 3:
        lines.append(
            f"*Insufficient data ({n_both} videos have both CTR and traffic data). "
            "Need at least 3 to analyze.*"
        )
        lines.append("")
    else:
        high = tier_data['high']
        mid = tier_data['mid']
        low = tier_data['low']

        lines.append(
            f"**High CTR** (>={HIGH_CTR_THRESHOLD}%): {high['count']} videos, "
            f"avg {_fmt_ctr(high['avg_ctr'] if high['count'] else None)}"
        )
        lines.append(
            f"**Mid CTR** ({LOW_CTR_THRESHOLD}-{HIGH_CTR_THRESHOLD}%): "
            f"{mid['count']} videos, "
            f"avg {_fmt_ctr(mid['avg_ctr'] if mid['count'] else None)}"
        )
        lines.append(
            f"**Low CTR** (<{LOW_CTR_THRESHOLD}%): {low['count']} videos, "
            f"avg {_fmt_ctr(low['avg_ctr'] if low['count'] else None)}"
        )
        lines.append("")

        # Table: source share by CTR tier
        sources_display = _sorted_sources()
        header = "| Source | High CTR (>={t}%) | Mid CTR | Low CTR (<{l}%) | Delta (H-L) |".format(
            t=HIGH_CTR_THRESHOLD, l=LOW_CTR_THRESHOLD
        )
        lines.append(header)
        lines.append("|--------|" + "|".join(["--------"] * 4) + "|")

        for source in sources_display:
            label = _source_label(source)
            h_pct = high['source_shares'].get(source, {}).get('mean')
            m_pct = mid['source_shares'].get(source, {}).get('mean')
            l_pct = low['source_shares'].get(source, {}).get('mean')

            if h_pct is not None and l_pct is not None:
                delta = h_pct - l_pct
                delta_str = f"{delta:+.1f}pp"
            else:
                delta_str = "n/a"

            lines.append(
                f"| {label} | {_fmt_pct(h_pct)} | {_fmt_pct(m_pct)} | "
                f"{_fmt_pct(l_pct)} | {delta_str} |"
            )

        lines.append("")

        # Search-CTR correlation coefficient
        corr = compute_search_ctr_correlation(ctr_map, traffic_data)
        if corr is not None:
            r, n = corr
            strength = "negligible"
            if abs(r) > 0.5:
                strength = "strong"
            elif abs(r) > 0.3:
                strength = "moderate"
            elif abs(r) > 0.1:
                strength = "weak"

            lines.append(
                f"**Search % vs CTR correlation:** r={r:.3f} ({strength}, n={n})"
            )
            lines.append("")

    # ---- Section 2: Source Mix by Title Pattern ----
    lines.append("## 2. Source Mix by Title Pattern")
    lines.append("")

    pattern_data = analyze_by_title_pattern(ctr_map, traffic_data, metadata)

    if not pattern_data:
        lines.append("*No data available.*")
        lines.append("")
    else:
        header = "| Title Pattern | n | Avg CTR | Search % | Suggested % | Subscriber % | External % |"
        lines.append(header)
        lines.append("|" + "|".join(["--------"] * 7) + "|")

        # Sort by count descending
        for pattern, data in sorted(
            pattern_data.items(), key=lambda x: x[1]['count'], reverse=True
        ):
            ctr_str = _fmt_ctr(data['avg_ctr'])
            n_str = f"{data['count']} ({data['count_with_ctr']} w/CTR)"
            shares = data['source_shares']

            lines.append(
                f"| {pattern} | {n_str} | {ctr_str} | "
                f"{_fmt_pct(shares.get('YT_SEARCH'))} | "
                f"{_fmt_pct(shares.get('RELATED_VIDEO'))} | "
                f"{_fmt_pct(shares.get('SUBSCRIBER'))} | "
                f"{_fmt_pct(shares.get('EXT_URL'))} |"
            )

        lines.append("")

    # ---- Section 3: Source Mix by Topic Type ----
    lines.append("## 3. Source Mix by Topic Type")
    lines.append("")

    topic_data = analyze_by_topic_type(ctr_map, traffic_data, metadata)

    if not topic_data:
        lines.append("*No data available.*")
        lines.append("")
    else:
        header = "| Topic Type | n | Avg CTR | Search % | Suggested % | Subscriber % | External % |"
        lines.append(header)
        lines.append("|" + "|".join(["--------"] * 7) + "|")

        for topic, data in sorted(
            topic_data.items(), key=lambda x: x[1]['count'], reverse=True
        ):
            ctr_str = _fmt_ctr(data['avg_ctr'])
            n_str = f"{data['count']} ({data['count_with_ctr']} w/CTR)"
            shares = data['source_shares']

            lines.append(
                f"| {topic} | {n_str} | {ctr_str} | "
                f"{_fmt_pct(shares.get('YT_SEARCH'))} | "
                f"{_fmt_pct(shares.get('RELATED_VIDEO'))} | "
                f"{_fmt_pct(shares.get('SUBSCRIBER'))} | "
                f"{_fmt_pct(shares.get('EXT_URL'))} |"
            )

        lines.append("")

    # ---- Section 4: Source Mix by CTR Tier (detailed) ----
    lines.append("## 4. Source Mix by CTR Tier")
    lines.append("")
    lines.append(
        "Which traffic sources feed high-CTR videos vs low-CTR videos?"
    )
    lines.append("")

    if n_both < 3:
        lines.append("*Insufficient data for tier analysis.*")
        lines.append("")
    else:
        # Detailed per-video listing for transparency
        lines.append("### Per-Video CTR + Source Breakdown")
        lines.append("")
        lines.append(
            "| Video | CTR | Search % | Suggested % | Subscriber % | Title Pattern |"
        )
        lines.append("|" + "|".join(["--------"] * 6) + "|")

        # Sort by CTR descending
        video_rows: list[Tuple[float, str, dict, dict]] = []
        for vid_id in both:
            ctr = ctr_map[vid_id]
            shares = compute_bucketed_shares(traffic_data[vid_id])
            meta = metadata.get(vid_id, {})
            video_rows.append((ctr, vid_id, shares, meta))

        video_rows.sort(key=lambda x: x[0], reverse=True)

        for ctr, vid_id, shares, meta in video_rows:
            title = (meta.get('title') or vid_id)[:45]
            pattern = meta.get('title_pattern', '?')
            lines.append(
                f"| {title} | {ctr:.2f}% | "
                f"{_fmt_pct(shares.get('YT_SEARCH'))} | "
                f"{_fmt_pct(shares.get('RELATED_VIDEO'))} | "
                f"{_fmt_pct(shares.get('SUBSCRIBER'))} | "
                f"{pattern} |"
            )

        lines.append("")

    # ---- Section 5: Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = _generate_findings(tier_data, pattern_data, topic_data, ctr_map, traffic_data, n_both)
    for finding in findings:
        lines.append(f"- {finding}")

    lines.append("")
    lines.append("## Data Quality Notes")
    lines.append("")
    lines.append(
        f"- CTR data from POST-PUBLISH-ANALYSIS files ({n_ctr} videos). "
        "These are single-snapshot values manually entered from YouTube Studio."
    )
    lines.append(
        f"- Traffic source data from YouTube Analytics API ({n_traffic} videos)."
    )
    lines.append(
        f"- Only {n_both} videos have both CTR and traffic data for correlation."
    )
    lines.append(
        "- CTR tiers are arbitrary thresholds, not statistically derived clusters."
    )
    lines.append(
        "- Small sample sizes mean correlations should be treated as directional "
        "hypotheses, not proven rules."
    )
    lines.append("")

    return "\n".join(lines)


def _generate_findings(
    tier_data: dict,
    pattern_data: Dict[str, dict],
    topic_data: Dict[str, dict],
    ctr_map: Dict[str, float],
    traffic_data: Dict[str, List[dict]],
    n_both: int,
) -> list[str]:
    """Generate interpreted findings from analysis results."""
    findings: list[str] = []

    if n_both < 3:
        findings.append(
            f"Insufficient data for analysis ({n_both} videos with both CTR "
            "and traffic data). Re-run after adding CTR to more POST-PUBLISH-ANALYSIS files."
        )
        return findings

    # Finding 1: Search share delta between high/low CTR
    high = tier_data.get('high', {})
    low = tier_data.get('low', {})
    h_search = high.get('source_shares', {}).get('YT_SEARCH', {}).get('mean')
    l_search = low.get('source_shares', {}).get('YT_SEARCH', {}).get('mean')

    if h_search is not None and l_search is not None:
        delta = h_search - l_search
        if abs(delta) > 5:
            direction = "more" if delta > 0 else "less"
            findings.append(
                f"High-CTR videos get {abs(delta):.1f}pp {direction} of their "
                f"views from Search ({h_search:.1f}% vs {l_search:.1f}%). "
                f"{'Front-load keywords in titles.' if delta > 0 else 'Curiosity-gap titles may drive CTR through Browse/Suggested.'}"
            )
        else:
            findings.append(
                f"Search share is similar across CTR tiers ({h_search:.1f}% vs "
                f"{l_search:.1f}%). CTR differences are not driven by traffic source."
            )

    # Finding 2: Suggested/Related delta
    h_sugg = high.get('source_shares', {}).get('RELATED_VIDEO', {}).get('mean')
    l_sugg = low.get('source_shares', {}).get('RELATED_VIDEO', {}).get('mean')
    if h_sugg is not None and l_sugg is not None:
        delta = h_sugg - l_sugg
        if abs(delta) > 5:
            direction = "more" if delta > 0 else "less"
            findings.append(
                f"High-CTR videos get {abs(delta):.1f}pp {direction} Suggested/Related "
                f"traffic ({h_sugg:.1f}% vs {l_sugg:.1f}%). "
                f"{'Good CTR earns algorithm distribution.' if delta > 0 else 'Algorithm favoring low-CTR videos suggests subscriber base is driving views.'}"
            )

    # Finding 3: Subscriber dependency
    h_sub = high.get('source_shares', {}).get('SUBSCRIBER', {}).get('mean')
    l_sub = low.get('source_shares', {}).get('SUBSCRIBER', {}).get('mean')
    if h_sub is not None and l_sub is not None:
        delta = h_sub - l_sub
        if abs(delta) > 5:
            direction = "more" if delta > 0 else "less"
            findings.append(
                f"High-CTR videos are {abs(delta):.1f}pp {direction} subscriber-dependent "
                f"({h_sub:.1f}% vs {l_sub:.1f}%). "
                f"{'High CTR may reflect subscriber loyalty, not packaging quality.' if delta > 0 else 'Lower subscriber share in high-CTR = these titles work on cold traffic.'}"
            )

    # Finding 4: Title pattern with best search share
    if pattern_data:
        best_search_pattern = None
        best_search_pct = 0.0
        for pattern, data in pattern_data.items():
            search_pct = data['source_shares'].get('YT_SEARCH', 0.0)
            if search_pct > best_search_pct and data['count'] >= 2:
                best_search_pct = search_pct
                best_search_pattern = pattern

        if best_search_pattern:
            findings.append(
                f"'{best_search_pattern}' titles have the highest Search traffic share "
                f"({best_search_pct:.1f}%). Optimize evergreen topics with this pattern."
            )

    # Finding 5: Correlation interpretation
    corr = compute_search_ctr_correlation(ctr_map, traffic_data)
    if corr is not None:
        r, n = corr
        if abs(r) < 0.1:
            findings.append(
                f"Search share has near-zero correlation with CTR (r={r:.3f}, n={n}). "
                "CTR is primarily driven by title/thumbnail quality, not traffic source."
            )
        elif r > 0.1:
            findings.append(
                f"Positive correlation between Search share and CTR (r={r:.3f}, n={n}). "
                "Videos that get found via Search tend to have better CTR — likely because "
                "search-optimized titles match user intent."
            )
        else:
            findings.append(
                f"Negative correlation between Search share and CTR (r={r:.3f}, n={n}). "
                "Higher CTR comes from Browse/Suggested, not Search — curiosity-gap "
                "titles may outperform keyword-stuffed ones for discoverability."
            )

    if not findings:
        findings.append("No actionable patterns detected at current sample size.")

    return findings


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Correlate CTR with traffic source mix to find packaging patterns.'
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full report to channel-data/patterns/')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached data only (no API calls). Default behavior.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress info logging')
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not args.report:
        args.report = True

    # Load all data sources
    logger.info("Loading CTR data from POST-PUBLISH-ANALYSIS files...")
    ctr_map = load_ctr_from_analyses()
    if not ctr_map:
        logger.warning("No CTR data found. Ensure POST-PUBLISH-ANALYSIS files "
                       "contain CTR values from YouTube Studio.")

    logger.info("Loading traffic source data...")
    traffic_data = merge_traffic_data(
        load_traffic_from_json(),
        load_traffic_from_db(),
    )
    if not traffic_data:
        logger.error("No traffic source data available. Run "
                     "traffic_analysis.py --fetch first.")
        return

    logger.info("Loading video metadata...")
    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata in analytics.db. Run backfill first.")
        return

    # Log overlap
    both = set(ctr_map.keys()) & set(traffic_data.keys())
    logger.info(
        "CTR: %d videos. Traffic: %d videos. Overlap: %d videos.",
        len(ctr_map), len(traffic_data), len(both),
    )

    # Generate report
    if args.report:
        report = generate_report(ctr_map, traffic_data, metadata)

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        print(report)


if __name__ == '__main__':
    main()
