# Routine 8 wrapper — DAILY CTR/impressions collection from the YouTube Reporting API.
# Invoked by Windows Scheduled Task "HvH-CtrTracker" DAILY 14:30, ahead of the rest of the
# chain, so channel-health computes its CTR baseline from a same-day snapshot.
#
# WHY DAILY (changed 2026-07-28 — it was weekly Mondays, and that cost us a launch window):
#   Reporting API retention is only ~60 days, and `impressions_daily` is the ONLY durable
#   record of what a video did on a given day. Video #59 published Sunday 2026-07-05; the
#   next Monday run missed, so days 0-4 were never captured — and 88% of that video's
#   lifetime impressions landed on day 1. The rolling figure in ctr_snapshots cannot
#   reconstruct a launch window, so a missed day used to be permanent data loss.
#   Ingest is now idempotent by DATA date, so a missed run self-heals on the next one
#   while those days are still inside retention. Daily is what keeps that guarantee real.
#   NOTE: nothing is gained by running more often than daily — the API publishes one
#   report per day.
#
# Created 2026-07-03: ctr_snapshots froze for 18 days (2026-06-15 → 2026-07-03) because
# nothing scheduled ctr_tracker; the freeze silently staled title_scorer's live-CTR
# enrichment and the channel-health CTR baseline (F14 in debugging-playbook).
# Writes tools/discovery/keywords.db (ctr_snapshots + impressions_daily). Logs to .brain/_inbox/.

. "$PSScriptRoot\_lib-preflight.ps1"
Set-RepoRoot

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
