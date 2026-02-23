"""
competitor_patterns.py — Cross-competitor topic cluster analysis

Classifies 1,000+ competitor videos by topic cluster and title formula,
then analyses which combinations drive outlier performance. Also identifies
gap opportunities (topics competitors cover but this channel doesn't).

Public API:
    classify_all_videos(db_path)           -> dict  (classify + persist)
    analyze_cluster_performance(db_path)   -> dict  (per-cluster stats)
    analyze_formula_performance(db_path)   -> dict  (formula x cluster)
    find_gaps(db_path, keywords_db_path)   -> list  (uncovered topics)
    get_pattern_report(db_path, keywords_db_path) -> str  (full Markdown)

All public functions follow the error-dict pattern: return {'error': msg}
on failure, never raise.
"""

import json
import sqlite3
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from tools.intel.topic_vocabulary import classify_title, primary_topic, detect_formulas

# Default paths
_INTEL_DIR = Path(__file__).parent
_DEFAULT_DB_PATH = str(_INTEL_DIR / "intel.db")
_DEFAULT_KEYWORDS_DB = str(_INTEL_DIR.parent / "discovery" / "keywords.db")


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_all_videos(db_path: str = None) -> dict:
    """
    Classify every competitor video by topic cluster and persist to DB.

    Reads all competitor_videos, runs classify_title() on each, stores the
    result as JSON in the topic_cluster column.

    Returns:
        {
            'classified': int,
            'distribution': {cluster: count, ...},
        }
        or {'error': str}
    """
    resolved = db_path or _DEFAULT_DB_PATH
    try:
        conn = _connect(resolved)
        rows = conn.execute("SELECT video_id, title, description FROM competitor_videos").fetchall()

        cluster_counter: Counter = Counter()
        classified = 0

        for row in rows:
            vid_id = row["video_id"]
            title = row["title"] or ""
            desc = row["description"] or ""
            clusters = classify_title(title, desc)
            topic = primary_topic(title, desc)

            cluster_counter[topic] += 1
            for c in clusters:
                if c != topic:
                    cluster_counter[c] += 1

            conn.execute(
                "UPDATE competitor_videos SET topic_cluster = ? WHERE video_id = ?",
                (json.dumps(clusters if clusters else [topic]), vid_id),
            )
            classified += 1

        conn.commit()
        conn.close()
        return {
            "classified": classified,
            "distribution": dict(cluster_counter.most_common()),
        }
    except Exception as exc:
        return {"error": f"classify_all_videos failed: {exc}"}


# ---------------------------------------------------------------------------
# Cluster performance analysis
# ---------------------------------------------------------------------------

def analyze_cluster_performance(db_path: str = None) -> dict:
    """
    Per-cluster: avg views, outlier rate, top videos, duration sweet spot.

    Returns:
        {
            cluster_name: {
                'video_count': int,
                'avg_views': float,
                'median_views': float,
                'outlier_count': int,
                'outlier_rate': float,       # 0.0-1.0
                'avg_duration_min': float,
                'top_videos': [{title, views, channel_id}, ...],  # top 3
            },
            ...
        }
        or {'error': str}
    """
    resolved = db_path or _DEFAULT_DB_PATH
    try:
        conn = _connect(resolved)
        rows = conn.execute(
            "SELECT video_id, title, channel_id, views, duration_seconds, "
            "is_outlier, topic_cluster FROM competitor_videos "
            "WHERE topic_cluster IS NOT NULL"
        ).fetchall()
        conn.close()

        # Group videos by cluster
        cluster_videos: dict[str, list] = defaultdict(list)
        for row in rows:
            clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []
            vid = dict(row)
            for cluster in clusters:
                cluster_videos[cluster].append(vid)

        result = {}
        for cluster, vids in sorted(cluster_videos.items(), key=lambda x: -len(x[1])):
            views_list = [v["views"] for v in vids if v["views"] and v["views"] > 0]
            durations = [v["duration_seconds"] for v in vids if v["duration_seconds"]]
            outlier_count = sum(1 for v in vids if v.get("is_outlier"))

            avg_views = round(statistics.mean(views_list), 0) if views_list else 0
            median_views = round(statistics.median(views_list), 0) if views_list else 0
            avg_dur = round(statistics.mean(durations) / 60, 1) if durations else 0

            # Top 3 by views
            sorted_vids = sorted(vids, key=lambda v: v.get("views") or 0, reverse=True)
            top = [
                {"title": v["title"][:60], "views": v["views"], "channel_id": v["channel_id"]}
                for v in sorted_vids[:3]
            ]

            result[cluster] = {
                "video_count": len(vids),
                "avg_views": avg_views,
                "median_views": median_views,
                "outlier_count": outlier_count,
                "outlier_rate": round(outlier_count / len(vids), 3) if vids else 0,
                "avg_duration_min": avg_dur,
                "top_videos": top,
            }

        return result
    except Exception as exc:
        return {"error": f"analyze_cluster_performance failed: {exc}"}


# ---------------------------------------------------------------------------
# Formula x cluster performance
# ---------------------------------------------------------------------------

def analyze_formula_performance(db_path: str = None) -> dict:
    """
    Which title formulas x clusters produce the highest views?

    Returns:
        {
            formula: {
                'video_count': int,
                'avg_views': float,
                'outlier_rate': float,
                'top_cluster': str,
            },
            ...
        }
        or {'error': str}
    """
    resolved = db_path or _DEFAULT_DB_PATH
    try:
        conn = _connect(resolved)
        rows = conn.execute(
            "SELECT title, views, is_outlier, topic_cluster FROM competitor_videos"
        ).fetchall()
        conn.close()

        formula_data: dict[str, list] = defaultdict(list)
        formula_cluster: dict[str, Counter] = defaultdict(Counter)

        for row in rows:
            title = row["title"] or ""
            formulas = detect_formulas(title)
            clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []

            for f in formulas:
                formula_data[f].append({
                    "views": row["views"] or 0,
                    "is_outlier": bool(row["is_outlier"]),
                })
                for c in clusters:
                    formula_cluster[f][c] += 1

        result = {}
        for formula, vids in sorted(formula_data.items(), key=lambda x: -len(x[1])):
            views_list = [v["views"] for v in vids if v["views"] > 0]
            outliers = sum(1 for v in vids if v["is_outlier"])
            top_cluster = formula_cluster[formula].most_common(1)

            result[formula] = {
                "video_count": len(vids),
                "avg_views": round(statistics.mean(views_list), 0) if views_list else 0,
                "outlier_rate": round(outliers / len(vids), 3) if vids else 0,
                "top_cluster": top_cluster[0][0] if top_cluster else "general",
            }

        return result
    except Exception as exc:
        return {"error": f"analyze_formula_performance failed: {exc}"}


# ---------------------------------------------------------------------------
# Gap analysis
# ---------------------------------------------------------------------------

def find_gaps(db_path: str = None, keywords_db_path: str = None) -> list:
    """
    Find competitor topics this channel isn't covering.

    Compares competitor video topic_clusters against own-channel
    video_performance.topic_type from keywords.db.

    Returns:
        [
            {
                'cluster': str,
                'competitor_count': int,
                'competitor_outlier_rate': float,
                'own_count': int,
                'gap_score': float,   # higher = bigger opportunity
            },
            ...
        ]
        Sorted by gap_score descending. Returns {'error': str} on failure.
    """
    resolved_intel = db_path or _DEFAULT_DB_PATH
    resolved_kw = keywords_db_path or _DEFAULT_KEYWORDS_DB
    try:
        # Competitor cluster counts
        conn = _connect(resolved_intel)
        rows = conn.execute(
            "SELECT topic_cluster, is_outlier FROM competitor_videos WHERE topic_cluster IS NOT NULL"
        ).fetchall()
        conn.close()

        comp_count: Counter = Counter()
        comp_outliers: Counter = Counter()
        for row in rows:
            clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []
            for c in clusters:
                comp_count[c] += 1
                if row["is_outlier"]:
                    comp_outliers[c] += 1

        # Own channel topic types
        own_count: Counter = Counter()
        if Path(resolved_kw).exists():
            kw_conn = sqlite3.connect(resolved_kw)
            kw_conn.row_factory = sqlite3.Row
            own_rows = kw_conn.execute(
                "SELECT topic_type, title FROM video_performance"
            ).fetchall()
            kw_conn.close()

            for row in own_rows:
                # Classify own titles with the unified vocabulary too
                title = row["title"] or ""
                clusters = classify_title(title)
                for c in clusters:
                    own_count[c] += 1

        # Build gap list
        gaps = []
        for cluster, c_count in comp_count.most_common():
            o_count = own_count.get(cluster, 0)
            outlier_rate = comp_outliers[cluster] / c_count if c_count > 0 else 0

            # Gap score: high competitor volume + high outlier rate + low own coverage
            coverage_penalty = min(o_count / max(c_count * 0.1, 1), 1.0)
            gap_score = round(c_count * (1 + outlier_rate * 5) * (1 - coverage_penalty * 0.7), 1)

            gaps.append({
                "cluster": cluster,
                "competitor_count": c_count,
                "competitor_outlier_rate": round(outlier_rate, 3),
                "own_count": o_count,
                "gap_score": gap_score,
            })

        gaps.sort(key=lambda g: g["gap_score"], reverse=True)
        return gaps

    except Exception as exc:
        return {"error": f"find_gaps failed: {exc}"}


# ---------------------------------------------------------------------------
# Full pattern report (Markdown)
# ---------------------------------------------------------------------------

def get_pattern_report(db_path: str = None, keywords_db_path: str = None) -> str:
    """
    Generate the full Markdown pattern report for /intel --patterns.

    Sections:
        1. Topic Cluster Performance (table)
        2. Title Formula Performance (table)
        3. Gap Opportunities (table)
        4. Top Outlier Videos by Cluster

    Returns:
        Formatted Markdown string ready for display.
    """
    resolved_db = db_path or _DEFAULT_DB_PATH
    resolved_kw = keywords_db_path or _DEFAULT_KEYWORDS_DB

    lines = ["## Competitor Pattern Analysis\n"]

    # Ensure videos are classified
    conn = _connect(resolved_db)
    unclassified = conn.execute(
        "SELECT COUNT(*) FROM competitor_videos WHERE topic_cluster IS NULL"
    ).fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM competitor_videos").fetchone()[0]
    conn.close()

    if unclassified > total * 0.5:
        # More than half unclassified — run classification first
        classify_result = classify_all_videos(resolved_db)
        if isinstance(classify_result, dict) and "error" in classify_result:
            lines.append(f"*Classification error: {classify_result['error']}*\n")
        else:
            lines.append(f"*Classified {classify_result.get('classified', 0)} videos*\n")

    # --- Section 1: Cluster performance ---
    cluster_perf = analyze_cluster_performance(resolved_db)
    if isinstance(cluster_perf, dict) and "error" not in cluster_perf and cluster_perf:
        lines.append("### Topic Cluster Performance\n")
        lines.append("| Cluster | Videos | Avg Views | Outlier Rate | Avg Duration |")
        lines.append("| ------- | ------:| ---------:| ------------:| ------------:|")

        sorted_clusters = sorted(
            cluster_perf.items(),
            key=lambda x: x[1]["avg_views"],
            reverse=True,
        )
        for cluster, stats in sorted_clusters[:15]:
            rate_pct = f"{stats['outlier_rate'] * 100:.1f}%"
            lines.append(
                f"| {cluster} | {stats['video_count']} | "
                f"{stats['avg_views']:,.0f} | {rate_pct} | "
                f"{stats['avg_duration_min']:.0f} min |"
            )
        lines.append("")

    # --- Section 2: Formula performance ---
    formula_perf = analyze_formula_performance(resolved_db)
    if isinstance(formula_perf, dict) and "error" not in formula_perf and formula_perf:
        lines.append("### Title Formula Performance\n")
        lines.append("| Formula | Videos | Avg Views | Outlier Rate | Top Cluster |")
        lines.append("| ------- | ------:| ---------:| ------------:| ----------- |")

        sorted_formulas = sorted(
            formula_perf.items(),
            key=lambda x: x[1]["avg_views"],
            reverse=True,
        )
        for formula, stats in sorted_formulas:
            rate_pct = f"{stats['outlier_rate'] * 100:.1f}%"
            lines.append(
                f"| {formula} | {stats['video_count']} | "
                f"{stats['avg_views']:,.0f} | {rate_pct} | "
                f"{stats['top_cluster']} |"
            )
        lines.append("")

    # --- Section 3: Gap opportunities ---
    gaps = find_gaps(resolved_db, resolved_kw)
    if isinstance(gaps, list) and gaps:
        lines.append("### Gap Opportunities\n")
        lines.append("*Topics competitors cover heavily but you don't (yet)*\n")
        lines.append("| Cluster | Competitor Videos | Outlier Rate | Your Videos | Gap Score |")
        lines.append("| ------- | -----------------:| ------------:| -----------:| ---------:|")

        for gap in gaps[:10]:
            rate_pct = f"{gap['competitor_outlier_rate'] * 100:.1f}%"
            lines.append(
                f"| {gap['cluster']} | {gap['competitor_count']} | "
                f"{rate_pct} | {gap['own_count']} | {gap['gap_score']:.0f} |"
            )
        lines.append("")

    # --- Section 4: Top outliers by cluster ---
    if isinstance(cluster_perf, dict) and "error" not in cluster_perf:
        lines.append("### Top Outlier Videos by Cluster\n")
        for cluster, stats in sorted_clusters[:8]:
            if stats["outlier_count"] > 0:
                top = stats["top_videos"][:2]
                for v in top:
                    views_str = f"{v['views']:,}" if v["views"] else "—"
                    lines.append(f"- **{cluster}:** {v['title']} ({views_str} views)")
        lines.append("")

    return "\n".join(lines)
