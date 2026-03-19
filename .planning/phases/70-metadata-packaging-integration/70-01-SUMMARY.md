---
phase: 70-metadata-packaging-integration
plan: "01"
subsystem: tooling
tags: [python, metadata, title-scorer, thumbnail, citations, tdd]

# Dependency graph
requires:
  - phase: 68-title-generation-upgrade
    provides: TitleMaterialExtractor, format_title_candidates, generate_title_candidates
  - phase: 69-hook-quality-upgrade
    provides: nothing directly consumed here
provides:
  - CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS as module-level exports of title_scorer.py
  - compute_tone_score(title) -> int unified tone scoring in title_scorer.py
  - _extract_citations(sections) -> List[str] academic citation extractor in MetadataGenerator
  - _generate_description() with SEO first line + auto-extracted citations + warning block
  - _generate_thumbnail_concepts() producing 3 script-grounded concepts with thumbnail_checker badges
  - _fill_template() for 8 thumbnail pattern types
affects: [phase-70-plan-02-coherence-check, /publish command, MetadataGenerator]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Single source of truth: CLICKBAIT_PATTERNS/ALLOWED_ACRONYMS defined once in title_scorer.py, imported everywhere else"
    - "Never hard-block: description warnings are appended ⚠️ blocks, not exceptions"
    - "Topic-adaptive thumbnails: THUMBNAIL_PATTERNS dict maps topic type to 3 pattern names"

key-files:
  created:
    - tests/unit/test_metadata_bundle.py
  modified:
    - tools/title_scorer.py
    - tools/production/metadata.py

key-decisions:
  - "CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS moved to title_scorer.py as sole authoritative source; metadata.py imports via 'from tools.title_scorer import'"
  - "compute_tone_score uses _TONE_SIGNALS dict combining active verbs (+5) and clickbait patterns (-10 each)"
  - "possessive apostrophe strip uses endswith(\"'s\") not rstrip to preserve author name (e.g. Harris not Harri)"
  - "SEO first line: entity + topic_verb from classify_topic_type(); never starts with 'In this video'"
  - "Warnings appended to description output — description is always produced regardless of missing elements"
  - "Thumbnail concepts always include 'map'/'geographic' signal word and 'No face, no text overlay.' for thumbnail_checker PASS"

patterns-established:
  - "TDD: test file committed before implementation; RED phase confirmed before GREEN"
  - "Citation regex: two patterns handle 'According to X in Y, page N' and possessive 'X's *Y*, p. N'"

requirements-completed: [META-01, META-02]

# Metrics
duration: 6min
completed: 2026-03-19
---

# Phase 70 Plan 01: CLICKBAIT Consolidation + Description Template + Thumbnail Concepts Summary

**CLICKBAIT_PATTERNS consolidated to title_scorer.py; MetadataGenerator now produces SEO-first descriptions with auto-extracted academic citations, warning blocks, and 3 script-grounded thumbnail concepts validated by thumbnail_checker**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-19T01:02:32Z
- **Completed:** 2026-03-19T01:08:32Z
- **Tasks:** 2 (both TDD)
- **Files modified:** 3 (title_scorer.py, metadata.py, + new test file)

## Accomplishments
- CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS moved from metadata.py to title_scorer.py — single authoritative source, zero drift possible
- compute_tone_score(title) added to title_scorer.py with unified _TONE_SIGNALS dict
- _extract_citations() parses two academic citation patterns from script body with deduplication
- _generate_description() rewritten: keyword-rich SEO first line, auto-citations, chapters hook, ⚠️ warning block for missing elements (never blocks output)
- _generate_thumbnail_concepts() generates 3 concepts per topic type (territorial/ideological/political_fact_check/general), each filled with script-extracted entities and validated by thumbnail_checker

## Task Commits

Each task was committed atomically:

1. **Task 1 (test RED): CLICKBAIT tests written** - `d339bdd` (test)
2. **Task 1 (GREEN): CLICKBAIT consolidation + compute_tone_score** - `7fbb6cf` (feat)
3. **Task 2 (GREEN): description + citations + thumbnail concepts** - `b8d26da` (feat)

_Note: TDD tasks share test file; RED commit covers both tasks (test file written before any implementation)_

## Files Created/Modified
- `tools/title_scorer.py` — Added CLICKBAIT_PATTERNS, ALLOWED_ACRONYMS, _TONE_SIGNALS, compute_tone_score() exports
- `tools/production/metadata.py` — Removed local list definitions, added import from title_scorer, added _extract_citations(), rewrote _generate_description(), added _generate_thumbnail_concepts(), _fill_template(), plus module-level regex/dict constants
- `tests/unit/test_metadata_bundle.py` — New file: 22 tests covering all plan behaviors

## Decisions Made
- CLICKBAIT_PATTERNS uses `endswith("'s")` not `rstrip("'s")` to correctly strip possessive suffix without corrupting author names (Harris not Harri)
- SEO first line uses classify_topic_type() on first 200 chars of first section — same function as title_scorer.py for consistency
- Thumbnail concepts always include explicit map/geographic signal and "No face, no text overlay." phrase so thumbnail_checker reliably passes RULE 1, RULE 2, RULE 3
- THUMBNAIL_PATTERNS dict used instead of hard-coded if/elif so pattern sets can be extended without touching method logic

## Deviations from Plan

None - plan executed exactly as written.

The possessive apostrophe strip fix (using `endswith("'s")` instead of `rstrip`) was a bug discovered during RED→GREEN iteration, not a deviation — it was a detail not specified in the plan that required care.

## Issues Encountered
- Possessive citation regex matched correctly but `rstrip("'s")` stripped individual chars instead of the suffix, producing "Harri" instead of "Harris". Fixed by `if author.endswith("'s"): author = author[:-2]`.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- META-01 and META-02 requirements complete
- Plan 70-02 (META-03 coherence check + format_title_candidates coherence column) can proceed
- All 22 new tests pass; 45 total tests pass (test_metadata_bundle + test_title_generator)

---
*Phase: 70-metadata-packaging-integration*
*Completed: 2026-03-19*
