$vttFiles = Get-ChildItem -Path 'D:\History vs Hype\transcripts' -Recurse -Filter '*.vtt'
foreach ($file in $vttFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    # Remove WEBVTT header
    $content = $content -replace 'WEBVTT[\s\S]*?Language: en\r?\n', ''

    # Remove timestamps
    $content = $content -replace '\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\r\n]*\r?\n', ''

    # Remove timing tags
    $content = $content -replace '<\d{2}:\d{2}:\d{2}\.\d{3}>', ''
    $content = $content -replace '</?c>', ''

    # Remove markers
    $content = $content -replace 'align:start position:0%', ''

    # Fix HTML entities
    $content = $content -replace '\[&nbsp;__&nbsp;\]', '[expletive]'
    $content = $content -replace '&nbsp;', ' '
    $content = $content -replace '&amp;', '&'

    # Remove duplicates
    $lines = $content -split '\r?\n' | Where-Object { $_.Trim() -ne '' }
    $uniqueLines = @()
    $prevLine = ''
    foreach ($line in $lines) {
        $cleanLine = $line.Trim()
        if ($cleanLine -ne $prevLine -and $cleanLine -notmatch '^\d+$') {
            $uniqueLines += $cleanLine
            $prevLine = $cleanLine
        }
    }

    # Join and clean
    $fullText = $uniqueLines -join ' '
    $fullText = $fullText -replace '\s+', ' '

    # Force paragraph break every 100 words
    $words = $fullText -split '\s+'
    $result = New-Object System.Text.StringBuilder
    $wordCount = 0

    foreach ($word in $words) {
        [void]$result.Append($word)
        [void]$result.Append(' ')
        $wordCount++

        if ($wordCount -ge 100) {
            [void]$result.Append("`n`n")
            $wordCount = 0
        }
    }

    $cleanContent = $result.ToString().Trim()

    # Output
    $outPath = $file.FullName -replace '\.en\.vtt$', '.txt'
    $cleanContent | Out-File -FilePath $outPath -Encoding UTF8
    Write-Host "Converted: $($file.Name)"
}
Write-Host "Done!"
