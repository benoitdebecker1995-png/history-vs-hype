---
name: debugging-playbook
description: Evidence-first diagnostic method and known-failure-mode catalog for this repo's automation, data pipelines, and tooling. Use when: something is broken, failing, stale, or "didn't run" (a scheduled HvH-* task, a routine, reconcile no-op/abort); a tool or test throws; data is missing or stale in a DB; an MCP server (NotebookLM/graphify/VidIQ) errors or returns suspicious output; yt-dlp/OAuth/Gemini auth failures; a strange Task Scheduler result code. NOT for schema reference (→ data-stores skill) or the task/hook/MCP inventory itself (→ automation-ops skill) — this skill owns HOW to diagnose and fix.
---

# Debugging Playbook

How to debug in `G:\History vs Hype`. The one-sentence version: **pull the evidence
artifact for the subsystem BEFORE forming any hypothesis, match against the known-failure
catalog, fix the root cause where it lives, verify against real data.** Never fix a symptom.

## The method (run this loop for ANY failure, known or unknown)

1. **Capture the exact symptom.** Verbatim error text, exit code, Task Scheduler result
   code, the alert file's actual words. "It failed" is not a symptom.
2. **Walk the evidence map (below).** Pull the log / timestamp / heartbeat for the failing
   subsystem. Do this even when you think you already know the cause.
3. **Normalize timestamps to UTC.** This machine is America/Lima (UTC-5). Scheduler times
   are local; `analytics.db` timestamps are UTC ISO strings. Most "impossible" orderings
   are this boundary. (The 2026-07-01 case study below crossed it.)
4. **Match against the catalog:** [FAILURE-MODES.md](FAILURE-MODES.md) — symptom → check →
   cause → fix for every failure mode this repo has actually hit. If a row matches,
   apply its recorded fix; do not invent a new one.
5. **Unknown failure:** narrow with read-only checks only. Form ONE hypothesis that
   explains ALL the evidence (not just the loudest piece), then test it with the cheapest
   read-only check that could falsify it. A hypothesis that ignores one artifact is wrong.
6. **Fix the root cause where the defect lives** — upstream module, not call site
   (precedent: ADR-0012 fixed `title_scorer.py` itself rather than patching around it in
   the new checker). Then **verify with real data**: run the fixed path against the live
   DBs/files and confirm a known-true fact, not a synthetic fixture (→ validation-standards).
7. **Capture the lesson.** Recurring failure → add/update a row in FAILURE-MODES.md.
   User correction → save to memory/wiki immediately.

## Evidence map — first stop per subsystem

All paths absolute; commands are PowerShell, copy-pasteable from any directory.

| Subsystem | Evidence artifact | How to read it |
|---|---|---|
| Scheduled routines (HvH-*) | Task Scheduler ground truth | `Get-ScheduledTask -TaskName "HvH-*" \| Get-ScheduledTaskInfo \| Format-Table TaskName, LastRunTime, LastTaskResult, NextRunTime` |
| Routine execution detail | `.brain/_inbox/` run logs (`growth-refresh-*.log`, `reconcile-*.log`, `channel-health-run-*.log`, `stale-projects-run-*.log`, `brain-hygiene-run-*.log`, `ctr-tracker-*.log`, `morning-catchup-*.log`) | `Get-ChildItem "G:\History vs Hype\.brain\_inbox" \| Sort-Object LastWriteTime -Descending \| Select-Object -First 10 Name, LastWriteTime` |
| Reconcile outcome | `.brain\_inbox\reconcile-YYYY-MM-DD.md` (summary), `reconcile-*-HHMM.diff` (reversible, powers `--undo`), `reconcile-stale-db-YYYY-MM-DD.md` (freshness abort) | Read the newest; the `.md` alert is the REAL signal for aborts — but on a no-op/gray-zone day NO `.md` is written: the `reconcile-YYYY-MM-DD.log` is then the load-bearing evidence (grep for "gray-zone" / "LOGGED", F20). The wrapper logs claude's exit (0), not the tool's (2) |
| Reconcile heartbeat | `.brain\last-reconcile-ts.txt` (ISO UTC of last successful run) | `Get-Content "G:\History vs Hype\.brain\last-reconcile-ts.txt"` |
| analytics.db freshness | `MAX(metrics_fetched_at)` in `videos` (UTC; reconcile gates at 36h) | `python -c "import sqlite3; print(sqlite3.connect('file:D:/History%20vs%20Hype/tools/youtube_analytics/analytics.db?mode=ro', uri=True).execute('SELECT MAX(metrics_fetched_at) FROM videos').fetchone()[0])"` |
| Live CTR freshness | `ctr_snapshots.snapshot_date` in keywords.db (separate from analytics.db freshness!) | `python -c "import sqlite3; print(sqlite3.connect('file:D:/History%20vs%20Hype/tools/discovery/keywords.db?mode=ro', uri=True).execute('SELECT MAX(snapshot_date) FROM ctr_snapshots').fetchone()[0])"` |
| intel.db freshness | `kb_meta.last_refresh`; every intel query output carries a staleness footer | `python -m tools.intel.query` output footer, or read `kb_meta` read-only as above |
| YouTube OAuth state | `tools\youtube_analytics\credentials\token.json` mtime (rewritten on every refresh/re-auth) + the newest `growth-refresh-*.log` | `Get-Item "G:\History vs Hype\tools\youtube_analytics\credentials\token.json" \| Select-Object LastWriteTime` |
| MCP servers | live connection status | `claude mcp list` (run from repo). NLM health = an authenticated call (`notebook_list`), NEVER `refresh_auth`/`server_info` — both false-report "expired" (0.6.14 bug) |
| Graphify code graph | `~/.cache/graphify-rebuild.log` (post-commit rebuilds) | `Get-Content "$env:USERPROFILE\.cache\graphify-rebuild.log" -Tail 20` |
| Graphify research graph | staleness marker `graphify-out\research\.needs_refresh` (touched by `/reconcile` on archive) | `Test-Path "G:\History vs Hype\graphify-out\research\.needs_refresh"` |
| Gemini CLI | `_gemini-output/` dated files (did the dispatch land?); `~/.gemini/settings.json` → `security.auth.selectedType` must be `"gemini-api-key"` | `Get-ChildItem "G:\History vs Hype\_gemini-output" \| Sort-Object LastWriteTime -Descending \| Select-Object -First 5` |
| Cloud routines 1–2 | dated files in `channel-data\competitor-drops\` / `channel-data\modern-relevance\` — a dated file = it ran | `Get-ChildItem` on those dirs; a dated file = a run happened (manual runs exist, latest 2026-05-09) — NOT registered as scheduled tasks, see F18 |
| Routine findings (not runs) | `.brain\_inbox\channel-health-*.md`, `stale-projects-*.md` — written ONLY on anomaly; silence is healthy | absence ≠ failure; check the `-run-*.log` for execution proof |

If the URI-form sqlite one-liner errors on your shell, fall back to
`sqlite3.connect(r'G:\History vs Hype\tools\youtube_analytics\analytics.db')` — read queries
only; never write to a live DB during diagnosis (all three main DBs are git-tracked).
Full DB semantics, tables, refresh chains: → data-stores skill.

**Task Scheduler result codes worth memorizing:** `0` ok · `1` script failed (open the
`.brain\_inbox` log) · `0x41306` (267014) terminated/limit-killed · `0x800710E0`
(2147946720) launch refused · `0x8007042B` process aborted.

## Known failure modes — triage index

Full symptom → check → cause → fix rows, plus reproduction recipes, live in
[FAILURE-MODES.md](FAILURE-MODES.md). Jump straight to a row ID:

| You're seeing | Row |
|---|---|
| Reconcile wrote `reconcile-stale-db-*.md` / exit 2 / no folder moves | F1 |
| Reconcile exit 0 / DB fresh / heartbeat advanced — but an upload never archived | F20 — gray-zone match, logged not acted |
| Channel-health silent even when metrics clearly moved | F21 — baseline file missing |
| All morning tasks share one LastRunTime; reconcile stale-aborted anyway | F2 (case study below) |
| "Refresh token revoked — need full re-authorization" in growth-refresh log | F3 |
| Routine log says "You've hit your session limit" | F4 |
| Routine exits 0 but did nothing / a NEW routine greet-and-exits | F5 |
| Task LastResult `0x800710E0` | F7 |
| NLM MCP `UNAUTHENTICATED` / file-upload-only failures | F8 |
| `notebook_query` returns confident quotes + page numbers | F9 — fabrication risk, raw-read before trusting |
| yt-dlp HTTP 429 / "confirm you're not a bot" / DPAPI cookie error | F10 |
| graphify-rebuild.log "Invalid control character" | F11 |
| `/retitle` surfaces already-retitled videos, `video_id = None` | F13 |
| `ctr_snapshots` weeks stale | F14 |
| Gemini `IneligibleTierError` | F15 |
| Mojibake (`ΓÇö`) in logs / UnicodeEncodeError | F16 |
| A credential-looking file is staged / the pre-commit hook fired | F17 |
| Cloud routines produce no recent dated files | F18 |
| A test skips forever (`skipUnless` guard) | T5 |
| A doc or alert blames "Routine 3" for stale analytics.db | D4 |
| `ModuleNotFoundError: No module named 'tools'` | T1 |
| pytest green but suites missing / INTERNALERROR / WinError 5 cache | T2–T4 |
| Freshness check returns 999 | D3 — sentinel for "can't read", looks identical to stale |
| git status shows the .db files modified | D1 — expected; live git-tracked DBs |

## Worked case study — the 2026-07-01 catch-up burst (how the method runs)

**Symptom.** Morning reconcile produced no archive. `.brain\_inbox\reconcile-stale-db-2026-07-01.md`
exists, claiming `analytics.db` was 48.9h stale — yet when you query the DB it looks fresh.
The wrapper log shows exit 0. Three facts that appear to contradict each other.

**Evidence walk (in map order):**
1. Scheduler ground truth: all four morning tasks (GrowthRefresh 07:45, ChannelHealth 08:00,
   Reconcile 08:30, StaleProjects 09:00) show the IDENTICAL LastRunTime `2026-07-01 09:17:38`.
   That is the signature fact — tasks never legitimately share a timestamp. Result codes:
   GrowthRefresh `0x41306` (terminated), ChannelHealth/StaleProjects `0x800710E0` (refused),
   Reconcile `0`.
2. Reconcile evidence: the stale-abort `.md` was written at 09:17. The wrapper's exit 0 is
   claude's exit, not the python tool's exit 2 — the alert file is the real verdict.
3. DB timestamp (UTC!): `MAX(metrics_fetched_at)` = `2026-07-01T14:19Z` = 09:19 **local** —
   two minutes AFTER reconcile checked at 09:17.
4. GrowthRefresh log: "Refresh token revoked — need full re-authorization", then a human
   browser OAuth; the DB write completed 09:19. `0x41306` = the task's execution limit (PT30M
   for GrowthRefresh since 2026-07-03; was PT20M) killed the task shell while python waited on the browser — yet python
   survived and finished.

**Root cause (one hypothesis explaining ALL four artifacts):** the PC was off at trigger
time, so `StartWhenAvailable` catch-up fired all four tasks SIMULTANEOUSLY at 09:17. The
07:45→08:30 ordering only exists on-schedule, not on catch-up. Reconcile read the DB
mid-refresh (genuinely 48.9h stale at that instant — the math crosses the UTC-5 boundary),
correctly aborted; GrowthRefresh landed fresh data two minutes later.

**Symptom-fixes the principal would refuse:** raising `MAX_DB_AGE_HOURS`, deleting the alert
file, or blind re-running until green. Each hides two real defects (ordering break + revoked
OAuth token) and guarantees recurrence.

**Resolution.** Immediate: once the refresh has finished, re-run
`python -m tools.reconcile.reconcile --auto-publish-only` from the repo root. Structural
(unbuilt as of 2026-07-01): chain reconcile to refresh completion or retry-on-stale — report
to owner as an open defect, in outcome terms ("on days the PC was off in the morning,
publishes won't auto-archive until re-run"). The `0x800710E0` on the two claude-driven tasks
recurs on catch-up storms and its root cause is [UNVERIFIED] — a live
`Export-ScheduledTask` settings review is the next diagnostic step, not a rewrite.

## Escalation rule — root cause > workaround

Global hard rule: don't disable, mock, swallow, or hide. Diagnose first, fix upstream.

A **workaround is acceptable ONLY when** (all recorded, never silent):
- The failure is an external outage you cannot fix (Google transient 500s → F19;
  YouTube bot-wall → F10): use the DOCUMENTED fallback chain, never an improvised
  degradation, and say which chain you used.
- The owner explicitly time-boxes it: record the time-box + revert condition in the
  relevant doc or a GitHub issue (`gh` CLI) before moving on.
- You are blocked on a human-only step (browser OAuth at `localhost:8080`, elevated shell
  for task registration): report and stop — a scheduled/headless context can NEVER complete
  these; looping on them is the anti-pattern.

**Stop and report to the owner instead of pushing when:** the fix requires destructive or
irreversible action (deleting data, force-pushing, rewriting a live DB); it needs elevation
or a human at a browser; two+ plausible root causes remain after a full evidence-map walk
and distinguishing them is expensive (ask, don't guess); or the evidence still contradicts
itself. The owner is a non-engineer: report in outcome terms ("daily publish-archiving is
down; needs you to click through a Google login once"), never architecture terms.

## Anti-patterns (what the retiring principal refuses)

1. **Fixing the symptom** — raising a staleness threshold, deleting an alert file,
   hand-editing an `<!-- AUTO:* -->` zone to make state look right.
2. **Disabling/mocking/skipping to silence red** — missing dependency = `pip install X`,
   never sys.modules injection, skip decorators, or try/except-pass.
3. **"Pre-existing failure" dismissal** — every red test gets root-caused and fixed, not
   just the ones your change broke.
4. **Retry/sleep loops instead of diagnosis** — a second identical run is only justified
   AFTER the evidence explains why the first failed and why now is different.
5. **Claiming "fixed/verified" without real data** — run the repaired path against the live
   DBs/CSVs and confirm a known-true fact (→ validation-standards).
6. **Trusting a confident number without checking its vintage** — `/retitle` parses a stale
   snapshot (bulk generated 2026-03-07, appended piecemeal since — F13); `ctr_snapshots` can be weeks stale (F14); Studio/VidIQ numbers
   confabulate — cross-check `analytics.db` before acting on any of them.
7. **Building on unexplained artifacts** — e.g. `.claude\scheduled_tasks.lock` has zero repo
   references; best hypothesis is a Claude Code harness mutex. Don't build on it.
8. **Re-testing known dead ends** — ollama graphify backend (dead on this laptop, smoke-tested
   2026-05-26); yt-dlp `--cookies-from-browser chrome` (App-Bound/DPAPI, dead). The catalog
   exists so these aren't re-litigated.

## Windows gotchas that masquerade as bugs

- **Quote every path** — `G:\History vs Hype` has a space; unquoted paths are the #1 way a
  new script breaks here. Git Bash form: `/d/History vs Hype/` (still quoted).
- **Two shells, two syntaxes:** scheduled tasks run PowerShell 7; git hooks run POSIX `sh`
  (Git Bash). `2>$null` vs `/dev/null` — never mix.
- **Run python modules as `python -m tools.x.y` from the repo root** — direct script paths
  hit `ModuleNotFoundError: No module named 'tools'` (T1). No `python3` shim exists; use `python`.
- **No `sqlite3` CLI** in Git Bash — use the python one-liners in the evidence map.
- **`SIGALRM` doesn't exist on Windows** — the graphify post-commit 600s timeout never arms;
  a wedged rebuild runs unbounded in the background (can pin CPU; won't block the commit).
- **cp1252 console:** `PYTHONIOENCODING=utf-8` is already a User env var; mojibake in logs is
  cosmetic, not corruption (F16).
- **Timezone:** local = UTC-5; DB timestamps UTC. Compare in UTC, always.
- **`~/.claude.json` has TWO project keys** (`D:\…` backslash = stale, `D:/…` forward-slash =
  live). MCP config edits to the wrong key silently don't take effect.
- **OAuth `run_local_server(port=8080)`** needs the port free AND a human + browser present.

## Related skills

- **data-stores** — when the question is what a table/column MEANS, who writes it, or the full
  refresh-chain/staleness semantics behind a freshness check you ran here.
- **automation-ops** — when you need the full inventory of scheduled tasks, wrappers, hooks, and
  MCP servers (schedules, registration, auth-recovery procedures) rather than a diagnosis.
- **validation-standards** — when the fix is in and you need the definition of done: how to run
  the test suites and what "verified against real data" means before you claim it.
