"""
DocumentTranslationPipeline — unified translation pipeline (TRAN-PIPE)

Consolidates all 9-module translation logic into a single class.
Keeps only translator.py (pure data builder) and smoke_test.py (diagnostics) separate.
"""

import re
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .translator import TranslationDataBuilder
from .smoke_test import run_smoke_test


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: StructureDetector (TRAN-01)
# ═══════════════════════════════════════════════════════════════════════════════

class StructureDetector:
    """Detect article/clause structure in legal documents."""

    ARTICLE_PATTERNS = [
        r'^(Article\s+\d+)',
        r'^(Art\.\s*\d+)',
        r'^(ARTICLE\s+\d+)',
        r'^(Artículo\s+\d+)',
        r'^(Articulo\s+\d+)',
        r'^(Artikel\s+\d+)',
        r'^(§\s*\d+)',
        r'^(Articulus\s+\d+)',
        r'^(Section\s+\d+)',
        r'^(Chapter\s+\d+)',
        r'^(Clause\s+\d+)',
        r'^([IVXLCDM]+\.?\s)',
    ]

    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE)
                                  for p in self.ARTICLE_PATTERNS]

    def detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        if not text or not text.strip():
            return {'error': 'Document text cannot be empty'}

        text = text.strip()
        lines = text.split('\n')
        article_positions = self._find_article_markers(lines)

        if article_positions:
            sections = self._extract_article_sections(lines, article_positions)
            detected_type = self._infer_document_type(article_positions, text)
            has_preamble = article_positions[0]['line_num'] > 0
        else:
            sections = self._extract_paragraph_sections(text)
            detected_type = 'other'
            has_preamble = False

        if has_preamble:
            preamble_text = '\n'.join(lines[:article_positions[0]['line_num']]).strip()
            if preamble_text:
                preamble_section = {
                    'id': 'preamble',
                    'heading': 'Preamble',
                    'body': preamble_text,
                    'start_line': 0,
                    'end_line': article_positions[0]['line_num'] - 1
                }
                sections.insert(0, preamble_section)

        return {
            'document_type': document_type if document_type else detected_type,
            'detected_type': detected_type,
            'sections': sections,
            'section_count': len(sections),
            'has_preamble': has_preamble,
            'raw_text': text
        }

    def _find_article_markers(self, lines: List[str]) -> List[Dict[str, Any]]:
        markers = []
        for line_num, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            for pattern_idx, pattern in enumerate(self.compiled_patterns):
                match = pattern.match(line_stripped)
                if match:
                    markers.append({
                        'line_num': line_num,
                        'marker_text': match.group(1).strip(),
                        'pattern_index': pattern_idx,
                        'full_line': line_stripped
                    })
                    break
        return markers

    def _extract_article_sections(self, lines: List[str], markers: List[Dict]) -> List[Dict]:
        sections = []
        for i, marker in enumerate(markers):
            start_line = marker['line_num']
            end_line = markers[i + 1]['line_num'] - 1 if i + 1 < len(markers) else len(lines) - 1
            heading = lines[start_line].strip()
            body_lines = [lines[j].strip() for j in range(start_line + 1, end_line + 1) if lines[j].strip()]
            body = '\n'.join(body_lines)
            section_id = self._generate_section_id(marker['marker_text'], i + 1)
            sections.append({
                'id': section_id,
                'heading': heading,
                'body': body,
                'start_line': start_line,
                'end_line': end_line
            })
        return sections

    def _extract_paragraph_sections(self, text: str) -> List[Dict]:
        paragraphs = re.split(r'\n\s*\n', text)
        sections = []
        line_counter = 0
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            para_lines = para.split('\n')
            start_line = line_counter
            end_line = line_counter + len(para_lines) - 1
            line_counter = end_line + 2
            sections.append({
                'id': f'paragraph-{i + 1}',
                'heading': f'Paragraph {i + 1}',
                'body': para,
                'start_line': start_line,
                'end_line': end_line
            })
        return sections

    def _generate_section_id(self, marker_text: str, section_num: int) -> str:
        marker_lower = marker_text.lower()
        num_match = re.search(r'\d+', marker_text)
        num = num_match.group() if num_match else str(section_num)

        if 'article' in marker_lower or 'art.' in marker_lower or 'articulo' in marker_lower:
            prefix = 'article'
        elif 'section' in marker_lower or '§' in marker_text:
            prefix = 'section'
        elif 'chapter' in marker_lower:
            prefix = 'chapter'
        elif 'clause' in marker_lower:
            prefix = 'clause'
        else:
            prefix = 'article'
        return f'{prefix}-{num}'

    def _infer_document_type(self, markers: List[Dict], full_text: str) -> str:
        if any(word in full_text.lower() for word in ['treaty', 'convention', 'protocol', 'agreement']):
            return 'treaty'
        if any(word in full_text.lower() for word in ['decree', 'statute', 'law', 'loi', 'statut']):
            return 'legal_code'
        if any('chapter' in m['marker_text'].lower() for m in markers):
            return 'book'
        return 'legal_code' if len(markers) > 0 else 'other'


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: CrossChecker (TRAN-02)
# ═══════════════════════════════════════════════════════════════════════════════

class CrossChecker:
    """Cross-check translations against independent sources."""

    def __init__(self, deepl_api_key: Optional[str] = None):
        self.deepl_key = deepl_api_key or os.environ.get('DEEPL_AUTH_KEY')

    def build_comparison_payload(self, claude_translation: str, backend_translation: str,
                                 original_text: str, clause_id: str,
                                 source_language: str = 'unknown',
                                 backend: str = 'independent') -> Dict[str, Any]:
        system_prompt = """You are a translation quality assessor. Compare two translations.
Identify SEMANTIC differences only — changes in meaning.
IGNORE stylistic differences: "shall" vs "will", word order, passive vs active voice.
Respond in JSON format."""

        user_prompt = f"""Original ({source_language}):
{original_text}

Translation A (Claude):
{claude_translation}

Translation B ({backend}):
{backend_translation}

Are there semantic differences? Respond in JSON:
{{
  "has_discrepancy": true/false,
  "severity": "none"|"minor"|"significant",
  "explanation": "1-2 sentence description",
  "recommendation": "what to do"
}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_comparison_response(self, response_text: str, clause_id: str) -> Dict[str, Any]:
        text = response_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            return {'clause_id': clause_id, 'error': f'Failed to parse JSON: {str(e)}'}

        required = ['has_discrepancy', 'severity', 'explanation', 'recommendation']
        if not all(k in result for k in required):
            return {'clause_id': clause_id, 'error': 'Response missing required fields'}

        return {
            'clause_id': clause_id,
            'has_discrepancy': result['has_discrepancy'],
            'severity': result['severity'],
            'explanation': result['explanation'],
            'recommendation': result['recommendation']
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: LegalAnnotator (TRAN-03)
# ═══════════════════════════════════════════════════════════════════════════════

class LegalAnnotator:
    """Annotate legal/technical terms."""

    def build_annotation_payload(self, clause_text: str, translation: str,
                                 clause_id: str, source_language: str = 'unknown',
                                 document_context: Optional[str] = None) -> Dict[str, Any]:
        system_prompt = """You are a legal and historical terminology expert.
Identify terms with NO direct English equivalent.
For each: provide original term, definition, English equivalent, alternatives, historical context.
Respond in JSON format."""

        context_info = f"\n\nDocument context: {document_context}" if document_context else ""

        user_prompt = f"""Original ({source_language}):
{clause_text}

Translation (English):
{translation}{context_info}

Identify terms with no direct English equivalent. Respond in JSON:
{{
  "annotations": [
    {{
      "original_term": "term",
      "source_language_definition": "definition",
      "english_equivalent": "translation used",
      "alternatives": ["alt1", "alt2"],
      "historical_context": "if relevant",
      "commonly_mistranslated": true/false,
      "common_mistranslation": "if mistranslated",
      "note": "explanation"
    }}
  ]
}}

If no terms require annotation, return {{"annotations": []}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_annotation_response(self, response_text: str, clause_id: str) -> Dict[str, Any]:
        text = response_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            return {'clause_id': clause_id, 'error': f'Failed to parse JSON: {str(e)}'}

        if 'annotations' not in result:
            return {'clause_id': clause_id, 'error': 'Response missing annotations field'}

        annotations = result['annotations']
        footnotes = self._format_footnotes(annotations)

        return {
            'clause_id': clause_id,
            'annotations': annotations,
            'footnotes': footnotes
        }

    def _format_footnotes(self, annotations: List[Dict]) -> List[str]:
        if not annotations:
            return []
        footnotes = []
        for i, ann in enumerate(annotations, 1):
            if not ann.get('original_term') or not ann.get('english_equivalent'):
                continue
            footnote = f"**{ann['english_equivalent']}** (original: *{ann['original_term']}*): "
            if ann.get('source_language_definition'):
                footnote += ann['source_language_definition']
            else:
                footnote += "No direct English equivalent."
            footnote += f" English equivalent: \"{ann['english_equivalent']}\"."
            if ann.get('alternatives'):
                alternatives_str = ", ".join(f"\"{alt}\"" for alt in ann['alternatives'])
                footnote += f" Alternatives: {alternatives_str}."
            if ann.get('historical_context'):
                footnote += f" Historical note: {ann['historical_context']}"
            if ann.get('commonly_mistranslated', False):
                common_error = ann.get('common_mistranslation', 'unknown')
                footnote += f" **WARNING:** Commonly rendered as \"{common_error}\" in English sources."
            footnotes.append(footnote)
        return footnotes


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: SurpriseDetector (TRAN-04)
# ═══════════════════════════════════════════════════════════════════════════════

class SurpriseDetector:
    """Detect clauses that contradict narratives."""

    def build_surprise_payload(self, clause_text: str, translation: str,
                               narrative_baseline: str, clause_id: str,
                               source_language: str = 'unknown',
                               document_context: Optional[str] = None,
                               full_context: Optional[str] = None) -> Dict[str, Any]:
        system_prompt = """You are a historical document analyst.
Identify where the actual document contradicts common narratives.
Classification: MAJOR (directly contradicts) / NOTABLE (omission) / MINOR (nuance) / NONE (aligns).
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
Analyze whether this clause contradicts, complicates, or is absent from the common narrative.
Respond in JSON:
{{
    "severity": "major" | "notable" | "minor" | "none",
    "explanation": "Why this is/isn't a surprise",
    "what_people_think": "What the common narrative claims",
    "what_document_says": "What this clause actually reveals",
    "script_beat": "1-2 sentence suggestion for video, or null if none"
}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_surprise_response(self, response_text: str, clause_id: str,
                                original: str = '', translation: str = '') -> Dict[str, Any]:
        text = response_text.strip()
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1] if lines[0].startswith('```') else lines)
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()

        try:
            analysis = json.loads(text)
        except json.JSONDecodeError as e:
            return {'clause_id': clause_id, 'error': f'Failed to parse JSON: {str(e)}'}

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


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: Formatter (TRAN-05)
# ═══════════════════════════════════════════════════════════════════════════════

class Formatter:
    """Format translated sections for output."""

    def format_paired(self, sections: List[Dict], output_format: str = 'markdown') -> str:
        if not sections:
            return {'error': 'No sections provided'}

        if output_format == 'json':
            return json.dumps({'sections': sections}, indent=2, ensure_ascii=False)

        output_lines = []
        for section in sections:
            if 'error' in section:
                output_lines.append(f"ERROR in {section.get('id', 'unknown')}: {section['error']}\n")
                continue

            heading = section.get('heading', section.get('id', 'Unknown'))
            output_lines.append(f"## {heading}\n")

            original = section.get('original', '')
            if original:
                output_lines.append("### Original\n")
                for line in original.split('\n'):
                    output_lines.append(f"> {line}")
                output_lines.append("")

            translation = section.get('translation', '')
            if translation:
                output_lines.append("### Translation\n")
                output_lines.append(translation)
                output_lines.append("")

            footnotes = section.get('footnotes') or section.get('notes')
            if footnotes:
                output_lines.append("---")
                output_lines.append("**Notes:**\n")
                for i, note in enumerate(footnotes, 1):
                    output_lines.append(f"{i}. {note}")
                output_lines.append("")

            output_lines.append("")

        return '\n'.join(output_lines)


# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED: TranslationVerifier (VERF-01)
# ═══════════════════════════════════════════════════════════════════════════════

class TranslationVerifier:
    """Verify translation quality."""

    def __init__(self, project_dir: Optional[str] = None):
        self.project_dir = project_dir

    def _audit_existing_output(self, content: str, file_path: str) -> Dict[str, Any]:
        result = {
            'completeness': {},
            'discrepancies': {},
            'annotations': {},
            'mode': 'audit'
        }

        has_cross_check = 'Cross-Check Summary' in content or 'DISCREPANCIES' in content
        pending_cross_check = '[PENDING]' in content or '[NEEDS CROSS-CHECK]' in content

        result['completeness']['cross_check_present'] = has_cross_check and not pending_cross_check
        result['completeness']['cross_check_status'] = (
            'Complete' if has_cross_check and not pending_cross_check
            else 'Pending' if pending_cross_check
            else 'Missing'
        )

        high_count = len(re.findall(r'severity.*?significant', content, re.IGNORECASE))
        medium_count = len(re.findall(r'severity.*?minor', content, re.IGNORECASE))

        result['discrepancies'] = {
            'high': high_count,
            'medium': medium_count,
            'low': 0
        }

        has_annotations = 'Legal Annotations' in content or 'FOOTNOTES' in content or '**' in content
        annotation_count = len(re.findall(r'\*\*.+?\*\*.+?:', content))

        result['annotations'] = {
            'present': has_annotations,
            'count': annotation_count,
            'coverage_percent': None
        }

        has_surprises = 'Surprise' in content or 'MAJOR' in content or 'NOTABLE' in content
        result['completeness']['surprise_detection_present'] = has_surprises

        result['completeness']['all_sections_present'] = all([
            result['completeness']['cross_check_present'],
            result['annotations']['present']
        ])

        return result

    def _calculate_verdict(self, verification_result: Dict) -> Dict[str, Any]:
        issues = []
        score = 100

        discrepancies = verification_result.get('discrepancies', {})
        high_count = discrepancies.get('high', 0)
        medium_count = discrepancies.get('medium', 0)

        if high_count > 0:
            score -= 40 * high_count
            issues.append(f"{high_count} HIGH severity discrepancy/ies found")

        if medium_count > 0:
            score -= 10 * medium_count
            if medium_count <= 2:
                issues.append(f"{medium_count} MEDIUM severity discrepancy/ies (reviewable)")
            else:
                issues.append(f"{medium_count} MEDIUM severity discrepancies (significant)")

        annotations = verification_result.get('annotations', {})
        if not annotations.get('present', False):
            score -= 20
            issues.append("Legal annotations missing")
        elif annotations.get('count', 0) == 0:
            score -= 15
            issues.append("No legal terms annotated")

        completeness = verification_result.get('completeness', {})
        if not completeness.get('cross_check_present', False):
            score -= 25
            issues.append("Cross-check not completed")

        if score >= 90 and high_count == 0:
            verdict = 'GREEN'
            reasoning = "Translation quality is excellent. No significant issues found."
        elif score >= 70 and high_count == 0:
            verdict = 'YELLOW'
            reasoning = "Translation quality is good with minor issues. Review flagged sections."
        else:
            verdict = 'RED'
            reasoning = "Translation has significant issues requiring revision."

        top_issues = issues[:3] if issues else ['No issues found']

        return {
            'verdict': verdict,
            'reasoning': reasoning,
            'top_issues': top_issues,
            'score': max(0, score)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN: DocumentTranslationPipeline
# ═══════════════════════════════════════════════════════════════════════════════

class DocumentTranslationPipeline:
    """Unified translation pipeline orchestrator. All logic consolidated."""

    def __init__(self, project_dir: Optional[str] = None):
        self.project_dir = project_dir
        self._structure_detector = StructureDetector()
        self._translator = TranslationDataBuilder()
        self._cross_checker = CrossChecker()
        self._annotator = LegalAnnotator()
        self._surprise_detector = SurpriseDetector()
        self._formatter = Formatter()
        self._verifier = TranslationVerifier(project_dir)

    def run_pipeline(
        self,
        document_text: str,
        source_language: str = 'french',
        document_type: Optional[str] = None,
        stages: Optional[List[str]] = None,
        narrative_baseline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run the translation pipeline on document_text."""
        if stages is None:
            stages = ['detect', 'translate', 'cross_check', 'annotate', 'surprise', 'verify', 'format']

        structure = self._detect_structure(document_text, document_type)
        if 'error' in structure:
            return {'error': structure['error']}

        sections = structure.get('sections', [])

        if 'translate' in stages:
            sections = self._build_translation_payloads(sections, source_language)

        if 'cross_check' in stages:
            sections = self._augment_with_cross_check_payloads(sections, source_language)

        if 'annotate' in stages:
            sections = self._augment_with_annotation_payloads(sections, source_language)

        if 'surprise' in stages and narrative_baseline:
            sections = self._augment_with_surprise_payloads(sections, narrative_baseline, source_language)

        verification_verdict = None
        if 'verify' in stages:
            verification = self._verify_translation(sections)
            verification_verdict = verification.get('verdict')

        formatted_output = None
        if 'format' in stages:
            formatted_output = self._format_output(sections)

        return {
            'detected_structure': structure,
            'sections': sections,
            'formatted_output': formatted_output,
            'verification_verdict': verification_verdict,
            'error': None,
        }

    def _detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        return self._structure_detector.detect_structure(text, document_type)

    def _build_translation_payloads(self, sections: List[Dict], source_language: str = 'french') -> List[Dict[str, Any]]:
        result = []
        full_document = '\n\n'.join(s.get('body', '') or s.get('heading', '') for s in sections)
        for section in sections:
            section = dict(section)
            payload = self._translator.build_translation_payload(
                clause_text=section.get('body', ''),
                full_document=full_document,
                source_language=source_language,
                clause_id=section.get('id', ''),
            )
            section['translation_payload'] = payload
            result.append(section)
        return result

    def _parse_translations(self, responses: List[Dict]) -> List[Dict]:
        result = []
        for resp in responses:
            parsed = self._translator.parse_response(
                response_text=resp.get('response_text', ''),
                clause_id=resp.get('clause_id', ''),
                original_text=resp.get('original_text', ''),
            )
            result.append(parsed)
        return result

    def _augment_with_cross_check_payloads(self, sections: List[Dict], source_language: str = 'french') -> List[Dict[str, Any]]:
        result = []
        for section in sections:
            section = dict(section)
            payload = self._cross_checker.build_comparison_payload(
                claude_translation=section.get('translation', ''),
                backend_translation='',
                original_text=section.get('body', ''),
                clause_id=section.get('id', ''),
                source_language=source_language,
            )
            section['cross_check_payload'] = payload
            result.append(section)
        return result

    def _augment_with_annotation_payloads(self, sections: List[Dict], source_language: str = 'french') -> List[Dict[str, Any]]:
        result = []
        for section in sections:
            section = dict(section)
            payload = self._annotator.build_annotation_payload(
                clause_text=section.get('body', ''),
                translation=section.get('translation', ''),
                clause_id=section.get('id', ''),
                source_language=source_language,
            )
            section['annotation_payload'] = payload
            result.append(section)
        return result

    def _augment_with_surprise_payloads(self, sections: List[Dict], narrative_baseline: str, source_language: str = 'french') -> List[Dict[str, Any]]:
        result = []
        for section in sections:
            section = dict(section)
            payload = self._surprise_detector.build_surprise_payload(
                clause_text=section.get('body', ''),
                translation=section.get('translation', ''),
                narrative_baseline=narrative_baseline,
                clause_id=section.get('id', ''),
                source_language=source_language,
            )
            section['surprise_payload'] = payload
            result.append(section)
        return result

    def _verify_translation(self, sections: List[Dict]) -> Dict[str, Any]:
        content = self._format_output(sections)
        audit = self._verifier._audit_existing_output(content, '<in-memory>')
        return self._verifier._calculate_verdict(audit)

    def _format_output(self, sections: List[Dict], output_format: str = 'markdown') -> str:
        return self._formatter.format_paired(sections, output_format=output_format)

    def smoke_test(self) -> int:
        """Pipeline health check. Returns exit code (0=ok)."""
        return run_smoke_test()
