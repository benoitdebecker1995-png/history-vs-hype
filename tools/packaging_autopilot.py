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

The swap logic (V5 thresholds, from SWAP-PROTOCOL.md, 2026-06-14 live data):
    CTR < 1.3% + >500 impressions -> SWAP one lever NOW (urgent; algo throttling)
    CTR 1.3-4% + >500 impressions -> SWAP one lever to lift
    CTR >= 4%  -> Hold steady
Single-variable doctrine: change the thumbnail OR the title, never both (changing
both re-blends the CTR). Surface picks the lever: Suggested/Browse -> thumbnail,
Search -> title. Log every swap with `tools/swap_ledger.py` so the delta is tracked.
"""

import json
import sqlite3
from tools.youtube_analytics.store import AnalyticsStore
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

        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d')

        with AnalyticsStore.open(_ANALYTICS_DB) as store:
            rows = store.videos(published_after=cutoff)

        for row in rows:
            assessment = _assess_video(row)
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

    # V5 thresholds (2026-06-14 live data): the algorithm throttles fast, and you
    # learn by changing ONE lever at a time (single-variable doctrine — changing
    # both title AND thumbnail re-blends the CTR and teaches nothing about which
    # moved it). See tools/SWAP-PROTOCOL.md, memory/feedback-filters-not-predictors.md.
    surface = (video.get('traffic_source') or video.get('surface') or '').strip()

    # CTR < 1.3%: urgent — swap ONE lever now
    if ctr > 0 and ctr < 1.3:
        assessment['action'] = 'SWAP'
        assessment['priority'] = 'URGENT'
        assessment['lever'] = _lever_guidance(surface)
        assessment['reason'] = (f'CTR {ctr:.1f}% < 1.3% with {impressions:,} impressions '
                                f'— algorithm throttling. {assessment["lever"]}')
        assessment['swap_candidates'] = _generate_swap_candidates(title)

    # CTR 1.3-4%: swap one lever to lift
    elif 1.3 <= ctr < 4.0:
        assessment['action'] = 'SWAP'
        assessment['priority'] = 'NORMAL'
        assessment['lever'] = _lever_guidance(surface)
        assessment['reason'] = (f'CTR {ctr:.1f}% in 1.3-4% range. {assessment["lever"]}')
        assessment['swap_candidates'] = _generate_swap_candidates(title)

    # CTR >= 4%: HOLD
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


def _lever_guidance(surface: str) -> str:
    """Single-variable swap guidance: pick ONE lever based on the dominant surface.

    Suggested/Browse-dominant = thumbnail-dominant surface, so swap the thumbnail.
    Search-dominant = title/keyword-dominant surface, so swap the title.
    Never both — changing two re-blends the CTR (filters-not-predictors doctrine).
    Log the swap with `python -m tools.swap_ledger open ...` so the delta is tracked.
    """
    s = surface.lower()
    if 'search' in s:
        return 'Swap the TITLE only (Search-dominant surface); leave the thumbnail. Log it in swap_ledger.'
    if 'suggest' in s or 'browse' in s or 'related' in s:
        return 'Swap the THUMBNAIL only (Suggested/Browse-dominant surface); leave the title. Log it in swap_ledger.'
    return ('Swap ONE lever, not both: thumbnail if traffic is mostly Suggested/Browse, '
            'title if mostly Search. Log it in swap_ledger.')


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
    """Suggest a DIFFERENT pattern to test against the failing one.

    A swap should change the pattern (so it's a real alternative), not "fix" a
    style flag. The colon/year/the_x_that "rules" are RETIRED causal claims —
    confounded single-snapshot correlations, A/B-testable hedges, never "remove
    it" (the channel's #1 and #3 videos both use colons). See PACKAGING_MANDATE
    Tier 2/3 and title_scorer v5.
    """
    pattern_alternatives = {
        'declarative': 'Try versus framing ("X vs Y") or add an evidence promise ("Here\'s the proof")',
        'how_why': 'Try declarative two-sentence ("Statement. Evidence promise.")',
        'versus': 'Try declarative with a controversy frame ("X Claims Y. The Documents Say Otherwise.")',
        'colon': 'Try a declarative two-punch (period instead of colon) — the colon itself is not the problem (#1/#3 videos use colons); change the pattern to get a real alternative arm.',
        'question': 'Try a declarative statement arm (small sample on questions; test the alternative).',
        'the_x_that': 'Try a versus or declarative arm — the "The X That Y" rule is retired (CIA Condor used it at 4.91% CTR); change the pattern to get contrast.',
    }
    return pattern_alternatives.get(current_pattern, 'Try a different title pattern as the alternative arm.')


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

    action_counts = {'SWAP': 0, 'HOLD': 0, 'WAIT': 0, 'CHECK_STUDIO': 0}
    for v in recent:
        if 'error' in v:
            lines.append(f"  ERROR: {v['error']}")
            continue

        action = v['action']
        action_counts[action] = action_counts.get(action, 0) + 1

        icon = {'SWAP': 'X.', 'HOLD': 'OK', 'WAIT': '..', 'CHECK_STUDIO': '??'}
        tag = action
        if action == 'SWAP' and v.get('priority') == 'URGENT':
            tag = 'SWAP!'
        lines.append(
            f"  [{icon.get(action, '??')}] {v['ctr']:.1f}% CTR | {v['views']:>5} views | "
            f"{v['title'][:45]}"
        )
        if action == 'SWAP':
            lines.append(f"       -> {v['reason']}")
            for cand in v.get('swap_candidates', []):
                if 'suggestion' in cand:
                    lines.append(f"       -> If swapping the title: {cand['suggestion']}")

    lines.append(f"\n  Summary: {action_counts.get('SWAP', 0)} need a single-lever swap, "
                 f"{action_counts.get('HOLD', 0)} performing well, "
                 f"{action_counts.get('WAIT', 0)} too early")

    # Section 2: Competitor outliers
    lines.append("\n--- COMPETITOR OUTLIERS (3x+ channel avg) ---\n")
    comp = scan_competitors_fresh()
    if comp['outliers']:
        for o in comp['outliers'][:5]:
            lines.append(f"  {o['ratio']}x | {o['views']:>12,} views | {o['title'][:50]}")
    else:
        lines.append("  No recent outliers found.")

    lines.append(f"\n  Total outliers in niche: {comp['outlier_count']}")

    # Section 2b: Swap experiments due to read
    lines.append("\n--- SWAP EXPERIMENTS DUE TO READ ---\n")
    try:
        from tools.swap_ledger import experiments_due
        due = experiments_due()
        if due:
            for e in due:
                lines.append(
                    f"  [DUE] #{e['id']} {e['video_id']} ({e['variable']}) — "
                    f"baseline {e['baseline_ctr']:.2f}%, read by {e['planned_read_date']}"
                )
                lines.append(f"        -> python -m tools.swap_ledger read {e['id']}")
        else:
            lines.append("  None due. (Open one after a single-variable swap: "
                         "python -m tools.swap_ledger open ...)")
    except Exception as e:
        lines.append(f"  Could not read swap ledger: {e}")

    # Section 3: Quick stats
    lines.append("\n--- CHANNEL PACKAGING HEALTH ---\n")
    try:
        with AnalyticsStore.open(_ANALYTICS_DB) as store:
            # Avg CTR across all videos with data.
            avg = store.execute(
                "SELECT AVG(ctr_percent) AS avg_ctr, COUNT(*) AS n "
                "FROM videos WHERE ctr_percent > 0"
            )
            if avg and avg[0]['avg_ctr']:
                lines.append(f"  Avg CTR: {avg[0]['avg_ctr']:.1f}% (across {avg[0]['n']} videos)")

            # Videos below the 4% hold floor with a real impression test (swap candidates).
            swap = store.execute(
                "SELECT COUNT(*) AS n FROM videos "
                "WHERE ctr_percent > 0 AND ctr_percent < 4.0 AND impressions > 500"
            )
            lines.append(f"  Swap candidates (<4% CTR, >500 imp): {swap[0]['n']}")

            # High retention + low views.
            retitle = store.execute(
                "SELECT COUNT(*) AS n FROM videos "
                "WHERE avg_view_percentage > 30 AND views < 100 "
                "AND ctr_percent > 0 AND ctr_percent < 3"
            )
            lines.append(f"  Retitle candidates: {retitle[0]['n']} (>30% retention, <100 views)")
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
