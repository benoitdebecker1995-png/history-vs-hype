---
description: Filming preparation - edit guides, B-roll planning, asset creation (Production Phase 3)
model: haiku
---

# /prep - Filming Preparation Entry Point

Generate editing guides, B-roll plans, and asset creation guides. Everything needed to prepare for filming.

## Usage

```
/prep                        # Interactive: asks what you need
/prep --edit-guide [project] # Generate shot-by-shot editing guide
/prep --assets [project]     # Generate zero-budget asset guide
/prep --full [project]       # Both edit guide + assets
/prep --split-screen [project] # Split-screen edit guide for document walkthrough
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--edit-guide` | Shot-by-shot visual staging guide | `/prep --edit-guide 19-flat-earth-medieval-2025` |
| `--assets` | Zero-budget DIY B-roll guide | `/prep --assets 19-flat-earth-medieval-2025` |
| `--full` | Both guides in one workflow | `/prep --full 19-flat-earth-medieval-2025` |
| `--split-screen` | Split-screen edit guide for document videos | `/prep --split-screen 37-vichy-statut-juifs-2026` |

---

## Channel Insights Context (Auto-run)

Before generating output, check for own-channel performance context:

1. Read `channel-data/channel-insights.md` if it exists
2. Use as **internal context** for decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- Channel Performance Context ---
[Extract 2-3 most relevant lines from channel-insights.md for this workflow]
Example: Top format: territorial (avg 1,950 views). Best retention: 42.0%.
Low signal: ~15 videos — experiment freely.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing analytics
5. Insights are advisory — guide experimentation, never dictate choices

**For /prep:** Focus on format/length insights (what video lengths retain best, what B-roll types correlate with engagement)

---

## YouTube Intelligence Context (Auto-run)

Before generating output, check for YouTube algorithm and niche intelligence:

1. Read `channel-data/youtube-intelligence.md` if it exists
2. Use as **internal context** for production decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- YouTube Intelligence Context ---
[Extract 2-3 most relevant lines from youtube-intelligence.md for this workflow]
Example: Niche trend: 20-30min docs with evidence B-roll outperforming shorter formats.
Competitor gap: No channels covering [topic angle] — differentiation opportunity.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing intelligence
5. If last refresh date is >30 days old, add note: "(Intel last refreshed [date] — consider running /intel --refresh)"
6. Intelligence is advisory — inform production decisions, never dictate

**For /prep:** Focus on:
- **Format/length insights:** What video lengths and formats are performing in the niche
- **B-roll patterns:** What visual styles correlate with outlier performance (evidence on screen, maps, documents)
- **Competitor production patterns:** What production approaches competitors are using

---

## Feedback Insights (Automatic)

Before generating prep materials, surface past production insights.

**Run automatically:**
```python
import sys
sys.path.insert(0, 'tools/youtube_analytics')
from feedback_queries import get_insights_preamble
topic = '{topic_type}'
preamble = get_insights_preamble(topic, 'prep')
if preamble:
    print(preamble)
else:
    print('No past performance insights available. Run: python -m tools.youtube_analytics.feedback backfill')
```

**Display the insights preamble** before generating prep outputs. If no insights, skip silently.

**Insight types for /prep:** Production insights (B-roll density, edit pacing, visual evidence patterns).

---

## Fact-Check Verification Gate (MANDATORY — Runs Before All Prep Output)

**Applies to:** ALL modes — `--edit-guide`, `--assets`, `--full`, `--split-screen`, and interactive (no mode specified). No exceptions — all prep modes are pre-filming and require verified facts.

**Step 1: Locate the fact-check file.**

Glob for `video-projects/**/[project]/03-FACT-CHECK-VERIFICATION.md`. If the file is not found, BLOCK — display the message below and STOP. Do NOT proceed.

```
--- FACT-CHECK VERIFICATION GATE: BLOCKED ---
Project: [project-name]
Status: No fact-check file found

Cannot proceed: 03-FACT-CHECK-VERIFICATION.md does not exist.
Run /verify first to generate the fact-check report, then re-run /prep.
---
```

**Step 2: Scan for verdict line.**

Search the file for lines containing "Verdict:" (case-insensitive). Check if the word "APPROVED" appears anywhere on that line.

- If NO line contains "Verdict:" at all — treat as placeholder/incomplete file. BLOCK:

```
--- FACT-CHECK VERIFICATION GATE: BLOCKED ---
Project: [project-name]
Status: Fact-check file exists but contains no verdict

Cannot proceed: 03-FACT-CHECK-VERIFICATION.md has no verdict line.
Complete the fact-check with /verify, then re-run /prep.
---
```

- If a verdict line exists but does NOT contain "APPROVED" — BLOCK. Extract the actual verdict text for display. Also scan the file for severity markers to build an issue summary:
  - Count lines/sections containing red circle emoji or "REQUIRED FIX" = required fixes
  - Count lines/sections containing yellow circle emoji or "SIMPLIFICATION" = simplification flags
  - Count lines/sections containing warning emoji or "NEEDS CLARIFICATION" or "Needs clarification" = clarification items

```
--- FACT-CHECK VERIFICATION GATE: BLOCKED ---
Project: [project-name]
Verdict: [extracted verdict text from the verdict line]
Required fixes: N
Clarification needed: N
Simplification flags: N

Cannot proceed: Fact-check verdict is not APPROVED.
Address the issues in 03-FACT-CHECK-VERIFICATION.md, re-run /verify, then re-run /prep.
---
```

After the bordered block, list each outstanding item with a one-line description. Format:
```
Outstanding items:
- [RED CIRCLE] [item title]: [one-line description from the file]
- [WARNING] [item title]: [one-line description]
```

**Step 3: Handle APPROVED verdict.**

If the verdict line contains "APPROVED":

First, check if any required fix sections still exist in the file (lines with red circle emoji or "REQUIRED FIX"). If yes, PASS but with a WARNING:

```
--- Fact-Check Verification Gate: PASSED (with warnings) ---
Verdict: [extracted verdict text]
Note: N required fix(es) still listed — verify these are resolved before filming.
---
```

If APPROVED with no outstanding required fixes, clean PASS. Extract summary stats from the executive summary table if present (total claims, verified count):

```
--- Fact-Check Verification Gate: PASSED ---
Verdict: [extracted verdict text]
Claims: X verified of Y total
---
```

Then proceed normally to the prep output generation.

---

## EDIT GUIDE (`--edit-guide`)

Generate comprehensive shot-by-shot editing guide from filmed A-roll.

### Before Starting

1. **Read the SRT file** - Get exact timestamps, total runtime, identify transcription errors
2. **Read the SCRIPT.md** - Understand argument structure and intended visuals
3. **Compare runtimes** - Script estimate vs actual SRT runtime (identifies pacing drift)
4. **Identify cut candidates FIRST** - Before shot-by-shot breakdown

### Required Sections (MANDATORY FORMAT)

#### 1. Header with Runtime Comparison

```markdown
# [VIDEO TITLE] - EDITING GUIDE

**Project:** [folder-name]
**Script Estimate:** [X] min
**Actual SRT Runtime:** [Y] min
**Delta:** [+/-Z] min ([needs trimming / on target / has room])
**Date Created:** [date]
```

**Runtime estimation:**
- Script: words / 150 = approximate minutes
- SRT: last timestamp = actual duration
- Delta interpretation:
  - +3 min or more: Needs trimming
  - +1-3 min: Light trimming
  - On target (+/- 1 min): Good
  - -1 min or more: Too short

#### 2. Cut Candidates

**MANDATORY before shot breakdown.**

```markdown
## CUT CANDIDATES

**Target:** Trim [X] minutes to reach [Y] minute target

### Priority 1: Easy Cuts (No narrative impact)
| Section | Timestamp | Duration | Cut Type | Saves |
|---------|-----------|----------|----------|-------|

### Priority 2: Moderate Cuts (Minor narrative impact)
| Section | Timestamp | Duration | Cut Type | Impact | Saves |
|---------|-----------|----------|----------|--------|-------|

### Priority 3: Hard Cuts (Significant tradeoffs)
| Section | Timestamp | Duration | Why it could go | Why it should stay |
|---------|-----------|----------|-----------------|-------------------|

### DO NOT CUT (Core to argument)
- [Section]: [Why essential]
```

**Cut Types:**
- **Full remove:** Delete entire section
- **Tighten:** Remove pauses, filler, redundant phrases
- **Condense:** Combine two sections saying similar things
- **Move to B-roll:** Cover with visuals while shortening VO

#### 3. Pacing & Retention Risk Analysis

```markdown
## PACING ANALYSIS

### Retention Risk Zones
| Timestamp | Duration | Risk | Issue | Fix |
|-----------|----------|------|-------|-----|

### Redundancy Flags
| First Instance | Second Instance | Recommendation |
|----------------|-----------------|----------------|

### Pattern Interrupt Check
- 0:00-2:00: [Status]
- 2:00-4:00: [Status]
[Continue every 2 min...]
```

#### 4. Editing Philosophy

```markdown
## EDITING PHILOSOPHY

**The Golden Rule:** If the B-roll doesn't make your argument stronger, stay on camera.

**B-roll is EVIDENCE, not decoration.**

Use B-roll when:
- [List specific to this video]

Stay on camera when:
- [List specific to this video]

**Target Ratio:** 65% talking head, 35% B-roll
```

#### 5. SRT Corrections

```markdown
## SRT CORRECTIONS (Fix in DaVinci before export)

| SRT # | Timestamp | Wrong | Correct |
|-------|-----------|-------|---------|
```

#### 6. Shot-by-Shot Breakdown

**Every shot MUST have ALL fields:**

```markdown
#### SHOT [#]: [TALKING HEAD/B-ROLL] - [Description] ([START] - [END])
**SRT #[X-Y]** | **Duration: [X] sec**

> "[Exact transcript text]"

**VISUAL:** [What to show - be SPECIFIC]
- [Detailed description]
- [Text overlays with exact wording]

**WHY [TALKING HEAD/B-ROLL]:** [Editorial reasoning]

**CAMERA NOTES:** [Performance direction - tone, emphasis]

**SOURCES:** (for B-roll only)
- [Specific source with search terms]

**CREATE IN:** [Tool] (for graphics only)
```

### Output Location

`video-projects/[project]/EDITING-GUIDE.md`

---

## ZERO-BUDGET ASSETS (`--assets`)

Generate comprehensive DIY guide for creating B-roll using free tools.

### Day-by-Day Workflow

**Day 1: Critical assets (3 hours)** - Can START FILMING after this
**Day 2-4: Remaining assets (6-8 hours total)**

### Free Tools Covered

| Tool | Use For |
|------|---------|
| **Canva** (free) | Quote documents, timelines, charts |
| **MapChart.net** | Historical maps, country highlights |
| **Google My Maps** | Routes, custom geographic data |
| **Wikimedia Commons** | Public domain historical images |
| **PowerPoint/Slides** | Alternative to all above |
| **Windows Snipping Tool** | Modern context screenshots |

### For Each Asset

- Step-by-step instructions (specific, not vague)
- Time estimates (realistic planning)
- Alternative methods (backup options)
- File naming conventions (organized workflow)

### Pro Tips Section

- Batch workflows (save 30-40% time)
- Canva keyboard shortcuts
- Template duplication techniques
- Quality standards for 1080p video

### Output Format

```markdown
# DIY ASSET GUIDE: [Video Title]

**Total Assets Needed:** [X]
**Day 1 (Critical):** [X] assets, [X] hours
**Day 2-4 (Remaining):** [X] assets, [X] hours

## DAY 1: CRITICAL ASSETS (Start filming after these)

### Asset 1: [Name]
**Type:** [Map / Quote Document / Timeline / etc.]
**Tool:** [Canva / MapChart / etc.]
**Time:** [X] min

**Steps:**
1. [Specific instruction]
2. [Specific instruction]
3. [Specific instruction]

**File name:** `[consistent-naming].png`

**Alternative:** [Backup method if primary fails]

[Continue for all Day 1 assets...]

## DAY 2-4: REMAINING ASSETS

[Continue same format...]

## PRO TIPS

### Batch Workflows
[Time-saving techniques]

### Quality Standards
[1080p requirements, font sizes, etc.]
```

### Output Location

`video-projects/[project]/DIY-ASSET-GUIDE.md`

---

## FULL WORKFLOW (`--full`)

Run both edit guide and assets generation:

1. Generate EDITING-GUIDE.md
2. Generate DIY-ASSET-GUIDE.md
3. Generate B-ROLL-DOWNLOAD-LINKS.md (specific sources)

**Best for:** Complete filming preparation in one session.

### Additional Output: B-Roll Download Links

```markdown
# B-ROLL DOWNLOAD LINKS: [Video Title]

## MAPS

### [Map 1 Name]
**Source:** [Wikimedia Commons / MapChart / etc.]
**Direct Link:** [URL]
**License:** [CC0 / CC-BY / etc.]
**Modifications needed:** [Crop, highlight, etc.]

[Continue for all assets...]
```

---

## SPLIT-SCREEN EDIT GUIDE (`--split-screen`)

Generate editing guide for document walkthrough videos with split-screen staging.

### When to Use

Use split-screen mode when:
- Video is clause-by-clause document walkthrough (Untranslated Evidence format)
- Visual format is original-language text LEFT, English translation RIGHT
- Script generated with `/script --document-mode`
- Need editor-ready timing and transition markers

### Prerequisites

1. **Translation output exists:** Phase 40 translation pipeline completed
2. **Script exists:** `/script --document-mode` generated SCRIPT.md
3. **Translation verified:** `/verify --translation` returned GREEN or YELLOW

### Process

**Step 1: Locate files**
- Translation output: Auto-detect `*-TRANSLATION-FORMATTED.md` in project folder
- Script: Read `SCRIPT.md` from project folder
- Archive lookup results: Check for document URLs from Phase 39 (optional)

**Step 2: Parse structure**
- Extract clause breakdown from translation output
- Match script sections to clauses
- Calculate word counts per clause segment
- Identify surprise markers (MAJOR, NOTABLE)

**Step 3: Generate timing estimates**

Per-clause breakdown (at 150 WPM):
- Context setup (talking head): [X] sec
- Read original (split-screen): [X] sec + 2-3 sec pause
- Translate (split-screen): [X] sec + 2-3 sec pause
- Explain significance (talking head): [X] sec
- Connect to myth (talking head): [X] sec

Section-level totals:
- Articles 1-5: 8 min 30 sec (cumulative: 00:00 - 08:30)
- Articles 6-10: 7 min 15 sec (cumulative: 08:30 - 15:45)

**Step 4: Add transition markers**

**Explicit key transitions:**
```
[00:05:23] SWITCH TO SPLIT-SCREEN for Article 3 reading
[00:05:45] RETURN TO TALKING HEAD for significance explanation
```

**Ratio guidance per section:**
```
Section: Articles 1-5
Visual Ratio: 40% talking head, 60% split-screen
```

**Step 5: Source assets**

**Auto-sourced from archive lookup:**
- Document scans: Direct URLs from Légifrance, Wikisource, Internet Archive
- Archival versions: National archives, university repositories

**Manual placeholders:**
- Maps: `[NEEDED] - Map showing [context]`
- Photos: `[NEEDED] - Photo of [subject]`
- Charts: `[NEEDED] - Timeline showing [events]`

**Step 6: Flag surprise clauses**

Major surprises (must highlight):
```
⚠️ MAJOR SURPRISE - Article 7 (12:45)
EDITOR NOTE: Contradicts common narrative
Suggestion: Slow zoom on key phrase, highlight box
```

Notable surprises (worth highlighting):
```
📍 NOTABLE SURPRISE - Article 12 (18:20)
EDITOR NOTE: Adds important nuance
Suggestion: Brief hold on key phrase
```

### Output Format

**File:** `SPLIT-SCREEN-EDIT-GUIDE.md` in project folder

**Sections:**
1. **Overview:** Total duration, visual format, section count
2. **Section-by-section breakdown:** Clause timing, visual staging, transition markers
3. **Surprise markers:** Editor emphasis notes for MAJOR/NOTABLE surprises
4. **Asset checklist:** Auto-sourced URLs + manual creation placeholders
5. **Pacing notes:** Section-specific guidance (opening, middle, synthesis)
6. **Synthesis section:** Recap structure with B-roll timing
7. **Conclusion:** Closing guidance

### Flags

| Flag | Purpose |
|------|---------|
| `--translation PATH` | Specify translation file (overrides auto-detect) |
| `--script PATH` | Specify script file (overrides SCRIPT.md default) |

### Output Location

`video-projects/[project]/SPLIT-SCREEN-EDIT-GUIDE.md`

### After Generation

**Proactive suggestion:**
> "Split-screen edit guide complete.
> - Total duration: [X] min [Y] sec
> - [X] clauses with timing breakdowns
> - [X] assets auto-sourced, [X] manual creation needed
>
> Edit guide saved to SPLIT-SCREEN-EDIT-GUIDE.md.
> Asset checklist includes:
> - Auto-sourced: [list archive URLs]
> - Manual creation: [list needed assets]
>
> Ready to film and edit!"

### Example Usage

```bash
# Auto-detect translation and script in project folder
/prep --split-screen 37-vichy-statut-juifs-2026

# Specify files explicitly
/prep --split-screen 37-vichy-statut-juifs-2026 --translation path/to/translation.md --script path/to/script.md
```

### Integration with Split-Screen Workflow

**Typical sequence:**
```
Phase 40: python tools/translation/cli.py full --language french ...
/verify --translation [project]
/script --document-mode [project]
/verify --script [project]
/prep --split-screen [project]  ← You are here
[User films + edits with split-screen guide]
/publish
```

### Reference Files

- **Format guide:** `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md`
- **Translation pipeline:** `tools/translation/cli.py`
- **Split-screen generator:** `tools/production/split_screen_guide.py`

---

## Integration with Production Workflow

### Typical Sequence

```
/script --new [project]      # Write script
/verify --script [project]   # Fact-check
[User films A-roll]
/prep --edit-guide [project] # Generate editing guide
/prep --assets [project]     # Generate asset guide
[User creates assets, edits video]
/publish                     # Generate metadata
```

### Prerequisites

- SCRIPT.md exists (for --assets)
- SRT file exists (for --edit-guide with runtime comparison)
- Fact-check APPROVED (for --full)

---

## Reference Examples

**Good editing guides to match:**
- `video-projects/_IN_PRODUCTION/6-bir-tawil-2025/EDITING-GUIDE.md`
- `video-projects/_IN_PRODUCTION/3-fuentes-fact-check-2025/FUENTES-EDITING-GUIDE.md`

**Quality standards:**
- WHY for every shot decision
- Camera notes for delivery
- Specific asset sources (not generic)
- Duration per shot
- Editing philosophy at top
- Retention timing section

---

## Absorbed Commands

This command consolidates functionality from:
- `/edit-guide` - Shot-by-shot editing guide
- `/zero-budget-assets` - DIY B-roll creation guide

All original functionality preserved through flags.
