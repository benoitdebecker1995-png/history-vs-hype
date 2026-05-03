"""
Pacing-to-Retention Cross-Video Analysis Tool

Correlates SRT speaking pace (WPM, sentence length, pauses, word complexity)
with YouTube retention data to find optimal pacing patterns.

Usage:
    python -m tools.youtube_analytics.pacing_analysis              # all videos
    python -m tools.youtube_analytics.pacing_analysis --video ID   # single video
    python -m tools.youtube_analytics.pacing_analysis --report     # generate markdown report
    python -m tools.youtube_analytics.pacing_analysis --cached     # skip API, use cache only
"""

import argparse
import json
import math
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

# Reuse SRT mapping and parsing from retention_analysis
from tools.youtube_analytics.retention_analysis import (
    build_srt_mapping,
    parse_srt,
    fetch_retention_cached,
    _load_cached,
)

logger = get_logger(__name__)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "tools" / "youtube_analytics" / "analytics.db"
REPORT_PATH = BASE_DIR / "channel-data" / "patterns" / "PACING-RETENTION-ANALYSIS.md"

# Analysis parameters
WINDOW_SECONDS = 30.0  # Sliding window size for pacing metrics
WINDOW_STEP = 0.01     # Step as fraction of video duration (matches retention data points)


# ---------------------------------------------------------------------------
# 1. Syllable Counter (CMU-free heuristic)
# ---------------------------------------------------------------------------

def _count_syllables(word: str) -> int:
    """
    Estimate syllable count for an English word using a heuristic.

    Based on the vowel-cluster method with common English adjustments.
    """
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Remove trailing silent e
    if word.endswith("e") and not word.endswith("le"):
        word = word[:-1]

    # Count vowel clusters
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    return max(1, count)


def avg_syllables_per_word(words: list[str]) -> float:
    """Average syllable count across a list of words."""
    if not words:
        return 0.0
    total = sum(_count_syllables(w) for w in words)
    return total / len(words)


# ---------------------------------------------------------------------------
# 2. Pacing Metrics for a Window
# ---------------------------------------------------------------------------

def _extract_words(text: str) -> list[str]:
    """Extract word tokens from text, stripping punctuation."""
    return [w for w in re.findall(r"[a-zA-Z']+", text) if len(w) > 0]


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on .!? boundaries."""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def compute_window_pacing(segments: list[dict], window_start: float,
                          window_end: float) -> dict | None:
    """
    Compute pacing metrics for SRT segments within a time window.

    Args:
        segments: Parsed SRT segments [{start_seconds, end_seconds, text}]
        window_start: Window start in seconds
        window_end: Window end in seconds

    Returns:
        {
            wpm: float,               # Words per minute
            sentence_len_avg: float,   # Average words per sentence
            sentence_len_std: float,   # Std dev of sentence lengths
            pause_density: float,      # Fraction of window that is silence
            avg_syllables: float,      # Average syllables per word
            word_count: int,           # Total words in window
        }
        or None if no text overlaps the window
    """
    # Collect segments overlapping this window
    overlapping = []
    for seg in segments:
        if seg["end_seconds"] >= window_start and seg["start_seconds"] <= window_end:
            overlapping.append(seg)

    if not overlapping:
        return None

    # Merge text from overlapping segments
    all_text = " ".join(seg["text"] for seg in overlapping)
    words = _extract_words(all_text)
    if not words:
        return None

    word_count = len(words)

    # Calculate spoken duration within window (sum of segment durations clipped to window)
    spoken_seconds = 0.0
    for seg in overlapping:
        seg_start = max(seg["start_seconds"], window_start)
        seg_end = min(seg["end_seconds"], window_end)
        spoken_seconds += max(0.0, seg_end - seg_start)

    window_duration = window_end - window_start
    if window_duration <= 0:
        return None

    # WPM: based on window duration (includes pauses)
    wpm = (word_count / window_duration) * 60.0

    # Sentence metrics
    sentences = _split_sentences(all_text)
    sentence_lengths = [len(_extract_words(s)) for s in sentences]
    sentence_lengths = [sl for sl in sentence_lengths if sl > 0]

    if sentence_lengths:
        sentence_len_avg = sum(sentence_lengths) / len(sentence_lengths)
        if len(sentence_lengths) > 1:
            mean = sentence_len_avg
            variance = sum((sl - mean) ** 2 for sl in sentence_lengths) / len(sentence_lengths)
            sentence_len_std = math.sqrt(variance)
        else:
            sentence_len_std = 0.0
    else:
        sentence_len_avg = word_count  # One long segment with no sentence-enders
        sentence_len_std = 0.0

    # Pause density: fraction of window that is NOT covered by subtitle blocks
    pause_seconds = window_duration - spoken_seconds
    pause_density = max(0.0, pause_seconds / window_duration)

    # Word complexity
    syllables = avg_syllables_per_word(words)

    return {
        "wpm": round(wpm, 1),
        "sentence_len_avg": round(sentence_len_avg, 1),
        "sentence_len_std": round(sentence_len_std, 2),
        "pause_density": round(pause_density, 3),
        "avg_syllables": round(syllables, 2),
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# 3. Per-Video Analysis
# ---------------------------------------------------------------------------

def analyze_video_pacing(video_id: str, title: str, duration_seconds: int,
                         topic_type: str, srt_path: Path,
                         retention_data: dict) -> dict | None:
    """
    Analyze pacing vs retention for a single video.

    Uses 30-second sliding windows aligned to retention data points.

    Returns:
        {
            video_id, title, topic_type, duration_seconds,
            data_points: [{position, retention, delta, timestamp_seconds,
                           wpm, sentence_len_avg, sentence_len_std,
                           pause_density, avg_syllables}],
            summary: {avg_wpm, avg_sentence_len, ...}
        }
    """
    segments = parse_srt(srt_path)
    if not segments:
        logger.warning("No SRT segments parsed for %s", video_id)
        return None

    data_points = retention_data.get("data_points", [])
    if len(data_points) < 2:
        logger.warning("Insufficient retention data for %s", video_id)
        return None

    analyzed = []
    half_window = WINDOW_SECONDS / 2.0

    for i, dp in enumerate(data_points):
        position = dp["position"]
        retention = dp["retention"]
        timestamp = position * duration_seconds

        # Delta from previous point
        if i == 0:
            delta = 0.0
        else:
            delta = retention - data_points[i - 1]["retention"]

        # Compute pacing in window around this timestamp
        w_start = max(0.0, timestamp - half_window)
        w_end = min(float(duration_seconds), timestamp + half_window)
        pacing = compute_window_pacing(segments, w_start, w_end)

        if pacing is None:
            continue

        analyzed.append({
            "position": round(position, 4),
            "retention": round(retention, 4),
            "delta": round(delta, 4),
            "timestamp_seconds": round(timestamp, 1),
            **pacing,
        })

    if not analyzed:
        logger.warning("No pacing data points for %s", video_id)
        return None

    # Video-level summary
    wpm_values = [p["wpm"] for p in analyzed]
    sent_values = [p["sentence_len_avg"] for p in analyzed]
    pause_values = [p["pause_density"] for p in analyzed]
    syll_values = [p["avg_syllables"] for p in analyzed]

    summary = {
        "avg_wpm": round(sum(wpm_values) / len(wpm_values), 1),
        "min_wpm": round(min(wpm_values), 1),
        "max_wpm": round(max(wpm_values), 1),
        "avg_sentence_len": round(sum(sent_values) / len(sent_values), 1),
        "avg_pause_density": round(sum(pause_values) / len(pause_values), 3),
        "avg_syllables": round(sum(syll_values) / len(syll_values), 2),
        "data_point_count": len(analyzed),
    }

    return {
        "video_id": video_id,
        "title": title,
        "topic_type": topic_type,
        "duration_seconds": duration_seconds,
        "data_points": analyzed,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# 4. Statistical Helpers
# ---------------------------------------------------------------------------

def _pearson_r(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """
    Compute Pearson correlation coefficient and two-tailed p-value.

    Falls back to manual calculation if scipy is not available.

    Returns:
        (r, p_value) or (0.0, 1.0) if computation fails
    """
    n = len(xs)
    if n < 3 or len(ys) != n:
        return 0.0, 1.0

    try:
        from scipy.stats import pearsonr
        r, p = pearsonr(xs, ys)
        return round(r, 4), round(p, 6)
    except ImportError:
        pass

    # Manual Pearson r
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    dx = [x - mean_x for x in xs]
    dy = [y - mean_y for y in ys]
    num = sum(a * b for a, b in zip(dx, dy))
    den_x = math.sqrt(sum(a * a for a in dx))
    den_y = math.sqrt(sum(b * b for b in dy))
    if den_x == 0 or den_y == 0:
        return 0.0, 1.0
    r = num / (den_x * den_y)

    # Approximate p-value via t-distribution (two-tailed)
    if abs(r) >= 1.0:
        return round(r, 4), 0.0
    t_stat = r * math.sqrt((n - 2) / (1 - r * r))
    # Use rough approximation for p-value (normal approx for large n)
    # For small n this is imprecise, but avoids external dependencies
    p_approx = 2.0 * (1.0 - _normal_cdf(abs(t_stat)))
    return round(r, 4), round(max(0.0, p_approx), 6)


def _normal_cdf(x: float) -> float:
    """Approximate standard normal CDF using Abramowitz & Stegun formula."""
    # Constants for the approximation
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    sign = 1.0 if x >= 0 else -1.0
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + sign * y)


def _bin_and_average(values: list[float], deltas: list[float],
                     n_bins: int = 10) -> list[tuple[float, float, int]]:
    """
    Bin values into n_bins quantiles and compute average delta per bin.

    Returns: [(bin_center, avg_delta, count), ...]
    """
    if not values or not deltas:
        return []

    paired = sorted(zip(values, deltas), key=lambda x: x[0])
    bin_size = max(1, len(paired) // n_bins)

    bins = []
    for i in range(0, len(paired), bin_size):
        chunk = paired[i:i + bin_size]
        if not chunk:
            continue
        vs = [c[0] for c in chunk]
        ds = [c[1] for c in chunk]
        center = (min(vs) + max(vs)) / 2.0
        avg_d = sum(ds) / len(ds)
        bins.append((round(center, 1), round(avg_d, 5), len(chunk)))

    return bins


# ---------------------------------------------------------------------------
# 5. Cross-Video Aggregation
# ---------------------------------------------------------------------------

def aggregate_pacing(analyses: list[dict]) -> dict:
    """
    Aggregate pacing-retention patterns across all analyzed videos.

    Returns:
        {
            videos_analyzed, total_data_points,
            correlations: {wpm_r, wpm_p, sent_len_r, sent_len_p, ...},
            wpm_bins: [(center, avg_delta, count), ...],
            sent_len_bins: [...],
            by_position: {early/mid/late: {avg_wpm, wpm_r, ...}},
            by_topic_type: {topic: {avg_wpm, wpm_r, ...}},
            video_summaries: [{video_id, title, avg_wpm, avg_retention, ...}],
            optimal_ranges: {wpm_best_range, sent_len_best_range, ...},
        }
    """
    # Collect all data points
    all_points = []
    for analysis in analyses:
        vid = analysis["video_id"]
        title = analysis["title"]
        topic = analysis["topic_type"]
        for pt in analysis["data_points"]:
            all_points.append({**pt, "video_id": vid, "video_title": title, "topic_type": topic})

    if not all_points:
        return {"videos_analyzed": 0, "total_data_points": 0}

    # Skip first few data points (intro drop confound) for correlation
    scoreable = [p for p in all_points if p["position"] > 0.05]

    # --- Global correlations ---
    wpm_vals = [p["wpm"] for p in scoreable]
    deltas = [p["delta"] for p in scoreable]
    sent_vals = [p["sentence_len_avg"] for p in scoreable]
    sent_std_vals = [p["sentence_len_std"] for p in scoreable]
    pause_vals = [p["pause_density"] for p in scoreable]
    syll_vals = [p["avg_syllables"] for p in scoreable]

    wpm_r, wpm_p = _pearson_r(wpm_vals, deltas)
    sent_r, sent_p = _pearson_r(sent_vals, deltas)
    sent_std_r, sent_std_p = _pearson_r(sent_std_vals, deltas)
    pause_r, pause_p = _pearson_r(pause_vals, deltas)
    syll_r, syll_p = _pearson_r(syll_vals, deltas)

    correlations = {
        "wpm_r": wpm_r, "wpm_p": wpm_p,
        "sentence_len_r": sent_r, "sentence_len_p": sent_p,
        "sentence_variation_r": sent_std_r, "sentence_variation_p": sent_std_p,
        "pause_density_r": pause_r, "pause_density_p": pause_p,
        "syllable_complexity_r": syll_r, "syllable_complexity_p": syll_p,
    }

    # --- WPM and sentence length bins ---
    wpm_bins = _bin_and_average(wpm_vals, deltas, n_bins=10)
    sent_bins = _bin_and_average(sent_vals, deltas, n_bins=8)
    pause_bins = _bin_and_average(pause_vals, deltas, n_bins=6)

    # --- By position (early/mid/late) ---
    position_bins = {"early": (0.05, 0.33), "mid": (0.33, 0.66), "late": (0.66, 1.01)}
    by_position = {}
    for bin_name, (lo, hi) in position_bins.items():
        pts = [p for p in scoreable if lo <= p["position"] < hi]
        if len(pts) < 5:
            continue
        w = [p["wpm"] for p in pts]
        d = [p["delta"] for p in pts]
        s = [p["sentence_len_avg"] for p in pts]
        r_wpm, p_wpm = _pearson_r(w, d)
        r_sent, p_sent = _pearson_r(s, d)
        by_position[bin_name] = {
            "avg_wpm": round(sum(w) / len(w), 1),
            "wpm_r": r_wpm, "wpm_p": p_wpm,
            "avg_sentence_len": round(sum(s) / len(s), 1),
            "sent_r": r_sent, "sent_p": p_sent,
            "avg_delta": round(sum(d) / len(d), 5),
            "count": len(pts),
        }

    # --- By topic type ---
    by_topic = defaultdict(list)
    for p in scoreable:
        by_topic[p["topic_type"]].append(p)

    by_topic_type = {}
    for topic, pts in by_topic.items():
        if len(pts) < 10:
            continue
        w = [p["wpm"] for p in pts]
        d = [p["delta"] for p in pts]
        s = [p["sentence_len_avg"] for p in pts]
        r_wpm, p_wpm = _pearson_r(w, d)
        by_topic_type[topic] = {
            "avg_wpm": round(sum(w) / len(w), 1),
            "wpm_r": r_wpm, "wpm_p": p_wpm,
            "avg_sentence_len": round(sum(s) / len(s), 1),
            "avg_delta": round(sum(d) / len(d), 5),
            "count": len(pts),
        }

    # --- Per-video summaries ---
    video_summaries = []
    for analysis in analyses:
        pts = analysis["data_points"]
        retentions = [p["retention"] for p in pts]
        avg_ret = sum(retentions) / len(retentions) if retentions else 0
        video_summaries.append({
            "video_id": analysis["video_id"],
            "title": analysis["title"],
            "topic_type": analysis["topic_type"],
            "duration_min": round(analysis["duration_seconds"] / 60, 1),
            "avg_wpm": analysis["summary"]["avg_wpm"],
            "avg_sentence_len": analysis["summary"]["avg_sentence_len"],
            "avg_pause_density": analysis["summary"]["avg_pause_density"],
            "avg_syllables": analysis["summary"]["avg_syllables"],
            "avg_retention": round(avg_ret, 4),
        })

    # --- Find optimal ranges (best-performing bins) ---
    optimal = {}
    if wpm_bins:
        best_wpm_bin = max(wpm_bins, key=lambda b: b[1])
        optimal["wpm_best_center"] = best_wpm_bin[0]
        optimal["wpm_best_delta"] = best_wpm_bin[1]
    if sent_bins:
        best_sent_bin = max(sent_bins, key=lambda b: b[1])
        optimal["sent_len_best_center"] = best_sent_bin[0]
        optimal["sent_len_best_delta"] = best_sent_bin[1]
    if pause_bins:
        best_pause_bin = max(pause_bins, key=lambda b: b[1])
        optimal["pause_best_center"] = best_pause_bin[0]
        optimal["pause_best_delta"] = best_pause_bin[1]

    return {
        "videos_analyzed": len(analyses),
        "total_data_points": len(all_points),
        "scoreable_points": len(scoreable),
        "correlations": correlations,
        "wpm_bins": wpm_bins,
        "sent_len_bins": sent_bins,
        "pause_bins": pause_bins,
        "by_position": by_position,
        "by_topic_type": by_topic_type,
        "video_summaries": video_summaries,
        "optimal_ranges": optimal,
    }


# ---------------------------------------------------------------------------
# 6. Report Generation
# ---------------------------------------------------------------------------

def _significance_label(p: float) -> str:
    """Return significance label for a p-value."""
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "n.s."


def _strength_label(r: float) -> str:
    """Return correlation strength label."""
    ar = abs(r)
    if ar >= 0.5:
        return "strong"
    elif ar >= 0.3:
        return "moderate"
    elif ar >= 0.1:
        return "weak"
    else:
        return "negligible"


def generate_report(agg: dict, analyses: list[dict]) -> str:
    """Generate markdown report from aggregated pacing data."""
    lines = [
        "# Pacing-to-Retention Correlation Analysis",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Videos analyzed:** {agg['videos_analyzed']}",
        f"**Total data points:** {agg['total_data_points']} "
        f"(scoreable: {agg['scoreable_points']}, excludes intro drop zone <5%)",
        f"**Window size:** {WINDOW_SECONDS}s sliding windows",
        "",
        "---",
        "",
        "## 1. Global Correlations: Pacing Metrics vs Retention Delta",
        "",
        "| Metric | Pearson r | p-value | Significance | Strength |",
        "|---|---|---|---|---|",
    ]

    corr = agg["correlations"]
    corr_rows = [
        ("Words per minute (WPM)", "wpm_r", "wpm_p"),
        ("Sentence length (avg words)", "sentence_len_r", "sentence_len_p"),
        ("Sentence length variation (std)", "sentence_variation_r", "sentence_variation_p"),
        ("Pause density (silence fraction)", "pause_density_r", "pause_density_p"),
        ("Word complexity (avg syllables)", "syllable_complexity_r", "syllable_complexity_p"),
    ]
    for label, r_key, p_key in corr_rows:
        r_val = corr[r_key]
        p_val = corr[p_key]
        lines.append(
            f"| {label} | {r_val:+.4f} | {p_val:.6f} | "
            f"{_significance_label(p_val)} | {_strength_label(r_val)} |"
        )

    lines.extend([
        "",
        "**Key:** \\* p<0.05, \\*\\* p<0.01, \\*\\*\\* p<0.001, n.s. = not significant",
        "",
        "### Interpretation",
        "",
        "- Positive r = higher metric value correlates with retention GAIN",
        "- Negative r = higher metric value correlates with retention DROP",
        "- Only values with p<0.05 should be considered statistically meaningful",
        "- Natural retention decay means most deltas are negative; "
        "correlation captures whether pacing DIFFERENCES predict retention DIFFERENCES",
        "",
    ])

    # --- WPM bins ---
    lines.extend([
        "---",
        "",
        "## 2. WPM vs Retention Delta (Binned)",
        "",
        "| WPM Range (center) | Avg Retention Delta | n |",
        "|---|---|---|",
    ])
    for center, avg_d, count in agg.get("wpm_bins", []):
        lines.append(f"| ~{center:.0f} WPM | {avg_d:+.5f} | {count} |")

    optimal = agg.get("optimal_ranges", {})
    if "wpm_best_center" in optimal:
        lines.extend([
            "",
            f"**Best WPM range:** ~{optimal['wpm_best_center']:.0f} WPM "
            f"(avg delta: {optimal['wpm_best_delta']:+.5f})",
        ])

    # --- Sentence length bins ---
    lines.extend([
        "",
        "---",
        "",
        "## 3. Sentence Length vs Retention Delta (Binned)",
        "",
        "| Avg Sentence Length (words) | Avg Retention Delta | n |",
        "|---|---|---|",
    ])
    for center, avg_d, count in agg.get("sent_len_bins", []):
        lines.append(f"| ~{center:.0f} words | {avg_d:+.5f} | {count} |")

    if "sent_len_best_center" in optimal:
        lines.extend([
            "",
            f"**Best sentence length:** ~{optimal['sent_len_best_center']:.0f} words/sentence "
            f"(avg delta: {optimal['sent_len_best_delta']:+.5f})",
        ])

    # --- Pause density bins ---
    lines.extend([
        "",
        "---",
        "",
        "## 4. Pause Density vs Retention Delta (Binned)",
        "",
        "| Pause Density (silence %) | Avg Retention Delta | n |",
        "|---|---|---|",
    ])
    for center, avg_d, count in agg.get("pause_bins", []):
        lines.append(f"| {center:.1%} silence | {avg_d:+.5f} | {count} |")

    if "pause_best_center" in optimal:
        lines.extend([
            "",
            f"**Best pause density:** ~{optimal['pause_best_center']:.1%} silence "
            f"(avg delta: {optimal['pause_best_delta']:+.5f})",
        ])

    # --- By position ---
    lines.extend([
        "",
        "---",
        "",
        "## 5. Pacing by Video Position",
        "",
        "Does optimal pacing differ for early/mid/late portions of videos?",
        "",
        "| Position | Avg WPM | WPM-Retention r | Avg Sentence Len | "
        "Sent-Retention r | Avg Delta | n |",
        "|---|---|---|---|---|---|---|",
    ])
    for bin_name in ["early", "mid", "late"]:
        data = agg["by_position"].get(bin_name)
        if not data:
            continue
        lines.append(
            f"| {bin_name} | {data['avg_wpm']:.0f} | "
            f"{data['wpm_r']:+.4f} {_significance_label(data['wpm_p'])} | "
            f"{data['avg_sentence_len']:.1f} | "
            f"{data['sent_r']:+.4f} {_significance_label(data['sent_p'])} | "
            f"{data['avg_delta']:+.5f} | {data['count']} |"
        )

    # --- By topic type ---
    if agg["by_topic_type"]:
        lines.extend([
            "",
            "---",
            "",
            "## 6. Pacing by Topic Type",
            "",
            "| Topic Type | Avg WPM | WPM-Retention r | "
            "Avg Sentence Len | Avg Delta | n |",
            "|---|---|---|---|---|---|",
        ])
        for topic, data in sorted(agg["by_topic_type"].items(),
                                   key=lambda x: x[1]["count"], reverse=True):
            lines.append(
                f"| {topic} | {data['avg_wpm']:.0f} | "
                f"{data['wpm_r']:+.4f} | {data['avg_sentence_len']:.1f} | "
                f"{data['avg_delta']:+.5f} | {data['count']} |"
            )

    # --- Per-video summary ---
    lines.extend([
        "",
        "---",
        "",
        "## 7. Per-Video Pacing Summary",
        "",
        "| Video | Duration | Avg WPM | Avg Sent Len | Pause % | "
        "Syllables | Avg Retention |",
        "|---|---|---|---|---|---|---|",
    ])
    # Sort by avg_wpm for easy scanning
    for vs in sorted(agg["video_summaries"], key=lambda x: x["avg_wpm"], reverse=True):
        title_short = vs["title"][:45] + ("..." if len(vs["title"]) > 45 else "")
        lines.append(
            f"| {title_short} | {vs['duration_min']:.0f}m | "
            f"{vs['avg_wpm']:.0f} | {vs['avg_sentence_len']:.1f} | "
            f"{vs['avg_pause_density']:.1%} | {vs['avg_syllables']:.2f} | "
            f"{vs['avg_retention']:.1%} |"
        )

    # --- Actionable recommendations ---
    lines.extend([
        "",
        "---",
        "",
        "## 8. Actionable Recommendations",
        "",
    ])
    recs = _generate_recommendations(agg)
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. {rec}")

    # --- Interpreted findings placeholder ---
    lines.extend([
        "",
        "---",
        "",
        "## 9. Interpreted Findings",
        "",
        "*This section is for human analysis after reviewing the data above.*",
        "",
        "### Key Takeaways",
        "",
        "- [ ] What WPM range should be the target for new scripts?",
        "- [ ] Does sentence length variation correlate with viewer engagement?",
        "- [ ] Are pauses helping or hurting retention?",
        "- [ ] Does optimal pacing differ between territorial and ideological topics?",
        "- [ ] Should the teleprompter speed be adjusted based on these findings?",
        "",
        "### Script-Writer-v2 Rule Candidates",
        "",
        "- [ ] WPM target range: ___-___ (based on optimal bin above)",
        "- [ ] Maximum sentence length: ___ words (based on drop-off point)",
        "- [ ] Minimum pause ratio: ___% (based on pause density data)",
        "",
        "---",
        "",
        f"*Analysis based on {agg['videos_analyzed']} videos with "
        f"{agg['total_data_points']} pacing-retention data points "
        f"({WINDOW_SECONDS:.0f}s sliding windows).*",
    ])

    return "\n".join(lines)


def _generate_recommendations(agg: dict) -> list[str]:
    """Generate data-driven recommendations from aggregated pacing data."""
    recs = []
    corr = agg.get("correlations", {})
    optimal = agg.get("optimal_ranges", {})

    # WPM recommendation
    wpm_r = corr.get("wpm_r", 0)
    wpm_p = corr.get("wpm_p", 1)
    if wpm_p < 0.05:
        direction = "faster" if wpm_r > 0 else "slower"
        recs.append(
            f"**WPM correlates with retention** (r={wpm_r:+.4f}, p={wpm_p:.4f}). "
            f"Slightly {direction} delivery may improve retention. "
            + (f"Best bin: ~{optimal['wpm_best_center']:.0f} WPM."
               if "wpm_best_center" in optimal else "")
        )
    else:
        recs.append(
            f"**WPM has no significant correlation with retention** (r={wpm_r:+.4f}, "
            f"p={wpm_p:.4f}). Current speaking pace is not a retention driver "
            f"-- focus on content quality instead."
        )

    # Sentence length recommendation
    sent_r = corr.get("sentence_len_r", 0)
    sent_p = corr.get("sentence_len_p", 1)
    if sent_p < 0.05:
        direction = "longer" if sent_r > 0 else "shorter"
        recs.append(
            f"**Sentence length correlates with retention** (r={sent_r:+.4f}, "
            f"p={sent_p:.4f}). Use {direction} sentences for better engagement."
            + (f" Optimal: ~{optimal['sent_len_best_center']:.0f} words/sentence."
               if "sent_len_best_center" in optimal else "")
        )
    else:
        recs.append(
            f"**Sentence length is not a significant retention driver** "
            f"(r={sent_r:+.4f}, p={sent_p:.4f}). "
            f"Vary naturally for rhythm without worrying about word count per sentence."
        )

    # Sentence variation
    var_r = corr.get("sentence_variation_r", 0)
    var_p = corr.get("sentence_variation_p", 1)
    if var_p < 0.05:
        direction = "more" if var_r > 0 else "less"
        recs.append(
            f"**Sentence length variation matters** (r={var_r:+.4f}, p={var_p:.4f}). "
            f"Use {direction} variation in sentence length (mix short punchy "
            f"sentences with longer explanatory ones)."
        )

    # Pause density
    pause_r = corr.get("pause_density_r", 0)
    pause_p = corr.get("pause_density_p", 1)
    if pause_p < 0.05:
        direction = "more pauses" if pause_r > 0 else "fewer pauses"
        recs.append(
            f"**Pause density correlates with retention** (r={pause_r:+.4f}, "
            f"p={pause_p:.4f}). Consider {direction} in delivery."
            + (f" Optimal silence ratio: ~{optimal['pause_best_center']:.0%}."
               if "pause_best_center" in optimal else "")
        )

    # Word complexity
    syll_r = corr.get("syllable_complexity_r", 0)
    syll_p = corr.get("syllable_complexity_p", 1)
    if syll_p < 0.05:
        direction = "more complex" if syll_r > 0 else "simpler"
        recs.append(
            f"**Word complexity affects retention** (r={syll_r:+.4f}, "
            f"p={syll_p:.4f}). Viewers respond to {direction} vocabulary."
        )

    # Position-specific insight
    pos = agg.get("by_position", {})
    if "early" in pos and "late" in pos:
        early_wpm = pos["early"]["avg_wpm"]
        late_wpm = pos["late"]["avg_wpm"]
        diff = late_wpm - early_wpm
        if abs(diff) > 5:
            direction = "speeds up" if diff > 0 else "slows down"
            recs.append(
                f"**Natural pacing shift:** delivery {direction} by "
                f"{abs(diff):.0f} WPM from early ({early_wpm:.0f}) to "
                f"late ({late_wpm:.0f}) video. Monitor whether this "
                f"helps or hurts late-video retention."
            )

    # Cross-video insight
    summaries = agg.get("video_summaries", [])
    if len(summaries) >= 5:
        # Correlate video-level avg_wpm with avg_retention
        v_wpm = [s["avg_wpm"] for s in summaries]
        v_ret = [s["avg_retention"] for s in summaries]
        v_r, v_p = _pearson_r(v_wpm, v_ret)
        if v_p < 0.1:
            recs.append(
                f"**Cross-video:** Videos with {'faster' if v_r > 0 else 'slower'} "
                f"avg WPM tend to have {'higher' if v_r > 0 else 'lower'} overall retention "
                f"(r={v_r:+.4f}, p={v_p:.4f}). Consider this for overall delivery calibration."
            )

    if not recs:
        recs.append(
            "No statistically significant correlations found between pacing "
            "metrics and retention. This suggests content quality and topic "
            "selection are stronger retention drivers than delivery pacing."
        )

    return recs


# ---------------------------------------------------------------------------
# 7. Main / CLI
# ---------------------------------------------------------------------------

def run_analysis(video_id: str | None = None, cached_only: bool = False,
                 generate_markdown: bool = False) -> dict:
    """
    Main entry point. Analyze pacing-to-retention patterns.

    Args:
        video_id: If set, analyze only this video
        cached_only: If True, skip API calls and use only cached data
        generate_markdown: If True, write report to PACING-RETENTION-ANALYSIS.md

    Returns:
        Aggregated results dict
    """
    # Load video metadata
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    if video_id:
        cur.execute(
            "SELECT video_id, title, duration_seconds, topic_type "
            "FROM videos WHERE video_id = ?",
            (video_id,),
        )
    else:
        cur.execute(
            "SELECT video_id, title, duration_seconds, topic_type "
            "FROM videos WHERE duration_seconds > 60"
        )
    videos = cur.fetchall()
    conn.close()

    if not videos:
        logger.error("No videos found in database")
        return {}

    logger.info("Processing %d videos...", len(videos))

    # Build SRT mapping
    srt_map = build_srt_mapping()

    analyses = []
    skipped_no_srt = 0
    skipped_no_retention = 0

    for i, (vid, title, duration, topic) in enumerate(videos, 1):
        # Check SRT
        if vid not in srt_map:
            skipped_no_srt += 1
            logger.debug("No SRT for %s (%s)", vid, title)
            continue

        # Get retention data
        if cached_only:
            ret_data = _load_cached(vid)
        else:
            ret_data = fetch_retention_cached(vid)

        if not ret_data:
            skipped_no_retention += 1
            logger.debug("No retention data for %s (%s)", vid, title)
            continue

        # Analyze
        safe_title = title.encode("ascii", errors="replace").decode("ascii")
        print(f"  [{i}/{len(videos)}] Analyzing: {safe_title}")
        result = analyze_video_pacing(vid, title, duration, topic or "general",
                                      srt_map[vid], ret_data)
        if result:
            analyses.append(result)

    logger.info(
        "Analyzed %d videos (skipped: %d no SRT, %d no retention)",
        len(analyses), skipped_no_srt, skipped_no_retention,
    )

    if not analyses:
        print("No videos had both SRT files and retention data.")
        return {}

    # Aggregate
    print(f"\nAggregating pacing data from {len(analyses)} videos...")
    agg = aggregate_pacing(analyses)

    # Print summary
    print("\n=== Pacing-Retention Correlations ===\n")
    print(f"{'Metric':<35} {'Pearson r':>10} {'p-value':>10} {'Sig':>5}")
    print("-" * 63)
    corr = agg.get("correlations", {})
    for label, r_key, p_key in [
        ("WPM", "wpm_r", "wpm_p"),
        ("Sentence length", "sentence_len_r", "sentence_len_p"),
        ("Sentence variation", "sentence_variation_r", "sentence_variation_p"),
        ("Pause density", "pause_density_r", "pause_density_p"),
        ("Word complexity", "syllable_complexity_r", "syllable_complexity_p"),
    ]:
        r_val = corr.get(r_key, 0)
        p_val = corr.get(p_key, 1)
        print(f"{label:<35} {r_val:>+10.4f} {p_val:>10.6f} {_significance_label(p_val):>5}")

    # Print WPM bins
    print("\n=== WPM vs Retention Delta (Binned) ===\n")
    print(f"{'WPM Center':>12} {'Avg Delta':>12} {'Count':>7}")
    print("-" * 34)
    for center, avg_d, count in agg.get("wpm_bins", []):
        print(f"{center:>12.0f} {avg_d:>+12.5f} {count:>7}")

    # Generate report
    if generate_markdown:
        report = generate_report(agg, analyses)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"\nReport written to: {REPORT_PATH}")

    return agg


def main():
    parser = argparse.ArgumentParser(
        description="Cross-video pacing-to-retention analysis tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.pacing_analysis
  python -m tools.youtube_analytics.pacing_analysis --video oDK52GwjTIo
  python -m tools.youtube_analytics.pacing_analysis --report
  python -m tools.youtube_analytics.pacing_analysis --cached --report""",
    )
    parser.add_argument(
        "--video", metavar="ID",
        help="Analyze a single video by ID",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Generate markdown report at channel-data/patterns/PACING-RETENTION-ANALYSIS.md",
    )
    parser.add_argument(
        "--cached", action="store_true",
        help="Use only cached retention data (no API calls)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Debug output")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Errors only")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    run_analysis(
        video_id=args.video,
        cached_only=args.cached,
        generate_markdown=args.report,
    )


if __name__ == "__main__":
    main()
