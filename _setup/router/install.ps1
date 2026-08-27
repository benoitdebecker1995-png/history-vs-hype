# Claude Code Router — install and wire up the bulk lane.
# Does NOT touch your API key. Does NOT change how plain `claude` works.
#
#   powershell -ExecutionPolicy Bypass -File "G:\History vs Hype\_setup\router\install.ps1"

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "Claude Code Router setup" -ForegroundColor Cyan
Write-Host "------------------------"

# 1. node / npm present?
try { $nodeV = (node --version) } catch { throw "Node.js not found. Install Node 18+ first, then re-run." }
Write-Host "  node $nodeV"

# 2. install the router (third-party package: @musistudio/claude-code-router)
Write-Host "  installing @musistudio/claude-code-router ..."
npm install -g @musistudio/claude-code-router

# 3. config directory
$Dir = Join-Path $env:USERPROFILE '.claude-code-router'
New-Item -ItemType Directory -Force -Path $Dir | Out-Null

$Target = Join-Path $Dir 'config.json'
$Source = Join-Path $PSScriptRoot 'config.json'

if (Test-Path -LiteralPath $Target) {
    $Backup = Join-Path $Dir ("config.backup-{0}.json" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
    Copy-Item -LiteralPath $Target -Destination $Backup
    Write-Host "  existing config backed up to $Backup" -ForegroundColor Yellow
}
Copy-Item -LiteralPath $Source -Destination $Target -Force
Write-Host "  config written to $Target"

# 4. key check — we never set this for you
if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY) -and
    [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY','User'))) {
    Write-Host ""
    Write-Host "  NEXT: set your own OpenRouter key. Get one at openrouter.ai/settings/keys" -ForegroundColor Yellow
    Write-Host '  [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY","<your-key>","User")' -ForegroundColor Yellow
    Write-Host "  Then open a NEW terminal." -ForegroundColor Yellow
} else {
    Write-Host "  OPENROUTER_API_KEY is set."
}

Write-Host ""
Write-Host "Then:  ccr start     (starts the local router on 127.0.0.1:3456)"
Write-Host "       ccr code      (Claude Code through the router — the BULK lane)"
Write-Host ""
Write-Host "Plain 'claude' is untouched and still runs on your subscription."
Write-Host ""
