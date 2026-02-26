"""
Translation Verification Module (VERF-01)

Pure data processor. LLM calls handled by Claude Code via /verify command.

Verifies translation quality before filming by checking:
1. Completeness (cross-check done, annotations present, surprises detected)
2. Discrepancy severity (HIGH/MEDIUM/LOW flags from cross-checker)
3. Annotation coverage (% of legal terms with definitions)
4. Scholarly comparison (payload builders for Claude Code to execute)

Two modes:
- Audit mode (default): Read existing translation output, check completeness (pure Python)
- Scholarly mode: Provides payload builders for Claude Code to run LLM comparisons

Output:
- Full report to TRANSLATION-VERIFICATION.md
- Tiered verdict: GREEN (proceed) / YELLOW (review) / RED (revise)
- Condensed terminal summary
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class TranslationVerifier:
    """
    Verify translation quality before filming.

    Pure data processor — no Anthropic SDK or API key needed.

    Two verification modes:
    1. Audit (default): Check existing output for completeness — pure Python, no LLM
    2. Scholarly: Provides payload builders for Claude Code to execute LLM comparisons

    The /verify command (Claude Code itself) orchestrates LLM calls using payloads
    from build_scholarly_comparison_payload() and build_knowledge_comparison_payload().

    Produces GREEN/YELLOW/RED verdict based on:
    - Discrepancy severity
    - Annotation coverage
    - Scholarly alignment
    """

    def __init__(self, project_dir: Optional[str] = None):
        """
        Initialize verifier.

        Args:
            project_dir: Optional project directory path (used when writing reports)
        """
        self.project_dir = project_dir

    def verify_translation(self, translation_file: str, mode: str = 'audit',
                          scholarly_result: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Verify translation quality.

        Args:
            translation_file: Path to translation output file
            mode: 'audit' (check existing, pure Python)
            scholarly_result: Optional pre-computed scholarly comparison result
                              (passed in by Claude Code after executing the payload)

        Returns:
            {
                'verdict': 'GREEN' | 'YELLOW' | 'RED',
                'report_path': str,
                'issues': List[str],
                'summary': str
            }

            Or {'error': msg} on failure
        """
        # Validate translation file exists
        if not os.path.exists(translation_file):
            return {'error': f'Translation file not found: {translation_file}'}

        # Read translation output
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Failed to read translation file: {str(e)}'}

        # Determine project directory
        project_dir = self.project_dir or os.path.dirname(translation_file)

        if mode == 'audit':
            # Audit mode: check existing output (pure Python)
            verification_result = self._audit_existing_output(content, translation_file)
        else:
            return {'error': f'Invalid mode: {mode}. Use "audit". For fresh/scholarly mode, use /verify command which provides Claude Code LLM integration.'}

        if 'error' in verification_result:
            return verification_result

        # Merge scholarly results if provided (Claude Code executed the payload and passed results back)
        if scholarly_result and 'error' not in scholarly_result:
            verification_result['scholarly_comparison'] = scholarly_result

        # Calculate verdict
        verdict_result = self._calculate_verdict(verification_result)

        # Generate full report
        report_path = os.path.join(project_dir, 'TRANSLATION-VERIFICATION.md')
        report_content = self._generate_full_report(verification_result, verdict_result)

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        except Exception as e:
            return {'error': f'Failed to write report: {str(e)}'}

        # Generate terminal summary
        terminal_summary = self._generate_terminal_summary(verdict_result, report_path)

        return {
            'verdict': verdict_result['verdict'],
            'report_path': report_path,
            'issues': verdict_result['top_issues'],
            'summary': terminal_summary
        }

    def _audit_existing_output(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Audit existing translation output for completeness.

        Pure Python regex parsing — no LLM calls.

        Args:
            content: Translation file content
            file_path: Path to file (for context)

        Returns:
            {
                'completeness': {...},
                'discrepancies': {...},
                'annotations': {...}
            }
        """
        result = {
            'completeness': {},
            'discrepancies': {},
            'annotations': {},
            'mode': 'audit'
        }

        # Check for cross-check section
        has_cross_check = 'Cross-Check Summary' in content or 'DISCREPANCIES' in content
        pending_cross_check = '[PENDING]' in content or '[NEEDS CROSS-CHECK]' in content

        result['completeness']['cross_check_present'] = has_cross_check and not pending_cross_check
        result['completeness']['cross_check_status'] = (
            'Complete' if has_cross_check and not pending_cross_check
            else 'Pending' if pending_cross_check
            else 'Missing'
        )

        # Parse discrepancy counts from cross-check section
        high_count = len(re.findall(r'severity.*?significant', content, re.IGNORECASE))
        medium_count = len(re.findall(r'severity.*?minor', content, re.IGNORECASE))

        result['discrepancies'] = {
            'high': high_count,
            'medium': medium_count,
            'low': 0  # Low severity not distinguished in current cross-checker
        }

        # Check for annotations
        has_annotations = 'Legal Annotations' in content or 'FOOTNOTES' in content or '**' in content
        annotation_count = len(re.findall(r'\*\*.+?\*\*.+?:', content))

        result['annotations'] = {
            'present': has_annotations,
            'count': annotation_count,
            'coverage_percent': None  # Can't calculate without knowing total legal terms
        }

        # Check for surprise section
        has_surprises = 'Surprise' in content or 'MAJOR' in content or 'NOTABLE' in content
        result['completeness']['surprise_detection_present'] = has_surprises

        # Overall completeness check
        result['completeness']['all_sections_present'] = all([
            result['completeness']['cross_check_present'],
            result['annotations']['present']
        ])

        return result

    def _parse_sections_from_output(self, content: str) -> List[Dict]:
        """
        Parse sections from formatted translation output.

        Returns:
            List of {'id': str, 'original': str, 'translation': str} dicts
        """
        sections = []

        # Look for article/section markers
        article_pattern = r'(?:Article|Section|Clause)\s+(\d+|[IVX]+)'

        # Split by article markers
        parts = re.split(f'({article_pattern})', content)

        current_id = None
        for i in range(len(parts)):
            if re.match(article_pattern, parts[i], re.IGNORECASE):
                current_id = parts[i].strip()

                # Look for original and translation in subsequent parts
                if i + 1 < len(parts):
                    section_content = parts[i + 1]

                    # Try to extract original and translation
                    original_match = re.search(r'\*\*Original.*?\*\*\s*(.+?)(?=\*\*Translation|\*\*Cross-Check|$)',
                                              section_content, re.DOTALL)
                    translation_match = re.search(r'\*\*Translation.*?\*\*\s*(.+?)(?=\*\*Cross-Check|\*\*Annotations|$)',
                                                 section_content, re.DOTALL)

                    if original_match and translation_match:
                        sections.append({
                            'id': current_id,
                            'original': original_match.group(1).strip(),
                            'translation': translation_match.group(1).strip()
                        })

        return sections

    def _extract_source_language(self, content: str) -> Optional[str]:
        """Extract source language from content."""
        # Look for language indicators
        lang_pattern = r'(?:Language|Source):\s*(\w+)'
        match = re.search(lang_pattern, content, re.IGNORECASE)

        if match:
            return match.group(1).lower()

        # Check for common language names in content
        for lang in ['french', 'spanish', 'german', 'latin', 'italian']:
            if lang in content.lower()[:500]:  # Check first 500 chars
                return lang

        return None

    def build_scholarly_comparison_payload(self, translation_text: str,
                                           scholarly_summary: str,
                                           document_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a Claude Code payload for comparing translation against a scholarly summary.

        Claude Code executes the LLM call using this payload.

        Args:
            translation_text: The translation output content
            scholarly_summary: Content of the scholarly summary file
            document_name: Optional document name for context

        Returns:
            {
                'system_prompt': str,
                'user_prompt': str
            }
        """
        system_prompt = """You are a historical document analyst comparing a translation against scholarly descriptions.

Your task: Identify key provisions mentioned in the scholarly summary and check if they appear in the translation.

Respond in JSON format."""

        content_preview = translation_text[:5000]
        ellipsis = "..." if len(translation_text) > 5000 else ""

        user_prompt = f"""# Scholarly Summary

{scholarly_summary}

# Translation Output

{content_preview}{ellipsis}

# Task

Compare the translation against the scholarly summary. Identify:
1. Key provisions mentioned in scholarly summary but missing/unclear in translation (omissions)
2. Provisions where translation contradicts scholarly interpretation (contradictions)
3. Overall alignment (0-1 score, where 1 = perfect alignment)

Respond in JSON:
{{
    "omissions": ["provision 1", "provision 2"],
    "contradictions": ["contradiction 1"],
    "alignment_score": 0.0-1.0,
    "explanation": "Brief explanation of alignment assessment"
}}"""

        return {
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_scholarly_comparison_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude Code's scholarly comparison response.

        Args:
            response_text: Raw text response from Claude Code

        Returns:
            {
                'omissions': List[str],
                'contradictions': List[str],
                'alignment_score': float,
                'explanation': str
            }
            {'error': str} on parse failure
        """
        text = response_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse scholarly comparison response: {str(e)}'}

    def build_knowledge_comparison_payload(self, translation_text: str,
                                           document_name: str) -> Dict[str, Any]:
        """
        Build a Claude Code payload for comparing translation against Claude's knowledge.

        Claude Code executes the LLM call using this payload.

        Args:
            translation_text: The translation output content
            document_name: Document name (Claude uses its training knowledge)

        Returns:
            {
                'system_prompt': str,
                'user_prompt': str
            }
        """
        system_prompt = """You are a historical document analyst with knowledge of key historical documents.

Your task: Based on your training knowledge about the specified document, identify what key provisions scholars typically cite, and check if the translation includes them.

Respond in JSON format."""

        content_preview = translation_text[:5000]
        ellipsis = "..." if len(translation_text) > 5000 else ""

        user_prompt = f"""# Document

{document_name}

# Translation Output

{content_preview}{ellipsis}

# Task

Based on your knowledge of {document_name}, what are the key provisions scholars typically cite?

Then compare against the translation above. Identify:
1. Key provisions from scholarly literature that seem missing/unclear (omissions)
2. Provisions where translation seems to contradict typical scholarly interpretations (contradictions)
3. Overall alignment (0-1 score)

Respond in JSON:
{{
    "key_provisions_expected": ["provision 1", "provision 2"],
    "omissions": ["missing provision"],
    "contradictions": ["contradiction if any"],
    "alignment_score": 0.0-1.0,
    "explanation": "Brief explanation"
}}"""

        return {
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_knowledge_comparison_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude Code's knowledge comparison response.

        Args:
            response_text: Raw text response from Claude Code

        Returns:
            Parsed comparison result dict
            {'error': str} on parse failure
        """
        text = response_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse knowledge comparison response: {str(e)}'}

    def _calculate_verdict(self, verification_result: Dict) -> Dict[str, Any]:
        """
        Calculate GREEN/YELLOW/RED verdict based on verification results.

        Criteria:
        - GREEN: 0 HIGH discrepancies, 0 annotation gaps, scholarly alignment >0.9
        - YELLOW: 1-2 MEDIUM discrepancies, minor annotation gaps, alignment 0.7-0.9
        - RED: Any HIGH discrepancies, >10% annotation gap, alignment <0.7

        Args:
            verification_result: Results from audit verification

        Returns:
            {
                'verdict': 'GREEN' | 'YELLOW' | 'RED',
                'reasoning': str,
                'top_issues': List[str]
            }
        """
        issues = []
        score = 100  # Start with perfect score, deduct points

        # Check discrepancies
        discrepancies = verification_result.get('discrepancies', {})
        high_count = discrepancies.get('high', 0)
        medium_count = discrepancies.get('medium', 0)

        if high_count > 0:
            score -= 40 * high_count  # Each HIGH discrepancy is major
            issues.append(f"{high_count} HIGH severity discrepancy/ies found")

        if medium_count > 0:
            score -= 10 * medium_count  # Each MEDIUM discrepancy is moderate
            if medium_count <= 2:
                issues.append(f"{medium_count} MEDIUM severity discrepancy/ies (reviewable)")
            else:
                issues.append(f"{medium_count} MEDIUM severity discrepancies (significant)")

        # Check annotation coverage
        annotations = verification_result.get('annotations', {})
        if not annotations.get('present', False):
            score -= 20
            issues.append("Legal annotations missing")
        elif annotations.get('count', 0) == 0:
            score -= 15
            issues.append("No legal terms annotated (may indicate annotation gap)")

        # Check completeness
        completeness = verification_result.get('completeness', {})
        if not completeness.get('cross_check_present', False):
            score -= 25
            issues.append("Cross-check not completed")

        # Check scholarly comparison if present
        scholarly = verification_result.get('scholarly_comparison', {})
        if scholarly and 'error' not in scholarly:
            alignment = scholarly.get('alignment_score', 1.0)
            omissions = scholarly.get('omissions', [])
            contradictions = scholarly.get('contradictions', [])

            if alignment < 0.7:
                score -= 30
                issues.append(f"Scholarly alignment low ({alignment:.1%})")
            elif alignment < 0.9:
                score -= 10
                issues.append(f"Scholarly alignment moderate ({alignment:.1%})")

            if contradictions:
                score -= 20 * len(contradictions)
                issues.append(f"{len(contradictions)} contradiction(s) with scholarly interpretation")

            if len(omissions) > 2:
                score -= 15
                issues.append(f"{len(omissions)} key provisions from scholarly summary not found")

        # Determine verdict
        if score >= 90 and high_count == 0:
            verdict = 'GREEN'
            reasoning = "Translation quality is excellent. No significant issues found."
        elif score >= 70 and high_count == 0:
            verdict = 'YELLOW'
            reasoning = "Translation quality is good with minor issues. Review flagged sections."
        else:
            verdict = 'RED'
            reasoning = "Translation has significant issues requiring revision."

        # Add top 3 issues
        top_issues = issues[:3] if issues else ['No issues found']

        return {
            'verdict': verdict,
            'reasoning': reasoning,
            'top_issues': top_issues,
            'score': max(0, score)
        }

    def _generate_full_report(self, verification_result: Dict,
                             verdict_result: Dict) -> str:
        """
        Generate full markdown report.

        Args:
            verification_result: Verification data
            verdict_result: Verdict calculation

        Returns:
            Markdown-formatted report
        """
        report = f"""# Translation Verification Report

**Verdict:** {verdict_result['verdict']}

**Mode:** {verification_result.get('mode', 'audit')}

**Score:** {verdict_result['score']}/100

---

## Summary

{verdict_result['reasoning']}

### Top Issues

"""

        for i, issue in enumerate(verdict_result['top_issues'], 1):
            report += f"{i}. {issue}\n"

        report += "\n---\n\n## Completeness Check\n\n"

        completeness = verification_result.get('completeness', {})
        report += f"- **Cross-check:** {completeness.get('cross_check_status', 'Unknown')}\n"
        report += f"- **Annotations:** {'Present' if verification_result.get('annotations', {}).get('present') else 'Missing'}\n"
        report += f"- **Surprise detection:** {'Present' if completeness.get('surprise_detection_present') else 'Not detected'}\n"

        report += "\n## Discrepancy Analysis\n\n"

        discrepancies = verification_result.get('discrepancies', {})
        report += f"- **HIGH severity:** {discrepancies.get('high', 0)}\n"
        report += f"- **MEDIUM severity:** {discrepancies.get('medium', 0)}\n"
        report += f"- **LOW severity:** {discrepancies.get('low', 0)}\n"

        if discrepancies.get('backend'):
            report += f"\n*Backend used:* {discrepancies['backend']}\n"

        report += "\n## Annotation Coverage\n\n"

        annotations = verification_result.get('annotations', {})
        report += f"- **Terms annotated:** {annotations.get('count', 0)}\n"

        if annotations.get('mistranslation_flags'):
            report += f"- **Mistranslation warnings:** {annotations['mistranslation_flags']}\n"

        # Scholarly comparison section
        scholarly = verification_result.get('scholarly_comparison')
        if scholarly and 'error' not in scholarly:
            report += "\n## Scholarly Comparison\n\n"
            report += f"- **Alignment score:** {scholarly.get('alignment_score', 0):.1%}\n\n"

            omissions = scholarly.get('omissions', [])
            if omissions:
                report += "### Omissions\n\n"
                for omission in omissions:
                    report += f"- {omission}\n"
                report += "\n"

            contradictions = scholarly.get('contradictions', [])
            if contradictions:
                report += "### Contradictions\n\n"
                for contradiction in contradictions:
                    report += f"- {contradiction}\n"
                report += "\n"

            if scholarly.get('explanation'):
                report += f"**Explanation:** {scholarly['explanation']}\n"

        report += "\n---\n\n## Recommendation\n\n"

        if verdict_result['verdict'] == 'GREEN':
            report += "**Proceed to script generation.** Translation quality is excellent.\n\n"
            report += "Next step: `/script --document-mode`\n"
        elif verdict_result['verdict'] == 'YELLOW':
            report += "**Review flagged sections before proceeding.** Translation quality is good but has minor issues.\n\n"
            report += "After review, proceed with: `/script --document-mode`\n"
        else:
            report += "**Revise translation before filming.** Significant issues found.\n\n"
            report += "Address flagged discrepancies and re-run verification.\n"

        return report

    def _generate_terminal_summary(self, verdict_result: Dict, report_path: str) -> str:
        """
        Generate condensed terminal summary.

        Args:
            verdict_result: Verdict calculation
            report_path: Path to full report

        Returns:
            Terminal-friendly summary string
        """
        verdict = verdict_result['verdict']

        # Color codes for terminal
        colors = {
            'GREEN': '\033[92m',  # Green
            'YELLOW': '\033[93m',  # Yellow
            'RED': '\033[91m',  # Red
            'RESET': '\033[0m'
        }

        summary = f"\nTRANSLATION VERIFICATION\n"
        summary += f"VERDICT: {colors.get(verdict, '')}{verdict}{colors['RESET']}\n\n"
        summary += f"Top issues:\n"

        for i, issue in enumerate(verdict_result['top_issues'], 1):
            summary += f"{i}. {issue}\n"

        summary += f"\nFull report: {report_path}\n"

        return summary


def main():
    """CLI entry point for verification module."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Verify translation quality before filming'
    )
    parser.add_argument('translation_file', help='Path to translation output file')
    parser.add_argument('--mode', choices=['audit'], default='audit',
                       help='Verification mode (default: audit). For scholarly comparison, use /verify command.')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Initialize verifier (no API key needed)
    verifier = TranslationVerifier()

    # Run verification
    result = verifier.verify_translation(
        translation_file=args.translation_file,
        mode=args.mode
    )

    if 'error' in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Print summary
    print(result['summary'])

    # Exit with code based on verdict
    exit_codes = {'GREEN': 0, 'YELLOW': 0, 'RED': 1}
    sys.exit(exit_codes.get(result['verdict'], 1))


if __name__ == '__main__':
    main()
