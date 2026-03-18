"""
Unit tests for tools/production/title_generator.py

Tests cover:
  - TitleMaterialExtractor: number extraction, document extraction,
    contradiction extraction, SRT input, position weighting
  - detect_versus_signal: entity pair detection, signal strength
  - TitleCandidateGenerator: declarative always present, scored candidates
"""

import sys
import types
import unittest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Stub score_title to avoid DB / benchmark_store dependencies in unit tests
# ---------------------------------------------------------------------------

def _stub_score_title(title: str, db_path=None, topic_type=None) -> dict:
    """Returns a predictable result dict matching the real score_title() signature."""
    from tools.title_scorer import detect_pattern
    pattern = detect_pattern(title)
    return {
        "title": title,
        "score": 65,
        "grade": "B",
        "pattern": pattern,
        "length": len(title),
        "base_score": 65,
        "penalties": [],
        "bonuses": [],
        "suggestions": [],
        "hard_rejects": [],
        "db_enriched": False,
        "db_base_score": None,
        "niche_enriched": False,
        "niche_base_score": None,
        "fallback_warning": None,
        "detected_topic": "general",
        "topic_type_target": {"pass": 60, "good": 70, "gap_message": ""},
        "niche_percentile_label": "",
    }


# Patch score_title before importing title_generator
PATCH_TARGET = "tools.production.title_generator.score_title"


class TestTitleMaterialExtractorNumbers(unittest.TestCase):
    """Tests for _extract_numbers_with_context (numbers extracted from body text)."""

    def setUp(self):
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            self.extractor = TitleMaterialExtractor()

    def test_extracts_number_from_body(self):
        """Script with '10-15%' in body -> material['numbers'] contains that value."""
        from tools.production.parser import ScriptParser, Section
        section = Section(
            heading="Literacy",
            content="Roman literacy was around 10-15% according to historians.",
            word_count=10,
            start_line=5,
            section_type="body",
        )
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = self.extractor.extract_from_sections([section])

        numbers = [item for item, _w in material["numbers"]]
        # At least one number/percentage should be extracted
        found = any("10" in n or "15" in n or "10-15" in n for n in numbers)
        self.assertTrue(found, f"Expected '10-15%' in numbers, got: {numbers}")

    def test_skips_year_in_number_extraction(self):
        """Years like 1453 must NOT appear in material['numbers']."""
        from tools.production.parser import Section
        section = Section(
            heading="Fall",
            content="Constantinople fell in 1453 after a 53-day siege.",
            word_count=9,
            start_line=1,
            section_type="body",
        )
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = self.extractor.extract_from_sections([section])

        numbers = [item for item, _w in material["numbers"]]
        year_found = any("1453" in n for n in numbers)
        self.assertFalse(year_found, f"Year 1453 should be excluded, got: {numbers}")

        # 53 (days) should be found
        non_year_found = any("53" in n for n in numbers)
        self.assertTrue(non_year_found, f"Expected '53' in numbers, got: {numbers}")


class TestTitleMaterialExtractorDocuments(unittest.TestCase):
    """Tests for document entity extraction."""

    def test_extracts_document_name(self):
        """Script mentioning 'Treaty of Utrecht' multiple times -> in material['documents']."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        from tools.production.parser import Section
        section = Section(
            heading="Background",
            content=(
                "The Treaty of Utrecht was signed in 1713. "
                "Under the Treaty of Utrecht, Spain ceded Gibraltar to Britain. "
                "The Treaty of Utrecht remains contested today."
            ),
            word_count=30,
            start_line=1,
            section_type="body",
        )
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_sections([section])

        docs = [item.text.lower() if hasattr(item, "text") else str(item).lower()
                for item, _w in material["documents"]]
        found = any("utrecht" in d for d in docs)
        self.assertTrue(found, f"Expected 'Treaty of Utrecht' in documents, got: {docs}")


class TestTitleMaterialExtractorContradictions(unittest.TestCase):
    """Tests for contradiction extraction."""

    def test_extracts_contradiction(self):
        """Script with 'contrary to popular belief ... weren't actually dark' -> contradiction pair."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        from tools.production.parser import Section
        section = Section(
            heading="Hook",
            content=(
                "Contrary to popular belief, the Dark Ages weren't actually dark. "
                "In fact, medieval scholars made significant advances in mathematics."
            ),
            word_count=20,
            start_line=1,
            section_type="intro",
        )
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_sections([section])

        contradictions = material.get("contradictions", [])
        self.assertGreater(len(contradictions), 0,
                           "Expected at least one contradiction pair extracted")

    def test_extracts_actually_pattern(self):
        """Script with 'the myth is X. In reality/actually Y' -> contradiction."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        from tools.production.parser import Section
        section = Section(
            heading="Body",
            content="The myth claims Spain discovered America, but in reality Columbus never reached the mainland.",
            word_count=15,
            start_line=1,
            section_type="body",
        )
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_sections([section])

        contradictions = material.get("contradictions", [])
        self.assertGreater(len(contradictions), 0,
                           "Expected contradiction from 'myth claims ... but in reality'")


class TestSRTInput(unittest.TestCase):
    """Tests for extract_from_srt — SRT produces same material types as markdown."""

    SRT_TEXT = """\
1
00:00:00,000 --> 00:00:05,000
Roman literacy was around 10-15% according to scholars.

2
00:00:05,001 --> 00:00:10,000
The Treaty of Utrecht reshaped European borders.

3
00:00:10,001 --> 00:00:15,000
Spain and Portugal divided the world between them.

4
00:00:15,001 --> 00:00:20,000
Contrary to popular belief, this division didn't last.
"""

    def test_srt_input_extracts_material(self):
        """SRT text produces numbers, documents, entities — same types as markdown."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_srt(self.SRT_TEXT)

        # Numbers should include 10-15% or similar
        numbers = [item for item, _w in material["numbers"]]
        has_number = len(numbers) > 0
        self.assertTrue(has_number, f"SRT should extract numbers, got: {numbers}")

        # Entities should be present
        entities = material.get("entities", [])
        self.assertGreater(len(entities), 0, "SRT should extract entities")

    def test_srt_strips_sequence_numbers_and_timestamps(self):
        """SRT sequence numbers and timestamps must not appear in extracted content."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_srt(self.SRT_TEXT)

        # Entities should not include raw timestamps like "00:00:05"
        entities = material.get("entities", [])
        entity_texts = [e.text if hasattr(e, "text") else str(e) for e, _w in entities]
        for t in entity_texts:
            self.assertNotRegex(t, r"\d{2}:\d{2}:\d{2}",
                                f"Timestamp leaked into entities: {t}")


class TestPositionWeighting(unittest.TestCase):
    """Tests for position weight multipliers: intro=2.0, conclusion=1.5, body=1.0."""

    def test_position_weighting_intro_higher_than_body(self):
        """Entity in intro section has higher weight than same-frequency entity in body."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleMaterialExtractor
            extractor = TitleMaterialExtractor()

        from tools.production.parser import Section

        # "Gibraltar" only in intro, "Somalia" only in body — same mention count
        intro_section = Section(
            heading="Hook",
            content="Gibraltar is a contested territory claimed by both Spain and Britain.",
            word_count=12,
            start_line=1,
            section_type="intro",
        )
        body_section = Section(
            heading="Background",
            content="Somalia declared independence in 1960 after years of colonial rule.",
            word_count=12,
            start_line=10,
            section_type="body",
        )

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            material = extractor.extract_from_sections([intro_section, body_section])

        entities_with_weights = material.get("entities", [])
        # Find Gibraltar (intro) and Somalia (body)
        gibraltar_weight = None
        somalia_weight = None
        for entity, weight in entities_with_weights:
            text = entity.text if hasattr(entity, "text") else str(entity)
            if "gibraltar" in text.lower():
                gibraltar_weight = weight
            elif "somalia" in text.lower():
                somalia_weight = weight

        if gibraltar_weight is not None and somalia_weight is not None:
            self.assertGreater(
                gibraltar_weight, somalia_weight,
                f"Intro entity ({gibraltar_weight}) should outweigh body entity ({somalia_weight})"
            )


class TestVersusDetection(unittest.TestCase):
    """Tests for detect_versus_signal."""

    def test_versus_auto_detection_strong_signal(self):
        """Spain + Portugal co-occurring with 'divided' and 'competed' -> signal > 0.5."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import detect_versus_signal
            from tools.production.entities import Entity

        entities = [
            Entity(text="Spain", entity_type="place", mentions=3,
                   positions=[1, 3, 5], normalized="spain"),
            Entity(text="Portugal", entity_type="place", mentions=3,
                   positions=[1, 3, 5], normalized="portugal"),
        ]
        full_text = (
            "Spain and Portugal divided the world between them. "
            "Spain competed with Portugal for colonial dominance. "
            "They disputed the boundaries repeatedly. "
            "Spain claimed the west, Portugal claimed the east. "
            "This rivalry between Spain and Portugal shaped history. "
            "Spain vs Portugal: who really won the colonial race?"
        )

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            entity_a, entity_b, strength = detect_versus_signal(entities, full_text)

        self.assertGreater(strength, 0.5,
                           f"Expected strong signal (>0.5), got {strength}")
        self.assertIn("spain", entity_a.lower() + entity_b.lower())
        self.assertIn("portugal", entity_a.lower() + entity_b.lower())

    def test_versus_weak_signal_not_primary(self):
        """Two entities with only 1 incidental co-occurrence -> signal_strength <= 0.5."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import detect_versus_signal
            from tools.production.entities import Entity

        entities = [
            Entity(text="France", entity_type="place", mentions=1,
                   positions=[1], normalized="france"),
            Entity(text="Germany", entity_type="place", mentions=1,
                   positions=[1], normalized="germany"),
        ]
        full_text = (
            "France and Germany signed the agreement peacefully. "
            "The cooperation between the two nations was unprecedented."
        )

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            _a, _b, strength = detect_versus_signal(entities, full_text)

        self.assertLessEqual(strength, 0.5,
                             f"Expected weak/no signal (<=0.5), got {strength}")

    def test_versus_no_entities_returns_empty(self):
        """Empty entity list returns ('', '', 0.0)."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import detect_versus_signal

        a, b, strength = detect_versus_signal([], "Some text here.")
        self.assertEqual(a, "")
        self.assertEqual(b, "")
        self.assertEqual(strength, 0.0)


class TestCandidateGeneration(unittest.TestCase):
    """Tests for TitleCandidateGenerator."""

    def _make_material(self):
        """Build a minimal material dict for generation tests."""
        from tools.production.entities import Entity
        entity = Entity(text="Haiti", entity_type="place", mentions=5,
                        positions=[1, 2, 3, 4, 5], normalized="haiti")
        return {
            "numbers": [("21 billion", 2.0)],
            "documents": [(entity, 1.5)],
            "entities": [(entity, 2.0)],
            "contradictions": [("Haiti was poor", "Haiti was the wealthiest colony", 1.0)],
        }

    def test_declarative_always_generated(self):
        """Any input -> at least one candidate with pattern='declarative'."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleCandidateGenerator
            gen = TitleCandidateGenerator()
            material = self._make_material()
            candidates = gen.generate(material, ("", "", 0.0))

        declarative_found = any(c["pattern"] == "declarative" for c in candidates)
        self.assertTrue(declarative_found,
                        f"No declarative candidate found in: {[c['pattern'] for c in candidates]}")

    def test_candidates_scored(self):
        """Every candidate has 'score', 'grade', 'pattern' keys."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleCandidateGenerator
            gen = TitleCandidateGenerator()
            material = self._make_material()
            candidates = gen.generate(material, ("", "", 0.0))

        self.assertGreater(len(candidates), 0, "Expected at least one candidate")
        for c in candidates:
            self.assertIn("score", c, f"Missing 'score' key in candidate: {c}")
            self.assertIn("grade", c, f"Missing 'grade' key in candidate: {c}")
            self.assertIn("pattern", c, f"Missing 'pattern' key in candidate: {c}")

    def test_versus_variant_generated_when_signal_detected(self):
        """When signal_strength > 0, a versus variant should be generated."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleCandidateGenerator
            gen = TitleCandidateGenerator()
            material = self._make_material()
            versus_signal = ("Spain", "Portugal", 0.8)
            candidates = gen.generate(material, versus_signal)

        versus_found = any(c["pattern"] == "versus" for c in candidates)
        self.assertTrue(versus_found,
                        f"Expected versus candidate when signal=0.8, got: {[c['pattern'] for c in candidates]}")

    def test_no_versus_variant_without_signal(self):
        """When signal_strength == 0.0, no versus candidate is generated."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleCandidateGenerator
            gen = TitleCandidateGenerator()
            # Material with no contradictions and no signal
            from tools.production.entities import Entity
            entity = Entity(text="Haiti", entity_type="place", mentions=5,
                            positions=[1, 2, 3, 4, 5], normalized="haiti")
            material = {
                "numbers": [],
                "documents": [(entity, 1.5)],
                "entities": [(entity, 2.0)],
                "contradictions": [],
            }
            candidates = gen.generate(material, ("", "", 0.0))

        versus_found = any(c["pattern"] == "versus" for c in candidates)
        self.assertFalse(versus_found,
                         "Versus candidate should not appear without versus signal")

    def test_titles_within_max_length(self):
        """All generated title strings must be <= 70 characters."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import TitleCandidateGenerator
            gen = TitleCandidateGenerator()
            material = self._make_material()
            candidates = gen.generate(material, ("Spain", "Portugal", 0.8))

        for c in candidates:
            self.assertLessEqual(
                len(c["title"]), 70,
                f"Title too long ({len(c['title'])} chars): {c['title']}"
            )


class TestConvenienceFunction(unittest.TestCase):
    """Tests for generate_title_candidates orchestration function."""

    def test_generate_title_candidates_from_sections(self):
        """generate_title_candidates returns sorted list with score/grade/pattern keys."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import generate_title_candidates
            from tools.production.parser import Section

        sections = [
            Section(
                heading="Opening",
                content=(
                    "Spain and Portugal divided the world in 1494. "
                    "The Treaty of Tordesillas split the globe between them. "
                    "Spain claimed everything west, Portugal everything east. "
                    "They competed and disputed boundaries for centuries. "
                    "Contrary to popular belief, the division was not permanent."
                ),
                word_count=40,
                start_line=1,
                section_type="intro",
            ),
        ]

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            results = generate_title_candidates(sections=sections)

        self.assertGreater(len(results), 0, "Expected candidates from sections")
        for r in results:
            self.assertIn("score", r)
            self.assertIn("grade", r)
            self.assertIn("pattern", r)

        # Check sorted descending by score
        scores = [r["score"] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True),
                         "Results should be sorted by score descending")

    def test_generate_title_candidates_from_srt(self):
        """generate_title_candidates works with srt_text parameter."""
        srt = """\
1
00:00:00,000 --> 00:00:05,000
Spain and Portugal divided the world.

2
00:00:05,001 --> 00:00:10,000
They competed and disputed territories for centuries.

3
00:00:10,001 --> 00:00:15,000
Contrary to popular belief, it was not a clean split.
"""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import generate_title_candidates
            results = generate_title_candidates(srt_text=srt)

        self.assertGreater(len(results), 0, "Expected candidates from SRT input")


class TestFormatTitleCandidates(unittest.TestCase):
    """Tests for format_title_candidates() — ranked table output with warning labels."""

    def _make_candidate(self, title: str, score: int, grade: str = "B",
                        pattern: str = "declarative", hard_rejects: list = None) -> dict:
        """Build a minimal candidate dict for formatting tests."""
        return {
            "title": title,
            "score": score,
            "grade": grade,
            "pattern": pattern,
            "penalties": [],
            "hard_rejects": hard_rejects or [],
        }

    def test_format_ranked_table(self):
        """4 candidate dicts -> output contains header, markdown table with correct columns."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import format_title_candidates

        candidates = [
            self._make_candidate("Haiti Changed History", 75, "A", "declarative"),
            self._make_candidate("Why Haiti History Is Wrong", 65, "B", "how_why"),
            self._make_candidate("Spain vs Haiti", 70, "B+", "versus"),
            self._make_candidate("Haiti and the myth", 60, "B-", "curiosity"),
        ]

        output = format_title_candidates(candidates)

        self.assertIn("Title Candidates (ranked by score)", output)
        self.assertIn("| # | Title | Score | Grade | Pattern |", output)
        # Top scorer should appear first (rank 1)
        lines = output.splitlines()
        table_rows = [l for l in lines if l.startswith("|") and "Haiti Changed History" in l]
        self.assertTrue(table_rows, "Top candidate should appear in table")
        # Check rank 1 is the highest score (75)
        rank1_row = [l for l in lines if l.startswith("| 1 |")]
        self.assertTrue(rank1_row, "Rank 1 row should be present")
        self.assertIn("Haiti Changed History", rank1_row[0])

    def test_penalized_candidates_show_warning(self):
        """Candidate with hard_rejects=['year in title'] -> warning line in output."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import format_title_candidates

        candidates = [
            self._make_candidate("Haiti Changed History", 75, "A", "declarative"),
            self._make_candidate("Haiti 1804 Revolution", 25, "D", "declarative",
                                 hard_rejects=["year in title"]),
        ]

        output = format_title_candidates(candidates)

        self.assertIn("penalized:", output.lower())
        self.assertIn("year in title", output)

    def test_all_candidates_shown(self):
        """5 candidates including 2 with hard_rejects -> all 5 appear in table (none dropped)."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import format_title_candidates

        candidates = [
            self._make_candidate("Haiti Changed History", 75, "A", "declarative"),
            self._make_candidate("Why Haiti", 70, "A-", "how_why"),
            self._make_candidate("Spain vs Portugal", 65, "B", "versus"),
            self._make_candidate("Haiti 1804", 25, "D", "declarative",
                                 hard_rejects=["year in title"]),
            self._make_candidate("The Haiti: Story", 30, "D", "declarative",
                                 hard_rejects=["colon in title"]),
        ]

        output = format_title_candidates(candidates)

        # All 5 titles should appear in the output
        for candidate in candidates:
            self.assertIn(candidate["title"], output,
                          f"Candidate '{candidate['title']}' was silently dropped")

    def test_year_candidate_ranked_last(self):
        """Candidate with low score (from year penalty) appears at bottom of ranked table."""
        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.title_generator import format_title_candidates

        candidates = [
            self._make_candidate("Haiti Changed History", 75, "A", "declarative"),
            self._make_candidate("Why Haiti History Is Wrong", 65, "B", "how_why"),
            self._make_candidate("Haiti 1804: The Revolution", 15, "F", "declarative",
                                 hard_rejects=["year in title", "colon in title"]),
        ]

        output = format_title_candidates(candidates)

        lines = output.splitlines()
        # Find the row indices for the year-penalized candidate and the top candidate
        haiti_row_idx = None
        year_row_idx = None
        for i, line in enumerate(lines):
            if "Haiti Changed History" in line and line.startswith("|"):
                haiti_row_idx = i
            if "Haiti 1804" in line and line.startswith("|"):
                year_row_idx = i

        self.assertIsNotNone(haiti_row_idx, "Top candidate not found in table")
        self.assertIsNotNone(year_row_idx, "Year-penalized candidate not found in table")
        self.assertLess(haiti_row_idx, year_row_idx,
                        "Top candidate should appear before year-penalized candidate in table")

    def test_output_replaces_abc(self):
        """generate_metadata_draft output contains 'Title Candidates', not 'Title A/B/C Test Variants'."""
        from tools.production.parser import Section
        from tools.production.entities import Entity

        section = Section(
            heading="Opening",
            content=(
                "Spain and Portugal competed for colonial dominance. "
                "They divided the world by the Treaty of Tordesillas. "
                "Contrary to popular belief, the division was never truly enforced."
            ),
            word_count=30,
            start_line=1,
            section_type="intro",
        )
        entity = Entity(text="Spain", entity_type="place", mentions=2,
                        positions=[1, 2], normalized="spain")

        with patch(PATCH_TARGET, side_effect=_stub_score_title):
            from tools.production.metadata import MetadataGenerator
            gen = MetadataGenerator("test-project")
            output = gen.generate_metadata_draft([section], [entity], [])

        self.assertIn("Title Candidates", output)
        self.assertNotIn("Title A/B/C Test Variants", output)
        self.assertNotIn("**Recommendation:** Test A vs B first", output)


if __name__ == "__main__":
    unittest.main()
