"""
Retention-to-Script Cross-Video Analysis Tool

Maps YouTube retention curves to SRT subtitle content to find cross-video
patterns about what script content types cause retention drops or spikes.

Usage:
    python -m tools.youtube_analytics.retention_analysis              # all videos
    python -m tools.youtube_analytics.retention_analysis --video ID   # single video
    python -m tools.youtube_analytics.retention_analysis --report     # generate markdown report
    python -m tools.youtube_analytics.retention_analysis --cached     # skip API, use cache only
"""

import argparse
import json
import os
import re
import sqlite3
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

logger = get_logger(__name__)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "tools" / "youtube_analytics" / "analytics.db"
CACHE_DIR = BASE_DIR / "tools" / "youtube_analytics" / "_retention_cache"
REPORT_PATH = BASE_DIR / "channel-data" / "patterns" / "RETENTION-SCRIPT-CORRELATION.md"
SRT_DIRS = [
    BASE_DIR / "transcripts",
    BASE_DIR / "video-projects" / "_IN_PRODUCTION",
]

# Skip non-English / non-primary SRT patterns
SRT_SKIP_PATTERNS = [
    r"-es\.srt$",       # Spanish
    r"-farsi\.srt$",    # Farsi
    r"_fr\.srt$",       # French
    r"_pt\.srt$",       # Portuguese
    r"SPANISH",         # Spanish subtitles
    r"BACKUP",          # Backup files
    r"_CORRECTED",      # Corrected duplicates
    r"definitive\.srt", # Alternate version
]


# ---------------------------------------------------------------------------
# 1. SRT-to-Video-ID Mapping
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace for fuzzy matching."""
    text = text.lower()
    text = re.sub(r"[''\".,!?:;|(){}\[\]\-–—]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _slug_tokens(slug: str) -> set:
    """Extract meaningful tokens from an SRT filename slug."""
    slug = slug.lower().replace("-", " ").replace("_", " ")
    return {t for t in slug.split() if len(t) > 2}


def _should_skip_srt(path: Path) -> bool:
    """Return True if SRT should be skipped (non-English, backup, etc.)."""
    name = path.name
    for pattern in SRT_SKIP_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return True
    return False


def find_all_srts() -> list[Path]:
    """Find all candidate SRT files across known directories."""
    srts = []
    for d in SRT_DIRS:
        if not d.exists():
            continue
        for srt in d.rglob("*.srt"):
            if not _should_skip_srt(srt):
                srts.append(srt)
    return srts


def build_srt_mapping() -> dict[str, Path]:
    """
    Map video IDs to SRT file paths via fuzzy title matching.

    Handles deduplication: if multiple videos match the same SRT,
    keeps only the best match for each SRT file.

    Returns:
        {video_id: Path_to_srt}
    """
    # Manual overrides for known tricky mappings (video_id -> SRT filename stem)
    # Add entries here when automatic matching fails
    MANUAL_OVERRIDES = {
        "Y21EjQ0v9W4": "belize guatemala icj",   # ICJ video, not the dispute video
        "XbGl1Kcspt4": "belize guatemala icj",   # Guatemala vs Belize ICJ
        "L5ZIP24-36s": "iran part2",              # Iran Part 2 (longer video)
        "HtVIC4dS0e8": "iran part1",              # Iran Part 1
        "FvqALriDCv4": "vance-part-1-published",  # JD Vance human rights
        "LO_fUeX9IEQ": "vance reaction2",         # JD Vance child sacrifice
        "P6yalauLDic": "bermeja",                  # Bermeja island
        "imPn_OxLYlk": "statut",                  # Vichy France
        "Q5Pfv_dPubU": "almada",                   # Operation Condor
        "n-CUSE4bDvg": "cyprus-division-petros",   # Cyprus
        "UH2PddfaaR8": "plo-kgb-russian-spies",   # KGB/Palestine
        "lPilDVSAeEM": "kashmir-british-sale",     # Kashmir
        "d1Bx3uptNuo": "kosovo-serbian-farmer-lie", # Kosovo/Serbia
        "BXyT8OTGBBo": "middle-east-ancient-hatreds",  # fallback
        "QgDJSu0Y5K0": "western-sahara-wall",     # Morocco/Western Sahara
        "6SdfqTYPviQ": "ukraine-isnt-fake",        # Ukraine history
        "TYNaIu28LeU": "belevezha",                # Belavezha Accords
        "2RQWu-cyO90": "lagertha-vikings-myth",    # Lagertha
        "UxsXdUj0EhU": "nagorno-karabakh-census",  # Armenia
        "JkH4XIHfnJU": "trade-wars-200-year-lie",  # Tariffs
        "X0dO-aJx-aQ": "indigenous-genocide-company",  # London Stock Exchange
        "lFGs5NHMxMw": "berlin",                   # Berlin Conference
        "ZZz_g_Ov6Lg": "chagos",                   # Chagos (| Britain Expelled)
    }

    # Load video metadata from DB
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT video_id, title FROM videos")
    videos = cur.fetchall()
    conn.close()

    srts = find_all_srts()
    logger.info("Found %d SRT files and %d videos in DB", len(srts), len(videos))

    # Build SRT index by stem (lowercased) for manual overrides
    srt_by_stem = {}
    for srt in srts:
        srt_by_stem[srt.stem.lower()] = srt

    # Build token index for fuzzy matching
    srt_by_tokens = {}
    for srt in srts:
        tokens = _slug_tokens(srt.stem)
        srt_by_tokens[srt] = tokens

    # Track: {srt_path: [(video_id, score)]} for deduplication
    candidates = defaultdict(list)

    for video_id, title in videos:
        # Check manual override first
        if video_id in MANUAL_OVERRIDES:
            override_stem = MANUAL_OVERRIDES[video_id].lower()
            # Try exact stem match, then partial
            matched_srt = srt_by_stem.get(override_stem)
            if not matched_srt:
                # Try partial match on stem
                for stem, srt in srt_by_stem.items():
                    if override_stem in stem or stem in override_stem:
                        matched_srt = srt
                        break
            if matched_srt:
                candidates[matched_srt].append((video_id, 100.0))  # High priority
                continue

        title_norm = _normalize(title)
        title_tokens = set(title_norm.split())

        best_srt = None
        best_score = 0

        for srt, srt_tokens in srt_by_tokens.items():
            if not srt_tokens:
                continue

            overlap = srt_tokens & title_tokens
            if not overlap:
                continue

            score = len(overlap) / len(srt_tokens)
            if len(overlap) >= 2:
                score += 0.1 * len(overlap)

            if score > best_score:
                best_score = score
                best_srt = srt

        if best_srt and best_score >= 0.5:
            candidates[best_srt].append((video_id, best_score))

    # Deduplicate: for each SRT, keep only the best-scoring video
    mapping = {}
    for srt_path, vid_scores in candidates.items():
        # Sort by score descending, take best
        vid_scores.sort(key=lambda x: x[1], reverse=True)
        best_vid, best_score = vid_scores[0]
        mapping[best_vid] = srt_path
        if len(vid_scores) > 1:
            logger.debug(
                "SRT %s: chose %s (%.2f) over %s",
                srt_path.name, best_vid, best_score,
                ", ".join(f"{v}({s:.2f})" for v, s in vid_scores[1:]),
            )

    logger.info("Mapped %d/%d videos to SRT files", len(mapping), len(videos))
    return mapping


# ---------------------------------------------------------------------------
# 2. SRT Parser
# ---------------------------------------------------------------------------

def _parse_srt_timestamp(ts: str) -> float:
    """Parse SRT timestamp 'HH:MM:SS,mmm' to seconds."""
    ts = ts.strip()
    match = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", ts)
    if not match:
        return 0.0
    h, m, s, ms = match.groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path: Path) -> list[dict]:
    """
    Parse an SRT file into segments.

    Handles DaVinci Resolve 1-hour offset (timestamps starting at 01:00:00).
    Strips HTML tags (<b>, <i>, etc.).

    Returns:
        [{start_seconds: float, end_seconds: float, text: str}, ...]
    """
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")

    segments = []
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # Find the timestamp line
        ts_line = None
        text_lines = []
        for i, line in enumerate(lines):
            if "-->" in line:
                ts_line = line
                text_lines = lines[i + 1:]
                break

        if not ts_line:
            continue

        parts = ts_line.split("-->")
        if len(parts) != 2:
            continue

        start = _parse_srt_timestamp(parts[0])
        end = _parse_srt_timestamp(parts[1])

        # Strip HTML tags
        text = " ".join(text_lines)
        text = re.sub(r"<[^>]+>", "", text).strip()

        if text:
            segments.append({
                "start_seconds": start,
                "end_seconds": end,
                "text": text,
            })

    if not segments:
        return segments

    # Detect and remove DaVinci Resolve 1-hour offset
    first_start = segments[0]["start_seconds"]
    if first_start >= 3500 and first_start <= 3700:  # ~1 hour offset
        offset = 3600.0
        for seg in segments:
            seg["start_seconds"] = max(0.0, seg["start_seconds"] - offset)
            seg["end_seconds"] = max(0.0, seg["end_seconds"] - offset)

    return segments


# ---------------------------------------------------------------------------
# 3. Content Classifier
# ---------------------------------------------------------------------------

# Regex patterns for classification (compiled once)
_QUOTE_PATTERNS = re.compile(
    r"(according to|wrote|said|states|argued|claimed|concluded|noted|observed|"
    r"page \d|pp?\. \d|quote|in his |in her |in their )",
    re.IGNORECASE,
)
_PRIMARY_SOURCE_PATTERNS = re.compile(
    r"(\[b-roll|article \d|treaty of|document|memorandum|decree|statute|"
    r"constitution|resolution \d|chapter \d|section \d|paragraph \d|"
    r"on screen|here is the|here's the actual|the original text|"
    r"let me read|reads as follows)",
    re.IGNORECASE,
)
_MODERN_RELEVANCE_PATTERNS = re.compile(
    r"(today|still |right now|currently|as of 202[0-9]|in 202[0-9]|"
    r"this year|last year|recent|modern|present[ -]day|ongoing)",
    re.IGNORECASE,
)
_TRANSITION_PATTERNS = re.compile(
    r"^(and that brings us|so |but here'?s|now |let'?s |which brings|"
    r"and this is where|this is where|that'?s where|"
    r"fast forward|moving on|turning to)",
    re.IGNORECASE,
)
_PERSONAL_AUTHORITY_PATTERNS = re.compile(
    r"(I read|I found|I checked|so I |I went|I looked|I downloaded|"
    r"I translated|I compared|I actually|I counted|when I |I dug)",
    re.IGNORECASE,
)
_STATISTIC_PATTERNS = re.compile(
    r"(\d+[,.]?\d*\s*(%|percent|billion|million|thousand|hundred)|"
    r"\d+/\d+|\d+ out of \d+|\d+\.\d+)",
    re.IGNORECASE,
)


def classify_content(text: str) -> str:
    """
    Classify a text segment into a content type.

    Priority order (first match wins):
        personal_authority > quote > primary_source > statistic >
        modern_relevance > transition > narration

    Returns one of:
        'personal_authority', 'quote', 'primary_source', 'statistic',
        'modern_relevance', 'transition', 'narration'
    """
    if _PERSONAL_AUTHORITY_PATTERNS.search(text):
        return "personal_authority"
    if _QUOTE_PATTERNS.search(text):
        return "quote"
    if _PRIMARY_SOURCE_PATTERNS.search(text):
        return "primary_source"
    if _STATISTIC_PATTERNS.search(text):
        return "statistic"
    if _MODERN_RELEVANCE_PATTERNS.search(text):
        return "modern_relevance"
    # Transition check: only for shorter segments that START with transition words
    if len(text.split()) <= 15 and _TRANSITION_PATTERNS.match(text):
        return "transition"
    return "narration"


def classify_window(segments: list[dict], center_time: float,
                    window_seconds: float = 15.0) -> tuple[str, str]:
    """
    Classify content around a specific timestamp using a time window.

    Merges text from all segments overlapping [center - window, center + window],
    then classifies the merged text.

    Returns:
        (content_type, text_preview)
    """
    t_start = center_time - window_seconds
    t_end = center_time + window_seconds

    texts = []
    for seg in segments:
        if seg["end_seconds"] >= t_start and seg["start_seconds"] <= t_end:
            texts.append(seg["text"])

    if not texts:
        return "narration", ""

    merged = " ".join(texts)
    content_type = classify_content(merged)
    # Return a preview (first 120 chars)
    preview = merged[:120].replace("\n", " ")
    if len(merged) > 120:
        preview += "..."

    return content_type, preview


# ---------------------------------------------------------------------------
# 4. Retention Cache
# ---------------------------------------------------------------------------

def _cache_path(video_id: str) -> Path:
    """Return cache file path for a video's retention data."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{video_id}.json"


def _load_cached(video_id: str) -> dict | None:
    """Load cached retention data if available."""
    p = _cache_path(video_id)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if "data_points" in data and data["data_points"]:
                return data
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def _save_cache(video_id: str, data: dict) -> None:
    """Save retention data to cache."""
    p = _cache_path(video_id)
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def fetch_retention_cached(video_id: str, force_refresh: bool = False) -> dict | None:
    """
    Fetch retention data with caching. Returns None on error.

    Args:
        video_id: YouTube video ID
        force_refresh: If True, skip cache and re-fetch from API
    """
    if not force_refresh:
        cached = _load_cached(video_id)
        if cached:
            return cached

    # Import here to avoid import errors when API deps missing
    try:
        from tools.youtube_analytics.retention import get_retention_data
    except ImportError:
        logger.error("Cannot import retention module — API dependencies missing")
        return None

    logger.info("Fetching retention data for %s from API...", video_id)
    data = get_retention_data(video_id)

    if "error" in data:
        logger.warning("API error for %s: %s", video_id, data["error"])
        return None

    _save_cache(video_id, data)
    return data


# ---------------------------------------------------------------------------
# 5. Per-Video Analysis
# ---------------------------------------------------------------------------

def analyze_video(video_id: str, title: str, duration_seconds: int,
                  topic_type: str, srt_path: Path,
                  retention_data: dict) -> dict | None:
    """
    Analyze a single video: map retention curve to SRT content.

    Returns:
        {
            video_id, title, topic_type, duration_seconds,
            data_points: [{position, retention, delta, timestamp_seconds,
                           content_type, text_preview}],
            summary: {avg_retention, content_type_breakdown}
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
    for i, dp in enumerate(data_points):
        position = dp["position"]
        retention = dp["retention"]
        timestamp = position * duration_seconds

        # Delta from previous point
        if i == 0:
            delta = 0.0
        else:
            delta = retention - data_points[i - 1]["retention"]

        content_type, text_preview = classify_window(segments, timestamp)

        analyzed.append({
            "position": round(position, 4),
            "retention": round(retention, 4),
            "delta": round(delta, 4),
            "timestamp_seconds": round(timestamp, 1),
            "content_type": content_type,
            "text_preview": text_preview,
        })

    # Content type breakdown
    type_counts = defaultdict(int)
    type_deltas = defaultdict(list)
    for pt in analyzed:
        ct = pt["content_type"]
        type_counts[ct] += 1
        type_deltas[ct].append(pt["delta"])

    breakdown = {}
    for ct in type_counts:
        deltas = type_deltas[ct]
        breakdown[ct] = {
            "count": type_counts[ct],
            "avg_delta": round(sum(deltas) / len(deltas), 5) if deltas else 0,
            "total_delta": round(sum(deltas), 4),
        }

    return {
        "video_id": video_id,
        "title": title,
        "topic_type": topic_type,
        "duration_seconds": duration_seconds,
        "data_points": analyzed,
        "content_type_breakdown": breakdown,
    }


# ---------------------------------------------------------------------------
# 6. Cross-Video Aggregation
# ---------------------------------------------------------------------------

def aggregate_results(analyses: list[dict]) -> dict:
    """
    Aggregate content-type retention patterns across all analyzed videos.

    Returns dict with:
        - by_content_type: {type: {avg_delta, count, avg_position}}
        - by_position: {early/mid/late: {type: avg_delta}}
        - by_topic_type: {topic: {type: avg_delta}}
        - worst_moments: top 10 drops
        - best_moments: top 10 gains/holds
    """
    # Collect all data points with video metadata
    all_points = []
    for analysis in analyses:
        vid = analysis["video_id"]
        title = analysis["title"]
        topic = analysis["topic_type"]
        for pt in analysis["data_points"]:
            all_points.append({
                **pt,
                "video_id": vid,
                "video_title": title,
                "topic_type": topic,
            })

    # --- By content type (global) ---
    ct_deltas = defaultdict(list)
    ct_positions = defaultdict(list)
    for pt in all_points:
        ct = pt["content_type"]
        ct_deltas[ct].append(pt["delta"])
        ct_positions[ct].append(pt["position"])

    by_content_type = {}
    for ct in ct_deltas:
        deltas = ct_deltas[ct]
        positions = ct_positions[ct]
        by_content_type[ct] = {
            "avg_delta": round(sum(deltas) / len(deltas), 5) if deltas else 0,
            "median_delta": round(sorted(deltas)[len(deltas) // 2], 5) if deltas else 0,
            "count": len(deltas),
            "avg_position": round(sum(positions) / len(positions), 3) if positions else 0,
            "positive_pct": round(
                100 * sum(1 for d in deltas if d >= 0) / len(deltas), 1
            ) if deltas else 0,
        }

    # --- By position (early <0.33, mid 0.33-0.66, late >0.66) ---
    position_bins = {"early": (0, 0.33), "mid": (0.33, 0.66), "late": (0.66, 1.01)}
    by_position = {}
    for bin_name, (lo, hi) in position_bins.items():
        bin_points = [p for p in all_points if lo <= p["position"] < hi]
        ct_deltas_bin = defaultdict(list)
        for pt in bin_points:
            ct_deltas_bin[pt["content_type"]].append(pt["delta"])

        by_position[bin_name] = {}
        for ct, deltas in ct_deltas_bin.items():
            by_position[bin_name][ct] = {
                "avg_delta": round(sum(deltas) / len(deltas), 5) if deltas else 0,
                "count": len(deltas),
            }

    # --- By topic type ---
    by_topic = defaultdict(lambda: defaultdict(list))
    for pt in all_points:
        by_topic[pt["topic_type"]][pt["content_type"]].append(pt["delta"])

    by_topic_type = {}
    for topic in by_topic:
        by_topic_type[topic] = {}
        for ct, deltas in by_topic[topic].items():
            by_topic_type[topic][ct] = {
                "avg_delta": round(sum(deltas) / len(deltas), 5) if deltas else 0,
                "count": len(deltas),
            }

    # --- Worst moments (biggest drops, skip position 0) ---
    scoreable = [p for p in all_points if p["position"] > 0.01]
    worst = sorted(scoreable, key=lambda p: p["delta"])[:10]

    # --- Best moments (biggest gains or flat holds) ---
    best = sorted(scoreable, key=lambda p: p["delta"], reverse=True)[:10]

    return {
        "videos_analyzed": len(analyses),
        "total_data_points": len(all_points),
        "by_content_type": by_content_type,
        "by_position": by_position,
        "by_topic_type": by_topic_type,
        "worst_moments": worst,
        "best_moments": best,
    }


# ---------------------------------------------------------------------------
# 7. Report Generation
# ---------------------------------------------------------------------------

def _fmt_time(seconds: float) -> str:
    """Format seconds as M:SS."""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m}:{s:02d}"


def _delta_indicator(delta: float) -> str:
    """Return a text indicator for retention delta."""
    if delta >= 0.005:
        return "GAIN"
    elif delta >= -0.002:
        return "HOLD"
    elif delta >= -0.01:
        return "slight drop"
    else:
        return "DROP"


def generate_report(agg: dict, analyses: list[dict]) -> str:
    """Generate markdown report from aggregated data."""
    lines = [
        "# Retention-to-Script Correlation Analysis",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Videos analyzed:** {agg['videos_analyzed']}",
        f"**Total data points:** {agg['total_data_points']}",
        "",
        "---",
        "",
        "## Summary: Content Type Impact on Retention",
        "",
        "| Content Type | Avg Delta | Median Delta | Count | Avg Position | Positive % |",
        "|---|---|---|---|---|---|",
    ]

    # Sort by avg_delta (best to worst)
    sorted_types = sorted(
        agg["by_content_type"].items(),
        key=lambda x: x[1]["avg_delta"],
        reverse=True,
    )
    for ct, stats in sorted_types:
        lines.append(
            f"| {ct} | {stats['avg_delta']:+.5f} | {stats['median_delta']:+.5f} "
            f"| {stats['count']} | {stats['avg_position']:.2f} | {stats['positive_pct']:.0f}% |"
        )

    # Recommendations
    lines.extend([
        "",
        "### Interpretation",
        "",
        "- **Positive avg delta** = viewers stay or return during this content type",
        "- **Negative avg delta** = viewers tend to leave during this content type",
        "- **Positive %** = percentage of data points where retention held or gained",
        "- Natural retention decay means ALL types trend negative; "
        "the key is RELATIVE performance",
        "",
    ])

    # Recommendations based on data
    if sorted_types:
        best_type = sorted_types[0][0]
        worst_type = sorted_types[-1][0]
        lines.extend([
            "### Actionable Recommendations",
            "",
            f"1. **Best retention type: `{best_type}`** -- "
            f"Use more of this content, especially in mid-video where dropout peaks",
            f"2. **Worst retention type: `{worst_type}`** -- "
            f"Keep these segments short, or pair with a stronger content type",
            "3. **Pattern interrupts:** Switch content types every 60-90 seconds "
            "to prevent monotony-driven dropout",
        ])

    # Position analysis
    lines.extend([
        "",
        "---",
        "",
        "## Position Analysis: What Works Where",
        "",
    ])
    for bin_name in ["early", "mid", "late"]:
        pos_data = agg["by_position"].get(bin_name, {})
        if not pos_data:
            continue
        lines.append(f"### {bin_name.capitalize()} (video position)")
        lines.append("")
        lines.append("| Content Type | Avg Delta | Count |")
        lines.append("|---|---|---|")
        for ct, stats in sorted(pos_data.items(), key=lambda x: x[1]["avg_delta"], reverse=True):
            lines.append(f"| {ct} | {stats['avg_delta']:+.5f} | {stats['count']} |")
        lines.append("")

    # Topic type breakdown
    lines.extend([
        "---",
        "",
        "## Topic Type Breakdown",
        "",
    ])
    for topic, ct_data in sorted(agg["by_topic_type"].items()):
        total_count = sum(v["count"] for v in ct_data.values())
        lines.append(f"### {topic} ({total_count} data points)")
        lines.append("")
        lines.append("| Content Type | Avg Delta | Count |")
        lines.append("|---|---|---|")
        for ct, stats in sorted(ct_data.items(), key=lambda x: x[1]["avg_delta"], reverse=True):
            lines.append(f"| {ct} | {stats['avg_delta']:+.5f} | {stats['count']} |")
        lines.append("")

    # Worst moments
    lines.extend([
        "---",
        "",
        "## Top 10 Worst Retention Moments",
        "",
        "These are the single biggest viewer drop-offs across all videos.",
        "",
    ])
    for i, pt in enumerate(agg["worst_moments"], 1):
        lines.extend([
            f"### {i}. {pt['video_title']}",
            f"- **Position:** {pt['position']:.0%} ({_fmt_time(pt['timestamp_seconds'])})",
            f"- **Retention drop:** {pt['delta']:+.4f} ({_delta_indicator(pt['delta'])})",
            f"- **Content type:** `{pt['content_type']}`",
            f"- **Text:** {pt.get('text_preview', 'N/A')}",
            "",
        ])

    # Best moments
    lines.extend([
        "---",
        "",
        "## Top 10 Best Retention Moments",
        "",
        "Moments where retention held steady or recovered.",
        "",
    ])
    for i, pt in enumerate(agg["best_moments"], 1):
        lines.extend([
            f"### {i}. {pt['video_title']}",
            f"- **Position:** {pt['position']:.0%} ({_fmt_time(pt['timestamp_seconds'])})",
            f"- **Retention change:** {pt['delta']:+.4f} ({_delta_indicator(pt['delta'])})",
            f"- **Content type:** `{pt['content_type']}`",
            f"- **Text:** {pt.get('text_preview', 'N/A')}",
            "",
        ])

    # Script-writer-v2 recommendations
    lines.extend([
        "---",
        "",
        "## Recommendations for script-writer-v2",
        "",
        "Based on cross-video retention data:",
        "",
    ])

    # Generate data-driven recommendations
    recs = _generate_recommendations(agg)
    for j, rec in enumerate(recs, 1):
        lines.append(f"{j}. {rec}")

    lines.extend([
        "",
        "---",
        "",
        f"*Analysis based on {agg['videos_analyzed']} videos "
        f"with {agg['total_data_points']} retention data points.*",
    ])

    return "\n".join(lines)


def _generate_recommendations(agg: dict) -> list[str]:
    """Generate actionable recommendations from aggregated data."""
    recs = []
    ct = agg["by_content_type"]
    pos = agg["by_position"]

    # Find best/worst content types
    sorted_ct = sorted(ct.items(), key=lambda x: x[1]["avg_delta"], reverse=True)
    if sorted_ct:
        best = sorted_ct[0]
        worst = sorted_ct[-1]
        recs.append(
            f"**{best[0]}** has the highest avg retention delta ({best[1]['avg_delta']:+.5f}). "
            f"Increase usage of this content type, especially in mid-video segments."
        )
        recs.append(
            f"**{worst[0]}** has the lowest avg retention delta ({worst[1]['avg_delta']:+.5f}). "
            f"Keep these segments under 30 seconds or pair with visual pattern interrupts."
        )

    # Position-specific recommendations
    for bin_name in ["early", "mid", "late"]:
        bin_data = pos.get(bin_name, {})
        if not bin_data:
            continue
        sorted_bin = sorted(bin_data.items(), key=lambda x: x[1]["avg_delta"], reverse=True)
        if sorted_bin:
            best_pos = sorted_bin[0]
            if best_pos[1]["count"] >= 5:
                recs.append(
                    f"In **{bin_name}** video segments, **{best_pos[0]}** performs best "
                    f"({best_pos[1]['avg_delta']:+.5f}). Prioritize this content type in "
                    f"the {bin_name} third of scripts."
                )

    # Personal authority check
    if "personal_authority" in ct:
        pa = ct["personal_authority"]
        if pa["avg_delta"] > -0.003:
            recs.append(
                f"**personal_authority** (\"I found\", \"I read\") holds retention well "
                f"({pa['avg_delta']:+.5f}). Continue using 2-3 per script as credibility signals."
            )
        else:
            recs.append(
                f"**personal_authority** correlates with drops ({pa['avg_delta']:+.5f}). "
                f"Reduce to 1-2 per script and keep brief."
            )

    # Quote/source check
    for qtype in ["quote", "primary_source"]:
        if qtype in ct:
            q = ct[qtype]
            recs.append(
                f"**{qtype}** segments average {q['avg_delta']:+.5f} delta "
                f"with {q['positive_pct']:.0f}% positive. "
                + (
                    "This is a retention asset -- lean into it."
                    if q["avg_delta"] > -0.005
                    else "Pair with visuals to maintain engagement."
                )
            )

    # Transition check
    if "transition" in ct:
        t = ct["transition"]
        if t["avg_delta"] < -0.005:
            recs.append(
                f"**Transitions** correlate with retention drops ({t['avg_delta']:+.5f}). "
                f"Replace bridge sentences with hook-forward lines "
                f"(tease what's coming next, not summarize what was said)."
            )

    return recs


# ---------------------------------------------------------------------------
# 8. Main / CLI
# ---------------------------------------------------------------------------

def run_analysis(video_id: str | None = None, cached_only: bool = False,
                 generate_markdown: bool = False) -> dict:
    """
    Main entry point. Analyze retention-to-script patterns.

    Args:
        video_id: If set, analyze only this video
        cached_only: If True, skip API calls and use only cached data
        generate_markdown: If True, write report to RETENTION-SCRIPT-CORRELATION.md

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
            # Rate limiting: 1s delay between API calls
            if not _load_cached(vid):
                time.sleep(1.0)

        if not ret_data:
            skipped_no_retention += 1
            logger.debug("No retention data for %s (%s)", vid, title)
            continue

        # Analyze
        print(f"  [{i}/{len(videos)}] Analyzing: {title}")
        result = analyze_video(vid, title, duration, topic or "general",
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
    print(f"\nAggregating results from {len(analyses)} videos...")
    agg = aggregate_results(analyses)

    # Print summary
    print("\n=== Content Type Impact on Retention ===\n")
    print(f"{'Type':<22} {'Avg Delta':>10} {'Count':>7} {'Positive%':>10}")
    print("-" * 52)
    for ct, stats in sorted(
        agg["by_content_type"].items(),
        key=lambda x: x[1]["avg_delta"],
        reverse=True,
    ):
        print(
            f"{ct:<22} {stats['avg_delta']:>+10.5f} {stats['count']:>7} "
            f"{stats['positive_pct']:>9.0f}%"
        )

    # Generate report
    if generate_markdown:
        report = generate_report(agg, analyses)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"\nReport written to: {REPORT_PATH}")

    return agg


def main():
    parser = argparse.ArgumentParser(
        description="Cross-video retention-to-script analysis tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.retention_analysis
  python -m tools.youtube_analytics.retention_analysis --video oDK52GwjTIo
  python -m tools.youtube_analytics.retention_analysis --report
  python -m tools.youtube_analytics.retention_analysis --cached --report""",
    )
    parser.add_argument(
        "--video", metavar="ID",
        help="Analyze a single video by ID",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Generate markdown report at channel-data/patterns/RETENTION-SCRIPT-CORRELATION.md",
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
