"""
Description SEO analyzer for History vs Hype.

Scrapes, caches, and analyzes YouTube video descriptions across competitor
channels and our own videos.  Outputs a cross-channel benchmark report.

Usage:
    python -m tools.benchmark.description_analyzer            # scrape + report
    python -m tools.benchmark.description_analyzer --scrape   # fetch missing descriptions only
    python -m tools.benchmark.description_analyzer --report   # generate analysis only (no scraping)
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from tools.logging_config import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
RAW_DIR = Path("tools/benchmark/raw_data")
ANALYTICS_DB = Path("tools/youtube_analytics/analytics.db")
METADATA_GLOB_ROOT = Path("video-projects")
OUTPUT_FILE = Path("channel-data/patterns/DESCRIPTION-SEO-ANALYSIS.md")

# Channels we consider "closest comparators" for detailed breakdown
CLOSEST_CHANNELS = {"Knowing Better", "Shaun", "Three Arrows", "WonderWhy", "Kraut"}

SKIP_JSON = {"verified_hooks.json", "en_gb_hooks.json", "all_channels_summary.json"}

# ---------------------------------------------------------------------------
# Stop words for keyword density
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "its", "this", "that", "was",
    "are", "be", "been", "has", "have", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "not", "no", "so",
    "if", "then", "than", "as", "up", "out", "about", "into", "over",
    "after", "before", "between", "through", "during", "all", "each",
    "every", "both", "few", "more", "most", "some", "any", "such", "only",
    "own", "other", "new", "old", "just", "also", "now", "here", "there",
    "when", "where", "how", "what", "which", "who", "whom", "why", "very",
    "too", "we", "our", "you", "your", "they", "their", "he", "she", "him",
    "her", "his", "my", "me", "i", "one", "two", "three", "four", "five",
    "first", "second", "like", "even", "still", "much", "many", "well",
    "back", "being", "those", "these", "were", "am", "yet", "us", "them",
    "while", "because", "since", "until", "once", "again", "further",
    "make", "made", "get", "got", "go", "went", "see", "come", "take",
    "know", "think", "say", "said", "tell", "let", "keep", "give", "find",
    "way", "use", "used", "part", "don", "doesn", "didn", "won", "http",
    "https", "www", "com", "youtube", "watch", "video", "subscribe",
    "channel", "follow", "patreon", "twitter", "instagram",
}


# ===================================================================
# Scraping helpers
# ===================================================================

def fetch_description_ytdlp(video_id: str) -> str | None:
    """Fetch a single video's description via yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = ["yt-dlp", "--dump-json", "--skip-download", "--no-warnings", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return data.get("description")
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        logger.warning("yt-dlp failed for %s: %s", video_id, exc)
    return None


def scrape_competitor_descriptions(top_n: int = 10) -> int:
    """Backfill descriptions into raw_data JSON files for top N videos per channel."""
    total_fetched = 0
    for fname in sorted(os.listdir(RAW_DIR)):
        if not fname.endswith(".json") or fname in SKIP_JSON:
            continue
        fpath = RAW_DIR / fname
        with open(fpath, encoding="utf-8") as f:
            channel_data = json.load(f)

        videos = channel_data.get("all_videos", channel_data.get("videos", []))
        if not videos:
            continue

        channel_name = channel_data.get("name", fname)

        # Sort by views, pick top N without descriptions
        ranked = sorted(videos, key=lambda v: v.get("view_count") or 0, reverse=True)
        need = [v for v in ranked[:top_n] if not v.get("description")]

        if not need:
            logger.info("%s — all top-%d already have descriptions", channel_name, top_n)
            continue

        logger.info("%s — fetching %d descriptions", channel_name, len(need))
        fetched = 0
        for v in need:
            vid_id = v.get("id")
            if not vid_id:
                continue
            desc = fetch_description_ytdlp(vid_id)
            if desc:
                v["description"] = desc
                fetched += 1
                safe = (v.get("title") or "")[:50]
                logger.info("  OK  %s  %s", vid_id, safe)
            else:
                logger.warning("  FAIL %s", vid_id)
            time.sleep(1)

        if fetched:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(channel_data, f, indent=2, ensure_ascii=False)
            logger.info("  Saved %d descriptions to %s", fetched, fpath)
        total_fetched += fetched

    return total_fetched


def scrape_own_descriptions() -> list[dict]:
    """Fetch descriptions for our published videos from YouTube."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return []

    conn = sqlite3.connect(str(ANALYTICS_DB))
    rows = conn.execute("SELECT video_id, title FROM videos").fetchall()
    conn.close()

    results = []
    logger.info("Fetching descriptions for %d own videos", len(rows))
    for vid_id, title in rows:
        desc = fetch_description_ytdlp(vid_id)
        if desc:
            results.append({"id": vid_id, "title": title, "description": desc, "source": "youtube"})
            safe = (title or "")[:50]
            logger.info("  OK  %s  %s", vid_id, safe)
        else:
            logger.warning("  FAIL %s %s", vid_id, title)
        time.sleep(1)

    return results


def load_metadata_descriptions() -> list[dict]:
    """Parse YOUTUBE-METADATA.md files for planned descriptions."""
    import glob as globmod
    results = []
    patterns = [
        str(METADATA_GLOB_ROOT / "**" / "*YOUTUBE-METADATA*.md"),
    ]
    found_files: list[str] = []
    for pat in patterns:
        found_files.extend(globmod.glob(pat, recursive=True))

    for fpath in sorted(set(found_files)):
        try:
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue

        # Extract description block: look for ## DESCRIPTION ... ``` ... ```
        desc_match = re.search(
            r"##\s*DESCRIPTION.*?\n```\n(.*?)\n```",
            content, re.DOTALL | re.IGNORECASE,
        )
        if not desc_match:
            # Alternate: ### Full Description ... ``` ... ```
            desc_match = re.search(
                r"###\s*Full Description.*?\n```\n(.*?)\n```",
                content, re.DOTALL | re.IGNORECASE,
            )
        if desc_match:
            desc_text = desc_match.group(1).strip()
            # Extract project name from path
            project = Path(fpath).parent.name
            results.append({
                "id": project,
                "title": project,
                "description": desc_text,
                "source": "metadata_file",
                "file": fpath,
            })

    logger.info("Loaded %d descriptions from YOUTUBE-METADATA files", len(results))
    return results


# ===================================================================
# Analysis helpers
# ===================================================================

def analyze_description(desc: str, title: str = "") -> dict[str, Any]:
    """Extract all metrics from a single description."""
    if not desc:
        return {"empty": True}

    lines = desc.strip().split("\n")
    words = desc.split()

    # Basic metrics
    char_count = len(desc)
    word_count = len(words)

    # First 2 lines (what shows before "Show More")
    first_2_lines = "\n".join(lines[:2]).strip()

    # Timestamps / chapters
    has_timestamps = bool(re.search(r"\d{1,2}:\d{2}", desc))

    # Source citations
    source_patterns = [
        r"\bsource", r"\breference", r"\bcitation", r"\bbibliography",
        r"university\s+press", r"\bpress,?\s+\d{4}", r"Oxford|Cambridge|Stanford|Harvard|Yale|Columbia|Princeton",
        r"ISBN\s", r"pp?\.\s*\d+",
    ]
    has_sources = any(re.search(p, desc, re.IGNORECASE) for p in source_patterns)

    # Hashtags
    hashtags = re.findall(r"#\w+", desc)
    hashtag_count = len(hashtags)
    # Position: check if hashtags appear in first 3 lines or at end
    first_3 = "\n".join(lines[:3])
    last_3 = "\n".join(lines[-3:]) if len(lines) >= 3 else desc
    hashtag_position = "none"
    if hashtag_count:
        in_first = bool(re.search(r"#\w+", first_3))
        in_last = bool(re.search(r"#\w+", last_3))
        if in_first and in_last:
            hashtag_position = "both"
        elif in_first:
            hashtag_position = "top"
        elif in_last:
            hashtag_position = "end"
        else:
            hashtag_position = "middle"

    # Links
    links = re.findall(r"https?://\S+", desc)
    link_count = len(links)

    # Call to action
    cta_patterns = [
        r"\bsubscribe\b", r"\bfollow\b", r"\bpatreon\b", r"\bsupport\b",
        r"\blike\b.*\bvideo\b", r"\bcomment\b.*below", r"\bbell\b",
        r"\bjoin\b.*\bmembership\b", r"\bnotification\b",
    ]
    has_cta = any(re.search(p, desc, re.IGNORECASE) for p in cta_patterns)

    # "About this video" section
    about_patterns = [
        r"in this video", r"this video is about", r"this video explores",
        r"this video covers", r"about this video", r"video summary",
        r"this video explains", r"we explore", r"we examine", r"we look at",
    ]
    has_about = any(re.search(p, desc, re.IGNORECASE) for p in about_patterns)

    # Keyword density (top 10 words excl stop words)
    combined_text = f"{title} {desc}".lower()
    all_words = re.findall(r"[a-z]{3,}", combined_text)
    filtered = [w for w in all_words if w not in STOP_WORDS and len(w) > 2]
    top_keywords = Counter(filtered).most_common(10)

    # Structure pattern
    if char_count < 100:
        structure = "minimal"
    elif char_count < 500:
        structure = "summary"
    elif char_count < 1500:
        structure = "detailed"
    else:
        structure = "comprehensive"

    return {
        "empty": False,
        "char_count": char_count,
        "word_count": word_count,
        "first_2_lines": first_2_lines,
        "has_timestamps": has_timestamps,
        "has_sources": has_sources,
        "hashtag_count": hashtag_count,
        "hashtag_position": hashtag_position,
        "link_count": link_count,
        "has_cta": has_cta,
        "has_about": has_about,
        "top_keywords": top_keywords,
        "structure": structure,
    }


def load_all_competitor_descriptions() -> dict[str, list[dict]]:
    """Load all descriptions from raw_data JSON files, grouped by channel."""
    by_channel: dict[str, list[dict]] = {}
    for fname in sorted(os.listdir(RAW_DIR)):
        if not fname.endswith(".json") or fname in SKIP_JSON:
            continue
        fpath = RAW_DIR / fname
        with open(fpath, encoding="utf-8") as f:
            channel_data = json.load(f)

        channel_name = channel_data.get("name", fname.replace(".json", ""))
        videos = channel_data.get("all_videos", channel_data.get("videos", []))
        entries = []
        for v in videos:
            desc = v.get("description")
            if desc:
                analysis = analyze_description(desc, v.get("title", ""))
                analysis["id"] = v.get("id")
                analysis["title"] = v.get("title", "")
                analysis["view_count"] = v.get("view_count", 0)
                analysis["description_raw"] = desc
                entries.append(analysis)
        by_channel[channel_name] = entries

    return by_channel


def aggregate_channel(entries: list[dict]) -> dict[str, Any]:
    """Compute channel-level aggregates from analyzed entries."""
    if not entries:
        return {
            "count": 0, "with_description": 0, "avg_chars": 0, "avg_words": 0,
            "pct_timestamps": 0, "pct_sources": 0, "pct_hashtags": 0,
            "pct_cta": 0, "pct_about": 0, "avg_links": 0,
            "structures": {}, "first_lines_sample": [],
        }

    n = len(entries)
    non_empty = [e for e in entries if not e.get("empty")]
    ne = len(non_empty) or 1

    avg_chars = sum(e.get("char_count", 0) for e in non_empty) / ne
    avg_words = sum(e.get("word_count", 0) for e in non_empty) / ne
    pct_ts = sum(1 for e in non_empty if e.get("has_timestamps")) / ne * 100
    pct_src = sum(1 for e in non_empty if e.get("has_sources")) / ne * 100
    pct_ht = sum(1 for e in non_empty if e.get("hashtag_count", 0) > 0) / ne * 100
    pct_cta = sum(1 for e in non_empty if e.get("has_cta")) / ne * 100
    pct_about = sum(1 for e in non_empty if e.get("has_about")) / ne * 100
    avg_links = sum(e.get("link_count", 0) for e in non_empty) / ne

    structs = Counter(e.get("structure", "unknown") for e in non_empty)

    # Most common first-line patterns
    first_lines = [e.get("first_2_lines", "")[:80] for e in non_empty if e.get("first_2_lines")]

    return {
        "count": n,
        "with_description": len(non_empty),
        "avg_chars": round(avg_chars),
        "avg_words": round(avg_words),
        "pct_timestamps": round(pct_ts, 1),
        "pct_sources": round(pct_src, 1),
        "pct_hashtags": round(pct_ht, 1),
        "pct_cta": round(pct_cta, 1),
        "pct_about": round(pct_about, 1),
        "avg_links": round(avg_links, 1),
        "structures": dict(structs.most_common()),
        "first_lines_sample": first_lines[:5],
    }


# ===================================================================
# Report generation
# ===================================================================

def generate_report(
    competitor_data: dict[str, list[dict]],
    own_youtube: list[dict],
    own_metadata: list[dict],
) -> str:
    """Generate the full markdown report."""
    sections: list[str] = []

    sections.append("# Description SEO Analysis\n")
    sections.append(f"*Generated: {time.strftime('%Y-%m-%d')}*\n")
    sections.append("Cross-channel benchmark of YouTube video descriptions: "
                     "structure, SEO patterns, and actionable recommendations.\n")

    # ----- 1. Cross-channel comparison table -----
    sections.append("---\n\n## 1. Cross-Channel Comparison\n")

    header = ("| Channel | Desc | Avg Chars | Avg Words | Timestamps | Sources | "
              "Hashtags | CTA | Links | Structure |")
    separator = ("|---|---|---|---|---|---|---|---|---|---|")
    rows = []

    channel_aggs: dict[str, dict] = {}
    for ch, entries in sorted(competitor_data.items()):
        agg = aggregate_channel(entries)
        channel_aggs[ch] = agg
        dominant_struct = max(agg["structures"], key=agg["structures"].get) if agg["structures"] else "—"
        rows.append(
            f"| {ch} | {agg['with_description']}/{agg['count']} "
            f"| {agg['avg_chars']:,} | {agg['avg_words']} "
            f"| {agg['pct_timestamps']:.0f}% | {agg['pct_sources']:.0f}% "
            f"| {agg['pct_hashtags']:.0f}% | {agg['pct_cta']:.0f}% "
            f"| {agg['avg_links']} | {dominant_struct} |"
        )

    # Our channel
    own_all = []
    for v in own_youtube:
        a = analyze_description(v.get("description", ""), v.get("title", ""))
        a["id"] = v.get("id")
        a["title"] = v.get("title", "")
        a["view_count"] = 0
        a["description_raw"] = v.get("description", "")
        own_all.append(a)
    own_agg = aggregate_channel(own_all)
    channel_aggs["**History vs Hype**"] = own_agg
    dominant_own = max(own_agg["structures"], key=own_agg["structures"].get) if own_agg["structures"] else "—"
    rows.append(
        f"| **History vs Hype** | {own_agg['with_description']}/{own_agg['count']} "
        f"| {own_agg['avg_chars']:,} | {own_agg['avg_words']} "
        f"| {own_agg['pct_timestamps']:.0f}% | {own_agg['pct_sources']:.0f}% "
        f"| {own_agg['pct_hashtags']:.0f}% | {own_agg['pct_cta']:.0f}% "
        f"| {own_agg['avg_links']} | {dominant_own} |"
    )

    sections.append(header)
    sections.append(separator)
    sections.extend(rows)
    sections.append("")

    # Niche averages
    all_comp_entries = [e for entries in competitor_data.values() for e in entries if not e.get("empty")]
    if all_comp_entries:
        n = len(all_comp_entries)
        sections.append(f"\n**Niche average** (n={n} descriptions across {len(competitor_data)} channels):")
        sections.append(f"- Avg length: {sum(e['char_count'] for e in all_comp_entries) / n:,.0f} chars / "
                        f"{sum(e['word_count'] for e in all_comp_entries) / n:,.0f} words")
        sections.append(f"- Timestamps: {sum(1 for e in all_comp_entries if e['has_timestamps']) / n * 100:.0f}%")
        sections.append(f"- Sources cited: {sum(1 for e in all_comp_entries if e['has_sources']) / n * 100:.0f}%")
        sections.append(f"- Hashtags: {sum(1 for e in all_comp_entries if e.get('hashtag_count', 0) > 0) / n * 100:.0f}%")
        sections.append(f"- CTA: {sum(1 for e in all_comp_entries if e['has_cta']) / n * 100:.0f}%")
        sections.append("")

    # ----- 2. Closest-match channel detail -----
    sections.append("---\n\n## 2. Closest-Match Channel Descriptions\n")
    sections.append("Detailed analysis of channels most similar to History vs Hype's format.\n")

    for ch_name in CLOSEST_CHANNELS:
        entries = competitor_data.get(ch_name, [])
        agg = channel_aggs.get(ch_name)
        if not agg or agg["count"] == 0:
            sections.append(f"### {ch_name}\n\n*No description data available. Run with `--scrape` to fetch.*\n")
            continue

        sections.append(f"### {ch_name}\n")
        sections.append(f"- **Descriptions analyzed:** {agg['with_description']}/{agg['count']}")
        sections.append(f"- **Avg length:** {agg['avg_chars']:,} chars / {agg['avg_words']} words")
        sections.append(f"- **Timestamps:** {agg['pct_timestamps']:.0f}%")
        sections.append(f"- **Source citations:** {agg['pct_sources']:.0f}%")
        sections.append(f"- **Hashtags:** {agg['pct_hashtags']:.0f}%")
        sections.append(f"- **CTA:** {agg['pct_cta']:.0f}%")
        sections.append(f"- **Avg links:** {agg['avg_links']}")
        sections.append(f"- **Dominant structure:** {max(agg['structures'], key=agg['structures'].get) if agg['structures'] else '—'}")

        if agg["first_lines_sample"]:
            sections.append("\n**First-line samples:**")
            for fl in agg["first_lines_sample"][:3]:
                sections.append(f"> {fl}")
        sections.append("")

    # ----- 3. Our descriptions vs benchmark -----
    sections.append("---\n\n## 3. Our Descriptions vs. Competitor Benchmark\n")

    if own_all:
        sections.append(f"**Videos analyzed:** {own_agg['with_description']}")
        sections.append(f"**Avg length:** {own_agg['avg_chars']:,} chars / {own_agg['avg_words']} words")

        # Compare to niche avg
        if all_comp_entries:
            niche_avg_chars = sum(e["char_count"] for e in all_comp_entries) / len(all_comp_entries)
            diff_pct = ((own_agg["avg_chars"] - niche_avg_chars) / niche_avg_chars * 100) if niche_avg_chars else 0
            direction = "above" if diff_pct > 0 else "below"
            sections.append(f"- Length vs niche: {abs(diff_pct):.0f}% {direction} average")
        sections.append(f"- Timestamps: {own_agg['pct_timestamps']:.0f}%")
        sections.append(f"- Sources: {own_agg['pct_sources']:.0f}%")
        sections.append(f"- Hashtags: {own_agg['pct_hashtags']:.0f}%")
        sections.append(f"- CTA: {own_agg['pct_cta']:.0f}%")
        sections.append("")
    else:
        sections.append("*No own video descriptions loaded. Run with `--scrape` to fetch from YouTube.*\n")

    # Also show metadata-file descriptions
    if own_metadata:
        sections.append(f"**From YOUTUBE-METADATA files:** {len(own_metadata)} descriptions found\n")
        for m in own_metadata[:5]:
            a = analyze_description(m["description"], m.get("title", ""))
            sections.append(f"- **{m['id']}**: {a.get('char_count', 0):,} chars, "
                            f"timestamps={'yes' if a.get('has_timestamps') else 'no'}, "
                            f"sources={'yes' if a.get('has_sources') else 'no'}, "
                            f"hashtags={a.get('hashtag_count', 0)}, "
                            f"structure={a.get('structure', '?')}")
        if len(own_metadata) > 5:
            sections.append(f"- *(+ {len(own_metadata) - 5} more)*")
        sections.append("")

    # ----- 4. Top 5 best descriptions by video performance -----
    sections.append("---\n\n## 4. Top 5 Best Descriptions (by Video Performance)\n")
    sections.append("Highest-viewed videos with descriptions available.\n")

    all_with_desc = []
    for ch, entries in competitor_data.items():
        for e in entries:
            if not e.get("empty") and e.get("description_raw"):
                all_with_desc.append((ch, e))

    all_with_desc.sort(key=lambda x: x[1].get("view_count", 0), reverse=True)

    for i, (ch, entry) in enumerate(all_with_desc[:5], 1):
        sections.append(f"### #{i}: {entry['title']}")
        sections.append(f"**Channel:** {ch} | **Views:** {entry.get('view_count', 0):,}")
        sections.append(f"**Length:** {entry['char_count']:,} chars | "
                        f"**Timestamps:** {'Yes' if entry['has_timestamps'] else 'No'} | "
                        f"**Sources:** {'Yes' if entry['has_sources'] else 'No'} | "
                        f"**Hashtags:** {entry.get('hashtag_count', 0)} | "
                        f"**Links:** {entry.get('link_count', 0)} | "
                        f"**Structure:** {entry.get('structure', '?')}")
        # Quote first 500 chars
        raw = entry["description_raw"]
        preview = raw[:500] + ("..." if len(raw) > 500 else "")
        sections.append(f"\n```\n{preview}\n```\n")

    if not all_with_desc:
        sections.append("*No descriptions available yet. Run with `--scrape` to fetch.*\n")

    # ----- 5. Recommendations -----
    sections.append("---\n\n## 5. Recommendations for Our Description Template\n")

    # Data-driven recommendations
    recs: list[str] = []

    if all_comp_entries:
        niche_ts_pct = sum(1 for e in all_comp_entries if e["has_timestamps"]) / len(all_comp_entries) * 100
        niche_src_pct = sum(1 for e in all_comp_entries if e["has_sources"]) / len(all_comp_entries) * 100
        niche_ht_pct = sum(1 for e in all_comp_entries if e.get("hashtag_count", 0) > 0) / len(all_comp_entries) * 100
        niche_cta_pct = sum(1 for e in all_comp_entries if e["has_cta"]) / len(all_comp_entries) * 100
        niche_avg_chars = sum(e["char_count"] for e in all_comp_entries) / len(all_comp_entries)

        if niche_ts_pct > 50:
            recs.append(f"1. **Always include timestamps/chapters.** {niche_ts_pct:.0f}% of niche videos use them. "
                        "YouTube uses chapters for search snippets and suggested video cards.")
        else:
            recs.append(f"1. **Timestamps are optional in this niche** ({niche_ts_pct:.0f}% usage), "
                        "but still recommended for viewer experience and search snippets.")

        if niche_src_pct > 30:
            recs.append(f"2. **Cite sources in description.** {niche_src_pct:.0f}% of niche does this. "
                        "This is our competitive advantage — lean into it harder than competitors.")
        else:
            recs.append(f"2. **Source citations are rare in niche** ({niche_src_pct:.0f}%), "
                        "so including them differentiates us. Keep doing it.")

        recs.append(f"3. **Target description length:** {niche_avg_chars:,.0f} chars (niche average). "
                    "Comprehensive descriptions (1500+) correlate with educational channels.")

        if niche_ht_pct > 40:
            recs.append(f"4. **Use hashtags.** {niche_ht_pct:.0f}% of niche uses them. "
                        "Place 3-8 hashtags at the END of description (not first line).")
        else:
            recs.append(f"4. **Hashtags are used by {niche_ht_pct:.0f}% of niche.** "
                        "Include 3-5 relevant hashtags at the end for discoverability.")

        recs.append("5. **First 2 lines are critical.** They appear in search results and above the fold. "
                    "Lead with the thesis or a specific claim, NOT a generic topic summary.")

    else:
        recs.append("*Run with `--scrape` to populate competitor data for data-driven recommendations.*")

    for r in recs:
        sections.append(r)
    sections.append("")

    # ----- 6. Description formula -----
    sections.append("---\n\n## 6. Description Formula\n")
    sections.append("Based on top-performing competitors and niche patterns:\n")
    sections.append("```")
    sections.append("LINE 1: Thesis statement or strongest specific claim (this shows in search)")
    sections.append("LINE 2: What this video covers / unique angle (second search-visible line)")
    sections.append("")
    sections.append("PARAGRAPH: 2-4 sentence summary expanding on the thesis.")
    sections.append("Include the main keyword naturally 2-3 times.")
    sections.append("")
    sections.append("TIMESTAMPS")
    sections.append("0:00 - [Chapter title]")
    sections.append("X:XX - [Chapter title]")
    sections.append("...")
    sections.append("")
    sections.append("SOURCES")
    sections.append("[Academic citations with author, title, publisher, year, page numbers]")
    sections.append("[Primary document references]")
    sections.append("")
    sections.append("[1-line subscribe CTA]")
    sections.append("")
    sections.append("#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5")
    sections.append("```\n")

    sections.append("**Key principles:**")
    sections.append("- First 2 lines = SEO real estate. No wasted words.")
    sections.append("- Timestamps = chapters in YouTube UI. Always include for videos >5 min.")
    sections.append("- Sources section = trust signal AND keyword density (author names, book titles).")
    sections.append("- Hashtags at END, not beginning (YouTube shows first 3 hashtags above title if in first lines).")
    sections.append("- Target 1000-2000 chars total for comprehensive/educational content.")
    sections.append("")

    return "\n".join(sections)


# ===================================================================
# Main
# ===================================================================

def main():
    parser = argparse.ArgumentParser(description="Description SEO analyzer")
    parser.add_argument("--scrape", action="store_true",
                        help="Fetch missing descriptions via yt-dlp")
    parser.add_argument("--report", action="store_true",
                        help="Generate analysis report only (no scraping)")
    parser.add_argument("--top-n", type=int, default=10,
                        help="Number of top videos per channel to scrape (default: 10)")
    args = parser.parse_args()

    # Default: both scrape and report
    do_scrape = not args.report  # scrape unless --report only
    do_report = not args.scrape  # report unless --scrape only
    if not args.scrape and not args.report:
        do_scrape = True
        do_report = True

    # --- Scrape phase ---
    own_youtube: list[dict] = []
    if do_scrape:
        logger.info("=== Scraping competitor descriptions ===")
        fetched = scrape_competitor_descriptions(top_n=args.top_n)
        logger.info("Fetched %d new competitor descriptions", fetched)

        logger.info("\n=== Scraping own descriptions from YouTube ===")
        own_youtube = scrape_own_descriptions()
        logger.info("Fetched %d own descriptions", len(own_youtube))

    # --- Report phase ---
    if do_report:
        logger.info("\n=== Generating report ===")

        competitor_data = load_all_competitor_descriptions()
        total_desc = sum(len(v) for v in competitor_data.values())
        logger.info("Loaded %d competitor descriptions across %d channels",
                     total_desc, len(competitor_data))

        own_metadata = load_metadata_descriptions()

        # If we didn't scrape this run, try to load cached own descriptions
        # (user might have run --scrape previously then --report separately)
        if not own_youtube:
            # No cached own-youtube store; own_youtube stays empty
            # The report will note this and suggest --scrape
            pass

        report = generate_report(competitor_data, own_youtube, own_metadata)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(report)

        logger.info("Report written to %s", OUTPUT_FILE)


if __name__ == "__main__":
    from tools.logging_config import setup_logging
    setup_logging(verbose=False, quiet=False)
    main()
