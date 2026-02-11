# NotebookLM Research Prompts

**Purpose:** Copy-paste-ready prompts for efficient academic research in NotebookLM during the research phase (building VERIFIED-RESEARCH.md).

**Companion tool:** `python tools/citation_extractor.py` — parses NotebookLM output into VERIFIED-RESEARCH.md format.

**Related file:** `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` — Use these after research is complete, during scriptwriting phase.

---

## How to Use This Document

1. Upload academic sources to NotebookLM (see `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`)
2. Copy the relevant prompt below and paste into NotebookLM chat
3. Replace [BRACKETED] placeholders with your specifics
4. Copy NotebookLM's response to a `.txt` file
5. Run `python tools/citation_extractor.py response.txt` to extract structured citations
6. Review extractions and copy verified claims to `01-VERIFIED-RESEARCH.md`

**Tip:** When using these prompts, always ask NotebookLM to include citation markers [1], [2] in its response. This makes the output compatible with the citation extractor tool.

---

## Core Research Prompts

### Prompt 1: Claim Verification

**When to use:** You have specific claims from preliminary research (Wikipedia, news articles, other videos) that need academic verification.

**Prompt:**
```
I need to verify the following claims about [TOPIC] using the sources you have access to:

CLAIM 1: [First claim to verify]
CLAIM 2: [Second claim to verify]
CLAIM 3: [Third claim to verify]

For each claim, provide:
1. VERDICT: VERIFIED / INACCURATE / PARTIALLY TRUE / NO EVIDENCE FOUND
2. EXACT QUOTE from source with page number
3. NUANCE: What context or complexity does the source add?
4. COUNTER-EVIDENCE: What do other sources say that contradicts or complicates this?

Use [1], [2] citation markers in your response and include a SOURCES section at the end with:
1. Author, "Title", p. XX
```

**Example usage:**
- Verifying specific statistics (population numbers, dates, percentages)
- Checking claims made in competitor YouTube videos
- Cross-checking information from Wikipedia against academic sources

---

### Prompt 2: Quote Extraction (for On-Screen Display)

**When to use:** You need punchy, authoritative quotes to display on screen during the video.

**Prompt:**
```
I need quotable excerpts from the uploaded sources about [SPECIFIC TOPIC/ASPECT].

Requirements for each quote:
- Under 30 words (fits on screen)
- Self-contained (makes sense without context)
- Authoritative (clearly from expert analysis)
- Visually presentable (no dense academic jargon)

For each quote provide:
1. The exact quote word-for-word
2. Author name and credential
3. Book title and page number
4. Brief context: what point does this support?

Find 5-7 quotes that support the argument that [YOUR ARGUMENT].

Include [1], [2] citation markers and a SOURCES section at the end.
```

**Example usage:**
- Finding dramatic quotes about historical events
- Extracting statistical claims with credibility markers
- Getting expert assessments suitable for overlay text

---

### Prompt 3: Counter-Evidence Discovery

**When to use:** You want to strengthen your argument by acknowledging and addressing opposing viewpoints (Alex O'Connor intellectual honesty style).

**Prompt:**
```
I'm arguing that [YOUR MAIN ARGUMENT].

Help me steelman the opposing view:

1. What is the STRONGEST counter-argument found in these sources?
2. What evidence supports that counter-argument?
3. What does the opposing side get RIGHT that I should acknowledge?
4. What are the legitimate concerns or valid points they raise?
5. How do historians who disagree with my position explain the same evidence?

For each counter-argument, provide:
- The argument in its strongest form
- Who makes this argument (scholar name)
- What evidence they cite
- Page numbers for all claims

Use [1], [2] citation markers and include a SOURCES section.
```

**Example usage:**
- Finding legitimate historical debates where multiple interpretations exist
- Identifying nuanced disagreements among scholars
- Strengthening your video by acknowledging complexity

---

### Prompt 4: Timeline Reconstruction

**When to use:** You need a chronological sequence of events with academic citations for each date.

**Prompt:**
```
Using the uploaded sources, create a chronological timeline of [EVENT/TOPIC] from [START DATE] to [END DATE].

For each timeline entry, provide:
1. EXACT DATE (or "circa [date]" if approximate)
2. WHAT HAPPENED (one sentence)
3. PRIMARY SOURCE (if mentioned in the uploaded academic works)
4. CITATION: [Author, Book, p. XX]

Format each entry like this:
- [DATE]: [Event description] [1]

Include a SOURCES section at the end with:
1. Author, "Title", p. XX

Focus on events that are:
- Directly relevant to [YOUR VIDEO TOPIC]
- Have clear documentation
- Include causal connections (how one event led to another)
```

**Example usage:**
- Building a treaty negotiation timeline
- Tracking a territorial dispute from origin to present
- Establishing sequence of events in a historical controversy

---

### Prompt 5: Cross-Source Synthesis

**When to use:** You have multiple sources uploaded and want to compare what they say about the same event or claim.

**Prompt:**
```
Compare what all uploaded sources say about [SPECIFIC EVENT/CLAIM/QUESTION].

Create a table with:
- Column 1: Author name
- Column 2: What they say (quote or paraphrase)
- Column 3: Page number
- Column 4: Their interpretation/emphasis

Then answer:
1. Where do sources AGREE unanimously?
2. Where do sources DISAGREE?
3. What does each source emphasize that others don't?
4. Are disagreements about FACTS or INTERPRETATION?
5. What is the MODERN CONSENSUS (sources from 2010-present)?

Use [1], [2] citation markers for all claims and include a SOURCES section at the end.
```

**Example usage:**
- Comparing competing historical interpretations
- Identifying the mainstream vs. fringe views
- Finding where scholarly consensus has shifted over time

---

## Video-Type Specialized Prompts

### Territorial Disputes

**When to use:** Researching border conflicts, treaty disputes, maritime boundaries, or territorial claims.

**Prompt:**
```
I'm researching the territorial dispute over [LOCATION/REGION].

Extract from the uploaded sources:

**LEGAL BASIS:**
1. What treaties define the borders? (exact treaty name, article number, date)
2. What is the specific boundary description? (geographic coordinates, natural features, legal language)
3. What legal principles apply? (uti possidetis, terra nullius, prescription, etc.)

**HISTORICAL CLAIMS:**
1. What is [COUNTRY A]'s historical claim? (with page numbers)
2. What is [COUNTRY B]'s historical claim? (with page numbers)
3. What does neutral scholarship say about each claim's validity?

**CURRENT STATUS:**
1. Who exercises de facto control?
2. What is the legal status (disputed, occupied, administered by, etc.)?
3. Are there active ICJ cases or arbitration proceedings?

**MODERN CONSEQUENCES:**
1. Economic stakes (resources, trade routes)
2. Deaths or conflicts caused by this dispute in last 20 years
3. Diplomatic incidents

For every factual claim, include [1], [2] citation markers and page numbers. Include a SOURCES section at the end.
```

**Example videos this applies to:** Belize-Guatemala, Bir Tawil, Essequibo, any colonial border dispute

---

### Ideological Myths

**When to use:** Debunking historical myths that fuel modern political or religious narratives.

**Prompt:**
```
I'm debunking the myth that [MYTH STATEMENT].

Help me build the evidence-based counter-narrative:

**MYTH ORIGINS:**
1. When did this myth first appear in popular discourse?
2. Who popularized it? (specific books, films, speeches)
3. What psychological or political need does this myth serve?

**MANUSCRIPT/ARTIFACT EVIDENCE:**
1. What primary sources from the period contradict the myth?
2. What do archaeological findings show?
3. Are there specific manuscripts, letters, or documents I can show on screen?

**SCHOLARLY CONSENSUS:**
1. What do historians specializing in this period say? (quotes with page numbers)
2. Has the consensus changed over time?
3. Are there any serious scholars who still support the myth?

**MODERN IMPACT:**
1. How does this myth shape current political/religious debates?
2. Who invokes this myth today and for what purpose?
3. What are the consequences of believing this myth?

Use [1], [2] citation markers for all claims. Include a SOURCES section at the end with page numbers.
```

**Example videos this applies to:** Library of Alexandria, Dark Ages, Crusades were defensive, Western civilization narratives

---

### Fact-Check Videos

**When to use:** Verifying specific claims made by a political figure, commentator, or in another video.

**Prompt:**
```
I'm fact-checking claims made by [PERSON] about [TOPIC] in [SOURCE - video, interview, speech].

Here are the specific claims that need verification:

CLAIM 1: "[Exact quote from target]"
CLAIM 2: "[Exact quote from target]"
CLAIM 3: "[Exact quote from target]"

For each claim, provide:

1. VERDICT: TRUE / FALSE / MISLEADING / LACKS CONTEXT / UNVERIFIABLE
2. EVIDENCE: What do the uploaded academic sources say?
3. EXACT QUOTE from source with page number
4. CONTEXT: What context makes this claim true/false/misleading?
5. CORRECTION: If false or misleading, what is the accurate version?

If the claim is UNVERIFIABLE (no academic source addresses it), note that clearly.

Use [1], [2] citation markers. Include a SOURCES section at the end.
```

**Example videos this applies to:** Nick Fuentes fact-check, JD Vance fact-check, political figure claims about history

---

## Audio Overview Prompts

### Customized Audio Overview Instructions

**When to use:** Before generating a NotebookLM Audio Overview, use the "Customize" button and paste this template.

**Prompt for the Customize field:**
```
Create a podcast focusing on:

1. SURPRISING FINDINGS: What in these sources contradicts popular belief about [TOPIC]?
2. SCHOLARLY DEBATES: Where do the uploaded sources disagree with each other?
3. PRIMARY SOURCE HIGHLIGHTS: What specific documents, manuscripts, or artifacts are mentioned that would work well as on-screen evidence?
4. MODERN RELEVANCE: How do these historical events/patterns connect to [MODERN SITUATION]?
5. METHODOLOGY: How do historians know what they know? What evidence do they rely on?

Emphasize:
- Specific page numbers for key claims (I'll need to cite these)
- Direct quotes suitable for video overlay text (under 30 words)
- Causal mechanisms (not just "what happened" but "why it happened")

De-emphasize:
- Biographical background of authors (I need content, not credentials)
- Overly broad summaries (I want specifics)
```

---

### Interactive Mode Follow-Up Questions

**When to use:** After listening to an Audio Overview in Interactive Mode, ask these follow-up questions to drill deeper.

**Clarification questions:**
```
1. You mentioned [CLAIM]. What page is that on, and what's the exact quote?
2. The sources disagree about [POINT]. Can you walk me through what each author says specifically?
3. When you said [VAGUE TERM], what does that mean in concrete terms? (e.g., "declined" = by how much? "conflict" = how many deaths?)
4. Is there a primary source document mentioned that shows [EVIDENCE]?
5. One of you said [SURPRISING CLAIM]. Is that from a single source or multiple? Which source is most authoritative on this?
```

**Evidence-gathering questions:**
```
1. What's the best quote about [TOPIC] that's under 30 words and works on screen?
2. Are there any statistics in the sources about [METRIC]? (population, deaths, economic impact)
3. Which source has the strongest counter-argument to my position?
4. What specific document, treaty, letter, or manuscript should I show on screen as evidence?
5. If I could only cite 3 pieces of evidence for [CLAIM], which would be strongest?
```

---

## Output Format Guide

### Making Output Extractor-Compatible

To ensure NotebookLM responses can be parsed by `citation_extractor.py`, always include this instruction in your prompt:

**Add to the end of any prompt:**
```
Use [1], [2], [3] citation markers in your response wherever you reference a source. At the end, include a SOURCES section formatted like:

SOURCES:
1. Author, "Book Title", p. XX
2. Author, "Book Title", p. XX
```

**Why this matters:** The citation extractor tool looks for `[N]` markers in the text and matches them to a SOURCES section. This format allows automatic extraction into VERIFIED-RESEARCH.md format.

---

### Example NotebookLM Output (Extractor-Compatible)

**Input prompt:** "What do the sources say about literacy rates in Roman vs. Medieval Europe? Include [N] citation markers and a SOURCES section."

**NotebookLM response:**
```
Roman literacy rates were approximately 10-15% of the population [1]. This estimate is based on analysis of inscriptions, graffiti, and documentary evidence from Pompeii and other sites. In Early Medieval Europe (500-800 CE), literacy rates dropped to around 1-5% [2]. The decline was particularly severe outside monastic communities, where literacy was preserved through manuscript copying [2].

However, Wickham notes that this comparison can be misleading, as Roman "literacy" often meant basic reading ability, while Medieval literacy meant Latin fluency [2]. The nature of literacy changed, not just the rates.

SOURCES:
1. Harris, William V. "Ancient Literacy" (1989), p. 22
2. Wickham, Chris. "The Inheritance of Rome" (2009), p. 147
```

**After running `python tools/citation_extractor.py response.txt`, you get:**

```markdown
### Claim 1
**Claim:** Roman literacy rates were approximately 10-15% of the population
**Source:** Harris, William V, Ancient Literacy, p. 22
**Status:** NEEDS REVIEW

### Claim 2
**Claim:** In Early Medieval Europe (500-800 CE), literacy rates dropped to around 1-5%
**Source:** Wickham, Chris, The Inheritance of Rome, p. 147
**Status:** NEEDS REVIEW
```

Now you can verify each claim against the actual source and copy verified claims to `01-VERIFIED-RESEARCH.md`.

---

## Related Resources

**Source quality standards:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`
**Scriptwriting phase prompts:** `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md`
**Citation extraction tool:** `python tools/citation_extractor.py --help`
**Workflow documentation:** `VERIFIED-WORKFLOW-QUICK-REFERENCE.md`

---

*Created: 2026-02-11*
*Integration: Phase 34 NotebookLM Research Bridge*
