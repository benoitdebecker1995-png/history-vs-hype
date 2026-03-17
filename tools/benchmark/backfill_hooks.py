"""
Phase 66: Backfill missing hooks from rate-limited transcript requests.
Run this when YouTube rate limit clears (typically 1-4 hours after initial extraction).

Usage: python tools/benchmark/backfill_hooks.py
Then:  python tools/benchmark/build_deliverables.py  (to rebuild all deliverables)
"""
import json
import re
import time
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

HOOKS_FILE = Path("tools/benchmark/raw_data/verified_hooks.json")


def extract_hook(api, video_id):
    """Extract first 2-3 sentences from transcript."""
    # Try en-GB first (Fall of Civilizations uses this), then en
    for langs in [["en-GB"], ["en"], ["en-GB", "en"]]:
        try:
            transcript = api.fetch(video_id, languages=langs)
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

            if not lines:
                continue

            raw_text = " ".join(lines)
            raw_text = re.sub(r'\s+', ' ', raw_text)

            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', raw_text)
            if len(sentences) >= 3:
                hook = " ".join(sentences[:3])
            elif len(sentences) >= 2:
                hook = " ".join(sentences[:2])
            else:
                hook = raw_text[:300]

            return hook.strip(), None

        except Exception as e:
            if "429" in str(e) or "blocking" in str(e).lower():
                return None, "RATE_LIMITED"
            continue

    return None, "NO_TRANSCRIPT"


def main():
    with open(HOOKS_FILE, encoding="utf-8") as f:
        hooks = json.load(f)

    # Find missing hooks
    missing = [h for h in hooks if not h.get("hook_verified") or h.get("hook") is None]
    if not missing:
        print("All hooks already extracted! Nothing to backfill.")
        return

    print(f"Found {len(missing)} missing hooks to backfill:\n")
    for h in missing:
        print(f"  {h['channel']:25s} | {h['title'][:50]}")
    print()

    api = YouTubeTranscriptApi()
    filled = 0
    still_missing = 0

    for h in missing:
        vid_id = h["id"]
        print(f"  Trying {h['channel']} - {h['title'][:40]}... ", end="", flush=True)

        hook, error = extract_hook(api, vid_id)

        if error == "RATE_LIMITED":
            print("RATE LIMITED - stopping (try again later)")
            still_missing += len(missing) - filled
            break

        if hook:
            h["hook"] = hook
            h["hook_verified"] = True
            h["error"] = None
            filled += 1
            print(f"OK ({len(hook)} chars)")
        else:
            still_missing += 1
            print(f"FAILED: {error}")

        time.sleep(2)  # Be gentle

    # Save updated hooks
    with open(HOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(hooks, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Backfilled: {filled}")
    print(f"Still missing: {still_missing}")
    print(f"Updated: {HOOKS_FILE}")

    if filled > 0:
        print(f"\nNow run: python tools/benchmark/build_deliverables.py")
        print("to rebuild all deliverables with the new hooks.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
