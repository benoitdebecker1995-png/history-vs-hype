
$lib    = "D:\History vs Hype\library\by-topic"
$outDir = "D:\History vs Hype\_gemini-output\layer2-rename"

$folderMap = [ordered]@{
    "african-history"        = "african-history"
    "colonialism-slavery"    = "colonialism-slavery"
    "crusades-christianity"  = "crusades-christianity"
    "middle-east-history"    = "middle-east-history"
    "reference-methodology"  = "reference-methodology"
    "territorial-disputes"   = "territorial-disputes"
    "general-history-batch1" = "general-history"
    "general-history-batch2" = "general-history"
    "general-history-batch3" = "general-history"
    "general-history-batch4" = "general-history"
    "general-history-batch5" = "general-history"
    "general-history-batch6" = "general-history"
}

$allEntries  = [System.Collections.Generic.List[hashtable]]::new()
$needsRead   = [System.Collections.Generic.List[hashtable]]::new()
$parseErrors = [System.Collections.Generic.List[string]]::new()

$noisePattern = '^Warning:|^YOLO mode|^Ripgrep|^Could not read|^Attempt \d+ failed|^```|node_modules|conpty|AttachConsole|^Node\.js|^var console|^C:\\Users\\.*npm|node:internal|at Module\._|at Object\.\.|at wrapModule|at TracingChannel|at Module\.load|at Module\._load|at Module\.execute|node:main|^\s*\^'

foreach ($key in $folderMap.Keys) {
    $jsonFile = "$outDir\meta-$key.json"
    if (-not (Test-Path $jsonFile)) { Write-Warning "MISSING: $jsonFile"; continue }

    $lines = Get-Content $jsonFile -Encoding UTF8
    $clean = ($lines | Where-Object { $_ -notmatch $noisePattern }) -join [System.Environment]::NewLine
    $clean = $clean.Trim()

    # Use last line-anchored '[' as array start (handles Gemini restart-attempts)
    $arrayStarts = [regex]::Matches($clean, '(?m)^\[')
    if ($arrayStarts.Count -eq 0) { $parseErrors.Add("NO JSON ARRAY in $key"); continue }
    $start = $arrayStarts[$arrayStarts.Count - 1].Index
    $end   = $clean.LastIndexOf(']')
    if ($end -le $start) { $parseErrors.Add("MALFORMED ARRAY in $key"); continue }
    $json = $clean.Substring($start, $end - $start + 1)
    # Fix Gemini line-wrapped string values: join continuation lines (indented non-structure chars)
    $json = [System.Text.RegularExpressions.Regex]::Replace($json, "(?m)\r?\n(?=[^{}\[\],\r\n])", " ")

    try {
        $entries = $json | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $parseErrors.Add("PARSE ERROR in ${key}: $_")
        continue
    }

    $topicFolder = $folderMap[$key]
    foreach ($e in $entries) {
        $entry = @{
            original  = $e.o
            canonical = $e.c
            confidence= $e.conf
            ncr       = [bool]$e.ncr
            folder    = $topicFolder
            srcPath   = "$lib\$topicFolder\$($e.o)"
            destPath  = if ($e.c) { "$lib\$topicFolder\$($e.c)" } else { $null }
        }
        if ([bool]$e.ncr -or -not $e.c) { $needsRead.Add($entry) }
        else                            { $allEntries.Add($entry) }
    }
}

Write-Host "=== Parse Summary ==="
Write-Host "Entries parsed     : $($allEntries.Count)"
Write-Host "Needs content read : $($needsRead.Count)"
Write-Host "Parse errors       : $($parseErrors.Count)"
$parseErrors | ForEach-Object { Write-Warning $_ }

$canonGroups = $allEntries | Group-Object -Property { $_.canonical }
$dups        = $canonGroups | Where-Object { $_.Count -gt 1 }
$dupTotal    = ($dups | ForEach-Object { $_.Count - 1 } | Measure-Object -Sum).Sum
Write-Host ""
Write-Host "=== Deduplication ==="
Write-Host "Unique canonical names : $(($canonGroups | Where-Object Count -eq 1).Count)"
Write-Host "Duplicate groups       : $($dups.Count)"
Write-Host "Total dup files        : $dupTotal"

# --- Rename script ---
$nl = [System.Environment]::NewLine
$rLines = [System.Collections.Generic.List[string]]::new()
$rLines.Add('# Layer 2 - Rename script (review before running)')
$rLines.Add("# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
$rLines.Add("# Renames below: $($allEntries.Count)")
$rLines.Add('')
$sameName = 0
foreach ($e in ($allEntries | Sort-Object { $_.folder + $_.original })) {
    if ($e.original -eq $e.canonical) { $sameName++; continue }
    $rLines.Add("# [$($e.confidence)] $($e.folder)")
    $rLines.Add("Rename-Item -LiteralPath '$($e.srcPath -replace "'","''")' -NewName '$($e.canonical -replace "'","''")'")
}
$rLines.Add('')
$rLines.Add('Write-Host "Done."')
[System.IO.File]::WriteAllLines("$outDir\DO-RENAME.ps1", $rLines, [System.Text.UTF8Encoding]::new($false))
Write-Host ""
Write-Host "Rename script  -> $outDir\DO-RENAME.ps1"
Write-Host "Already canonical (skipped): $sameName"

# --- Dedup script ---
$dLines = [System.Collections.Generic.List[string]]::new()
$dLines.Add('# Layer 2 - Dedup DELETE script (REVIEW CAREFULLY - removes duplicate files)')
$dLines.Add("# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
$dLines.Add('# Remove -WhatIf to actually delete after review')
$dLines.Add('')
foreach ($grp in $dups) {
    $keep = $grp.Group | Sort-Object { $_.srcPath } | Select-Object -First 1
    $dLines.Add("# KEEP: $($keep.srcPath)")
    foreach ($del in ($grp.Group | Sort-Object { $_.srcPath } | Select-Object -Skip 1)) {
        $dLines.Add("Remove-Item -LiteralPath '$($del.srcPath -replace "'","''")' -WhatIf  # DUP")
    }
    $dLines.Add('')
}
[System.IO.File]::WriteAllLines("$outDir\DO-DEDUP.ps1", $dLines, [System.Text.UTF8Encoding]::new($false))
Write-Host "Dedup script   -> $outDir\DO-DEDUP.ps1"

# --- Needs-content-read list ---
$ncrLines = $needsRead | ForEach-Object { "$($_.folder)\$($_.original)" }
[System.IO.File]::WriteAllLines("$outDir\NEEDS-CONTENT-READ.txt", $ncrLines, [System.Text.UTF8Encoding]::new($false))
Write-Host "NCR list       -> $outDir\NEEDS-CONTENT-READ.txt ($($needsRead.Count) files)"
