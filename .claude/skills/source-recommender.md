# Source Recommender Skill - History vs Hype

Recommend authoritative books and academic articles worth purchasing for NotebookLM upload. Prioritize "standard works" - the definitive scholarship that other academics cite.

## When to Use

- User runs `/suggest-sources` command
- Part of `/create-video` workflow at Stage 3
- After deep research shows topic is viable

## Your Task

Research and recommend 20-30 sources (up to 40-50 if all essential) that provide comprehensive academic coverage of the topic. No filler - quality over quantity.

## Step 1: Get Context

You should have access to the deep research report. If not, ask:
1. **Topic:** What are we researching?
2. **Research gaps:** What questions need answers?
3. **Key scholars:** Who did preliminary research identify?

## Step 2: Source Research Strategy

### Identify "Standard Works" First

**What makes a "standard work":**
- Cited 100+ times in Google Scholar
- Published by university press (Oxford, Cambridge, Harvard, Yale, etc.)
- Author is leading scholar in the field
- Considered foundational/definitive by other academics
- Multiple editions (shows lasting relevance)
- Assigned in graduate courses on the topic

**How to find them:**
- Google Scholar: "[topic]" + sort by citations
- Wikipedia bibliography section (check citations on key claims)
- Academic reviews: "essential reading on [topic]"
- University syllabi: "[topic] graduate seminar syllabus"
- Prize winners: Check Pulitzer, Bancroft Prize, etc.

### Source Categories to Cover

Aim for balanced coverage across:

1. **Monographs (8-12 sources):** Comprehensive single-topic books
2. **Primary Source Collections (3-5):** Edited document volumes, treaty collections
3. **Academic Articles (5-10):** Peer-reviewed journal articles on specific aspects
4. **Contemporary Analysis (2-4):** Recent books/articles on modern implications
5. **Counter-Perspective (2-3):** Works defending the myth or offering alternative view
6. **Historical Context (2-4):** Background on the era/region

## Step 3: Research Each Category

### Monographs Research

**Search patterns:**
- Google Scholar: "[topic] definitive history"
- Amazon: "[topic]" + filter by university press + check "customers also bought"
- WorldCat: "[topic]" + filter by "most held by libraries" (shows standard works)
- Academic reviews: "[book title] review" (check reception)

**For each candidate monograph:**
- Check Google Scholar citation count
- Read preview pages (Google Books, Amazon)
- Check author credentials (university affiliation, other works)
- Look for reviews in academic journals
- Verify it addresses your research gaps

### Primary Source Collections

**Search patterns:**
- "[Topic] primary sources"
- "[Topic] documents and correspondence"
- "[Treaty name] text"
- "[Era] diplomatic correspondence [region]"
- University press + "documents" + topic

**Priority:**
- Collections that include the exact treaties/documents you need
- Scholarly editions with annotations
- Multiple perspectives (both sides of dispute, etc.)

### Academic Articles

**Search patterns:**
- Google Scholar: "[specific claim]" + "historical analysis"
- JSTOR: "[topic]" (note for purchase)
- Project MUSE: "[topic]"
- Cambridge Core, Oxford Academic

**Select articles that:**
- Address specific research gaps from deep research
- Offer recent reassessments (last 10 years)
- Provide statistical/quantitative analysis
- Challenge conventional narratives

### Contemporary Analysis

**Find books/articles on:**
- Modern political uses of this history
- Current policy debates involving this history
- Recent news analysis connecting past to present
- Academic takes on why this myth persists

### Counter-Perspective Sources

**Deliberately include:**
- Best scholarly defense of the conventional narrative
- Works from the "other side" of the dispute
- Historical apologists' strongest arguments
- Contemporary defenders of the myth

**Why:** Video must acknowledge strongest counter-evidence. Academic balance.

## Step 4: Cost Research

For each recommended source, find:

**Books:**
- Kindle/ebook price (fastest access)
- Used hardcover price (if ebook unavailable)
- New paperback price
- Library availability (WorldCat "find in library")

**Articles:**
- Individual purchase price (JSTOR, publisher)
- Included in any free access programs
- Available via ResearchGate/Academia.edu requests

**Tools:**
- Google Books (check ebook availability + price)
- Amazon (Kindle + used prices)
- AbeBooks (used academic books)
- JSTOR (individual article purchase)
- WorldCat (library availability)

## Step 5: Generate Recommendation Report

```markdown
# SOURCE RECOMMENDATIONS: [Topic]

**Topic:** [Full description]
**NotebookLM Target:** 20-30 essential sources (up to 50 if all worthwhile)
**Total Estimated Cost:** $[Calculate total]
**Research Date:** [Date]

---

## TIER 1: ESSENTIAL STANDARD WORKS (Must-Have)

These are the foundational scholarly works. Any serious research on this topic requires these.

### 1. [Book Title]
- **Author:** [Name] ([University affiliation / credentials])
- **Publisher:** [University press / academic publisher]
- **Year:** [Publication year] ([Note if multiple editions])
- **Citations:** [Google Scholar count] citations
- **Why Essential:** [What makes this the standard work - e.g., "Most comprehensive analysis of the 1899 arbitration," "Definitive account using declassified archives"]
- **What It Provides:** [Specific research gaps this fills]
- **Cost:** Kindle $[XX] / Used hardcover $[XX] / Library: [Available at X libraries nearby]
- **Access Speed:** [Immediate ebook / 3-5 days shipping / Library hold]
- **Preview:** [Google Books / Amazon link]

### 2. [Book Title]
[Same structure - continue for 5-8 essential monographs]

---

## TIER 2: PRIMARY SOURCE COLLECTIONS (Critical Evidence)

### 1. [Collection Title]
- **Editor:** [Name]
- **Publisher:** [Press]
- **Year:** [Year]
- **Content:** [What documents/treaties included - be specific]
- **Why Needed:** [Which smoking gun evidence is in here]
- **Cost:** $[XX]
- **Alternative:** [Free access to any of these docs online? Note URLs]

### 2. [Collection Title]
[Continue for 3-5 primary source collections]

---

## TIER 3: KEY ACADEMIC ARTICLES (Specific Claims)

### 1. "[Article Title]"
- **Author:** [Name]
- **Journal:** [Journal name], Vol. [X], No. [X] ([Year]), pp. [XX-XX]
- **Focus:** [What specific aspect this covers]
- **Key Finding:** [Main argument/evidence relevant to your video]
- **Why Include:** [What research gap this fills]
- **Cost:** [JSTOR $X / Publisher $X / Available free via ResearchGate]
- **Citations:** [XX citations]

### 2. "[Article Title]"
[Continue for 5-10 articles]

---

## TIER 4: CONTEMPORARY ANALYSIS (Modern Relevance)

### 1. [Book/Article Title]
- **Author:** [Name]
- **Publisher/Journal:** [Source]
- **Year:** [Recent - ideally 2020-2025]
- **Focus:** [Modern political/cultural impact of this myth]
- **Why Needed:** [Strengthens "why this matters in 2025" section]
- **Cost:** $[XX]

### 2. [Title]
[Continue for 2-4 contemporary sources]

---

## TIER 5: COUNTER-PERSPECTIVE (Academic Balance)

### 1. [Book/Article Title]
- **Author:** [Name]
- **Position:** [What counter-argument they make]
- **Why Include:** [Strongest opposing view - must address in video]
- **Scholarly Merit:** [Is this credible scholarship or fringe? Note.]
- **Cost:** $[XX]

### 2. [Title]
[Continue for 2-3 counter-perspective sources]

---

## TIER 6: HISTORICAL CONTEXT (Background)

### 1. [Book Title]
- **Focus:** [Broader context - the era, the region, the political situation]
- **Why Helpful:** [Provides background for understanding the specific topic]
- **Priority:** [Medium - helpful but not critical]
- **Cost:** $[XX]

### 2. [Title]
[Continue for 2-4 context sources]

---

## COST SUMMARY

| Category | Sources | Est. Cost |
|----------|---------|-----------|
| Essential Standard Works | [X] | $[XXX] |
| Primary Source Collections | [X] | $[XXX] |
| Academic Articles | [X] | $[XX] |
| Contemporary Analysis | [X] | $[XX] |
| Counter-Perspective | [X] | $[XX] |
| Historical Context | [X] | $[XX] |
| **TOTAL** | **[XX]** | **$[XXX]** |

**Cost-Saving Options:**
- [X] sources available free via library
- [X] sources available as cheaper ebooks vs. hardcover
- [X] articles might be available via ResearchGate requests (free)
- Used books could save $[XX]

**Minimum Viable Source Set (Budget Option):**
If budget is tight, prioritize these [10-12] sources: [List specific titles]
Estimated cost: $[XX]

---

## ACQUISITION PRIORITY

### Order These First (Critical Path):
1. [Source] - [Why: "Contains the treaty text" or "Only source on X"]
2. [Source] - [Why]
3. [Source] - [Why]

[Priority = sources that fill biggest research gaps or contain unique primary documents]

### Order These Second (Important Supporting):
4. [Source]
5. [Source]
[Continue...]

### Order These Last (Nice-to-Have):
[Sources that add depth but aren't critical]

---

## LIBRARY ALTERNATIVES

**Check These Libraries:**
- [Local university library] - Has [X] of these sources
- [Public library system] - Has [X] of these sources
- [Specialized library] - [If applicable - law library, historical society, etc.]

**Interlibrary Loan Candidates:**
[List sources that are expensive but might be available via ILL]

---

## DIGITAL ACCESS NOTES

**Immediate Access (Ebooks Available):**
- [List sources with instant Kindle/ebook access]

**3-5 Day Shipping:**
- [List print-only sources]

**Special Access:**
- [Any sources requiring special requests, archival visits, etc.]

---

## SOURCE QUALITY VERIFICATION

**Cross-Reference Check:**
How many of these sources cite each other?
[This shows they're part of the scholarly conversation - good sign]

**Author Credentials:**
All recommended authors:
- [X] are tenured professors at research universities
- [X] are subject matter experts (not generalists)
- [X] have published multiple peer-reviewed works on this topic

**Publication Quality:**
- [X] published by university presses
- [X] published in top-tier journals
- [X] peer-reviewed

**Citation Impact:**
- Average citation count: [XXX]
- Most cited source: [Title] with [XXX] citations

---

## RESEARCH GAPS AFTER THESE SOURCES

Even with all recommended sources, we might still lack:
- [Gap 1 - e.g., "Specific archival documents only available at X archive"]
- [Gap 2]
- [Gap 3]

**Mitigation:**
[How to handle these gaps - acknowledge in video, use secondary sources, etc.]

---

## NOTEBOOKLM UPLOAD STRATEGY

**Total Sources:** [XX]
**NotebookLM Limit:** 50 sources, 25M words

**Upload Priority:**
1. **Phase 1 (Essential - upload first):** [10-12 sources]
2. **Phase 2 (Important - add next):** [8-10 sources]
3. **Phase 3 (If space allows):** [Remaining sources]

**Format Notes:**
- Ebooks: Convert to PDF if needed
- Articles: Direct PDF upload
- Large books: Consider uploading specific chapters vs. full book (save space)

---

## ALTERNATIVE SOURCES CONSIDERED BUT NOT RECOMMENDED

### [Title]
**Why Not:** [Outdated / Fringe scholarship / Superseded by better work / Too general]

### [Title]
**Why Not:** [Reason]

[Continue - shows you did thorough research and made deliberate choices]

---

## NEXT STEPS

1. **Review recommendations** - Any sources you already own? Any you want to skip?
2. **Acquire sources** - Purchase, borrow, or request
3. **Upload to NotebookLM** - Follow upload priority
4. **Run `/notebooklm-prompts`** - Get customized research prompts for these specific sources

---

**Recommendation Confidence:** [High/Medium] - [Why]
**Estimated Research Strength After Upload:** [Scale of 1-10]
```

## Quality Standards

### Good Recommendations:
- Every source serves a specific purpose (no padding)
- Mix of breadth (standard works) + depth (articles on specifics)
- Counter-perspectives included (academic balance)
- Costs researched and noted
- Priority/sequencing thought through

### Red Flags in Your Own Work:
- Recommending sources you haven't verified exist
- Generic "this looks good" without checking citations/credentials
- All sources from one perspective (confirmation bias)
- Recommending 50 sources when 25 would suffice (filler)
- No cost research (user needs to budget)

## Research Tools

**Use these to find and verify sources:**
- Google Scholar (citation counts, related works)
- WorldCat (library holdings, editions)
- Google Books (previews, tables of contents)
- Amazon (prices, reviews, "customers also bought")
- JSTOR (article access and pricing)
- Publisher websites (check for free sample chapters)

## Output Location

Save recommendation report to: `video-projects/[topic-slug]/03-source-recommendations.md`

## After Completion

Ask user:
1. Does this source list look comprehensive?
2. Any sources you already have that I should note?
3. What's your budget comfort level - full list or minimum viable set?
4. Ready to start acquiring sources?
5. Want me to generate NotebookLM prompts while you source hunt?
