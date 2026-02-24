"""
Repetition Checker (SCRIPT-01)

Detects repeated phrases (3+ occurrences) while distinguishing rhetorical
repetition (intentional emphasis) from redundant repetition (filler).

Rhetorical patterns (NOT flagged):
- "Not X. Not Y. Not Z." (fragment emphasis)
- Repetition within 2 sentences (potential rhetorical device)
- Anaphora: same phrase starting consecutive sentences

Redundant patterns (FLAGGED):
- Same phrase scattered across script
- Filler phrases repeated ("the thing is", "the fact that")
"""

import re
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple
from checkers import BaseChecker


class RepetitionChecker(BaseChecker):
    """Detects repeated phrases with rhetorical pattern recognition"""

    @property
    def name(self) -> str:
        return "Repetition"

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for repetitive phrases.

        Args:
            text: Script text to analyze

        Returns:
            Dictionary with issues and stats:
                - issues: List of repeated phrase issues
                - stats: Analysis statistics
        """
        # Extract sentences and phrases
        sentences = self._split_sentences(text)
        phrases = self._extract_phrases(sentences)

        # Find repetitions
        repetitions = self._find_repetitions(phrases)

        # Classify rhetorical vs redundant
        issues = []
        for phrase_info in repetitions:
            is_rhetorical = self._is_rhetorical(phrase_info, sentences)

            # Only flag non-rhetorical or severe cases
            if not is_rhetorical or phrase_info['count'] >= 5:
                severity = self._calculate_severity(phrase_info, is_rhetorical)
                reason = self._get_reason(phrase_info, is_rhetorical)

                issues.append({
                    'phrase': phrase_info['phrase'],
                    'count': phrase_info['count'],
                    'positions': phrase_info['positions'],
                    'is_rhetorical': is_rhetorical,
                    'severity': severity,
                    'reason': reason
                })

        # Calculate stats
        stats = {
            'total_phrases_analyzed': len(phrases),
            'unique_phrases': len(set(p['phrase'] for p in phrases)),
            'repeated_phrases': len(repetitions),
            'rhetorical_detected': len([i for i in issues if i['is_rhetorical']]),
            'severity': self._overall_severity(issues)
        }

        return {'issues': issues, 'stats': stats}

    def _split_sentences(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into sentences with position tracking.

        Returns:
            List of {text, start_char, sentence_num}
        """
        # Simple sentence splitting using regex
        sentences = []
        sent_num = 0

        # Split on sentence endings
        for match in re.finditer(r'[^.!?]+[.!?]+', text):
            sent_text = match.group().strip()
            if sent_text:
                sentences.append({
                    'text': sent_text,
                    'start_char': match.start(),
                    'sentence_num': sent_num
                })
                sent_num += 1

        return sentences

    def _extract_phrases(self, sentences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract 2-4 word phrases from sentences.

        Returns:
            List of {phrase, sentence_num, start_char}
        """
        min_words = self.config.repetition_min_phrase_words
        max_words = self.config.repetition_max_phrase_words
        phrases = []

        for sent in sentences:
            words = sent['text'].split()
            # Extract phrases of various lengths
            for length in range(min_words, min(max_words + 1, len(words) + 1)):
                for i in range(len(words) - length + 1):
                    phrase = ' '.join(words[i:i+length])
                    # Normalize: lowercase, remove punctuation
                    phrase_normalized = re.sub(r'[^\w\s]', '', phrase.lower())

                    if phrase_normalized:
                        phrases.append({
                            'phrase': phrase_normalized,
                            'original': phrase,
                            'sentence_num': sent['sentence_num'],
                            'start_char': sent['start_char']
                        })

        return phrases

    def _find_repetitions(self, phrases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find exact and near-duplicate phrases.

        Returns:
            List of {phrase, count, positions, sentence_nums}
        """
        min_occurrences = self.config.repetition_min_occurrences

        # Group by exact match
        phrase_groups = {}
        for p in phrases:
            key = p['phrase']
            if key not in phrase_groups:
                phrase_groups[key] = []
            phrase_groups[key].append(p)

        # Convert to output format (only exact matches for performance)
        # Near-duplicate detection with difflib can be O(n²), skip for now
        repetitions = []
        for phrase, group in phrase_groups.items():
            if len(group) >= min_occurrences:
                repetitions.append({
                    'phrase': phrase,
                    'count': len(group),
                    'positions': [(p['sentence_num'], p['start_char']) for p in group],
                    'sentence_nums': [p['sentence_num'] for p in group]
                })

        return repetitions

    def _is_rhetorical(self, phrase_info: Dict[str, Any], sentences: List[Dict[str, Any]]) -> bool:
        """
        Determine if repetition is rhetorical (intentional emphasis).

        Rhetorical patterns:
        - ALL occurrences clustered closely (within 2 sentences of each other)
        - Anaphora (same phrase starting consecutive sentences)
        - Fragment emphasis pattern (short emphatic sentences)
        """
        proximity = self.config.repetition_rhetorical_proximity
        sent_nums = phrase_info['sentence_nums']

        # Check proximity: ALL occurrences must be close together (not scattered)
        if len(sent_nums) >= 2:
            # Check if all occurrences are within proximity range
            max_gap = max(sent_nums[i+1] - sent_nums[i] for i in range(len(sent_nums) - 1))
            min_sent = min(sent_nums)
            max_sent = max(sent_nums)
            total_span = max_sent - min_sent

            # If span is small relative to occurrences, it's clustered
            if total_span <= proximity and max_gap <= proximity:
                # Additional check: are these fragments or short sentences?
                short_sentences = 0
                for sent_num in sent_nums:
                    if sent_num < len(sentences):
                        sent_text = sentences[sent_num]['text']
                        word_count = len(sent_text.split())
                        if word_count <= 5:  # Fragment threshold
                            short_sentences += 1

                # Only consider rhetorical if they're fragments
                if short_sentences >= len(sent_nums) / 2:
                    return True

        # Check for anaphora (phrase starts consecutive sentences)
        consecutive_starts = 0
        for i in range(len(sent_nums) - 1):
            if sent_nums[i+1] == sent_nums[i] + 1:  # Consecutive
                # Both sentences start with phrase?
                sent1 = sentences[sent_nums[i]]['text'].lower()
                sent2 = sentences[sent_nums[i+1]]['text'].lower()
                if sent1.startswith(phrase_info['phrase']) and sent2.startswith(phrase_info['phrase']):
                    consecutive_starts += 1

        if consecutive_starts >= 2:
            return True

        return False

    def _calculate_severity(self, phrase_info: Dict[str, Any], is_rhetorical: bool) -> str:
        """Calculate issue severity"""
        count = phrase_info['count']

        if is_rhetorical:
            # Rhetorical but excessive
            return 'info' if count < 7 else 'warning'
        else:
            # Redundant repetition
            if count >= 7:
                return 'error'
            elif count >= 5:
                return 'warning'
            else:
                return 'info'

    def _get_reason(self, phrase_info: Dict[str, Any], is_rhetorical: bool) -> str:
        """Generate explanation for flagged repetition"""
        count = phrase_info['count']
        phrase = phrase_info['phrase']

        if is_rhetorical:
            return f"Rhetorical repetition of '{phrase}' ({count} times) may be excessive"
        else:
            return f"Repeated {count} times across script (redundant)"

    def _overall_severity(self, issues: List[Dict[str, Any]]) -> str:
        """Determine overall severity from all issues"""
        if not issues:
            return 'ok'

        severities = [i['severity'] for i in issues]
        if 'error' in severities:
            return 'error'
        elif 'warning' in severities:
            return 'warning'
        elif 'info' in severities:
            return 'info'
        else:
            return 'ok'
