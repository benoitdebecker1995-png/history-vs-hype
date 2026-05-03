"""
Composite Demand Scorer — estimates YouTube search demand from free sources.

Combines three signals to reduce VidIQ dependency:
1. YouTube Autocomplete (demand signal + keyword discovery)
2. pytrends with YouTube filter (relative volume via calibration)
3. YouTube Data API top-result views (competition/demand proxy)

Calibrates against known VidIQ volumes in keywords.db to produce
estimated monthly search volume for any keyword.

Usage:
    python -m tools.preflight.demand_scorer "battle of thermopylae"
    python -m tools.preflight.demand_scorer "treaty of tordesillas" --verbose
    python -m tools.preflight.demand_scorer "bakassi peninsula" --json
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from statistics import median
from typing import Dict, List, Optional, Tuple

import requests

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

DB_PATH = str(Path(__file__).resolve().parent.parent / "discovery" / "keywords.db")

# Thresholds (same as demand_checker.py for consistency)
GO_VOLUME = 1000
CAUTION_VOLUME = 200

# Calibration anchors: keywords with known VidIQ volumes, spread across range.
# Picked from keywords.db — diverse topics, stable volume.
# Updated manually when VidIQ data refreshes.
CALIBRATION_ANCHORS = [
    ("scramble for africa", 11648),
    ("panama canal history", 6600),
    ("crimea russia ukraine", 4400),
    ("ethiopia never colonized", 3600),
    ("battle of adwa", 2900),
]

# YouTube autocomplete endpoint
YT_SUGGEST_URL = "https://suggestqueries.google.com/complete/search"


def get_autocomplete(query: str) -> List[str]:
    """Fetch YouTube autocomplete suggestions for a query."""
    try:
        resp = requests.get(
            YT_SUGGEST_URL,
            params={"client": "youtube", "ds": "yt", "q": query},
            timeout=10,
        )
        resp.raise_for_status()
        text = resp.text
        start = text.index("(") + 1
        end = text.rindex(")")
        data = json.loads(text[start:end])
        return [s[0] for s in data[1]]
    except Exception as e:
        logger.warning("Autocomplete failed for '%s': %s", query, e)
        return []


def score_autocomplete(query: str, suggestions: List[str]) -> Dict:
    """Score autocomplete signals.

    Returns:
        exists: bool — does the exact query appear in suggestions?
        position: int or None — rank in suggestions (1-based, lower = more popular)
        suggestion_count: int — total suggestions returned
        related: list — all suggestions
    """
    query_lower = query.lower().strip()
    position = None
    for i, s in enumerate(suggestions):
        if s.lower().strip() == query_lower:
            position = i + 1
            break

    return {
        "exists": position is not None,
        "position": position,
        "suggestion_count": len(suggestions),
        "related": suggestions,
    }


def get_pytrends_estimate(
    query: str, anchors: Optional[List[Tuple[str, int]]] = None
) -> Dict:
    """Estimate monthly volume using pytrends YouTube filter + calibration.

    Compares the query against calibration anchors (keywords with known VidIQ
    volumes) in the same pytrends batch. Since pytrends returns relative scores,
    comparing within the same batch gives valid ratios.

    Uses median of all anchor estimates for robustness.
    """
    if anchors is None:
        anchors = CALIBRATION_ANCHORS

    try:
        from pytrends.request import TrendReq
    except ImportError:
        logger.warning("pytrends not installed. Run: pip install pytrends")
        return {"estimated_volume": None, "confidence": "none", "error": "pytrends not installed"}

    try:
        pytrends = TrendReq(hl="en-US")

        # pytrends allows max 5 keywords — use query + 4 anchors
        # Exclude any anchor that matches the query itself
        selected_anchors = [a for a in anchors if a[0].lower() != query.lower()][:4]
        if not selected_anchors:
            return {"estimated_volume": None, "confidence": "none", "error": "query matches all anchors"}
        kw_list = [query] + [a[0] for a in selected_anchors]

        pytrends.build_payload(kw_list, timeframe="today 12-m", gprop="youtube")
        data = pytrends.interest_over_time()

        if data.empty:
            return {"estimated_volume": None, "confidence": "none", "error": "no pytrends data"}

        query_avg = data[query].mean()
        query_max = data[query].max()

        if query_avg == 0:
            return {
                "estimated_volume": 0,
                "confidence": "high",
                "pytrends_avg": 0,
                "pytrends_max": 0,
                "anchor_estimates": [],
            }

        estimates = []
        anchor_details = []
        for anchor_kw, anchor_vol in selected_anchors:
            anchor_avg = data[anchor_kw].mean()
            # Skip anchors with very low pytrends scores — ratio becomes unreliable
            if anchor_avg >= 5:
                est = anchor_vol * (query_avg / anchor_avg)
                estimates.append(est)
                anchor_details.append({
                    "anchor": anchor_kw,
                    "anchor_volume": anchor_vol,
                    "anchor_pytrends": round(anchor_avg, 1),
                    "estimate": round(est),
                })

        if not estimates:
            return {"estimated_volume": None, "confidence": "none", "error": "all anchors scored 0"}

        median_est = round(median(estimates))

        # Confidence based on estimate spread
        spread = max(estimates) / min(estimates) if min(estimates) > 0 else 999
        if spread < 2:
            confidence = "high"
        elif spread < 5:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "estimated_volume": median_est,
            "confidence": confidence,
            "pytrends_avg": round(query_avg, 1),
            "pytrends_max": round(query_max, 1),
            "estimate_range": (round(min(estimates)), round(max(estimates))),
            "anchor_estimates": anchor_details,
        }

    except Exception as e:
        logger.warning("pytrends failed: %s", e)
        return {"estimated_volume": None, "confidence": "none", "error": str(e)}


def get_top_result_views(query: str, api_key: Optional[str] = None) -> Dict:
    """Pull view counts of top YouTube search results as a demand proxy.

    Requires YOUTUBE_API_KEY environment variable or api_key parameter.
    Falls back gracefully if no key available.
    """
    key = api_key or os.environ.get("YOUTUBE_API_KEY")
    if not key:
        return {"available": False, "reason": "no API key"}

    try:
        # Search for top results
        search_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 10,
                "order": "relevance",
                "key": key,
            },
            timeout=15,
        )
        search_resp.raise_for_status()
        items = search_resp.json().get("items", [])

        if not items:
            return {"available": True, "top_results": 0, "median_views": 0, "max_views": 0}

        # Get video stats
        video_ids = [item["id"]["videoId"] for item in items if "videoId" in item.get("id", {})]
        if not video_ids:
            return {"available": True, "top_results": 0, "median_views": 0, "max_views": 0}

        stats_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": key,
            },
            timeout=15,
        )
        stats_resp.raise_for_status()
        stats_items = stats_resp.json().get("items", [])

        views = [int(item["statistics"].get("viewCount", 0)) for item in stats_items]
        views.sort(reverse=True)

        return {
            "available": True,
            "top_results": len(views),
            "median_views": round(median(views)) if views else 0,
            "max_views": max(views) if views else 0,
            "top_5_views": views[:5],
        }

    except Exception as e:
        logger.warning("YouTube API search failed: %s", e)
        return {"available": False, "reason": str(e)}


def check_local_db(query: str) -> Dict:
    """Check if keywords.db already has volume data for this query."""
    if not Path(DB_PATH).exists():
        return {"found": False}

    tokens = {w.lower() for w in query.split() if len(w) > 1 and w.lower() not in
              {"the", "of", "a", "an", "in", "on", "and", "is", "to", "for", "by"}}

    conn = sqlite3.connect(DB_PATH)
    try:
        matches = []
        for token in tokens:
            rows = conn.execute(
                "SELECT keyword, search_volume FROM keywords "
                "WHERE LOWER(keyword) LIKE ? AND search_volume IS NOT NULL AND search_volume > 0",
                (f"%{token}%",),
            ).fetchall()
            for kw, vol in rows:
                kw_tokens = {w.lower() for w in kw.split() if len(w) > 1
                             and w.lower() not in {"the", "of", "a", "an", "in", "on", "and", "is", "to", "for", "by"}}
                content_tokens = tokens  # already cleaned
                overlap = len(content_tokens & kw_tokens) / min(len(content_tokens), len(kw_tokens)) if content_tokens and kw_tokens else 0
                # Require 0.6+ overlap to prevent "battle of X" matching "battle of Y"
                if overlap >= 0.6:
                    matches.append({"keyword": kw, "volume": vol, "overlap": round(overlap, 2)})

        # Deduplicate
        seen = set()
        unique = []
        for m in matches:
            if m["keyword"] not in seen:
                seen.add(m["keyword"])
                unique.append(m)
        unique.sort(key=lambda x: x["volume"], reverse=True)

        if unique:
            return {"found": True, "matches": unique[:5], "best_volume": unique[0]["volume"]}
        return {"found": False}
    finally:
        conn.close()


def composite_score(query: str, api_key: Optional[str] = None) -> Dict:
    """Run all demand signals and produce a composite verdict.

    Returns structured result with verdict, estimated volume, and all signals.
    """
    # Signal 1: Local DB (instant, free)
    db_result = check_local_db(query)

    # Signal 2: YouTube Autocomplete (fast, free)
    suggestions = get_autocomplete(query)
    autocomplete = score_autocomplete(query, suggestions)

    # Signal 3: pytrends calibrated estimate (slow, free)
    pytrends_result = get_pytrends_estimate(query)

    # Signal 4: YouTube API top results (optional, costs quota)
    yt_api = get_top_result_views(query, api_key)

    # Combine into verdict
    estimated_volume = None
    confidence = "none"
    source = "none"

    # Priority: DB > pytrends > autocomplete heuristic
    if db_result.get("found"):
        estimated_volume = db_result["best_volume"]
        confidence = "high"
        source = "keywords.db (VidIQ)"
    elif pytrends_result.get("estimated_volume") is not None:
        estimated_volume = pytrends_result["estimated_volume"]
        confidence = pytrends_result["confidence"]
        source = "pytrends calibrated"

    # Autocomplete boost: if keyword autocompletes, it has real demand
    autocomplete_boost = False
    if autocomplete["exists"] and autocomplete["position"] and autocomplete["position"] <= 3:
        autocomplete_boost = True
        if estimated_volume is not None and estimated_volume < GO_VOLUME:
            # Strong autocomplete signal overrides low pytrends estimate
            estimated_volume = max(estimated_volume, GO_VOLUME)
            source += " + autocomplete boost"

    # Determine verdict
    if estimated_volume is not None and estimated_volume >= GO_VOLUME:
        verdict = "GO"
    elif estimated_volume is not None and estimated_volume >= CAUTION_VOLUME:
        verdict = "CAUTION"
    elif autocomplete["exists"]:
        # Keyword autocompletes but volume estimate is low/missing
        verdict = "CAUTION"
        if estimated_volume is None:
            estimated_volume = CAUTION_VOLUME  # Floor estimate
            source = "autocomplete (floor estimate)"
    elif autocomplete["suggestion_count"] > 0:
        # Related suggestions exist but exact match doesn't autocomplete
        verdict = "CAUTION"
    else:
        verdict = "STOP"

    # Build result
    result = {
        "query": query,
        "verdict": verdict,
        "estimated_volume": estimated_volume,
        "confidence": confidence,
        "source": source,
        "signals": {
            "local_db": db_result,
            "autocomplete": autocomplete,
            "pytrends": pytrends_result,
            "youtube_api": yt_api,
        },
    }

    # Reasons
    reasons = []
    if estimated_volume:
        reasons.append(f"Estimated {estimated_volume:,}/mo ({source})")
    if autocomplete["exists"]:
        reasons.append(f"Autocompletes at position {autocomplete['position']}")
    elif autocomplete["suggestion_count"] > 0:
        reasons.append(f"{autocomplete['suggestion_count']} related suggestions (exact match not in autocomplete)")
    if pytrends_result.get("estimate_range"):
        lo, hi = pytrends_result["estimate_range"]
        reasons.append(f"Pytrends range: {lo:,}-{hi:,}/mo (confidence: {pytrends_result['confidence']})")
    if yt_api.get("available") and yt_api.get("median_views"):
        reasons.append(f"Top results median views: {yt_api['median_views']:,}")
    if not reasons:
        reasons.append("No demand signals found")

    result["reasons"] = reasons
    return result


def print_report(result: Dict) -> None:
    """Print human-readable demand report."""
    v = result["verdict"]
    colors = {"GO": "\033[32m", "CAUTION": "\033[33m", "STOP": "\033[31m"}
    reset = "\033[0m"
    use_color = sys.stderr.isatty()
    v_display = f"{colors.get(v, '')}{v}{reset}" if use_color else v

    print(f"\n{'=' * 64}")
    print(f"  DEMAND SCORER: {result['query']}")
    print(f"{'=' * 64}")
    print(f"\n  Verdict: {v_display}")

    vol = result.get("estimated_volume")
    if vol:
        print(f"  Estimated volume: {vol:,}/mo ({result['confidence']} confidence)")
        print(f"  Source: {result['source']}")

    print(f"\n  Signals:")
    for r in result["reasons"]:
        print(f"    - {r}")

    # Autocomplete details
    ac = result["signals"]["autocomplete"]
    if ac["related"]:
        print(f"\n  YouTube Autocomplete ({ac['suggestion_count']} suggestions):")
        for i, s in enumerate(ac["related"][:8]):
            marker = " <<" if s.lower().strip() == result["query"].lower().strip() else ""
            print(f"    {i+1}. {s}{marker}")

    # pytrends details
    pt = result["signals"]["pytrends"]
    if pt.get("anchor_estimates"):
        print(f"\n  Pytrends Calibration (YouTube filter, 12-month avg):")
        print(f"    Query interest: {pt['pytrends_avg']}/100 (peak: {pt['pytrends_max']})")
        for a in pt["anchor_estimates"]:
            print(f"    vs {a['anchor']:<30s} ({a['anchor_volume']:>6,}/mo) -> {a['estimate']:>8,}/mo est")

    # YouTube API details
    yt = result["signals"]["youtube_api"]
    if yt.get("available") and yt.get("top_5_views"):
        print(f"\n  YouTube Top Results (by views):")
        for i, v in enumerate(yt["top_5_views"]):
            print(f"    #{i+1}: {v:>12,} views")

    # Local DB
    db = result["signals"]["local_db"]
    if db.get("found"):
        print(f"\n  Local DB matches:")
        for m in db["matches"][:3]:
            print(f"    {m['keyword']:<40s} {m['volume']:>8,}/mo")

    print(f"\n{'=' * 64}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Composite demand scorer - estimates YouTube keyword demand from free sources"
    )
    parser.add_argument("query", help="Keyword or topic to check")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of report")
    parser.add_argument("--api-key", help="YouTube Data API key (or set YOUTUBE_API_KEY env var)")
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)
    result = composite_score(args.query, api_key=args.api_key)

    if args.json:
        # Clean for JSON serialization
        output = {k: v for k, v in result.items() if k != "signals"}
        output["signals_summary"] = {
            "autocomplete_position": result["signals"]["autocomplete"]["position"],
            "autocomplete_count": result["signals"]["autocomplete"]["suggestion_count"],
            "pytrends_avg": result["signals"]["pytrends"].get("pytrends_avg"),
            "pytrends_confidence": result["signals"]["pytrends"].get("confidence"),
            "db_found": result["signals"]["local_db"].get("found", False),
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(result)

    exit_codes = {"GO": 0, "CAUTION": 1, "STOP": 2}
    sys.exit(exit_codes.get(result["verdict"], 2))


if __name__ == "__main__":
    main()
