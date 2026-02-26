#!/usr/bin/env python3
"""
CTR Analysis Engine - Phase 30 Benchmark Analysis

Provides verdict calculation for A/B variant testing and channel-specific CTR benchmarks.

Usage:
    python benchmarks.py verdict VIDEO_ID [--type thumbnail|title]
    python benchmarks.py benchmarks

Python:
    from benchmarks import calculate_verdict, compare_variants_for_video, get_benchmarks_report
    verdict = calculate_verdict(variant_data, category_avg=3.5)

Output:
    Verdict with status (winner_found, no_clear_winner, insufficient_data, etc.),
    confidence level, and recommendation.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import statistics

from tools.discovery.database import KeywordDB


# =========================================================================
# CONSTANTS - Threshold Configuration
# =========================================================================

# Impression tiers for confidence levels
IMPRESSIONS_LOW = 200      # Minimum for any verdict
IMPRESSIONS_MEDIUM = 500   # Medium confidence
IMPRESSIONS_HIGH = 1000    # High confidence

# CTR difference thresholds (percentage points)
CTR_DELTA_TIE = 0.5        # Below this = no clear winner
CTR_DELTA_EDGE = 1.5       # 0.5-1.5 = edge/marginal
CTR_DELTA_CLEAR = 3.0      # Above this = clear winner

# Freshness warning threshold
FRESHNESS_DAYS = 60

# Minimum videos for reliable category benchmark
MIN_CATEGORY_VIDEOS = 2


# =========================================================================
# CORE VERDICT FUNCTION (Pure, no DB dependency)
# =========================================================================

def calculate_verdict(
    variant_data: List[Dict[str, Any]],
    category_avg: Optional[float] = None
) -> Dict[str, Any]:
    """
    Calculate verdict for variant comparison.

    Pure function - no database dependency. Uses heuristic thresholds
    appropriate for small channels.

    Args:
        variant_data: List of dicts with keys:
            - variant_letter: str (A, B, C...)
            - avg_ctr: float (percentage)
            - total_impressions: int
            - snapshot_count: int
        category_avg: Optional category CTR average for single-variant comparison

    Returns:
        Dict with keys:
            - status: 'no_data' | 'insufficient_data' | 'single_variant' |
                     'no_clear_winner' | 'edge' | 'winner_found'
            - winner: str or None (variant letter)
            - confidence: 'low' | 'medium' | 'high' or None
            - recommendation: str (actionable advice)
            - delta_pp: float or None (percentage point difference)
    """
    # Empty data
    if not variant_data:
        return {
            'status': 'no_data',
            'winner': None,
            'confidence': None,
            'recommendation': 'Record CTR snapshots first',
            'delta_pp': None
        }

    # Calculate total impressions
    total_impressions = sum(v.get('total_impressions', 0) for v in variant_data)

    # Single variant case
    if len(variant_data) == 1:
        v = variant_data[0]
        variant_letter = v.get('variant_letter', '?')
        avg_ctr = v.get('avg_ctr', 0)
        impressions = v.get('total_impressions', 0)

        # Determine confidence based on impressions
        if impressions < IMPRESSIONS_LOW:
            confidence = 'low'
            confidence_note = ' (low sample size)'
        elif impressions < IMPRESSIONS_MEDIUM:
            confidence = 'medium'
            confidence_note = ''
        else:
            confidence = 'high'
            confidence_note = ''

        # Compare to category average if provided
        if category_avg is not None and impressions >= IMPRESSIONS_LOW:
            delta = avg_ctr - category_avg
            if abs(delta) < 0.5:
                position = 'near'
                rec = f"Variant {variant_letter} CTR ({avg_ctr:.1f}%) is near category average ({category_avg:.1f}%){confidence_note}"
            elif delta > 0:
                position = 'above'
                rec = f"Variant {variant_letter} CTR ({avg_ctr:.1f}%) is +{delta:.1f}pp above category average ({category_avg:.1f}%){confidence_note}"
            else:
                position = 'below'
                rec = f"Variant {variant_letter} CTR ({avg_ctr:.1f}%) is {delta:.1f}pp below category average ({category_avg:.1f}%){confidence_note}"

            return {
                'status': 'single_variant',
                'winner': None,
                'confidence': confidence,
                'recommendation': rec,
                'delta_pp': delta,
                'position': position
            }
        else:
            # No category comparison available or low impressions
            if impressions < IMPRESSIONS_LOW:
                rec = f"Variant {variant_letter} has only {impressions} impressions. Need {IMPRESSIONS_LOW}+ for reliable analysis."
            else:
                rec = f"Variant {variant_letter} CTR: {avg_ctr:.1f}%. No category benchmark available for comparison."

            return {
                'status': 'single_variant',
                'winner': None,
                'confidence': confidence,
                'recommendation': rec,
                'delta_pp': None
            }

    # Multi-variant case: check minimum impressions first
    if total_impressions < IMPRESSIONS_LOW:
        return {
            'status': 'insufficient_data',
            'winner': None,
            'confidence': None,
            'recommendation': f'Only {total_impressions} total impressions. Need {IMPRESSIONS_LOW}+ for reliable comparison.',
            'delta_pp': None
        }

    # Sort by CTR descending to find top performers
    sorted_variants = sorted(variant_data, key=lambda x: x.get('avg_ctr', 0), reverse=True)
    best = sorted_variants[0]
    second = sorted_variants[1]

    best_letter = best.get('variant_letter', '?')
    best_ctr = best.get('avg_ctr', 0)
    second_letter = second.get('variant_letter', '?')
    second_ctr = second.get('avg_ctr', 0)

    delta_pp = best_ctr - second_ctr

    # Determine confidence based on total impressions
    if total_impressions < IMPRESSIONS_MEDIUM:
        confidence = 'low'
    elif total_impressions < IMPRESSIONS_HIGH:
        confidence = 'medium'
    else:
        confidence = 'high'

    # Apply thresholds
    if delta_pp < CTR_DELTA_TIE:
        return {
            'status': 'no_clear_winner',
            'winner': None,
            'confidence': confidence,
            'recommendation': f'CTR difference ({delta_pp:.2f}pp) is below {CTR_DELTA_TIE}pp threshold. Variants {best_letter} and {second_letter} are effectively tied.',
            'delta_pp': delta_pp
        }
    elif delta_pp < CTR_DELTA_EDGE:
        return {
            'status': 'edge',
            'winner': best_letter,
            'confidence': confidence,
            'recommendation': f'Variant {best_letter} ({best_ctr:.1f}%) has marginal advantage over {second_letter} ({second_ctr:.1f}%). Delta: +{delta_pp:.2f}pp. Consider collecting more data.',
            'delta_pp': delta_pp
        }
    elif delta_pp < CTR_DELTA_CLEAR:
        return {
            'status': 'winner_found',
            'winner': best_letter,
            'confidence': confidence,
            'recommendation': f'Variant {best_letter} ({best_ctr:.1f}%) outperforms {second_letter} ({second_ctr:.1f}%) by +{delta_pp:.2f}pp.',
            'delta_pp': delta_pp
        }
    else:
        # Clear winner (3.0+pp difference)
        return {
            'status': 'winner_found',
            'winner': best_letter,
            'confidence': confidence,
            'recommendation': f'CLEAR WINNER: Variant {best_letter} ({best_ctr:.1f}%) decisively outperforms {second_letter} ({second_ctr:.1f}%) by +{delta_pp:.2f}pp.',
            'delta_pp': delta_pp
        }


# =========================================================================
# ORCHESTRATOR FUNCTIONS
# =========================================================================

def compare_variants_for_video(
    video_id: str,
    variant_type: str = 'thumbnail',
    benchmarks: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Compare variants for a specific video and return verdict with context.

    Orchestrates database calls and verdict calculation.

    Args:
        video_id: YouTube video ID
        variant_type: 'thumbnail' or 'title'
        benchmarks: Optional pre-fetched benchmarks (avoids extra DB query)

    Returns:
        Dict with:
            - verdict: Full verdict dict from calculate_verdict
            - video_id: str
            - variant_type: str
            - category: str or None (topic_type)
            - freshness_warning: str or None
            - attribution_rate: str (e.g., "2 of 5 snapshots have variant attribution")
    """
    try:
        db = KeywordDB()

        # Get variant CTR summary
        variant_data = db.get_variant_ctr_summary(video_id, variant_type)

        # Get category from video_performance
        category = None
        try:
            cursor = db._conn.cursor()
            cursor.execute(
                "SELECT topic_type FROM video_performance WHERE video_id = ?",
                (video_id,)
            )
            row = cursor.fetchone()
            if row and row[0]:
                category = row[0]
        except sqlite3.Error:
            pass  # Non-blocking: metadata enrichment only

        # Get benchmarks if not provided
        if benchmarks is None:
            benchmarks = db.get_channel_ctr_benchmarks()

        # Get category average
        category_avg = None
        if category and 'by_category' in benchmarks:
            cat_data = benchmarks.get('by_category', {}).get(category)
            if cat_data and cat_data.get('video_count', 0) >= MIN_CATEGORY_VIDEOS:
                category_avg = cat_data.get('avg_ctr')

        # Fall back to overall average
        if category_avg is None:
            overall = benchmarks.get('overall', {})
            if overall.get('video_count', 0) >= 1:
                category_avg = overall.get('avg_ctr')

        # Calculate verdict
        verdict = calculate_verdict(variant_data, category_avg)

        # Check freshness
        freshness_warning = None
        try:
            cursor = db._conn.cursor()
            cursor.execute(
                "SELECT MAX(snapshot_date) FROM ctr_snapshots WHERE video_id = ?",
                (video_id,)
            )
            row = cursor.fetchone()
            if row and row[0]:
                latest_date = datetime.strptime(row[0], '%Y-%m-%d')
                days_old = (datetime.now(timezone.utc) - latest_date).days
                if days_old > FRESHNESS_DAYS:
                    freshness_warning = f"Data is {days_old} days old. Consider recording fresh CTR snapshots."
        except (sqlite3.Error, ValueError):
            pass  # Non-blocking: freshness check failure does not affect verdict

        # Calculate attribution rate
        attribution_rate = None
        try:
            cursor = db._conn.cursor()
            col = 'active_thumbnail_id' if variant_type == 'thumbnail' else 'active_title_id'
            cursor.execute(
                f"SELECT COUNT(*), SUM(CASE WHEN {col} IS NOT NULL THEN 1 ELSE 0 END) FROM ctr_snapshots WHERE video_id = ?",
                (video_id,)
            )
            row = cursor.fetchone()
            if row and row[0]:
                total = row[0]
                attributed = row[1] or 0
                attribution_rate = f"{attributed} of {total} snapshots have variant attribution"
        except sqlite3.Error:
            pass  # Non-blocking: metadata enrichment only

        db.close()

        return {
            'verdict': verdict,
            'video_id': video_id,
            'variant_type': variant_type,
            'category': category,
            'category_avg': category_avg,
            'freshness_warning': freshness_warning,
            'attribution_rate': attribution_rate
        }

    except Exception as e:
        return {
            'error': f'Failed to compare variants: {e}',
            'video_id': video_id,
            'variant_type': variant_type
        }


def get_benchmarks_report() -> Dict[str, Any]:
    """
    Get channel-wide CTR benchmarks with freshness check.

    Returns:
        Dict with:
            - overall: {avg_ctr, video_count, date_range}
            - by_category: {category: {avg_ctr, video_count, low_sample}}
            - freshness_warning: str or None
    """
    try:
        db = KeywordDB()
        benchmarks = db.get_channel_ctr_benchmarks()
        db.close()

        # Add low_sample flags to categories
        by_category = benchmarks.get('by_category', {})
        for cat, data in by_category.items():
            data['low_sample'] = data.get('video_count', 0) < MIN_CATEGORY_VIDEOS

        # Check freshness
        freshness_warning = None
        date_range = benchmarks.get('overall', {}).get('date_range', {})
        latest_str = date_range.get('latest')
        if latest_str:
            try:
                latest_date = datetime.strptime(latest_str, '%Y-%m-%d')
                days_old = (datetime.now(timezone.utc) - latest_date).days
                if days_old > FRESHNESS_DAYS:
                    freshness_warning = f"Most recent data is {days_old} days old. Consider updating CTR snapshots."
            except ValueError:
                pass  # Non-blocking: date parse failure does not affect benchmarks

        return {
            'overall': benchmarks.get('overall', {}),
            'by_category': by_category,
            'freshness_warning': freshness_warning
        }

    except Exception as e:
        return {
            'error': f'Failed to get benchmarks: {e}'
        }


# =========================================================================
# CLI INTERFACE
# =========================================================================

STATUS_BADGES = {
    'winner_found': 'WINNER',
    'edge': 'EDGE',
    'no_clear_winner': 'TIE',
    'insufficient_data': 'WAIT',
    'single_variant': 'NOTE',
    'no_data': 'NO DATA'
}


def analyze_video_ctr(video_id: str) -> Dict[str, Any]:
    """
    Analyze both thumbnail and title variants for a video.

    Returns combined analysis with both verdicts and benchmark context.
    """
    benchmarks_data = get_benchmarks_report()
    thumb_verdict = compare_variants_for_video(video_id, 'thumbnail', benchmarks_data.get('overall', {}))
    title_verdict = compare_variants_for_video(video_id, 'title', benchmarks_data.get('overall', {}))

    # Get snapshot count and attribution rate
    snapshot_info = None
    try:
        db = KeywordDB()
        cursor = db._conn.cursor()
        cursor.execute(
            """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN active_thumbnail_id IS NOT NULL OR active_title_id IS NOT NULL THEN 1 ELSE 0 END) as attributed,
                MAX(snapshot_date) as latest
            FROM ctr_snapshots WHERE video_id = ?
            """,
            (video_id,)
        )
        row = cursor.fetchone()
        if row and row[0]:
            total = row[0]
            attributed = row[1] or 0
            latest = row[2]
            days_old = None
            if latest:
                try:
                    latest_date = datetime.strptime(latest, '%Y-%m-%d')
                    days_old = (datetime.now(timezone.utc) - latest_date).days
                except ValueError:
                    pass  # Non-blocking: date parse failure does not affect snapshot info
            snapshot_info = {
                'total': total,
                'attributed': attributed,
                'latest': latest,
                'days_old': days_old
            }
        db.close()
    except sqlite3.Error:
        pass  # Non-blocking: snapshot info enrichment only

    return {
        'video_id': video_id,
        'thumbnail_verdict': thumb_verdict,
        'title_verdict': title_verdict,
        'benchmarks': benchmarks_data,
        'snapshot_info': snapshot_info
    }


def format_video_terminal(analysis: Dict[str, Any]) -> str:
    """Format video CTR analysis for terminal display."""
    lines = []
    video_id = analysis.get('video_id', 'Unknown')

    lines.append(f"CTR Analysis: {video_id}")
    lines.append("=" * 60)
    lines.append("")

    # Thumbnail verdict
    thumb = analysis.get('thumbnail_verdict', {})
    thumb_verdict = thumb.get('verdict', {})
    thumb_status = thumb_verdict.get('status', 'no_data')
    thumb_badge = STATUS_BADGES.get(thumb_status, thumb_status.upper())

    lines.append("Thumbnail Verdict:")
    if thumb_verdict.get('winner'):
        lines.append(f"  [{thumb_badge}] Variant {thumb_verdict['winner']} (+{thumb_verdict.get('delta_pp', 0):.1f}pp CTR)")
    else:
        lines.append(f"  [{thumb_badge}] {thumb_verdict.get('recommendation', 'No data')[:60]}")
    if thumb_verdict.get('confidence'):
        lines.append(f"  Confidence: {thumb_verdict['confidence'].upper()}")
    lines.append("")

    # Title verdict
    title = analysis.get('title_verdict', {})
    title_verdict = title.get('verdict', {})
    title_status = title_verdict.get('status', 'no_data')
    title_badge = STATUS_BADGES.get(title_status, title_status.upper())

    lines.append("Title Verdict:")
    if title_verdict.get('winner'):
        lines.append(f"  [{title_badge}] Variant {title_verdict['winner']} (+{title_verdict.get('delta_pp', 0):.1f}pp CTR)")
    else:
        lines.append(f"  [{title_badge}] {title_verdict.get('recommendation', 'No data')[:60]}")
    if title_verdict.get('confidence'):
        lines.append(f"  Confidence: {title_verdict['confidence'].upper()}")
    lines.append("")

    # Benchmark context
    benchmarks = analysis.get('benchmarks', {})
    overall = benchmarks.get('overall', {})
    by_category = benchmarks.get('by_category', {})
    category = thumb.get('category') or title.get('category')

    lines.append("Benchmark Context:")
    if overall.get('video_count', 0) > 0:
        lines.append(f"  Channel avg CTR: {overall.get('avg_ctr', 0):.2f}%")
    if category and category in by_category:
        cat_data = by_category[category]
        sample_note = " *" if cat_data.get('low_sample') else ""
        lines.append(f"  Category ({category}): {cat_data.get('avg_ctr', 0):.2f}% (n={cat_data.get('video_count', 0)} videos){sample_note}")
    lines.append("")

    # Snapshot info
    snap_info = analysis.get('snapshot_info')
    if snap_info:
        lines.append(f"Data: {snap_info['attributed']} of {snap_info['total']} snapshots with variant attribution")
        if snap_info.get('latest'):
            days_str = f" ({snap_info['days_old']} days ago)" if snap_info.get('days_old') is not None else ""
            lines.append(f"Latest snapshot: {snap_info['latest']}{days_str}")
        lines.append("")

    # Freshness warning
    if snap_info and snap_info.get('days_old') and snap_info['days_old'] > FRESHNESS_DAYS:
        lines.append(f"WARNING: Latest snapshot is {snap_info['days_old']} days old - data may be stale")
        lines.append("")

    return "\n".join(lines)


def format_video_markdown(analysis: Dict[str, Any]) -> str:
    """Format video CTR analysis as markdown."""
    lines = []
    video_id = analysis.get('video_id', 'Unknown')

    lines.append(f"# CTR Analysis: {video_id}")
    lines.append("")

    # Thumbnail verdict
    thumb = analysis.get('thumbnail_verdict', {})
    thumb_verdict = thumb.get('verdict', {})
    thumb_status = thumb_verdict.get('status', 'no_data')
    thumb_badge = STATUS_BADGES.get(thumb_status, thumb_status.upper())

    lines.append("## Thumbnail Verdict")
    lines.append("")
    if thumb_verdict.get('winner'):
        lines.append(f"**[{thumb_badge}]** Variant {thumb_verdict['winner']} (+{thumb_verdict.get('delta_pp', 0):.1f}pp CTR)")
    else:
        lines.append(f"**[{thumb_badge}]** {thumb_verdict.get('recommendation', 'No data')}")
    if thumb_verdict.get('confidence'):
        lines.append(f"- Confidence: {thumb_verdict['confidence'].upper()}")
    lines.append("")

    # Title verdict
    title = analysis.get('title_verdict', {})
    title_verdict = title.get('verdict', {})
    title_status = title_verdict.get('status', 'no_data')
    title_badge = STATUS_BADGES.get(title_status, title_status.upper())

    lines.append("## Title Verdict")
    lines.append("")
    if title_verdict.get('winner'):
        lines.append(f"**[{title_badge}]** Variant {title_verdict['winner']} (+{title_verdict.get('delta_pp', 0):.1f}pp CTR)")
    else:
        lines.append(f"**[{title_badge}]** {title_verdict.get('recommendation', 'No data')}")
    if title_verdict.get('confidence'):
        lines.append(f"- Confidence: {title_verdict['confidence'].upper()}")
    lines.append("")

    # Benchmark context
    benchmarks = analysis.get('benchmarks', {})
    overall = benchmarks.get('overall', {})
    by_category = benchmarks.get('by_category', {})
    category = thumb.get('category') or title.get('category')

    lines.append("## Benchmark Context")
    lines.append("")
    if overall.get('video_count', 0) > 0:
        lines.append(f"- **Channel avg CTR:** {overall.get('avg_ctr', 0):.2f}%")
    if category and category in by_category:
        cat_data = by_category[category]
        sample_note = " *(low sample)*" if cat_data.get('low_sample') else ""
        lines.append(f"- **Category ({category}):** {cat_data.get('avg_ctr', 0):.2f}% (n={cat_data.get('video_count', 0)} videos){sample_note}")
    lines.append("")

    # Snapshot info
    snap_info = analysis.get('snapshot_info')
    if snap_info:
        lines.append(f"_Data: {snap_info['attributed']} of {snap_info['total']} snapshots with variant attribution_")
        if snap_info.get('latest'):
            days_str = f" ({snap_info['days_old']} days ago)" if snap_info.get('days_old') is not None else ""
            lines.append(f"_Latest snapshot: {snap_info['latest']}{days_str}_")
        lines.append("")

    # Freshness warning
    if snap_info and snap_info.get('days_old') and snap_info['days_old'] > FRESHNESS_DAYS:
        lines.append(f"> **Warning:** Latest snapshot is {snap_info['days_old']} days old - data may be stale")
        lines.append("")

    return "\n".join(lines)


def format_benchmarks_terminal(report: Dict[str, Any]) -> str:
    """Format benchmarks report for terminal display."""
    if 'error' in report:
        return f"Error: {report['error']}"

    lines = []
    lines.append("Channel CTR Benchmarks")
    lines.append("=" * 60)
    lines.append("")

    overall = report.get('overall', {})
    if overall.get('video_count', 0) > 0:
        lines.append(f"Overall: {overall.get('avg_ctr', 0):.2f}% avg CTR ({overall.get('video_count', 0)} videos)")
        date_range = overall.get('date_range', {})
        if date_range.get('earliest') and date_range.get('latest'):
            lines.append(f"Data range: {date_range['earliest']} to {date_range['latest']}")
        lines.append("")

    by_category = report.get('by_category', {})
    if by_category:
        lines.append("By Category:")
        # Find max category name length for alignment
        max_len = max(len(cat) for cat in by_category.keys()) if by_category else 10
        for cat, data in sorted(by_category.items(), key=lambda x: x[1].get('avg_ctr', 0), reverse=True):
            sample_note = " *low sample" if data.get('low_sample') else ""
            lines.append(f"  {cat:<{max_len}}  {data.get('avg_ctr', 0):>5.2f}%  (n={data.get('video_count', 0)}){sample_note}")
        lines.append("")
        lines.append("* Categories with fewer than 2 videos have limited reliability")
        lines.append("")

    if not overall.get('video_count'):
        lines.append("No CTR data recorded yet.")
        lines.append("Use: python variants.py record-ctr VIDEO_ID CTR IMPRESSIONS VIEWS")
        lines.append("")

    if report.get('freshness_warning'):
        lines.append(f"WARNING: {report['freshness_warning']}")
        lines.append("")

    return "\n".join(lines)


def format_benchmarks_markdown(report: Dict[str, Any]) -> str:
    """Format benchmarks report as markdown."""
    if 'error' in report:
        return f"# CTR Benchmarks\n\n**Error:** {report['error']}\n"

    lines = []
    lines.append("# Channel CTR Benchmarks")
    lines.append("")
    lines.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}_")
    lines.append("")

    overall = report.get('overall', {})
    if overall.get('video_count', 0) > 0:
        lines.append("## Overall")
        lines.append("")
        lines.append(f"- **Average CTR:** {overall.get('avg_ctr', 0):.2f}%")
        lines.append(f"- **Videos analyzed:** {overall.get('video_count', 0)}")
        date_range = overall.get('date_range', {})
        if date_range.get('earliest') and date_range.get('latest'):
            lines.append(f"- **Data range:** {date_range['earliest']} to {date_range['latest']}")
        lines.append("")

    by_category = report.get('by_category', {})
    if by_category:
        lines.append("## By Category")
        lines.append("")
        lines.append("| Category | Avg CTR | Videos | Note |")
        lines.append("|----------|---------|--------|------|")
        for cat, data in sorted(by_category.items(), key=lambda x: x[1].get('avg_ctr', 0), reverse=True):
            note = "low sample" if data.get('low_sample') else ""
            lines.append(f"| {cat} | {data.get('avg_ctr', 0):.2f}% | {data.get('video_count', 0)} | {note} |")
        lines.append("")

    if not overall.get('video_count'):
        lines.append("_No CTR data recorded yet._")
        lines.append("")

    if report.get('freshness_warning'):
        lines.append(f"> **Warning:** {report['freshness_warning']}")
        lines.append("")

    return "\n".join(lines)


def find_project_folder(video_id: str) -> Optional[Path]:
    """Find project folder for a video ID."""
    project_root = Path(__file__).resolve().parent.parent.parent
    video_projects = project_root / 'video-projects'

    if not video_projects.exists():
        return None

    # Search in lifecycle folders
    for lifecycle in ['_IN_PRODUCTION', '_READY_TO_FILM', '_ARCHIVED']:
        lifecycle_path = video_projects / lifecycle
        if lifecycle_path.exists():
            for project in lifecycle_path.iterdir():
                if project.is_dir():
                    # Check if any file in project contains video_id
                    for f in project.glob('*.md'):
                        try:
                            content = f.read_text(encoding='utf-8')
                            if video_id in content:
                                return project
                        except (OSError, UnicodeDecodeError):
                            pass  # Non-blocking: file read failure skips this file
    return None


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='CTR Analysis - Compare variant performance and channel benchmarks',
        epilog="""
Examples:
  python benchmarks.py VIDEO_ID              Analyze video variants
  python benchmarks.py VIDEO_ID --markdown   Save analysis as markdown
  python benchmarks.py --benchmarks          Show channel CTR benchmarks
  python benchmarks.py --benchmarks --markdown  Save benchmarks as markdown

Note: Only record CTR for long-form videos. Shorts are excluded from analysis.
        """
    )
    parser.add_argument('video_id', nargs='?', help='YouTube video ID to analyze')
    parser.add_argument('--benchmarks', action='store_true', help='Show channel CTR benchmarks')
    parser.add_argument('--markdown', action='store_true', help='Output/save as markdown')

    args = parser.parse_args()

    if args.benchmarks:
        # Channel benchmarks mode
        report = get_benchmarks_report()
        if args.markdown:
            output = format_benchmarks_markdown(report)
            # Save to channel-data folder
            project_root = Path(__file__).resolve().parent.parent.parent
            output_path = project_root / 'channel-data' / 'CTR-BENCHMARKS.md'
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Saved to: {output_path}")
        else:
            print(format_benchmarks_terminal(report))

    elif args.video_id:
        # Video analysis mode
        analysis = analyze_video_ctr(args.video_id)
        if args.markdown:
            output = format_video_markdown(analysis)
            # Try to find project folder, fall back to current dir
            project_folder = find_project_folder(args.video_id)
            if project_folder:
                output_path = project_folder / f'CTR-ANALYSIS-{args.video_id}.md'
            else:
                output_path = Path(f'CTR-ANALYSIS-{args.video_id}.md')
            output_path.write_text(output, encoding='utf-8')
            print(f"Saved to: {output_path}")
        else:
            print(format_video_terminal(analysis))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
