"""
Production Constraint Detection Module

Keyword-based detection for production feasibility: animation requirements (hard blocks),
document-friendliness scoring (0-4 scale), and academic source hints. Used in Phase 17
format filtering to fail fast on incompatible topics before investing research hours.

Usage:
    from tools.discovery.format_filters import is_animation_required, calculate_document_score

    # Check if topic requires animation (hard block)
    result = is_animation_required('How Quantum Mechanics Work')
    if result['is_blocked']:
        print(f"Skip topic: {result['reason']}")

    # Score document-friendliness (0-4, higher = better fit)
    score = calculate_document_score('The Treaty That Split a Country')
    print(f"Document score: {score}/4")

    # Get source hints for pre-research screening
    hints = get_source_hints('The Treaty of Versailles')
    print(f"Try searching: {hints['queries'][0]}")

CLI Usage:
    python format_filters.py "The Treaty of Versailles"
    python format_filters.py "How Quantum Mechanics Work" --json
"""

from typing import Dict, Any, List


# Keywords that strongly indicate animation requirement
ANIMATION_REQUIRED_KEYWORDS = [
    # Physics/Science visualization
    'quantum', 'molecular', 'atomic', 'particle', 'chemical reaction',
    'biological process', 'cellular', 'genetic', 'dna', 'rna',
    'photosynthesis', 'metabolism', 'electron', 'neutron', 'proton',
    # Abstract/Theoretical
    'theoretical', 'simulation', 'model', 'mechanism', 'how it works',
    'visualize', 'visualizing', 'animated', 'animation',
    # Process-heavy (needs step-by-step visualization)
    'step by step', 'process of', 'stages of', 'phases of',
    'evolution of', 'development of', 'formation of',
    # Scale-based (microscopic or cosmic)
    'microscopic', 'microscale', 'nanoscale', 'cosmic', 'universe',
    'solar system', 'galaxy', 'black hole', 'supernova',
    # Technical diagrams
    'how computers', 'how engines', 'how machines', 'circuit',
    'algorithm', 'data structure', 'neural network'
]

# Keywords that indicate documentary format is viable (overrides animation signals)
DOCUMENTARY_SAFE_KEYWORDS = [
    # Primary source indicators
    'treaty', 'agreement', 'accord', 'protocol', 'convention',
    'document', 'archive', 'manuscript', 'letter', 'correspondence',
    'court', 'ruling', 'verdict', 'judgment', 'case',
    # Visual evidence
    'map', 'border', 'territory', 'frontier', 'boundary',
    'photo', 'photograph', 'footage', 'recording', 'interview',
    # Historical events
    'war', 'battle', 'siege', 'invasion', 'occupation',
    'revolution', 'coup', 'uprising', 'rebellion',
    # Legal/Political structures
    'constitution', 'law', 'statute', 'decree', 'edict',
    'empire', 'kingdom', 'dynasty', 'colony', 'colonial',
    # Documentary subjects
    'genocide', 'massacre', 'atrocity', 'war crimes',
    'census', 'statistics', 'demographics', 'population'
]

# Point values for document-friendly keywords
DOCUMENT_FRIENDLY_KEYWORDS = {
    # Primary source gold (treaty-heavy = perfect fit)
    'treaty': 3, 'agreement': 3, 'accord': 3, 'protocol': 3,
    'court': 3, 'ruling': 3, 'verdict': 3, 'icj': 3,
    'map': 3, 'border': 3, 'territory': 3, 'constitution': 3,
    'document': 3, 'archive': 3, 'manuscript': 3,
    # Strong document indicators
    'law': 2, 'claim': 2, 'dispute': 2, 'colonial': 2,
    'sovereignty': 2, 'jurisdiction': 2, 'annexation': 2,
    'occupation': 2, 'referendum': 2, 'election': 2,
    # Moderate document indicators
    'war': 1, 'battle': 1, 'history': 1, 'historical': 1,
    'empire': 1, 'kingdom': 1, 'dynasty': 1, 'century': 1,
    'ancient': 1, 'medieval': 1, 'modern': 1
}

# Point values for concept-heavy keywords (reduce document score)
CONCEPT_HEAVY_KEYWORDS = {
    # Abstract/Philosophical
    'philosophy': -2, 'philosophical': -2, 'theory': -2, 'theoretical': -2,
    'concept': -2, 'framework': -2, 'paradigm': -2, 'model': -2,
    # Ideological
    'ideology': -1, 'belief': -1, 'principle': -2, 'idea': -1,
    'ism': -1, 'movement': -1, 'school of thought': -2,
    # Speculative
    'hypothesis': -2, 'speculation': -2, 'what if': -2, 'imagine': -1,
    # Process-focused (hard to document)
    'how to': -1, 'step by step': -2, 'guide': -1, 'tutorial': -2
}

# Academic publisher and database patterns for source hints
PUBLISHER_PATTERNS = {
    'university_press': [
        'cambridge.org',
        'oup.com',
        'press.princeton.edu',
        'press.uchicago.edu',
        'yalebooks.yale.edu',
        'hup.harvard.edu',
        'cornellpress.cornell.edu',
    ],
    'academic_databases': [
        'jstor.org',
        'academia.edu',
        'scholar.google.com',
        'worldcat.org',
    ],
    'archives': [
        'nationalarchives.gov.uk',
        'archives.gov',
        'europeana.eu',
        'loc.gov',
    ]
}

# Source type indicators based on topic keywords
SOURCE_TYPE_INDICATORS = {
    'primary': ['treaty', 'agreement', 'document', 'archive', 'manuscript',
                'letter', 'correspondence', 'decree', 'edict', 'constitution',
                'court', 'ruling', 'verdict', 'case'],
    'monograph': ['history', 'historical', 'war', 'empire', 'colonial',
                  'dynasty', 'kingdom', 'century', 'medieval', 'ancient'],
    'journal': ['dispute', 'claim', 'sovereignty', 'jurisdiction',
                'border', 'territory', 'referendum', 'election']
}


def is_animation_required(title: str, description: str = '') -> Dict[str, Any]:
    """
    Detect if a topic requires animation to explain effectively.

    Animation-required topics are hard blocks for the channel (documentary format only).
    Returns a dict with blocking status, reasoning, and confidence level.

    Args:
        title: Video/topic title
        description: Optional description for additional context

    Returns:
        {
            'is_blocked': bool,      # True if animation required (skip this topic)
            'reason': str,           # Human-readable explanation
            'confidence': float,     # 0-1, lower if mixed signals
            'matched_keywords': list # Keywords that triggered detection
        }

    Examples:
        >>> is_animation_required("How Quantum Mechanics Work")
        {'is_blocked': True, 'reason': 'Requires visualization...', ...}

        >>> is_animation_required("The Treaty That Changed Europe")
        {'is_blocked': False, 'reason': 'Documentary-viable topic', ...}
    """
    combined_text = (title + ' ' + description).lower()

    # Find animation-required keyword matches
    animation_matches = []
    for keyword in ANIMATION_REQUIRED_KEYWORDS:
        if keyword in combined_text:
            animation_matches.append(keyword)

    # Find documentary-safe keyword matches (can override animation signals)
    safe_matches = []
    for keyword in DOCUMENTARY_SAFE_KEYWORDS:
        if keyword in combined_text:
            safe_matches.append(keyword)

    # No animation keywords = not blocked
    if not animation_matches:
        return {
            'is_blocked': False,
            'reason': 'Documentary-viable topic',
            'confidence': 0.9,
            'matched_keywords': []
        }

    # Animation keywords but also safe keywords = mixed signals
    if animation_matches and safe_matches:
        # More safe keywords = probably documentary-viable
        if len(safe_matches) >= len(animation_matches):
            return {
                'is_blocked': False,
                'reason': f'Mixed signals but documentary elements dominate ({len(safe_matches)} documentary vs {len(animation_matches)} animation keywords)',
                'confidence': 0.6,
                'matched_keywords': animation_matches
            }
        else:
            return {
                'is_blocked': True,
                'reason': f'Animation likely required despite documentary elements ({len(animation_matches)} animation vs {len(safe_matches)} documentary keywords)',
                'confidence': 0.5,
                'matched_keywords': animation_matches
            }

    # Animation keywords only = blocked
    return {
        'is_blocked': True,
        'reason': f'Topic requires visualization/animation to explain effectively. Matched: {", ".join(animation_matches[:3])}',
        'confidence': 0.85,
        'matched_keywords': animation_matches
    }


def calculate_document_score(title: str, description: str = '') -> int:
    """
    Calculate document-friendliness score for a topic.

    Score indicates how well the topic fits the channel's document-heavy format.
    Higher scores mean more primary sources, treaties, maps, and visual evidence.

    Scale:
        4 = Treaty-heavy (perfect fit: court cases, territorial disputes, treaties)
        3 = Document-rich (good fit: colonial history, wars with documented evidence)
        2 = Mixed (acceptable: historical narratives with some document support)
        1 = Concept-leaning (marginal: needs careful framing)
        0 = Concept-heavy (poor fit: philosophy, theory, abstract ideas)

    Args:
        title: Video/topic title
        description: Optional description for additional context

    Returns:
        Integer 0-4 representing document-friendliness

    Examples:
        >>> calculate_document_score("The Treaty That Split a Country")
        4

        >>> calculate_document_score("The Philosophy of Freedom")
        0
    """
    combined_text = (title + ' ' + description).lower()

    # Start at baseline (neutral topic)
    score = 2.0

    # Add points for document-friendly keywords
    for keyword, points in DOCUMENT_FRIENDLY_KEYWORDS.items():
        if keyword in combined_text:
            score += points

    # Subtract points for concept-heavy keywords
    for keyword, points in CONCEPT_HEAVY_KEYWORDS.items():
        if keyword in combined_text:
            score += points  # points are negative

    # Clamp to 0-4 range
    score = max(0, min(4, score))

    return int(round(score))


def evaluate_production_constraints(
    title: str,
    description: str = ''
) -> Dict[str, Any]:
    """
    Comprehensive production constraint evaluation.

    Combines animation detection and document scoring into a single evaluation.
    Use this for complete topic screening before investing research time.

    Args:
        title: Video/topic title
        description: Optional description for additional context

    Returns:
        {
            'is_viable': bool,           # True if topic can be produced
            'animation_check': dict,     # Full is_animation_required() result
            'document_score': int,       # 0-4 document-friendliness score
            'recommendation': str,       # Action recommendation
            'production_notes': list     # Additional production considerations
        }

    Examples:
        >>> result = evaluate_production_constraints("The Treaty of Versailles")
        >>> result['is_viable']
        True
        >>> result['document_score']
        4
    """
    animation_check = is_animation_required(title, description)
    document_score = calculate_document_score(title, description)

    # Determine viability
    is_viable = not animation_check['is_blocked']

    # Build recommendation
    if animation_check['is_blocked']:
        recommendation = 'SKIP: Topic requires animation format'
    elif document_score >= 3:
        recommendation = 'PROCEED: Excellent fit for document-heavy format'
    elif document_score >= 2:
        recommendation = 'PROCEED WITH CARE: Ensure sufficient primary sources'
    else:
        recommendation = 'RECONSIDER: Topic may lack visual evidence'

    # Production notes
    production_notes = []
    if document_score >= 3:
        production_notes.append('Look for treaty texts, court documents, historical maps')
    if document_score == 2:
        production_notes.append('May need to supplement with interview clips or archival footage')
    if document_score <= 1:
        production_notes.append('Consider reframing around a specific document or event')
    if animation_check['confidence'] < 0.7:
        production_notes.append('Mixed signals - manual review recommended')

    # Get source hints
    source_hints = get_source_hints(title, description)

    return {
        'is_viable': is_viable,
        'animation_check': animation_check,
        'document_score': document_score,
        'source_hints': source_hints,
        'recommendation': recommendation,
        'production_notes': production_notes
    }


def get_source_hints(title: str, description: str = '') -> Dict[str, Any]:
    """
    Generate academic source search query hints for a topic.

    Creates search queries that user can run manually in Google Scholar,
    JSTOR, WorldCat, etc. No HTTP requests made - query generation only.

    Args:
        title: Video/topic title
        description: Optional description for additional context

    Returns:
        {
            'queries': list,          # Search strings ready to copy-paste
            'expected_types': list,   # ['monograph', 'journal', 'primary']
            'publisher_sites': list,  # Recommended sites to check
            'confidence': float       # 0-1 based on topic specificity
        }

    Examples:
        >>> hints = get_source_hints("The Treaty of Versailles")
        >>> hints['queries'][0]
        '"Treaty of Versailles" site:cambridge.org OR site:oup.com'

        >>> hints['expected_types']
        ['primary', 'monograph', 'journal']
    """
    combined_text = (title + ' ' + description).lower()

    # Determine expected source types based on topic keywords
    expected_types = []
    for source_type, keywords in SOURCE_TYPE_INDICATORS.items():
        for keyword in keywords:
            if keyword in combined_text:
                if source_type not in expected_types:
                    expected_types.append(source_type)
                break

    # Default to monograph if no specific types detected
    if not expected_types:
        expected_types = ['monograph']

    # Build search queries
    queries = []

    # Clean title for search (use as-is, quotes will be added)
    search_term = title.strip()

    # University press search
    press_sites = ' OR '.join(f'site:{s}' for s in PUBLISHER_PATTERNS['university_press'][:3])
    queries.append(f'"{search_term}" {press_sites}')

    # Academic database search
    if 'journal' in expected_types or 'primary' in expected_types:
        queries.append(f'"{search_term}" site:jstor.org peer-reviewed')

    # Primary source / archive search
    if 'primary' in expected_types:
        queries.append(f'"{search_term}" primary source archive')

    # General scholarly search
    queries.append(f'"{search_term}" "university press" academic')

    # Calculate confidence based on specificity
    # More specific topics (with document-friendly keywords) = higher confidence
    specificity_score = 0
    for keyword in DOCUMENT_FRIENDLY_KEYWORDS:
        if keyword in combined_text:
            specificity_score += 1

    if specificity_score >= 3:
        confidence = 0.9
    elif specificity_score >= 2:
        confidence = 0.7
    elif specificity_score >= 1:
        confidence = 0.5
    else:
        confidence = 0.3

    return {
        'queries': queries,
        'expected_types': expected_types,
        'publisher_sites': PUBLISHER_PATTERNS['university_press'][:5],
        'confidence': confidence
    }


def main():
    """CLI entry point for production constraint evaluation."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description='Evaluate production constraints for a topic',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python format_filters.py "The Treaty of Versailles"
  python format_filters.py "How Quantum Mechanics Work"
  python format_filters.py "Medieval border disputes" --json
  python format_filters.py "Sykes-Picot Agreement" -v
        """
    )

    parser.add_argument('topic', help='Topic to evaluate')
    parser.add_argument('--json', action='store_true',
                        help='Output JSON format')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output with details')

    args = parser.parse_args()

    # Run evaluation
    result = evaluate_production_constraints(args.topic)

    # JSON output
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    # Pretty print output
    print(f"\n{'='*70}")
    print(f"  Production Constraints: {args.topic}")
    print(f"{'='*70}\n")

    # Verdict
    if result['is_viable']:
        if result['document_score'] >= 3:
            verdict = 'PROCEED'
            verdict_symbol = '\\u2713'  # checkmark
        else:
            verdict = 'REVIEW'
            verdict_symbol = '!'
    else:
        verdict = 'SKIP'
        verdict_symbol = 'X'

    print(f"VERDICT: {verdict}")

    # Document score with visual bar (ASCII-safe)
    score = result['document_score']
    bar_filled = score * 5
    bar_empty = 20 - bar_filled
    bar = '#' * bar_filled + '-' * bar_empty  # ASCII-safe characters
    print(f"  Document Score:     {score}/4  [{bar}]")

    # Animation risk
    anim = result['animation_check']
    risk_level = 'HIGH' if anim['is_blocked'] else 'LOW' if anim['confidence'] > 0.7 else 'MEDIUM'
    print(f"  Animation Risk:     {risk_level:4s} (confidence: {anim['confidence']:.2f})")
    print()

    # Source hints
    hints = result['source_hints']
    print("SOURCE HINTS:")
    print(f"  Expected types: {', '.join(hints['expected_types'])}")
    print()
    print("  Try these searches:")
    for i, query in enumerate(hints['queries'][:3], 1):
        print(f"  {i}. {query}")
    print()

    # Production notes
    if result['production_notes']:
        print("NOTES:")
        for note in result['production_notes']:
            print(f"  - {note}")
        print()

    # Blocked reason
    if anim['is_blocked']:
        print(f"BLOCKED: {anim['reason']}")
        print()

    # Verbose: show matched keywords
    if args.verbose:
        print("DETAILED ANALYSIS:")
        print(f"  Is viable: {result['is_viable']}")
        print(f"  Recommendation: {result['recommendation']}")
        if anim['matched_keywords']:
            print(f"  Animation keywords: {', '.join(anim['matched_keywords'][:5])}")
        print(f"  Source confidence: {hints['confidence']:.2f}")
        print()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
