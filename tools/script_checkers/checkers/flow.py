"""
Flow Checker (SCRIPT-02)

Analyzes narrative flow by detecting:
1. Terms used before definition
2. Abrupt topic transitions

Aims for 80% accuracy with high-confidence flagging. User makes final decisions.
"""

import re
from typing import Dict, List, Any, Set, Tuple
from . import BaseChecker


class FlowChecker(BaseChecker):
    """Analyzes script flow and term definitions"""

    def __init__(self, config):
        super().__init__(config)
        self._nlp = None  # Lazy load spaCy if needed

    @property
    def name(self) -> str:
        return "Flow"

    @property
    def nlp(self):
        """Lazy-load spaCy model"""
        if self._nlp is None:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm")
            except (ImportError, OSError) as e:
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm"
                ) from e
        return self._nlp

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for flow issues.

        Args:
            text: Script text to analyze

        Returns:
            Dictionary with issues and stats
        """
        issues = []

        # Check 1: Undefined terms
        undefined_issues = self._check_undefined_terms(text)
        issues.extend(undefined_issues)

        # Check 2: Abrupt transitions
        transition_issues = self._check_transitions(text)
        issues.extend(transition_issues)

        # Calculate stats
        stats = {
            'undefined_terms': len(undefined_issues),
            'abrupt_transitions': len(transition_issues),
            'total_issues': len(issues),
            'severity': self._overall_severity(issues)
        }

        return {'issues': issues, 'stats': stats}

    def _check_undefined_terms(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect technical terms used before definition.

        Returns:
            List of undefined term issues
        """
        doc = self.nlp(text)
        issues = []

        # Extract capitalized multi-word phrases (potential terms)
        seen_terms = {}  # term -> first occurrence char position
        defined_terms = set()  # terms that have been defined

        for sent in doc.sents:
            sent_start = sent.start_char

            # Look for definition patterns first
            defined_in_sent = self._extract_definitions(sent)
            defined_terms.update(defined_in_sent)

            # Look for potential technical terms
            for chunk in sent.noun_chunks:
                # Skip common terms
                if self._is_common_term(chunk.text):
                    continue

                # Capitalized multi-word phrases
                words = chunk.text.split()
                if len(words) >= self.config.flow_term_min_words:
                    # Check if any word is capitalized (proper noun indicator)
                    if any(w[0].isupper() for w in words if w):
                        term = chunk.text
                        term_normalized = term.lower()

                        # First occurrence of this term?
                        if term_normalized not in seen_terms:
                            seen_terms[term_normalized] = {
                                'term': term,
                                'line': self._get_line_number(text, sent_start),
                                'char': sent_start
                            }

                        # Is it defined yet?
                        if term_normalized in defined_terms:
                            # Already defined, mark as seen
                            if term_normalized in seen_terms:
                                del seen_terms[term_normalized]

        # Terms that were never defined = issues
        for term_info in seen_terms.values():
            issues.append({
                'type': 'undefined_term',
                'term': term_info['term'],
                'first_use_line': term_info['line'],
                'severity': 'warning',
                'suggestion': f"Consider defining '{term_info['term']}' before first use"
            })

        return issues

    def _extract_definitions(self, sent) -> Set[str]:
        """
        Extract terms that are being defined in this sentence.

        Patterns:
        - "X - [definition]"
        - "X — [definition]"
        - "X, which is [definition]"
        - "X, meaning [definition]"
        """
        defined = set()
        sent_text = sent.text

        # Pattern 1: Dash definitions
        dash_pattern = r'([A-Z][A-Za-z\s]{2,30})\s*[—\-]\s*'
        for match in re.finditer(dash_pattern, sent_text):
            term = match.group(1).strip()
            defined.add(term.lower())

        # Pattern 2: "which is" definitions
        which_pattern = r'([A-Z][A-Za-z\s]{2,30}),?\s+which\s+(?:is|was|means?)'
        for match in re.finditer(which_pattern, sent_text):
            term = match.group(1).strip()
            defined.add(term.lower())

        # Pattern 3: "meaning" definitions
        meaning_pattern = r'([A-Z][A-Za-z\s]{2,30}),?\s+meaning'
        for match in re.finditer(meaning_pattern, sent_text):
            term = match.group(1).strip()
            defined.add(term.lower())

        # Pattern 4: Parenthetical definitions
        paren_pattern = r'([A-Z][A-Za-z\s]{2,30})\s*\([^)]{10,}\)'
        for match in re.finditer(paren_pattern, sent_text):
            term = match.group(1).strip()
            defined.add(term.lower())

        return defined

    def _is_common_term(self, term: str) -> bool:
        """Check if term is common (not technical) and should be ignored"""
        common_words = set(self.config.flow_common_terms)
        term_lower = term.lower()

        # Single word terms are usually common
        if len(term.split()) == 1:
            return True

        # Check against stoplist
        term_words = set(term_lower.split())
        if term_words.issubset(common_words):
            return True

        return False

    def _check_transitions(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect abrupt topic transitions between sentences.

        Returns:
            List of transition issues
        """
        doc = self.nlp(text)
        issues = []

        sentences = list(doc.sents)
        transition_phrases = set(p.lower() for p in self.config.flow_transition_phrases)

        for i in range(len(sentences) - 1):
            sent1 = sentences[i]
            sent2 = sentences[i + 1]

            # Does sent2 start with transition phrase?
            sent2_start = sent2.text.strip().lower().split()
            if len(sent2_start) > 0:
                # Check first word or first two words
                first_word = sent2_start[0].rstrip('.,')
                first_two = ' '.join(sent2_start[:2]).rstrip('.,') if len(sent2_start) >= 2 else ''

                if first_word in transition_phrases or first_two in transition_phrases:
                    # Has transition, skip
                    continue

            # No transition phrase - check if subjects differ significantly
            if self._subjects_differ(sent1, sent2):
                issues.append({
                    'type': 'abrupt_transition',
                    'lines': [
                        self._get_line_number(text, sent1.start_char),
                        self._get_line_number(text, sent2.start_char)
                    ],
                    'prev_subject': self._get_main_subject(sent1),
                    'next_subject': self._get_main_subject(sent2),
                    'severity': 'info',
                    'suggestion': 'Consider adding transition phrase between these sentences'
                })

        return issues

    def _subjects_differ(self, sent1, sent2) -> bool:
        """
        Check if two consecutive sentences have significantly different subjects.

        Returns True if subjects seem unrelated.
        """
        subj1 = self._get_main_subject(sent1)
        subj2 = self._get_main_subject(sent2)

        if not subj1 or not subj2:
            return False

        # Same subject?
        if subj1.lower() == subj2.lower():
            return False

        # Related subjects (pronouns referring to previous)?
        if subj2.lower() in ('it', 'this', 'that', 'these', 'they', 'them'):
            return False

        # Subjects are different and no pronoun reference
        return True

    def _get_main_subject(self, sent) -> str:
        """Extract main subject of sentence"""
        for token in sent:
            if token.dep_ in ('nsubj', 'nsubjpass'):
                # Get the full noun phrase
                return self._get_full_phrase(token)
        return ""

    def _get_full_phrase(self, token) -> str:
        """Get full noun phrase from token"""
        phrase_tokens = [token]

        # Add children (determiners, adjectives, etc.)
        for child in token.children:
            if child.dep_ in ('det', 'amod', 'compound', 'poss'):
                phrase_tokens.append(child)

        # Sort by position and join
        phrase_tokens.sort(key=lambda t: t.i)
        return ' '.join(t.text for t in phrase_tokens)

    def _get_line_number(self, text: str, char_pos: int) -> int:
        """Convert character position to line number"""
        return text[:char_pos].count('\n') + 1

    def _overall_severity(self, issues: List[Dict[str, Any]]) -> str:
        """Determine overall severity"""
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
