"""
SCRIPT-05: Pacing Analysis - Script Energy and Readability Checker

Analyzes script pacing through multiple metrics:
- Sentence variance per section (rhythm consistency)
- Flesch Reading Ease delta between sections (complexity shifts)
- Entity density per section (proper noun overload)
- Composite scoring (0-100 scale)
- Energy arc visualization (sparkline)
- Flat zone detection (monotonous sections)
- Hook/interrupt advisories (modern relevance and visual variety)

Uses spaCy for sentence parsing and POS tagging.
Uses textstat for readability scoring.
Uses ScriptParser for section detection.
"""

from typing import Dict, List, Any
import re
import statistics
from pathlib import Path
import sys

# Add parent directories to path for imports (tools/ directory)
_file_path = Path(__file__).resolve()
_tools_dir = _file_path.parent.parent.parent  # Go up to tools/
sys.path.insert(0, str(_tools_dir))

from production.parser import ScriptParser
from checkers import BaseChecker


def generate_sparkline(scores: List[float]) -> str:
    """
    Generate Unicode sparkline from section scores.

    Maps scores to visual energy arc where:
    - Low score (poor pacing) = high complexity = tall bar
    - High score (good pacing) = low complexity = short bar

    Args:
        scores: List of section scores (0-100)

    Returns:
        String of Unicode block characters representing energy arc
    """
    if not scores:
        return ""

    # Invert scores to complexity (low score = high complexity)
    complexity = [100 - score for score in scores]

    # Handle all identical values
    if len(set(complexity)) == 1:
        return "▄" * len(complexity)

    # Map to 8 levels of Unicode blocks
    blocks = "▁▂▃▄▅▆▇█"

    # Min-max normalization to 0-7 index
    min_val = min(complexity)
    max_val = max(complexity)
    range_val = max_val - min_val

    sparkline = ""
    for val in complexity:
        if range_val == 0:
            index = 3  # Mid-level
        else:
            normalized = (val - min_val) / range_val
            index = min(7, int(normalized * 7))
        sparkline += blocks[index]

    return sparkline


def detect_flat_zones(scores: List[float], window: int = 3, tolerance: int = 10) -> List[str]:
    """
    Detect flat zones: consecutive sections with similar scores.

    Args:
        scores: List of section scores (0-100)
        window: Minimum consecutive sections to form flat zone (default 3)
        tolerance: Maximum point difference within zone (default 10)

    Returns:
        List of advisory strings describing flat zones
    """
    if len(scores) < window:
        return []

    flat_zones = []
    i = 0

    while i <= len(scores) - window:
        # Check if next 'window' scores are within tolerance
        window_scores = scores[i:i + window]
        min_score = min(window_scores)
        max_score = max(window_scores)

        if max_score - min_score <= tolerance:
            # Found a flat zone, extend it as far as possible
            zone_end = i + window
            while zone_end < len(scores):
                # Check if next score fits in the zone
                extended_scores = scores[i:zone_end + 1]
                if max(extended_scores) - min(extended_scores) <= tolerance:
                    zone_end += 1
                else:
                    break

            # Create advisory message (1-indexed sections)
            start_idx = i + 1
            end_idx = zone_end
            flat_zones.append(
                f"Energy plateau: sections {start_idx}-{end_idx} have similar complexity — consider pattern interrupt"
            )

            # Skip past this zone
            i = zone_end
        else:
            i += 1

    return flat_zones


class PacingChecker(BaseChecker):
    """Analyze script pacing through sentence variance, readability shifts, and entity density"""

    def __init__(self, config):
        super().__init__(config)
        self._nlp = None  # Lazy load spaCy model
        self._textstat = None  # Lazy load textstat
        self._parser = ScriptParser()

    @property
    def name(self) -> str:
        return "pacing"

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

    @property
    def textstat(self):
        """Lazy-load textstat library"""
        if self._textstat is None:
            try:
                import textstat
                self._textstat = textstat
            except ImportError:
                raise RuntimeError(
                    "textstat library not found. "
                    "Install with: pip install textstat"
                )
        return self._textstat

    def _strip_markers(self, text: str) -> str:
        """
        Strip all bracketed B-roll markers from text.

        Uses same patterns as ScriptParser.MARKER_PATTERNS

        Args:
            text: Text with potential markers

        Returns:
            Clean text without markers
        """
        # Apply all marker patterns from ScriptParser
        for pattern in self._parser.MARKER_PATTERNS:
            text = pattern.sub('', text)

        # Strip any remaining bracketed content
        text = re.sub(r'\[[^\]]+\]', '', text)

        return text

    def _calculate_sentence_variance(self, text: str) -> float:
        """
        Calculate standard deviation of sentence lengths.

        Args:
            text: Section content (markers stripped)

        Returns:
            Standard deviation of word counts per sentence, or 0.0 if < 2 sentences
        """
        if not text.strip():
            return 0.0

        doc = self.nlp(text)
        sentences = list(doc.sents)

        if len(sentences) < 2:
            return 0.0

        # Count words per sentence (exclude punctuation and spaces)
        word_counts = []
        for sent in sentences:
            words = [t for t in sent if not t.is_punct and not t.is_space]
            word_counts.append(len(words))

        return statistics.stdev(word_counts)

    def _calculate_flesch(self, text: str) -> float:
        """
        Calculate Flesch Reading Ease score.

        Args:
            text: Section content (markers stripped)

        Returns:
            Flesch Reading Ease score (0-100+, higher = easier)
        """
        if not text.strip():
            return 0.0

        return self.textstat.flesch_reading_ease(text)

    def _calculate_entity_density(self, text: str) -> float:
        """
        Calculate ratio of proper nouns to total words.

        Args:
            text: Section content (markers stripped)

        Returns:
            Ratio of PROPN tokens to total tokens (0.0-1.0)
        """
        if not text.strip():
            return 0.0

        doc = self.nlp(text)

        # Count tokens (exclude punctuation and spaces)
        total_words = 0
        proper_nouns = 0

        for token in doc:
            if not token.is_punct and not token.is_space:
                total_words += 1
                if token.pos_ == "PROPN":
                    proper_nouns += 1

        if total_words == 0:
            return 0.0

        return proper_nouns / total_words

    def _calculate_score(self, metrics: Dict, prev_flesch: float) -> int:
        """
        Calculate composite pacing score (0-100).

        Starts at 100 and deducts penalties:
        - Sentence variance penalty: up to 30 points
        - Flesch delta penalty: up to 35 points
        - Entity density penalty: up to 35 points

        Args:
            metrics: Dict with sentence_variance, flesch_score, entity_density
            prev_flesch: Previous section's Flesch score (for delta calculation)

        Returns:
            Score from 0-100 (100 = perfect pacing)
        """
        # Get thresholds from config with defaults
        variance_threshold = getattr(self.config, 'pacing_variance_threshold', 15)
        flesch_threshold = getattr(self.config, 'pacing_flesch_delta_threshold', 20)
        entity_threshold = getattr(self.config, 'pacing_entity_density_threshold', 0.4)

        score = 100

        # Sentence variance penalty (max 30 points)
        if metrics['sentence_variance'] > variance_threshold:
            penalty = (metrics['sentence_variance'] - variance_threshold) * 2
            score -= min(30, penalty)

        # Flesch delta penalty (max 35 points)
        flesch_delta = abs(metrics['flesch_score'] - prev_flesch)
        if flesch_delta > flesch_threshold:
            penalty = (flesch_delta - flesch_threshold) * 1.75
            score -= min(35, penalty)

        # Entity density penalty (max 35 points)
        if metrics['entity_density'] > entity_threshold:
            penalty = (metrics['entity_density'] - entity_threshold) * 87.5
            score -= min(35, penalty)

        return max(0, int(score))

    def _explain_issues(self, metrics: Dict, prev_flesch: float) -> List[str]:
        """
        Generate human-readable explanations for flagged metrics.

        Args:
            metrics: Dict with sentence_variance, flesch_score, flesch_delta, entity_density
            prev_flesch: Previous section's Flesch score

        Returns:
            List of reason strings explaining issues
        """
        reasons = []

        # Get thresholds from config with defaults
        variance_threshold = getattr(self.config, 'pacing_variance_threshold', 15)
        flesch_threshold = getattr(self.config, 'pacing_flesch_delta_threshold', 20)
        entity_threshold = getattr(self.config, 'pacing_entity_density_threshold', 0.4)

        # Check sentence variance
        if metrics['sentence_variance'] > variance_threshold:
            reasons.append(
                f"high sentence variance ({metrics['sentence_variance']:.1f}) — "
                "inconsistent rhythm between short and long sentences"
            )

        # Check Flesch delta
        flesch_delta = metrics['flesch_score'] - prev_flesch
        if abs(flesch_delta) > flesch_threshold:
            direction = "drop" if flesch_delta < 0 else "jump"
            reasons.append(
                f"readability {direction} of {abs(flesch_delta):.0f} points from previous section — "
                "sudden complexity spike" if flesch_delta < 0 else "sudden simplification"
            )

        # Check entity density
        if metrics['entity_density'] > entity_threshold:
            reasons.append(
                f"entity density ({metrics['entity_density']:.2f}) — "
                "too many proper nouns in sequence"
            )

        return reasons

    def _detect_hooks(self, text: str) -> List[int]:
        """
        Find character positions of modern relevance markers.

        Detects:
        - Time keywords: today, 2024, 2025, 2026, still, currently, now
        - B-roll markers: [NEWS ...], [MODERN ...], [CURRENT ...]

        Args:
            text: Section content

        Returns:
            List of character positions where hooks found
        """
        hooks = []

        # Time keywords (word boundary, case-insensitive)
        time_keywords = r'\b(today|2024|2025|2026|still|currently|now)\b'
        for match in re.finditer(time_keywords, text, re.IGNORECASE):
            hooks.append(match.start())

        # B-roll markers
        marker_patterns = [
            r'\[NEWS[^\]]*\]',
            r'\[MODERN[^\]]*\]',
            r'\[CURRENT[^\]]*\]'
        ]
        for pattern in marker_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                hooks.append(match.start())

        return hooks

    def _check_hook_gaps(self, sections: List) -> List[str]:
        """
        Check for sections lacking modern relevance hooks or visual variety.

        Args:
            sections: List of Section objects from ScriptParser

        Returns:
            List of advisory strings
        """
        advisories = []

        for section in sections:
            # Check for modern relevance hooks
            hooks = self._detect_hooks(section.content)
            if not hooks and section.word_count > 100:
                advisories.append(
                    f'Section "{section.heading}" ({section.word_count} words) has no modern relevance hooks'
                )

            # Check for B-roll marker variety (sections >200 words)
            if section.word_count > 200:
                # Count bracketed markers
                markers = re.findall(r'\[[^\]]+\]', section.content)
                if len(markers) == 0:
                    advisories.append(
                        f'Section "{section.heading}" has no B-roll markers — consider adding visual variety'
                    )

        return advisories

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for pacing issues.

        Args:
            text: Script text to analyze

        Returns:
            {
                'issues': [  # Sections with score < 75
                    {
                        'section': 'Section Name',
                        'score': 62,
                        'metrics': {
                            'sentence_variance': 18.2,
                            'flesch_score': 45.3,
                            'flesch_delta': -25.0,
                            'entity_density': 0.48
                        },
                        'reasons': [...]
                    }
                ],
                'all_sections': [  # Full data for verbose mode
                    {...}
                ],
                'stats': {
                    'total_sections': 8,
                    'flagged_sections': 2,
                    'average_score': 72,
                    'energy_arc': '▅▃▆▇▂▄▅▃',
                    'flat_zones': [...],
                    'verdict': 'NEEDS WORK'
                },
                'advisories': [  # Hook/interrupt advisories
                    ...
                ]
            }
        """
        # Parse into sections
        sections = self._parser.parse_text(text)

        # Handle single-section scripts
        if len(sections) == 1:
            return {
                'issues': [],
                'all_sections': [],
                'stats': {
                    'total_sections': 1,
                    'flagged_sections': 0,
                    'average_score': 0,
                    'energy_arc': '',
                    'flat_zones': [],
                    'verdict': 'SKIPPED'
                },
                'advisories': ['Single-section script — pacing analysis requires multiple sections']
            }

        # Analyze each section
        all_sections = []
        scores = []
        prev_flesch = 0  # First section has delta = 0

        for section in sections:
            # Strip markers before analysis
            clean_content = self._strip_markers(section.content)

            # Calculate metrics
            sentence_variance = self._calculate_sentence_variance(clean_content)
            flesch_score = self._calculate_flesch(clean_content)
            entity_density = self._calculate_entity_density(clean_content)

            # Calculate delta from previous section
            flesch_delta = flesch_score - prev_flesch if prev_flesch > 0 else 0

            metrics = {
                'sentence_variance': sentence_variance,
                'flesch_score': flesch_score,
                'flesch_delta': flesch_delta,
                'entity_density': entity_density
            }

            # Calculate composite score
            score = self._calculate_score(metrics, prev_flesch)
            scores.append(score)

            # Generate reasons if score < 75
            reasons = self._explain_issues(metrics, prev_flesch)

            all_sections.append({
                'section': section.heading,
                'score': score,
                'metrics': metrics,
                'reasons': reasons
            })

            # Update for next iteration
            prev_flesch = flesch_score

        # Calculate stats
        pass_threshold = getattr(self.config, 'pacing_pass_threshold', 75)
        fail_threshold = getattr(self.config, 'pacing_fail_threshold', 50)

        average_score = sum(scores) / len(scores)
        flagged_sections = [s for s in all_sections if s['score'] < pass_threshold]

        # Determine verdict
        if average_score >= pass_threshold:
            verdict = 'PASS'
        elif average_score >= fail_threshold:
            verdict = 'NEEDS WORK'
        else:
            verdict = 'FAIL'

        # Generate visualizations
        energy_arc = generate_sparkline(scores)
        flat_zone_window = getattr(self.config, 'pacing_flat_zone_window', 3)
        flat_zone_tolerance = getattr(self.config, 'pacing_flat_zone_tolerance', 10)
        flat_zones = detect_flat_zones(scores, flat_zone_window, flat_zone_tolerance)

        # Generate hook advisories
        advisories = self._check_hook_gaps(sections)

        return {
            'issues': flagged_sections,
            'all_sections': all_sections,
            'stats': {
                'total_sections': len(sections),
                'flagged_sections': len(flagged_sections),
                'average_score': int(average_score),
                'energy_arc': energy_arc,
                'flat_zones': flat_zones,
                'verdict': verdict
            },
            'advisories': advisories
        }
