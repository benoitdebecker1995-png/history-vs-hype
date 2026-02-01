"""
Production Constraint Detection Module

Keyword-based detection for production feasibility: animation requirements (hard blocks)
and document-friendliness scoring (0-4 scale). Used in Phase 17 format filtering to
fail fast on incompatible topics before investing research hours.

Usage:
    from tools.discovery.format_filters import is_animation_required, calculate_document_score

    # Check if topic requires animation (hard block)
    result = is_animation_required('How Quantum Mechanics Work')
    if result['is_blocked']:
        print(f"Skip topic: {result['reason']}")

    # Score document-friendliness (0-4, higher = better fit)
    score = calculate_document_score('The Treaty That Split a Country')
    print(f"Document score: {score}/4")
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

    return {
        'is_viable': is_viable,
        'animation_check': animation_check,
        'document_score': document_score,
        'recommendation': recommendation,
        'production_notes': production_notes
    }
