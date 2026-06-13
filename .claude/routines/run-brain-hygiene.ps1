# Routine 5 wrapper — nightly brain hygiene + index maintenance (claude-driven).
# Invoked by Windows Scheduled Task "HvH-BrainHygiene" daily 22:00.
# Logs claude -p output + exit code to .brain/_inbox/ so an abort is DIAGNOSABLE.
# (Before 2026-06-13 this was bare `claude -p $prompt` with no capture — the 2026-06-11
#  ERROR_PROCESS_ABORTED run left zero diagnostics, which is why W3 couldn't see the cause.)

Set-Location "D:\History vs Hype"

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = Join-Path $logDir "brain-hygiene-run-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 5 brain-hygiene run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

$prompt = (Get-Content ".claude\routines\brain-hygiene.md" -Raw)
claude -p $prompt 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode @ $(Get-Date -Format 'HH:mm:ss') ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
