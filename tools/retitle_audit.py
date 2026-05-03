"""
Retitle Audit — surfaces videos losing views to bad packaging.

Reads POST-PUBLISH-ANALYSIS files and CROSS-VIDEO-SYNTHESIS data,
calculates "wasted impressions" for each video, and outputs a
prioritized retitle/rethumb list.

Wasted impressions = impressions × (target_CTR - actual_CTR)
This estimates how many extra clicks you'd get if the title/thumb
performed at your target CTR.

Usage:
    python -m tools.retitle_audit                 # Full audit
    python -m tools.retitle_audit --top 5         # Top 5 only
    python -m tools.retitle_audit --min-impressions 1000  # Filter low-impression videos
    python -m tools.retitle_audit --save          # Save report to channel-data/

"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

# Target CTR — videos performing above this don't need retitling
TARGET_CTR = 3.5  # percent — based on top performer average (excluding JD Vance outlier)

# Title patterns that trigger hard-reject per PACKAGING_MANDATE
YEAR_RE = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')
COLON_RE = re.compile(r':')
THE_X_THAT_RE = re.compile(r'^the\s+(?:\w+\s+){0,2}\w+\s+that\s+', re.I)
CLICKBAIT_RE = re.compile(r'SHOCKING|TRUTH|EXPOSED|REVEALED|SECRET', re.I)


def _parse_synthesis_table(synthesis_path: Path) -> List[Dict]:
    """Parse the master performance table from CROSS-VIDEO-SYNTHESIS.md."""
    text = synthesis_path.read_text(encoding='utf-8')
    videos = []

    # Find the table after "## Master Performance Table"
    in_table = False
    header_seen = False
    for line in text.splitlines():
        if '## Master Performance Table' in line:
            in_table = True
            continue
        if in_table and line.startswith('|') and '---' in line:
            header_seen = True
            continue
        if in_table and header_seen and line.startswith('|'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 8:
                title = cols[1]
                try:
                    views = int(cols[2].replace(',', ''))
                except (ValueError, IndexError):
                    views = 0

                # Parse retention
                ret_str = cols[3].replace('%', '').strip()
                try:
                    retention = float(ret_str) if ret_str and ret_str != 'TBD' and ret_str != 'n/a' else None
                except ValueError:
                    retention = None

                # Parse CTR
                ctr_str = cols[4].replace('%', '').strip()
                try:
                    ctr = float(ctr_str) if ctr_str and ctr_str != 'TBD' and ctr_str != 'n/a' else None
                except ValueError:
                    ctr = None

                # Parse impressions
                imp_str = cols[5].replace(',', '').strip()
                try:
                    impressions = int(imp_str) if imp_str and imp_str != 'TBD' and imp_str != 'n/a' else None
                except ValueError:
                    impressions = None

                # Parse subs
                subs_str = cols[6].replace('+', '').strip()
                try:
                    subs = int(subs_str) if subs_str and subs_str != 'TBD' and subs_str != 'n/a' else None
                except ValueError:
                    subs = None

                topic_type = cols[7] if len(cols) > 7 else ''

                videos.append({
                    'title': title,
                    'views': views,
                    'retention': retention,
                    'ctr': ctr,
                    'impressions': impressions,
                    'subs': subs,
                    'topic_type': topic_type,
                })
        elif in_table and header_seen and not line.startswith('|'):
            break  # End of table

    return videos


def _detect_title_issues(title: str) -> List[str]:
    """Detect PACKAGING_MANDATE violations in a title."""
    issues = []
    if YEAR_RE.search(title):
        issues.append('YEAR in title (-46% CTR)')
    if COLON_RE.search(title):
        issues.append('COLON in title (-28% CTR)')
    if THE_X_THAT_RE.search(title):
        issues.append('"The X That Y" pattern (worst performer)')
    if CLICKBAIT_RE.search(title):
        issues.append('Clickbait caps (violates channel DNA)')
    if title.strip().endswith('?'):
        issues.append('Question pattern (-36% CTR, n=3)')
    return issues


def _calc_wasted_impressions(impressions: int, actual_ctr: float, target_ctr: float) -> int:
    """Calculate how many additional clicks target CTR would deliver."""
    actual_clicks = impressions * (actual_ctr / 100)
    target_clicks = impressions * (target_ctr / 100)
    return max(0, int(target_clicks - actual_clicks))


def audit(min_impressions: int = 0, top_n: int = 0) -> List[Dict]:
    """Run the retitle audit.

    Returns list of videos sorted by wasted impressions (desc).
    """
    synthesis_path = Path('channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md')
    if not synthesis_path.exists():
        print("ERROR: CROSS-VIDEO-SYNTHESIS.md not found. Run /patterns first.")
        return []

    videos = _parse_synthesis_table(synthesis_path)

    results = []
    for v in videos:
        # Skip videos without CTR/impression data
        if v['ctr'] is None or v['impressions'] is None:
            continue

        # Skip videos already above target
        if v['ctr'] >= TARGET_CTR:
            continue

        # Apply impression filter
        if v['impressions'] < min_impressions:
            continue

        title_issues = _detect_title_issues(v['title'])
        wasted = _calc_wasted_impressions(v['impressions'], v['ctr'], TARGET_CTR)

        diagnosis = 'BAD PACKAGING'
        if v['impressions'] < 500:
            diagnosis = 'LOW DEMAND'
        elif v['ctr'] < 2.0:
            diagnosis = 'BAD PACKAGING — SWAP TITLE + THUMBNAIL'
        elif v['ctr'] < TARGET_CTR:
            diagnosis = 'MEDIOCRE PACKAGING — SWAP TITLE'

        results.append({
            **v,
            'title_issues': title_issues,
            'wasted_impressions': wasted,
            'wasted_views': wasted,  # At current retention, these clicks ≈ views
            'diagnosis': diagnosis,
        })

    # Sort by wasted impressions (most wasted first)
    results.sort(key=lambda x: -x['wasted_impressions'])

    if top_n > 0:
        results = results[:top_n]

    return results


def format_report(results: List[Dict]) -> str:
    """Format audit results as readable report."""
    lines = []
    lines.append('')
    lines.append('=' * 70)
    lines.append('  RETITLE AUDIT — Wasted Impressions Report')
    lines.append('=' * 70)
    lines.append(f'  Target CTR: {TARGET_CTR}%')
    lines.append(f'  Videos below target: {len(results)}')

    total_wasted = sum(r['wasted_impressions'] for r in results)
    lines.append(f'  Total wasted clicks: {total_wasted:,}')
    lines.append('')

    for i, r in enumerate(results, 1):
        lines.append(f'  #{i} {r["title"]}')
        lines.append(f'     Views: {r["views"]:,} | CTR: {r["ctr"]:.2f}% | Impressions: {r["impressions"]:,}')
        lines.append(f'     Retention: {r["retention"]:.1f}%' if r['retention'] else '     Retention: n/a')
        lines.append(f'     Wasted clicks at {TARGET_CTR}% CTR: +{r["wasted_impressions"]:,}')
        lines.append(f'     Diagnosis: {r["diagnosis"]}')

        if r['title_issues']:
            for issue in r['title_issues']:
                lines.append(f'     VIOLATION: {issue}')

        # Actionability hint
        if r['retention'] and r['retention'] >= 35:
            lines.append(f'     HIGH PRIORITY — strong retention ({r["retention"]:.1f}%), content is good, packaging is the bottleneck')
        elif r['impressions'] >= 3000:
            lines.append(f'     HIGH PRIORITY — YouTube gave {r["impressions"]:,} impressions, title/thumb failed to convert')

        lines.append('')

    lines.append('-' * 70)
    lines.append(f'  If all {len(results)} videos hit {TARGET_CTR}% CTR: +{total_wasted:,} additional clicks')
    lines.append('')

    return '\n'.join(lines)


def save_report(report: str) -> Path:
    """Save report to channel-data/."""
    out = Path('channel-data/RETITLE-AUDIT-REPORT.md')
    out.write_text(f'# Retitle Audit Report\n\n```\n{report}\n```\n', encoding='utf-8')
    return out


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Retitle audit — find videos losing views to bad packaging')
    parser.add_argument('--top', type=int, default=0, help='Show top N only')
    parser.add_argument('--min-impressions', type=int, default=0, help='Min impressions to include')
    parser.add_argument('--save', action='store_true', help='Save report to channel-data/')
    args = parser.parse_args()

    results = audit(min_impressions=args.min_impressions, top_n=args.top)

    if not results:
        print('No videos found below target CTR. All packaging looks good.')
        return

    report = format_report(results)
    print(report)

    if args.save:
        path = save_report(report)
        print(f'Report saved to {path}')


if __name__ == '__main__':
    main()
