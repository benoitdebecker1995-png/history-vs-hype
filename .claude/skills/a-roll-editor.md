# A-Roll Editor Skill - History vs Hype

Generate shot-by-shot visual staging guides based on filmed A-roll transcripts. This skill takes your actual talking head footage and suggests exactly when to cut to B-roll, documents, maps, or graphics.

## Activation

Use when user says:
- "Create editing guide for [video]"
- "Suggest edits for my A-roll"
- "Generate visual staging for [transcript]"
- "Make an editing guide like the Vance video"

## STEP 1: Gather Materials

Ask user for:
1. **A-roll transcript file:** SRT subtitle file or plain text transcript with timestamps
2. **Script file (if available):** Original production script to understand intended visuals
3. **Video length:** Total runtime from the transcript
4. **Topic/thesis:** What's being argued in this video?
5. **Available assets:** What primary sources, maps, graphics exist already?

## STEP 2: Analyze Transcript Structure

Read through the full transcript and identify:

### Content Sections:
- Cold open/hook (first 15-30 seconds)
- Main claims (usually 2-4 major claims)
- Modern relevance/stakes (why it matters today)
- Conclusion/CTA

### Key Moments to Flag:
- **Primary source citations:** When you mention specific documents, studies, quotes
- **Geographic references:** Locations, distances, boundaries mentioned
- **Statistical claims:** Numbers, ratios, calculations mentioned
- **Pattern reveals:** When multiple examples build to a conclusion
- **Verdict moments:** Definitive statements debunking or confirming claims
- **Transitions:** Moving between claims or sections

### Speaking Patterns:
- Natural pauses (places for visual cuts)
- Emphasis moments (slower delivery, needs visual reinforcement)
- Rapid delivery (list-making, can handle quick cuts)

## STEP 3: Apply Visual Strategy Rules

### DEFAULT: YOU ON CAMERA (60-70% of video)

**Stay on talking head when:**
- Making arguments and interpretations
- Explaining causation ("X happened because Y")
- Connecting historical events
- Asking rhetorical questions
- Building narrative
- Providing analysis
- Transitions between sections
- Emotional emphasis moments
- Complex timelines that need host to guide

### CUT TO B-ROLL (30-40% of video)

**Cut away ONLY when B-roll strengthens the argument:**

**MAPS (15-20%):**
- Geographic boundaries mentioned
- Distances ("2,000 miles from...")
- Territorial expansion
- Location comparisons
- Maritime zones
- "Show WHERE" moments

**PRIMARY SOURCES (10-15%):**
- Treaty documents mentioned by name
- Archaeological studies cited
- DNA studies referenced
- Diplomatic correspondence
- Official proclamations
- Historical quotes from documents
- Academic papers cited

**HISTORICAL PHOTOS/PORTRAITS (5-10%):**
- Key figures mentioned by name
- Historical events described
- Archaeological sites referenced
- Period scenes if adding context

**MODERN FOOTAGE (5%):**
- Current events referenced
- News headlines mentioned
- Contemporary scenes
- Modern consequences shown

**GRAPHICS/TEXT (5%):**
- Mathematical calculations
- Statistical comparisons
- Timelines showing progression
- Quote cards (when no document image available)
- "ZERO" or emphasis moments

### NEVER USE:
- ❌ Generic B-roll (random jungle, stock handshakes, aesthetic shots)
- ❌ Decorative transitions
- ❌ B-roll that doesn't prove or illustrate the claim
- ❌ Cuts that interrupt natural speaking rhythm

## STEP 4: Generate Shot-by-Shot Breakdown

For each section of the transcript, create entries in this format:

```markdown
## SECTION [NUMBER]: [SECTION NAME] ([START TIME] - [END TIME])

**[TIMESTAMP] [Exact quote from transcript]**
- **SHOW:** [What visual to display]
- **WHY:** [Why this visual strengthens the argument]
- **DURATION:** [How long to hold this visual]
- **CRITICAL:** [If this visual is essential, note it]
- **OPTIONAL:** [If simpler alternative exists, provide it]

**Alternative (simpler):**
- **SHOW:** [Easier-to-create option]
- **WHY:** [Why this still works]
```

### Example Entry:

```markdown
**[01:01:30-01:01:39] "Spanish chronicler Diego Durán claimed over 80,000 victims in a single 1487 ceremony."**
- **SHOW:** Spanish chronicle page with "80,400" highlighted
- **WHY:** PRIMARY SOURCE - shows you found the actual document
- **DURATION:** 5-6 seconds
- **CRITICAL:** This establishes the inflated number before comparing to archaeological finds
- **OPTIONAL:** If can't source document, stay on comparison graphic from previous shot

**Alternative (simpler):**
- **SHOW:** Text overlay: "Spanish Chronicle: 80,400 victims claimed"
- **WHY:** Communicates the same information without needing to source historical document
```

## STEP 5: Visual Type Breakdown Summary

After shot-by-shot breakdown, provide summary:

```markdown
## VISUAL TYPE BREAKDOWN

### Talking Head (YOU on camera)
**Estimated Quantity:** [X:XX] total ([X]% of video)
**When used:**
- [List specific moments from this video]

### Primary Sources (Documents, Studies, Quotes)
**Essential (MUST HAVE):**
1. [Document/source name] - [What it proves]
2. [Document/source name] - [What it proves]
[List 8-15 essential sources]

**Nice to Have:**
- [Optional source]
- [Optional source]

### Maps & Graphics
**Essential (MUST HAVE):**
1. [Map/graphic description] - [What it shows]
2. [Map/graphic description] - [What it shows]
[List 5-10 essential graphics]

**Nice to Have:**
- [Optional graphic]

### Archival/News Footage
**Essential (MUST HAVE):**
- [Footage description]

**Nice to Have:**
- [Optional footage]
```

## STEP 6: Must-Nail Moments

Identify 6-8 critical delivery moments that need best performance:

```markdown
## MUST-NAIL MOMENTS

These require your best delivery, multiple takes if needed:

1. **[TIMESTAMP] "[Quote from video]"**
   - **Tone:** [How to deliver this line]
   - **Energy:** [High/Medium/Low]
   - **Why:** [Why this moment matters]
   - **Visual:** [Stay on camera or cut to evidence]

2. **[TIMESTAMP] "[Quote]"**
   [Same structure]
```

## STEP 7: Visual Rhythm Strategy

Provide pacing guidance:

```markdown
## VISUAL RHYTHM STRATEGY

### Typical 30-Second Pattern:
1. Host on camera ([X] sec) - [What you're doing]
2. Cut to [visual type] ([X] sec) - [What it shows]
3. Back to host ([X] sec) - [What you're doing]
4. Cut to [visual type] ([X] sec) - [What it shows]
5. Back to host ([X] sec) - [Transition]

### Pattern Interrupt Schedule:
- Every 20-30 seconds: [Type of change]
- Every 45-60 seconds: [Type of change]
- Every 90-120 seconds: [Type of change]

### Pacing Notes:

**FAST PACING ([TIME RANGE]):**
- [Section name]: [Why fast pacing]
- Quick cuts, [frequency]
- Goal: [What you're achieving]

**MEDIUM PACING ([TIME RANGE]):**
- [Section name]: [Why medium pacing]
- Mix of [visual breakdown]
- Goal: [What you're achieving]

**STRATEGIC HOLDS ([Type of Content]):**
- [Content type]: Hold [duration] as you [action]
- [Content type]: Hold [duration] for [reason]

**FASTER PACING ([Type of Montage]):**
- [Montage type]: Rapid succession, [duration] each
```

## STEP 8: Asset Priority List

Create sourcing checklist:

```markdown
## ASSET PRIORITY LIST

### ESSENTIAL (Video doesn't work without these)

**Documents/Primary Sources:**
1. ✅ [Document name/description]
2. ✅ [Document name/description]
[List 8-12 critical documents]

**Maps/Graphics:**
[X]. ✅ [Map/graphic description]
[Continue numbering]

**Quotes (can be text cards):**
[X]. ✅ [Quote from person/source]

### NICE TO HAVE (Improves quality but not critical)

[X]. ⭐ [Asset description]
[Continue list]

### NOT NEEDED (Skip these)

[X]. ❌ [Asset type to avoid]
[Continue list]
```

## STEP 9: Production Timeline

Provide realistic editing schedule:

```markdown
## PRODUCTION TIMELINE

### Phase 1: Review A-Roll Footage ([X]-[X] hours)
- Watch all takes
- Mark best takes for each line
- Note any unusable sections
- Create rough assembly of talking head only

### Phase 2: Edit Talking Head Base ([X]-[X] hours)
- Import best takes into timeline
- Cut together full narrative
- Remove pauses, "ums," false starts
- Ensure pacing feels natural
- **Checkpoint:** Watch full video, talking head only. Does narrative flow?

### Phase 3: Source Essential Assets ([X]-[X] hours)
**Where to find assets:**
- [Source type]: [Where to find]
- [Source type]: [Where to find]

**Asset creation:**
- [Asset type]: [How to create]
- [Asset type]: [How to create]

### Phase 4: Add Strategic B-Roll ([X]-[X] hours)
- Insert documents at exact timestamps
- Add maps where geographic evidence is discussed
- Create/add comparison graphics
- Insert quote cards
- **CRITICAL:** Every B-roll cut happens on the beat of your narration

### Phase 5: Polish & Export ([X]-[X] hours)
- Add subtle background music
- Color correct for consistency
- Add text overlays for key facts/dates
- Create end screen
- Audio mix
- Export: 1080p, H.264, 8-10 Mbps

### Phase 6: Thumbnail & Metadata ([X]-[X] hours)
- Create 3 thumbnail variations
- Write title
- Description with timestamps and source links
- Tags

---

**TOTAL TIME ESTIMATE: [X]-[X] hours**

**Realistic Schedule:**
- Day 1-2: [Tasks]
- Day 3-4: [Tasks]
- [Continue breakdown]
```

## STEP 10: Editing Checklist

```markdown
## EDITING CHECKLIST

Before considering this video done, verify:

### Content Quality
- [ ] Every claim has visual evidence supporting it
- [ ] All primary sources are on screen 5-8 seconds (readable but not too long)
- [ ] No B-roll is decorative - every cut serves the argument
- [ ] Source citations appear when showing documents

### Visual Rhythm
- [ ] Visual change happens every 5-8 seconds minimum
- [ ] Pattern interrupt (major visual shift) every 20-30 seconds
- [ ] Cold open is under 15-20 seconds before you appear on camera
- [ ] YOU on camera 60-70% of total runtime

### Technical Quality
- [ ] Text overlays are clear and don't obstruct face
- [ ] Audio is balanced (no sudden loud/quiet sections)
- [ ] Color is consistent throughout
- [ ] End screen appears with subscribe button

### Publishing
- [ ] Thumbnail is created and compelling
- [ ] Description includes timestamps and source links
- [ ] Tags are relevant
```

## STEP 11: Editing Tips Section

```markdown
## EDITING TIPS FOR THIS VIDEO

### Keep It Simple
- You're building trust through evidence, not flashy effects
- Clean cuts > fancy transitions
- Documents speak for themselves - don't over-animate

### Respect the Evidence
- When showing a document, give viewers time to see it (5-6 seconds)
- Zoom to relevant sections when possible
- Don't cut away too fast - frustrates viewers

### Maintain Authority
- Default to YOU on camera for analysis and interpretation
- Only cut away to show proof
- Come back to you after showing evidence to explain what it means

### Watch for These Common Mistakes
- **Too much B-roll:** If you're on camera less than 50%, you've over-cut
- **Text overlays covering your face:** Keep text in bottom third or sides
- **Inconsistent volumes:** Documents with music should be -20dB below voice
- **Rushed evidence:** Don't flash documents too fast to read

### Test Your Work
- Watch the full video without editing timeline visible
- Ask: "Can I follow the argument?"
- Ask: "Does each visual ADD information or just decorate?"
- If a cut feels unnecessary, remove it
```

## Quality Control Standards

Before delivering editing guide, verify:

### Structure
- [ ] Shot-by-shot breakdown covers entire transcript
- [ ] Every timestamp from transcript is accounted for
- [ ] Visual suggestions align with "you on camera 60-70%" rule
- [ ] All primary source citations get visual staging suggestions

### Practicality
- [ ] Simpler alternatives provided for complex visuals
- [ ] Asset priority clearly distinguishes MUST HAVE vs NICE TO HAVE
- [ ] Timeline estimates are realistic for beginner editors
- [ ] Editing tips address common mistakes

### Channel Alignment
- [ ] Visual strategy matches "evidence over decoration" philosophy
- [ ] Default to host authority (talking head) maintained
- [ ] B-roll only used when it strengthens argument
- [ ] Primary sources prioritized over generic footage

## Output Format

Save editing guide to: `video-projects/[topic-slug]/[topic]-EDITING-GUIDE.md`

## Output Style

Match the tone and format of the example VANCE_VIDEO_EDITING_GUIDE.md:
- Conversational but instructional
- Specific timestamps with exact quotes
- Clear **SHOW/WHY/DURATION** structure
- Checkboxes for asset lists
- Emoji section headers (🎯 📋 📊 etc.)
- Practical alternatives marked as "OPTIONAL" or "Alternative (simpler)"
- Emphasis markers: **CRITICAL** for must-haves

## Common Scenarios

### Scenario 1: Primary Source Citation
When transcript says: "According to the 2024 Nature study..."

**Suggested visual:**
- **SHOW:** Nature study cover, zoom to title
- **WHY:** PRIMARY SOURCE - proves you have the actual research
- **DURATION:** 5-6 seconds
- **CRITICAL:** This establishes credibility

### Scenario 2: Geographic Claim
When transcript says: "2,000 miles from where settlers landed..."

**Suggested visual:**
- **SHOW:** Map with two points connected, distance marked
- **WHY:** Geographic evidence makes abstract distance concrete
- **DURATION:** 5-6 seconds
- **OPTIONAL:** Simple arrow with "2,000 miles" text

### Scenario 3: Statistical Comparison
When transcript says: "They claimed 80,000, but archaeologists found 126..."

**Suggested visual:**
- **SHOW:** Side-by-side comparison graphic
- **WHY:** Visual comparison makes inflation obvious
- **DURATION:** 6-8 seconds
- **CRITICAL:** This IS the thesis - essential visual

### Scenario 4: Mathematical Calculation
When transcript says: "That's 20 times inflation"

**Suggested visual:**
- **SHOW:** Math on screen: "80,400 ÷ 4,000 = 20x"
- **WHY:** Makes the calculation transparent
- **DURATION:** 4-5 seconds
- **OPTIONAL:** Simple text overlay

### Scenario 5: Analysis/Interpretation
When transcript says: "What this means is..." or "The significance is..."

**Suggested visual:**
- **SHOW:** YOU on camera
- **WHY:** Host authority - you're interpreting evidence
- **DURATION:** Continue on camera until next evidence point

### Scenario 6: Transition Question
When transcript says: "So what about..." or "Which brings us to..."

**Suggested visual:**
- **SHOW:** YOU on camera
- **WHY:** Host guiding viewer through narrative
- **DURATION:** Stay on camera through transition

### Scenario 7: Verdict Moment
When transcript says: "So no, [claim] doesn't hold up" or "Three claims checked, none held up"

**Suggested visual:**
- **SHOW:** YOU on camera
- **WHY:** Authority delivering final judgment - needs your conviction
- **DURATION:** Stay on camera for emphasis

## After Generation

Ask user:
1. Does this editing guide match your footage?
2. Any visual suggestions that seem too complex?
3. Should I prioritize simpler alternatives throughout?
4. Want me to expand any section (specific timestamps, asset sourcing, etc.)?
5. Need help sourcing specific documents or creating graphics?

## Integration with Other Skills

**Before creating editing guide:**
- Script should be filmed (obviously)
- FINAL_PRODUCTION_SCRIPT already has visual staging notes

**After editing guide is created:**
- User can reference this during editing in DaVinci Resolve
- Asset priority list guides what to source/create first
- Timestamp-specific breakdown allows precise editing

---

**This skill ensures every cut serves the argument and maintains host authority while leveraging evidence-based B-roll strategically.**
