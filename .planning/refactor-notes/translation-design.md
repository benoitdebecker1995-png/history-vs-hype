# Translation Pipeline Refactoring: DocumentTranslationPipeline Design

**Phase:** I (Deepening #3)  
**Date:** 2026-05-05  
**Status:** Design (ready for I3 implementation)

---

## Executive Summary

The 9-module translation pipeline (structure_detector, translator, cross_checker, legal_annotator, surprise_detector, formatter, verification, smoke_test, cli) will consolidate into a single **DocumentTranslationPipeline** class. This class acts as the unified entry point, orchestrating stages internally while delegating LLM work to Claude Code.

**Key principle:** The pipeline class is a *seam*, not a monolith. Each stage method calls a pure data-processor module, keeping modules independent and testable.

---

## DocumentTranslationPipeline Class Interface

### Constructor

```python
class DocumentTranslationPipeline:
    def __init__(self, project_dir: Optional[str] = None):
        """
        Initialize the translation pipeline.
        
        Args:
            project_dir: Optional project directory for writing reports/output
        """
```

### Main Entry Point

```python
def run_pipeline(
    self,
    document_text: str,
    source_language: str = 'french',
    document_type: Optional[str] = None,
    stages: Optional[List[str]] = None,
    narrative_baseline: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the full translation pipeline on a document.
    
    Args:
        document_text: Raw document text (string or file path)
        source_language: Source language name (default: 'french')
        document_type: Document type hint (legal_code, treaty, decree, etc.)
        stages: List of stages to run (default: all). Options:
            - 'detect' (required, always first)
            - 'translate' (requires Claude Code execution of payloads)
            - 'cross_check'
            - 'annotate'
            - 'surprise'
            - 'verify'
            - 'format'
        narrative_baseline: Narrative text for surprise detection (optional)
    
    Returns:
        {
            'detected_structure': {...},  # from _detect_structure()
            'sections': [  # article-by-article results
                {
                    'id': 'article-1',
                    'original': '...',
                    'translation': '...',
                    'cross_check_payload': {...},  # for Claude Code
                    'annotation_payload': {...},   # for Claude Code
                    'surprise_payload': {...},     # for Claude Code
                    'annotations': [...],          # after annotation stage
                    'surprise_severity': 'major',  # after surprise stage
                    'verification': {...}          # after verify stage
                }
            ],
            'formatted_output': '...',  # markdown or JSON
            'verification_verdict': 'GREEN|YELLOW|RED',
            'error': None  # or error message
        }
    """
```

### Per-Stage Methods (Internal)

Each method corresponds to one of the 9 existing modules:

#### Stage 1: Detect Structure

```python
def _detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Detect article/clause boundaries.
    
    Module: structure_detector.py → StructureDetector.detect_structure()
    Pure Python, no API calls.
    
    Returns: Dict with 'sections', 'document_type', 'section_count', etc.
    """
```

#### Stage 2: Translate (Payload Builder)

```python
def _build_translation_payloads(
    self,
    sections: List[Dict],
    source_language: str = 'french'
) -> List[Dict[str, Any]]:
    """
    Build Claude Code payloads for translating each section.
    
    Module: translator.py → TranslationDataBuilder.build_translation_payload()
    Returns: List of dicts, each ready for Claude Code to execute via API.
    
    Claude Code will call the API, then pass responses to _parse_translations().
    """
```

```python
def _parse_translations(self, responses: List[Dict]) -> List[Dict]:
    """
    Parse Claude API responses back into section dicts.
    
    Module: translator.py → TranslationDataBuilder.parse_response()
    Pure Python.
    
    Called by Claude Code after executing translation payloads.
    """
```

#### Stage 3: Cross-Check (Payload Builder)

```python
def _build_cross_check_payloads(
    self,
    sections: List[Dict],
    source_language: str = 'french'
) -> List[Dict[str, Any]]:
    """
    Build payloads for semantic comparison vs independent translation.
    
    Module: cross_checker.py → CrossChecker.build_comparison_payload()
    Returns: Payloads for Claude Code execution.
    
    Steps:
    1. CrossChecker internally gets independent translation (DeepL/googletrans/deep_translator)
    2. Returns payload for Claude Code to semantically compare Claude translation vs independent
    """
```

#### Stage 4: Annotate (Payload Builder)

```python
def _build_annotation_payloads(
    self,
    sections: List[Dict],
    source_language: str = 'french',
) -> List[Dict[str, Any]]:
    """
    Build payloads for annotating legal/technical terms.
    
    Module: legal_annotator.py → LegalAnnotator.build_annotation_payload()
    Returns: Payloads for Claude Code execution.
    """
```

#### Stage 5: Surprise Detection (Payload Builder)

```python
def _build_surprise_payloads(
    self,
    sections: List[Dict],
    narrative_baseline: str,
    source_language: str = 'french',
) -> List[Dict[str, Any]]:
    """
    Build payloads for identifying narrative-contradicting clauses.
    
    Module: surprise_detector.py → SurpriseDetector.build_surprise_payload()
    Returns: Payloads for Claude Code execution.
    """
```

#### Stage 6: Verify (Audit + Payload Builder)

```python
def _verify_translation(self, sections: List[Dict]) -> Dict[str, Any]:
    """
    Audit mode: check translation completeness (pure Python, no LLM).
    
    Module: verification.py → TranslationVerifier
    Returns: Audit result (GREEN/YELLOW/RED) + coverage report.
    
    For scholarly verification, returns payload builders for Claude Code.
    """
```

#### Stage 7: Format Output

```python
def _format_output(
    self,
    sections: List[Dict],
    output_format: str = 'markdown'
) -> str:
    """
    Format sections as paired original/translation.
    
    Module: formatter.py → Formatter.format_paired()
    Pure Python, no API calls.
    
    Returns: Markdown or JSON string.
    """
```

#### Health Check (Standalone)

```python
def smoke_test(self) -> Dict[str, Any]:
    """
    Pipeline health check.
    
    Module: smoke_test.py → run_smoke_test()
    Pure Python, no API calls.
    
    Returns: {'status': 'ok'} or {'error': msg}
    """
```

---

## Module → Stage Method Mapping

| Existing Module | Method(s) | Responsibility | Deletion Candidate? |
|---|---|---|---|
| **structure_detector.py** | `_detect_structure()` | Detect article boundaries | NO — keeps core structure |
| **translator.py** | `_build_translation_payloads()`, `_parse_translations()` | Build + parse translation payloads | NO — pure data builder, lightweight |
| **cross_checker.py** | `_build_cross_check_payloads()` | Build semantic comparison payload | NO — independent translation backend logic |
| **legal_annotator.py** | `_build_annotation_payloads()` | Build annotation payload | NO — term identification logic |
| **surprise_detector.py** | `_build_surprise_payloads()` | Build surprise payload | NO — narrative comparison logic |
| **verification.py** | `_verify_translation()` | Audit translation completeness | NO — verification logic stays modular |
| **formatter.py** | `_format_output()` | Format sections for display | NO — output formatting logic |
| **smoke_test.py** | `smoke_test()` | Health check | NO — diagnostic utility |
| **cli.py** | (see "What Stays Separate" below) | CLI argument parsing | YES — replaced by pipeline class |

---

## What Stays Separate

### translator.py (Keep — Lightweight)

**Why:** TranslationDataBuilder is pure data construction with no external dependencies. It's simple, testable, and reusable. Moving it inside DocumentTranslationPipeline adds no value.

**Interface remains unchanged:**
```python
from tools.translation.translator import TranslationDataBuilder

builder = TranslationDataBuilder()
payload = builder.build_translation_payload(...)
result = builder.parse_response(...)
```

### cli.py (Modify → Thin Wrapper)

**Current role:** Argument parsing + orchestration + file I/O

**New role (after I3):** Thin wrapper that instantiates DocumentTranslationPipeline and delegates

**New cli.py:**
```python
def main():
    args = parse_args()  # argument parsing (stays here)
    pipeline = DocumentTranslationPipeline(project_dir=args.project)
    result = pipeline.run_pipeline(
        document_text=read_file(args.file),
        source_language=args.language,
        stages=args.stages,
        narrative_baseline=args.narrative
    )
    print_output(result)  # output formatting (stays here)
```

---

## Deletion Test Annotations

### Files Eligible for Deletion (I4)

After consolidating into DocumentTranslationPipeline, these files can be deleted because their logic is fully absorbed:

1. ✅ **structure_detector.py** — Logic moved to `_detect_structure()` method
2. ✅ **cross_checker.py** — Logic moved to `_build_cross_check_payloads()` method
3. ✅ **legal_annotator.py** — Logic moved to `_build_annotation_payloads()` method
4. ✅ **surprise_detector.py** — Logic moved to `_build_surprise_payloads()` method
5. ✅ **verification.py** — Logic moved to `_verify_translation()` method
6. ✅ **formatter.py** — Logic moved to `_format_output()` method

### Files to Keep

- **translator.py** — Lightweight, pure data builder. No logic duplication — just imported by pipeline.
- **smoke_test.py** — Diagnostic utility. Imported by `smoke_test()` method.
- **cli.py** — Thin wrapper after refactor. Argument parsing + output I/O.
- **__init__.py** — Package init.

---

## Callers (Deletion Impact Check)

**Direct callers of individual modules (before refactor):**

1. `.claude/commands/translate.md` (slash command) → Will import DocumentTranslationPipeline instead
2. `tools/translation/cli.py` → Will use DocumentTranslationPipeline internally (stays, just refactored)
3. Tests in `tests/test_translation.py` → Will test DocumentTranslationPipeline + individual stage methods

**No external callers** (checked via `rg "from tools.translation.structure_detector|cross_checker|legal_annotator|..."` in `.claude/` and `tools/`)

---

## Integration Points for I3

### CLI Entry Point
```python
# OLD (before I3):
from tools.translation.structure_detector import StructureDetector
from tools.translation.cross_checker import CrossChecker
# ... 6 more imports ...

# NEW (after I3):
from tools.translation.pipeline import DocumentTranslationPipeline
```

### Slash Command (`/translate`)
```
# OLD: /translate orchestrated via multiple tool calls
# NEW: /translate calls DocumentTranslationPipeline.run_pipeline()
#      and handles Claude Code payloads internally
```

### Tests
```
# Existing tests (from I1):
- test_structure_detector_detects_articles() → stays, tests _detect_structure()
- test_cross_checker_builds_comparison_payload() → stays, tests _build_cross_check_payloads()
- etc.

# New tests (from I1):
- test_full_pipeline_integration() → already covers run_pipeline()
```

---

## Success Criteria (I3)

1. ✅ DocumentTranslationPipeline class exists in `tools/translation/pipeline.py`
2. ✅ All 9 modules' logic consolidated into stage methods
3. ✅ Pinning tests from I1 pass without modification
4. ✅ `/translate` slash command uses new pipeline
5. ✅ CLI thin wrapper works (parses args → instantiates pipeline → runs)

---

## Next Steps

- **I3:** Implement DocumentTranslationPipeline class + migrate CLI + update slash command (Sonnet recommended)
- **I4:** Delete 6 superseded modules (structure_detector, cross_checker, legal_annotator, surprise_detector, formatter, verification)

---

## Appendix: Class Skeleton (for I3 implementation)

```python
from typing import Dict, Any, List, Optional
from pathlib import Path

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
        """Main entry point. See class docstring."""
        
        stages = stages or ['detect', 'translate', 'cross_check', 'annotate', 'surprise', 'verify', 'format']
        
        # Stage 1: Always detect structure first
        structure = self._detect_structure(document_text, document_type)
        if 'error' in structure:
            return structure
        
        sections = structure.get('sections', [])
        
        # Subsequent stages (conditional)
        if 'cross_check' in stages:
            sections = self._augment_with_cross_check_payloads(sections, source_language)
        
        if 'annotate' in stages:
            sections = self._augment_with_annotation_payloads(sections, source_language)
        
        if 'surprise' in stages and narrative_baseline:
            sections = self._augment_with_surprise_payloads(sections, narrative_baseline, source_language)
        
        if 'verify' in stages:
            verification = self._verify_translation(sections)
        
        if 'format' in stages:
            formatted = self._format_output(sections, output_format='markdown')
        
        return {
            'detected_structure': structure,
            'sections': sections,
            'formatted_output': formatted if 'format' in stages else None,
            'verification_verdict': verification.get('verdict') if 'verify' in stages else None,
            'error': None
        }

    # Stage methods (see above for signatures)
    def _detect_structure(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        return self._structure_detector.detect_structure(text, document_type)
    
    # ... (other stage methods follow)
    
    def smoke_test(self) -> Dict[str, Any]:
        return run_smoke_test()
```

