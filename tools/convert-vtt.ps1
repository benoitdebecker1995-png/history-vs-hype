$vttFiles = Get-ChildItem -Path 'D:\History vs Hype\transcripts' -Recurse -Filter '*.vtt'
foreach ($file in $vttFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    # Remove WEBVTT header and metadata
    $content = $content -replace 'WEBVTT[\s\S]*?Language: en\r?\n', ''
    # Remove timestamps
    $content = $content -replace '\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\r\n]*\r?\n', ''
    # Remove inline timing tags
    $content = $content -replace '<\d{2}:\d{2}:\d{2}\.\d{3}>', ''
    $content = $content -replace '<c>', ''
    $content = $content -replace '</c>', ''
    # Remove position/alignment markers
    $content = $content -replace 'align:start position:0%', ''
    # Remove duplicate consecutive lines
    $lines = $content -split '\r?\n' | Where-Object { $_.Trim() -ne '' }
    $uniqueLines = @()
    $prevLine = ''
    foreach ($line in $lines) {
        $cleanLine = $line.Trim()
        if ($cleanLine -ne $prevLine -and $cleanLine -notmatch '^\[.*\]$') {
            $uniqueLines += $cleanLine
            $prevLine = $cleanLine
        }
    }
    $cleanContent = $uniqueLines -join ' '
    # Clean up extra spaces
    $cleanContent = $cleanContent -replace '\s+', ' '
    # Output file
    $outPath = $file.FullName -replace '\.en\.vtt$', '.txt'
    $cleanContent | Out-File -FilePath $outPath -Encoding UTF8
    Write-Host "Converted: $($file.Name)"
}
Write-Host "Done! All VTT files converted to clean text."
