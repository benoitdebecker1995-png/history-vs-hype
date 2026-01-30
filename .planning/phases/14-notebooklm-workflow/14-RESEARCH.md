# Phase 14: NotebookLM Workflow - Research

**Researched:** 2026-01-30
**Domain:** Research workflow optimization, citation management, prompt engineering
**Confidence:** HIGH

## Summary

Phase 14 focuses on enhancing the NotebookLM research-to-script pipeline with structured prompt templates, session logging formats, and citation extraction helpers. This is NOT about automation (explicitly ruled out in REQUIREMENTS.md) but about providing reusable templates and parsers for manual workflows.

The channel already has strong NotebookLM infrastructure: 13 use case prompts in NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md, source standards in NOTEBOOKLM-SOURCE-STANDARDS.md, and multiple project examples showing SOURCE-LIST.md + PROMPTS.md patterns. Phase 14 expands this foundation with more templates, standardized logging, and citation extraction from pasted output.

NotebookLM 2026 features (Gemini 3, Deep Research, inline citations with source scrolling) enable sophisticated research workflows where users paste AI responses and extract structured citations. The existing workflow uses Markdown files for session results (see bir-tawil NOTEBOOKLM-RESEARCH-RESULTS.md), which provides the pattern for standardized logging.

**Primary recommendation:** Create prompt template library (15+ scenarios), standardized session log template (capture findings with citations), and citation extraction script that parses NotebookLM output into structured format.

## Standard Stack

The established tools/formats for this domain:

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| NotebookLM | Web (2026) | Source-grounded research with Gemini 3 | Google's official academic research tool, no API needed for manual workflow |
| Markdown | N/A | Documentation format | Already used across all .claude/REFERENCE/ and video-projects/ |
| Plain text templates | N/A | Prompt reusability | Copy-paste friendly, version-controllable |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| Regular expressions | POSIX | Citation pattern matching | Parsing NotebookLM inline citations [1], [2] format |
| PowerShell/Bash | Native | Text processing scripts | Extracting citations from pasted output |
| JSON/YAML | N/A | Structured metadata | Optional for citation mapping |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom templates | Generic note-taking | Templates encode channel-specific research patterns (identity stakes, Big Six, etc.) |
| Manual parsing | Zotero/EndNote | Those are reference managers, not NotebookLM output parsers - different use case |
| Browser automation | Manual workflow | REQUIREMENTS.md explicitly rules out automation as "brittle and slower" |

**Installation:**
```bash
# No installation needed - uses existing text editors and shell scripts
# Templates are Markdown files in .claude/templates/
# Parser scripts go in .claude/tools/
```

## Architecture Patterns

### Recommended Project Structure
```
.claude/
├── templates/
│   ├── notebooklm-prompts/     # 15+ prompt templates by use case
│   └── NOTEBOOKLM-SESSION-LOG-TEMPLATE.md  # Standard logging format
├── tools/
│   └── extract-citations.ps1   # Parse NotebookLM output
└── REFERENCE/
    ├── NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md  # Already exists (13 use cases)
    └── NOTEBOOKLM-SOURCE-STANDARDS.md       # Already exists

video-projects/_IN_PRODUCTION/[project]/
├── NOTEBOOKLM-SOURCE-LIST.md       # Already standard
├── NOTEBOOKLM-PROMPTS.md           # Already standard
├── NOTEBOOKLM-SESSION-LOG-[DATE].md  # NEW - session results
└── 01-VERIFIED-RESEARCH.md         # Citations flow here
```

### Pattern 1: Prompt Template Library Structure
**What:** Organized collection of 15+ research prompt templates covering common scenarios
**When to use:** User needs to query NotebookLM for specific research tasks

**Structure:**
```markdown
# [Scenario Name]

**Use case:** [When to use this prompt]
**Sources needed:** [Which types of sources to upload]
**Expected output:** [What NotebookLM should return]

## Prompt Template

> [Copy-paste ready prompt with [PLACEHOLDERS] for customization]

## Example Usage

**Context:** [Real example from a video project]
**Customized prompt:** [Filled-in version]
**Output sample:** [What was returned]
```

**Categories for 15+ templates:**
1. Argument structure verification (Toulmin model)
2. Identity stake assessment (Kahan framework)
3. Backfire effect prevention (Lewandowsky)
4. Historical thinking audit (Big Six)
5. Trust-building language (Besley)
6. Alternative explanation development (gap filling)
7. Source credibility audit (myth origins)
8. Contested history framing (sedimented histories)
9. Gateway effect analysis (conspiracy connections)
10. Customized audio overview (topic immersion)
11. International comparison discovery (NEW from existing doc)
12. Data comparison hook development (Kraut-style)
13. Competitor differentiation research (unique angles)
14. **Timeline extraction** (chronological event ordering)
15. **Quantitative data verification** (statistics cross-check)
16. **Quote mining** (find best on-screen quotes)
17. **Counterargument mapping** (strongest opposing evidence)

### Pattern 2: Session Logging Format
**What:** Standardized template for capturing NotebookLM research session findings
**When to use:** After running prompts, to document results before writing script

**Structure follows existing bir-tawil example:**
```markdown
# NotebookLM Session Log - [Topic]

**Date:** [YYYY-MM-DD]
**Notebook(s):** [Act 1/Act 2/Act 3 or source categories]
**Prompts used:** [List by ID: A1, B2, C3]
**Status:** [In Progress / Ready for Scripting]
**Verification Level:** [X%]

---

## Session Summary

**Research questions addressed:**
- [Question 1]
- [Question 2]

**Key findings:**
- [Finding with citation]
- [Finding with citation]

**Open questions:**
- [What still needs research]

---

## Detailed Findings by Claim

### CLAIM 1: "[The claim statement]"
- **Verdict:** ✅ VERIFIED / ⚠️ PARTIALLY VERIFIED / 🔄 NEEDS HEDGE / ❌ UNVERIFIABLE
- **Evidence:**
  - [Quote or data point]
  - **Source:** [Title] [Page/Section]
  - **NotebookLM citation:** [1] or [2] (as returned)
- **On-screen quote ready:** "[Exact text formatted for display]"

### CLAIM 2: ...

---

## Citations to Add to VERIFIED-RESEARCH.md

[List of ✅ VERIFIED claims ready to transfer]

---

## Next Steps

- [ ] [Action item]
- [ ] [Research gap to fill]
```

**Why this structure:**
- Mirrors existing bir-tawil NOTEBOOKLM-RESEARCH-RESULTS.md pattern
- Verdict system (✅⚠️🔄❌) already in use
- "On-screen quote ready" prepares text for B-roll
- Clear transfer path to 01-VERIFIED-RESEARCH.md

### Pattern 3: Citation Extraction Script
**What:** Parser that takes pasted NotebookLM output and extracts structured citations
**When to use:** After copying chat responses from NotebookLM to convert inline citations to reference list

**Input format (NotebookLM output):**
```
Medieval scholars understood Earth's sphericity. [1] Bede wrote in 725 CE
that Earth is "like a ball, not a shield." [2] Sacrobosco's textbook was
used in universities for 400 years. [3]

SOURCES:
1. Lindberg, David C. "The Beginnings of Western Science" (2007), p. 147
2. Bede, "The Reckoning of Time" (Wallis translation, 1999), p. 90
3. Grant, Edward. "Planets, Stars, and Orbs" (1996), p. 265
```

**Output format (structured):**
```markdown
## Extracted Claims

**Claim:** Medieval scholars understood Earth's sphericity
- **Status:** NEEDS VERIFICATION
- **Source:** [1] Lindberg 2007, p. 147

**Claim:** Bede wrote in 725 CE that Earth is "like a ball, not a shield"
- **Status:** DIRECT QUOTE - needs page verification
- **Source:** [2] Bede, Wallis trans. 1999, p. 90

**Claim:** Sacrobosco's textbook was used in universities for 400 years
- **Status:** NEEDS VERIFICATION
- **Source:** [3] Grant 1996, p. 265

---

## Bibliography (from NotebookLM output)

[1] Lindberg, David C. "The Beginnings of Western Science" (2007), p. 147
[2] Bede, "The Reckoning of Time" (Wallis translation, 1999), p. 90
[3] Grant, Edward. "Planets, Stars, and Orbs" (1996), p. 265
```

**Script implementation (PowerShell example):**
```powershell
# extract-citations.ps1
# Parses NotebookLM output into structured claims + bibliography

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [string]$OutputFile = "extracted-citations.md"
)

# Read input
$content = Get-Content $InputFile -Raw

# Split into text and sources sections
$sections = $content -split "SOURCES:"
$text = $sections[0]
$sources = $sections[1]

# Extract citation numbers from text
$citations = [regex]::Matches($text, '\[(\d+)\]') |
    ForEach-Object { $_.Groups[1].Value } |
    Select-Object -Unique | Sort-Object

# Parse source list
$sourceMap = @{}
$sources -split "`n" | ForEach-Object {
    if ($_ -match '^(\d+)\.\s+(.+)$') {
        $sourceMap[$matches[1]] = $matches[2]
    }
}

# Extract sentences with citations
$claims = [regex]::Matches($text, '([^.]+\[\d+\][^.]*\.)')

# Generate output
$output = "## Extracted Claims`n`n"

foreach ($claim in $claims) {
    $claimText = $claim.Value.Trim()
    $citNums = [regex]::Matches($claimText, '\[(\d+)\]') |
        ForEach-Object { $_.Groups[1].Value }

    $cleanText = $claimText -replace '\[\d+\]', ''

    $output += "**Claim:** $cleanText`n"
    $output += "- **Status:** NEEDS VERIFICATION`n"

    foreach ($num in $citNums) {
        $source = $sourceMap[$num]
        $output += "- **Source:** [$num] $source`n"
    }

    $output += "`n"
}

$output += "---`n`n## Bibliography (from NotebookLM output)`n`n"
foreach ($num in $citations) {
    $source = $sourceMap[$num]
    $output += "[$num] $source`n"
}

$output | Out-File $OutputFile -Encoding UTF8
Write-Host "Citations extracted to $OutputFile"
```

### Anti-Patterns to Avoid
- **Don't automate NotebookLM queries** - REQUIREMENTS.md explicitly rules this out as brittle
- **Don't create single mega-template** - Users need focused prompts for specific tasks, not one-size-fits-all
- **Don't skip session logging** - Findings get lost without structured capture between NotebookLM and VERIFIED-RESEARCH.md
- **Don't parse citations manually** - Error-prone and time-consuming, use script

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Prompt organization | Flat list of examples | Categorized library with templates | User needs to find right prompt fast by use case, not browse examples |
| Citation extraction | Copy-paste each citation individually | Regex-based parser script | NotebookLM uses consistent [N] format, automate extraction |
| Session documentation | Ad-hoc notes | Standardized template | Ensures consistency, nothing gets lost, clear transfer to VERIFIED-RESEARCH.md |
| Template customization | Rewrite prompts each time | [PLACEHOLDER] system | Fill-in-the-blanks faster than rewriting |

**Key insight:** This is a "workflow optimization" phase, not "feature development." The goal is to reduce friction in existing manual processes, not build new automation.

## Common Pitfalls

### Pitfall 1: Template Overgeneralization
**What goes wrong:** Creating generic prompts that work for any research, losing channel-specific value
**Why it happens:** Trying to make templates "reusable" for all contexts
**How to avoid:** Encode channel-specific frameworks (Big Six, Kahan identity stakes, Toulmin argument structure) into templates. Generic = less useful.
**Warning signs:** Template says "analyze the topic" instead of "assess identity stakes using Kahan's framework"

### Pitfall 2: Citation Format Assumptions
**What goes wrong:** Parser breaks when NotebookLM output format varies slightly
**Why it happens:** Assuming [1], [2] format is always consistent
**How to avoid:**
- Parse multiple format variants (inline citations, footnote-style, "Source: Title" format)
- Test with real NotebookLM outputs from multiple sessions
- Graceful degradation when format unrecognized
**Warning signs:** Script works on test data but fails on real paste

### Pitfall 3: Session Log Abandonment
**What goes wrong:** Users create logs for first video, then stop using them
**Why it happens:** Template too complex, unclear value, or redundant with VERIFIED-RESEARCH.md
**How to avoid:**
- Make template quick to fill (5-10 minutes max)
- Clear value proposition: "session log = intermediate capture before committing to VERIFIED-RESEARCH"
- Show it prevents lost findings between NotebookLM and script
**Warning signs:** Template has 20+ fields to fill manually

### Pitfall 4: Prompt Template Bloat
**What goes wrong:** Adding 50+ prompts that users never use
**Why it happens:** "More is better" thinking
**How to avoid:**
- Start with 15-20 most common scenarios
- Track actual usage
- Add new templates only when users repeatedly ask for them
**Warning signs:** Most templates have zero usage after 3 months

### Pitfall 5: Ignoring Existing Patterns
**What goes wrong:** Creating new formats that conflict with existing PROJECT-STATUS.md, VERIFIED-RESEARCH.md conventions
**Why it happens:** Not reviewing existing project files first
**How to avoid:**
- Study bir-tawil, flat-earth, chagos examples
- Match emoji conventions (✅⚠️🔄❌)
- Use existing file naming patterns
**Warning signs:** New files don't look like existing project documentation

## Code Examples

Verified patterns from research:

### Prompt Template Example (Timeline Extraction)
```markdown
# Timeline Extraction

**Use case:** Converting scattered date references into chronological sequence for Act 1 setup
**Sources needed:** All primary and secondary sources uploaded
**Expected output:** Chronological list with dates, events, and citations

## Prompt Template

> I'm creating a video about [TOPIC]. I need a chronological timeline of key events.
>
> Using ALL uploaded sources, extract:
> 1. Every dated event mentioned (year, month/day if available)
> 2. The event description (1 sentence max)
> 3. The source citation (Title, page number)
>
> Format as:
> **[DATE]:** [Event description] [Citation number]
>
> Sort from earliest to latest. If multiple sources mention same event, list all citations.
>
> Focus on events central to [SPECIFIC ASPECT OF TOPIC - e.g., "the myth's creation" or "territorial dispute escalation"].

## Example Usage

**Context:** Flat Earth video Act 2 (myth invention timeline)
**Customized prompt:**
> I'm creating a video about the medieval flat earth myth. I need a chronological timeline of key myth-creation events.
>
> Using ALL uploaded sources, extract:
> 1. Every dated event mentioned about how the myth was created/spread (1828-1950)
> 2. The event description (1 sentence max)
> 3. The source citation (Title, page number)
>
> Focus on events central to the myth's creation and propagation.

**Output sample:**
> **1828:** Washington Irving publishes *A History of the Life and Voyages of Christopher Columbus*, inventing the Salamanca flat-earth debate [1]
> **1874:** John William Draper's *History of the Conflict Between Religion and Science* popularizes conflict thesis [2]
> **1896:** Andrew Dickson White's *A History of the Warfare of Science with Theology in Christendom* gives myth scholarly veneer [3]
```

### Citation Extraction Script (Bash Alternative)
```bash
#!/bin/bash
# extract-citations.sh
# Parses NotebookLM output into structured claims + bibliography

INPUT_FILE="$1"
OUTPUT_FILE="${2:-extracted-citations.md}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found"
    exit 1
fi

# Read file content
CONTENT=$(cat "$INPUT_FILE")

# Split at "SOURCES:" marker
TEXT=$(echo "$CONTENT" | sed -n '1,/SOURCES:/p' | sed '$d')
SOURCES=$(echo "$CONTENT" | sed -n '/SOURCES:/,$p' | tail -n +2)

# Start output file
echo "## Extracted Claims" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Extract sentences with citations [N]
echo "$TEXT" | grep -oP '([^.]+\[\d+\][^.]*\.)' | while read -r CLAIM; do
    # Clean citation markers for claim text
    CLEAN_CLAIM=$(echo "$CLAIM" | sed 's/\[\d\+\]//g' | xargs)

    echo "**Claim:** $CLEAN_CLAIM" >> "$OUTPUT_FILE"
    echo "- **Status:** NEEDS VERIFICATION" >> "$OUTPUT_FILE"

    # Extract citation numbers from this claim
    echo "$CLAIM" | grep -oP '\[\K\d+(?=\])' | while read -r NUM; do
        SOURCE=$(echo "$SOURCES" | grep "^$NUM\." | sed "s/^$NUM\. //")
        echo "- **Source:** [$NUM] $SOURCE" >> "$OUTPUT_FILE"
    done

    echo "" >> "$OUTPUT_FILE"
done

# Add bibliography section
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Bibliography (from NotebookLM output)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "$SOURCES" | grep -P '^\d+\.' | while read -r LINE; do
    NUM=$(echo "$LINE" | grep -oP '^\d+')
    SOURCE=$(echo "$LINE" | sed "s/^$NUM\. //")
    echo "[$NUM] $SOURCE" >> "$OUTPUT_FILE"
done

echo "Citations extracted to $OUTPUT_FILE"
```

### Session Log Template (Standardized)
```markdown
# NotebookLM Session Log - [Topic Name]

**Date:** [YYYY-MM-DD]
**Session focus:** [What you're researching in this session]
**Notebook(s):** [Which NotebookLM notebook(s) queried]
**Prompts used:** [Template IDs: Timeline-1, Argument-2, etc.]
**Duration:** [Approx time spent]
**Status:** 🟡 In Progress / 🟢 Ready for Scripting

---

## Quick Summary

**What I was trying to verify:**
- [Research question 1]
- [Research question 2]

**What I found:**
- [Key finding 1]
- [Key finding 2]

**Still need to research:**
- [Gap 1]
- [Gap 2]

---

## Findings by Claim (Detailed)

### CLAIM 1: "[Statement being verified]"

**Verdict:** ✅ VERIFIED / ⚠️ PARTIALLY VERIFIED / 🔄 NEEDS HEDGE / ❌ UNVERIFIABLE

**Evidence:**
- [Quote or data from NotebookLM]
- **Source:** [Title cited by NotebookLM] [Page/section]
- **Citation number:** [1] (as it appears in NotebookLM output)

**Confidence:** HIGH / MEDIUM / LOW
**Why:** [Reason for confidence level]

**Script-ready language:**
> "[How this will be phrased in the script - with proper hedging if needed]"

**On-screen display:**
> [If this is a quote that will be shown on screen, format it here exactly as it should appear]

---

### CLAIM 2: ...

[Repeat structure for each claim verified]

---

## Next Actions

- [ ] Transfer ✅ VERIFIED claims to 01-VERIFIED-RESEARCH.md
- [ ] Re-query NotebookLM for [specific gap]
- [ ] Find additional source for [partially verified claim]
- [ ] Update PROJECT-STATUS.md with verification percentage

---

## Notes & Insights

**Surprising findings:**
- [Anything unexpected]

**Potential script angles:**
- [Ideas sparked by research]

**Cross-video connections:**
- [Links to other videos in production]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Ad-hoc NotebookLM queries | 13 use case prompts in REFERENCE doc | Dec 2025 | Faster research setup, but still needs expansion |
| Copy-paste citations manually | (None - manual) | N/A | Phase 14 will add parser |
| Scattered notes | Example session logs (bir-tawil) | Jan 2025 | Inconsistent format, needs standardization |
| Generic research prompts | Channel-specific frameworks (Big Six, Kahan) | Dec 2025 | Higher quality research aligned with channel voice |

**Recent NotebookLM updates (2026):**
- **Gemini 3 integration:** Faster, more accurate responses
- **Deep Research mode:** Multi-step decomposition, parallel searches, structured briefing
- **Enhanced citations:** Inline [N] format with clickable source scrolling
- **Data tables:** Convert sources to structured tables
- **Learning features:** Flashcards, quizzes, learning guides

**What this means for Phase 14:**
- Citation extraction is feasible (consistent [N] format)
- Deep Research mode not yet needed (manual workflow preferred)
- Templates should encode "source constraints" (tell NotebookLM which sources to trust)

**Deprecated/outdated:**
- NotebookLM API automation - explicitly out of scope per REQUIREMENTS.md
- Generic research prompts - channel now has domain-specific frameworks

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal number of prompt templates**
   - What we know: Existing doc has 13, requirement says "15+"
   - What's unclear: Sweet spot between coverage and discoverability
   - Recommendation: Start with 17 templates (13 existing + 4 new high-value), track usage, add more based on user requests

2. **Citation extraction robustness**
   - What we know: NotebookLM uses [N] format consistently in 2026
   - What's unclear: Edge cases (footnotes, multiple formats in one response)
   - Recommendation: Build parser for primary [N] format, log unparseable sections for manual review

3. **Session log adoption**
   - What we know: bir-tawil example shows value, but only one instance
   - What's unclear: Will users consistently use standardized template?
   - Recommendation: Keep template minimal (5-10 min to fill), show clear value in reducing re-research

4. **Cross-project citation reuse**
   - What we know: .claude/VERIFIED-CLAIMS-DATABASE.md exists for fact reuse
   - What's unclear: How session logs should feed into cross-project database
   - Recommendation: Phase 14 focuses on single-project workflow, defer cross-project synthesis to future phase

## Sources

### Primary (HIGH confidence)
- Existing channel documentation:
  - D:\History vs Hype\.claude\REFERENCE\NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md (13 use cases)
  - D:\History vs Hype\.claude\REFERENCE\NOTEBOOKLM-SOURCE-STANDARDS.md (standards + 2026 features)
  - D:\History vs Hype\video-projects\_IN_PRODUCTION\6-bir-tawil-2025\NOTEBOOKLM-RESEARCH-RESULTS.md (session log example)
  - D:\History vs Hype\video-projects\_IN_PRODUCTION\19-flat-earth-medieval-2025\NOTEBOOKLM-SOURCE-LIST.md (source organization pattern)
  - D:\History vs Hype\video-projects\_IN_PRODUCTION\19-flat-earth-medieval-2025\NOTEBOOKLM-PROMPTS.md (prompt examples)

### Secondary (MEDIUM confidence)
- [NotebookLM 2026 Guide: Features, Tools & Best Practices](https://www.geeky-gadgets.com/notebooklm-complete-guide-2026/) - Gemini 3, Deep Research features
- [NotebookLM Evolution: Complete Guide 2023-2026](https://medium.com/@jimmisound/the-cognitive-engine-a-comprehensive-analysis-of-notebooklms-evolution-2023-2026-90b7a7c2df36) - Feature timeline
- [NotebookLM Research Upgrade 2026](https://www.geeky-gadgets.com/notebooklm-research-upgrade-2026/) - 2026 updates
- [How To Use NotebookLM For Research In 2026](https://7scribes.com/how-to-use-notebooklm-for-research-in-2026/) - Academic workflow best practices

### Tertiary (LOW confidence)
- [notebookLM-citation GitHub](https://github.com/nicremo/notebookLM-citation) - Browser extension for citation preservation (not needed for manual workflow)
- [NotebookLM API on Apify](https://apify.com/clearpath/notebooklm-api) - Third-party API wrapper (explicitly not using per REQUIREMENTS.md)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Existing Markdown/template infrastructure, no new tools needed
- Architecture: HIGH - Clear patterns from existing project files, minimal new structure
- Pitfalls: MEDIUM - Based on general workflow design principles, not NotebookLM-specific experience reports

**Research date:** 2026-01-30
**Valid until:** 90 days (NotebookLM features stable, workflow patterns unlikely to change)

**Key assumptions verified:**
- ✅ NotebookLM uses consistent [N] citation format (verified from existing project files)
- ✅ Channel already uses Markdown for all documentation (verified from repo structure)
- ✅ Session logging pattern exists and is valuable (verified from bir-tawil example)
- ✅ 13 prompt use cases already documented (verified from SCRIPTWRITING-PROMPTS.md)
- ✅ No automation desired (verified from REQUIREMENTS.md "Out of Scope" section)

**Implementation risks:**
- LOW: Prompt templates (copy existing patterns)
- LOW: Session log template (standardize existing bir-tawil format)
- MEDIUM: Citation parser (regex complexity, format edge cases)
