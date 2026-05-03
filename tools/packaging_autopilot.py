"""
Packaging Autopilot — Single command for the entire packaging feedback loop.

Runs weekly (or on demand) to:
1. Snapshot own-channel CTR/view velocity
2. Check recent videos against swap thresholds (48h protocol)
3. Scan competitor channels for new outliers
4. Generate swap candidates for underperforming videos
5. Output a packaging status report

Replaces the manual SWAP-PROTOCOL.md and weekly check workflow.

Usage:
    python -m tools.packaging_autopilot                    # Full report
    python -m tools.packaging_autopilot --check-recent     # 48h swap check only
    python -m tools.packaging_autopilot --competitors      # Competitor scan only
    python -m tools.packaging_autopilot --retitle VIDEO_ID # Generate swap candidates for one video

The 48h swap logic (from SWAP-PROTOCOL.md):
    CTR < 2% at 48h + >500 impressions -> SWAP TITLE + THUMBNAIL
    CTR 2-4% at 48h + >500 impressions -> SWAP TITLE only
    CTR > 4% -> Hold steady
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from tools.logging_config import get_logger

logger = get_logger(__name__)

_PROJECT_ROOT = Path(__file__).parent.parent
_ANALYTICS_DB = _PROJECT_ROOT / "tools" / "youtube_analytics" / "analytics.db"


# =============================================================================
# 48-hour swap check
# =============================================================================

def check_recent_videos(days: int = 7) -> List[Dict[str, Any]]:
    """
    Check recent videos against the 48h swap protocol thresholds.

    Pulls from analytics.db and ctr_snapshots to find videos that need
    title/thumbnail swaps.

    Args:
        days: Look at videos published in the last N days (default 7)

    Returns:
        List of video assessments, each with action recommendation.
    """
    results = []

    try:
        if not _ANALYTICS_DB.exists():
            return [{'error': 'analytics.db not found'}]

        conn = sqlite3.connect(str(_ANALYTICS_DB))
        conn.row_factory = sqlite3.Row

        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d')

        cursor = conn.cursor()
        cursor.execute("""
            SELECT video_id, title, published_at, views, impressions, ctr_percent,
                   avg_view_percentage, subscribers_gained, topic_type
            FROM videos
            WHERE published_at >= ?
            ORDER BY published_at DESC
        """, (cutoff,))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            assessment = _assess_video(dict(row))
            results.append(assessment)

    except Exception as e:
        logger.error("Failed to check recent videos: %s", e)
        results.append({'error': str(e)})

    return results


def _assess_video(video: Dict) -> Dict[str, Any]:
    """Apply the 48h swap protocol to a single video."""
    ctr = video.get('ctr_percent') or 0
    impressions = video.get('impressions') or 0
    views = video.get('views') or 0
    title = video.get('title', '')

    assessment = {
        'video_id': video.get('video_id', ''),
        'title': title,
        'published': video.get('published_at', ''),
        'views': views,
        'impressions': impressions,
        'ctr': ctr,
        'retention': video.get('avg_view_percentage') or 0,
        'subs_gained': video.get('subscribers_gained') or 0,
        'action': 'HOLD',
        'reason': '',
        'swap_candidates': [],
    }

    # Try to get CTR from ctr_snapshots if analytics.db has nulls
    if ctr == 0 and video.get('video_id'):
        try:
            kw_db = _PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
            if kw_db.exists():
                kw_conn = sqlite3.connect(str(kw_db))
                kw_cursor = kw_conn.cursor()
                kw_cursor.execute("""
                    SELECT ctr_percent, impression_count, view_count
                    FROM ctr_snapshots
                    WHERE video_id = ? AND ctr_percent > 0
                    ORDER BY snapshot_date DESC LIMIT 1
                """, (video['video_id'],))
                row = kw_cursor.fetchone()
                if row:
                    ctr = row[0]
                    impressions = impressions or row[1]
                    views = views or row[2]
                    assessment['ctr'] = ctr
                    assessment['impressions'] = impressions
                    assessment['views'] = views
                    assessment['ctr_source'] = 'ctr_snapshots'
                kw_conn.close()
        except Exception:
            pass

    # Not enough data yet
    if impressions < 500:
        assessment['action'] = 'WAIT'
        assessment['reason'] = f'Only {impressions} impressions — need 500+ for reliable CTR'
        return assessment

    # CTR < 2%: SWAP TITLE + THUMBNAIL
    if ctr > 0 and ctr < 2.0:
        assessment['action'] = 'SWAP_BOTH'
        assessment['reason'] = f'CTR {ctr:.1f}% < 2% with {impressions:,} impressions'
        assessment['swap_candidates'] = _generate_swap_candidates(title)

    # CTR 2-4%: SWAP TITLE ONLY
    elif ctr >= 2.0 and ctr < 4.0:
        assessment['action'] = 'SWAP_TITLE'
        assessment['reason'] = f'CTR {ctr:.1f}% in 2-4% range — title swap may help'
        assessment['swap_candidates'] = _generate_swap_candidates(title)

    # CTR > 4%: HOLD
    elif ctr >= 4.0:
        assessment['action'] = 'HOLD'
        assessment['reason'] = f'CTR {ctr:.1f}% is strong — hold steady'

    # No CTR data
    else:
        assessment['action'] = 'CHECK_STUDIO'
        assessment['reason'] = 'No CTR data available — check YouTube Studio manually'

    # Flag high-retention + low-views as retitle candidates
    retention = video.get('avg_view_percentage') or 0
    if retention > 30 and views < 100 and ctr > 0 and ctr < 3:
        assessment['retitle_candidate'] = True
        assessment['reason'] += f' | RETITLE CANDIDATE: {retention:.0f}% retention but only {views} views'

    return assessment


def _generate_swap_candidates(current_title: str) -> List[Dict[str, Any]]:
    """Generate alternative title candidates using title_scorer."""
    try:
        from tools.title_scorer import score_title, detect_pattern

        current_pattern = detect_pattern(current_title)
        current_score = score_title(current_title)

        # Suggest the user needs to generate alternatives
        # (We can't auto-generate titles, but we can score what pattern to try)
        return [{
            'current_pattern': current_pattern,
            'current_score': current_score['score'],
            'suggestion': _suggest_pattern_change(current_pattern, current_score),
        }]
    except Exception:
        return []


def _suggest_pattern_change(current_pattern: str, score_result: dict) -> str:
    """Suggest what pattern to switch to based on current pattern's failure."""
    pattern_alternatives = {
        'declarative': 'Try versus framing ("X vs Y") or add evidence promise ("Here\'s the proof")',
        'how_why': 'Try declarative with two sentences ("Statement. Evidence promise.")',
        'versus': 'Try declarative with controversy frame ("X Claims Y. The Documents Say Otherwise.")',
        'colon': 'Remove colon — use period or em-dash. Try declarative pattern.',
        'question': 'Convert to declarative statement. Questions underperform.',
        'the_x_that': 'Completely rewrite — worst pattern. Try versus or declarative.',
    }
    return pattern_alternatives.get(current_pattern, 'Try a different title pattern.')


# =============================================================================
# Competitor scan
# =============================================================================

def scan_competitors_fresh() -> Dict[str, Any]:
    """
    Run a fresh competitor scan and return outliers.

    This wraps the existing competitor_tracker + packaging_intel outlier scanner.
    """
    from tools.packaging_intel import scan_competitor_outliers

    outliers = scan_competitor_outliers()

    return {
        'outlier_count': len(outliers),
        'outliers': outliers[:10],  # top 10
        'scan_time': datetime.now(timezone.utc).isoformat(),
    }


# =============================================================================
# Full report
# =============================================================================

def generate_full_report(days: int = 14) -> str:
    """Generate a complete packaging status report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  PACKAGING AUTOPILOT REPORT")
    lines.append(f"  Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 60)

    # Section 1: Recent video check
    lines.append("\n--- RECENT VIDEOS (48h SWAP CHECK) ---\n")
    recent = check_recent_videos(days=days)

    action_counts = {'SWAP_BOTH': 0, 'SWAP_TITLE': 0, 'HOLD': 0, 'WAIT': 0, 'CHECK_STUDIO': 0}
    for v in recent:
        if 'error' in v:
            lines.append(f"  ERROR: {v['error']}")
            continue

        action = v['action']
        action_counts[action] = action_counts.get(action, 0) + 1

        icon = {'SWAP_BOTH': 'XX', 'SWAP_TITLE': 'X.', 'HOLD': 'OK', 'WAIT': '..', 'CHECK_STUDIO': '??'}
        lines.append(
            f"  [{icon.get(action, '??')}] {v['ctr']:.1f}% CTR | {v['views']:>5} views | "
            f"{v['title'][:45]}"
        )
        if action.startswith('SWAP'):
            lines.append(f"       -> {v['reason']}")
            for cand in v.get('swap_candidates', []):
                if 'suggestion' in cand:
                    lines.append(f"       -> Suggestion: {cand['suggestion']}")

    lines.append(f"\n  Summary: {action_counts.get('SWAP_BOTH', 0)} need full swap, "
                 f"{action_counts.get('SWAP_TITLE', 0)} need title swap, "
                 f"{action_counts.get('HOLD', 0)} performing well")

    # Section 2: Competitor outliers
    lines.append("\n--- COMPETITOR OUTLIERS (3x+ channel avg) ---\n")
    comp = scan_competitors_fresh()
    if comp['outliers']:
        for o in comp['outliers'][:5]:
            lines.append(f"  {o['ratio']}x | {o['views']:>12,} views | {o['title'][:50]}")
    else:
        lines.append("  No recent outliers found.")

    lines.append(f"\n  Total outliers in niche: {comp['outlier_count']}")

    # Section 3: Quick stats
    lines.append("\n--- CHANNEL PACKAGING HEALTH ---\n")
    try:
        conn = sqlite3.connect(str(_ANALYTICS_DB))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Avg CTR across all videos with data
        cursor.execute("SELECT AVG(ctr_percent), COUNT(*) FROM videos WHERE ctr_percent > 0")
        row = cursor.fetchone()
        if row and row[0]:
            lines.append(f"  Avg CTR: {row[0]:.1f}% (across {row[1]} videos)")

        # Videos with CTR < 2% and > 500 impressions (actionable swaps)
        cursor.execute("""
            SELECT COUNT(*) FROM videos
            WHERE ctr_percent > 0 AND ctr_percent < 2.0 AND impressions > 500
        """)
        swap_count = cursor.fetchone()[0]
        lines.append(f"  Videos needing swap: {swap_count}")

        # High retention + low views
        cursor.execute("""
            SELECT COUNT(*) FROM videos
            WHERE avg_view_percentage > 30 AND views < 100 AND ctr_percent > 0 AND ctr_percent < 3
        """)
        retitle_count = cursor.fetchone()[0]
        lines.append(f"  Retitle candidates: {retitle_count} (>30% retention, <100 views)")

        conn.close()
    except Exception as e:
        lines.append(f"  Could not read analytics: {e}")

    lines.append("")
    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Packaging Autopilot -- automated feedback loop',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--check-recent', action='store_true',
                        help='Check recent videos against swap thresholds')
    parser.add_argument('--competitors', action='store_true',
                        help='Scan competitor channels for outliers')
    parser.add_argument('--days', type=int, default=14,
                        help='Look back N days (default 14)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.check_recent:
        results = check_recent_videos(days=args.days)
        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            for v in results:
                if 'error' in v:
                    print(f"ERROR: {v['error']}")
                else:
                    print(f"[{v['action']}] {v['ctr']:.1f}% CTR | {v['views']} views | {v['title'][:50]}")
                    print(f"  {v['reason']}")
        return

    if args.competitors:
        comp = scan_competitors_fresh()
        if args.json:
            print(json.dumps(comp, indent=2, default=str))
        else:
            for o in comp['outliers']:
                print(f"  {o['ratio']}x | {o['views']:>12,} views | {o['title'][:55]}")
            print(f"\nTotal: {comp['outlier_count']} outliers")
        return

    # Default: full report
    report = generate_full_report(days=args.days)
    # Handle Windows cp1252 encoding issues with non-ASCII chars in titles
    sys.stdout.buffer.write(report.encode('utf-8', errors='replace'))
    sys.stdout.buffer.write(b'\n')


if __name__ == '__main__':
    main()
