---
name: project-onboarding
description: Entry-point router for the History vs Hype repo — the two work surfaces (content production vs engineering), the truth-source hierarchy, a task-type→read-order router into the 7 domain skills + historian, the never-do list, and how to work with the owner. Use when: starting work in this repo without prior context, onboarding, unsure which skill/doc/command applies, or asking how this project is organized. This skill ROUTES — it contains no deep procedure; jump to the routed skill before acting.
---

# Project Onboarding

You have AGENTS.md and MEMORY.md loaded and nothing else. This skill is the missing layer:
which kind of session you're in, what is authoritative, where to read next for your task,
and the ten mistakes that are never acceptable here. Repo root: `D:\History vs Hype`
(Windows 11; PowerShell primary, Git Bash available; Python is `python`, run modules as
`python -m tools.<pkg>.<module>` from repo root).

## The two surfaces

This repo is two things sharing one directory:

1. **A content-production operation** — a real YouTube channel. `video-projects/` lifecycle
   folders, `.Codex/commands/` pipeline (`/greenlight` → `/research` → `/script` → … →
   `/reconcile`), research discipline, packaging gates. Governing skills: **production-map**
   + **historian**. Conversational triggers ("I uploaded X", "script locked") are ARMED here.
2. **An engineering codebase** — `tools/` (241 Python files), three live SQLite DBs,
   scheduled tasks, hooks, MCP servers, a pytest suite. Governing skills: **codebase-atlas**,
   **extending-safely**, **validation-standards**, **data-stores**, **debugging-playbook**,
   **automation-ops**.

Which am I in? If the user talks about a video, topic, title, script, or research → content.
If about a tool, test, DB, task, or error → engineering. Sessions cross over constantly
("why is this number stale?" starts content, ends engineering) — the truth sources and the
never-do list below apply to BOTH. On either surface the owner is a non-engineer: report
outcomes, not architecture (see The owner, below).

## Truth-source hierarchy

| Source | Authoritative for | Trust notes |
|---|---|---|
| Filesystem (`video-projects/` lifecycle folders) | Which lifecycle stage a project is in | `_BACKLOG/` + `_ARCHIVED/old-*` are outside the lifecycle, invisible to every scanner — by design |
| `tools/youtube_analytics/analytics.db` | Publish status + channel performance ground truth | Outranks YT Studio / VidIQ dashboards (both confabulate). Not an **API** CTR source (`videos.ctr_percent` is NULL): per-video CTR → keywords.db `ctr_snapshots`; browse/suggested splits → analytics.db `surface_ctr` |
| Per-folder `PROJECT-STATUS.md` narrative (below `<!-- /AUTO:reconcile -->`) | Hand-written project state | Never machine-touched; everything ABOVE that marker is machine-owned |
| AGENTS.md + `.Codex/REFERENCE/` + `docs/adr/` | Rules, style, and standing decisions | Newer ADR beats older prose (e.g. ADR-0012 beats PACKAGING_MANDATE's "65+ gate" line) |
| Memory files (`MEMORY.md` + topic files) | Owner preferences and recorded incidents | Point-in-time — verify any code-behavior or file:line claim against current code before asserting |

**The one-line rule: derived docs are regenerated, never hand-edited.** Root
`video-projects/PROJECT_STATUS.md`, `PROJECT_REGISTRY.md`, `SWAP-LEDGER.md`,
`youtube-intelligence.md`, folder locations themselves — all derived; fix the truth source
and re-run the tool (`/reconcile`, `swap_ledger`, …).

**AUTO-zone warning:** any `<!-- AUTO:* -->` fenced block (reconcile, packaging-lock,
reconcile-dashboard) is machine-owned, matched by EXACT marker string — a "harmless" edit
inside or to the marker line orphans the zone or gets silently overwritten. Full zone rules,
schemas, staleness semantics → **data-stores** skill.

Lifecycle in three judgment lines (the spec itself is in AGENTS.md — don't re-derive it):
folder location is DERIVED state — `/reconcile` moves folders, you never move them by hand
mid-conversation; before creating any project file, Glob for the existing folder and confirm
its stage; `_BACKLOG/` is for parked work only, never filmed/published work.

## Task-type → read-order router (the core section)

Read in the order given, then act. Each row names the owning skill(s) plus at most the 1–2
files that are authoritative beyond it. Skills live in `D:\History vs Hype\.Codex\skills\<name>\SKILL.md`.

| You were asked to… | Read, in this order | Then act |
|---|---|---|
| Debug something broken / stale / "didn't run" (task, tool, MCP, data) | **debugging-playbook** (evidence-first method + evidence map) → its `FAILURE-MODES.md` if a row matches | Pull the evidence artifact BEFORE hypothesizing; fix root cause upstream; verify on real data |
| Add or modify code under `tools/` | **codebase-atlas** (where it lives, which seam) → **extending-safely** (routing checklist, conventions) → the matching `docs/adr/NNNN-*.md` | Route through the seam; tests land with the change → validation-standards for the done bar |
| Run or interpret tests | **validation-standards** (exact pytest commands + collection traps) → `docs/TEST-STATUS-2026-06.md` (noting its recorded staleness) | `python -m pytest -p no:cacheprovider -q` from repo root; fix ALL reds, not just yours |
| Query or cite channel data (views, CTR, retention, traffic) | **data-stores** (which table, staleness, read-only recipes) → **production-map** § decision epistemics if the number backs a recommendation | Cite n + source; distribution over aggregates; n<30 channel data is info-only |
| Work on a video project (any phase) | **production-map** (pipeline spine, which command next) → that project's `PROJECT-STATUS.md` | Run the phase command (`/greenlight`/`/research`/`/script`/…); never freelance the pipeline |
| Touch packaging / titles / thumbnails | **production-map** § gate authority → `tools/PACKAGING_MANDATE.md` (read with the ADR-0012 correction: title_scorer 65 = enrichment, not a gate) | Four filters decide via `packaging_lock.py`; scores never do |
| Do historical research (claims, quotes, sources, NLM) | **historian** (four hard rules + stop flags) → the project's `01-VERIFIED-RESEARCH.md` | File nothing past an unresolved flag; verbatims need an NLM anchor |
| Decide what document/verbatim goes ON SCREEN · trace a claim's provenance · genealogy-before-filing · /verify 7.8 | **primary-source** (on-screen-provenance discipline) → the project's `_research/SOURCE-GENEALOGY.md` ledger | Every on-screen claim needs a genealogy verdict before script-ready; a secondary-only claim is never framed as "documents show"; deep single-claim traces → `primary-source-hunter` agent |
| Touch automation: scheduled tasks / hooks / MCP servers / OAuth | **automation-ops** (inventory + admin, LOOK-ONLY vs MUTATES) — if it's BROKEN, **debugging-playbook** first | Check state LOOK-ONLY before running anything that mutates |
| Spawn sub-agents / run a big multi-step build | **extending-safely** § agent-spawn digest → `.Codex/AGENT-ORCHESTRATION.md` (the spec, incl. return contract + rate-limit rule) | Three spawn triggers; return contract verbatim; main context stays lean |
| The user said something trigger-shaped ("I uploaded X", "X is live", "script locked", "lock it", "T1 passed") | **production-map** § conversational triggers | ACT FIRST — run `/reconcile <X>` or the calibration delta-mine immediately; the utterance IS the trigger |
| Anything else / "how is this organized?" | This skill + AGENTS.md, then the closest row above | If two skills could own it, the routed skill's description settles the lane |

## Never-do list

The ten things no session gets to do here, each with the one-clause why:

1. **Never treat a score as a verdict** — #62's packaging was "locked" on a lone "VidIQ 95/100" with zero filters run; filters decide, scores inform (ADR-0012).
2. **Never hand-edit inside an `<!-- AUTO:* -->` zone** — exact-string markers mean your edit orphans the zone or is overwritten on the next tool run.
3. **Never dismiss a failing test as "pre-existing"** — the owner once had to manually order the fix of 6 failures dismissed that way; every red gets root-caused.
4. **Never claim verified/done without a real-data check** — synthetic fixtures prove code runs, only live DBs/CSVs prove behavior survived (recorded owner rule, 2026-07-01).
5. **Never fabricate claims about data or visuals you haven't opened** — "3rd best performer" turned out to be ~11 views; check `analytics.db` / Read the file first.
6. **Never include an unverified quote or claim in research** — exclude or flag it; NLM `notebook_query` synthesis fabricates verbatims and page numbers, so raw-read load-bearing quotes.
7. **Never create new surface area without the extend-don't-add test** — three discovery greps first; skipping them once rebuilt what `/fix` already did (~30% of a build wasted).
8. **Never work around a root cause without an explicit owner time-box** — don't disable, mock, swallow, or hide; missing dependency = `pip install`, never a mock.
9. **Never analyze Shorts with `/analyze`** — the tool and every benchmark behind it are long-form only.
10. **Never let n<30 channel-specific data drive a decision** — at ~57 videos every channel pattern is noise; decide on niche-wide corpora (n=85+), channel numbers are info-only.

Two engineering-side additions the principal enforced just as hard: never bypass the
pre-commit secret-guard to force a commit through, and never wire in a pattern derived from
best/worst extremes without a holdout test (all four 2026-06 opening formulas died out-of-sample).

## The owner

Non-engineer channel creator, scientific temperament, terse by nature. Working with him:

- **Frame outcomes, not architecture.** Say which command/report a code change affects and
  what improves — never an option menu of technical choices ("4 vs 6 fetches?" was rejected
  as "too technical"). Make the technical calls yourself; offer a plain go/no-go, and
  surface real risks plainly ("rearranging untested code first is how you break things").
- **Terse/shorthand messages are how he thinks, not laziness.** Infer intent, read between
  the lines, restate your understanding before a large task. His shorthand is direction,
  not copy — never paste his rough phrasing into a draft.
- **Ask only at genuine forks** you cannot resolve by research: max 4 sharp options,
  different ANGLES not synonyms. Researchable questions get researched, not offloaded.
- **Data-backed pushback, no yes-manning.** Lock recommendations and defend them with
  specific numbers (n + source) when challenged; flip only by naming which rule the old
  answer violated. Never dress an opinion as a metric — tier claims FACT/HEURISTIC/OPINION.
- **Corrections are captured live.** The moment he pushes back, save the derived rule to
  memory/wiki (and `video-projects/_CORRECTIONS-LOG.md` for process fixes) — "I'll remember"
  is not a fix.
- **Terse output back:** no preamble past one sentence, no emoji, no unrequested summaries.

## Session patterns

The first three moves of a well-run session:

1. **Check what surfaced at session start.** The SessionStart hook
   (`tools/hooks/session_context.py`) injects active projects into your first turn — read
   it before asking what's in flight. It shows only the active stages (`_IN_PRODUCTION/` +
   `_READY_TO_FILM/`); published work and `_BACKLOG/` never appear — by design.
2. **Content work? Run `/status`** for project state + ranked next action instead of
   reconstructing it by hand. Engineering work? Route through the table above before
   opening files at random.
3. **Glob/Read before asking.** If the user mentions something that exists (a script, a
   file, a video), find and read it yourself — never ask for information a file can give you.

Standing hygiene: batch independent tool calls in parallel; scope Reads to the part of the
file you need; treat memory-file claims about code as point-in-time (verify against current
code); on this machine, compare timestamps in UTC (local is UTC-5) and quote every path —
the repo root has a space in it.

## Related skills

- **production-map** — any content-production question: which command next, gate authority, conversational triggers, content-decision epistemics.
- **historian** — the moment you act as a researcher: NLM queries, `_IN_PRODUCTION/` folders, filing claims in `01-VERIFIED-RESEARCH.md`.
- **primary-source** — the on-screen-provenance layer on top of historian: what document goes on screen, the genealogy-before-filing gate, the `SOURCE-GENEALOGY.md` ledger, and when to spawn the `primary-source-hunter` agent.
- **codebase-atlas** — locate code: where X lives, what depends on it, exact run commands, seam catalog, graph-vs-grep navigation.
- **extending-safely** — before changing code or creating ANY new surface: extend-don't-add test, seam routing, conventions, commit + secret-guard, agent-spawn digest.
- **validation-standards** — running tests, the real-data verification rule, filters-not-predictors philosophy, per-artifact definition of done.
- **data-stores** — the three DBs' schemas and staleness, truth hierarchy depth, AUTO-zone rules, safe query recipes.
- **debugging-playbook** — anything broken, stale, or "didn't run": evidence-first method + the known-failure catalog. Go there BEFORE re-running things.
- **automation-ops** — scheduled-task/hook/MCP inventory and admin: check, run-once, re-register, re-auth (NLM `nlm login`, VidIQ OAuth, YouTube token).
