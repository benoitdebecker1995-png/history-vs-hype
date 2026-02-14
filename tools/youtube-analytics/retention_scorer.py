"""
Retention Scorer Module

Scores script sections for predicted retention risk based on length, evidence
density, modern relevance proximity, and voice pattern presence.

Generates actionable warnings referencing STYLE-GUIDE patterns.

Usage:
    from retention_scorer import score_section, score_all_sections

    # Score single section
    result = score_section(
        section_text="According to Smith...",
        section_type="body",
        topic_type="territorial"
    )

    # Score all sections
    from parser import ScriptParser
    parser = ScriptParser()
    sections = parser.parse_file('script.md')
    results = score_all_sections(sections, 'territorial')
    print(format_retention_warnings(results))

CLI:
    python retention_scorer.py SCRIPT_PATH [--topic TOPIC_TYPE]
    python retention_scorer.py --help
"""

import sys
import re
from pathlib import Path
from statistics import mean, stdev

# Feature flag for KeywordDB availability
SCORER_AVAILABLE = True

# Try to import KeywordDB for topic baseline data
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / 'discovery'))
    from database import KeywordDB
except ImportError:
    SCORER_AVAILABLE = False
    KeywordDB = None

# Try to import load_voice_patterns from section_diagnostics
try:
    from section_diagnostics import load_voice_patterns
except ImportError:
    # Fallback: minimal pattern detection
    def load_voice_patterns():
        return {
            'transitions': {},
            'evidence': {},
            'rhythm': {},
            'openings': {},
            'closings': {},
            'additional': {}
        }


def count_evidence_markers(text):
    """
    Count evidence markers in text.

    Markers include:
    - "according to"
    - "page "
    - "in his", "in her"
    - "the treaty states", "the document shows"
    - Direct quotes (text between quotation marks)

    Args:
        text: Section text to analyze

    Returns:
        Integer count of evidence markers found
    """
    if not text:
        return 0

    text_lower = text.lower()
    count = 0

    # Count phrase markers
    markers = [
        'according to',
        'page ',
        'in his',
        'in her',
        'the treaty states',
        'the document shows'
    ]

    for marker in markers:
        count += text_lower.count(marker)

    # Count direct quotes (text between quotation marks)
    quote_pattern = r'["\']([^"\']+)["\']'
    quotes = re.findall(quote_pattern, text)
    count += len(quotes)

    return count


def measure_modern_relevance_gap(text):
    """
    Measure word gap from last modern relevance marker to end of text.

    Modern markers: "today", "2024", "2025", "2026", "currently",
                     "modern", "now", "recent", "still"

    Args:
        text: Section text to analyze

    Returns:
        Integer word count from last modern marker to end.
        If no marker found, returns total word count.
        If marker is in last word, returns 0.
    """
    if not text:
        return 0

    words = text.split()
    if not words:
        return 0

    # Modern relevance markers with word boundary patterns
    markers = [
        r'\btoday\b',
        r'\b2024\b',
        r'\b2025\b',
        r'\b2026\b',
        r'\bcurrently\b',
        r'\bmodern\b',
        r'\bnow\b',
        r'\brecent\b',
        r'\bstill\b'
    ]

    # Find last occurrence of any marker using regex word boundaries
    last_position = -1

    for marker_pattern in markers:
        matches = list(re.finditer(marker_pattern, text, re.IGNORECASE))
        if matches:
            pos = matches[-1].start()
            if pos > last_position:
                last_position = pos

    # No marker found
    if last_position == -1:
        return len(words)

    # Count words after last marker
    text_after_marker = text[last_position:]
    words_after = text_after_marker.split()

    # Subtract 1 because the marker itself is one word
    gap = max(0, len(words_after) - 1)

    return gap


def detect_voice_patterns(text):
    """
    Detect voice patterns from STYLE-GUIDE Part 6.

    Checks for:
    - Causal connectors ("consequently", "thereby", "which meant that")
    - Evidence markers (overlap with count_evidence_markers)
    - Rhythm patterns (short fragments after long sentences)
    - Question patterns ("?")

    Args:
        text: Section text to analyze

    Returns:
        List of detected pattern names/types
    """
    if not text:
        return []

    patterns_found = []
    text_lower = text.lower()

    # Causal connectors
    causal_connectors = [
        'consequently',
        'thereby',
        'which meant that',
        'as a result',
        'which created'
    ]

    for connector in causal_connectors:
        if connector in text_lower:
            patterns_found.append('causal_chain')
            break

    # Evidence markers
    evidence_markers = [
        'according to',
        'the treaty states',
        'the document shows',
        'reading directly from'
    ]

    for marker in evidence_markers:
        if marker in text_lower:
            patterns_found.append('evidence_introduction')
            break

    # Question patterns
    if '?' in text:
        patterns_found.append('question_pattern')

    # Rhythm patterns: look for short sentence after longer text
    # Simple heuristic: sentence ending with period followed by short sentence (< 6 words)
    sentences = re.split(r'[.!?]+', text)
    for i in range(len(sentences) - 1):
        current_words = len(sentences[i].split())
        next_words = len(sentences[i + 1].split())

        if current_words > 20 and next_words < 6 and next_words > 0:
            patterns_found.append('rhythm_variation')
            break

    return patterns_found


def get_topic_baseline(topic_type):
    """
    Get baseline metrics for topic type from video_performance database.

    Falls back to channel average when topic has <3 videos.
    Falls back to hardcoded defaults when no database data available.

    Args:
        topic_type: String topic type ('territorial', 'ideological', etc.)

    Returns:
        Dict with baseline metrics:
        {
            'avg_section_length': int,
            'std_dev_length': int,
            'avg_evidence_density': float,
            'avg_modern_relevance_gap': int,
            'high_retention_patterns': list,
            'video_count': int,
            'confidence': 'default' | 'channel_avg' | 'topic_specific'
        }
    """
    # Hardcoded defaults (used when no database data available)
    defaults = {
        'avg_section_length': 150,
        'std_dev_length': 50,
        'avg_evidence_density': 0.5,
        'avg_modern_relevance_gap': 100,
        'high_retention_patterns': [],
        'video_count': 0,
        'confidence': 'default'
    }

    if not SCORER_AVAILABLE or KeywordDB is None:
        return defaults

    try:
        db = KeywordDB()
        all_performance = db.get_all_performance()

        if not all_performance:
            return defaults

        # Filter by topic type
        topic_videos = [v for v in all_performance if v.get('topic_type') == topic_type]

        # If <3 videos for this topic, use channel average
        if len(topic_videos) < 3:
            topic_videos = all_performance
            confidence = 'channel_avg'
        else:
            confidence = 'topic_specific'

        # Calculate baseline metrics
        # Note: lessons_learned may not have section-level data yet
        # For now, use simple averages from available data

        section_lengths = []
        evidence_densities = []
        relevance_gaps = []

        # Extract metrics from lessons_learned JSON if available
        for video in topic_videos:
            lessons = video.get('lessons_learned', '{}')
            if isinstance(lessons, str):
                import json
                try:
                    lessons = json.loads(lessons)
                except:
                    lessons = {}

            # For now, use placeholder values
            # In future, extract from actual section analysis
            section_lengths.append(150)  # placeholder

        # Calculate averages
        if section_lengths:
            avg_length = int(mean(section_lengths))
            std_dev = int(stdev(section_lengths)) if len(section_lengths) > 1 else 50
        else:
            avg_length = 150
            std_dev = 50

        return {
            'avg_section_length': avg_length,
            'std_dev_length': std_dev,
            'avg_evidence_density': 0.5,  # placeholder
            'avg_modern_relevance_gap': 100,  # placeholder
            'high_retention_patterns': [],
            'video_count': len(topic_videos),
            'confidence': confidence
        }

    except Exception:
        return defaults


def score_section(section_text, section_type, topic_type, baseline=None):
    """
    Score a script section for predicted retention risk.

    Analyzes:
    - Word count vs. topic baseline
    - Evidence density (markers per 100 words)
    - Modern relevance gap (words since last modern connection)
    - Voice pattern presence

    Generates warnings for specific issues with STYLE-GUIDE pattern recommendations.

    Args:
        section_text: Full text content of section
        section_type: 'intro', 'body', 'conclusion'
        topic_type: 'territorial', 'ideological', etc.
        baseline: Optional baseline dict (will fetch if not provided)

    Returns:
        {
            'score': float (0.0-1.0),
            'risk_level': 'LOW' | 'MEDIUM' | 'HIGH',
            'warnings': [
                {
                    'issue': str,
                    'severity': str,
                    'recommendation': str,
                    'pattern_ref': str
                },
                ...
            ],
            'metrics': {
                'word_count': int,
                'evidence_density': float,
                'modern_relevance_gap': int,
                'voice_patterns_found': list
            }
        }
    """
    if not section_text:
        return {
            'score': 0.5,
            'risk_level': 'MEDIUM',
            'warnings': [],
            'metrics': {}
        }

    try:
        # Get baseline if not provided
        if baseline is None:
            baseline = get_topic_baseline(topic_type)

        # Calculate metrics
        word_count = len(section_text.split())
        evidence_count = count_evidence_markers(section_text)
        evidence_density = (evidence_count / word_count * 100) if word_count > 0 else 0
        modern_gap = measure_modern_relevance_gap(section_text)
        voice_patterns = detect_voice_patterns(section_text)

        # Calculate deviation scores
        # Length deviation (normalized)
        length_diff = word_count - baseline['avg_section_length']
        std_dev = baseline['std_dev_length']
        length_deviation = max(0, length_diff / std_dev) if std_dev > 0 else 0

        # Evidence penalty (scale to 0-1 range)
        # Low evidence density (<0.5) should be heavily penalized
        evidence_penalty = max(0, (baseline['avg_evidence_density'] - evidence_density) / baseline['avg_evidence_density'])

        # Relevance penalty (normalize to 0-1 range)
        # Gap >150 words = major penalty
        relevance_penalty = min(1.0, max(0, modern_gap - 100) / 100)

        # Pattern bonus
        pattern_bonus = min(0.2, len(voice_patterns) * 0.05)

        # Composite score - adjusted weights for stronger penalties
        raw_score = 1.0 - (
            length_deviation * 0.2 +
            evidence_penalty * 0.35 +
            relevance_penalty * 0.4
        ) + pattern_bonus

        # Clamp to 0.0-1.0
        score = max(0.0, min(1.0, raw_score))

        # Generate warnings
        warnings = []
        text_lower = section_text.lower()

        # Warning 1: Excessive length
        if length_diff > baseline['std_dev_length'] * 1.5:
            warnings.append({
                'issue': f'Section exceeds topic baseline by {length_diff} words',
                'severity': 'HIGH',
                'recommendation': 'Break into smaller sections with pattern interrupts',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.4 (rhythm variation)'
            })

        # Warning 2: Low evidence density
        if evidence_density < 0.3:
            warnings.append({
                'issue': 'Low evidence density - few source citations',
                'severity': 'MEDIUM',
                'recommendation': 'Add academic quotes or primary sources with attribution',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.3 Pattern 1 (Setup → Quote → Implication)'
            })

        # Warning 3: Large modern relevance gap
        # If gap equals word count, there's NO modern relevance at all
        # If gap > 150 words OR no modern markers in long section
        if modern_gap > 150 or (modern_gap == word_count and word_count > 100):
            warnings.append({
                'issue': f'Modern relevance gap: {modern_gap} words since last connection',
                'severity': 'HIGH',
                'recommendation': 'Add modern relevance bridge connecting history to present',
                'pattern_ref': 'STYLE-GUIDE.md Part 2 (modern relevance every 90 seconds)'
            })

        # Warning 4: Abstract opening (intro only)
        if section_type == 'intro':
            abstract_starters = ['the concept', 'the idea', 'the notion', 'to understand', 'in order to']
            if any(text_lower[:50].startswith(starter) for starter in abstract_starters):
                warnings.append({
                    'issue': 'Abstract opening - no concrete anchor',
                    'severity': 'HIGH',
                    'recommendation': 'Start with concrete date/place/document instead of abstraction',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.1 Pattern 1-2 (Visual Contrast or Current Event Hook)'
                })

        # Warning 5: Weak closing (conclusion only)
        if section_type == 'conclusion':
            closing_markers = ['today', 'still', 'watching', 'question', 'who', 'never got', 'why does', 'future', 'continues']
            if not any(marker in text_lower for marker in closing_markers):
                warnings.append({
                    'issue': 'Weak closing - no forward-looking statement',
                    'severity': 'MEDIUM',
                    'recommendation': 'Apply proven closing pattern from Part 6.5',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.5 Pattern 1-3 (Stakeholders, Unanswered Question, Modern Relevance)'
                })

        # Determine risk level
        if score < 0.5:
            risk_level = 'HIGH'
        elif score < 0.7:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'score': score,
            'risk_level': risk_level,
            'warnings': warnings,
            'metrics': {
                'word_count': word_count,
                'evidence_density': evidence_density,
                'modern_relevance_gap': modern_gap,
                'voice_patterns_found': voice_patterns
            }
        }

    except Exception:
        # Return safe defaults on error
        return {
            'score': 0.5,
            'risk_level': 'MEDIUM',
            'warnings': [],
            'metrics': {}
        }


def score_all_sections(sections, topic_type):
    """
    Score all sections in batch.

    Gets baseline once and reuses for efficiency.

    Args:
        sections: List of Section objects with .heading and .text attributes
        topic_type: 'territorial', 'ideological', etc.

    Returns:
        List of score dicts, one per section, with added 'section_heading' field
    """
    if not sections:
        return []

    try:
        # Get baseline once
        baseline = get_topic_baseline(topic_type)

        results = []

        for section in sections:
            # Determine section type from heading
            heading_lower = section.heading.lower()
            if any(word in heading_lower for word in ['intro', 'opening', 'hook']):
                section_type = 'intro'
            elif any(word in heading_lower for word in ['conclusion', 'closing', 'summary']):
                section_type = 'conclusion'
            else:
                section_type = 'body'

            # Score section
            result = score_section(
                section_text=section.text,
                section_type=section_type,
                topic_type=topic_type,
                baseline=baseline
            )

            # Add section heading
            result['section_heading'] = section.heading

            results.append(result)

        return results

    except Exception:
        return []


def format_retention_warnings(scored_sections):
    """
    Format retention warnings as markdown table.

    Shows only MEDIUM and HIGH risk sections.

    Args:
        scored_sections: List of score dicts from score_all_sections

    Returns:
        Formatted markdown string showing risky sections
    """
    if not scored_sections:
        return "No sections to analyze."

    try:
        # Filter to MEDIUM and HIGH only
        risky_sections = [
            s for s in scored_sections
            if s.get('risk_level') in ['MEDIUM', 'HIGH']
        ]

        if not risky_sections:
            return "All sections scored LOW risk."

        # Build markdown table
        lines = []
        lines.append("# Retention Risk Warnings\n")
        lines.append("| Section | Risk | Score | Top Warning |")
        lines.append("|---------|------|-------|-------------|")

        for section in risky_sections:
            heading = section.get('section_heading', 'Unknown')
            risk = section.get('risk_level', 'UNKNOWN')
            score = section.get('score', 0)
            warnings = section.get('warnings', [])

            # Get top warning
            if warnings:
                top_warning = warnings[0].get('issue', 'No details')
            else:
                top_warning = 'No specific issues detected'

            lines.append(f"| {heading} | {risk} | {score:.2f} | {top_warning} |")

        lines.append("")

        # Add detailed recommendations
        lines.append("## Detailed Recommendations\n")

        for section in risky_sections:
            heading = section.get('section_heading', 'Unknown')
            warnings = section.get('warnings', [])

            if not warnings:
                continue

            lines.append(f"### {heading}\n")

            for warning in warnings:
                lines.append(f"**{warning.get('issue', 'Issue')}** ({warning.get('severity', 'MEDIUM')})")
                lines.append(f"- Fix: {warning.get('recommendation', 'No recommendation')}")
                lines.append(f"- Reference: {warning.get('pattern_ref', 'See STYLE-GUIDE.md')}")
                lines.append("")

        return '\n'.join(lines)

    except Exception:
        return "Error formatting retention warnings."


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Score script sections for predicted retention risk'
    )
    parser.add_argument(
        'script_path',
        nargs='?',
        help='Path to script file'
    )
    parser.add_argument(
        '--topic',
        default='territorial',
        help='Topic type (territorial, ideological, etc.)'
    )

    args = parser.parse_args()

    if not args.script_path:
        parser.print_help()
        print("\nExamples:")
        print("  python retention_scorer.py script.md --topic territorial")
        print("  python retention_scorer.py script.md")
        sys.exit(0)

    # Try to import ScriptParser
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / 'production'))
        from parser import ScriptParser

        parser_obj = ScriptParser()
        sections = parser_obj.parse_file(args.script_path)

        if not sections:
            print("Error: No sections found in script")
            sys.exit(1)

        # Score all sections
        results = score_all_sections(sections, args.topic)

        # Print formatted warnings
        print(format_retention_warnings(results))

    except ImportError:
        print("Error: ScriptParser not available")
        print("Install production tools or use as library:")
        print("  from retention_scorer import score_section")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
