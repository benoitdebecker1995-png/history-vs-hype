"""
Heuristic scoring engine for clip detection.
Every score is fully explainable through transparent rules.
"""

from typing import Dict, List, Tuple
from scoring import patterns
from utils.config import config


class ClipScorer:
    """
    Scores transcript segments based on academic/historical content quality.
    All scoring decisions are logged with reasoning.
    """

    def __init__(self):
        """Initialize scorer with rules from config."""
        self.rules = config.scoring_rules

        # Extract rule values
        self.evidence = self.rules['evidence_markers']
        self.argument = self.rules['argument_structure']
        self.penalties = self.rules['penalties']
        self.segment_quality = self.rules['segment_quality']
        self.weights = self.rules['weights']

    def score_segment(self, text: str, start: float, end: float) -> Dict:
        """
        Score a transcript segment for clip worthiness.

        Args:
            text: Transcript text
            start: Start timestamp in seconds
            end: End timestamp in seconds

        Returns:
            Dictionary with score, reasons, duration, and text
        """
        score = 0
        reasons = []
        duration = end - start

        # ===================================================================
        # EVIDENCE MARKERS (weighted by config)
        # ===================================================================

        # Primary source references
        if patterns.contains_any_keyword(text, patterns.PRIMARY_SOURCE_KEYWORDS):
            points = self.evidence['primary_source_reference']
            score += points
            reasons.append(f"Contains primary source reference (+{points})")

        # Date references
        date_matches = patterns.count_pattern_matches(text, patterns.DATE_COMPILED)
        if date_matches > 0:
            points = self.evidence['date_reference']
            score += points
            reasons.append(f"References specific date(s): {date_matches} found (+{points})")

        # Citation language
        citation_matches = patterns.count_pattern_matches(text, patterns.CITATION_COMPILED)
        if citation_matches > 0:
            points = self.evidence['citation_language']
            score += points
            reasons.append(f"Citation language detected: {citation_matches} instances (+{points})")

        # Quantitative data
        quant_matches = patterns.count_pattern_matches(text, patterns.QUANTITATIVE_COMPILED)
        if quant_matches > 0:
            points = self.evidence['quantitative_data']
            score += points
            reasons.append(f"Quantitative data: {quant_matches} statistics/numbers (+{points})")

        # Legal language
        if patterns.contains_any_keyword(text, patterns.LEGAL_KEYWORDS):
            points = self.evidence['legal_language']
            score += points
            reasons.append(f"Legal/technical terminology (+{points})")

        # ===================================================================
        # ARGUMENT STRUCTURE (weighted by config)
        # ===================================================================

        # Causal explanations
        causal_matches = patterns.count_pattern_matches(text, patterns.CAUSAL_COMPILED)
        if causal_matches > 0:
            points = self.argument['causal_explanation']
            score += points
            reasons.append(f"Causal explanation: {causal_matches} instances (+{points})")

        # Myth-debunking
        debunk_matches = patterns.count_pattern_matches(text, patterns.DEBUNK_COMPILED)
        if debunk_matches > 0:
            points = self.argument['myth_debunk_pattern']
            score += points
            reasons.append(f"Myth-debunking pattern detected (+{points})")

        # Comparative analysis
        comparison_matches = patterns.count_pattern_matches(text, patterns.COMPARISON_COMPILED)
        if comparison_matches > 0:
            points = self.argument['comparison']
            score += points
            reasons.append(f"Comparative analysis (+{points})")

        # Conclusion signals
        conclusion_matches = patterns.count_pattern_matches(text, patterns.CONCLUSION_COMPILED)
        if conclusion_matches > 0:
            points = self.argument['conclusion_signal']
            score += points
            reasons.append(f"Conclusion/synthesis signal (+{points})")

        # ===================================================================
        # COMPLETENESS CHECK
        # ===================================================================

        # Check if segment is a complete sentence
        text_stripped = text.strip()
        if text_stripped and text_stripped[-1] in '.!?':
            score += 10
            reasons.append("Complete sentence boundary (+10)")
        else:
            penalty = self.penalties['incomplete_thought']
            score += penalty  # This is negative
            reasons.append(f"Incomplete thought unit ({penalty})")

        # Check for unnatural cutoffs (mid-word, mid-phrase)
        if text_stripped.endswith((',', ':', ';', '-', 'and', 'but', 'or', 'the', 'a')):
            score -= 10
            reasons.append("Unnatural cutoff detected (-10)")

        # ===================================================================
        # PENALTIES
        # ===================================================================

        # Clickbait language
        clickbait_count = sum(
            1 for word in patterns.CLICKBAIT_WORDS
            if word.lower() in text.lower()
        )
        if clickbait_count > 0:
            penalty = self.penalties['clickbait_words']
            score += penalty  # This is negative
            reasons.append(f"Clickbait language: {clickbait_count} instances ({penalty})")

        # Emotional exaggeration
        exaggeration_count = patterns.count_pattern_matches(text, patterns.EXAGGERATION_COMPILED)
        if exaggeration_count > 0:
            penalty = self.penalties['emotional_exaggeration']
            score += penalty
            reasons.append(f"Emotional exaggeration: {exaggeration_count} instances ({penalty})")

        # Vague attribution
        vague_count = patterns.count_pattern_matches(text, patterns.VAGUE_ATTRIBUTION_COMPILED)
        if vague_count > 0:
            penalty = self.penalties['vague_attribution']
            score += penalty
            reasons.append(f"Vague attribution: {vague_count} instances ({penalty})")

        # ===================================================================
        # DURATION SCORING
        # ===================================================================

        min_viable = self.segment_quality['min_viable_duration']
        optimal_min = self.segment_quality['optimal_duration_min']
        optimal_max = self.segment_quality['optimal_duration_max']

        if duration < min_viable:
            score = 0  # Hard reject
            reasons.append(f"TOO SHORT: {duration:.1f}s < {min_viable}s minimum (REJECTED)")
        elif optimal_min <= duration <= optimal_max:
            score += 10
            reasons.append(f"Optimal duration: {duration:.1f}s (+10)")
        elif duration > optimal_max:
            excess = duration - optimal_max
            if excess > 30:
                score -= 5
                reasons.append(f"Too long: {duration:.1f}s exceeds optimal by {excess:.1f}s (-5)")

        # ===================================================================
        # NORMALIZE AND RETURN
        # ===================================================================

        # Ensure score is within 0-100 range
        final_score = max(0, min(100, score))

        return {
            "score": final_score,
            "reasons": reasons,
            "duration": duration,
            "start_time": start,
            "end_time": end,
            "text": text
        }

    def score_transcript_segments(
        self,
        segments: List[Dict],
        min_score: float = 30.0,
        max_clips: int = 20
    ) -> List[Dict]:
        """
        Score all segments and return top candidates.

        Args:
            segments: List of transcript segments with start, end, text
            min_score: Minimum score threshold for inclusion
            max_clips: Maximum number of clips to return

        Returns:
            List of scored clips, sorted by score descending
        """
        scored_clips = []

        for segment in segments:
            score_result = self.score_segment(
                text=segment['text'],
                start=segment['start'],
                end=segment['end']
            )

            # Only include clips above threshold
            if score_result['score'] >= min_score:
                scored_clips.append(score_result)

        # Sort by score descending
        scored_clips.sort(key=lambda x: x['score'], reverse=True)

        # Return top N clips
        return scored_clips[:max_clips]
