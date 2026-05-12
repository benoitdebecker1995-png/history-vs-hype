# Routine 6 — Daily Reconcile

**Purpose:** Archive any newly-uploaded YouTube videos that the conversational trigger missed, and keep derived docs (root `PROJECT_STATUS.md`, `PROJECT_REGISTRY.md`, `.brain/index.md §3`) in sync with reality. Narrower than interactive `/reconcile` — never touches memory snapshots or MEMORY.md.

**Triggers (intermittent-PC resilient):**
- Daily 08:30 (primary) — after 08:00 channel-health-snapshot refreshes `analytics.db`, before 09:00 stale-project-nudge reads project state
- `StartWhenAvailable` — if PC was off at 08:30, runs as soon as the machine wakes
- `AtLogOn` — runs at user login (catches the case where the PC stays off for multiple days). Task is idempotent — running twice in a day is a no-op when state is clean.

**Why Desktop:** Reads local filesystem, writes to local `.brain/_inbox/`, executes folder moves via `shutil.move`.
**Expected cost:** 1 of the 5 daily Routines credits, sometimes 0 (no-op if no new state).

---

## What it does

```
python -m tools.reconcile.reconcile --auto-publish-only
```

This mode:

1. **Freshness gate.** Reads `analytics.db` max `metrics_fetched_at`. If older than 36h, aborts and writes alert to `.brain/_inbox/reconcile-stale-db-YYYY-MM-DD.md`. (Catches the case where Routine 3 channel-health-snapshot at 08:00 silently failed and analytics.db is stale.)

2. **Scan.** Enumerates `_IN_PRODUCTION/`, `_READY_TO_FILM/`, `_ARCHIVED/published/`. Detects phase per folder.

3. **Match.** For each folder, runs the 3-tier matcher: manual overrides → Tier 1 Video ID extraction → Tier 2 fuzzy. **Only Tier 1 + high-confidence Tier 2 matches are eligible for auto-archive.** Gray-zone (0.5–0.85) and no-match folders are LOGGED, not acted upon.

4. **Apply only publish transitions.** Filter proposals to `target_bucket == _ARCHIVED/published` with confidence in (`tier1`, `high`). All other transitions (script-lock, filming, fact-check moves) are LOGGED but skipped — waiting for the next interactive `/reconcile`.

5. **NEVER touches memory snapshots or MEMORY.md.** Even when archiving a folder, the corresponding `memory/[N]-production-state.md` and its MEMORY.md index line are left untouched. The log notes "snapshot for #X still active — run /reconcile to promote lessons + delete."

6. **Writes:**
   - Folder moves (`shutil.move`)
   - AUTO:reconcile blocks in each archived folder's `PROJECT-STATUS.md`
   - Root `video-projects/PROJECT_STATUS.md` regenerated
   - Root `video-projects/PROJECT_REGISTRY.md` regenerated
   - `.brain/_inbox/reconcile-YYYY-MM-DD-HHMM.diff` (machine-readable; consumed by `--undo`)
   - `.brain/_inbox/reconcile-YYYY-MM-DD.md` (human-readable summary)
   - `.brain/last-reconcile-ts.txt`

---

## Paste into Desktop Scheduled Task (PowerShell wrapper)

```powershell
# Wrapper: D:\History vs Hype\.claude\routines\run-reconcile.ps1
Set-Location "D:\History vs Hype"
python -m tools.reconcile.reconcile --auto-publish-only 2>&1 |
    Out-File -FilePath ".brain\_inbox\reconcile-$(Get-Date -Format 'yyyy-MM-dd').log" -Append -Encoding utf8
```

## Setup (Windows Task Scheduler — admin PowerShell)

```powershell
# Intermittent-PC-resilient: daily 08:30 + at-logon backup + start-when-available catch-up.
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"D:\History vs Hype\.claude\routines\run-reconcile.ps1`"" `
    -WorkingDirectory "D:\History vs Hype"

$dailyTrigger = New-ScheduledTaskTrigger -Daily -At "08:30"
$logonTrigger = New-ScheduledTaskTrigger -AtLogOn
# Delay logon trigger by 2 min so the OS has settled before we hit it
$logonTrigger.Delay = "PT2M"

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName "HvH-Reconcile" `
    -Action $action `
    -Trigger @($dailyTrigger, $logonTrigger) `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Get-ScheduledTask -TaskName "HvH-Reconcile" | Get-ScheduledTaskInfo |
    Format-List TaskName, NextRunTime, State, LastRunTime
```

### Resilience notes

- **`StartWhenAvailable`** — Windows tracks missed runs. If your PC was off at 08:30, the task fires when the PC wakes.
- **`AtLogOn` with 2-min delay** — runs at every user login. Belt-and-braces if `StartWhenAvailable` somehow misses (e.g. PC stayed off for days, wake didn't catch up). 2-minute delay lets the OS settle (services start, network up) before reconcile reads analytics.db.
- **`MultipleInstances IgnoreNew`** — if a previous run is still going when a new trigger fires, the new trigger is ignored (no double-run race).
- **Idempotent script** — even if both daily AND at-logon fire on the same day, the second run is a no-op (`No changes needed. Everything reconciled.`).

### Verify after registering

```powershell
Get-ScheduledTask -TaskName "HvH-Reconcile" | Get-ScheduledTaskInfo
# Expect: State=Ready, NextRunTime in the future, no errors.
```

## Guardrails

- **Never** edits `memory/*-production-state.md` or MEMORY.md.
- **Never** moves a folder unless match confidence is `tier1` or `high` (≥0.85). Gray-zone matches are logged only.
- **Never** auto-archives a folder whose phase doesn't independently signal published OR filmed (i.e., something on disk corroborates the analytics.db match).
- **Never** pushes to git — local state changes only. User reviews `git status` for the resulting moves and edits, then commits when they want.
- If freshness gate trips (analytics.db >36h stale): write alert, exit code 2, no state changes.
- If anything else fails partway: the `.pre-diff` backups + diff log allow `/reconcile --undo` recovery.

## Interpreting results

- **No new publishes today:** silent. No file written beyond a brief log line.
- **1+ folders archived:** diff log written. Run `/reconcile` interactively to promote lessons from newly-archived memory snapshots before they accumulate.
- **Freshness alert:** Routine 3 likely failed. Check `tools/youtube_analytics/` auth and `analytics.db` `metrics_fetched_at` timestamps.
