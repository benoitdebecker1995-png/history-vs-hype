# Routine 3 wrapper — daily channel-health snapshot (claude-driven).
# Invoked by Windows Scheduled Task "HvH-ChannelHealth" daily 08:00.
# Logs claude -p output + exit code to .brain/_inbox/ so a no-op greeting or abort is DIAGNOSABLE
# (before 2026-06-13 this was bare `claude -p $prompt` with no capture; the routine .md lacked an
#  execution directive, so claude -p greeted-and-exited instead of running — fixed in the .md).

. "$PSScriptRoot\_lib-preflight.ps1"
Set-RepoRoot

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = Join-Path $logDir "channel-health-run-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 3 channel-health run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

if (-not (Test-ClaudeAuth -LogFile $logFile)) {
    "=== Exit code: $EXIT_AUTH_EXPIRED (auth pre-flight) @ $(Get-Date -Format 'HH:mm:ss') ===" |
        Out-File -FilePath $logFile -Append -Encoding utf8
    exit $EXIT_AUTH_EXPIRED
}

$prompt = (Get-Content ".claude\routines\channel-health-snapshot.md" -Raw)
$claudeExe = Resolve-ClaudeExe -LogFile $logFile
& $claudeExe -p $prompt 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode @ $(Get-Date -Format 'HH:mm:ss') ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
