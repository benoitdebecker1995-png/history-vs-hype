# Mirror library/by-topic/ to Google Drive (gdrive:HvH-library/by-topic).
# Usage: powershell tools/drive_sync.ps1          # sync (uploads new/changed, deletes remote orphans)
#        powershell tools/drive_sync.ps1 -Check   # verify mirror integrity, no transfers
# Remote "gdrive" configured 2026-06-12 (rclone OAuth, benoit.debecker1995@gmail.com).
param([switch]$Check)

$rclone = (Get-Command rclone -ErrorAction SilentlyContinue).Source
if (-not $rclone) {
    $winget = "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.74.3-windows-amd64\rclone.exe"
    if (Test-Path $winget) { $rclone = $winget }
}
if (-not $rclone) { Write-Error "rclone not found — winget install Rclone.Rclone"; exit 1 }

$src = Join-Path $PSScriptRoot "..\library\by-topic"
$dst = "gdrive:HvH-library/by-topic"

if ($Check) {
    & $rclone check $src $dst --one-way
} else {
    & $rclone sync $src $dst --transfers 8 --checkers 16 -v --stats 60s --stats-one-line
}
exit $LASTEXITCODE
