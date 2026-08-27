# Routine 5 wrapper — nightly brain hygiene + index maintenance (claude-driven).
# Invoked by Windows Scheduled Task "HvH-BrainHygiene" daily 22:00.
# Logs claude -p output + exit code to .brain/_inbox/ so an abort is DIAGNOSABLE.
# (Before 2026-06-13 this was bare `claude -p $prompt` with no capture — the 2026-06-11
#  ERROR_PROCESS_ABORTED run left zero diagnostics, which is why W3 couldn't see the cause.)

. "$PSScriptRoot\_lib-preflight.ps1"
Set-RepoRoot

$logDir = ".brain\_inbox"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$logFile = Join-Path $logDir "brain-hygiene-run-$(Get-Date -Format 'yyyy-MM-dd').log"

"=== Routine 5 brain-hygiene run @ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" |
    Out-File -FilePath $logFile -Append -Encoding utf8

if (-not (Test-ClaudeAuth -LogFile $logFile)) {
    "=== Exit code: $EXIT_AUTH_EXPIRED (auth pre-flight) @ $(Get-Date -Format 'HH:mm:ss') ===" |
        Out-File -FilePath $logFile -Append -Encoding utf8
    exit $EXIT_AUTH_EXPIRED
}

$prompt = (Get-Content ".claude\routines\brain-hygiene.md" -Raw)
$claudeExe = Resolve-ClaudeExe -LogFile $logFile

# Headless `claude -p` cannot answer a permission prompt, so without an explicit grant
# the routine composes its index edits and then asks a human to apply them — which is
# what it did on 2026-08-27, silently, while still exiting 0.
#
# The grant mirrors the routine's OWN guardrails (brain-hygiene.md STEP 5: "All writes
# are local to .brain/"): read anywhere, write only inside .brain/. Scoped here on the
# invocation rather than in settings.json so it applies to this routine alone and not
# to interactive sessions in this repo.
$allowed = @(
    'Read', 'Glob', 'Grep',
    'Edit(.brain/**)', 'Write(.brain/**)'
)
& $claudeExe -p $prompt --allowedTools @allowed 2>&1 |
    Out-File -FilePath $logFile -Append -Encoding utf8

$exitCode = $LASTEXITCODE
"=== Exit code: $exitCode @ $(Get-Date -Format 'HH:mm:ss') ===" | Out-File -FilePath $logFile -Append -Encoding utf8
exit $exitCode
