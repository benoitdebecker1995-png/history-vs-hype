"""
Intent Classification Module

Classifies keywords and titles by search intent using 6 custom history-niche categories.
Provides DNA fit scoring to identify channel-appropriate topics vs clickbait.

Usage:
    CLI:
        python intent_mapper.py "dark ages myth"
        python intent_mapper.py "why crusades were defensive" --json
        python intent_mapper.py --batch "dark ages, crusades, colonialism"

    Python:
        from intent_mapper import classify_intent, calculate_dna_fit, classify_title

        result = classify_intent('dark ages myth')
        print(result['primary']['category'])  # 'MYTH_BUSTING'

        fit = calculate_dna_fit('secret history they don\'t want you to know')
        print(fit['recommendation'])  # 'POOR_FIT'

Dependencies:
    - database.py (Phase 13-01) for storing classifications
"""

import sys
import json
import re
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from pathlib import Path

# Intent categories with pattern matching
INTENT_CATEGORIES = {
    'MYTH_BUSTING': {
        'patterns': ['myth', 'true', 'false', 'really', 'actually', 'fact check', 'debunk', 'lie', 'wrong'],
        'description': 'Correcting historical misconceptions',
        'examples': ['dark ages myth', 'did crusades really happen', 'flat earth medieval']
    },
    'TERRITORIAL_DISPUTE': {
        'patterns': ['border', 'dispute', 'conflict', 'claim', 'territory', 'land', 'war', 'occupied'],
        'description': 'Border conflicts and territorial claims',
        'examples': ['bir tawil unclaimed', 'belize guatemala border', 'somaliland recognition']
    },
    'PRIMARY_SOURCE': {
        'patterns': ['document', 'treaty', 'original', 'manuscript', 'archive', 'letter', 'text'],
        'description': 'Primary source reveals and analysis',
        'examples': ['treaty of guadalupe hidalgo text', 'sykes picot agreement document']
    },
    'MECHANISM_EXPLAINER': {
        'patterns': ['how did', 'how was', 'how to', 'process', 'method', 'system', 'worked'],
        'description': 'Explaining historical mechanisms and processes',
        'examples': ['how did USSR collapse', 'how was berlin wall built', 'how empires fall']
    },
    'TIMELINE_CORRECTION': {
        'patterns': ['when', 'timeline', 'chronology', 'date', 'year', 'century', 'era', 'period'],
        'description': 'Correcting timeline misconceptions',
        'examples': ['when did somaliland declare independence', 'dark ages timeline']
    },
    'IDEOLOGICAL_NARRATIVE': {
        'patterns': ['why', 'ideology', 'belief', 'narrative', 'claim', 'said', 'argued'],
        'description': 'Analyzing ideological claims and narratives',
        'examples': ['why crusades were defensive', 'communism definition', 'colonialism justified']
    }
}

# DNA fit scoring signals
DNA_FIT_SIGNALS = {
    'positive': [
        'evidence', 'document', 'source', 'proof', 'archive', 'manuscript',
        'treaty', 'original', 'historical', 'primary', 'fact', 'debunk',
        'verify', 'analysis', 'study', 'research', 'scholar', 'academic'
    ],
    'negative': [
        'conspiracy', 'secret', 'hidden', 'shocking', 'you won\'t believe',
        'breaking', 'exposed', 'truth they', 'don\'t want you', 'mainstream',
        'they\'re hiding', 'wake up', 'sheeple'
    ]
}


def classify_intent(query: str, min_confidence: float = 0.3) -> Dict[str, Any]:
    """
    Classify search intent of a keyword/title against 6 history-niche categories.

    Matches query text against category patterns and calculates confidence scores.
    Returns primary intent (highest confidence) and optional secondary intent.

    Args:
        query: Keyword or title to classify
        min_confidence: Minimum confidence threshold (0-1, default 0.3)

    Returns:
        dict:
            {
                'query': 'dark ages myth',
                'primary': {
                    'category': 'MYTH_BUSTING',
                    'confidence': 0.67,
                    'matched': ['myth']
                },
                'secondary': {
                    'category': 'TIMELINE_CORRECTION',
                    'confidence': 0.33,
                    'matched': ['ages']
                } or None,
                'all_matches': [...],  # Sorted by confidence
                'classified_at': 'ISO timestamp'
            }

        If no matches above min_confidence:
            {
                'query': '...',
                'primary': None,
                'secondary': None,
                'all_matches': [],
                'note': 'No intent categories matched above threshold',
                'classified_at': 'ISO timestamp'
            }
    """
    query_lower = query.lower()
    matches = []

    # Match against each category
    for category, data in INTENT_CATEGORIES.items():
        patterns = data['patterns']
        matched_patterns = []

        for pattern in patterns:
            # Check if pattern appears in query (substring match)
            # Use word boundary checking for multi-word patterns
            if ' ' in pattern:
                # Multi-word pattern: exact phrase match
                if pattern in query_lower:
                    matched_patterns.append(pattern)
            else:
                # Single word: check as substring (matches "myth" in "mythology")
                if pattern in query_lower:
                    matched_patterns.append(pattern)

        if matched_patterns:
            # Calculate confidence based on number of matches (not ratio)
            # 1 match = 0.33, 2 matches = 0.66, 3+ matches = 1.0
            # This allows single strong matches to qualify
            confidence = min(len(matched_patterns) * 0.33, 1.0)

            matches.append({
                'category': category,
                'confidence': confidence,
                'matched': matched_patterns
            })

    # Sort by confidence (highest first)
    matches.sort(key=lambda m: m['confidence'], reverse=True)

    # Filter by minimum confidence
    qualifying_matches = [m for m in matches if m['confidence'] >= min_confidence]

    # Determine primary and secondary
    primary = qualifying_matches[0] if qualifying_matches else None
    secondary = qualifying_matches[1] if len(qualifying_matches) > 1 else None

    result = {
        'query': query,
        'primary': primary,
        'secondary': secondary,
        'all_matches': qualifying_matches,
        'classified_at': datetime.now(timezone.utc).isoformat() + 'Z'
    }

    if not primary:
        result['note'] = 'No intent categories matched above threshold'

    return result


def calculate_dna_fit(query: str) -> Dict[str, Any]:
    """
    Score how well a query fits channel's documentary/evidence style.

    Identifies positive signals (evidence-based, academic) and negative signals
    (clickbait, conspiracy) to determine if topic aligns with channel DNA.

    Args:
        query: Keyword or title to evaluate

    Returns:
        dict:
            {
                'query': '...',
                'fit_score': 0.0-1.0,
                'positive_matches': ['evidence', 'document'],
                'negative_matches': ['secret'],
                'recommendation': 'GOOD_FIT' | 'MARGINAL' | 'POOR_FIT',
                'reason': 'Explanation of recommendation'
            }

        Recommendation thresholds:
            GOOD_FIT: >= 0.6
            MARGINAL: 0.4-0.6
            POOR_FIT: < 0.4
    """
    query_lower = query.lower()

    positive_matches = []
    negative_matches = []

    # Check positive signals
    for signal in DNA_FIT_SIGNALS['positive']:
        if signal in query_lower:
            positive_matches.append(signal)

    # Check negative signals
    for signal in DNA_FIT_SIGNALS['negative']:
        if signal in query_lower:
            negative_matches.append(signal)

    # Calculate fit score
    # Positive signals increase score, negative signals decrease
    positive_weight = len(positive_matches) * 0.2  # Each positive signal = +0.2
    negative_weight = len(negative_matches) * 0.3  # Each negative signal = -0.3

    # Base score starts at 0.5 (neutral)
    fit_score = 0.5 + positive_weight - negative_weight

    # Clamp to 0-1 range
    fit_score = max(0.0, min(1.0, fit_score))

    # Determine recommendation
    if fit_score >= 0.6:
        recommendation = 'GOOD_FIT'
        reason = 'Evidence-based, documentary tone'
    elif fit_score >= 0.4:
        recommendation = 'MARGINAL'
        reason = 'Neutral tone - could work with proper framing'
    else:
        recommendation = 'POOR_FIT'
        reason = 'Clickbait/conspiracy signals detected'

    return {
        'query': query,
        'fit_score': round(fit_score, 2),
        'positive_matches': positive_matches,
        'negative_matches': negative_matches,
        'recommendation': recommendation,
        'reason': reason
    }


def classify_title(title: str) -> Dict[str, Any]:
    """
    Convenience wrapper: classify intent + calculate DNA fit in one call.

    Args:
        title: Title or keyword to classify

    Returns:
        dict combining intent classification and DNA fit:
            {
                'query': '...',
                'intent': {
                    'primary': {...},
                    'secondary': {...} or None,
                    'all_matches': [...]
                },
                'dna_fit': {
                    'fit_score': 0.0-1.0,
                    'recommendation': '...',
                    'positive_matches': [...],
                    'negative_matches': [...]
                },
                'classified_at': 'ISO timestamp'
            }
    """
    intent = classify_intent(title)
    dna_fit = calculate_dna_fit(title)

    return {
        'query': title,
        'intent': {
            'primary': intent['primary'],
            'secondary': intent['secondary'],
            'all_matches': intent['all_matches']
        },
        'dna_fit': {
            'fit_score': dna_fit['fit_score'],
            'recommendation': dna_fit['recommendation'],
            'reason': dna_fit['reason'],
            'positive_matches': dna_fit['positive_matches'],
            'negative_matches': dna_fit['negative_matches']
        },
        'classified_at': intent['classified_at']
    }


def save_classification_to_db(keyword_id: int, classification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save intent classification to database for a keyword.

    Args:
        keyword_id: Keyword ID from keywords table
        classification: Result from classify_intent()

    Returns:
        {'status': 'saved', 'intents_saved': N} on success
        {'error': msg} on failure
    """
    try:
        from database import KeywordDB

        db = KeywordDB()
        intents_saved = 0

        # Save primary intent
        if classification.get('primary'):
            primary = classification['primary']
            result = db.set_intent(
                keyword_id=keyword_id,
                category=primary['category'],
                confidence=primary['confidence'],
                is_primary=True
            )
            if 'error' not in result:
                intents_saved += 1

        # Save secondary intent
        if classification.get('secondary'):
            secondary = classification['secondary']
            result = db.set_intent(
                keyword_id=keyword_id,
                category=secondary['category'],
                confidence=secondary['confidence'],
                is_primary=False
            )
            if 'error' not in result:
                intents_saved += 1

        db.close()

        return {
            'status': 'saved',
            'intents_saved': intents_saved
        }

    except ImportError:
        return {
            'error': 'database.py not available - cannot save to database'
        }
    except Exception as e:
        return {
            'error': f'Failed to save classification: {type(e).__name__}',
            'details': str(e)
        }


def format_classification_text(classification: Dict[str, Any]) -> str:
    """
    Format classification as human-readable text.

    Args:
        classification: Result from classify_intent() or classify_title()

    Returns:
        Formatted text string
    """
    lines = []

    query = classification.get('query', 'Unknown')
    lines.append(f"Query: {query}")
    lines.append("")

    # Intent classification
    if 'intent' in classification:
        # Full classification (from classify_title)
        intent = classification['intent']
    else:
        # Direct classification (from classify_intent)
        intent = classification

    primary = intent.get('primary')
    secondary = intent.get('secondary')

    if primary:
        lines.append(f"Primary Intent: {primary['category']}")
        lines.append(f"  Confidence: {primary['confidence']:.2f}")
        lines.append(f"  Matched: {', '.join(primary['matched'])}")

        # Get category description
        category_info = INTENT_CATEGORIES.get(primary['category'])
        if category_info:
            lines.append(f"  Description: {category_info['description']}")

        lines.append("")
    else:
        lines.append("Primary Intent: None (no matches above threshold)")
        lines.append("")

    if secondary:
        lines.append(f"Secondary Intent: {secondary['category']}")
        lines.append(f"  Confidence: {secondary['confidence']:.2f}")
        lines.append(f"  Matched: {', '.join(secondary['matched'])}")
        lines.append("")

    # DNA fit (if present)
    dna_fit = classification.get('dna_fit')
    if dna_fit:
        lines.append(f"Channel DNA Fit: {dna_fit['recommendation']}")
        lines.append(f"  Score: {dna_fit['fit_score']}")
        lines.append(f"  Reason: {dna_fit['reason']}")

        if dna_fit['positive_matches']:
            lines.append(f"  Positive signals: {', '.join(dna_fit['positive_matches'])}")

        if dna_fit['negative_matches']:
            lines.append(f"  Negative signals: {', '.join(dna_fit['negative_matches'])}")

        lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Classify search intent and calculate channel DNA fit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.discovery.intent_mapper "dark ages myth"
  python -m tools.discovery.intent_mapper "why crusades were defensive" --json
  python -m tools.discovery.intent_mapper --batch "dark ages, crusades, colonialism" """,
    )
    parser.add_argument(
        "query", nargs="?",
        help="Query or title to classify (omit when using --batch)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON (default: human-readable text)",
    )
    parser.add_argument(
        "--batch", metavar="QUERIES",
        help="Classify multiple queries (comma-separated list)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    if args.batch:
        queries = [q.strip() for q in args.batch.split(',')]
        results = []

        for query in queries:
            result = classify_title(query)
            results.append(result)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for i, result in enumerate(results):
                if i > 0:
                    print("\n" + "="*60 + "\n")
                print(format_classification_text(result))

    elif args.query:
        result = classify_title(args.query)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_classification_text(result))

    else:
        parser.print_help()
        sys.exit(1)
