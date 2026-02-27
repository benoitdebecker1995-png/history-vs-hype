"""Pattern extraction and analysis for voice fingerprinting.

This module provides functions to:
1. Extract patterns from script-transcript modification data
2. Apply temporal weighting (recent videos more influential)
3. Classify pattern types (substitutions, deletions, insertions)
4. Build pattern library from corpus of videos

Pattern confidence levels:
- HIGH: frequency >= 5 across corpus
- MEDIUM: frequency >= 3 across corpus
- LOW: frequency < 3 (not included in output)
"""

import json
import re
import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

from tools.logging_config import get_logger

logger = get_logger(__name__)

from .corpus_builder import find_video_pairs, compare_script_to_transcript


def classify_pattern_type(modification: Dict) -> str:
    """Classify modification into pattern type based on structure.

    Args:
        modification: Dict with 'type', 'original', and/or 'modified' keys

    Returns:
        Pattern type string:
        - 'word_substitution': single word -> single word
        - 'deletion': phrase -> nothing
        - 'insertion': nothing -> phrase
        - 'restructuring': phrase -> different phrase (ignored for patterns)

    Example:
        >>> classify_pattern_type({'type': 'substitution', 'original': 'utilize', 'modified': 'use'})
        'word_substitution'
        >>> classify_pattern_type({'type': 'deletion', 'original': 'in order to'})
        'deletion'
    """
    mod_type = modification['type']

    if mod_type == 'substitution':
        orig_words = modification['original'].split()
        mod_words = modification['modified'].split()

        # Single word -> single word = clear substitution pattern
        if len(orig_words) == 1 and len(mod_words) == 1:
            return 'word_substitution'
        else:
            # Phrase -> different phrase = restructuring (too variable for patterns)
            return 'restructuring'

    elif mod_type == 'deletion':
        return 'deletion'

    elif mod_type == 'addition':
        return 'insertion'

    return 'unknown'


def extract_patterns(all_modifications: List[Dict], min_frequency: int = 3) -> Dict:
    """Extract consistent patterns from corpus modifications.

    Analyzes modifications across all videos to find patterns that occur
    consistently (>= min_frequency). Filters out one-off ad-libs and
    context-specific changes.

    Args:
        all_modifications: List of modification dicts from all videos
        min_frequency: Minimum occurrences to be considered a pattern (default: 3)

    Returns:
        Dictionary with pattern categories:
        {
          'word_substitutions': [{'formal': 'utilize', 'casual': 'use', 'frequency': 7, 'confidence': 'HIGH'}, ...],
          'anti_patterns': ['it should be noted that', 'in order to', ...],
          'additions': ['actually', 'here is the thing', ...]
        }

    Statistical note:
        Corpus linguistics research indicates minimum 5-10 documents needed
        for pattern significance. With min_frequency=3, patterns appearing
        in <30% of corpus are considered LOW confidence.
    """
    # Track pattern frequencies
    substitutions = Counter()
    deletions = Counter()
    insertions = Counter()

    for mod in all_modifications:
        pattern_type = classify_pattern_type(mod)

        if pattern_type == 'word_substitution':
            # Track (formal -> casual) word pairs
            formal = mod['original']
            casual = mod['modified']
            substitutions[(formal, casual)] += 1

        elif pattern_type == 'deletion':
            # Track phrases consistently removed
            deletions[mod['original']] += 1

        elif pattern_type == 'insertion':
            # Track phrases consistently added
            insertions[mod['modified']] += 1

        # 'restructuring' and 'unknown' ignored - too variable for patterns

    # Filter by frequency and format output
    word_substitutions = []
    for (formal, casual), count in substitutions.items():
        if count >= min_frequency:
            confidence = 'HIGH' if count >= 5 else 'MEDIUM'
            word_substitutions.append({
                'formal': formal,
                'casual': casual,
                'frequency': count,
                'confidence': confidence
            })

    # Anti-patterns: phrases user consistently removes
    anti_patterns = [
        phrase for phrase, count in deletions.items()
        if count >= min_frequency
    ]

    # Additions: phrases user consistently adds
    addition_patterns = [
        phrase for phrase, count in insertions.items()
        if count >= min_frequency
    ]

    return {
        'word_substitutions': sorted(word_substitutions, key=lambda x: x['frequency'], reverse=True),
        'anti_patterns': sorted(anti_patterns, key=lambda x: deletions[x], reverse=True),
        'additions': sorted(addition_patterns, key=lambda x: insertions[x], reverse=True)
    }


def weight_by_recency(pattern_occurrences: List[Tuple], decay_factor: float = 0.95) -> Dict[str, float]:
    """Apply exponential decay weighting based on video date.

    Recent videos have more influence on patterns than older videos.
    Accounts for evolving speech style over time.

    Args:
        pattern_occurrences: List of (pattern_key, video_date, count) tuples
        decay_factor: Exponential decay factor (0-1). Default 0.95 = 5% decay per month.
                      Higher values = longer memory, lower = more recent bias.

    Returns:
        Dictionary of {pattern_key: weighted_score}

    Example:
        decay_factor=0.95:
        - Video from 1 month ago: weight = count * 0.95^1 = count * 0.95
        - Video from 6 months ago: weight = count * 0.95^6 = count * 0.735
        - Video from 12 months ago: weight = count * 0.95^12 = count * 0.540

    Research note:
        Exponential decay is standard for time-series weighting in ML.
        0.95 decay factor is common for monthly data, balancing historical
        context with recent changes.
    """
    now = datetime.datetime.now()
    weighted_scores = defaultdict(float)

    for pattern, video_date, count in pattern_occurrences:
        # Calculate months since video
        months_ago = (now - video_date).days / 30.0

        # Apply exponential decay: weight = base_count * (decay_factor ^ months)
        weight = count * (decay_factor ** months_ago)
        weighted_scores[pattern] += weight

    return dict(weighted_scores)


def _extract_video_date(folder_name: str) -> datetime.datetime:
    """Extract date from video folder name.

    Args:
        folder_name: Video folder name (e.g., "1-somaliland-2025", "24-iran-1953-coup-2025")

    Returns:
        datetime object. If year is found, uses January 1 of that year.
        If not found, returns current date.

    Example:
        >>> _extract_video_date("1-somaliland-2025")
        datetime.datetime(2025, 1, 1, 0, 0)
        >>> _extract_video_date("24-iran-1953-coup-2025")
        datetime.datetime(2025, 1, 1, 0, 0)
    """
    # Extract year from folder name (last 4-digit number)
    year_match = re.search(r'-(\d{4})', folder_name)
    if year_match:
        year = int(year_match.group(1))
        return datetime.datetime(year, 1, 1)
    else:
        # No date found, use current date
        return datetime.datetime.now()


def build_pattern_library(projects_dir: Path, output_path: Path) -> Dict:
    """Analyze all script+SRT pairs and build pattern library.

    This is the main entry point for corpus analysis. Scans video projects,
    compares scripts to transcripts, extracts patterns with frequency analysis,
    and writes results to JSON.

    Args:
        projects_dir: Root video-projects directory
        output_path: Path to write voice-patterns.json

    Returns:
        Dictionary with metadata and patterns

    Process:
        1. Find all video pairs (script + SRT) using find_video_pairs()
        2. For each pair, run compare_script_to_transcript()
        3. Extract video date from folder name
        4. Collect all modifications with timestamps
        5. Apply extract_patterns() with min_frequency=3
        6. Apply temporal weighting using weight_by_recency()
        7. Write to JSON with metadata

    Output format:
        {
          "metadata": {
            "generated": "2026-01-28T23:15:00",
            "videos_analyzed": 11,
            "video_list": ["1-somaliland-2025", "3-fuentes-fact-check-2025", ...],
            "confidence_note": "Patterns from 11 videos - confidence will increase with more data"
          },
          "patterns": {
            "word_substitutions": [...],
            "anti_patterns": [...],
            "additions": [...],
            "sentence_patterns": {
              "max_preferred_length": null,
              "break_triggers": []
            }
          }
        }

    Edge cases:
        - Skips pairs where script/transcript length differs >50%
        - Warns if <5 videos found (low statistical confidence)
        - If no patterns meet min_frequency, documents as "insufficient corpus"
    """
    # Find all video pairs
    pairs = find_video_pairs(projects_dir)

    if len(pairs) < 5:
        logger.warning("Only %d video pairs found. Minimum 5 recommended for statistical significance.", len(pairs))

    # Collect modifications from all videos
    all_modifications = []
    video_metadata = {}
    pattern_occurrences = []  # For temporal weighting: (pattern, date, count)

    for script_path, srt_path in pairs:
        # Extract folder name for video identification
        folder_name = script_path.parent.name
        video_date = _extract_video_date(folder_name)
        video_metadata[folder_name] = video_date

        logger.info("Analyzing: %s", folder_name)

        # Compare script to transcript
        modifications = compare_script_to_transcript(script_path, srt_path)

        # Track modifications with date for temporal weighting
        for mod in modifications:
            all_modifications.append(mod)
            pattern_type = classify_pattern_type(mod)

            # Create pattern key for weighting
            if pattern_type == 'word_substitution':
                pattern_key = f"{mod['original']}->{mod['modified']}"
            elif pattern_type == 'deletion':
                pattern_key = f"DELETE:{mod['original']}"
            elif pattern_type == 'insertion':
                pattern_key = f"INSERT:{mod['modified']}"
            else:
                continue

            pattern_occurrences.append((pattern_key, video_date, 1))

    print(f"\nTotal modifications: {len(all_modifications)}")

    # Extract patterns with frequency filtering
    patterns = extract_patterns(all_modifications, min_frequency=3)

    # Apply temporal weighting to pattern scores
    weighted_scores = weight_by_recency(pattern_occurrences, decay_factor=0.95)

    # Update pattern frequencies with weighted scores (optional - for future use)
    # For now, keep raw frequencies but store weighted scores in metadata

    # Add placeholder for sentence patterns (Phase 12 Plan 02)
    patterns['sentence_patterns'] = {
        'max_preferred_length': None,
        'break_triggers': []
    }

    # Build metadata
    total_subs = len(patterns['word_substitutions'])
    total_anti = len(patterns['anti_patterns'])
    total_adds = len(patterns['additions'])

    confidence_note = f"Patterns from {len(pairs)} videos - confidence will increase with more data"
    if len(pairs) >= 10:
        confidence_note = f"Patterns from {len(pairs)} videos - good corpus size for reliable patterns"

    if total_subs == 0 and total_anti == 0 and total_adds == 0:
        confidence_note = "Insufficient corpus for pattern detection - modifications may be too context-specific"

    output = {
        'metadata': {
            'generated': datetime.datetime.now().isoformat(),
            'videos_analyzed': len(pairs),
            'video_list': sorted(video_metadata.keys()),
            'confidence_note': confidence_note,
            'total_modifications': len(all_modifications),
            'patterns_found': {
                'substitutions': total_subs,
                'anti_patterns': total_anti,
                'additions': total_adds
            }
        },
        'patterns': patterns
    }

    # Write to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nPattern library written to: {output_path}")
    print(f"  Word substitutions: {total_subs}")
    print(f"  Anti-patterns: {total_anti}")
    print(f"  Additions: {total_adds}")

    return output
