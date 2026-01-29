"""Voice fingerprinting module for learning speech patterns from script-transcript comparisons.

This module analyzes the differences between written scripts and delivered transcripts
to extract the user's natural speech patterns. It then applies these patterns during
script generation to make AI-generated scripts sound more natural.

Phase 12: Voice Fingerprinting
"""

# Pattern applier imports (no dependencies)
from .pattern_applier import (
    apply_voice_patterns,
    VoicePatternApplier
)

# Corpus builder and pattern extractor imports (require srt library)
# These are lazy-imported to avoid blocking pattern_applier usage
# when srt is not installed
def _lazy_import_corpus_builder():
    from .corpus_builder import (
        extract_script_body,
        parse_srt_to_text,
        compare_script_to_transcript,
        find_video_pairs
    )
    return {
        'extract_script_body': extract_script_body,
        'parse_srt_to_text': parse_srt_to_text,
        'compare_script_to_transcript': compare_script_to_transcript,
        'find_video_pairs': find_video_pairs
    }

def _lazy_import_pattern_extractor():
    from .pattern_extractor import (
        extract_patterns,
        weight_by_recency,
        build_pattern_library
    )
    return {
        'extract_patterns': extract_patterns,
        'weight_by_recency': weight_by_recency,
        'build_pattern_library': build_pattern_library
    }

# Export pattern applier directly (always available)
__all__ = [
    'apply_voice_patterns',
    'VoicePatternApplier'
]

# Lazy-load corpus functions when accessed
def __getattr__(name):
    if name in ['extract_script_body', 'parse_srt_to_text', 'compare_script_to_transcript', 'find_video_pairs']:
        funcs = _lazy_import_corpus_builder()
        return funcs[name]
    elif name in ['extract_patterns', 'weight_by_recency', 'build_pattern_library']:
        funcs = _lazy_import_pattern_extractor()
        return funcs[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
