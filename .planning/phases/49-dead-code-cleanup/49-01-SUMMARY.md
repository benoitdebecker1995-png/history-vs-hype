---
phase: 49-dead-code-cleanup
plan: 01
subsystem: tooling
tags: [dead-code, git, gitignore, cleanup, prompt_evaluation, youtube_analytics]

# Dependency graph
requires:
  - phase: 48-package-structure
    provides: Proper absolute imports; tools/youtube_analytics/ renamed from tools/youtube-analytics/
provides:
  - 7 untracked scratch files deleted from tools/youtube_analytics/
  - tools/prompt_evaluation.py removed (tracked, 953 lines)
  - .gitignore patterns blocking future re-tracking of scratch files and backup dirs
  - Skill files updated to reference script-writer-v2 instead of deleted prompt_evaluation.py
  - CLEAN-01 satisfied (dead file removal complete)
  - CLEAN-03 satisfied (pre-satisfied — zero datetime.utcnow() occurrences)
affects: [49-02-dead-code-cleanup, 50-error-handling, 51-logging-cli]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Untracked scratch files removed with rm (not git rm) — untracked files require filesystem deletion, not git staging"
    - "Tracked dead code removed with git rm — single command stages deletion and removes from working tree"
    - "Scoped .gitignore patterns (tools/youtube_analytics/_longform_*.json) preferred over broad patterns (_*.json) to avoid suppressing legitimate files"

key-files:
  created:
    - .planning/phases/49-dead-code-cleanup/49-01-SUMMARY.md
  modified:
    - .gitignore (3 new patterns for scratch files and backups dir)
    - .claude/skills/notebooklm-prompt-generator.md (line 666: voice check reference updated)
    - .claude/skills/script-reviewer.md (line 655: voice check reference updated)
  deleted:
    - tools/youtube_analytics/_csv_backfill.py (untracked scratch runner)
    - tools/youtube_analytics/_competitor_fetch.py (untracked competitor fetcher)
    - tools/youtube_analytics/_backfill_ids.txt (untracked ID list)
    - tools/youtube_analytics/_longform_all.json (untracked pre-fetch data)
    - tools/youtube_analytics/_longform_enriched.json (untracked pre-fetch data)
    - tools/youtube_analytics/_longform_ids.json (untracked pre-fetch data)
    - tools/youtube_analytics/_longform_metrics.json (untracked pre-fetch data)
    - tools/prompt_evaluation.py (tracked, 953 lines — prompt templates + heuristic scorer + Anthropic API runner)

key-decisions:
  - "prompt_evaluation.py deleted: zero Python callers, channel_voice_check CLI arg it advertised was never a real flag (just a dict key), references stale file paths from v3.0, superseded by script-writer-v2 (19 rules) + script_checkers/ + STYLE-GUIDE Part 6"
  - "Skill references updated to point to script-writer-v2 rather than removed script — avoids breaking production sessions that follow notebooklm-prompt-generator.md and script-reviewer.md integration steps"
  - "CLEAN-03 marked pre-satisfied: grep confirms zero datetime.utcnow() occurrences across codebase — migration to datetime.now(timezone.utc) already complete from prior phases"
  - "backups/ added to .gitignore (not deleted): database.py still writes to it during v27 schema migration for fresh installs; directory auto-creates on demand"

patterns-established:
  - "Dead file deletion pattern: rm for untracked, git rm for tracked; verify with git ls-files before choosing"
  - "Skill file maintenance: update .claude/skills/ references immediately when referenced tools are removed"

requirements-completed: [CLEAN-01, CLEAN-03]

# Metrics
duration: 3min
completed: 2026-02-25
---

# Phase 49 Plan 01: Dead Code Cleanup — File Deletion Summary

**8 dead files deleted (7 untracked scratch + 1 tracked stub), .gitignore hardened with 3 scoped patterns, skill files updated from stale prompt_evaluation.py references to script-writer-v2**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-25T13:56:02Z
- **Completed:** 2026-02-25T13:59:26Z
- **Tasks:** 2
- **Files deleted:** 8 | **Files modified:** 3

## Accomplishments

- Deleted 7 untracked scratch files from tools/youtube_analytics/ — git status is now clean of all backfill artifacts
- Deleted tools/prompt_evaluation.py (953 lines, tracked) — a standalone prompt evaluation suite with zero Python callers, stale file references, and a CLI flag that never existed
- Added 3 scoped .gitignore patterns: `tools/youtube_analytics/_longform_*.json`, `tools/youtube_analytics/_backfill_ids.txt`, `tools/discovery/backups/` — prevents future scratch file re-tracking
- Updated 2 skill files to redirect voice check from deleted prompt_evaluation.py to script-writer-v2 agent
- CLEAN-01 and CLEAN-03 requirements satisfied

## Task Commits

Each task was committed atomically:

1. **Task 1: Delete dead files and add .gitignore patterns** - `c2a45b5` (chore)
2. **Task 2: Assess and remove prompt_evaluation.py + clean skill references** - `bcbf1e5` (chore)

## Files Created/Modified

- `.gitignore` — Added 3 patterns: _longform_*.json, _backfill_ids.txt, tools/discovery/backups/
- `.claude/skills/notebooklm-prompt-generator.md` — Line 666: replaced stale `tools/prompt_evaluation.py channel_voice_check` with script-writer-v2 reference
- `.claude/skills/script-reviewer.md` — Line 655: same replacement

**Deleted (8 files):**
- `tools/youtube_analytics/_csv_backfill.py` — One-time backfill runner, never committed
- `tools/youtube_analytics/_competitor_fetch.py` — Manual competitor data fetcher, never committed
- `tools/youtube_analytics/_backfill_ids.txt` — Scratch ID list for _csv_backfill.py
- `tools/youtube_analytics/_longform_all.json` — Pre-fetch data (4 _longform JSON files total)
- `tools/youtube_analytics/_longform_enriched.json`
- `tools/youtube_analytics/_longform_ids.json`
- `tools/youtube_analytics/_longform_metrics.json`
- `tools/prompt_evaluation.py` — Prompt templates + heuristic scorer + Anthropic API runner (953 lines)

## Decisions Made

- **prompt_evaluation.py deleted** rather than kept: confirmed zero Python callers; the `channel_voice_check` CLI subcommand advertised in two skill files was never a real CLI argument — just a dict key in `VOICE_CHECK_PROMPTS`; references stale file paths (`SCRIPTWRITING-STYLE-GUIDE.md`, `CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md`) deleted in v3.0; functionality fully superseded by script-writer-v2 (19 rules), `tools/youtube_analytics/script_checkers/`, and STYLE-GUIDE Part 6
- **Skill files updated immediately** on deletion to prevent production sessions from trying to invoke a non-existent file
- **backups/ gitignored not deleted**: `database.py` `_backup_database()` and `_ensure_variant_tables()` still write there during v27 migration for fresh installs; adding to .gitignore is correct handling since production DB is already at v29

## Deviations from Plan

None — plan executed exactly as written. All findings confirmed the research assessment. prompt_evaluation.py was tracked (git rm was correct, not rm), as expected from research Finding 1 caveat.

## Issues Encountered

None. The 7 scratch files were correctly untracked (rm, not git rm). prompt_evaluation.py was correctly tracked (git rm). Import smoke tests passed on first attempt.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 49-02 can proceed: CLEAN-01 and CLEAN-03 are satisfied; CLEAN-02 (function-level dead code audit in patterns.py and database.py) is the remaining work
- Working tree is clean of all scratch backfill artifacts
- Active skill files no longer reference deleted modules

## Self-Check: PASSED

- FOUND: tools/youtube_analytics/_csv_backfill.py deleted (confirmed gone)
- FOUND: tools/prompt_evaluation.py deleted (confirmed gone)
- FOUND: .gitignore with backups pattern (confirmed present)
- FOUND: .planning/phases/49-dead-code-cleanup/49-01-SUMMARY.md (this file)
- FOUND: commit c2a45b5 — chore(49-01): delete 7 dead scratch files, add .gitignore patterns
- FOUND: commit bcbf1e5 — chore(49-01): remove prompt_evaluation.py, clean stale skill references
- V1 PASS: no dead _* files remain in youtube_analytics/
- V2 PASS: prompt_evaluation.py deleted
- V3 PASS: no prompt_evaluation refs in tools/ or .claude/skills/
- V4 PASS: no untracked files in youtube_analytics/
- V5 PASS: tools/discovery/backups/ pattern in .gitignore
- V6 PASS: youtube_analytics.backfill and discovery.database imports succeed

---
*Phase: 49-dead-code-cleanup*
*Completed: 2026-02-25*
