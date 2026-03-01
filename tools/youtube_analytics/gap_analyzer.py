"""
Competitor Gap Analyzer

Identifies topic-angle combinations where competitors are absent and demand exists.
Cross-references 870+ competitor videos with own-channel coverage to find white space.

This is the core of Phase 57 (v5.2 Growth Engine).

Features:
  1. Classify competitor videos by topic AND angle (document-first, narrative, legal, explainer)
  2. Cross-reference with own videos to identify uncovered combinations
  3. Score gaps by: demand signal × competitor absence × channel competitive advantage
  4. Surface top gaps with reasoning for /next integration

Usage:
    from tools.youtube_analytics.gap_analyzer import GapAnalyzer

    ga = GapAnalyzer()
    gaps = ga.find_gaps()
    for g in gaps[:5]:
        print(f"{g['topic']} from {g['angle']} — score: {g['gap_score']}")

CLI:
    python -m tools.youtube_analytics.gap_analyzer              # Show top gaps
    python -m tools.youtube_analytics.gap_analyzer --map        # Full coverage map
    python -m tools.youtube_analytics.gap_analyzer --classify   # Re-classify competitor angles

Dependencies:
    - tools/intel/intel.db (competitor_videos table, 870+ rows)
    - tools/youtube_analytics/analytics.db (own videos)
    - tools/discovery/keywords.db (search demand data)
"""

import re
import json
import sqlite3
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from tools.logging_config import get_logger

logger = get_logger(__name__)

INTEL_DB = Path(__file__).parent.parent / 'intel' / 'intel.db'
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
KEYWORDS_DB = Path(__file__).parent.parent / 'discovery' / 'keywords.db'

# ── Angle classification rules ──────────────────────────────────────
# Each video can have multiple angles. These patterns match title + description.

ANGLE_RULES = {
    'document-first': {
        'title_patterns': [
            r'document', r'letter', r'treaty', r'decree', r'charter',
            r'manuscript', r'source', r'archive', r'primary',
            r'wrote', r'signed', r'original text', r'constitution',
            r'memo', r'telegram', r'dispatch', r'proclamation',
            r'declassified', r'secret file', r'evidence',
        ],
        'description': 'Uses primary documents as core evidence',
    },
    'narrative': {
        'title_patterns': [
            r'story of', r'rise and fall', r'how .+ became',
            r'history of', r'fall of', r'age of', r'empire of',
            r'journey', r'saga', r'epic', r'tale of',
            r'what happened', r'the .+ that changed',
        ],
        'description': 'Chronological storytelling without document focus',
    },
    'legal': {
        'title_patterns': [
            r'legal', r'law', r'court', r'ruling', r'treaty',
            r'constitution', r'sovereignty', r'jurisdiction',
            r'icj', r'international law', r'dispute',
            r'border', r'claim', r'recognition', r'legitimate',
        ],
        'description': 'Focuses on legal frameworks, court rulings, treaties',
    },
    'explainer': {
        'title_patterns': [
            r'explain', r'why .+ (is|are|was|were|can\'t|won\'t)',
            r'how .+ work', r'what (is|are|was|were)',
            r'understand', r'guide to', r'introduction',
            r'in \d+ minutes', r'everything you need',
        ],
        'description': 'Educational explainer format',
    },
    'fact-check': {
        'title_patterns': [
            r'fact.?check', r'debunk', r'myth', r'wrong about',
            r'actually', r'truth about', r'lie', r'false',
            r'misinformation', r'propaganda', r'claim',
        ],
        'description': 'Explicitly challenges claims or myths',
    },
    'geographic': {
        'title_patterns': [
            r'map', r'border', r'territory', r'island',
            r'region', r'land', r'country', r'nation',
            r'peninsula', r'strait', r'sea', r'ocean',
        ],
        'description': 'Centered on geographic/territorial concepts',
    },
}

# ── Topic normalization ─────────────────────────────────────────────
# Normalize the JSON array topic_cluster from intel.db to simple categories

TOPIC_NORMALIZE = {
    'territorial': 'territorial',
    'ideological': 'ideological',
    'colonial': 'colonial',
    'war': 'war',
    'legal': 'legal',
    'archaeological': 'archaeological',
    'medieval': 'medieval',
    'religion': 'religion',
    'trade': 'trade',
    'revolution': 'revolution',
    'politician': 'politician',
    'general': 'general',
}

# Channel's competitive advantages (for scoring)
CHANNEL_ADVANTAGES = {
    'document-first': 1.5,   # Core differentiator: primary sources on screen
    'legal': 1.3,            # Treaty/court analysis is channel strength
    'fact-check': 1.2,       # Myth-busting is channel identity
    'geographic': 1.1,       # Map-focused content performs well
    'narrative': 0.8,        # Not the channel's primary approach
    'explainer': 0.9,        # Can do but not distinctive
}


class GapAnalyzer:
    """Analyzes competitor coverage to find white-space opportunities."""

    def __init__(self):
        self.intel_db = INTEL_DB
        self.analytics_db = ANALYTICS_DB
        self.keywords_db = KEYWORDS_DB

    def _get_competitor_videos(self) -> List[Dict]:
        """Load all competitor videos from intel.db."""
        if not self.intel_db.exists():
            return []
        conn = sqlite3.connect(str(self.intel_db))
        conn.row_factory = sqlite3.Row
        rows = conn.execute('''
            SELECT cv.video_id, cv.title, cv.views, cv.duration_seconds,
                   cv.topic_cluster, cv.is_outlier, cv.outlier_ratio,
                   cv.description, cc.channel_name
            FROM competitor_videos cv
            JOIN competitor_channels cc ON cv.channel_id = cc.channel_id
            WHERE cc.track_active = 1
        ''').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _get_own_videos(self) -> List[Dict]:
        """Load own videos from analytics.db."""
        if not self.analytics_db.exists():
            return []
        conn = sqlite3.connect(str(self.analytics_db))
        conn.row_factory = sqlite3.Row
        rows = conn.execute('''
            SELECT video_id, title, views, topic_type, angles
            FROM videos
        ''').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _get_search_demand(self) -> Dict[str, int]:
        """Load search volume data from keywords.db."""
        if not self.keywords_db.exists():
            return {}
        conn = sqlite3.connect(str(self.keywords_db))
        try:
            rows = conn.execute('''
                SELECT keyword, search_volume FROM keywords
                WHERE search_volume IS NOT NULL AND search_volume > 0
            ''').fetchall()
            conn.close()
            return {r[0]: r[1] for r in rows}
        except Exception:
            conn.close()
            return {}

    def classify_angle(self, title: str, description: str = '') -> List[str]:
        """Classify a video's angle based on title and description."""
        text = f"{title} {description}".lower()
        angles = []
        for angle, rules in ANGLE_RULES.items():
            for pattern in rules['title_patterns']:
                if re.search(pattern, text):
                    angles.append(angle)
                    break
        if not angles:
            angles = ['narrative']  # Default
        return angles

    def normalize_topics(self, topic_cluster_json: str) -> List[str]:
        """Normalize topic_cluster JSON from intel.db to simple list."""
        try:
            topics = json.loads(topic_cluster_json)
            if isinstance(topics, list):
                return [t for t in topics if t in TOPIC_NORMALIZE]
        except (json.JSONDecodeError, TypeError):
            pass
        return ['general']

    def classify_all_competitors(self) -> List[Dict]:
        """Classify all competitor videos by topic and angle."""
        videos = self._get_competitor_videos()
        for v in videos:
            v['topics'] = self.normalize_topics(v.get('topic_cluster', '[]'))
            v['angles'] = self.classify_angle(
                v.get('title', ''),
                v.get('description', '')
            )
        return videos

    def build_coverage_map(self) -> Dict[str, Dict[str, Dict]]:
        """
        Build a topic × angle coverage map.

        Returns:
            {topic: {angle: {
                'competitor_count': int,
                'competitor_views': int,
                'competitor_channels': set,
                'own_count': int,
                'own_views': int,
                'outlier_count': int,
            }}}
        """
        competitors = self.classify_all_competitors()
        own_videos = self._get_own_videos()

        coverage = defaultdict(lambda: defaultdict(lambda: {
            'competitor_count': 0,
            'competitor_views': 0,
            'competitor_channels': set(),
            'own_count': 0,
            'own_views': 0,
            'outlier_count': 0,
        }))

        # Map competitor coverage
        for v in competitors:
            for topic in v['topics']:
                for angle in v['angles']:
                    cell = coverage[topic][angle]
                    cell['competitor_count'] += 1
                    cell['competitor_views'] += v.get('views', 0) or 0
                    cell['competitor_channels'].add(v.get('channel_name', ''))
                    if v.get('is_outlier'):
                        cell['outlier_count'] += 1

        # Map own coverage
        for v in own_videos:
            topic = v.get('topic_type', 'general')
            own_angles = self.classify_angle(v.get('title', ''))
            for angle in own_angles:
                cell = coverage[topic][angle]
                cell['own_count'] += 1
                cell['own_views'] += v.get('views', 0) or 0

        return coverage

    def find_gaps(self, min_demand: int = 0) -> List[Dict]:
        """
        Find topic-angle gaps where competitors exist but channel doesn't,
        or where demand exists but nobody covers it well.

        Returns sorted list of gap opportunities.
        """
        coverage = self.build_coverage_map()
        search_demand = self._get_search_demand()
        gaps = []

        all_topics = set(coverage.keys())
        all_angles = set()
        for topic_angles in coverage.values():
            all_angles.update(topic_angles.keys())

        for topic in all_topics:
            # Find demand signal for this topic from keywords
            topic_demand = 0
            for kw, vol in search_demand.items():
                if topic.lower() in kw.lower():
                    topic_demand = max(topic_demand, vol)

            for angle in all_angles:
                cell = coverage[topic].get(angle, {
                    'competitor_count': 0,
                    'competitor_views': 0,
                    'competitor_channels': set(),
                    'own_count': 0,
                    'own_views': 0,
                    'outlier_count': 0,
                })

                comp_count = cell['competitor_count']
                own_count = cell['own_count']
                comp_views = cell['competitor_views']
                outlier_count = cell['outlier_count']
                channels = cell.get('competitor_channels', set())

                # Skip if we already cover this well
                if own_count >= 3:
                    continue

                # Skip general/narrative (too broad to be actionable)
                if topic == 'general' and angle == 'narrative':
                    continue

                # Calculate gap score components
                # 1. Demand signal (0-40 points)
                demand_score = min(40, (topic_demand / 500) * 10) if topic_demand > 0 else 5

                # 2. Competitor absence (0-30 points)
                # More points if competitors exist (proven demand) but channel is absent
                if comp_count == 0 and own_count == 0:
                    absence_score = 5  # Unknown territory
                elif comp_count > 0 and own_count == 0:
                    # Proven demand, we're missing out
                    absence_score = min(30, 10 + comp_count * 2)
                elif comp_count > 0 and own_count > 0 and own_count < comp_count // 3:
                    # Underrepresented
                    absence_score = min(20, 5 + comp_count)
                else:
                    absence_score = 0

                # 3. Channel advantage (0-30 points)
                advantage_mult = CHANNEL_ADVANTAGES.get(angle, 1.0)
                advantage_score = (advantage_mult - 0.7) * 50  # Scale 0.7-1.5 → 0-40

                # 4. Outlier bonus (if competitors have outliers here, demand is real)
                outlier_bonus = min(10, outlier_count * 3)

                gap_score = demand_score + absence_score + advantage_score + outlier_bonus

                if gap_score < 10:
                    continue

                avg_comp_views = comp_views // comp_count if comp_count > 0 else 0

                gaps.append({
                    'topic': topic,
                    'angle': angle,
                    'gap_score': round(gap_score, 1),
                    'demand_signal': topic_demand,
                    'competitor_videos': comp_count,
                    'competitor_avg_views': avg_comp_views,
                    'competitor_channels': len(channels),
                    'own_videos': own_count,
                    'outlier_count': outlier_count,
                    'channel_advantage': advantage_mult,
                    'reasoning': self._build_reasoning(
                        topic, angle, comp_count, own_count,
                        topic_demand, advantage_mult, outlier_count,
                        channels
                    ),
                })

        # Sort by gap score descending
        gaps.sort(key=lambda g: g['gap_score'], reverse=True)
        return gaps

    def _build_reasoning(self, topic, angle, comp_count, own_count,
                         demand, advantage, outliers, channels) -> str:
        """Build human-readable reasoning for a gap opportunity."""
        parts = []

        if comp_count > 0 and own_count == 0:
            channel_names = sorted(channels)[:3]
            parts.append(
                f"No own video covers {topic} from {angle} angle. "
                f"{comp_count} competitor videos exist"
                + (f" ({', '.join(channel_names)})" if channel_names else "")
            )
        elif comp_count > 0 and own_count > 0:
            parts.append(
                f"Only {own_count} own video(s) vs {comp_count} competitor videos "
                f"for {topic}/{angle}"
            )
        else:
            parts.append(f"Uncovered {topic}/{angle} space — no one covers this")

        if demand > 0:
            parts.append(f"Search demand: {demand:,}/mo")

        if advantage > 1.1:
            parts.append(f"Strong channel advantage for {angle} content ({advantage}x)")

        if outliers > 0:
            parts.append(f"{outliers} outlier video(s) — proven viral potential")

        return ". ".join(parts) + "."

    def get_gap_recommendations(self, limit: int = 5) -> List[Dict]:
        """Get top gap recommendations formatted for /next integration."""
        gaps = self.find_gaps()
        recs = []
        for g in gaps[:limit]:
            recs.append({
                'topic': g['topic'],
                'angle': g['angle'],
                'gap_score': g['gap_score'],
                'reasoning': g['reasoning'],
                'competitor_videos': g['competitor_videos'],
                'own_videos': g['own_videos'],
                'demand_signal': g['demand_signal'],
            })
        return recs


def _print_gaps(gaps: List[Dict], limit: int = 15):
    """Print gap analysis results."""
    print(f"\n{'='*60}")
    print(f"COMPETITOR GAP ANALYSIS")
    print(f"{'='*60}")
    print(f"\nTop {min(limit, len(gaps))} opportunities (by gap score):\n")

    for i, g in enumerate(gaps[:limit], 1):
        adv_str = f" [advantage: {g['channel_advantage']}x]" if g['channel_advantage'] > 1.0 else ""
        print(f"  #{i:>2}  {g['topic']:>15} / {g['angle']:<15} "
              f"score: {g['gap_score']:>5.1f}{adv_str}")
        print(f"       Comp: {g['competitor_videos']} videos "
              f"(avg {g['competitor_avg_views']:,} views) | "
              f"Own: {g['own_videos']} | "
              f"Outliers: {g['outlier_count']}")
        print(f"       {g['reasoning']}")
        print()


def _print_coverage_map(coverage: Dict):
    """Print the topic × angle coverage map."""
    all_angles = sorted(set(
        angle for topic_angles in coverage.values()
        for angle in topic_angles.keys()
    ))

    print(f"\n{'='*60}")
    print(f"COVERAGE MAP (Competitor / Own)")
    print(f"{'='*60}\n")

    # Header
    header = f"{'Topic':>15}"
    for angle in all_angles:
        header += f" | {angle[:10]:>10}"
    print(header)
    print("-" * len(header))

    # Rows
    for topic in sorted(coverage.keys()):
        row = f"{topic:>15}"
        for angle in all_angles:
            cell = coverage[topic].get(angle, {})
            comp = cell.get('competitor_count', 0)
            own = cell.get('own_count', 0)
            if comp == 0 and own == 0:
                row += f" | {'--':>10}"
            else:
                row += f" | {f'{comp}/{own}':>10}"
        print(row)

    print(f"\nFormat: competitor_count / own_count")
    print(f"'--' = no coverage from either side")


if __name__ == '__main__':
    # Force UTF-8 output on Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Competitor Gap Analyzer -- find uncovered topic-angle opportunities.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.gap_analyzer              # Top gaps
  python -m tools.youtube_analytics.gap_analyzer --map        # Coverage map
  python -m tools.youtube_analytics.gap_analyzer --limit 20   # More results
  python -m tools.youtube_analytics.gap_analyzer --json       # JSON output
        """
    )
    parser.add_argument('--map', action='store_true',
                        help='Show full topic x angle coverage map')
    parser.add_argument('--classify', action='store_true',
                        help='Show angle classification for all competitor videos')
    parser.add_argument('--limit', type=int, default=15,
                        help='Number of gaps to show (default: 15)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('--verbose', '-v', action='store_true')
    verbosity.add_argument('--quiet', '-q', action='store_true')

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    ga = GapAnalyzer()

    if args.classify:
        videos = ga.classify_all_competitors()
        print(f"\n{'='*60}")
        print(f"COMPETITOR VIDEO CLASSIFICATION — {len(videos)} videos")
        print(f"{'='*60}\n")

        # Angle distribution
        angle_counts = defaultdict(int)
        for v in videos:
            for a in v['angles']:
                angle_counts[a] += 1

        print("Angle distribution:")
        for angle, count in sorted(angle_counts.items(), key=lambda x: -x[1]):
            print(f"  {angle:>15}: {count}")

        print(f"\nSample classifications:")
        for v in videos[:20]:
            print(f"  [{'/'.join(v['topics'][:2])}|{'/'.join(v['angles'])}] "
                  f"{v['title'][:55]}")

    elif args.map:
        coverage = ga.build_coverage_map()
        _print_coverage_map(coverage)

    elif args.json:
        gaps = ga.find_gaps()
        print(json.dumps(gaps[:args.limit], indent=2, default=str))

    else:
        gaps = ga.find_gaps()
        if not gaps:
            print("No gaps found. Check that intel.db and analytics.db have data.")
            sys.exit(1)
        _print_gaps(gaps, args.limit)

    sys.exit(0)
