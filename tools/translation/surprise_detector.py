"""
Surprise Clause Detector (TRAN-04)

Pure data processor. LLM calls handled by Claude Code via /translate command.

Post-translation analysis module that provides payload builders for comparing translated
clauses against user-provided narrative baselines, to identify clauses that contradict
common English-language narratives.

Three-tier severity classification:
- Major: Directly contradicts common narrative
- Notable: Significant omission (people don't know this clause exists)
- Minor: Adds nuance but doesn't fundamentally change narrative

Modular design: operates on translator output sections, can re-run with different
narratives without retranslating.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional, Callable


class SurpriseDetector:
    """
    Detect clauses where translation contradicts common English-language narratives.

    Pure data processor — no Anthropic SDK or API key needed.
    Claude Code executes LLM calls using payloads from build_surprise_payload().

    This is the "aha moment" generator for Untranslated Evidence videos.
    When a translated clause contradicts what English sources claim about the document,
    that becomes a highlight moment. Three-tier severity system maps to video pacing:
    Major surprises get the most screen time.
    """

    def build_surprise_payload(self, clause_text: str, translation: str,
                               narrative_baseline: str, clause_id: str,
                               source_language: str = 'unknown',
                               document_context: Optional[str] = None,
                               full_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a Claude Code payload for surprise clause detection.

        Claude Code executes the LLM call using this payload.

        Args:
            clause_text: Original source-language clause text
            translation: English translation of the clause
            narrative_baseline: What people commonly believe the document says
            clause_id: Clause identifier
            source_language: Source language name (for prompt context)
            document_context: Optional document description
            full_context: Optional full translated document for reference context

        Returns:
            {
                'clause_id': str,
                'system_prompt': str,
                'user_prompt': str
            }
        """
        system_prompt = """You are a historical document analyst specializing in comparing primary source translations against popular narratives.

Your task is to identify where the actual document text contradicts, complicates, or adds nuance missing from common English-language descriptions of this document.

Classification criteria:
- MAJOR: Directly contradicts the common narrative (what people believe vs. what document says are opposites)
- NOTABLE: Significant omission — people don't know this clause exists and it changes the understanding
- MINOR: Adds nuance but doesn't fundamentally change the narrative
- NONE: Clause aligns with or is already well-represented in the common narrative

For non-NONE classifications, provide:
1. Clear explanation of the discrepancy
2. What people commonly think (based on the narrative baseline)
3. What the document actually says (based on this clause)
4. A 1-2 sentence script suggestion for how to present this surprise moment in a video

Respond in JSON format."""

        context_desc = f" ({document_context})" if document_context else ""
        full_context_section = ""
        if full_context:
            preview = full_context[:2000]
            ellipsis = "..." if len(full_context) > 2000 else ""
            full_context_section = f"\n\nFull document translation (for reference):\n{preview}{ellipsis}"

        user_prompt = f"""# Common Narrative Baseline

{narrative_baseline}

# Document Context

Source language: {source_language}{context_desc}{full_context_section}

# Clause to Analyze

**ID:** {clause_id}

**Original ({source_language}):**
{clause_text}

**Translation (English):**
{translation}

# Task

Analyze whether this clause contradicts, complicates, or is entirely absent from the common narrative baseline.

Respond in JSON format:
{{
    "severity": "major" | "notable" | "minor" | "none",
    "explanation": "Why this is/isn't a surprise",
    "what_people_think": "What the common narrative claims (or omits)",
    "what_document_says": "What this clause actually reveals",
    "script_beat": "1-2 sentence suggestion for presenting this in video, or null if severity is none"
}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_surprise_response(self, response_text: str, clause_id: str,
                                original: str = '', translation: str = '') -> Dict[str, Any]:
        """
        Parse Claude Code's surprise detection response into a structured result.

        Args:
            response_text: Raw text response from Claude Code
            clause_id: Clause identifier
            original: Original source-language text (for including in result)
            translation: English translation (for including in result)

        Returns:
            For non-NONE severity:
            {
                'clause_id': str,
                'severity': 'major'|'notable'|'minor',
                'explanation': str,
                'what_people_think': str,
                'what_document_says': str,
                'script_beat': str,
                'original': str,
                'translation': str
            }

            For NONE severity:
            {'clause_id': str, 'severity': 'none'}

            {'clause_id': str, 'error': str} on parse failure
        """
        # Extract JSON from response (may be wrapped in markdown code blocks)
        text = response_text.strip()
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1] if lines[0].startswith('```') else lines)

        # Also handle ```json blocks
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()

        try:
            analysis = json.loads(text)
        except json.JSONDecodeError as e:
            return {'clause_id': clause_id, 'error': f'Failed to parse response as JSON: {str(e)}'}

        # Validate and normalize severity
        severity = analysis.get('severity', 'none').lower()
        if severity not in ['major', 'notable', 'minor', 'none']:
            severity = 'none'

        if severity == 'none':
            return {'clause_id': clause_id, 'severity': 'none'}

        return {
            'clause_id': clause_id,
            'severity': severity,
            'explanation': analysis.get('explanation', ''),
            'what_people_think': analysis.get('what_people_think', ''),
            'what_document_says': analysis.get('what_document_says', ''),
            'script_beat': analysis.get('script_beat', ''),
            'original': original,
            'translation': translation
        }

    def format_report(self, results: Dict) -> str:
        """
        Format surprise detection results as markdown report.

        Args:
            results: Dict with 'surprises', 'total_clauses', 'surprise_count',
                     'by_severity', 'narrative_used' keys

        Returns:
            Markdown-formatted report grouped by severity (Major, Notable, Minor)
        """
        if 'error' in results:
            return f"# Error\n\n{results['error']}"

        narrative_preview = results['narrative_used'][:200]
        if len(results['narrative_used']) > 200:
            narrative_preview += "..."

        # Header
        report = f"""# Surprise Clause Analysis

**Narrative tested:** {narrative_preview}

**Clauses analyzed:** {results['total_clauses']}
**Surprises found:** {results['surprise_count']} ({results['by_severity']['major']} major, {results['by_severity']['notable']} notable, {results['by_severity']['minor']} minor)

"""

        # Group surprises by severity
        surprises_by_severity = {'major': [], 'notable': [], 'minor': []}
        for surprise in results['surprises']:
            severity = surprise['severity']
            if severity in surprises_by_severity:
                surprises_by_severity[severity].append(surprise)

        # Output Major surprises first
        if surprises_by_severity['major']:
            report += "## MAJOR Surprises\n\n"
            for surprise in surprises_by_severity['major']:
                report += self._format_surprise_entry(surprise)

        # Then Notable
        if surprises_by_severity['notable']:
            report += "## NOTABLE Surprises\n\n"
            for surprise in surprises_by_severity['notable']:
                report += self._format_surprise_entry(surprise)

        # Then Minor
        if surprises_by_severity['minor']:
            report += "## MINOR Surprises\n\n"
            for surprise in surprises_by_severity['minor']:
                report += self._format_surprise_entry(surprise)

        # List clauses with no surprises
        if results['surprise_count'] < results['total_clauses']:
            no_surprise_count = results['total_clauses'] - results['surprise_count']
            report += f"\n## No Surprises\n\n{no_surprise_count} clauses aligned with the common narrative.\n"

        return report

    def _format_surprise_entry(self, surprise: Dict) -> str:
        """Format a single surprise clause entry."""
        entry = f"""### {surprise['clause_id']} — {surprise['severity'].upper()}

**Common belief:** {surprise['what_people_think']}

**Document actually says:** {surprise['what_document_says']}

**Why this matters:** {surprise['explanation']}

**Script suggestion:** {surprise['script_beat']}

> **Original:** {surprise['original']}

> **Translation:** {surprise['translation']}

---

"""
        return entry

    def update_sections_with_surprises(self, sections: List[Dict],
                                      surprises: List[Dict]) -> List[Dict]:
        """
        Merge surprise data into section dicts for formatter.

        Args:
            sections: Original section list from translator
            surprises: Surprise list (from parsed surprise responses)

        Returns:
            Updated sections list with 'surprise' key added to each section
            - Sections with surprises get: {'severity': str, 'explanation': str, 'script_beat': str}
            - Sections without surprises get: {'surprise': None}
        """
        # Build lookup dict by clause_id
        surprise_lookup = {}
        for surprise in surprises:
            clause_id = surprise.get('clause_id')
            if clause_id:
                surprise_lookup[clause_id] = {
                    'severity': surprise.get('severity'),
                    'explanation': surprise.get('explanation'),
                    'script_beat': surprise.get('script_beat')
                }

        # Update sections
        updated_sections = []
        for section in sections:
            section_copy = section.copy()
            clause_id = section_copy.get('id', '')

            if clause_id in surprise_lookup:
                section_copy['surprise'] = surprise_lookup[clause_id]
            else:
                section_copy['surprise'] = None

            updated_sections.append(section_copy)

        return updated_sections
