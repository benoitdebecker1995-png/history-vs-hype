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
        python performance.py --report              # Generate full report
        python performance.py --report --save       # Generate and save report
        python performance.py --by-topic            # Show conversion by topic type
        python performance.py --by-angle            # Show conversion by angle
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
    - performance_report.py (Phase 19-02) for report generation
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

from tools.logging_config import get_logger
from .metrics import get_video_metrics
from .channel_averages import get_recent_video_ids

logger = get_logger(__name__)

# Import database and classifiers with graceful fallback
try:
    from tools.discovery.database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from tools.discovery.classifiers import classify_angles
    CLASSIFIERS_AVAILABLE = True
except ImportError:
    CLASSIFIERS_AVAILABLE = False

# Import report functions with graceful fallback
try:
    from .performance_report import (
        generate_performance_report,
        aggregate_by_topic,
        aggregate_by_angle,
        save_report
    )
    REPORT_AVAILABLE = True
except ImportError:
    REPORT_AVAILABLE = False

# Import pattern extractor with graceful fallback
try:
    from .pattern_extractor import (
        extract_winning_patterns,
        generate_winning_patterns_report,
        calculate_channel_strengths
    )
    PATTERNS_AVAILABLE = True
except ImportError:
    PATTERNS_AVAILABLE = False


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
        'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z',
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
        logger.info("Fetching %d/%d: %s", i + 1, len(video_ids), video_id)

        result = fetch_video_performance(video_id, save_to_db=save_to_db)

        if 'error' in result:
            logger.warning("Error fetching %s: %s", video_id, result['error'])
        else:
            logger.debug("Fetched %s: %.3f%% conversion", video_id, result['conversion_rate'])

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
        logger.warning("Database not available. Run --fetch-all first.")
        return []

    try:
        db = KeywordDB()
        results = db.get_top_converters(limit=limit)
        db.close()
        return results
    except Exception as e:
        logger.error("Error querying top converters: %s", e)
        return []


def print_topic_aggregation() -> None:
    """
    Print performance aggregated by topic type.

    Fetches all videos from database and shows conversion stats per topic.
    """
    if not DATABASE_AVAILABLE:
        logger.warning("Database not available. Run --fetch-all first.")
        return

    if not REPORT_AVAILABLE:
        logger.warning("Report module not available.")
        return

    try:
        db = KeywordDB()
        videos = db.get_all_video_performance(limit=500)
        db.close()
    except Exception as e:
        logger.error("Error fetching data: %s", e)
        return

    if not videos:
        logger.warning("No video performance data found. Run --fetch-all first.")
        return

    stats = aggregate_by_topic(videos, min_count=1)

    if not stats:
        print("No topic data available.")
        return

    # Sort by conversion rate descending
    sorted_stats = sorted(
        stats.items(),
        key=lambda x: x[1]['avg_conversion_rate'],
        reverse=True
    )

    print()
    print(f"{'Topic':<15} {'Videos':>7} {'Avg Conv%':>10} {'Median':>10} {'Total Subs':>10}")
    print("-" * 55)

    for topic, s in sorted_stats:
        print(
            f"{topic:<15} {s['count']:>7} "
            f"{s['avg_conversion_rate']:>9.3f}% "
            f"{s['median_conversion_rate']:>9.3f}% "
            f"{s['total_subscribers_gained']:>10}"
        )

    print("-" * 55)
    print()


def print_angle_aggregation() -> None:
    """
    Print performance aggregated by content angle.

    Fetches all videos from database and shows conversion stats per angle.
    """
    if not DATABASE_AVAILABLE:
        logger.warning("Database not available. Run --fetch-all first.")
        return

    if not REPORT_AVAILABLE:
        logger.warning("Report module not available.")
        return

    try:
        db = KeywordDB()
        videos = db.get_all_video_performance(limit=500)
        db.close()
    except Exception as e:
        logger.error("Error fetching data: %s", e)
        return

    if not videos:
        logger.warning("No video performance data found. Run --fetch-all first.")
        return

    stats = aggregate_by_angle(videos, min_count=1)

    if not stats:
        logger.warning("No angle data available.")
        return

    # Sort by conversion rate descending
    sorted_stats = sorted(
        stats.items(),
        key=lambda x: x[1]['avg_conversion_rate'],
        reverse=True
    )

    print()
    print(f"{'Angle':<15} {'Videos':>7} {'Avg Conv%':>10} {'Median':>10} {'Total Subs':>10}")
    print("-" * 55)

    for angle, s in sorted_stats:
        print(
            f"{angle:<15} {s['count']:>7} "
            f"{s['avg_conversion_rate']:>9.3f}% "
            f"{s['median_conversion_rate']:>9.3f}% "
            f"{s['total_subscribers_gained']:>10}"
        )

    print("-" * 55)
    print()


def print_winning_patterns() -> None:
    """
    Print winning patterns extracted from performance data.

    Shows topic ranking, angle ranking, top converter profile,
    channel strengths, and actionable insights.
    """
    if not PATTERNS_AVAILABLE:
        logger.error("Pattern extractor module not available.")
        return

    logger.info("Extracting winning patterns...")

    profile = extract_winning_patterns()

    if 'error' in profile:
        logger.error("Pattern extraction failed: %s", profile['error'])
        return

    print(f"Videos Analyzed: {profile['videos_analyzed']}")
    print()

    # Topic Ranking
    print("TOPIC RANKING (by conversion rate)")
    print("-" * 55)
    print(f"{'Topic':<15} {'Avg Conv%':>10} {'Videos':>8} {'Total Subs':>12}")
    print("-" * 55)
    for t in profile['topic_ranking']:
        print(
            f"{t['topic']:<15} {t['avg_conversion']:>9.3f}% "
            f"{t['count']:>8} {t['total_subs']:>12}"
        )
    print()

    # Angle Ranking
    print("ANGLE RANKING (by conversion rate)")
    print("-" * 55)
    print(f"{'Angle':<15} {'Avg Conv%':>10} {'Videos':>8} {'Total Subs':>12}")
    print("-" * 55)
    for a in profile['angle_ranking']:
        print(
            f"{a['angle']:<15} {a['avg_conversion']:>9.3f}% "
            f"{a['count']:>8} {a['total_subs']:>12}"
        )
    print()

    # Top Converter Profile
    tp = profile['top_converter_profile']
    print(f"TOP {tp['n']} CONVERTER PROFILE")
    print("-" * 55)
    print(f"Dominant Topic:   {tp['dominant_topic'] or 'N/A'}")
    print(f"Dominant Angles:  {', '.join(tp['dominant_angles']) if tp['dominant_angles'] else 'N/A'}")
    print(f"Avg Duration:     {tp['avg_duration_seconds']:.0f} seconds")
    print(f"Avg Views:        {tp['avg_views']:,.0f}")
    print(f"Likes/View:       {tp['avg_likes_per_view']:.4f}")
    print(f"Comments/View:    {tp['avg_comments_per_view']:.5f}")
    print()

    # Channel Strengths
    cs = profile['channel_strengths']
    print("CHANNEL STRENGTHS")
    print("-" * 55)

    def strength_bar(score: float) -> str:
        """Generate ASCII bar for strength score."""
        filled = int(score / 10)
        empty = 10 - filled
        return '#' * filled + '-' * empty

    print(f"Document-heavy:    [{strength_bar(cs['document_heavy'])}] {cs['document_heavy']:.1f}")
    print(f"Academic:          [{strength_bar(cs['academic'])}] {cs['academic']:.1f}")
    print(f"Legal/Territorial: [{strength_bar(cs['legal_territorial'])}] {cs['legal_territorial']:.1f}")
    print()

    # Insights
    print("INSIGHTS")
    print("-" * 55)
    for insight in profile['insights']:
        print(f"  - {insight}")
    print()


def print_channel_strengths() -> None:
    """
    Print channel strength scores in focused view.

    Shows strength assessment with ASCII bars for quick overview.
    """
    if not PATTERNS_AVAILABLE:
        logger.error("Pattern extractor module not available.")
        return

    if not REPORT_AVAILABLE:
        logger.error("Report module not available.")
        return

    if not DATABASE_AVAILABLE:
        logger.warning("Database not available. Run --fetch-all first.")
        return

    try:
        db = KeywordDB()
        videos = db.get_all_video_performance(limit=500)
        db.close()
    except Exception as e:
        logger.error("Error fetching data: %s", e)
        return

    if not videos:
        logger.warning("No video performance data found. Run --fetch-all first.")
        return

    # Get aggregated stats for strength calculation
    topic_stats = aggregate_by_topic(videos, min_count=1)
    angle_stats = aggregate_by_angle(videos, min_count=1)

    # Calculate strengths
    strengths = calculate_channel_strengths(topic_stats, angle_stats)

    def strength_bar(score: float) -> str:
        """Generate ASCII bar for strength score."""
        filled = int(score / 10)
        empty = 10 - filled
        return '#' * filled + '-' * empty

    print()
    print("CHANNEL STRENGTH ASSESSMENT")
    print("=" * 50)
    print(f"Based on {len(videos)} videos analyzed")
    print()
    print(f"{'Strength':<20} {'Score':>8} {'Bar':<12}")
    print("-" * 50)
    print(f"{'Document-heavy':<20} {strengths['document_heavy']:>7.1f} [{strength_bar(strengths['document_heavy'])}]")
    print(f"{'Academic':<20} {strengths['academic']:>7.1f} [{strength_bar(strengths['academic'])}]")
    print(f"{'Legal/Territorial':<20} {strengths['legal_territorial']:>7.1f} [{strength_bar(strengths['legal_territorial'])}]")
    print("-" * 50)
    print()

    # Interpretation
    best_strength = max(strengths.items(), key=lambda x: x[1])
    strength_names = {
        'document_heavy': 'Document-heavy format',
        'academic': 'Academic fact-checking',
        'legal_territorial': 'Legal/territorial analysis'
    }
    print(f"Primary strength: {strength_names.get(best_strength[0], best_strength[0])}")
    print()


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
Usage: python performance.py [OPTIONS]

Fetch and analyze video performance metrics.

Data Commands:
  VIDEO_ID              Fetch metrics for single video
  --fetch-all [-n N]    Fetch metrics for all/last N videos

Report Commands:
  --report [--save]     Generate performance report
  --top N               Show top N converting videos
  --by-topic            Show conversion aggregated by topic type
  --by-angle            Show conversion aggregated by content angle
  --patterns [--save]   Extract winning patterns from performance data
  --strengths           Show channel strength assessment

Examples:
  python performance.py abc123               Fetch single video
  python performance.py --fetch-all          Fetch all recent videos
  python performance.py --fetch-all -n 20    Fetch last 20 videos
  python performance.py --top 10             Show top 10 converters
  python performance.py --report --save      Generate and save report
  python performance.py --by-topic           Topic analysis
  python performance.py --by-angle           Angle analysis
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
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate full performance report'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save report to file (use with --report)'
    )
    parser.add_argument(
        '--by-topic',
        action='store_true',
        help='Show conversion rates aggregated by topic type'
    )
    parser.add_argument(
        '--by-angle',
        action='store_true',
        help='Show conversion rates aggregated by content angle'
    )
    parser.add_argument(
        '--patterns',
        action='store_true',
        help='Extract and display winning patterns from performance data'
    )
    parser.add_argument(
        '--strengths',
        action='store_true',
        help='Display channel strength scores'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Validate arguments
    has_action = (
        args.video_id or
        args.fetch_all or
        args.top is not None or
        args.report or
        args.by_topic or
        args.by_angle or
        args.patterns or
        args.strengths
    )
    if not has_action:
        parser.print_help()
        sys.exit(1)

    # Handle --patterns flag
    if args.patterns:
        if not PATTERNS_AVAILABLE:
            print("ERROR: Pattern extractor module not available.", file=sys.stderr)
            sys.exit(1)
        print_winning_patterns()
        if args.save:
            result = generate_winning_patterns_report()
            if result.startswith("Error"):
                print(result, file=sys.stderr)
            else:
                print(f"Report saved to: {result}")
        sys.exit(0)

    # Handle --strengths flag
    if args.strengths:
        if not PATTERNS_AVAILABLE:
            print("ERROR: Pattern extractor module not available.", file=sys.stderr)
            sys.exit(1)
        print_channel_strengths()
        sys.exit(0)

    # Handle --report flag
    if args.report:
        if not REPORT_AVAILABLE:
            print("ERROR: Report module not available.", file=sys.stderr)
            sys.exit(1)

        logger.info("Generating performance report...")
        report = generate_performance_report()
        print()
        print(report)

        if args.save:
            result = save_report(report)
            if 'error' in result:
                print(f"ERROR: {result['error']}", file=sys.stderr)
            else:
                print(f"\nReport saved to: {result['saved_to']}")

        sys.exit(0)

    # Handle --by-topic flag
    if args.by_topic:
        logger.info("Generating conversion rates by topic type...")
        print_topic_aggregation()
        sys.exit(0)

    # Handle --by-angle flag
    if args.by_angle:
        logger.info("Generating conversion rates by content angle...")
        print_angle_aggregation()
        sys.exit(0)

    # Handle --top flag
    if args.top is not None:
        logger.info("Fetching top %d videos by conversion rate...", args.top)
        videos = get_top_converters(limit=args.top)
        print_performance_table(videos)
        sys.exit(0)

    # Handle --fetch-all flag
    if args.fetch_all:
        logger.info("Fetching metrics for last %d videos...", args.max_videos)
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
        logger.info("Fetching metrics for video: %s", args.video_id)
        result = fetch_video_performance(
            args.video_id,
            save_to_db=not args.no_save
        )

        if 'error' in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            if 'details' in result:
                print(f"Details: {result['details']}", file=sys.stderr)
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
