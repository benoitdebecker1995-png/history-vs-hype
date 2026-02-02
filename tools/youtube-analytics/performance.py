"""
YouTube Video Performance Fetcher

Fetches performance metrics for video catalog and calculates subscriber conversion rates.
Stores data to keywords.db via Phase 19 video_performance table.

Usage:
    CLI:
        python performance.py VIDEO_ID              # Fetch single video
        python performance.py --fetch-all           # Fetch all recent videos
        python performance.py --fetch-all -n 20    # Fetch last 20 videos
        python performance.py --top 10              # Show top 10 converters
        python performance.py --help                # Show usage

    Python:
        from performance import fetch_video_performance, fetch_catalog_metrics
        from performance import calculate_conversion_rate, classify_topic_type

        # Fetch single video
        result = fetch_video_performance('VIDEO_ID')
        print(f"Conversion rate: {result['conversion_rate']:.3f}%")

        # Fetch all recent videos
        results = fetch_catalog_metrics(max_videos=30)
        for r in results:
            print(f"{r['title']}: {r['conversion_rate']:.3f}% conversion")

Dependencies:
    - metrics.py (Phase 8) for YouTube Analytics API
    - channel_averages.py (Phase 8) for get_recent_video_ids
    - database.py (Phase 15+) for KeywordDB storage
    - classifiers.py (Phase 16) for angle classification
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# Add discovery to path for database and classifiers
sys.path.insert(0, str(Path(__file__).parent.parent / 'discovery'))

from metrics import get_video_metrics
from channel_averages import get_recent_video_ids

# Import database and classifiers with graceful fallback
try:
    from database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from classifiers import classify_angles
    CLASSIFIERS_AVAILABLE = True
except ImportError:
    CLASSIFIERS_AVAILABLE = False


# Topic classification vocabulary (from patterns.py TAG_VOCABULARY)
# Used to classify own videos by primary topic type
TAG_VOCABULARY = {
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'occupation', 'icj', 'sovereignty', 'bir tawil', 'chagos', 'essequibo'],
    'ideological': ['myth', 'debunk', 'fact-check', 'propaganda', 'narrative', 'lie', 'dark ages', 'flat earth'],
    'colonial': ['colonial', 'empire', 'independence', 'decolonization', 'imperial', 'somaliland', 'haiti'],
    'politician': ['vance', 'netanyahu', 'trump', 'fuentes', 'reagan', 'politician'],
    'archaeological': ['dna', 'excavation', 'artifact', 'manuscript', 'archaeology'],
    'medieval': ['medieval', 'dark ages', 'crusade', 'viking', 'middle ages'],
    'legal': ['treaty', 'court', 'icj', 'ruling', 'law', 'sovereignty', 'referendum'],
}


def calculate_conversion_rate(views: int, subscribers_gained: int) -> float:
    """
    Calculate subscriber conversion rate as percentage.

    Formula: (subscribers_gained / views) * 100

    Args:
        views: Total video views
        subscribers_gained: Subscribers gained from this video

    Returns:
        Conversion rate as percentage (e.g., 0.167 for 0.167%)
        Returns 0.0 if views is 0

    Example:
        >>> calculate_conversion_rate(15000, 25)
        0.16666666666666666
    """
    if views <= 0:
        return 0.0
    return (subscribers_gained / views) * 100


def classify_topic_type(title: str) -> str:
    """
    Classify video into primary topic type based on title keywords.

    Uses TAG_VOCABULARY to match keywords in title.
    Returns first matching topic type or 'general' if no match.

    Args:
        title: Video title

    Returns:
        Topic type string: 'territorial', 'ideological', 'colonial',
        'politician', 'archaeological', 'medieval', 'legal', or 'general'

    Example:
        >>> classify_topic_type('Why This Border Dispute Still Matters')
        'territorial'
        >>> classify_topic_type('The Dark Ages Myth')
        'ideological'
    """
    if not title:
        return 'general'

    title_lower = title.lower()

    for topic, keywords in TAG_VOCABULARY.items():
        if any(kw in title_lower for kw in keywords):
            return topic

    return 'general'


def classify_own_video(title: str) -> Dict[str, Any]:
    """
    Classify own video by topic type and angles.

    Combines topic classification with angle classification from Phase 16.

    Args:
        title: Video title

    Returns:
        {
            'topic_type': str,
            'angles': List[str]
        }

    Example:
        >>> classify_own_video('The Treaty That Split Somaliland')
        {'topic_type': 'colonial', 'angles': ['legal', 'historical']}
    """
    topic_type = classify_topic_type(title)

    # Use Phase 16 classifier if available
    if CLASSIFIERS_AVAILABLE:
        angles = classify_angles(title)
    else:
        # Fallback: derive angles from topic type
        angle_mapping = {
            'territorial': ['geographic'],
            'ideological': ['historical'],
            'colonial': ['historical'],
            'politician': ['political'],
            'archaeological': ['historical'],
            'medieval': ['historical'],
            'legal': ['legal'],
            'general': ['general'],
        }
        angles = angle_mapping.get(topic_type, ['general'])

    return {
        'topic_type': topic_type,
        'angles': angles
    }


def fetch_video_performance(video_id: str, save_to_db: bool = True) -> Dict[str, Any]:
    """
    Fetch performance metrics for a single video.

    Retrieves metrics from YouTube Analytics API, calculates conversion rate,
    classifies by topic/angle, and optionally stores to database.

    Args:
        video_id: YouTube video ID
        save_to_db: Whether to save to database (default True)

    Returns:
        Performance dict on success:
            {
                'video_id': str,
                'title': str,
                'views': int,
                'subscribers_gained': int,
                'subscribers_lost': int,
                'conversion_rate': float,
                'watch_time_minutes': float,
                'avg_view_duration_seconds': int,
                'likes': int,
                'comments': int,
                'shares': int,
                'topic_type': str,
                'angles': List[str],
                'fetched_at': str,
                'saved_to_db': bool
            }

        Error dict on failure:
            {'error': msg, 'video_id': str}

    Example:
        result = fetch_video_performance('abc123')
        if 'error' not in result:
            print(f"Conversion: {result['conversion_rate']:.3f}%")
    """
    # Fetch metrics from YouTube Analytics API
    metrics = get_video_metrics(video_id)

    if 'error' in metrics:
        return metrics

    # Extract relevant fields
    views = metrics.get('views', 0)
    subs_gained = metrics.get('subscribers_gained', 0)
    subs_lost = metrics.get('subscribers_lost', 0)
    title = metrics.get('title', '')

    # Calculate conversion rate
    conversion_rate = calculate_conversion_rate(views, subs_gained)

    # Classify video
    classification = classify_own_video(title)

    # Build result
    result = {
        'video_id': video_id,
        'title': title,
        'views': views,
        'subscribers_gained': subs_gained,
        'subscribers_lost': subs_lost,
        'conversion_rate': conversion_rate,
        'watch_time_minutes': metrics.get('watch_time_minutes', 0),
        'avg_view_duration_seconds': metrics.get('avg_view_duration_seconds', 0),
        'likes': metrics.get('likes', 0),
        'comments': metrics.get('comments', 0),
        'shares': metrics.get('shares', 0),
        'topic_type': classification['topic_type'],
        'angles': classification['angles'],
        'fetched_at': datetime.utcnow().isoformat() + 'Z',
        'saved_to_db': False
    }

    # Save to database if requested and available
    if save_to_db and DATABASE_AVAILABLE:
        try:
            db = KeywordDB()
            db_result = db.add_video_performance(
                video_id=video_id,
                title=title,
                views=views,
                subscribers_gained=subs_gained,
                subscribers_lost=subs_lost,
                conversion_rate=conversion_rate,
                watch_time_minutes=metrics.get('watch_time_minutes'),
                avg_view_duration_seconds=metrics.get('avg_view_duration_seconds'),
                likes=metrics.get('likes'),
                comments=metrics.get('comments'),
                shares=metrics.get('shares'),
                topic_type=classification['topic_type'],
                angles=classification['angles']
            )
            db.close()

            if 'error' not in db_result:
                result['saved_to_db'] = True
        except Exception as e:
            result['db_error'] = str(e)

    return result


def fetch_catalog_metrics(max_videos: int = 50, save_to_db: bool = True) -> List[Dict[str, Any]]:
    """
    Fetch performance metrics for recent video catalog.

    Retrieves video IDs from channel, fetches metrics for each,
    and stores to database.

    Args:
        max_videos: Maximum number of videos to fetch (default 50)
        save_to_db: Whether to save to database (default True)

    Returns:
        List of performance dicts (same format as fetch_video_performance)
        Videos with errors will have 'error' key

    Example:
        results = fetch_catalog_metrics(max_videos=20)
        success = [r for r in results if 'error' not in r]
        print(f"Fetched {len(success)} of {len(results)} videos")
    """
    # Get recent video IDs
    video_ids = get_recent_video_ids(max_videos)

    if isinstance(video_ids, dict) and 'error' in video_ids:
        return [video_ids]

    if not video_ids:
        return [{'error': 'No videos found in channel'}]

    results = []

    for i, video_id in enumerate(video_ids):
        print(f"Fetching {i+1}/{len(video_ids)}: {video_id}...", end=' ', flush=True)

        result = fetch_video_performance(video_id, save_to_db=save_to_db)

        if 'error' in result:
            print(f"ERROR: {result['error']}")
        else:
            print(f"OK ({result['conversion_rate']:.3f}% conversion)")

        results.append(result)

    return results


def get_top_converters(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get videos with highest conversion rates from database.

    Args:
        limit: Number of top videos to return

    Returns:
        List of video performance dicts sorted by conversion_rate DESC
        Empty list if database unavailable or no data
    """
    if not DATABASE_AVAILABLE:
        print("Database not available. Run --fetch-all first.")
        return []

    try:
        db = KeywordDB()
        results = db.get_top_converters(limit=limit)
        db.close()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []


def print_performance_table(videos: List[Dict[str, Any]]) -> None:
    """
    Print performance data as formatted table.

    Args:
        videos: List of performance dicts
    """
    if not videos:
        print("No videos to display.")
        return

    # Filter out error entries
    valid_videos = [v for v in videos if 'error' not in v]

    if not valid_videos:
        print("No valid video data to display.")
        return

    # Print header
    print()
    print(f"{'Title':<40} {'Views':>10} {'Subs':>6} {'Conv%':>7} {'Topic':<12}")
    print("-" * 80)

    for v in valid_videos:
        title = (v.get('title') or 'Unknown')[:38]
        views = v.get('views', 0)
        subs = v.get('subscribers_gained', 0)
        conv = v.get('conversion_rate', 0)
        topic = v.get('topic_type', 'general')[:10]

        print(f"{title:<40} {views:>10,} {subs:>6} {conv:>6.3f}% {topic:<12}")

    print("-" * 80)

    # Summary
    total_views = sum(v.get('views', 0) for v in valid_videos)
    total_subs = sum(v.get('subscribers_gained', 0) for v in valid_videos)
    avg_conv = calculate_conversion_rate(total_views, total_subs) if total_views > 0 else 0

    print(f"{'TOTAL':<40} {total_views:>10,} {total_subs:>6} {avg_conv:>6.3f}%")
    print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch video performance metrics and calculate conversion rates.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python performance.py abc123               Fetch single video
  python performance.py --fetch-all          Fetch all recent videos
  python performance.py --fetch-all -n 20    Fetch last 20 videos
  python performance.py --top 10             Show top 10 converters
  python performance.py --no-save abc123     Fetch without saving to DB

Data is stored in tools/discovery/keywords.db (video_performance table).
        '''
    )

    parser.add_argument(
        'video_id',
        nargs='?',
        help='YouTube video ID to fetch'
    )
    parser.add_argument(
        '--fetch-all',
        action='store_true',
        help='Fetch metrics for all recent videos'
    )
    parser.add_argument(
        '-n', '--max-videos',
        type=int,
        default=50,
        help='Maximum videos to fetch with --fetch-all (default: 50)'
    )
    parser.add_argument(
        '--top',
        type=int,
        metavar='N',
        help='Show top N videos by conversion rate from database'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save results to database'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.video_id and not args.fetch_all and args.top is None:
        parser.print_help()
        sys.exit(1)

    # Handle --top flag
    if args.top is not None:
        print(f"Top {args.top} videos by conversion rate:")
        videos = get_top_converters(limit=args.top)
        print_performance_table(videos)
        sys.exit(0)

    # Handle --fetch-all flag
    if args.fetch_all:
        print(f"Fetching metrics for last {args.max_videos} videos...")
        print()
        results = fetch_catalog_metrics(
            max_videos=args.max_videos,
            save_to_db=not args.no_save
        )
        print_performance_table(results)

        # Show summary
        success = [r for r in results if 'error' not in r]
        saved = [r for r in success if r.get('saved_to_db')]
        print(f"Fetched: {len(success)}/{len(results)} videos")
        print(f"Saved to DB: {len(saved)}")
        sys.exit(0)

    # Handle single video ID
    if args.video_id:
        print(f"Fetching metrics for video: {args.video_id}")
        print()
        result = fetch_video_performance(
            args.video_id,
            save_to_db=not args.no_save
        )

        if 'error' in result:
            print(f"Error: {result['error']}")
            if 'details' in result:
                print(f"Details: {result['details']}")
            sys.exit(1)

        # Print detailed result
        print(f"Title: {result['title']}")
        print(f"Views: {result['views']:,}")
        print(f"Subscribers gained: {result['subscribers_gained']}")
        print(f"Subscribers lost: {result['subscribers_lost']}")
        print(f"Conversion rate: {result['conversion_rate']:.3f}%")
        print(f"Watch time: {result['watch_time_minutes']:,.0f} minutes")
        print(f"Avg view duration: {result['avg_view_duration_seconds']} seconds")
        print(f"Likes: {result['likes']}")
        print(f"Comments: {result['comments']}")
        print(f"Shares: {result['shares']}")
        print(f"Topic type: {result['topic_type']}")
        print(f"Angles: {', '.join(result['angles'])}")
        print(f"Saved to DB: {result['saved_to_db']}")
        sys.exit(0)
