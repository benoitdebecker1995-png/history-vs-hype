#!/usr/bin/env python3
"""
Variant Management CLI - Phase 29 Thumbnail & Title Tracking

Provides commands for registering thumbnail/title variants and recording CTR snapshots.

Usage:
    python variants.py register-thumb VIDEO_ID VARIANT_LETTER FILE_PATH --tags "map,face"
    python variants.py register-title VIDEO_ID VARIANT_LETTER TITLE_TEXT --tags "mechanism,paradox"
    python variants.py record-ctr VIDEO_ID CTR IMPRESSIONS VIEWS [--thumbnail-id N] [--title-id N] [--date YYYY-MM-DD] [--late]
    python variants.py list VIDEO_ID
    python variants.py snapshots VIDEO_ID

Python:
    from variants import register_thumbnail, register_title, record_ctr_snapshot
    result = register_thumbnail('VIDEO_ID', 'A', '/path/to/thumb.jpg', ['map', 'text'])

Output:
    Human-readable formatted tables showing registered variants and CTR snapshots.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

from tools.discovery.database import KeywordDB

# Try to import imagehash for perceptual hash generation
try:
    import imagehash
    from PIL import Image
    IMAGEHASH_AVAILABLE = True
except ImportError:
    IMAGEHASH_AVAILABLE = False


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def generate_thumbnail_hash(file_path: str) -> Optional[str]:
    """
    Generate perceptual hash for thumbnail image.

    Args:
        file_path: Path to image file

    Returns:
        Hex string of perceptual hash, or None if unavailable/error
    """
    if not IMAGEHASH_AVAILABLE:
        print("Warning: imagehash not installed, skipping hash generation")
        print("Install with: pip install imagehash pillow")
        return None

    path = Path(file_path)
    if not path.exists():
        print(f"Warning: File not found: {file_path}")
        return None

    try:
        with Image.open(path) as img:
            hash_value = imagehash.phash(img)
            return str(hash_value)
    except Exception as e:
        print(f"Warning: Could not generate hash: {e}")
        return None


def validate_video_id(video_id: str) -> str:
    """
    Validate and return YouTube video ID.

    Args:
        video_id: Video ID to validate

    Returns:
        Validated video ID

    Raises:
        ValueError: If video ID is invalid
    """
    video_id = video_id.strip()
    if not re.match(r'^[\w-]{11}$', video_id):
        raise ValueError(f"Invalid video ID: {video_id} (must be 11 characters)")
    return video_id


def validate_tags(tags_str: str) -> List[str]:
    """
    Parse and validate tag string.

    Args:
        tags_str: Comma-separated tag string

    Returns:
        List of tag strings
    """
    tags = [tag.strip() for tag in tags_str.split(',')]
    return [tag for tag in tags if tag]  # Filter empty strings


# =========================================================================
# COMMAND FUNCTIONS
# =========================================================================

def cmd_register_thumb(args):
    """Register a thumbnail variant."""
    try:
        video_id = validate_video_id(args.video_id)
        variant_letter = args.variant_letter.upper().strip()

        if len(variant_letter) != 1 or variant_letter < 'A' or variant_letter > 'Z':
            print(f"Error: variant_letter must be a single uppercase letter (A-Z), got: {variant_letter}")
            sys.exit(1)

        file_path = args.file_path
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        visual_patterns = validate_tags(args.tags)
        if not visual_patterns:
            print("Error: --tags required (e.g., 'map,face,text')")
            sys.exit(1)

        # Generate perceptual hash
        perceptual_hash = generate_thumbnail_hash(file_path)

        # Register in database
        db = KeywordDB()
        result = db.add_thumbnail_variant(
            video_id, variant_letter, file_path, visual_patterns, perceptual_hash
        )
        db.close()

        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(f"Registered thumbnail variant {variant_letter} for {video_id}")
        print(f"  File: {file_path}")
        print(f"  Tags: {', '.join(visual_patterns)}")
        if perceptual_hash:
            print(f"  Hash: {perceptual_hash[:16]}...")
        else:
            print(f"  Hash: (not generated)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_register_title(args):
    """Register a title variant."""
    try:
        video_id = validate_video_id(args.video_id)
        variant_letter = args.variant_letter.upper().strip()

        if len(variant_letter) != 1 or variant_letter < 'A' or variant_letter > 'Z':
            print(f"Error: variant_letter must be a single uppercase letter (A-Z), got: {variant_letter}")
            sys.exit(1)

        title_text = args.title_text
        formula_tags = validate_tags(args.tags)
        if not formula_tags:
            print("Error: --tags required (e.g., 'mechanism,paradox')")
            sys.exit(1)

        # Register in database
        db = KeywordDB()
        result = db.add_title_variant(video_id, variant_letter, title_text, formula_tags)
        db.close()

        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(f"Registered title variant {variant_letter}: '{title_text}'")
        print(f"  Length: {len(title_text)} chars")
        print(f"  Tags: {', '.join(formula_tags)}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_record_ctr(args):
    """Record a CTR snapshot."""
    try:
        video_id = validate_video_id(args.video_id)
        ctr_percent = float(args.ctr)
        impression_count = int(args.impressions)
        view_count = int(args.views)

        # Optional parameters
        thumbnail_id = args.thumbnail_id
        title_id = args.title_id
        snapshot_date = args.date
        is_late_entry = args.late

        # Register in database
        db = KeywordDB()
        result = db.add_ctr_snapshot(
            video_id, ctr_percent, impression_count, view_count,
            thumbnail_id, title_id, snapshot_date, is_late_entry
        )
        db.close()

        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(f"Recorded CTR snapshot: {ctr_percent}% ({impression_count} impressions, {view_count} views)")
        if snapshot_date:
            print(f"  Date: {snapshot_date}")
        if thumbnail_id:
            print(f"  Active thumbnail: variant ID {thumbnail_id}")
        if title_id:
            print(f"  Active title: variant ID {title_id}")
        if is_late_entry:
            print(f"  Marked as late entry")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_list_variants(args):
    """List all variants for a video."""
    try:
        video_id = validate_video_id(args.video_id)

        db = KeywordDB()
        thumbs = db.get_thumbnail_variants(video_id)
        titles = db.get_title_variants(video_id)
        snapshots = db.get_ctr_snapshots(video_id)
        db.close()

        if not thumbs and not titles and not snapshots:
            print(f"No variants registered for {video_id}")
            return

        print(f"\nVariants for video: {video_id}")
        print("=" * 80)

        # Thumbnails
        if thumbs:
            print("\nTHUMBNAILS:")
            print("-" * 80)
            for thumb in thumbs:
                print(f"  [{thumb['variant_letter']}] {thumb['file_path']}")
                print(f"      Tags: {', '.join(thumb['visual_pattern_tags'])}")
                if thumb.get('perceptual_hash'):
                    print(f"      Hash: {thumb['perceptual_hash'][:8]}...")
                print()

        # Titles
        if titles:
            print("\nTITLES:")
            print("-" * 80)
            for title in titles:
                title_text = title['title_text']
                if len(title_text) > 50:
                    title_text = title_text[:47] + "..."
                print(f"  [{title['variant_letter']}] {title_text}")
                print(f"      Length: {title['character_count']} chars")
                print(f"      Tags: {', '.join(title['formula_tags'])}")
                print()

        # CTR Snapshots
        if snapshots:
            print("\nCTR SNAPSHOTS:")
            print("-" * 80)
            for snap in snapshots:
                print(f"  {snap['snapshot_date']}: {snap['ctr_percent']}% CTR")
                print(f"      {snap['impression_count']} impressions, {snap['view_count']} views")
                if snap.get('active_thumbnail_id'):
                    print(f"      Active thumbnail: variant ID {snap['active_thumbnail_id']}")
                if snap.get('active_title_id'):
                    print(f"      Active title: variant ID {snap['active_title_id']}")
                print()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_show_snapshots(args):
    """Show detailed CTR snapshot history for a video."""
    try:
        video_id = validate_video_id(args.video_id)

        db = KeywordDB()
        snapshots = db.get_ctr_snapshots(video_id)
        db.close()

        if not snapshots:
            print(f"No CTR snapshots for {video_id}")
            return

        print(f"\nCTR Snapshot History: {video_id}")
        print("=" * 80)
        print(f"{'Date':<12} {'CTR %':<8} {'Impressions':<12} {'Views':<8} {'Thumb ID':<9} {'Title ID'}")
        print("-" * 80)

        for snap in snapshots:
            thumb_id = snap.get('active_thumbnail_id') or '-'
            title_id = snap.get('active_title_id') or '-'
            print(f"{snap['snapshot_date']:<12} {snap['ctr_percent']:<8.2f} "
                  f"{snap['impression_count']:<12} {snap['view_count']:<8} "
                  f"{str(thumb_id):<9} {title_id}")

        # Show trend if multiple snapshots
        if len(snapshots) > 1:
            earliest = snapshots[0]
            latest = snapshots[-1]
            delta = latest['ctr_percent'] - earliest['ctr_percent']
            direction = "UP" if delta > 0 else "DOWN" if delta < 0 else "FLAT"

            print()
            print(f"Trend: {earliest['snapshot_date']} to {latest['snapshot_date']}")
            print(f"  CTR change: {earliest['ctr_percent']:.2f}% -> {latest['ctr_percent']:.2f}% "
                  f"({delta:+.2f}% {direction})")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# =========================================================================
# CLI ENTRY POINT
# =========================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Variant Management CLI - Track thumbnails, titles, and CTR performance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register thumbnail variant
  python variants.py register-thumb dQw4w9WgXcQ A thumbnail-a.jpg --tags "map,face,text"

  # Register title variant
  python variants.py register-title dQw4w9WgXcQ A "How Colonial Borders Still Kill Today" --tags "mechanism,document"

  # Record CTR snapshot
  python variants.py record-ctr dQw4w9WgXcQ 4.5 1200 54 --thumbnail-id 1 --title-id 1

  # List all variants
  python variants.py list dQw4w9WgXcQ

  # Show CTR history
  python variants.py snapshots dQw4w9WgXcQ

Suggested thumbnail tags: map, face, text, document, evidence, split
Suggested title tags: mechanism, document, paradox, question, comparison
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # register-thumb
    thumb_parser = subparsers.add_parser('register-thumb', help='Register a thumbnail variant')
    thumb_parser.add_argument('video_id', help='YouTube video ID')
    thumb_parser.add_argument('variant_letter', help='Variant letter (A-Z)')
    thumb_parser.add_argument('file_path', help='Path to thumbnail file')
    thumb_parser.add_argument('--tags', required=True, help='Comma-separated visual pattern tags')

    # register-title
    title_parser = subparsers.add_parser('register-title', help='Register a title variant')
    title_parser.add_argument('video_id', help='YouTube video ID')
    title_parser.add_argument('variant_letter', help='Variant letter (A-Z)')
    title_parser.add_argument('title_text', help='Title text')
    title_parser.add_argument('--tags', required=True, help='Comma-separated formula tags')

    # record-ctr
    ctr_parser = subparsers.add_parser('record-ctr', help='Record a CTR snapshot')
    ctr_parser.add_argument('video_id', help='YouTube video ID')
    ctr_parser.add_argument('ctr', type=float, help='CTR percentage (0-100)')
    ctr_parser.add_argument('impressions', type=int, help='Impression count')
    ctr_parser.add_argument('views', type=int, help='View count')
    ctr_parser.add_argument('--thumbnail-id', type=int, help='Active thumbnail variant ID')
    ctr_parser.add_argument('--title-id', type=int, help='Active title variant ID')
    ctr_parser.add_argument('--date', help='Snapshot date (YYYY-MM-DD)')
    ctr_parser.add_argument('--late', action='store_true', help='Mark as late entry')

    # list
    list_parser = subparsers.add_parser('list', help='List all variants for a video')
    list_parser.add_argument('video_id', help='YouTube video ID')

    # snapshots
    snap_parser = subparsers.add_parser('snapshots', help='Show CTR snapshot history')
    snap_parser.add_argument('video_id', help='YouTube video ID')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Route to command handlers
    if args.command == 'register-thumb':
        cmd_register_thumb(args)
    elif args.command == 'register-title':
        cmd_register_title(args)
    elif args.command == 'record-ctr':
        cmd_record_ctr(args)
    elif args.command == 'list':
        cmd_list_variants(args)
    elif args.command == 'snapshots':
        cmd_show_snapshots(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
