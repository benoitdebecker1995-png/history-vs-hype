"""
Phase 66: Extract real first-sentence hooks from outlier videos.
Uses youtube-transcript-api (v1.x+ API with .fetch()).
"""
import json
import re
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

RAW_DIR = Path("tools/benchmark/raw_data")
OUTPUT_FILE = RAW_DIR / "verified_hooks.json"

# All outlier video IDs from the channel extraction
# Kraut outliers
# Fall of Civilizations outliers
# Knowing Better outliers
# Toldinstone outliers
# Plus additional high-view videos from each channel for more hook samples


def load_outliers():
    """Load outlier videos from all channel JSON files."""
    outliers = []
    for f in RAW_DIR.glob("*.json"):
        if f.name == "all_channels_summary.json" or f.name == "verified_hooks.json":
            continue
        with open(f) as fh:
            data = json.load(fh)

        channel = data["name"]
        format_match = data["format_match"]

        # Skip transcript extraction for title-pattern-only channels
        if format_match == "TITLE_PATTERN_ONLY":
            print(f"Skipping {channel} (title-pattern-only)")
            continue

        # Get outliers + next tier (2x+ median) for more hook samples
        median = data["median_views"]
        high_performers = [
            v for v in data["all_videos"]
            if v.get("view_count", 0) >= median * 2
        ]
        high_performers.sort(key=lambda x: x.get("view_count", 0), reverse=True)

        for v in high_performers[:10]:  # Top 10 per channel
            outliers.append({
                "channel": channel,
                "id": v["id"],
                "title": v["title"],
                "view_count": v["view_count"],
                "ratio": round(v["view_count"] / median, 1) if median > 0 else 0,
                "is_3x_outlier": v["view_count"] >= median * 3,
            })

    return outliers


def extract_hook(video_id):
    """Extract the first 2-3 sentences from a video transcript."""
    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id, languages=["en"])
    except Exception as e1:
        # Try without language filter
        try:
            transcript = api.fetch(video_id)
        except Exception as e2:
            return None, str(e2)

    # Collect text from first ~90 seconds (some hooks take longer)
    lines = []
    for entry in transcript:
        if entry.start > 90:
            break
        text = entry.text.strip()
        # Skip music/sound markers
        if text.startswith("[") and text.endswith("]"):
            continue
        if not text:
            continue
        lines.append(text)

    if not lines:
        return None, "No text in first 90 seconds"

    # Join and clean up
    raw_text = " ".join(lines)
    # Clean up common transcript artifacts
    raw_text = re.sub(r'\s+', ' ', raw_text)

    # Extract first 3 sentences
    # Split on sentence boundaries (period, exclamation, question mark followed by space + capital or end)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', raw_text)

    if len(sentences) >= 3:
        hook = " ".join(sentences[:3])
    elif len(sentences) >= 2:
        hook = " ".join(sentences[:2])
    else:
        # Take first 300 chars as fallback
        hook = raw_text[:300]

    return hook.strip(), None


def main():
    outliers = load_outliers()
    print(f"Found {len(outliers)} high-performing videos to extract hooks from\n")

    results = []
    success = 0
    fail = 0

    for v in outliers:
        vid_id = v["id"]
        print(f"  {v['channel']:25s} | {v['title'][:50]:50s} | ", end="", flush=True)

        hook, error = extract_hook(vid_id)

        if hook:
            success += 1
            print(f"OK ({len(hook)} chars)")
            results.append({
                **v,
                "hook": hook,
                "hook_verified": True,
                "error": None,
            })
        else:
            fail += 1
            print(f"FAILED: {error}")
            results.append({
                **v,
                "hook": None,
                "hook_verified": False,
                "error": error,
            })

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Hooks extracted: {success}/{len(outliers)}")
    print(f"Failed: {fail}")
    print(f"Saved: {OUTPUT_FILE}")
    print(f"{'='*60}")

    # Print verified hooks for review
    print(f"\n{'='*60}")
    print("VERIFIED HOOKS (first sentences)")
    print(f"{'='*60}\n")
    for r in results:
        if r["hook"]:
            print(f"[{r['channel']}] {r['title']}")
            print(f"  Views: {r['view_count']:,} ({r['ratio']}x median)")
            print(f"  Hook: \"{r['hook'][:200]}\"")
            print()


if __name__ == "__main__":
    main()
