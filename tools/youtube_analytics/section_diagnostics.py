"""
Section Diagnostics Module

Diagnoses WHY retention dropped in script sections and recommends
specific voice patterns from STYLE-GUIDE.md Part 6.

Usage:
    from section_diagnostics import diagnose_section_drop, diagnose_all_drops

    # Diagnose single section
    diagnosis = diagnose_section_drop(
        section_text="The concept of sovereignty...",
        section_heading="Introduction",
        section_type="intro",
        drop_magnitude=0.12
    )

    # Diagnose all drops
    diagnoses = diagnose_all_drops(mapped_drops, sections)
"""

import re

from tools.logging_config import get_logger

logger = get_logger(__name__)


def load_voice_patterns():
    """
    Load voice patterns from STYLE-GUIDE.md Part 6.

    Returns:
        Dict of voice patterns organized by category:
        {
            'openings': {...},
            'transitions': {...},
            'evidence': {...},
            'rhythm': {...}
        }

    Note: Hardcoded from STYLE-GUIDE.md Part 6 (29 patterns across 6 categories)
    """
    return {
        'openings': {
            'visual_contrast_hook': {
                'name': 'Visual Contrast Hook',
                'formula': '[Show visual A] → [Show visual B] → [State tension]',
                'when': 'Territorial disputes with map changes',
                'style_guide_ref': 'Part 6.1 Pattern 1'
            },
            'current_event_hook': {
                'name': 'Current Event Hook',
                'formula': '[Specific date/time] → [Military action] → [Quote] → [Context]',
                'when': 'Active territorial disputes with military dimension',
                'style_guide_ref': 'Part 6.1 Pattern 2'
            },
            'fact_check_declaration': {
                'name': 'Fact-Check Declaration',
                'formula': '[Quote from figure] → "I fact-checked..." → "Here\'s what [authority] says."',
                'when': 'Political figure fact-checks',
                'style_guide_ref': 'Part 6.1 Pattern 3'
            },
            'personal_research_authority': {
                'name': 'Personal Research Authority',
                'formula': '[Dispute] → "So, I read that [document]." → [What it says]',
                'when': 'Establishing documentary evidence early',
                'style_guide_ref': 'Part 6.1 Pattern 4'
            },
            'escalation_timeline': {
                'name': 'Escalation Timeline',
                'formula': '[Incident] → [X days later] → [High-level response] → [Counter-response]',
                'when': 'Diplomatic crisis with recent confrontation',
                'style_guide_ref': 'Part 6.1 Pattern 5'
            }
        },
        'transitions': {
            'causal_chain': {
                'name': 'Kraut-Style Causal Chain',
                'formula': '[Event A] → consequently/thereby/which meant that → [Result B] → [Result C]',
                'when': 'Explaining multi-step causation',
                'style_guide_ref': 'Part 6.2 Pattern 1'
            },
            'temporal_jump': {
                'name': 'Temporal Jump with "Now"',
                'formula': '[Complete section] → "Now" → [New topic/time] → [Bridge]',
                'when': 'Contrasting two perspectives or time periods',
                'style_guide_ref': 'Part 6.2 Pattern 2'
            },
            'how_did_we_get_here': {
                'name': '"So how did we get here?"',
                'formula': '[Present consequence] → "So how did we get here?" → [Historical chronology]',
                'when': 'Pivoting from modern to historical',
                'style_guide_ref': 'Part 6.2 Pattern 3'
            },
            'but_heres_where_interesting': {
                'name': '"But here\'s where it gets interesting"',
                'formula': '[Expected narrative] → "But here\'s where it gets interesting." → [Complication]',
                'when': 'Introducing complication (1x per script max)',
                'style_guide_ref': 'Part 6.2 Pattern 4'
            },
            'look_what_happened': {
                'name': '"Look at what just happened"',
                'formula': '[Events] → "Look at what just happened." → [Pattern revealed]',
                'when': 'Revealing pattern or manipulation',
                'style_guide_ref': 'Part 6.2 Pattern 5'
            },
            'which_brings_us': {
                'name': '"Which brings us to..."',
                'formula': '[Context complete] → "Which brings us to [key moment]" → [New section]',
                'when': 'Moving from background to key moment',
                'style_guide_ref': 'Part 6.2 Pattern 6'
            },
            'date_as_break': {
                'name': 'Date as Section Break',
                'formula': '[Narrative] → [DATE.] → [New event] → [Connection]',
                'when': 'Chronological sequence',
                'style_guide_ref': 'Part 6.2 Pattern 7'
            },
            'contrast_pair': {
                'name': 'Contrast Pair (Competing Perspectives)',
                'formula': '[Side A perspective] → [Side B saw it different] → [Why divergence matters]',
                'when': 'Showing two sides interpret same events differently',
                'style_guide_ref': 'Part 6.2 Pattern 8'
            }
        },
        'evidence': {
            'setup_quote_implication': {
                'name': 'Setup → Quote → Implication',
                'formula': '[State claim] → [Source + quote] → [Repeat key number] → [Why it matters]',
                'when': 'Introducing academic quotes or primary sources',
                'style_guide_ref': 'Part 6.3 Pattern 1'
            },
            'notice_this_phrase': {
                'name': '"Notice this specific phrase"',
                'formula': '[Document shown] → "Notice this phrase." → [Quote] → [Why wording matters]',
                'when': 'Close-reading treaty/document language',
                'style_guide_ref': 'Part 6.3 Pattern 2'
            },
            'heres_what_actually_says': {
                'name': '"Here\'s what [X] actually says"',
                'formula': '"Here\'s what [document] actually says." → [Display] → [Key phrase] → [Interpretation]',
                'when': 'Document reveal (B-roll moment, 2-4x per script max)',
                'style_guide_ref': 'Part 6.3 Pattern 3'
            },
            'reading_directly_from': {
                'name': '"Reading directly from..."',
                'formula': '"Reading directly from [source]:" → [Exact quote] → [Plain language translation]',
                'when': 'Formal document language needs exact quoting',
                'style_guide_ref': 'Part 6.3 Pattern 4'
            },
            'quote_stacking': {
                'name': 'Quote Stacking (Authority Stack)',
                'formula': '[Disputed claim] → [Authority 1 + quote] → [Authority 2 + quote] → "So what\'s going on?"',
                'when': 'Multiple sources confirm same fact',
                'style_guide_ref': 'Part 6.3 Pattern 5'
            }
        },
        'rhythm': {
            'long_setup_short_punch': {
                'name': 'Long Setup + Short Punch',
                'formula': '[Long sentence with details, commas, context]. [Short 2-5 word verdict].',
                'when': 'Creates emphasis through contrast',
                'style_guide_ref': 'Part 6.4 Pattern 1'
            },
            'question_zero_answer': {
                'name': 'Question → Zero/None Answer',
                'formula': '[Question about inclusion/evidence]? Zero. / None.',
                'when': 'Dramatic emphasis on exclusion/absence',
                'style_guide_ref': 'Part 6.4 Pattern 2'
            },
            'fragment_for_verdict': {
                'name': 'Fragment for Verdict',
                'formula': '[Context building tension]. [2-5 word declarative]. [Continue].',
                'when': 'Delivers moral or factual judgment with weight',
                'style_guide_ref': 'Part 6.4 Pattern 3'
            },
            'contrast_pair_rhythm': {
                'name': 'Contrast Pair (This vs. That)',
                'formula': '[Side A] [verb] it as [interpretation]. [Side B] [verb] it as [opposite].',
                'when': 'Highlights contradiction in parallel structure',
                'style_guide_ref': 'Part 6.4 Pattern 4'
            }
        },
        'closings': {
            'overlooked_stakeholders': {
                'name': 'Return to Overlooked Stakeholders',
                'formula': '[Big-picture stakes] → [Return to who\'s actually affected] → [Timeline contrast] → [Final exclusion statement]',
                'when': 'Ending with human cost, indigenous exclusion',
                'style_guide_ref': 'Part 6.5 Pattern 1'
            },
            'unanswered_question': {
                'name': 'Unanswered Question (Almada Pattern)',
                'formula': '[What was found] → [What perpetrators believed] → "So the question isn\'t just [historical]" → "It\'s [present-tense question]"',
                'when': 'Stories about discovered secrets, when the pattern could repeat',
                'style_guide_ref': 'Part 6.5 Pattern 2'
            },
            'modern_relevance_closing': {
                'name': 'Modern Relevance (Vance Pattern)',
                'formula': '[Summarize myth-busting] → "Why does anyone in [year] care?" → [Modern policy connection] → [Final pattern statement]',
                'when': 'Political fact-checks, myth rehabilitation',
                'style_guide_ref': 'Part 6.5 Pattern 3'
            }
        },
        'additional': {
            'immediate_contradiction': {
                'name': 'Immediate Contradiction',
                'formula': '[What is claimed/shown publicly] → "But" → [What actually exists/happened]',
                'when': 'Opening seconds, revealing hypocrisy or gap between claim and reality',
                'style_guide_ref': 'Part 6.7 Pattern 1'
            },
            'specific_stakeholder_quote': {
                'name': 'Specific Stakeholder Quote',
                'formula': '[Name] is [credentials/position]. [What they said with exact quote]',
                'when': 'Giving voice to affected populations, indigenous perspectives',
                'style_guide_ref': 'Part 6.7 Pattern 2'
            },
            'bureaucratic_detail_horror': {
                'name': 'Bureaucratic Detail as Horror',
                'formula': '[What was found] → [Specific bureaucratic details] → [Understated conclusion]',
                'when': 'Showing how authoritarian regimes document their crimes',
                'style_guide_ref': 'Part 6.7 Pattern 3'
            },
            'timeline_acceleration': {
                'name': 'Timeline Acceleration',
                'formula': '[Normal timeframe] → [Actual timeframe] → [What timing reveals]',
                'when': 'Showing rushed or suspicious timing',
                'style_guide_ref': 'Part 6.7 Pattern 4'
            }
        }
    }


def diagnose_section_drop(section_text, section_heading, section_type, drop_magnitude, position_in_section=0.5):
    """
    Diagnose WHY viewers dropped in this section.

    Checks for anti-patterns:
    - Abstract opening (starts with "The concept", "To understand", etc.)
    - Missing causal chains (no "consequently", "thereby", "which meant that")
    - No evidence introduction (no quotes, "according to", page numbers)
    - Long paragraphs without breaks (>150 words without pattern interrupt)
    - Missing modern relevance (no "today", "2024", "2025", "2026", "currently", "modern")
    - Section-type specific issues

    Args:
        section_text: Full text content of section
        section_heading: H2 heading text
        section_type: 'intro', 'body', 'conclusion'
        drop_magnitude: Float (e.g., 0.08 = 8% drop)
        position_in_section: Float 0.0-1.0 where drop occurred within section

    Returns:
        {
            'root_causes': [str, ...],
            'recommendations': [
                {
                    'fix': str,
                    'pattern': str,
                    'pattern_ref': str,
                    'insertion_hint': str
                },
                ...
            ],
            'severity': 'HIGH' | 'MEDIUM' | 'LOW',
            'confidence': 'high' | 'medium' | 'low'
        }
    """
    try:
        patterns = load_voice_patterns()
        root_causes = []
        recommendations = []

        text_lower = section_text.lower()

        # Check 1: Abstract opening
        abstract_starters = ['the concept', 'the idea', 'to understand', 'in order to', 'the notion']
        if any(text_lower[:50].startswith(starter) for starter in abstract_starters):
            root_causes.append('Abstract opening - no concrete anchor')
            recommendations.append({
                'fix': 'Start with concrete date/place/document instead of abstraction',
                'pattern': 'Visual Contrast Hook or Current Event Hook',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.1 Pattern 1-2',
                'insertion_hint': 'Replace first sentence with: [Specific date], [action with details], [quote/evidence].'
            })

        # Check 2: Missing causal chains
        causal_connectors = ['consequently', 'thereby', 'which meant that', 'as a result', 'which created']
        if not any(connector in text_lower for connector in causal_connectors):
            root_causes.append('Missing causal chain - sequence without causation')
            recommendations.append({
                'fix': 'Add causal chain to show WHY things happened, not just WHAT',
                'pattern': 'Kraut-Style Causal Chain',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.2 Pattern 1',
                'insertion_hint': 'After describing event, add: "which meant that [consequence], consequently [implication]."'
            })

        # Check 3: Missing evidence introduction
        evidence_markers = ['according to', 'page ', 'in his', 'in her', 'the treaty states', 'the document shows']
        if not any(marker in text_lower for marker in evidence_markers):
            root_causes.append('No evidence introduction - claims without sources')
            recommendations.append({
                'fix': 'Introduce academic quotes or primary sources with attribution',
                'pattern': 'Setup → Quote → Implication',
                'pattern_ref': 'STYLE-GUIDE.md Part 6.3 Pattern 1',
                'insertion_hint': 'Add: "According to [historian] in [book], page [#]: \'[quote]\'. [Why it matters]."'
            })

        # Check 4: Missing modern relevance
        modern_markers = ['today', '2024', '2025', '2026', 'currently', 'modern', 'now', 'recent']
        if not any(marker in text_lower for marker in modern_markers):
            root_causes.append('Missing modern relevance - no connection to present')
            recommendations.append({
                'fix': 'Connect historical events to current consequences',
                'pattern': 'Modern relevance bridge',
                'pattern_ref': 'STYLE-GUIDE.md Part 2 (modern relevance every 90 seconds)',
                'insertion_hint': 'Add: "which is why today [current consequence/dispute/debate]."'
            })

        # Check 5: Long paragraphs without rhythm breaks
        if len(section_text) > 150:
            # Check for pattern interrupts (questions, short punches, zero/none moments)
            interrupt_markers = ['?', '. zero', '. none', '. they won', '. britain']
            interrupt_count = sum(1 for marker in interrupt_markers if marker in text_lower)
            if interrupt_count == 0:
                root_causes.append('Long section without pacing variation')
                recommendations.append({
                    'fix': 'Add pattern interrupt for pacing',
                    'pattern': 'Long Setup + Short Punch or Question → Zero Answer',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.4 Pattern 1-2',
                    'insertion_hint': 'After long buildup, add short declarative: "They didn\'t." or "How many? Zero."'
                })

        # Check 6: Conclusion-specific checks
        if section_type == 'conclusion':
            # Check for weak ending (no stakeholder reference, no forward question, no modern connection)
            closing_markers = ['today', 'still', 'watching', 'question', 'who', 'never got', 'why does']
            if not any(marker in text_lower for marker in closing_markers):
                root_causes.append('Weak closing - no forward-looking statement or stakeholder reference')
                recommendations.append({
                    'fix': 'Apply a proven closing pattern from Part 6.5',
                    'pattern': 'Return to Overlooked Stakeholders or Unanswered Question',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.5 Pattern 1-2',
                    'insertion_hint': 'End with: "And [affected group] never got a vote." or "So the question isn\'t [historical]. It\'s [present-tense]."'
                })

        # Check 7: Section-type specific
        if section_type == 'intro' and position_in_section < 0.3:
            # Intro drop early = weak hook
            if not any(text_lower[:100].startswith(hook) for hook in ['open a map', 'on ', 'march ', 'in ']):
                root_causes.append('Weak opening hook - no immediate stakes')
                recommendations.append({
                    'fix': 'Start with concrete visual contrast or current event',
                    'pattern': 'Visual Contrast Hook or Current Event Hook',
                    'pattern_ref': 'STYLE-GUIDE.md Part 6.1 Pattern 1-2',
                    'insertion_hint': 'Open with: "Open a map of [region], you see [A]. Now open [B]\'s map. [Contradiction]."'
                })

        # Determine severity
        if drop_magnitude > 0.10:
            severity = 'HIGH'
        elif drop_magnitude >= 0.05:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'

        # Determine confidence
        if drop_magnitude > 0.10 and len(root_causes) >= 2:
            confidence = 'high'
        elif drop_magnitude >= 0.05 or len(root_causes) >= 1:
            confidence = 'medium'
        else:
            confidence = 'low'

        return {
            'root_causes': root_causes,
            'recommendations': recommendations,
            'severity': severity,
            'confidence': confidence
        }

    except Exception:
        # Return empty diagnosis on error
        return {
            'root_causes': [],
            'recommendations': [],
            'severity': 'LOW',
            'confidence': 'low'
        }


def diagnose_all_drops(mapped_drops, sections):
    """
    Diagnose all mapped drops in batch.

    Args:
        mapped_drops: List of mapped drop dicts from retention_mapper.py
        sections: List of Section objects from parser.py

    Returns:
        List of diagnosis dicts, one per drop, sorted by severity then magnitude.
        Each diagnosis includes section_heading and drop_magnitude fields.
    """
    try:
        # Create section lookup
        section_lookup = {s.heading: s for s in sections}

        diagnoses = []

        for drop in mapped_drops:
            section_heading = drop.get('section_heading', '')
            section = section_lookup.get(section_heading)

            if not section:
                continue

            # Run diagnosis
            diagnosis = diagnose_section_drop(
                section_text=section.content,
                section_heading=section_heading,
                section_type=drop.get('section_type', 'body'),
                drop_magnitude=drop.get('drop_magnitude', 0),
                position_in_section=drop.get('position_in_section', 0.5)
            )

            # Add drop context
            diagnosis['section_heading'] = section_heading
            diagnosis['drop_magnitude'] = drop.get('drop_magnitude', 0)

            diagnoses.append(diagnosis)

        # Sort by severity (HIGH first), then magnitude (biggest first)
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        diagnoses.sort(key=lambda d: (severity_order.get(d['severity'], 3), -d['drop_magnitude']))

        return diagnoses

    except Exception:
        return []


def format_diagnostics_markdown(diagnoses):
    """
    Format all diagnoses as markdown report.

    Groups by severity (HIGH → MEDIUM → LOW).
    Shows section name, drop %, root causes, recommended patterns.
    Includes confidence flag when applicable.

    Args:
        diagnoses: List of diagnosis dicts from diagnose_all_drops

    Returns:
        Formatted markdown string
    """
    if not diagnoses:
        return "No retention drops to diagnose."

    try:
        lines = []
        lines.append("# Section Diagnostics Report\n")

        # Group by severity
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            severity_drops = [d for d in diagnoses if d.get('severity') == severity]

            if not severity_drops:
                continue

            lines.append(f"## {severity} Priority Drops\n")

            for diagnosis in severity_drops:
                section = diagnosis.get('section_heading', 'Unknown')
                magnitude = diagnosis.get('drop_magnitude', 0)
                confidence = diagnosis.get('confidence', 'medium')

                lines.append(f"### {section} (Drop: {magnitude:.1%})\n")

                # Root causes
                root_causes = diagnosis.get('root_causes', [])
                if root_causes:
                    lines.append("**Root Causes:**")
                    for cause in root_causes:
                        lines.append(f"- {cause}")
                    lines.append("")

                # Recommendations
                recommendations = diagnosis.get('recommendations', [])
                if recommendations:
                    lines.append("**Recommended Fixes:**")
                    for rec in recommendations:
                        lines.append(f"- **{rec.get('pattern', 'Pattern')}** ({rec.get('pattern_ref', 'Reference')})")
                        lines.append(f"  - {rec.get('fix', 'Fix description')}")
                        if 'insertion_hint' in rec:
                            lines.append(f"  - *Hint:* {rec['insertion_hint']}")
                    lines.append("")

                # Confidence warning
                if confidence == 'low':
                    lines.append("*Note: Low confidence - limited historical data for this pattern.*\n")

        return '\n'.join(lines)

    except Exception:
        return "Error formatting diagnostics report."


if __name__ == '__main__':
    # Example usage
    print("Section Diagnostics Module")
    print("Usage: from section_diagnostics import diagnose_section_drop")
