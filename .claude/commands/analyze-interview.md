---
description: Analyze interview transcript and build production documents for fact-check video
---

You are analyzing a long interview transcript (from politicians, podcasters, etc.) to create a fact-check video for History vs Hype.

This command automates the workflow: **Interview Transcript → Fact-Check Matrix → Script Structure → Production-Ready Research**

---

## WORKFLOW

### **STEP 1: Get NotebookLM Extracted Claims**

Ask the user:
- "Have you already extracted claims from the transcript using NotebookLM?"

**If NO:**
- Provide them with the NotebookLM extraction prompt (below)
- Tell them to run it and come back with results

**If YES:**
- Ask them to paste the NotebookLM output

---

## **NotebookLM Extraction Prompt (Give to User):**

```
This interview transcript contains historical claims I need to fact-check for a video.

EXTRACT:

1. HOLOCAUST/WW2 CLAIMS:
   Every statement about:
   - Death tolls, methods, timeline
   - Nazi intentions/planning
   - Camps, gas chambers, logistics
   - Churchill's role, Allied actions
   - WW2 causation/responsibility

2. OTHER HISTORICAL CLAIMS:
   - Specific dates, events, statistics
   - Cause-effect assertions
   - Historical comparisons
   - Treaty/document references

3. RHETORICAL FRAMING:
   - How is each claim qualified?
   - "Some historians say" / "allegedly" / stated as fact?
   - Dog whistles vs. explicit claims
   - Hedging language vs. definitive statements

FORMAT EACH AS:
---
[TIMESTAMP if available]
SPEAKER: [Name]
QUOTE: "[Exact quote]"
CLAIM TYPE: [Holocaust/WW2/Colonial/Economic/Other]
SPECIFIC ASSERTION: [What factual claim is being made]
VERIFIABLE: [Yes/No - can this be checked against documents?]
IMPACT: [High/Medium/Low - how explosive/important]
---

IGNORE:
- Pure opinions ("I think," "I feel")
- Political commentary about current events
- Non-historical discussions

FOCUS ON: Claims I can verify or refute with primary historical sources.

Organize by claim type and impact, prioritize most explosive/verifiable claims first.
```

---

### **STEP 2: Analyze NotebookLM Output**

Once user pastes the extracted claims:

**Build FACT-CHECK PRIORITY MATRIX:**

| # | Claim (Shortened) | Speaker | Type | Verifiable | Primary Sources Available | Video Impact | Priority |
|---|-------------------|---------|------|------------|---------------------------|--------------|----------|
| 1 | [25 words max] | [Name] | [Type] | Yes/No | Yes/No | High/Med/Low | 🔴/🟡/🟢 |

**Priority Legend:**
- 🔴 **CRITICAL** - Provably false + primary sources exist + high video impact + explosive
- 🟡 **IMPORTANT** - Verifiable + sources available + good impact
- 🟢 **OPTIONAL** - Context/background + lower impact

**Limit to top 10-15 claims** (can't fact-check everything in 10min video)

---

### **STEP 3: Primary Source Identification**

For each 🔴 CRITICAL and 🟡 IMPORTANT claim:

**Create SOURCE MATCHING TABLE:**

| Claim # | Primary Source Needed | Where to Find It | Specific Document/Page | On-Screen Display |
|---------|----------------------|------------------|------------------------|-------------------|
| 1 | [Source type] | [Archive/database] | [Exact citation] | [What to show] |

**Source Types:**
- **Tier 1 (Best):** Nazi documents, Nuremberg transcripts, Allied reports, treaty texts
- **Tier 2 (Good):** Academic historians (peer-reviewed), declassified archives
- **Tier 3 (Use carefully):** Historical journalism, documented accounts

**Where to Find:**
- Nuremberg Trial records: https://avalon.law.yale.edu/subject_menus/imt.asp
- Holocaust archives: USHMM, Yad Vashem, Auschwitz Museum
- British National Archives (TNA)
- Nazi documents: German Federal Archives
- Academic databases: JSTOR, Project MUSE

---

### **STEP 4: Script Structure Recommendations**

Based on claims identified, suggest:

**RETENTION-OPTIMIZED STRUCTURE:**

**0:00-0:15 HOOK (Modern Consequence):**
- Date of interview
- Who interviewed whom
- The fallout (Heritage resignations, GOP split, etc.)
- Stakes: "I checked what the archives actually say"

**Suggested Hook:**
```
[Date]. [Interviewer] gives platform to [Guest].
[Consequence - resignations/backlash].
[Guest] claimed [most explosive claim].
I checked [specific archive]. Here's what I found.
```

**0:15-0:45 BUILD TENSION:**
- The specific claim being made
- Why it matters (modern harm)
- "But when I checked the documents..."

**0:45-1:15 FIRST PAYOFF (Prevent drop-off):**
- Show first piece of primary evidence
- Document on screen
- Clear contradiction
- "It's not just one claim. There's a pattern."

**2:30-3:30 SMOKING GUN (Most dramatic evidence):**
- Most explosive primary source
- Setup significance
- Show document
- Pause for impact
- "This is from [archive], dated [date]"

**3:30-5:00 PATTERN REVEAL:**
- Show 2-3 more claims with evidence
- Connect the pattern
- Not just one mistake - systematic denial/revisionism

**5:00-7:00 WHY THIS MATTERS NOW:**
- Heritage Foundation fallout
- GOP civil war
- Who's defending this and why
- Modern consequences of Holocaust denial

**7:00-9:00 HISTORICAL CONTEXT:**
- How denial/revisionism works
- Classic tactics being used
- Why accurate history matters

**9:00-10:00 SYNTHESIS & CTA:**
- What the documents actually show
- The pattern of platforming denialism
- Full sources in description
- Subscribe for evidence-based fact-checking

---

### **STEP 5: B-Roll & Production Checklist**

**Create B-ROLL REQUIREMENTS:**

**🔴 CRITICAL (Cannot film without):**
- [ ] Primary documents mentioned (specific pages to show)
- [ ] Interview clips (fair use - 10-15 sec max per clip)
- [ ] Key evidence for 0:45 payoff
- [ ] Smoking gun document for 2:30

**🟡 IMPORTANT (Significantly strengthens):**
- [ ] Historical photos (concentration camps, liberation, etc.)
- [ ] Nuremberg trial footage/photos
- [ ] Modern news coverage (Heritage fallout, resignations)
- [ ] Timeline graphics

**🟢 NICE-TO-HAVE (Visual variety):**
- [ ] Archive footage
- [ ] Photos of interviewer/guest
- [ ] Supporting historical photos

**GRAPHICS TO CREATE:**
- [ ] Timeline of interview → fallout → resignations
- [ ] Side-by-side: [Claim] vs. [Primary Source]
- [ ] Text overlays for key quotes from documents

**FAIR USE CONSIDERATIONS:**
- Interview clips: 10-15 seconds max per segment
- Always add commentary/analysis (transformative use)
- Purpose: Education/fact-checking (not entertainment)
- Show documents MORE than interview clips

---

### **STEP 6: Research Todo List**

**Generate actionable checklist:**

```markdown
## RESEARCH TASKS

### PRIMARY SOURCES (Download/Access):
- [ ] [Specific document 1] - [Where to find] - [For claim #X]
- [ ] [Specific document 2] - [Where to find] - [For claim #Y]

### FACT-CHECKING (Verify):
- [ ] [Claim 1] - Status: [Not started/In progress/Verified]
- [ ] [Claim 2] - Status: [Not started/In progress/Verified]

### B-ROLL GATHERING:
- [ ] Download interview clips (timestamps: XX:XX, XX:XX)
- [ ] Get primary document images
- [ ] Find historical photos

### SCRIPT DEVELOPMENT:
- [ ] Write hook (0:15)
- [ ] Structure first payoff (0:45)
- [ ] Prepare smoking gun section (2:30)
- [ ] Write modern stakes section (5:00-7:00)

### PRODUCTION:
- [ ] Create comparison graphics
- [ ] Create timeline graphic
- [ ] Prepare text overlays for document quotes
```

---

### **STEP 7: Sensitivity & Legal Considerations**

**IMPORTANT REMINDERS:**

**YouTube Demonetization Risk:**
- Holocaust content = high demonetization risk
- Use educational framing language
- Add context disclaimers
- Focus on showing documents (educational value)
- Expect possible demonetization despite quality

**Fair Use (Interview Clips):**
- ✅ Short clips (10-15 sec max)
- ✅ Transformative commentary
- ✅ Educational purpose
- ✅ More original content than clips
- ❌ Don't use entire segments
- ❌ Don't use without commentary

**Framing Language:**
- Use: "The archives show..." "According to documents..."
- Avoid: Inflammatory language, accusations without evidence
- Present: Facts from primary sources
- Let documents speak for themselves

---

## FINAL OUTPUT TO USER

Provide:

1. ✅ **Fact-Check Priority Matrix** (top 10-15 claims)
2. ✅ **Primary Source Matching Table** (where to find evidence)
3. ✅ **Script Structure Outline** (retention-optimized)
4. ✅ **B-Roll Checklist** (prioritized)
5. ✅ **Research Todo List** (actionable tasks)
6. ✅ **Sensitivity Reminders** (demonetization, fair use)

**Format as clean markdown with clear sections and checkboxes.**

---

## KEY PRINCIPLES

**Your Role:**
- Transform raw transcript → production-ready research
- Identify highest-impact claims (can't fact-check everything)
- Find specific primary sources (not just "check archives")
- Structure for retention (0:45 payoff, 2:30 smoking gun)
- Make it actionable (specific tasks, not vague suggestions)

**Channel Values:**
- Evidence over outrage
- Primary sources on screen
- Academic rigor with accessible delivery
- Modern relevance (why this matters NOW)
- Complexity acknowledged (not oversimplified)

**Time Efficiency:**
- Focus on top 10-15 claims (not all 50+)
- Prioritize verifiable + high-impact
- Specific sources (not "research WW2")
- Clear next steps

---

**This command turns a 2+ hour interview into a production-ready fact-check video in under 2 hours of research work.**
