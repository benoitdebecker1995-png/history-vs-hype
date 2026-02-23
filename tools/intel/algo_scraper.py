"""
algo_scraper.py — Algorithm source scraper for the YouTube Intelligence Engine

Scrapes authoritative YouTube algorithm content from:
    - Blog sources (requests + simple HTML-to-text)
    - YouTube RSS feeds (feedparser)

Sources are intentionally limited to HIGH/MEDIUM-HIGH authority per RESEARCH.md.
BeautifulSoup is NOT used — simple regex text extraction is sufficient;
the LLM synthesis step (algo_synthesizer.py) handles messy text.

feedparser is imported with graceful fallback in case it's not installed.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# feedparser import with graceful fallback
# ---------------------------------------------------------------------------
try:
    import feedparser  # pip install feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

# requests is already installed (tools/youtube-analytics uses it)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ---------------------------------------------------------------------------
# YouTube RSS URL template (also used for Creator Insider)
# ---------------------------------------------------------------------------
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

# ---------------------------------------------------------------------------
# Authoritative algorithm sources
# ---------------------------------------------------------------------------
# Creator Insider channel ID: UCkRfArvrzheW2E7b6SVT7vQ
#   Source: https://www.youtube.com/@YouTube Creators (formerly Creator Insider)
#   NOTE: Verify by visiting https://www.youtube.com/channel/UCkRfArvrzheW2E7b6SVT7vQ
#   Verified against RSS feed 2026-02-23. Old ID UCr-pWa7LMHX71Uhr7D4wqMQ was 404.
ALGO_SOURCES = [
    {
        "name": "vidIQ Algorithm Guide",
        "url": "https://vidiq.com/blog/post/understanding-youtube-algorithm/",
        "type": "blog",
        "authority": "high",
        "notes": "Industry tool with proprietary YouTube data access",
    },
    {
        "name": "OutlierKit Algorithm Updates",
        "url": "https://outlierkit.com/resources/youtube-algorithm-updates/",
        "type": "blog",
        "authority": "high",
        "notes": "Niche tool focused on YouTube algorithm mechanics",
    },
    {
        "name": "Creator Insider YouTube",
        "channel_id": "UCkRfArvrzheW2E7b6SVT7vQ",
        "type": "rss",
        "authority": "highest",
        "notes": "YouTube's own official creator-facing channel — primary algorithm source",
    },
    {
        "name": "Buffer YouTube Resources",
        "url": "https://buffer.com/resources/youtube-algorithm/",
        "type": "blog",
        "authority": "medium",
        "notes": "Marketing platform; covers browse vs search distinction well",
    },
    {
        "name": "marketingagent Algorithm Signals",
        "url": "https://marketingagent.blog/2025/11/04/youtubes-recommendation-algorithm-satisfaction-signals-what-you-can-control/",
        "type": "blog",
        "authority": "medium",
        "notes": "Covers named satisfaction signals: WSS, QCR, RD, VLI",
    },
]

# ---------------------------------------------------------------------------
# HTML text extraction
# ---------------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_MAX_CONTENT_CHARS = 8000  # Prevent token explosion in LLM synthesis


def _html_to_text(html: str, max_chars: int = _MAX_CONTENT_CHARS) -> str:
    """
    Strip HTML tags and collapse whitespace. Limit output length.

    Args:
        html:      Raw HTML string
        max_chars: Maximum characters to return

    Returns:
        Plain text string, truncated to max_chars
    """
    text = _HTML_TAG_RE.sub(" ", html)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text[:max_chars]


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Core scraping functions
# ---------------------------------------------------------------------------

def scrape_source(source: dict) -> dict:
    """
    Fetch content from a single algorithm source.

    For 'rss' type:   Parse YouTube RSS feed with feedparser. Concatenate
                      entry titles and summaries (up to 10 entries).
    For 'blog' type:  GET with User-Agent header, extract text via regex,
                      limit to _MAX_CONTENT_CHARS.

    Args:
        source: Dict from ALGO_SOURCES with at minimum 'name' and 'type' keys.
                RSS sources need 'channel_id'; blog sources need 'url'.

    Returns:
        {'source': name, 'content': text, 'fetched_at': iso_timestamp}
        or {'error': str}
    """
    name = source.get("name", "unknown")
    source_type = source.get("type", "blog")
    fetched_at = _now_iso()

    if source_type == "rss":
        if not FEEDPARSER_AVAILABLE:
            return {"error": f"feedparser not installed — cannot scrape RSS source '{name}'"}
        channel_id = source.get("channel_id")
        if not channel_id:
            return {"error": f"RSS source '{name}' missing channel_id"}
        url = YOUTUBE_RSS_URL.format(channel_id=channel_id)
        try:
            # Fetch with requests first for HTTP status visibility, then parse
            if REQUESTS_AVAILABLE:
                resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 404:
                    return {"error": f"RSS 404 for '{name}': channel ID '{channel_id}' not found"}
                if resp.status_code != 200:
                    return {"error": f"RSS HTTP {resp.status_code} for '{name}'"}
                feed = feedparser.parse(resp.text)
            else:
                feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                bozo_exc = getattr(feed, "bozo_exception", "unknown parse error")
                return {"error": f"RSS parse failed for '{name}': {bozo_exc}"}
            parts = []
            for entry in feed.entries[:10]:
                title = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                parts.append(f"{title}: {summary}")
            content = _html_to_text("\n".join(parts))
            return {
                "source": name,
                "content": content,
                "fetched_at": fetched_at,
                "authority": source.get("authority", "medium"),
            }
        except Exception as exc:
            return {"error": f"RSS scrape failed for '{name}': {exc}"}

    else:  # blog type
        if not REQUESTS_AVAILABLE:
            return {"error": f"requests not installed — cannot scrape blog source '{name}'"}
        url = source.get("url")
        if not url:
            return {"error": f"Blog source '{name}' missing url"}
        try:
            resp = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                },
            )
            resp.raise_for_status()
            content = _html_to_text(resp.text)
            return {
                "source": name,
                "content": content,
                "fetched_at": fetched_at,
                "authority": source.get("authority", "medium"),
            }
        except Exception as exc:
            return {"error": f"Blog scrape failed for '{name}': {exc}"}


def scrape_all_sources(sources: list[dict] | None = None) -> list[dict]:
    """
    Scrape all algorithm sources (or a custom list).

    Args:
        sources: List of source dicts. Defaults to ALGO_SOURCES.

    Returns:
        List of results — each is either a success dict or an {'error': str} dict.
        Always returns a list even if all sources fail.
    """
    if sources is None:
        sources = ALGO_SOURCES
    results = []
    for source in sources:
        result = scrape_source(source)
        results.append(result)
    return results
