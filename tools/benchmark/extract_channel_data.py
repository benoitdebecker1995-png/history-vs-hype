"""
Phase 66: Extract real video data from YouTube channels for benchmarking.
Uses yt-dlp for metadata and youtube-transcript-api for transcripts.
"""
import subprocess
import json
import sys
import os
from pathlib import Path

# Target channels with their YouTube handles
CHANNELS = {
    "Kraut": {
        "url": "https://www.youtube.com/@Kraut_the_Parrot/videos",
        "format_match": "HIGH",
        "notes": "Talking head + animated maps, documentary essay"
    },
    "Knowing Better": {
        "url": "https://www.youtube.com/@KnowingBetter/videos",
        "format_match": "HIGH",
        "notes": "Talking head, maps, source-heavy, 15-40 min"
    },
    "Toldinstone": {
        "url": "https://www.youtube.com/@toldinstone/videos",
        "format_match": "HIGH",
        "notes": "Talking head, primary source focus, ancient history"
    },
    "Fall of Civilizations": {
        "url": "https://www.youtube.com/@FallofCivilizations/videos",
        "format_match": "HIGH",
        "notes": "Cinematic narration, primary sources, long-form"
    },
    "RealLifeLore": {
        "url": "https://www.youtube.com/@RealLifeLore/videos",
        "format_match": "TITLE_PATTERN_ONLY",
        "notes": "Animated geography — title patterns only, NOT hooks"
    },
}

OUTPUT_DIR = Path("tools/benchmark/raw_data")


def extract_channel_videos(name, channel_info, max_videos=50):
    """Extract video metadata from a YouTube channel using yt-dlp."""
    print(f"\n{'='*60}")
    print(f"Extracting: {name}")
    print(f"URL: {channel_info['url']}")
    print(f"{'='*60}")

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        f"--playlist-end={max_videos}",
        channel_info["url"]
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
        return []

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            videos.append({
                "id": data.get("id"),
                "title": data.get("title"),
                "duration": data.get("duration"),
                "description": (data.get("description") or "")[:200],
            })
        except json.JSONDecodeError:
            continue

    print(f"  Found {len(videos)} videos (flat playlist, no view counts yet)")
    return videos


def get_video_details(video_ids, batch_label=""):
    """Get full metadata (including view counts) for specific videos."""
    print(f"\n  Getting detailed metadata for {len(video_ids)} videos {batch_label}...")
    details = []

    for vid_id in video_ids:
        url = f"https://www.youtube.com/watch?v={vid_id}"
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--skip-download",
            "--no-warnings",
            url
        ]
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
                })
                v = details[-1]
                safe_title = v['title'][:60].encode('ascii', 'replace').decode()
                print(f"    {safe_title:60s} | {v['view_count']:>12,} views")
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"    SKIP {vid_id}: {e}")
            continue

    return details


def extract_transcripts(video_ids):
    """Extract first 60 seconds of transcript for hook analysis."""
    from youtube_transcript_api import YouTubeTranscriptApi

    hooks = {}
    for vid_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid_id, languages=["en"])
            # Get first ~60 seconds
            first_lines = []
            for entry in transcript:
                if entry["start"] > 60:
                    break
                first_lines.append(entry["text"])

            full_text = " ".join(first_lines)
            # Extract first 2-3 sentences
            sentences = []
            current = ""
            for char in full_text:
                current += char
                if char in ".!?" and len(current.strip()) > 20:
                    sentences.append(current.strip())
                    current = ""
                    if len(sentences) >= 3:
                        break

            if sentences:
                hooks[vid_id] = " ".join(sentences)
                safe_hook = hooks[vid_id][:80].encode('ascii', 'replace').decode()
                print(f"    {vid_id}: \"{safe_hook}...\"")
            else:
                # Fallback: just take first 200 chars
                hooks[vid_id] = full_text[:200]
                safe_hook = hooks[vid_id][:80].encode('ascii', 'replace').decode()
                print(f"    {vid_id}: (no sentence breaks) \"{safe_hook}...\"")

        except Exception as e:
            print(f"    {vid_id}: TRANSCRIPT FAILED - {e}")
            hooks[vid_id] = None

    return hooks


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_channel_data = {}

    for name, info in CHANNELS.items():
        # Step 1: Get video list (flat, fast)
        videos = extract_channel_videos(name, info, max_videos=50)

        if not videos:
            print(f"  SKIPPING {name} - no videos extracted")
            continue

        # Step 2: Get detailed metadata for all videos (need view counts)
        video_ids = [v["id"] for v in videos if v.get("id")]
        details = get_video_details(video_ids, batch_label=f"({name})")

        if not details:
            print(f"  SKIPPING {name} - no details extracted")
            continue

        # Step 3: Calculate median and find outliers
        view_counts = sorted([d["view_count"] for d in details if d.get("view_count")])
        if not view_counts:
            continue

        median_views = view_counts[len(view_counts) // 2]
        sub_count = details[0].get("channel_subscriber_count") if details else None

        print(f"\n  Channel: {name}")
        print(f"  Subscribers: {sub_count:,}" if sub_count else "  Subscribers: unknown")
        print(f"  Videos analyzed: {len(details)}")
        print(f"  Median views: {median_views:,}")
        print(f"  Outlier threshold (3x): {median_views * 3:,}")

        outliers = [d for d in details if d.get("view_count", 0) >= median_views * 3]
        outliers.sort(key=lambda x: x.get("view_count", 0), reverse=True)

        print(f"  Outliers found: {len(outliers)}")
        for o in outliers[:10]:
            ratio = o["view_count"] / median_views if median_views > 0 else 0
            safe_t = o['title'][:60].encode('ascii', 'replace').decode()
            print(f"    {ratio:.1f}x | {o['view_count']:>12,} | {safe_t}")

        # Step 4: Extract transcripts for outlier videos (hooks)
        if info["format_match"] != "TITLE_PATTERN_ONLY":
            outlier_ids = [o["id"] for o in outliers[:8]]
            print(f"\n  Extracting transcripts for {len(outlier_ids)} outliers...")
            hooks = extract_transcripts(outlier_ids)
        else:
            hooks = {}
            print(f"\n  Skipping transcript extraction (title-pattern-only channel)")

        # Save raw data
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
            "hooks": hooks,
        }

        safe_name = name.lower().replace(" ", "_")
        out_file = OUTPUT_DIR / f"{safe_name}.json"
        with open(out_file, "w") as f:
            json.dump(channel_data, f, indent=2)
        print(f"\n  Saved: {out_file}")

        all_channel_data[name] = channel_data

    # Save combined summary
    summary_file = OUTPUT_DIR / "all_channels_summary.json"
    summary = {}
    for name, data in all_channel_data.items():
        summary[name] = {
            "subscriber_count": data["subscriber_count"],
            "format_match": data["format_match"],
            "videos_analyzed": data["videos_analyzed"],
            "median_views": data["median_views"],
            "outlier_count": len(data["outliers"]),
            "outlier_titles": [o["title"] for o in data["outliers"][:10]],
            "hooks_extracted": sum(1 for v in data["hooks"].values() if v),
            "hooks_failed": sum(1 for v in data["hooks"].values() if v is None),
        }

    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(all_channel_data)} channels processed")
    print(f"Summary: {summary_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
