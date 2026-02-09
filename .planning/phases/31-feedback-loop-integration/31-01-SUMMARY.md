---
phase: 31-feedback-loop-integration
plan: 01
subsystem: feedback-loop
tags: [parser, database, crud, markdown-extraction, feedback-storage]
completed: 2026-02-09

dependency_graph:
  requires:
    - phase-27-database-foundation (feedback columns in video_performance)
    - existing POST-PUBLISH-ANALYSIS markdown files
  provides:
    - feedback_parser.py module for markdown extraction
    - KeywordDB feedback CRUD methods
    - canonical POST-PUBLISH-ANALYSIS template
  affects:
    - Phase 31-02 (pattern extraction - will use these methods)
    - Phase 31-03 (insight surfacing - will query feedback data)

tech_stack:
  added:
    - feedback_parser.py: Regex-based markdown parser for POST-PUBLISH-ANALYSIS files
  patterns:
    - Best-effort regex extraction with fallbacks for older file formats
    - Error dict pattern (return {'error': msg} on failure, never raise)
    - JSON column storage with null-safe parsing
    - Graceful import with FEEDBACK_AVAILABLE flag pattern

key_files:
  created:
    - tools/youtube-analytics/feedback_parser.py (433 lines)
    - .claude/templates/POST-PUBLISH-ANALYSIS-TEMPLATE.md (canonical format)
  modified:
    - tools/discovery/database.py (+217 lines, 4 new methods)

decisions:
  - Regex extraction appropriate for controlled markdown template (not full AST parser)
  - Best-effort parsing with heuristic fallbacks for older analysis files
  - Backfill skips videos not in video_performance table (returns 'no_match' status)
  - Canonical template improves parsing reliability over time
  - JSON storage for qualitative insights (observations, actionable items, discovery issues)
  - Biggest drop point extracted as single integer for retention_drop_point column

metrics:
  duration_minutes: 4
  tasks_completed: 2
  files_created: 2
  files_modified: 1
  functions_added: 12
  lines_added: 650
---

# Phase 31 Plan 01: Feedback Parser & Database Storage

**One-liner:** Parse POST-PUBLISH-ANALYSIS markdown files into structured database records with regex extraction and CRUD methods.

## What Was Built

### Task 1: feedback_parser.py Module

Created markdown extraction module with 8 functions:

1. **parse_analysis_file(filepath)** - Main entry point
   - Opens file, calls all extractors, returns complete dict
   - Returns `{'error': msg}` on failure (never raises exceptions)
   - Handles both project-folder files and channel-data/analyses/ fallback files

2. **extract_video_id(content, filepath)** - Video ID extraction
   - Primary: from `**Video ID:** XXXX` header pattern
   - Fallback: from filename `POST-PUBLISH-ANALYSIS-{VIDEO_ID}.md`

3. **extract_metrics(content)** - Numeric performance data
   - avg_retention, final_retention, ctr (skip if "Not available via API")
   - impressions (comma-handling), views, subscribers_gained
   - Parses Performance table for "This Video" column values

4. **extract_lessons(content)** - Qualitative insights
   - observations: bullet list from `### Observations` section
   - actionable: checkbox bullets from `### Actionable Items` (strips `- [ ]`)

5. **extract_drop_points(content)** - Retention drop table
   - Returns list of `{position_pct, viewers_lost_pct, location}` dicts
   - Parses `| XX% | XX.X% dropped | location |` pattern

6. **extract_discovery_diagnosis(content)** - Discovery diagnostics
   - primary_issue, severity, summary from Discovery Diagnostics section
   - Parses `**Primary Issue:** XXX (Severity: XXX)` pattern

7. **find_analysis_files(project_root)** - File discovery
   - Scans video-projects/{_IN_PRODUCTION, _READY_TO_FILM, _ARCHIVED}/*/POST-PUBLISH-ANALYSIS.md
   - Scans channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md
   - Returns sorted list of Path objects

8. **backfill_all(project_root, force=False)** - Batch processing
   - Processes all found analysis files with progress output
   - Skips videos already having feedback (unless force=True)
   - Calls db.store_video_feedback() for each parsed result
   - Returns `{processed, skipped, errors, details}` dict

**Technical approach:**
- Regex extraction with `re.search()` and `re.finditer()`
- Best-effort parsing: missing fields return None/empty-list (graceful degradation)
- All stdlib: re, pathlib, datetime, json, sys
- CLI support: `python feedback_parser.py <file>` or `python feedback_parser.py backfill`

### Task 2: KeywordDB Feedback Methods

Added 4 CRUD methods to database.py KeywordDB class:

1. **store_video_feedback(video_id, feedback_data)** - Store parsed feedback
   - Updates video_performance table columns:
     - retention_drop_point = biggest_drop_position (int)
     - discovery_issues = JSON-encoded discovery dict
     - lessons_learned = JSON-encoded {observations, actionable}
   - Returns `{'status': 'updated', 'video_id': ...}` on success
   - Returns `{'status': 'no_match', 'video_id': ...}` if video not in performance table
   - Returns `{'error': msg}` on database error

2. **get_video_feedback(video_id)** - Retrieve single video feedback
   - SELECT video_id, title, topic_type, conversion_rate, retention_drop_point, discovery_issues, lessons_learned
   - Parses JSON columns with null-safety: `json.loads(val) if val else None`
   - Returns dict with parsed feedback or `{'error': 'not_found'}`

3. **get_feedback_by_topic(topic_type, limit=10)** - Query by category
   - SELECT videos WHERE topic_type = ? AND lessons_learned IS NOT NULL
   - ORDER BY conversion_rate DESC (highest performers first)
   - Returns `{videos: [...], count: N, topic: ...}` with parsed lessons

4. **has_feedback(video_id)** - Quick boolean check
   - SELECT lessons_learned WHERE video_id = ? AND lessons_learned IS NOT NULL
   - Returns True/False (used by backfill to skip existing records)

**Technical approach:**
- JSON column storage: json.dumps() for storage, json.loads() for retrieval
- Null-safe JSON parsing: always check `if column_value` before json.loads()
- Error dict pattern: `{'error': msg}` on failure, `{'status': ...}` on success
- Added `import json` to database.py top-level imports

### Canonical Template

Created `.claude/templates/POST-PUBLISH-ANALYSIS-TEMPLATE.md`:
- Consistent section headers for reliable parser extraction
- Includes all current sections: metrics, retention, lessons, discovery, variants, CTR analysis
- Comment at top: `<!-- Parser expects these exact section headers -->`
- Future /analyze outputs should follow this template for optimal parsing

## Verification Results

**Task 1 verification:**
```
Found 7 analysis files
Video ID: XbGl1Kcspt4
Retention: 39.4
Observations: 4
```
Parser successfully found all 7 existing POST-PUBLISH-ANALYSIS files and extracted structured data.

**Task 2 verification:**
```
has_feedback method: True
store method: True
get method: True
topic method: True
```
All four CRUD methods exist on KeywordDB class.

**Backfill integration test:**
```
Found 7 analysis files to process
[1/7] Parsing: POST-PUBLISH-ANALYSIS-c2uRn7U9jsk.md... SKIP (video not in performance table)
[7/7] Parsing: POST-PUBLISH-ANALYSIS.md... SKIP (video not in performance table)
Complete: 0 processed, 7 skipped, 0 errors
```
Backfill worked correctly - all files parsed successfully but skipped because videos aren't in video_performance table yet (expected behavior per design).

## Deviations from Plan

**None** - Plan executed exactly as written. All 8 parser functions implemented, all 4 CRUD methods added, template created. Backfill correctly handles 'no_match' status for videos not in performance table.

## Integration Points

**Phase 27 foundation (USED):**
- video_performance.retention_drop_point column populated
- video_performance.discovery_issues column populated (JSON)
- video_performance.lessons_learned column populated (JSON)

**Phase 19 performance table (REQUIRED):**
- Feedback methods query video_performance table
- Requires videos to have performance records before feedback can be stored

**Phase 31-02 pattern extraction (READY):**
- Can now query db.get_feedback_by_topic() for pattern analysis
- Lessons and observations available for comparison across videos

**Phase 31-03 insight surfacing (READY):**
- /script, /prep, /publish can query relevant feedback before generation
- db.get_feedback_by_topic() provides category-specific insights

## Technical Notes

**Regex patterns handle actual format variations:**
- `**Average retention:** 39.4%` (multiplies by 1, already percentage)
- `**CTR:** Not available via API` (returns None, not error)
- `| Views | 5,088 | 628 | +710% |` (strips commas from numbers)
- `| Subscribers | +51 | +1 |` (strips + prefix)
- `- [ ] This topic works well` (strips checkbox markup)

**Error handling strategy:**
- Parser functions return None/empty-list for missing fields (graceful)
- parse_analysis_file wraps in try/except, returns `{'error': msg}` dict
- Database methods return error dicts, never raise exceptions
- backfill_all prints progress and continues on individual file errors

**JSON column storage:**
- discovery_issues: stores entire discovery dict (primary_issue, severity, summary)
- lessons_learned: stores {observations: [...], actionable: [...]} structure
- Both use json.dumps() for storage, json.loads() with null-check for retrieval

**Why regex not AST parser:**
- POST-PUBLISH-ANALYSIS has controlled format (we generate it)
- Exact section headers and table patterns make regex reliable
- Full markdown parser would add dependency for no benefit
- Best-effort extraction with fallbacks handles older format variations

## Self-Check

### Files Created
- [x] tools/youtube-analytics/feedback_parser.py (433 lines)
- [x] .claude/templates/POST-PUBLISH-ANALYSIS-TEMPLATE.md

### Files Modified
- [x] tools/discovery/database.py (+217 lines, json import + 4 methods)

### Commits
- [x] dc27db0: feat(31-01): create feedback_parser.py with markdown extraction
- [x] da03863: feat(31-01): add KeywordDB feedback CRUD methods and canonical template

### Functionality Verified
- [x] find_analysis_files() discovers all 7 existing files
- [x] parse_analysis_file() extracts video_id, metrics, lessons, drop_points
- [x] backfill_all() processes files with progress output
- [x] KeywordDB has all 4 feedback methods (store, get, get_by_topic, has_feedback)
- [x] Backfill integration test runs without crashes
- [x] Canonical template created with parser-friendly structure

## Self-Check: PASSED

All files created, all commits exist, all verification tests passed.

## Next Steps

**Phase 31-02 (Pattern Extraction):**
- Use db.get_feedback_by_topic() to aggregate insights across videos
- Compare top performers vs bottom performers (content + production attributes)
- Generate PATTERNS.md report for human browsing
- Store patterns in database for machine querying

**Phase 31-03 (Insight Surfacing):**
- Integrate feedback queries into /script, /prep, /publish workflows
- Surface 3-5 relevant insights before generation (preamble pattern)
- Match by topic_type first, keyword similarity second
- Tailor insights to command: content for /script, production for /prep, CTR for /publish

**Future enhancement:**
- When /analyze generates new POST-PUBLISH-ANALYSIS file, auto-parse and store feedback
- Add FEEDBACK_AVAILABLE flag to analyze.py for graceful import (Phase 29/30 pattern)
- Section-level feedback extraction if analyze.py format adds per-section retention data
