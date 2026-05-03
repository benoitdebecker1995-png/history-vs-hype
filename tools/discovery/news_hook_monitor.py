"""
News Hook Monitor — detects when news events create publishing windows for pipeline topics.

Scans Google News RSS for recent articles matching monitored topics from the
topic pipeline and active projects. Detects spikes vs baseline to flag urgent
publishing opportunities.

The channel's biggest video (Belize, 29K views) worked because of an active
legal case creating search demand. This tool automates that detection.

Usage:
    python -m tools.discovery.news_hook_monitor --scan          # Scan all topics
    python -m tools.discovery.news_hook_monitor --topic "india pakistan"  # Specific topic
    python -m tools.discovery.news_hook_monitor --init          # Init config from pipeline
    python -m tools.discovery.news_hook_monitor --report        # Generate NEWS-ALERTS.md

Called by: /next --timely, /status
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_PATH = ROOT / "channel-data" / "TOPIC-PIPELINE.md"
PRODUCTION_DIR = ROOT / "video-projects" / "_IN_PRODUCTION"
CONFIG_PATH = ROOT / "tools" / "discovery" / "_news_monitor_config.json"
CACHE_PATH = ROOT / "tools" / "discovery" / "_news_cache.json"
ALERTS_PATH = ROOT / "channel-data" / "NEWS-ALERTS.md"

# Google News RSS base URL (free, no API key)
GNEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en"

# Rate-limit delay between RSS fetches (seconds)
FETCH_DELAY = 1.5

# Spike detection thresholds
SPIKE_URGENT = 3.0     # 3x baseline = URGENT
SPIKE_TRENDING = 1.5   # 1.5x baseline = TRENDING

# Maximum age for articles to count (days)
MAX_ARTICLE_AGE_DAYS = 7

# ---------------------------------------------------------------------------
# Topic extraction — reuses news_scanner patterns + pipeline parsing
# ---------------------------------------------------------------------------

# Slug overrides for better search terms (extended from news_scanner.py)
SLUG_OVERRIDES = {
    "fuentes-fact-check": "Nick Fuentes fact check history",
    "vance-part-2-review": "JD Vance history claims",
    "netanyahu-map": "Netanyahu map Greater Israel",
    "vichy-statut-juifs": "Vichy France anti-Jewish law",
    "adwa-wuchale": "Battle of Adwa Treaty Wuchale Ethiopia Italy",
    "belavezha-accords": "Belavezha Accords Soviet Union dissolution",
    "guadalupe-hidalgo": "Treaty Guadalupe Hidalgo Mexico border",
    "bir-tawil": "Bir Tawil unclaimed territory Egypt Sudan",
    "panama-canal-deconcini": "Panama Canal treaty sovereignty",
    "belize-icj-endgame": "Belize Guatemala ICJ dispute",
    "bermeja-island": "Bermeja Island Mexico missing island",
    "gibraltar-treaty-utrecht": "Gibraltar sovereignty Spain UK Treaty Utrecht",
    "spanish-colonial-law-untranslated": "Spanish colonial law Latin America",
    "greenland-independence": "Greenland independence Denmark Trump",
    "india-pakistan-partition": "India Pakistan partition 1947 Radcliffe",
    "berlin-conference-1884": "Berlin Conference 1884 scramble Africa",
    "treaty-tordesillas": "Treaty Tordesillas Spain Portugal",
    "why-brazil-speaks-portuguese": "Brazil Portuguese language history",
    "operation-condor": "Operation Condor South America CIA",
    "communism-definition": "communism definition history",
    "haiti-independence-debt": "Haiti independence debt France",
    "industrial-revolution": "Industrial Revolution myths",
    "crusades-fact-check": "Crusades defensive war myth",
    "dark-ages": "Dark Ages myth medieval",
    "flat-earth-medieval": "flat earth medieval myth",
    "iran-1953-coup": "Iran 1953 coup Mosaddegh CIA",
    "iran-protests-history": "Iran constitution democracy protests",
    "christmas-calendar-354": "Christmas pagan origins calendar",
    "christmas-origins": "Christmas pagan origins history",
    "viking-laws-gragas": "Viking laws Gragas Iceland",
    "chagos-islands": "Chagos Islands Mauritius UK sovereignty",
    "guatemala-maya-claims": "Guatemala Belize territorial dispute",
    "somaliland": "Somaliland recognition independence",
    "genocide-definition": "genocide definition history",
    "czechoslovakia-velvet-divorce": "Czechoslovakia Velvet Divorce 1993",
    "antarctic-treaty": "Antarctic Treaty 2048 expiration",
}

# Keywords to monitor per topic (more specific than slug-derived terms)
KEYWORD_EXPANSIONS = {
    "india-pakistan-partition": [
        "india pakistan", "kashmir conflict", "india pakistan border",
        "radcliffe line", "partition 1947",
    ],
    "berlin-conference-1884": [
        "berlin conference africa", "scramble for africa",
        "partition of africa", "colonial borders africa",
    ],
    "treaty-tordesillas": [
        "treaty tordesillas", "spain portugal divide world",
        "papal line demarcation",
    ],
    "greenland-independence": [
        "greenland independence", "greenland denmark",
        "trump greenland", "greenland sovereignty",
    ],
    "belize-icj-endgame": [
        "belize guatemala", "belize ICJ", "guatemala territorial claim",
    ],
    "gibraltar-treaty-utrecht": [
        "gibraltar sovereignty", "gibraltar spain",
        "gibraltar border", "gibraltar treaty",
    ],
    "panama-canal-deconcini": [
        "panama canal sovereignty", "panama canal treaty",
        "panama canal history",
    ],
    "haiti-independence-debt": [
        "haiti independence", "haiti france debt",
        "haiti reparations",
    ],
    "adwa-wuchale": [
        "battle adwa", "treaty wuchale", "ethiopia italy",
        "menelik II",
    ],
    "crimea": [
        "crimea history", "crimea ukraine", "crimea russia",
        "crimea annexation",
    ],
    "falklands": [
        "falklands islands", "malvinas argentina",
        "falklands sovereignty",
    ],
    "antarctic-treaty": [
        "antarctic treaty 2048", "antarctica sovereignty",
        "antarctic territorial claims",
    ],
}

# Skip these project slugs
SKIP_SLUGS = {"format-research", "README", "Taiwan", "Tariffs", "29-format-research-2025"}


def _slug_to_clean(slug: str) -> str:
    """Strip leading number and year suffix from a project slug."""
    clean = re.sub(r"^\d+-", "", slug)
    clean = re.sub(r"-\d{4}$", "", clean)
    return clean


def _slug_to_topic(slug: str) -> str:
    """Convert project folder slug to search-friendly topic string."""
    clean = _slug_to_clean(slug)
    if clean in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[clean]
    return clean.replace("-", " ").title()


def _slug_to_keywords(slug: str) -> List[str]:
    """Get monitoring keywords for a project slug."""
    clean = _slug_to_clean(slug)
    if clean in KEYWORD_EXPANSIONS:
        return KEYWORD_EXPANSIONS[clean]
    # Fallback: generate from topic name
    topic = _slug_to_topic(slug).lower()
    words = topic.split()
    keywords = [topic]
    # Also add 2-word combinations if topic has 3+ words
    if len(words) >= 3:
        keywords.append(" ".join(words[:2]))
        keywords.append(" ".join(words[-2:]))
    return keywords


def extract_pipeline_topics() -> List[Dict[str, Any]]:
    """Extract topics from the pipeline markdown and production folders.

    Combines:
    1. Topics from TOPIC-PIPELINE.md (curated top 10 + ranked list)
    2. Active projects from _IN_PRODUCTION/

    Returns list of topic dicts with: slug, topic, keywords, status, project_path
    """
    topics = {}

    # --- Source 1: Parse TOPIC-PIPELINE.md curated table ---
    if PIPELINE_PATH.exists():
        try:
            text = PIPELINE_PATH.read_text(encoding="utf-8")
            # Parse the ranked table rows: | Rank | Score | Topic | Type | ...
            for m in re.finditer(
                r"\|\s*\d+\s*\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*(\w+)\s*\|.*?\|\s*(\w[\w ]*?)\s*\|",
                text,
            ):
                topic_name = m.group(1).strip()
                topic_type = m.group(2).strip()
                status = m.group(3).strip()
                slug = topic_name.lower().replace(" ", "-")
                if slug not in topics:
                    topics[slug] = {
                        "slug": slug,
                        "topic": topic_name,
                        "type": topic_type,
                        "keywords": [topic_name.lower()],
                        "status": status,
                        "project_path": None,
                        "baseline_articles": 2,
                    }
        except Exception as e:
            logger.warning("Failed to parse pipeline: %s", e)

    # --- Source 2: Scan _IN_PRODUCTION folders ---
    if PRODUCTION_DIR.is_dir():
        for folder in sorted(PRODUCTION_DIR.iterdir()):
            if not folder.is_dir():
                continue
            slug = folder.name
            clean = _slug_to_clean(slug)
            if clean in SKIP_SLUGS or slug in SKIP_SLUGS:
                continue

            # Determine status
            status = "UNKNOWN"
            post_pub = folder / "POST-PUBLISH-ANALYSIS.md"
            if post_pub.exists():
                status = "PUBLISHED"
                continue  # Skip published projects
            status_file = folder / "PROJECT-STATUS.md"
            if status_file.exists():
                try:
                    st_text = status_file.read_text(encoding="utf-8")[:500]
                    sm = re.search(r"Status[:\s]*\*?\*?([A-Z ]+)", st_text)
                    if sm:
                        status = sm.group(1).strip()
                except Exception:
                    pass

            topic_str = _slug_to_topic(slug)
            keywords = _slug_to_keywords(slug)

            if slug not in topics and clean not in topics:
                topics[slug] = {
                    "slug": slug,
                    "topic": topic_str,
                    "type": "unknown",
                    "keywords": keywords,
                    "status": status,
                    "project_path": str(folder),
                    "baseline_articles": 2,
                }
            elif slug in topics:
                topics[slug]["project_path"] = str(folder)
                topics[slug]["keywords"] = keywords

    return list(topics.values())


# ---------------------------------------------------------------------------
# Google News RSS fetcher
# ---------------------------------------------------------------------------

def _parse_rfc2822_date(date_str: str) -> Optional[datetime]:
    """Parse RFC 2822 date from RSS feed."""
    from email.utils import parsedate_to_datetime
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        # Fallback: try common formats
        for fmt in [
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S %z",
        ]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
    return None


def fetch_google_news_rss(query: str, max_results: int = 20) -> List[Dict[str, str]]:
    """Fetch articles from Google News RSS for a query.

    Args:
        query: Search query string
        max_results: Maximum articles to return

    Returns:
        List of dicts with: title, source, date, url, published_dt
    """
    encoded = urllib.parse.quote_plus(query)
    url = GNEWS_RSS.format(query=encoded)

    logger.debug("Fetching RSS: %s", url)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        logger.warning("Failed to fetch news for '%s': %s", query, e)
        return []

    # Parse XML
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        logger.warning("Failed to parse RSS XML for '%s': %s", query, e)
        return []

    articles = []
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=MAX_ARTICLE_AGE_DAYS)

    for item in root.iter("item"):
        if len(articles) >= max_results:
            break

        title_el = item.find("title")
        link_el = item.find("link")
        pub_date_el = item.find("pubDate")
        source_el = item.find("source")

        title = title_el.text.strip() if title_el is not None and title_el.text else "?"
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        pub_date_str = pub_date_el.text.strip() if pub_date_el is not None and pub_date_el.text else ""
        source = source_el.text.strip() if source_el is not None and source_el.text else "Unknown"

        # Parse date and filter by age
        pub_dt = _parse_rfc2822_date(pub_date_str) if pub_date_str else None
        if pub_dt and pub_dt < cutoff:
            continue  # Too old

        articles.append({
            "title": title,
            "source": source,
            "date": pub_date_str,
            "url": link,
            "published_dt": pub_dt.isoformat() if pub_dt else "",
            "age_days": (now - pub_dt).days if pub_dt else 999,
        })

    return articles


def scan_topic(topic_config: Dict[str, Any], use_cache: bool = True) -> Dict[str, Any]:
    """Scan a single topic for news articles.

    Args:
        topic_config: Topic dict with slug, keywords, baseline_articles, etc.
        use_cache: Whether to check cache before fetching

    Returns:
        Dict with topic info, articles found, spike level
    """
    slug = topic_config["slug"]
    keywords = topic_config.get("keywords", [topic_config["topic"].lower()])
    baseline = topic_config.get("baseline_articles", 2)

    # Check cache
    cache = _load_cache()
    cached = cache.get(slug)
    if use_cache and cached:
        cached_time = cached.get("fetched_at", "")
        if cached_time:
            try:
                ct = datetime.fromisoformat(cached_time)
                if (datetime.now(timezone.utc) - ct).total_seconds() < 3600:  # 1h cache
                    logger.debug("Using cached results for %s", slug)
                    return cached
            except ValueError:
                pass

    # Fetch articles for each keyword
    all_articles = []
    seen_titles = set()

    for kw in keywords[:5]:  # Limit to 5 keywords per topic
        articles = fetch_google_news_rss(kw, max_results=10)
        for art in articles:
            # Deduplicate by title
            title_key = art["title"].lower()[:60]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                art["matched_keyword"] = kw
                all_articles.append(art)
        time.sleep(FETCH_DELAY)  # Rate limit

    # Sort by recency
    all_articles.sort(key=lambda a: a.get("age_days", 999))

    # Detect spike
    article_count = len(all_articles)
    if baseline == 0:
        baseline = 1  # Avoid division by zero
    spike_ratio = article_count / baseline

    if spike_ratio >= SPIKE_URGENT:
        level = "URGENT"
    elif spike_ratio >= SPIKE_TRENDING:
        level = "TRENDING"
    else:
        level = "MONITORING"

    result = {
        "slug": slug,
        "topic": topic_config["topic"],
        "type": topic_config.get("type", "unknown"),
        "status": topic_config.get("status", "UNKNOWN"),
        "project_path": topic_config.get("project_path"),
        "keywords": keywords,
        "articles": all_articles[:15],  # Cap stored articles
        "article_count": article_count,
        "baseline": baseline,
        "spike_ratio": round(spike_ratio, 2),
        "level": level,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

    # Update cache
    cache[slug] = result
    _save_cache(cache)

    return result


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

def _load_cache() -> Dict:
    """Load cached scan results."""
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_cache(cache: Dict) -> None:
    """Save scan results to cache."""
    try:
        CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as e:
        logger.warning("Failed to save cache: %s", e)


# ---------------------------------------------------------------------------
# Config management
# ---------------------------------------------------------------------------

def load_config() -> Dict:
    """Load monitor config."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"topics": [], "last_init": ""}


def save_config(config: Dict) -> None:
    """Save monitor config."""
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Config saved to %s", CONFIG_PATH)


def init_config() -> Dict:
    """Initialize config from pipeline topics.

    Extracts all topics, generates keyword lists, saves to config file.
    """
    topics = extract_pipeline_topics()
    config = {
        "topics": [],
        "last_init": datetime.now(timezone.utc).isoformat(),
    }

    for t in topics:
        config["topics"].append({
            "project": t["slug"],
            "topic": t["topic"],
            "type": t.get("type", "unknown"),
            "keywords": t["keywords"],
            "baseline_articles": t.get("baseline_articles", 2),
            "status": t.get("status", "UNKNOWN"),
            "project_path": t.get("project_path"),
            "last_checked": "",
        })

    save_config(config)
    logger.info("Initialized config with %d topics", len(config["topics"]))
    return config


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results: List[Dict[str, Any]]) -> str:
    """Generate NEWS-ALERTS.md from scan results."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# News Hook Alerts",
        "",
        f"**Generated:** {now}",
        f"**Topics scanned:** {len(results)}",
        "",
        "> Spike detection: URGENT = 3x+ baseline articles, TRENDING = 1.5x+ baseline.",
        "> Baseline = typical article count for this topic in a 7-day window.",
        "",
        "---",
        "",
    ]

    # Sort by level priority then article count
    level_order = {"URGENT": 0, "TRENDING": 1, "MONITORING": 2}
    results.sort(key=lambda r: (level_order.get(r.get("level", "MONITORING"), 3),
                                -r.get("article_count", 0)))

    # --- URGENT section ---
    urgent = [r for r in results if r.get("level") == "URGENT"]
    if urgent:
        lines.append("## URGENT — Publish Within 48h for Maximum Impact")
        lines.append("")
        for r in urgent:
            lines.append(f"### {r['topic']}")
            if r.get("project_path"):
                lines.append(f"**Project:** `{Path(r['project_path']).name}`")
            lines.append(f"**Status:** {r.get('status', '?')} | "
                         f"**Articles:** {r['article_count']} "
                         f"(baseline: {r['baseline']}, spike: {r['spike_ratio']}x)")
            lines.append(f"**Keywords:** {', '.join(r.get('keywords', []))}")
            lines.append("")
            lines.append("**Recent articles:**")
            for art in r.get("articles", [])[:5]:
                date_short = art.get("date", "?")[:16]
                lines.append(f"- [{art['title']}]({art['url']}) — {art['source']} ({date_short})")
            lines.append("")
            lines.append("**Recommended action:** Fast-track this topic. "
                         "News events create search demand spikes that decay within 1-2 weeks. "
                         "Prioritize publishing or accelerate research.")
            lines.append("")
        lines.append("---")
        lines.append("")

    # --- TRENDING section ---
    trending = [r for r in results if r.get("level") == "TRENDING"]
    if trending:
        lines.append("## TRENDING — Elevated News Coverage")
        lines.append("")
        for r in trending:
            lines.append(f"### {r['topic']}")
            if r.get("project_path"):
                lines.append(f"**Project:** `{Path(r['project_path']).name}`")
            lines.append(f"**Status:** {r.get('status', '?')} | "
                         f"**Articles:** {r['article_count']} "
                         f"(baseline: {r['baseline']}, spike: {r['spike_ratio']}x)")
            lines.append("")
            lines.append("**Recent articles:**")
            for art in r.get("articles", [])[:3]:
                date_short = art.get("date", "?")[:16]
                lines.append(f"- [{art['title']}]({art['url']}) — {art['source']} ({date_short})")
            lines.append("")
            lines.append("**Recommended action:** Consider accelerating production. "
                         "Monitor for further spike.")
            lines.append("")
        lines.append("---")
        lines.append("")

    # --- MONITORING section ---
    monitoring = [r for r in results if r.get("level") == "MONITORING"]
    if monitoring:
        lines.append("## MONITORING — Normal Baseline")
        lines.append("")
        lines.append("| Topic | Articles | Baseline | Status |")
        lines.append("|-------|----------|----------|--------|")
        for r in monitoring:
            topic_display = r["topic"][:40]
            lines.append(f"| {topic_display} | {r['article_count']} | "
                         f"{r['baseline']} | {r.get('status', '?')} |")
        lines.append("")

    # --- Summary ---
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **URGENT:** {len(urgent)} topics")
    lines.append(f"- **TRENDING:** {len(trending)} topics")
    lines.append(f"- **MONITORING:** {len(monitoring)} topics")
    lines.append("")
    lines.append("*Run `python -m tools.discovery.news_hook_monitor --scan` to refresh.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="News Hook Monitor — detect publishing windows for pipeline topics",
    )
    parser.add_argument("--scan", action="store_true",
                        help="Scan all pipeline topics for news")
    parser.add_argument("--topic", type=str,
                        help="Scan a specific topic by keyword match")
    parser.add_argument("--init", action="store_true",
                        help="Initialize config from pipeline topics")
    parser.add_argument("--report", action="store_true",
                        help="Generate NEWS-ALERTS.md report")
    parser.add_argument("--no-cache", action="store_true",
                        help="Bypass cache, fetch fresh data")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    # Default to --scan --report if no action specified
    if not any([args.scan, args.topic, args.init, args.report]):
        args.scan = True
        args.report = True

    # --- Init config ---
    if args.init:
        config = init_config()
        print(f"Initialized config with {len(config['topics'])} topics")
        for t in config["topics"]:
            print(f"  [{t['status'][:8]:>8}] {t['topic']:<45} ({len(t['keywords'])} keywords)")
        return

    # --- Load or create config ---
    config = load_config()
    if not config.get("topics"):
        logger.info("No config found, initializing from pipeline...")
        config = init_config()

    # --- Filter topics if --topic specified ---
    topics_to_scan = config["topics"]
    if args.topic:
        query = args.topic.lower()
        topics_to_scan = [
            t for t in topics_to_scan
            if query in t["topic"].lower()
            or any(query in kw.lower() for kw in t.get("keywords", []))
            or query in t.get("project", "").lower()
        ]
        if not topics_to_scan:
            print(f"No topics match '{args.topic}'")
            return

    # --- Scan ---
    results = []
    if args.scan or args.report:
        total = len(topics_to_scan)
        print(f"Scanning {total} topics for news hooks...\n")

        for i, topic_cfg in enumerate(topics_to_scan, 1):
            # Convert config format to scan format
            scan_input = {
                "slug": topic_cfg.get("project", topic_cfg.get("slug", "")),
                "topic": topic_cfg["topic"],
                "type": topic_cfg.get("type", "unknown"),
                "keywords": topic_cfg.get("keywords", []),
                "baseline_articles": topic_cfg.get("baseline_articles", 2),
                "status": topic_cfg.get("status", "UNKNOWN"),
                "project_path": topic_cfg.get("project_path"),
            }

            label = topic_cfg["topic"][:40]
            print(f"  [{i}/{total}] {label}...", end="", flush=True)

            result = scan_topic(scan_input, use_cache=not args.no_cache)
            results.append(result)

            # Update config with last_checked
            topic_cfg["last_checked"] = datetime.now(timezone.utc).isoformat()
            topic_cfg["baseline_articles"] = max(
                topic_cfg.get("baseline_articles", 2),
                1,  # Never let baseline drop to 0
            )

            level = result.get("level", "?")
            count = result.get("article_count", 0)
            marker = {"URGENT": " !!!", "TRENDING": " !", "MONITORING": ""}
            print(f" {count} articles [{level}]{marker.get(level, '')}")

        save_config(config)

        # Print summary
        urgent = sum(1 for r in results if r.get("level") == "URGENT")
        trending = sum(1 for r in results if r.get("level") == "TRENDING")
        print(f"\nDone. URGENT: {urgent} | TRENDING: {trending} | "
              f"MONITORING: {len(results) - urgent - trending}")

    # --- Generate report ---
    if args.report and results:
        report = generate_report(results)
        ALERTS_PATH.write_text(report, encoding="utf-8")
        print(f"\nReport saved to {ALERTS_PATH}")
    elif args.report and not results:
        # Use cached results
        cache = _load_cache()
        if cache:
            results = list(cache.values())
            report = generate_report(results)
            ALERTS_PATH.write_text(report, encoding="utf-8")
            print(f"\nReport generated from cache, saved to {ALERTS_PATH}")
        else:
            print("No cached results. Run --scan first.")


if __name__ == "__main__":
    main()
