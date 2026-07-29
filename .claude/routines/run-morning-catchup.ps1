# HvH-MorningCatchup — ordered catch-up chain, fired AT LOGON (2-min delay).
# Created 2026-07-03. Problem it solves: scheduled tasks can't run while the laptop is off,
# and Windows' own StartWhenAvailable catch-up fires ALL missed tasks SIMULTANEOUSLY on wake,
# breaking the 07:30→07:45→08:00→08:30→09:00 data-dependency ordering (the "catch-up storm",
# F2 in debugging-playbook — observed live 2026-07-01/02: reconcile stale-aborted because it
# ran at the same instant as the refresh it depends on).
#
# Design: evidence-based + sequential. Each step runs ONLY if today's success evidence is
# missing, in dependency order. Safe to fire on every logon — converges to a no-op once the
# day's chain is complete. BrainHygiene (22:00) is deliberately NOT included: catching an
# evening task up at morning logon would run it at the wrong time of day; its own
# StartWhenAvailable handles it.

. "$PSScriptRoot\_lib-preflight.ps1"
Set-RepoRoot

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$today   = Get-Date -Format 'yyyy-MM-dd'
$logFile = Join-Path $logDir "morning-catchup-$today.log"

function Log([string]$msg) {
    "$(Get-Date -Format 'HH:mm:ss') $msg" | Out-File -FilePath $logFile -Append -Encoding utf8
}

function StepDone([string]$evidenceLog) {
    # Done today iff the wrapper log's MOST RECENT exit-code line is 0. Parsing the
    # last "=== Exit code: N ===" (rather than substring-matching "0 ===") is
    # tolerant of the trailing "@ HH:mm:ss" that channel-health/stale-projects
    # append — that format drift made those two steps never register as done and
    # re-run on every logon (2026-07 audit) — and checking the LAST line means an
    # earlier success no longer masks a later failure the same day.
    $p = Join-Path $logDir $evidenceLog
    if (-not (Test-Path $p)) { return $false }
    # @(...) forces an array: with a single exit-code line, an unwrapped scalar
    # string would make $codes[-1] index the last CHARACTER (e.g. "10" -> "0"),
    # falsely reading a failed step as done.
    $codes = @(Select-String -Path $p -Pattern '=== Exit code: (\d+)' -AllMatches |
             ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value })
    if ($codes.Count -eq 0) { return $false }
    return ($codes[-1] -eq '0')
}

$failed = $false

Log "=== Morning catch-up chain start (logon trigger) ==="

# Step 0 (Mondays only) — CTR tracker (writes keywords.db; feeds channel-health CTR baseline)
if ((Get-Date).DayOfWeek -eq 'Monday') {
    if (StepDone "ctr-tracker-$today.log") { Log "ctr-tracker: already ran today - skip" }
    else {
        Log "ctr-tracker: missing - running"
        & pwsh -File "$PSScriptRoot\run-ctr-tracker.ps1"
        Log "ctr-tracker: exit $LASTEXITCODE"
        if ($LASTEXITCODE -ne 0) { $failed = $true }
    }
}

# Step 1 — analytics.db refresh (everything downstream reads this)
if (StepDone "growth-refresh-$today.log") { Log "growth-refresh: already ran today - skip"; $growthOk = $true }
else {
    Log "growth-refresh: missing - running"
    & pwsh -File "$PSScriptRoot\run-growth-refresh.ps1"
    Log "growth-refresh: exit $LASTEXITCODE"
    $growthOk = ($LASTEXITCODE -eq 0)
    if (-not $growthOk) { $failed = $true }
}

# Steps 2 & 3 READ analytics.db — fail-fast: if the refresh isn't in place this run,
# skip them rather than snapshot/reconcile against stale-or-missing data. They catch
# up on the next logon once the refresh succeeds.
if (-not $growthOk) {
    Log "channel-health + reconcile: SKIPPED — analytics.db refresh not complete this run"
}
else {
    # Step 2 — channel-health snapshot (reads analytics.db; silent unless anomaly)
    if (StepDone "channel-health-run-$today.log") { Log "channel-health: already ran today - skip" }
    else {
        Log "channel-health: missing - running"
        & pwsh -File "$PSScriptRoot\run-channel-health.ps1"
        Log "channel-health: exit $LASTEXITCODE"
        if ($LASTEXITCODE -ne 0) { $failed = $true }
    }

    # Step 3 — reconcile (freshness-gates on analytics.db; success advances the heartbeat).
    # Heartbeat is the true marker: a stale-abort leaves it behind even when the wrapper exits 0.
    $hb = ".brain\last-reconcile-ts.txt"
    $reconcileDone = (Test-Path $hb) -and ((Get-Content $hb -Raw) -match "^$today")
    if ($reconcileDone) { Log "reconcile: heartbeat already today - skip" }
    else {
        Log "reconcile: heartbeat not today - running"
        & pwsh -File "$PSScriptRoot\run-reconcile.ps1"
        Log "reconcile: exit $LASTEXITCODE"
        if ($LASTEXITCODE -ne 0) { $failed = $true }
    }
}

# Step 4 — stale-project nudge (reads project STATE, not analytics.db — runs regardless)
if (StepDone "stale-projects-run-$today.log") { Log "stale-projects: already ran today - skip" }
else {
    Log "stale-projects: missing - running"
    & pwsh -File "$PSScriptRoot\run-stale-projects.ps1"
    Log "stale-projects: exit $LASTEXITCODE"
    if ($LASTEXITCODE -ne 0) { $failed = $true }
}

Log "=== Morning catch-up chain complete (failed=$failed) ==="
if ($failed) { exit 1 } else { exit 0 }
