"""
SCRIPT-04: Scaffolding Counter

Counts scaffolding phrases ("Here's", "So", "Now", "Let me", "Let's") and alerts
when overused. Thresholds scale proportionally with script length.

Special handling:
- "Here's what X actually says" is a SIGNATURE PHRASE, not filler (exempted)
- "So" and "Now" only flagged at sentence start (after period/newline)
"""

import re
from typing import Dict, List, Any, Tuple
from checkers import BaseChecker
from config import calculate_threshold


class ScaffoldingChecker(BaseChecker):
    """Detect overuse of scaffolding language"""

    def __init__(self, config):
        super().__init__(config)

    @property
    def name(self) -> str:
        return "scaffolding"

    def _is_signature_phrase(self, text: str, match_pos: int) -> bool:
        """
        Check if "Here's" is part of a signature phrase (document reveal pattern).

        Signature patterns:
        - "Here's what X actually says/said/shows/showed"
        - "Here's what the X says/said/shows/showed"

        Args:
            text: Full text
            match_pos: Position of "here's" match

        Returns:
            True if signature phrase, False if filler
        """
        # Extract context window (50 chars after match)
        context = text[match_pos:match_pos + 60].lower()

        for pattern in self.config.signature_patterns:
            if re.search(pattern, context, re.IGNORECASE):
                return True

        return False

    def _is_sentence_initial(self, text: str, match_pos: int) -> bool:
        """
        Check if match is at sentence start (after period, newline, or start of text).

        Args:
            text: Full text
            match_pos: Position of match

        Returns:
            True if sentence-initial, False otherwise
        """
        # Check what comes before the match
        before = text[:match_pos].rstrip()

        # Start of text
        if not before:
            return True

        # After sentence boundary
        if before[-1] in '.!?':
            return True

        return False

    def check(self, text: str) -> Dict[str, Any]:
        """
        Count scaffolding phrases and check against proportional threshold.

        Detection:
        - Match scaffolding phrases from config (case-insensitive)
        - For "so," and "now,": only flag if sentence-initial
        - Exempt signature phrases from count
        - Calculate threshold using calculate_threshold(word_count, base_rate)

        Severity:
        - count <= threshold: 'ok'
        - count <= threshold * warn_multiplier: 'warning'
        - count > threshold * error_multiplier: 'error'

        Args:
            text: Script text to analyze

        Returns:
            {
                'issues': [
                    {
                        'phrase': "here's",
                        'count': N,
                        'positions': [char_indices],
                        'threshold': N,
                        'severity': 'ok'|'warning'|'error',
                        'reason': "..."
                    }
                ],
                'stats': {
                    'total_scaffolding': N,
                    'words': N,
                    'threshold': N,
                    'rate_per_1000': N,
                    'severity': 'ok'|'warning'|'error'
                }
            }
        """
        # Count words
        words = len(text.split())

        # Calculate threshold
        threshold = calculate_threshold(words, self.config.scaffolding_base_rate)

        # Define patterns
        patterns = {
            "here's": r"\bhere'?s\b",
            "so": r"\bso,\b",  # Only with comma (sentence-initial marker)
            "now": r"\bnow,\b",  # Only with comma
            "let me": r"\blet me\b",
            "let's": r"\blet'?s\b"
        }

        # Track counts and positions
        phrase_data = {}
        total_count = 0

        for phrase_name, pattern in patterns.items():
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            positions = []

            for match in matches:
                match_pos = match.start()

                # Special handling for "here's" - check if signature phrase
                if phrase_name == "here's":
                    if self._is_signature_phrase(text, match_pos):
                        continue  # Skip signature phrases

                # Special handling for "so" and "now" - only sentence-initial
                if phrase_name in ("so", "now"):
                    if not self._is_sentence_initial(text, match_pos):
                        continue  # Skip non-sentence-initial

                positions.append(match_pos)

            count = len(positions)
            total_count += count

            phrase_data[phrase_name] = {
                'count': count,
                'positions': positions
            }

        # Determine overall severity
        warn_threshold = threshold * self.config.scaffolding_warn_multiplier
        error_threshold = threshold * self.config.scaffolding_error_multiplier

        if total_count <= threshold:
            severity = 'ok'
            reason = f"Within limit ({total_count}/{threshold})"
        elif total_count <= warn_threshold:
            severity = 'warning'
            reason = f"Approaching limit ({total_count}/{threshold}, warn at {int(warn_threshold)})"
        elif total_count <= error_threshold:
            severity = 'warning'
            reason = f"Exceeds threshold ({total_count}/{threshold}, error at {int(error_threshold)})"
        else:
            severity = 'error'
            reason = f"Significantly exceeds threshold ({total_count}/{threshold})"

        # Build issues list (one issue per phrase type with counts)
        issues = []
        for phrase_name, data in phrase_data.items():
            if data['count'] > 0:
                issues.append({
                    'phrase': phrase_name,
                    'count': data['count'],
                    'positions': data['positions'],
                    'threshold': threshold,
                    'severity': severity,
                    'reason': f"Found {data['count']} instances"
                })

        # Calculate rate per 1000 words
        rate_per_1000 = (total_count / words * 1000) if words > 0 else 0

        return {
            'issues': issues,
            'stats': {
                'total_scaffolding': total_count,
                'words': words,
                'threshold': threshold,
                'rate_per_1000': round(rate_per_1000, 2),
                'severity': severity
            }
        }
