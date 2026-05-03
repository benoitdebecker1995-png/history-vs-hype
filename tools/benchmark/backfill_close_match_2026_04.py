"""
Phase B (Thumbnail Notebook Audit) — extract 3 new close-match channels.

Date: 2026-04-26
Channels:
- PolyMatter — closest format match (talking-head + B-roll, hybrid history/geo)
- Asianometry — mechanism / HOW gap
- Lindybeige — myth-busting + primary sources, smaller-scale

Mirrors backfill_channels.py pattern but isolated to these 3 adds.
"""
import subprocess
import json
import time
from pathlib import Path

RAW_DIR = Path("tools/benchmark/raw_data")

NEW_CHANNELS = {
    "PolyMatter": {
        "url": "https://www.youtube.com/@PolyMatter/videos",
        "format_match": "HIGH",
        "notes": "Hybrid history/geo/business explainer, 8-15 min talking-head + B-roll, primary sources, document overlays",
    },
    "Asianometry": {
        "url": "https://www.youtube.com/@Asianometry/videos",
        "format_match": "HIGH",
        "notes": "Mechanism / HOW topics (industrial history, supply chain, geopolitics), faceless, document-heavy",
    },
    "Lindybeige": {
        "url": "https://www.youtube.com/@Lindybeige/videos",
        "format_match": "HIGH",
        "notes": "Myth-busting + primary sources, military/medieval focus, talking-head, eccentric brand",
    },
}


def extract_channel(name, info, max_videos=50):
    print(f"\n{'='*60}\nExtracting: {name}\nURL: {info['url']}\n{'='*60}")

    cmd = ["yt-dlp", "--flat-playlist", "--dump-json",
           f"--playlist-end={max_videos}", info["url"]]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:300]}")
        return None

    video_ids = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            if data.get("id"):
                video_ids.append(data["id"])
        except json.JSONDecodeError:
            continue
    print(f"  Found {len(video_ids)} video IDs")

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
                    "description": (data.get("description") or "")[:300],
                })
                v = details[-1]
                safe = (v['title'] or '')[:55].encode('ascii', 'replace').decode()
                vc = v.get('view_count') or 0
                print(f"    {safe:55s} | {vc:>12,} views")
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            continue
        time.sleep(0.3)  # gentle rate limit

    if not details:
        print(f"  No details extracted for {name}")
        return None

    view_counts = sorted([d["view_count"] for d in details if d.get("view_count")])
    if not view_counts:
        return None
    median = view_counts[len(view_counts) // 2]
    sub_count = details[0].get("channel_subscriber_count")

    outliers = sorted(
        [d for d in details if (d.get("view_count") or 0) >= median * 3],
        key=lambda x: x.get("view_count", 0), reverse=True
    )

    print(f"\n  Subs: {sub_count:,}" if sub_count else "\n  Subs: unknown")
    print(f"  Videos: {len(details)} | Median: {median:,} | Outliers (3x+): {len(outliers)}")

    return {
        "name": name,
        "subscriber_count": sub_count,
        "format_match": info["format_match"],
        "notes": info["notes"],
        "videos_analyzed": len(details),
        "median_views": median,
        "outlier_threshold": median * 3,
        "all_videos": details,
        "outliers": outliers,
        "hooks": {},
    }


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, info in NEW_CHANNELS.items():
        safe = name.lower().replace(" ", "_")
        out = RAW_DIR / f"{safe}.json"
        if out.exists():
            print(f"\n{name}: already extracted — delete {out} to re-extract")
            continue
        data = extract_channel(name, info)
        if data:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  Saved: {out}")
    print(f"\n{'='*60}\nEXTRACTION COMPLETE\n{'='*60}")


if __name__ == "__main__":
    main()
