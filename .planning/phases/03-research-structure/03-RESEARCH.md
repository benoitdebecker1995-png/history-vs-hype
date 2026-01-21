# Phase 3: Research Structure - Research

**Researched:** 2026-01-21
**Domain:** Research file organization and cross-video knowledge management
**Confidence:** HIGH

## Summary

This research examines the current state of research organization in the History vs Hype workspace and identifies opportunities for improvement. The workspace already has strong foundations: a 3-phase verified workflow (01-VERIFIED-RESEARCH.md -> 02-SCRIPT-DRAFT.md -> 03-FACT-CHECK-VERIFICATION.md), detailed templates, and an existing cross-video claims database.

The primary gaps are:
1. **Inconsistent research file organization** - Some projects use `_research/` subfolders with multiple files, others have everything at project root
2. **Claims database underutilized** - Only 2 topic clusters populated despite 6+ completed videos
3. **Source attribution format varies** - No single standard enforced across all research files
4. **NotebookLM outputs scattered** - Some in project folders, some in `research/` folder, no clear integration point

**Primary recommendation:** Standardize the per-video research structure while making the cross-video claims database a mandatory checkpoint in the workflow.

## Current State Analysis

### What Exists

| File/System | Location | Purpose | Status |
|-------------|----------|---------|--------|
| 01-VERIFIED-RESEARCH-TEMPLATE.md | `.claude/templates/` | Per-video research structure | Good template, inconsistently followed |
| VERIFIED-CLAIMS-DATABASE.md | `.claude/` | Cross-video fact reuse | 2 topic clusters only (Belize-Guatemala, Somaliland) |
| NOTEBOOKLM-SOURCE-STANDARDS.md | `.claude/REFERENCE/` | Source quality requirements | Comprehensive, well-documented |
| research/ folder | Root | Pre-commitment topic exploration | 35+ files, cleanup incomplete |
| _research/ subfolders | Per-project | NotebookLM prompts, source lists | Used in 4 of 6 active projects |

### Current Per-Video Research Patterns

**Pattern A: Flat structure (Flat Earth, Somaliland)**
```
19-flat-earth-medieval-2025/
  01-VERIFIED-RESEARCH.md        # Main research document
  02-SCRIPT-DRAFT.md
  03-FACT-CHECK-VERIFICATION.md
  FINAL-SCRIPT.md
  EDITING-GUIDE.md
  [Other production files]
```

**Pattern B: With _research subfolder (Fuentes, Crusades, Haiti)**
```
3-fuentes-fact-check-2025/
  01-VERIFIED-RESEARCH.md
  02-SCRIPT-DRAFT.md
  _research/
    00-QUICK-START-CHECKLIST.md
    01-topic-brief.md
    02-preliminary-research.md
    03-source-recommendations.md
    04-notebooklm-prompts.md
    DOWNLOAD-CHECKLIST.md
    FINAL-NOTEBOOKLM-SOURCES.md
    GROK-RESEARCH-RAW.md
    notebooklm output fuentes.md
    PROJECT-STATUS.md
```

**Observation:** Pattern B creates more files but better supports the two-phase research workflow (preliminary internet research -> NotebookLM academic verification).

### Source Attribution Formats Currently In Use

**Format 1: Inline quotes with attribution (Somaliland)**
```markdown
**Verified quote:**
> "union between Somaliland and Somalia was never ratified"
> — AU 2005 Mission, p.4
```

**Format 2: Source + page table (Flat Earth)**
```markdown
**Sources:**
1. Russell (Tier 1) - *Inventing the Flat Earth*, p. 47
2. Gould (Tier 1) - *Dinosaur in a Haystack*, p. 192
```

**Format 3: Full bibliographic in template**
```markdown
### [A1] Stein, Eric. *Czecho/Slovakia*
- **Type:** Academic monograph
- **Publisher:** University of Michigan Press, 2000
- **ISBN:** 978-0472108046
- **Access:** JSTOR
```

### Cross-Video Claims Database Analysis

The existing VERIFIED-CLAIMS-DATABASE.md has excellent structure:
- Topic clusters organized by subject
- Each claim has: verified date, video used in, tier, status, minimum 2 sources, notes
- Sections for research gaps, outdated claims, usage statistics
- Integration instructions for `/script`, `/fact-check`, `/respond-to-comment`

**Gap:** Only 2 of 6+ video topics have entries:
- Belize-Guatemala: 4 claims
- Somaliland: 6 claims
- Missing: Flat Earth medieval, Crusades, Haiti, JD Vance, Dark Ages, Fuentes

**Impact:** Verified facts from completed videos are not being captured for reuse.

## Architecture Patterns

### Recommended Project Structure

**Standard per-video structure:**
```
[number]-[topic]-[year]/
  01-VERIFIED-RESEARCH.md          # Single source of truth
  02-SCRIPT-DRAFT.md               # Written from verified facts only
  03-FACT-CHECK-VERIFICATION.md    # Cross-check before filming
  _research/                       # Supporting research materials
    00-NOTEBOOKLM-SOURCE-LIST.md   # What to download (mandatory)
    01-PRELIMINARY-RESEARCH.md     # Internet research (Phase 1)
    02-NOTEBOOKLM-PROMPTS.md       # Verification queries (Phase 2)
    [notebooklm-outputs/]          # Raw outputs, organized by date
  FINAL-SCRIPT.md                  # Production-ready script
  [Other production files]
```

**Rationale:**
- `01-VERIFIED-RESEARCH.md` at root = easy to find, single source of truth
- `_research/` subfolder = keeps supporting materials organized but out of the way
- Numbered prefixes = clear workflow order
- NotebookLM outputs in subfolder = preserves raw data without cluttering main view

### Source Attribution Standard

**Recommended unified format:**

For **quotes** (display on screen):
```markdown
### Quote: [Topic/Description]
> "[Exact quote, word-for-word]"
>
> **Source:** [Author], *[Title]*, p. [page]
> **Tier:** [1/2/3]
> **Verified:** [date]
> **Used in script:** Lines [XX-YY]
```

For **claims** (facts to use):
```markdown
### Claim: [Clear statement of fact]
**Status:** ✅ VERIFIED / ⏳ RESEARCHING / ❌ UNVERIFIABLE
**Sources (min 2):**
1. [Author] (Tier [1/2/3]) - *[Title]*, p. [page] - [URL if available]
2. [Author] (Tier [1/2/3]) - *[Title]*, p. [page]
**Notes:** [Context, caveats, how to present]
```

For **bibliographic entries** (source list):
```markdown
### [P1] [Document Name]
- **Type:** [Primary source / Academic monograph / etc.]
- **Author/Origin:** [Who created it, when]
- **Access:** [URL / Library / Purchased]
- **Key content:** [What's relevant to this video]
- **Status:** ✅ Downloaded / ⏳ Pending
```

### Cross-Video Claims Database Integration

**Recommended workflow checkpoint:**

BEFORE starting new video research:
```
1. Search VERIFIED-CLAIMS-DATABASE.md for topic keywords
2. Copy any existing verified claims to new 01-VERIFIED-RESEARCH.md
3. Mark copied claims as "Previously verified: [date], [video]"
4. Only research claims NOT already in database
```

AFTER completing video:
```
1. Extract reusable claims from 01-VERIFIED-RESEARCH.md
2. Add to appropriate topic cluster in VERIFIED-CLAIMS-DATABASE.md
3. Include: video title, verification date, tier, full sources
4. Flag any claims that may become outdated
```

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Source organization | Custom folder hierarchy per video | Standard `_research/` subfolder pattern | Consistency enables searching |
| Citation format | Ad-hoc formatting | Templates in `01-VERIFIED-RESEARCH-TEMPLATE.md` | Already comprehensive |
| Cross-video fact lookup | Manual memory / searching | VERIFIED-CLAIMS-DATABASE.md | Already structured, just needs population |
| NotebookLM workflow | Random prompts | NOTEBOOKLM-SOURCE-STANDARDS.md | Has prompt templates, checklist |

**Key insight:** The infrastructure exists. The gap is enforcement and population, not design.

## Common Pitfalls

### Pitfall 1: Research Files Outside Project Folders
**What goes wrong:** Research gets done in `research/` folder, then forgotten when video project starts
**Why it happens:** Exploration happens before committing to a video
**How to avoid:** When committing to a video, MOVE relevant files from `research/` to `_research/` subfolder
**Warning signs:** `research/` folder growing with files that have corresponding video projects

### Pitfall 2: Verified Claims Not Migrated to Database
**What goes wrong:** Same facts get researched multiple times across videos
**Why it happens:** No checkpoint in workflow to populate database
**How to avoid:** Add "Update VERIFIED-CLAIMS-DATABASE" as final step in video completion
**Warning signs:** Database has fewer topic clusters than completed videos

### Pitfall 3: Inconsistent Source Attribution
**What goes wrong:** Can't find citation when needed for YouTube description or comment response
**Why it happens:** Different formats used in different videos
**How to avoid:** Template enforcement; always include page number, access method, date accessed
**Warning signs:** "Source?" comments during fact-check phase

### Pitfall 4: NotebookLM Outputs Unprocessed
**What goes wrong:** Raw AI outputs never get distilled into VERIFIED-RESEARCH.md
**Why it happens:** NotebookLM is easy to use, but extraction is work
**How to avoid:** "Save to Notes" in NotebookLM, then structured transfer to research doc
**Warning signs:** Large `notebooklm output X.md` files with no corresponding entries in 01-VERIFIED-RESEARCH.md

### Pitfall 5: research/ Folder Becomes Dumping Ground
**What goes wrong:** 35+ files with inconsistent naming, duplicates, unclear purpose
**Why it happens:** No cleanup routine; files created during exploration never organized
**How to avoid:** Monthly cleanup; files older than 30 days either go to video project or archive
**Warning signs:** README.md "Cleanup Checklist" items never completed

## Implementation Approach

### Recommended Sequence

**Task Group 1: Standardize per-video structure**
1. Define canonical folder structure (as above)
2. Update 01-VERIFIED-RESEARCH-TEMPLATE.md if needed
3. Add `_research/` subfolder template with standard files

**Task Group 2: Make claims database a workflow checkpoint**
1. Add "Check VERIFIED-CLAIMS-DATABASE" to `/new-video` command
2. Add "Update VERIFIED-CLAIMS-DATABASE" to video completion checklist
3. Backfill database with claims from completed videos (Flat Earth, Dark Ages, etc.)

**Task Group 3: Enforce source attribution standard**
1. Update template to use unified format
2. Add attribution format to fact-check verification checklist
3. Ensure every claim has: source, page, tier, access method

**Task Group 4: Clean up research/ folder**
1. Complete cleanup checklist from README.md
2. Move relevant files to video project folders
3. Archive or delete outdated files
4. Establish monthly cleanup routine

### What NOT to Change

- Keep 01/02/03 numbered file convention (already established)
- Keep VERIFIED-CLAIMS-DATABASE.md location in `.claude/` (cross-video reference)
- Keep NOTEBOOKLM-SOURCE-STANDARDS.md as-is (comprehensive)
- Keep source tier system (1-4) already defined

## Code Examples

### Standard Source List Entry (NotebookLM-ready)

```markdown
## PRIMARY SOURCES [P]

### [P1] British Somaliland Independence Act 1960
- **Type:** Primary legislation
- **Date:** June 1960
- **Repository:** UK Parliament Archives
- **Access:** legislation.gov.uk (free)
- **Key content:** Legal instrument of independence
- **Status:** ✅ Downloaded
- **NotebookLM filename:** `[P1] British-Somaliland-Independence-Act-1960.pdf`

## ACADEMIC SOURCES [A]

### [A1] Crawford, James. *The Creation of States in International Law*
- **Type:** Academic monograph
- **Publisher:** Oxford University Press, 2006
- **ISBN:** 978-0199228423
- **Access:** University library
- **Key chapters:** Ch. 10 (Secession), Ch. 12 (Recognition)
- **Relevance:** Defines "restoration of independence" vs "secession"
- **Status:** ⏳ Pending download
- **NotebookLM filename:** `[A1] Crawford-Creation-of-States-Ch10-12.pdf`
```

### Standard Verified Claim Entry (Claims Database)

```markdown
### Medieval Europeans knew Earth was spherical
**Verified:** 2025-12-29
**Used in:** Medieval Flat Earth Myth (Video #19)
**Tier:** 1 (Primary sources + scholarly consensus)
**Status:** ✅ Current

**Sources:**
1. Russell, Jeffrey Burton - *Inventing the Flat Earth* (Praeger, 1991), pp. 1-5
   - "With extraordinary few exceptions no educated person in the history of Western Civilization from the third century B.C. onward believed that the earth was flat."
2. Gould, Stephen Jay - "The Late Birth of a Flat Earth" in *Dinosaur in a Haystack* (1996)
   - "From the seventh century to the fourteenth, every important medieval thinker concerned about the natural world stated more or less explicitly that the world was a round globe."
3. Aquinas, Thomas - *Summa Theologica* (c. 1265-1274)
   - "Both an astronomer and a physical scientist may demonstrate the same conclusion, for instance that the earth is spherical."

**Notes:** The rare exceptions (Lactantius, Cosmas Indicopleustes) were marginal figures. Cosmas was unknown in Western Europe until 1706.
```

### NotebookLM Verification Prompt Template

```markdown
## Verification Prompt for [Claim]

I need to verify this specific claim: "[Exact claim statement]"

Please:
1. Confirm if this is accurate based on the sources
2. Provide the exact source and page number (click the citation link)
3. Note any caveats or nuances
4. Identify if any scholars in these sources dispute this
5. Give me a word-for-word quote I can display on screen

If the claim is contested, tell me:
- What the majority view is
- What the minority view argues
- Which sources support each position
```

## State of the Art

| Current Approach | Recommended Approach | Impact |
|------------------|---------------------|--------|
| Per-video research structure varies | Standard `_research/` subfolder always | Findability, consistency |
| Claims database optional | Claims database mandatory checkpoint | 3-5x research time savings |
| Source attribution varies | Unified format with page numbers | Easier comment responses, descriptions |
| NotebookLM outputs scattered | Organized in `_research/notebooklm-outputs/` | Raw data preserved, distillation required |
| research/ folder unmanaged | Monthly cleanup routine | Prevents cruft accumulation |

## Open Questions

1. **Should _research/ subfolder be mandatory for all videos?**
   - Some videos (simple fact-checks) may not need extensive supporting files
   - Recommendation: Required for videos with 10+ sources, optional for simpler projects

2. **How much backfill of claims database is worthwhile?**
   - 6+ completed videos have claims not in database
   - Recommendation: Prioritize topics likely to recur (colonialism, borders, Middle Ages)

3. **Should research/ folder be eliminated entirely?**
   - Currently serves as "inbox" for topic exploration
   - Recommendation: Keep but enforce 30-day cleanup rule

## Sources

### Primary (HIGH confidence)
- Direct examination of workspace files:
  - `01-VERIFIED-RESEARCH-TEMPLATE.md`
  - `VERIFIED-CLAIMS-DATABASE.md`
  - `NOTEBOOKLM-SOURCE-STANDARDS.md`
  - `research/README.md`
  - Sample project folders (Somaliland, Flat Earth, Fuentes, Haiti)

### Secondary (HIGH confidence)
- Existing workflow documentation in CLAUDE.md
- Template files showing intended patterns

### Tertiary (N/A)
- No external research needed; this is workspace-specific organizational research

## Metadata

**Confidence breakdown:**
- Current state analysis: HIGH - direct file examination
- Recommended patterns: HIGH - based on existing best practices in workspace
- Pitfalls: HIGH - based on observed problems in current files

**Research date:** 2026-01-21
**Valid until:** Ongoing (workspace-specific, not time-sensitive)
