---
phase: 35-actionable-analytics
plan: 03
subsystem: youtube-analytics
tags: [integration, command-update, retention-diagnostics, pre-script-insights]
dependency_graph:
  requires:
    - 35-01-retention-mapper
    - 35-02-topic-strategy
  provides:
    - section-diagnostics-in-analyze
    - pre-script-intelligence-in-script
  affects:
    - analyze-command
    - script-command
tech_stack:
  added: []
  patterns: [cli-integration, optional-imports, graceful-fallback]
key_files:
  created: []
  modified:
    - tools/youtube-analytics/analyze.py
    - .claude/commands/analyze.md
    - .claude/commands/script.md
decisions:
  - "Use optional --script flag for section diagnostics (backward compatible)"
  - "Import retention_mapper and section_diagnostics with DIAGNOSTICS_AVAILABLE flag"
  - "Insert section diagnostics before Feedback Insights section in markdown output"
  - "Use get_pre_script_insights() function for /script pre-intelligence"
  - "Display pre-script insights automatically before script generation begins"
metrics:
  duration_minutes: 3
  completed_date: 2026-02-11
  tasks_completed: 3
  files_modified: 3
  loc_added: 127
  loc_modified: 96
---

# Phase 35 Plan 03: Command Integration Summary

Wire retention mapper, section diagnostics, and pre-script insights into /analyze and /script commands — completing Actionable Analytics.

## One-Liner

Connected Phase 35 intelligence modules (retention mapping, diagnostics, topic strategy) to user-facing commands with optional --script flag and automatic pre-script insights.

## What Was Built

### Task 1: Extended analyze.py with Section Diagnostics

**File:** `tools/youtube-analytics/analyze.py`

**Added:**
- `generate_section_diagnostics(video_id, script_path)` function
  - Imports retention_mapper and section_diagnostics with try/except
  - Imports ScriptParser from production/parser.py
  - Gets retention data and finds drop-off points
  - Parses script sections and maps drops to sections
  - Generates diagnostics with root causes and recommendations
  - Returns dict with status/error pattern
- `DIAGNOSTICS_AVAILABLE` feature flag for graceful imports
- `--script PATH` CLI argument
- Integration into main analysis workflow
- Section diagnostics output in `format_analysis_markdown()`
  - Retention Drop Map table
  - Diagnostics with root causes and pattern recommendations
  - Inserted before Feedback Insights section

**Error handling:**
- Missing script file → warning, skip diagnostics
- No retention data → warning, skip diagnostics
- Import errors → set DIAGNOSTICS_AVAILABLE=False, skip silently
- Existing analyze behavior unchanged when --script omitted

**Commit:** `3edc5aa`

### Task 2: Updated /analyze Command Documentation

**File:** `.claude/commands/analyze.md`

**Added:**
- `--script PATH` to usage and flags table
- New section: "SECTION-LEVEL RETENTION DIAGNOSTICS (`--script`)"
  - How it works (5-step process)
  - Output description (Retention Drop Map + Section Diagnostics)
  - Requirements (retention data + markdown script with H2 headings)
  - Example usage
  - Anti-patterns detected (6 types)
- Updated example commands with --script flag

**Commit:** `1899527`

### Task 3: Updated /script Command with Pre-Script Intelligence

**File:** `.claude/commands/script.md`

**Changes:**
- Replaced "Feedback Insights (Automatic)" with comprehensive "PRE-SCRIPT INTELLIGENCE" section
  - Automatic display details (topic performance, retention lessons, suggested patterns)
  - How to use insights (concrete examples)
  - Technical details (feedback_queries.py, topic_strategy.py, keywords.db)
  - Requirements (feedback.py backfill)
  - Implementation details for Claude (get_pre_script_insights call)
- Added "Workflow Steps" subsection under "Write the Script"
  - Step 1: Surface pre-script intelligence (automatic)
  - Step 2: Gather information and context
  - Step 3: Generate script

**Commit:** `61f9ed5`

## Integration Points

### analyze.py → retention_mapper → section_diagnostics
- `generate_section_diagnostics()` orchestrates full pipeline
- `map_retention_to_sections()` maps drops to script sections
- `diagnose_all_drops()` generates recommendations
- `format_diagnostics_markdown()` formats output

### script.md → feedback_queries → topic_strategy
- `get_pre_script_insights(topic_type)` fetches past lessons
- `generate_topic_strategy()` aggregates performance by topic
- Automatic display before script generation begins

## Deviations from Plan

None - plan executed exactly as written.

## What Works

### Section Diagnostics Integration

```bash
python tools/youtube-analytics/analyze.py VIDEO_ID --script path/to/script.md --save
```

Output includes:
- Standard POST-PUBLISH-ANALYSIS sections (unchanged)
- **New:** Section-Level Retention Analysis
  - Retention Drop Map table (sorted by severity)
  - Diagnostics by section (root causes + recommended patterns)
- Feedback Insights (existing)

### Pre-Script Intelligence

When user runs `/script`, Claude automatically:
1. Detects topic type from user input
2. Calls `get_pre_script_insights(topic_type)`
3. Displays intelligence block before script generation
4. Uses insights to inform structure decisions

No user action required - fully automatic.

## Self-Check: PASSED

### Verify Files Modified

```
[FOUND] tools/youtube-analytics/analyze.py
[FOUND] .claude/commands/analyze.md
[FOUND] .claude/commands/script.md
```

### Verify Commits Exist

```
[FOUND] 3edc5aa - feat(35-03): extend analyze.py with section-level retention diagnostics
[FOUND] 1899527 - docs(35-03): update /analyze command with --script flag documentation
[FOUND] 61f9ed5 - docs(35-03): update /script command with pre-script intelligence surfacing
```

### Verify Functionality Added

```
[FOUND] generate_section_diagnostics function in analyze.py
[FOUND] DIAGNOSTICS_AVAILABLE flag in analyze.py
[FOUND] --script CLI argument parsing
[FOUND] "SECTION-LEVEL RETENTION DIAGNOSTICS" section in analyze.md
[FOUND] "PRE-SCRIPT INTELLIGENCE" section in script.md
[FOUND] "Workflow Steps" subsection in script.md
```

All checks passed.

## Lessons Learned

**Pattern: Optional imports with feature flags**
- DIAGNOSTICS_AVAILABLE pattern allows graceful degradation
- analyze.py works without Phase 35 modules installed
- No breaking changes to existing functionality

**Pattern: Backward-compatible CLI extension**
- --script is optional flag, doesn't change default behavior
- Existing analyze.py usage unchanged
- Users opt-in to new diagnostics feature

**Pattern: Automatic intelligence surfacing**
- Pre-script insights surface automatically (no user flag needed)
- Skip silently if no data available (non-blocking)
- Intelligence informs script generation without requiring explicit action

## Next Steps

**For user:**
1. Run `/analyze VIDEO_ID --script path/to/script.md` on published videos
2. Review section diagnostics for retention drop patterns
3. Use pre-script insights when running `/script` for new videos
4. Backfill feedback data: `python tools/youtube-analytics/feedback.py backfill`

**For future work:**
- Phase 35 complete — v2.0 Channel Intelligence milestone complete
- Next milestone (if any): TBD via `/gsd:new-milestone`
