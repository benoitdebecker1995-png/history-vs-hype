"""Integration smoke tests for the translation pipeline.

Tests TranslationDataBuilder payload build and response parsing
without making actual Claude API calls.
The pipeline's no-API steps can be tested directly.
"""
import pytest


SAMPLE_CLAUSE = (
    "Article 1. Les personnes physiques qui ont \u00e9t\u00e9 consid\u00e9r\u00e9es "
    "comme juives par les lois de l'ennemi sont regard\u00e9es comme telles."
)
SAMPLE_DOCUMENT = (
    "Article 1. Les personnes physiques qui ont \u00e9t\u00e9 consid\u00e9r\u00e9es "
    "comme juives par les lois de l'ennemi sont regard\u00e9es comme telles.\n\n"
    "Article 2. Sont interdits aux Juifs, les professions ci-apr\u00e8s \u00e9num\u00e9r\u00e9es."
)

MOCK_RESPONSE = """TRANSLATION:
Article 1. Natural persons who were considered Jewish under the laws of the enemy are regarded as such for the purposes of this ordinance.

NOTES:
- This clause established the legal definition of Jewish identity under the Vichy regime.
- The phrase "lois de l'ennemi" (laws of the enemy) refers to Nazi racial definitions."""


def test_translation_data_builder_imports_cleanly():
    """TranslationDataBuilder is importable without sys.path hacks."""
    from tools.translation.translator import TranslationDataBuilder
    assert TranslationDataBuilder is not None


def test_translation_data_builder_instantiates():
    """TranslationDataBuilder can be instantiated without arguments."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()
    assert builder is not None


def test_build_translation_payload_returns_dict():
    """build_translation_payload() returns a dict with no error."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    payload = builder.build_translation_payload(
        clause_text=SAMPLE_CLAUSE,
        full_document=SAMPLE_DOCUMENT,
        source_language="french",
        clause_id="article-1",
    )

    assert isinstance(payload, dict)
    assert "error" not in payload


def test_build_payload_contains_required_keys():
    """Payload includes clause_id, system_prompt, and user_prompt keys."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    payload = builder.build_translation_payload(
        clause_text=SAMPLE_CLAUSE,
        full_document=SAMPLE_DOCUMENT,
        source_language="french",
        clause_id="article-1",
    )

    assert payload.get("clause_id") == "article-1"
    assert "system_prompt" in payload
    assert "user_prompt" in payload
    assert len(payload["user_prompt"]) > 0


def test_build_payload_clause_id_preserved():
    """Payload clause_id matches the input clause_id."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    payload = builder.build_translation_payload(
        clause_text=SAMPLE_CLAUSE,
        full_document=SAMPLE_DOCUMENT,
        source_language="spanish",
        clause_id="articulo-3",
    )

    assert "error" not in payload
    assert payload.get("clause_id") == "articulo-3"


def test_parse_response_returns_dict():
    """parse_response() parses a mock Claude response without API call.

    Signature: parse_response(response_text, clause_id, original_text)
    """
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    result = builder.parse_response(
        response_text=MOCK_RESPONSE,
        clause_id="article-1",
        original_text=SAMPLE_CLAUSE,
    )

    assert isinstance(result, dict)


def test_parse_response_extracts_translation():
    """parse_response() extracts translation text from TRANSLATION: marker."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    result = builder.parse_response(
        response_text=MOCK_RESPONSE,
        clause_id="article-1",
        original_text=SAMPLE_CLAUSE,
    )

    assert result.get("clause_id") == "article-1"
    assert result.get("translation") is not None
    assert len(result.get("translation", "")) > 0


def test_parse_response_empty_notes_graceful():
    """parse_response() handles response with no NOTES section."""
    from tools.translation.translator import TranslationDataBuilder
    builder = TranslationDataBuilder()

    no_notes_response = "TRANSLATION:\nNatural persons considered Jewish are regarded as such."
    result = builder.parse_response(
        response_text=no_notes_response,
        clause_id="article-1",
        original_text=SAMPLE_CLAUSE,
    )

    assert isinstance(result, dict)
    assert isinstance(result.get("notes", []), list)


# ====== COMPREHENSIVE PIPELINE PINNING TESTS (Phase I) ======

def test_structure_detector_reads_test_fixture():
    """StructureDetector can read and parse test_french.txt fixture."""
    from pathlib import Path
    from tools.translation.pipeline import StructureDetector

    fixture_path = Path("tests/fixtures/test_french.txt")
    assert fixture_path.exists(), "test_french.txt fixture missing"

    text = fixture_path.read_text(encoding="utf-8")
    assert len(text) > 0
    assert "Article" in text


def test_structure_detector_detects_articles():
    """StructureDetector.detect_structure() correctly identifies articles."""
    from pathlib import Path
    from tools.translation.pipeline import StructureDetector

    fixture_path = Path("tests/fixtures/test_french.txt")
    text = fixture_path.read_text(encoding="utf-8")

    detector = StructureDetector()
    result = detector.detect_structure(text, document_type="legal_code")

    assert isinstance(result, dict)
    assert "error" not in result
    assert "articles" in result or "sections" in result or "lines" in result


def test_cross_checker_builds_comparison_payload():
    """CrossChecker builds valid comparison payloads without API calls."""
    from tools.translation.pipeline import CrossChecker

    checker = CrossChecker()
    payload = checker.build_comparison_payload(
        claude_translation="Natural persons who were considered Jewish are regarded as such.",
        backend_translation="Persons considered Jewish under the enemy laws are so regarded.",
        original_text=SAMPLE_CLAUSE,
        clause_id="article-1",
        source_language="french"
    )

    assert isinstance(payload, dict)
    assert "error" not in payload
    assert "system_prompt" in payload or "prompt" in payload


def test_legal_annotator_builds_annotation_payload():
    """LegalAnnotator builds valid annotation payloads without API calls."""
    from tools.translation.pipeline import LegalAnnotator

    annotator = LegalAnnotator()
    payload = annotator.build_annotation_payload(
        clause_text=SAMPLE_CLAUSE,
        translation="Natural persons who were considered Jewish are regarded as such.",
        clause_id="article-1",
        source_language="french",
        document_context="1940 Vichy statute"
    )

    assert isinstance(payload, dict)
    assert "error" not in payload
    assert "system_prompt" in payload or "prompt" in payload


def test_surprise_detector_builds_surprise_payload():
    """SurpriseDetector builds valid surprise payloads without API calls."""
    from tools.translation.pipeline import SurpriseDetector

    detector = SurpriseDetector()
    payload = detector.build_surprise_payload(
        clause_text=SAMPLE_CLAUSE,
        translation="Natural persons who were considered Jewish are regarded as such.",
        narrative_baseline="The Vichy regime only applied French law.",
        clause_id="article-1",
        source_language="french",
        document_context="1940 Vichy statute"
    )

    assert isinstance(payload, dict)
    assert "error" not in payload
    assert "system_prompt" in payload or "prompt" in payload


def test_formatter_formats_paired_output():
    """Formatter.format_paired() correctly formats translated sections."""
    from tools.translation.pipeline import Formatter

    formatter = Formatter()
    sections = [
        {
            "id": "article-1",
            "heading": "Article 1",
            "original": SAMPLE_CLAUSE,
            "translation": "Natural persons who were considered Jewish are regarded as such for the purposes of this ordinance.",
            "footnotes": []
        },
        {
            "id": "article-2",
            "heading": "Article 2",
            "original": "Article 2. Sont interdits aux Juifs.",
            "translation": "Article 2. The following professions are forbidden to Jews.",
            "footnotes": ["Note: This section lists prohibited occupations"]
        }
    ]

    result = formatter.format_paired(sections, output_format="markdown")

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Article 1" in result


def test_full_pipeline_integration():
    """Full pipeline: detect structure → build payloads → format output."""
    from pathlib import Path
    from tools.translation.pipeline import StructureDetector, CrossChecker, LegalAnnotator, SurpriseDetector, Formatter

    # Stage 1: Detect structure
    fixture_path = Path("tests/fixtures/test_french.txt")
    text = fixture_path.read_text(encoding="utf-8")

    detector = StructureDetector()
    structure = detector.detect_structure(text, document_type="legal_code")
    assert "error" not in structure

    # Stage 2: Build cross-check payload
    checker = CrossChecker()
    check_payload = checker.build_comparison_payload(
        claude_translation="Natural persons who were considered Jewish are regarded as such.",
        backend_translation="Persons considered Jewish under the enemy laws are so regarded.",
        original_text=SAMPLE_CLAUSE,
        clause_id="article-1",
        source_language="french"
    )
    assert "error" not in check_payload

    # Stage 3: Build annotation payload
    annotator = LegalAnnotator()
    annot_payload = annotator.build_annotation_payload(
        clause_text=SAMPLE_CLAUSE,
        translation="Natural persons who were considered Jewish are regarded as such.",
        clause_id="article-1",
        source_language="french"
    )
    assert "error" not in annot_payload

    # Stage 4: Build surprise payload
    surprise = SurpriseDetector()
    surprise_payload = surprise.build_surprise_payload(
        clause_text=SAMPLE_CLAUSE,
        translation="Natural persons who were considered Jewish are regarded as such.",
        narrative_baseline="The Vichy regime only applied French law.",
        clause_id="article-1",
        source_language="french"
    )
    assert "error" not in surprise_payload

    # Stage 5: Format output
    formatter = Formatter()
    sections = [
        {
            "id": "article-1",
            "heading": "Article 1",
            "original": SAMPLE_CLAUSE,
            "translation": "Natural persons who were considered Jewish are regarded as such.",
            "footnotes": []
        }
    ]
    formatted = formatter.format_paired(sections, output_format="markdown")
    assert isinstance(formatted, str)
    assert len(formatted) > 0
