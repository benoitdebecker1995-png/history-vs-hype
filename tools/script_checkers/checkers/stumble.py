"""
SCRIPT-03: Stumble Test - Teleprompter Readability Checker

Detects sentences that pose stumble risks when reading from teleprompter:
- Sentences over 25 words (hard to read without breath)
- Sentences with 2+ subordinate clauses (complex nested structures)

Uses spaCy for accurate sentence parsing and dependency analysis.
"""

from typing import Dict, List, Any
from checkers import BaseChecker


class StumbleChecker(BaseChecker):
    """Detect teleprompter stumble risks in script"""

    def __init__(self, config):
        super().__init__(config)
        self._nlp = None  # Lazy load spaCy model

    @property
    def name(self) -> str:
        return "stumble"

    @property
    def nlp(self):
        """Lazy-load spaCy model to avoid import-time overhead"""
        if self._nlp is None:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm")
            except OSError:
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm"
                )
        return self._nlp

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for teleprompter stumble risks.

        Detection logic:
        - Flag sentences with word_count > config.stumble_max_words
        - Flag sentences with 2+ subordinate clauses (dep_ in ['advcl', 'acl', 'relcl'])
        - Severity: 'medium' for 25-30 words OR 2 clauses
        - Severity: 'high' for >30 words OR 3+ clauses

        Args:
            text: Script text to analyze

        Returns:
            {
                'issues': [
                    {
                        'line': N,
                        'text': "...",
                        'word_count': N,
                        'sub_clauses': N,
                        'severity': 'medium'|'high',
                        'reason': "..."
                    }
                ],
                'stats': {
                    'total_sentences': N,
                    'flagged_sentences': N,
                    'avg_words_per_sentence': N
                }
            }
        """
        doc = self.nlp(text)

        issues = []
        total_sentences = 0
        total_words = 0

        for sent_idx, sent in enumerate(doc.sents, start=1):
            # Count words (exclude punctuation)
            words = [t for t in sent if not t.is_punct and not t.is_space]
            word_count = len(words)
            total_words += word_count
            total_sentences += 1

            # Count subordinate clauses
            # advcl = adverbial clause ("when X happened, Y occurred")
            # acl = clausal modifier of noun ("the treaty that ended the war")
            # relcl = relative clause ("which was signed in 1919")
            sub_clauses = len([t for t in sent if t.dep_ in ('advcl', 'acl', 'relcl')])

            # Determine if this is a stumble risk
            is_long = word_count > self.config.stumble_max_words
            is_complex = sub_clauses >= self.config.stumble_max_clauses

            if not (is_long or is_complex):
                continue

            # Calculate severity
            severity = 'medium'
            reason_parts = []

            if word_count > 30:
                severity = 'high'
                reason_parts.append(f"{word_count} words (>30)")
            elif is_long:
                reason_parts.append(f"{word_count} words (>25)")

            if sub_clauses >= 3:
                severity = 'high'
                reason_parts.append(f"{sub_clauses} nested clauses")
            elif is_complex:
                reason_parts.append(f"{sub_clauses} nested clauses")

            reason = "Stumble risk: " + ", ".join(reason_parts)

            issues.append({
                'line': sent_idx,
                'text': sent.text.strip(),
                'word_count': word_count,
                'sub_clauses': sub_clauses,
                'severity': severity,
                'reason': reason
            })

        # Calculate stats
        avg_words = total_words / total_sentences if total_sentences > 0 else 0

        return {
            'issues': issues,
            'stats': {
                'total_sentences': total_sentences,
                'flagged_sentences': len(issues),
                'avg_words_per_sentence': round(avg_words, 1)
            }
        }
