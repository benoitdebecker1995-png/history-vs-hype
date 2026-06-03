"""
rescan_corpus.py — Grow the benchmark corpus depth from the canonical channel list.

The benchmark thumbnail/transcript corpus is built from `raw_data/*.json`. The old
`extract_channel_data.py` drove that scrape from a HARDCODED channel dict capped at 50
videos/channel — so (a) channels added to `tools/intel/competitor_channels.json` (the
single source of truth) never entered the corpus, and (b) `download_thumbnails.py` could
only ever see those 50. This tool fixes both: it reads the canonical channel list and
re-scrapes each channel up to a configurable cap, writing/merging `raw_data/{slug}.json`
in the existing schema so the downstream thumbnail/transcript pipeline grows in depth.

Why this is the real lever (not recency): per-channel OUTLIER n is the binding constraint
on the thumbnail playbook (most channels sit at 3-8 outliers → "directional, not locked").
More videos/channel → more outliers/channel. See
`memory/reference-corpus-refresh-mechanics.md`.

Usage:
    # Re-scan all canonical channels, 120 videos each (flat = fast, ids+titles, no views):
    python -m tools.benchmark.rescan_corpus --cap 120

    # Only specific channels:
    python -m tools.benchmark.rescan_corpus --cap 150 --channels "Voices of the Past,ReligionForBreakfast"

    # Also fetch per-video view counts (SLOW — one yt-dlp call per video; needed for
    # outlier detection, not for thumbnails):
    python -m tools.benchmark.rescan_corpus --cap 100 --details

After running, grow the actual corpus:
    python tools/benchmark/download_thumbnails.py     # thumbnails for the expanded set
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

_BENCH_DIR = Path(__file__).parent
_RAW_DIR = _BENCH_DIR / "raw_data"
_CONFIG = _BENCH_DIR.parent / "intel" / "competitor_channels.json"


def _slug(name: str) -> str:
    """raw_data filename convention: lowercase, spaces->underscores (e.g. 'Atun-Shei Films'->'atun-shei_films')."""
    return name.lower().replace(" ", "_")


def load_channels(only: set[str] | None) -> list[dict]:
    """Load the canonical tracked-channel list from competitor_channels.json."""
    data = json.loads(_CONFIG.read_text(encoding="utf-8"))
    chans = [c for c in data.get("channels", []) if c.get("id")]
    if only:
        chans = [c for c in chans if c["name"] in only]
    return chans


def flat_scrape(channel_id: str, cap: int) -> list[dict]:
    """Fast: one yt-dlp call returns up to `cap` video ids/titles/durations (no view counts)."""
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    cmd = [
        "yt-dlp", "--flat-playlist", "--dump-json",
        "--no-warnings", f"--playlist-end={cap}", url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        print(f"    TIMEOUT scraping {channel_id}")
        return []
    if result.returncode != 0:
        print(f"    ERROR ({channel_id}): {result.stderr[:160]}")
        return []
    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("id"):
            videos.append({
                "id": d.get("id"),
                "title": d.get("title"),
                "duration": d.get("duration"),
                "view_count": d.get("view_count"),  # often present in flat for channels
                "description": (d.get("description") or "")[:200],
            })
    return videos


def fetch_details(video_ids: list[str]) -> dict[str, dict]:
    """SLOW: one yt-dlp call per video for full metadata incl. view_count."""
    out = {}
    for i, vid in enumerate(video_ids, 1):
        cmd = ["yt-dlp", "--dump-json", "--skip-download", "--no-warnings",
               f"https://www.youtube.com/watch?v={vid}"]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
            if r.returncode == 0 and r.stdout.strip():
                d = json.loads(r.stdout)
                out[vid] = {
                    "view_count": d.get("view_count"),
                    "like_count": d.get("like_count"),
                    "upload_date": d.get("upload_date"),
                    "channel_subscriber_count": d.get("channel_follower_count"),
                }
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            continue
        if i % 25 == 0:
            print(f"      details {i}/{len(video_ids)}")
    return out


def write_channel(channel: dict, videos: list[dict]) -> Path:
    """Merge scraped videos into raw_data/{slug}.json, preserving existing analysis fields."""
    path = _RAW_DIR / f"{_slug(channel['name'])}.json"
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    existing.update({
        "name": channel["name"],
        "format_match": existing.get("format_match", channel.get("category")),
        "notes": existing.get("notes", channel.get("notes", "")),
        "all_videos": videos,
        "videos_analyzed": len(videos),
    })
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-scan canonical channels into raw_data with a configurable cap.")
    ap.add_argument("--cap", type=int, default=120, help="max videos per channel (default 120)")
    ap.add_argument("--channels", type=str, default=None, help="comma-separated channel names (default: all)")
    ap.add_argument("--details", action="store_true", help="also fetch per-video view counts (SLOW)")
    args = ap.parse_args()

    if not _CONFIG.exists():
        print(f"Channel config not found: {_CONFIG}")
        return 1
    _RAW_DIR.mkdir(parents=True, exist_ok=True)

    only = {c.strip() for c in args.channels.split(",")} if args.channels else None
    channels = load_channels(only)
    if not channels:
        print("No matching channels.")
        return 1

    print(f"Re-scanning {len(channels)} channel(s), cap={args.cap}, details={args.details}\n")
    total = 0
    for ch in channels:
        print(f"[{ch['name']}] ({ch['id']})")
        vids = flat_scrape(ch["id"], args.cap)
        if not vids:
            print("    no videos — skipped\n")
            continue
        if args.details:
            print(f"    fetching view details for {len(vids)} videos (slow)...")
            det = fetch_details([v["id"] for v in vids])
            for v in vids:
                v.update(det.get(v["id"], {}))
        path = write_channel(ch, vids)
        total += len(vids)
        print(f"    {len(vids)} videos -> {path.name}\n")

    print(f"Done. {total} videos across {len(channels)} channel(s).")
    print("Next: python tools/benchmark/download_thumbnails.py  (grows the thumbnail corpus)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
