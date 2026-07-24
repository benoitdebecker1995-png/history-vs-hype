# Skill Library Build — 2026-07

> **Goal:** A complete skill library under `.claude/skills/` so junior/mid-level engineers and
> Sonnet-class model sessions can debug, extend, validate, and advance this project at the
> standard held today. Authored via multi-agent orchestration (mapping → authoring → review → fix).
> Correctness over token cost.

## Design principles

1. **Skills are procedures + judgment + routers — never forked truth.** Where an authoritative
   file exists (ADR, REFERENCE doc, command), the skill points at it and says *when/why* to read
   it. Skills own only what is written nowhere else: navigation, failure modes, seams, standards.
2. **Audience: a cold Sonnet-class session.** Assume CLAUDE.md + MEMORY.md are loaded and nothing
   else. No prior conversation. Every instruction must be executable from a fresh prompt.
3. **Every referenced path/command must exist and run.** Mechanically verified in Wave 3.
4. **Frontmatter descriptions are triggers.** Each skill's `description:` states concrete
   trigger conditions (like `historian`) so auto-invocation works.
5. **Extend, don't add — justification:** no existing surface carries engineering-enablement
   knowledge (CLAUDE.md assumes expertise; commands are task procedures; REFERENCE is
   content-side). Boundary: these skills carry *how to work on the machine*, not *how to make
   videos* (that stays in commands/REFERENCE, skill 8 only routes to it).

## Library architecture (8 skills)

| # | Skill dir | Scope (owns) | Defers to |
|---|---|---|---|
| 1 | `project-onboarding` | First-session orientation: the two surfaces (channel ops vs engineering), truth-source hierarchy, lifecycle folders, read-order per task type, never-do list, session patterns | CLAUDE.md, all other skills |
| 2 | `codebase-atlas` | Where code lives: package map of `tools/`, entry points & CLIs, seam catalog (ADR 0004/0005/0008/0009/0010/0011/0012/0014), graphify MCP navigation, god nodes | `docs/adr/`, `.claude/REFERENCE/CODE-MAP.md` |
| 3 | `data-stores` | analytics.db / keywords.db / intel.db: schemas, owners (who reads/writes), refresh chains (07:45→08:00→08:30), truth hierarchy, AUTO zones, DB staleness semantics | ADR 0004/0014, `tools/youtube_analytics/` |
| 4 | `debugging-playbook` | Symptom→cause→fix table for known failure modes; diagnostic method for this repo (real-data verification, where evidence lives, reproduction recipes); Windows/PowerShell gotchas | skills 3/5, `docs/AUDIT-COMMANDS-2026-06.md` |
| 5 | `automation-ops` | Scheduled tasks (HvH-*), hooks (settings + tools/hooks/), MCP servers (NLM/VidIQ/graphify/playwright) health + auth recovery, external APIs (YouTube OAuth), routines | `docs/VIDIQ-MCP-SETUP.md`, memory NLM notes |
| 6 | `extending-safely` | How to change code at standard: extend-don't-add test, which seam to use when touching X, code/test conventions, secret-guard, commit format, agent-spawn rules digest | `.claude/AGENT-ORCHESTRATION.md`, ADRs |
| 7 | `validation-standards` | pytest map, how to run what, real-data validation rule, DB-pin test, gates philosophy (filters-not-predictors), per-artifact definition of done | `docs/TEST-STATUS-2026-06.md`, tests/ |
| 8 | `production-map` | ROUTER for the content pipeline: command sequence + gate authority model + conversational triggers (reconcile / script-lock) + artifact standards. Judgment digest only — zero procedure duplication | `.claude/commands/*`, historian skill, REFERENCE/ |

Plus `.claude/skills/README.md` — one-screen index with "which skill for which situation".

## Waves

- [x] **Wave 0 — Recon + this plan** (main context)
- [x] **Wave 1 — Mapping** (4 parallel agents → inventory docs in scratchpad `skill-build/`)
  - A `code-inventory` — packages, entry points, CLIs, tests map, run commands
  - B `data-inventory` — DB schemas (dumped live), table owners, refresh chains, AUTO zones
  - C `ops-inventory` — scheduled tasks, hooks, MCP servers, auth flows, known failure modes (audit docs + git log fix-commits)
  - D `standards-inventory` — engineering-relevant hard rules, gate authority, definition of done, orchestration rules
- [x] **Wave 2 — Authoring** (8 agents, one per skill; consume Wave-1 inventories + primary sources; format exemplar = `historian/SKILL.md`)
- [x] **Wave 3 — Review** (R1 engineering / R2 ops / R3 content scenario reviewers + R4 library-wide consistency; mechanical path/command existence check by orchestrator)
- [x] **Wave 4 — Fix + integrate** (all findings applied; `README.md` index written; CLAUDE.md pointer added; this doc closed)

## Resume instructions (if session dies mid-build)

Inventories live in the session scratchpad under `skill-build/` — if lost, re-run Wave 1
(prompts are reconstructable from the table above). Completed skills are in `.claude/skills/`;
check which of the 8 dirs exist to find the frontier. Review findings, if any, are appended
below.

## Build log

- 2026-07-01: Plan written. Wave 1 spawned (4 parallel agents).
- 2026-07-01: Wave 1 partial failure — session token limit hit mid-wave; standards-inventory completed, code/data/ops agents stalled before writing output. Recovery: resuming stalled agents SEQUENTIALLY (per AGENT-ORCHESTRATION.md rate-limit fallback) after quota reset.
- 2026-07-02: Wave 1 complete — all 4 inventories on disk (~1,200 lines, live-verified). Notable live findings: ctr_snapshots frozen at 2026-06-15; 2026-07-01 StartWhenAvailable catch-up burst broke the 07:45→08:30 chain ordering (reconcile stale-aborted); 4 dead keywords.db tables; stale plaintext YouTube API key in an old `~/.claude.json` project entry. Wave 2 spawning in batches of 3 (session-limit mitigation).
- 2026-07-02/03: Wave 2 complete — all 8 skills on disk, valid frontmatter, all registered. Session limits cut agents mid-run three separate times; all recovered by transcript-resume. Serial spawning from batch 2 on.
- 2026-07-03: Wave 3 mechanical check — ~316 path refs checked, 1 real dead path (data-stores cited `channel-data/stats.md`, which the channel-health routine reads but which never existed = live routine bug). All pytest invocations in validation-standards re-run live (649 default / 685 full / -k works).
- 2026-07-03: R1 (engineering lane): 1 CRITICAL (unimplemented `/status --surface` cited as live enforcement), 2 MAJOR (checker `ordered`-list silent skip; `list_all` exact-5 pin re-baseline), 7 minor. Verdicts: atlas SHIP, extending-safely SHIP-WITH-FIXES, validation-standards SHIP. **All fixed.**
- 2026-07-03: R2 (ops lane): 3 CRITICAL (stats.md dead path; false "cloud routines never-ran"; ctr_snapshots channel-filter trap — naive median = 2.04 vs canonical 2.51), 3 MAJOR (missing gray-zone-match F-row — live w/ #59; F13 date wrong in 2 places; registration recipe was prose+false-AtLogOn+stale example), 5 minor. All SHIP-WITH-FIXES. **All fixed**, incl. new F20/F21 rows, live-verified `Register-ScheduledTask` recipe (per-task limits corrected: PT10M/PT20M/PT1H), `nlm notebook query` word order, repo-bug corrections in reconcile-daily.md + channel-health-snapshot.md, and the stale NLM memory one-liner.
- 2026-07-03: R3 (content/onboarding): 0 CRITICAL, 3 MAJOR (analytics.db "NOT a CTR source" over-broad — `surface_ctr` is populated; demand-gate threshold ambiguity CLAUDE.md-vs-greenlight; idea-save trigger could induce a loose folder), 6 minor. Both SHIP-WITH-FIXES; all 5 simulations PASS (triggers, gate authority, router coverage all correct). **All fixed** + reconcile.md Routine-3/7 repo bug corrected.
- 2026-07-03: R4 (library-as-a-system): 2 CRITICAL (dead `/intel --refresh` instruction; CTR verify-line drift in 2 of 6 copies), 2 MAJOR (PT20M in case study; Feb-2023 ghost date), 4 minor, 3 [UNVERIFIED] resolved read-only. All 12 trigger probes route (zero-fire: none; contradictory overlap: none); all 33 cross-links resolve; 15-entry duplication register with declared canonicals. Verdict SHIP-WITH-FIXES → **all fixed**.
- 2026-07-03: Wave 4 complete — final sweep clean (frontmatter, "Use when:" triggers, ≤250-line caps, no control chars). `README.md` index + CLAUDE.md § Skill Library pointer added. **LIBRARY COMPLETE: 8 skills + index, 4-review trail, every path/command live-verified.**

## Owner-facing repo bugs surfaced during the build — RESOLUTION (2026-07-03)

1. **Channel-health baseline** — FIXED at root: STEP 1 no longer reads the never-created `channel-data/stats.md`; it now computes the baseline live (AVD/retention mean+σ from analytics.db `videos` last-10-before-window; CTR mean+σ from channel-filtered `ctr_snapshots` with a 14-day staleness skip). Both queries run-verified. F21 + data-stores updated to the fixed state.
2. **#59 "not archived"** — was a FALSE POSITIVE. A Sonnet agent following F20's verify-first rule established that 7fpBz6uo504 published 2025-07-29 (folder-less pre-2026 video) and #59 is genuinely still in edit. Documented in `manual-matches.json` `_left_unmatched` notes; F20 rewritten to teach verify-before-registering. No `null` block added (would break #59's real future auto-archive).
3. **ctr_snapshots** — UNFROZEN and now SCHEDULED: `ctr_tracker` run 2026-07-03 (newest snapshot 2026-07-03, was 2026-06-15), then owner approved Routine 8: task `HvH-CtrTracker` registered 2026-07-03, weekly Mon 07:30 (`run-ctr-tracker.ps1`, PT20M limit, StartWhenAvailable, IgnoreNew), first run 2026-07-06. Companion: SessionStart hook now emits a manual-CSV-pull staleness banner (Studio >30d / VidIQ >45d) for the data no API can fetch. Skills updated to six-task state.

## Laptop-off resilience (owner request, 2026-07-03)

Diagnosis: tasks can't run with the laptop off (expected), but ALL SIX were also `DisallowStartIfOnBatteries` (silently skipped/killed when unplugged — a laptop-killer), ChannelHealth + StaleProjects had NO catch-up, and the existing catch-up storms (F2, observed live 2026-07-01/02) broke chain ordering on every late wake. Fixes, all live-verified:
1. All tasks: `AllowStartIfOnBatteries` + `DontStopIfGoingOnBatteries` + `StartWhenAvailable` (XML-verified across all seven).
2. NEW `HvH-MorningCatchup` (`run-morning-catchup.ps1`): at LOGON (2-min delay) + daily 10:30 sweeper (covers wake-from-sleep, which fires no logon event). Evidence-gated, ORDERED re-run of missing steps only (Mon-CTR → refresh → health → reconcile → stale-nudge); no-op when the day is complete; BrainHygiene deliberately excluded (evening task). Structurally fixes F2.
3. LIVE TEST 2026-07-03 15:42: runner correctly detected all four steps missing (today's morning chain had genuinely not run), executed them in order, all exit 0 — reconcile ran AFTER a completed refresh, heartbeat advanced.
4. Evidence from the test: growth refresh took 23.5 min → standalone `HvH-GrowthRefresh` limit raised PT20M → PT30M (would have been limit-killed).
Skills updated to seven-task state (automation-ops inventory + F2/F3/F14 + data-stores chain + reconcile-daily.md notes).
4. **Stale plaintext API key** — REMOVED: dead backslash project entry deleted from `~/.claude.json` (backup at `~/.claude.json.bak-2026-07-03`), all MCP servers verified still connected. The removed `AIzaSy…` key is NOT used by any live tooling (current auth is OAuth2) — **owner should still revoke it in Google Cloud Console** since it sat in plaintext.
5. `reconcile.py`'s stale-DB alert text still blames "Routine 3" for the refresh Routine 7 owns (cosmetic; alert wording documented as-is in F1/D4). Left as-is deliberately — the string is cited verbatim by existing alerts and the F-catalog.
