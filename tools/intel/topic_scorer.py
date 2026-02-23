"""
topic_scorer.py — Algorithm-informed topic scoring engine

Scores a topic idea 0-100 based on five weighted components:
    1. Own channel performance  (0.30) — keywords.db video_performance
    2. Competitor signal         (0.30) — intel.db competitor_videos outlier rates
    3. Algorithm alignment       (0.20) — intel.db algo_snapshots satisfaction signals
    4. Trending boost            (0.10) — intel.db niche_snapshots trending topics
    5. Gap opportunity           (0.10) — cross-DB coverage analysis

Public API:
    score_topic(topic_text, db_path, keywords_db_path) -> dict
    format_score_report(result) -> str

All public functions follow the error-dict pattern.
"""

import json
import re
import sqlite3
import statistics
from pathlib import Path

from tools.intel.topic_vocabulary import classify_title, primary_topic, detect_formulas

_INTEL_DIR = Path(__file__).parent
_DEFAULT_DB_PATH = str(_INTEL_DIR / "intel.db")
_DEFAULT_KEYWORDS_DB = str(_INTEL_DIR.parent / "discovery" / "keywords.db")

# Weights
W_OWN = 0.30
W_COMPETITOR = 0.30
W_ALGO = 0.20
W_TRENDING = 0.10
W_GAP = 0.10


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _grade(score: float) -> str:
    """Convert 0-100 score to letter grade."""
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "F"


# ---------------------------------------------------------------------------
# Component scorers (each returns 0-100)
# ---------------------------------------------------------------------------

def _score_own_channel(topic_clusters: list[str], keywords_db: str) -> tuple[float, dict]:
    """Score based on own-channel historical performance for matching topics."""
    info = {"matching_videos": 0, "avg_retention": None, "avg_conversion": None}
    if not Path(keywords_db).exists():
        return 50.0, info  # Neutral if no data

    try:
        conn = _connect(keywords_db)
        rows = conn.execute(
            "SELECT title, avg_retention_pct, conversion_rate, views FROM video_performance"
        ).fetchall()
        conn.close()

        if not rows:
            return 50.0, info

        # Find matching videos
        matching = []
        all_retentions = []
        all_conversions = []

        for row in rows:
            title = row["title"] or ""
            ret = row["avg_retention_pct"]
            conv = row["conversion_rate"]
            clusters = classify_title(title)

            if ret is not None and ret > 0:
                all_retentions.append(ret)
            if conv is not None and conv > 0:
                all_conversions.append(conv)

            if any(c in topic_clusters for c in clusters):
                matching.append({"retention": ret, "conversion": conv, "views": row["views"]})

        info["matching_videos"] = len(matching)

        if not matching:
            return 40.0, info  # Untested topic — slight penalty

        # Compare matching performance to channel average
        avg_channel_ret = statistics.mean(all_retentions) if all_retentions else 30
        avg_channel_conv = statistics.mean(all_conversions) if all_conversions else 0.1

        match_rets = [m["retention"] for m in matching if m["retention"] and m["retention"] > 0]
        match_convs = [m["conversion"] for m in matching if m["conversion"] and m["conversion"] > 0]

        ret_score = 50.0
        if match_rets and avg_channel_ret > 0:
            avg_match_ret = statistics.mean(match_rets)
            info["avg_retention"] = round(avg_match_ret, 1)
            ratio = avg_match_ret / avg_channel_ret
            ret_score = min(ratio * 50, 100)

        conv_score = 50.0
        if match_convs and avg_channel_conv > 0:
            avg_match_conv = statistics.mean(match_convs)
            info["avg_conversion"] = round(avg_match_conv, 2)
            ratio = avg_match_conv / avg_channel_conv
            conv_score = min(ratio * 50, 100)

        return round(ret_score * 0.6 + conv_score * 0.4, 1), info

    except Exception:
        return 50.0, info


def _score_competitor(topic_clusters: list[str], db_path: str) -> tuple[float, dict]:
    """Score based on competitor outlier rates for matching clusters."""
    info = {"matching_cluster_videos": 0, "outlier_rate": 0}
    try:
        conn = _connect(db_path)
        rows = conn.execute(
            "SELECT topic_cluster, is_outlier, views FROM competitor_videos "
            "WHERE topic_cluster IS NOT NULL"
        ).fetchall()
        conn.close()

        if not rows:
            return 50.0, info

        matching = []
        for row in rows:
            clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []
            if any(c in topic_clusters for c in clusters):
                matching.append({"is_outlier": bool(row["is_outlier"]), "views": row["views"]})

        if not matching:
            return 40.0, info

        info["matching_cluster_videos"] = len(matching)
        outlier_count = sum(1 for m in matching if m["is_outlier"])
        outlier_rate = outlier_count / len(matching) if matching else 0
        info["outlier_rate"] = round(outlier_rate, 3)

        # 20% outlier rate = 100 score; linear scale
        score = min(outlier_rate / 0.20 * 100, 100)
        return round(score, 1), info

    except Exception:
        return 50.0, info


def _score_algo_alignment(title: str, db_path: str) -> tuple[float, dict]:
    """Score based on algorithm knowledge (satisfaction signals, mechanism framing)."""
    info = {"signals_matched": []}
    score = 50.0  # Base

    # Title quality heuristics aligned with algo knowledge
    title_lower = title.lower()

    # Mechanism framing (how/why) — strong for satisfaction + session continuation
    if re.search(r"\b(?:how|why)\b", title_lower):
        score += 15
        info["signals_matched"].append("mechanism_framing")

    # Question format — drives CTR
    if "?" in title:
        score += 10
        info["signals_matched"].append("question_ctr")

    # Title length 40-65 chars — optimal for mobile
    if 40 <= len(title) <= 65:
        score += 10
        info["signals_matched"].append("optimal_title_length")
    elif len(title) > 80:
        score -= 10
        info["signals_matched"].append("title_too_long")

    # Colon/dash split — common high-performer pattern
    if re.search(r"[:\u2014\u2013]", title):
        score += 5
        info["signals_matched"].append("colon_split")

    # Check algo snapshot for satisfaction signals
    try:
        conn = _connect(db_path)
        row = conn.execute(
            "SELECT algorithm_model FROM algo_snapshots ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()

        if row and row["algorithm_model"]:
            algo = json.loads(row["algorithm_model"])
            satisfaction = algo.get("satisfaction_signals", [])
            # Bonus if topic aligns with known satisfaction patterns
            if any("depth" in s.lower() or "detail" in s.lower() for s in satisfaction if isinstance(s, str)):
                score += 5
                info["signals_matched"].append("depth_satisfaction")
    except Exception:
        pass

    return round(min(max(score, 0), 100), 1), info


def _score_trending(topic_clusters: list[str], db_path: str) -> tuple[float, dict]:
    """Score based on overlap with trending topics from niche snapshots."""
    info = {"trending_matches": []}
    try:
        conn = _connect(db_path)
        row = conn.execute(
            "SELECT trending_topics FROM niche_snapshots ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()

        if not row or not row["trending_topics"]:
            return 50.0, info

        trending = json.loads(row["trending_topics"])
        trending_topics = [t.get("topic", "").lower() for t in trending if isinstance(t, dict)]

        matches = [c for c in topic_clusters if c in trending_topics]
        info["trending_matches"] = matches

        if not matches:
            return 30.0, info

        # More matches = higher score
        score = min(len(matches) * 35, 100)
        return round(score, 1), info

    except Exception:
        return 50.0, info


def _score_gap(topic_clusters: list[str], db_path: str, keywords_db: str) -> tuple[float, dict]:
    """Score based on whether competitors cover this but you don't."""
    info = {"is_gap": False, "competitor_coverage": 0, "own_coverage": 0}
    try:
        # Competitor coverage
        conn = _connect(db_path)
        rows = conn.execute(
            "SELECT topic_cluster FROM competitor_videos WHERE topic_cluster IS NOT NULL"
        ).fetchall()
        conn.close()

        comp_count = 0
        for row in rows:
            clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []
            if any(c in topic_clusters for c in clusters):
                comp_count += 1

        info["competitor_coverage"] = comp_count

        # Own coverage
        own_count = 0
        if Path(keywords_db).exists():
            kw_conn = _connect(keywords_db)
            own_rows = kw_conn.execute("SELECT title FROM video_performance").fetchall()
            kw_conn.close()

            for row in own_rows:
                clusters = classify_title(row["title"] or "")
                if any(c in topic_clusters for c in clusters):
                    own_count += 1

        info["own_coverage"] = own_count

        if comp_count > 10 and own_count == 0:
            info["is_gap"] = True
            return 90.0, info
        elif comp_count > 5 and own_count <= 1:
            info["is_gap"] = True
            return 70.0, info
        elif comp_count > 0 and own_count == 0:
            return 60.0, info
        else:
            return 30.0, info

    except Exception:
        return 50.0, info


# ---------------------------------------------------------------------------
# Main scoring function
# ---------------------------------------------------------------------------

def score_topic(topic_text: str, db_path: str = None, keywords_db_path: str = None) -> dict:
    """
    Score a topic idea 0-100 based on five weighted components.

    Args:
        topic_text:      Topic title/description to score
        db_path:         Path to intel.db
        keywords_db_path: Path to keywords.db

    Returns:
        {
            'topic': str,
            'clusters': list[str],
            'primary_cluster': str,
            'total_score': float,
            'grade': str,
            'breakdown': {
                'own_channel':   {'score': float, 'weight': float, 'weighted': float, ...},
                'competitor':    {'score': float, 'weight': float, 'weighted': float, ...},
                'algo_alignment':{'score': float, 'weight': float, 'weighted': float, ...},
                'trending':      {'score': float, 'weight': float, 'weighted': float, ...},
                'gap_opportunity':{'score': float, 'weight': float, 'weighted': float, ...},
            },
            'recommendations': {
                'duration_min': float,
                'title_formulas': list[str],
                'comparable_outliers': list[dict],
            },
        }
        or {'error': str}
    """
    resolved_db = db_path or _DEFAULT_DB_PATH
    resolved_kw = keywords_db_path or _DEFAULT_KEYWORDS_DB

    try:
        clusters = classify_title(topic_text)
        p_topic = primary_topic(topic_text)
        if not clusters:
            clusters = [p_topic]

        # Score each component
        own_score, own_info = _score_own_channel(clusters, resolved_kw)
        comp_score, comp_info = _score_competitor(clusters, resolved_db)
        algo_score, algo_info = _score_algo_alignment(topic_text, resolved_db)
        trend_score, trend_info = _score_trending(clusters, resolved_db)
        gap_score, gap_info = _score_gap(clusters, resolved_db, resolved_kw)

        # Weighted total
        total = round(
            own_score * W_OWN +
            comp_score * W_COMPETITOR +
            algo_score * W_ALGO +
            trend_score * W_TRENDING +
            gap_score * W_GAP,
            1,
        )

        # Duration recommendation from competitor cluster data
        duration_rec = 20.0  # default
        try:
            from tools.intel.competitor_patterns import analyze_cluster_performance
            cluster_perf = analyze_cluster_performance(resolved_db)
            if isinstance(cluster_perf, dict) and p_topic in cluster_perf:
                duration_rec = cluster_perf[p_topic].get("avg_duration_min", 20.0)
        except Exception:
            pass

        # Formula recommendation
        formulas_detected = detect_formulas(topic_text)

        # Comparable outlier videos
        comparable = []
        try:
            conn = _connect(resolved_db)
            outlier_rows = conn.execute(
                "SELECT title, views, channel_id, topic_cluster FROM competitor_videos "
                "WHERE is_outlier = 1 AND topic_cluster IS NOT NULL "
                "ORDER BY views DESC LIMIT 50"
            ).fetchall()
            conn.close()

            for row in outlier_rows:
                vid_clusters = json.loads(row["topic_cluster"]) if row["topic_cluster"] else []
                if any(c in clusters for c in vid_clusters):
                    comparable.append({
                        "title": row["title"],
                        "views": row["views"],
                        "channel_id": row["channel_id"],
                    })
                    if len(comparable) >= 5:
                        break
        except Exception:
            pass

        return {
            "topic": topic_text,
            "clusters": clusters,
            "primary_cluster": p_topic,
            "total_score": total,
            "grade": _grade(total),
            "breakdown": {
                "own_channel": {"score": own_score, "weight": W_OWN, "weighted": round(own_score * W_OWN, 1), **own_info},
                "competitor": {"score": comp_score, "weight": W_COMPETITOR, "weighted": round(comp_score * W_COMPETITOR, 1), **comp_info},
                "algo_alignment": {"score": algo_score, "weight": W_ALGO, "weighted": round(algo_score * W_ALGO, 1), **algo_info},
                "trending": {"score": trend_score, "weight": W_TRENDING, "weighted": round(trend_score * W_TRENDING, 1), **trend_info},
                "gap_opportunity": {"score": gap_score, "weight": W_GAP, "weighted": round(gap_score * W_GAP, 1), **gap_info},
            },
            "recommendations": {
                "duration_min": round(duration_rec, 0),
                "title_formulas": formulas_detected,
                "comparable_outliers": comparable,
            },
        }

    except Exception as exc:
        return {"error": f"score_topic failed: {exc}"}


# ---------------------------------------------------------------------------
# Markdown formatter
# ---------------------------------------------------------------------------

def format_score_report(result: dict) -> str:
    """
    Format a score_topic() result as readable Markdown.

    Returns formatted string even for error results.
    """
    if "error" in result:
        return f"**Scoring error:** {result['error']}"

    topic = result.get("topic", "Unknown")
    total = result.get("total_score", 0)
    grade = result.get("grade", "?")
    clusters = result.get("clusters", [])
    breakdown = result.get("breakdown", {})
    recs = result.get("recommendations", {})

    lines = [
        f"## Topic Score: {topic}\n",
        f"**Score: {total}/100 (Grade {grade})**",
        f"**Clusters:** {', '.join(clusters) if clusters else 'general'}\n",
        "### Score Breakdown\n",
        "| Component | Raw | Weight | Weighted |",
        "| --------- | ---:| ------:| --------:|",
    ]

    component_labels = {
        "own_channel": "Own Channel History",
        "competitor": "Competitor Signal",
        "algo_alignment": "Algorithm Alignment",
        "trending": "Trending Boost",
        "gap_opportunity": "Gap Opportunity",
    }

    for key, label in component_labels.items():
        comp = breakdown.get(key, {})
        raw = comp.get("score", 0)
        weight = comp.get("weight", 0)
        weighted = comp.get("weighted", 0)
        lines.append(f"| {label} | {raw:.0f} | {weight:.0%} | {weighted:.1f} |")

    lines.append("")

    # Component details
    own = breakdown.get("own_channel", {})
    if own.get("matching_videos", 0) > 0:
        lines.append(f"- **Own channel:** {own['matching_videos']} matching videos")
        if own.get("avg_retention"):
            lines.append(f"  (avg retention {own['avg_retention']}%)")

    comp = breakdown.get("competitor", {})
    if comp.get("matching_cluster_videos", 0) > 0:
        lines.append(
            f"- **Competitor:** {comp['matching_cluster_videos']} matching videos, "
            f"{comp.get('outlier_rate', 0) * 100:.1f}% outlier rate"
        )

    algo = breakdown.get("algo_alignment", {})
    if algo.get("signals_matched"):
        lines.append(f"- **Algo signals:** {', '.join(algo['signals_matched'])}")

    gap = breakdown.get("gap_opportunity", {})
    if gap.get("is_gap"):
        lines.append(f"- **Gap detected:** {gap['competitor_coverage']} competitor videos, {gap['own_coverage']} yours")

    lines.append("")

    # Recommendations
    lines.append("### Recommendations\n")
    dur = recs.get("duration_min", 20)
    lines.append(f"- **Target duration:** ~{dur:.0f} min")
    formulas = recs.get("title_formulas", [])
    lines.append(f"- **Title formula:** {', '.join(formulas)}")

    outliers = recs.get("comparable_outliers", [])
    if outliers:
        lines.append("\n**Comparable outlier videos:**\n")
        for v in outliers:
            views_str = f"{v['views']:,}" if v.get("views") else "—"
            lines.append(f"- {v['title']} ({views_str} views)")

    lines.append("")
    return "\n".join(lines)
