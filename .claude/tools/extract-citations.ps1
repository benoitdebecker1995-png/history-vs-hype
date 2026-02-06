# extract-citations.ps1
# Parses NotebookLM output into structured claims and bibliography
#
# Usage:
#   .\extract-citations.ps1 -InputFile "notebooklm-paste.txt"
#   .\extract-citations.ps1 -InputFile "paste.txt" -OutputFile "citations-flat-earth.md"
#
# Input: Text file with pasted NotebookLM response (include SOURCES section if available)
# Output: Markdown file with claims to verify and bibliography
#
# Expected input format:
#   Medieval scholars understood Earth's sphericity. [1] Bede wrote in 725 CE
#   that Earth is "like a ball, not a shield." [2] Sacrobosco's textbook was
#   used in universities for 400 years. [3]
#
#   SOURCES:
#   1. Lindberg, David C. "The Beginnings of Western Science" (2007), p. 147
#   2. Bede, "The Reckoning of Time" (Wallis translation, 1999), p. 90
#   3. Grant, Edward. "Planets, Stars, and Orbs" (1996), p. 265

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [string]$OutputFile = "extracted-citations.md"
)

# Check input file exists
if (-not (Test-Path $InputFile)) {
    Write-Error "Error: Input file not found: $InputFile"
    exit 1
}

# Read input file with UTF8 encoding
$content = Get-Content $InputFile -Raw -Encoding UTF8

# Initialize counters
$claimCount = 0
$sourceCount = 0
$warnings = @()

# Check for SOURCES section
$hasSources = $content -match "SOURCES:"
if (-not $hasSources) {
    $warnings += "WARNING: No 'SOURCES:' section found. Citations will be listed inline."
}

# Split content at SOURCES: marker
$sections = $content -split "SOURCES:", 2
$text = $sections[0].Trim()
$sourcesRaw = if ($sections.Count -gt 1) { $sections[1].Trim() } else { "" }

# Parse source list into hashtable
$sourceMap = @{}
if ($sourcesRaw) {
    $sourcesRaw -split "`n" | ForEach-Object {
        $line = $_.Trim()
        if ($line -match '^(\d+)\.\s+(.+)$') {
            $num = $matches[1]
            $citation = $matches[2]
            $sourceMap[$num] = $citation
            $sourceCount++
        }
    }
}

# Extract all citation numbers used in text
$citationsInText = [regex]::Matches($text, '\[(\d+)\]') |
    ForEach-Object { $_.Groups[1].Value } |
    Select-Object -Unique |
    Sort-Object { [int]$_ }

# Check for mismatched citations
foreach ($citNum in $citationsInText) {
    if ($hasSources -and -not $sourceMap.ContainsKey($citNum)) {
        $warnings += "WARNING: Citation [$citNum] appears in text but not in SOURCES list"
    }
}

# Extract sentences containing citations
# Pattern matches sentences that contain at least one [N] citation
$sentencePattern = '([^.!?]*\[\d+\][^.!?]*[.!?])'
$claims = [regex]::Matches($text, $sentencePattern)

# Build output
$output = @()
$output += "# Extracted Citations"
$output += ""
$output += "**Source file:** $InputFile"
$output += "**Extracted:** $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$output += ""

# Add warnings if any
if ($warnings.Count -gt 0) {
    $output += "---"
    $output += ""
    $output += "## Warnings"
    $output += ""
    foreach ($warn in $warnings) {
        $output += "- $warn"
    }
    $output += ""
}

$output += "---"
$output += ""
$output += "## Claims to Verify"
$output += ""

foreach ($claim in $claims) {
    $claimText = $claim.Value.Trim()

    # Extract citation numbers from this claim
    $citNums = [regex]::Matches($claimText, '\[(\d+)\]') |
        ForEach-Object { $_.Groups[1].Value }

    # Clean citation markers for display
    $cleanText = $claimText -replace '\s*\[\d+\]\s*', ' '
    $cleanText = $cleanText -replace '\s+', ' '
    $cleanText = $cleanText.Trim()

    $claimCount++

    $output += "**Claim:** $cleanText"
    $output += "- **Status:** NEEDS VERIFICATION"

    foreach ($num in $citNums) {
        if ($sourceMap.ContainsKey($num)) {
            $source = $sourceMap[$num]
            $output += "- **Source:** [$num] $source"
        } else {
            $output += "- **Source:** [$num] (not found in SOURCES list)"
        }
    }

    $output += ""
}

# Add bibliography section
$output += "---"
$output += ""
$output += "## Bibliography (from NotebookLM output)"
$output += ""

if ($sourceMap.Count -gt 0) {
    foreach ($num in ($sourceMap.Keys | Sort-Object { [int]$_ })) {
        $source = $sourceMap[$num]
        $output += "[$num] $source"
    }
} else {
    $output += "*No sources section found in input. Citations appear inline in claims above.*"
}

$output += ""
$output += "---"
$output += ""
$output += "## Usage"
$output += ""
$output += "Copy verified claims to your session log, update Status:"
$output += "- NEEDS VERIFICATION -> ✅ VERIFIED (confirmed in source)"
$output += "- NEEDS VERIFICATION -> ⚠️ PARTIALLY VERIFIED (needs context)"
$output += "- NEEDS VERIFICATION -> 🔄 NEEDS HEDGE (conflicting info)"
$output += "- NEEDS VERIFICATION -> ❌ UNVERIFIABLE (couldn't confirm)"
$output += ""
$output += "---"
$output += ""
$output += "*Extracted by extract-citations.ps1*"

# Write output file with UTF8 encoding
$output -join "`n" | Out-File $OutputFile -Encoding UTF8

# Print summary
Write-Host ""
Write-Host "Citation Extraction Complete" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host "Claims extracted: $claimCount"
Write-Host "Unique sources: $sourceCount"
Write-Host "Output file: $OutputFile"

if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "Warnings:" -ForegroundColor Yellow
    foreach ($warn in $warnings) {
        Write-Host "  - $warn" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open $OutputFile"
Write-Host "  2. Verify each claim against original source"
Write-Host "  3. Update status and transfer to session log"
