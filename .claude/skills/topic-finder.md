# Topic Finder Skill - History vs Hype

Find trending topics that could be hits on the History vs Hype channel by analyzing current news and identifying historical myths with modern relevance.

## When to Use

- User runs `/find-topic` command
- Part of `/create-video` workflow at Stage 1

## Your Task

You will do preliminary web trend research, then the user will supplement with VidIQ CoachPro insights.

## Step 1: Web Trend Research

Use WebSearch to research:

1. **Recent news hooks** (last 7-30 days) involving:
   - Colonial history controversies
   - Border disputes or territorial claims
   - Historical myths in political speeches/statements
   - Cultural misconceptions going viral
   - Geopolitical conflicts with historical roots

2. **Evergreen topics with recent triggers:**
   - Old disputes with new developments (like Essequibo: 1899 treaty + 2025 warship)
   - Historical figures being misquoted/misrepresented recently
   - Academic research contradicting popular narratives
   - Anniversaries of historical events with modern debates

3. **Search queries to run:**
   - "border dispute 2025"
   - "colonial history controversy"
   - "historical myth debunked"
   - "territorial claim [current month/year]"
   - "historian fact-checks politician"
   - "[recent political figure] historical claim"

## Step 2: Topic Evaluation

For each potential topic found, evaluate:

### ✅ STRONG FIT (Recommend highly)
- Has recent news hook (last 3 months)
- Involves historical myth with modern consequences
- Primary sources likely accessible (treaties, documents, archives)
- NOT overdone by other creators
- **CRITICAL: Frame as myth-busting vs. explanatory** (VidIQ data shows myth-busting angle has LOWER competition)
- Clear "before and after" or pattern to reveal
- Emotional stakes (affects real people today)

### ⚠️ MAYBE (Flag for user consideration)
- Interesting but sources might be hard to access
- Good topic but similar videos exist
- Strong evidence but low current relevance
- Recent news hook but story still developing

### ❌ SKIP (Note why it doesn't fit)
- No accessible primary sources
- Too overdone (every history channel covered it)
- Too recent (still unfolding, facts unclear)
- Purely opinion-based (no objective evidence to analyze)

## Step 3: Present Findings

Format your research as:

```markdown
# TOPIC RESEARCH RESULTS - [Date]

## 🔥 HIGHLY RECOMMENDED TOPICS

### Topic 1: [Catchy Title]
**Recent Hook:** [What happened in last 3 months that makes this timely]
**Historical Myth:** [What false narrative is being spread]
**Modern Stakes:** [Why this matters in 2025 - political/cultural impact]
**Evidence Potential:** [Types of primary sources likely available]
**Viral Potential:** [Why this could perform well - controversy, relevance, etc.]
**Similar Coverage:** [Has anyone else done this? How would yours be different?]

### Topic 2: [Catchy Title]
[Same structure]

## ⚠️ POTENTIAL TOPICS (Need More Investigation)

### Topic 3: [Title]
**Why Interesting:** [What caught your attention]
**Concerns:** [Why it's not an immediate yes - source access, overdone, etc.]

## ❌ TOPICS RESEARCHED BUT NOT RECOMMENDED

### Topic 4: [Title]
**Why Skipped:** [No sources / Too overdone / Too recent / etc.]

---

## VidIQ COACHPRO INTEGRATION

Now paste this prompt into VidIQ CoachPro and provide the results:

**Prompt for VidIQ:**
"Based on my channel's performance (History vs Hype - historical myth-busting with primary sources, best videos on colonial borders and political fact-checking), what topics are trending in the history/education/political commentary space? Focus on:
1. Historical controversies in recent news (last 30 days)
2. Border disputes or territorial claims
3. Politicians or public figures making historical claims
4. Cultural myths going viral
5. Topics similar to my top performers: [Vance fact-checking, Essequibo dispute]

Provide search volume, competition level, and recent trend data."

**After VidIQ Results:**
Paste VidIQ's response below and I'll cross-reference with my web research to finalize recommendations.
```

## Step 4: Cross-Reference with VidIQ

When user provides VidIQ CoachPro output:

1. **Identify overlaps** - Topics you found that VidIQ also shows trending
2. **Highlight VidIQ exclusives** - Trending topics you didn't find (evaluate against criteria)
3. **Search volume analysis** - Which topics have best discoverability
4. **Competition check** - Are topics oversaturated or underserved?

Then provide:

```markdown
# FINAL TOPIC RECOMMENDATIONS

## 🎯 TOP 3 TOPICS (Web Research + VidIQ Validated)

### 1. [TOPIC NAME]
**Why This One:**
- ✅ Recent news hook: [Event/date]
- ✅ VidIQ search volume: [Data from VidIQ]
- ✅ Competition: [Low/Medium - from VidIQ]
- ✅ Primary sources available: [List 2-3 you found]
- ✅ Fits channel brand: [How it matches Vance/Essequibo formula]
- ✅ Viral quote potential: [Example of dramatic quote/statistic]

**Suggested Angle:** [Specific approach - "Fact-checking [Person]'s claim about X" or "The [Treaty] that's causing [Current Event]"]

**Myth-Busting Framing:** [How to position as myth-busting vs. explanatory - e.g., "Politicians Blame X. It Was Never Used." vs. "The History of X Explained"]

**Competition Analysis:** [VidIQ shows myth-busting angle competition vs. explanatory angle]

**Estimated Research Difficulty:** [Easy/Medium/Hard]

### 2. [TOPIC NAME]
[Same structure]

### 3. [TOPIC NAME]
[Same structure]

---

**Next Step:** Choose a topic and I'll run `/deep-research` to do comprehensive preliminary analysis before you buy sources.
```

## Quality Standards

### Good Topic Signals:
- Specific person made a false historical claim recently
- Treaty/document from decades/centuries ago causing problems NOW
- Academic research directly contradicts popular narrative
- Pattern of 3+ related incidents showing systematic issue
- Clear "smoking gun" evidence exists (treaty text, primary documents)
- **CAN BE FRAMED AS MYTH-BUSTING** (lower competition than explanatory content)

### VidIQ Competitive Advantage:
- **MYTH-BUSTING TITLES** (e.g., "Politicians Blame X. It Was Never Used.") have lower competition than EXPLANATORY TITLES (e.g., "The History of X Explained")
- **FACT-CHECK ANGLES** (e.g., "I Fact-Checked 3 Claims") outperform general historical analysis
- **AUTHORITY CHALLENGE** formats create curiosity gap and imply hidden truth

### Red Flags:
- "I think this might be interesting..." (need concrete news hook)
- No primary sources mentioned in news coverage
- Topic relies on interpretation rather than documents
- Every major history channel already covered it
- Story still developing (facts not settled)

## Channel Performance Context

Reference these when evaluating topics:

**Top Performers:**
- Vance fact-checking (1.4K views) - Political figure's historical claims debunked
- Essequibo dispute (236 views but 41.5% retention) - Colonial border + current crisis

**Audience:**
- Males 25-44
- International (UK, Germany, Canada, US)
- Interested in: Geopolitics, colonial history, border disputes, myth-busting

**Formula That Works:**
- Modern political/cultural relevance
- Primary source evidence
- "Colonial decisions still causing deaths/conflicts" angle
- Academic rigor, not punditry

## Output Location

Save your research to: `video-projects/topic-research-[date]/01-trend-research.md`

Create the directory if it doesn't exist.
