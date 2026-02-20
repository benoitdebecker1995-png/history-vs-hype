"""
Translation Verification Module (VERF-01)

Verifies translation quality before filming by checking:
1. Completeness (cross-check done, annotations present, surprises detected)
2. Discrepancy severity (HIGH/MEDIUM/LOW flags from cross-checker)
3. Annotation coverage (% of legal terms with definitions)
4. Scholarly comparison (against user's summary or Claude's knowledge)

Two modes:
- Audit mode (default): Read existing translation output, check completeness
- Fresh mode (--fresh): Re-run cross-checker, annotator, surprise detector

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

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from env_loader import load_api_key, wrap_api_error
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from env_loader import load_api_key, wrap_api_error

# Import Phase 40 modules
try:
    from tools.translation.cross_checker import CrossChecker
    from tools.translation.legal_annotator import LegalAnnotator
    from tools.translation.surprise_detector import SurpriseDetector
except ImportError:
    # Handle relative imports
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from tools.translation.cross_checker import CrossChecker
    from tools.translation.legal_annotator import LegalAnnotator
    from tools.translation.surprise_detector import SurpriseDetector


class TranslationVerifier:
    """
    Verify translation quality before filming.

    Two verification modes:
    1. Audit (default): Check existing output for completeness
    2. Fresh (--fresh): Re-run cross-check and annotation tools

    Optional scholarly comparison against academic descriptions or Claude knowledge.

    Produces GREEN/YELLOW/RED verdict based on:
    - Discrepancy severity
    - Annotation coverage
    - Scholarly alignment
    """

    def __init__(self, model: str = 'claude-sonnet-4-20250514'):
        """
        Initialize verifier with Claude API client.

        Args:
            model: Claude model to use for scholarly comparison
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

    def verify_translation(self, translation_file: str, mode: str = 'audit',
                          scholarly_file: Optional[str] = None,
                          document_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify translation quality.

        Args:
            translation_file: Path to translation output file
            mode: 'audit' (check existing) or 'fresh' (re-run tools)
            scholarly_file: Optional path to scholarly summary file
            document_name: Optional document name for Claude comparison

        Returns:
            {
                'verdict': 'GREEN' | 'YELLOW' | 'RED',
                'report_path': str,
                'issues': List[str],
                'summary': str
            }

            Or {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

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
        project_dir = os.path.dirname(translation_file)

        if mode == 'audit':
            # Audit mode: check existing output
            verification_result = self._audit_existing_output(content, translation_file)
        elif mode == 'fresh':
            # Fresh mode: re-run tools
            verification_result = self._run_fresh_verification(content, translation_file)
        else:
            return {'error': f'Invalid mode: {mode}. Use "audit" or "fresh"'}

        if 'error' in verification_result:
            return verification_result

        # Scholarly comparison (if requested)
        scholarly_result = None
        if scholarly_file:
            scholarly_result = self._compare_against_scholarly_summary(
                content, scholarly_file, document_name
            )
        elif document_name:
            scholarly_result = self._compare_against_claude_knowledge(
                content, document_name
            )

        # Merge scholarly results
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

    def _run_fresh_verification(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Re-run cross-checker and annotator from scratch.

        Args:
            content: Translation file content
            file_path: Path to file

        Returns:
            Fresh verification results
        """
        # Parse sections from content
        sections = self._parse_sections_from_output(content)

        if not sections:
            return {'error': 'No sections found in translation output'}

        # Extract source language from content
        source_language = self._extract_source_language(content)
        if not source_language:
            source_language = 'french'  # Default fallback

        result = {
            'completeness': {},
            'discrepancies': {},
            'annotations': {},
            'mode': 'fresh'
        }

        # Run CrossChecker
        print("Running cross-check...")
        checker = CrossChecker()
        if checker.error:
            result['completeness']['cross_check_status'] = f'Error: {checker.error}'
            result['discrepancies'] = {'high': 0, 'medium': 0, 'low': 0, 'error': checker.error}
        else:
            check_results = checker.check_document(sections, source_language)

            if 'error' in check_results:
                result['completeness']['cross_check_status'] = f'Error: {check_results["error"]}'
                result['discrepancies'] = {'high': 0, 'medium': 0, 'low': 0, 'error': check_results['error']}
            else:
                result['completeness']['cross_check_present'] = True
                result['completeness']['cross_check_status'] = 'Complete'

                # Count discrepancies by severity
                high_count = sum(1 for r in check_results['results']
                               if r.get('has_discrepancy') and r.get('severity') == 'significant')
                medium_count = sum(1 for r in check_results['results']
                                 if r.get('has_discrepancy') and r.get('severity') == 'minor')

                result['discrepancies'] = {
                    'high': high_count,
                    'medium': medium_count,
                    'low': 0,
                    'backend': check_results.get('backend_used', 'unknown')
                }

        # Run LegalAnnotator
        print("Running legal annotation...")
        annotator = LegalAnnotator()
        if annotator.error:
            result['annotations'] = {
                'present': False,
                'count': 0,
                'error': annotator.error
            }
        else:
            annotation_results = annotator.annotate_document(sections, source_language)

            if 'error' in annotation_results:
                result['annotations'] = {
                    'present': False,
                    'count': 0,
                    'error': annotation_results['error']
                }
            else:
                result['annotations'] = {
                    'present': True,
                    'count': annotation_results['total_annotations'],
                    'mistranslation_flags': annotation_results['mistranslation_flags']
                }

        result['completeness']['all_sections_present'] = (
            result['completeness'].get('cross_check_present', False) and
            result['annotations'].get('present', False)
        )

        return result

    def _parse_sections_from_output(self, content: str) -> List[Dict]:
        """
        Parse sections from formatted translation output.

        Returns:
            List of {'id': str, 'original': str, 'translation': str} dicts
        """
        sections = []

        # Look for article/section markers
        # Pattern: Article markers followed by original and translation
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
                    # Assuming format: **Original:** text **Translation:** text
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

    def _compare_against_scholarly_summary(self, content: str, scholarly_file: str,
                                          document_name: Optional[str]) -> Dict[str, Any]:
        """
        Compare translation against user-provided scholarly summary.

        Args:
            content: Translation content
            scholarly_file: Path to scholarly summary
            document_name: Optional document name

        Returns:
            {
                'omissions': List[str],
                'contradictions': List[str],
                'alignment_score': float (0-1)
            }
        """
        # Read scholarly summary
        try:
            with open(scholarly_file, 'r', encoding='utf-8') as f:
                scholarly_summary = f.read()
        except Exception as e:
            return {'error': f'Failed to read scholarly summary: {str(e)}'}

        # Use Claude to compare
        system_prompt = """You are a historical document analyst comparing a translation against scholarly descriptions.

Your task: Identify key provisions mentioned in the scholarly summary and check if they appear in the translation.

Respond in JSON format."""

        user_prompt = f"""# Scholarly Summary

{scholarly_summary}

# Translation Output

{content[:5000]}{"..." if len(content) > 5000 else ""}

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_prompt}]
            )

            result_text = response.content[0].text

            # Extract JSON
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()

            result = json.loads(result_text)
            return result

        except Exception as e:
            return {'error': f'Scholarly comparison failed: {str(e)}'}

    def _compare_against_claude_knowledge(self, content: str,
                                         document_name: str) -> Dict[str, Any]:
        """
        Compare translation against Claude's knowledge of the document.

        Args:
            content: Translation content
            document_name: Document name

        Returns:
            Comparison results similar to scholarly summary comparison
        """
        system_prompt = """You are a historical document analyst with knowledge of key historical documents.

Your task: Based on your training knowledge about the specified document, identify what key provisions scholars typically cite, and check if the translation includes them.

Respond in JSON format."""

        user_prompt = f"""# Document

{document_name}

# Translation Output

{content[:5000]}{"..." if len(content) > 5000 else ""}

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_prompt}]
            )

            result_text = response.content[0].text

            # Extract JSON
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()

            result = json.loads(result_text)
            return result

        except Exception as e:
            return {'error': f'Claude knowledge comparison failed: {str(e)}'}

    def _calculate_verdict(self, verification_result: Dict) -> Dict[str, Any]:
        """
        Calculate GREEN/YELLOW/RED verdict based on verification results.

        Criteria:
        - GREEN: 0 HIGH discrepancies, 0 annotation gaps, scholarly alignment >0.9
        - YELLOW: 1-2 MEDIUM discrepancies, minor annotation gaps, alignment 0.7-0.9
        - RED: Any HIGH discrepancies, >10% annotation gap, alignment <0.7

        Args:
            verification_result: Results from audit or fresh verification

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
    parser.add_argument('--mode', choices=['audit', 'fresh'], default='audit',
                       help='Verification mode (default: audit)')
    parser.add_argument('--scholarly-summary', dest='scholarly_file',
                       help='Path to scholarly summary file for comparison')
    parser.add_argument('--document-name', dest='document_name',
                       help='Document name for Claude knowledge comparison')

    args = parser.parse_args()

    # Initialize verifier
    verifier = TranslationVerifier()

    if verifier.error:
        print(f"ERROR: {verifier.error}", file=sys.stderr)
        sys.exit(1)

    # Run verification
    result = verifier.verify_translation(
        translation_file=args.translation_file,
        mode=args.mode,
        scholarly_file=args.scholarly_file,
        document_name=args.document_name
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
