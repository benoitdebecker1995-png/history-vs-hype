"""
Competitor Outlier Title Dissector

Analyzes WHY outlier titles (3x+ channel median views) worked by extracting
granular patterns beyond the basic how_why/declarative/versus categories.
Generates actionable title templates from proven formulas.

Data sources:
  - tools/benchmark/raw_data/*.json (competitor video data)
  - analytics.db (own channel data)

Usage:
    python -m tools.benchmark.outlier_title_dissector --report
    python -m tools.benchmark.outlier_title_dissector --templates
    python -m tools.benchmark.outlier_title_dissector --score "My Title Here"
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = Path(__file__).parent / "raw_data"
DB_PATH = PROJECT_ROOT / "tools" / "youtube_analytics" / "analytics.db"
CACHE_PATH = Path(__file__).parent / "_outlier_analysis.json"
REPORT_PATH = PROJECT_ROOT / "channel-data" / "patterns" / "OUTLIER-TITLE-DISSECTION.md"

# Skip non-video data files
SKIP_FILES = {'all_channels_summary.json', 'en_gb_hooks.json', 'verified_hooks.json'}

# Country/region names for entity detection
COUNTRIES = {
    'afghanistan', 'africa', 'albania', 'algeria', 'america', 'argentina',
    'armenia', 'australia', 'austria', 'azerbaijan', 'bahrain', 'bangladesh',
    'belarus', 'belgium', 'belize', 'bolivia', 'bosnia', 'brazil', 'britain',
    'british', 'bulgaria', 'burma', 'cambodia', 'cameroon', 'canada', 'chad',
    'chile', 'china', 'chinese', 'colombia', 'congo', 'croatia', 'cuba',
    'cyprus', 'czech', 'czechoslovakia', 'denmark', 'ecuador', 'egypt',
    'england', 'eritrea', 'estonia', 'ethiopia', 'europe', 'european',
    'finland', 'france', 'french', 'georgia', 'germany', 'german', 'ghana',
    'gibraltar', 'greece', 'greek', 'greenland', 'guatemala', 'guyana',
    'haiti', 'hawaii', 'hungary', 'hungarian', 'iceland', 'india', 'indian',
    'indonesia', 'iran', 'iranian', 'iraq', 'iraqi', 'ireland', 'irish',
    'israel', 'israeli', 'italy', 'italian', 'japan', 'japanese', 'jordan',
    'kashmir', 'kazakhstan', 'kenya', 'korea', 'korean', 'kosovo', 'kurdish',
    'kuwait', 'kyrgyzstan', 'latvia', 'lebanon', 'libya', 'lithuania',
    'macedonia', 'malaysia', 'mali', 'mauritius', 'mexico', 'mexican',
    'mongolia', 'mongol', 'montenegro', 'morocco', 'mozambique', 'myanmar',
    'nato', 'nepal', 'netherlands', 'nicaragua', 'niger', 'nigeria',
    'norway', 'norwegian', 'oman', 'ottoman', 'pakistan', 'pakistani',
    'palestine', 'palestinian', 'panama', 'paraguay', 'peru', 'peruvian',
    'philippines', 'poland', 'polish', 'portugal', 'portuguese', 'prussia',
    'prussian', 'qatar', 'romania', 'rome', 'roman', 'russia', 'russian',
    'rwanda', 'saudi', 'scotland', 'scottish', 'serbia', 'serbian',
    'singapore', 'slovakia', 'slovenia', 'somalia', 'somaliland',
    'south africa', 'spain', 'spanish', 'sri lanka', 'sudan', 'sweden',
    'swedish', 'switzerland', 'swiss', 'syria', 'syrian', 'taiwan',
    'tajikistan', 'tanzania', 'thailand', 'tibet', 'tibetan', 'tunisia',
    'turkey', 'turkish', 'turkmenistan', 'uganda', 'ukraine', 'ukrainian',
    'ussr', 'uruguay', 'uzbekistan', 'vatican', 'venezuela', 'vietnam',
    'vietnamese', 'wales', 'yemen', 'yugoslavia', 'zimbabwe',
}

# Geographic terms
GEO_TERMS = {
    'island', 'islands', 'border', 'borders', 'wall', 'sea', 'ocean',
    'river', 'mountain', 'canal', 'strait', 'peninsula', 'continent',
    'region', 'territory', 'coast', 'desert', 'jungle', 'rainforest',
    'arctic', 'antarctic', 'pacific', 'atlantic', 'mediterranean',
    'city', 'capital', 'province', 'state',
}

# Scale/stakes words
SCALE_WORDS = {
    'world', 'global', 'entire', 'every', 'all', 'million', 'billion',
    'trillion', 'thousand', 'century', 'centuries', 'millennium',
    'civilization', 'empire', 'collapse', 'fall', 'rise', 'war',
    'revolution', 'genocide', 'nuclear', 'apocalypse', 'extinction',
    'massive', 'biggest', 'largest', 'deadliest', 'worst', 'greatest',
}

# Authority/evidence words
AUTHORITY_WORDS = {
    'document', 'documents', 'evidence', 'proof', 'prove', 'proved',
    'proven', 'exposed', 'reveal', 'revealed', 'shows', 'show',
    'explained', 'explain', 'truth', 'real', 'actually', 'really',
    'fact', 'facts', 'myth', 'lie', 'lies', 'debunk', 'debunked',
    'sources', 'primary', 'original', 'official',
}

# Temporal urgency words
URGENCY_WORDS = {
    'still', 'today', 'now', 'modern', 'current', 'recent', 'just',
    'new', 'latest', 'breaking', 'ongoing', 'continues', 'happening',
}


def load_all_channel_data() -> list:
    """Load all competitor video data from raw_data/ JSON files."""
    all_videos = []
    channels_loaded = 0

    for json_file in sorted(RAW_DATA_DIR.glob('*.json')):
        if json_file.name in SKIP_FILES:
            continue

        try:
            with open(json_file, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.warning("Error reading %s: %s", json_file.name, e)
            continue

        channel_name = data.get('name', json_file.stem)
        channel_median = data.get('median_views', 0)
        videos = data.get('all_videos', [])

        if not videos:
            continue

        # Compute median if not provided
        if not channel_median:
            view_counts = [v.get('view_count', 0) for v in videos if v.get('view_count')]
            channel_median = median(view_counts) if view_counts else 0

        for v in videos:
            views = v.get('view_count', 0)
            ratio = views / max(channel_median, 1)
            v['channel'] = channel_name
            v['channel_median'] = channel_median
            v['views_ratio'] = ratio
            v['is_outlier'] = ratio >= 3.0
            all_videos.append(v)

        channels_loaded += 1
        logger.info("Loaded %s: %d videos, median %d views",
                    channel_name, len(videos), channel_median)

    logger.info("Total: %d videos from %d channels", len(all_videos), channels_loaded)
    return all_videos


def load_own_videos() -> list:
    """Load own channel videos from DB."""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT video_id, title, views, topic_type FROM videos")
    videos = []
    view_counts = []
    for row in cur.fetchall():
        views = row['views'] or 0
        view_counts.append(views)
        videos.append({
            'id': row['video_id'],
            'title': row['title'],
            'view_count': views,
            'channel': 'History vs Hype',
            'topic_type': row['topic_type'],
        })
    conn.close()

    own_median = median(view_counts) if view_counts else 0
    for v in videos:
        v['channel_median'] = own_median
        v['views_ratio'] = v['view_count'] / max(own_median, 1)
        v['is_outlier'] = v['views_ratio'] >= 3.0

    return videos


def extract_patterns(title: str) -> dict:
    """Extract granular patterns from a title."""
    title_lower = title.lower()
    words = title_lower.split()
    clean_words = re.sub(r'[^\w\s]', ' ', title_lower).split()

    patterns = {}

    # --- Structural ---
    patterns['char_count'] = len(title)
    patterns['word_count'] = len(words)
    patterns['sentence_count'] = len(re.split(r'[.!?]', title.rstrip('.!?')))
    patterns['has_period'] = '.' in title[:-1]  # Period mid-title (sentence separator)
    patterns['has_question'] = '?' in title
    patterns['has_exclamation'] = '!' in title
    patterns['has_colon'] = ':' in title
    patterns['has_dash'] = '—' in title or ' - ' in title or '–' in title
    patterns['has_ellipsis'] = '...' in title
    patterns['has_parentheses'] = '(' in title
    patterns['has_quotes'] = '"' in title or '"' in title or '\'' in title

    # First word
    patterns['first_word'] = words[0] if words else ''

    # --- Entity patterns ---
    found_countries = [w for w in clean_words if w in COUNTRIES]
    patterns['has_country'] = len(found_countries) > 0
    patterns['country_count'] = len(set(found_countries))
    patterns['countries'] = list(set(found_countries))

    patterns['has_number'] = bool(re.search(r'\d', title))
    numbers = re.findall(r'[\d,]+(?:\.\d+)?', title)
    patterns['numbers'] = numbers
    patterns['number_count'] = len(numbers)

    patterns['has_year'] = bool(re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title))

    patterns['has_vs'] = bool(re.search(r'\bvs\.?\b', title_lower))
    patterns['has_versus'] = 'versus' in title_lower

    geo_found = [w for w in clean_words if w in GEO_TERMS]
    patterns['has_geo_term'] = len(geo_found) > 0
    patterns['geo_terms'] = list(set(geo_found))

    # --- Cognitive patterns ---
    patterns['starts_how'] = title_lower.startswith('how ')
    patterns['starts_why'] = title_lower.startswith('why ')
    patterns['starts_what'] = title_lower.startswith('what ')
    patterns['starts_the'] = title_lower.startswith('the ')
    patterns['is_how_why'] = patterns['starts_how'] or patterns['starts_why']

    # Mystery/curiosity
    mystery_words = {'nobody', 'hidden', 'secret', 'mysterious', 'unknown',
                     'forgotten', 'lost', 'untold', 'never', 'no one'}
    patterns['has_mystery'] = any(w in clean_words for w in mystery_words)

    # Scale/stakes
    patterns['has_scale'] = any(w in clean_words for w in SCALE_WORDS)
    scale_found = [w for w in clean_words if w in SCALE_WORDS]
    patterns['scale_words'] = list(set(scale_found))

    # Authority/evidence
    patterns['has_authority'] = any(w in clean_words for w in AUTHORITY_WORDS)
    auth_found = [w for w in clean_words if w in AUTHORITY_WORDS]
    patterns['authority_words'] = list(set(auth_found))

    # Urgency
    patterns['has_urgency'] = any(w in clean_words for w in URGENCY_WORDS)

    # Specificity (named entities beyond countries)
    # Dollar amounts, specific dates, named people
    patterns['has_dollar'] = '$' in title
    patterns['has_specific_quantity'] = bool(re.search(
        r'\b\d+[\s-]?(week|day|year|month|hour|minute|mile|km|trillion|billion|million)\b',
        title_lower
    ))

    # --- Formula classification ---
    if patterns['has_vs'] or patterns['has_versus']:
        patterns['formula'] = 'versus'
    elif patterns['has_question']:
        patterns['formula'] = 'question'
    elif patterns['has_colon']:
        patterns['formula'] = 'colon'
    elif patterns['is_how_why']:
        patterns['formula'] = 'how_why'
    elif patterns['has_period'] and patterns['sentence_count'] >= 2:
        patterns['formula'] = 'two_sentence'
    else:
        patterns['formula'] = 'declarative'

    return patterns


def compute_pattern_stats(all_videos: list) -> dict:
    """Compute pattern frequency and performance stats."""
    outliers = [v for v in all_videos if v.get('is_outlier')]
    non_outliers = [v for v in all_videos if not v.get('is_outlier')]

    logger.info("Outliers: %d, Non-outliers: %d", len(outliers), len(non_outliers))

    # Extract patterns for all videos
    for v in all_videos:
        v['patterns'] = extract_patterns(v.get('title', ''))

    # Pattern dimensions to compare
    bool_patterns = [
        'has_country', 'has_number', 'has_year', 'has_vs', 'has_geo_term',
        'starts_how', 'starts_why', 'starts_the', 'is_how_why',
        'has_mystery', 'has_scale', 'has_authority', 'has_urgency',
        'has_question', 'has_colon', 'has_period', 'has_dollar',
        'has_specific_quantity', 'has_quotes',
    ]

    stats = {}
    for pattern in bool_patterns:
        outlier_count = sum(1 for v in outliers if v['patterns'].get(pattern))
        non_outlier_count = sum(1 for v in non_outliers if v['patterns'].get(pattern))

        outlier_pct = outlier_count / max(len(outliers), 1) * 100
        non_outlier_pct = non_outlier_count / max(len(non_outliers), 1) * 100

        # Average views ratio for videos with this pattern
        with_pattern = [v for v in all_videos if v['patterns'].get(pattern)]
        without_pattern = [v for v in all_videos if not v['patterns'].get(pattern)]

        avg_ratio_with = mean(v['views_ratio'] for v in with_pattern) if with_pattern else 0
        avg_ratio_without = mean(v['views_ratio'] for v in without_pattern) if without_pattern else 0

        lift = avg_ratio_with / max(avg_ratio_without, 0.01)

        stats[pattern] = {
            'outlier_count': outlier_count,
            'outlier_pct': outlier_pct,
            'non_outlier_count': non_outlier_count,
            'non_outlier_pct': non_outlier_pct,
            'total_with': len(with_pattern),
            'avg_ratio_with': avg_ratio_with,
            'avg_ratio_without': avg_ratio_without,
            'lift': lift,
        }

    # Formula distribution
    formula_stats = defaultdict(lambda: {'outlier': 0, 'non_outlier': 0, 'total': 0, 'ratios': []})
    for v in all_videos:
        f = v['patterns'].get('formula', 'other')
        formula_stats[f]['total'] += 1
        formula_stats[f]['ratios'].append(v['views_ratio'])
        if v.get('is_outlier'):
            formula_stats[f]['outlier'] += 1
        else:
            formula_stats[f]['non_outlier'] += 1

    for f in formula_stats:
        formula_stats[f]['avg_ratio'] = mean(formula_stats[f]['ratios']) if formula_stats[f]['ratios'] else 0
        formula_stats[f]['outlier_pct'] = (
            formula_stats[f]['outlier'] / max(formula_stats[f]['total'], 1) * 100
        )

    # Word count stats
    outlier_wc = [v['patterns']['word_count'] for v in outliers]
    non_outlier_wc = [v['patterns']['word_count'] for v in non_outliers]

    return {
        'pattern_stats': stats,
        'formula_stats': dict(formula_stats),
        'outlier_avg_word_count': mean(outlier_wc) if outlier_wc else 0,
        'non_outlier_avg_word_count': mean(non_outlier_wc) if non_outlier_wc else 0,
        'outlier_avg_char_count': mean(v['patterns']['char_count'] for v in outliers) if outliers else 0,
        'total_outliers': len(outliers),
        'total_videos': len(all_videos),
    }


def extract_templates(outliers: list) -> list:
    """Extract reusable title templates from outlier titles."""
    templates = []

    # Group by formula type
    by_formula = defaultdict(list)
    for v in outliers:
        f = v['patterns'].get('formula', 'other')
        by_formula[f].append(v)

    # Two-sentence pattern (period-separated)
    two_sent = [v for v in outliers if v['patterns'].get('has_period') and v['patterns']['sentence_count'] >= 2]
    if two_sent:
        examples = [v['title'] for v in sorted(two_sent, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Two-Sentence Declaration',
            'template': '[Statement about entity]. [Consequence or mechanism].',
            'examples': examples,
            'count': len(two_sent),
            'avg_ratio': mean(v['views_ratio'] for v in two_sent),
            'key_feature': 'Period creates two distinct ideas. Second sentence often reveals mechanism.',
        })

    # Country + mechanism
    country_mech = [v for v in outliers
                    if v['patterns'].get('has_country')
                    and (v['patterns'].get('is_how_why') or v['patterns'].get('has_authority'))]
    if country_mech:
        examples = [v['title'] for v in sorted(country_mech, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Country + Mechanism',
            'template': 'How/Why [Country] [Mechanism Verb] [Object/Consequence]',
            'examples': examples,
            'count': len(country_mech),
            'avg_ratio': mean(v['views_ratio'] for v in country_mech),
            'key_feature': 'Named country + explanation framing. Promises understanding of a system.',
        })

    # Versus pattern
    vs_vids = [v for v in outliers if v['patterns'].get('has_vs')]
    if vs_vids:
        examples = [v['title'] for v in sorted(vs_vids, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Versus/Comparison',
            'template': '[Entity A] vs [Entity B]. [Stakes or mechanism].',
            'examples': examples,
            'count': len(vs_vids),
            'avg_ratio': mean(v['views_ratio'] for v in vs_vids),
            'key_feature': 'Direct comparison creates inherent tension. Works best with countries.',
        })

    # Number + specificity
    num_specific = [v for v in outliers
                    if v['patterns'].get('has_specific_quantity')
                    or (v['patterns'].get('has_number') and v['patterns'].get('has_country'))]
    if num_specific:
        examples = [v['title'] for v in sorted(num_specific, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Specificity Bomb',
            'template': '[Number] [Unit] [Action/Consequence]',
            'examples': examples,
            'count': len(num_specific),
            'avg_ratio': mean(v['views_ratio'] for v in num_specific),
            'key_feature': 'Specific numbers create credibility and curiosity. "$1 Trillion" > "expensive".',
        })

    # Scale/stakes pattern
    scale_vids = [v for v in outliers if v['patterns'].get('has_scale') and not v['patterns'].get('is_how_why')]
    if scale_vids:
        examples = [v['title'] for v in sorted(scale_vids, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Scale Signal',
            'template': '[Scale word] [Entity] [Action]',
            'examples': examples,
            'count': len(scale_vids),
            'avg_ratio': mean(v['views_ratio'] for v in scale_vids),
            'key_feature': 'Words like "entire", "world", "collapse" signal stakes.',
        })

    # Mystery/curiosity
    mystery_vids = [v for v in outliers if v['patterns'].get('has_mystery')]
    if mystery_vids:
        examples = [v['title'] for v in sorted(mystery_vids, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Mystery/Forgotten',
            'template': 'The [Adjective] [Thing] That [Nobody/Never] [Action]',
            'examples': examples,
            'count': len(mystery_vids),
            'avg_ratio': mean(v['views_ratio'] for v in mystery_vids),
            'key_feature': 'Creates curiosity gap. "Nobody", "hidden", "forgotten" promise exclusive knowledge.',
        })

    # Question format
    question_vids = [v for v in outliers if v['patterns'].get('has_question')]
    if question_vids:
        examples = [v['title'] for v in sorted(question_vids, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Direct Question',
            'template': '[Question about topic]?',
            'examples': examples,
            'count': len(question_vids),
            'avg_ratio': mean(v['views_ratio'] for v in question_vids),
            'key_feature': 'Questions engage the viewer\'s internal answer reflex.',
        })

    # Geographic/territorial
    geo_vids = [v for v in outliers if v['patterns'].get('has_geo_term')]
    if geo_vids:
        examples = [v['title'] for v in sorted(geo_vids, key=lambda x: x['views_ratio'], reverse=True)[:5]]
        templates.append({
            'name': 'Geographic Hook',
            'template': '[Geographic feature] + [conflict/stakes]',
            'examples': examples,
            'count': len(geo_vids),
            'avg_ratio': mean(v['views_ratio'] for v in geo_vids),
            'key_feature': 'Island, border, wall, sea — geographic terms ground abstract conflicts.',
        })

    # Sort by avg_ratio
    templates.sort(key=lambda x: x['avg_ratio'], reverse=True)
    return templates


def score_title_against_outliers(title: str, pattern_stats: dict) -> dict:
    """Score a title against outlier patterns."""
    patterns = extract_patterns(title)

    positive_signals = []
    negative_signals = []
    neutral_signals = []

    for pattern_name, stats in pattern_stats.items():
        has_pattern = patterns.get(pattern_name, False)
        lift = stats['lift']

        if has_pattern:
            if lift > 1.3:
                positive_signals.append({
                    'pattern': pattern_name,
                    'lift': lift,
                    'outlier_pct': stats['outlier_pct'],
                    'note': f'{stats["outlier_pct"]:.0f}% of outliers have this (vs {stats["non_outlier_pct"]:.0f}% non-outliers)',
                })
            elif lift < 0.8:
                negative_signals.append({
                    'pattern': pattern_name,
                    'lift': lift,
                    'note': f'Only {stats["outlier_pct"]:.0f}% of outliers have this',
                })
            else:
                neutral_signals.append({'pattern': pattern_name, 'lift': lift})

    # Compute composite score
    if positive_signals:
        avg_pos_lift = mean(s['lift'] for s in positive_signals)
    else:
        avg_pos_lift = 1.0

    neg_penalty = len(negative_signals) * 0.1
    score = min(100, max(0, int((avg_pos_lift - 1) * 50 + 50 - neg_penalty * 20)))

    return {
        'title': title,
        'patterns': patterns,
        'score': score,
        'positive_signals': sorted(positive_signals, key=lambda x: x['lift'], reverse=True),
        'negative_signals': sorted(negative_signals, key=lambda x: x['lift']),
        'neutral_signals': neutral_signals,
    }


def generate_report(all_videos: list, stats: dict, templates: list,
                    own_videos: list = None) -> str:
    """Generate the full outlier title dissection report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    outliers = [v for v in all_videos if v.get('is_outlier')]

    lines = []
    lines.append("# Outlier Title Dissection")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {stats['total_videos']} | **Outliers (3x+):** {stats['total_outliers']}")
    lines.append("")

    # ---- Section 1: Outlier Dataset ----
    lines.append("## 1. Top Outlier Titles")
    lines.append("")
    lines.append("| # | Title | Channel | Views | Ratio | Formula | Key Patterns |")
    lines.append("|---|-------|---------|------:|------:|---------|-------------|")

    top_outliers = sorted(outliers, key=lambda x: x['views_ratio'], reverse=True)[:30]
    for i, v in enumerate(top_outliers, 1):
        p = v['patterns']
        # Build pattern tags
        tags = []
        if p.get('has_country'):
            tags.append(f"🌍{p['country_count']}")
        if p.get('has_number'):
            tags.append("🔢")
        if p.get('has_scale'):
            tags.append("📏")
        if p.get('has_mystery'):
            tags.append("❓")
        if p.get('has_authority'):
            tags.append("📄")
        if p.get('has_urgency'):
            tags.append("⏰")
        if p.get('has_geo_term'):
            tags.append("🗺️")

        tag_str = ' '.join(tags) if tags else '—'
        title_display = v['title'][:55]
        lines.append(
            f"| {i} | {title_display} | {v['channel'][:15]} | "
            f"{v['view_count']:,} | {v['views_ratio']:.1f}x | "
            f"{p.get('formula', '?')} | {tag_str} |"
        )
    lines.append("")

    # ---- Section 2: Pattern Frequency ----
    lines.append("## 2. Pattern Frequency (Outliers vs Non-Outliers)")
    lines.append("")
    lines.append("| Pattern | Outlier % | Non-Outlier % | Lift | n (with) | Signal |")
    lines.append("|---------|--------:|-------------:|-----:|---------:|--------|")

    sorted_patterns = sorted(
        stats['pattern_stats'].items(),
        key=lambda x: x[1]['lift'],
        reverse=True
    )
    for name, s in sorted_patterns:
        signal = "✅ STRONG" if s['lift'] > 1.5 else "👍 Positive" if s['lift'] > 1.2 else "⚠️ Negative" if s['lift'] < 0.8 else "— Neutral"
        display_name = name.replace('has_', '').replace('starts_', 'starts_').replace('is_', '')
        lines.append(
            f"| {display_name} | {s['outlier_pct']:.0f}% | {s['non_outlier_pct']:.0f}% | "
            f"{s['lift']:.2f}x | {s['total_with']} | {signal} |"
        )
    lines.append("")

    # ---- Section 3: Formula Performance ----
    lines.append("## 3. Title Formula Performance")
    lines.append("")
    lines.append("| Formula | Total | Outliers | Outlier Rate | Avg Views Ratio |")
    lines.append("|---------|------:|---------:|------------:|---------------:|")

    sorted_formulas = sorted(
        stats['formula_stats'].items(),
        key=lambda x: x[1]['avg_ratio'],
        reverse=True
    )
    for name, fs in sorted_formulas:
        lines.append(
            f"| {name} | {fs['total']} | {fs['outlier']} | "
            f"{fs['outlier_pct']:.0f}% | {fs['avg_ratio']:.2f}x |"
        )
    lines.append("")

    # ---- Section 4: Title Template Library ----
    lines.append("## 4. Title Template Library")
    lines.append("")
    lines.append(f"Extracted from {len(outliers)} outlier titles.")
    lines.append("")

    for i, t in enumerate(templates, 1):
        lines.append(f"### Template {i}: {t['name']}")
        lines.append(f"**Pattern:** `{t['template']}`")
        lines.append(f"**Frequency:** {t['count']} outliers | **Avg views ratio:** {t['avg_ratio']:.1f}x")
        lines.append(f"**Key feature:** {t['key_feature']}")
        lines.append("")
        lines.append("**Examples:**")
        for ex in t['examples'][:4]:
            lines.append(f"- {ex}")
        lines.append("")

    # ---- Section 5: Own Channel Gap Analysis ----
    if own_videos:
        lines.append("## 5. History vs Hype Title Gap Analysis")
        lines.append("")
        lines.append("Patterns we USE vs patterns outliers use.")
        lines.append("")

        own_patterns = defaultdict(int)
        for v in own_videos:
            v['patterns'] = extract_patterns(v.get('title', ''))
            for key in stats['pattern_stats']:
                if v['patterns'].get(key):
                    own_patterns[key] += 1

        lines.append("| Pattern | Outlier % | Our % | Gap | Action |")
        lines.append("|---------|--------:|------:|----:|--------|")

        for name, s in sorted_patterns:
            if s['lift'] < 1.1:
                continue
            our_pct = own_patterns[name] / max(len(own_videos), 1) * 100
            gap = s['outlier_pct'] - our_pct
            action = "ADD MORE" if gap > 20 else "ON TRACK" if gap > -10 else "OVERUSING"
            display_name = name.replace('has_', '').replace('starts_', 'starts_').replace('is_', '')
            lines.append(
                f"| {display_name} | {s['outlier_pct']:.0f}% | {our_pct:.0f}% | "
                f"{gap:+.0f}% | {action} |"
            )
        lines.append("")

    # ---- Section 6: Word Count ----
    lines.append("## 6. Title Length")
    lines.append("")
    lines.append(f"- **Outlier avg word count:** {stats['outlier_avg_word_count']:.1f}")
    lines.append(f"- **Non-outlier avg word count:** {stats['non_outlier_avg_word_count']:.1f}")
    lines.append(f"- **Outlier avg char count:** {stats['outlier_avg_char_count']:.0f}")
    lines.append("")

    # ---- Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    # Top 3 patterns by lift
    top_patterns = sorted_patterns[:3]
    for name, s in top_patterns:
        display = name.replace('has_', '').replace('starts_', 'starts_').replace('is_', '')
        lines.append(f"- **{display}** appears in {s['outlier_pct']:.0f}% of outliers vs "
                     f"{s['non_outlier_pct']:.0f}% of non-outliers ({s['lift']:.1f}x lift).")

    if templates:
        best = templates[0]
        lines.append(f"- **Best-performing template:** \"{best['name']}\" with {best['avg_ratio']:.1f}x avg views ratio.")

    lines.append(f"- **Outlier titles average {stats['outlier_avg_word_count']:.0f} words** vs "
                 f"{stats['non_outlier_avg_word_count']:.0f} for non-outliers.")

    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by `outlier_title_dissector.py` on {now}. "
                 f"Data covers {stats['total_videos']} videos from "
                 f"{len(set(v['channel'] for v in all_videos))} channels.*")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Competitor outlier title dissection — extract proven title patterns"
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full analysis report')
    parser.add_argument('--templates', action='store_true',
                        help='Show only the template library')
    parser.add_argument('--score', type=str,
                        help='Score a title against outlier patterns')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    # Load data
    all_videos = load_all_channel_data()
    if not all_videos:
        print("No competitor data found in tools/benchmark/raw_data/")
        sys.exit(1)

    # Compute stats
    stats = compute_pattern_stats(all_videos)

    # Extract templates from outliers
    outliers = [v for v in all_videos if v.get('is_outlier')]
    templates = extract_templates(outliers)

    if args.score:
        result = score_title_against_outliers(args.score, stats['pattern_stats'])
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(f"\nTitle: {result['title']}")
        print(f"Outlier Pattern Score: {result['score']}/100")
        print(f"\nPositive signals ({len(result['positive_signals'])}):")
        for s in result['positive_signals'][:5]:
            print(f"  ✅ {s['pattern']}: {s['lift']:.1f}x lift — {s['note']}")
        print(f"\nNegative signals ({len(result['negative_signals'])}):")
        for s in result['negative_signals'][:5]:
            print(f"  ⚠️ {s['pattern']}: {s['lift']:.1f}x lift — {s['note']}")
        return

    if args.templates:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        for i, t in enumerate(templates, 1):
            print(f"\n--- Template {i}: {t['name']} ---")
            print(f"Pattern: {t['template']}")
            print(f"Frequency: {t['count']} outliers | Avg ratio: {t['avg_ratio']:.1f}x")
            print(f"Key: {t['key_feature']}")
            for ex in t['examples'][:3]:
                print(f"  • {ex}")
        return

    # Full report
    own_videos = load_own_videos()
    report = generate_report(all_videos, stats, templates, own_videos)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(f"Report saved to {REPORT_PATH}")

    # Cache
    cache_data = {
        'generated': now if (now := datetime.now(timezone.utc).isoformat()) else '',
        'total_videos': stats['total_videos'],
        'total_outliers': stats['total_outliers'],
        'template_count': len(templates),
        'templates': [{'name': t['name'], 'count': t['count'], 'avg_ratio': t['avg_ratio']}
                      for t in templates],
    }
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2)

    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(report)


if __name__ == '__main__':
    main()
