Set-Location "D:\History vs Hype"
$prompt = (Get-Content ".claude\routines\brain-hygiene.md" -Raw)
claude -p $prompt
