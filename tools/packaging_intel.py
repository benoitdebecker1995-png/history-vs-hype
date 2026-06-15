"""
Packaging Intelligence Module — Connects competitor data + demand signals to title scoring.

Bridges three data sources the title_scorer was blind to:
1. Competitor topic viability — do similar topics get views in the niche? (870 videos, 10 channels)
2. Demand proxy — does autocomplete suggest people search for this? (YouTube autocomplete position)
3. Own-channel topic history — how did our similar topics perform?

This module provides signals that title_scorer.py can query to penalize/boost titles
based on whether the underlying TOPIC has demand, not just whether the title CONSTRUCTION
is good.

v1 (2026-04-08): Initial build after audit showed 3/18 titles over-scored due to
zero topic demand ("good title, nobody cares about the topic").

Usage:
    from tools.packaging_intel import get_topic_viability

    viability = get_topic_viability("tariff history myth")
    # Returns: {'score': 25, 'competitor_signal': 'low', 'demand_signal': 'none', ...}

    # Or from CLI:
    python -m tools.packaging_intel "tariff history myth"
    python -m tools.packaging_intel "venezuela guyana essequibo"
    python -m tools.packaging_intel --scan-competitors   # scan for new outliers
"""

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List

from tools.logging_config import get_logger

logger = get_logger(__name__)

_PROJECT_ROOT = Path(__file__).parent.parent

# Entity words that are high-signal for topic matching (countries, regions, historical terms)
_ENTITY_WORDS = {
    'venezuela', 'guyana', 'essequibo', 'turkey', 'greece', 'iran', 'iraq',
    'israel', 'palestine', 'russia', 'ukraine', 'china', 'taiwan', 'india',
    'pakistan', 'kashmir', 'morocco', 'sahara', 'cyprus', 'kosovo', 'armenia',
    'georgia', 'haiti', 'peru', 'spain', 'portugal', 'france', 'britain',
    'germany', 'japan', 'korea', 'vietnam', 'afghanistan', 'syria', 'egypt',
    'sudan', 'somalia', 'somaliland', 'gibraltar', 'bermeja', 'cambodia',
    'thailand', 'belize', 'guatemala', 'mexico', 'nato', 'cia', 'kgb',
    'crusades', 'ottoman', 'byzantine', 'roman', 'viking', 'colonial',
    'trump', 'vance', 'stalin', 'hitler', 'putin', 'lagertha',
    'tariff', 'genocide', 'treaty', 'coup', 'revolution', 'independence',
}
_INTEL_DB = _PROJECT_ROOT / "tools" / "intel" / "intel.db"
_KEYWORDS_DB = _PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
_ANALYTICS_DB = _PROJECT_ROOT / "tools" / "youtube_analytics" / "analytics.db"


# =============================================================================
# Topic viability scoring
# =============================================================================

def get_topic_viability(query: str, intel_db: str = None, keywords_db: str = None) -> Dict[str, Any]:
    """
    Score a topic's viability based on competitor performance + demand signals.

    This answers: "If I make a video about this topic, will anyone see it?"
    — which title_scorer.py cannot answer (it only scores construction).

    Args:
        query: Topic description or title to evaluate (e.g., "tariff history myth")
        intel_db: Path to intel.db (default: auto-detect)
        keywords_db: Path to keywords.db (default: auto-detect)

    Returns:
        {
            'query': str,
            'viability_score': int,          # 0-100, topic demand score
            'viability_label': str,           # 'high', 'medium', 'low', 'unknown'
            'competitor_signal': {
                'matching_videos': int,       # competitor videos on similar topics
                'avg_views': int,             # avg views of those videos
                'outlier_count': int,         # how many were 3x+ outliers
                'top_title': str,             # best-performing similar title
                'top_views': int,
            },
            'own_channel_signal': {
                'similar_videos': int,
                'avg_views': int,
                'avg_ctr': float,
                'best_title': str,
            },
            'demand_signal': {
                'autocomplete_score': int,    # 0-100 from demand.py
                'available': bool,
            },
            'recommendation': str,            # actionable one-liner
        }
    """
    intel_path = intel_db or str(_INTEL_DB)
    kw_path = keywords_db or str(_KEYWORDS_DB)

    result = {
        'query': query,
        'viability_score': 50,  # neutral default
        'viability_label': 'unknown',
        'competitor_signal': _get_competitor_signal(query, intel_path),
        'own_channel_signal': _get_own_channel_signal(query),
        'demand_signal': _get_demand_signal(query, kw_path),
        'recommendation': '',
    }

    # Calculate composite viability score
    score = _calculate_viability_score(result)
    result['viability_score'] = score
    result['viability_label'] = _score_to_label(score)
    result['recommendation'] = _generate_recommendation(result)

    return result


def _get_competitor_signal(query: str, db_path: str) -> Dict[str, Any]:
    """Search competitor videos for similar topics."""
    default = {
        'matching_videos': 0, 'avg_views': 0, 'outlier_count': 0,
        'top_title': '', 'top_views': 0,
    }

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # Extract key terms from query for matching
        terms = _extract_search_terms(query)
        if not terms:
            conn.close()
            return default

        # Two-pass search strategy:
        # Pass 1: Find videos matching entity terms (countries, proper nouns) — high precision
        # Pass 2: Find videos matching 2+ generic terms — broader but still relevant
        entity_terms = [t for t in terms if len(t) > 3 and t[0:1] != t[0:1].lower()
                        or t in _ENTITY_WORDS]
        generic_terms = [t for t in terms if t not in entity_terms]

        where_clauses = []
        params = []

        # Entity matches: any single entity term is sufficient
        for term in entity_terms[:3]:
            where_clauses.append("LOWER(title) LIKE ?")
            params.append(f"%{term}%")

        # Generic matches: require 2+ to avoid "myth" matching everything
        if len(generic_terms) >= 2:
            match_exprs = []
            match_params = []
            for term in generic_terms[:4]:
                match_exprs.append(f"(CASE WHEN LOWER(title) LIKE ? THEN 1 ELSE 0 END)")
                match_params.append(f"%{term}%")
            score_expr = " + ".join(match_exprs)
            where_clauses.append(f"({score_expr}) >= 2")
            params.extend(match_params)

        if not where_clauses:
            # Fallback: just use all terms with OR
            for term in terms[:3]:
                where_clauses.append("LOWER(title) LIKE ?")
                params.append(f"%{term}%")

        sql = f"""
            SELECT title, views, is_outlier, outlier_ratio, topic_cluster
            FROM competitor_videos
            WHERE {' OR '.join(where_clauses)}
            ORDER BY views DESC
            LIMIT 50
        """

        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return default

        total_views = sum(r['views'] for r in rows)
        outliers = sum(1 for r in rows if r['is_outlier'])

        return {
            'matching_videos': len(rows),
            'avg_views': total_views // len(rows),
            'outlier_count': outliers,
            'top_title': rows[0]['title'],
            'top_views': rows[0]['views'],
        }

    except Exception as e:
        logger.warning("Competitor signal failed: %s", e)
        return default


def _get_own_channel_signal(query: str) -> Dict[str, Any]:
    """Check how our own similar topics performed."""
    default = {
        'similar_videos': 0, 'avg_views': 0, 'avg_ctr': 0.0, 'best_title': '',
    }

    try:
        if not _ANALYTICS_DB.exists():
            return default

        from tools.youtube_analytics.store import AnalyticsStore

        terms = _extract_search_terms(query)
        if not terms:
            return default

        where_clauses = []
        params: List[Any] = []
        for term in terms[:5]:
            where_clauses.append("LOWER(title) LIKE ?")
            params.append(f"%{term}%")

        sql = (
            "SELECT title, views, ctr_percent FROM videos "
            f"WHERE {' OR '.join(where_clauses)} "
            "ORDER BY views DESC LIMIT 20"
        )

        with AnalyticsStore.open(_ANALYTICS_DB) as store:
            rows = store.execute(sql, params)

        if not rows:
            return default

        total_views = sum(r['views'] or 0 for r in rows)
        ctrs = [r['ctr_percent'] for r in rows if r['ctr_percent'] and r['ctr_percent'] > 0]
        avg_ctr = sum(ctrs) / len(ctrs) if ctrs else 0.0

        return {
            'similar_videos': len(rows),
            'avg_views': total_views // len(rows),
            'avg_ctr': round(avg_ctr, 2),
            'best_title': rows[0]['title'],
        }

    except Exception as e:
        logger.warning("Own channel signal failed: %s", e)
        return default


def _get_demand_signal(query: str, db_path: str) -> Dict[str, Any]:
    """Check autocomplete demand score for the topic."""
    default = {'autocomplete_score': 0, 'available': False}

    try:
        if not Path(db_path).exists():
            return default

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # Check if we have cached demand data for any matching keyword
        terms = _extract_search_terms(query)
        for term in terms:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT search_volume FROM keywords WHERE LOWER(keyword) LIKE ? AND search_volume > 0 LIMIT 1",
                (f"%{term}%",)
            )
            row = cursor.fetchone()
            if row:
                conn.close()
                return {'autocomplete_score': row['search_volume'], 'available': True}

        conn.close()
        return default

    except Exception as e:
        logger.warning("Demand signal failed: %s", e)
        return default


def _extract_search_terms(query: str) -> List[str]:
    """Extract meaningful search terms from a query, filtering stopwords."""
    stopwords = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
        'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
        'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
        'but', 'and', 'or', 'if', 'because', 'until', 'while', 'about',
        'that', 'this', 'these', 'those', 'what', 'which', 'who', 'whom',
        'its', 'his', 'her', 'their', 'our', 'your', 'my', 'vs', 'versus',
    }
    # Split on non-alphanumeric, lowercase, filter
    words = re.findall(r'[a-zA-Z]+', query.lower())
    return [w for w in words if w not in stopwords and len(w) > 2]


def _calculate_viability_score(result: Dict) -> int:
    """
    Calculate composite viability score 0-100.

    Weighting:
    - Competitor signal (50%): do similar topics get views in the niche?
    - Demand signal (30%): does autocomplete suggest search interest?
    - Own channel signal (20%): how did our similar topics perform?
    """
    score = 0

    # Competitor signal (0-50 points)
    comp = result['competitor_signal']
    if comp['matching_videos'] > 0:
        # Scale by avg views relative to niche median (~1M for these channels)
        view_score = min(50, int(comp['avg_views'] / 50000))  # 2.5M+ = 50
        # Boost for outliers
        if comp['outlier_count'] > 0:
            view_score = min(50, view_score + 10)
        score += view_score
    else:
        score += 10  # unknown = slight penalty, not zero

    # Demand signal (0-30 points)
    demand = result['demand_signal']
    if demand['available'] and demand['autocomplete_score'] > 0:
        score += min(30, int(demand['autocomplete_score'] * 0.3))
    else:
        score += 10  # unknown = neutral

    # Own channel signal (0-20 points)
    own = result['own_channel_signal']
    if own['similar_videos'] > 0:
        if own['avg_ctr'] >= 3.5:
            score += 20
        elif own['avg_ctr'] >= 2.5:
            score += 15
        elif own['avg_views'] > 100:
            score += 10
        else:
            score += 5
    else:
        score += 10  # no similar = neutral

    return min(100, max(0, score))


def _score_to_label(score: int) -> str:
    if score >= 70:
        return 'high'
    elif score >= 45:
        return 'medium'
    elif score >= 25:
        return 'low'
    else:
        return 'very_low'


def _generate_recommendation(result: Dict) -> str:
    """Generate a one-line actionable recommendation."""
    score = result['viability_score']
    comp = result['competitor_signal']
    demand = result['demand_signal']

    if score >= 70:
        return f"Strong topic. {comp['matching_videos']} competitor videos, {comp['outlier_count']} outliers. Go."
    elif score >= 45:
        if comp['matching_videos'] == 0:
            return "No competitor data — topic may be too niche. Verify search demand manually."
        return f"Moderate topic. {comp['avg_views']:,} avg competitor views. Consider a stronger angle."
    elif score >= 25:
        if not demand['available']:
            return "Low demand signal. Check VidIQ manually before committing research time."
        return f"Weak topic. Competitors average {comp['avg_views']:,} views. Consider higher-demand alternative."
    else:
        return "Very low viability. Competitors and demand both weak. Strongly reconsider."


# =============================================================================
# Competitor outlier scanner
# =============================================================================

def scan_competitor_outliers(
    db_path: str = None,
    min_ratio: float = 3.0,
    days: int = 90,
) -> List[Dict[str, Any]]:
    """
    Find recent competitor outlier videos (3x+ channel average).

    Useful for spotting what's working NOW in the niche.

    Args:
        db_path: Path to intel.db
        min_ratio: Minimum outlier ratio (default 3.0x)
        days: Only look at videos published in last N days

    Returns:
        List of outlier dicts sorted by outlier_ratio descending.
    """
    path = db_path or str(_INTEL_DB)

    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Recency filter: only outliers published within the window ("what's working NOW").
        # Rows with NULL published_at fail the comparison and are excluded (can't confirm
        # recent) — intentional, matches the lever's purpose.
        cursor.execute("""
            SELECT cv.title, cv.views, cv.outlier_ratio, cv.topic_cluster,
                   cv.published_at, cc.channel_id
            FROM competitor_videos cv
            LEFT JOIN competitor_channels cc ON cv.channel_id = cc.channel_id
            WHERE cv.is_outlier = 1
              AND cv.outlier_ratio >= ?
              AND cv.published_at >= date('now', ?)
            ORDER BY cv.outlier_ratio DESC
            LIMIT 30
        """, (min_ratio, f'-{int(days)} days'))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'title': r['title'],
                'views': r['views'],
                'ratio': round(r['outlier_ratio'], 1),
                'topic': r['topic_cluster'],
                'published': r['published_at'],
            }
            for r in rows
        ]

    except Exception as e:
        logger.warning("Outlier scan failed: %s", e)
        return []


# =============================================================================
# Title scorer integration
# =============================================================================

def get_viability_modifier(query: str) -> int:
    """
    Get a score modifier for title_scorer.py based on topic viability.

    Returns:
        int: Score modifier to add to the title score.
        - High viability: +10
        - Medium viability: 0
        - Low viability: -10
        - Very low viability: -15
    """
    viability = get_topic_viability(query)
    label = viability['viability_label']

    if label == 'high':
        return 10
    elif label == 'medium':
        return 0
    elif label == 'low':
        return -10
    else:  # very_low
        return -15


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Packaging Intelligence -- topic viability + competitor scanning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('query', nargs='?', help='Topic to evaluate')
    parser.add_argument('--scan-competitors', action='store_true',
                        help='Scan for recent competitor outliers')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.scan_competitors:
        outliers = scan_competitor_outliers()
        if args.json:
            print(json.dumps(outliers, indent=2, default=str))
        else:
            print(f"\n{'=' * 60}")
            print(f"  COMPETITOR OUTLIERS (3x+ channel average)")
            print(f"{'=' * 60}")
            for o in outliers:
                print(f"\n  {o['ratio']}x | {o['views']:>12,} views | {o['title'][:55]}")
                print(f"       Topic: {o['topic']}")
            print(f"\n  Total: {len(outliers)} outliers")
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    result = get_topic_viability(args.query)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"\n{'=' * 60}")
        print(f"  TOPIC VIABILITY: {args.query}")
        print(f"{'=' * 60}")
        print(f"  Score:  {result['viability_score']}/100 ({result['viability_label']})")
        print(f"  Rec:    {result['recommendation']}")

        comp = result['competitor_signal']
        print(f"\n  Competitor: {comp['matching_videos']} similar videos, {comp['avg_views']:,} avg views, {comp['outlier_count']} outliers")
        if comp['top_title']:
            print(f"  Top match: {comp['top_title'][:60]} ({comp['top_views']:,} views)")

        own = result['own_channel_signal']
        if own['similar_videos'] > 0:
            print(f"\n  Own channel: {own['similar_videos']} similar, {own['avg_views']:,} avg views, {own['avg_ctr']:.1f}% avg CTR")

        demand = result['demand_signal']
        if demand['available']:
            print(f"\n  Demand: autocomplete score {demand['autocomplete_score']}/100")
        else:
            print(f"\n  Demand: no cached data (run demand.py for this topic)")

        print()


if __name__ == '__main__':
    main()
