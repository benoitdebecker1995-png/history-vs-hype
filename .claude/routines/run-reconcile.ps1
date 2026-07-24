# Routine 6 wrapper — claude-driven daily reconcile (auto-publish-only).
# Invoked by Windows Scheduled Task "HvH-Reconcile" (Daily 08:30 + AtLogOn + StartWhenAvailable).
# Matches the sibling routine pattern (run-stale-projects.ps1 etc.): claude -p reads the routine .md
# and executes its EXECUTION DIRECTIVE (run `python -m tools.reconcile.reconcile --auto-publish-only` + summarize).
# Logs to .brain/_inbox/ so a missed/failed run is detectable (W3 2026-06-12: bare-python predecessor left no log + was never scheduled).
# Schedule logic: after Routine 7 HvH-GrowthRefresh (07:45, REFRESHES analytics.db, which reconcile's
# freshness gate depends on) and Routine 3 channel-health (08:00, reads it); before Routine 4 (09:00, reads post-reconcile state).

Set-Location "D:\History vs Hype"

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "reconcile-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 6 (claude-driven) run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

$prompt = (Get-Content ".claude\routines\reconcile-daily.md" -Raw)
claude -p $prompt 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
