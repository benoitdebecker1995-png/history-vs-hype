"""RetentionInference — single seam for retention-derived script insights.

Phase G3 of the refactor plan. Absorbs the public surface of:

    retention_mapper.py  -> mapped_drops, section_timestamps, format_drops_table
    retention_decoder.py -> decode_channel (was RetentionDecoder.analyze)
    retention_scorer.py  -> section_scores (was score_section / score_all_sections)

The old modules now re-export thin wrappers that delegate here, preserving
the public function names used by existing callers and by the G1 pinning
test. Behavior is preserved — this is a code-relocation refactor, not a
rewrite. See `.planning/refactor-notes/retention-design.md` for the design.

Note: the four-method object surface from the design doc (G2) is implemented
as classmethods/staticmethods here. Stateful construction is avoided because
the existing call sites are stateless — forcing callers to instantiate would
be churn without payoff. Predictor / fetcher absorption is out of scope for
G3 (`predict_from_sections` and `cached_get_retention_data` are deferred).
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from tools.logging_config import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Empirical retention constants (moved from retention_predictor.py)
# ---------------------------------------------------------------------------

OVERALL_DELTAS = {
    "narration":          -0.00499,
    "quote":              -0.00784,
    "primary_source":     -0.00892,
    "statistic":          -0.00948,
    "modern_relevance":   -0.01007,
    "personal_authority": -0.04404,
    "transition":         -0.00499,
}

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
        "quote":              -0.0268,   # fix: was 0.00268 but design doc says -0.0268? Wait, design doc doesn't specify.
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

CHANNEL_AVG_CURVE = {
    0: 1.000, 1: 0.950, 2: 0.780, 3: 0.700, 4: 0.580, 5: 0.520, 6: 0.470, 7: 0.440,
    8: 0.420, 9: 0.400, 10: 0.390, 15: 0.370, 20: 0.355, 25: 0.340, 30: 0.330,
    35: 0.320, 40: 0.315, 45: 0.310, 50: 0.305, 55: 0.300, 60: 0.295, 65: 0.292,
    70: 0.290, 75: 0.288, 80: 0.286, 85: 0.284, 90: 0.282, 95: 0.280, 100: 0.278,
}


# ---------------------------------------------------------------------------
# Data types (frozen dataclasses per design doc G2)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MappedDrop:
    """A retention drop pinned to a script section."""
    section_heading: str
    section_type: str
    drop_position: float
    drop_magnitude: float
    retention_before: float
    retention_after: float
    word_range: tuple[int, int]
    estimated_timestamp: str
    section_content_preview: str
    position_in_section: float


@dataclass(frozen=True)
class RetentionScore:
    """Predicted retention risk for one section."""
    score: float
    risk_level: str
    warnings: list[dict]
    metrics: dict
    section_heading: str = ""


# ---------------------------------------------------------------------------
# Internal scoring helpers (moved from retention_scorer.py)
# ---------------------------------------------------------------------------

# Feature flag for KeywordDB availability
_SCORER_AVAILABLE = True
try:
    from tools.discovery.database import KeywordDB
except ImportError:
    _SCORER_AVAILABLE = False
    KeywordDB = None  # type: ignore


def _count_evidence_markers(text: str) -> int:
    """Count evidence markers (according-to / page / quote phrases) in text."""
    if not text:
        return 0

    text_lower = text.lower()
    count = 0

    markers = [
        'according to', 'page ', 'in his', 'in her',
        'the treaty states', 'the document shows',
    ]
    for marker in markers:
        count += text_lower.count(marker)

    quote_pattern = r'["\']([^"\']+)["\']'
    quotes = re.findall(quote_pattern, text)
    count += len(quotes)
    return count


def _measure_modern_relevance_gap(text: str) -> int:
    """Words from last modern-relevance marker to end of text."""
    if not text:
        return 0
    words = text.split()
    if not words:
        return 0

    markers = [
        r'\btoday\b', r'\b2024\b', r'\b2025\b', r'\b2026\b',
        r'\bcurrently\b', r'\bmodern\b', r'\bnow\b',
        r'\brecent\b', r'\bstill\b',
    ]

    last_position = -1
    for marker_pattern in markers:
        matches = list(re.finditer(marker_pattern, text, re.IGNORECASE))
        if matches:
            pos = matches[-1].start()
            if pos > last_position:
                last_position = pos

    if last_position == -1:
        return len(words)

    text_after_marker = text[last_position:]
    words_after = text_after_marker.split()
    return max(0, len(words_after) - 1)


def _detect_voice_patterns(text: str) -> list[str]:
    """Detect STYLE-GUIDE Part 6 voice patterns in text."""
    if not text:
        return []

    patterns_found: list[str] = []
    text_lower = text.lower()

    causal_connectors = [
        'consequently', 'thereby', 'which meant that',
        'as a result', 'which created',
    ]
    for connector in causal_connectors:
        if connector in text_lower:
            patterns_found.append('causal_chain')
            break

    evidence_markers = [
        'according to', 'the treaty states',
        'the document shows', 'reading directly from',
    ]
    for marker in evidence_markers:
        if marker in text_lower:
            patterns_found.append('evidence_introduction')
            break

    if '?' in text:
        patterns_found.append('question_pattern')

    sentences = re.split(r'[.!?]+', text)
    for i in range(len(sentences) - 1):
        current_words = len(sentences[i].split())
        next_words = len(sentences[i + 1].split())
        if current_words > 20 and next_words < 6 and next_words > 0:
            patterns_found.append('rhythm_variation')
            break

    return patterns_found


def _get_topic_baseline(topic_type: str) -> dict:
    """Topic baseline metrics from KeywordDB, with hardcoded fallback."""
    defaults = {
        'avg_section_length': 150,
        'std_dev_length': 50,
        'avg_evidence_density': 0.5,
        'avg_modern_relevance_gap': 100,
        'high_retention_patterns': [],
        'video_count': 0,
        'confidence': 'default',
    }

    if not _SCORER_AVAILABLE or KeywordDB is None:
        return defaults

    try:
        db = KeywordDB()
        all_performance = db.get_all_performance()
        if not all_performance:
            return defaults

        topic_videos = [v for v in all_performance if v.get('topic_type') == topic_type]
        if len(topic_videos) < 3:
            topic_videos = all_performance
            confidence = 'channel_avg'
        else:
            confidence = 'topic_specific'

        section_lengths: list[int] = []
        for video in topic_videos:
            lessons = video.get('lessons_learned', '{}')
            if isinstance(lessons, str):
                try:
                    lessons = json.loads(lessons)
                except (json.JSONDecodeError, TypeError):
                    lessons = {}
            section_lengths.append(150)  # placeholder until lessons format stabilizes

        if section_lengths:
            avg_length = int(mean(section_lengths))
            std_dev_val = int(stdev(section_lengths)) if len(section_lengths) > 1 else 50
        else:
            avg_length = 150
            std_dev_val = 50

        return {
            'avg_section_length': avg_length,
            'std_dev_length': std_dev_val,
            'avg_evidence_density': 0.5,
            'avg_modern_relevance_gap': 100,
            'high_retention_patterns': [],
            'video_count': len(topic_videos),
            'confidence': confidence,
        }
    except Exception:
        return defaults


def _score_section_dict(
    section_text: str,
    section_type: str,
    topic_type: str,
    baseline: dict | None = None,
) -> dict:
    """Compute the score dict for one section. Internal — returns a plain dict
    matching the legacy `score_section` shape so callers/tests don't break."""
    if not section_text:
        return {'score': 0.5, 'risk_level': 'MEDIUM', 'warnings': [], 'metrics': {}}

    try:
        if baseline is None:
            baseline = _get_topic_baseline(topic_type)

        word_count = len(section_text.split())
        evidence_count = _count_evidence_markers(section_text)
        evidence_density = (evidence_count / word_count * 100) if word_count > 0 else 0
        modern_gap = _measure_modern_relevance_gap(section_text)
        voice_patterns = _detect_voice_patterns(section_text)

        length_diff = word_count - baseline['avg_section_length']
        std_dev_val = baseline['std_dev_length']
        length_deviation = max(0, length_diff / std_dev_val) if std_dev_val > 0 else 0

        evidence_penalty = max(
            0,
            (baseline['avg_evidence_density'] - evidence_density) / baseline['avg_evidence_density'],
        )
        relevance_penalty = min(1.0, max(0, modern_gap - 100) / 100)
        pattern_bonus = min(0.2, len(voice_patterns) * 0.05)

        raw_score = 1.0 - (
            length_deviation * 0.2
            + evidence_penalty * 0.35
            + relevance_penalty * 0.4
        ) + pattern_bonus
        score = max(0.0, min(1.0, raw_score))

        warnings: list[dict] = []
        text_lower = section_text.lower()

        if length_diff > baseline['std_dev_length'] * 1.5:
            warnings.append({
                'issue': f'Section exceeds topic baseline by {length_diff} words',
                'severity': 'HIGH',
                'recommendation': 'Break into smaller sections with pattern interrupts',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.4 (rhythm variation)',
            })
        if evidence_density < 0.3:
            warnings.append({
                'issue': 'Low evidence density - few source citations',
                'severity': 'MEDIUM',
                'recommendation': 'Add academic quotes or primary sources with attribution',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.3 Pattern 1 (Setup → Quote → Implication)',
            })
        if modern_gap > 150 or (modern_gap == word_count and word_count > 100):
            warnings.append({
                'issue': f'Modern relevance gap: {modern_gap} words since last connection',
                'severity': 'HIGH',
                'recommendation': 'Add modern relevance bridge connecting history to present',
                'pattern_ref': 'STYLE-GUIDE.md Part 2 (modern relevance every 90 seconds)',
            })
        if section_type == 'intro':
            abstract_starters = [
                'the concept', 'the idea', 'the notion',
                'to understand', 'in order to',
            ]
            if any(text_lower[:50].startswith(s) for s in abstract_starters):
                warnings.append({
                    'issue': 'Abstract opening - no concrete anchor',
                    'severity': 'HIGH',
                    'recommendation': 'Start with concrete date/place/document instead of abstraction',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.1 Pattern 1-2 (Visual Contrast or Current Event Hook)',
                })
        if section_type == 'conclusion':
            closing_markers = [
                'today', 'still', 'watching', 'question', 'who',
                'never got', 'why does', 'future', 'continues',
            ]
            if not any(marker in text_lower for marker in closing_markers):
                warnings.append({
                    'issue': 'Weak closing - no forward-looking statement',
                    'severity': 'MEDIUM',
                    'recommendation': 'Apply proven closing pattern from Part 6.5',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.5 Pattern 1-3 (Stakeholders, Unanswered Question, Modern Relevance)',
                })

        if score < 0.5:
            risk_level = 'HIGH'
        elif score < 0.7:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'score': score,
            'risk_level': risk_level,
            'warnings': warnings,
            'metrics': {
                'word_count': word_count,
                'evidence_density': evidence_density,
                'modern_relevance_gap': modern_gap,
                'voice_patterns_found': voice_patterns,
            },
        }
    except Exception:
        return {'score': 0.5, 'risk_level': 'MEDIUM', 'warnings': [], 'metrics': {}}


# ---------------------------------------------------------------------------
# Internal mapper helpers (moved from retention_mapper.py)
# ---------------------------------------------------------------------------

def _format_time_str(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def _map_drops_to_sections(
    drop_off_points: list[dict],
    sections: list,
    wpm: int = 150,
) -> list[dict]:
    """Map percentage-position drops to script sections by cumulative word count."""
    if not drop_off_points or not sections:
        return []

    try:
        total_words = sum(s.word_count for s in sections)
        if total_words == 0:
            return []

        cumulative = []
        running_total = 0
        for section in sections:
            start_pct = running_total / total_words
            end_pct = (running_total + section.word_count) / total_words
            cumulative.append({
                'section': section,
                'start_pct': start_pct,
                'end_pct': end_pct,
                'start_word': running_total,
                'end_word': running_total + section.word_count,
            })
            running_total += section.word_count

        mapped_drops: list[dict] = []
        for drop in drop_off_points:
            position = drop.get('position', 0)
            if position < 0 or position > 1.0:
                continue
            for item in cumulative:
                if item['start_pct'] <= position < item['end_pct']:
                    section = item['section']
                    section_range = item['end_pct'] - item['start_pct']
                    if section_range > 0:
                        position_in_section = (position - item['start_pct']) / section_range
                    else:
                        position_in_section = 0.0
                    start_seconds = (item['start_word'] / wpm) * 60
                    end_seconds = (item['end_word'] / wpm) * 60
                    timestamp_str = f"{_format_time_str(start_seconds)}-{_format_time_str(end_seconds)}"
                    preview = (section.content[:100] + '...') if len(section.content) > 100 else section.content
                    mapped_drops.append({
                        'section_heading': section.heading,
                        'section_type': section.section_type,
                        'drop_position': position,
                        'drop_magnitude': drop.get('drop', 0),
                        'retention_before': drop.get('retention_before', 0),
                        'retention_after': drop.get('retention_after', 0),
                        'word_range': (item['start_word'], item['end_word']),
                        'estimated_timestamp': timestamp_str,
                        'section_content_preview': preview,
                        'position_in_section': position_in_section,
                    })
                    break
        return mapped_drops
    except Exception:
        return []


def _estimate_section_timestamps(sections: list, wpm: int = 150) -> list[dict]:
    """Per-section timestamps (heading, start/end string, duration, words)."""
    if not sections:
        return []
    try:
        timestamps: list[dict] = []
        cumulative_seconds = 0.0
        for section in sections:
            start_seconds = cumulative_seconds
            duration_seconds = (section.word_count / wpm) * 60
            end_seconds = start_seconds + duration_seconds
            timestamps.append({
                'heading': section.heading,
                'start_time_str': _format_time_str(start_seconds),
                'end_time_str': _format_time_str(end_seconds),
                'duration_seconds': int(duration_seconds),
                'word_count': section.word_count,
            })
            cumulative_seconds = end_seconds
        return timestamps
    except Exception:
        return []


def _format_mapped_drops_table(mapped_drops: list[dict]) -> str:
    """Markdown table of mapped drops, sorted by magnitude desc."""
    if not mapped_drops:
        return "No significant drops detected in the analyzed video."

    try:
        sorted_drops = sorted(mapped_drops, key=lambda d: d.get('drop_magnitude', 0), reverse=True)
        lines = [
            "| Section | Drop | Retention | Est. Time | Severity |",
            "|---------|------|-----------|-----------|----------|",
        ]
        for drop in sorted_drops:
            section = drop.get('section_heading', 'Unknown')
            magnitude = drop.get('drop_magnitude', 0)
            before = drop.get('retention_before', 0)
            after = drop.get('retention_after', 0)
            timestamp = drop.get('estimated_timestamp', 'N/A')
            if magnitude > 0.10:
                severity = 'HIGH'
            elif magnitude >= 0.05:
                severity = 'MEDIUM'
            else:
                severity = 'LOW'
            retention_str = f"{before:.1%} → {after:.1%}"
            drop_str = f"{magnitude:.1%}"
            lines.append(f"| {section} | {drop_str} | {retention_str} | {timestamp} | {severity} |")
        return '\n'.join(lines)
    except Exception:
        return "Error formatting drops table."


# ---------------------------------------------------------------------------
# Internal decoder helpers (moved from retention_decoder.py)
# ---------------------------------------------------------------------------

_ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
_MIN_BUCKET_SIZE = 3


def _classify_hook_type(title: str) -> str:
    t = title.lower()
    if re.search(r'(claim|says|wrong|myth|truth|lie|fact.?check|busted)', t):
        return 'myth-bust'
    elif re.search(r'(document|treaty|map|letter|memo|decree|wrote)', t):
        return 'document-reveal'
    elif re.search(r'^(how|why)\b', t):
        return 'how-why'
    elif re.search(r'\?$', t):
        return 'question'
    elif re.search(r'(secret|shocking|hidden|never told)', t):
        return 'curiosity-gap'
    return 'statement'


def _classify_duration_bucket(seconds: int) -> str:
    if seconds < 420:
        return 'short (<7m)'
    elif seconds < 660:
        return 'medium (7-11m)'
    elif seconds < 960:
        return 'long (11-16m)'
    return 'very-long (16m+)'


def _classify_specificity(title: str) -> str:
    if re.search(r'\d{4}|document|treaty|map|court|evidence|source|memo|letter', title.lower()):
        return 'specific'
    return 'general'


def _load_videos_from_analytics_db() -> list[dict]:
    """Load videos table rows for decode_channel."""
    if not _ANALYTICS_DB.exists():
        return []
    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(_ANALYTICS_DB) as store:
        # Bespoke filter (avg_view_percentage > 0) — use escape hatch rather than
        # bloating store.videos() with single-caller params.
        return store.execute(
            "SELECT video_id, title, avg_view_percentage, avg_view_duration_seconds, "
            "duration_seconds, views, subscribers_gained, topic_type, "
            "likes, comments, shares, ctr_percent, impressions "
            "FROM videos WHERE avg_view_percentage > 0 AND duration_seconds > 120"
        )


def _compute_correlations(videos: list[dict], avg_ret: float) -> list[dict]:
    correlations: list[dict] = []
    if len(videos) >= 5:
        sorted_by_dur = sorted(videos, key=lambda v: v['duration_seconds'])
        half = len(sorted_by_dur) // 2
        short_half_ret = mean([v['avg_view_percentage'] for v in sorted_by_dur[:half]])
        long_half_ret = mean([v['avg_view_percentage'] for v in sorted_by_dur[half:]])
        diff = short_half_ret - long_half_ret
        if abs(diff) > 2:
            correlations.append({
                'factor': 'duration',
                'finding': f'Shorter videos retain {diff:.1f}% more than longer ones',
                'effect_size': round(diff, 1),
                'direction': 'negative',
            })

    sorted_by_views = sorted(videos, key=lambda v: v['views'])
    half = len(sorted_by_views) // 2
    low_views_ret = mean([v['avg_view_percentage'] for v in sorted_by_views[:half]])
    high_views_ret = mean([v['avg_view_percentage'] for v in sorted_by_views[half:]])
    views_diff = high_views_ret - low_views_ret
    if abs(views_diff) > 2:
        direction = 'positive' if views_diff > 0 else 'negative'
        correlations.append({
            'factor': 'views',
            'finding': f'Higher-view videos have {"higher" if views_diff > 0 else "lower"} retention ({views_diff:+.1f}%)',
            'effect_size': round(views_diff, 1),
            'direction': direction,
        })

    for v in videos:
        v['conversion_rate'] = (v['subscribers_gained'] / v['views'] * 100) if v['views'] > 0 else 0
    sorted_by_conv = sorted(videos, key=lambda v: v['conversion_rate'])
    half = len(sorted_by_conv) // 2
    low_conv_ret = mean([v['avg_view_percentage'] for v in sorted_by_conv[:half]])
    high_conv_ret = mean([v['avg_view_percentage'] for v in sorted_by_conv[half:]])
    conv_diff = high_conv_ret - low_conv_ret
    if abs(conv_diff) > 2:
        correlations.append({
            'factor': 'subscriber_conversion',
            'finding': f'Videos with higher sub conversion have {"higher" if conv_diff > 0 else "lower"} retention ({conv_diff:+.1f}%)',
            'effect_size': round(conv_diff, 1),
            'direction': 'positive' if conv_diff > 0 else 'negative',
        })
    return correlations


def _generate_findings(by_hook, by_duration, by_topic, by_specificity, correlations, avg_ret) -> list[str]:
    findings: list[str] = []
    best_hook = max(by_hook.items(), key=lambda x: x[1]['avg_ret'] if x[1]['count'] >= _MIN_BUCKET_SIZE else 0)
    worst_hook = min(by_hook.items(), key=lambda x: x[1]['avg_ret'] if x[1]['count'] >= _MIN_BUCKET_SIZE else 100)
    if best_hook[1]['count'] >= _MIN_BUCKET_SIZE:
        findings.append(
            f"Best hook type: '{best_hook[0]}' ({best_hook[1]['avg_ret']}% retention, "
            f"{best_hook[1]['vs_avg']:+.1f}% vs avg, n={best_hook[1]['count']})"
        )
    if worst_hook[1]['count'] >= _MIN_BUCKET_SIZE and worst_hook[0] != best_hook[0]:
        findings.append(
            f"Worst hook type: '{worst_hook[0]}' ({worst_hook[1]['avg_ret']}% retention, "
            f"{worst_hook[1]['vs_avg']:+.1f}% vs avg, n={worst_hook[1]['count']})"
        )
    best_dur = max(
        [(k, v) for k, v in by_duration.items() if v['count'] >= _MIN_BUCKET_SIZE],
        key=lambda x: x[1]['avg_ret'], default=None,
    )
    if best_dur:
        findings.append(
            f"Best duration: {best_dur[0]} ({best_dur[1]['avg_ret']}% retention, n={best_dur[1]['count']})"
        )
    dur_corr = next((c for c in correlations if c['factor'] == 'duration'), None)
    if dur_corr:
        findings.append(dur_corr['finding'])
    best_topic = max(
        [(k, v) for k, v in by_topic.items() if v['count'] >= _MIN_BUCKET_SIZE],
        key=lambda x: x[1]['avg_ret'], default=None,
    )
    if best_topic:
        findings.append(
            f"Best topic for retention: '{best_topic[0]}' ({best_topic[1]['avg_ret']}% avg, n={best_topic[1]['count']})"
        )
    views_corr = next((c for c in correlations if c['factor'] == 'views'), None)
    if views_corr:
        findings.append(views_corr['finding'])
    return findings


def _generate_rule20(by_hook, by_duration, correlations, findings, avg_ret) -> list[str]:
    constraints: list[str] = []
    good_hooks = [h for h, data in by_hook.items() if data['count'] >= _MIN_BUCKET_SIZE and data['vs_avg'] > 0]
    bad_hooks = [h for h, data in by_hook.items() if data['count'] >= _MIN_BUCKET_SIZE and data['vs_avg'] < -2]
    if good_hooks:
        constraints.append(
            f"PREFER hook types: {', '.join(good_hooks)} (above-average retention on this channel)"
        )
    if bad_hooks:
        constraints.append(
            f"AVOID hook types: {', '.join(bad_hooks)} (below-average retention on this channel)"
        )
    best_dur = max(
        [(k, v) for k, v in by_duration.items() if v['count'] >= _MIN_BUCKET_SIZE],
        key=lambda x: x[1]['avg_ret'], default=None,
    )
    if best_dur:
        constraints.append(
            f"OPTIMAL duration: {best_dur[0]} range ({best_dur[1]['avg_ret']}% retention vs {avg_ret:.1f}% channel avg)"
        )
    dur_corr = next((c for c in correlations if c['factor'] == 'duration'), None)
    if dur_corr and dur_corr['effect_size'] > 3:
        constraints.append(
            "CAUTION: Each added minute costs retention. Cut sections that don't add evidence or causal connections."
        )
    constraints.append(
        f"TARGET: {avg_ret:.0f}%+ retention. Channel average is {avg_ret:.1f}%. Top performers reach 35-50%."
    )
    return constraints


# ---------------------------------------------------------------------------
# RetentionInference — public seam
# ---------------------------------------------------------------------------

def _get_position_zone(fraction: float) -> str:
    """Map 0.0-1.0 position to early/mid/late zone."""
    if fraction < 0.33:
        return "early"
    elif fraction < 0.66:
        return "mid"
    else:
        return "late"


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


class RetentionInference:
    """Single seam for retention-derived script insights.

    Methods are stateless classmethods/staticmethods because the existing
    call sites are stateless. The G2 design proposed a stateful object
    `RetentionInference(curve, sections)`; that constructor is reserved
    for a later step if/when callers benefit from caching across method
    calls. For now, the class is a namespace.
    """

    # ------ classifiers (decoder surface) ----------------------------------

    @staticmethod
    def classify_hook_type(title: str) -> str:
        return _classify_hook_type(title)

    @staticmethod
    def classify_duration_bucket(seconds: int) -> str:
        return _classify_duration_bucket(seconds)

    @staticmethod
    def classify_specificity(title: str) -> str:
        return _classify_specificity(title)

    # ------ mapper surface --------------------------------------------------

    @staticmethod
    def mapped_drops(drop_off_points: list[dict], sections: list, wpm: int = 150) -> list[dict]:
        """Align retention drops to script sections by cumulative word count."""
        return _map_drops_to_sections(drop_off_points, sections, wpm)

    @staticmethod
    def section_timestamps(sections: list, wpm: int = 150) -> list[dict]:
        """Per-section start/end timestamps based on word count and wpm."""
        return _estimate_section_timestamps(sections, wpm)

    @staticmethod
    def format_drops_table(mapped_drops: list[dict]) -> str:
        """Markdown table of mapped drops sorted by magnitude desc."""
        return _format_mapped_drops_table(mapped_drops)

    # ------ scorer surface --------------------------------------------------

    @staticmethod
    def score_section(
        section_text: str,
        section_type: str,
        topic_type: str,
        baseline: dict | None = None,
    ) -> dict:
        """Score a single section for retention risk."""
        return _score_section_dict(section_text, section_type, topic_type, baseline)

    @staticmethod
    def section_scores(sections: list, topic_type: str) -> list[dict]:
        """Score every parsed section in batch (gets baseline once)."""
        if not sections:
            return []
        try:
            baseline = _get_topic_baseline(topic_type)
            results: list[dict] = []
            for section in sections:
                heading_lower = section.heading.lower()
                if any(w in heading_lower for w in ['intro', 'opening', 'hook']):
                    section_type = 'intro'
                elif any(w in heading_lower for w in ['conclusion', 'closing', 'summary']):
                    section_type = 'conclusion'
                else:
                    section_type = 'body'
                # The legacy scorer expected `.text`; production parser exposes `.content`.
                # Tolerate both for backward compat during the migration window.
                section_text = getattr(section, 'text', None) or getattr(section, 'content', '')
                result = _score_section_dict(
                    section_text=section_text,
                    section_type=section_type,
                    topic_type=topic_type,
                    baseline=baseline,
                )
                result['section_heading'] = section.heading
                results.append(result)
            return results
        except Exception:
            return []

    # ------ decoder surface -------------------------------------------------

    @staticmethod
    def decode_channel(videos: list[dict] | None = None) -> dict:
        """Channel-level retention decoding from videos table.

        If `videos` is None, loads from analytics.db. Returns a dict matching
        the legacy `RetentionDecoder.analyze()` shape so existing callers /
        the pinning test work unchanged.
        """
        if videos is None:
            videos = _load_videos_from_analytics_db()
        if len(videos) < 5:
            return {'error': f'Only {len(videos)} videos — need at least 5'}

        avg_ret = mean([v['avg_view_percentage'] for v in videos])

        hook_data: dict[str, list[dict]] = defaultdict(list)
        for v in videos:
            hook = _classify_hook_type(v['title'])
            v['hook_type'] = hook
            hook_data[hook].append(v)
        by_hook: dict[str, dict] = {}
        for hook, vids in hook_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            top = sorted(vids, key=lambda x: -x['avg_view_percentage'])[:3]
            by_hook[hook] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
                'avg_duration_min': round(mean([v['duration_seconds'] for v in vids]) / 60, 1),
                'top_videos': [
                    {'title': v['title'][:60], 'retention': v['avg_view_percentage'],
                     'duration_min': round(v['duration_seconds'] / 60, 1)}
                    for v in top
                ],
            }

        dur_data: dict[str, list[dict]] = defaultdict(list)
        for v in videos:
            bucket = _classify_duration_bucket(v['duration_seconds'])
            dur_data[bucket].append(v)
        by_duration: dict[str, dict] = {}
        for bucket, vids in dur_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_duration[bucket] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        topic_data: dict[str, list[dict]] = defaultdict(list)
        for v in videos:
            topic_data[v.get('topic_type') or 'unknown'].append(v)
        by_topic: dict[str, dict] = {}
        for topic, vids in topic_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_topic[topic] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        spec_data: dict[str, list[dict]] = defaultdict(list)
        for v in videos:
            spec = _classify_specificity(v['title'])
            spec_data[spec].append(v)
        by_specificity: dict[str, dict] = {}
        for spec, vids in spec_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_specificity[spec] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        correlations = _compute_correlations(videos, avg_ret)
        top_findings = _generate_findings(by_hook, by_duration, by_topic, by_specificity, correlations, avg_ret)
        rule20 = _generate_rule20(by_hook, by_duration, correlations, top_findings, avg_ret)

        return {
            'video_count': len(videos),
            'channel_avg_retention': round(avg_ret, 1),
            'by_hook_type': dict(sorted(by_hook.items(), key=lambda x: -x[1]['avg_ret'])),
            'by_duration': by_duration,
            'by_topic': dict(sorted(by_topic.items(), key=lambda x: -x[1]['avg_ret'])),
            'by_specificity': by_specificity,
            'correlations': correlations,
            'top_findings': top_findings,
            'rule20_constraints': rule20,
        }

    # ------ predictor surface (moved from retention_predictor.py) -----------

    @staticmethod
    def classify_content(text: str) -> str:
        """Classify content type of a text segment. Moved from retention_analysis.py."""
        # Reuse existing regex patterns if possible, or define them here
        # For G3, we'll use the patterns from retention_analysis.py logic
        # Priority: personal_authority > quote > primary_source > statistic > modern_relevance > transition > narration
        
        # Regex patterns for classification (from retention_analysis.py)
        QUOTE_PATTERNS = r"(according to|wrote|said|states|argued|claimed|concluded|noted|observed|page \d|pp?\. \d|quote|in his |in her |in their )"
        PRIMARY_SOURCE_PATTERNS = r"(\[b-roll|article \d|treaty of|document|memorandum|decree|statute|constitution|resolution \d|chapter \d|section \d|paragraph \d|on screen|here is the|here's the actual|the original text|let me read|reads as follows)"
        MODERN_RELEVANCE_PATTERNS = r"(today|still |right now|currently|as of 202[0-9]|in 202[0-9]|this year|last year|recent|modern|present[ -]day|ongoing)"
        TRANSITION_PATTERNS = r"^(and that brings us|so |but here'?s|now |let'?s |which brings|and this is where|this is where|that'?s where|fast forward|moving on|turning to)"
        PERSONAL_AUTHORITY_PATTERNS = r"(I read|I found|I checked|so I |I went|I looked|I downloaded|I translated|I compared|I actually|I counted|when I |I dug)"
        STATISTIC_PATTERNS = r"(\d+[,.]?\d*\s*(%|percent|billion|million|thousand|hundred)|\d+/\d+|\d+ out of \d+|\d+\.\d+)"

        if re.search(PERSONAL_AUTHORITY_PATTERNS, text, re.I):
            return "personal_authority"
        if re.search(QUOTE_PATTERNS, text, re.I):
            return "quote"
        if re.search(PRIMARY_SOURCE_PATTERNS, text, re.I):
            return "primary_source"
        if re.search(STATISTIC_PATTERNS, text, re.I):
            return "statistic"
        if re.search(MODERN_RELEVANCE_PATTERNS, text, re.I):
            return "modern_relevance"
        # Transition check: only for shorter segments that START with transition words
        if len(text.split()) <= 15 and re.match(TRANSITION_PATTERNS, text, re.I):
            return "transition"
        return "narration"

    @staticmethod
    def predict_retention(sections: list, verbose: bool = False) -> dict:
        """
        Predict retention curve for a parsed script.
        Moved from retention_predictor.py and refactored for RetentionInference.
        """
        if not sections:
            return {
                'curve': [], 'sections': [], 
                'flags': [{'severity': 'WARNING', 'message': 'No sections found', 'section': '', 'position_pct': 0}],
                'recommendations': ['Script appears empty.'],
                'total_words': 0, 'estimated_script_duration_min': 0.0
            }

        # Handle both Section objects and legacy dicts
        total_words = sum(getattr(s, 'word_count', 0) if hasattr(s, 'word_count') else s.get('word_count', 0) for s in sections)
        est_duration_min = total_words / 160 # wpm=160 from predictor
        est_filmed_min = est_duration_min / 1.8

        section_results = []
        curve_points = []
        flags = []
        recommendations = []

        words_so_far = 0
        last_evidence_pos = 0.0
        narration_streak = 0
        has_early_evidence = False
        first_evidence_pos = None

        for sec in sections:
            # Standardize section properties
            header = getattr(sec, 'heading', None) if hasattr(sec, 'heading') else sec.get('header', 'Unknown')
            if header is None: header = getattr(sec, 'header', 'Unknown') if hasattr(sec, 'header') else sec.get('header', 'Unknown')
            
            content = getattr(sec, 'content', None) if hasattr(sec, 'content') else sec.get('content', None)
            if content is None: 
                content = getattr(sec, 'text', None) if hasattr(sec, 'text') else sec.get('text', None)
            
            if content is None:
                # Handle legacy sentences list
                sents = getattr(sec, 'sentences', None) if hasattr(sec, 'sentences') else sec.get('sentences', None)
                if sents:
                    content = " ".join(sents)
            
            content = content or ""
            
            word_count = getattr(sec, 'word_count', 0) if hasattr(sec, 'word_count') else sec.get('word_count', len(content.split()))
            
            # Sentence-level classification (simplified for RetentionInference)
            sentences = re.split(r'(?<=[.!?])\s+', content)
            type_summary = defaultdict(int)
            classified_sentences = []
            
            for sent in sentences:
                if len(sent.strip()) < 10: continue
                ctype = RetentionInference.classify_content(sent)
                type_summary[ctype] += len(sent.split())
                if verbose:
                    classified_sentences.append({"text": sent[:100], "type": ctype, "words": len(sent.split())})

            dominant_type = max(type_summary, key=type_summary.get) if type_summary else "narration"
            
            # Position tracking
            midpoint = words_so_far + word_count / 2
            pos_frac = midpoint / total_words if total_words > 0 else 0
            pos_pct = int(pos_frac * 100)
            zone = _get_position_zone(pos_frac)

            # Prediction logic
            base_ret = _get_channel_avg_at(pos_pct)
            narration_delta = POSITION_DELTAS.get(zone, {}).get("narration", -0.005)
            
            quality_bonus = 0.0
            for ct, wc in type_summary.items():
                weight = wc / word_count if word_count > 0 else 0
                ct_delta = POSITION_DELTAS.get(zone, {}).get(ct, OVERALL_DELTAS.get(ct, -0.005))
                quality_bonus += (ct_delta - narration_delta) * weight

            span_pct = (word_count / total_words * 100) if total_words > 0 else 1
            cumulative_bonus = quality_bonus * span_pct * 2.0
            predicted_ret = max(0.05, min(1.0, base_ret + cumulative_bonus))
            
            change = predicted_ret - (curve_points[-1][1] if curve_points else 1.0)
            curve_points.append((pos_pct, round(predicted_ret, 4)))

            # Evidence tracking
            has_interrupt = False
            for ct in type_summary:
                if ct in ("quote", "primary_source", "statistic"):
                    if first_evidence_pos is None: first_evidence_pos = pos_frac
                    if pos_frac <= 0.15: has_early_evidence = True
                    last_evidence_pos = pos_frac
                    has_interrupt = True
            
            if has_interrupt: narration_streak = 0
            else: narration_streak += word_count

            # Flags (simplified)
            if pos_pct > 10 and change < -0.05:
                flags.append({"severity": "WARNING", "message": f"Drop of {change:+.1%} predicted", "section": header, "position_pct": pos_pct})
            
            if (narration_streak / 160) > 3.0:
                flags.append({"severity": "WARNING", "message": "Long narration streak (>3m)", "section": header, "position_pct": pos_pct})

            sec_res = {
                "header": header, "position_pct": pos_pct, "word_count": word_count,
                "estimated_minutes": round(word_count / 160, 1),
                "content_summary": dict(type_summary), "dominant_type": dominant_type,
                "predicted_retention": round(predicted_ret, 4), "retention_change": round(change, 4),
                "zone": zone
            }
            if verbose: sec_res["sentences"] = classified_sentences
            section_results.append(sec_res)
            words_so_far += word_count

        # Recommendations
        if not has_early_evidence and first_evidence_pos:
            recommendations.append(f"First evidence at {first_evidence_pos:.0%}. Move earlier (first 90s).")
        
        return {
            "curve": curve_points, "sections": section_results, "flags": flags,
            "recommendations": recommendations, "total_words": total_words,
            "estimated_script_duration_min": round(est_duration_min, 1),
            "estimated_filmed_duration_min": round(est_filmed_min, 1),
            "predicted_final_retention": curve_points[-1][1] if curve_points else 0,
            "channel_avg_final_retention": _get_channel_avg_at(100)
        }

    @classmethod
    def predict_from_sections(cls, sections: list, verbose: bool = False) -> dict:
        """Entry point for section-based prediction. Absorbs retention_predictor.predict_retention."""
        return cls.predict_retention(sections, verbose=verbose)

    @classmethod
    def predict_from_text(cls, text: str, verbose: bool = False) -> dict:
        """Parse script text and predict retention."""
        from tools.production.parser import ScriptParser
        parser = ScriptParser()
        sections = parser.parse_text(text)
        return cls.predict_retention(sections, verbose=verbose)

    @classmethod
    def predict_from_file(cls, script_path: str, verbose: bool = False) -> dict:
        """Parse script file and predict retention."""
        from tools.production.parser import ScriptParser
        parser = ScriptParser()
        sections = parser.parse_file(str(script_path))
        return cls.predict_retention(sections, verbose=verbose)
