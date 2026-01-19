---
description: Generate shot-by-shot visual staging guide from A-roll transcript
---

You are creating an editing guide for filmed A-roll footage. Generate a comprehensive shot-by-shot breakdown following the **MANDATORY FORMAT** below.

## BEFORE YOU START

1. **Read the SRT file** - Get exact timestamps, total runtime, identify transcription errors
2. **Read the FINAL-SCRIPT** - Understand argument structure and intended visuals
3. **Compare runtimes** - Script estimate vs actual SRT runtime (identifies pacing drift)
4. **Identify cut candidates FIRST** - Before shot-by-shot breakdown

---

## MANDATORY FORMAT REQUIREMENTS

**Every editing guide MUST include these elements in this order:**

### 1. HEADER WITH RUNTIME COMPARISON
```markdown
# [VIDEO TITLE] - EDITING GUIDE

**Project:** [folder-name]
**Script Estimate:** [X] min
**Actual SRT Runtime:** [Y] min
**Delta:** [+/-Z] min ([needs trimming / on target / has room])
**Date Created:** [date]
```

**Runtime Estimation:**

*Script estimate calculation:*
- Count words in FINAL-SCRIPT (exclude stage directions, headers)
- Divide by 150 (average speaking pace for this channel)
- Result = approximate minutes

*SRT actual runtime:*
- Check last timestamp in SRT file
- This is the real recorded duration

*Delta interpretation:*
| Delta | Status | Action |
|-------|--------|--------|
| **+3 min or more** | Needs trimming | Use Priority 1 cuts first, then Priority 2 |
| **+1-3 min** | Light trimming | Priority 1 cuts should be sufficient |
| **On target (+/- 1 min)** | Good | Focus on pacing, not cutting |
| **-1 min or more** | Too short | May be rushed - check pacing, add breathing room |

### 2. CUT CANDIDATES (BEFORE shot breakdown)

**This section is MANDATORY.** Identify sections that can be trimmed if runtime needs reduction.

```markdown
## CUT CANDIDATES

**Target:** Trim [X] minutes to reach [Y] minute target

### Priority 1: Easy Cuts (No narrative impact)
| Section | Timestamp | Duration | Cut Type | Saves |
|---------|-----------|----------|----------|-------|
| [Name] | XX:XX-XX:XX | X sec | Full remove | X sec |
| [Name] | XX:XX-XX:XX | X sec | Tighten | X sec |

**Total Priority 1 savings:** [X] seconds

### Priority 2: Moderate Cuts (Minor narrative impact)
| Section | Timestamp | Duration | Cut Type | Impact | Saves |
|---------|-----------|----------|----------|--------|-------|
| [Name] | XX:XX-XX:XX | X sec | Full remove | [impact] | X sec |

**Total Priority 2 savings:** [X] seconds

### Priority 3: Hard Cuts (Significant tradeoffs)
| Section | Timestamp | Duration | Why it could go | Why it should stay |
|---------|-----------|----------|-----------------|-------------------|
| [Name] | XX:XX-XX:XX | X sec | [reason] | [reason] |

### DO NOT CUT (Core to argument)
- [Section]: [Why essential]
- [Section]: [Why essential]
```

**Cut Types:**
- **Full remove:** Delete entire section
- **Tighten:** Remove pauses, filler, redundant phrases
- **Condense:** Combine two sections saying similar things
- **Move to B-roll:** Cover with visuals while shortening VO

**How to Identify Cut Candidates:**

**Priority 1 (Easy Cuts):**
- Repeated explanations (saying the same thing twice in different words)
- Filler phrases ("So basically...", "What I mean is...", "In other words...")
- Unnecessary context that doesn't advance the argument
- Tangents that don't connect back to main thesis
- Pauses longer than 2 seconds
- Hedging language that weakens claims without adding nuance

**Priority 2 (Moderate Cuts):**
- Examples beyond the first two (diminishing returns on proof)
- Historical context that could be summarized in one sentence
- Quotes that could be shortened without losing core meaning
- Secondary evidence after the main proof is established
- Transitions that over-explain the connection

**Priority 3 (Hard Cuts):**
- Sections that feel like "darlings" (author loves them, audience doesn't need them)
- Secondary arguments that compete with rather than support the main thesis
- Evidence stacking beyond the proof point (when 3 examples exist but 1 suffices)
- Interesting tangents that belong in a separate video

**DO NOT CUT:**
- Opening hook (first 60 seconds) - critical for retention
- Thesis statements and reframes - structural anchors
- Primary source evidence shown on screen - channel differentiator
- Pattern interrupts every 90-120 seconds - retention tool
- Payoff moments that reward viewer patience
- Call to action - conversion opportunity

### 3. PACING & RETENTION RISK ANALYSIS
```markdown
## PACING ANALYSIS

### Retention Risk Zones (High dropout probability)
| Timestamp | Duration | Risk | Issue | Fix |
|-----------|----------|------|-------|-----|
| XX:XX-XX:XX | X sec | HIGH | [Dense exposition without visual change] | [Add B-roll / tighten] |
| XX:XX-XX:XX | X sec | MED | [Long talking head stretch] | [Pattern interrupt] |

### Redundancy Flags
| First Instance | Second Instance | Recommendation |
|----------------|-----------------|----------------|
| XX:XX "[quote]" | XX:XX "[similar]" | Keep first, cut second |

### Pattern Interrupt Check
- 0:00-2:00: [Hook - OK]
- 2:00-4:00: [Visual change at X:XX - OK / NEEDS INTERRUPT]
- [Continue every 2 min...]

**Rule:** Something should change every 90-120 seconds (visual, tone, or topic)
```

### 4. EDITING PHILOSOPHY SECTION
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

### 5. SRT CORRECTIONS TABLE
```markdown
## SRT CORRECTIONS (Fix in DaVinci before export)

| SRT # | Timestamp | Wrong | Correct |
|-------|-----------|-------|---------|
| X | XX:XX | "error" | "correction" |
```

### 6. SHOT-BY-SHOT FORMAT (MANDATORY STRUCTURE)

**Every single shot MUST have ALL of these fields:**

```markdown
#### SHOT [#]: [TALKING HEAD/B-ROLL] - [Description] ([START] - [END])
**SRT #[X-Y]** | **Duration: [X] sec**

> "[Exact transcript text for this segment]"

**VISUAL:** [What to show - be SPECIFIC]
- [Detailed description]
- [Text overlays with exact wording]
- [Source suggestions]

**WHY [TALKING HEAD/B-ROLL]:** [Explain the editorial reasoning - why this cut decision]

**CAMERA NOTES:** [Performance direction - tone, emphasis, delivery notes]

**SOURCES:** (for B-roll only)
- [Specific source with search terms]
- [Alternative source]

**CREATE IN:** [Tool - DaVinci/Canva/PowerPoint] (for graphics only)
```

**QUALITY STANDARDS FOR SHOT-BY-SHOT:**

- **WHY field is MANDATORY** - Every shot must explain the editorial reasoning
- **CAMERA NOTES are MANDATORY** - Performance direction for every talking head shot
- **SPECIFIC SOURCES are MANDATORY** - Not just "Wikimedia Commons" but specific item names
- **DURATION is MANDATORY** - Every shot needs timing in seconds

---

## Your Task

1. **Read the SRT file** - Get exact timestamps and identify transcription errors
2. **Read the FINAL-SCRIPT** - Understand argument structure and intended visuals
3. **Generate guide** - Following the MANDATORY FORMAT above exactly

## Reference Examples

**Good editing guides to match:**
- `video-projects/_IN_PRODUCTION/6-bir-tawil-2025/EDITING-GUIDE.md`
- `video-projects/_IN_PRODUCTION/3-fuentes-fact-check-2025/FUENTES-EDITING-GUIDE.md`

**These guides have:**
- WHY for every shot decision
- Camera notes for delivery
- Specific asset sources (not generic)
- Duration per shot
- Editing philosophy at top
- Retention timing section
- Troubleshooting section

---

## ALSO GENERATE: B-Roll Download Links

After creating the editing guide, generate companion file:
`video-projects/[topic-slug]/B-ROLL-DOWNLOAD-LINKS.md`

See existing B-ROLL-DOWNLOAD-LINKS.md files for format.

---

## Output Location

Save to: `video-projects/[lifecycle]/[project-folder]/EDITING-GUIDE.md`

**CRITICAL: Do NOT create a guide that's just a table of shots. Every shot needs WHY, CAMERA NOTES, and SPECIFIC SOURCES.**
