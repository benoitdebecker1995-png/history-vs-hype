"""Pattern applier for transforming scripts using learned voice patterns.

This module applies learned speech patterns from voice-patterns.json to new scripts,
transforming formal AI-generated text to match the user's natural delivery style.

Features:
- Word substitutions (formal -> casual)
- Anti-pattern removal (unwanted phrases)
- High-confidence pattern filtering (only apply patterns with freq >= 5)
- Change tracking for transparency

Phase 12: Voice Fingerprinting - Pattern Application
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


class VoicePatternApplier:
    """Apply learned voice patterns to transform script text.

    Loads patterns from voice-patterns.json and applies:
    1. Word substitutions (e.g., "utilize" -> "use")
    2. Anti-pattern removal (e.g., "it should be noted that")

    Only HIGH-confidence patterns (frequency >= 5) are applied by default.
    """

    def __init__(self, patterns_path: Path = None):
        """Load patterns from JSON file.

        Args:
            patterns_path: Path to voice-patterns.json. If None, auto-detect
                          in parent directory of this module.
        """
        self.patterns = {}
        self.metadata = {}

        if patterns_path is None:
            patterns_path = Path(__file__).parent.parent / 'voice-patterns.json'

        if patterns_path.exists():
            with open(patterns_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = data.get('patterns', {})
                self.metadata = data.get('metadata', {})
        else:
            # No patterns yet - return text unchanged
            self.patterns = {}
            self.metadata = {'videos_analyzed': 0}

    def apply_word_substitutions(self, text: str) -> Tuple[str, List[Dict]]:
        """Apply word substitution patterns.

        Only applies HIGH-confidence patterns (confidence == 'HIGH').
        Uses word boundaries to avoid partial matches.

        Args:
            text: Input text to transform

        Returns:
            Tuple of (modified_text, changes_list)
            changes_list: List of {type, original, replacement, count}
        """
        changes = []
        modified_text = text

        substitutions = self.patterns.get('word_substitutions', [])

        for pattern in substitutions:
            # Only apply HIGH confidence patterns
            if pattern.get('confidence') != 'HIGH':
                continue

            formal = pattern.get('formal')
            casual = pattern.get('casual')

            if not formal or not casual:
                continue

            # Use word boundaries for exact word matching
            # Case-insensitive to catch "Utilize" and "utilize"
            regex = r'\b' + re.escape(formal) + r'\b'

            # Count occurrences before replacement
            matches = re.findall(regex, modified_text, re.IGNORECASE)
            count = len(matches)

            if count > 0:
                # Replace while preserving case of first letter
                def replace_with_case(match):
                    matched_text = match.group(0)
                    if matched_text[0].isupper():
                        return casual.capitalize()
                    return casual

                modified_text = re.sub(regex, replace_with_case, modified_text, flags=re.IGNORECASE)

                changes.append({
                    'type': 'substitution',
                    'original': formal,
                    'replacement': casual,
                    'count': count
                })

        return modified_text, changes

    def remove_anti_patterns(self, text: str) -> Tuple[str, List[Dict]]:
        """Remove anti-pattern phrases.

        Removes unwanted phrases completely and normalizes whitespace.

        Args:
            text: Input text to transform

        Returns:
            Tuple of (modified_text, changes_list)
            changes_list: List of {type, phrase, count}
        """
        changes = []
        modified_text = text

        anti_patterns = self.patterns.get('anti_patterns', [])

        for pattern in anti_patterns:
            phrase = pattern.get('phrase')

            if not phrase:
                continue

            # Case-insensitive removal
            regex = re.escape(phrase)
            matches = re.findall(regex, modified_text, re.IGNORECASE)
            count = len(matches)

            if count > 0:
                modified_text = re.sub(regex, '', modified_text, flags=re.IGNORECASE)

                # Normalize whitespace (don't create double spaces)
                modified_text = re.sub(r'\s+', ' ', modified_text)
                modified_text = re.sub(r'\s+([.,!?;:])', r'\1', modified_text)

                changes.append({
                    'type': 'removal',
                    'phrase': phrase,
                    'count': count
                })

        return modified_text, changes

    def apply(self, text: str, show_changes: bool = False) -> Tuple[str, List[Dict]]:
        """Apply all voice patterns to text.

        Applies patterns in order:
        1. Word substitutions (formal -> casual)
        2. Anti-pattern removal

        Args:
            text: Input text to transform
            show_changes: If True, return detailed change list

        Returns:
            Tuple of (modified_text, changes_list)
        """
        all_changes = []

        # Apply word substitutions first
        text, sub_changes = self.apply_word_substitutions(text)
        all_changes.extend(sub_changes)

        # Remove anti-patterns second
        text, removal_changes = self.remove_anti_patterns(text)
        all_changes.extend(removal_changes)

        return text, all_changes


def apply_voice_patterns(text: str, patterns_path: Path = None, show_changes: bool = False) -> Tuple[str, List[Dict]]:
    """Apply learned voice patterns to text (convenience function).

    Args:
        text: Input text to transform
        patterns_path: Path to voice-patterns.json (auto-detect if None)
        show_changes: If True, return detailed change list

    Returns:
        Tuple of (modified_text, changes_list)

    Example:
        >>> text = "You should utilize this approach."
        >>> modified, changes = apply_voice_patterns(text)
        >>> print(modified)
        'You should use this approach.'
    """
    applier = VoicePatternApplier(patterns_path)
    return applier.apply(text, show_changes)
