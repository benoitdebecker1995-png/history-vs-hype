"""
Configuration and Thresholds for Script Quality Checkers

Provides:
- Config dataclass with all threshold settings
- calculate_threshold() for proportional scaling based on script length
- Default thresholds derived from STYLE-GUIDE.md and teleprompter best practices
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """Configuration for all script checkers"""

    # SCRIPT-03: Stumble Test - Teleprompter readability
    stumble_max_words: int = 25  # Sentences over this flagged (teleprompter best practice)
    stumble_max_clauses: int = 2  # Nested subordinate clauses trigger stumble risk

    # SCRIPT-04: Scaffolding Counter
    scaffolding_base_rate: float = 0.002  # Per word (~3 per 1500 words matches STYLE-GUIDE 2-4)
    scaffolding_warn_multiplier: float = 1.5  # Warn at 1.5x threshold
    scaffolding_error_multiplier: float = 2.0  # Error at 2x threshold

    # Scaffolding phrases to detect
    scaffolding_phrases: List[str] = field(default_factory=lambda: [
        "here's",
        "so,",      # Only sentence-initial
        "now,",     # Only sentence-initial
        "let me",
        "let's"
    ])

    # SCRIPT-04: Signature phrase exemptions (not counted as filler)
    signature_patterns: List[str] = field(default_factory=lambda: [
        r"here'?s what .{1,30} actually (say|said|show|showed)",
        r"here'?s what the .{1,30} (say|said|show|showed)",
    ])

    # SCRIPT-01: Repetition Detection
    repetition_min_phrase_words: int = 2  # Minimum words to consider a phrase (2-3 words)
    repetition_max_phrase_words: int = 4  # Maximum words to consider
    repetition_similarity_threshold: float = 0.8  # Fuzzy match threshold (0-1)
    repetition_min_occurrences: int = 3  # Flag phrases appearing 3+ times
    repetition_rhetorical_proximity: int = 2  # Sentences within this distance = potential rhetorical


def calculate_threshold(word_count: int, base_rate: float, min_val: int = 1) -> int:
    """
    Calculate proportional threshold based on script length.

    Examples:
        - 8-min script (~1200 words) at 0.002 = 2.4 → 2 allowed
        - 15-min script (~2250 words) at 0.002 = 4.5 → 4 allowed
        - 30-min script (~4500 words) at 0.002 = 9.0 → 9 allowed

    Args:
        word_count: Total words in script
        base_rate: Rate per word (e.g., 0.002 = 2 per 1000 words)
        min_val: Minimum threshold value (default 1)

    Returns:
        Calculated threshold (integer)
    """
    threshold = max(int(word_count * base_rate), min_val)
    return threshold
