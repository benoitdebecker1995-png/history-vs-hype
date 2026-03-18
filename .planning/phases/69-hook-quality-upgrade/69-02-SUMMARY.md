---
phase: 69-hook-quality-upgrade
plan: "02"
subsystem: script-command
tags: [script-command, hook-scorer, title-fulfillment, style-recommendation, document-reveal]
dependency_graph:
  requires: [tools.research.hook_scorer.score_hook, tools.research.hook_scorer.rank_hooks, tools.research.hook_scorer.format_hook_ranking, tools.research.hook_scorer.detect_topic_from_script]
  provides: [/script --hooks (upgraded)]
  affects: [user-facing /script --hooks workflow]
tech_stack:
  added: []
  patterns: [LLM-generated variants via Document Reveal framework, title-fulfillment display, style recommendation banner, urgency thresholds]
key_files:
  created: []
  modified:
    - .claude/commands/script.md
decisions:
  - "--title flag is optional: omitting it skips fulfillment check silently (no error)"
  - "Urgency thresholds: score>=70 AND fulfillment pass = LOW; score>=50 OR fail = MEDIUM; score<50 = HIGH"
  - "Fulfillment displayed outside the 100-pt table per Plan 01 decision (not added to total)"
  - "Variant count is proportional to script material (3-5 typical), not fixed at 5"
  - "Output is spoken text only — NO [VISUAL]/[AUDIO]/[B-ROLL] cues in generated variants"
metrics:
  duration_minutes: 8
  completed_date: "2026-03-18"
  tasks_completed: 1
  files_created: 0
  files_modified: 1
  tests_added: 0
  tests_passing: 0
requirements_satisfied: [HOOK-01, HOOK-02]
---

# Phase 69 Plan 02: Hook Quality Upgrade — Command Integration Summary

**One-liner:** /script --hooks rewritten with LLM-generated Document Reveal variants (not template-based), style recommendation banner before scores, title-fulfillment pass/fail display, urgency thresholds, and auto-scored ranked comparison table with Framework + Fulfillment columns.

## What Was Built

### Task 1: Rewrite --hooks section

**File modified:** `.claude/commands/script.md`

**Changes:**

1. **Flags table** — Added `--title "Title Text"` flag row. Documents that omitting `--title` silently skips the fulfillment check. Updated `--hooks` row description to match new flow.

2. **Process section** — Complete rewrite from template-based to LLM-driven flow:
   - Step 1: Read SCRIPT.md, extract first ~300 spoken words via `strip_for_teleprompter()`
   - Step 2: Auto-detect topic type via `detect_topic_from_script(clean_text)` (overridable with `--topic`)
   - Step 3: Score existing hook with `score_hook(existing_hook, label='Current Hook', title=title, topic_type=topic_type)`
   - Step 4: Style recommendation banner displayed FIRST (topic type → recommended style, confidence, examples)
   - Step 5: Existing hook score table (Framework/Pattern/Authority/Gap dimensions, then Fulfillment block separately)
   - Step 6: Urgency thresholds (LOW/MEDIUM/HIGH based on score + fulfillment)
   - Step 7: LLM variant generation guidance — Document Reveal layers (anomaly → stakes → inciting incident), brand voice ("Forensic, intelligent, skeptical. Bureaucratic Horror."), spoken text only
   - Step 8: Auto-score each variant via `rank_hooks(hooks, title=title, topic_type=topic_type)`
   - Step 9: Ranked comparison table with Framework column (not Beats) and Fulfillment E:Y/N P:Y/N

3. **Scoring Criteria table** — Updated from 4-row "Beat completeness" table to 6-row table:
   - Framework (40) — Anomaly + stakes + inciting incident (Document Reveal)
   - Pattern match (30)
   - Authority signal (15)
   - Information gap (15)
   - Style modifier (+/-5, HIGH confidence only)
   - Fulfillment (PASS/FAIL, displayed separately, NOT in 100-pt score)

4. **Example output** — Updated to show style recommendation banner, fulfillment PASS/FAIL display, ranked table with Framework and E:Y/N P:Y/N columns.

5. **After Selection section** — Kept. Updated prompt numbering (1/2/3 not A/B/C/D/E) to match new ranked table format.

6. **All other sections untouched** — --new, --revise, --review, --teleprompter, --document-mode, --variants are unchanged.

## Verification

All plan verification criteria passed:

1. `grep -c "fulfillment" .claude/commands/script.md` → 11 (fulfillment documented throughout)
2. `grep -c "Framework" .claude/commands/script.md` → 7 (Framework column, not Beats)
3. `grep "detect_topic_from_script" .claude/commands/script.md` → topic auto-detection wired in (2 occurrences)
4. `grep "Document Reveal" .claude/commands/script.md` → framework generation guidance present (2 occurrences)
5. `grep -c "\-\-title" .claude/commands/script.md` → 4 occurrences (flags table + examples)
6. Old "Beat completeness" / "4/4" references removed — 0 occurrences
7. Brand voice ("Forensic, intelligent, skeptical. Bureaucratic Horror.") present
8. Urgency thresholds (LOW/MEDIUM/HIGH) documented as table

## Deviations from Plan

None — plan executed exactly as written.

## Commits

| Task | Commit | Message |
|------|--------|---------|
| Task 1 | 2906afd | feat(69-02): rewrite --hooks section with LLM variants, fulfillment display, style banner |

## Self-Check: PASSED

- `.claude/commands/script.md` modified (189 insertions, 8 deletions)
- Commit 2906afd confirmed in git log
- All verification grep checks passed
- No other sections of script.md touched (diff shows changes only in flags table + --hooks section)
