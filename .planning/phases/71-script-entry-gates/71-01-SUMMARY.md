---
phase: 71-script-entry-gates
plan: "01"
subsystem: script-command
tags: [quality-gates, script, verification, structure-check]
dependency_graph:
  requires: []
  provides: [research-verification-gate, auto-structure-check]
  affects: [.claude/commands/script.md]
tech_stack:
  added: []
  patterns: [gate-before-generation, graceful-degradation, agent-auto-invocation]
key_files:
  created: []
  modified:
    - .claude/commands/script.md
decisions:
  - "Gate applies only to --new and default modes; --revise/--review/--teleprompter/--hooks/--collaborate bypass it to avoid blocking work on existing scripts"
  - "Missing 01-VERIFIED-RESEARCH.md emits a warning and proceeds (no block) — gate only runs when file exists"
  - "Structure check placed after Retention Prediction, before Format Template Selection, so it runs in the post-generation review flow"
  - "CRITICAL findings are flagged with explicit message but do not hard-block — user can acknowledge and proceed"
metrics:
  duration_seconds: 86
  tasks_completed: 2
  files_modified: 1
  completed_date: "2026-04-15"
requirements_fulfilled:
  - GATE-01
  - GATE-02
  - STRUCT-01
  - STRUCT-02
---

# Phase 71 Plan 01: Script Entry Gates Summary

**One-liner:** Added 90%-verification block gate and auto structure-checker-v2 invocation to `/script --new` with graceful degradation on missing files or agent failure.

## What Was Built

Two quality gates added to `.claude/commands/script.md`:

**Gate 1 — Research Verification Gate (GATE-01, GATE-02)**
Positioned immediately before the Duration & Structure Gate so it runs as the first check for any new script. Claude globs for `01-VERIFIED-RESEARCH.md`, counts `✅`/`⏳`/`❌` markers, and:
- Below 90%: emits a BLOCKED message with exact counts/percentages and stops
- At or above 90%: emits a PASSED summary and proceeds
- File missing: emits a one-line warning and proceeds
- Skipped entirely for: `--revise`, `--review`, `--teleprompter`, `--hooks`, `--collaborate`

**Gate 2 — Automatic Structure Check (STRUCT-01, STRUCT-02)**
Positioned after Retention Prediction in the post-generation flow. Claude reads `.claude/agents/structure-checker-v2.md` and applies it against the generated script, then displays findings by severity (CRITICAL / WARNING / INFO). When CRITICAL findings are present, an explicit block stating "Fix the CRITICAL items above or explicitly acknowledge them before running /verify" is appended. Graceful degradation: agent file missing = one-line skip note, no block.

**After Generation section updated** to include question 5 ("Any structure check findings you want to address first?") and changed the proactive suggestion to reference reviewing structure check findings before `/verify`.

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- `FOUND: .claude/commands/script.md`
- `FOUND: commit 54b612a`
- Research Verification Gate section: 2 occurrences (section header + PASSED banner)
- Automatic Structure Check section: 2 occurrences (section header + display template)
- CRITICAL ISSUES DETECTED: 1 occurrence
- structure-checker-v2 references: 3 occurrences
