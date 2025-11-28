# History vs Hype: Master Video Project Template

**A reusable framework for evidence-based myth-busting documentaries**

---

## 🎯 PROJECT OVERVIEW

**Video Title:** [Insert working title]  
**Target Length:** [8-12 min / 15-20 min / 30+ min]  
**Core Thesis:** [One sentence: What myth are you debunking?]  
**Why This Matters:** [Why is this historical distortion dangerous today?]  
**Upload Date Target:** [YYYY-MM-DD]

---

## 📚 PHASE 1: NOTEBOOKLM RESEARCH SETUP

### Initial Research Organization

**Step 1: Create Project Notebook**
- Notebook Name: `[Topic]_[Date]_Research`
- Upload cap: 50 sources, 25M words total
- Organization categories:
  - Primary Sources (treaties, documents, speeches)
  - Academic Papers (peer-reviewed research)
  - News/Analysis (contemporary reporting)
  - Counter-Evidence (opposing viewpoints)

**Step 2: Source Upload Checklist**
- [ ] Primary historical documents (timeless)
- [ ] Modern consensus scholarship (2010-present peer-reviewed)
- [ ] Classic works (pre-2010) - note for verification against recent scholarship
- [ ] Statistical data sources
- [ ] Counter-narrative sources (strongest academic rebuttals, not strawmen)
- [ ] Related documentaries (transcript links)

### NotebookLM Research Prompts

**🔍 RESEARCH ORGANIZATION PROMPT:**
```
Analyze all inputs and generate 5 essential questions that capture the core meaning of this topic. For each question:
1. Provide specific source and page references for answers
2. Note publication dates (prioritize 2010-present for modern consensus)
3. Identify any contradictions or gaps in the evidence
4. Extract strongest academic counter-arguments (steel-manned versions)
5. Flag pre-2010 sources that may need verification against recent scholarship
6. Note which claims have strongest/weakest source support
```

**🎬 VIDEO HOOK GENERATION PROMPT:**
```
Based on all sources, identify 3 most compelling opening hooks for [specific topic]. For each hook provide:
1. Exact quote or statistic that grabs attention
2. Source citation with page number
3. Why this hooks the audience (emotional/intellectual appeal)
4. How it connects to the main narrative
```

**📊 EVIDENCE EXTRACTION PROMPT:**
```
Create a tiered evidence list for debunking [specific myth]:

TIER 1 - SMOKING GUN EVIDENCE (impossible to dispute):
- Direct quotes with attribution
- Statistical patterns that prove systematic issues
- Documents that reveal intentions

TIER 2 - STRONG SUPPORTING EVIDENCE:
- Academic consensus findings
- Economic/demographic data
- Multiple source corroboration

TIER 3 - CONTEXTUAL EVIDENCE:
- Historical background
- Expert analysis
- Comparative examples

For each item, provide: exact quote/data, source, and persuasive power ranking (1-10)
```

**✅ FACT-CHECKING PROMPT (Optimized for NotebookLM length limits):**
```
Verify this script against all sources. Check:

STATISTICS (exact numbers & sources with page numbers):
[List all numerical claims from script]

DIRECT QUOTES (confirm exact wording with page numbers):
[List all quotes used in script]

KEY CLAIMS (identify sources with publication dates):
[List major interpretive claims]

SOURCE CURRENCY:
- Are claims based on 2010-present scholarship?
- Are pre-2010 sources contextualized as "foundational" with recent updates noted?

COUNTER-ARGUMENTS:
- Are strongest academic rebuttals addressed?
- Are contested claims labeled as debated?

FLAG:
- ❌ Incorrect facts
- ⚠️ Missing context needed
- 🔍 Unsourced claims
- ⚡ Contradictions with sources
- 📅 Outdated scholarship (pre-2010) presented as current consensus

Priority: [List 3 most critical evidence points]
```

**🎥 B-ROLL SHOT LIST PROMPT:**
```
Create comprehensive B-roll shot list including:
1. Key visual moments that illustrate evidence
2. Suggested archival footage/images with search terms
3. Charts/graphics that need to be created
4. Map overlays showing geographic/territorial changes
5. Document close-ups for primary source reveals
6. Section transition visuals

Organize by video segment and note which visuals are CRITICAL vs. NICE-TO-HAVE.
```

**🔄 COUNTER-EVIDENCE PROMPT:**
```
What are the 3 strongest counter-arguments to my thesis? For each:
1. Most compelling evidence supporting the counter-view
2. Source attribution for counter-argument
3. Valid points I should acknowledge
4. Where counter-evidence is weak/incomplete
5. How to address fairly without undermining my thesis
```

---

## 🎨 PHASE 2: THUMBNAIL DESIGN (PHOTOSHOP)

### Thumbnail Strategy Framework

**Core Design Principles:**
- Resolution: 1280x720px (16:9 ratio)
- Safe zone: Keep key elements within 1184x666px (avoid mobile crop)
- Text: Maximum 3-4 words, readable at small size
- Color: High contrast, bold palette
- Faces: Show emotion/reaction when possible
- Clarity: Instantly communicates video premise

### Thumbnail Template (Photoshop)

**LAYER STRUCTURE:**
```
📁 TEXT LAYERS
  └─ Primary Headline (120-140pt, bold sans-serif)
  └─ Secondary Text (80-90pt, accent color)
  └─ Small Stat/Label (30-40pt, supporting info)

📁 VISUAL ELEMENTS
  └─ Background Image/Map
  └─ Subject Photo (if using)
  └─ Overlay Graphics (icons, flags, symbols)
  └─ Dividing Elements (split-screen lines, tears)

📁 EFFECTS
  └─ Drop Shadows (black, 3-4px offset)
  └─ Stroke/Outline (3-4px black on white text)
  └─ Color Grading Adjustment Layer
  └─ Vignette (subtle focus)

📁 BRANDING
  └─ Channel Logo (small, bottom corner)
  └─ "MYTH-BUSTING" or "EXPOSED" badge (optional)
```

**RECOMMENDED DESIGN CONCEPTS:**

**Concept 1: "The Split Revelation"**
- Left side (40%): "The Myth" - faded historical imagery
- Right side (60%): "The Reality" - bold modern evidence
- Jagged dividing line creating visual tension
- Primary text spans both sides for unity

**Concept 2: "The Document Reveal"**
- Close-up of historical document as background
- Key damning quote highlighted in yellow
- Your face reacting with serious expression
- "DECLASSIFIED" or "EXPOSED" stamp graphic

**Concept 3: "The Geographic Pattern"**
- Map showing region/territory in question
- Visual markers (lightning bolts, crosses, icons) showing pattern
- Statistics overlay: "X of Y" showing concentration
- Bold title questioning the narrative

**COLOR PALETTES:**

*Academic Authority:*
- Navy blue (#1A3A52)
- White (#FFFFFF)
- Gold accent (#FFD60A)

*Urgent Revelation:*
- Deep red (#8B1E3F)
- Black (#000000)
- Bright yellow (#FFD60A)

*Geopolitical Tension:*
- Military green (#3D5A3D)
- Steel blue (#4A6E7C)
- Warning orange (#E07A5F)

### Thumbnail Checklist

- [ ] Passes "squint test" (readable when very small)
- [ ] Text has sufficient contrast against background
- [ ] No copyright issues with images used
- [ ] Aligns with video content (not clickbait)
- [ ] Clearly signals "educational/documentary" content
- [ ] Exported at high quality (no compression artifacts)
- [ ] Tested on mobile display size

---

## 📝 PHASE 3: SCRIPT DEVELOPMENT

### Script Structure Template

**OPENING HOOK (0:00-1:30) - 200 words**
- Lead with shocking statistic or pattern
- Frame as investigation, not opinion
- Promise: "We're examining X myths that obscure Y reality"
- Establish academic credibility immediately

*Checklist:*
- [ ] Opens with pattern/statistic that challenges conventional wisdom
- [ ] Establishes stakes (why this matters today)
- [ ] Promises specific myths to debunk (3-4 maximum)
- [ ] Uses academic framing language

**MYTH #1 DEMOLITION (1:30-4:00) - 400 words**
- State the myth clearly
- Present the "smoking gun" evidence
- Show the pattern/mechanism of deception
- Connect to present-day consequences

*Structure:*
1. Setup: "The conventional narrative says..."
2. Counter-evidence: "But declassified documents reveal..."
3. Mechanism: "Here's how this works..."
4. Impact: "The consequences are still felt today..."

**TRANSITION 1 (4:00-4:30) - 80 words**
- Connect first myth to second myth
- Build momentum: "If that's true, then what about..."
- Visual bridge technique

**MYTH #2 DEMOLITION (4:30-7:00) - 400 words**
[Same structure as Myth #1]

**TRANSITION 2 (7:00-7:30) - 80 words**
[Connect second to third myth]

**MYTH #3 DEMOLITION (7:30-10:00) - 400 words**
[Same structure as Myth #1]

**CONCLUSION (10:00-12:00) - 300 words**
- Synthesis: "These three myths interconnect..."
- The real issue: Systematic pattern, not isolated incidents
- Why distortion is dangerous
- What accurate history reveals
- Call-to-action (check sources, seek multiple perspectives)

*Avoid:*
- [ ] Telling viewers what to think/believe
- [ ] Oversimplifying complex historical events
- [ ] Presenting contested claims as settled fact
- [ ] Ignoring legitimate counter-evidence

### Academic Balance Framework

**✅ VALID CRITICISMS (Use with confidence):**
- Documented structural problems with evidence
- Statistical patterns showing systematic issues
- Direct documentary evidence of deception
- Academic consensus on specific claims

**❌ OVERSIMPLIFICATIONS (Avoid or qualify):**
- Presenting complex historical actors as purely evil/good
- Ignoring agency of affected populations
- Reducing decades of policy to single motivation
- Claiming historical figures had perfect knowledge of consequences

**⚖️ GRAY AREAS (Handle with nuance):**
- Economic systems with both benefits and costs
- Military interventions with mixed motives
- Colonial administrators with varying approaches
- Post-independence leaders making constrained choices

**LANGUAGE GUIDANCE:**

Replace politically charged language with academic phrasing:

| ❌ Avoid | ✅ Use Instead |
|---------|----------------|
| "X is occupying Y" | "X's military presence has fueled nationalist opposition" |
| "Z destroyed the culture" | "Z's policies fragmented traditional systems while..." |
| "Leaders are heroes/villains" | "Leaders exploited/addressed these structural issues..." |
| "The West is recolonizing" | "These policies risk prioritizing external over local interests" |

### Script Checklist

- [ ] Every major claim has source attribution
- [ ] Statistics are specific and sourced
- [ ] Counter-evidence is acknowledged
- [ ] Complexity is maintained (not oversimplified)
- [ ] Academic framing language used throughout
- [ ] Pacing: 100-110 words per minute
- [ ] Engagement trigger every 2 minutes (revelation/question/visual)
- [ ] Narrator voice is public historian, not pundit
- [ ] Conclusion emphasizes why accurate history matters

---

## 🎬 PHASE 4: PRODUCTION PLANNING

### Pre-Production Checklist

**Visual Assets Needed:**
- [ ] Maps showing geographic scope (list specific maps)
- [ ] Infographics for statistical data (list specific graphics)
- [ ] Timeline visualizations (identify date ranges)
- [ ] Document close-ups (list specific documents)
- [ ] Archival footage (list search terms/sources)
- [ ] Stock footage (list B-roll needs)
- [ ] Charts/graphs (list data visualizations needed)

**Technical Setup:**
- [ ] Camera/recording setup tested
- [ ] Lighting adequate for talking head footage
- [ ] Audio quality check (no echo, clear voice)
- [ ] Teleprompter or notes organized
- [ ] Background appropriate (neutral/professional)
- [ ] Backup recording device ready

**Editing Resources:**
- [ ] All visual assets collected and organized
- [ ] Music tracks selected (royalty-free)
- [ ] Sound effects identified (if needed)
- [ ] Color grading preset prepared
- [ ] Export settings confirmed (YouTube specs)

### File Organization Structure

```
📁 [PROJECT_NAME]_[DATE]
  ├─ 📁 01_RESEARCH
  │   ├─ NotebookLM_Exports
  │   ├─ Primary_Sources
  │   ├─ Academic_Papers
  │   └─ Fact_Check_Log.md
  │
  ├─ 📁 02_SCRIPT
  │   ├─ Draft_v01.md
  │   ├─ Draft_v02.md
  │   ├─ FINAL_Script.md
  │   └─ Filming_Notes.md
  │
  ├─ 📁 03_VISUAL_ASSETS
  │   ├─ Maps
  │   ├─ Infographics
  │   ├─ Documents
  │   ├─ Archival_Footage
  │   └─ Stock_Footage
  │
  ├─ 📁 04_PRODUCTION
  │   ├─ RAW_Footage
  │   ├─ Audio_Files
  │   ├─ Project_Files
  │   └─ Exports
  │
  └─ 📁 05_PUBLISHING
      ├─ Thumbnail_Final.psd
      ├─ Thumbnail_Export.jpg
      ├─ YouTube_Description.md
      └─ Source_List.md
```

**File Naming Convention:**
- Research: `YYYYMMDD_SourceType_Keyword_V##`
- Scripts: `ProjectName_ScriptType_YYYYMMDD_V##`
- Assets: `ProjectName_AssetType_Description_##`

---

## ✅ PHASE 5: FACT-CHECKING & REVIEW

### Three-Tier Fact-Check Process

**TIER 1: NOTEBOOKLM VERIFICATION (Day before filming)**
- [ ] Run fact-checking prompt on complete script
- [ ] Verify all statistics against original sources
- [ ] Confirm exact wording of all quotes
- [ ] Check that interpretations are supported by sources
- [ ] Flag any unsourced claims

**TIER 2: SELF-REVIEW (After filming, before editing)**
- [ ] Re-read script aloud checking for overstatements
- [ ] Verify you maintained academic balance
- [ ] Confirm you acknowledged counter-evidence
- [ ] Check that you didn't oversimplify complex issues
- [ ] Review that conclusions match evidence strength

**TIER 3: EXTERNAL REVIEW (Optional but recommended)**
- [ ] Share script with subject matter expert if possible
- [ ] Post in relevant academic forums for feedback
- [ ] Have someone unfamiliar with topic read for clarity
- [ ] Check that myths are fairly stated before debunking

### Fact-Check Documentation

**For each major claim, record:**
1. **Claim:** [What you state in video]
2. **Source:** [Specific document/study]
3. **Page/Timestamp:** [Exact location]
4. **Confidence Level:** [High/Medium/Low]
5. **Counter-Evidence:** [Any opposing data]
6. **Notes:** [Context/caveats]

**Example:**
```
Claim: "16 of 23 African coups since 2000 occurred in former French colonies"
Source: Usman, A. A. (2024). "France has become the common denominator"
Page: Abstract, para 2
Confidence: HIGH - multiple sources corroborate
Counter-Evidence: None found in literature
Notes: Defines "French colonies" as territories under direct French colonial rule
```

### Correction Protocol

**If errors discovered after publishing:**
1. Pin correction comment immediately
2. Add correction to video description
3. Consider adding annotation/card if serious error
4. Update source document for your records
5. Learn: What process failed? How to prevent next time?

---

## 📺 PHASE 6: YOUTUBE OPTIMIZATION

### Title Formula Options

**Pattern 1: The Myth Reveal**
`"[Myth] vs. Reality: What [Evidence] Reveals About [Topic]"`
Example: "Colonial Lies vs. Reality: What Declassified Documents Reveal About Sahel Coups"

**Pattern 2: The Hidden Pattern**
`"The [Pattern] Behind [Event]: [Key Insight]"`
Example: "The Coup Belt Pattern: Why 12 of 13 Takeovers Happened in French Colonies"

**Pattern 3: The Question Hook**
`"Why Does [Surprising Pattern] Keep Happening? [Short Answer]"`
Example: "Why Do 70% of African Coups Happen in 25% of Countries? Colonial Legacy"

**Optimization Checklist:**
- [ ] Under 70 characters (full display on all devices)
- [ ] Front-loads key terms (first 40 characters critical)
- [ ] Includes searchable terms (geographic names, events)
- [ ] Signals educational content (not clickbait)
- [ ] Creates curiosity without misleading

### Description Template

```
[2-3 SENTENCE HOOK - What shocking pattern/evidence does this video reveal?]

In this evidence-based analysis, I examine three persistent myths about [topic]:
• Myth 1: [State myth briefly]
• Myth 2: [State myth briefly]  
• Myth 3: [State myth briefly]

Using declassified documents, academic research, and statistical analysis, I reveal [key finding that connects all three myths].

⏱️ TIMESTAMPS
0:00 - Introduction: [Brief description]
1:30 - Myth #1: [Title]
4:30 - Myth #2: [Title]
7:30 - Myth #3: [Title]
10:00 - Conclusion: [Key takeaway]

📚 KEY SOURCES (Select 5-8 most important)

PRIMARY SOURCES:
• [Document name] - [Archive/location] ([Year])
• [Treaty/agreement name] - [Citation] ([Year])

ACADEMIC RESEARCH:
• [Author last name], [First initial]. ([Year]). [Title]. [Journal/Publisher].
• [Author last name], [First initial]. ([Year]). [Title]. [Journal/Publisher].

STATISTICAL DATA:
• [Organization name]. ([Year]). [Dataset name]. [URL if available]

INVESTIGATIVE JOURNALISM:
• [Author name]. ([Year]). "[Title]." [Publication]. [URL]

📖 FULL SOURCE LIST: [Link to complete bibliography on your website/Google Doc]

🔍 METHODOLOGY
This video follows academic standards for historical analysis:
- Multiple source verification for all major claims
- Primary sources prioritized over secondary accounts
- Counter-evidence acknowledged and addressed
- Complex issues presented with appropriate nuance

⚠️ CORRECTIONS & UPDATES
[Leave this section empty unless corrections needed]
Any factual errors discovered after publication will be noted here with timestamps and corrections.

---

📧 CONTACT & TRANSPARENCY
Research questions or source requests: [your email]
This video was [independently researched / crowd-funded / etc.]
No conflicts of interest to disclose.

---

🔖 FEATURED TOPICS:
[List 10-15 relevant keywords/topics separated by pipes]
Example: French colonialism | CFA franc | Sahel crisis | Mali coup | Academic history | Myth-busting | Geopolitics

---

#[Topic] #[Geography] #[KeyEvent] #History #Documentary #Research

[Add 2-3 more relevant hashtags, keep total under 15]
```

### Tags Strategy (YouTube Studio)

**Primary Tags (Most important - use exact phrases):**
- Your main topic keywords (3-5 tags)
- Geographic locations featured (2-3 tags)
- Your channel brand tag: "History vs Hype"

**Secondary Tags (Broad reach):**
- Related historical periods
- Academic fields (political science, history, international relations)
- Format tags (documentary, educational, explainer)

**Long-Tail Tags (Niche audience):**
- Specific events/documents mentioned
- Academic concepts explored
- Comparison terms

**Example Tag Set:**
```
French colonialism, Sahel crisis, Mali coup, CFA franc, Operation Persil, 
African coups, neocolonialism, History vs Hype, geopolitics explained, 
documentary history, academic analysis, myth-busting history, 
declassified documents, political science, West Africa
```

---

## 🎯 PHASE 7: POST-PRODUCTION REVIEW

### Pre-Upload Final Checklist

**Content Review:**
- [ ] All facts verified against sources
- [ ] Quotes are accurate and attributed
- [ ] No overstatements or unsupported claims
- [ ] Academic balance maintained throughout
- [ ] Counter-evidence acknowledged appropriately
- [ ] Conclusion matches evidence strength

**Technical Review:**
- [ ] Video quality check (no compression artifacts)
- [ ] Audio levels consistent throughout
- [ ] Color grading applied uniformly
- [ ] Transitions are smooth
- [ ] Text overlays are readable
- [ ] End screen elements added

**Metadata Review:**
- [ ] Title optimized and accurate
- [ ] Description complete with sources
- [ ] Tags include all relevant terms
- [ ] Thumbnail uploaded (1280x720px)
- [ ] Timestamps added to description
- [ ] Custom URL slug if available

**YouTube Settings:**
- [ ] Upload as unlisted first (for review)
- [ ] Age restriction: Usually "No" for educational content
- [ ] Category: Education
- [ ] Language: [Select appropriate]
- [ ] Captions: Auto-generate, then review/edit
- [ ] End screens configured
- [ ] Cards added at key moments
- [ ] Publishing schedule set

### 24-Hour Post-Upload Monitoring

**Engagement Check:**
- Monitor first comments for factual challenges
- Respond to substantive questions/corrections
- Pin top comment with additional context if needed
- Note any confusion patterns (improve next video)

**Performance Metrics:**
- Average view duration (target: 50%+ for educational)
- Click-through rate (target: 4-8% for educational thumbnails)
- Engagement rate (likes/comments relative to views)
- Traffic sources (search vs. suggested vs. external)

---

## 📊 PROJECT POST-MORTEM TEMPLATE

*Complete within 48 hours of publishing*

### What Worked Well
1. **Research:** [What sources were most valuable?]
2. **Script:** [Which segments engaged viewers most?]
3. **Visuals:** [What graphics/B-roll was most effective?]
4. **Production:** [What workflow improvements helped?]

### What Needs Improvement
1. **Research:** [What sources were you missing?]
2. **Script:** [Where did pacing drag or rush?]
3. **Visuals:** [What visuals were weak/missing?]
4. **Production:** [What bottlenecks slowed you down?]

### Audience Feedback Themes
- [Summarize common comments/questions]
- [Note any factual corrections requested]
- [Identify topics viewers want explored further]

### Next Video Improvements
1. [Specific change #1]
2. [Specific change #2]
3. [Specific change #3]

### Time Breakdown
- Research: [X hours]
- Script writing: [X hours]
- Asset creation: [X hours]
- Filming: [X hours]
- Editing: [X hours]
- Publishing: [X hours]
**Total:** [X hours]

*Goal: Reduce time while maintaining quality*

---

## 🎓 HISTORY VS HYPE: CORE PRINCIPLES

*Review before starting every project*

**Your Mission:**
You're a public historian showing why historical accuracy matters. Oversimplification and romanticization can be dangerous—your role is revealing how distorted history fuels present-day conflicts and misconceptions.

**Your Audience Expects:**
- Rigorous fact-checking with transparent methodology
- Primary sources and academic citations
- Nuanced analysis (not binary good/evil narratives)
- Acknowledgment of complexity and counter-evidence
- Myth-busting backed by evidence, not opinion

**Your Differentiators:**
- Evidence-based demolition of propaganda
- Handling sensitive topics with academic rigor
- Showing patterns in historical distortion
- Dual format: quick myth-busts + deep analysis
- Specialization in contentious geopolitical topics

**What You're NOT:**
- General history entertainment
- Opinion/commentary channel
- Simplification for clicks
- Taking political sides
- Avoiding controversy

**The Golden Rule:**
Validate real structural problems while correcting historical oversimplifications. Your viewers should leave understanding that issues are more complex than headlines suggest, but certain patterns of exploitation are systematically documented.

---

## 📋 QUICK-START CHECKLIST

*Use this for rapid project setup*

### Day 1: Research Setup
- [ ] Create NotebookLM notebook
- [ ] Upload 10-20 key sources
- [ ] Run research organization prompt
- [ ] Identify 3 core myths to debunk

### Day 2-3: Evidence Gathering
- [ ] Run evidence extraction prompts
- [ ] Document tier 1 smoking gun evidence
- [ ] Identify counter-evidence to address
- [ ] Create source citation list

### Day 4: Script Draft
- [ ] Write hook using best statistic/revelation
- [ ] Draft myth #1 demolition (400 words)
- [ ] Draft myth #2 demolition (400 words)
- [ ] Draft myth #3 demolition (400 words)
- [ ] Write transitions and conclusion

### Day 5: Fact-Check
- [ ] Run NotebookLM fact-check prompt
- [ ] Verify all statistics and quotes
- [ ] Check academic balance
- [ ] Review for overstatements

### Day 6: Visual Prep
- [ ] List all B-roll/graphics needed
- [ ] Create Photoshop thumbnail
- [ ] Source archival footage/images
- [ ] Create infographics/maps

### Day 7: Production
- [ ] Film talking head footage
- [ ] Edit with visuals and B-roll
- [ ] Add captions/text overlays
- [ ] Export final video

### Day 8: Publishing
- [ ] Write YouTube description with sources
- [ ] Create tags and set metadata
- [ ] Schedule or publish
- [ ] Monitor first 24 hours

---

## 📚 RESOURCE LINKS

**NotebookLM:**
- Platform: https://notebooklm.google/
- Max sources: 50 per notebook
- Max words: 25 million per notebook
- Best for: Source-grounded research, no hallucinations

**Citation Management:**
- Zotero (free): https://www.zotero.org/
- Reference format: Chicago Manual of Style (academic standard)

**Stock Footage:**
- Internet Archive: https://archive.org/
- CriticalPast: https://www.criticalpast.com/
- Public domain verification: Check specific collection terms

**Map Creation:**
- Google My Maps: https://www.google.com/maps/about/mymaps/
- Datawrapper: https://www.datawrapper.de/
- Keep it simple: Clear boundaries, limited colors, readable labels

**Infographic Tools:**
- Canva: https://www.canva.com/ (280+ templates)
- Piktochart: https://piktochart.com/ (data viz focus)
- For Photoshop users: Design layouts in PS for maximum control

**Timeline Visualization:**
- TimelineJS: https://timeline.knightlab.com/ (free, Google Sheets integration)
- Excel/Google Sheets: Create simple timeline graphics
- Photoshop: Manual design for maximum customization

**Thumbnail Testing:**
- View on phone before publishing
- Ask: "Would I click this if I didn't make it?"
- A/B test: Create 2-3 options, get feedback

---

## 💡 ADVANCED TIPS

**For Complex Topics:**
- Create glossary of terms in description
- Add cards linking to background videos
- Consider releasing shorter "primer" video first

**For Controversial Topics:**
- Document your methodology extra thoroughly
- Get academic peer review if possible
- Prepare for criticism by anticipating objections
- Pin top comment with additional nuance/context

**For Viral Potential:**
- Focus on pattern recognition (viewers love "aha" moments)
- Lead with shocking but verifiable statistics
- Create quotable phrases for social sharing
- Time release to current events when relevant

**For Long-Term Value:**
- Evergreen topics > trending news
- Deep analysis > surface coverage
- Build series that reference each other
- Update descriptions if new evidence emerges

---

*Last Updated: [Date]*  
*Version: 1.0*  
*Created for History vs Hype by Claude*

---

## Template Usage Notes

This template is designed to be:
- **Copied for each project** (don't edit this master)
- **Customized as needed** (not all sections required for every video)
- **Evolved over time** (update based on lessons learned)
- **Shared with collaborators** (if you expand beyond solo creator)

Save project-specific versions as:
`[PROJECT_NAME]_Production-Guide_[DATE].md`

**Remember:** Process serves quality, not bureaucracy. Use what helps, skip what doesn't. The goal is better myth-busting videos, not perfect paperwork.
