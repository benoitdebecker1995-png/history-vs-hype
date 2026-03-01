"""
Title & CTR Intelligence Module

Analyzes title patterns correlated with CTR from own-channel data.
Predicts CTR for new title variants and audits SEO keyword coverage.

This is the core of Phase 56 (v5.2 Growth Engine).

Features:
  1. Title pattern extraction (length, structure, keywords, format)
  2. CTR correlation analysis (which patterns predict higher CTR)
  3. CTR prediction for new title variants
  4. SEO keyword audit (search demand vs title keyword overlap)
  5. Search traffic % per video

Usage:
    from tools.youtube_analytics.title_intelligence import TitleIntelligence

    ti = TitleIntelligence()
    analysis = ti.analyze_title_patterns()
    prediction = ti.predict_ctr("The 1713 Treaty That Controls Gibraltar")
    audit = ti.seo_audit("Y21EjQ0v9W4")

CLI:
    python -m tools.youtube_analytics.title_intelligence                    # Full analysis
    python -m tools.youtube_analytics.title_intelligence --predict "Title"  # Predict CTR
    python -m tools.youtube_analytics.title_intelligence --audit            # SEO audit all videos

Dependencies:
    - tools.youtube_analytics.growth_data (analytics.db)
    - tools.discovery.database (keywords.db for CTR snapshots)
"""

import re
import json
import sqlite3
import argparse
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from statistics import mean, stdev

from tools.logging_config import get_logger

logger = get_logger(__name__)

ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
KEYWORDS_DB = Path(__file__).parent.parent / 'discovery' / 'keywords.db'


# =========================================================================
# TITLE PATTERN FEATURES
# =========================================================================

@dataclass
class TitleFeatures:
    """Extracted features from a video title."""
    title: str
    length: int
    word_count: int
    has_colon: bool
    has_question: bool
    has_number: bool
    has_year: bool
    has_quote: bool
    has_parenthetical: bool
    starts_with_how: bool
    starts_with_why: bool
    starts_with_the: bool
    has_country_name: bool
    has_person_name: bool
    format_type: str  # question, statement, colon_split, quote_lead, how_why
    topic_type: str

    def to_dict(self) -> Dict:
        return asdict(self)


COUNTRY_KEYWORDS = [
    'guatemala', 'belize', 'venezuela', 'guyana', 'turkey', 'greece',
    'cyprus', 'israel', 'palestine', 'ukraine', 'russia', 'china',
    'taiwan', 'kashmir', 'india', 'pakistan', 'iran', 'morocco',
    'somalia', 'somaliland', 'gibraltar', 'spain', 'britain', 'uk',
    'france', 'peru', 'haiti', 'chagos', 'egypt', 'sudan', 'ethiopia',
    'panama', 'cuba', 'nicaragua', 'cambodia', 'thailand', 'kosovo',
    'armenia', 'georgia', 'bermeja', 'ceuta', 'melilla',
]

PERSON_KEYWORDS = [
    'vance', 'fuentes', 'trump', 'putin', 'stalin', 'lagertha',
    'tucker', 'nick', 'franco',
]


def extract_title_features(title: str, topic_type: str = 'general') -> TitleFeatures:
    """Extract structural features from a title for CTR correlation."""
    t = title.strip()
    t_lower = t.lower()
    words = t.split()

    has_colon = ':' in t
    has_question = '?' in t
    has_number = bool(re.search(r'\b\d+\b', t))
    has_year = bool(re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', t))
    has_quote = '"' in t or '\u201c' in t or '\u201d' in t or "'" in t
    has_paren = '(' in t and ')' in t
    starts_how = t_lower.startswith('how ')
    starts_why = t_lower.startswith('why ')
    starts_the = t_lower.startswith('the ')
    has_country = any(c in t_lower for c in COUNTRY_KEYWORDS)
    has_person = any(p in t_lower for p in PERSON_KEYWORDS)

    # Determine format type
    if has_question:
        fmt = 'question'
    elif starts_how or starts_why:
        fmt = 'how_why'
    elif has_colon:
        fmt = 'colon_split'
    elif has_quote:
        fmt = 'quote_lead'
    else:
        fmt = 'statement'

    return TitleFeatures(
        title=t,
        length=len(t),
        word_count=len(words),
        has_colon=has_colon,
        has_question=has_question,
        has_number=has_number,
        has_year=has_year,
        has_quote=has_quote,
        has_parenthetical=has_paren,
        starts_with_how=starts_how,
        starts_with_why=starts_why,
        starts_with_the=starts_the,
        has_country_name=has_country,
        has_person_name=has_person,
        format_type=fmt,
        topic_type=topic_type,
    )


# =========================================================================
# TITLE INTELLIGENCE ENGINE
# =========================================================================

class TitleIntelligence:
    """
    Analyzes title patterns, predicts CTR, and audits SEO.

    Uses data from:
      - analytics.db (videos table: title, topic_type, views, retention, traffic)
      - keywords.db (ctr_snapshots: actual CTR per video)
      - analytics.db (traffic_sources: search traffic %)
    """

    def __init__(self, analytics_db: Path = None, keywords_db: Path = None):
        self._analytics_path = analytics_db or ANALYTICS_DB
        self._keywords_path = keywords_db or KEYWORDS_DB
        self._patterns: Optional[Dict] = None

    def _get_video_data(self) -> List[Dict]:
        """
        Merge video metadata from analytics.db with CTR from keywords.db.

        Returns list of dicts with: title, topic_type, views, avg_view_percentage,
        subscribers_gained, ctr_percent, impressions, search_traffic_pct
        """
        # Get videos from analytics.db
        conn = sqlite3.connect(str(self._analytics_path))
        conn.row_factory = sqlite3.Row
        videos = {}
        for row in conn.execute(
            "SELECT * FROM videos WHERE views > 10 ORDER BY views DESC"
        ).fetchall():
            vid = dict(row)
            vid['search_views'] = 0
            vid['total_traffic_views'] = 0
            videos[row['video_id']] = vid

        # Get search traffic %
        for row in conn.execute(
            "SELECT video_id, source_type, views FROM traffic_sources"
        ).fetchall():
            vid = row['video_id']
            if vid in videos:
                videos[vid]['total_traffic_views'] += row['views']
                if row['source_type'] == 'YT_SEARCH':
                    videos[vid]['search_views'] = row['views']
        conn.close()

        # Get CTR from keywords.db (latest snapshot per video)
        try:
            conn2 = sqlite3.connect(str(self._keywords_path))
            conn2.row_factory = sqlite3.Row
            for row in conn2.execute("""
                SELECT video_id, ctr_percent, impression_count
                FROM ctr_snapshots
                WHERE ctr_percent > 0
                GROUP BY video_id
                HAVING snapshot_date = MAX(snapshot_date)
            """).fetchall():
                vid = row['video_id']
                if vid in videos:
                    videos[vid]['ctr_percent'] = row['ctr_percent']
                    videos[vid]['impressions'] = row['impression_count']
            conn2.close()
        except Exception as e:
            logger.warning("Could not read keywords.db CTR data: %s", e)

        # Compute search traffic %
        result = []
        for vid_data in videos.values():
            total = vid_data.get('total_traffic_views', 0)
            search = vid_data.get('search_views', 0)
            vid_data['search_traffic_pct'] = round(
                (search / total * 100) if total > 0 else 0, 1
            )
            result.append(vid_data)

        return result

    def analyze_title_patterns(self) -> Dict[str, Any]:
        """
        Analyze title patterns correlated with CTR.

        Returns dict with:
          - pattern_stats: CTR averages by format type, length bucket, features
          - top_patterns: ranked list of feature combinations that predict high CTR
          - recommendations: actionable insights
        """
        videos = self._get_video_data()
        if not videos:
            return {'error': 'No video data available'}

        # Extract features for each video
        entries = []
        for v in videos:
            ctr = v.get('ctr_percent')
            if not ctr or ctr <= 0:
                continue
            features = extract_title_features(v['title'], v.get('topic_type', 'general'))
            entries.append({
                'features': features,
                'ctr': ctr,
                'views': v.get('views', 0),
                'retention': v.get('avg_view_percentage', 0),
                'subs': v.get('subscribers_gained', 0),
                'search_pct': v.get('search_traffic_pct', 0),
            })

        if len(entries) < 5:
            return {'error': f'Only {len(entries)} videos with CTR data — need at least 5'}

        # Filter to long-form only (exclude legacy videos with < 100 impressions)
        entries = [e for e in entries if e['views'] >= 20]

        all_ctrs = [e['ctr'] for e in entries]
        avg_ctr = mean(all_ctrs)

        # --- By format type ---
        by_format = {}
        for e in entries:
            fmt = e['features'].format_type
            if fmt not in by_format:
                by_format[fmt] = []
            by_format[fmt].append(e['ctr'])

        format_stats = {
            fmt: {
                'avg_ctr': round(mean(ctrs), 2),
                'count': len(ctrs),
                'vs_avg': round(mean(ctrs) - avg_ctr, 2),
            }
            for fmt, ctrs in by_format.items()
            if len(ctrs) >= 2
        }

        # --- By length bucket ---
        length_buckets = {'short (<45)': [], 'medium (45-60)': [], 'long (60-70)': [], 'very_long (70+)': []}
        for e in entries:
            ln = e['features'].length
            if ln < 45:
                length_buckets['short (<45)'].append(e['ctr'])
            elif ln < 60:
                length_buckets['medium (45-60)'].append(e['ctr'])
            elif ln <= 70:
                length_buckets['long (60-70)'].append(e['ctr'])
            else:
                length_buckets['very_long (70+)'].append(e['ctr'])

        length_stats = {
            bucket: {
                'avg_ctr': round(mean(ctrs), 2),
                'count': len(ctrs),
                'vs_avg': round(mean(ctrs) - avg_ctr, 2),
            }
            for bucket, ctrs in length_buckets.items()
            if ctrs
        }

        # --- By boolean features ---
        feature_effects = {}
        for feat_name in ['has_colon', 'has_question', 'has_number', 'has_year',
                          'has_quote', 'has_country_name', 'has_person_name',
                          'starts_with_the']:
            with_feat = [e['ctr'] for e in entries if getattr(e['features'], feat_name)]
            without_feat = [e['ctr'] for e in entries if not getattr(e['features'], feat_name)]

            if len(with_feat) >= 2 and len(without_feat) >= 2:
                feature_effects[feat_name] = {
                    'with': round(mean(with_feat), 2),
                    'without': round(mean(without_feat), 2),
                    'delta': round(mean(with_feat) - mean(without_feat), 2),
                    'count_with': len(with_feat),
                }

        # --- By topic type ---
        by_topic = {}
        for e in entries:
            topic = e['features'].topic_type
            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(e['ctr'])

        topic_stats = {
            topic: {
                'avg_ctr': round(mean(ctrs), 2),
                'count': len(ctrs),
            }
            for topic, ctrs in by_topic.items()
            if len(ctrs) >= 2
        }

        # --- Build recommendations ---
        recommendations = self._build_ctr_recommendations(
            avg_ctr, format_stats, length_stats, feature_effects, topic_stats
        )

        self._patterns = {
            'avg_ctr': round(avg_ctr, 2),
            'video_count': len(entries),
            'format_stats': format_stats,
            'length_stats': length_stats,
            'feature_effects': feature_effects,
            'topic_stats': topic_stats,
            'recommendations': recommendations,
        }

        return self._patterns

    def predict_ctr(self, title: str, topic_type: str = 'territorial') -> Dict[str, Any]:
        """
        Predict CTR for a candidate title based on own-channel patterns.

        Returns:
          - predicted_ctr: estimated CTR percentage
          - confidence: low/medium/high based on pattern match count
          - factors: list of features that raise or lower the prediction
          - comparison: how this title compares to channel average
        """
        if not self._patterns:
            self.analyze_title_patterns()
        if not self._patterns or 'error' in self._patterns:
            return {'error': 'No pattern data available'}

        features = extract_title_features(title, topic_type)
        base_ctr = self._patterns['avg_ctr']
        adjustments = []
        confidence_signals = 0

        # Format type adjustment
        fmt_stats = self._patterns['format_stats']
        if features.format_type in fmt_stats:
            delta = fmt_stats[features.format_type]['vs_avg']
            if abs(delta) > 0.3:
                adjustments.append((delta * 0.5, f'Format "{features.format_type}" typically {delta:+.1f}% vs avg'))
            confidence_signals += fmt_stats[features.format_type]['count']

        # Length adjustment
        ln = features.length
        length_stats = self._patterns['length_stats']
        for bucket, stats in length_stats.items():
            if (('short' in bucket and ln < 45) or
                ('medium' in bucket and 45 <= ln < 60) or
                ('long (60' in bucket and 60 <= ln <= 70) or
                ('very_long' in bucket and ln > 70)):
                delta = stats['vs_avg']
                if abs(delta) > 0.3:
                    adjustments.append((delta * 0.4, f'Length {ln} chars ({bucket}) typically {delta:+.1f}% vs avg'))
                confidence_signals += stats['count']

        # Feature adjustments
        effects = self._patterns['feature_effects']
        for feat_name, stats in effects.items():
            has_feature = getattr(features, feat_name)
            delta = stats['delta']
            if abs(delta) > 0.5:
                if has_feature:
                    adjustments.append((delta * 0.3, f'{feat_name}=True adds {delta:+.1f}%'))
                else:
                    adjustments.append((-delta * 0.15, f'{feat_name}=False (missing {delta:+.1f}% boost)'))

        # Topic adjustment
        topic_stats = self._patterns['topic_stats']
        if topic_type in topic_stats:
            topic_avg = topic_stats[topic_type]['avg_ctr']
            topic_delta = topic_avg - base_ctr
            if abs(topic_delta) > 0.3:
                adjustments.append((topic_delta * 0.3, f'Topic "{topic_type}" typically {topic_delta:+.1f}% vs avg'))

        # Calculate predicted CTR
        total_adjustment = sum(a[0] for a in adjustments)
        predicted = max(1.0, base_ctr + total_adjustment)

        # Confidence level
        if confidence_signals >= 20:
            confidence = 'medium'
        elif confidence_signals >= 10:
            confidence = 'low'
        else:
            confidence = 'very_low'

        return {
            'title': title,
            'predicted_ctr': round(predicted, 2),
            'channel_avg_ctr': base_ctr,
            'vs_avg': round(predicted - base_ctr, 2),
            'confidence': confidence,
            'factors': [{'adjustment': round(a[0], 2), 'reason': a[1]} for a in adjustments if abs(a[0]) > 0.1],
            'features': features.to_dict(),
        }

    def rank_title_variants(self, variants: List[str],
                            topic_type: str = 'territorial') -> List[Dict]:
        """
        Rank multiple title variants by predicted CTR.

        Returns list of predictions sorted by predicted_ctr descending.
        """
        predictions = [self.predict_ctr(t, topic_type) for t in variants]
        predictions.sort(key=lambda p: p.get('predicted_ctr', 0), reverse=True)
        return predictions

    def seo_audit(self) -> List[Dict]:
        """
        Audit all videos for SEO keyword coverage and search traffic.

        Returns list of dicts with: video_id, title, search_traffic_pct,
        keyword_coverage, recommendations
        """
        videos = self._get_video_data()
        results = []

        for v in videos:
            if v.get('views', 0) < 20:
                continue

            title = v.get('title', '')
            search_pct = v.get('search_traffic_pct', 0)
            features = extract_title_features(title, v.get('topic_type', 'general'))

            issues = []
            if search_pct < 5:
                issues.append(f'Low search traffic ({search_pct:.1f}%) — title may not match search queries')
            if features.length > 70:
                issues.append(f'Title too long ({features.length} chars) — gets truncated in search results')
            if not features.has_country_name and features.topic_type == 'territorial':
                issues.append('Territorial video without country name — misses geographic search queries')
            if features.word_count < 5:
                issues.append('Very short title — may lack keyword density for search')

            results.append({
                'video_id': v['video_id'],
                'title': title,
                'views': v.get('views', 0),
                'ctr_percent': v.get('ctr_percent'),
                'search_traffic_pct': search_pct,
                'topic_type': v.get('topic_type', 'general'),
                'title_length': features.length,
                'issues': issues,
            })

        # Sort: most issues first, then by views desc
        results.sort(key=lambda r: (-len(r['issues']), -r['views']))
        return results

    def keyword_gaps(self) -> List[Dict]:
        """
        Find high-demand keywords where channel has no video or underperforms.

        Cross-references keywords.db demand data with own-channel titles.
        """
        try:
            conn = sqlite3.connect(str(self._keywords_path))
            conn.row_factory = sqlite3.Row
            keywords = conn.execute("""
                SELECT keyword, search_volume, competition_score, opportunity_score_final
                FROM keywords
                WHERE search_volume > 0 AND lifecycle_state != 'REJECTED'
                ORDER BY search_volume DESC
            """).fetchall()
            conn.close()
        except Exception:
            return []

        # Get all own-channel titles
        videos = self._get_video_data()
        all_titles = ' '.join(v.get('title', '').lower() for v in videos)

        gaps = []
        for kw in keywords:
            keyword = kw['keyword']
            kw_lower = keyword.lower()
            # Check if any video title contains this keyword
            if kw_lower not in all_titles:
                gaps.append({
                    'keyword': keyword,
                    'search_volume': kw['search_volume'],
                    'competition': kw['competition_score'],
                    'opportunity_score': kw['opportunity_score_final'],
                    'covered': False,
                })

        gaps.sort(key=lambda g: g.get('search_volume', 0) or 0, reverse=True)
        return gaps[:20]

    def _build_ctr_recommendations(self, avg_ctr, format_stats, length_stats,
                                   feature_effects, topic_stats) -> List[str]:
        """Build actionable CTR recommendations from pattern analysis."""
        recs = []

        # Best format
        if format_stats:
            best_fmt = max(format_stats.items(), key=lambda x: x[1]['avg_ctr'])
            if best_fmt[1]['vs_avg'] > 0.5:
                recs.append(
                    f'"{best_fmt[0]}" format titles average {best_fmt[1]["avg_ctr"]}% CTR '
                    f'(+{best_fmt[1]["vs_avg"]}% vs channel avg). '
                    f'Based on {best_fmt[1]["count"]} videos.'
                )

        # Best length
        if length_stats:
            best_len = max(length_stats.items(), key=lambda x: x[1]['avg_ctr'])
            if best_len[1]['vs_avg'] > 0.3:
                recs.append(
                    f'Titles in the {best_len[0]} range average {best_len[1]["avg_ctr"]}% CTR '
                    f'(+{best_len[1]["vs_avg"]}% vs avg).'
                )

        # Strongest feature effects
        if feature_effects:
            sorted_effects = sorted(feature_effects.items(), key=lambda x: abs(x[1]['delta']), reverse=True)
            for feat, stats in sorted_effects[:3]:
                direction = 'boosts' if stats['delta'] > 0 else 'reduces'
                recs.append(
                    f'Titles with {feat} {direction} CTR by {abs(stats["delta"]):.1f}% '
                    f'({stats["with"]}% with vs {stats["without"]}% without, n={stats["count_with"]}).'
                )

        # Topic-specific
        if topic_stats:
            best_topic = max(topic_stats.items(), key=lambda x: x[1]['avg_ctr'])
            recs.append(
                f'{best_topic[0].title()} videos have highest CTR at {best_topic[1]["avg_ctr"]}% '
                f'(n={best_topic[1]["count"]}).'
            )

        return recs


# =========================================================================
# CLI
# =========================================================================

def _print_analysis(analysis: Dict) -> None:
    """Pretty-print title pattern analysis."""
    if 'error' in analysis:
        print(f"Error: {analysis['error']}", file=sys.stderr)
        return

    print(f"\n{'='*60}")
    print(f"TITLE & CTR INTELLIGENCE")
    print(f"{'='*60}")
    print(f"Videos analyzed: {analysis['video_count']}")
    print(f"Channel avg CTR: {analysis['avg_ctr']}%")

    print(f"\n--- By Format Type ---")
    for fmt, stats in sorted(analysis['format_stats'].items(), key=lambda x: -x[1]['avg_ctr']):
        marker = '+' if stats['vs_avg'] > 0 else ''
        print(f"  {fmt:>15}: {stats['avg_ctr']}% CTR ({marker}{stats['vs_avg']}%) — {stats['count']} videos")

    print(f"\n--- By Title Length ---")
    for bucket, stats in analysis['length_stats'].items():
        marker = '+' if stats['vs_avg'] > 0 else ''
        print(f"  {bucket:>20}: {stats['avg_ctr']}% CTR ({marker}{stats['vs_avg']}%) — {stats['count']} videos")

    print(f"\n--- Feature Effects ---")
    for feat, stats in sorted(analysis['feature_effects'].items(), key=lambda x: -abs(x[1]['delta'])):
        direction = '+' if stats['delta'] > 0 else ''
        print(f"  {feat:>20}: {direction}{stats['delta']}% CTR (with={stats['with']}%, without={stats['without']}%, n={stats['count_with']})")

    print(f"\n--- By Topic ---")
    for topic, stats in sorted(analysis['topic_stats'].items(), key=lambda x: -x[1]['avg_ctr']):
        print(f"  {topic:>15}: {stats['avg_ctr']}% CTR — {stats['count']} videos")

    print(f"\n--- Recommendations ---")
    for rec in analysis['recommendations']:
        print(f"  - {rec}")
    print()


def _print_prediction(pred: Dict) -> None:
    """Pretty-print CTR prediction."""
    if 'error' in pred:
        print(f"Error: {pred['error']}", file=sys.stderr)
        return

    print(f"\n  Title: {pred['title']}")
    print(f"  Predicted CTR: {pred['predicted_ctr']}%  (channel avg: {pred['channel_avg_ctr']}%,  {pred['vs_avg']:+.2f}%)")
    print(f"  Confidence: {pred['confidence']}")
    if pred['factors']:
        print(f"  Factors:")
        for f in pred['factors']:
            print(f"    {f['adjustment']:+.2f}%  {f['reason']}")
    print()


if __name__ == '__main__':
    # Force UTF-8 output on Windows to handle em-dashes and special chars
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Title & CTR Intelligence — analyze patterns and predict performance.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.title_intelligence
  python -m tools.youtube_analytics.title_intelligence --predict "The 1713 Treaty That Controls Gibraltar"
  python -m tools.youtube_analytics.title_intelligence --rank "Title A" "Title B" "Title C"
  python -m tools.youtube_analytics.title_intelligence --audit
  python -m tools.youtube_analytics.title_intelligence --gaps
        """
    )
    parser.add_argument('--predict', metavar='TITLE', help='Predict CTR for a title')
    parser.add_argument('--rank', nargs='+', metavar='TITLE', help='Rank multiple title variants by predicted CTR')
    parser.add_argument('--topic', default='territorial', help='Topic type for prediction (default: territorial)')
    parser.add_argument('--audit', action='store_true', help='Run SEO audit on all videos')
    parser.add_argument('--gaps', action='store_true', help='Show keyword gaps')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Debug output")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Errors only")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(getattr(args, 'verbose', False), getattr(args, 'quiet', False))

    ti = TitleIntelligence()

    if args.predict:
        analysis = ti.analyze_title_patterns()
        pred = ti.predict_ctr(args.predict, args.topic)
        _print_prediction(pred)

    elif args.rank:
        analysis = ti.analyze_title_patterns()
        ranked = ti.rank_title_variants(args.rank, args.topic)
        print(f"\n{'='*60}")
        print(f"TITLE RANKING BY PREDICTED CTR")
        print(f"{'='*60}")
        for i, pred in enumerate(ranked, 1):
            print(f"\n  #{i}")
            _print_prediction(pred)

    elif args.audit:
        results = ti.seo_audit()
        print(f"\n{'='*60}")
        print(f"SEO AUDIT — {len(results)} videos")
        print(f"{'='*60}")
        for r in results:
            if not r['issues']:
                continue
            ctr_str = f"{r['ctr_percent']:.1f}%" if r['ctr_percent'] else 'N/A'
            print(f"\n  {r['title'][:55]}")
            print(f"    Views: {r['views']} | CTR: {ctr_str} | Search: {r['search_traffic_pct']}%")
            for issue in r['issues']:
                print(f"    ! {issue}")

    elif args.gaps:
        gaps = ti.keyword_gaps()
        print(f"\n{'='*60}")
        print(f"KEYWORD GAPS — uncovered search demand")
        print(f"{'='*60}")
        for g in gaps[:15]:
            print(f"  {g['keyword']:>40} | vol: {g['search_volume'] or '?':>5} | opp: {g.get('opportunity_score') or '?'}")

    else:
        # Default: full analysis
        analysis = ti.analyze_title_patterns()
        _print_analysis(analysis)

    sys.exit(0)
