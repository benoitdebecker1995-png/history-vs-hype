# Routine 7 wrapper — refresh analytics.db from the YouTube Data + Analytics APIs.
# Invoked by Windows Scheduled Task "HvH-GrowthRefresh" daily at 07:45 — BEFORE Routine 3
# channel-health (08:00, reads the DB) and Routine 6 reconcile (08:30, freshness-gates on it).
# This is a pure data pipeline (no claude): it writes `metrics_fetched_at` via store.upsert_video.
# Created 2026-06-13: nothing previously refreshed analytics.db on a schedule, so it went >36h stale
# and reconcile's freshness gate no-op'd every run (debug session 2026-06-13).
# Logs to .brain/_inbox/ so a missed/failed refresh is visible.

Set-Location "D:\History vs Hype"

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = Join-Path $logDir "growth-refresh-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 7 growth_data --refresh @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

python -m tools.youtube_analytics.growth_data --refresh 2>&1 |
    Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
