# New Video Project Initializer for History vs Hype
# Creates standardized project structure with templates

param(
    [Parameter(Mandatory=$true)]
    [string]$TopicName,

    [Parameter(Mandatory=$false)]
    [ValidateSet("research", "scripting", "ready")]
    [string]$InitialStatus = "research",

    [Parameter(Mandatory=$false)]
    [ValidateSet("high", "medium", "low")]
    [string]$Priority = "medium"
)

# Configuration
$RepoRoot = "C:\Users\benoi\Documents\History vs Hype"
$Date = Get-Date -Format "yyyy-MM-dd"
$Year = Get-Date -Format "yyyy"

# Sanitize topic name for folder
$FolderName = $TopicName.ToLower() -replace '[^a-z0-9\s-]', '' -replace '\s+', '-'
$FolderName = "$FolderName-$Year"

# Determine target folder based on status
switch ($InitialStatus) {
    "ready" { $TargetFolder = "$RepoRoot\video-projects\_READY_TO_FILM" }
    default { $TargetFolder = "$RepoRoot\video-projects\_IN_PRODUCTION" }
}

# Add priority prefix if ready to film
if ($InitialStatus -eq "ready") {
    $PriorityNum = switch ($Priority) {
        "high" { "1" }
        "medium" { "2" }
        "low" { "3" }
    }
    $FolderName = "$PriorityNum-$FolderName"
}

$ProjectPath = "$TargetFolder\$FolderName"

# Check if project already exists
if (Test-Path $ProjectPath) {
    Write-Host "❌ Error: Project folder already exists: $ProjectPath" -ForegroundColor Red
    exit 1
}

# Create project structure
Write-Host "🎬 Creating new video project..." -ForegroundColor Cyan
Write-Host "   Topic: $TopicName" -ForegroundColor White
Write-Host "   Folder: $FolderName" -ForegroundColor White
Write-Host "   Location: $TargetFolder" -ForegroundColor White
Write-Host ""

New-Item -ItemType Directory -Path $ProjectPath -Force | Out-Null

# Create README
$ReadmeContent = @"
# $TopicName

**Created:** $Date
**Status:** $InitialStatus
**Priority:** $Priority

---

## Project Overview

**Topic:** $TopicName

**Modern Hook:** [Describe current event or controversy]

**Both Extremes:**
- **Extreme A:** [Common myth or oversimplification]
- **Extreme B:** [Opposite oversimplification]

**Academic Reality:** [Nuanced truth between extremes]

---

## Production Checklist

### Research Phase
- [ ] Preliminary research complete
- [ ] Modern relevance identified
- [ ] "Both extremes" framed
- [ ] Source recommendations gathered
- [ ] NotebookLM notebook created
- [ ] NotebookLM prompts run

### Scripting Phase
- [ ] First draft complete
- [ ] Voice check passed
- [ ] Retention structure optimized
- [ ] Modern relevance every 90 seconds
- [ ] Authority markers present (8-10)

### Verification Phase
- [ ] Every claim has 2+ sources
- [ ] Contested claims labeled
- [ ] Sources formatted for description
- [ ] Counter-evidence acknowledged
- [ ] Logical fallacies checked

### Pre-Production Phase
- [ ] B-roll checklist created
- [ ] Visual evidence identified
- [ ] Autocue script formatted
- [ ] Pre-filming checklist complete
- [ ] Expected duration calculated

### Production Phase
- [ ] Filmed
- [ ] Edited
- [ ] Metadata generated
- [ ] Thumbnail created
- [ ] Published

---

## Files in This Project

- **README.md** - This file (project overview)
- **research.md** - Preliminary research and sources
- **script-draft.md** - Working script (iterative)
- **script-FINAL.md** - Final approved script
- **sources.md** - Source citations
- **B-ROLL-CHECKLIST.md** - Visual evidence needed
- **STATUS.md** - Current status and next actions

---

## Key Dates

- **Created:** $Date
- **Research Complete:**
- **Script Complete:**
- **Filming Target:**
- **Publication Target:**

---

## Expected Performance

**VidIQ Prediction:** [Add after research]
**Expected Views:** [Add after research]
**Retention Goal:** 30-35%
**Target Duration:** 8-12 minutes

---

## Notes

[Add project-specific notes, decisions, or considerations here]

---

**Last Updated:** $Date
"@

$ReadmeContent | Out-File -FilePath "$ProjectPath\README.md" -Encoding UTF8

# Create research template
$ResearchContent = @"
# Research - $TopicName

**Last Updated:** $Date

---

## Modern Hook

**Current Event:** [Describe the 2024-2025 news hook]

**Why This Matters Now:** [Explain contemporary relevance]

**Controversy:** [What's being debated or misunderstood today?]

---

## Both Extremes Framework

### Extreme A: [Common Myth/Oversimplification]
**What people believe:**
- [Claim 1]
- [Claim 2]
- [Claim 3]

**Sources spreading this:**
- [Political figures, media outlets, social media]

### Extreme B: [Opposite Oversimplification]
**What opponents believe:**
- [Counter-claim 1]
- [Counter-claim 2]
- [Counter-claim 3]

**Sources spreading this:**
- [Political figures, media outlets, social media]

### Academic Reality: [Nuanced Truth]
**What evidence actually shows:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Key scholars:**
- [Academic 1] - [Institution] - [Key work]
- [Academic 2] - [Institution] - [Key work]

---

## Preliminary Research

### Key Facts to Verify:
1. [Fact 1] - Source: [Citation]
2. [Fact 2] - Source: [Citation]
3. [Fact 3] - Source: [Citation]

### Primary Documents Needed:
- [ ] [Document 1] - [Location/Archive]
- [ ] [Document 2] - [Location/Archive]
- [ ] [Document 3] - [Location/Archive]

### Maps/Visual Evidence:
- [ ] [Map 1] - [Source]
- [ ] [Image 1] - [Source]

---

## Source Recommendations

### Tier 1 (Academic):
1. [Book/Article] by [Author] ([Year])
   - [Why it's important]
   - Available: [Where to find]

2. [Book/Article] by [Author] ([Year])
   - [Why it's important]
   - Available: [Where to find]

### Tier 2 (Journalistic):
1. [Article] by [Author] - [Publication] ([Date])
   - [URL]

### Tier 3 (Other):
1. [Source] - [Type]
   - [Notes]

---

## NotebookLM Strategy

### Sources to Upload:
1. [Source 1]
2. [Source 2]
3. [Source 3]

### Prompts to Run:
1. Research organization
2. Evidence extraction
3. Counter-evidence analysis
4. Source contradiction check

---

## VidIQ Analysis

**Search Volume:** [Monthly searches for key terms]
**Competition:** [Low/Medium/High]
**Expected Views:** [VidIQ prediction]
**Trending:** [Yes/No]
**Demonetization Risk:** [Low/Medium/High]

**Decision:** [Proceed/Modify/Cancel]

---

## Research Notes

[Add freeform research notes, interesting findings, questions to investigate]

---

**Next Steps:**
1. [Action 1]
2. [Action 2]
3. [Action 3]
"@

$ResearchContent | Out-File -FilePath "$ProjectPath\research.md" -Encoding UTF8

# Create STATUS file
$StatusContent = @"
# Project Status - $TopicName

**Last Updated:** $Date
**Current Phase:** $InitialStatus
**Priority:** $Priority

---

## Current Status

**Phase:** $InitialStatus

**Progress:** [0-100%]

**Next Action:** [What needs to happen next?]

**Blockers:** [Any issues preventing progress?]

**Target Completion:** [Date or timeframe]

---

## Phase Checklist

### ✅ Completed:
- [x] Project initialized

### 🚧 In Progress:
- [ ] [Current tasks]

### ⏳ To Do:
- [ ] [Upcoming tasks]

---

## Time Tracking

**Time Spent:** [Hours]
- Research: [Hours]
- Scripting: [Hours]
- Fact-checking: [Hours]
- Production: [Hours]

---

## Notes

[Add status updates, decisions made, changes in direction]

---

**Quick Status:** [One-line summary of where project stands]
"@

$StatusContent | Out-File -FilePath "$ProjectPath\STATUS.md" -Encoding UTF8

# Create sources template
$SourcesContent = @"
# Sources - $TopicName

**Last Updated:** $Date

---

## Primary Sources (Tier 1)

### Documents
1. **[Document Name]** ([Year])
   - Type: [Treaty/Census/Official Record]
   - Location: [Archive/URL]
   - Relevance: [Why it matters]
   - Citation: [Full citation]

### Academic Publications
1. **[Title]** by [Author] ([Year])
   - Journal: [Name]
   - DOI: [Link]
   - Key findings: [Summary]
   - Citation: [Full citation]

---

## Secondary Sources (Tier 2)

### Expert Analysis
1. **[Title]** by [Author/Organization] ([Year])
   - Publication: [Name]
   - URL: [Link]
   - Relevance: [Why included]

---

## Tertiary Sources (Tier 3)

### Context and Background
1. **[Title]** - [Source]
   - URL: [Link]
   - Use: [How it helps]

---

## Visual Sources

### Maps
1. **[Map Name]** ([Year])
   - Source: [Archive/Commons]
   - URL: [Link]
   - License: [Public domain/CC/etc]

### Images
1. **[Image Description]**
   - Source: [Where from]
   - URL: [Link]
   - License: [Status]

---

## Source Verification

**Total Claims:** [Number]
**Sources per Claim:** [Average]
**Tier 1 Sources:** [Count]
**Tier 2 Sources:** [Count]
**Contested Claims:** [Count]

**Verification Status:** [Complete/In Progress]

---

## Formatted for YouTube Description

\`\`\`
📚 SOURCES:

PRIMARY SOURCES:
• [Citation 1]
• [Citation 2]

ACADEMIC RESEARCH:
• [Citation 3]
• [Citation 4]

FURTHER READING:
• [Citation 5]
• [Citation 6]
\`\`\`
"@

$SourcesContent | Out-File -FilePath "$ProjectPath\sources.md" -Encoding UTF8

# Success message
Write-Host "✅ Project created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Location: $ProjectPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Files created:" -ForegroundColor Yellow
Write-Host "   - README.md (project overview)" -ForegroundColor White
Write-Host "   - research.md (research template)" -ForegroundColor White
Write-Host "   - STATUS.md (progress tracking)" -ForegroundColor White
Write-Host "   - sources.md (citation management)" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Fill in research.md with preliminary findings" -ForegroundColor White
Write-Host "   2. Identify modern hook and both extremes" -ForegroundColor White
Write-Host "   3. Run /notebooklm-prompts for research strategy" -ForegroundColor White
Write-Host "   4. Update STATUS.md as you progress" -ForegroundColor White
Write-Host ""
Write-Host "💡 Quick commands:" -ForegroundColor Yellow
Write-Host "   cd `"$ProjectPath`"" -ForegroundColor White
Write-Host "   code ." -ForegroundColor White
Write-Host ""

# Open project folder in Explorer
Start-Process explorer.exe $ProjectPath

# Update PROJECT_STATUS.md
Write-Host "📊 Updating PROJECT_STATUS.md..." -ForegroundColor Cyan

$StatusFile = "$RepoRoot\video-projects\PROJECT_STATUS.md"
if (Test-Path $StatusFile) {
    $NewEntry = @"

### [New Project] $TopicName
**Location:** ``$($TargetFolder -replace [regex]::Escape($RepoRoot), '')/$FolderName/``
**Status:** 📚 Just Started
**Created:** $Date
**Priority:** $Priority

**Next Action:** Begin preliminary research

---
"@

    $StatusContent = Get-Content $StatusFile -Raw
    $UpdatedContent = $StatusContent -replace "(## 🚧 IN PRODUCTION)", "`$1$NewEntry"
    $UpdatedContent | Out-File -FilePath $StatusFile -Encoding UTF8

    Write-Host "✅ PROJECT_STATUS.md updated" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎬 Ready to start researching '$TopicName'!" -ForegroundColor Green
Write-Host ""
