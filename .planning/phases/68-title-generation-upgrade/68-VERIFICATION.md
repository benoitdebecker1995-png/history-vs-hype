---
phase: 68-title-generation-upgrade
verified: 2026-03-18T12:00:00Z
status: passed
score: 8/8 must-haves verified
re_verification: false
gaps: []
human_verification:
  - test: "Run /publish --titles on a real video script"
    expected: "Ranked markdown table with # / Title / Score / Grade / Pattern columns; penalized candidates shown with [warning] lines at bottom, not omitted"
    why_human: "Requires Claude generation context + formatted output review; no automated test covers the full /publish CLI path"
---

# Phase 68: Title Generation Upgrade — Verification Report

**Phase Goal:** Upgrade title generation from generic A/B/C suggestions to script-material-driven, auto-scored candidates with penalty warnings
**Verified:** 2026-03-18
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| #  | Truth                                                                                                          | Status     | Evidence                                                                                                 |
|----|----------------------------------------------------------------------------------------------------------------|------------|----------------------------------------------------------------------------------------------------------|
| 1  | Full script scan extracts specific numbers, document names, contradictions, and entity pairs with position weighting | VERIFIED   | `TitleMaterialExtractor.extract_from_sections()` applies intro=2.0/conclusion=1.5/body=1.0 weights; 5 tests cover all 4 material types |
| 2  | SRT subtitle files produce the same material types as markdown scripts                                         | VERIFIED   | `extract_from_srt()` strips sequence numbers/timestamps/HTML; creates synthetic sections; 2 tests pass  |
| 3  | Two named entities co-occurring with conflict language trigger versus detection with a signal strength score    | VERIFIED   | `detect_versus_signal()` uses 100-word co-occurrence window + CONFLICT_MARKERS list; score = hits/3.0 capped at 1.0; 3 tests pass |
| 4  | Candidate generation always includes at least one declarative variant                                          | VERIFIED   | `TitleCandidateGenerator.generate()` always appends declarative titles first; `test_declarative_always_generated` passes |
| 5  | Versus variant is generated when conflict signal is detected                                                   | VERIFIED   | `generate()` adds versus title when signal_strength > 0; `test_versus_variant_generated_when_signal_detected` passes |
| 6  | Running /publish --titles shows a ranked table instead of A/B/C format                                         | VERIFIED   | `metadata.py` calls `format_title_candidates()` which renders `## Title Candidates (ranked by score)` header + markdown table; no "Title A/B/C Test Variants" string in file |
| 7  | Penalized candidates appear with warning labels, not silently dropped                                          | VERIFIED   | `format_title_candidates()` appends `[warning] #N penalized: reason` for every `hard_rejects` entry; `test_all_candidates_shown` confirms none dropped |
| 8  | Output format shows rank, title, score, grade, and pattern for each candidate                                  | VERIFIED   | Table columns: `# | Title | Score | Grade | Pattern`; confirmed in `test_format_ranked_table` |

**Score:** 8/8 truths verified

---

### Required Artifacts

| Artifact                                    | Expected                                                          | Status     | Details                                                                 |
|---------------------------------------------|-------------------------------------------------------------------|------------|-------------------------------------------------------------------------|
| `tools/production/title_generator.py`       | TitleMaterialExtractor, TitleCandidateGenerator, detect_versus_signal, generate_title_candidates, format_title_candidates | VERIFIED   | File exists, 806 lines, all 5 exports present, substantive implementation |
| `tests/unit/test_title_generator.py`        | Unit tests >= 120 lines covering extraction, versus detection, candidate generation | VERIFIED   | File exists, 636 lines, 23 tests in 7 test classes |
| `tools/production/metadata.py`              | Updated _generate_title_variants() delegating to title_generator; ranked output format | VERIFIED   | Imports `generate_title_candidates, format_title_candidates`; `_generate_title_variants()` delegates; no A/B/C table |

---

### Key Link Verification

| From                              | To                              | Via                                               | Status     | Details                                                      |
|-----------------------------------|---------------------------------|---------------------------------------------------|------------|--------------------------------------------------------------|
| `tools/production/title_generator.py` | `tools/production/entities.py`  | `from tools.production.entities import Entity, EntityExtractor` | WIRED      | Line 28: `from tools.production.entities import Entity, EntityExtractor` |
| `tools/production/title_generator.py` | `tools/production/parser.py`    | `from tools.production.parser import ScriptParser, Section, strip_for_teleprompter` | WIRED      | Line 29: confirmed import |
| `tools/production/title_generator.py` | `tools/title_scorer.py`         | `from tools.title_scorer import score_title`      | WIRED      | Line 30: import present; `score_title()` called at line 684 inside `_score()` |
| `tools/production/metadata.py`    | `tools/production/title_generator.py` | `from .title_generator import generate_title_candidates, format_title_candidates` | WIRED      | Line 25: import present; both functions called in `generate_metadata_draft()` |
| `tools/production/metadata.py`    | `tools/title_scorer.py`         | Scoring pipeline through title_generator           | WIRED      | Indirect via title_generator._score() -> score_title(); pipeline confirmed |

---

### Requirements Coverage

| Requirement | Source Plan(s) | Description                                                                                                                          | Status    | Evidence                                                                                          |
|-------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------|
| TITLE-01    | 68-01         | `/publish --titles` reads the script and extracts specific numbers, document names, and contradictions as raw material for title candidates | SATISFIED | `TitleMaterialExtractor` extracts all 3 material types from full script; wired into metadata.py  |
| TITLE-02    | 68-01, 68-02  | Title generation produces versus and declarative variants as default output when topic has two competing entities                     | SATISFIED | `detect_versus_signal()` + `TitleCandidateGenerator` always produce declarative; versus generated when signal > 0 |
| TITLE-03    | 68-02         | Titles with penalty patterns receive heavy score penalties and are shown ranked last with warning labels — never silently dropped     | SATISFIED | `format_title_candidates()` shows all candidates; hard_rejects shown as warning lines; scoring via `score_title()` applies penalties |

No orphaned requirements: all three TITLE-* IDs declared in plan frontmatter match REQUIREMENTS.md and have implementation evidence.

---

### Anti-Patterns Found

| File                                    | Line | Pattern                    | Severity | Impact |
|-----------------------------------------|------|----------------------------|----------|--------|
| `tools/production/metadata.py`          | 413  | `[PLACEHOLDER: Add academic sources from script]` | Info     | Description section placeholder — not related to title generation goal; pre-existing |
| `tools/production/metadata.py`          | 421  | `[PLACEHOLDER: Related video links]`              | Info     | Same — pre-existing description placeholder |
| `tools/production/metadata.py`          | 157  | `[PLACEHOLDER: To be added manually...]`          | Info     | Thumbnail concepts placeholder — expected manual step |

No blockers. All placeholders are in the description/thumbnail section which is outside the phase goal scope. The title generation path contains no stubs.

---

### Human Verification Required

#### 1. End-to-End /publish --titles Output

**Test:** Run `/publish --titles` on an actual video project (e.g., `video-projects/_IN_PRODUCTION/41-treaty-tordesillas-2026/`) and review the terminal output.
**Expected:** A ranked markdown table appears with columns `# | Title | Score | Grade | Pattern`. Penalized titles (with year or colon) appear at the bottom with `[warning] #N penalized: reason` lines. No "Title A" / "Title B" / "Title C" headers appear.
**Why human:** Requires the full Claude generation pipeline + command dispatch context; no automated test covers the `/publish` slash command entry point end-to-end.

---

### Gaps Summary

No gaps. All automated checks passed:

- 23/23 unit tests green (`python -m pytest tests/unit/test_title_generator.py -q`)
- Full test suite: 275 passed, 8 pre-existing failures in unrelated modules (test_intel, test_pacing, test_ctr_tracker — confirmed pre-existing in plan 02 SUMMARY)
- All 5 public exports importable
- metadata.py delegation wired and confirmed
- Old A/B/C format absent from metadata.py
- All 3 TITLE requirements satisfied with implementation evidence

One item flagged for human verification: end-to-end `/publish --titles` CLI path cannot be tested programmatically.

---

_Verified: 2026-03-18_
_Verifier: Claude (gsd-verifier)_
