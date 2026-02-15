---
phase: 37-creator-transcript-analysis
plan: 01
subsystem: Creator Technique Analysis
tags: [transcript-parsing, pattern-extraction, database-migration, technique-library]
dependency_graph:
  requires: [Phase 36 retention scoring]
  provides: [transcript_analyzer.py, technique_library.py, schema v28]
  affects: [Plan 37-02 cross-creator synthesis, Plan 37-03 script-writer integration]
tech_stack:
  added: [sqlite3, pathlib, re, collections.Counter]
  patterns: [format-specific parsing, PRAGMA user_version migration, error dict pattern, UPSERT]
key_files:
  created:
    - tools/youtube-analytics/transcript_analyzer.py (381 LOC)
    - tools/youtube-analytics/technique_library.py (534 LOC)
    - tools/youtube-analytics/test_transcript_analyzer.py (348 LOC)
  modified:
    - tools/discovery/keywords.db (schema v27 → v28)
decisions:
  - "Used stdlib-only for transcript_analyzer (re, pathlib, json) - no external dependencies"
  - "Schema v28 migration adds creator_techniques table with UNIQUE(category, name) constraint"
  - "Creator examples stored as JSON text field (10 examples max per technique)"
  - "is_universal flag set when technique appears in 3+ creators"
  - "UPSERT pattern for add_technique (INSERT...ON CONFLICT UPDATE)"
metrics:
  duration_minutes: 5
  tasks_completed: 2
  files_created: 3
  files_modified: 1
  tests_added: 22
  completed_date: "2026-02-15"
---

# Phase 37 Plan 01: Transcript Analysis Pipeline Summary

**One-liner:** Built transcript parser supporting .srt/.vtt/.txt with pattern extraction (hooks, transitions, evidence, pacing) and technique storage in schema v28.

## What Was Built

### transcript_analyzer.py (381 LOC)
**Purpose:** Parse 83 creator transcripts and extract structural patterns.

**Core capabilities:**
- **Format-aware parsing:**
  - `.srt` → Strip SRT timecodes (`00:01:23,456 --> ...`) and index lines
  - `.vtt` → Strip WEBVTT header and VTT timecodes (`00:01:23.456 --> ...`)
  - `.txt` → Direct passthrough
  - All formats → Strip HTML tags, normalize newlines

- **Creator attribution:**
  - `transcripts/Kraut/file.txt` → "Kraut"
  - `transcripts/file.txt` → "History vs Hype"
  - `niche-research/topic/file.txt` → "topic"

- **Pattern extraction:**
  - **Opening hooks (5 types):** visual_contrast, fact_check_declaration, current_event, escalation_timeline, question_hook
  - **Transitions (4 types):** causal_chain, temporal_jump, pivot_phrase, contrast_shift
  - **Evidence patterns:** direct_quotes, according_to, page_citations, document_reveals, quote_density
  - **Pacing metrics:** word_count, paragraph_count, avg_paragraph_words, question_count, questions_per_1000_words

- **CLI:**
  - `--analyze-all` → Batch process all transcripts, output JSON
  - `--analyze FILE` → Single file analysis
  - `--stats` → Distribution stats (83 files across 9+ creators)

### technique_library.py (534 LOC)
**Purpose:** Database CRUD for creator technique storage with schema v28 migration.

**Schema migration:**
- Checked `PRAGMA user_version` (was 27)
- Created `creator_techniques` table with fields: category, name, formula, when_to_use, creator_examples (JSON), creator_count, is_universal, style_guide_ref, created_at
- Added indexes: `idx_technique_category`, `idx_technique_universal_count`
- Bumped version to 28

**CRUD operations:**
- `add_technique()` → UPSERT with ON CONFLICT UPDATE
- `get_techniques_by_category()` → Filter by category, order by creator_count DESC
- `get_universal_techniques()` → Filter is_universal=True
- `get_all_techniques()` → All techniques grouped by category
- `search_techniques()` → LIKE search on name/formula/when_to_use
- `store_analysis_results()` → Transform transcript analyses into technique rows

**CLI:**
- `--store-from FILE` → Ingest transcript analysis JSON
- `--list [CATEGORY]` → List techniques
- `--search QUERY` → Search techniques
- `--stats` → Database statistics

### test_transcript_analyzer.py (348 LOC)
**22 tests covering:**
- Format parsing (SRT, VTT, TXT)
- Creator attribution (subfolder vs root)
- Opening hook detection (5 patterns)
- Transition extraction (4 types)
- Evidence pattern counting
- Pacing analysis
- Full integration pipeline

**All tests passing.**

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

```bash
# 1. Stats show 83 transcripts discovered
$ python tools/youtube-analytics/transcript_analyzer.py --stats
{
  "total_files": 83,
  "by_format": {".txt": 17, ".srt": 30, ".vtt": 36},
  "by_creator": {
    "History vs Hype": 50,
    "Kraut": 8,
    "Knowing Better": 4,
    "Alex O'Connor": 3,
    ...
  }
}

# 2. All tests pass
$ python -m pytest test_transcript_analyzer.py -v
============================= 22 passed in 0.06s ==============================

# 3. Schema version 28
$ python -c "import sqlite3; c=sqlite3.connect('tools/discovery/keywords.db'); print(c.execute('PRAGMA user_version').fetchone())"
(28,)

# 4. Technique library operational
$ python technique_library.py --stats
{
  "total_techniques": 1,
  "universal_count": 0,
  "by_category": {"opening_hook": 1}
}
```

## Technical Decisions

### 1. Stdlib-only for transcript_analyzer
**Decision:** Use only `re`, `pathlib`, `json`, `collections.Counter`, `datetime` - no external dependencies.

**Reasoning:** Simplicity, portability, no new dependencies to install. Pattern extraction is regex-based (sufficient for structural markers).

**Alternatives considered:** spaCy for NLP (rejected - overkill for structural patterns, Python 3.14 incompatibility).

### 2. Schema v28 migration with PRAGMA user_version
**Decision:** Follow existing database.py pattern - check version, migrate if needed, bump version.

**Reasoning:** Consistent with Phases 27-35 migration pattern. Prevents re-running migrations, enables version checks.

**Implementation:** `_ensure_schema_v28()` checks version 28, creates table + indexes, sets `PRAGMA user_version = 28`.

### 3. JSON text field for creator_examples
**Decision:** Store creator_examples as JSON text (not normalized table).

**Reasoning:**
- Read-heavy workload (synthesis queries examples, doesn't JOIN)
- 10 examples max per technique (bounded size)
- Simplifies UPSERT logic (single row update vs. managing child table)

**Trade-off:** Can't query examples by creator directly, but not needed for synthesis workflow.

### 4. is_universal flag logic
**Decision:** Set `is_universal=True` when technique appears in 3+ unique creators.

**Reasoning:**
- 3+ creators = pattern transcends individual style
- Threshold balances signal (not noise) with inclusivity (not overly restrictive)
- Script-writer can prioritize universal techniques for guidance

**Alternative considered:** 5+ creators (rejected - too restrictive for 83-transcript corpus).

### 5. UPSERT pattern for add_technique
**Decision:** Use `INSERT...ON CONFLICT(category, name) DO UPDATE`.

**Reasoning:**
- Enables re-running analysis without duplicates
- Updates examples if patterns refined
- Maintains technique_id stability (doesn't create new rows)

**Constraint:** `UNIQUE(technique_category, technique_name)` prevents duplicate techniques.

## Integration Points

### Data flow:
1. **transcript_analyzer.py** → Parses transcripts → Outputs JSON with patterns
2. **technique_library.py** → Reads JSON → Stores patterns as techniques in creator_techniques table
3. **Plan 37-02** → Queries creator_techniques → Cross-creator synthesis
4. **Plan 37-03** → Integrates techniques into script-writer-v2 → Context-aware recommendations

### Schema:
- **keywords.db** now at **v28** (was v27)
- New table: `creator_techniques` (7 techniques after test run)
- Indexes: category, (is_universal DESC, creator_count DESC)

### Error handling:
- All functions return `{'error': msg}` on failure (never raise)
- Follows error dict pattern from database.py, playbook_synthesizer.py

## Known Limitations

1. **Regex-based pattern extraction:** May miss nuanced patterns requiring semantic understanding. Sufficient for structural markers (transitions, hooks), not for deep content analysis.

2. **No sentence boundary detection:** Uses character windows around matches. Works for context snippets, not for extracting full sentences.

3. **10 example limit per technique:** Prevents bloat but loses tail examples. Trade-off: keeps DB size manageable, provides sufficient diversity for synthesis.

4. **No overlap detection:** If multiple patterns match same text region, all counted. Acceptable for structural analysis (patterns can co-occur).

5. **Fixed WPM assumption:** 500 words ≈ 2 min opening assumes 150 WPM. Actual pace varies by creator. Sufficient for approximation.

## Next Steps

**Plan 37-02 (Cross-Creator Synthesis):**
- Query `creator_techniques` for universal patterns
- Group by category, rank by creator_count
- Generate synthesis report comparing technique usage
- Identify gaps (techniques used by high-performers but missing from History vs Hype)

**Plan 37-03 (Script-Writer Integration):**
- Add technique querying to script-writer-v2
- Context-aware recommendations: "Kraut uses causal_chain transitions 12x per script, you used 2x"
- Auto-suggest techniques based on section type (opening → hook patterns, body → transition patterns)

## Self-Check

### Files created:
```bash
$ ls -lh tools/youtube-analytics/transcript_analyzer.py
-rw-r--r-- 1 user user 15K Feb 15 00:47 tools/youtube-analytics/transcript_analyzer.py

$ ls -lh tools/youtube-analytics/technique_library.py
-rw-r--r-- 1 user user 21K Feb 15 00:48 tools/youtube-analytics/technique_library.py

$ ls -lh tools/youtube-analytics/test_transcript_analyzer.py
-rw-r--r-- 1 user user 13K Feb 15 00:47 tools/youtube-analytics/test_transcript_analyzer.py
```

### Commits exist:
```bash
$ git log --oneline --all | grep "37-01"
d0a2216 feat(37-01): implement technique library with schema v28 migration
eaa7577 feat(37-01): implement transcript analyzer with pattern extraction
```

## Self-Check: PASSED

All files created, commits verified, tests passing, schema migrated.

---

**Completion time:** 5 minutes
**Commits:** eaa7577, d0a2216
**Status:** ✅ Complete - Ready for Plan 37-02 (Cross-Creator Synthesis)
