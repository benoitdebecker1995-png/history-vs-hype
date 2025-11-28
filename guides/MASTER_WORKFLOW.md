# Master Workflow Guide - History vs Hype

**Complete Production Process from Idea → Published Video**

**Last Updated:** 2025-11-08
**Estimated Time:** 25-35 hours per video
**Target Output:** 8-12 minute videos, 2-3 per week

---

## 📋 QUICK OVERVIEW

**Complete Workflow:**
1. **Topic Selection** (2-3 hours) - VidIQ research + viability check
2. **Research** (8-12 hours) - NotebookLM deep dive + source gathering
3. **Scripting** (4-6 hours) - VidIQ draft + Claude enhancement
4. **Fact-Checking** (2-4 hours) - NotebookLM verification + source documentation
5. **B-Roll Gathering** (4-8 hours) - Documents, maps, footage collection
6. **Recording** (2-4 hours) - Talking head footage, multiple takes
7. **Editing** (6-12 hours) - DaVinci Resolve assembly + polish
8. **Publishing** (2-3 hours) - Thumbnail, metadata, upload

**Total Time:** 30-52 hours per video

---

## STEP 1: TOPIC SELECTION (2-3 hours)

### A. Use VidIQ for Topic Discovery

**Tools:** VidIQ Pro + VidIQ Coach AI

#### Standard VidIQ Coach Prompt:

```
I debunk historical propaganda that causes real-world harm using primary sources displayed on screen.

MY CRITERIA FOR TOPICS:
✅ Primary sources I can show (documents, records, evidence)
✅ Real-world harm TODAY (violence, discrimination, policy)
✅ Evidence-based debunking (unbiased, multiple sources)
✅ Relevant to educated 25-44 audience

MY SCOPE: Historical propaganda (10+ years old with scholarly consensus), not breaking news.

WHAT I'VE ALREADY COVERED:
[List 3-5 recent videos]

CRITICAL QUESTION:
What HISTORICAL propaganda has:
- High search volume (5,000+ monthly)
- Low competition (under 45)
- Clear academic primary sources I can display
- Documented modern harm (violence, discrimination, policy)
- Established scholarly consensus

Give me ONE recommendation with:
- Exact title
- Why it's urgent NOW
- Search volume + competition data
- Primary historical sources available
- Expected performance
- Real-world impact potential

My audience: Males 25-44, educated, international (US/UK/Canada/Germany).
Goal: Monetization (1K subs/4K watch hours) + harm reduction.
```

**How to Use:**
1. Open VidIQ Coach
2. Paste prompt
3. Update "WHAT I'VE ALREADY COVERED" section
4. Review recommendation
5. If not excited, ask: "What's the SECOND best option?" or "Any topics related to [current news event]?"

#### Alternative Prompts:

**For Territorial Disputes (Your Proven Niche):**
```
I specialize in territorial disputes with historical roots. What colonial border conflicts are:
- In the news NOW (November 2025)
- Have high search volume
- Can be explained with primary treaty documents
- Still causing violence or diplomatic crisis

Examples of what I've covered: Venezuela-Guyana, Kashmir, Cyprus.
Give me the next highest-impact territorial dispute to cover.
```

**For Politician Fact-Checks (High CTR):**
```
What historical claims are politicians making in late 2025 that I can fact-check with primary sources?

I need:
- Specific politician quote from recent speech/interview
- Historical claim that's verifiable/debunkable
- Primary documents I can show contradicting the claim
- High search interest

Example: JD Vance colonial myths video got 11.21% CTR.
What's the next politician fact-check opportunity?
```

### B. Evaluate Topic Viability

**Decision Framework Checklist:**

Modern Relevance:
- [ ] Connected to current events (last 6 months)
- [ ] News hook or trending discussion
- [ ] Affects real people today

Evidence Availability:
- [ ] Primary sources accessible (archives, libraries, PDFs)
- [ ] At least 2-3 academic sources available
- [ ] Can be verified through NotebookLM
- [ ] Documents can be shown on screen

Visual Potential:
- [ ] Maps available (for territorial disputes)
- [ ] Historical photographs/footage exists
- [ ] Primary documents are visual (not just text)
- [ ] Modern news footage available

Controversy Level:
- [ ] Engaging but not inflammatory
- [ ] Won't trigger instant demonetization
- [ ] Can present fairly with evidence
- [ ] Audience will care about correction

Performance Potential:
- [ ] VidIQ shows 3,000+ monthly searches
- [ ] Competition score under 50
- [ ] Similar past videos performed well
- [ ] Topic fits proven formula

**If 4+ boxes checked:** Green light - proceed to research
**If 2-3 boxes checked:** Yellow light - modify angle or find better topic
**If 0-1 boxes checked:** Red light - skip this topic

### C. Topic Types That Work

**Based on Channel Analytics:**

**🔥 TIER 1 - Proven High Performers:**
1. **Territorial Disputes** (1,905 views avg)
   - Modern conflict + historical treaty
   - Example: Venezuela/Guyana Essequibo

2. **Politician Fact-Checks** (11.21% CTR avg)
   - Recent claim + primary source contradiction
   - Example: JD Vance colonial myths

**⭐ TIER 2 - Strong Performers:**
3. **Colonial Border Myths** (556-1,049 views avg)
   - Widespread myth + archival documents
   - Example: Sykes-Picot, Haiti slavery

4. **Archaeological Evidence** (8% CTR avg)
   - Popular belief + new scientific evidence
   - Example: Aztec DNA, Ancient artifacts

**❌ AVOID:**
- Generic "History of X" topics
- Topics without modern relevance
- Purely academic debates without stakes
- Subjects lacking visual evidence

---

## STEP 2: RESEARCH (8-12 hours)

### A. NotebookLM Setup

**Tool:** Google NotebookLM (https://notebooklm.google.com)

**Source Limits:**
- Max 50 sources per notebook
- 25M words total
- Supports PDFs, Google Docs, text files, web pages

**Research Organization Strategy:**

1. **Create New Notebook** for each video project
   - Name: "[Topic] - [YYYY-MM]"
   - Example: "Sykes-Picot Myths - 2025-11"

2. **Upload Sources in Priority Order:**

   **Tier 1 - Primary Sources (Upload First):**
   - Treaties, agreements, official documents
   - Government archives, diplomatic correspondence
   - Census data, official statistics
   - Court records, legal documents

   **Tier 2 - Academic Sources:**
   - Peer-reviewed journal articles
   - Academic history books (PDFs)
   - University press publications
   - Scholarly monographs

   **Tier 3 - Secondary Sources:**
   - Respected journalism with expertise
   - International organization reports
   - Declassified government documents
   - Expert historian analysis

3. **Document Each Source:**
   - Full citation
   - Why it's credible (author credentials, publisher, peer review)
   - Key findings for your video
   - Specific pages/quotes to reference

### B. NotebookLM Research Prompts

**Once sources uploaded, run these prompts:**

#### Prompt 1: Evidence Extraction
```
Please analyze all uploaded sources and identify:

1. KEY CLAIMS with source citations:
   - What are the main factual assertions about [topic]?
   - Which sources support each claim? (with page numbers)
   - Note publication dates (prioritize 2010-present for modern consensus)
   - Are there contradictions between sources?

2. PRIMARY SOURCE QUOTES:
   - Extract exact quotes from treaties, documents, letters
   - Include page numbers or chapter references
   - Include dates and full context
   - Note any contested interpretations

3. STATISTICS & DATA:
   - All numbers (deaths, distances, populations, etc.)
   - Source for each statistic with page number
   - Methodology if provided
   - Note if from peer-reviewed source

4. TIMELINE OF EVENTS:
   - Chronological sequence
   - Specific dates (not just years)
   - Causal connections between events

5. CONTESTED INFORMATION:
   - What do historians disagree about?
   - What claims need qualification?
   - What's speculation vs documented fact?
   - Are there scholarly debates requiring acknowledgment?

Format each finding with: [CLAIM] - Source: [Author, Title, Page X, Year]
```

#### Prompt 2: Modern Connections
```
Based on the uploaded sources:

1. How does this historical event connect to current events (2023-2025)?
2. Who references this history in modern political discourse?
3. What modern conflicts/policies trace back to this historical decision?
4. What are the real-world consequences TODAY?

Provide specific examples with dates and sources.
```

#### Prompt 3: Counter-Evidence Check
```
Playing devil's advocate:

1. What are the STRONGEST academic counter-arguments (steel-manned, not strawmen)?
2. Which credible scholars present opposing interpretations? (names, publications, page numbers)
3. What evidence complicates or contradicts simple explanations?
4. Where is the historical consensus uncertain or evolving?
5. What am I at risk of oversimplifying?
6. For pre-2010 sources: Has recent scholarship (2010-present) revised these claims?

I need to present this fairly - show me the complexity.
```

### C. Source Documentation

**Create a Source Spreadsheet:**

| Source | Type | Author | Date | Key Claim | Page/Quote | Tier |
|--------|------|--------|------|-----------|------------|------|
| Treaty of X | Primary | Government | 1916 | Border clause | Art. 5 | 1 |
| Book Title | Academic | Historian | 2020 | Analysis | pp. 45-67 | 2 |

**For Each Source, Note:**
- Full citation (Chicago/APA format)
- Credibility tier (1-3)
- Specific claims used from this source
- Exact quotes with page numbers
- Any biases or limitations

**Build Your Source Library:**
- Create folders by topic category
- Keep PDFs organized and backed up
- Build reference library over time
- Tag sources by region/time period

### D. Visual Research

**While researching, identify:**

**Maps to Gather:**
- [ ] Historical maps (contemporary to event)
- [ ] Modern maps (current borders)
- [ ] Side-by-side comparison potential

**Primary Documents to Show:**
- [ ] Treaty pages (specific articles)
- [ ] Letters/correspondence (smoking guns)
- [ ] Government records
- [ ] Newspaper headlines (historical)

**Photos/Footage:**
- [ ] Historical photographs (events, figures)
- [ ] Modern news footage (current relevance)
- [ ] Archaeological evidence (if applicable)

**Graphics to Create:**
- [ ] Timelines (multi-year processes)
- [ ] Comparison charts
- [ ] Text overlays (key quotes)

---

## STEP 3: SCRIPTING (4-6 hours)

### A. Generate Initial Draft with VidIQ

**Tools:** VidIQ Script Writer + Claude Pro

**Process:**
1. Use VidIQ Script Writer for initial draft
   - Input topic from Step 1
   - Specify 8-12 minute length (1,200-1,800 words)
   - Review generated structure

2. VidIQ provides decent structure but needs enhancement:
   - Hooks are often generic
   - Transitions need work
   - Evidence integration is shallow
   - Modern connections may be weak

### B. Enhance with Claude Pro

**Use Claude Pro for:**

**Better Hooks:**
```
I'm writing a video about [topic]. VidIQ gave me this hook: [paste hook]

My audience is educated males 25-44 who want evidence over hype. They value:
- Modern political relevance
- Primary source verification
- Nuanced takes

The hook needs to:
1. Show modern consequence first (0-15 seconds)
2. Promise evidence reveal at 0:45
3. Create tension/question

Rewrite this hook to be more compelling while staying accurate.
```

**Stronger Transitions:**
```
I need "because/therefore" transitions between these sections:
[paste two script sections]

Create 2-3 transition options that:
- Connect causally (not just chronologically)
- Maintain narrative momentum
- Set up next payoff

Educational tone, not clickbait.
```

**Evidence Integration:**
```
I have this primary source: [paste document quote]

How do I introduce this in the script to maximize impact?
- When should I reveal it? (timing)
- What setup does it need?
- What phrasing makes it feel like a smoking gun?
```

### C. Script Structure (Proven Formula)

**Use This Exact Structure:**

#### SECTION 1: COLD OPEN / HOOK (0:00-0:15)
**Goal:** Show modern political consequence

**Formula:**
- Date (recent, specific)
- Modern figure/event
- Historical claim they make
- Stakes (what's at risk)

**Example:**
> December 8, 2024. Israel invades Syria. Seizes several hundred square miles.
> Netanyahu: "We'll remain until another arrangement is found."
> January 2025. US Envoy: "Israel sees Sykes-Picot borders as meaningless."

**Length:** 50-60 words (15 seconds)

#### SECTION 2: BUILD TENSION (0:15-0:45)
**Goal:** Set up the contradiction you'll reveal

**Formula:**
- The claim being made
- Why it matters
- What people believe
- "But when I checked the documents..."

**Example:**
> Politicians blame Sykes-Picot for every Middle East conflict.
> "One secret agreement." "Drew borders on an empty map."
> But when I checked the actual treaty...

**Length:** 100-120 words (30 seconds)

#### SECTION 3: FIRST PAYOFF (0:45-1:15)
**Goal:** Deliver first piece of evidence - prevents drop-off at 1:11 mark

**Formula:**
- Show primary document/map
- State the contradiction clearly
- Visual evidence on screen
- "It's more complicated than that"

**Example:**
> Side-by-side: 1916 Sykes-Picot map vs. modern borders.
> They don't match.
> Iraq's borders weren't finalized in 1916. They were finalized in 1926.
> After a 10-year negotiation process.

**Length:** 120-150 words (30 seconds)

**CRITICAL:** This payoff at 0:45 is what prevents viewer drop-off. Must deliver real evidence, not just promise.

#### SECTION 4: DEEP DIVE - CLAIM 1 (1:15-3:00)
**Goal:** First interconnected claim with evidence

**Formula:**
- State claim
- Historical context (briefly)
- Primary source quote/document
- Analysis (what this means)
- Transition to next claim ("But it gets worse")

**Example Structure:**
> Let's start with the promise to the Arabs.
> October 24, 1915. McMahon-Hussein Correspondence.
> [Show letter on screen]
> Britain promised: "...independence of the Arabs..."
> Seven months before Sykes-Picot.

**Length:** 400-500 words (1:45 minutes)

#### SECTION 5: CLAIM 2 - SMOKING GUN (3:00-5:00)
**Goal:** Most dramatic piece of evidence

**Formula:**
- Setup the significance
- Build anticipation ("Here's the smoking gun")
- Show document/quote
- Pause for impact
- Explain implications

**Example Structure:**
> November 23, 1915. Seven British officials brief François Georges-Picot.
> They tell him about the Arab promises.
> Picot's response - official meeting minutes:
> (PAUSE)
> [Show quote on screen]
> He knew. They all knew.

**Length:** 400-500 words (2 minutes)

**This is your STRONGEST evidence. Give it dramatic weight.**

#### SECTION 6: CLAIM 3 - MODERN IMPACT (5:00-7:00)
**Goal:** Connect pattern to current events

**Formula:**
- Pattern revealed (not just one instance)
- Modern parallel (recent news)
- Why this matters today
- Who benefits from the myth

**Example Structure:**
> This wasn't one bad agreement. It was three contradictory promises:
> 1915: Arabs → Independence
> 1916: France → Colonial zones
> 1917: Zionists → National home
> All incompatible.
>
> Fast forward to 2025: [modern news hook]
> Same pattern. Different players.

**Length:** 400-600 words (2 minutes)

#### SECTION 7: COMPLEXITY & NUANCE (7:00-9:00)
**Goal:** Show you're not oversimplifying

**Formula:**
- Acknowledge what's contested
- Present counter-evidence
- Show complexity
- Explain why simple narrative persists
- Who benefits from oversimplification

**Example:**
> Did European colonial powers cause problems? Absolutely.
> Are borders part of modern conflicts? Yes.
> But it wasn't one secret map in 1916.
> It was a 15-year process with multiple actors.

**Length:** 400-600 words (2 minutes)

#### SECTION 8: SYNTHESIS & CTA (9:00-10:00)
**Goal:** Bring it together, call to action

**Formula:**
- Restate main finding
- Why accurate history matters
- Modern consequences of believing myth
- CTA: "Full sources in description. Subscribe for more myth-busting."

**Example:**
> So when politicians cite Sykes-Picot to justify 2025 expansion...
> They're using oversimplified history to justify current policy.
> Accurate history matters. Full source list in description.
> Subscribe if you want evidence, not hype.

**Length:** 150-200 words (1 minute)

**TOTAL:** ~1,500-2,000 words = 10-12 minutes at 150 words/minute

### D. Script Writing Checklist

Before moving to fact-checking:

**Structure:**
- [ ] Hook delivers modern consequence (0-15 sec)
- [ ] First payoff at 0:45 (prevents drop-off)
- [ ] Micro-hooks every 2 minutes ("But it gets worse")
- [ ] "Because/therefore" transitions (causal, not chronological)
- [ ] Synthesis brings it back to modern impact

**Language:**
- [ ] Academic framing (not punditry)
- [ ] Complexity acknowledged
- [ ] Avoid absolutist language ("all historians agree")
- [ ] No conspiracy framing
- [ ] Respectful of all sides while showing evidence

**Evidence:**
- [ ] Every major claim has source attribution
- [ ] Primary sources quoted directly
- [ ] Statistics are specific
- [ ] Counter-evidence acknowledged
- [ ] Complexity maintained

**Retention:**
- [ ] Visual variety planned every 30-45 seconds
- [ ] Questions posed to audience
- [ ] "You might think X, but actually Y" structure
- [ ] Engagement triggers every 2 minutes

---

## STEP 4: FACT-CHECKING (2-4 hours)

### A. NotebookLM Verification

**Upload completed script to your NotebookLM notebook** (the one with all your sources)

#### Fact-Check Prompt:
```
I'm about to film this script. I need you to fact-check EVERY claim against the uploaded sources.

For each factual assertion in the script:
1. Is it supported by the sources? Which one(s)?
2. Is the quote exact or paraphrased?
3. Are dates/numbers accurate?
4. Is anything oversimplified or missing context?
5. Are there contradictions I should note?

Format:
✅ VERIFIED: [claim] - Source: [citation]
❌ NOT FOUND: [claim] - No source supports this
⚠️ NEEDS CONTEXT: [claim] - True but needs qualification: [context]

Be strict. My credibility depends on accuracy.
```

#### Quote Verification Prompt:
```
Verify these specific quotes are EXACT from primary sources:

[List all quotes in script]

For each:
- Exact text match? (Yes/No)
- Source citation: [Author, Title, Page]
- Any missing context that changes meaning?
```

#### Statistics Verification Prompt:
```
Verify all numbers in the script:

[List all statistics, dates, measurements, casualties, etc.]

For each:
- Source: [citation]
- Methodology if relevant
- Any disputes about this number?
```

### B. Manual Fact-Checking

**Source Hierarchy (from fact-checking-protocol.md):**

**Tier 1 - Most Reliable:**
- Primary documents (treaties, census, archives)
- Peer-reviewed academic publications
- Expert historians specializing in topic

**Tier 2 - Reliable:**
- Respected journalists with expertise
- International organization reports
- University press books

**Tier 3 - Use With Caution:**
- Declassified government documents (note bias)
- News reports (verify with academic sources)
- Popular history books (check credentials)

**For Each Major Claim:**
- [ ] At least 2 sources (preferably Tier 1-2)
- [ ] No logical fallacies in argument
- [ ] Contested information clearly labeled
- [ ] Academic consensus noted where it exists
- [ ] Counter-evidence acknowledged

### C. Create Verification Spreadsheet

**Template:**

| Claim | Script Location | Source 1 | Source 2 | Status | Notes |
|-------|----------------|----------|----------|--------|-------|
| "Treaty signed May 16, 1916" | 0:45 | Treaty text | Barr pg 23 | ✅ Verified | |
| "460 square kilometers" | 0:10 | ❌ Not found | Web only | ⚠️ Change | Use "several hundred sq mi" |

**Status Codes:**
- ✅ Verified (2+ Tier 1-2 sources)
- ⚠️ Needs Context (true but incomplete)
- ❌ Not Found (no source supports)
- 🔄 Contested (historians disagree)

### D. Script Updates

**Based on fact-check results:**

1. **Correct all ❌ Not Found claims**
   - Remove or find source
   - Never publish unverified claims

2. **Add context to ⚠️ claims**
   - "According to most historians..."
   - "The evidence suggests..."
   - "Records show... though some dispute..."

3. **Label 🔄 Contested claims**
   - "Historians disagree about..."
   - "Some sources claim X, others Y"
   - Present multiple perspectives

4. **Enhance ✅ Verified claims**
   - Add "Reading from the treaty..."
   - "Official records show..."
   - Strengthen attribution

### E. Final Pre-Production Checklist

- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments
- [ ] Counter-evidence acknowledged
- [ ] Complexity maintained (not oversimplified)
- [ ] Modern consequences clearly stated

**If ALL boxes checked:** Approved for filming
**If ANY box unchecked:** Fix before filming

---

## STEP 5: B-ROLL GATHERING (4-8 hours)

### A. B-Roll Requirements List

**Create a checklist based on script** (see example: sykes-picot-2025/B-ROLL-CHECKLIST.md)

**Categorize by Priority:**

🔴 **CRITICAL (Cannot Film Without):**
- Primary documents mentioned in script
- Maps for geographic explanations
- Key comparison graphics
- Evidence for 0:45 payoff

🟡 **IMPORTANT (Significantly Strengthens):**
- Historical portraits
- Treaty documents
- Timeline graphics
- Modern news footage

🟢 **NICE-TO-HAVE (Visual Variety):**
- Historical photos
- B-roll footage
- Supporting graphics
- Atmospheric shots

### B. Where to Find B-Roll

**Public Domain / Free Sources:**

**Primary Documents:**
- Yale Avalon Project: https://avalon.law.yale.edu
- National Archives (US): https://www.archives.gov
- British National Archives: https://www.nationalarchives.gov.uk
- Library of Congress: https://www.loc.gov
- Your NotebookLM PDFs (extract images)

**Historical Maps:**
- Wikipedia Commons: https://commons.wikimedia.org
- David Rumsey Map Collection: https://www.davidrumsey.com
- Old Maps Online: https://www.oldmapsonline.org

**Historical Photos:**
- Wikipedia Commons (check individual licenses)
- Library of Congress
- Imperial War Museums: https://www.iwm.org.uk
- National Archives

**Modern Footage:**
- News clips (Fair Use for education/commentary)
- YouTube (Creative Commons filter)
- Reuters/AP (stock footage - may require license)

### C. Licensing Notes

**Public Domain (Free):**
- Pre-1928 US works
- Government documents
- Expired copyrights
- Check each source

**Creative Commons:**
- Wikipedia Commons (check each image)
- Attribute as required
- Note license type (CC-BY, CC-BY-SA, etc.)

**Fair Use (Educational):**
- News footage (short clips only)
- Commentary/analysis (transformative use)
- Limit: ~10-15 seconds max per clip
- Always add commentary

### D. B-Roll Organization

**File Naming Convention:**
```
[Topic]-[Type]-[Description]-[Source].jpg

Examples:
SykesPicot-Map-1916Agreement-WikiCommons.png
SykesPicot-Document-McMahonLetter-YaleAvalon.pdf
SykesPicot-Photo-MarkSykes-WikiCommons.jpg
```

**Folder Structure:**
```
B-Roll/
├── Maps/
├── Documents/
├── Photos-Historical/
├── Photos-Modern/
├── Graphics-Created/
└── Footage/
```

**Document Sources:**
- Create credits.txt with all attributions
- Full URL to source
- License type
- Download date

---

## STEP 6: RECORDING (2-4 hours)

### A. Setup & Preparation

**Before Recording:**
- [ ] Script printed or on teleprompter
- [ ] Camera setup with 4 focal lengths (1.0, 1.2, 1.4, 1.6)
- [ ] Lighting consistent
- [ ] Audio test (USB microphone)
- [ ] Background appropriate
- [ ] Hydrated, warmed up voice

**When to Show Your Face (60-70% of video):**
- Making arguments and interpretations
- Explaining causation
- Connecting historical events
- Asking rhetorical questions
- Building narrative
- Emotional emphasis
- "This is why it matters" moments

**When to Use B-Roll (30-40% of video):**
- Showing evidence (maps, documents, photos)
- Geographic explanations
- Timeline sequences
- Modern news hooks
- Visual proof of claims

### B. Recording Best Practices

**Multiple Takes:**
- Record each section 2-3 times
- Different energy levels
- Vary pacing
- Choose best in editing

**Focal Length Variety:**
- Wide (1.0): Scene setting
- Medium (1.2): Main delivery
- Close (1.4): Emphasis moments
- Very Close (1.6): Intimate/serious points

**Energy & Pacing:**
- Higher energy than feels natural (camera dampens)
- Pause for emphasis (edit out filler)
- Vary tone (monotone = retention drop)
- Rehearse difficult sections

**Common Mistakes:**
- Too flat delivery
- Reading instead of performing
- No pauses for emphasis
- Inconsistent energy

### C. Hybrid Talking Head Strategy

**See: guides/HYBRID_TALKING_HEAD_GUIDE.md for full details**

**Golden Rule:**
If the B-roll doesn't make your argument stronger, stay on camera.

**B-roll is evidence, not decoration.**

You are the authority making an argument, not just a narrator.

---

## STEP 7: EDITING (6-12 hours)

### A. DaVinci Resolve Workflow

**Tools:** DaVinci Resolve (free version sufficient)

**Import & Organization:**
1. Create project: [Topic]-[Date]
2. Import all footage to Media Pool
3. Create bins:
   - Talking Head
   - B-Roll - Maps
   - B-Roll - Documents
   - B-Roll - Photos
   - B-Roll - Modern
   - Graphics
   - Audio

**Rough Cut (2-3 hours):**
1. Lay down talking head footage following script
2. Cut out mistakes, pauses, filler words
3. Maintain pacing (don't let energy drop)
4. Use jump cuts to compress time
5. Mark B-roll insertion points

**B-Roll Integration (3-5 hours):**
1. Insert B-roll at marked points
2. Show documents when quoting them
3. Maps for geographic explanations
4. Photos for historical context
5. Modern footage for news hooks

**Visual Variety Rules:**
- Change visual every 30-45 seconds
- Mix: talking head → B-roll → talking head
- Never more than 90 seconds straight talking head
- Never more than 30 seconds pure B-roll (except critical evidence)

**Text Overlays (1-2 hours):**
1. Key dates (large, clear)
2. Important quotes (exact text from documents)
3. Names of figures
4. Timeline markers
5. Source citations (bottom right)

**Example Overlays:**
- "December 8, 2024"
- "October 24, 1915: McMahon-Hussein Correspondence"
- "Mark Sykes, British Diplomat"
- "Source: TNA, FO 882/2"

**Color Grading (1 hour):**
- Consistent color across all talking head shots
- Enhance contrast slightly
- Warm tone for talking head
- Cooler tone for historical documents (makes them feel old)

**Audio Mixing (1-2 hours):**
- Normalize talking head audio
- Remove background noise
- Add subtle music (30-40% volume)
- Duck music under important points
- Fade in/out smoothly

**Music Selection:**
- YouTube Audio Library (royalty-free)
- Subtle, not distracting
- Match tone (serious topics = serious music)
- See: COPYRIGHT_FREE_MUSIC_GUIDE.md

**Final Polish (1-2 hours):**
- Watch full video start to finish
- Check pacing (does it drag anywhere?)
- Verify all text overlays are readable
- Ensure audio levels consistent
- Add fade in/out
- Export settings: 1080p, H.264, 20 Mbps

### B. Retention Optimization During Editing

**Critical Moments:**

**0:00-0:15:** Cold open
- Highest energy
- Modern hook
- No intro card (get right to it)

**0:45:** First payoff
- Clear visual evidence
- "Here's the smoking gun"
- Prevent 1:11 drop-off

**Every 2 minutes:** Micro-hooks
- "But it gets worse"
- "Here's what they're not telling you"
- "This is where it gets interesting"

**Pattern Breaks:**
- Zoom in for emphasis
- Cut to B-roll at perfect moment
- Silence/pause before revelation
- Music swell at key points

### C. Common Editing Mistakes

**Avoid:**
- ❌ Too much B-roll (you are the authority)
- ❌ Text overlays that distract from speech
- ❌ Music too loud
- ❌ Inconsistent pacing
- ❌ Letting energy drop mid-video
- ❌ Not enough visual variety
- ❌ Jump cuts that are jarring

**Seek:**
- ✅ Smooth flow despite cuts
- ✅ B-roll that strengthens arguments
- ✅ Consistent energy throughout
- ✅ Clear visual hierarchy (what to look at)
- ✅ Readable text at mobile size

---

## STEP 8: PUBLISHING (2-3 hours)

### A. Thumbnail Creation

**Tools:** Photoshop or Canva

**Proven Formula:**
- Face (yours) showing emotion + Document/Map
- Split screen or layered composition
- Bold text: "[POLITICIAN/TOPIC] vs. THE DOCUMENTS"
- High contrast (readable on mobile)
- 3-5 words maximum text

**Examples of What Works:**
- "JD VANCE vs. THE DOCUMENTS"
- "SYKES-PICOT: THE LIE"
- "I CHECKED THE MAPS"

**Testing:**
- Create 2-3 versions
- A/B test with VidIQ
- Check readability at phone size
- Avoid clickbait that script doesn't deliver

**Technical Specs:**
- 1280x720 pixels
- Under 2MB file size
- JPG or PNG
- High contrast, saturated colors

### B. Title Optimization

**Formula That Works:**
"[BOLD CLAIM/FIGURE] | [EVIDENCE PROMISE]"

**Examples:**
- "JD Vance's Colonial Myths | I Checked the Documents" (11.21% CTR ✅)
- "Sykes-Picot Didn't Draw Iraq's Borders | Here's What Did"
- "Aztec Child Sacrifice: What DNA Actually Shows" (8% CTR ✅)

**Title Checklist:**
- [ ] Under 60 characters (doesn't get cut off)
- [ ] Includes searchable keywords
- [ ] Creates curiosity gap
- [ ] Promises evidence/reveal
- [ ] Specific, not generic
- [ ] Accurate to content (no clickbait)

**Avoid:**
- Generic: "The History of Sykes-Picot"
- Clickbait: "You Won't BELIEVE What I Found!"
- Academic: "Reassessing the Sykes-Picot Agreement's Impact"

**Seek:**
- Specific: "Sykes-Picot Didn't Create Modern Borders | Primary Sources"
- Evidence: "I Fact-Checked JD Vance | The Documents Don't Match"

### C. Description Template

```
[2-3 sentence hook - visible before "show more"]

Politicians blame Sykes-Picot for every Middle East conflict. But when I checked the actual treaty and border finalization records, the story is far more complicated—and more interesting.

[Paragraph summary]

In this video, I fact-check the myth that Sykes-Picot "drew borders on an empty map" by showing you the primary sources: the actual 1916 agreement, the McMahon-Hussein Correspondence, the Balfour Declaration, and the League of Nations border negotiations that happened over 10 years.

TIMESTAMPS:
0:00 - Modern Crisis: Israel & Syria
0:45 - The Map Comparison (First Reveal)
2:15 - Sykes-Picot: What It Actually Said
3:40 - The Three Contradictory Promises
5:50 - Iraq Existed Before 1916
7:30 - How Borders Were REALLY Finalized
9:15 - Why This Myth Persists

PRIMARY SOURCES SHOWN:
• Sykes-Picot Agreement (May 16, 1916)
• McMahon-Hussein Correspondence (October 24, 1915)
• Balfour Declaration (November 2, 1917)
• 1893 Ottoman Map showing "al-'Iraq al-'Arabi"
• Treaty of Sèvres (August 10, 1920)
• Treaty of Lausanne (July 24, 1923)

FULL SOURCE LIST:
[List all sources with citations]

1. Barr, James. *A Line in the Sand: Britain, France and the Struggle That Shaped the Middle East.* London: Simon & Schuster, 2011.
2. Pedersen, Susan. *The Guardians: The League of Nations and the Crisis of Empire.* Oxford: Oxford University Press, 2015.
[etc.]

RELATED VIDEOS:
• Venezuela vs Guyana: [link]
• JD Vance Colonial Myths: [link]

ABOUT THIS CHANNEL:
History vs Hype debunks historical myths using primary source verification. Evidence over opinions. Sources in every video.

Subscribe for fact-based history that connects past propaganda to modern consequences.

#SykesPicot #HistoryFacts #MiddleEast #Geopolitics #BorderDisputes #HistoricalMyths

---

📚 Research tools: NotebookLM, Yale Avalon Project, British National Archives
🎥 Edited in: DaVinci Resolve
📖 Full bibliography: [link to Google Doc if extensive]

For corrections or additional sources, comment below. This channel values accuracy above all.
```

**Description Checklist:**
- [ ] First 2 sentences are hooks (visible before "show more")
- [ ] Timestamps for all major sections
- [ ] Primary sources listed
- [ ] Full source bibliography
- [ ] Related video links (keep viewers watching)
- [ ] Channel description
- [ ] Keywords naturally integrated
- [ ] Contact for corrections

### D. Tags & Metadata

**10-15 Tags (Mix Broad & Specific):**

Broad:
- History
- Documentary
- Educational
- Fact-checking

Specific:
- Sykes-Picot Agreement
- Middle East history
- Colonial borders
- Geopolitics
- Historical myths
- Primary sources

Branded:
- History vs Hype
- Historical fact-checking

**Category:** Education

**Language:** English

**Caption:** Upload SRT if available (improves accessibility & SEO)

### E. Publishing Checklist

Before clicking "Publish":

- [ ] Title optimized (under 60 chars, includes keywords)
- [ ] Thumbnail uploaded (1280x720, under 2MB)
- [ ] Description complete (timestamps, sources, links)
- [ ] Tags added (10-15 relevant tags)
- [ ] Category set to "Education"
- [ ] Visibility: Public (or scheduled)
- [ ] End screen: Subscribe + related video
- [ ] Cards: Related videos at 2:00, 5:00, 8:00
- [ ] Playlist: Added to relevant playlist
- [ ] Comments: Enabled
- [ ] Sharing: Enabled

**Best Upload Time (Based on Analytics):**
- Tuesday-Thursday
- 2-4 PM EST
- Avoid Friday-Sunday

### F. Post-Publishing

**Within 1 Hour:**
- [ ] Pin comment with key source or question
- [ ] Share to Reddit (r/history, topic-specific subs)
- [ ] Tweet/X with key finding
- [ ] Check for any upload errors

**Within 24 Hours:**
- [ ] Monitor comments, respond to questions
- [ ] Check analytics (CTR, retention at 0:45 and 1:11)
- [ ] Note any patterns for future videos

**Within 1 Week:**
- [ ] Create 5-10 Shorts from best moments
- [ ] Respond to all substantive comments
- [ ] Document performance in analytics tracker

---

## 🔄 POST-PRODUCTION WORKFLOW

### Create Shorts (2-3 hours)

**Tools:** VidIQ Clipping Tool or manual editing

**Strategy:**
- Identify 5-10 self-contained 30-60 second segments
- Focus on single point/fact per short
- Add text captions (essential for shorts)
- Vertical format (9:16)
- Post on off-days from long-form

**Example Shorts from Long-Form:**
1. The 0:45 payoff (map comparison)
2. Smoking gun quote (2:30)
3. Modern news hook (0:10)
4. Single statistic reveal
5. Counter-intuitive fact
6. "Here's what they don't tell you"

**Shorts Goal:**
- Drive traffic to long-form
- Include CTA: "Full video on my channel"
- Don't make standalone shorts (low conversion)

### Analytics Review

**Track These Metrics:**
- Views (first 24 hours, first week)
- CTR (target: 4-5%+)
- Retention (target: 30-35%+, check drop-off at 0:45, 1:11, 2:00)
- Subscribers gained (target: 5-10+)
- Watch time (target: 20-50+ hours)
- Traffic sources (Search, Suggested, Browse)

**What to Learn:**
- Where do people drop off? (improve structure)
- What thumbnails work? (test styles)
- What titles get clicks? (refine formula)
- What topics perform? (double down)

**Monthly Review:**
- Top 5 videos - what worked?
- Worst 5 videos - what failed?
- Retention patterns across all videos
- Subscriber conversion rate
- Adjust strategy accordingly

---

## 📚 TOOLS & RESOURCES

### Essential Tools

**Research:**
- NotebookLM (free) - Source-grounded research
- VidIQ Pro ($) - Topic research, script generation
- Claude Pro ($) - Fact-checking, editing help
- Yale Avalon Project (free) - Primary documents
- Wikipedia Commons (free) - Public domain images

**Production:**
- DaVinci Resolve (free) - Video editing
- Photoshop or Canva ($) - Thumbnails
- USB Microphone ($50-150) - Audio
- Camera/Phone - Video recording

**Publishing:**
- YouTube Studio (free) - Upload & analytics
- VidIQ (free/pro) - Optimization & clipping

### Learning Resources

**DaVinci Resolve:**
- Ask Claude with screenshots for specific help
- Official tutorials: blackmagicdesign.com/products/davinciresolve/training
- YouTube: "DaVinci Resolve for beginners"

**Thumbnail Design:**
- Ask Claude for feedback on drafts
- Study top performers in your niche
- A/B test different styles

**Fact-Checking:**
- fact-checking-protocol.md (this repository)
- NotebookLM verification prompts (above)
- Source hierarchy guidelines (Tier 1-3)

**YouTube Strategy:**
- Channel analytics (YouTube Studio)
- VidIQ trend reports
- channel-data/CHANNEL_ANALYTICS_MASTER.md

---

## ⏱️ TIME MANAGEMENT

### Realistic Timeline

**Per Video (Total: 30-52 hours):**
- Day 1 (3 hours): Topic selection + initial research
- Day 2-3 (10 hours): Deep research + source gathering
- Day 4 (6 hours): Scripting + fact-checking
- Day 5 (6 hours): B-roll gathering
- Day 6 (4 hours): Recording
- Day 7-8 (12 hours): Editing
- Day 9 (3 hours): Thumbnail + publishing

**Target Output:**
- 2-3 videos per week = ~90-150 hours/week (FULL TIME)
- 1 video per week = ~40 hours (manageable part-time)

**Ways to Speed Up:**
- Build B-roll library (reuse footage)
- Create template projects in DaVinci
- Batch record multiple videos
- Improve editing speed with practice
- Use slash commands for automation

---

## 🎯 QUALITY GATES

### Before Publishing, Verify:

**Research Quality:**
- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for major points
- [ ] No logical fallacies

**Production Quality:**
- [ ] Audio clear (no background noise)
- [ ] Video sharp (no blur)
- [ ] Consistent lighting
- [ ] Text overlays readable on mobile
- [ ] B-roll strengthens arguments (not just decoration)

**Retention Optimization:**
- [ ] Hook delivers modern consequence (0-15 sec)
- [ ] First payoff at 0:45
- [ ] Visual variety every 30-45 sec
- [ ] Micro-hooks every 2 minutes
- [ ] Energy maintained throughout

**Publishing Optimization:**
- [ ] Thumbnail tested at mobile size
- [ ] Title under 60 characters with keywords
- [ ] Description includes timestamps & sources
- [ ] Tags relevant (10-15)
- [ ] End screen & cards added

**Mission Alignment:**
- [ ] Modern relevance clear
- [ ] Primary sources shown
- [ ] Complexity maintained (not oversimplified)
- [ ] Academic balance (counter-evidence acknowledged)
- [ ] Why it matters today is explicit

---

## 🚫 COMMON PITFALLS

**Avoid These Mistakes:**

**Research Phase:**
- ❌ Relying on single source
- ❌ Skipping fact-check to save time
- ❌ Using Wikipedia as primary source
- ❌ Not checking author credentials

**Scripting Phase:**
- ❌ Generic hooks ("Today I'm going to tell you about...")
- ❌ Delaying first payoff past 1:00
- ❌ Oversimplifying complexity
- ❌ Not connecting to modern relevance

**Editing Phase:**
- ❌ Too much B-roll (you lose authority)
- ❌ Not enough visual variety (retention drops)
- ❌ Inconsistent audio levels
- ❌ Text overlays too small/too fast

**Publishing Phase:**
- ❌ Clickbait titles that script doesn't deliver
- ❌ No timestamps in description
- ❌ Forgetting source list
- ❌ Not monitoring early comments

---

## 🎓 CONTINUOUS IMPROVEMENT

### After Each Video:

**Ask:**
1. What worked? (check retention graph)
2. What didn't? (where did people leave?)
3. What would I do differently next time?
4. What took longer than expected?
5. How can I streamline the process?

**Document:**
- Update this workflow with learnings
- Track what thumbnail styles work
- Note which topics perform
- Build templates for repetitive tasks

**Iterate:**
- Refine hook formula based on data
- Improve B-roll sourcing efficiency
- Speed up editing workflow
- Optimize publishing checklist

---

## 📋 WORKFLOW CHECKLIST (Quick Reference)

**Print this for each video:**

- [ ] Topic selected via VidIQ
- [ ] Viability check (4+ criteria met)
- [ ] NotebookLM notebook created
- [ ] Primary sources uploaded to NotebookLM
- [ ] Research prompts run
- [ ] Source spreadsheet created
- [ ] Script drafted (VidIQ + Claude)
- [ ] Script follows proven structure
- [ ] Script fact-checked via NotebookLM
- [ ] Verification spreadsheet complete
- [ ] All ❌ and ⚠️ items resolved
- [ ] B-roll checklist created
- [ ] Critical B-roll gathered
- [ ] Recording setup tested
- [ ] Video recorded (multiple takes)
- [ ] Rough cut complete
- [ ] B-roll integrated
- [ ] Text overlays added
- [ ] Audio mixed
- [ ] Color graded
- [ ] Thumbnail created (2-3 versions)
- [ ] Title optimized
- [ ] Description complete (timestamps, sources)
- [ ] Tags added
- [ ] End screen & cards configured
- [ ] Quality gates passed
- [ ] Published at optimal time
- [ ] Shorts created from best moments
- [ ] Performance tracked in analytics

**When ALL boxes checked:** Video complete ✅

---

## 🔗 RELATED DOCUMENTS

- **Master-Project-Template.md** - NotebookLM research prompts
- **fact-checking-protocol.md** - Source verification standards
- **HYBRID_TALKING_HEAD_GUIDE.md** - When to show face vs. B-roll
- **youtube-comment-response-guide.md** - How to respond to comments
- **CHANNEL_ANALYTICS_MASTER.md** - What's working, performance data
- **channel-strategy-2025.md** - Overall strategy and vision

---

**This workflow is your production bible. Follow it for consistency, efficiency, and quality.**

**Last Updated:** 2025-11-08
**Next Review:** December 2025 (incorporate learnings from Sykes-Picot video)
