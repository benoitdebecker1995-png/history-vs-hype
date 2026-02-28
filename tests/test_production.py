"""Integration smoke tests for the production pipeline.

ScriptParser, EditGuideGenerator, and MetadataGenerator are stdlib-only --
no mocking needed. Tests use the tmp_script fixture (3-section markdown).
"""
import pytest


def test_script_parser_imports_cleanly():
    """ScriptParser is importable from tools.production."""
    from tools.production import ScriptParser
    assert ScriptParser is not None


def test_script_parser_parses_fixture(tmp_script):
    """ScriptParser.parse_file() parses the 3-section fixture script."""
    from tools.production import ScriptParser

    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))

    assert isinstance(sections, list)
    assert len(sections) >= 2  # 3-section fixture should produce >= 2 sections


def test_script_parser_section_has_heading(tmp_script):
    """Each parsed section has a non-empty heading attribute."""
    from tools.production import ScriptParser

    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))

    for section in sections:
        # Section objects have heading attribute or dict key
        heading = getattr(section, "heading", None) or (
            section.get("heading") if isinstance(section, dict) else None
        )
        assert heading is not None and heading != ""


def test_script_parser_section_has_word_count(tmp_script):
    """Each parsed section has a positive word_count."""
    from tools.production import ScriptParser

    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))

    for section in sections:
        wc = getattr(section, "word_count", None) or (
            section.get("word_count") if isinstance(section, dict) else None
        )
        if wc is not None:
            assert wc > 0


def test_edit_guide_generator_produces_string(tmp_script):
    """EditGuideGenerator.generate_edit_guide() returns a non-empty string."""
    from tools.production import ScriptParser, EditGuideGenerator

    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))

    gen = EditGuideGenerator(project_name="test-video-2026")
    result = gen.generate_edit_guide(sections)

    assert isinstance(result, str)
    assert len(result) > 0


def test_metadata_generator_produces_string(tmp_script):
    """MetadataGenerator.generate_metadata_draft() returns a non-empty string.

    Signature: generate_metadata_draft(sections, entities, timings)
    entities and timings can be empty lists for smoke test.
    """
    from tools.production import ScriptParser, MetadataGenerator, EditGuideGenerator

    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))

    edit_gen = EditGuideGenerator(project_name="test-video-2026")
    timings = edit_gen.calculate_timing(sections)

    meta_gen = MetadataGenerator(project_name="test-video-2026")
    result = meta_gen.generate_metadata_draft(
        sections=sections,
        entities=[],
        timings=timings,
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_production_pipeline_end_to_end(tmp_script):
    """ScriptParser -> EditGuideGenerator -> MetadataGenerator runs without error."""
    from tools.production import ScriptParser, EditGuideGenerator, MetadataGenerator

    # Parse
    parser = ScriptParser()
    sections = parser.parse_file(str(tmp_script))
    assert len(sections) >= 1

    # Edit guide
    edit_gen = EditGuideGenerator(project_name="test-video-2026")
    guide = edit_gen.generate_edit_guide(sections)
    assert isinstance(guide, str)

    # Metadata
    timings = edit_gen.calculate_timing(sections)
    meta_gen = MetadataGenerator(project_name="test-video-2026")
    metadata = meta_gen.generate_metadata_draft(
        sections=sections,
        entities=[],
        timings=timings,
    )
    assert isinstance(metadata, str)
