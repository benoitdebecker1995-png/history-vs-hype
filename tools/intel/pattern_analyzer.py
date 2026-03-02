"""
pattern_analyzer.py — Outlier detection and niche pattern extraction

Two core responsibilities:
    1. Outlier detection: flag videos with views >= channel_median * multiplier (default 3x).
       Requires minimum 3 videos per channel for a meaningful median.

    2. Niche pattern extraction: analyse competitor video lists to identify format
       trends (duration distribution), title formulas, trending topics, and posting
       cadence.

All public functions follow the error-dict pattern: return {'error': msg} on failure,
never raise.
"""

import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Duration bucket labels
# ---------------------------------------------------------------------------
_DURATION_BUCKETS = [
    (0,    600,  "0-10min"),
    (600,  1200, "10-20min"),
    (1200, 1800, "20-30min"),
    (1800, 2700, "30-45min"),
    (2700, None, "45+min"),
]

# ---------------------------------------------------------------------------
# Title formula patterns
# ---------------------------------------------------------------------------
_TITLE_FORMULAS = {
    "question":    re.compile(r"\?"),
    "how_why":     re.compile(r"\b(how|why)\b", re.IGNORECASE),
    "list":        re.compile(r"\b(\d+\s+(?:ways|reasons|things|facts|tips|secrets|steps))\b", re.IGNORECASE),
    "colon_split": re.compile(r"[:\u2014\u2013]"),   # colon or em/en dash
    "quote":       re.compile(r'["\u201c\u201d\u2018\u2019]'),  # straight or curly quotes
}

# ---------------------------------------------------------------------------
# Topic keyword clusters for history/edu niche
# ---------------------------------------------------------------------------
_TOPIC_CLUSTERS = {
    "war":      ["war", "battle", "invasion", "conflict", "military", "siege", "weapon"],
    "empire":   ["empire", "imperial", "imperialism", "colony", "colonial", "conquest"],
    "roman":    ["roman", "rome", "caesar", "republic", "augustus", "byzantine"],
    "medieval": ["medieval", "middle ages", "feudal", "crusade", "knight", "castle"],
    "colonial": ["colonial", "colonialism", "colony", "settler", "independence"],
    "border":   ["border", "territory", "territorial", "boundary", "dispute", "claim"],
    "revolution": ["revolution", "revolt", "uprising", "independence", "liberation"],
    "trade":    ["trade", "silk road", "spice", "merchant", "economy", "commerce"],
    "religion": ["religion", "church", "christian", "islam", "crusade", "faith"],
    "politics": ["politics", "political", "government", "democracy", "election"],
}


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _bucket_duration(duration_seconds: int | None) -> str:
    """Return the bucket label for a video duration in seconds."""
    if duration_seconds is None:
        return "unknown"
    for lo, hi, label in _DURATION_BUCKETS:
        if hi is None or duration_seconds < hi:
            return label
    return "45+min"


def _detect_title_formula(title: str) -> list:
    """Return list of formula labels that match the title."""
    matched = []
    for name, pattern in _TITLE_FORMULAS.items():
        if pattern.search(title):
            matched.append(name)
    return matched or ["other"]


def _extract_topics(title: str) -> list:
    """Return list of topic cluster names that appear in the title (case-insensitive)."""
    title_lower = title.lower()
    found = []
    for topic, keywords in _TOPIC_CLUSTERS.items():
        if any(kw in title_lower for kw in keywords):
            found.append(topic)
    return found


def _parse_published_at(published_at: str | None) -> datetime | None:
    """
    Parse an ISO 8601 published_at string into a UTC-aware datetime.

    Returns None if parsing fails.
    """
    if not published_at:
        return None
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def detect_outliers(videos: list, multiplier: float = 3.0) -> list:
    """
    Flag videos that outperform their channel median by multiplier.

    Groups videos by channel_id. For each channel with >= 3 videos that have
    view counts > 0, calculates the median view count and flags any video with
    views >= median * multiplier as an outlier.

    Args:
        videos:     List of video dicts. Each must have 'video_id', 'channel_id',
                    and 'views' (int | None).
        multiplier: Threshold multiple of median (default 3.0 = 3x).

    Returns:
        Same list with 'is_outlier' (bool) and 'outlier_ratio' (float) added
        to every video dict.
        Returns {'error': str} on catastrophic failure.
    """
    try:
        # Group view counts by channel
        channel_views: dict[str, list] = defaultdict(list)
        for video in videos:
            cid = video.get("channel_id")
            views = video.get("views")
            if cid and views and views > 0:
                channel_views[cid].append(views)

        # Compute per-channel median (only channels with >= 3 data points)
        channel_median: dict[str, float] = {}
        for cid, view_list in channel_views.items():
            if len(view_list) >= 3:
                channel_median[cid] = statistics.median(view_list)

        # Annotate each video
        result = []
        for video in videos:
            vid = dict(video)  # Shallow copy — don't mutate input
            cid = vid.get("channel_id")
            views = vid.get("views") or 0
            median = channel_median.get(cid)

            if median is not None and median > 0 and views > 0:
                ratio = views / median
                vid["is_outlier"] = ratio >= multiplier
                vid["outlier_ratio"] = round(ratio, 2)
            else:
                vid["is_outlier"] = False
                vid["outlier_ratio"] = 0.0

            result.append(vid)

        return result

    except Exception as exc:
        return {"error": f"detect_outliers failed: {exc}"}


# ---------------------------------------------------------------------------
# Niche pattern extraction
# ---------------------------------------------------------------------------

def extract_niche_patterns(videos: list) -> dict:
    """
    Extract format, hook, and topic patterns from a list of competitor videos.

    Analyses:
        - Duration distribution across standard buckets (0-10min ... 45+min)
        - Average and median duration
        - Title formula distribution (question, how/why, list, colon-split, quote)
        - Average title length (characters)
        - Common topics extracted from titles via keyword clusters
        - Posting cadence per channel (average days between uploads)

    Args:
        videos: List of video dicts with at minimum 'title', 'duration_seconds',
                'channel_id', and 'published_at'.

    Returns:
        {
            'format_patterns': {
                'avg_duration_seconds': float,
                'median_duration_seconds': float,
                'duration_distribution': {bucket_label: count, ...},
                'avg_title_length': float,
                'video_count': int,
            },
            'hook_patterns': {
                'title_formula_counts': {formula: count, ...},
                'title_formula_pct': {formula: pct_str, ...},
            },
            'trending_topics': [
                {'topic': str, 'count': int, 'pct': str},
                ...
            ]
        }
        or {'error': str}
    """
    try:
        if not videos:
            return {
                "format_patterns": {},
                "hook_patterns": {},
                "trending_topics": [],
            }

        # --- Duration stats ---
        durations = [v.get("duration_seconds") for v in videos if v.get("duration_seconds")]
        avg_duration = round(statistics.mean(durations), 1) if durations else 0.0
        median_duration = round(statistics.median(durations), 1) if durations else 0.0

        bucket_counts: Counter = Counter()
        for video in videos:
            bucket = _bucket_duration(video.get("duration_seconds"))
            bucket_counts[bucket] += 1

        # --- Title stats ---
        titles = [v.get("title", "") for v in videos if v.get("title")]
        avg_title_len = round(statistics.mean(len(t) for t in titles), 1) if titles else 0.0

        # --- Title formula distribution ---
        formula_counter: Counter = Counter()
        for title in titles:
            formulas = _detect_title_formula(title)
            for f in formulas:
                formula_counter[f] += 1

        total_titles = len(titles) if titles else 1
        formula_pct = {
            f: f"{round(count / total_titles * 100, 1)}%"
            for f, count in formula_counter.most_common()
        }

        # --- Topic extraction ---
        # Prefer topic_cluster column (set by Phase 7b using UNIFIED_TOPICS)
        # Fall back to title-based extraction for raw video dicts without it
        topic_counter: Counter = Counter()
        for video in videos:
            cluster = video.get("topic_cluster")
            if cluster:
                # topic_cluster is stored as JSON string: '["territorial", "colonial"]'
                import json as _json
                try:
                    topics = _json.loads(cluster) if isinstance(cluster, str) else cluster
                except (_json.JSONDecodeError, TypeError):
                    topics = []
                for topic in topics:
                    if topic and topic != "general":
                        topic_counter[topic] += 1
            else:
                title = video.get("title", "")
                for topic in _extract_topics(title):
                    topic_counter[topic] += 1

        total_videos = len(videos) if videos else 1
        trending_topics = [
            {
                "topic": topic,
                "count": count,
                "pct": f"{round(count / total_videos * 100, 1)}%",
            }
            for topic, count in topic_counter.most_common(10)
        ]

        return {
            "format_patterns": {
                "avg_duration_seconds": avg_duration,
                "median_duration_seconds": median_duration,
                "duration_distribution": dict(bucket_counts),
                "avg_title_length": avg_title_len,
                "video_count": len(videos),
            },
            "hook_patterns": {
                "title_formula_counts": dict(formula_counter.most_common()),
                "title_formula_pct": formula_pct,
            },
            "trending_topics": trending_topics,
        }

    except Exception as exc:
        return {"error": f"extract_niche_patterns failed: {exc}"}


# ---------------------------------------------------------------------------
# Outlier analysis
# ---------------------------------------------------------------------------

def generate_outlier_analysis(outlier_videos: list) -> list:
    """
    Generate heuristic analysis for each outlier video.

    For each outlier, assigns possible performance reasons based on title and
    duration signals.

    Args:
        outlier_videos: List of video dicts with is_outlier == True.
                        Expected fields: title, channel_id, views, outlier_ratio,
                        duration_seconds. May also have 'channel_name'.

    Returns:
        List of analysis dicts:
        [
            {
                'video_id':        str,
                'title':           str,
                'channel':         str,
                'views':           int,
                'outlier_ratio':   float,
                'duration_seconds':int,
                'possible_reasons':list[str],
            },
            ...
        ]
        Returns {'error': str} on catastrophic failure.
    """
    try:
        result = []
        for video in outlier_videos:
            if not video.get("is_outlier"):
                continue

            title = video.get("title", "")
            title_lower = title.lower()
            duration = video.get("duration_seconds") or 0
            possible_reasons = []

            # Heuristic: question-format title
            if "?" in title:
                possible_reasons.append("Question-format title")

            # Heuristic: long-form deep dive
            if duration > 1800:  # > 30 minutes
                possible_reasons.append("Long-form deep dive (30+ min)")
            elif duration > 1200:  # > 20 minutes
                possible_reasons.append("In-depth treatment (20+ min)")

            # Heuristic: specific factual claim (numbers or dates)
            if re.search(r"\b\d{4}\b|\b\d+\s*(?:years?|centuries|decades)\b", title, re.IGNORECASE):
                possible_reasons.append("Specific factual claim or historical date")

            # Heuristic: comparison / versus format
            if re.search(r"\bvs\.?\b|\bversus\b", title_lower):
                possible_reasons.append("Comparison format (vs)")

            # Heuristic: how/why mechanism framing (strong for this channel's audience)
            if re.search(r"\b(how|why)\b", title_lower):
                possible_reasons.append("Mechanism/explanation framing (how/why)")

            # Heuristic: territorial or border angle
            if any(kw in title_lower for kw in ["border", "territory", "island", "land", "map"]):
                possible_reasons.append("Territorial/geographic hook")

            # Heuristic: colonial or historical myth angle
            if any(kw in title_lower for kw in ["myth", "truth", "real", "actually", "really", "fact"]):
                possible_reasons.append("Myth-busting / factual correction framing")

            if not possible_reasons:
                possible_reasons.append("No clear heuristic pattern identified")

            result.append({
                "video_id":         video.get("video_id", ""),
                "title":            title,
                "channel":          video.get("channel_name") or video.get("channel_id", ""),
                "views":            video.get("views") or 0,
                "outlier_ratio":    video.get("outlier_ratio", 0.0),
                "duration_seconds": duration,
                "possible_reasons": possible_reasons,
            })

        return result

    except Exception as exc:
        return {"error": f"generate_outlier_analysis failed: {exc}"}
