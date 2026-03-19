---
phase: 70-metadata-packaging-integration
plan: "02"
subsystem: tooling
tags: [python, metadata, coherence-check, title-generator, tdd, publish-command]

# Dependency graph
requires:
  - phase: 70-01
    provides: _generate_thumbnail_concepts, _generate_description, CLICKBAIT_PATTERNS
  - phase: 68-title-generation-upgrade
    provides: format_title_candidates, TitleMaterialExtractor

provides:
  - _coherence_check(candidates, thumbnail_concepts_text, description) -> str in MetadataGenerator
  - format_title_candidates() with optional coherence column (thumbnail_concepts + desc_first_line)
  - generate_metadata_draft() with topic_type param + locked section order
  - /publish --topic and --thumbs flags documented

affects: [MetadataGenerator, format_title_candidates, /publish command]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "_primary_entity set once in generate_metadata_draft from material, reused in _coherence_check"
    - "Coherence is annotation-only — N/3 badge in title table, detail section for mismatches only"
    - "format_title_candidates() backward-compatible: no coherence column when called without extra args"
    - "Locked section order: Titles → Description → Chapters → Tags → Thumbnail Concepts → Coherence Check → VidIQ Notes"

key-files:
  created:
    - (test additions to) tests/unit/test_metadata_bundle.py
    - (test additions to) tests/unit/test_title_generator.py
  modified:
    - tools/production/metadata.py
    - tools/production/title_generator.py
    - .claude/commands/publish.md

key-decisions:
  - "_primary_entity uses 4+ char minimum to exclude short tokens like 'UK' that produce false coherence hits"
  - "Coherence does NOT affect ranking — pure annotation; users see score and coherence independently"
  - "format_title_candidates backward compat: both thumbnail_concepts AND desc_first_line must be non-None to show column"
  - "Coherence detail section uses candidate index not rank to find position in list for accuracy"
  - "publish.md --topic documents valid types: territorial, ideological, political_fact_check"

# Metrics
duration: 7min
completed: 2026-03-19
---

# Phase 70 Plan 02: Metadata Coherence Check + Format Title Candidates Coherence Column Summary

**Metadata coherence check (META-03) wired end-to-end: _coherence_check() annotates each title candidate with a 3/3 ✅ / 2/3 ⚠️ / 1/3 ❌ badge, format_title_candidates() shows coherence column when called with thumbnail data, and generate_metadata_draft() assembles output in locked section order with topic_type passthrough**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-19T01:20:04Z
- **Completed:** 2026-03-19T01:27:11Z
- **Tasks:** 2 (Task 1 TDD, Task 2 auto)
- **Files modified:** 4 (metadata.py, title_generator.py, publish.md, + test file additions)

## Accomplishments

- `_coherence_check(candidates, thumbnail_concepts_text, description)` added to MetadataGenerator:
  - Uses `self._primary_entity` (set at top of `generate_metadata_draft` from material)
  - Annotates each candidate dict in-place: `candidate["coherence"] = "N/3 badge"`
  - Returns markdown detail section for candidates with count < 3 (mismatches only)
  - Returns `""` for empty candidates, warning string for `None` primary entity
- `format_title_candidates()` updated with optional `thumbnail_concepts` and `desc_first_line` params:
  - Backward-compatible: no extra args = no Coherence column (existing tests unchanged)
  - When both params provided: adds Coherence column using `candidate.get("coherence", "---")`
  - Sort order by score descending unchanged regardless of coherence
- `generate_metadata_draft()` updated:
  - Adds `topic_type: Optional[str] = None` parameter
  - `TitleMaterialExtractor` called once at top; result reused for description + thumbnails + coherence
  - `self._primary_entity` set from material before any section generation
  - `topic_type` passed through to `_generate_title_variants()` and `_generate_thumbnail_concepts()`
  - Final output in locked section order: Titles → Description → Chapters → Tags → Thumbnail Concepts → Coherence Check → VidIQ Notes
- `publish.md` updated:
  - `--topic` flag documented: overrides topic type for thumbnail patterns and coherence check
  - `--thumbs` flag documented: generates thumbnail concepts only
  - Thumbnail Concepts section rewritten to document auto-generation + validation badges
  - New Coherence Check section with example table showing 3/3 ✅ / 2/3 ⚠️ / 1/3 ❌ format

## Task Commits

1. **Task 1 (RED): Failing tests** — `a8c5a28` (test)
2. **Task 1 (GREEN): _coherence_check + format_title_candidates coherence column** — `3053b13` (feat)
3. **Task 2: Wire generate_metadata_draft + publish.md** — `f7aa6c1` (feat)

## Files Created/Modified

- `tools/production/metadata.py` — Added `_coherence_check()`, updated `generate_metadata_draft()` signature + output assembly, updated `_generate_title_variants()` signature
- `tools/production/title_generator.py` — Updated `format_title_candidates()` with optional coherence column params
- `.claude/commands/publish.md` — Added `--topic` and `--thumbs` to Flags table; new Thumbnail Concepts and Coherence Check documentation sections
- `tests/unit/test_metadata_bundle.py` — Added `TestCoherenceCheck` (7 tests) and `TestGenerateMetadataDraftIntegration` (1 test)
- `tests/unit/test_title_generator.py` — Added `TestFormatTitleCandidatesCoherenceColumn` (4 tests)

## Decisions Made

- 4-char minimum on primary entity: avoids false positives from short tokens ("UK", "EU") creating misleading coherence hits
- Annotation-only coherence: coherence never reorders candidates — user sees title score and coherence independently, consistent with CONTEXT.md "annotation per CONTEXT.md" specification
- Both `thumbnail_concepts` AND `desc_first_line` must be non-None for coherence column to appear in `format_title_candidates()` — prevents partial state where column header exists but data is missing
- Detail section uses `candidates.index(candidate)` for rank display, keeping it stable even if candidate list was pre-sorted

## Deviations from Plan

None - plan executed exactly as written.

The detail section wording ("Coherence Detail" header inside the returned string vs. as a separate markdown `##` header) was a minor presentation decision not specified in the plan — chose inline markdown within the string returned by `_coherence_check()` since it gets embedded in the larger output.

## Self-Check: PASSED

Files created/modified:
- FOUND: tools/production/metadata.py
- FOUND: tools/production/title_generator.py
- FOUND: .claude/commands/publish.md
- FOUND: tests/unit/test_metadata_bundle.py (additions)
- FOUND: tests/unit/test_title_generator.py (additions)

Commits:
- FOUND: a8c5a28 (test RED)
- FOUND: 3053b13 (feat GREEN Task 1)
- FOUND: f7aa6c1 (feat Task 2)

Test result: 57 passed, 0 failed
