#!/usr/bin/env python3
"""
Transcript Analysis Pipeline - Extract structural patterns from creator transcripts.

Parses 83+ creator transcripts (.txt, .srt, .vtt), extracts opening hooks, transitions,
evidence markers, and pacing patterns. Designed for cross-creator synthesis and technique
library population.

Usage:
    python transcript_analyzer.py --analyze-all
    python transcript_analyzer.py --analyze FILE
    python transcript_analyzer.py --stats
"""

import re
import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

from tools.logging_config import get_logger

logger = get_logger(__name__)


def read_transcript(file_path: Path) -> str:
    """
    Read and clean transcript file with format-specific metadata stripping.

    Supports:
    - .srt: Strip SRT timecodes and index lines
    - .vtt: Strip WEBVTT header and VTT timecodes
    - .txt: Read directly

    All formats: Remove HTML tags, normalize excessive newlines
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
    except Exception as e:
        return f"[ERROR READING FILE: {e}]"

    suffix = file_path.suffix.lower()

    if suffix == '.srt':
        # Remove SRT index lines (digits only on line)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        # Remove SRT timecodes: 00:01:23,456 --> 00:01:25,789
        text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', '', text)

    elif suffix == '.vtt':
        # Remove WEBVTT header
        text = re.sub(r'^WEBVTT\s*\n', '', text, flags=re.MULTILINE)
        # Remove VTT timecodes: 00:01:23.456 --> 00:01:25.789
        text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', text)

    # Remove HTML tags (common in subtitle files)
    text = re.sub(r'<[^>]+>', '', text)

    # Normalize excessive newlines (3+ → 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def get_creator_name(file_path: Path) -> str:
    """
    Extract creator name from file path.

    Rules:
    - File in subfolder → folder name (e.g., transcripts/Kraut/file.txt → "Kraut")
    - File in transcripts/ root → "History vs Hype"
    - File in niche-research/ subfolder → preserve subfolder name
    """
    parts = file_path.parts

    # Find 'transcripts' or 'niche-research' in path
    if 'transcripts' in parts:
        idx = parts.index('transcripts')
        if idx + 1 < len(parts) - 1:  # Has subfolder before filename
            return parts[idx + 1]
        else:
            return "History vs Hype"

    elif 'niche-research' in parts:
        idx = parts.index('niche-research')
        if idx + 1 < len(parts) - 1:
            return parts[idx + 1]
        else:
            return "niche-research"

    # Fallback: parent directory name
    return file_path.parent.name


def get_first_n_words(text: str, n: int = 500) -> str:
    """Extract first N words from text (proxy for ~2 min opening @ 150 WPM)."""
    words = text.split()
    return ' '.join(words[:n])


def get_context(text: str, position: int, window: int = 100) -> str:
    """Extract text window around position (characters)."""
    start = max(0, position - window)
    end = min(len(text), position + window)
    return text[start:end].strip()


def extract_opening_hook(text: str) -> Dict[str, Any]:
    """
    Detect hook patterns in opening section (first 500 words).

    Patterns:
    - visual_contrast: Show X → Show Y → State tension
    - fact_check_declaration: "I fact-checked", "I read", "I checked"
    - current_event: Time references (today, last week, in 2024)
    - escalation_timeline: Temporal progression (days later, within hours)
    - question_hook: Opens with question in first 100 words

    Returns: {category, detected_patterns, text_sample, confidence}
    """
    opening = get_first_n_words(text, 500)
    first_100_words = get_first_n_words(text, 100)
    detected = []

    # Visual contrast pattern
    if re.search(r'\b(now|instead|but)\b.*\b(see|look|open|shows?)\b', opening, re.IGNORECASE):
        detected.append('visual_contrast')

    # Fact-check declaration
    if re.search(r'\b(fact[- ]checked?|I checked|I read|I found)\b', opening, re.IGNORECASE):
        detected.append('fact_check_declaration')

    # Current event hook
    if re.search(r'\b(today|yesterday|last (week|month)|this (week|month|year)|in 20[12]\d)\b', opening, re.IGNORECASE):
        detected.append('current_event')

    # Escalation timeline
    if re.search(r'\b(\d+ (days?|hours?|weeks?) later|within (hours|days|weeks))\b', opening, re.IGNORECASE):
        detected.append('escalation_timeline')

    # Question hook
    if '?' in first_100_words:
        detected.append('question_hook')

    # Confidence: high if 2+ patterns, else low
    confidence = 'high' if len(detected) >= 2 else 'low' if detected else 'none'

    return {
        'category': 'opening_hook',
        'detected_patterns': detected,
        'text_sample': opening[:200],
        'confidence': confidence
    }


def extract_transitions(text: str) -> List[Dict[str, Any]]:
    """
    Find transition patterns throughout transcript.

    Types:
    - causal_chain: consequently, thereby, which meant that, as a result
    - temporal_jump: Now, Fast forward, Years later, Meanwhile
    - pivot_phrase: So how did, But here's where, And this is where
    - contrast_shift: But/However/On the other hand at sentence start
    """
    transitions = []

    # Causal chain markers
    causal_pattern = r'\b(consequently|thereby|which meant that|this led to|as a result|because of this)\b'
    for match in re.finditer(causal_pattern, text, re.IGNORECASE):
        transitions.append({
            'pattern_type': 'causal_chain',
            'text': get_context(text, match.start(), window=80),
            'position': match.start()
        })

    # Temporal jumps
    temporal_pattern = r'\b(Now,|Fast forward|Years later|Meanwhile|By \d{4})\b'
    for match in re.finditer(temporal_pattern, text, re.IGNORECASE):
        transitions.append({
            'pattern_type': 'temporal_jump',
            'text': get_context(text, match.start(), window=80),
            'position': match.start()
        })

    # Pivot phrases
    pivot_pattern = r'\b(So how did|But here\'s where|And this is where|Here\'s the problem)\b'
    for match in re.finditer(pivot_pattern, text, re.IGNORECASE):
        transitions.append({
            'pattern_type': 'pivot_phrase',
            'text': get_context(text, match.start(), window=80),
            'position': match.start()
        })

    # Contrast shifts (sentence start only)
    contrast_pattern = r'(?:^|[.!?]\s+)(But|However|On the other hand|And yet)\b'
    for match in re.finditer(contrast_pattern, text, re.IGNORECASE | re.MULTILINE):
        transitions.append({
            'pattern_type': 'contrast_shift',
            'text': get_context(text, match.start(), window=80),
            'position': match.start()
        })

    return transitions


def extract_evidence_patterns(text: str) -> Dict[str, Any]:
    """
    Count evidence presentation patterns.

    Metrics:
    - direct_quotes: Attribution + quote patterns
    - according_to: "according to" phrase count
    - page_citations: "page \\d+" references
    - document_reveals: Direct evidence presentation ("notice this", "reading directly from")
    - quote_density: Quoted segments per 1000 words
    """
    word_count = len(text.split())

    # Direct quotes with attribution
    direct_quotes = len(re.findall(r'Here\'s what .{1,50} (actually )?said', text, re.IGNORECASE))
    direct_quotes += len(re.findall(r'["""].{10,200}["""]', text))  # Quoted text segments

    # According to phrases
    according_to = len(re.findall(r'\baccording to\b', text, re.IGNORECASE))

    # Page citations
    page_citations = len(re.findall(r'\bpage \d+\b', text, re.IGNORECASE))

    # Document reveal language
    document_reveals = 0
    reveal_patterns = [r'\bnotice this\b', r'\breading directly from\b', r'\blook at this\b']
    for pattern in reveal_patterns:
        document_reveals += len(re.findall(pattern, text, re.IGNORECASE))

    # Quote density (quoted segments per 1000 words)
    quoted_segments = len(re.findall(r'["""].{10,200}["""]', text))
    quote_density = (quoted_segments / word_count * 1000) if word_count > 0 else 0

    return {
        'direct_quotes': direct_quotes,
        'according_to': according_to,
        'page_citations': page_citations,
        'document_reveals': document_reveals,
        'quote_density': round(quote_density, 2)
    }


def analyze_pacing(text: str) -> Dict[str, Any]:
    """
    Analyze structural pacing metrics.

    Metrics:
    - word_count: Total words
    - paragraph_count: Double-newline separated blocks
    - avg_paragraph_words: Average words per paragraph
    - question_count: Total question marks (engagement signals)
    - questions_per_1000_words: Normalized question density
    """
    words = text.split()
    word_count = len(words)

    # Paragraphs (double newline separated)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)

    avg_paragraph_words = round(word_count / paragraph_count, 1) if paragraph_count > 0 else 0

    # Questions
    question_count = text.count('?')
    questions_per_1000_words = round((question_count / word_count * 1000), 2) if word_count > 0 else 0

    return {
        'word_count': word_count,
        'paragraph_count': paragraph_count,
        'avg_paragraph_words': avg_paragraph_words,
        'question_count': question_count,
        'questions_per_1000_words': questions_per_1000_words
    }


def analyze_transcript_file(file_path: Path) -> Dict[str, Any]:
    """
    Full analysis pipeline for single transcript file.

    Returns consolidated analysis with:
    - metadata (file, creator, format)
    - opening_hook analysis
    - transitions list
    - evidence_patterns
    - pacing metrics
    """
    text = read_transcript(file_path)

    if text.startswith('[ERROR'):
        return {
            'file': str(file_path),
            'error': text
        }

    creator = get_creator_name(file_path)

    analysis = {
        'file': str(file_path),
        'creator': creator,
        'format': file_path.suffix,
        'analyzed_at': datetime.now().isoformat(),
        'opening_hook': extract_opening_hook(text),
        'transitions': extract_transitions(text),
        'evidence_patterns': extract_evidence_patterns(text),
        'pacing': analyze_pacing(text)
    }

    return analysis


def analyze_all_transcripts(transcripts_dir: Path) -> List[Dict[str, Any]]:
    """
    Batch analysis of all transcripts in directory.

    Discovers .txt, .srt, .vtt files recursively, analyzes each,
    prints progress to stderr.
    """
    # Discover all transcript files
    extensions = ['.txt', '.srt', '.vtt']
    files = []
    for ext in extensions:
        files.extend(transcripts_dir.rglob(f'*{ext}'))

    logger.info("Discovered %d transcript files", len(files))

    results = []
    for i, file_path in enumerate(files, 1):
        logger.debug("[%d/%d] Analyzing %s...", i, len(files), file_path.name)
        analysis = analyze_transcript_file(file_path)
        results.append(analysis)

    logger.info("Analysis complete: %d files processed", len(results))
    return results


def get_stats(transcripts_dir: Path) -> Dict[str, Any]:
    """
    Get distribution statistics for transcripts.

    Returns counts by:
    - Total files
    - Format breakdown (.txt, .srt, .vtt)
    - Creator breakdown
    """
    extensions = ['.txt', '.srt', '.vtt']
    files = []
    for ext in extensions:
        files.extend(transcripts_dir.rglob(f'*{ext}'))

    format_counts = Counter([f.suffix for f in files])
    creator_counts = Counter([get_creator_name(f) for f in files])

    return {
        'total_files': len(files),
        'by_format': dict(format_counts),
        'by_creator': dict(creator_counts)
    }


def main():
    parser = argparse.ArgumentParser(description='Transcript Analysis Pipeline')
    parser.add_argument('--analyze-all', action='store_true',
                        help='Analyze all transcripts and print JSON summary')
    parser.add_argument('--analyze', metavar='FILE',
                        help='Analyze single transcript file')
    parser.add_argument('--stats', action='store_true',
                        help='Print transcript distribution statistics')
    parser.add_argument('--transcripts-dir', metavar='DIR',
                        help='Override transcripts directory (default: ../../transcripts)')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Default transcripts directory (relative to script location)
    if args.transcripts_dir:
        transcripts_dir = Path(args.transcripts_dir)
    else:
        script_dir = Path(__file__).parent
        transcripts_dir = script_dir / '../../transcripts'

    transcripts_dir = transcripts_dir.resolve()

    if not transcripts_dir.exists():
        print(f"ERROR: Transcripts directory not found: {transcripts_dir}", file=sys.stderr)
        sys.exit(1)

    if args.stats:
        stats = get_stats(transcripts_dir)
        print(json.dumps(stats, indent=2))

    elif args.analyze:
        file_path = Path(args.analyze)
        if not file_path.exists():
            print(f"ERROR: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        analysis = analyze_transcript_file(file_path)
        print(json.dumps(analysis, indent=2))

    elif args.analyze_all:
        results = analyze_all_transcripts(transcripts_dir)
        # Print summary to stdout
        summary = {
            'total_analyzed': len(results),
            'analyzed_at': datetime.now().isoformat(),
            'transcripts_dir': str(transcripts_dir),
            'analyses': results
        }
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
