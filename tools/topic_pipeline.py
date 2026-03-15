"""
Topic Pipeline — Ranks future video topics by (search volume x channel fit x competitor gap).

Uses discovery DB keywords, intel DB competitor data, and own-channel performance patterns
to produce a ranked list of topic opportunities.

v2.0 (2026-03-07): Added geographic monopoly scoring, news hook urgency,
    subscriber conversion weighting, and hybrid topic detection.

Usage:
    python -m tools.topic_pipeline [--top N] [--save]
"""

import sqlite3
import argparse
import math
import sys
from pathlib import Path
from datetime import datetime

try:
    from tools.title_scorer import score_title as _score_title
    TITLE_SCORER_AVAILABLE = True
except ImportError:
    TITLE_SCORER_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent


# =============================================================================
# GEOGRAPHIC MONOPOLY DATA (from cross-video analysis)
# =============================================================================
# Key insight: Guatemala/Belize got 28,955 views because 46.6% came from Belize
# (pop 400K, English-speaking, zero quality YouTube coverage).
# Formula: underserved English-speaking population + active dispute + no competition
#
# Population = English-speaking population of the affected country/region
# Scores are pre-calculated: log10(population) normalized, capped at 25 bonus points
GEOGRAPHIC_MONOPOLY_TARGETS = {
    # Country/region: (english_speaking_pop, keywords_that_trigger)
    'belize': (400_000, ['belize', 'belizean', 'sapodilla', 'guatemala belize']),
    'guyana': (800_000, ['guyana', 'essequibo', 'guyanese']),
    'trinidad': (1_400_000, ['trinidad', 'tobago']),
    'jamaica': (2_900_000, ['jamaica', 'jamaican']),
    'fiji': (900_000, ['fiji', 'fijian']),
    'mauritius': (1_300_000, ['mauritius', 'chagos', 'diego garcia']),
    'cyprus': (1_200_000, ['cyprus', 'cypriot', 'northern cyprus']),
    'malta': (500_000, ['malta', 'maltese']),
    'gibraltar': (33_000, ['gibraltar', 'utrecht']),
    'somaliland': (4_000_000, ['somaliland', 'somali']),
    'taiwan': (23_000_000, ['taiwan', 'taiwanese']),
    'hong kong': (7_500_000, ['hong kong']),
    'singapore': (5_700_000, ['singapore', 'singaporean']),
    'ireland': (5_000_000, ['ireland', 'irish', 'northern ireland']),
    'scotland': (5_500_000, ['scotland', 'scottish']),
    'puerto rico': (3_200_000, ['puerto rico']),
    'bermuda': (64_000, ['bermuda', 'bermeja']),
    'falklands': (3_500, ['falkland', 'malvinas']),
    'peru': (33_000_000, ['peru', 'peruvian']),
}

# =============================================================================
# NEWS HOOK / URGENCY KEYWORDS
# =============================================================================
# Topics with active legal proceedings, upcoming deadlines, or recent events
# get a bonus because they have natural urgency without clickbait.
NEWS_HOOK_KEYWORDS = {
    'high_urgency': [  # +15 bonus
        'icj', 'ruling', 'verdict', 'treaty expires', 'referendum',
        'election 2026', 'deadline', 'vote',
    ],
    'medium_urgency': [  # +8 bonus
        'court', 'tribunal', 'lawsuit', 'protest', 'crisis',
        'negotiation', 'summit', 'hearing',
    ],
}


def get_keyword_data():
    """Get keyword opportunities from discovery DB."""
    db_path = PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT keyword, search_volume, competition_score, opportunity_score_final,
               lifecycle_state
        FROM keywords
        WHERE search_volume > 0
        ORDER BY COALESCE(opportunity_score_final, 0) DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_own_channel_patterns():
    """Get performance patterns from own channel."""
    db_path = PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
    if not db_path.exists():
        return {}

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Topic type performance
    cur.execute("""
        SELECT topic_type,
               COUNT(*) as n,
               ROUND(AVG(views), 0) as avg_views,
               ROUND(AVG(avg_retention_pct), 1) as avg_ret,
               ROUND(CAST(SUM(subscribers_gained) AS FLOAT) / NULLIF(SUM(views), 0) * 100, 2) as conv_rate
        FROM video_performance
        WHERE topic_type NOT IN ('short', 'general')
          AND views > 0
        GROUP BY topic_type
    """)
    topic_perf = {}
    for r in cur.fetchall():
        topic_perf[r[0]] = {
            'n': r[1], 'avg_views': r[2], 'avg_ret': r[3], 'conv_rate': r[4]
        }

    conn.close()
    return topic_perf


def get_competitor_gaps():
    """Find topics underserved by competitors."""
    db_path = PROJECT_ROOT / "tools" / "intel" / "intel.db"
    if not db_path.exists():
        return {}

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Count videos per topic cluster
    cur.execute("""
        SELECT topic_cluster, COUNT(*) as cnt, ROUND(AVG(views)) as avg_views
        FROM competitor_videos
        WHERE topic_cluster IS NOT NULL
        GROUP BY topic_cluster
        ORDER BY cnt DESC
    """)
    clusters = {}
    for r in cur.fetchall():
        clusters[r[0]] = {'count': r[1], 'avg_views': r[2]}

    conn.close()
    return clusters


def classify_topic(keyword):
    """Classify a keyword into channel topic types."""
    k = keyword.lower()

    territorial_terms = ['border', 'territory', 'dispute', 'partition', 'annex',
                         'island', 'strait', 'sovereignty', 'falkland', 'malvina',
                         'crimea', 'kashmir', 'chagos', 'diego garcia', 'iron curtain',
                         'antarctic treaty']
    colonial_terms = ['colonial', 'scramble', 'imperialism', 'conquest',
                      'slave', 'independence', 'decolonization', 'berlin conference',
                      'ottoman', 'tordesillas', 'sykes picot', 'monroe doctrine',
                      'british empire', 'french empire', 'spanish empire',
                      'dutch empire', 'portuguese empire', 'belgian congo']
    ideological_terms = ['myth', 'misconception', 'propaganda', 'debunk', 'lie',
                         'narrative', 'belief', 'conspiracy', 'hoax', 'destruction',
                         'burning', 'library of alexandria', 'flat earth', 'dark ages']
    legal_terms = ['law', 'court', 'icj', 'tribunal', 'statute', 'constitution',
                   'convention', 'rights', 'treaty of utrecht']
    medieval_terms = ['medieval', 'viking', 'crusade', 'dark ages', 'middle ages',
                      'byzantine', 'roman', 'ancient', 'empire', 'dynasty',
                      'pharaoh', 'phoenician', 'assyrian', 'persian', 'mongol',
                      'aztec', 'inca', 'maya', 'khmer', 'songhai']

    if any(t in k for t in territorial_terms):
        return 'territorial'
    if any(t in k for t in colonial_terms):
        return 'colonial'
    if any(t in k for t in ideological_terms):
        return 'ideological'
    if any(t in k for t in legal_terms):
        return 'legal'
    if any(t in k for t in medieval_terms):
        return 'medieval'
    return 'general'


def get_existing_projects():
    """Get list of topics already in production."""
    projects = set()
    prod_dir = PROJECT_ROOT / "video-projects" / "_IN_PRODUCTION"
    if prod_dir.exists():
        for p in prod_dir.iterdir():
            if p.is_dir():
                projects.add(p.name.lower())
    arch_dir = PROJECT_ROOT / "video-projects" / "_ARCHIVED"
    if arch_dir.exists():
        for p in arch_dir.iterdir():
            if p.is_dir():
                projects.add(p.name.lower())
    return projects


def score_topics(top_n=20):
    """Score and rank topic opportunities."""
    keywords = get_keyword_data()
    topic_perf = get_own_channel_patterns()
    existing = get_existing_projects()

    # Topic type multipliers (from own-channel data)
    # Updated with subscriber conversion weighting:
    #   territorial = most views (2,449 avg) but 0.65% sub rate
    #   ideological = best conversion (2.31% sub rate) but fewer views (179 avg)
    #   colonial = good balance
    # Strategy: boost types that CONVERT, not just get views
    type_multipliers = {
        'territorial': 1.4,   # high views, low conversion
        'colonial': 1.4,      # good views + good conversion
        'ideological': 1.5,   # best conversion rate (3.5x territorial)
        'legal': 1.1,         # pairs well with territorial for hybrid
        'medieval': 0.9,
        'general': 0.7,
    }

    # Group keywords by root topic (deduplicate variants)
    topic_groups = {}
    for kw in keywords:
        # Simple grouping: use first 3 words as key
        words = kw['keyword'].split()
        root = ' '.join(words[:3]) if len(words) >= 3 else kw['keyword']

        if root not in topic_groups or (kw['search_volume'] or 0) > (topic_groups[root].get('search_volume') or 0):
            topic_groups[root] = kw

    results = []
    for root, kw in topic_groups.items():
        keyword = kw['keyword']
        topic_type = classify_topic(keyword)
        search_vol = kw['search_volume'] or 0
        competition = kw['competition_score'] or 50
        opp_score = kw['opportunity_score_final'] or 0
        state = kw['lifecycle_state'] or 'new'

        # Check if already in production (check multiple keyword words)
        kw_words = keyword.lower().split()
        is_in_prod = False
        for proj in existing:
            # Match if 2+ keyword words appear in project name
            matches = sum(1 for w in kw_words if w in proj)
            if matches >= 2 or (len(kw_words) == 1 and kw_words[0] in proj):
                is_in_prod = True
                break
        # Also check common aliases
        aliases = {
            'scramble for africa': 'berlin',
            'berlin conference': 'berlin',
            'library of alexandria': 'alexandria',
        }
        for alias_key, alias_val in aliases.items():
            if alias_key in keyword.lower() and any(alias_val in p for p in existing):
                is_in_prod = True

        # Base score from discovery DB opportunity score
        base = opp_score

        # Channel fit multiplier
        type_mult = type_multipliers.get(topic_type, 0.7)

        # Competition gap bonus (lower competition = more opportunity)
        comp_bonus = max(0, (100 - competition) / 100 * 15)

        # Search volume bonus (log scale)
        vol_bonus = min(20, math.log10(max(search_vol, 1)) * 5)

        # --- NEW: Geographic monopoly bonus ---
        # Underserved English-speaking population with no quality YouTube coverage
        geo_bonus = 0
        geo_target = None
        k_lower = keyword.lower()
        for region, (pop, triggers) in GEOGRAPHIC_MONOPOLY_TARGETS.items():
            if any(t in k_lower for t in triggers):
                # Log-scaled population bonus, capped at 25
                geo_bonus = min(25, math.log10(max(pop, 1)) * 4)
                geo_target = region
                break

        # --- NEW: News hook urgency bonus ---
        urgency_bonus = 0
        for term in NEWS_HOOK_KEYWORDS.get('high_urgency', []):
            if term in k_lower:
                urgency_bonus = 15
                break
        if urgency_bonus == 0:
            for term in NEWS_HOOK_KEYWORDS.get('medium_urgency', []):
                if term in k_lower:
                    urgency_bonus = 8
                    break

        # --- NEW: Hybrid topic bonus ---
        # Topics that combine territorial (views) + ideological (conversion)
        # are the holy grail: they get both views AND subscribers
        hybrid_bonus = 0
        is_hybrid = False
        if topic_type == 'territorial':
            # Check if keyword also has ideological markers
            ideo_terms = ['myth', 'misconception', 'propaganda', 'debunk',
                          'narrative', 'belief', 'true', 'false', 'fact']
            if any(t in k_lower for t in ideo_terms):
                hybrid_bonus = 10
                is_hybrid = True
        elif topic_type == 'ideological':
            # Check if keyword also has territorial markers
            terr_terms = ['border', 'territory', 'dispute', 'island',
                          'sovereignty', 'land', 'claim']
            if any(t in k_lower for t in terr_terms):
                hybrid_bonus = 10
                is_hybrid = True

        # Penalty for already-started topics
        prod_penalty = -30 if is_in_prod else 0

        # Penalty for published topics
        pub_penalty = -50 if state == 'published' else 0

        final_score = ((base * type_mult) + comp_bonus + vol_bonus
                       + geo_bonus + urgency_bonus + hybrid_bonus
                       + prod_penalty + pub_penalty)

        results.append({
            'keyword': keyword,
            'topic_type': topic_type,
            'search_volume': search_vol,
            'competition': competition,
            'base_score': round(opp_score, 1),
            'type_multiplier': type_mult,
            'geo_bonus': round(geo_bonus, 1),
            'geo_target': geo_target,
            'urgency_bonus': urgency_bonus,
            'hybrid_bonus': hybrid_bonus,
            'is_hybrid': is_hybrid,
            'final_score': round(final_score, 1),
            'state': state,
            'in_production': is_in_prod,
            'channel_perf': topic_perf.get(topic_type, {}),
        })

    # Sort by final score
    results.sort(key=lambda x: -x['final_score'])
    return results[:top_n]


def _check_data_freshness():
    """Check if databases are stale and return warning lines."""
    from tools.logging_config import check_db_freshness

    warnings = []
    kw_db = PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
    intel_db = PROJECT_ROOT / "tools" / "intel" / "intel.db"

    for label, path, table, col in [
        ("Discovery DB", kw_db, "keywords", "last_updated"),
        ("Intel DB", intel_db, "competitor_videos", "fetched_at"),
    ]:
        if path.exists():
            result = check_db_freshness(str(path), table, col)
            if result.get('is_stale'):
                warnings.append(
                    f"**{label}** last updated {result['last_updated']} "
                    f"({result['days_old']} days ago)"
                )
    return warnings


def format_report(results):
    """Format results as markdown."""
    staleness = _check_data_freshness()

    lines = [
        "# Topic Pipeline — Ranked Opportunities",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Method:** (search volume x channel fit x competitor gap x geographic monopoly x urgency)",
        f"**Sources:** Discovery DB keywords + own-channel performance + intel DB competitors",
        "",
    ]

    if staleness:
        lines.extend([
            "> **Data Staleness Warning:**",
            *[f"> - {w}" for w in staleness],
            "",
        ])

    lines.extend([
        "## Scoring Factors",
        "",
        "- **Base:** Discovery DB opportunity score (search volume, competition, relevance)",
        "- **Channel fit:** Topic type multiplier from own performance data",
        "  - Ideological: 1.5x (best sub conversion 2.31%), Territorial: 1.4x (most views), Colonial: 1.4x",
        "- **Competition gap:** Lower competition = higher bonus (up to +15)",
        "- **Volume bonus:** Log-scaled search volume bonus (up to +20)",
        "- **Geographic monopoly:** Underserved English-speaking audience bonus (up to +25)",
        "- **News hook urgency:** Active legal/political event bonus (+8 to +15)",
        "- **Hybrid bonus:** Topics combining views (territorial) + conversion (ideological) (+10)",
        "- **Penalties:** -30 if already in production, -50 if published",
        "",
        "## Top Opportunities",
        "",
        "| Rank | Score | Topic | Type | Vol | Geo | Urg | Hyb | Status |",
        "|------|-------|-------|------|-----|-----|-----|-----|--------|",
    ])

    for i, r in enumerate(results, 1):
        status = r['state']
        if r['in_production']:
            status = "IN PROD"
        geo_col = f"+{r['geo_bonus']:.0f}" if r.get('geo_bonus', 0) > 0 else "-"
        urg_col = f"+{r['urgency_bonus']}" if r.get('urgency_bonus', 0) > 0 else "-"
        hyb_col = "+10" if r.get('is_hybrid') else "-"
        lines.append(
            f"| {i} | {r['final_score']:.0f} | {r['keyword']} | "
            f"{r['topic_type']} | {r['search_volume']:,} | {geo_col} | {urg_col} | {hyb_col} | {status} |"
        )

    lines.extend([
        "",
        "## Topic Type Performance (Own Channel)",
        "",
        "| Type | Avg Views | Retention | Sub Conv Rate |",
        "|------|-----------|-----------|---------------|",
    ])

    # Add performance context
    topic_perf = get_own_channel_patterns()
    for tt in ['territorial', 'ideological', 'colonial', 'legal', 'medieval']:
        perf = topic_perf.get(tt, {})
        if perf:
            lines.append(
                f"| {tt} | {perf.get('avg_views', 'N/A')} | "
                f"{perf.get('avg_ret', 'N/A')}% | {perf.get('conv_rate', 'N/A')}% |"
            )

    lines.extend([
        "",
        "## Recommended Next Videos",
        "",
        "Top 5 NOT already in production:",
        "",
    ])

    not_in_prod = [r for r in results if not r['in_production'] and r['state'] != 'published']
    for i, r in enumerate(not_in_prod[:5], 1):
        perf = r.get('channel_perf', {})
        expected = perf.get('avg_views', 'unknown')
        lines.append(
            f"{i}. **{r['keyword']}** (score: {r['final_score']:.0f})")
        lines.append(
            f"   - Type: {r['topic_type']} | Volume: {r['search_volume']:,} | "
            f"Competition: {r['competition']:.0f}")
        lines.append(
            f"   - Expected views based on type: ~{expected}")

        # Title quality check: score the keyword as if it were a title
        if TITLE_SCORER_AVAILABLE:
            title_result = _score_title(r['keyword'])
            lines.append(
                f"   - Title quality as-is: {title_result['score']}/100 ({title_result['grade']}) "
                f"— {', '.join(title_result['suggestions'][:2]) if title_result['suggestions'] else 'no issues'}")

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Topic Pipeline — Ranks future video topics by opportunity score.",
        epilog="Example: python -m tools.topic_pipeline --top 10 --save",
    )
    parser.add_argument("--top", type=int, default=25, help="Number of topics to show (default: 25)")
    parser.add_argument("--save", action="store_true", help="Save report to channel-data/TOPIC-PIPELINE.md")
    parser.add_argument("--type", help="Filter by topic type (territorial, ideological, colonial, legal, medieval)")
    args = parser.parse_args()

    results = score_topics(args.top)

    if args.type:
        results = [r for r in results if r['topic_type'] == args.type]

    report = format_report(results)

    if args.save:
        out_path = PROJECT_ROOT / "channel-data" / "TOPIC-PIPELINE.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"Saved to {out_path}")
    else:
        print(report)

    sys.exit(0)
