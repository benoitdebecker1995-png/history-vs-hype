---
phase: 61-data-driven-packaging-gate
plan: 01
subsystem: tools
tags: [title-scorer, ctr, sqlite, packaging-gate]

requires:
  - phase: 27-ctr-tracking
    provides: ctr_snapshots and video_performance tables in keywords.db

provides:
  - tools/title_ctr_store.py with get_pattern_ctr_from_db() — DB-backed CTR lookup by title pattern
  - tools/title_scorer.py score_title() now accepts optional db_path — uses live DB scores when available

affects:
  - 61-02 (CTR ingestion tool wires data into the same ctr_snapshots table)
  - 61-03 (greenlight command will pass db_path to score_title())

tech-stack:
  added: []
  patterns:
    - "Lazy import pattern: title_ctr_store imports detect_pattern from title_scorer at call time (not module top), avoiding circular import"
    - "Silent fallback pattern: DB errors always return empty dict, score_title always falls back to static — no crash paths from DB layer"
    - "CTR-to-score calibration: score = min(100, max(0, int(ctr_percent * 17))) mapping 3.8% -> 64 (near static declarative baseline of 65)"

key-files:
  created:
    - tools/title_ctr_store.py
    - tests/unit/test_title_ctr_store.py
    - tests/unit/test_title_scorer_db.py
  modified:
    - tools/title_scorer.py

key-decisions:
  - "Lazy import used in title_ctr_store to import detect_pattern from title_scorer — avoids circular import since title_scorer conditionally imports from title_ctr_store"
  - "Only latest non-zero CTR snapshot per video used — prevents double-counting videos with multiple snapshots; zero-CTR rows are API velocity artifacts"
  - "min_sample=3 default — patterns with fewer than 3 videos excluded as statistically unreliable"
  - "db_enriched flag added to return dict — callers can distinguish static vs DB-derived scores without inspecting internals"
  - "Hard rejects (year, colon, the_x_that) are unaffected by DB scores — these are structural disqualifiers, not base-score adjustments"

requirements-completed: [GATE-01, GATE-02]

duration: 25min
completed: 2026-03-14
---

# Phase 61 Plan 01: TitleCTRStore Summary

**DB-backed title pattern scoring via get_pattern_ctr_from_db() + optional db_path on score_title(), replacing static constants with live CTR averages from keywords.db when n>=3**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-03-14T12:15:00Z
- **Completed:** 2026-03-14T12:41:20Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Created `tools/title_ctr_store.py` with `get_pattern_ctr_from_db()` that queries `ctr_snapshots JOIN video_performance`, classifies titles by pattern, and converts CTR% to 0-100 scores
- Wired DB scores into `tools/title_scorer.py` via optional `db_path` parameter — live scores replace static constants when available, silent fallback otherwise
- 22 unit tests covering empty DB, zero-CTR exclusion, min_sample threshold, multi-pattern independence, latest-snapshot-only logic, hard-reject preservation, and backward compatibility

## Task Commits

1. **Task 1: Create TitleCTRStore module with tests** — `b890f3e` (feat)
2. **Task 2: Wire DB scores into title_scorer.py with tests** — `a76b3d8` (feat)

## Files Created/Modified

- `tools/title_ctr_store.py` — DB-backed pattern CTR lookup; single public function get_pattern_ctr_from_db()
- `tools/title_scorer.py` — score_title() extended with optional db_path; adds db_enriched and db_base_score to return dict
- `tests/unit/test_title_ctr_store.py` — 10 unit tests for CTR store
- `tests/unit/test_title_scorer_db.py` — 12 unit tests for score_title with db_path

## Decisions Made

- Lazy import: `title_ctr_store` imports `detect_pattern` from `title_scorer` at call time to break potential circular import (title_scorer conditionally imports back)
- Zero-CTR exclusion: `ctr_percent > 0` in SQL — YouTube API returns 0 for very new videos, not a real CTR reading
- Latest-snapshot-only: subquery `MAX(snapshot_date) WHERE ctr_percent > 0` per video prevents double-weighting videos with frequent snapshots
- `db_enriched=False` when the specific pattern isn't in DB results — gives callers accurate signal about which patterns have live data

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

Pre-existing test failures in `tests/unit/test_pacing.py` (score assertion mismatch) and `tests/test_intel.py` (feedparser mock) were present before this plan and are out of scope. Both confirmed as pre-existing via baseline check before any changes.

## Next Phase Readiness

- `get_pattern_ctr_from_db()` ready for Plan 02 (CTR ingestion tool to populate ctr_snapshots)
- `score_title(db_path=...)` ready for Plan 03 (greenlight command integration)
- Circular import hazard documented — future callers must not import both modules at module load time

---
*Phase: 61-data-driven-packaging-gate*
*Completed: 2026-03-14*
