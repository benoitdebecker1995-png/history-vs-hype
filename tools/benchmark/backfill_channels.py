"""
Backfill benchmark data from additional channels to close v7.0 data gaps:
1. versus title pattern (currently sample_count=1)
2. authority_challenge hook pattern (currently 0 examples)

Targets channels likely to have these patterns.
Run: python tools/benchmark/backfill_channels.py
Then: python tools/benchmark/build_deliverables.py
"""
import subprocess
import json
import re
import time
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    HAS_TRANSCRIPT_API = True
except ImportError:
    HAS_TRANSCRIPT_API = False

RAW_DIR = Path("tools/benchmark/raw_data")
HOOKS_FILE = RAW_DIR / "verified_hooks.json"

# New channels selected for gap coverage:
# - WonderWhy: geography/borders videos, likely versus titles
# - CaspianReport: geopolitics analysis, authority_challenge hooks
# - History Matters: prolific, short + long form, likely versus titles
NEW_CHANNELS = {
    "WonderWhy": {
        "url": "https://www.youtube.com/@WonderWhy/videos",
        "format_match": "HIGH",
        "notes": "Geography/geopolitics, map-heavy, borders/disputes"
    },
    "CaspianReport": {
        "url": "https://www.youtube.com/@CaspianReport/videos",
        "format_match": "HIGH",
        "notes": "Geopolitics analysis, authority-style narration"
    },
    "History Matters": {
        "url": "https://www.youtube.com/@HistoryMatters/videos",
        "format_match": "TITLE_PATTERN_ONLY",
        "notes": "Prolific short+long form, versus titles common. Hooks not format-matched (animation, not talking head)."
    },
    "Atun-Shei Films": {
        "url": "https://www.youtube.com/@atunsheifilms/videos",
        "format_match": "HIGH",
        "notes": "History myth-busting, page-number citations, documents on screen, talking head"
    },
    "Three Arrows": {
        "url": "https://www.youtube.com/@ThreeArrows/videos",
        "format_match": "HIGH",
        "notes": "Document-first debunking, academic sourcing, long-form history"
    },
    "TIKhistory": {
        "url": "https://www.youtube.com/@TheImperatorKnight/videos",
        "format_match": "HIGH",
        "notes": "Multi-source verification, buys books, shows sources, WWII focus"
    },
    "Shaun": {
        "url": "https://www.youtube.com/@Shaun_vids/videos",
        "format_match": "HIGH",
        "notes": "Document-first argumentation, chronological precision, debunking"
    },
    "Kings and Generals": {
        "url": "https://www.youtube.com/@KingsandGenerals/videos",
        "format_match": "ANIMATED_NO_TALKING_HEAD",
        "notes": "Military history, map-heavy, colonial content. Animated format, no talking head."
    },
    "Historia Civilis": {
        "url": "https://www.youtube.com/@HistoriaCivilis/videos",
        "format_match": "ANIMATED_NO_TALKING_HEAD",
        "notes": "Deep systems-thinking, causal chains, legal/constitutional focus. Animated, no talking head."
    },
}


def extract_channel(name, info, max_videos=50):
    """Extract video list + detailed metadata for a channel."""
    print(f"\n{'='*60}")
    print(f"Extracting: {name}")
    print(f"URL: {info['url']}")
    print(f"{'='*60}")

    # Step 1: flat playlist
    cmd = [
        "yt-dlp", "--flat-playlist", "--dump-json",
        f"--playlist-end={max_videos}", info["url"]
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
        return None

    video_ids = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            vid_id = data.get("id")
            if vid_id:
                video_ids.append(vid_id)
        except json.JSONDecodeError:
            continue

    print(f"  Found {len(video_ids)} videos")

    # Step 2: detailed metadata (need view counts + subscriber count)
    details = []
    for vid_id in video_ids:
        url = f"https://www.youtube.com/watch?v={vid_id}"
        cmd = ["yt-dlp", "--dump-json", "--skip-download", "--no-warnings", url]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                details.append({
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "view_count": data.get("view_count"),
                    "like_count": data.get("like_count"),
                    "duration": data.get("duration"),
                    "upload_date": data.get("upload_date"),
                    "channel": data.get("channel"),
                    "channel_subscriber_count": data.get("channel_follower_count"),
                    "description": data.get("description"),
                })
                v = details[-1]
                safe_title = (v['title'] or '')[:55].encode('ascii', 'replace').decode()
                print(f"    {safe_title:55s} | {v.get('view_count', 0):>12,} views")
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            continue

    if not details:
        print(f"  No details extracted for {name}")
        return None

    # Calculate stats
    view_counts = sorted([d["view_count"] for d in details if d.get("view_count")])
    if not view_counts:
        return None

    median_views = view_counts[len(view_counts) // 2]
    sub_count = details[0].get("channel_subscriber_count") if details else None

    outliers = [d for d in details if d.get("view_count", 0) >= median_views * 3]
    outliers.sort(key=lambda x: x.get("view_count", 0), reverse=True)

    print(f"\n  Subscribers: {sub_count:,}" if sub_count else "\n  Subscribers: unknown")
    print(f"  Videos: {len(details)} | Median: {median_views:,} | Outliers (3x): {len(outliers)}")

    channel_data = {
        "name": name,
        "subscriber_count": sub_count,
        "format_match": info["format_match"],
        "notes": info["notes"],
        "videos_analyzed": len(details),
        "median_views": median_views,
        "outlier_threshold": median_views * 3,
        "all_videos": details,
        "outliers": outliers,
        "hooks": {},
    }

    # Step 3: Extract hooks for format-matched channels only
    if info["format_match"] != "TITLE_PATTERN_ONLY" and HAS_TRANSCRIPT_API:
        outlier_ids = [o["id"] for o in outliers[:8]]
        print(f"\n  Extracting hooks for {len(outlier_ids)} outliers...")
        api = YouTubeTranscriptApi()
        for vid_id in outlier_ids:
            try:
                for langs in [["en"], ["en-GB"]]:
                    try:
                        transcript = api.fetch(vid_id, languages=langs)
                        lines = []
                        for entry in transcript:
                            if entry.start > 90:
                                break
                            text = entry.text.strip()
                            if text.startswith("[") and text.endswith("]"):
                                continue
                            if not text:
                                continue
                            lines.append(text)
                        if lines:
                            raw = re.sub(r'\s+', ' ', " ".join(lines))
                            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', raw)
                            hook = " ".join(sentences[:3]) if len(sentences) >= 3 else raw[:300]
                            channel_data["hooks"][vid_id] = hook
                            print(f"    {vid_id}: OK ({len(hook)} chars)")
                            break
                    except Exception:
                        continue
                else:
                    channel_data["hooks"][vid_id] = None
                    print(f"    {vid_id}: no transcript")
            except Exception as e:
                if "429" in str(e):
                    print(f"    RATE LIMITED — stopping hooks")
                    break
                channel_data["hooks"][vid_id] = None
            time.sleep(1.5)

    return channel_data


def update_hooks_file(channel_data_list):
    """Add new outlier hooks to verified_hooks.json."""
    with open(HOOKS_FILE, encoding="utf-8") as f:
        hooks = json.load(f)

    existing_ids = {h["id"] for h in hooks}
    added = 0

    for ch_data in channel_data_list:
        name = ch_data["name"]
        sub_count = ch_data["subscriber_count"] or 1
        median = ch_data["median_views"] or 1

        for outlier in ch_data["outliers"][:8]:
            vid_id = outlier["id"]
            if vid_id in existing_ids:
                continue

            hook_text = ch_data["hooks"].get(vid_id)
            hooks.append({
                "channel": name,
                "id": vid_id,
                "title": outlier["title"],
                "view_count": outlier["view_count"],
                "ratio": round(outlier["view_count"] / median, 1),
                "is_3x_outlier": True,
                "hook": hook_text,
                "hook_verified": bool(hook_text),
                "error": None if hook_text else "not_extracted",
            })
            added += 1

    with open(HOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(hooks, f, indent=2, ensure_ascii=False)

    print(f"\nAdded {added} new hook entries to {HOOKS_FILE}")
    return added


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for name, info in NEW_CHANNELS.items():
        safe_name = name.lower().replace(" ", "_")
        out_file = RAW_DIR / f"{safe_name}.json"

        # Skip if already extracted
        if out_file.exists():
            print(f"\n  {name}: already extracted ({out_file}), skipping.")
            print(f"  Delete the file to re-extract.")
            with open(out_file, encoding="utf-8") as f:
                results.append(json.load(f))
            continue

        data = extract_channel(name, info)
        if data:
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n  Saved: {out_file}")
            results.append(data)

    if results:
        update_hooks_file(results)

    print(f"\n{'='*60}")
    print("BACKFILL COMPLETE")
    print(f"New channels: {len(results)}")
    print(f"\nNext step: python tools/benchmark/build_deliverables.py")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
