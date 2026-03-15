---
phase: 63-v6-gap-closure
plan: 01
subsystem: tools
tags: [retitle, ctr-ingest, database, requirements, documentation, gap-closure]
requirements_completed: [RETITLE-02, GATE-02]

dependency_graph:
  requires:
    - tools/title_scorer.py (score_title with db_path parameter)
    - tools/discovery/database.py (KeywordDB)
    - tools/ctr_ingest.py (_lookup_video_id)
    - .claude/commands/retitle.md (Step 4c)
  provides:
    - KeywordDB.search_video_performance_by_title() public method
    - ctr_ingest._lookup_video_id() delegates to public API
    - /retitle Step 4c passes db_path to score_title()
    - Accurate REQUIREMENTS.md traceability for all shipped phases
  affects:
    - tools/discovery/database.py
    - tools/ctr_ingest.py
    - .claude/commands/retitle.md
    - .planning/REQUIREMENTS.md
    - SUMMARY frontmatter for 60-02, 61-02, 61-03

tech_stack:
  added: []
  patterns:
    - Public method delegation (KeywordDB.search_video_performance_by_title)
    - DB-enriched scoring via db_path parameter (matches greenlight.md + scorer.py pattern)

key_files:
  created: []
  modified:
    - tools/discovery/database.py
    - tools/ctr_ingest.py
    - .claude/commands/retitle.md
    - .planning/REQUIREMENTS.md
    - .planning/phases/60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr/60-02-SUMMARY.md
    - .planning/phases/61-data-driven-packaging-gate-for-new-videos-title-scorer-reads-real-ctr-from-db-greenlight-enforces-minimum-score-feedback-loop-closes-automatically/61-02-SUMMARY.md
    - .planning/phases/61-data-driven-packaging-gate-for-new-videos-title-scorer-reads-real-ctr-from-db-greenlight-enforces-minimum-score-feedback-loop-closes-automatically/61-03-SUMMARY.md

decisions:
  - "search_video_performance_by_title() added to KeywordDB as public method — ctr_ingest now delegates entirely to it, eliminating the only private _conn access pattern outside of the DB class itself"
  - "retitle.md Step 4c matches greenlight.md and scorer.py pattern: KeywordDB().db_path then score_title(t, db_path=db_path) then db.close()"

metrics:
  duration: 157s
  completed: 2026-03-15
  tasks_completed: 2
  files_modified: 7
---

# Phase 63 Plan 01: v6.0 Gap Closure Summary

**One-liner:** Wired DB-enriched title scoring into /retitle, replaced private KeywordDB._conn access with public search_video_performance_by_title() method, and marked all 24 v5.2 requirements as Complete in REQUIREMENTS.md.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Wire DB-enriched scoring into /retitle and fix ctr_ingest private access | 915e625 | tools/discovery/database.py, tools/ctr_ingest.py, .claude/commands/retitle.md |
| 2 | Fix SUMMARY frontmatter gaps and REQUIREMENTS.md traceability | cf644d3 | .planning/REQUIREMENTS.md, 60-02-SUMMARY.md, 61-02-SUMMARY.md, 61-03-SUMMARY.md |

## What Was Built

**Task 1 — Functional fix (INT-01):**
- Added `search_video_performance_by_title(title_prefix)` as a public method on `KeywordDB` in `tools/discovery/database.py`. Uses parameterized LIKE query (first 40 chars, case-insensitive) with proper exception handling.
- Updated `_lookup_video_id()` in `tools/ctr_ingest.py` to delegate entirely to the new public method. Eliminated the `db._conn` private access and the unnecessary `.replace("'", "''")` (redundant with parameterized queries).
- Updated `.claude/commands/retitle.md` Step 4c to instantiate `KeywordDB()`, pass `_db.db_path` to `score_title()`, then call `_db.close()` — matching the exact pattern used in `greenlight.md` and `tools/preflight/scorer.py`.

**Task 2 — Documentation accuracy:**
- Added `requirements_completed` keys to frontmatter of 60-02-SUMMARY.md (RETITLE-04/05/06), 61-02-SUMMARY.md (GATE-03), and 61-03-SUMMARY.md (GATE-04/05).
- Updated REQUIREMENTS.md traceability table: changed all 24 v5.2 rows (DATA-01/02/03/04, CTR-01/02/03/04, SEO-01/02/03, GAP-01/02/03/04, RET-01/02/03/04, GROW-01/02/03/04/05) from "Not started" to "Complete".
- Checked all 24 v5.2 requirement checkboxes from `- [ ]` to `- [x]`.

## Verification Results

All 7 plan verification checks passed:
1. `pytest tests/integration/test_ctr_ingest.py -x` — 8 passed (behavior unchanged)
2. `grep "db._conn" tools/ctr_ingest.py` — zero matches
3. `grep "db_path" .claude/commands/retitle.md` — match found in Step 4c
4. `grep "search_video_performance_by_title" tools/discovery/database.py` — match found
5. `grep -c "Not started" .planning/REQUIREMENTS.md` — 0
6. `grep "requirements_completed"` in all 3 SUMMARY files — 1 match each

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- `tools/discovery/database.py` — FOUND: search_video_performance_by_title method
- `tools/ctr_ingest.py` — FOUND: delegates to public method, zero db._conn references
- `.claude/commands/retitle.md` — FOUND: db_path in Step 4c
- `.planning/REQUIREMENTS.md` — FOUND: zero "Not started" rows
- Commit 915e625 — FOUND
- Commit cf644d3 — FOUND
