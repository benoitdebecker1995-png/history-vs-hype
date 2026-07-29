# Shared pre-flight helpers for the HvH-* routine wrappers.
#
# WHY THIS EXISTS (2026-07-28):
# The `claude` CLI's OAuth refresh token expired 2026-07-23. Every claude-driven routine
# (ChannelHealth, Reconcile, BrainHygiene, StaleProjects) then failed with a bare exit 1 for
# FIVE CONSECUTIVE DAYS, and nothing surfaced it — four identical silent `1`s look like any
# other failure, and `/reconcile` silently stopped archiving publishes.
#
# Two hardening jobs, both learned from that outage:
#   Test-ClaudeAuth  — fail with a DISTINCT, ACTIONABLE code before burning a run on a dead session.
#   Set-RepoRoot     — every wrapper had an UNCHECKED `Set-Location`. If it fails, the script keeps
#                      going: Get-Content returns $null, `claude -p` runs on an empty prompt, and the
#                      failure looks like a model problem instead of a path problem.
#
# Dot-source from a wrapper:  . "$PSScriptRoot\_lib-preflight.ps1"

Set-StrictMode -Version Latest

# Distinct from claude's generic 1 so the cause is readable straight off the task result.
$script:EXIT_AUTH_EXPIRED = 78   # sysexits EX_CONFIG
$script:EXIT_BAD_REPO_ROOT = 79

function Set-RepoRoot {
    <#  Set-Location, but fatal on failure instead of silently continuing. #>
    param(
        [string]$Path = "D:\History vs Hype",
        [string]$LogFile
    )
    try {
        Set-Location -Path $Path -ErrorAction Stop
    } catch {
        $msg = "PREFLIGHT FAIL: cannot enter repo root '$Path' — $($_.Exception.Message)"
        Write-Host $msg
        if ($LogFile) { $msg | Out-File -FilePath $LogFile -Append -Encoding utf8 }
        exit $script:EXIT_BAD_REPO_ROOT
    }
}

function Test-ClaudeAuth {
    <#
        Returns $true when the claude CLI has a usable OAuth session.
        Writes an actionable message and returns $false when it does not.
        Never reads, logs, or returns token VALUES — only presence and expiry.
    #>
    param([string]$LogFile)

    $credPath = Join-Path $env:USERPROFILE ".claude\.credentials.json"

    function Fail([string]$reason) {
        $lines = @(
            "PREFLIGHT FAIL: claude CLI is not authenticated — $reason",
            "  The routine was NOT run. This is not a model or repo problem.",
            "  FIX: open a terminal (as THIS Windows user) and run:  claude auth login --claudeai",
            "  Verify with:  claude auth status   -> expect loggedIn: true",
            "  NOTE: /login only works inside an interactive CLI session, not the desktop app.",
            "  Until then every claude-driven routine (ChannelHealth, Reconcile, BrainHygiene,",
            "  StaleProjects) will keep failing, and /reconcile will not archive new publishes."
        )
        foreach ($l in $lines) {
            Write-Host $l
            if ($LogFile) { $l | Out-File -FilePath $LogFile -Append -Encoding utf8 }
        }
        return $false
    }

    if (-not (Test-Path $credPath)) { return (Fail "no credentials file at $credPath") }

    try {
        $cred = Get-Content $credPath -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
    } catch {
        return (Fail "credentials file unreadable or not valid JSON")
    }

    if (-not $cred.PSObject.Properties.Name.Contains('claudeAiOauth')) {
        return (Fail "credentials file has no claudeAiOauth section")
    }
    $oauth = $cred.claudeAiOauth

    # The observed failure shape: the CLI blanks both tokens after a refresh attempt fails.
    $refresh = if ($oauth.PSObject.Properties.Name.Contains('refreshToken')) { $oauth.refreshToken } else { $null }
    if ([string]::IsNullOrWhiteSpace($refresh)) {
        return (Fail "refresh token is empty (the CLI blanks it after a failed refresh)")
    }

    if ($oauth.PSObject.Properties.Name.Contains('refreshTokenExpiresAt')) {
        $expMs = [double]$oauth.refreshTokenExpiresAt
        if ($expMs -gt 0) {
            $exp = [DateTimeOffset]::FromUnixTimeMilliseconds([long]$expMs).LocalDateTime
            if ($exp -lt (Get-Date)) {
                return (Fail ("refresh token expired {0:yyyy-MM-dd HH:mm}" -f $exp))
            }
        }
    }

    return $true
}
