"""
Discovery Diagnostics Module

Analyzes why videos aren't being discovered by diagnosing impression and CTR issues.
Provides actionable fixes AND learnings for future videos.

Usage:
    CLI:
        python diagnostics.py VIDEO_ID
        python diagnostics.py VIDEO_ID --ctr 3.5
        python diagnostics.py VIDEO_ID --json

    Python:
        from diagnostics import diagnose_discovery, get_diagnostic_thresholds

        thresholds = get_diagnostic_thresholds(channel_averages)
        diagnosis = diagnose_discovery(video_metrics, channel_averages, ctr=4.2)

Diagnostic logic:
    - Low impressions (< 50% of channel avg) = SEO/metadata issue
    - Low CTR (< 4%) = Title/thumbnail issue
    - Both low = Topic selection issue

Dependencies:
    - channel_averages.py (Phase 9-01) for channel benchmarks
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import channel averages module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / 'youtube-analytics'))
    from channel_averages import get_channel_averages
    from metrics import get_video_metrics
except ImportError:
    get_channel_averages = None
    get_video_metrics = None


def get_diagnostic_thresholds(channel_averages: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate channel-specific diagnostic thresholds.

    Uses channel averages to determine what counts as "low" for this channel.

    Args:
        channel_averages: dict from get_channel_averages() with avg_views, sample_size, etc.

    Returns:
        dict:
            {
                'impressions_low': float,       # 50% of channel average
                'impressions_baseline': float,  # Channel average
                'ctr_low': 4.0,                 # Fixed industry benchmark
                'ctr_good': 6.0,
                'retention_low': 25.0,
                'retention_good': 35.0
            }
    """
    avg_views = channel_averages.get('avg_views', 1000)

    # Impressions thresholds (channel-specific)
    impressions_baseline = avg_views
    impressions_low = avg_views * 0.5

    # CTR thresholds (industry benchmarks for educational content)
    ctr_low = 4.0
    ctr_good = 6.0

    # Retention thresholds (industry benchmarks)
    retention_low = 25.0
    retention_good = 35.0

    return {
        'impressions_low': impressions_low,
        'impressions_baseline': impressions_baseline,
        'ctr_low': ctr_low,
        'ctr_good': ctr_good,
        'retention_low': retention_low,
        'retention_good': retention_good
    }


def diagnose_discovery(
    video_metrics: Dict[str, Any],
    channel_averages: Dict[str, Any],
    ctr: Optional[float] = None
) -> Dict[str, Any]:
    """
    Diagnose why a video isn't being discovered.

    Analyzes impressions and CTR to identify the primary discovery blocker.
    Generates actionable fixes AND learnings for future videos.

    Args:
        video_metrics: dict from get_video_metrics() with views, watch_time, etc.
        channel_averages: dict from get_channel_averages()
        ctr: Optional CTR percentage (0-100). If None, assumes CTR unavailable.

    Returns:
        dict:
            {
                'video_id': '...',
                'diagnosis': {
                    'primary_issue': 'LOW_IMPRESSIONS' | 'LOW_CTR' | 'BOTH' | 'NONE',
                    'severity': 'HIGH' | 'MEDIUM' | 'LOW',
                    'summary': 'Brief one-line diagnosis'
                },
                'issues': [
                    {
                        'type': 'LOW_IMPRESSIONS',
                        'severity': 'HIGH',
                        'value': 230,
                        'benchmark': 1500,
                        'description': 'Impressions 85% below channel average - YouTube not showing this video'
                    }
                ],
                'fixes': [
                    {
                        'action': 'Add long-tail keywords to description',
                        'rationale': 'Low impressions = YouTube doesn\'t understand topic relevance',
                        'priority': 'IMMEDIATE'
                    }
                ],
                'learnings': [
                    {
                        'insight': 'Topic keyword "X" has low search demand',
                        'apply_to': 'Future topic selection - verify search volume before committing'
                    }
                ],
                'thresholds_used': {...}
            }

        If inputs are invalid:
            {'error': 'msg'}
    """
    # Validate inputs
    if 'error' in video_metrics:
        return {
            'error': 'Video metrics contain error',
            'details': video_metrics.get('error')
        }

    if 'error' in channel_averages:
        return {
            'error': 'Channel averages contain error',
            'details': channel_averages.get('error')
        }

    # Extract video data
    video_id = video_metrics.get('video_id', 'unknown')
    views = video_metrics.get('views', 0)

    # Get thresholds
    thresholds = get_diagnostic_thresholds(channel_averages)

    # Analyze issues
    issues = []
    fixes = []
    learnings = []

    # Issue 1: Low impressions
    impressions_low_threshold = thresholds['impressions_low']
    impressions_baseline = thresholds['impressions_baseline']

    # Use views as proxy for impressions if actual impressions unavailable
    # (YouTube doesn't provide impressions via API)
    impressions = views

    if impressions < impressions_low_threshold:
        delta_percent = ((impressions - impressions_baseline) / impressions_baseline) * 100

        severity = 'HIGH' if impressions < impressions_low_threshold * 0.5 else 'MEDIUM'

        issues.append({
            'type': 'LOW_IMPRESSIONS',
            'severity': severity,
            'value': impressions,
            'benchmark': int(impressions_baseline),
            'description': f'Views {abs(delta_percent):.0f}% below channel average - YouTube not showing this video'
        })

        # Fixes for low impressions
        fixes.append({
            'action': 'Add long-tail keywords to description',
            'rationale': 'Low impressions = YouTube doesn\'t understand topic relevance',
            'priority': 'IMMEDIATE'
        })

        fixes.append({
            'action': 'Add video to relevant playlists',
            'rationale': 'Increases discoverability through browse features',
            'priority': 'HIGH'
        })

        fixes.append({
            'action': 'Check title for search-friendly keywords',
            'rationale': 'Title should match what people actually search for',
            'priority': 'HIGH'
        })

        # Learnings for low impressions
        learnings.append({
            'insight': 'Topic may have low search demand or high competition',
            'apply_to': 'Future topic selection - verify search volume with keyword tools before committing'
        })

    # Issue 2: Low CTR (if available)
    ctr_issue_detected = False

    if ctr is not None:
        ctr_low_threshold = thresholds['ctr_low']

        if ctr < ctr_low_threshold:
            severity = 'HIGH' if ctr < 2.0 else 'MEDIUM'

            issues.append({
                'type': 'LOW_CTR',
                'severity': severity,
                'value': ctr,
                'benchmark': ctr_low_threshold,
                'description': f'CTR ({ctr}%) below industry baseline ({ctr_low_threshold}%) - title/thumbnail not compelling'
            })

            ctr_issue_detected = True

            # Fixes for low CTR
            fixes.append({
                'action': 'A/B test alternative thumbnails',
                'rationale': 'Low CTR usually means thumbnail doesn\'t stand out or communicate value',
                'priority': 'IMMEDIATE'
            })

            fixes.append({
                'action': 'Test title variants with VidIQ',
                'rationale': 'Title may not communicate payoff clearly enough',
                'priority': 'HIGH'
            })

            # Learnings for low CTR
            learnings.append({
                'insight': 'Current thumbnail style or title formula underperforming',
                'apply_to': 'Future videos - test thumbnail concepts before filming, validate title hooks'
            })

    # Determine primary issue
    has_impression_issue = any(i['type'] == 'LOW_IMPRESSIONS' for i in issues)
    has_ctr_issue = ctr_issue_detected

    if has_impression_issue and has_ctr_issue:
        primary_issue = 'BOTH'
        severity = 'HIGH'
        summary = 'Discovery blocked: low impressions AND low CTR - likely topic selection issue'

        # Additional fix for both issues
        fixes.insert(0, {
            'action': 'Reconsider topic - may not align with audience demand',
            'rationale': 'Both impressions and CTR low suggests topic mismatch',
            'priority': 'CRITICAL'
        })

        learnings.insert(0, {
            'insight': 'Topic failed both discovery phases (impressions + CTR)',
            'apply_to': 'Future topic selection - validate demand AND hook strength before starting research'
        })

    elif has_impression_issue:
        primary_issue = 'LOW_IMPRESSIONS'
        severity = issues[0]['severity'] if issues else 'MEDIUM'
        summary = 'SEO/metadata issue - YouTube not showing video to enough people'

    elif has_ctr_issue:
        primary_issue = 'LOW_CTR'
        severity = issues[0]['severity'] if issues else 'MEDIUM'
        summary = 'Title/thumbnail issue - getting impressions but not clicks'

    else:
        primary_issue = 'NONE'
        severity = 'LOW'
        summary = 'Discovery performing at or above benchmarks'

    return {
        'video_id': video_id,
        'diagnosis': {
            'primary_issue': primary_issue,
            'severity': severity,
            'summary': summary
        },
        'issues': issues,
        'fixes': fixes,
        'learnings': learnings,
        'thresholds_used': thresholds
    }


def format_diagnosis_markdown(diagnosis: Dict[str, Any]) -> str:
    """
    Format diagnosis as markdown for /analyze output.

    Args:
        diagnosis: Result from diagnose_discovery()

    Returns:
        Markdown-formatted string
    """
    if 'error' in diagnosis:
        return f"*Discovery diagnostics unavailable: {diagnosis['error']}*"

    lines = []

    # Header
    lines.append("## Discovery Diagnostics")
    lines.append("")

    # Summary
    diag = diagnosis.get('diagnosis', {})
    primary_issue = diag.get('primary_issue', 'UNKNOWN')
    severity = diag.get('severity', 'UNKNOWN')
    summary = diag.get('summary', 'No diagnosis available')

    lines.append(f"**Diagnosis:** {summary}")
    lines.append(f"**Primary Issue:** {primary_issue} (Severity: {severity})")
    lines.append("")

    # Issues detail
    issues = diagnosis.get('issues', [])
    if issues:
        lines.append("### Issues Detected")
        lines.append("")
        for issue in issues:
            issue_type = issue.get('type', 'UNKNOWN')
            issue_severity = issue.get('severity', 'UNKNOWN')
            description = issue.get('description', '')
            lines.append(f"- **{issue_type}** ({issue_severity}): {description}")
        lines.append("")

    # Fixes
    fixes = diagnosis.get('fixes', [])
    if fixes:
        lines.append("### Recommended Fixes")
        lines.append("")
        for fix in fixes:
            priority = fix.get('priority', 'NORMAL')
            action = fix.get('action', '')
            rationale = fix.get('rationale', '')
            lines.append(f"- [{priority}] {action}")
            lines.append(f"  - *Why:* {rationale}")
        lines.append("")

    # Learnings
    learnings = diagnosis.get('learnings', [])
    if learnings:
        lines.append("### Learnings for Future Videos")
        lines.append("")
        for learn in learnings:
            insight = learn.get('insight', '')
            apply_to = learn.get('apply_to', '')
            lines.append(f"- {insight}")
            lines.append(f"  - *Apply to:* {apply_to}")
        lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    # CLI interface
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python diagnostics.py VIDEO_ID [OPTIONS]")
        print("")
        print("Diagnose discovery issues for a video.")
        print("")
        print("Options:")
        print("  --ctr VALUE     Provide CTR percentage (e.g., --ctr 3.5)")
        print("  --json          Output as JSON (default: human-readable)")
        print("")
        print("Examples:")
        print("  python diagnostics.py wCFReiCGiks")
        print("  python diagnostics.py wCFReiCGiks --ctr 3.5")
        print("  python diagnostics.py wCFReiCGiks --json")
        sys.exit(0)

    # Check dependencies
    if get_video_metrics is None or get_channel_averages is None:
        print("Error: Required dependencies not available")
        print("Ensure youtube-analytics/metrics.py and channel_averages.py are present")
        sys.exit(1)

    # Parse arguments
    video_id = sys.argv[1]
    output_json = '--json' in sys.argv
    manual_ctr = None

    # Parse --ctr argument
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--ctr' and i + 1 < len(args):
            try:
                ctr_value = float(args[i + 1])
                if 0 <= ctr_value <= 100:
                    manual_ctr = ctr_value
                else:
                    print(f"Error: --ctr must be between 0 and 100, got {ctr_value}")
                    sys.exit(1)
            except ValueError:
                print(f"Error: --ctr must be a number, got '{args[i + 1]}'")
                sys.exit(1)

    # Fetch video metrics
    print(f"Fetching metrics for video: {video_id}...", file=sys.stderr)
    video_metrics = get_video_metrics(video_id)

    if 'error' in video_metrics:
        print(f"Error fetching video metrics: {video_metrics['error']}")
        sys.exit(1)

    # Fetch channel averages
    print("Fetching channel averages...", file=sys.stderr)
    channel_averages = get_channel_averages()

    if 'error' in channel_averages:
        print(f"Error fetching channel averages: {channel_averages['error']}")
        sys.exit(1)

    # Run diagnosis
    diagnosis = diagnose_discovery(video_metrics, channel_averages, ctr=manual_ctr)

    # Output
    if output_json:
        print(json.dumps(diagnosis, indent=2))
    else:
        print(format_diagnosis_markdown(diagnosis))
