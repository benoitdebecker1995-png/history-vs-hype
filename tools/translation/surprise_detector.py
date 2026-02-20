"""
Surprise Clause Detector (TRAN-04)

Post-translation analysis module that compares translated clauses against user-provided
narrative baselines to identify clauses that contradict common English-language narratives.

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

try:
    import anthropic
except ImportError:
    anthropic = None

from env_loader import load_api_key, wrap_api_error


class SurpriseDetector:
    """
    Detect clauses where translation contradicts common English-language narratives.

    This is the "aha moment" generator for Untranslated Evidence videos.
    When a translated clause contradicts what English sources claim about the document,
    that becomes a highlight moment. Three-tier severity system maps to video pacing:
    Major surprises get the most screen time.
    """

    def __init__(self, model: str = 'claude-sonnet-4-20250514'):
        """
        Initialize detector with Claude API client.

        Args:
            model: Claude model to use for analysis

        Returns error dict if anthropic SDK not installed or API key missing.
        """
        self.model = model
        self.client = None
        self.error = None

        # Check for anthropic SDK
        if anthropic is None:
            self.error = "anthropic package not installed. Run: pip install anthropic>=0.40.0"
            return

        # Check for API key (reads from .env file or environment variable)
        key_result = load_api_key()
        if 'error' in key_result:
            self.error = key_result['error']
            return
        api_key = key_result['key']

        # Initialize client
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            self.error = f"Failed to initialize Anthropic client: {str(e)}"

    def detect_surprises(self, sections: List[Dict], narrative: str,
                        source_language: str, document_context: Optional[str] = None,
                        on_progress: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Analyze all translated sections against narrative baseline.

        Args:
            sections: List of section dicts from translator (with 'original', 'translation')
            narrative: User-provided description of what people commonly believe document says
            source_language: Source language of document
            document_context: Optional document description
            on_progress: Optional callback(current, total, clause_id)

        Returns:
            {
                'surprises': List[Dict],  # Only non-NONE severities
                'total_clauses': int,
                'surprise_count': int,
                'by_severity': {'major': int, 'notable': int, 'minor': int},
                'narrative_used': str
            }

            Or {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        if not sections:
            return {
                'surprises': [],
                'total_clauses': 0,
                'surprise_count': 0,
                'by_severity': {'major': 0, 'notable': 0, 'minor': 0},
                'narrative_used': narrative
            }

        if not narrative or not narrative.strip():
            return {'error': 'Narrative baseline required'}

        # Build full document context from all sections
        full_context = "\n\n".join([
            f"{section.get('heading', section.get('id', 'Unknown'))}\n{section.get('translation', '')}"
            for section in sections
        ])

        surprises = []
        total = len(sections)
        by_severity = {'major': 0, 'notable': 0, 'minor': 0}

        # Analyze each section
        for i, section in enumerate(sections, 1):
            if on_progress:
                on_progress(i, total, section.get('id', f'section-{i}'))

            result = self._analyze_clause(
                clause_id=section.get('id', f'section-{i}'),
                original=section.get('original', ''),
                translation=section.get('translation', ''),
                narrative=narrative,
                full_context=full_context,
                source_language=source_language,
                document_context=document_context
            )

            if 'error' in result:
                # Individual failure - continue to next section
                continue

            if result.get('severity') != 'none':
                # Found a surprise
                surprises.append(result)
                severity = result['severity']
                if severity in by_severity:
                    by_severity[severity] += 1

        return {
            'surprises': surprises,
            'total_clauses': total,
            'surprise_count': len(surprises),
            'by_severity': by_severity,
            'narrative_used': narrative
        }

    def _analyze_clause(self, clause_id: str, original: str, translation: str,
                       narrative: str, full_context: str, source_language: str,
                       document_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a single clause against narrative baseline.

        Args:
            clause_id: Clause identifier
            original: Original-language text
            translation: English translation
            narrative: What people commonly believe document says
            full_context: Full translated document for reference
            source_language: Source language
            document_context: Optional document description

        Returns:
            For non-NONE severities:
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

            Or {'error': msg} on API failure
        """
        if not translation or not translation.strip():
            # Empty clause - skip
            return {'clause_id': clause_id, 'severity': 'none'}

        # Build prompt
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

        user_prompt = f"""# Common Narrative Baseline

{narrative}

# Document Context

Source language: {source_language}{context_desc}

Full document translation (for reference):
{full_context[:2000]}{"..." if len(full_context) > 2000 else ""}

# Clause to Analyze

**ID:** {clause_id}

**Original ({source_language}):**
{original}

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

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Parse response
            content = response.content[0].text

            # Extract JSON from response (may be wrapped in markdown code blocks)
            json_text = content.strip()
            if json_text.startswith('```'):
                # Remove markdown code block markers
                lines = json_text.split('\n')
                json_text = '\n'.join(lines[1:-1] if lines[0].startswith('```') else lines)

            analysis = json.loads(json_text)

            # Validate structure
            severity = analysis.get('severity', 'none').lower()
            if severity not in ['major', 'notable', 'minor', 'none']:
                severity = 'none'

            # Build result
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

        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse Claude response as JSON: {str(e)}'}
        except Exception as e:
            return {'error': wrap_api_error(e)}

    def format_report(self, results: Dict) -> str:
        """
        Format surprise detection results as markdown report.

        Args:
            results: Output from detect_surprises()

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
            surprises: Surprise list from detect_surprises()

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
