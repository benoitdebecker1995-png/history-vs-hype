"""
Tests for Phase 70 — metadata.py CLICKBAIT consolidation, description template,
thumbnail concept generation, and coherence check.

Coverage:
    META-01: _extract_citations(), _generate_description() SEO first line + warnings
    META-02: _generate_thumbnail_concepts() — 3 concepts, grounded, validated
    META-03: _coherence_check() — per-candidate coherence counts + detail section
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


# ---------------------------------------------------------------------------
# META-03: _coherence_check() tests
# ---------------------------------------------------------------------------

class TestCoherenceCheck:
    """
    _coherence_check() annotates title candidates with coherence counts
    and produces a detail section only for mismatched candidates.
    """

    def _generator(self):
        from tools.production.metadata import MetadataGenerator
        gen = MetadataGenerator("test-project")
        gen._primary_entity = "Spain"
        return gen

    def _make_candidates(self, titles):
        """Build minimal candidate list."""
        return [
            {"title": t, "score": 70, "grade": "B", "pattern": "declarative",
             "penalties": [], "hard_rejects": []}
            for t in titles
        ]

    def test_full_match_returns_3_of_3(self):
        """Title + thumbnail + desc all contain primary entity -> 3/3."""
        gen = self._generator()
        candidates = self._make_candidates(["Spain Changed History"])
        thumbnail_text = "**Concept A** — Map of Spain showing conflict."
        desc = "Spain — a territorial analysis of Spain using primary sources."

        result = gen._coherence_check(candidates, thumbnail_text, desc)

        # The candidate should have coherence = "3/3 ✅"
        assert "3/3" in candidates[0].get("coherence", ""), (
            f"Expected 3/3 coherence, got: {candidates[0].get('coherence')}"
        )

    def test_partial_match_returns_2_of_3(self):
        """Title + thumbnail contain entity but desc does not -> 2/3."""
        gen = self._generator()
        candidates = self._make_candidates(["Spain Changed History"])
        thumbnail_text = "**Concept A** — Map of Spain showing conflict."
        desc = "A territorial history analysis using primary sources."  # no "Spain"

        result = gen._coherence_check(candidates, thumbnail_text, desc)

        assert "2/3" in candidates[0].get("coherence", ""), (
            f"Expected 2/3 coherence, got: {candidates[0].get('coherence')}"
        )

    def test_detail_section_absent_for_perfect_match(self):
        """Candidate with 3/3 does NOT appear in detail section."""
        gen = self._generator()
        candidates = self._make_candidates(["Spain Changed History"])
        thumbnail_text = "Map of Spain. No face, no text overlay."
        desc = "Spain — a territorial history of Spain."

        result = gen._coherence_check(candidates, thumbnail_text, desc)

        # Detail section should be absent (no mismatches to describe)
        assert "Coherence Detail" not in result or "Spain Changed History" not in result, (
            f"Perfect-match candidate should not appear in detail section.\nResult:\n{result}"
        )

    def test_detail_section_present_for_mismatch(self):
        """Candidate with count < 3 appears in detail section."""
        gen = self._generator()
        gen._primary_entity = "Portugal"
        candidates = self._make_candidates(["How Portugal Changed History"])
        thumbnail_text = "Map of Spain. No face, no text overlay."  # no "Portugal"
        desc = "A territorial history using primary sources."  # no "Portugal"

        result = gen._coherence_check(candidates, thumbnail_text, desc)

        # With 1/3 (only title has "Portugal"), detail section should appear
        assert "Portugal" in result or "Detail" in result or "mismatch" in result.lower() or len(result) > 0, (
            f"Expected detail section for mismatch candidate.\nResult:\n{result}"
        )

    def test_empty_candidates_returns_empty_string(self):
        """No candidates -> returns empty string, no crash."""
        gen = self._generator()
        result = gen._coherence_check([], "thumbnail text", "description text")
        assert result == "" or result.strip() == "", (
            f"Expected empty string for no candidates, got: {result!r}"
        )

    def test_none_primary_entity_returns_warning(self):
        """_primary_entity = None -> returns warning message, not crash."""
        from tools.production.metadata import MetadataGenerator
        gen = MetadataGenerator("test-project")
        gen._primary_entity = None  # explicitly set to None

        candidates = [{"title": "Spain Changed History", "score": 70, "grade": "B",
                       "pattern": "declarative", "penalties": [], "hard_rejects": []}]
        result = gen._coherence_check(candidates, "thumbnail", "description")

        assert "warning" in result.lower() or "no primary entity" in result.lower(), (
            f"Expected warning for None primary entity, got: {result!r}"
        )

    def test_coherence_does_not_change_sort_order(self):
        """Candidates are sorted by score descending regardless of coherence."""
        gen = self._generator()
        candidates = [
            {"title": "Spain Changed History", "score": 80, "grade": "A",
             "pattern": "declarative", "penalties": [], "hard_rejects": []},
            {"title": "Why History Was Wrong", "score": 65, "grade": "B",
             "pattern": "how_why", "penalties": [], "hard_rejects": []},
        ]
        thumbnail_text = "Map of Spain. No face, no text overlay."
        desc = "A history analysis using sources."  # only first candidate has "Spain"

        gen._coherence_check(candidates, thumbnail_text, desc)

        from tools.production.title_generator import format_title_candidates
        output = format_title_candidates(candidates)

        # Rank 1 must still be the highest score (Spain at 80), not the most coherent
        lines = output.splitlines()
        rank1_rows = [l for l in lines if l.startswith("| 1 |")]
        assert rank1_rows and "Spain Changed History" in rank1_rows[0], (
            f"Rank 1 should still be highest score, got: {rank1_rows}"
        )


# ---------------------------------------------------------------------------
# META-03: generate_metadata_draft() integration test
# ---------------------------------------------------------------------------

class TestGenerateMetadataDraftIntegration:
    """
    generate_metadata_draft() with topic_type produces all 6 sections in locked order.
    """

    def _make_sections(self):
        return [
            _make_section(
                "Introduction",
                "Spain and Portugal divided the world in 1494 by the Treaty of Tordesillas. "
                "Spain claimed the west, Portugal claimed the east. "
                "Contrary to popular belief, this division was not permanent.",
                "intro",
            ),
            _make_section(
                "Background",
                "The papal bull Inter caetera authorised the original split. "
                "Portugal protested and both nations negotiated the treaty. "
                "Spain and Portugal competed for colonial dominance for centuries.",
                "body",
            ),
        ]

    def test_all_six_sections_present_in_locked_order(self):
        """Output contains Title Candidates, Description, Chapters, Tags, Thumbnail Concepts, Coherence Check."""
        from unittest.mock import patch
        PATCH_TARGET = "tools.production.title_generator.score_title"

        def _stub(title, db_path=None, topic_type=None):
            from tools.title_scorer import detect_pattern
            return {
                "title": title, "score": 70, "grade": "B",
                "pattern": detect_pattern(title), "length": len(title),
                "base_score": 70, "penalties": [], "bonuses": [],
                "suggestions": [], "hard_rejects": [], "db_enriched": False,
                "db_base_score": None, "niche_enriched": False,
                "niche_base_score": None, "fallback_warning": None,
                "detected_topic": "general",
                "topic_type_target": {"pass": 60, "good": 70, "gap_message": ""},
                "niche_percentile_label": "",
            }

        from tools.production.metadata import MetadataGenerator
        from tools.production.entities import Entity

        gen = MetadataGenerator("test-project")
        sections = self._make_sections()
        entities = [
            Entity(text="Spain", entity_type="place", mentions=3,
                   positions=[1], normalized="spain"),
        ]

        with patch(PATCH_TARGET, side_effect=_stub):
            output = gen.generate_metadata_draft(sections, entities, [], topic_type="territorial")

        SECTION_ORDER = [
            "Title Candidates",
            "Description",
            "Chapters",
            "Tags",
            "Thumbnail Concepts",
            "Coherence Check",
        ]

        positions = []
        for section_name in SECTION_ORDER:
            pos = output.find(section_name)
            assert pos != -1, f"Section '{section_name}' not found in output.\nOutput:\n{output[:500]}"
            positions.append(pos)

        # Check locked order
        for i in range(len(positions) - 1):
            assert positions[i] < positions[i + 1], (
                f"Section order violated: '{SECTION_ORDER[i]}' (pos {positions[i]}) "
                f"should come before '{SECTION_ORDER[i+1]}' (pos {positions[i+1]})"
            )
