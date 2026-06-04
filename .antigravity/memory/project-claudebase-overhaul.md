---
name: Claudebase overhaul plan (Gemini + brain + routines)
description: Active multi-session plan to integrate Gemini, build .brain/, deploy 5 daily routines, and assign per-agent Claude models. Executed in 11 ordered steps with a proof point at step 5.
type: project
originSessionId: 0c71c86c-a978-4caf-a38d-642837363a87
---
Active plan file: `C:\Users\Benoi\.claude\plans\robust-forging-pretzel.md`

**Why:** 47-video claudebase has fragmented knowledge, all-Opus default model use, and no automation watching for outliers/health/drift. User has Google AI Plan (Gemini access) and 5 free routines/day.

**How to apply:** When the user references "the plan", "the overhaul", "the brain", "the routines", or asks about Gemini integration / model routing — read the plan file first. The plan has 11 ordered execution steps with a STOP-the-world proof point at Step 5 (wiki-researcher retrofit). Do not fan out steps 6-11 if Step 5 doesn't pass.

**Locked decisions:**
- `.brain/` is additive only (NO migration of `channel-data/` — 91 hardcoded refs)
- 5 routines: 2 cloud (existing drafts at `.claude/routines/`), 3 Desktop scheduled tasks
- Routine 1 fires 04:00 GMT-5 (resets daily routine cap window early)
- Schema lock REQUIRED before any agent retrofit (contract.md + diff harness)
- Per-step model assignment matrix (Haiku/Sonnet/Opus) — see plan §Execution order

**Model-budget guardrail:** if an executor finds itself on Opus for a task assigned to Sonnet/Haiku in the execution table, switch model before continuing.
