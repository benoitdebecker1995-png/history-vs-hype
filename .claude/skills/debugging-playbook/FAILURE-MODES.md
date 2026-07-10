# Failure-Mode Catalog — symptom → check → cause → fix

Companion to [SKILL.md](SKILL.md). Every row was live-verified or incident-sourced on
2026-07-01 (ops/data/code inventories) unless marked `[UNVERIFIED]`. Row IDs are stable —
cite them ("this is F9") in reports and when adding cross-references.

Run all `python -m …` commands from the repo root `D:\History vs Hype`. Quote every path.

## F-rows — automation, auth, external APIs

| # | Symptom | Check (evidence) | Cause | Fix |
|---|---|---|---|---|
| F1 | Reconcile writes `.brain\_inbox\reconcile-stale-db-YYYY-MM-DD.md`, exit 2, no folder moves | analytics.db freshness one-liner (SKILL.md evidence map); newest `growth-refresh-*.log` | `MAX(metrics_fetched_at)` in `tools\youtube_analytics\analytics.db` > 36h — the 07:45 refresh didn't run (PC off) or failed (auth, F3). NOTE: the alert text blames "Routine 3" — stale wording; the refresher is Routine 7 (see D4) | `python -m tools.youtube_analytics.growth_data --refresh`, then re-run `python -m tools.reconcile.reconcile --auto-publish-only` (or `/reconcile`) |
| F2 | All morning HvH-* tasks show IDENTICAL LastRunTime; reconcile stale-aborted even though the refresh ran the same minute | `Get-ScheduledTask -TaskName "HvH-*" \| Get-ScheduledTaskInfo`; then walk F1's checks | PC off at trigger times → `StartWhenAvailable` catch-up fires ALL tasks simultaneously; the 07:45→08:30 ordering only exists on-schedule. Observed live 2026-07-01 (full worked case study in SKILL.md) | Immediate: after refresh completes, re-run reconcile (F1 fix). Structural (BUILT 2026-07-03): `HvH-MorningCatchup` (logon + daily 10:30 sweeper) re-runs missing steps IN ORDER, evidence-gated — a storm-broken morning self-heals by 10:30. If storms still leave the day broken, check that task's `morning-catchup-*.log` |
| F3 | `growth-refresh-*.log`: "Refresh token revoked — need full re-authorization" / "Opening browser…"; task LastResult `0x41306` | log + `token.json` mtime (`tools\youtube_analytics\credentials\token.json`) | Google OAuth refresh token revoked (periodic); a scheduled context can't finish the browser flow; the task's execution limit kills the shell while python waits (per-task limits verified 2026-07-03: Reconcile PT10M, GrowthRefresh PT30M, CtrTracker PT20M, BrainHygiene PT1H) | A human completes browser consent at `localhost:8080`; `token.json` auto-rewrites. Wedged: delete `token.json`, run any analytics module interactively to re-auth. After an `0x41306` kill, check for a surviving child python (`Get-Process python`). HUMAN-ONLY — never loop on this headless |
| F4 | Routine log: "You've hit your session limit · resets HH:MM", exit 1 | the `.brain\_inbox` run log for that routine | `claude -p` routines share the Claude Pro usage cap with interactive work | Nothing to fix in code; rerun after reset. Recurring at 22:00 → propose moving the BrainHygiene slot |
| F5 | Routine exits 0 but did nothing; a NEW routine "greets and exits" | run log shows greeting text instead of tool output | (Historical, fixed 2026-06-13, commit `afbe6d3`.) Routine .md read as documentation; headless claude lacked `.brain/**` write permission | Any NEW routine needs all three: "▶ EXECUTION DIRECTIVE" atop its .md, scoped `Edit/Write(.brain/**)` allow-rules, wrapper logging output + exit code |
| F6 | Reconcile no-ops daily; channel-health silently useless | (Historical, fixed 2026-06-13, commit `1518e67`) | Nothing refreshed analytics.db on any schedule; channel-health queried a non-existent table at the wrong DB path | Fixed (Routine 7 created; query repointed). Kept as a lesson: a read-only consumer can be "green" for weeks while reading garbage — verify the WRITER exists |
| F7 | Task LastResult `0x800710E0` ("operator or administrator has refused the request") on ChannelHealth / StaleProjects | scheduler ground truth + the task's `.brain\_inbox` run log (did it actually execute?) | `[UNVERIFIED]` — appeared during the 2026-07-01 catch-up storm; plausibly task settings refusing the catch-up-style launch. Recurs | Needs a live debug: `Export-ScheduledTask` settings review. Meanwhile run the wrapper `.ps1` manually and treat the run log as truth, not the result code |
| F8 | NLM MCP call fails `UNAUTHENTICATED`; or ONLY `source_add(file)` fails while reads work | an authenticated call (`notebook_list`) — NEVER `refresh_auth`/`server_info`, both false-report "expired" (0.6.14 bug) | NotebookLM auth expires constantly. Upload-only failure = stale CSRF after upgrade/reconnect | Auto-recover, don't ask: `nlm login` (then `--force` if needed) → retry. CSRF variant: `nlm login --force` → SECOND `/mcp` reconnect → retry. Full flow: memory `feedback-nlm-auth-autorecover` (its body agrees; its stale index one-liner suggesting refresh_auth-first was corrected 2026-07-03) |
| F9 | `notebook_query` returns confident verbatim quotes + page numbers | the response's `sources_used` field — EMPTY = unverified. Caught live on #62: two invented Polish Motyka quotes | `notebook_query` is a synthesis layer; it fabricates verbatim + pages, worst on leading prompts | Load-bearing quotes: read the RAW source via `nlm source content <source_id>` and confirm the actual words (Claude reads PL/UA directly). Query = discovery only. See memory `reference-nlm-raw-read-verification` |
| F10 | yt-dlp: HTTP 429 + "Sign in to confirm you're not a bot"; `--cookies-from-browser chrome` → "Failed to decrypt with DPAPI" | reproduce once; don't retry-loop | YouTube bot-wall on this IP (since 2026-06-29); Chrome App-Bound cookie encryption. BOTH dead ends | Documented fallback chain: comments → `python -m tools.youtube_analytics.comments VIDEO_ID --max-comments N` (Data API, OAuth); transcripts → `youtube_transcript_api` (pip; request `languages=['pl','uk','ru','en']` as needed); descriptions → Data API `videos.list(part='snippet')`. `/comment-mine`'s "ALWAYS yt-dlp" is outdated |
| F11 | `~/.cache/graphify-rebuild.log`: "Invalid control character at line X col 41" | the log; graph queries still answering (`mcp__graphify-code__graph_stats`) | Post-commit hook race on `graphify-out\graph.json` with rapid back-to-back commits (repo issue #3, upstream graphify#1037). Graph stays internally consistent | Manual rebuild always works (Git Bash): `python -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'), changed_paths=[Path('CLAUDE.md')], force=False)"` |
| F12 | Temptation to run `graphify extract --backend ollama` | — | Dead end on this laptop (smoke-tested 2026-05-26): gemma3:4b can't emit valid JSON; qwen2.5:7b minutes-per-chunk on CPU | AST-only for the code graph; Gemini Flash (`python tools/refresh-research-graph.py` — script path, hyphen forbids `-m`) for the research graph. Don't re-test |
| F13 | `/retitle` audit surfaces already-retitled or dormant videos, `video_id = None` | compare its output against `keywords.db` → `ctr_snapshots` (SKILL.md evidence map one-liner) | It parses `channel-data\patterns\CROSS-VIDEO-SYNTHESIS.md` — bulk generated 2026-03-07, appended piecemeal since (stale bulk + appends, not current) | Query real CTR first: `ctr_snapshots` (video_id, ctr_percent, impression_count, snapshot_date). Prioritize videos with live impressions |
| F14 | `ctr_snapshots` stale (>10 days old) | `MAX(snapshot_date)` one-liner | HISTORICAL cause fixed 2026-07-03: nothing scheduled `ctr_tracker`, so it froze 18 days. Now scheduled: `HvH-CtrTracker`, weekly Mon 07:30 (`run-ctr-tracker.ps1`). If stale AGAIN → the task failed: check `ctr-tracker-*.log` + `Get-ScheduledTaskInfo` | `python -m tools.youtube_analytics.ctr_tracker` manually to unfreeze, then diagnose the task per F7/F3 |
| F15 | Gemini CLI: `IneligibleTierError` / auth failures | `~/.gemini/settings.json` → `security.auth.selectedType` | Reset to `"oauth-personal"` (dead tier — interactive login/updates silently revert it), or `GEMINI_API_KEY` env var missing | Set `selectedType: "gemini-api-key"` + confirm the env var. CLI still down → output a paste-ready `=== PASTE INTO GEMINI (Flash) ===` web-UI block; NEVER silently re-route to another model |
| F16 | Mojibake (`ΓÇö` for —) in `.brain\_inbox` logs; historical `UnicodeEncodeError: 'charmap' can't encode '✓'` | read the log with a UTF-8-aware reader | UTF-8 output vs cp1252 Windows console | Cosmetic, not corruption. Root fix in place: `PYTHONIOENCODING=utf-8` User env var; prefix explicitly in one-off shells |
| F17 | A credential-looking file is staged / nearly commits | `git status`; the pre-commit secret-guard should block | 2026-06-03 origin: `.gitignore` had `youtube-analytics` (hyphen) vs real `youtube_analytics` (underscore) — dead ignore path | Guard installed via `sh tools/hooks/install.sh`. Lesson: verify ignore paths against REAL paths. Never `--no-verify` past the guard except a confirmed false positive |
| F18 | Cloud Routines 1–2 (competitor-drop / modern-relevance) produce no RECENT dated files (manual runs exist through 2026-05-09) | `channel-data\competitor-drops\`, `channel-data\modern-relevance\` | Never registered as scheduled cloud agents (W3 audit); the python scanners work when run manually `[UNVERIFIED recently]` | Register via the `schedule` skill (owner's call) or downgrade the docs' claims — don't leave docs asserting automation that doesn't exist |
| F19 | Analytics API intermittent `HttpError 500 backendError` on per-video search-term fetch | the refresh log (seen 2026-06-29) | Google-side transient | Per-video loops already catch and skip. Ignore unless persistent across runs — then it's not this row |
| F20 | Reconcile exit 0, DB fresh, heartbeat advanced — but a published upload never archived | newest `.brain\_inbox\reconcile-YYYY-MM-DD.log` for "gray-zone" / "fuzzy-matched" / "LOGGED" | Fuzzy title match below auto-archive confidence — only tier1/high acts; 0.5–0.85 is logged, not acted | FIRST verify the match is real — compare the video's `published_at` against the project's timeline; gray-zone can be a FALSE positive (2026-07-02: #59, still unpublished, fuzzy-matched 0.50 to a folder-less 2025 video — resolved as false, noted in manual-matches.json). If real: add the Video ID to the folder's PROJECT-STATUS.md or a `manual-matches.json` entry (`null` = never-match; → data-stores), then `/reconcile <slug>` interactively |
| F21 | Channel-health alerts absent or nonsensical even when metrics clearly moved | `Test-Path "D:\History vs Hype\channel-data\stats.md"` → False | HISTORICAL (fixed 2026-07-03): routine STEP 1 used to read `channel-data/stats.md`, which never existed, so the 1.5σ comparison ran baseline-less. STEP 1 now COMPUTES the baseline live (AVD/retention from analytics.db `videos`, CTR from channel-filtered `ctr_snapshots`, 14-day staleness skip) | If alerts look wrong now, run STEP 1's two baseline queries by hand (they're in `.claude/routines/channel-health-snapshot.md`) and check n + newest_snapshot in their output |

## T-rows — test & tooling traps (full run commands → validation-standards skill)

| # | Symptom | Check | Cause | Fix |
|---|---|---|---|---|
| T1 | `python tools\title_scorer.py --help` → `ModuleNotFoundError: No module named 'tools'` | reproduce (1s) | No sys.path bootstrap; intra-repo `tools.*` imports | `python -m tools.title_scorer --help` from repo root. Assume for ALL repo modules: `-m` from root, always |
| T2 | pytest "all green" but repo-side suites never executed | `python -m pytest --collect-only -q` and look for `tools/` paths | `testpaths` in pyproject = `tests/` only; `tools/tests/`, `tools/script_checkers/tests/`, `tools/research/test_opener_diagnostic.py` need explicit paths | Pass the extra paths explicitly when your change touches those areas. "I ran the tests" without them is a false claim |
| T3 | pytest collection errors / INTERNALERROR from `tools\youtube_analytics\` | run collection from repo root, not inside the dir | 3 files error at collection (bare imports); modules' own `except ImportError: sys.exit(1)` can kill the collector. Working twins live in `tests/unit/` | Run the `tests/unit/` twins. Documented root fix (conftest + re-raise instead of sys.exit) is still UNAPPLIED — applying it properly beats avoiding the dir forever |
| T4 | `.pytest_cache` WinError 5 (Permission denied); `find`/walks die on `tools\youtube_analytics\.pytest_cache` | reproduce | Unwritable cache dir | Always pass `-p no:cacheprovider`; exclude that dir from filesystem walks |
| T5 | `tests\unit\test_retention_scorer.py` skips forever | read its `skipUnless` guard | Targets `tools\youtube_analytics\retention_scorer.py` which does NOT exist — TDD suite for unimplemented behavior | Leave it. "Fixing" the import un-skips tests for code that was never written. Not a broken test — a placeholder |

## D-rows — data-layer diagnostics (semantics → data-stores skill)

| # | Symptom | Check | Cause | Fix |
|---|---|---|---|---|
| D1 | `git status` shows `analytics.db` / `keywords.db` / `intel.db` modified after running any tool | expected — confirm no `-wal`/`-shm` sidecars linger | The three live DBs are git-tracked; WAL mode; any tool run dirties them | Normal. Never commit a mid-write snapshot; tests stay on `:memory:`/`tmp_path`; inspect with `mode=ro` URIs. Committed DB copies LAG local — never trust a checked-out .db for freshness |
| D2 | KBStore queries return empty on a DB you just populated in a test | you used `:memory:` | `KBStore` opens per-call connections — each call gets a FRESH empty in-memory DB. (`KeywordDB` accepts `:memory:` fine) | Use a temp FILE for KBStore tests (conftest codifies this) |
| D3 | Freshness check returns exactly `999` (hours or days) | try the read manually with the `mode=ro` one-liner | 999 is the "can't read" SENTINEL in both `analytics_db_age_hours()` and `check_db_freshness()` — missing file, lock, or permission error looks IDENTICAL to a stale DB | Diagnose the read failure first (path? lock? perms?). Reconcile aborts exit-2 either way, so don't assume "stale" from the alert alone |
| D4 | Docs/alerts blame "Routine 3" for a stale analytics.db | — | `reconcile.py`'s alert text + `run-reconcile.ps1` line 6 predate the 2026-06-13 fix | The refresher is Routine 7 `HvH-GrowthRefresh` (07:45); Routine 3 only READS. Trust `reconcile-daily.md` / `channel-health-snapshot.md` (corrected). Fixing the stale strings is a welcome one-line PR |

## Reproduction & verification recipes (the majors)

**F1/F2 — stale-DB chain.** Reproduce: read the freshness one-liner; if >36h, running
`python -m tools.reconcile.reconcile --auto-publish-only` will abort exit 2 and write the
alert (safe — no state changes on abort). Verify the fix: after `growth_data --refresh`,
the one-liner returns a timestamp minutes old; re-run reconcile; confirm exit 0 AND
`.brain\last-reconcile-ts.txt` advanced. Wrapper exit codes lie (claude's 0 masks python's 2)
— the artifact files are the verdict.

**F3 — OAuth revocation.** Recognize, don't reproduce: the growth-refresh log line +
`0x41306` + old `token.json` mtime. Verify recovery: `token.json` mtime is now current AND a
fresh `growth_data --refresh` completes without the browser prompt.

**F8/F9 — NLM auth + fabrication.** Reproduce F8's false-negative trap: `refresh_auth` may
say "expired" while `notebook_list` succeeds — only the authenticated call counts. F9 spot
check on any load-bearing quote: does the response name non-empty `sources_used`? Then does
`nlm source content <id>` contain the words verbatim? Both yes or the quote doesn't ship.

**F10 — yt-dlp wall.** One attempt to confirm the 429/botcheck text, then straight to the
Data-API fallbacks. Verify: the fallback module produced the file you needed (read it).

**F11 — graphify race.** Signature: JSON control-character error in the rebuild log seconds
after two rapid commits. Verify after manual rebuild: `mcp__graphify-code__graph_stats`
answers and the log's newest rebuild entry is clean.

**F13/F14 — stale-number traps.** Reproduce: run the consumer, then check the source's own
date (`snapshot_date` max, or the snapshot file's header date). Any tool citing a number
older than its decision window gets its input refreshed BEFORE its output is used — this is
the vintage check from SKILL.md anti-pattern 6.

**T1–T4 — pytest traps.** Each reproduces in seconds with the command in its row; that IS
the check. Before claiming a test result, state which paths you collected (T2).

## Adding a row

A failure diagnosed twice, or once with >30 min of diagnosis, earns a row: stable ID
(next free F/T/D number), symptom in the words you'd grep for, the CHEAPEST decisive check,
root cause (dated incident if known), and the root-cause fix — never the workaround you
used under time pressure. Keep `[UNVERIFIED]` markers honest; a wrong row is worse than no row.
