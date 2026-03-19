"""
Tests for Phase 70 — metadata.py CLICKBAIT consolidation, description template,
thumbnail concept generation.

Coverage:
    META-01: _extract_citations(), _generate_description() SEO first line + warnings
    META-02: _generate_thumbnail_concepts() — 3 concepts, grounded, validated
    CLICKBAIT: CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS exported from title_scorer.py
              and imported (not re-defined) in metadata.py
"""

import inspect
import re
import types

import pytest

from tools.production.parser import Section


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_section(heading: str, content: str, section_type: str = "body") -> Section:
    return Section(
        heading=heading,
        content=content,
        word_count=len(content.split()),
        start_line=1,
        section_type=section_type,
    )


# ---------------------------------------------------------------------------
# CLICKBAIT consolidation tests
# ---------------------------------------------------------------------------

class TestClickbaitConsolidation:
    """CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS must live in title_scorer.py."""

    def test_clickbait_patterns_importable_from_title_scorer(self):
        """CLICKBAIT_PATTERNS is a module-level export of title_scorer.py."""
        from tools import title_scorer
        assert hasattr(title_scorer, "CLICKBAIT_PATTERNS"), (
            "title_scorer.py must export CLICKBAIT_PATTERNS at module level"
        )
        assert isinstance(title_scorer.CLICKBAIT_PATTERNS, list)
        assert len(title_scorer.CLICKBAIT_PATTERNS) >= 5

    def test_allowed_acronyms_importable_from_title_scorer(self):
        """ALLOWED_ACRONYMS is a module-level export of title_scorer.py."""
        from tools import title_scorer
        assert hasattr(title_scorer, "ALLOWED_ACRONYMS"), (
            "title_scorer.py must export ALLOWED_ACRONYMS at module level"
        )
        assert isinstance(title_scorer.ALLOWED_ACRONYMS, list)
        assert len(title_scorer.ALLOWED_ACRONYMS) >= 10

    def test_metadata_imports_clickbait_from_title_scorer(self):
        """metadata.py must NOT define its own CLICKBAIT_PATTERNS — must import from title_scorer."""
        import tools.production.metadata as metadata_mod
        # The module should have CLICKBAIT_PATTERNS (via import), but it must
        # NOT be defined in the metadata module's own source code
        source = inspect.getsource(metadata_mod)
        # Check that CLICKBAIT_PATTERNS is not defined locally
        assert "CLICKBAIT_PATTERNS = [" not in source, (
            "metadata.py must not define CLICKBAIT_PATTERNS locally — import from title_scorer"
        )
        # Check that the import exists
        assert "from tools.title_scorer import" in source or "from ..title_scorer import" in source, (
            "metadata.py must import CLICKBAIT_PATTERNS from title_scorer"
        )

    def test_allowed_acronyms_not_defined_in_metadata(self):
        """ALLOWED_ACRONYMS must not be redefined in metadata.py."""
        import tools.production.metadata as metadata_mod
        source = inspect.getsource(metadata_mod)
        assert "ALLOWED_ACRONYMS = [" not in source, (
            "metadata.py must not define ALLOWED_ACRONYMS locally — import from title_scorer"
        )


# ---------------------------------------------------------------------------
# compute_tone_score tests
# ---------------------------------------------------------------------------

class TestComputeToneScore:
    """compute_tone_score() is defined in title_scorer.py."""

    def test_compute_tone_score_exists(self):
        from tools import title_scorer
        assert hasattr(title_scorer, "compute_tone_score"), (
            "title_scorer.py must define compute_tone_score()"
        )

    def test_active_verb_returns_positive(self):
        """Title with active verb returns positive score."""
        from tools.title_scorer import compute_tone_score
        result = compute_tone_score("Spain DESTROYED Portugal")
        assert result > 0, f"Expected positive score for active verb title, got {result}"

    def test_clickbait_returns_negative(self):
        """Title with clickbait pattern returns negative score."""
        from tools.title_scorer import compute_tone_score
        result = compute_tone_score("SHOCKING Truth About Spain")
        assert result < 0, f"Expected negative score for clickbait title, got {result}"

    def test_neutral_returns_zero(self):
        """Title with no active verb and no clickbait returns 0."""
        from tools.title_scorer import compute_tone_score
        result = compute_tone_score("Spain vs Portugal")
        # no active verb, no clickbait → 0
        assert result == 0, f"Expected 0 for neutral title, got {result}"


# ---------------------------------------------------------------------------
# _extract_citations tests
# ---------------------------------------------------------------------------

class TestExtractCitations:
    """_extract_citations() parses academic citation patterns from script sections."""

    def _generator(self):
        from tools.production.metadata import MetadataGenerator
        return MetadataGenerator("test-project")

    def test_extracts_according_to_pattern(self):
        """Finds 'According to X in Y, page N' pattern."""
        gen = self._generator()
        sections = [_make_section(
            "Section 1",
            "According to Chris Wickham in The Inheritance of Rome, page 147, literacy dropped.",
        )]
        citations = gen._extract_citations(sections)
        assert len(citations) >= 1
        assert any("Wickham" in c for c in citations), f"Expected Wickham citation, got: {citations}"
        assert any("Inheritance" in c for c in citations)
        assert any("147" in c for c in citations)

    def test_extracts_possessive_apostrophe_pattern(self):
        """Finds 'Author's *Title*, p. N' pattern."""
        gen = self._generator()
        sections = [_make_section(
            "Section 2",
            "Harris's *Ancient Literacy*, p. 23 suggests Roman literacy was around 10%.",
        )]
        citations = gen._extract_citations(sections)
        assert len(citations) >= 1, f"Expected citation from possessive pattern, got: {citations}"
        assert any("Harris" in c for c in citations)

    def test_empty_on_no_citations(self):
        """Returns empty list when script has no citations."""
        gen = self._generator()
        sections = [_make_section(
            "Section 3",
            "France and Britain competed for dominance in the 18th century.",
        )]
        citations = gen._extract_citations(sections)
        assert isinstance(citations, list)
        assert citations == [], f"Expected empty list, got: {citations}"

    def test_deduplicates_citations(self):
        """Same citation appearing twice in different sections is returned once."""
        gen = self._generator()
        text = "According to Chris Wickham in The Inheritance of Rome, page 147, literacy dropped."
        sections = [
            _make_section("Section 1", text),
            _make_section("Section 2", text),
        ]
        citations = gen._extract_citations(sections)
        # Count Wickham citations
        wickham_count = sum(1 for c in citations if "Wickham" in c and "147" in c)
        assert wickham_count == 1, f"Expected 1 Wickham citation, got {wickham_count}"


# ---------------------------------------------------------------------------
# _generate_description tests
# ---------------------------------------------------------------------------

class TestGenerateDescription:
    """_generate_description() produces SEO first line, citations, and warnings."""

    def _generator(self):
        from tools.production.metadata import MetadataGenerator
        return MetadataGenerator("test-project")

    def test_first_line_not_in_this_video(self):
        """First line must not start with 'In this video'."""
        gen = self._generator()
        sections = [_make_section("Introduction", "Spain and Portugal divided the world in 1494.", "intro")]
        entities = []
        timings = []
        desc = gen._generate_description(sections, entities, timings)
        first_line = desc.splitlines()[0]
        assert not first_line.lower().startswith("in this video"), (
            f"Description first line must not start with 'In this video', got: {first_line!r}"
        )

    def test_first_line_contains_primary_entity_or_keyword(self):
        """First line should contain a keyword/entity name, not generic filler."""
        gen = self._generator()
        # Script about Spain (a findable entity)
        sections = [
            _make_section(
                "Introduction",
                "Spain and Portugal signed the Treaty of Tordesillas in 1494 to divide the world.",
                "intro",
            )
        ]
        entities = []
        timings = []
        desc = gen._generate_description(sections, entities, timings)
        first_line = desc.splitlines()[0]
        # Should contain 'Spain' or 'Portugal' or 'Tordesillas' — something grounded
        found_keyword = any(kw in first_line for kw in ["Spain", "Portugal", "Tordesillas", "Treaty"])
        assert found_keyword, (
            f"First line should contain a script-derived keyword, got: {first_line!r}"
        )

    def test_description_contains_extracted_citations(self):
        """When citations exist in script, description body includes them."""
        gen = self._generator()
        sections = [_make_section(
            "Section 1",
            "According to Chris Wickham in The Inheritance of Rome, page 147, literacy dropped.",
        )]
        desc = gen._generate_description(sections, [], [])
        assert "Wickham" in desc, (
            f"Expected 'Wickham' in description from auto-extracted citation, desc:\n{desc}"
        )

    def test_warning_when_no_citations(self):
        """Appends warning block when no citations found."""
        gen = self._generator()
        sections = [_make_section("Section 1", "France expanded in the 19th century.")]
        desc = gen._generate_description(sections, [], [])
        assert "⚠️" in desc or "MISSING" in desc, (
            f"Expected warning block when no citations found, desc:\n{desc}"
        )

    def test_warning_when_no_timings(self):
        """Appends warning block when no timings provided."""
        gen = self._generator()
        sections = [_make_section("Section 1", "France expanded in the 19th century.")]
        desc = gen._generate_description(sections, [], [])
        # Should warn about missing timestamps
        lower_desc = desc.lower()
        assert "timestamp" in lower_desc or "timing" in lower_desc or "⚠️" in desc, (
            f"Expected timing warning when no timings, desc:\n{desc}"
        )

    def test_description_always_outputs_text_despite_warnings(self):
        """Even with missing elements, description is not empty."""
        gen = self._generator()
        sections = [_make_section("Section 1", "France was powerful.")]
        desc = gen._generate_description(sections, [], [])
        assert desc.strip() != "", "Description must not be empty even when warnings are present"
        # Must have at least some real content (more than just warnings)
        non_warning_lines = [l for l in desc.splitlines() if l.strip() and "⚠️" not in l and "MISSING" not in l]
        assert len(non_warning_lines) >= 1, (
            f"Description must contain content beyond warnings, got:\n{desc}"
        )


# ---------------------------------------------------------------------------
# _generate_thumbnail_concepts tests
# ---------------------------------------------------------------------------

class TestGenerateThumbnailConcepts:
    """_generate_thumbnail_concepts() returns exactly 3 script-grounded concepts."""

    def _generator(self):
        from tools.production.metadata import MetadataGenerator
        return MetadataGenerator("test-project")

    def _territorial_material(self):
        """Material dict for a territorial topic."""
        from tools.production.entities import Entity
        spain = Entity(text="Spain", entity_type="place", mentions=5, positions=[1], normalized="spain")
        portugal = Entity(text="Portugal", entity_type="place", mentions=4, positions=[2], normalized="portugal")
        tordesillas = Entity(
            text="Treaty of Tordesillas", entity_type="document",
            mentions=3, positions=[3], normalized="treaty of tordesillas"
        )
        return {
            "entities": [(spain, 10.0), (portugal, 8.0)],
            "documents": [(tordesillas, 6.0)],
            "numbers": [("370 leagues", 2.0)],
            "contradictions": [],
        }

    def _ideological_material(self):
        """Material dict for an ideological topic."""
        from tools.production.entities import Entity
        myth = Entity(text="Catholic Church", entity_type="organization", mentions=4, positions=[1], normalized="catholic church")
        return {
            "entities": [(myth, 8.0)],
            "documents": [],
            "numbers": [],
            "contradictions": [("The church controlled science", "Actually scientists disagreed", 2.0)],
        }

    def test_territorial_returns_three_concepts(self):
        """Returns string with exactly 3 Concept blocks for territorial topic."""
        gen = self._generator()
        material = self._territorial_material()
        result = gen._generate_thumbnail_concepts(material, [], topic_type="territorial")
        concept_count = len(re.findall(r'\*\*Concept [ABC]\*\*', result))
        assert concept_count == 3, (
            f"Expected exactly 3 Concept blocks for territorial topic, got {concept_count}.\n"
            f"Output:\n{result}"
        )

    def test_ideological_returns_three_concepts(self):
        """Returns string with exactly 3 Concept blocks for ideological topic."""
        gen = self._generator()
        material = self._ideological_material()
        result = gen._generate_thumbnail_concepts(material, [], topic_type="ideological")
        concept_count = len(re.findall(r'\*\*Concept [ABC]\*\*', result))
        assert concept_count == 3, (
            f"Expected exactly 3 Concept blocks for ideological topic, got {concept_count}.\n"
            f"Output:\n{result}"
        )

    def test_concept_contains_script_entity(self):
        """Concept text contains a script-extracted entity name, not generic placeholder."""
        gen = self._generator()
        material = self._territorial_material()
        result = gen._generate_thumbnail_concepts(material, [], topic_type="territorial")
        # Should contain Spain or Portugal or Tordesillas (extracted from material)
        has_entity = any(e in result for e in ["Spain", "Portugal", "Tordesillas", "370 leagues"])
        assert has_entity, (
            f"Concept text should contain script-extracted entity names.\nOutput:\n{result}"
        )

    def test_each_concept_has_thumbnail_checker_badge(self):
        """Each concept has a ✅ or ⚠️ badge from thumbnail_checker."""
        gen = self._generator()
        material = self._territorial_material()
        result = gen._generate_thumbnail_concepts(material, [], topic_type="territorial")
        # Each **Concept X** line should be followed by a badge character
        # The badge is either ✅ or ⚠️ somewhere near the Concept header
        badge_count = result.count("✅") + result.count("⚠️")
        assert badge_count >= 3, (
            f"Expected at least 3 badges (one per concept), got {badge_count}.\nOutput:\n{result}"
        )
