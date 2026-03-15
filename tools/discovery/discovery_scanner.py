"""
Discovery Scanner — Proactive topic discovery pipeline.

Orchestrates autocomplete mining, competitor gap detection, and
Google Trends pulse into a unified ranked opportunity feed.

Writes channel-data/DISCOVERY-FEED.md with top-N ranked opportunities
scored by the extended Belize formula (5 factors + breakout boost).

Usage:
    python -m tools.discovery.discovery_scanner
    python -m tools.discovery.discovery_scanner --limit 10
    python -m tools.discovery.discovery_scanner --json
    python -m tools.discovery.discovery_scanner --verbose
"""

import json
import re
import argparse
import sys
import urllib.parse
import urllib.request
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Cross-module imports with feature flags (established codebase pattern)
# ---------------------------------------------------------------------------

try:
    from tools.discovery.autocomplete import extract_keywords_batch
    AUTOCOMPLETE_AVAILABLE = True
except ImportError:
    AUTOCOMPLETE_AVAILABLE = False
    extract_keywords_batch = None  # type: ignore[assignment]

try:
    from tools.intel.competitor_tracker import fetch_all_competitors
    COMPETITOR_TRACKER_AVAILABLE = True
except ImportError:
    COMPETITOR_TRACKER_AVAILABLE = False
    fetch_all_competitors = None  # type: ignore[assignment]

try:
    from tools.discovery.trends import TrendsClient, TRENDSPYG_AVAILABLE
except ImportError:
    TRENDSPYG_AVAILABLE = False
    TrendsClient = None  # type: ignore[assignment]

from tools.discovery.recommender import get_existing_topics, topic_matches_existing
from tools.discovery.database import KeywordDB
from tools.topic_pipeline import classify_topic, NEWS_HOOK_KEYWORDS

# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

# Hardcoded channel DNA seed keywords (15 for ~<90s runtime)
# Source: CONTEXT.md + RESEARCH.md channel DNA categories
CHANNEL_SEEDS = [
    # Territorial / border (5)
    "territorial dispute history",
    "border dispute explained",
    "colonial border history",
    "disputed island history",
    "partition history explained",
    # Colonial / ideological (5)
    "colonial history myth",
    "historical misconception debunked",
    "scramble for africa history",
    "history propaganda explained",
    "dark ages myth debunked",
    # Legal / untranslated (3)
    "icj ruling history",
    "untranslated document history",
    "treaty history explained",
    # High-conversion wildcard (2)
    "history fact check documentary",
    "history vs reality",
]

# Fallback channel average views (conservative — median lower than mean due to outliers)
# Channel: 199K views / 47 videos ≈ 4,234 mean, but Belize/Tariffs/Bermeja are outliers
CHANNEL_AVG_VIEWS_FALLBACK = 1000.0

# Subscriber conversion potential by topic type (from channel data — CLAUDE.md)
# ideological=2.31%, territorial=0.65%, scaled to 0-100
CONVERSION_SCORES: Dict[str, float] = {
    "ideological": 100,  # 2.31% sub rate — best
    "colonial": 65,      # good balance
    "legal": 50,         # neutral — pairs with territorial
    "medieval": 40,
    "territorial": 28,   # 0.65% sub rate — most views, low conversion
    "general": 25,
}

# Blocked lifecycle states — topics in these states are filtered out
_BLOCKED_LIFECYCLE_STATES = frozenset({"SCRIPTING", "FILMED", "PUBLISHED", "ARCHIVED"})

# Extended Belize formula weights (sum = 1.0)
_BELIZE_WEIGHTS = {
    "demand": 0.25,
    "map_angle": 0.20,
    "news_hook": 0.15,
    "no_competitor": 0.20,
    "conversion": 0.20,
}

# Channel suggestion threshold: how many times must an untracked channel appear
_CHANNEL_SUGGESTION_THRESHOLD = 3


# ---------------------------------------------------------------------------
# DiscoveryScanner
# ---------------------------------------------------------------------------

class DiscoveryScanner:
    """
    Orchestrates autocomplete, competitor gap, and trends signals into a
    ranked DISCOVERY-FEED.md report.

    Signal sources are independent — failure of one does not stop others.
    Missing signals score at neutral midpoint (50) with an "unavailable" flag.

    Example:
        scanner = DiscoveryScanner()
        result = scanner.scan(limit=10)
        print(result["feed_path"])
    """

    def __init__(self, output_dir: Optional[str] = None):
        """
        Args:
            output_dir: Directory for DISCOVERY-FEED.md.
                        Defaults to channel-data/ relative to project root.
        """
        if output_dir is None:
            project_root = Path(__file__).parent.parent.parent
            self.output_dir = project_root / "channel-data"
        else:
            self.output_dir = Path(output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._channel_avg: Optional[float] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(self, limit: int = 10) -> Dict[str, Any]:
        """
        Run full discovery pipeline.

        1. Collect autocomplete candidates
        2. Collect competitor gap candidates
        3. Merge and deduplicate candidate list
        4. Enrich with trends data
        5. Score each candidate with extended Belize formula
        6. Sort, take top `limit`, write DISCOVERY-FEED.md

        Returns:
            {
                'opportunities': list[dict],   # top-N ranked
                'feed_path': str,              # path to written feed file
                'signal_quality': dict,        # per-source status flags
            }
        """
        logger.info("Discovery scan started (limit=%d)", limit)
        scan_start = datetime.now(timezone.utc)
        signal_quality: Dict[str, Any] = {}

        # --- Signal source 1: Autocomplete ---
        autocomplete_candidates: List[Dict[str, Any]] = []
        try:
            autocomplete_candidates = self._run_autocomplete()
            signal_quality["autocomplete"] = {
                "status": "OK",
                "candidates": len(autocomplete_candidates),
            }
        except Exception as exc:
            logger.warning("Autocomplete signal failed: %s", exc)
            signal_quality["autocomplete"] = {"status": "FAILED", "error": str(exc)}

        # --- Signal source 2: Competitor gaps ---
        competitor_candidates: List[Dict[str, Any]] = []
        try:
            competitor_candidates = self._run_competitor_gaps()
            signal_quality["competitor"] = {
                "status": "OK",
                "candidates": len(competitor_candidates),
            }
        except Exception as exc:
            logger.warning("Competitor gap signal failed: %s", exc)
            signal_quality["competitor"] = {"status": "FAILED", "error": str(exc)}

        # Merge candidates (autocomplete + competitor gaps)
        all_candidates = autocomplete_candidates + competitor_candidates
        logger.info("Merged %d candidates before dedup", len(all_candidates))

        # --- Inter-candidate dedup (same topic from multiple competitors) ---
        all_candidates = self._dedup_candidates(all_candidates)

        # --- Pipeline deduplication (against existing projects + keywords.db) ---
        try:
            deduped = self._deduplicate(all_candidates)
            logger.info("%d candidates after dedup (%d removed)",
                        len(deduped), len(all_candidates) - len(deduped))
        except Exception as exc:
            logger.warning("Dedup failed, using unfiltered candidates: %s", exc)
            deduped = all_candidates

        # --- Signal source 3: Trends pulse (enriches existing candidates) ---
        try:
            enriched = self._run_trends_pulse(deduped)
            signal_quality["trends"] = {
                "status": "OK",
                "checked": len(enriched),
            }
        except Exception as exc:
            logger.warning("Trends signal failed: %s", exc)
            signal_quality["trends"] = {"status": "FAILED", "error": str(exc)}
            enriched = deduped

        # --- Score each candidate ---
        for candidate in enriched:
            try:
                candidate["score"] = self._score_extended_belize(candidate)
            except Exception as exc:
                logger.warning("Scoring failed for '%s': %s", candidate.get("keyword", "?"), exc)
                candidate["score"] = 0.0

        # --- Sort and limit ---
        ranked = sorted(enriched, key=lambda c: c.get("score", 0), reverse=True)
        top_n = ranked[:limit]

        # --- Detect channel suggestions ---
        channel_suggestions = self._detect_channel_suggestions(
            competitor_candidates,
            tracked_channels=self._get_tracked_channels(),
        )

        # --- Write feed ---
        feed_path = self._write_feed(top_n, signal_quality, channel_suggestions, scan_start)

        logger.info("Discovery scan complete. Feed: %s", feed_path)
        return {
            "opportunities": top_n,
            "feed_path": str(feed_path),
            "signal_quality": signal_quality,
        }

    # ------------------------------------------------------------------
    # Signal sources
    # ------------------------------------------------------------------

    def _run_autocomplete(self) -> List[Dict[str, Any]]:
        """
        Run autocomplete mining against CHANNEL_SEEDS.

        Uses YouTube's public suggest API (HTTP) first. Falls back to
        pyppeteer browser automation if available.

        Returns candidate dicts with demand_score based on suggestion position.
        Position 0 = highest relevance (score 100), position N = lower (score 60).
        """
        # Try HTTP-based suggest API first (no dependencies needed)
        results = self._http_autocomplete(CHANNEL_SEEDS)

        # Fall back to pyppeteer if HTTP returned nothing
        if not any(r.get("suggestions") for r in results):
            if AUTOCOMPLETE_AVAILABLE and extract_keywords_batch is not None:
                logger.info("HTTP autocomplete empty, falling back to pyppeteer")
                try:
                    results = extract_keywords_batch(CHANNEL_SEEDS)
                except Exception as exc:
                    logger.warning("pyppeteer fallback failed: %s", exc)

        candidates = []
        for result in results:
            if "error" in result:
                logger.debug("Autocomplete error for seed '%s': %s",
                             result.get("keyword", "?"), result["error"])
                continue

            suggestions = result.get("suggestions", [])
            for i, suggestion in enumerate(suggestions):
                if not suggestion:
                    continue
                # Position-based demand score: position 0=100, position 9=60
                demand_score = max(60, 100 - i * 4)
                candidates.append({
                    "keyword": suggestion.lower().strip(),
                    "source": "autocomplete",
                    "demand_score": demand_score,
                    "seed": result.get("keyword", ""),
                })

        logger.info("Autocomplete: %d candidates from %d seeds", len(candidates), len(CHANNEL_SEEDS))
        return candidates

    @staticmethod
    def _http_autocomplete(seeds: List[str], delay: float = 0.5) -> List[Dict[str, Any]]:
        """
        Fetch YouTube autocomplete suggestions via the public suggest API.

        No browser or pyppeteer needed — plain HTTP GET to Google's
        suggestqueries endpoint with client=youtube.
        """
        _SUGGEST_URL = "https://suggestqueries-clients6.youtube.com/complete/search"
        results = []

        for i, seed in enumerate(seeds):
            try:
                params = urllib.parse.urlencode({"client": "youtube", "ds": "yt", "q": seed})
                url = f"{_SUGGEST_URL}?{params}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                resp = urllib.request.urlopen(req, timeout=10)
                raw = resp.read().decode("utf-8")

                # Response is JSONP: window.google.ac.h([...])
                start = raw.index("(") + 1
                end = raw.rindex(")")
                data = json.loads(raw[start:end])
                suggestions = [item[0] for item in data[1] if item[0] != seed]

                results.append({
                    "keyword": seed,
                    "suggestions": suggestions,
                    "count": len(suggestions),
                })
                logger.debug("HTTP autocomplete '%s': %d suggestions", seed, len(suggestions))

            except Exception as exc:
                logger.debug("HTTP autocomplete failed for '%s': %s", seed, exc)
                results.append({"keyword": seed, "error": str(exc), "suggestions": []})

            # Rate limit — light delay between requests
            if i < len(seeds) - 1:
                time.sleep(delay)

        return results

    def _run_competitor_gaps(self) -> List[Dict[str, Any]]:
        """
        Detect coverage gaps from competitor videos.

        Filters to videos with views >= 2x channel average.
        Checks if channel already has a video on that topic.
        Tracks untracked channel appearances for channel_suggestions.

        Returns candidate dicts with gap_confirmed=True.
        """
        if not COMPETITOR_TRACKER_AVAILABLE or fetch_all_competitors is None:
            logger.info("Competitor tracker unavailable (feedparser not installed)")
            return []

        try:
            result = fetch_all_competitors()
        except Exception as exc:
            logger.warning("fetch_all_competitors failed: %s", exc)
            return []

        if "error" in result:
            logger.warning("Competitor tracker error: %s", result["error"])
            return []

        channel_avg = self._get_channel_avg_views()
        view_threshold = channel_avg * 2
        videos = result.get("videos", [])
        existing_topics = get_existing_topics()

        logger.info("Competitor gap detection: %d videos, threshold=%.0f views",
                    len(videos), view_threshold)

        candidates = []
        for video in videos:
            views = video.get("views") or 0
            if views < view_threshold:
                continue  # Didn't "get views" by relative standard

            title = (video.get("title") or "").strip()
            if not title:
                continue

            # Check if channel already covers this topic
            if topic_matches_existing(title, existing_topics):
                logger.debug("Competitor gap dedup: '%s' matches existing topic", title[:50])
                continue

            # This is a coverage gap — normalize title into topic keyword
            keyword = self._normalize_title(title)
            if not keyword:
                continue
            candidates.append({
                "keyword": keyword,
                "source": "competitor_gap",
                "demand_score": min(100, int(views / channel_avg * 25)),  # views → 0-100 proxy
                "competitor_channel": video.get("channel_name", ""),
                "competitor_views": views,
                "competitor_video_id": video.get("video_id", ""),
                "gap_confirmed": True,
            })

        logger.info("Competitor gaps: %d confirmed", len(candidates))
        return candidates

    def _run_trends_pulse(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich each candidate with trends data (is_breakout, is_rising flags).

        If a keyword fails trends lookup, that candidate still survives —
        it just won't have trend flags set.

        Uses TRENDSPYG_AVAILABLE feature flag. Niche history topics
        frequently return no data — this is expected, not a failure.
        """
        if not TRENDSPYG_AVAILABLE or TrendsClient is None:
            logger.info("Trends signal unavailable (trendspyg not installed)")
            for c in candidates:
                c.setdefault("is_breakout", False)
                c.setdefault("is_rising", False)
            return candidates

        trends = TrendsClient()
        seen_keywords: Dict[str, Dict[str, Any]] = {}

        for candidate in candidates:
            keyword = candidate.get("keyword", "")
            if not keyword:
                continue

            # Cache per keyword to avoid duplicate API calls
            if keyword not in seen_keywords:
                try:
                    trend_data = trends.get_interest_over_time(keyword)
                    pct = trend_data.get("percent_change", 0) if "error" not in trend_data else 0
                    seen_keywords[keyword] = {
                        "is_breakout": pct > 5000,   # Google Trends "Breakout" threshold
                        "is_rising": pct > 100,       # Strong 30-day rise
                        "percent_change": pct,
                        "trend_direction": trend_data.get("direction", "stable"),
                    }
                except Exception as exc:
                    logger.debug("Trends lookup failed for '%s': %s", keyword[:50], exc)
                    seen_keywords[keyword] = {
                        "is_breakout": False,
                        "is_rising": False,
                        "percent_change": 0,
                        "trend_direction": "unavailable",
                    }

            trend_result = seen_keywords[keyword]
            candidate["is_breakout"] = trend_result["is_breakout"]
            candidate["is_rising"] = trend_result["is_rising"]
            candidate["trend_percent_change"] = trend_result["percent_change"]
            candidate["trend_direction"] = trend_result["trend_direction"]

        return candidates

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    def _deduplicate(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out topics already in production, archived, or in keywords.db pipeline.

        Layers:
        1. Folder-based dedup: _IN_PRODUCTION/ and _ARCHIVED/ via get_existing_topics()
        2. keywords.db lifecycle state: filter SCRIPTING, FILMED, PUBLISHED, ARCHIVED

        DISCOVERED and ANALYZED states are kept (they're candidates, not in production).
        """
        existing = get_existing_topics()
        db = KeywordDB()
        fresh = []
        removed = 0

        for candidate in candidates:
            keyword = candidate.get("keyword", "")

            # Layer 1: folder-based dedup
            if topic_matches_existing(keyword, existing):
                logger.debug("Dedup (folder): %s", keyword[:50])
                removed += 1
                continue

            # Layer 2: keywords.db lifecycle state
            try:
                kw_record = db.get_keyword(keyword)
                if isinstance(kw_record, dict) and "error" not in kw_record:
                    state = kw_record.get("lifecycle_state", "")
                    if state in _BLOCKED_LIFECYCLE_STATES:
                        logger.debug("Dedup (DB %s): %s", state, keyword[:50])
                        removed += 1
                        continue
            except Exception as exc:
                logger.debug("DB lookup failed for '%s': %s", keyword[:50], exc)
                # On DB error, keep the candidate (don't filter on uncertainty)

            fresh.append(candidate)

        try:
            db.close()
        except Exception:
            pass

        logger.debug("Dedup: removed=%d, remaining=%d", removed, len(fresh))
        return fresh

    # ------------------------------------------------------------------
    # Scoring (Extended Belize Formula)
    # ------------------------------------------------------------------

    def _score_extended_belize(self, candidate: Dict[str, Any]) -> float:
        """
        5-factor weighted score with optional breakout boost.

        Factors (weights sum to 1.0):
          demand            0.25  — autocomplete position or competitor views proxy
          map_angle         0.20  — territorial/colonial topic type (0 or 100)
          news_hook         0.15  — NEWS_HOOK_KEYWORDS urgency (0/50/100)
          no_competitor     0.20  — coverage gap exists (0 or 100)
          conversion        0.20  — subscriber conversion potential by topic type

        Missing signals score at 50 (neutral midpoint).
        Breakout boost: +15 if is_breakout=True.
        Cap: 100.

        Returns:
            float: 0-100 score
        """
        keyword = candidate.get("keyword", "").lower()

        # --- Factor 1: Demand (0-100) ---
        demand = candidate.get("demand_score", 50)  # 50 = neutral midpoint if missing

        # --- Factor 2: Map angle (0 or 100) ---
        topic_type = classify_topic(keyword)
        map_angle = 100.0 if topic_type in ("territorial", "colonial") else 0.0

        # --- Factor 3: News hook (0 / 50 / 100) ---
        news_hook = 0.0
        high_urgency = NEWS_HOOK_KEYWORDS.get("high_urgency", [])
        medium_urgency = NEWS_HOOK_KEYWORDS.get("medium_urgency", [])
        if any(term in keyword for term in high_urgency):
            news_hook = 100.0
        elif any(term in keyword for term in medium_urgency):
            news_hook = 50.0

        # --- Factor 4: No competitor coverage (0 or 100) ---
        # True if source is competitor_gap (confirmed gap) or explicitly flagged
        no_competitor = 100.0 if (
            candidate.get("gap_confirmed") is True or
            candidate.get("source") == "competitor_gap"
        ) else 0.0

        # --- Factor 5: Conversion potential (0-100) ---
        conversion = CONVERSION_SCORES.get(topic_type, CONVERSION_SCORES["general"])

        # --- Weighted sum ---
        raw_score = (
            _BELIZE_WEIGHTS["demand"] * demand
            + _BELIZE_WEIGHTS["map_angle"] * map_angle
            + _BELIZE_WEIGHTS["news_hook"] * news_hook
            + _BELIZE_WEIGHTS["no_competitor"] * no_competitor
            + _BELIZE_WEIGHTS["conversion"] * conversion
        )

        # --- Breakout boost ---
        if candidate.get("is_breakout"):
            raw_score += 15.0

        return min(100.0, raw_score)

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def _write_feed(
        self,
        ranked: List[Dict[str, Any]],
        signal_quality: Dict[str, Any],
        channel_suggestions: List[Dict[str, Any]],
        scan_start: datetime,
    ) -> Path:
        """
        Write DISCOVERY-FEED.md to output_dir.

        Format: header, top-N table, per-opportunity details, channel suggestions, signal quality.

        Returns:
            Path to written file.
        """
        feed_path = self.output_dir / "DISCOVERY-FEED.md"
        scan_time = scan_start.strftime("%Y-%m-%d %H:%M")

        lines = [
            "# Discovery Feed",
            "",
            f"**Scanned:** {scan_time}",
            f"**Seeds:** {len(CHANNEL_SEEDS)} | "
            f"**Opportunities:** {len(ranked)}",
            "",
        ]

        # Signal quality summary line
        signal_statuses = []
        for src in ("autocomplete", "competitor", "trends"):
            sq = signal_quality.get(src, {})
            status = sq.get("status", "UNKNOWN")
            signal_statuses.append(f"{src}={status}")
        lines.append(f"> Signals: {' | '.join(signal_statuses)}")
        lines.append("")

        # --- Top opportunities table ---
        lines.append(f"## Top {len(ranked)} Opportunities")
        lines.append("")

        if ranked:
            lines.append("| Rank | Score | Topic | Demand | Map | Hook | No Comp | Conversion | Flags |")
            lines.append("|------|-------|-------|--------|-----|------|---------|------------|-------|")

            for i, opp in enumerate(ranked, 1):
                keyword = opp.get("keyword", "")
                score = opp.get("score", 0)
                demand = opp.get("demand_score", "?")
                topic_type = classify_topic(keyword)
                map_angle = "YES" if topic_type in ("territorial", "colonial") else "NO"

                kw_lower = keyword.lower()
                high_urgency = NEWS_HOOK_KEYWORDS.get("high_urgency", [])
                medium_urgency = NEWS_HOOK_KEYWORDS.get("medium_urgency", [])
                if any(t in kw_lower for t in high_urgency):
                    hook_str = "high"
                elif any(t in kw_lower for t in medium_urgency):
                    hook_str = "med"
                else:
                    hook_str = "none"

                no_comp = "YES" if opp.get("gap_confirmed") else "NO"
                flags = []
                if opp.get("is_breakout"):
                    flags.append("BREAKOUT")
                if opp.get("is_rising"):
                    flags.append("RISING")
                flags_str = ", ".join(flags) if flags else "-"

                # Truncate long keyword for table
                kw_display = keyword[:40] + "..." if len(keyword) > 40 else keyword

                lines.append(
                    f"| {i} | {score:.0f} | {kw_display} | {demand} | {map_angle} | "
                    f"{hook_str} | {no_comp} | {topic_type} | {flags_str} |"
                )
        else:
            lines.append("*No opportunities found — check signal sources*")

        lines.append("")

        # --- Per-opportunity details ---
        lines.append("## Opportunity Details")
        lines.append("")

        for i, opp in enumerate(ranked, 1):
            keyword = opp.get("keyword", "")
            score = opp.get("score", 0)
            topic_type = classify_topic(keyword)
            source = opp.get("source", "unknown")

            lines.append(f"### {i}. {keyword} ({score:.0f}/100)")
            lines.append("")

            if source == "competitor_gap":
                channel = opp.get("competitor_channel", "Unknown")
                views = opp.get("competitor_views", 0)
                lines.append(f"**Why now:** Competitor coverage gap — {channel} got {views:,} views, channel has no video")
            else:
                lines.append(f"**Source:** {source}")

            lines.append(f"**Topic type:** {topic_type} | **Conversion:** {CONVERSION_SCORES.get(topic_type, 25)}/100")

            if opp.get("is_breakout"):
                pct = opp.get("trend_percent_change", 0)
                lines.append(f"**Trends:** BREAKOUT (+{pct:.0f}%) — +15 score boost applied")
            elif opp.get("is_rising"):
                pct = opp.get("trend_percent_change", 0)
                lines.append(f"**Trends:** Rising (+{pct:.0f}%)")

            lines.append(f"**Action:** `/greenlight \"{keyword[:50]}\"`")
            lines.append("")
            lines.append("---")
            lines.append("")

        # --- Channel suggestions ---
        if channel_suggestions:
            lines.append("## Channel Suggestions")
            lines.append("")
            lines.append("*Untracked channels appearing frequently in results — consider adding to competitor_channels.json*")
            lines.append("")
            for suggestion in channel_suggestions:
                name = suggestion.get("channel_name", "Unknown")
                count = suggestion.get("appearances", 0)
                lines.append(f"- **{name}** (appeared {count} times in scan)")
            lines.append("")

        # --- Signal quality table ---
        lines.append("## Signal Quality")
        lines.append("")
        lines.append("| Signal | Status | Notes |")
        lines.append("|--------|--------|-------|")

        for src, sq in signal_quality.items():
            status = sq.get("status", "UNKNOWN")
            candidates_n = sq.get("candidates", sq.get("checked", "?"))
            error = sq.get("error", "")
            if error:
                note = f"Error: {error[:80]}"
            elif candidates_n != "?":
                note = f"{candidates_n} candidates/videos"
            else:
                note = ""
            lines.append(f"| {src.capitalize()} | {status} | {note} |")

        lines.append("")
        lines.append("*Generated by `discovery_scanner.py` — regenerated fresh each run*")

        feed_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("DISCOVERY-FEED.md written: %s", feed_path)
        return feed_path

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_channel_avg_views(self) -> float:
        """
        Get channel average views from analytics DB, or use fallback constant.

        Caches result for the lifetime of this scanner instance.
        """
        if self._channel_avg is not None:
            return self._channel_avg

        try:
            from tools.youtube_analytics.analyze import get_channel_stats
            stats = get_channel_stats()
            avg = stats.get("avg_views_per_video")
            if avg and avg > 0:
                self._channel_avg = float(avg)
                return self._channel_avg
        except Exception as exc:
            logger.debug("Could not load channel avg from analytics: %s", exc)

        self._channel_avg = CHANNEL_AVG_VIEWS_FALLBACK
        return self._channel_avg

    def _get_tracked_channels(self) -> set:
        """Get set of channel names from competitor_channels.json."""
        try:
            from tools.intel.competitor_tracker import load_channel_config
            channels = load_channel_config()
            if isinstance(channels, list):
                return {ch.get("name", "") for ch in channels if ch.get("name")}
        except Exception:
            pass
        return set()

    # Meta/reaction video patterns — not actual historical topics
    _META_PATTERNS = re.compile(
        r'^(?:how .+ lies|everything wrong with|response to|reacting to|'
        r'debunking .+ video|why .+ is wrong about|i watched)',
        re.IGNORECASE,
    )

    # Non-history brand/business/entertainment terms
    _NON_HISTORY_TERMS = frozenset({
        'red bull', 'netflix', 'amazon', 'tesla', 'spacex', 'apple', 'google',
        'microsoft', 'uber', 'airbnb', 'spotify', 'disney', 'marvel', 'star wars',
        'cinemasins', 'cinema sins', 'movie', 'film review', 'video essay',
        'tier list', 'gaming', 'minecraft', 'fortnite', 'podcast clip',
    })

    @staticmethod
    def _normalize_title(title: str) -> str:
        """
        Clean competitor video titles into topic keywords.

        Strips episode numbers ("20. "), pipe-delimited suffixes,
        series markers, hashtags, and trailing noise.
        Returns empty string for Shorts and meta/reaction videos.
        """
        t = title.strip().lower()
        # Filter out Shorts
        if '#short' in t:
            return ''
        # Filter out meta/reaction videos (about other creators, not topics)
        if DiscoveryScanner._META_PATTERNS.search(t):
            return ''
        # Filter out non-history content (business, entertainment, gaming)
        if any(term in t for term in DiscoveryScanner._NON_HISTORY_TERMS):
            return ''
        # Strip leading episode numbers: "20. ", "EP 5: ", "#3 - "
        t = re.sub(r'^(?:ep\.?\s*)?#?\d+[\.\)\-:]\s*', '', t)
        # Strip pipe-delimited suffixes: " | series name | channel"
        # Keep only the first segment before any pipe
        if ' | ' in t:
            t = t.split(' | ')[0].strip()
        # Strip series markers in brackets/parens: "[Part 1]", "(Full Documentary)"
        t = re.sub(r'\s*[\[\(][^\]\)]*[\]\)]', '', t)
        # Strip hashtags
        t = re.sub(r'#\w+', '', t)
        # Strip trailing " - subtitle" for very long titles (likely channel/series suffix)
        if len(t) > 60:
            t = re.sub(r'\s*-\s*[^-]{0,30}$', '', t)
        # Collapse whitespace
        t = re.sub(r'\s+', ' ', t).strip()
        # Strip leading "the " for better dedup matching
        t = re.sub(r'^the\s+', '', t)
        return t

    @staticmethod
    def _extract_topic_words(keyword: str) -> set:
        """Extract significant words from a keyword for overlap matching."""
        stop = {'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'and',
                'or', 'is', 'was', 'by', 'from', 'with', 'its', 'how', 'why',
                'what', 'when', 'this', 'that', 'first', 'new', 'full'}
        words = set(re.findall(r'[a-z]+', keyword.lower()))
        return words - stop

    def _dedup_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate candidates against each other using word-overlap matching.

        Two candidates are considered duplicates if they share 2+ significant
        words (same logic as topic_matches_existing). Keeps the one with the
        highest competitor_views or demand_score.
        """
        kept: List[Dict[str, Any]] = []
        kept_words: List[set] = []

        # Sort by signal strength so we keep the best version first
        by_signal = sorted(
            candidates,
            key=lambda c: (c.get("competitor_views", 0), c.get("demand_score", 0)),
            reverse=True,
        )

        for c in by_signal:
            words = self._extract_topic_words(c.get("keyword", ""))
            if len(words) < 2:
                continue
            # Check overlap against already-kept candidates
            is_dup = False
            for kw in kept_words:
                overlap = words & kw
                if len(overlap) >= 2:
                    is_dup = True
                    break
            if not is_dup:
                kept.append(c)
                kept_words.append(words)

        removed = len(candidates) - len(kept)
        if removed > 0:
            logger.info("Inter-candidate dedup: %d duplicates removed", removed)
        return kept

    def _detect_channel_suggestions(
        self,
        competitor_candidates: List[Dict[str, Any]],
        tracked_channels: set,
    ) -> List[Dict[str, Any]]:
        """
        Identify untracked channels appearing 3+ times in competitor scan results.

        These are channels that keep surfacing in relevant topic searches but
        are not in competitor_channels.json — candidates for manual addition.

        Returns:
            List of dicts: {channel_name, appearances}
        """
        counts: Dict[str, int] = {}
        for candidate in competitor_candidates:
            channel = candidate.get("competitor_channel", "")
            if channel and channel not in tracked_channels:
                counts[channel] = counts.get(channel, 0) + 1

        return [
            {"channel_name": name, "appearances": n}
            for name, n in sorted(counts.items(), key=lambda x: -x[1])
            if n >= _CHANNEL_SUGGESTION_THRESHOLD
        ]


# ---------------------------------------------------------------------------
# __main__ entry point
# ---------------------------------------------------------------------------

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Discovery Scanner — proactive topic discovery for History vs Hype",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.discovery.discovery_scanner
  python -m tools.discovery.discovery_scanner --limit 5
  python -m tools.discovery.discovery_scanner --json
  python -m tools.discovery.discovery_scanner --verbose

Output: channel-data/DISCOVERY-FEED.md (regenerated each run)
        """,
    )
    parser.add_argument("--limit", "-n", type=int, default=10, help="Top N opportunities (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output JSON summary to stdout")
    parser.add_argument("--output-dir", type=str, help="Override output directory for feed file")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    scanner = DiscoveryScanner(output_dir=args.output_dir)
    result = scanner.scan(limit=args.limit)

    if args.json:
        # Serialize opportunities (drop non-JSON-safe items)
        output = {
            "feed_path": result["feed_path"],
            "opportunities_count": len(result["opportunities"]),
            "signal_quality": result["signal_quality"],
            "top_5": [
                {"rank": i + 1, "keyword": o["keyword"], "score": o["score"]}
                for i, o in enumerate(result["opportunities"][:5])
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable summary
        print()
        print("=" * 60)
        print("  DISCOVERY SCAN COMPLETE")
        print("=" * 60)
        print(f"\nFeed: {result['feed_path']}")
        print(f"Opportunities: {len(result['opportunities'])}")

        sq = result["signal_quality"]
        for src in ("autocomplete", "competitor", "trends"):
            status = sq.get(src, {}).get("status", "N/A")
            print(f"  {src}: {status}")

        print()
        if result["opportunities"]:
            print("Top 5:")
            print("-" * 60)
            for i, opp in enumerate(result["opportunities"][:5], 1):
                print(f"  {i:>2}. [{opp.get('score', 0):>5.1f}] {opp.get('keyword', '')[:50]}")
        print()


if __name__ == "__main__":
    main()
