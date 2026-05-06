Set-Location "D:\History vs Hype"
$prompt = (Get-Content ".claude\routines\channel-health-snapshot.md" -Raw)
claude -p $prompt
