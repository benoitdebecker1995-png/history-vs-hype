# Routine 6 wrapper — claude-driven daily reconcile (auto-publish-only).
# Invoked by Windows Scheduled Task "HvH-Reconcile" (Daily 08:30 + AtLogOn + StartWhenAvailable).
# Matches the sibling routine pattern (run-stale-projects.ps1 etc.): claude -p reads the routine .md
# and executes its EXECUTION DIRECTIVE (run `python -m tools.reconcile.reconcile --auto-publish-only` + summarize).
# Logs to .brain/_inbox/ so a missed/failed run is detectable (W3 2026-06-12: bare-python predecessor left no log + was never scheduled).
# Schedule logic: after Routine 7 HvH-GrowthRefresh (07:45, REFRESHES analytics.db, which reconcile's
# freshness gate depends on) and Routine 3 channel-health (08:00, reads it); before Routine 4 (09:00, reads post-reconcile state).

. "$PSScriptRoot\_lib-preflight.ps1"
Set-RepoRoot

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "reconcile-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 6 (claude-driven) run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

if (-not (Test-ClaudeAuth -LogFile $logFile)) {
    # DEGRADED MODE (2026-08-04). This routine's own directive says "the python tool does the
    # actual work; your job is to invoke it and report" — so a dead claude session should cost us
    # the prose summary, not the archiving. Between 2026-07-23 and 2026-08-04 it cost us both:
    # five published videos sat unarchived because the wrapper exited at this line.
    # --auto-publish-only is the narrow mode by construction (Tier-1/high-confidence publish
    # transitions only, freshness-gated, never touches memory snapshots) and every run writes a
    # .diff that `--undo` reverses.
    $msg = "AUTH DEGRADED: running the python reconcile directly; no model summary this run."
    Write-Host $msg
    $msg | Out-File -FilePath $logFile -Append -Encoding utf8

    $env:PYTHONIOENCODING = "utf-8"
    python -m tools.reconcile.reconcile --auto-publish-only --apply 2>&1 |
        Out-File -FilePath $logFile -Append -Encoding utf8
    $fallbackExit = $LASTEXITCODE

    if ($fallbackExit -eq 0) {
        "=== Exit code: 0 (degraded: archiving ran, summary skipped — fix with 'claude auth login --claudeai') ===" |
            Out-File -FilePath $logFile -Append -Encoding utf8
        exit 0
    }
    "=== Exit code: $fallbackExit (degraded fallback also failed) ===" |
        Out-File -FilePath $logFile -Append -Encoding utf8
    exit $fallbackExit
}

$prompt = (Get-Content ".claude\routines\reconcile-daily.md" -Raw)
$output = claude -p $prompt 2>&1
$exitCode = $LASTEXITCODE
$output | Out-File -FilePath $logFile -Append -Encoding utf8

# F1/F20: this wrapper only ever saw CLAUDE's exit code, so a failure inside
# `python -m tools.reconcile.reconcile` was invisible — claude exits 0 after reporting a
# python error in prose. Scan the captured output for the python failure signature and
# escalate, so a broken reconcile cannot report success. Exit 80 = inner python failed.
if ($exitCode -eq 0) {
    $innerFailure = $output | Select-String -Pattern 'Traceback \(most recent call last\)|ModuleNotFoundError|reconcile (?:failed|aborted)|sqlite3\.\w*Error' -Quiet
    if ($innerFailure) {
        $msg = "PREFLIGHT FAIL: claude exited 0 but its output contains a python failure signature — treating as failed."
        Write-Host $msg
        $msg | Out-File -FilePath $logFile -Append -Encoding utf8
        $exitCode = 80
    }
}

"=== Exit code: $exitCode ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
