"""
Competitor Gap Analysis — find what competing videos cover and what they miss.

Given a topic, this tool:
1. Searches YouTube for top competing videos
2. Fetches their transcripts
3. Extracts claims/topics covered
4. Identifies gaps your video can fill

Usage (via agent, not standalone):
    The /research command or wiki-researcher agent calls this tool's
    functions. WebSearch results are passed in from the calling agent.

Standalone test:
    python tools/research/competitor_gap.py "Treaty of Tordesillas"
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter


# ---------------------------------------------------------------------------
# Transcript analysis
# ---------------------------------------------------------------------------

def extract_topics_from_transcript(transcript: str) -> Dict[str, Any]:
    """Extract key topics, claims, and structure from a competitor transcript.

    Returns dict with:
        - topics: list of topic strings mentioned
        - claims: list of factual assertions
        - figures: list of named people
        - dates: list of dates/years mentioned
        - sources_cited: list of academic sources mentioned (if any)
        - structure: rough section breakdown
        - word_count: total words
        - has_primary_sources: bool (do they show documents?)
    """
    if not transcript:
        return {'error': 'Empty transcript'}

    words = transcript.split()
    word_count = len(words)
    text_lower = transcript.lower()

    # Extract dates/years
    years = re.findall(r'\b(1[0-9]{3}|20[0-2][0-9])\b', transcript)
    year_counts = Counter(years)

    # Extract named figures (capitalized multi-word sequences)
    # Simple heuristic: two+ capitalized words in sequence
    figures = re.findall(r'(?:[A-Z][a-z]+\s){1,3}[A-Z][a-z]+', transcript)
    figure_counts = Counter(figures)
    # Filter out common false positives
    stop_figures = {
        'The United', 'United States', 'South America', 'North America',
        'New York', 'New World', 'Old World', 'Middle Ages',
        'Western Europe', 'Eastern Europe', 'Central America',
        'Atlantic Ocean', 'Pacific Ocean', 'Indian Ocean',
    }
    top_figures = [
        f for f, c in figure_counts.most_common(20)
        if f not in stop_figures and c >= 2
    ]

    # Check for academic source citations
    source_patterns = [
        r'according to [\w\s]+',
        r'(?:professor|historian|scholar|author) [\w\s]+',
        r'(?:writes|wrote|argues|argued) (?:in|that)',
        r'page \d+',
        r'pp?\.\s*\d+',
        r'university (?:of|press)',
    ]
    sources_cited = []
    for pat in source_patterns:
        matches = re.findall(pat, text_lower)
        sources_cited.extend(matches)

    has_primary_sources = bool(sources_cited) or any(
        phrase in text_lower for phrase in [
            'the document', 'the treaty text', 'the original',
            'primary source', 'the manuscript', 'the actual text',
            'let me show you', 'here is the', 'on screen',
        ]
    )

    # Identify major topics by keyword clusters
    topic_keywords = {
        'treaty/legal': ['treaty', 'agreement', 'signed', 'ratified', 'article', 'clause', 'provision'],
        'colonialism': ['colony', 'colonial', 'empire', 'imperial', 'conquest', 'colonize'],
        'religion/church': ['pope', 'papal', 'church', 'catholic', 'christian', 'muslim', 'bishop'],
        'navigation/maritime': ['sail', 'ship', 'navigation', 'maritime', 'ocean', 'voyage', 'fleet'],
        'trade/economics': ['trade', 'merchant', 'gold', 'spice', 'economic', 'wealth', 'commerce'],
        'war/conflict': ['war', 'battle', 'fight', 'conflict', 'army', 'military', 'siege'],
        'language/culture': ['language', 'speak', 'culture', 'indigenous', 'native', 'tupi', 'lingua'],
        'borders/territory': ['border', 'territory', 'boundary', 'line', 'divide', 'partition', 'demarcation'],
        'modern consequences': ['today', 'modern', 'current', 'still', 'now', 'contemporary', '2020', '2021', '2022', '2023', '2024', '2025', '2026'],
        'slavery': ['slave', 'slavery', 'enslaved', 'forced labor', 'plantation'],
        'independence': ['independence', 'independent', 'liberation', 'freedom', 'self-determination'],
    }

    topics_found = {}
    for topic, keywords in topic_keywords.items():
        count = sum(text_lower.count(kw) for kw in keywords)
        if count >= 3:
            topics_found[topic] = count

    # Sort topics by frequency
    sorted_topics = sorted(topics_found.items(), key=lambda x: x[1], reverse=True)

    return {
        'topics': [t[0] for t in sorted_topics],
        'topic_counts': dict(sorted_topics),
        'figures': top_figures[:10],
        'dates': [y for y, c in year_counts.most_common(15)],
        'sources_cited': sources_cited[:10],
        'has_primary_sources': has_primary_sources,
        'word_count': word_count,
        'estimated_minutes': round(word_count / 150, 1),
    }


def compare_coverage(
    our_topics: List[str],
    competitor_analyses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Compare our planned coverage against competitor videos.

    Args:
        our_topics: Topics/angles we plan to cover
        competitor_analyses: List of extract_topics_from_transcript results

    Returns:
        Gap analysis with: covered_by_all, covered_by_some, our_unique, their_unique
    """
    if not competitor_analyses:
        return {'error': 'No competitor analyses provided'}

    # Aggregate competitor topics
    all_competitor_topics = set()
    common_topics = None  # intersection
    for analysis in competitor_analyses:
        topics = set(analysis.get('topics', []))
        all_competitor_topics |= topics
        if common_topics is None:
            common_topics = topics
        else:
            common_topics &= topics

    common_topics = common_topics or set()
    our_set = set(our_topics)

    # Any competitors use primary sources?
    any_primary = any(a.get('has_primary_sources') for a in competitor_analyses)
    all_primary = all(a.get('has_primary_sources') for a in competitor_analyses)

    return {
        'standard_narrative': list(common_topics),
        'covered_by_some': list(all_competitor_topics - common_topics),
        'our_unique_angles': list(our_set - all_competitor_topics),
        'their_unique_not_ours': list(all_competitor_topics - our_set),
        'overlap': list(our_set & all_competitor_topics),
        'competitors_use_primary_sources': any_primary,
        'all_competitors_use_primary_sources': all_primary,
        'primary_source_advantage': not any_primary,
        'competitor_count': len(competitor_analyses),
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_gap_report(
    topic: str,
    competitor_videos: List[Dict[str, str]],
    competitor_analyses: List[Dict[str, Any]],
    comparison: Dict[str, Any],
) -> str:
    """Format a competitor gap analysis report."""
    lines = [
        f'# Competitor Gap Analysis: {topic}',
        '',
        f'**Videos analyzed:** {len(competitor_videos)}',
        '',
        '---',
        '',
        '## Competitor Videos',
        '',
        '| # | Title | Channel | Duration | Primary Sources? |',
        '|---|-------|---------|----------|-----------------|',
    ]

    for i, (vid, analysis) in enumerate(zip(competitor_videos, competitor_analyses), 1):
        ps = 'Yes' if analysis.get('has_primary_sources') else 'No'
        dur = f"~{analysis.get('estimated_minutes', '?')} min"
        lines.append(
            f"| {i} | {vid.get('title', '?')} | {vid.get('channel', '?')} | {dur} | {ps} |"
        )

    lines.extend(['', '---', ''])

    # Standard narrative
    lines.append('## Standard Narrative (All competitors cover this)')
    lines.append('')
    if comparison.get('standard_narrative'):
        for t in comparison['standard_narrative']:
            lines.append(f'- {t}')
    else:
        lines.append('- No topics covered by ALL competitors (diverse angles)')
    lines.append('')

    # What some cover
    if comparison.get('covered_by_some'):
        lines.append('## Partially Covered (Some competitors)')
        lines.append('')
        for t in comparison['covered_by_some']:
            lines.append(f'- {t}')
        lines.append('')

    # Key figures across competitors
    all_figures = []
    for a in competitor_analyses:
        all_figures.extend(a.get('figures', []))
    if all_figures:
        figure_counts = Counter(all_figures).most_common(10)
        lines.append('## Key Figures Mentioned')
        lines.append('')
        for fig, count in figure_counts:
            coverage = f"({count}/{len(competitor_analyses)} videos)"
            lines.append(f'- **{fig}** {coverage}')
        lines.append('')

    # Primary source advantage
    lines.append('## Primary Source Advantage')
    lines.append('')
    if comparison.get('primary_source_advantage'):
        lines.append('**NONE of the competitors use primary sources on screen.**')
        lines.append('This is your biggest differentiator. Show the actual documents.')
    elif comparison.get('all_competitors_use_primary_sources'):
        lines.append('All competitors cite sources. You need to go DEEPER — page numbers, original language, document close-ups.')
    else:
        lines.append('Some competitors cite sources but none show them on screen with the rigor you do.')
    lines.append('')

    # Gaps
    lines.append('## YOUR UNIQUE ANGLES (Gaps to fill)')
    lines.append('')
    if comparison.get('our_unique_angles'):
        for t in comparison['our_unique_angles']:
            lines.append(f'- **{t}** — not covered by any competitor')
    else:
        lines.append('- (Define your angles first, then re-run comparison)')
    lines.append('')

    # What they cover that you don't
    if comparison.get('their_unique_not_ours'):
        lines.append('## Competitor-Only Topics (Consider adding?)')
        lines.append('')
        for t in comparison['their_unique_not_ours']:
            lines.append(f'- {t}')
        lines.append('')

    # Recommendation
    lines.extend([
        '---',
        '',
        '## Recommendation',
        '',
        f'**Strongest angle:** Focus on topics in "YOUR UNIQUE ANGLES" above.',
        f'**Primary sources:** {"Major advantage — exploit it." if comparison.get("primary_source_advantage") else "Match or exceed competitor sourcing."}',
        f'**Standard narrative to transcend:** {", ".join(comparison.get("standard_narrative", ["N/A"]))}',
    ])

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Quick test: extract topics from a sample transcript
    if len(sys.argv) < 2:
        print("Usage: python tools/research/competitor_gap.py <transcript_file>")
        print("  Or pass a topic string to see planned search queries")
        sys.exit(1)

    arg = sys.argv[1]
    p = Path(arg)
    if p.exists():
        text = p.read_text(encoding='utf-8')
        result = extract_topics_from_transcript(text)
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Topic: {arg}")
        print(f"Search queries to run:")
        print(f'  1. "{arg}" site:youtube.com')
        print(f'  2. "{arg}" explained OR history OR documentary site:youtube.com')
        print(f"\nAfter finding videos, fetch transcripts with:")
        print(f"  python .claude/tools/get-transcript.py <video_id>")
