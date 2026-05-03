"""
Competitor drop scanner.

Reads channel-data/competitor-channels.yaml, fetches YouTube RSS for each
channel, flags any upload from the last LOOKBACK_HOURS. Compares against
active projects in video-projects/_IN_PRODUCTION/ and channel-data/TOPIC-PIPELINE.md
for topic overlap.

Outputs:
- channel-data/competitor-drops/YYYY-MM-DD.json   (machine-readable)
- channel-data/competitor-drops/YYYY-MM-DD.md     (human report)

CLI:
    python -m tools.routines.competitor_drop_scan
    python -m tools.routines.competitor_drop_scan --lookback-hours 48
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = REPO_ROOT / "channel-data" / "competitor-channels.yaml"
PIPELINE_FILE = REPO_ROOT / "channel-data" / "TOPIC-PIPELINE.md"
PRODUCTION_DIR = REPO_ROOT / "video-projects" / "_IN_PRODUCTION"
OUTPUT_DIR = REPO_ROOT / "channel-data" / "competitor-drops"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (compatible; HvHCompetitorScan/1.0)"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
YT_NS = "{http://www.youtube.com/xml/schemas/2015}"
LOOKBACK_HOURS_DEFAULT = 24


def fetch(url: str, timeout: int = 15) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def resolve_channel_id(handle: str) -> str | None:
    """Scrape YouTube channel page to extract channel_id from @handle."""
    url = f"https://www.youtube.com/{handle.lstrip('@')}"
    if not url.startswith("https://www.youtube.com/@"):
        url = f"https://www.youtube.com/@{handle.lstrip('@')}"
    try:
        html = fetch(url)
    except Exception:
        return None
    m = re.search(r'"channelId":"(UC[\w-]{20,})"', html) or \
        re.search(r'channel/(UC[\w-]{20,})', html)
    return m.group(1) if m else None


def fetch_channel_uploads(channel_id: str) -> list[dict]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        xml = fetch(url)
    except Exception as e:
        return [{"error": f"fetch failed: {e}"}]
    root = ET.fromstring(xml)
    entries = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        vid_el = entry.find(f"{YT_NS}videoId")
        title_el = entry.find(f"{ATOM_NS}title")
        published_el = entry.find(f"{ATOM_NS}published")
        link_el = entry.find(f"{ATOM_NS}link")
        if vid_el is None or title_el is None or published_el is None:
            continue
        entries.append({
            "video_id": vid_el.text,
            "title": title_el.text,
            "published": published_el.text,
            "url": link_el.get("href") if link_el is not None else None,
        })
    return entries


def within_lookback(iso_date: str, hours: int) -> bool:
    published = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return published >= cutoff


def load_config() -> dict:
    return yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))


def save_config(data: dict) -> None:
    CONFIG_FILE.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def active_topics() -> list[dict]:
    """Collect topic signals from active projects + TOPIC-PIPELINE.md."""
    topics = []
    if PRODUCTION_DIR.exists():
        for project_dir in PRODUCTION_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            metadata = project_dir / "YOUTUBE-METADATA.md"
            if metadata.exists():
                text = metadata.read_text(encoding="utf-8", errors="replace")
                topics.append({
                    "source": f"project:{project_dir.name}",
                    "text": text[:8000],
                })
    if PIPELINE_FILE.exists():
        topics.append({
            "source": "TOPIC-PIPELINE.md",
            "text": PIPELINE_FILE.read_text(encoding="utf-8", errors="replace"),
        })
    return topics


def keyword_overlap(video_title: str, topics: list[dict]) -> list[str]:
    """Very simple bag-of-words overlap. Returns matching topic sources."""
    title_tokens = {t for t in re.findall(r"\w{4,}", video_title.lower())}
    stop = {"that", "with", "they", "this", "from", "were", "have", "video",
            "their", "which", "about", "when", "your", "than", "what", "would"}
    title_tokens -= stop
    matches = []
    for topic in topics:
        topic_tokens = {t for t in re.findall(r"\w{4,}", topic["text"].lower())}
        topic_tokens -= stop
        shared = title_tokens & topic_tokens
        if len(shared) >= 2:
            matches.append({"source": topic["source"], "shared_keywords": sorted(shared)})
    return matches


def scan(lookback_hours: int) -> dict:
    config = load_config()
    topics = active_topics()
    config_changed = False
    drops = []

    for channel in config.get("channels", []):
        if not channel.get("channel_id") and channel.get("handle"):
            resolved = resolve_channel_id(channel["handle"])
            if resolved:
                channel["channel_id"] = resolved
                config_changed = True
        if not channel.get("channel_id"):
            drops.append({
                "channel": channel["name"],
                "error": f"Could not resolve channel_id for {channel.get('handle')}",
            })
            continue

        uploads = fetch_channel_uploads(channel["channel_id"])
        for upload in uploads:
            if "error" in upload:
                drops.append({"channel": channel["name"], **upload})
                continue
            if not within_lookback(upload["published"], lookback_hours):
                continue
            overlap = keyword_overlap(upload["title"], topics)
            drops.append({
                "channel": channel["name"],
                "video_id": upload["video_id"],
                "title": upload["title"],
                "published": upload["published"],
                "url": upload["url"],
                "niche_relevance": channel.get("niche_relevance", "medium"),
                "topic_overlap": overlap,
                "is_collision": bool(overlap),
            })

    if config_changed:
        save_config(config)

    return {"drops": drops}


def render_report(today_str: str, result: dict) -> str:
    drops = result["drops"]
    collisions = [d for d in drops if d.get("is_collision")]
    new_uploads = [d for d in drops if "video_id" in d and not d.get("is_collision")]
    errors = [d for d in drops if "error" in d]

    lines = [
        f"# Competitor Drops — {today_str}",
        "",
        f"**New uploads detected:** {len(drops) - len(errors)}",
        f"**Topic collisions:** {len(collisions)}",
        f"**Errors:** {len(errors)}",
        "",
    ]
    if collisions:
        lines.append("## COLLISIONS (review today)")
        lines.append("")
        for d in collisions:
            lines.append(f"### {d['channel']} — {d['title']}")
            lines.append(f"- URL: {d['url']}")
            lines.append(f"- Published: {d['published']}")
            lines.append(f"- Niche relevance: {d['niche_relevance']}")
            for o in d["topic_overlap"]:
                lines.append(f"- Overlap with `{o['source']}`: {', '.join(o['shared_keywords'])}")
            lines.append("")
    if new_uploads:
        lines.append("## Other new uploads (no collision)")
        lines.append("")
        for d in new_uploads:
            lines.append(f"- **{d['channel']}** — [{d['title']}]({d['url']}) ({d['published'][:10]})")
        lines.append("")
    if errors:
        lines.append("## Errors")
        lines.append("")
        for e in errors:
            lines.append(f"- {e.get('channel', '?')}: {e['error']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback-hours", type=int, default=LOOKBACK_HOURS_DEFAULT)
    args = parser.parse_args()

    today = datetime.now().date().isoformat()
    print(f"Scanning competitors (last {args.lookback_hours}h)...")
    result = scan(args.lookback_hours)

    (OUTPUT_DIR / f"{today}.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    report = render_report(today, result)
    report_path = OUTPUT_DIR / f"{today}.md"
    report_path.write_text(report, encoding="utf-8")

    collisions = sum(1 for d in result["drops"] if d.get("is_collision"))
    print(f"Report: {report_path}")
    print(f"Collisions: {collisions}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
