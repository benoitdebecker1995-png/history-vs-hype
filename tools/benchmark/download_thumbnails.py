"""Download thumbnails for all benchmark videos.

Usage:
    python tools/benchmark/download_thumbnails.py

Downloads maxresdefault.jpg (1280x720) for each video, falling back to
hqdefault.jpg (480x360) if maxres isn't available.

Output: tools/benchmark/thumbnails/<channel>/<video_id>.jpg
"""

import json
import glob
import os
import sys
import time
import urllib.request
import urllib.error

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "raw_data")
THUMB_DIR = os.path.join(os.path.dirname(__file__), "thumbnails")

# YouTube thumbnail URL patterns (highest quality first)
THUMB_URLS = [
    "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    "https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
]


def load_all_videos():
    """Load all videos from raw benchmark data."""
    videos = []
    for filepath in sorted(glob.glob(os.path.join(RAW_DATA_DIR, "*.json"))):
        basename = os.path.basename(filepath)
        if "summary" in basename or "hooks" in basename:
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        channel_name = data.get("name", basename.replace(".json", ""))
        for vid in data.get("all_videos", []):
            vid["_channel"] = channel_name
            videos.append(vid)
    return videos


def download_thumbnail(video_id, channel_name):
    """Download thumbnail for a video. Returns (path, quality) or (None, None)."""
    channel_dir = os.path.join(THUMB_DIR, channel_name.replace(" ", "_"))
    os.makedirs(channel_dir, exist_ok=True)

    out_path = os.path.join(channel_dir, f"{video_id}.jpg")
    if os.path.exists(out_path):
        return out_path, "cached"

    for url_template in THUMB_URLS:
        url = url_template.format(video_id=video_id)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read()
            # maxresdefault returns a small placeholder (< 5KB) if not available
            if len(data) < 5000 and "maxresdefault" in url:
                continue
            with open(out_path, "wb") as f:
                f.write(data)
            quality = "maxres" if "maxresdefault" in url else "hq"
            return out_path, quality
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            continue

    return None, None


def main():
    videos = load_all_videos()
    print(f"Loaded {len(videos)} videos from {len(set(v['_channel'] for v in videos))} channels")

    os.makedirs(THUMB_DIR, exist_ok=True)

    success = 0
    cached = 0
    failed = 0
    quality_counts = {"maxres": 0, "hq": 0}

    for i, vid in enumerate(videos, 1):
        video_id = vid["id"]
        channel = vid["_channel"]
        path, quality = download_thumbnail(video_id, channel)

        if quality == "cached":
            cached += 1
            success += 1
        elif path:
            success += 1
            quality_counts[quality] += 1
            # Be polite — small delay between downloads
            if i % 10 == 0:
                time.sleep(0.5)
        else:
            failed += 1
            print(f"  FAILED: {video_id} ({channel}) - {vid.get('title', '?')[:60]}")

        if i % 50 == 0:
            print(f"  Progress: {i}/{len(videos)} ({success} ok, {cached} cached, {failed} failed)")

    print(f"\nDone: {success}/{len(videos)} thumbnails downloaded")
    print(f"  maxres: {quality_counts['maxres']}, hq: {quality_counts['hq']}, cached: {cached}")
    if failed:
        print(f"  Failed: {failed}")


if __name__ == "__main__":
    main()
