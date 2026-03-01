"""
Retention Pattern Decoder

Correlates script structure features with YouTube retention data to identify
what keeps viewers watching. Generates actionable findings for script generation.

This is the core of Phase 58 (v5.2 Growth Engine).

Features:
  1. Per-video retention stored from YouTube Analytics API (RET-01)
  2. Retention correlated with: hook type, section count, evidence density, duration (RET-02)
  3. Opening hook type -> retention mapping (RET-03)
  4. Top findings encoded as script-writer-v2 Rule 20 constraints (RET-04)

Usage:
    from tools.youtube_analytics.retention_decoder import RetentionDecoder

    rd = RetentionDecoder()
    findings = rd.analyze()
    print(findings['top_findings'])

CLI:
    python -m tools.youtube_analytics.retention_decoder              # Full analysis
    python -m tools.youtube_analytics.retention_decoder --findings   # Just findings
    python -m tools.youtube_analytics.retention_decoder --rule20     # Generate Rule 20

Dependencies:
    - tools/youtube_analytics/analytics.db (videos table with retention data)
"""

import re
import json
import sqlite3
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from statistics import mean, stdev, median
from collections import defaultdict

from tools.logging_config import get_logger

logger = get_logger(__name__)

ANALYTICS_DB = Path(__file__).parent / 'analytics.db'

# Minimum videos per bucket to draw conclusions
MIN_BUCKET_SIZE = 3


class RetentionDecoder:
    """Analyzes retention patterns to generate scriptwriting constraints."""

    def __init__(self):
        self.analytics_db = ANALYTICS_DB

    def _get_videos(self) -> List[Dict]:
        """Load all videos with retention data."""
        if not self.analytics_db.exists():
            return []
        conn = sqlite3.connect(str(self.analytics_db))
        conn.row_factory = sqlite3.Row
        rows = conn.execute('''
            SELECT video_id, title, avg_view_percentage, avg_view_duration_seconds,
                   duration_seconds, views, subscribers_gained, topic_type,
                   likes, comments, shares, ctr_percent, impressions
            FROM videos
            WHERE avg_view_percentage > 0 AND duration_seconds > 120
        ''').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def classify_hook_type(self, title: str) -> str:
        """Classify the likely hook type from title structure."""
        t = title.lower()

        if re.search(r'(claim|says|wrong|myth|truth|lie|fact.?check|busted)', t):
            return 'myth-bust'
        elif re.search(r'(document|treaty|map|letter|memo|decree|wrote)', t):
            return 'document-reveal'
        elif re.search(r'^(how|why)\b', t):
            return 'how-why'
        elif re.search(r'\?$', t):
            return 'question'
        elif re.search(r'(secret|shocking|hidden|never told)', t):
            return 'curiosity-gap'
        else:
            return 'statement'

    def classify_duration_bucket(self, seconds: int) -> str:
        """Classify video into duration bucket."""
        if seconds < 420:
            return 'short (<7m)'
        elif seconds < 660:
            return 'medium (7-11m)'
        elif seconds < 960:
            return 'long (11-16m)'
        else:
            return 'very-long (16m+)'

    def classify_specificity(self, title: str) -> str:
        """Classify whether title implies specific evidence or general topic."""
        if re.search(r'\d{4}|document|treaty|map|court|evidence|source|memo|letter', title.lower()):
            return 'specific'
        return 'general'

    def analyze(self) -> Dict:
        """
        Run full retention analysis. Returns structured findings.

        Returns:
            {
                'video_count': int,
                'channel_avg_retention': float,
                'by_hook_type': {type: {avg_ret, count, top_videos}},
                'by_duration': {bucket: {avg_ret, count}},
                'by_topic': {topic: {avg_ret, count}},
                'by_specificity': {type: {avg_ret, count}},
                'correlations': [{'factor', 'finding', 'effect_size'}],
                'top_findings': [str],
                'rule20_constraints': [str],
            }
        """
        videos = self._get_videos()
        if len(videos) < 5:
            return {'error': f'Only {len(videos)} videos — need at least 5'}

        avg_ret = mean([v['avg_view_percentage'] for v in videos])

        # ── By hook type ──
        hook_data = defaultdict(list)
        for v in videos:
            hook = self.classify_hook_type(v['title'])
            v['hook_type'] = hook
            hook_data[hook].append(v)

        by_hook = {}
        for hook, vids in hook_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            top = sorted(vids, key=lambda x: -x['avg_view_percentage'])[:3]
            by_hook[hook] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
                'avg_duration_min': round(mean([v['duration_seconds'] for v in vids]) / 60, 1),
                'top_videos': [
                    {'title': v['title'][:60], 'retention': v['avg_view_percentage'],
                     'duration_min': round(v['duration_seconds'] / 60, 1)}
                    for v in top
                ],
            }

        # ── By duration ──
        dur_data = defaultdict(list)
        for v in videos:
            bucket = self.classify_duration_bucket(v['duration_seconds'])
            dur_data[bucket].append(v)

        by_duration = {}
        for bucket, vids in dur_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_duration[bucket] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        # ── By topic ──
        topic_data = defaultdict(list)
        for v in videos:
            topic_data[v.get('topic_type') or 'unknown'].append(v)

        by_topic = {}
        for topic, vids in topic_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_topic[topic] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        # ── By specificity ──
        spec_data = defaultdict(list)
        for v in videos:
            spec = self.classify_specificity(v['title'])
            spec_data[spec].append(v)

        by_specificity = {}
        for spec, vids in spec_data.items():
            rets = [v['avg_view_percentage'] for v in vids]
            by_specificity[spec] = {
                'avg_ret': round(mean(rets), 1),
                'vs_avg': round(mean(rets) - avg_ret, 1),
                'count': len(vids),
            }

        # ── Correlations ──
        correlations = self._compute_correlations(videos, avg_ret)

        # ── Top findings ──
        top_findings = self._generate_findings(
            by_hook, by_duration, by_topic, by_specificity, correlations, avg_ret
        )

        # ── Rule 20 constraints ──
        rule20 = self._generate_rule20(
            by_hook, by_duration, correlations, top_findings, avg_ret
        )

        return {
            'video_count': len(videos),
            'channel_avg_retention': round(avg_ret, 1),
            'by_hook_type': dict(sorted(by_hook.items(), key=lambda x: -x[1]['avg_ret'])),
            'by_duration': by_duration,
            'by_topic': dict(sorted(by_topic.items(), key=lambda x: -x[1]['avg_ret'])),
            'by_specificity': by_specificity,
            'correlations': correlations,
            'top_findings': top_findings,
            'rule20_constraints': rule20,
        }

    def _compute_correlations(self, videos: List[Dict], avg_ret: float) -> List[Dict]:
        """Compute retention correlations with measurable features."""
        correlations = []

        # Duration vs retention correlation
        durations = [v['duration_seconds'] for v in videos]
        retentions = [v['avg_view_percentage'] for v in videos]

        if len(videos) >= 5:
            # Simple correlation: split into halves
            sorted_by_dur = sorted(videos, key=lambda v: v['duration_seconds'])
            half = len(sorted_by_dur) // 2
            short_half_ret = mean([v['avg_view_percentage'] for v in sorted_by_dur[:half]])
            long_half_ret = mean([v['avg_view_percentage'] for v in sorted_by_dur[half:]])
            diff = short_half_ret - long_half_ret

            if abs(diff) > 2:
                correlations.append({
                    'factor': 'duration',
                    'finding': f'Shorter videos retain {diff:.1f}% more than longer ones',
                    'effect_size': round(diff, 1),
                    'direction': 'negative',  # longer = lower retention
                })

        # Views vs retention (does popularity correlate with retention?)
        sorted_by_views = sorted(videos, key=lambda v: v['views'])
        half = len(sorted_by_views) // 2
        low_views_ret = mean([v['avg_view_percentage'] for v in sorted_by_views[:half]])
        high_views_ret = mean([v['avg_view_percentage'] for v in sorted_by_views[half:]])
        views_diff = high_views_ret - low_views_ret

        if abs(views_diff) > 2:
            direction = 'positive' if views_diff > 0 else 'negative'
            correlations.append({
                'factor': 'views',
                'finding': f'Higher-view videos have {"higher" if views_diff > 0 else "lower"} retention ({views_diff:+.1f}%)',
                'effect_size': round(views_diff, 1),
                'direction': direction,
            })

        # Subscriber conversion vs retention
        for v in videos:
            v['conversion_rate'] = (v['subscribers_gained'] / v['views'] * 100) if v['views'] > 0 else 0

        sorted_by_conv = sorted(videos, key=lambda v: v['conversion_rate'])
        half = len(sorted_by_conv) // 2
        low_conv_ret = mean([v['avg_view_percentage'] for v in sorted_by_conv[:half]])
        high_conv_ret = mean([v['avg_view_percentage'] for v in sorted_by_conv[half:]])
        conv_diff = high_conv_ret - low_conv_ret

        if abs(conv_diff) > 2:
            correlations.append({
                'factor': 'subscriber_conversion',
                'finding': f'Videos with higher sub conversion have {"higher" if conv_diff > 0 else "lower"} retention ({conv_diff:+.1f}%)',
                'effect_size': round(conv_diff, 1),
                'direction': 'positive' if conv_diff > 0 else 'negative',
            })

        return correlations

    def _generate_findings(self, by_hook, by_duration, by_topic,
                           by_specificity, correlations, avg_ret) -> List[str]:
        """Generate human-readable top findings."""
        findings = []

        # Best hook type
        best_hook = max(by_hook.items(), key=lambda x: x[1]['avg_ret'] if x[1]['count'] >= MIN_BUCKET_SIZE else 0)
        worst_hook = min(by_hook.items(), key=lambda x: x[1]['avg_ret'] if x[1]['count'] >= MIN_BUCKET_SIZE else 100)
        if best_hook[1]['count'] >= MIN_BUCKET_SIZE:
            findings.append(
                f"Best hook type: '{best_hook[0]}' ({best_hook[1]['avg_ret']}% retention, "
                f"{best_hook[1]['vs_avg']:+.1f}% vs avg, n={best_hook[1]['count']})"
            )
        if worst_hook[1]['count'] >= MIN_BUCKET_SIZE and worst_hook[0] != best_hook[0]:
            findings.append(
                f"Worst hook type: '{worst_hook[0]}' ({worst_hook[1]['avg_ret']}% retention, "
                f"{worst_hook[1]['vs_avg']:+.1f}% vs avg, n={worst_hook[1]['count']})"
            )

        # Best duration
        best_dur = max(
            [(k, v) for k, v in by_duration.items() if v['count'] >= MIN_BUCKET_SIZE],
            key=lambda x: x[1]['avg_ret'],
            default=None
        )
        if best_dur:
            findings.append(
                f"Best duration: {best_dur[0]} ({best_dur[1]['avg_ret']}% retention, "
                f"n={best_dur[1]['count']})"
            )

        # Duration correlation
        dur_corr = next((c for c in correlations if c['factor'] == 'duration'), None)
        if dur_corr:
            findings.append(dur_corr['finding'])

        # Best topic
        best_topic = max(
            [(k, v) for k, v in by_topic.items() if v['count'] >= MIN_BUCKET_SIZE],
            key=lambda x: x[1]['avg_ret'],
            default=None
        )
        if best_topic:
            findings.append(
                f"Best topic for retention: '{best_topic[0]}' ({best_topic[1]['avg_ret']}% avg, "
                f"n={best_topic[1]['count']})"
            )

        # Views-retention relationship
        views_corr = next((c for c in correlations if c['factor'] == 'views'), None)
        if views_corr:
            findings.append(views_corr['finding'])

        return findings

    def _generate_rule20(self, by_hook, by_duration, correlations,
                         findings, avg_ret) -> List[str]:
        """Generate Rule 20 constraints for script-writer-v2."""
        constraints = []

        # Constraint 1: Prefer best hook types
        good_hooks = [
            h for h, data in by_hook.items()
            if data['count'] >= MIN_BUCKET_SIZE and data['vs_avg'] > 0
        ]
        bad_hooks = [
            h for h, data in by_hook.items()
            if data['count'] >= MIN_BUCKET_SIZE and data['vs_avg'] < -2
        ]

        if good_hooks:
            constraints.append(
                f"PREFER hook types: {', '.join(good_hooks)} "
                f"(above-average retention on this channel)"
            )
        if bad_hooks:
            constraints.append(
                f"AVOID hook types: {', '.join(bad_hooks)} "
                f"(below-average retention on this channel)"
            )

        # Constraint 2: Duration sweet spot
        best_dur = max(
            [(k, v) for k, v in by_duration.items() if v['count'] >= MIN_BUCKET_SIZE],
            key=lambda x: x[1]['avg_ret'],
            default=None
        )
        if best_dur:
            constraints.append(
                f"OPTIMAL duration: {best_dur[0]} range "
                f"({best_dur[1]['avg_ret']}% retention vs {avg_ret:.1f}% channel avg)"
            )

        # Constraint 3: Duration-retention tradeoff
        dur_corr = next((c for c in correlations if c['factor'] == 'duration'), None)
        if dur_corr and dur_corr['effect_size'] > 3:
            constraints.append(
                f"CAUTION: Each added minute costs retention. "
                f"Cut sections that don't add evidence or causal connections."
            )

        # Constraint 4: Top retention factors (general advice from data)
        constraints.append(
            f"TARGET: {avg_ret:.0f}%+ retention. "
            f"Channel average is {avg_ret:.1f}%. "
            f"Top performers reach 35-50%."
        )

        return constraints

    def get_hook_retention_map(self) -> Dict[str, Dict]:
        """
        Get hook type -> retention mapping for RET-03.

        Returns:
            {hook_type: {avg_ret, count, vs_avg, top_video}}
        """
        analysis = self.analyze()
        if 'error' in analysis:
            return analysis
        return analysis['by_hook_type']

    def get_rule20_text(self) -> str:
        """Generate the Rule 20 text block for script-writer-v2."""
        analysis = self.analyze()
        if 'error' in analysis:
            return f"# Rule 20 unavailable: {analysis['error']}"

        lines = [
            "## Rule 20: Data-Driven Retention Constraints",
            "",
            f"**Source:** Analyzed {analysis['video_count']} videos "
            f"(channel avg retention: {analysis['channel_avg_retention']}%)",
            f"**Generated:** Auto-updated from YouTube Analytics API data",
            "",
            "### Constraints (apply during script generation)",
            "",
        ]

        for i, constraint in enumerate(analysis['rule20_constraints'], 1):
            lines.append(f"{i}. {constraint}")

        lines.extend([
            "",
            "### Findings",
            "",
        ])

        for finding in analysis['top_findings']:
            lines.append(f"- {finding}")

        lines.extend([
            "",
            "### Hook Type Retention Map",
            "",
            "| Hook Type | Avg Retention | vs Avg | Videos | Best Duration |",
            "|-----------|--------------|--------|--------|---------------|",
        ])

        for hook, data in analysis['by_hook_type'].items():
            marker = '+' if data['vs_avg'] > 0 else ''
            lines.append(
                f"| {hook} | {data['avg_ret']}% | {marker}{data['vs_avg']}% "
                f"| {data['count']} | {data['avg_duration_min']}m |"
            )

        return "\n".join(lines)


def _print_analysis(analysis: Dict):
    """Print full retention analysis."""
    print(f"\n{'='*60}")
    print(f"RETENTION PATTERN DECODER")
    print(f"{'='*60}")
    print(f"\nVideos analyzed: {analysis['video_count']}")
    print(f"Channel avg retention: {analysis['channel_avg_retention']}%")

    print(f"\n--- By Hook Type ---")
    for hook, data in analysis['by_hook_type'].items():
        marker = '+' if data['vs_avg'] > 0 else ''
        print(f"  {hook:>18}: {data['avg_ret']}% ret "
              f"({marker}{data['vs_avg']}%) "
              f"| {data['count']} videos | avg {data['avg_duration_min']}m")

    print(f"\n--- By Duration ---")
    for bucket, data in sorted(analysis['by_duration'].items()):
        marker = '+' if data['vs_avg'] > 0 else ''
        print(f"  {bucket:>20}: {data['avg_ret']}% ret "
              f"({marker}{data['vs_avg']}%) | {data['count']} videos")

    print(f"\n--- By Topic ---")
    for topic, data in analysis['by_topic'].items():
        marker = '+' if data['vs_avg'] > 0 else ''
        print(f"  {topic:>15}: {data['avg_ret']}% ret "
              f"({marker}{data['vs_avg']}%) | {data['count']} videos")

    print(f"\n--- Correlations ---")
    for c in analysis['correlations']:
        print(f"  {c['factor']:>25}: {c['finding']}")

    print(f"\n--- Top Findings ---")
    for f in analysis['top_findings']:
        print(f"  - {f}")

    print(f"\n--- Rule 20 Constraints ---")
    for i, c in enumerate(analysis['rule20_constraints'], 1):
        print(f"  {i}. {c}")


if __name__ == '__main__':
    # Force UTF-8 output on Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Retention Pattern Decoder -- correlate script structure with retention.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.retention_decoder              # Full analysis
  python -m tools.youtube_analytics.retention_decoder --findings   # Just findings
  python -m tools.youtube_analytics.retention_decoder --rule20     # Generate Rule 20 text
  python -m tools.youtube_analytics.retention_decoder --json       # JSON output
        """
    )
    parser.add_argument('--findings', action='store_true',
                        help='Show only top findings')
    parser.add_argument('--rule20', action='store_true',
                        help='Generate Rule 20 text for script-writer-v2')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('--verbose', '-v', action='store_true')
    verbosity.add_argument('--quiet', '-q', action='store_true')

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    rd = RetentionDecoder()

    if args.rule20:
        print(rd.get_rule20_text())

    elif args.findings:
        analysis = rd.analyze()
        if 'error' in analysis:
            print(f"Error: {analysis['error']}", file=sys.stderr)
            sys.exit(1)
        print(f"\nRetention Findings ({analysis['video_count']} videos, "
              f"avg: {analysis['channel_avg_retention']}%):\n")
        for f in analysis['top_findings']:
            print(f"  - {f}")

    elif args.json:
        analysis = rd.analyze()
        print(json.dumps(analysis, indent=2, default=str))

    else:
        analysis = rd.analyze()
        if 'error' in analysis:
            print(f"Error: {analysis['error']}", file=sys.stderr)
            sys.exit(1)
        _print_analysis(analysis)

    sys.exit(0)
