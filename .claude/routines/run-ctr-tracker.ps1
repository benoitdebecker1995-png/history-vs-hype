# Routine 8 wrapper — weekly CTR/impressions snapshot from the YouTube Analytics API.
# Invoked by Windows Scheduled Task "HvH-CtrTracker" weekly Monday 07:30 — BEFORE the
# morning chain (07:45 GrowthRefresh, 08:00 channel-health, 08:30 reconcile), so Monday's
# channel-health computes its CTR baseline from a same-morning snapshot.
# Created 2026-07-03: ctr_snapshots froze for 18 days (2026-06-15 → 2026-07-03) because
# nothing scheduled ctr_tracker; the freeze silently staled title_scorer's live-CTR
# enrichment and the channel-health CTR baseline (F14 in debugging-playbook).
# Writes tools/discovery/keywords.db (ctr_snapshots). Logs to .brain/_inbox/.

Set-Location "D:\History vs Hype"

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = Join-Path $logDir "ctr-tracker-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 8 ctr_tracker @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

python -m tools.youtube_analytics.ctr_tracker 2>&1 |
    Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
