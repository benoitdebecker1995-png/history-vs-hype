# Routine 6 wrapper — runs reconcile in auto-publish-only mode.
# Invoked by Windows Scheduled Task "HvH-Reconcile" daily at 08:30.
# Schedule logic: after Routine 3 (08:00, refreshes analytics.db),
# before Routine 4 (09:00, stale-project-nudge reads post-reconcile state).

Set-Location "D:\History vs Hype"

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "reconcile-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 6 reconcile run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

python -m tools.reconcile.reconcile --auto-publish-only 2>&1 |
    Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode ===" | Out-File -FilePath $logFile -Append -Encoding utf8

exit $exitCode
