# A-Roll Editor Skill - History vs Hype

Generate shot-by-shot visual staging guides based on filmed A-roll transcripts. This skill takes your actual talking head footage and suggests exactly when to cut to B-roll, documents, maps, or graphics.

## CRITICAL: Quality Standards

**Every editing guide MUST match the quality of:**
- `video-projects/_IN_PRODUCTION/6-bir-tawil-2025/EDITING-GUIDE.md`
- `video-projects/_IN_PRODUCTION/3-fuentes-fact-check-2025/FUENTES-EDITING-GUIDE.md`

**Guides that are just tables of shots will be rejected. Every shot needs:**
1. **WHY** - Editorial reasoning for the cut decision
2. **CAMERA NOTES** - Performance/delivery direction
3. **DURATION** - Timing in seconds
4. **SPECIFIC SOURCES** - Not "Wikimedia Commons" but "Wikimedia Commons: 'Athenian kleroterion pinakion'"

---

## Activation

Use when user says:
- "Create editing guide for [video]"
- "Suggest edits for my A-roll"
- "Generate visual staging for [transcript]"
- `/edit-guide`

---

## MANDATORY OUTPUT FORMAT

### Required Sections (in this order)

1. **Header**
```markdown
# [Video Title] - EDITING GUIDE
## Video Length: ~[X:XX] | A-Roll Runtime from SRT: [START] - [END]

**Topic:** [One-line description]
```

2. **Editing Philosophy**
```markdown
## EDITING PHILOSOPHY

**The Golden Rule:** If the B-roll doesn't make your argument stronger, stay on camera.

**B-roll is EVIDENCE, not decoration.**

Use B-roll when:
- [Specific to this video - e.g., "Showing statistics/data"]
- [e.g., "Displaying maps for geographic claims"]
- [e.g., "Presenting primary sources"]

Stay on camera when:
- [e.g., "Making arguments and interpretations"]
- [e.g., "Explaining causation"]
- [e.g., "Rhetorical questions"]

**Target Ratio:** 65% talking head, 35% B-roll
```

3. **SRT Corrections Table**
```markdown
## SRT CORRECTIONS (Fix in DaVinci before export)

| SRT # | Timestamp | Wrong | Correct |
|-------|-----------|-------|---------|
| 17 | 00:41 | "Burink" | "Buringh" |
| 90 | 03:25 | "Visicotic" | "Visigothic" |
```

4. **Shot-by-Shot Breakdown** (MANDATORY FORMAT FOR EACH SHOT)

```markdown
### SECTION [#]: [SECTION NAME] ([START] - [END])

**Purpose:** [What this section accomplishes]

---

#### SHOT [#]: [TALKING HEAD/B-ROLL] - [Description] ([START] - [END])
**SRT #[X-Y]** | **Duration: [X] sec**

> "[Exact transcript text for this segment]"

**VISUAL:** [For B-roll - detailed description]
- [Specific elements to include]
- [Text overlays with EXACT wording]
- [Timing for each element if sequence]

**WHY [TALKING HEAD/B-ROLL]:** [Editorial reasoning - THIS IS MANDATORY]

**CAMERA NOTES:** [Performance direction - THIS IS MANDATORY for talking head shots]

**SOURCES:** [For B-roll only - SPECIFIC sources, not generic]
- Wikimedia Commons: "[Exact search term]"
- [Alternative source]: "[Specific item]"

**CREATE IN:** [DaVinci/Canva/PowerPoint] [For graphics only]
```

5. **Asset Checklist**
```markdown
## ASSET CHECKLIST

### Maps (Create in PowerPoint/Canva) - PRIORITY 1
- [ ] **[Map name]** - [Description, what to highlight]

### Historical Images (Wikimedia Commons) - PRIORITY 1
- [ ] **[Image name]** - [Specific search term or museum source]

### Text Overlays (Create in DaVinci) - PRIORITY 1
- [ ] **[Overlay name]** - [Exact text content]
```

6. **Retention Optimization**
```markdown
## RETENTION OPTIMIZATION

### Pattern Interrupts (Every 60-90 seconds)

| Timestamp | Interrupt Type | Content |
|-----------|---------------|---------|
| 00:00 | Hook | [Description] |
| 01:15 | Section shift | [Description] |
| 02:30 | Evidence | [Description] |

**Average interval:** ~[X] seconds between major visual shifts
```

7. **Quality Checklist**
```markdown
## QUALITY CHECKLIST

### Before Export:
- [ ] All SRT corrections applied
- [ ] All text overlays legible at 480p (mobile test)
- [ ] B-roll timed to exact narration sync
- [ ] [Video-specific critical moment] lands
- [ ] Color grade consistent
- [ ] End screen properly timed

### Channel DNA Check:
- [ ] Primary sources shown on screen
- [ ] Smoking gun evidence lands
- [ ] "Both extremes wrong" framework clear (if applicable)
- [ ] Academic authority established
- [ ] Documentary tone maintained
```

8. **Troubleshooting**
```markdown
## TROUBLESHOOTING

**"This segment feels too long on camera"**
→ Check if it's analytical/interpretive. If yes, stay on camera. Only cut to B-roll if there's EVIDENCE to show.

**"I have great B-roll but it's not in the guide"**
→ Ask: Does this EVIDENCE prove a claim? If no = decoration. Don't use.

**"The [key visual] doesn't land"**
→ Add more beats. Let numbers hang. Consider animation.
```

9. **Change Log**
```markdown
## CHANGE LOG

| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial guide created |
```

---

## Step-by-Step Process

### STEP 1: Gather Materials

Ask user for:
1. **SRT file location** - Need exact timestamps
2. **FINAL-SCRIPT location** - Need argument structure
3. **Video topic** - What's being argued?
4. **Available assets** - What exists already?

### STEP 2: Read SRT File

- Extract ALL timestamps
- Identify ALL transcription errors (names, technical terms, dates)
- Note natural section breaks

### STEP 3: Read FINAL-SCRIPT

- Understand argument structure
- Identify key claims and evidence
- Note intended B-roll callouts in script

### STEP 4: Generate Shot-by-Shot

For EVERY segment of audio:
1. Assign a shot number
2. Determine TALKING HEAD or B-ROLL
3. Write the WHY (editorial reasoning)
4. Write CAMERA NOTES (for talking head)
5. Specify VISUAL details (for B-roll)
6. List SPECIFIC SOURCES (for B-roll)
7. Note DURATION in seconds

### STEP 5: Quality Check

Before delivering, verify:
- [ ] Every shot has WHY field
- [ ] Every talking head shot has CAMERA NOTES
- [ ] Every B-roll shot has SPECIFIC SOURCES (not generic)
- [ ] Every shot has DURATION
- [ ] SRT corrections table is complete
- [ ] Retention timing table exists
- [ ] Troubleshooting section exists

---

## WHY Field Examples (Mandatory Quality)

**Good WHY fields:**
- "WHY TALKING HEAD: Rhetorical question - your face sells the intrigue."
- "WHY TALKING HEAD: KEY ARGUMENT - 'under new management' is a memorable reframe. Your delivery makes it land."
- "WHY B-ROLL: PRIMARY SOURCE EVIDENCE. This proves limited literacy was functional."
- "WHY B-ROLL: THIS IS YOUR SMOKING GUN. The whole video builds to this moment."
- "WHY TALKING HEAD: Analysis and interpretation - 'What does that tell us?' requires YOUR delivery."

**Bad WHY fields (DO NOT USE):**
- "WHY: Show the document" (too vague)
- "WHY: Visual interest" (decoration, not evidence)
- "WHY: Break up talking head" (wrong reasoning)

---

## CAMERA NOTES Examples (Mandatory for Talking Head)

**Good CAMERA NOTES:**
- "Direct to camera, confident. 'Here's what they found' = slight lean forward, building anticipation."
- "Slightly conspiratorial tone. 'Here's what everyone gets wrong...'"
- "'Both extremes oversimplify' = slight emphasis, this is your core claim."
- "'Romanized. Bilingual.' = punchy, declarative. 'Under new management' = slight smile."
- "Explaining the logic. Teacher mode. 'Tight, functional government' = key phrase."

**Bad CAMERA NOTES (DO NOT USE):**
- "Normal delivery" (too vague)
- "Look at camera" (obvious)
- [Missing entirely] (NEVER acceptable)

---

## SOURCE Examples (Mandatory Specificity)

**Good SOURCES:**
- "Wikimedia Commons: 'Athenian kleroterion pinakion'"
- "British Museum: Bronze pinakion collection"
- "Wikimedia Commons: 'Aachen Cathedral interior Palatine Chapel'"
- "Wikimedia Commons: 'Library of Celsus Ephesus'"

**Bad SOURCES (DO NOT USE):**
- "Wikimedia Commons" (too generic)
- "Find online" (useless)
- "Historical image" (not specific)

---

## Visual Sequence Format (For Complex B-Roll)

When B-roll has multiple frames/elements, use table format:

```markdown
**VISUAL:** 7-frame reveal sequence:

| Timestamp | Frame | Visual | Audio Sync |
|-----------|-------|--------|------------|
| 06:04 | 1 | Black screen | "And we can quantify this" |
| 06:09 | 2 | "6TH-7TH CENTURIES" | "supposed dark period" |
| 06:13 | 3 | "24,191 MANUSCRIPTS" | Number appears |
| 06:22 | 6 | "245,444 MANUSCRIPTS" | Number PUNCHES in (larger) |
| 06:26 | 7 | "915% INCREASE" | BIG - animate zoom/pulse |

**DESIGN NOTES:**
- Use contrasting colors
- 245,444 should be LARGER and BOLDER than 24,191
- 915% should be the BIGGEST element
```

---

## Common Mistakes to Avoid

1. **Table-only guides** - Just listing shots in a table without WHY/CAMERA NOTES
2. **Generic sources** - "Wikimedia Commons" instead of specific search terms
3. **Missing durations** - Every shot needs timing in seconds
4. **Missing SRT corrections** - Always scan for transcription errors
5. **No retention timing** - Must include pattern interrupt schedule
6. **No troubleshooting** - Must anticipate common editing problems

---

## Output Location

Save to: `video-projects/[lifecycle]/[project-folder]/EDITING-GUIDE.md`

Also generate: `video-projects/[lifecycle]/[project-folder]/B-ROLL-DOWNLOAD-LINKS.md`

---

**This skill ensures editing guides are production-ready with clear editorial reasoning, not just shot lists.**
