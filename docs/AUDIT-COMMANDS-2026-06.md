# Command / Skill / Agent Audit — 2026-06

> **UPGRADE-PLAN W1.** Inventory + usage signal + overlap shortlist. **No merges or retirements executed** — the user picks from § Shortlist (grill-locked: audit-report first). W2 records decisions in the § Decision log. W3 (routine health) may append its table here.

## Method + caveats (read before trusting numbers)

- **Invocations** = count across the 164 retained session logs in `~/.claude/projects/D--History-vs-Hype/*.jsonl` (~220 MB), summing `<command-name>` tags + `Skill` tool calls + `subagent_type` spawns. **These UNDERCOUNT real usage**: logs rotate, and much of the workflow fires via natural language ("I uploaded X" → /reconcile, "script locked" → calibration mine) or inside other commands without a logged invocation tag. Zero invocations ≠ dead — it means *no direct invocation in retained logs*.
- **Inbound refs** = number of files under `.claude/`, `CLAUDE.md`, `docs/`, `tools/` mentioning `/name` or `name.md` (excluding self). **Common-word names are inflated** (`patterns` 72, `historian` 155, `analyze` 30, `status` 24 match prose, not just the command). Distinctive names are accurate.
- **Reads** = distinct `.claude/REFERENCE|templates|skills|agents`, `memory/*.md`, `tools/*` paths the file instructs to read — a proxy for total context cost beyond its own size.

## Commands (`.claude/commands/`, 30 active + `_DEPRECATED/`)

| Command | Size (KB) | Inbound refs | Reads | Invocations | Note |
|---|---|---|---|---|---|
| script | 55.6 | 80 | 16 | 1 | Biggest command; canonical v18 flow |
| verify | 46.8 | 28 | 9 | 4 | incl. ambiguous `verify` Skill hits (built-in /verify collision) |
| research | 41.6 | 56 | 16 | 5 | absorbed /sources 2026-05-03 |
| publish | 34.2 | 33 | 9 | 0 | |
| thumbnail | 21.1 | 30 | 3 | 3 | |
| greenlight | 18.9 | 21 | 4 | 3 | |
| prep | 18.9 | 17 | 3 | 0 | |
| retitle | 18.2 | 8 | 6 | 1 | |
| polish | 15.3 | 3 | 3 | 3 | overlap → shortlist #3 |
| analyze | 13.5 | 30* | 0 | 0 | *common-word inflation |
| opener | 12.7 | 1 | 2 | 1 | |
| learn-from-paper | 11.6 | 2 | 4 | 0 | |
| editing-guide | 10.2 | 8 | 0 | 1 | |
| translate | 10.0 | 19 | 2 | 0 | Untranslated Evidence series |
| next | 9.6 | 17 | 0 | 0 | |
| status | 9.1 | 24* | 1 | 1 | |
| engage | 8.5 | 7 | 1 | 0 | |
| reconcile | 8.3 | 10 | 5 | 4 | + NL-triggered (undercounted) |
| script-research-pass | 7.4 | 0 | 3 | 1 | overlap → shortlist #2 |
| help | 7.1 | 6 | 1 | 0 | |
| comment-mine | 6.9 | 4 | 0 | 2 | |
| refactor | 6.4 | 7 | 0 | 17 | plan executor (this plan) |
| preflight | 6.4 | 12 | 2 | 0 | |
| fix | 5.9 | 11 | 0 | 4 | |
| verify-flow-nlm | 5.6 | 1 | 1 | 2 | overlap → shortlist #2 |
| gemini | 5.4 | 18 | 0 | 2 | dispatch utility |
| patterns | 5.4 | 72* | 0 | 0 | *heavy common-word inflation |
| growth | 2.4 | 8 | 0 | 1 | overlap → shortlist #4 |
| voice | 2.5 | 13 | 5 | 4 | +1 voice-discovery +1 voice-tooling (legacy names, already folded in) |
| curiosity | 1.4 | 8 | 0 | 2 | overlap → shortlist #1 |

`_DEPRECATED/README.md`: migration table only. **Stale pointer finding:** it routes 3 old commands to `/sources`, which was itself folded into `/research` (2026-05-03) — table needs a one-line update if touched in W2.

User-level command: `wiki-ingest` (2.8 KB, 1 invocation) — wiki triage, fine standalone.

## Agents (`.claude/agents/`, 11 + 6 contracts + 1 changelog)

| Agent | Size (KB) | Inbound refs | Reads | Spawns | Note |
|---|---|---|---|---|---|
| script-writer-v2 | 154.1 | 52 | 12 | 5 | v18.0; + 20.9 KB CHANGELOG |
| structure-checker-v2 | 114.1 | 23 | 4 | 3 | Wave 12 |
| research-organizer | 57.2 | 14 | 5 | 0 | shortlist #5 |
| article-writer | 52.7 | 20 | 5 | 0 | invoked directly per CLAUDE.md; newsletter lane |
| fact-checker | 31.6 | 26* | 1 | 0 | *name matches "fact-check" prose |
| notebook-researcher | 18.7 | 3 | 3 | 3 | NLM MCP lane, active |
| claims-extractor | 15.7 | 8 | 0 | 0 | shortlist #6 |
| diy-asset-creator | 15.1 | 9 | 0 | 0 | wired via /prep --assets |
| wiki-researcher | 12.2 | 8 | 0 | 3 | /research Step 5, active |
| thumbnail-critic | 8.3 | 3 | 5 | 0 | 2-stage thumbnail gate (gut-check first → critic only if unsure, so low spawn rate is by design) |
| competitor-gap | 8.1 | 4 | 2 | 6 | most-spawned specialist |

Built-in agent usage for scale: `general-purpose` 35, `Explore` 10.

## Skills

**Project:** `historian` — 5 files, 37.4 KB total, 8 invocations, deeply wired (/research stages A–C, stop-flags, web policy). Healthy; no action.

**User-level (relevance to this repo varies):**

| Skill | Size (KB) | Invocations | Note |
|---|---|---|---|
| grill-with-docs | 11.4 | 30 | most-used skill overall |
| graphify | 68.9 | 2 | MCP graphs do the daily work; skill = rebuild path |
| improve-codebase-architecture | 14.4 | 3 | |
| triage / to-issues / to-prd | 15.8 / 3.3 / 2.9 | 0 | issue-tracker lane documented in CLAUDE.md, unused so far |
| setup-matt-pocock-skills | 13.6 | 0 | one-shot installer, likely spent |
| diagnose | 8.5 | 0 | |
| write-a-skill | 3.2 | 0 | |
| caveman | 2.0 | 0 | |
| zoom-out | 0.4 | 0 | |

User-level files cost nothing in this repo's context until invoked; listed for completeness, not as merge candidates.

## Shortlist — merge / retire candidates (user picks; nothing executed)

1. **Fold `/curiosity` into `/greenlight`** as a scoring lens/flag. It evaluates exactly the decision /greenlight owns (title viability), is 1.4 KB, and both get invoked around the same moment. Risk: none visible. Counter-argument: it's also used ad-hoc on single titles mid-conversation, where a 1.4 KB standalone is cheaper than loading 18.9 KB of greenlight.
2. **Consolidate the deep-verification trio** — `/verify` (46.8 KB) vs `/verify-flow-nlm` (5.6 KB, self-described as "the deeper pass /verify --script skips") vs `/script-research-pass` (7.4 KB, paragraph-by-paragraph NLM + flow + polish, **0 inbound refs**). Three entry points to overlapping NLM-backed script checking. Options: (a) make verify-flow-nlm a `/verify --flow` flag and keep script-research-pass as the editor-pass; (b) merge script-research-pass and verify-flow-nlm (their NLM-query cores intersect heavily); (c) leave as-is — they were deliberately split for context economy (loading 47 KB verify.md to run a 5 KB pass is the thing the split avoids). Needs your call on which pass you actually reach for.
3. **`/polish` vs `/script --review` + voice_lint** — /polish (15.3 KB, 3 invocations) does the final AI-pattern pass; v18 flow already ends with a heavy gate + zero-feedback read-through, and voice_lint covers fingerprint checks. Question for W2: is /polish still a distinct stage in the v18 flow, or absorbed?
4. **Analytics family** — `/growth` (2.4 KB) and `/patterns` (5.4 KB) could become `/analyze --growth` / `--patterns`. Low value, low risk; mostly menu-decluttering.
5. **`research-organizer` agent (57.2 KB, 0 spawns in retained logs)** — /research's current flow spawns wiki-researcher + notebook-researcher; research-organizer's 14 inbound refs need a live-wiring check (refs may be stale docs). If nothing current spawns it: archive candidate (preserve under `.claude/_ARCHIVE/`).
6. **`claims-extractor` agent (15.7 KB, 0 spawns)** — /verify --extract territory; check whether verify.md still delegates to it or does extraction inline. If inline: archive candidate.
7. **`fact-checker` agent (31.6 KB, 0 spawns)** — same question as #6 for /verify's main path. Its 26 inbound refs are partly prose inflation ("fact-checker"/"fact-checking").

## Decision log (W2 — 2026-06-12, interactive walk)

| # | Candidate | Decision | Action taken |
|---|---|---|---|
| 1 | Fold `/curiosity` into `/greenlight` | **KEEP STANDALONE** | None. 1.4 KB; distinct cheap one-off title scorer worth keeping out-of-flow. |
| 2 | Verify/editor trio consolidation | **KEEP SPLIT, FIX DISCOVERABILITY** | Added a "Deeper passes" pointer block to `verify.md` flags section linking `/verify-flow-nlm` + `/script-research-pass` (the latter had 0 inbound refs). Context-economy split preserved (memory: `feedback-workflow-architecture`). |
| 3 | `/polish` retire (absorbed by v18 flow) | **KEEP, CLARIFY SCOPE** | Added scope note to `polish.md`: v18 `/script` flow already runs this in-flow; `/polish` is for out-of-flow scripts (parked/imported/hand-written) only. |
| 4 | Three unspawned agents | **ARCHIVE ALL THREE** | `git mv`'d `fact-checker`, `claims-extractor`, `research-organizer` (+ contracts) to `.claude/_ARCHIVE/agents-2026-06/` with a README. |
| — | Analytics family (`/growth`, `/patterns` → `/analyze` flags) | **DEFERRED** (not raised in W2 walk) | None. Lowest-value, pure menu-declutter; revisit only if the command menu needs trimming. |

**Reference cleanup on agent archive (W2):** `verify.md` (dropped fact-checker pointer), `primary-sources.md` ("Referenced by" trimmed), `.brain/methodology/gemini-routing.md` (3 routing rows removed), `competitor-gap.contract.md` (research-organizer consumer row removed), `AGENTS.md` (stale tree-comment example), `notebook-researcher.md` (fact-checking pointer → `/verify`). Remaining hits for the three names are prose role-mentions ("act as editor, fact-checker") or point-in-time `.planning/` + `.antigravity/` (parked) records — left as-is; none is live spawn wiring.

---

## Routine health check (W3 — 2026-06-12)

Assessed routines 1–6 against their declared output locations + cadence. **Phase-0 path breakage: NONE** — grep of all routine specs (`.claude/routines/*.md`) and launchers (`run-*.ps1`) for every Phase-0-moved path (`REFACTOR-PLAN`, `WORKSPACE_RULES`, `flight-deals`, `ANTIGRAVITY_MIGRATION`, `_BACKLOG/36`, etc.) returned clean. The only moved path a routine consumes — Panama #36 `_BACKLOG/` → `_IN_PRODUCTION/` — is correct current state that stale-project-nudge + reconcile are *supposed* to see. **Nothing to fix; all issues below are behavioral/config findings (out of W3 fix-scope, per the plan).**

| # | Routine | Runner | Declared output | Last evidence | Verdict |
|---|---|---|---|---|---|
| 1 | competitor-drop-scanner | cloud (no Desktop launcher) | `channel-data/competitor-drops/YYYY-MM-DD.md` | **2026-05-09** (~5 wks stale) | ⚠ DORMANT |
| 2 | modern-relevance-hook-hunter | cloud (no Desktop launcher) | project `MODERN-RELEVANCE-QUEUE.md` + metadata | **never** (queue file absent repo-wide) | ⚠ NO OUTPUT |
| 3 | channel-health-snapshot | Desktop `HvH-ChannelHealth` | `.brain/_inbox/channel-health-*.md` *(only on anomaly)* | ran 2026-06-12 08:00, result 0; silent | ✅ HEALTHY (silent = no anomalies, by design) |
| 4 | stale-project-nudge | Desktop `HvH-StaleProjects` | `.brain/_inbox/stale-projects-*.md` *(only if stale)* + index §3 | ran 2026-06-12 09:00, result 0; last dated file 2026-05-18 | ✅ HEALTHY (silent = nothing stale, by design) |
| 5 | brain-hygiene | Desktop `HvH-BrainHygiene` | `.brain/index.md` AUTO blocks + `_inbox/brain-hygiene-*.md` | ran 2026-06-11 22:00, **result 0x8007042B = Win32 1067 ERROR_PROCESS_ABORTED**; output dated 2026-06-11 present | ⚠ ABORTING |
| 6 | reconcile-daily | Desktop — wrapper expects task `HvH-Reconcile` | `_inbox/reconcile-*.diff` + `-*.md` + `-*.log` | **no `HvH-Reconcile` task registered; zero `reconcile-*.log` files ever**; last `.diff` 2026-06-08 (manual /reconcile) | ✗ NOT SCHEDULED |

### Findings (behavioral/config — for user decision, not fixed here)

1. **Routine 6 reconcile is not actually scheduled.** `run-reconcile.ps1` documents "Scheduled Task HvH-Reconcile daily at 08:30," but no such task exists (`Get-ScheduledTask` shows only BrainHygiene/ChannelHealth/StaleProjects). No `reconcile-*.log` has ever been written, confirming the wrapper never fired on schedule — the `.diff` files are all from manual `/reconcile`. CLAUDE.md's claim that "Routine 6 runs daily 08:30 as a backstop" is **currently false.** Fix = register the task: `schtasks /Create /TN HvH-Reconcile /TR "powershell -File 'D:\History vs Hype\.claude\routines\run-reconcile.ps1'" /SC DAILY /ST 08:30`. Held for user approval (touches OS scheduler; outside W3 path-fix scope).
2. **Routine 5 brain-hygiene aborts.** Last run terminated unexpectedly (Win32 1067). The `claude -p` headless invocation is crashing — likely a long-prompt/timeout or auth issue in the non-interactive context. The 2026-06-11 output exists (wrote before aborting or on a prior run), but the failure means index AUTO-block refresh is unreliable. Needs a live debug run of `run-brain-hygiene.ps1` to capture the crash.
3. **Routines 1 & 2 (the two "cloud" routines) show no recent output.** Competitor-drop last wrote 2026-05-09; modern-relevance has never produced its queue file. Neither has a Desktop launcher, so they were meant to run as scheduled cloud agents — but there's no evidence they're registered/firing. Verify via the `schedule` skill (cloud-agent list); if unregistered, either register them or downgrade the CLAUDE.md/brain-index claims that imply daily routines 1–3 run.
4. **`.brain/index.md` line 31 minor doc drift:** lists Routine 1 output as `.brain/_inbox/competitor-drops-*.md`, but the spec writes to `channel-data/competitor-drops/*.md`. Cosmetic; flag only.
