"""
Retention Curve Shape Classification Tool

Classifies each video's retention curve into shape categories (cliff, slow_burn,
bump, plateau, other) and correlates shapes with views, traffic sources, and
topic types.

Data sources:
  - _retention_cache/{video_id}.json (pre-fetched retention data)
  - analytics.db (videos table for metadata)
  - _traffic_sources.json (pre-fetched traffic source data)

Usage:
    python -m tools.youtube_analytics.curve_shape_analysis              # summary
    python -m tools.youtube_analytics.curve_shape_analysis --video ID   # single video
    python -m tools.youtube_analytics.curve_shape_analysis --report     # generate markdown report
    python -m tools.youtube_analytics.curve_shape_analysis --cached     # (no-op, all data is cached)
    python -m tools.youtube_analytics.curve_shape_analysis --verbose    # debug logging
    python -m tools.youtube_analytics.curve_shape_analysis --quiet      # errors only

Output:
    channel-data/patterns/RETENTION-CURVE-SHAPES.md
"""

import argparse
import json
import math
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).resolve().parent / "analytics.db"
CACHE_DIR = Path(__file__).resolve().parent / "_retention_cache"
TRAFFIC_JSON = Path(__file__).resolve().parent / "_traffic_sources.json"
REPORT_PATH = PROJECT_ROOT / "channel-data" / "patterns" / "RETENTION-CURVE-SHAPES.md"

# Try numpy for linear regression; fall back to manual
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    logger.debug("numpy not available, using manual linear regression fallback")


# =========================================================================
# MATH HELPERS
# =========================================================================

def _linear_r_squared(x: List[float], y: List[float]) -> float:
    """
    Compute R² of a linear fit to (x, y) data.

    Uses numpy if available, otherwise manual computation.
    """
    n = len(x)
    if n < 3:
        return 0.0

    if HAS_NUMPY:
        xa = np.array(x)
        ya = np.array(y)
        coeffs = np.polyfit(xa, ya, 1)
        y_pred = np.polyval(coeffs, xa)
        ss_res = float(np.sum((ya - y_pred) ** 2))
        ss_tot = float(np.sum((ya - np.mean(ya)) ** 2))
        if ss_tot == 0:
            return 1.0
        return 1.0 - ss_res / ss_tot

    # Manual fallback
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi * xi for xi in x)
    mean_y = sum_y / n

    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        return 1.0

    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n

    ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
    ss_tot = sum((yi - mean_y) ** 2 for yi in y)

    if ss_tot == 0:
        return 1.0
    return 1.0 - ss_res / ss_tot


def _stdev(values: List[float]) -> float:
    """Standard deviation (population) for a list of floats."""
    if len(values) < 2:
        return 0.0

    if HAS_NUMPY:
        return float(np.std(values))

    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


# =========================================================================
# DATA LOADING
# =========================================================================

def load_retention_cache(video_id: Optional[str] = None) -> Dict[str, List[dict]]:
    """
    Load retention data from the _retention_cache directory.

    Args:
        video_id: If provided, load only that video. Otherwise load all.

    Returns:
        Dict mapping video_id -> list of data_point dicts.
    """
    if not CACHE_DIR.exists():
        logger.warning("Retention cache directory not found: %s", CACHE_DIR)
        return {}

    result = {}

    if video_id:
        cache_file = CACHE_DIR / f"{video_id}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                result[video_id] = data.get("data_points", [])
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning("Failed to parse %s: %s", cache_file.name, e)
        else:
            logger.warning("No cache file for video %s", video_id)
        return result

    for cache_file in sorted(CACHE_DIR.glob("*.json")):
        vid = cache_file.stem
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            points = data.get("data_points", [])
            if points:
                result[vid] = points
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse %s: %s", cache_file.name, e)

    logger.info("Loaded retention curves for %d videos from cache", len(result))
    return result


def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db videos table."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    conn = sqlite3.connect(str(ANALYTICS_DB))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT video_id, title, duration_seconds, views,
               topic_type, subscribers_gained, avg_view_percentage
        FROM videos
        WHERE duration_seconds > 60
    """)
    rows = cur.fetchall()
    conn.close()

    result = {}
    for row in rows:
        result[row["video_id"]] = dict(row)

    logger.info("Loaded metadata for %d videos from analytics.db", len(result))
    return result


def load_traffic_data() -> Dict[str, List[dict]]:
    """Load traffic source data from _traffic_sources.json."""
    if not TRAFFIC_JSON.exists():
        logger.warning("No traffic sources JSON found at %s", TRAFFIC_JSON)
        return {}

    with open(TRAFFIC_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info("Loaded traffic data for %d videos from JSON cache", len(data))
    return data


# =========================================================================
# CURVE CLASSIFICATION
# =========================================================================

def classify_curve(data_points: List[dict]) -> str:
    """
    Classify a retention curve shape from 100 data points.

    Categories:
      - "cliff"      Sharp early drop, then relatively flat
      - "slow_burn"  Gradual linear decline throughout
      - "bump"       Mid-video recovery (retention increases)
      - "plateau"    Drops early, then holds steady
      - "other"      Doesn't clearly fit any category

    Args:
        data_points: List of dicts with 'position' and 'retention' keys.

    Returns:
        Shape classification string.
    """
    if not data_points or len(data_points) < 10:
        return "other"

    # Sort by position and extract retention values
    sorted_pts = sorted(data_points, key=lambda p: p["position"])
    positions = [p["position"] for p in sorted_pts]
    retentions = [p["retention"] for p in sorted_pts]

    # Find key reference points
    # Position 0.01 (first point) and position 0.10
    ret_start = retentions[0]
    if ret_start == 0:
        return "other"

    # Find retention at ~position 0.10 (index 9 in 100-point curve)
    idx_10 = _find_nearest_index(positions, 0.10)
    ret_10 = retentions[idx_10]

    # Find retention at ~position 0.15
    idx_15 = _find_nearest_index(positions, 0.15)

    # Find retention at ~position 0.20
    idx_20 = _find_nearest_index(positions, 0.20)

    # ----- Check for BUMP first (most specific) -----
    # At any point after position 0.15, retention increases by >= 3%
    # over the previous 10 positions
    bump_found = False
    bump_position = None
    for i in range(idx_15, len(retentions)):
        if i >= 10:
            lookback = retentions[i - 10]
            if retentions[i] - lookback >= 0.03:
                bump_found = True
                bump_position = positions[i]
                break

    if bump_found:
        return "bump"

    # ----- Check for CLIFF -----
    # Retention at position 0.10 < 50% of position 0.01
    # AND remaining curve (0.10 to 1.0) drops less than 30% additional
    if ret_10 < 0.50 * ret_start:
        remaining_retentions = retentions[idx_10:]
        if remaining_retentions:
            remaining_drop = ret_10 - retentions[-1]
            if remaining_drop < 0.30:
                return "cliff"

    # ----- Check for PLATEAU -----
    # After position 0.20, stdev of retention < 0.03
    post_20_retentions = retentions[idx_20:]
    if post_20_retentions and len(post_20_retentions) >= 5:
        post_20_std = _stdev(post_20_retentions)
        if post_20_std < 0.03:
            return "plateau"

    # ----- Check for SLOW_BURN -----
    # No single 10-point segment drops > 15%, and R² of linear fit > 0.85
    max_segment_drop = 0.0
    for i in range(0, len(retentions) - 10):
        segment_drop = retentions[i] - retentions[i + 10]
        if segment_drop > max_segment_drop:
            max_segment_drop = segment_drop

    if max_segment_drop <= 0.15:
        r2 = _linear_r_squared(positions, retentions)
        if r2 > 0.85:
            return "slow_burn"

    return "other"


def _find_nearest_index(positions: List[float], target: float) -> int:
    """Find the index of the position value nearest to target."""
    best_idx = 0
    best_diff = abs(positions[0] - target)
    for i, pos in enumerate(positions):
        diff = abs(pos - target)
        if diff < best_diff:
            best_diff = diff
            best_idx = i
    return best_idx


def classify_all_curves(
    retention_data: Dict[str, List[dict]],
) -> Dict[str, str]:
    """
    Classify all videos' retention curves.

    Returns:
        Dict mapping video_id -> shape classification.
    """
    shapes = {}
    for vid, points in retention_data.items():
        shapes[vid] = classify_curve(points)
    logger.info(
        "Classified %d curves: %s",
        len(shapes),
        dict(sorted(
            defaultdict(int, {s: list(shapes.values()).count(s) for s in set(shapes.values())}).items()
        )),
    )
    return shapes


# =========================================================================
# ANALYSIS FUNCTIONS
# =========================================================================

def analyze_shapes_vs_views(
    shapes: Dict[str, str],
    metadata: Dict[str, dict],
    retention_data: Dict[str, List[dict]],
) -> List[dict]:
    """
    Average views and retention by curve shape.

    Returns:
        List of dicts with shape, count, pct, avg_views, avg_retention.
    """
    shape_stats: Dict[str, dict] = defaultdict(lambda: {
        "views": [], "retentions": [],
    })

    for vid, shape in shapes.items():
        meta = metadata.get(vid, {})
        views = meta.get("views", 0) or 0
        avg_pct = meta.get("avg_view_percentage", 0) or 0

        shape_stats[shape]["views"].append(views)
        shape_stats[shape]["retentions"].append(avg_pct)

    total = len(shapes)
    results = []
    for shape in ["cliff", "slow_burn", "bump", "plateau", "other"]:
        stats = shape_stats.get(shape)
        if not stats or not stats["views"]:
            results.append({
                "shape": shape, "count": 0, "pct": 0.0,
                "avg_views": 0, "avg_retention": 0.0,
            })
            continue

        count = len(stats["views"])
        results.append({
            "shape": shape,
            "count": count,
            "pct": (count / total * 100) if total else 0.0,
            "avg_views": int(mean(stats["views"])),
            "avg_retention": round(mean(stats["retentions"]), 1),
        })

    return results


def analyze_shapes_vs_traffic(
    shapes: Dict[str, str],
    traffic_data: Dict[str, List[dict]],
) -> List[dict]:
    """
    Traffic source breakdown by curve shape.

    Returns:
        List of dicts with shape, search_pct, suggested_pct, subscriber_pct, total_views.
    """
    shape_traffic: Dict[str, dict] = defaultdict(lambda: {
        "search": 0, "suggested": 0, "subscriber": 0, "total": 0,
    })

    for vid, shape in shapes.items():
        sources = traffic_data.get(vid, [])
        for src in sources:
            source_type = src.get("source_type", "")
            views = src.get("views", 0) or 0

            shape_traffic[shape]["total"] += views

            if source_type == "YT_SEARCH":
                shape_traffic[shape]["search"] += views
            elif source_type == "RELATED_VIDEO":
                shape_traffic[shape]["suggested"] += views
            elif source_type == "SUBSCRIBER":
                shape_traffic[shape]["subscriber"] += views

    results = []
    for shape in ["cliff", "slow_burn", "bump", "plateau", "other"]:
        t = shape_traffic.get(shape, {"search": 0, "suggested": 0, "subscriber": 0, "total": 0})
        total = t["total"] or 1  # avoid division by zero
        results.append({
            "shape": shape,
            "search_pct": round(t["search"] / total * 100, 1),
            "suggested_pct": round(t["suggested"] / total * 100, 1),
            "subscriber_pct": round(t["subscriber"] / total * 100, 1),
            "total_views": t["total"],
        })

    return results


def analyze_shapes_vs_topic(
    shapes: Dict[str, str],
    metadata: Dict[str, dict],
) -> Dict[str, Dict[str, int]]:
    """
    Cross-tabulate curve shape by topic type.

    Returns:
        Dict mapping topic_type -> {shape: count}.
    """
    cross_tab: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for vid, shape in shapes.items():
        meta = metadata.get(vid, {})
        topic = meta.get("topic_type") or "unknown"
        cross_tab[topic][shape] += 1

    return dict(cross_tab)


def find_bump_locations(
    shapes: Dict[str, str],
    retention_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    For videos classified as 'bump', find WHERE the recovery happens.

    Categorizes bump position as early (0.15-0.35), mid (0.35-0.65), late (0.65-1.0).

    Returns:
        List of dicts with video_id, title, bump_position, bump_zone, bump_magnitude.
    """
    results = []

    for vid, shape in shapes.items():
        if shape != "bump":
            continue

        points = retention_data.get(vid, [])
        if len(points) < 15:
            continue

        sorted_pts = sorted(points, key=lambda p: p["position"])
        positions = [p["position"] for p in sorted_pts]
        retentions = [p["retention"] for p in sorted_pts]

        idx_15 = _find_nearest_index(positions, 0.15)

        best_magnitude = 0.0
        best_position = 0.0

        for i in range(idx_15, len(retentions)):
            if i >= 10:
                magnitude = retentions[i] - retentions[i - 10]
                if magnitude > best_magnitude:
                    best_magnitude = magnitude
                    best_position = positions[i]

        # Categorize zone
        if best_position < 0.35:
            zone = "early"
        elif best_position < 0.65:
            zone = "mid"
        else:
            zone = "late"

        meta = metadata.get(vid, {})
        duration = meta.get("duration_seconds", 0) or 0
        timestamp_seconds = int(best_position * duration) if duration else 0
        timestamp = f"{timestamp_seconds // 60}:{timestamp_seconds % 60:02d}"

        results.append({
            "video_id": vid,
            "title": meta.get("title", vid),
            "bump_position": round(best_position, 2),
            "bump_zone": zone,
            "bump_magnitude": round(best_magnitude, 3),
            "timestamp": timestamp,
            "duration_seconds": duration,
        })

    results.sort(key=lambda r: r["bump_magnitude"], reverse=True)
    return results


# =========================================================================
# SINGLE VIDEO REPORT
# =========================================================================

def single_video_report(
    video_id: str,
    retention_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate a summary for a single video's curve shape."""
    points = retention_data.get(video_id, [])
    if not points:
        return f"No retention data found for {video_id}"

    shape = classify_curve(points)
    meta = metadata.get(video_id, {})
    title = meta.get("title", video_id)
    views = meta.get("views", "N/A")
    avg_ret = meta.get("avg_view_percentage", "N/A")

    sorted_pts = sorted(points, key=lambda p: p["position"])
    retentions = [p["retention"] for p in sorted_pts]

    lines = [
        f"Video: {title}",
        f"ID: {video_id}",
        f"Shape: {shape}",
        f"Views: {views}",
        f"Avg Retention: {avg_ret}%",
        f"",
        f"Retention checkpoints:",
        f"  Start (0.01): {retentions[0]:.1%}" if retentions else "",
        f"  10% mark:     {retentions[min(9, len(retentions)-1)]:.1%}" if len(retentions) > 9 else "",
        f"  25% mark:     {retentions[min(24, len(retentions)-1)]:.1%}" if len(retentions) > 24 else "",
        f"  50% mark:     {retentions[min(49, len(retentions)-1)]:.1%}" if len(retentions) > 49 else "",
        f"  75% mark:     {retentions[min(74, len(retentions)-1)]:.1%}" if len(retentions) > 74 else "",
        f"  End (1.0):    {retentions[-1]:.1%}" if retentions else "",
    ]

    if shape == "bump":
        bumps = find_bump_locations(
            {video_id: shape}, retention_data, metadata,
        )
        if bumps:
            b = bumps[0]
            lines.extend([
                f"",
                f"Bump detected at position {b['bump_position']} ({b['timestamp']})",
                f"  Zone: {b['bump_zone']}",
                f"  Magnitude: +{b['bump_magnitude']:.1%}",
            ])

    return "\n".join(lines)


# =========================================================================
# FULL REPORT GENERATION
# =========================================================================

def generate_full_report(
    shapes: Dict[str, str],
    retention_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
    traffic_data: Dict[str, List[dict]],
) -> str:
    """Generate the full markdown report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = len(shapes)

    # Run all analyses
    view_stats = analyze_shapes_vs_views(shapes, metadata, retention_data)
    traffic_stats = analyze_shapes_vs_traffic(shapes, traffic_data)
    topic_cross = analyze_shapes_vs_topic(shapes, metadata)
    bumps = find_bump_locations(shapes, retention_data, metadata)

    lines = [
        "# Retention Curve Shape Analysis",
        f"**Generated:** {now}",
        f"**Videos analyzed:** {total}",
        "",
        "## Classification Rules",
        "",
        "| Shape | Criteria |",
        "|-------|----------|",
        "| cliff | Retention at 10% mark < 50% of start, then drops < 30% more |",
        "| slow_burn | No 10-point segment drops > 15%, linear R² > 0.85 |",
        "| bump | After 15% mark, retention increases >= 3% over previous 10 points |",
        "| plateau | After 20% mark, retention stdev < 0.03 (nearly flat) |",
        "| other | Does not clearly fit any category |",
        "",
    ]

    # Section 1: Shape Distribution
    lines.extend([
        "## 1. Shape Distribution",
        "",
        "| Shape | Count | % | Avg Views | Avg Retention |",
        "|-------|------:|--:|----------:|--------------:|",
    ])
    for s in view_stats:
        lines.append(
            f"| {s['shape']} | {s['count']} | {s['pct']:.0f}% "
            f"| {s['avg_views']:,} | {s['avg_retention']:.1f}% |"
        )
    lines.append("")

    # Section 2: Shape x Traffic Source
    lines.extend([
        "## 2. Shape × Traffic Source",
        "",
        "| Shape | Search % | Suggested % | Subscriber % | Total Views |",
        "|-------|--------:|-----------:|-------------:|------------:|",
    ])
    for t in traffic_stats:
        lines.append(
            f"| {t['shape']} | {t['search_pct']:.1f}% | {t['suggested_pct']:.1f}% "
            f"| {t['subscriber_pct']:.1f}% | {t['total_views']:,} |"
        )
    lines.append("")

    # Section 3: Shape x Topic Type
    all_shapes = ["cliff", "slow_burn", "bump", "plateau", "other"]
    topics_sorted = sorted(topic_cross.keys())

    lines.extend([
        "## 3. Shape × Topic Type",
        "",
        "| Topic | " + " | ".join(all_shapes) + " | Total |",
        "|-------" + "|------:" * len(all_shapes) + "|------:|",
    ])
    for topic in topics_sorted:
        counts = topic_cross[topic]
        row_total = sum(counts.values())
        cells = " | ".join(str(counts.get(s, 0)) for s in all_shapes)
        lines.append(f"| {topic} | {cells} | {row_total} |")
    lines.append("")

    # Section 4: Bump Analysis
    lines.extend([
        "## 4. Bump Analysis",
        "",
    ])
    if bumps:
        lines.extend([
            "Where do mid-video recoveries happen?",
            "",
            "| Video | Position | Timestamp | Zone | Magnitude |",
            "|-------|--------:|-----------|------|----------:|",
        ])
        for b in bumps:
            title_short = b["title"][:50] + ("..." if len(b["title"]) > 50 else "")
            lines.append(
                f"| {title_short} | {b['bump_position']:.0%} "
                f"| {b['timestamp']} | {b['bump_zone']} "
                f"| +{b['bump_magnitude']:.1%} |"
            )
        lines.append("")

        # Zone summary
        zone_counts = defaultdict(int)
        for b in bumps:
            zone_counts[b["bump_zone"]] += 1
        lines.append("**Bump zone distribution:**")
        for zone in ["early", "mid", "late"]:
            count = zone_counts.get(zone, 0)
            lines.append(f"- {zone}: {count} videos")
        lines.append("")
    else:
        lines.append("No bump-shaped curves detected in the dataset.")
        lines.append("")

    # Section 5: Best-Performing Shapes
    lines.extend([
        "## 5. Best-Performing Shapes",
        "",
    ])

    # Sort by avg views descending
    ranked_by_views = sorted(
        [s for s in view_stats if s["count"] > 0],
        key=lambda s: s["avg_views"],
        reverse=True,
    )
    if ranked_by_views:
        best_views = ranked_by_views[0]
        lines.append(
            f"**Highest avg views:** {best_views['shape']} "
            f"({best_views['avg_views']:,} avg, n={best_views['count']})"
        )

    # Best for Suggested traffic
    ranked_by_suggested = sorted(
        [t for t in traffic_stats if t["total_views"] > 0],
        key=lambda t: t["suggested_pct"],
        reverse=True,
    )
    if ranked_by_suggested:
        best_suggested = ranked_by_suggested[0]
        lines.append(
            f"**Highest Suggested traffic:** {best_suggested['shape']} "
            f"({best_suggested['suggested_pct']:.1f}% of traffic)"
        )

    # Best retention
    ranked_by_retention = sorted(
        [s for s in view_stats if s["count"] > 0],
        key=lambda s: s["avg_retention"],
        reverse=True,
    )
    if ranked_by_retention:
        best_ret = ranked_by_retention[0]
        lines.append(
            f"**Highest avg retention:** {best_ret['shape']} "
            f"({best_ret['avg_retention']:.1f}%, n={best_ret['count']})"
        )

    lines.append("")

    # Section 6: Interpreted Findings
    lines.extend([
        "## Interpreted Findings",
        "",
    ])

    # Generate data-driven findings
    findings = _generate_findings(view_stats, traffic_stats, topic_cross, bumps)
    for f in findings:
        lines.append(f"- {f}")
    lines.append("")

    # Per-video appendix
    lines.extend([
        "## Appendix: Per-Video Classifications",
        "",
        "| Video | Shape | Views | Retention |",
        "|-------|-------|------:|----------:|",
    ])
    for vid, shape in sorted(shapes.items(), key=lambda x: -(metadata.get(x[0], {}).get("views", 0) or 0)):
        meta = metadata.get(vid, {})
        title = meta.get("title", vid)
        title_short = title[:55] + ("..." if len(title) > 55 else "")
        views = meta.get("views", 0) or 0
        avg_pct = meta.get("avg_view_percentage", 0) or 0
        lines.append(f"| {title_short} | {shape} | {views:,} | {avg_pct:.1f}% |")
    lines.append("")

    return "\n".join(lines)


def _generate_findings(
    view_stats: List[dict],
    traffic_stats: List[dict],
    topic_cross: Dict[str, Dict[str, int]],
    bumps: List[dict],
) -> List[str]:
    """Generate actionable finding bullets from the data."""
    findings = []

    # View stats insights
    active = [s for s in view_stats if s["count"] > 0]
    if len(active) >= 2:
        best = max(active, key=lambda s: s["avg_views"])
        worst = min(active, key=lambda s: s["avg_views"])
        if best["shape"] != worst["shape"]:
            findings.append(
                f"**{best['shape']}** curves average {best['avg_views']:,} views "
                f"vs **{worst['shape']}** at {worst['avg_views']:,} views "
                f"({best['avg_views'] / max(worst['avg_views'], 1):.1f}x difference)."
            )

    # Traffic insights
    active_traffic = [t for t in traffic_stats if t["total_views"] > 0]
    if active_traffic:
        best_search = max(active_traffic, key=lambda t: t["search_pct"])
        if best_search["search_pct"] > 15:
            findings.append(
                f"**{best_search['shape']}** curves get the most Search traffic "
                f"({best_search['search_pct']:.1f}%), suggesting these videos "
                f"rank well for their target keywords."
            )
        best_sugg = max(active_traffic, key=lambda t: t["suggested_pct"])
        if best_sugg["suggested_pct"] > 10:
            findings.append(
                f"**{best_sugg['shape']}** curves get the most Suggested/Related traffic "
                f"({best_sugg['suggested_pct']:.1f}%), indicating the algorithm "
                f"recommends these videos more."
            )

    # Bump insights
    if bumps:
        avg_mag = mean([b["bump_magnitude"] for b in bumps])
        zone_counts = defaultdict(int)
        for b in bumps:
            zone_counts[b["bump_zone"]] += 1
        dominant_zone = max(zone_counts, key=zone_counts.get) if zone_counts else "mid"
        findings.append(
            f"{len(bumps)} videos show mid-video recoveries (avg +{avg_mag:.1%}), "
            f"most commonly in the **{dominant_zone}** section. "
            f"Investigate what content triggers these recoveries."
        )

    # Topic-shape dominant patterns
    for topic, shape_counts in topic_cross.items():
        total = sum(shape_counts.values())
        if total >= 3:
            dominant = max(shape_counts, key=shape_counts.get)
            pct = shape_counts[dominant] / total * 100
            if pct >= 50:
                findings.append(
                    f"**{topic}** videos are predominantly **{dominant}** "
                    f"({pct:.0f}%, n={total})."
                )

    if not findings:
        findings.append("Not enough data to generate confident findings. Collect more retention curves.")

    return findings


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Classify retention curve shapes and correlate with performance.",
    )
    parser.add_argument(
        "--video", type=str, default=None,
        help="Analyze a single video by ID",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Generate full markdown report",
    )
    parser.add_argument(
        "--cached", action="store_true",
        help="Use cached data only (default behavior, kept for CLI consistency)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Errors only",
    )
    args = parser.parse_args()

    # Configure logging
    setup_logging(args.verbose, args.quiet)

    # Load data
    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata found in analytics.db. Run backfill first.")
        sys.exit(1)

    retention_data = load_retention_cache(video_id=args.video)
    if not retention_data:
        logger.error(
            "No retention cache data found at %s. Run retention backfill first.",
            CACHE_DIR,
        )
        sys.exit(1)

    # Single video mode
    if args.video:
        report = single_video_report(args.video, retention_data, metadata)
        print(report)
        return

    # Classify all curves
    shapes = classify_all_curves(retention_data)

    if not shapes:
        logger.error("No curves to classify.")
        sys.exit(1)

    # Summary mode (default)
    if not args.report:
        print(f"\nRetention Curve Shape Classification ({len(shapes)} videos)\n")
        view_stats = analyze_shapes_vs_views(shapes, metadata, retention_data)
        print(f"{'Shape':<12} {'Count':>5} {'%':>5}  {'Avg Views':>10}  {'Avg Ret':>8}")
        print("-" * 48)
        for s in view_stats:
            if s["count"] > 0:
                print(
                    f"{s['shape']:<12} {s['count']:>5} {s['pct']:>4.0f}%"
                    f"  {s['avg_views']:>10,}  {s['avg_retention']:>7.1f}%"
                )
        return

    # Full report mode
    traffic_data = load_traffic_data()
    report = generate_full_report(shapes, retention_data, metadata, traffic_data)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info("Report saved to %s", REPORT_PATH)

    print(report)


if __name__ == "__main__":
    main()
