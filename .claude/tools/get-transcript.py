#!/usr/bin/env python3
"""
YouTube Transcript Extractor for History vs Hype

Extracts transcripts from YouTube videos for use with /extract-claims workflow.

Usage:
    python get-transcript.py [YouTube URL or Video ID]

Examples:
    python get-transcript.py https://www.youtube.com/watch?v=6aFkoX6g1fE
    python get-transcript.py 6aFkoX6g1fE
    python get-transcript.py "https://youtu.be/6aFkoX6g1fE"

Output:
    Saves transcript to transcripts/[video-title].txt
    Also prints transcript to console for quick copy/paste
"""

import sys
import re
import os
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable
    )
except ImportError:
    print("ERROR: youtube-transcript-api not installed")
    print("Run: pip install youtube-transcript-api")
    sys.exit(1)

# Optional: for getting video title
try:
    import urllib.request
    import json
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats."""

    # Already a video ID (11 characters, alphanumeric with - and _)
    if re.match(r'^[\w-]{11}$', url_or_id):
        return url_or_id

    # Standard watch URL: youtube.com/watch?v=VIDEO_ID
    match = re.search(r'[?&]v=([\w-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Short URL: youtu.be/VIDEO_ID
    match = re.search(r'youtu\.be/([\w-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Embed URL: youtube.com/embed/VIDEO_ID
    match = re.search(r'embed/([\w-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Shorts URL: youtube.com/shorts/VIDEO_ID
    match = re.search(r'shorts/([\w-]{11})', url_or_id)
    if match:
        return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_video_title(video_id: str) -> str:
    """Attempt to get video title using oembed API (no API key needed)."""
    if not HAS_URLLIB:
        return video_id

    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('title', video_id)
    except Exception:
        return video_id


def sanitize_filename(title: str) -> str:
    """Convert title to safe filename."""
    # Remove or replace unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = re.sub(r'\s+', '-', safe)
    safe = safe.strip('-')
    # Limit length
    if len(safe) > 80:
        safe = safe[:80].rsplit('-', 1)[0]
    return safe.lower()


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_transcript(video_id: str, include_timestamps: bool = True) -> tuple[list, str, str]:
    """
    Fetch transcript from YouTube.

    Returns:
        tuple: (raw transcript list, formatted text, source type)
    """
    source = "auto-generated"
    api = YouTubeTranscriptApi()

    # New API (v1.0+): use fetch() directly
    # It automatically finds the best available transcript
    try:
        raw_transcript = api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
    except NoTranscriptFound:
        # Try without language filter
        try:
            raw_transcript = api.fetch(video_id)
            source = "auto (any language)"
        except Exception as e:
            raise NoTranscriptFound(video_id, ['en'], None)

    # Format output
    lines = []
    for entry in raw_transcript:
        text = entry.text.replace('\n', ' ') if hasattr(entry, 'text') else entry.get('text', '').replace('\n', ' ')
        start = entry.start if hasattr(entry, 'start') else entry.get('start', 0)
        if include_timestamps:
            timestamp = format_timestamp(start)
            lines.append(f"[{timestamp}] {text}")
        else:
            lines.append(text)

    formatted = '\n'.join(lines)

    # Convert to list of dicts for compatibility
    if raw_transcript and hasattr(raw_transcript[0], 'text'):
        raw_transcript = [{'text': e.text, 'start': e.start, 'duration': e.duration} for e in raw_transcript]

    return raw_transcript, formatted, source


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python get-transcript.py [YouTube URL or Video ID]")
        print("\nExamples:")
        print("  python get-transcript.py https://www.youtube.com/watch?v=6aFkoX6g1fE")
        print("  python get-transcript.py 6aFkoX6g1fE")
        print("\nOptions:")
        print("  --no-timestamps    Exclude timestamps from output")
        print("  --no-save          Print only, don't save to file")
        sys.exit(1)

    url_or_id = sys.argv[1]
    include_timestamps = '--no-timestamps' not in sys.argv
    save_file = '--no-save' not in sys.argv

    # Extract video ID
    try:
        video_id = extract_video_id(url_or_id)
        print(f"Video ID: {video_id}")
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Get video title
    print("Fetching video info...")
    title = get_video_title(video_id)
    print(f"Title: {title}")

    # Get transcript
    print("Fetching transcript...")
    try:
        raw, formatted, source = get_transcript(video_id, include_timestamps)
        print(f"Source: {source} ({len(raw)} segments)")
    except TranscriptsDisabled:
        print("ERROR: Transcripts are disabled for this video")
        sys.exit(1)
    except NoTranscriptFound:
        print("ERROR: No English transcript found for this video")
        sys.exit(1)
    except VideoUnavailable:
        print("ERROR: Video is unavailable (private, deleted, or region-locked)")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Save to file
    if save_file:
        script_dir = Path(__file__).parent
        transcripts_dir = script_dir / "transcripts"
        transcripts_dir.mkdir(exist_ok=True)

        filename = sanitize_filename(title) + ".txt"
        filepath = transcripts_dir / filename

        # Add header with metadata
        header = f"""# {title}
# Video ID: {video_id}
# URL: https://www.youtube.com/watch?v={video_id}
# Transcript source: {source}
# Segments: {len(raw)}
#
# Use with: /extract-claims
# ---

"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + formatted)

        print(f"\nSaved to: {filepath}")

    # Print transcript
    print("\n" + "="*60)
    print("TRANSCRIPT")
    print("="*60 + "\n")
    print(formatted)
    print("\n" + "="*60)

    # Summary
    word_count = sum(len(entry['text'].split()) for entry in raw)
    duration = raw[-1]['start'] + raw[-1].get('duration', 0) if raw else 0

    print(f"\nSummary:")
    print(f"  Words: ~{word_count:,}")
    print(f"  Duration: {format_timestamp(duration)}")
    print(f"  Segments: {len(raw)}")

    if save_file:
        print(f"\nNext step: Run /extract-claims and reference {filepath.name}")


if __name__ == "__main__":
    main()
