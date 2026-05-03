"""
Retention Prediction Tool for History vs Hype

Given a NEW script (pre-filming), predicts the retention curve and flags
sections likely to cause viewer dropout, based on empirical data from
42 videos and 4,200 retention data points.

Data sources:
  - channel-data/patterns/RETENTION-SCRIPT-CORRELATION.md (content type → retention)
  - tools/youtube_analytics/retention_analysis.py (content classifier)
  - tools/youtube_analytics/script_srt_deviation.py (script parser)
  - tools/youtube_analytics/_retention_cache/*.json (actual retention curves)

Usage:
    python -m tools.youtube_analytics.retention_predictor --script PATH
    python -m tools.youtube_analytics.retention_predictor --project PROJECT_SLUG
    python -m tools.youtube_analytics.retention_predictor --script PATH --verbose
    python -m tools.youtube_analytics.retention_predictor --script PATH --output PATH
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

from tools.logging_config import get_logger, setup_logging
from tools.youtube_analytics.retention_analysis import classify_content

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = PROJECT_ROOT / "video-projects" / "_IN_PRODUCTION"
CACHE_DIR = PROJECT_ROOT / "tools" / "youtube_analytics" / "_retention_cache"

# ---------------------------------------------------------------------------
# Empirical retention deltas by content type and position
# From RETENTION-SCRIPT-CORRELATION.md (42 videos, 4200 data points)
# ---------------------------------------------------------------------------

# Overall average deltas (per data point within that content type)
OVERALL_DELTAS = {
    "narration":          -0.00499,
    "quote":              -0.00784,
    "primary_source":     -0.00892,
    "statistic":          -0.00948,
    "modern_relevance":   -0.01007,
    "personal_authority": -0.04404,
    "transition":         -0.00499,   # treat as narration (no separate data)
}

# Position-specific deltas: early (0-33%), mid (33-66%), late (66-100%)
POSITION_DELTAS = {
    "early": {
        "narration":          -0.01131,
        "quote":              -0.01710,
        "primary_source":     -0.02246,
        "modern_relevance":   -0.02846,
        "statistic":          -0.03254,
        "personal_authority": -0.05139,
        "transition":         -0.01131,
    },
    "mid": {
        "personal_authority": -0.00012,
        "narration":          -0.00172,
        "primary_source":     -0.00174,
        "statistic":          -0.00258,
        "quote":              -0.00268,
        "modern_relevance":   -0.00364,
        "transition":         -0.00172,
    },
    "late": {
        "personal_authority": +0.00770,
        "statistic":          +0.00071,
        "quote":              -0.00194,
        "modern_relevance":   -0.00290,
        "primary_source":     -0.00290,
        "narration":          -0.00330,
        "transition":         -0.00330,
    },
}

# Positive rate by content type (% of data points where retention held or gained)
POSITIVE_RATES = {
    "narration":          0.56,
    "quote":              0.54,
    "primary_source":     0.56,
    "statistic":          0.61,
    "modern_relevance":   0.52,
    "personal_authority": 0.22,
    "transition":         0.56,
}

# Average channel retention curve (empirical, from cached data)
# These are absolute retention values at each 1% position
# Channel average is ~29% (from structure-checker-v2: 28.8% average)
# Steep intro drop is universal, then gradual decline
CHANNEL_AVG_CURVE = {
    0: 1.000,
    1: 0.950,
    2: 0.780,
    3: 0.700,
    4: 0.580,
    5: 0.520,
    6: 0.470,
    7: 0.440,
    8: 0.420,
    9: 0.400,
    10: 0.390,
    15: 0.370,
    20: 0.355,
    25: 0.340,
    30: 0.330,
    35: 0.320,
    40: 0.315,
    45: 0.310,
    50: 0.305,
    55: 0.300,
    60: 0.295,
    65: 0.292,
    70: 0.290,
    75: 0.288,
    80: 0.286,
    85: 0.284,
    90: 0.282,
    95: 0.280,
    100: 0.278,
}


# ---------------------------------------------------------------------------
# Script parsing (extended from script_srt_deviation.py)
# ---------------------------------------------------------------------------

# Markdown elements to strip (not spoken aloud)
SCRIPT_STRIP_PATTERNS = [
    r"^\[.*?\]\s*$",             # Full-line B-roll/visual cues
    r"\[B-ROLL:.*?\]",           # Inline B-roll cues
    r"\[VISUAL:.*?\]",           # Visual cues
    r"\[TRANSITION:.*?\]",       # Transition cues
    r"\[Beat\]",                 # Beat markers
    r"\[CTA.*?\]",               # CTA markers
    r"\{.*?\}",                  # Retention triggers
    r"^>.*$",                    # Block quotes (on-screen text, not spoken)
    r"^//.*$",                   # Production notes
    r"^\*\*.*\*\*:?$",          # Bold-only lines (section labels)
    r"^---+$",                   # Horizontal rules
    r"^\|.*\|$",                 # Table rows
    r"^\*[^*].*\*$",             # Italic notes
    r"^\(.*\)\s*$",              # Parenthesized stage directions
]


def _is_header(line: str) -> bool:
    """Check if line is a markdown header."""
    return bool(re.match(r"^#{1,6}\s+", line.strip()))


def _extract_header(line: str) -> str:
    """Extract header text from markdown header line."""
    m = re.match(r"^#{1,6}\s+(.*)", line.strip())
    return m.group(1) if m else line.strip()


def _is_metadata_block(lines: list[str], start: int) -> int:
    """
    Check if we're in a YAML-like metadata block or checklist block.
    Returns the index after the block, or start if not a block.
    """
    if start >= len(lines):
        return start
    line = lines[start].strip()
    # Detect YAML front matter (---)
    if line == "---":
        for i in range(start + 1, len(lines)):
            if lines[i].strip() == "---":
                return i + 1
        return start
    return start


def _should_skip_line(line: str) -> bool:
    """Check if a script line is non-spoken content."""
    stripped = line.strip()
    if not stripped:
        return True
    compiled = [re.compile(p, re.MULTILINE) for p in SCRIPT_STRIP_PATTERNS]
    for pattern in compiled:
        if pattern.match(stripped):
            return True
    # Skip metadata-style lines (checkbox items, key-value pairs at top)
    if re.match(r"^- \[[ x]\]", stripped):
        return True
    if re.match(r"^\*\*[A-Z].*\*\*:", stripped):
        return True
    return False


def _clean_inline_markdown(text: str) -> str:
    """Strip inline markdown formatting from text."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # Italic
    text = re.sub(r'\[B-ROLL:.*?\]', '', text)
    text = re.sub(r'\[VISUAL:.*?\]', '', text)
    text = re.sub(r'\[TRANSITION:.*?\]', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    return text.strip()


def parse_script_with_structure(script_path: Path) -> list[dict]:
    """
    Parse a script markdown file into structured sections.

    Returns list of sections, each containing:
        {
            'header': str,         # Section/act header
            'sentences': [str],    # Spoken sentences
            'line_start': int,     # First line number in original file
            'word_count': int,     # Total words in spoken sentences
        }
    """
    text = script_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Skip YAML front matter
    content_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                content_start = i + 1
                break

    # Headers that indicate metadata sections to skip entirely
    METADATA_HEADERS = {
        "SCRIPT METADATA", "VOICE PATTERNS APPLIED", "DEBUNKING FRAMEWORK",
        "FORMAT TEMPLATE", "STYLE APPROACH", "Script Draft",
        "SCRIPT DRAFT", "FINAL SCRIPT",
    }

    sections = []
    current_header = "INTRO"
    current_sentences = []
    current_line_start = content_start
    in_metadata_section = False

    i = content_start
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for section header
        if _is_header(stripped):
            # Save current section if it has content
            if current_sentences and not in_metadata_section:
                wc = sum(len(s.split()) for s in current_sentences)
                sections.append({
                    "header": current_header,
                    "sentences": current_sentences,
                    "line_start": current_line_start,
                    "word_count": wc,
                })
            current_header = _extract_header(stripped)
            current_sentences = []
            current_line_start = i + 1
            # Check if this is a metadata section to skip
            in_metadata_section = any(
                meta.lower() in current_header.lower()
                for meta in METADATA_HEADERS
            )
            i += 1
            continue

        # Skip metadata sections and non-spoken content
        if in_metadata_section or _should_skip_line(stripped):
            i += 1
            continue

        # Clean and split into sentences
        cleaned = _clean_inline_markdown(stripped)
        if cleaned and len(cleaned) > 5:
            parts = re.split(r'(?<=[.!?])\s+', cleaned)
            for part in parts:
                part = part.strip()
                if part and len(part) > 10:
                    current_sentences.append(part)

        i += 1

    # Don't forget the last section
    if current_sentences and not in_metadata_section:
        wc = sum(len(s.split()) for s in current_sentences)
        sections.append({
            "header": current_header,
            "sentences": current_sentences,
            "line_start": current_line_start,
            "word_count": wc,
        })

    logger.info(
        "Parsed %d sections, %d total sentences from %s",
        len(sections),
        sum(len(s["sentences"]) for s in sections),
        script_path.name,
    )
    return sections


# ---------------------------------------------------------------------------
# Content classification per section
# ---------------------------------------------------------------------------

def classify_section(section: dict) -> list[dict]:
    """
    Classify each sentence in a section.

    Returns list of:
        {'text': str, 'content_type': str, 'word_count': int}
    """
    classified = []
    for sentence in section["sentences"]:
        ctype = classify_content(sentence)
        classified.append({
            "text": sentence,
            "content_type": ctype,
            "word_count": len(sentence.split()),
        })
    return classified


def summarize_section_types(classified: list[dict]) -> dict:
    """
    Summarize content type distribution for a section.

    Returns: {content_type: word_count}
    """
    counts = defaultdict(int)
    for item in classified:
        counts[item["content_type"]] += item["word_count"]
    return dict(counts)


# ---------------------------------------------------------------------------
# Retention curve prediction
# ---------------------------------------------------------------------------

def _get_position_zone(fraction: float) -> str:
    """Map 0.0-1.0 position to early/mid/late zone."""
    if fraction < 0.33:
        return "early"
    elif fraction < 0.66:
        return "mid"
    else:
        return "late"


def _estimate_read_minutes(word_count: int, wpm: int = 160) -> float:
    """Estimate spoken duration in minutes at typical speaking pace."""
    return word_count / wpm


def _get_channel_avg_at(position_pct: int) -> float:
    """Interpolate channel average retention at a given percentage position."""
    if position_pct in CHANNEL_AVG_CURVE:
        return CHANNEL_AVG_CURVE[position_pct]
    # Linear interpolation
    keys = sorted(CHANNEL_AVG_CURVE.keys())
    for i in range(len(keys) - 1):
        if keys[i] <= position_pct <= keys[i + 1]:
            lo, hi = keys[i], keys[i + 1]
            frac = (position_pct - lo) / (hi - lo)
            return CHANNEL_AVG_CURVE[lo] + frac * (CHANNEL_AVG_CURVE[hi] - CHANNEL_AVG_CURVE[lo])
    return CHANNEL_AVG_CURVE[keys[-1]]


def predict_from_file(script_path: str, verbose: bool = False) -> dict:
    """Convenience wrapper: parse a script file and predict retention."""
    sections = parse_script_with_structure(Path(script_path))
    return predict_retention(sections, verbose=verbose)


def predict_from_text(script_text: str, verbose: bool = False) -> dict:
    """Convenience wrapper: parse script text (not file) and predict retention."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script_text)
        f.flush()
        sections = parse_script_with_structure(Path(f.name))
    return predict_retention(sections, verbose=verbose)


def predict_retention(sections: list[dict], verbose: bool = False) -> dict:
    """
    Predict retention curve for a parsed script.

    Args:
        sections: Output from parse_script_with_structure()
        verbose: If True, include per-sentence classifications

    Returns:
        {
            'curve': [(position_pct, predicted_retention), ...],
            'sections': [{header, position_pct, content_summary, predicted_retention, flags}, ...],
            'flags': [{'severity': str, 'message': str, 'section': str, 'position_pct': int}, ...],
            'recommendations': [str, ...],
            'total_words': int,
            'estimated_duration_min': float,
        }
    """
    # Total words → estimate total duration
    total_words = sum(s["word_count"] for s in sections)
    est_duration_min = _estimate_read_minutes(total_words)

    # Account for filming adaptation (44% survival rate from deviation data)
    # Script is ~1.8x longer than final video
    est_filmed_min = est_duration_min / 1.8

    logger.info(
        "Total: %d words, ~%.1f min script, ~%.1f min filmed (44%% survival)",
        total_words, est_duration_min, est_filmed_min,
    )

    # Build per-section analysis
    section_results = []
    curve_points = []  # (position_pct, retention)
    flags = []
    recommendations = []

    # Early return for empty sections
    if not sections:
        return {
            'curve': [],
            'sections': [],
            'flags': [{'severity': 'WARNING', 'message': 'No sections found in script', 'section': '', 'position_pct': 0}],
            'recommendations': ['Script appears empty — no sections could be parsed.'],
            'total_words': 0,
            'estimated_duration_min': 0.0,
        }

    # Track running state
    words_so_far = 0
    last_stat_or_quote_position = 0.0
    narration_streak_words = 0
    has_early_evidence = False
    first_evidence_position = None

    for sec_idx, section in enumerate(sections):
        classified = classify_section(section)
        type_summary = summarize_section_types(classified)
        dominant_type = max(type_summary, key=type_summary.get) if type_summary else "narration"

        # Position of this section in the overall script
        section_midpoint_words = words_so_far + section["word_count"] / 2
        position_frac = section_midpoint_words / total_words if total_words > 0 else 0
        position_pct = int(position_frac * 100)
        zone = _get_position_zone(position_frac)

        # BASE: start from the empirical channel-average curve at this position
        # This captures the universal intro drop and gradual decline
        base_retention = _get_channel_avg_at(position_pct)

        # ADJUSTMENT: content type quality relative to "average" content
        # If this section has better content types than average, predict above avg
        # Narration delta is the baseline (-0.005 overall); compare others to it
        narration_delta = POSITION_DELTAS.get(zone, {}).get("narration", -0.005)

        section_quality_bonus = 0.0
        for item in classified:
            ct = item["content_type"]
            wc = item["word_count"]
            weight = wc / section["word_count"] if section["word_count"] > 0 else 0
            ct_delta = POSITION_DELTAS.get(zone, {}).get(ct, OVERALL_DELTAS.get(ct, -0.005))
            # Positive bonus = this content type is better than narration baseline
            # Negative bonus = worse than narration
            section_quality_bonus += (ct_delta - narration_delta) * weight

        # Scale the bonus by section span (how much of the video this section covers)
        section_span_pct = (section["word_count"] / total_words * 100) if total_words > 0 else 1
        # Scale factor: each content-type advantage/disadvantage compounds over the span
        # Multiply by 2 to make differences more visible in predictions
        cumulative_bonus = section_quality_bonus * section_span_pct * 2.0

        # Predicted retention = channel average + quality adjustment
        current_retention = base_retention + cumulative_bonus

        # Clamp
        current_retention = max(0.05, min(1.0, current_retention))

        # Calculate change from previous section for display
        if curve_points:
            retention_change = current_retention - curve_points[-1][1]
        else:
            retention_change = current_retention - 1.0

        # Record curve point
        curve_points.append((position_pct, round(current_retention, 4)))

        # Track evidence timing
        for item in classified:
            if item["content_type"] in ("quote", "primary_source", "statistic"):
                if first_evidence_position is None:
                    first_evidence_position = position_frac
                if position_frac <= 0.15:
                    has_early_evidence = True
                last_stat_or_quote_position = position_frac

        # Track narration streaks — reset if ANY sentence in section is
        # a pattern interrupt (quote, statistic, primary_source)
        interrupt_types = {"quote", "statistic", "primary_source"}
        has_interrupt = any(
            item["content_type"] in interrupt_types for item in classified
        )
        if has_interrupt:
            narration_streak_words = 0
        else:
            narration_streak_words += section["word_count"]

        # --- FLAG GENERATION ---

        # Flag: large single-section drop
        # Skip flagging the intro zone (first 10%) — all videos lose 15-25% there
        # regardless of content. Only flag if worse than channel average at same position.
        if position_pct > 10 and retention_change < -0.05:
            flags.append({
                "severity": "WARNING",
                "message": f"Predicted {retention_change:+.1%} retention drop in this section "
                           f"(dominant type: {dominant_type})",
                "section": section["header"],
                "position_pct": position_pct,
            })
        elif position_pct <= 10 and current_retention < base_retention - 0.05:
            flags.append({
                "severity": "WARNING",
                "message": f"Intro retention ({current_retention:.1%}) is significantly below "
                           f"channel average ({base_retention:.1%}) at this position. "
                           f"Content type ({dominant_type}) may be hurting the hook.",
                "section": section["header"],
                "position_pct": position_pct,
            })

        # Flag: narration streak > 3 minutes without pattern interrupt
        narration_streak_min = _estimate_read_minutes(narration_streak_words)
        if narration_streak_min > 3.0:
            flags.append({
                "severity": "WARNING",
                "message": f"{narration_streak_min:.1f} min of pure narration without a "
                           f"pattern interrupt (quote/statistic/primary source)",
                "section": section["header"],
                "position_pct": position_pct,
            })

        # Flag: modern relevance after minute 8 (may disrupt flow)
        section_time_min = _estimate_read_minutes(int(section_midpoint_words))
        if dominant_type == "modern_relevance" and section_time_min > 8:
            flags.append({
                "severity": "CHECK",
                "message": "Modern relevance bridge after minute 8 — may disrupt narrative flow. "
                           "Consider weaving into narration instead.",
                "section": section["header"],
                "position_pct": position_pct,
            })

        # Flag: no stats/quotes for >4 minutes
        if position_frac - last_stat_or_quote_position > 0.25:  # ~25% of video
            evidence_gap_min = _estimate_read_minutes(
                int((position_frac - last_stat_or_quote_position) * total_words)
            )
            if evidence_gap_min > 4.0:
                flags.append({
                    "severity": "WARNING",
                    "message": f"No statistics, quotes, or primary sources for ~{evidence_gap_min:.1f} min. "
                               f"Losing the channel's retention advantage.",
                    "section": section["header"],
                    "position_pct": position_pct,
                })
                last_stat_or_quote_position = position_frac  # Don't re-flag

        # Flag: personal_authority in early zone (intro confound)
        if zone == "early" and dominant_type == "personal_authority":
            flags.append({
                "severity": "CHECK",
                "message": "personal_authority ('I read...') in the first third. "
                           "Empirically -0.051 delta (worst in early zone). "
                           "Move to mid-video where it's essentially flat (-0.0001).",
                "section": section["header"],
                "position_pct": position_pct,
            })

        # Good flag: evidence in first 2 minutes
        if section_time_min <= 2 and dominant_type in ("statistic", "quote", "primary_source"):
            flags.append({
                "severity": "GOOD",
                "message": f"Early {dominant_type} — good for retention (high positive rate).",
                "section": section["header"],
                "position_pct": position_pct,
            })

        # Good flag: late statistics
        if zone == "late" and dominant_type == "statistic":
            flags.append({
                "severity": "GOOD",
                "message": "Late statistics — empirically the ONLY content type that gains "
                           "viewers late (+0.001 delta). Excellent placement.",
                "section": section["header"],
                "position_pct": position_pct,
            })

        section_result = {
            "header": section["header"],
            "position_pct": position_pct,
            "word_count": section["word_count"],
            "estimated_minutes": round(_estimate_read_minutes(section["word_count"]), 1),
            "content_summary": type_summary,
            "dominant_type": dominant_type,
            "predicted_retention": round(current_retention, 4),
            "retention_change": round(retention_change, 4),
            "zone": zone,
        }

        if verbose:
            section_result["sentences"] = [
                {"text": c["text"][:100], "type": c["content_type"], "words": c["word_count"]}
                for c in classified
            ]

        section_results.append(section_result)
        words_so_far += section["word_count"]

    # Post-analysis recommendations
    if not has_early_evidence and first_evidence_position is not None:
        first_ev_min = _estimate_read_minutes(int(first_evidence_position * total_words))
        recommendations.append(
            f"First evidence (quote/stat/source) appears at ~{first_ev_min:.1f} min "
            f"({first_evidence_position:.0%} position). Move a specific number, quote, "
            f"or source into the first 90 seconds for retention."
        )

    if first_evidence_position is None:
        recommendations.append(
            "WARNING: No quotes, statistics, or primary sources detected in the script. "
            "This channel's competitive advantage is real quotes with page numbers."
        )

    # Check content type diversity
    all_types = defaultdict(int)
    for sr in section_results:
        for ct, wc in sr["content_summary"].items():
            all_types[ct] += wc
    narration_pct = all_types.get("narration", 0) / total_words if total_words else 0
    if narration_pct > 0.75:
        recommendations.append(
            f"Script is {narration_pct:.0%} narration. Add more quotes, statistics, "
            f"and primary sources to break up the narration and anchor viewer attention."
        )

    stat_pct = all_types.get("statistic", 0) / total_words if total_words else 0
    if stat_pct < 0.05:
        recommendations.append(
            "Statistics make up <5% of the script. Stats have the highest positive rate "
            "(61%) of any content type. Add specific numbers throughout."
        )

    # Check for late statistics (the retention gold)
    late_stats = any(
        sr["zone"] == "late" and "statistic" in sr["content_summary"]
        for sr in section_results
    )
    if not late_stats:
        recommendations.append(
            "No statistics in the final third. Late stats are the ONLY content type "
            "that gains viewers (+0.001 delta). Save a shocking number for the closing."
        )

    # Final predicted retention
    final_retention = current_retention
    channel_avg_final = _get_channel_avg_at(100)

    if final_retention > channel_avg_final + 0.03:
        recommendations.append(
            f"Predicted final retention ({final_retention:.1%}) is above channel average "
            f"({channel_avg_final:.1%}). Good script structure."
        )
    elif final_retention < channel_avg_final - 0.03:
        recommendations.append(
            f"Predicted final retention ({final_retention:.1%}) is below channel average "
            f"({channel_avg_final:.1%}). Consider restructuring flagged sections."
        )

    return {
        "curve": curve_points,
        "sections": section_results,
        "flags": flags,
        "recommendations": recommendations,
        "total_words": total_words,
        "estimated_script_duration_min": round(est_duration_min, 1),
        "estimated_filmed_duration_min": round(est_filmed_min, 1),
        "predicted_final_retention": round(final_retention, 4),
        "channel_avg_final_retention": channel_avg_final,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _ascii_chart(curve: list[tuple], channel_avg: dict = None, width: int = 50) -> str:
    """Generate an ASCII retention curve chart."""
    lines = []
    lines.append("```")
    lines.append("Retention %  |  Predicted curve vs channel average")
    lines.append("             |")

    # Build sparse curve at 10% intervals
    # Collect curve points closest to each 10% mark
    curve_at_10 = {}
    for pos, ret in curve:
        bucket = round(pos / 10) * 10
        if bucket not in curve_at_10 or abs(pos - bucket) < abs(curve_at_10[bucket][0] - bucket):
            curve_at_10[bucket] = (pos, ret)

    max_ret = 1.0
    for pct in range(0, 101, 10):
        predicted = curve_at_10.get(pct, (pct, None))
        pred_val = predicted[1] if predicted[1] is not None else _get_channel_avg_at(pct)
        avg_val = _get_channel_avg_at(pct)

        # Scale to chart width
        pred_bar = int(pred_val / max_ret * width)
        avg_bar = int(avg_val / max_ret * width)

        # Build the bar
        bar = list(" " * (width + 2))
        # Place channel average marker
        if avg_bar < len(bar):
            bar[avg_bar] = "·"
        # Place predicted marker (overwrites avg if same position)
        if pred_bar < len(bar):
            bar[pred_bar] = "█"

        # Fill predicted bar
        bar_str = ""
        for j in range(width + 2):
            if j < pred_bar:
                bar_str += "▓"
            elif j == pred_bar:
                bar_str += "█"
            elif j == avg_bar:
                bar_str += "·"
            else:
                bar_str += " "

        label = f"{pct:>3}% ({pred_val:>5.1%})"
        lines.append(f"  {label} |{bar_str}")

    lines.append("             |" + "─" * (width + 2))
    lines.append("             | ▓█ = predicted   · = channel avg")
    lines.append("```")
    return "\n".join(lines)


def generate_report(result: dict, script_path: Path, verbose: bool = False) -> str:
    """Generate a markdown report from prediction results."""
    lines = []

    lines.append("# Retention Prediction Report")
    lines.append("")
    lines.append(f"**Script:** `{script_path.name}`")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Total words:** {result['total_words']:,}")
    lines.append(f"**Estimated script read-aloud:** {result['estimated_script_duration_min']:.1f} min")
    lines.append(f"**Estimated filmed duration:** {result['estimated_filmed_duration_min']:.1f} min "
                 f"(44% script survival rate)")
    lines.append(f"**Predicted final retention:** {result['predicted_final_retention']:.1%}")
    lines.append(f"**Channel average final retention:** {result['channel_avg_final_retention']:.1%}")
    lines.append("")

    # Verdict
    diff = result["predicted_final_retention"] - result["channel_avg_final_retention"]
    if diff > 0.03:
        lines.append("> **Verdict:** Script structure is ABOVE channel average. Good to proceed.")
    elif diff > -0.03:
        lines.append("> **Verdict:** Script structure is IN LINE with channel average.")
    else:
        lines.append("> **Verdict:** Script structure is BELOW channel average. Review flagged sections.")
    lines.append("")

    lines.append("---")
    lines.append("")

    # 1. Predicted retention curve
    lines.append("## 1. Predicted Retention Curve")
    lines.append("")
    lines.append(_ascii_chart(result["curve"]))
    lines.append("")

    # 2. Section-by-section analysis
    lines.append("## 2. Section-by-Section Analysis")
    lines.append("")
    lines.append("| # | Section | Position | Words | ~Min | Dominant Type | Retention | Change |")
    lines.append("|---|---------|----------|------:|-----:|---------------|----------:|-------:|")

    for i, sec in enumerate(result["sections"], 1):
        change_str = f"{sec['retention_change']:+.2%}"
        lines.append(
            f"| {i} | {sec['header'][:40]} | {sec['position_pct']}% ({sec['zone']}) "
            f"| {sec['word_count']} | {sec['estimated_minutes']} "
            f"| {sec['dominant_type']} | {sec['predicted_retention']:.1%} | {change_str} |"
        )
    lines.append("")

    # Content type breakdown per section (detail)
    if verbose:
        lines.append("### Detailed Content Type Breakdown")
        lines.append("")
        for i, sec in enumerate(result["sections"], 1):
            lines.append(f"**{i}. {sec['header']}** (position {sec['position_pct']}%)")
            summary = sec["content_summary"]
            total_wc = sec["word_count"]
            for ct, wc in sorted(summary.items(), key=lambda x: -x[1]):
                pct = wc / total_wc * 100 if total_wc > 0 else 0
                lines.append(f"  - {ct}: {wc} words ({pct:.0f}%)")
            if "sentences" in sec:
                lines.append("")
                lines.append("  | Sentence | Type |")
                lines.append("  |----------|------|")
                for s in sec["sentences"]:
                    lines.append(f"  | {s['text'][:80]}{'...' if len(s['text']) > 80 else ''} | {s['type']} |")
            lines.append("")

    # 3. Dropout risk flags
    lines.append("## 3. Dropout Risk Flags")
    lines.append("")

    severity_order = {"WARNING": 0, "CHECK": 1, "GOOD": 2}
    sorted_flags = sorted(result["flags"], key=lambda f: severity_order.get(f["severity"], 9))

    warnings = [f for f in sorted_flags if f["severity"] == "WARNING"]
    checks = [f for f in sorted_flags if f["severity"] == "CHECK"]
    goods = [f for f in sorted_flags if f["severity"] == "GOOD"]

    if warnings:
        lines.append("### Warnings (likely dropout)")
        lines.append("")
        for f in warnings:
            lines.append(f"- **{f['section']}** ({f['position_pct']}%): {f['message']}")
        lines.append("")

    if checks:
        lines.append("### Checks (review recommended)")
        lines.append("")
        for f in checks:
            lines.append(f"- **{f['section']}** ({f['position_pct']}%): {f['message']}")
        lines.append("")

    if goods:
        lines.append("### Positive signals")
        lines.append("")
        for f in goods:
            lines.append(f"- **{f['section']}** ({f['position_pct']}%): {f['message']}")
        lines.append("")

    if not result["flags"]:
        lines.append("No flags generated.")
        lines.append("")

    # 4. Recommendations
    lines.append("## 4. Recommendations")
    lines.append("")
    for i, rec in enumerate(result["recommendations"], 1):
        lines.append(f"{i}. {rec}")
    if not result["recommendations"]:
        lines.append("No specific recommendations — script structure looks solid.")
    lines.append("")

    # 5. Comparison to channel average
    lines.append("## 5. Comparison to Channel Average")
    lines.append("")
    lines.append("| Position | Predicted | Channel Avg | Difference |")
    lines.append("|----------|----------:|------------:|-----------:|")

    for pct in range(0, 101, 10):
        # Find closest curve point
        closest = None
        for pos, ret in result["curve"]:
            if closest is None or abs(pos - pct) < abs(closest[0] - pct):
                closest = (pos, ret)
        pred = closest[1] if closest else _get_channel_avg_at(pct)
        avg = _get_channel_avg_at(pct)
        diff_val = pred - avg
        lines.append(f"| {pct}% | {pred:.1%} | {avg:.1%} | {diff_val:+.1%} |")
    lines.append("")

    # Content type summary
    lines.append("## 6. Content Type Distribution")
    lines.append("")
    all_types = defaultdict(int)
    for sec in result["sections"]:
        for ct, wc in sec["content_summary"].items():
            all_types[ct] += wc
    total = result["total_words"]
    lines.append("| Content Type | Words | % of Script | Empirical Delta | Positive Rate |")
    lines.append("|-------------|------:|------------:|--------------:|--------------:|")
    for ct, wc in sorted(all_types.items(), key=lambda x: -x[1]):
        pct = wc / total * 100 if total > 0 else 0
        delta = OVERALL_DELTAS.get(ct, -0.005)
        pos_rate = POSITIVE_RATES.get(ct, 0.5)
        lines.append(f"| {ct} | {wc:,} | {pct:.1f}% | {delta:+.5f} | {pos_rate:.0%} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Predictions based on empirical data from 42 videos and 4,200 retention data points. "
                 "Actual retention depends on filming execution, thumbnail CTR, and audience mix.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _find_script_for_project(slug: str) -> Path | None:
    """Find the script file for a project slug."""
    project_dir = None
    for d in PROJECTS_DIR.iterdir():
        if d.is_dir() and slug.lower() in d.name.lower():
            project_dir = d
            break

    if not project_dir:
        logger.error("Project not found matching slug: %s", slug)
        return None

    # Try common script names
    candidates = [
        project_dir / "02-SCRIPT-DRAFT.md",
        project_dir / "SCRIPT.md",
        project_dir / "FINAL-SCRIPT.md",
    ]
    for c in candidates:
        if c.exists():
            return c

    # Glob for any script-like file
    for md in project_dir.glob("*SCRIPT*.md"):
        return md

    logger.error("No script file found in %s", project_dir)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Predict retention curve for a History vs Hype script"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--script", type=str, help="Path to script markdown file")
    group.add_argument("--project", type=str, help="Project slug (e.g. 43-india-pakistan)")
    parser.add_argument("--verbose", action="store_true", help="Include per-sentence classification")
    parser.add_argument("--quiet", action="store_true", help="Suppress info messages")
    parser.add_argument("--output", type=str, help="Output path for report (default: same folder as script)")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    # Resolve script path
    if args.script:
        script_path = Path(args.script).resolve()
    else:
        script_path = _find_script_for_project(args.project)

    if not script_path or not script_path.exists():
        logger.error("Script not found: %s", script_path)
        sys.exit(1)

    logger.info("Analyzing script: %s", script_path)

    # Parse
    sections = parse_script_with_structure(script_path)
    if not sections:
        logger.error("No sections parsed from script")
        sys.exit(1)

    # Predict
    result = predict_retention(sections, verbose=args.verbose)

    # Generate report
    report = generate_report(result, script_path, verbose=args.verbose)

    # Write output
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = script_path.parent / "RETENTION-PREDICTION.md"

    output_path.write_text(report, encoding="utf-8")
    logger.info("Report written to %s", output_path)

    # Print summary to stdout
    print(f"\n{'='*60}")
    print(f"RETENTION PREDICTION: {script_path.name}")
    print(f"{'='*60}")
    print(f"Words: {result['total_words']:,}")
    print(f"Script duration: ~{result['estimated_script_duration_min']:.1f} min")
    print(f"Filmed duration: ~{result['estimated_filmed_duration_min']:.1f} min")
    print(f"Predicted final retention: {result['predicted_final_retention']:.1%}")
    print(f"Channel average: {result['channel_avg_final_retention']:.1%}")

    n_warnings = sum(1 for f in result["flags"] if f["severity"] == "WARNING")
    n_checks = sum(1 for f in result["flags"] if f["severity"] == "CHECK")
    n_goods = sum(1 for f in result["flags"] if f["severity"] == "GOOD")
    print(f"\nFlags: {n_warnings} warnings, {n_checks} checks, {n_goods} positive")

    if result["recommendations"]:
        print(f"\nTop recommendations:")
        for rec in result["recommendations"][:3]:
            print(f"  - {rec}")

    print(f"\nFull report: {output_path}")


if __name__ == "__main__":
    main()
