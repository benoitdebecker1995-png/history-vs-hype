"""
DocumentTranslationPipeline — unified translation pipeline orchestrator (TRAN-PIPE)

Consolidates the 9-module translation pipeline into a single seam class.
Each stage method delegates to a module; no logic lives here.
"""

from typing import Dict, Any, List, Optional

from .structure_detector import StructureDetector
from .translator import TranslationDataBuilder
from .cross_checker import CrossChecker
from .legal_annotator import LegalAnnotator
from .surprise_detector import SurpriseDetector
from .formatter import Formatter
from .verification import TranslationVerifier
from .smoke_test import run_smoke_test


class DocumentTranslationPipeline:
    """Unified translation pipeline orchestrator."""

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
        """
        Run the translation pipeline on document_text.

        stages defaults to all stages. Available: detect, translate, cross_check,
        annotate, surprise, verify, format.

        Returns dict with detected_structure, sections, formatted_output,
        verification_verdict, error keys.
        """
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

    # ── Stage methods ──────────────────────────────────────────────────────────

    def _detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        return self._structure_detector.detect_structure(text, document_type)

    def _build_translation_payloads(
        self,
        sections: List[Dict],
        source_language: str = 'french',
    ) -> List[Dict[str, Any]]:
        """Augment each section with a translation_payload built by TranslationDataBuilder."""
        result = []
        full_document = '\n\n'.join(
            s.get('body', '') or s.get('heading', '') for s in sections
        )
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
        """Parse Claude API responses into section dicts."""
        result = []
        for resp in responses:
            parsed = self._translator.parse_response(
                response_text=resp.get('response_text', ''),
                clause_id=resp.get('clause_id', ''),
                original_text=resp.get('original_text', ''),
            )
            result.append(parsed)
        return result

    def _augment_with_cross_check_payloads(
        self,
        sections: List[Dict],
        source_language: str = 'french',
    ) -> List[Dict[str, Any]]:
        """Augment each section with a cross_check_payload."""
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

    def _augment_with_annotation_payloads(
        self,
        sections: List[Dict],
        source_language: str = 'french',
    ) -> List[Dict[str, Any]]:
        """Augment each section with an annotation_payload."""
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

    def _augment_with_surprise_payloads(
        self,
        sections: List[Dict],
        narrative_baseline: str,
        source_language: str = 'french',
    ) -> List[Dict[str, Any]]:
        """Augment each section with a surprise_payload."""
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
        """Audit-mode verification: returns verdict dict without writing to disk."""
        content = self._format_output(sections)
        audit = self._verifier._audit_existing_output(content, '<in-memory>')
        return self._verifier._calculate_verdict(audit)

    def _format_output(
        self,
        sections: List[Dict],
        output_format: str = 'markdown',
    ) -> str:
        return self._formatter.format_paired(sections, output_format=output_format)

    def smoke_test(self) -> int:
        """Pipeline health check. Returns exit code (0=ok)."""
        return run_smoke_test()
