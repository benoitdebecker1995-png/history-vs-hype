"""
Retention-by-Topic-Type Analysis

Breaks down retention curves and content-type deltas by topic category
(territorial, ideological, colonial, explainer) using real cached retention
data and SRT content classification.

Usage:
    python -m tools.youtube_analytics.retention_by_topic
"""

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "tools" / "youtube_analytics" / "analytics.db"
CACHE_DIR = BASE_DIR / "tools" / "youtube_analytics" / "_retention_cache"
OUTPUT_PATH = BASE_DIR / "channel-data" / "patterns" / "RETENTION-BY-TOPIC-TYPE.md"

# Import content classification from retention_analysis
from .retention_analysis import (
    classify_content,
    classify_window,
    build_srt_mapping,
    parse_srt,
)

# ---------------------------------------------------------------------------
# Topic classification
# ---------------------------------------------------------------------------

TOPIC_KEYWORDS = {
    "territorial": [
        "vs", "dispute", "border", "territory", "island", "claim", "icj",
        "treaty", "wall", "sea", "islands", "sovereignty", "division",
        "gibraltar", "kashmir", "belize", "guatemala", "guyana", "essequibo",
        "cyprus", "bermeja", "sahara", "bir tawil", "south china",
        "georgia", "ukraine", "taiwan", "missing island",
    ],
    "ideological": [
        "myth", "fact-check", "claims", "narrative", "propaganda", "proof",
        "evidence", "busted", "busted!", "debunk", "never happened",
        "erased", "dangerous", "playbook", "copied", "purged",
        "destroy", "crusades", "nato promised", "flat earth",
        "pagans", "christmas", "lagertha", "viking warriors",
        "weaponized", "kgb",
    ],
    "colonial": [
        "colonial", "empire", "independence", "africa", "coups", "control",
        "cia", "condor", "genocide", "stock exchange", "french control",
        "ethnic groups", "berlin conference", "expelled", "chagos",
    ],
    "explainer": [
        "how", "why", "origins", "history", "explained", "what happened",
        "democracy", "revolutions", "invented", "human rights",
        "tariff", "walked back", "ancient hatreds",
    ],
}


def classify_topic(title: str, db_topic_type: str) -> str:
    """
    Classify a video into a topic type based on title keywords.
    Falls back to db_topic_type mapping if no keyword match.
    """
    title_lower = title.lower()

    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in title_lower:
                score += 1
        scores[topic] = score

    best = max(scores, key=scores.get)
    if scores[best] > 0:
        # If there's a tie or close match, use db_topic_type as tiebreaker
        tied = [t for t, s in scores.items() if s == scores[best]]
        if len(tied) > 1:
            # Use DB topic_type as tiebreaker
            db_map = {
                "territorial": "territorial",
                "ideological": "ideological",
                "colonial": "colonial",
                "factcheck": "ideological",
                "legal": "colonial",
                "general": None,
            }
            mapped = db_map.get(db_topic_type)
            if mapped and mapped in tied:
                return mapped
        return best

    # No keyword match — map from DB topic_type
    db_map = {
        "territorial": "territorial",
        "ideological": "ideological",
        "colonial": "colonial",
        "factcheck": "ideological",
        "legal": "colonial",
        "general": "explainer",
    }
    return db_map.get(db_topic_type, "explainer")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_all_videos():
    """Load video metadata from DB, filtered to long-form with retention cache."""
    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(DB_PATH) as store:
        rows = store.videos(min_duration_seconds=121)  # preserve old `> 120`

    # Filter to videos that have retention cache
    cached_ids = {p.stem for p in CACHE_DIR.glob("*.json")}
    videos = []
    for r in rows:
        vid_id, title, duration, views, topic_type = (
            r['video_id'], r['title'], r['duration_seconds'], r['views'], r['topic_type']
        )
        if vid_id in cached_ids:
            videos.append({
                "video_id": vid_id,
                "title": title,
                "duration": duration,
                "views": views,
                "db_topic_type": topic_type or "general",
            })
    return videos


def load_retention(video_id: str) -> list[dict] | None:
    """Load retention data points from cache."""
    p = CACHE_DIR / f"{video_id}.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("data_points", [])
    except (json.JSONDecodeError, KeyError):
        return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze_retention_curve(data_points: list[dict]) -> dict:
    """Analyze a single retention curve."""
    if not data_points:
        return {}

    positions = [dp["position"] for dp in data_points]
    retentions = [dp["retention"] for dp in data_points]

    # Final retention
    final_retention = retentions[-1] if retentions else 0

    # Intro drop: retention lost in first 10% of video
    intro_points = [dp for dp in data_points if dp["position"] <= 0.10]
    if intro_points and retentions[0] > 0:
        intro_drop = (retentions[0] - intro_points[-1]["retention"]) / retentions[0]
    else:
        intro_drop = 0

    # Stabilization point: first position where consecutive drop < 0.5%
    stabilization = None
    for i in range(1, len(retentions)):
        if abs(retentions[i] - retentions[i - 1]) < 0.005:
            stabilization = positions[i]
            break

    return {
        "final_retention": final_retention,
        "intro_drop_pct": intro_drop,
        "stabilization_position": stabilization,
        "curve": list(zip(positions, retentions)),
    }


def compute_avg_curve(all_curves: list[list[tuple]]) -> list[tuple]:
    """Compute average retention at each position across multiple curves."""
    # Collect all unique positions, then average retention at each
    pos_values = defaultdict(list)
    for curve in all_curves:
        for pos, ret in curve:
            # Round position to 2 decimal places for alignment
            pos_key = round(pos, 2)
            pos_values[pos_key].append(ret)

    avg_curve = []
    for pos in sorted(pos_values.keys()):
        vals = pos_values[pos]
        avg_curve.append((pos, sum(vals) / len(vals), len(vals)))

    return avg_curve


def analyze_content_deltas_by_topic(
    topic_videos: dict[str, list[dict]],
    srt_mapping: dict[str, Path],
) -> dict[str, dict[str, dict]]:
    """
    For each topic type, compute content-type retention deltas.

    Returns:
        {topic_type: {content_type: {avg_delta, count, avg_retention}}}
    """
    results = {}

    for topic_type, videos in topic_videos.items():
        content_deltas = defaultdict(list)
        content_retentions = defaultdict(list)
        mapped_count = 0

        for video in videos:
            vid_id = video["video_id"]
            if vid_id not in srt_mapping:
                continue

            srt_path = srt_mapping[vid_id]
            segments = parse_srt(srt_path)
            if not segments:
                continue

            data_points = load_retention(vid_id)
            if not data_points or len(data_points) < 10:
                continue

            duration = video["duration"]
            mapped_count += 1

            # Map each retention data point to content type
            for i, dp in enumerate(data_points):
                pos = dp["position"]
                ret = dp["retention"]
                timestamp = pos * duration

                content_type, _ = classify_window(segments, timestamp)
                content_retentions[content_type].append(ret)

                # Delta from previous point
                if i > 0:
                    prev_ret = data_points[i - 1]["retention"]
                    delta = ret - prev_ret
                    content_deltas[content_type].append(delta)

        # Compute averages
        topic_results = {}
        for ct in sorted(set(list(content_deltas.keys()) + list(content_retentions.keys()))):
            deltas = content_deltas.get(ct, [])
            rets = content_retentions.get(ct, [])
            topic_results[ct] = {
                "avg_delta": sum(deltas) / len(deltas) if deltas else 0,
                "count": len(deltas),
                "avg_retention": sum(rets) / len(rets) if rets else 0,
                "positive_rate": sum(1 for d in deltas if d > 0) / len(deltas) if deltas else 0,
            }

        results[topic_type] = {
            "content_types": topic_results,
            "videos_with_srt": mapped_count,
        }

    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    topic_groups: dict[str, list[dict]],
    topic_curves: dict[str, dict],
    content_deltas: dict[str, dict],
) -> str:
    """Generate markdown report."""
    lines = [
        "# Retention by Topic Type",
        "",
        f"**Generated:** 2026-03-21 | **Source:** {len(sum(topic_groups.values(), []))} videos with retention data",
        "",
        "## Summary",
        "",
        "| Topic Type | Videos | Avg Final Retention | Avg Intro Drop | Stabilization |",
        "|------------|--------|--------------------:|---------------:|--------------:|",
    ]

    for topic in ["territorial", "ideological", "colonial", "explainer"]:
        if topic not in topic_curves:
            continue
        stats = topic_curves[topic]
        n = len(topic_groups[topic])
        conf = "LOW" if n < 5 else ""
        stab = f"{stats['avg_stabilization']:.0%}" if stats.get("avg_stabilization") else "N/A"
        lines.append(
            f"| {topic} | {n}{' (' + conf + ')' if conf else ''} | "
            f"{stats['avg_final_retention']:.1%} | "
            f"{stats['avg_intro_drop']:.1%} | "
            f"{stab} |"
        )

    lines.extend(["", "---", ""])

    # Per-topic sections
    for topic in ["territorial", "ideological", "colonial", "explainer"]:
        if topic not in topic_groups:
            continue
        videos = topic_groups[topic]
        stats = topic_curves[topic]

        lines.extend([
            f"## {topic.title()} Videos (n={len(videos)})",
            "",
            "### Videos in this category",
            "",
        ])

        for v in sorted(videos, key=lambda x: x["views"], reverse=True):
            lines.append(f"- **{v['title']}** ({v['views']:,} views, {v['duration']}s)")

        lines.extend([
            "",
            "### Retention Curve (sampled at key positions)",
            "",
            "| Position | Avg Retention | Videos at Position |",
            "|----------|-------------:|---------:|",
        ])

        # Sample key positions from average curve
        avg_curve = stats.get("avg_curve", [])
        sample_positions = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
        for target_pos in sample_positions:
            # Find closest position in curve
            closest = min(avg_curve, key=lambda x: abs(x[0] - target_pos), default=None)
            if closest and abs(closest[0] - target_pos) < 0.03:
                lines.append(f"| {closest[0]:.0%} | {closest[1]:.1%} | {closest[2]} |")

        lines.append("")

        # Content deltas for this topic
        if topic in content_deltas and content_deltas[topic]["videos_with_srt"] > 0:
            cd = content_deltas[topic]
            lines.extend([
                f"### Content-Type Retention Deltas (from {cd['videos_with_srt']} videos with SRT)",
                "",
                "| Content Type | Avg Delta | Avg Retention | Positive Rate | Observations |",
                "|-------------|----------:|--------------:|--------------:|------|",
            ])

            for ct, data in sorted(cd["content_types"].items(), key=lambda x: x[1]["avg_delta"], reverse=True):
                if data["count"] < 3:
                    continue
                lines.append(
                    f"| {ct} | {data['avg_delta']:+.4f} | "
                    f"{data['avg_retention']:.1%} | "
                    f"{data['positive_rate']:.0%} | "
                    f"n={data['count']} |"
                )

            lines.append("")
        else:
            srt_count = content_deltas.get(topic, {}).get("videos_with_srt", 0)
            lines.extend([
                f"### Content-Type Retention Deltas",
                f"",
                f"*No SRT files matched for this topic type ({srt_count} videos mapped).*",
                "",
            ])

        lines.extend(["---", ""])

    # Cross-topic comparison
    lines.extend([
        "## Cross-Topic Content Delta Comparison",
        "",
        "How the same content type performs differently across topic types:",
        "",
    ])

    # Get all content types across all topics
    all_cts = set()
    for topic_data in content_deltas.values():
        all_cts.update(topic_data.get("content_types", {}).keys())

    if all_cts:
        header = "| Content Type |"
        sep = "|-------------|"
        for topic in ["territorial", "ideological", "colonial", "explainer"]:
            if topic in content_deltas and content_deltas[topic]["videos_with_srt"] > 0:
                header += f" {topic.title()} |"
                sep += "----------:|"

        lines.append(header)
        lines.append(sep)

        for ct in sorted(all_cts):
            row = f"| {ct} |"
            for topic in ["territorial", "ideological", "colonial", "explainer"]:
                if topic in content_deltas and content_deltas[topic]["videos_with_srt"] > 0:
                    data = content_deltas[topic].get("content_types", {}).get(ct)
                    if data and data["count"] >= 3:
                        row += f" {data['avg_delta']:+.4f} (n={data['count']}) |"
                    else:
                        row += " — |"
            lines.append(row)

        lines.append("")

    # Key findings
    lines.extend([
        "## Key Findings",
        "",
    ])

    # Auto-generate findings
    findings = []

    # 1. Which topic retains best?
    best_topic = max(
        [(t, s["avg_final_retention"]) for t, s in topic_curves.items()],
        key=lambda x: x[1],
    )
    worst_topic = min(
        [(t, s["avg_final_retention"]) for t, s in topic_curves.items()],
        key=lambda x: x[1],
    )
    findings.append(
        f"**Best final retention:** {best_topic[0]} ({best_topic[1]:.1%}) vs "
        f"worst: {worst_topic[0]} ({worst_topic[1]:.1%})"
    )

    # 2. Intro drop comparison
    least_drop = min(
        [(t, s["avg_intro_drop"]) for t, s in topic_curves.items()],
        key=lambda x: x[1],
    )
    most_drop = max(
        [(t, s["avg_intro_drop"]) for t, s in topic_curves.items()],
        key=lambda x: x[1],
    )
    findings.append(
        f"**Smallest intro drop:** {least_drop[0]} ({least_drop[1]:.1%}) vs "
        f"largest: {most_drop[0]} ({most_drop[1]:.1%})"
    )

    # 3. Content type differences across topics
    for ct in ["statistic", "quote", "narration", "modern_relevance"]:
        deltas_by_topic = {}
        for topic in ["territorial", "ideological", "colonial", "explainer"]:
            td = content_deltas.get(topic, {}).get("content_types", {}).get(ct)
            if td and td["count"] >= 3:
                deltas_by_topic[topic] = td["avg_delta"]
        if len(deltas_by_topic) >= 2:
            best_ct = max(deltas_by_topic, key=deltas_by_topic.get)
            worst_ct = min(deltas_by_topic, key=deltas_by_topic.get)
            if best_ct != worst_ct:
                findings.append(
                    f"**{ct}:** performs best in {best_ct} ({deltas_by_topic[best_ct]:+.4f}) "
                    f"vs worst in {worst_ct} ({deltas_by_topic[worst_ct]:+.4f})"
                )

    for f in findings:
        lines.append(f"- {f}")

    lines.extend([
        "",
        "---",
        "",
        "*Analysis uses cached retention data and SRT content classification from retention_analysis.py.*",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading video data...")
    videos = load_all_videos()
    print(f"  Found {len(videos)} long-form videos with retention cache")

    # Classify by topic
    topic_groups = defaultdict(list)
    for v in videos:
        topic = classify_topic(v["title"], v["db_topic_type"])
        v["topic_type"] = topic
        topic_groups[topic].append(v)

    print("\nTopic classification:")
    for topic in ["territorial", "ideological", "colonial", "explainer"]:
        vids = topic_groups.get(topic, [])
        print(f"  {topic}: {len(vids)} videos")
        for v in vids:
            print(f"    - {v['title']}")

    # Analyze retention curves per topic
    print("\nAnalyzing retention curves...")
    topic_curves = {}
    for topic, vids in topic_groups.items():
        all_analyses = []
        all_curve_data = []

        for v in vids:
            dp = load_retention(v["video_id"])
            if not dp:
                continue
            analysis = analyze_retention_curve(dp)
            if analysis:
                all_analyses.append(analysis)
                all_curve_data.append(analysis["curve"])

        if all_analyses:
            avg_final = sum(a["final_retention"] for a in all_analyses) / len(all_analyses)
            avg_intro = sum(a["intro_drop_pct"] for a in all_analyses) / len(all_analyses)
            stab_vals = [a["stabilization_position"] for a in all_analyses if a.get("stabilization_position")]
            avg_stab = sum(stab_vals) / len(stab_vals) if stab_vals else None

            avg_curve = compute_avg_curve(all_curve_data)

            topic_curves[topic] = {
                "avg_final_retention": avg_final,
                "avg_intro_drop": avg_intro,
                "avg_stabilization": avg_stab,
                "avg_curve": avg_curve,
            }

            print(f"  {topic}: final={avg_final:.1%}, intro_drop={avg_intro:.1%}, n={len(all_analyses)}")

    # Content-type deltas by topic
    print("\nBuilding SRT mapping...")
    srt_mapping = build_srt_mapping()
    print(f"  Mapped {len(srt_mapping)} videos to SRT files")

    print("\nAnalyzing content-type deltas by topic...")
    content_deltas = analyze_content_deltas_by_topic(topic_groups, srt_mapping)

    for topic, data in content_deltas.items():
        n_srt = data["videos_with_srt"]
        print(f"  {topic}: {n_srt} videos with SRT data")

    # Generate report
    print("\nGenerating report...")
    report = generate_report(topic_groups, topic_curves, content_deltas)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
