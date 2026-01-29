"""Voice fingerprinting module for learning speech patterns from script-transcript comparisons.

This module analyzes the differences between written scripts and delivered transcripts
to extract the user's natural speech patterns. It then applies these patterns during
script generation to make AI-generated scripts sound more natural.

Phase 12: Voice Fingerprinting
"""

from .corpus_builder import (
    extract_script_body,
    parse_srt_to_text,
    compare_script_to_transcript,
    find_video_pairs
)
from .pattern_extractor import (
    extract_patterns,
    weight_by_recency,
    build_pattern_library
)

__all__ = [
    'extract_script_body',
    'parse_srt_to_text',
    'compare_script_to_transcript',
    'find_video_pairs',
    'extract_patterns',
    'weight_by_recency',
    'build_pattern_library'
]
