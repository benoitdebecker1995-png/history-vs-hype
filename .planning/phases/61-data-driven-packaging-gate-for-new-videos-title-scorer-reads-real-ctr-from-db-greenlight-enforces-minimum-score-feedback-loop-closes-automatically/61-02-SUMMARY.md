---
phase: 61-data-driven-packaging-gate
plan: 02
subsystem: tools
tags: [ctr-ingest, database, integration-test, tdd]
requirements_completed: [GATE-03]
dependency_graph:
  requires:
    - tools/retitle_audit.py (_parse_synthesis_table)
    - tools/discovery/database.py (KeywordDB.add_ctr_snapshot)
    - channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md (data source)
  provides:
    - tools/ctr_ingest.py (CTR ingestion CLI + library function)
    - tests/integration/test_ctr_ingest.py (integration test suite)
  affects:
    - tools/discovery/keywords.db (ctr_snapshots table populated)
tech_stack:
  added: []
  patterns:
    - TDD (RED → GREEN cycle)
    - error-dict return pattern (matches existing tools/)
    - case-insensitive LIKE title matching for fuzzy resolution
    - dry-run flag for safe preview before mutation
key_files:
  created:
    - tools/ctr_ingest.py
    - tests/integration/test_ctr_ingest.py
    - tests/integration/__init__.py
  modified: []
decisions:
  - "Title matching uses LIKE on first 40 chars — synthesis table uses descriptive titles, video_performance stores YouTube API titles; no hard join possible"
  - "is_late_entry=True and snapshot_date=2026-02-23 for all ingest rows — marks historical backfill clearly"
  - "dry_run parameter added to ingest_synthesis_ctr() — not in original spec but required for safe production use"
  - "Unmatched titles logged at WARNING (not ERROR) — expected for videos not yet in video_performance"
metrics:
  duration: "~2 minutes"
  completed: "2026-03-14"
  tasks_completed: 1
  tasks_total: 1
  files_created: 3
  files_modified: 0
---

# Phase 61 Plan 02: CTR Ingest Summary

**One-liner:** CTR ingestion CLI that reads CROSS-VIDEO-SYNTHESIS.md, resolves video_ids via fuzzy title matching, and writes historical CTR snapshots to keywords.db with dry-run support.

## What Was Built

`tools/ctr_ingest.py` — a library + CLI that bridges the manually-maintained synthesis table to the database.

**Core function:**

```python
ingest_synthesis_ctr(synthesis_path: Path, db: KeywordDB, dry_run: bool = False) -> dict
# Returns: {'written': int, 'skipped': int, 'unmatched': int, 'errors': list, 'would_write': int}
```

**Key design choices:**

1. **Reuses `_parse_synthesis_table`** from `tools/retitle_audit.py` — no duplicate parsing logic
2. **Title matching** uses `LIKE '%{prefix}%' COLLATE NOCASE` on first 40 chars — handles minor formatting differences between the synthesis descriptive titles and YouTube API titles
3. **`dry_run=True`** skips all writes and returns `would_write` count — added beyond spec for safe production use
4. **`snapshot_date=2026-02-23`** and `is_late_entry=True` mark all ingested rows as historical backfill

**CLI flags:** `--synthesis`, `--dry-run`, `--verbose`, `--quiet`

## Test Results

8 integration tests in `tests/integration/test_ctr_ingest.py` — all pass:

- Correct row count written (3 of 5 fixture videos with CTR + title match)
- Skipped count for n/a CTR entries
- Unmatched count for titles not in video_performance
- Result dict has required keys
- Idempotent: no crash on second run
- CTR values match synthesis table (4.31% for VID001)
- Dry-run writes zero rows

## Real Data Smoke Test (--dry-run)

Against real CROSS-VIDEO-SYNTHESIS.md and keywords.db:
- Would write: 2 (2 titles matched video_performance)
- Skipped: 3 (Vichy/Operation Ajax rows with TBD/n/a CTR)
- Unmatched: 30 (synthesis uses descriptive titles; video_performance has YouTube API titles)

The 30 unmatched entries are expected — the synthesis table was written with human-readable descriptive names. The tool logs each unmatched title at WARNING level so the user can see exactly which videos need video_performance entries.

## Deviations from Plan

### Auto-added Missing Functionality

**1. [Rule 2 - Missing Feature] Added dry_run parameter**
- **Found during:** Implementation
- **Issue:** Plan spec only described basic ingest; no preview mode before mutating production DB
- **Fix:** Added `dry_run=True` parameter that skips writes, returns `would_write` count, and logs what would happen
- **Files modified:** tools/ctr_ingest.py
- **Commit:** bd410d5

## Self-Check

- [x] `tools/ctr_ingest.py` exists (confirmed)
- [x] `tests/integration/test_ctr_ingest.py` exists (confirmed)
- [x] Integration tests pass: 8 passed
- [x] Dry-run smoke test works against real data
- [x] Commits: e452692 (test RED), bd410d5 (feat GREEN)
