#!/usr/bin/env python3
"""
Tests for transcript_analyzer.py

Run with: python -m pytest test_transcript_analyzer.py -v
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from transcript_analyzer import (
    read_transcript,
    get_creator_name,
    get_first_n_words,
    get_context,
    extract_opening_hook,
    extract_transitions,
    extract_evidence_patterns,
    analyze_pacing,
    analyze_transcript_file
)


# Sample SRT format
SAMPLE_SRT = """1
00:00:01,000 --> 00:00:05,000
Today we're looking at a historical myth that still shapes modern beliefs.

2
00:00:05,500 --> 00:00:10,000
I fact-checked the claim and found the <b>primary sources</b>.

3
00:00:10,500 --> 00:00:15,000
Consequently, this led to major policy changes in 2024.
"""

# Sample VTT format
SAMPLE_VTT = """WEBVTT

00:00:01.000 --> 00:00:05.000
Fast forward to 1945 and everything changed.

00:00:05.500 --> 00:00:10.000
According to <i>historian Smith</i> on page 47, the treaty failed.

00:00:10.500 --> 00:00:15.000
But here's where it gets interesting.
"""

# Sample plain text
SAMPLE_TXT = """So how did this happen? Let me show you the documents.

This is what the treaty actually said: "All territories shall be returned."

Notice this clause in the original text. Years later, this led to conflict.
"""


class TestFormatParsing:
    """Test format-specific transcript parsing."""

    def test_srt_format_stripping(self):
        """Test SRT timecode and index removal."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as f:
            f.write(SAMPLE_SRT)
            temp_path = Path(f.name)

        try:
            text = read_transcript(temp_path)

            # Should not contain SRT metadata
            assert '00:00:01,000' not in text
            assert '1\n' not in text[:5]  # No index at start

            # Should contain actual text
            assert 'Today' in text
            assert 'fact-checked' in text

            # Should strip HTML tags
            assert '<b>' not in text
            assert 'primary sources' in text

        finally:
            temp_path.unlink()

    def test_vtt_format_stripping(self):
        """Test VTT header and timecode removal."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False, encoding='utf-8') as f:
            f.write(SAMPLE_VTT)
            temp_path = Path(f.name)

        try:
            text = read_transcript(temp_path)

            # Should not contain VTT metadata
            assert 'WEBVTT' not in text
            assert '00:00:01.000' not in text

            # Should contain actual text
            assert 'Fast forward' in text
            assert 'page 47' in text

            # Should strip HTML tags
            assert '<i>' not in text
            assert 'historian Smith' in text

        finally:
            temp_path.unlink()

    def test_txt_format_passthrough(self):
        """Test plain text reads without modification (except normalization)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(SAMPLE_TXT)
            temp_path = Path(f.name)

        try:
            text = read_transcript(temp_path)

            # Should preserve all text
            assert 'So how did this happen?' in text
            assert 'documents' in text
            assert 'treaty actually said' in text

        finally:
            temp_path.unlink()


class TestCreatorAttribution:
    """Test creator name extraction from file paths."""

    def test_subfolder_creator(self):
        """Test creator name from subfolder."""
        path = Path('transcripts/Kraut/video-title.txt')
        assert get_creator_name(path) == 'Kraut'

        path = Path('transcripts/Shaun/analysis.vtt')
        assert get_creator_name(path) == 'Shaun'

    def test_root_creator(self):
        """Test History vs Hype for root transcripts."""
        path = Path('transcripts/my-video.txt')
        assert get_creator_name(path) == 'History vs Hype'

    def test_niche_research_subfolder(self):
        """Test niche-research subfolder preservation."""
        path = Path('niche-research/topic-x/video.txt')
        assert get_creator_name(path) == 'topic-x'


class TestOpeningHookDetection:
    """Test opening hook pattern extraction."""

    def test_visual_contrast_hook(self):
        """Test visual contrast pattern detection."""
        text = "Now look at this map. But see what they actually drew instead."
        result = extract_opening_hook(text)

        assert 'visual_contrast' in result['detected_patterns']
        assert result['confidence'] in ['low', 'high']

    def test_fact_check_declaration(self):
        """Test fact-check declaration pattern."""
        text = "I fact-checked this claim using primary sources from the archive."
        result = extract_opening_hook(text)

        assert 'fact_check_declaration' in result['detected_patterns']

    def test_current_event_hook(self):
        """Test current event time reference."""
        text = "Today in 2025, this treaty is still being debated."
        result = extract_opening_hook(text)

        assert 'current_event' in result['detected_patterns']

    def test_question_hook(self):
        """Test question hook in first 100 words."""
        text = "Why did this happen? Let me show you the evidence."
        result = extract_opening_hook(text)

        assert 'question_hook' in result['detected_patterns']

    def test_multiple_patterns_high_confidence(self):
        """Test high confidence with 2+ patterns."""
        text = "Today I fact-checked this claim. Why did they lie? Look at this document."
        result = extract_opening_hook(text)

        assert len(result['detected_patterns']) >= 2
        assert result['confidence'] == 'high'


class TestTransitionExtraction:
    """Test transition pattern detection."""

    def test_causal_chain_transitions(self):
        """Test causal chain marker detection."""
        text = "The treaty was signed in 1919. Consequently, this led to border disputes."
        transitions = extract_transitions(text)

        causal = [t for t in transitions if t['pattern_type'] == 'causal_chain']
        assert len(causal) > 0
        assert 'Consequently' in causal[0]['text'] or 'consequently' in causal[0]['text']

    def test_temporal_jump_transitions(self):
        """Test temporal jump detection."""
        text = "The war ended. Fast forward to 1945, and everything changed."
        transitions = extract_transitions(text)

        temporal = [t for t in transitions if t['pattern_type'] == 'temporal_jump']
        assert len(temporal) > 0

    def test_pivot_phrase_transitions(self):
        """Test pivot phrase detection."""
        text = "The plan seemed perfect. But here's where it all went wrong."
        transitions = extract_transitions(text)

        pivots = [t for t in transitions if t['pattern_type'] == 'pivot_phrase']
        assert len(pivots) > 0

    def test_contrast_shift_transitions(self):
        """Test contrast shift at sentence start."""
        text = "The policy was approved. However, implementation failed."
        transitions = extract_transitions(text)

        contrasts = [t for t in transitions if t['pattern_type'] == 'contrast_shift']
        assert len(contrasts) > 0


class TestEvidencePatterns:
    """Test evidence pattern counting."""

    def test_according_to_counting(self):
        """Test 'according to' phrase counting."""
        text = "According to Smith, this happened. According to the treaty, it was illegal."
        patterns = extract_evidence_patterns(text)

        assert patterns['according_to'] == 2

    def test_page_citation_counting(self):
        """Test page number citation counting."""
        text = "On page 47, the treaty states this. See also page 123 for details."
        patterns = extract_evidence_patterns(text)

        assert patterns['page_citations'] == 2

    def test_document_reveal_counting(self):
        """Test document reveal language counting."""
        text = "Notice this clause. Reading directly from the document, it says..."
        patterns = extract_evidence_patterns(text)

        assert patterns['document_reveals'] >= 2


class TestPacingAnalysis:
    """Test pacing metrics calculation."""

    def test_word_count(self):
        """Test word counting."""
        text = "This is a test sentence with ten words total."
        pacing = analyze_pacing(text)

        assert pacing['word_count'] == 9  # Actual count

    def test_question_density(self):
        """Test question mark density calculation."""
        text = "Why did this happen? " * 100  # 400 words with 100 questions
        pacing = analyze_pacing(text)

        assert pacing['question_count'] == 100
        assert pacing['questions_per_1000_words'] > 200  # High density

    def test_paragraph_counting(self):
        """Test paragraph counting and average calculation."""
        text = "Paragraph one with five words.\n\nParagraph two with five words."
        pacing = analyze_pacing(text)

        assert pacing['paragraph_count'] == 2


class TestFullAnalysis:
    """Test full analysis pipeline."""

    def test_analyze_transcript_file_integration(self):
        """Test complete analysis of transcript file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Today I fact-checked this claim. " * 200)  # ~400 words
            temp_path = Path(f.name)

        try:
            result = analyze_transcript_file(temp_path)

            # Check all analysis sections present
            assert 'opening_hook' in result
            assert 'transitions' in result
            assert 'evidence_patterns' in result
            assert 'pacing' in result

            # Check metadata
            assert 'file' in result
            assert 'format' in result
            assert result['format'] == '.txt'

        finally:
            temp_path.unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
