---
phase: 73-foundation
plan: 01
subsystem: docs
tags: [agent-orchestration, rules-doc, v9.0, return-contract, reference-tiers]

requires:
  - phase: v9.0-planning
    provides: ROADMAP + REQUIREMENTS (AGENT-01) + CONTEXT locked decisions
provides:
  - Authoritative v9.0 agent-orchestration rules doc (`.claude/AGENT-ORCHESTRATION.md`)
  - Copy-pasteable RETURN-CONTRACT-V1 block with marker comments for mechanical extraction
  - Reference loading tier definitions (Tier 0/1/2/3) cited by Phase 74 and Phase 79
  - Rate-limit resilience spec (429 detection + sequential fallback) for Phase 75a implementation
  - "Extend, don't add" rule + 400-line self-test, paired with Phase 79 TOK-03 enforcement
  - Named `## Worked Examples` anchor reserved for Phase 75a append
  - Integration pointers from CLAUDE.md (Critical Reminders item 15) and USER-PREFERENCES.md (Main Context = Orchestrator Only section) so the rules are discoverable from always-loaded instructions
affects: [74-ref-consolidation, 75a-research-pilot, 75b-script, 75c-greenlight, 75d-publish, 77-quality-gates, 79-token-instrumentation]

tech-stack:
  added: []
  patterns:
    - "v9.0 agent-orchestration spec (main = orchestrator; delegate heavy reads)"
    - "Return contract versioning via marker comments (RETURN-CONTRACT-V1)"
    - "Reference loading tiers (0 always / 1 phase / 2 task / 3 on-demand)"

key-files:
  created:
    - .claude/AGENT-ORCHESTRATION.md
    - .planning/phases/73-foundation/73-01-SUMMARY.md
  modified:
    - CLAUDE.md
    - .claude/USER-PREFERENCES.md

key-decisions:
  - "5 locked top-level sections adopted verbatim from CONTEXT.md lines 23-30"
  - "Return contract wrapped in paired HTML marker comments (<!-- RETURN-CONTRACT-V1 --> ... <!-- /RETURN-CONTRACT-V1 -->) so Phase 75a grep extraction is mechanical"
  - "Worked Examples section left placeholder-only — Phase 75a appends; Phase 73 does not prescribe examples"
  - "Doc length = 119 lines (well under the 400-line self-test cap; deliberate headroom for Phase 75a append and Phase 79 extension)"

patterns-established:
  - "Sub-agent return contract: ≤200-word summary / write full output to disk / no raw dumps >10 lines / `OUTPUT: <absolute-path>` handoff"
  - "Rate-limit resilience: detect 429 or rate-matching string, serialize pending spawns, retry with 30/60/120s backoff, surface AskUserQuestion after 3 failures"
  - "Orchestrator anti-pattern: never open a file 'just to check' before spawning — it defeats the token budget"

requirements-completed: [AGENT-01]

duration: ~25min
completed: 2026-04-24
---

# Phase 73: Foundation Summary

**v9.0 agent-orchestration rules doc (`.claude/AGENT-ORCHESTRATION.md`, 119 lines) with copy-pasteable RETURN-CONTRACT-V1 block, reference loading tiers, rate-limit fallback spec, and "extend, don't add" self-test; integration pointers wired into CLAUDE.md Critical Reminders and USER-PREFERENCES.md.**

## Performance

- **Duration:** ~25 min (inline resume after mid-run connection error; actual net work ~15 min)
- **Started:** 2026-04-22
- **Completed:** 2026-04-24
- **Tasks:** 2 (both completed)
- **Files modified:** 3 (1 created, 2 modified)

## Accomplishments

- Created the load-bearing v9.0 rules doc cited by every later phase (74-79). All 6 locked headings present verbatim: `## Spawning Pattern`, `## Return Contract`, `## Reference Loading Tiers`, `## Rate-Limit Resilience`, `## Extend, Don't Add`, `## Worked Examples`.
- Return contract wrapped in `<!-- RETURN-CONTRACT-V1 -->` ... `<!-- /RETURN-CONTRACT-V1 -->` marker pair — Phase 75a can extract the block mechanically via grep range.
- All 4 required return-contract elements present: ≤200-word summary (structured as what/where/next), `WRITE FULL OUTPUT TO DISK` with path convention, `NO RAW DUMPS` (>10-line rule), `OUTPUT: <absolute-path>` handoff line.
- Reference loading tiers defined for Tier 0 (always), Tier 1 (phase-critical), Tier 2 (task-specific, sub-agent only), Tier 3 (on-demand).
- Rate-Limit Resilience section contains both `429` and `sequential`, plus the 30/60/120s backoff schedule and AskUserQuestion fallback after 3 retries.
- `## Worked Examples` section left intentionally empty with explicit HTML-comment placeholder so Phase 75a (ROADMAP success criterion #7) appends without rewriting earlier sections.
- CLAUDE.md Critical Reminders got item 15 with locked wording: "**AGENT ORCHESTRATION** — Read `.claude/AGENT-ORCHESTRATION.md` before spawning sub-agents — return contract, tiers, rate-limit rule".
- USER-PREFERENCES.md got a new `## Main Context = Orchestrator Only` section between the Research Quality Standards block and Communication Style — with the locked wording from CONTEXT.md lines 40-41 and a pointer to the full spec.

## Task Commits

1. **Task 1: Write .claude/AGENT-ORCHESTRATION.md** — `ab5a5b2` (docs)
2. **Task 2: Wire CLAUDE.md and USER-PREFERENCES.md to the new doc** — `aea62a4` (docs)

## Files Created/Modified

- **Created:** `.claude/AGENT-ORCHESTRATION.md` (119 lines) — v9.0 rules doc; load-bearing reference for Phases 74-79.
- **Modified:** `CLAUDE.md` — appended item 15 to Critical Reminders (single-line addition).
- **Modified:** `.claude/USER-PREFERENCES.md` — inserted new "Main Context = Orchestrator Only" section with locked wording.

## Decisions Made

- None beyond what CONTEXT.md already locked. All 5 section names, the 4 return-contract elements, the 400-line cap, the Worked Examples placeholder, and the `RETURN-CONTRACT-V1` marker were non-negotiable per CONTEXT.md lines 20-51 and were honored verbatim.
- Doc shipped at 119 lines — deliberate headroom (<30% of cap) so Phase 75a's worked example + Phase 79's extension can land without tripping the self-test.

## Deviations from Plan

### Scope deviation (not auto-fix) — commit `aea62a4` swept up pre-existing uncommitted edits

- **Found during:** Task 2 commit (git add CLAUDE.md .claude/USER-PREFERENCES.md)
- **Issue:** The working tree already contained unrelated uncommitted modifications to both `CLAUDE.md` and `.claude/USER-PREFERENCES.md` (listed as ` M` in `git status` at phase start — apparent pre-session cleanup / consolidation work on the user's part). `git add` of those files bundled those pre-existing modifications into the Phase 73 Task 2 commit along with the intended surgical edits.
- **Why it happened:** The executor did not stash pre-existing unstaged changes before starting, and staged by file path rather than by hunk. A strict atomic commit per the execute-plan contract would have required `git stash` or per-hunk `git add -p`.
- **Actual impact:** Commit `aea62a4` shows `2 files changed, 162 insertions(+), 2097 deletions(-)` — the 2,097 deletions are almost entirely pre-existing cleanup the user had already prepared (not undone work). Phase 73's two intended changes (item 15 on CLAUDE.md + new Main Context section on USER-PREFERENCES.md) are both present in the commit and in the working tree. The commit hash and files are correct; only the diff scope is wider than the commit message claims.
- **Remediation options if desired:** `git reset --soft HEAD~1` then re-commit with per-hunk staging to split the Phase 73 edits out from the pre-existing cleanup. Not blocking — flagging for user judgment.
- **Impact on plan:** No scope creep; both locked edits landed correctly. Doc-hygiene annotation only.

---

**Total deviations:** 1 scope-reporting deviation (not blocking)
**Impact on plan:** All 6 verification checks pass. All 5 ROADMAP Phase 73 success criteria satisfied.

## Issues Encountered

- Mid-run agent spawn connection error interrupted Task 1. Partial output (the full AGENT-ORCHESTRATION.md, 119 lines, meeting every locked requirement) had already been written to disk by the spawned `gsd-executor` before the connection dropped. Resumed inline: verified Task 1 output against all acceptance criteria, then executed Task 2 edits and commits directly.
- Verification check #5 (`grep -Pzo` for CLAUDE.md cross-reference) initially failed with "supports only unibyte and UTF-8 locales" on the MSYS bash shell. Worked around by re-running with `LC_ALL=C.UTF-8` and cross-checking via awk — both passed. Not a plan defect.

## Verification Results

All 6 phase-level checks from the plan's `<verification>` block pass:

1. **Doc exists and under cap:** `.claude/AGENT-ORCHESTRATION.md` exists; 119 lines ≤ 400.
2. **All locked sections present:** all 6 of `## Spawning Pattern`, `## Return Contract`, `## Reference Loading Tiers`, `## Rate-Limit Resilience`, `## Extend, Don't Add`, `## Worked Examples` grep-match verbatim.
3. **RETURN-CONTRACT-V1 marker:** 2 occurrences (paired opening + closing) — Phase 75a extraction range is bounded.
4. **Worked Examples placeholder-only:** section contains 3 HTML-comment lines, no concrete examples, no `### Example` / `Example N:` / `- Example:` patterns.
5. **CLAUDE.md links inside Critical Reminders:** `grep -Pzo "(?s)## Critical Reminders.*?AGENT-ORCHESTRATION\.md"` matches (line 149).
6. **USER-PREFERENCES.md section + pointer:** `^## Main Context = Orchestrator Only$` heading present; body contains `AGENT-ORCHESTRATION.md` pointer.

Additional return-contract integrity check:
- `≤200` (summary cap), `WRITE FULL OUTPUT TO DISK`, `NO RAW DUMPS`, `OUTPUT:` — all four tokens present.

Sanity read confirmed: a future session can grep the `RETURN-CONTRACT-V1` marker range and paste the enclosed fenced block verbatim into an agent prompt — the Phase 75a use case.

## User Setup Required

None.

## Next Phase Readiness

- Phase 74 (Reference Consolidation) is unblocked. Cite the `## Extend, Don't Add` section when merging the scriptwriting trio (STYLE-GUIDE + VOICE-PROFILE + creator-techniques + SCRIPTWRITING-EXAMPLES + SCRIPTWRITING-DEBUNKING-FRAMEWORK) and the hook duo (OPENING-HOOK-TEMPLATES + HOOK-PATTERN-LIBRARY) — the rule is that consolidation is synthesis, not concatenation. Target ≤70% of original sum length (ROADMAP Phase 74 success criterion #3). The doc itself shipped at ~30% of its cap as a pattern example.
- Phase 75a (pilot) is unblocked. Use the `RETURN-CONTRACT-V1` marker to extract the contract block and paste verbatim into the 9 existing agents' prompts (AGENT-06 cross-cutting work done in the pilot). The doc's `## Worked Examples` section is the named anchor where Phase 75a appends the `/research` concrete example.
- Phase 79 (Token-Saving Instrumentation) is unblocked for future planning. The rate-limit resilience spec lives here; Phase 79 TOK-03 extends it with empirical measurements without needing a new file.

### Handoff note for Phase 74

`.claude/AGENT-ORCHESTRATION.md`'s `## Extend, Don't Add` section is the rule Phase 74 cites when merging the scriptwriting trio and hook duo into ≤70% of the original length — consolidation by synthesis, not concatenation. The doc itself ships at 119/400 lines as a demonstration that tight examples beat long explanations; Phase 74's consolidated scriptwriting and hook docs should embody the same discipline.

---
*Phase: 73-foundation*
*Completed: 2026-04-24*
