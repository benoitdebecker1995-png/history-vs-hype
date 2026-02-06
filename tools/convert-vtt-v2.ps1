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

    # Fix HTML entities
    $content = $content -replace '&nbsp;', ' '
    $content = $content -replace '&amp;', '&'
    $content = $content -replace '&lt;', '<'
    $content = $content -replace '&gt;', '>'

    # Remove duplicate consecutive lines but keep structure
    $lines = $content -split '\r?\n' | Where-Object { $_.Trim() -ne '' }
    $uniqueLines = @()
    $prevLine = ''
    foreach ($line in $lines) {
        $cleanLine = $line.Trim()
        if ($cleanLine -ne $prevLine -and $cleanLine -notmatch '^\[.*\]$' -and $cleanLine -notmatch '^\d+$') {
            $uniqueLines += $cleanLine
            $prevLine = $cleanLine
        }
    }

    # Join with spaces, then add paragraph breaks every ~150 words
    $fullText = $uniqueLines -join ' '
    $fullText = $fullText -replace '\s+', ' '

    # Add paragraph breaks at sentence endings (. ! ?) every ~100-150 words
    $words = $fullText -split '\s+'
    $result = New-Object System.Text.StringBuilder
    $wordCount = 0

    foreach ($word in $words) {
        [void]$result.Append($word)
        [void]$result.Append(' ')
        $wordCount++

        # Add paragraph break after sentence-ending punctuation every ~100 words
        if ($wordCount -ge 100 -and $word -match '[.!?]$') {
            [void]$result.Append("`n`n")
            $wordCount = 0
        }
    }

    $cleanContent = $result.ToString().Trim()

    # Output file
    $outPath = $file.FullName -replace '\.en\.vtt$', '.txt'
    $cleanContent | Out-File -FilePath $outPath -Encoding UTF8
    Write-Host "Converted: $($file.Name)"
}
Write-Host "Done! All VTT files converted with paragraph breaks."
