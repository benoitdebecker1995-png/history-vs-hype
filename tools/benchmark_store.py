"""
Benchmark Store — Single interface for niche_benchmark.json data.

Provides:
- load()                   — reads niche_benchmark.json, returns dict or None
- get_niche_score()        — VPS-to-score conversion for a given title pattern
- get_topic_thresholds()   — grade thresholds keyed by topic type
- normalize_topic_type()   — maps performance.py taxonomy -> niche taxonomy
- TOPIC_GRADE_THRESHOLDS   — per-topic pass/good score targets

Design principles:
- Never raises: all public functions return None / defaults on any failure
- No caching: simple file read each call (benchmark data is small, rarely changes)
- No hard dependencies: pathlib + json only

Colon IMPORTANT NOTE:
    Niche colon data shows 0.776 median VPS (higher than declarative 0.565).
    This is INFLATED by pipe-style titles used by Knowing Better and Kraut
    (e.g., "The Part of History You've Always Skipped | Neoslavery").
    Pipe-style is NOT a colon in the YouTube title character sense.
    The own-channel measured CTR penalty for colons is -28.1% (HIGH confidence, n=9).
    Therefore: colon remains a HARD REJECT in title_scorer.py.
    get_niche_score('colon') still works for informational purposes only —
    title_scorer must NOT use it to override the colon hard-reject.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

# Default path: channel-data/niche_benchmark.json relative to project root
# Resolve relative to this file's grandparent directory (project root)
_PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_PATH = str(_PROJECT_ROOT / "channel-data" / "niche_benchmark.json")


# =============================================================================
# Topic grade thresholds — per CONTEXT.md two-tier grading system
#
# Rationale (from Phase 67 CONTEXT.md):
#   territorial:          lower bar — high-volume audience, many competitor titles pass
#   ideological:          medium bar — subscriber conversion is 2.31% (best for growth)
#   political_fact_check: high bar — same-niche competitors score significantly higher;
#                         a score that is "okay" for territorial is NOT okay here
#   general:              neutral defaults
# =============================================================================

TOPIC_GRADE_THRESHOLDS: Dict[str, Dict[str, int]] = {
    "territorial":          {"pass": 50, "good": 65},
    "ideological":          {"pass": 60, "good": 70},
    "political_fact_check": {"pass": 75, "good": 85},
    "general":              {"pass": 60, "good": 70},
}


# =============================================================================
# Type normalizer — maps performance.py 8-type taxonomy to niche 3+1 taxonomy
# =============================================================================

_TYPE_MAP: Dict[str, str] = {
    # 1:1 passthroughs
    "territorial":          "territorial",
    "ideological":          "ideological",
    "political_fact_check": "political_fact_check",
    "general":              "general",
    # Mapped
    "politician":           "political_fact_check",
    "colonial":             "territorial",
    "legal":                "territorial",
    "archaeological":       "general",
    "medieval":             "general",
}


def normalize_topic_type(t: str) -> str:
    """
    Map a performance.py topic taxonomy value to the niche_benchmark.json taxonomy.

    performance.py returns 8 types: territorial, ideological, colonial, politician,
    archaeological, medieval, legal, general.
    niche_benchmark.json uses 3 types + general: territorial, ideological,
    political_fact_check, general.

    Args:
        t: Topic type string from classify_topic_type() or any caller.

    Returns:
        Normalized topic type string. Unknown inputs fall back to 'general'.
    """
    return _TYPE_MAP.get(t, "general")


def get_topic_thresholds(topic_type: str) -> Dict[str, int]:
    """
    Return grade thresholds {'pass': int, 'good': int} for a topic type.

    Args:
        topic_type: Normalized topic type string (e.g., 'territorial').

    Returns:
        Dict with 'pass' and 'good' keys. Falls back to general defaults for
        unknown types.
    """
    return TOPIC_GRADE_THRESHOLDS.get(topic_type, TOPIC_GRADE_THRESHOLDS["general"])


# =============================================================================
# File loader
# =============================================================================

def load(path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Read niche_benchmark.json and return its contents as a dict.

    Args:
        path: Optional absolute path to JSON file. When None, reads from
              channel-data/niche_benchmark.json relative to project root.

    Returns:
        Parsed JSON dict, or None if the file is missing, unreadable, or invalid.
        Never raises an exception.
    """
    target = path if path is not None else DEFAULT_PATH
    try:
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            return None
        return json.loads(text)
    except Exception:
        return None


# =============================================================================
# VPS conversion
# =============================================================================

def _vps_to_score(vps: float) -> int:
    """
    Convert a views-per-subscriber ratio (VPS) to a 0-100 score.

    Calibration anchor:
        declarative median VPS = 0.565 -> score = 64 ≈ static baseline 65

    Formula: min(100, max(0, int(vps * 115)))

    Note: VPS is NOT CTR. It is a directional proxy (views/subscriber ratio)
    extracted from competitor channels. Higher VPS = more views per subscriber =
    better packaging effectiveness.
    """
    return min(100, max(0, int(vps * 115)))


# =============================================================================
# Niche score lookup
# =============================================================================

_SENTINEL = object()  # distinct from None — used to distinguish "not passed" from "None passed"


def get_niche_score(pattern: str, data=_SENTINEL) -> Optional[int]:
    """
    Return a 0-100 score for a title pattern based on niche benchmark data.

    Args:
        pattern: Title pattern string (e.g., 'declarative', 'how_why', 'versus').
        data:    Optional pre-loaded benchmark dict from load(). When omitted,
                 load() is called internally using the default path. When explicitly
                 passed as None (e.g., the result of a failed load()), returns None
                 without attempting a fresh load.

    Returns:
        Integer score (0-100), or None if:
        - Data is None (benchmark file missing or failed load passed in)
        - Pattern is not in by_pattern
        - confidence == "LOW" AND sample_count < 3 (guards against versus n=1)

    COLON NOTE: Returns a score for 'colon' but title_scorer.py must NOT use it
    to override the colon hard-reject — see module docstring for rationale.
    """
    if data is _SENTINEL:
        data = load()
    if data is None:
        return None

    by_pattern = data.get("by_pattern", {})
    entry = by_pattern.get(pattern)
    if entry is None:
        return None

    confidence = entry.get("confidence", "")
    sample_count = entry.get("sample_count", 0)

    # Guard: LOW confidence with tiny sample is not reliable
    if confidence == "LOW" and sample_count < 3:
        return None

    vps = entry.get("median_vps")
    if vps is None:
        return None

    return _vps_to_score(vps)
