"""
competitor_tracker.py — RSS feed fetcher + YouTube Data API enrichment

Tracks competitor channels by:
    1. Fetching the last 15 videos per channel via YouTube RSS feeds
       (free, no API quota, officially supported by YouTube)
    2. Enriching video data (view counts, duration) via YouTube Data API
       videos.list — 1 quota unit per call, 50 IDs per call
       NEVER uses search.list (100 units) — see RESEARCH.md Pitfall 4

Channel registry is loaded from competitor_channels.json (same directory).
Auth reuses the existing tools/youtube-analytics/auth.py pattern.

All public functions follow the error-dict pattern: return {'error': msg}
on failure, never raise.
"""

import json
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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

# Default path to channel config JSON (same directory as this module)
_DEFAULT_CONFIG_PATH = Path(__file__).parent / "competitor_channels.json"

# ---------------------------------------------------------------------------
# ISO 8601 duration parsing
# ---------------------------------------------------------------------------

_ISO_DURATION_RE = re.compile(
    r"^PT"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?$",
    re.IGNORECASE,
)


def parse_iso_duration(duration_str: str) -> int:
    """
    Convert ISO 8601 duration string to total seconds.

    Handles hours, minutes, and seconds components.

    Args:
        duration_str: ISO 8601 duration, e.g. 'PT15M30S', 'PT1H2M3S', 'PT45S'

    Returns:
        Total seconds as int, or 0 if parsing fails

    Examples:
        parse_iso_duration('PT15M30S')  -> 930
        parse_iso_duration('PT1H2M3S') -> 3723
        parse_iso_duration('PT45S')    -> 45
        parse_iso_duration('')         -> 0
    """
    if not duration_str:
        return 0
    match = _ISO_DURATION_RE.match(duration_str.strip())
    if not match:
        return 0
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)
    return hours * 3600 + minutes * 60 + seconds


# ---------------------------------------------------------------------------
# Channel config loader
# ---------------------------------------------------------------------------

def load_channel_config(config_path: str | Path | None = None) -> list[dict]:
    """
    Load competitor channel list from JSON config file.

    Args:
        config_path: Path to competitor_channels.json.
                     Defaults to the file in the same directory as this module.

    Returns:
        List of channel dicts with 'id', 'name', 'category' fields.
        Returns {'error': str} if the file is missing or malformed.
    """
    path = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        channels = data.get("channels", [])
        if not isinstance(channels, list):
            return {"error": f"competitor_channels.json 'channels' key is not a list"}
        return channels
    except FileNotFoundError:
        return {"error": f"Channel config not found: {path}"}
    except json.JSONDecodeError as exc:
        return {"error": f"Invalid JSON in channel config: {exc}"}
    except Exception as exc:
        return {"error": f"load_channel_config failed: {exc}"}


# ---------------------------------------------------------------------------
# RSS feed fetcher
# ---------------------------------------------------------------------------

def fetch_channel_rss(channel_id: str, channel_name: str) -> dict:
    """
    Fetch the last 15 videos from a YouTube channel's RSS feed.

    Uses feedparser to parse YouTube's official RSS feed:
        https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID

    Args:
        channel_id:   YouTube channel ID
        channel_name: Human-readable name (for error messages)

    Returns:
        {
            'channel_id':   str,
            'channel_name': str,
            'videos': [
                {
                    'video_id':    str,
                    'title':       str,
                    'published':   str,   # ISO 8601 from feed
                    'description': str,   # first 500 chars
                    'channel_id':  str,
                    'channel_name':str,
                }
            ]
        }
        or {'error': str}
    """
    if not FEEDPARSER_AVAILABLE:
        return {
            "error": f"feedparser not installed — cannot fetch RSS for '{channel_name}'. "
                     "Run: pip install feedparser"
        }

    url = YOUTUBE_RSS_URL.format(channel_id=channel_id)
    try:
        feed = feedparser.parse(url)

        # bozo flag means the feed was malformed, but may still have entries
        if feed.bozo and not feed.entries:
            bozo_exc = getattr(feed, "bozo_exception", "unknown parse error")
            return {"error": f"RSS parse failed for '{channel_name}': {bozo_exc}"}

        videos = []
        for entry in feed.entries:
            video_id = getattr(entry, "yt_videoid", None)
            if not video_id:
                # Skip entries without a video ID
                continue
            description = ""
            if hasattr(entry, "summary"):
                description = entry.summary[:500]
            videos.append({
                "video_id": video_id,
                "title": getattr(entry, "title", ""),
                "published": getattr(entry, "published", ""),
                "description": description,
                "channel_id": channel_id,
                "channel_name": channel_name,
            })

        return {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "videos": videos,
        }

    except Exception as exc:
        return {"error": f"RSS fetch failed for '{channel_name}': {exc}"}


# ---------------------------------------------------------------------------
# YouTube Data API enrichment
# ---------------------------------------------------------------------------

def enrich_videos_with_metadata(video_ids: list[str]) -> dict:
    """
    Batch fetch view counts, likes, and duration for YouTube video IDs.

    Uses YouTube Data API videos.list (1 quota unit per call, 50 IDs max).
    NEVER uses search.list (100 units each) — see RESEARCH.md Pitfall 4.

    Auth uses the existing tools/youtube-analytics/auth.py pattern.
    If auth fails (no token, no client_secret.json), returns graceful error
    so caller can proceed with RSS-only data.

    Args:
        video_ids: List of YouTube video ID strings

    Returns:
        {
            video_id: {
                'views':            int,
                'likes':            int,
                'duration_seconds': int,
            }
        }
        or {'error': str}

    Note:
        Batches input in groups of 50 if len(video_ids) > 50.
    """
    if not video_ids:
        return {}

    # Auth: reuse tools/youtube-analytics/auth.py (same pattern as analyze.py)
    try:
        _auth_dir = Path(__file__).parent.parent / "youtube-analytics"
        if str(_auth_dir) not in sys.path:
            sys.path.insert(0, str(_auth_dir))
        from auth import get_authenticated_service  # noqa: F401
        youtube = get_authenticated_service("youtube", "v3")
    except FileNotFoundError as exc:
        return {"error": f"YouTube API not authenticated: {exc}"}
    except Exception as exc:
        return {"error": f"YouTube API auth failed: {exc}"}

    result = {}
    # Batch in groups of 50 (API limit per call)
    for batch_start in range(0, len(video_ids), 50):
        batch = video_ids[batch_start : batch_start + 50]
        try:
            response = youtube.videos().list(
                part="statistics,contentDetails",
                id=",".join(batch),
            ).execute()

            for item in response.get("items", []):
                vid_id = item["id"]
                stats = item.get("statistics", {})
                content = item.get("contentDetails", {})
                duration_str = content.get("duration", "")
                result[vid_id] = {
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "duration_seconds": parse_iso_duration(duration_str),
                }
        except Exception as exc:
            # Return what we have so far + the error
            result["_error"] = f"API enrichment batch {batch_start//50 + 1} failed: {exc}"
            break

    return result


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def fetch_all_competitors(config_path: str | Path | None = None) -> dict:
    """
    Fetch RSS feeds for all configured competitor channels and enrich
    with YouTube API metadata.

    Process:
        1. Load channel config from JSON
        2. Fetch RSS feed for each active channel
        3. Collect all video IDs
        4. Batch enrich with YouTube Data API (view counts + duration)
        5. Merge RSS data + API enrichment into unified video list

    Args:
        config_path: Optional path to competitor_channels.json.
                     Defaults to the file next to this module.

    Returns:
        {
            'channels_fetched': int,
            'videos_total':     int,
            'videos': [
                {
                    'video_id':        str,
                    'channel_id':      str,
                    'channel_name':    str,
                    'title':           str,
                    'published_at':    str,
                    'description':     str,
                    'views':           int | None,
                    'likes':           int | None,
                    'duration_seconds':int | None,
                }
            ],
            'errors': [str]   # non-fatal errors (individual channel failures)
        }
        or {'error': str}  # fatal error (config failure)
    """
    # 1. Load channel config
    channels = load_channel_config(config_path)
    if isinstance(channels, dict) and "error" in channels:
        return channels  # Fatal — can't proceed without channel list

    if not channels:
        return {"error": "No channels configured in competitor_channels.json"}

    errors = []
    all_videos = []
    channels_fetched = 0

    # 2. Fetch RSS for each channel
    for channel in channels:
        channel_id = channel.get("id")
        channel_name = channel.get("name", channel_id)

        if not channel_id:
            errors.append(f"Channel entry missing 'id' field: {channel}")
            continue

        rss_result = fetch_channel_rss(channel_id, channel_name)

        if "error" in rss_result:
            errors.append(f"{channel_name}: {rss_result['error']}")
            continue

        all_videos.extend(rss_result.get("videos", []))
        channels_fetched += 1

    # 3. Collect all video IDs for batch enrichment
    video_ids = [v["video_id"] for v in all_videos if v.get("video_id")]

    # 4. Batch enrich with YouTube API (graceful fallback if auth fails)
    enrichment = {}
    if video_ids:
        enrichment_result = enrich_videos_with_metadata(video_ids)
        if isinstance(enrichment_result, dict) and "error" in enrichment_result:
            # Whole enrichment failed — log as non-fatal error, continue with RSS-only
            errors.append(f"API enrichment failed (RSS-only mode): {enrichment_result['error']}")
        else:
            # Extract any batch-level error
            if "_error" in enrichment_result:
                errors.append(enrichment_result.pop("_error"))
            enrichment = enrichment_result

    # 5. Merge RSS data + API enrichment
    merged_videos = []
    for video in all_videos:
        vid_id = video.get("video_id")
        meta = enrichment.get(vid_id, {})
        merged_videos.append({
            "video_id":         vid_id,
            "channel_id":       video.get("channel_id"),
            "channel_name":     video.get("channel_name"),
            "title":            video.get("title"),
            "published_at":     video.get("published"),
            "description":      video.get("description"),
            "views":            meta.get("views"),
            "likes":            meta.get("likes"),
            "duration_seconds": meta.get("duration_seconds"),
        })

    return {
        "channels_fetched": channels_fetched,
        "videos_total": len(merged_videos),
        "videos": merged_videos,
        "errors": errors,
    }
