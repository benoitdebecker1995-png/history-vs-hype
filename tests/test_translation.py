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
