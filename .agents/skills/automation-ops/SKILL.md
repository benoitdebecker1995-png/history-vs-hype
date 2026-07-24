---
name: automation-ops
description: Operational inventory and admin procedures for this repo's automation — the seven HvH-* Windows scheduled tasks (schedules, wrappers, check last-run, run-once, re-register), all hooks (Codex, git secret-guard, graphify), the 7 MCP servers (config location, health checks, auth recovery incl. NLM `nlm login` and VidIQ OAuth), and external API surfaces (YouTube OAuth token repair, yt-dlp fallback, Gemini CLI dispatch, nlm CLI). Use when: checking, running, registering, or modifying a scheduled task; asking "what hooks exist" or "did the hook fire"; an MCP server is down or needs re-auth; asking where OAuth tokens / API keys live; adding a NEW routine. NOT for diagnosing WHY something broke (→ debugging-playbook owns the method and the F-row catalog).
---

# Automation Ops

Inventory + admin for everything that runs unattended in `D:\History vs Hype`.
Every command below is tagged **LOOK-ONLY** (safe anywhere) or **MUTATES** (changes task
state, tokens, config, or data — know what you're doing first). Diagnosis of a broken
automation is NOT this skill — jump to debugging-playbook and cite its F-row IDs.

## 1. Scheduled tasks (Windows Task Scheduler)

Seven `HvH-*` tasks, all `Ready` (five live-verified 2026-07-02; HvH-CtrTracker + HvH-MorningCatchup registered 2026-07-03). All run
`C:\Program Files\PowerShell\7\pwsh.exe -File "D:\History vs Hype\.Codex\routines\<wrapper>.ps1"`,
daily trigger ONLY — the `AtLogOn` trigger documented in `reconcile-daily.md` is NOT
registered (needs an elevated shell; still pending). `MultipleInstances IgnoreNew`,
per-task execution limits (Reconcile 10 min · GrowthRefresh 30 min · CtrTracker 20 min · BrainHygiene/MorningCatchup 1 h;
ChannelHealth/StaleProjects none set — XML-verified 2026-07-03). Since 2026-07-03 ALL tasks have
`StartWhenAvailable` catch-up AND `AllowStartIfOnBatteries` + `DontStopIfGoingOnBatteries`
(before that, every task was battery-blocked — a laptop-killer — and ChannelHealth/StaleProjects
had no catch-up at all). Storm caveat still applies: per-task catch-up fires ALL missed tasks
at once and breaks the chain ordering — that's F2 in debugging-playbook, observed live 2026-07-01).

| Task | Schedule | Wrapper (`.Codex/routines/`) | Underlying command |
|---|---|---|---|
| HvH-CtrTracker (Routine 8) | Mon 07:30 | `run-ctr-tracker.ps1` | `python -m tools.youtube_analytics.ctr_tracker` (pure python) — writes keywords.db `ctr_snapshots`; registered 2026-07-03 after an 18-day freeze (F14) |
| HvH-GrowthRefresh (Routine 7) | daily 07:45 | `run-growth-refresh.ps1` | `python -m tools.youtube_analytics.growth_data --refresh` (pure python, no Codex) — writes analytics.db |
| HvH-ChannelHealth (Routine 3) | 08:00 | `run-channel-health.ps1` | `Codex -p channel-health-snapshot.md` — READS analytics.db, alert only on anomaly |
| HvH-Reconcile (Routine 6) | 08:30 | `run-reconcile.ps1` | `Codex -p reconcile-daily.md` → `python -m tools.reconcile.reconcile --auto-publish-only` |
| HvH-StaleProjects (Routine 4) | 09:00 | `run-stale-projects.ps1` | `Codex -p stale-project-nudge.md` — scans `_IN_PRODUCTION/` mtimes |
| HvH-MorningCatchup | at LOGON (2-min delay) + daily 10:30 sweeper | `run-morning-catchup.ps1` | Evidence-based ORDERED re-run of any morning step missing today (Mon CTR → refresh → health → reconcile → stale-nudge); converges to no-op when the chain is complete. Fixes both the laptop-was-off case and the F2 catch-up storm. Registered 2026-07-03 |
| HvH-BrainHygiene (Routine 5) | daily 22:00 | `run-brain-hygiene.ps1` | `Codex -p brain-hygiene.md` — `.brain/_queue/` + index refresh |

The morning chain is a data dependency: 07:45 refresh WRITES `analytics.db` → 08:00 reads it
→ 08:30 freshness-gates on it (36h) → 09:00 reads project state. Semantics of the gate and
the DB → data-stores skill.

**Codex-driven wrapper pattern** (all but GrowthRefresh): `Set-Location "D:\History vs Hype"`
→ read routine `.md` → `Codex -p $prompt` → append output + exit code to
`.brain\_inbox\<name>-YYYY-MM-DD.log`. The wrapper logs *Codex's* exit code, not the inner
python's — the `.brain\_inbox` artifact files are the real verdict (F1/F2).

### Check state — LOOK-ONLY

```powershell
# Last run, result code, next run for all seven
Get-ScheduledTask -TaskName "HvH-*" | Get-ScheduledTaskInfo |
  Format-Table TaskName, LastRunTime, LastTaskResult, NextRunTime

# What a task actually executes (action + args)
(Get-ScheduledTask -TaskName "HvH-Reconcile").Actions

# Full settings/triggers as XML (the F7 diagnostic read)
Export-ScheduledTask -TaskName "HvH-ChannelHealth"

# Newest run logs (execution proof — result codes lie, logs don't)
Get-ChildItem "D:\History vs Hype\.brain\_inbox" | Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 Name, LastWriteTime
```

Result-code decoding and what to do about a bad one → debugging-playbook (`0x41306`
terminated, `0x800710E0` refused → F7, exit 1 session-limit → F4, stale-abort → F1/F2).

### Run once now — MUTATES

```powershell
# Preferred: run the wrapper directly — same behavior, output visible, log written
pwsh -File "D:\History vs Hype\.Codex\routines\run-growth-refresh.ps1"

# Or via the scheduler (fires detached; check the log afterwards)
Start-ScheduledTask -TaskName "HvH-Reconcile"
```

Running GrowthRefresh writes `analytics.db`; running Reconcile can MOVE project folders
(reversible via `python -m tools.reconcile.reconcile --undo`, repo root). Never run these
just to "see if it works" — check the logs first (LOOK-ONLY above).

### Re-register / modify a task — MUTATES

Live-verified registration pattern (exported from `HvH-GrowthRefresh` task XML, 2026-07-03):

```powershell
$action  = New-ScheduledTaskAction -Execute "C:\Program Files\PowerShell\7\pwsh.exe" `
           -Argument '-File "D:\History vs Hype\.Codex\routines\run-<name>.ps1"' `
           -WorkingDirectory "D:\History vs Hype"
$trigger = New-ScheduledTaskTrigger -Daily -At 07:45   # weekly variant: -Weekly -DaysOfWeek Monday -At 09:00
$set     = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
           -ExecutionTimeLimit (New-TimeSpan -Minutes 20)
Register-ScheduledTask -TaskName "HvH-<Name>" -Action $action -Trigger $trigger -Settings $set   # MUTATES
```

Principal: default current user, Limited, InteractiveToken — do NOT add `-RunLevel Highest`. For a
pure-python routine the wrapper .ps1 just calls `python -m tools.routines.<module>` (mirror
`run-growth-refresh.ps1`, the live exemplar); Codex-driven routines follow the checklist below. An
`AtLogOn` trigger needs an **elevated** shell — planned for Reconcile but NEVER registered (the prose
in `reconcile-daily.md` § "Task registration" claimed it was; corrected 2026-07-03). **Do NOT copy
the `Register-ScheduledTask` block in `channel-health-snapshot.md` § Setup** — stale pre-wrapper
example (`Codex --print` direct, `-RunLevel Highest`, no settings); it matches no live task.
`Disable-ScheduledTask` / `Enable-ScheduledTask -TaskName "HvH-*"` also MUTATE. After any change,
verify LOOK-ONLY: `Get-ScheduledTaskInfo` shows `NextRunTime` in the future.

### Adding a NEW Codex-driven routine — checklist (F5, incident 2026-06-13)

All three or it will exit 0 having done nothing: (1) "▶ EXECUTION DIRECTIVE" at the top of the
routine `.md` (headless Codex otherwise treats it as documentation and greets-and-exits);
(2) scoped `Edit(.brain/**)`/`Write(.brain/**)` allow-rules in `.Codex/settings.local.json`
(already present — don't widen them); (3) wrapper logs full output + `$LASTEXITCODE` to
`.brain\_inbox\`.

### Cloud routines 1–2 — specs only, NOT scheduled

`competitor-drop-scanner.md` / `modern-relevance-hook-hunter.md` in `.Codex/routines/` were
never registered anywhere (F18). Evidence they ran = dated files in
`channel-data\competitor-drops\` / `channel-data\modern-relevance\`. Registering them is the
owner's call — propose, don't silently register.

## 2. Hooks

### Codex — project (`D:\History vs Hype\.Codex\settings.json`)

| Event | Matcher | Script | Behavior |
|---|---|---|---|
| PreToolUse | `Edit\|Write\|NotebookEdit` | `python tools/hooks/locked_asset_guard.py` | Asks (never denies) before edits to `_ARCHIVED/published/**`, `FINAL-SCRIPT-TELEPROMPTER*`, or files carrying a LOCK marker in the first 2000 chars. Fails open. |
| SessionStart | `startup\|resume\|clear` | `python tools/hooks/session_context.py` | Injects active projects into first-turn context via `VideoProjectRepo`. Globs only the 3 lifecycle folders, and DISPLAYS in-production + ready-to-film only — `_BACKLOG/` and published invisible BY DESIGN, not a bug. Also emits the manual-CSV-pull staleness banner (Studio export >30d / VidIQ export >45d, mtimes under `channel-data/`; added 2026-07-03). |

`.Codex/settings.local.json` holds permissions only (incl. the `.brain/**` rules above) — no hooks.

### Codex — user-global (`C:\Users\Benoi\.Codex\settings.json`)

GSD suite (SessionStart/PreToolUse/PostToolUse guards) + the **Stop hook**
`extract-learnings.js`, which drops candidate learnings into `~/.Codex/wiki/_queue/` for
`/wiki-ingest`. Scripts live in `C:\Users\Benoi\.Codex\hooks\`. These fire in every project;
their internals are outside this repo — don't debug them here.

### Git hooks (`.git/hooks/` — installed, NOT version-controlled)

| Hook | Source / install | Behavior |
|---|---|---|
| pre-commit (secret-guard) | tracked at `tools/hooks/pre-commit`; install: `sh tools/hooks/install.sh` (Git Bash, idempotent — MUTATES `.git/hooks/`) | Blocks staged credential-looking files (`token.json`, `client_secret*.json`, `*oauth*.json`, `.pem/.key/.p12/.pfx`, `.env`, …) and `BEGIN … PRIVATE KEY` blocks. Origin: 2026-06-03 gitignore hyphen bug nearly committed a real token (F17). Override `git commit --no-verify` ONLY for a confirmed false positive. |
| post-commit (graphify) | installed by `graphify hook install` (MUTATES) | Background rebuild of `graphify-out\graph.json`; log `~/.cache/graphify-rebuild.log`. **Known race bug:** rapid back-to-back commits corrupt-looking "Invalid control character" log errors (repo issue #3, upstream graphify#1037) — graph stays consistent, manual rebuild recipe is F11. Its 600s SIGALRM timeout is inert on Windows: a wedged rebuild runs unbounded (can pin CPU, won't block commits). |
| post-checkout (graphify) | same | Full rebuild on branch switch only. Same log, same caveats. |

Fresh clone / hooks missing? Reinstall both: `sh tools/hooks/install.sh` then
`graphify hook install` (both MUTATE `.git/hooks/`). Verify LOOK-ONLY:
`Get-ChildItem "D:\History vs Hype\.git\hooks" | Where-Object Name -notlike "*.sample"`.

## 3. MCP servers (7)

**Config:** there is NO project `.mcp.json`. Everything lives in `C:\Users\Benoi\.Codex.json`,
which has **two project keys**: `D:/History vs Hype` (forward-slash — the ACTIVE one) and
`D:\History vs Hype` (backslash — stale legacy; holds a dead `youtube-data` server with a
plaintext API key, see §5). Edits to the wrong key silently don't take effect. User scope
(top-level `mcpServers`): context7, notebooklm.

**Health check for everything — LOOK-ONLY:** `Codex mcp list` (run from the repo).
All six configured servers were ✔ connected at last audit (2026-07-01).

| Server | Role here | Health check (LOOK-ONLY) | Auth / recovery |
|---|---|---|---|
| notebooklm | Phase-2 academic verification (via `notebook-researcher` agent); coverage notebook `HvH-coverage-corpus` id `f3bc649e-b90e-4832-92d7-e1d4b9932dc4` | An authenticated call (`notebook_list`). **NEVER** trust `refresh_auth`/`server_info` — both false-report "expired" (0.6.14 bug, F8) | On `UNAUTHENTICATED`: `nlm login` via Bash (MUTATES token; auto-recover, don't ask), `nlm login --force` if stubborn → retry. Upload-only (`source_add(file)`) failure = stale CSRF: `nlm login --force` → SECOND `/mcp` reconnect → retry (F8). Query output is a synthesis layer that fabricates quotes — F9 before trusting any verbatim. |
| vidiq | Enrichment ONLY, below the packaging gates (ADR-0012/0013); generation suite = REJECT per identity guard; scores never decide | Listed ✔ in `Codex mcp list`; any cheap utility call (e.g. `vidiq_balance`) confirms auth | OAuth 2.0: `Codex mcp add --transport http vidiq https://mcp.vidiq.com/mcp` then complete the browser OAuth (MUTATES config + token). Boost plan, ~5 credits/call, 10 for Video Watch. Down / out of credits → manual in-app VidIQ with paste-ready prompts. Setup: `docs/VIDIQ-MCP-SETUP.md`; tool map: `docs/VIDIQ-MCP-CAPABILITY-MAP.md`. |
| graphify-code | AST code graph (node count grows with commits — 63K at the 2026-07-02 rebuild; see rebuild log) — preferred over grep for structural questions (AGENTS.md) | `mcp__graphify-code__graph_stats` | No auth. Freshness = post-commit hook (§2, race bug F11). Recovery/rollback table: `.Codex/REFERENCE/GRAPHIFY-OPS.md`. |
| graphify-research | Sparse research concept graph. DEPRECATED for coverage queries (notebook scored 10/10 vs graph 0/10) — kept for visualization | `mcp__graphify-research__graph_stats`; staleness marker `graphify-out\research\.needs_refresh` | No auth. Rebuild (MUTATES graph): `python tools/refresh-research-graph.py` (Gemini Flash; `--skip-gemini` rebuilds from existing JSON). Script path, not `-m` — the hyphen forbids it. |
| playwright | HTML-deck B-roll render verification, SERP/thumbnail studies | `browser_navigate` + `browser_snapshot` round-trip | No auth. Browsers missing → `playwright install` (MUTATES: downloads). |
| Codex-in-chrome | Drives the user's real Chrome (extension-based; NOT in `.Codex.json`) | `list_connected_browsers` | Permissions live in the Chrome extension, not this repo. |
| context7 | Library docs lookup (user scope) | any `resolve-library-id` call | No auth. |

## 4. External API surfaces

**YouTube Data + Analytics (OAuth).** Module: `tools/youtube_analytics/auth.py`. Credentials:
`tools/youtube_analytics/credentials/client_secret.json` + auto-written `token.json` (both
gitignored + secret-guard-backstopped). Expired token → silent refresh, no action. **Revoked**
refresh token → browser consent at `localhost:8080`, HUMAN-ONLY — a scheduled run cannot
complete it and gets limit-killed (F3). Wedged: delete `token.json`, run any analytics module
interactively to re-auth (MUTATES token). Health LOOK-ONLY: `token.json` mtime + newest
`growth-refresh-*.log`. Note: the Analytics API serves no CTR for this channel — CTR lives in
keywords.db `ctr_snapshots` via `python -m tools.youtube_analytics.ctr_tracker` (→ data-stores).

**yt-dlp.** Bot-walled since 2026-06-29 (HTTP 429 + botcheck); Chrome cookie extraction also
dead (App-Bound/DPAPI). Don't retry — go straight to the documented fallback chain in F10:
Data-API comments module → `youtube_transcript_api` → `videos.list(part='snippet')`.
(`/comment-mine`'s "ALWAYS yt-dlp" is outdated.)

**Gemini CLI** (`/gemini` command). Dispatch pattern:
`gemini -m gemini-2.5-flash -p "<prompt>" --yolo -o text > <out>` → outputs in `_gemini-output/`;
never read full output back into context. Flash is default; Pro needs explicit approval.
Auth: `~/.gemini/settings.json` → `security.auth.selectedType` MUST be `"gemini-api-key"` with
`GEMINI_API_KEY` set (User env var) — interactive logins/updates silently reset it to the dead
`oauth-personal` tier (F15). CLI down → emit a paste-ready `=== PASTE INTO GEMINI (Flash) ===`
web-UI block; NEVER silently re-route to another model.

**`nlm` CLI** (same pip package as the notebooklm MCP server). `nlm login [--check|--force]`
(MUTATES token) · `nlm notebook query <id> "<q>" --timeout 180` (verified: `notebook query`, NOT `query notebook`) · `nlm source content <source_id>`
(the raw-read verification path, F9). `PYTHONIOENCODING=utf-8` is already a User env var; prefix
it explicitly in one-off shells.

## 5. Where credentials live (security note)

Documented so you never go hunting — and never print or commit them. The pre-commit
secret-guard (§2) is the enforcement backstop, not permission to be careless.

| Credential | Location | Handling |
|---|---|---|
| YouTube OAuth client + token | `D:\History vs Hype\tools\youtube_analytics\credentials\` (`client_secret.json`, `token.json`) | Gitignored + guard-blocked. Check mtime, never cat contents into a transcript. |
| Gemini API key | `GEMINI_API_KEY` User env var | Never echo it. |
| NLM auth token | Managed entirely by `nlm login` (dedicated auth-Chrome profile) | Recover via the CLI only; don't locate/copy the token file. |
| VidIQ OAuth token | Held by Codex's MCP config after the browser flow | Re-auth via `Codex mcp add`, never by hand-editing. |
| ⚠ Plaintext YouTube API key | `C:\Users\Benoi\.Codex.json` under the STALE backslash project key (dead `youtube-data` server) | Known hygiene flag. Never print that file wholesale; when editing MCP config, target the forward-slash key. |

## 6. Admin gotchas (Windows)

- **Quote every path** — the repo root has a space. Git Bash form: `/d/History vs Hype/`.
- **Elevation:** `Register-ScheduledTask` with an `AtLogOn` trigger needs an elevated shell; daily-only triggers don't.
- **Two shells:** wrappers are PowerShell 7; git hooks are POSIX `sh`. Never mix syntaxes.
- **Task limits:** per-task execution limits (Reconcile PT10M, GrowthRefresh PT30M — raised from PT20M 2026-07-03 after a live 23.5-min run, CtrTracker PT20M, BrainHygiene/MorningCatchup PT1H; ChannelHealth/StaleProjects none set) + `IgnoreNew` instance policy — a long OAuth wait gets the shell killed (`0x41306`) while the child python may survive (F3: `Get-Process python`). All tasks start-on-battery + survive-unplug since 2026-07-03.
- **Timezone:** scheduler times are local (America/Lima, UTC-5); DB timestamps are UTC. Compare in UTC.
- **`.Codex\scheduled_tasks.lock`** has zero repo references — best hypothesis is a Codex harness mutex. Don't build on it.

## Related skills

- **debugging-playbook** — when any of the above is broken, stale, or "didn't run": it owns the evidence-first method, the F/T/D failure catalog, and the 2026-07-01 catch-up case study. Go there BEFORE re-running or re-registering anything.
- **data-stores** — when the question is what the automations read/write: DB schemas, the 36h freshness gate's semantics, refresh chains, AUTO-zone rules.
