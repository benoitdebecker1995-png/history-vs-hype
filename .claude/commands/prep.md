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
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--edit-guide` | Shot-by-shot visual staging guide | `/prep --edit-guide 19-flat-earth-medieval-2025` |
| `--assets` | Zero-budget DIY B-roll guide | `/prep --assets 19-flat-earth-medieval-2025` |
| `--full` | Both guides in one workflow | `/prep --full 19-flat-earth-medieval-2025` |

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
