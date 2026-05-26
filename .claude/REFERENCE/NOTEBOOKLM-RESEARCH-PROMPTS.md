# NotebookLM Research Prompts

**Purpose:** Copy-paste-ready prompts for efficient academic research in NotebookLM during the research phase (building VERIFIED-RESEARCH.md).

**Updated:** 2026-03-28 — Citation format upgraded (now includes publisher, year, translator). Added Physical Document Description prompt (Rule 31) and Diamond Chain prompt (Rule 29).

**Companion tool:** `python tools/citation_extractor.py` — parses NotebookLM output into VERIFIED-RESEARCH.md format.

**Related file:** `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` — Use these after research is complete, during scriptwriting phase.

**Citation format standard:** Every prompt in this file asks NLM to return citations as:
`Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]`
This prevents the downstream citation gaps (missing publishers, missing translators) identified in the 2026-03-28 audit.

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

Use [1], [2] citation markers in your response and include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
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

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
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

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
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

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example usage:**
- Comparing competing historical interpretations
- Identifying the mainstream vs. fringe views
- Finding where scholarly consensus has shifted over time

---

## Angle-Discovery Prompts (P11.2)

**Purpose:** Run during `--apply-review` after the Mechanism-Word Lock Gate (P11.1b) has LOCKED at least one candidate. These three prompts mine the NLM notebook for script-stage angle candidates — hook quotes, thesis verbs, closing payoffs — so the script writer has specificity-grounded material to choose from rather than improvising.

**Trigger:** Run via `/research --apply-review` once per ingestion pass that adds claims. Output replaces the `## CANDIDATE ANGLES` section in `01-VERIFIED-RESEARCH.md` (OVERWRITE, not append).

**Placeholders in all three prompts:**
- `[TOPIC]` — the video topic (e.g., "Ottoman Empire hijab regulations")
- `[LOCKED_MECHANISM_WORD]` — the mechanism word confirmed LOCK in `RESEARCH-VIABILITY.md` (e.g., "systematized")
- `[NOTEBOOK_ID]` — the NLM project notebook ID

**Citation format:** All three prompts use `[1], [2]` markers, compatible with `tools/citation_extractor.py`.

---

### Prompt AD-1: Candidate Hook Quotes (Specificity-Ranked)

**When to use:** After mechanism-word lock. Surfaces the top 5 most specific, surprising, anchor-able quotes from the notebook. Input to `script-writer-v2` Rule 17 (hook anchoring) and Rule 32I (stageable scene).

**Prompt:**
```
I'm building a video about [TOPIC]. My locked mechanism word is "[LOCKED_MECHANISM_WORD]".

From the uploaded sources, find the top 5 most SPECIFIC, SURPRISING, and ANCHOR-ABLE quotes that could open the video. Each candidate quote must contain:
- ≥1 named person (a historical actor, official, scholar, or institution)
- ≥1 named document, date, or event (something concrete and verifiable)
- ≥1 concrete fact (a number, a ruling, a physical description, a consequence)

For each quote, provide:
1. The exact quote, word-for-word
2. Author, book, page number
3. T-tier: [T1 = primary document / T2 = scholar citing primary / T3 = scholar interpretation only]
4. Specificity score 0–100 (higher = more named persons + documents + facts per 30 words)
5. One sentence: why would a viewer in the first 60 seconds find this surprising?

Rank by specificity score, highest first. Use [1], [2] citation markers. Include SOURCES section:
1. Author Last, First. "Full Title." Publisher, Year. p. XX.
```

**Ranking criteria (deterministic):** Named persons count +20 each; named documents/dates count +15 each; concrete facts (numbers, rulings, measurements) count +10 each; maximum 100. T1 sources get +10 bonus; T3-only get −10 penalty.

**Worked example (Tripoli #51):** Query on Treaty of Tripoli / Article 11 surfaced: *"The government of the United States of America is not in any sense founded on the Christian Religion"* — John Adams, Senate ratification 1797, Treaty text Article 11 (T1, Score 92). That quote became the video's opening anchor because it names the president, the document, and delivers a concrete constitutional claim in under 20 words.

---

### Prompt AD-2: Candidate Thesis Verbs

**When to use:** After mechanism-word lock. Surfaces the top 3 verbs describing what historical actors actually did — raw material for the throughline's action verb (per `THESIS-DISCIPLINE.md` Step 3). The thesis verb may be the locked mechanism word itself or a variant with stronger source grounding.

**Prompt:**
```
I'm building a video about [TOPIC]. My locked mechanism word is "[LOCKED_MECHANISM_WORD]".

From the uploaded sources, identify the top 3 verbs that describe what the HISTORICAL ACTORS in this topic actually DID — not what happened to them, but what they chose to do. These are the action verbs for a throughline: "[Subject] [verb] [object] by [mechanism]."

For each verb candidate, provide:
1. The verb (one word or short phrase)
2. A quote from the sources that shows historical actors performing this action
3. Author, book, page number
4. NLM confidence that this verb is grounded in primary sources: HIGH / MEDIUM / LOW
5. A draft 12-word-or-fewer throughline using this verb: "[Subject] [verb] [object] by [mechanism]."

Is "[LOCKED_MECHANISM_WORD]" itself a viable thesis verb? If yes, provide the same evidence. If no, explain why not and suggest the strongest alternative.

Use [1], [2] citation markers. Include SOURCES section:
1. Author Last, First. "Full Title." Publisher, Year. p. XX.
```

**Ranking criteria:** HIGH confidence = verb sourced to primary document in notebook + scholar confirmation; MEDIUM = scholar-attributed only; LOW = inferred from context. Rank HIGH first, then by throughline sharpness.

**Worked example (Inquisition #54):** Mechanism word was "standardized." AD-2 surfaced three verbs: *standardized* (HIGH — Lea's Inquisition manual structure), *bureaucratized* (HIGH — the 1484 Manuale de Inquisitoribus), *formalized* (MEDIUM — secondary synthesis only). Throughline became: "The Inquisition standardized persecution — not because of fanaticism, but because of paperwork."

---

### Prompt AD-3: Candidate Closing Payoffs

**When to use:** After mechanism-word lock. Surfaces the top 3 most surprising or anchoring facts that could carry the script's closing beat. Input to `script-writer-v2` Rule 32G (closer specificity) and the "modern relevance every 90s" discipline.

**Prompt:**
```
I'm building a video about [TOPIC]. My locked mechanism word is "[LOCKED_MECHANISM_WORD]".

From the uploaded sources, find the top 3 facts that are:
- SURPRISING: counter-intuitive, or contradicts what viewers expect based on the topic's pop-history version
- CONCRETE: specific numbers, named outcomes, verifiable events — not general observations
- MEMORABLE: the fact a viewer would repeat to a friend the next day

For each closing payoff candidate, provide:
1. The fact, stated precisely
2. Author, book, page number
3. T-tier: [T1 / T2 / T3]
4. Why it's surprising (one sentence: what does the viewer expect instead?)
5. A draft closing phrasing (1–2 sentences, spoken delivery, past-tense declarative)

Rank by SURPRISE × CONCRETENESS × MEMORABILITY (qualitative assessment, highest first).

Use [1], [2] citation markers. Include SOURCES section:
1. Author Last, First. "Full Title." Publisher, Year. p. XX.
```

**Ranking criteria:** Surprise assessed against "what a viewer who watched 3 competitor videos on this topic would assume." Concreteness requires at least one named person, date, or number. Memorability = can it be repeated in a single sentence?

**Worked example (Tripoli #51):** AD-3 surfaced: The Senate's ratification of Article 11 — which explicitly stated the US was not a Christian nation — passed unanimously and without debate in 1797. That became the closing payoff: *"The Senate voted unanimously. Not a single objection. The treaty was the law."* T1 source, Score: Surprise 9/10, Concrete 8/10, Memorable 9/10.

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

For every factual claim, use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
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

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
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

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example videos this applies to:** Nick Fuentes fact-check, JD Vance fact-check, political figure claims about history

---

### Physical Document Description (Rule 31 — Artifact as Witness)

**When to use:** Your video will show primary documents on screen. You need to know what they look like physically — not just what they say.

**Prompt:**
```
I need physical descriptions of key documents for on-screen presentation. For each document below, tell me anything the sources say about its physical form, appearance, or material properties:

[LIST YOUR DOCUMENTS, e.g.:]
1. [TREATY/LAW NAME]: Is the original extant? Where is it held? Is it handwritten or printed? Does it bear marks, seals, signatures? What language is it written in? What size/format?
2. [COURT RULING]: How long is it? How is it structured? Are there accompanying maps or annexes?
3. [LETTER/DECREE]: Who wrote it? Is it a draft with annotations, or a final clean copy?

For each:
- Physical description (size, material, condition, language, script)
- Where the original is held (archive, court, museum, library)
- Whether images are publicly available (digitized archives, museum collections)
- Any physical detail that makes the document feel REAL (X marks from illiterate signatories, margin annotations, damage, wax seals, crossed-out text)

This is for visual storytelling — I need to describe documents before reading them. The viewer should SEE the artifact before hearing what it says.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example usage:**
- Territorial videos: treaties, maps referenced in ICJ cases, boundary commission reports
- Untranslated Evidence series: the original-language document (what does the Vichy Statute look like? The Code Noir?)
- Colonial topics: letters, decrees, administrative orders with visible signatures

**Why this matters:** Script-writer Rule 31 (Artifact as Witness) requires describing documents physically BEFORE explaining their meaning. NLM can surface physical details from academic sources that describe manuscripts, archival holdings, or document provenance. Without this prompt, you default to "the treaty says..." (lecture mode) instead of "the treaty is a two-page handwritten document bearing the X marks of six chiefs who could not write their names" (prosecutor mode).

---

### Diamond Chain — Push to Ultimate Causes (Rule 29)

**When to use:** After verifying the factual claims, push the causal explanation deeper. Why did this specific outcome happen? Not just the event, but the institutional and geographic/structural causes.

**Prompt:**
```
I need to build a three-level causal chain explaining WHY [OUTCOME] happened:

LEVEL 1 (Event): [What happened — the surface-level story]

LEVEL 2 (Institution): What INSTITUTIONAL factors made this outcome likely?
- What legal frameworks, bureaucratic structures, or political systems shaped the decision?
- What institutional incentives existed? Who benefited from the outcome?
- Were there institutional failures (corruption, negligence, conflicting mandates)?

LEVEL 3 (Geography/Biology/Independent Variables): What STRUCTURAL factors that humans did NOT choose explain this?
- Geographic factors: resources, location, access routes, climate, natural boundaries
- Demographic factors: population distribution, ethnic geography, migration patterns
- Economic factors: trade routes, resource deposits, labor markets
- Path dependency: what earlier events (pre-dating the institutions) locked in this trajectory?

For each level, provide:
1. The causal factor
2. Academic evidence with page numbers
3. How this level CAUSED the level above it (the causal mechanism)

Stop when you reach factors that are genuinely independent of human decisions — geography, biology, or deep structural constraints. That is Level 3.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example usage:**
- Bakassi: Event (ICJ ruling) → Institution (uti possidetis juris + colonial treaty system) → Geography (Gulf of Guinea oil proximity + river-based boundary drawing)
- Partition of India: Event (Radcliffe Line) → Institution (5-week timeline + commission deadlock) → Geography (Punjab's Sutlej river + canal headworks placement)
- Code Noir: Event (60-article slave code) → Institution (French colonial plantation economy + Catholic Church monopoly) → Geography (Caribbean sugar economics + distance from metropolitan oversight)

**Why this matters:** Script-writer Rule 29 requires at least one causal chain reaching Level 3 in scripts over 8 minutes. NLM can surface the geographic, demographic, and structural factors that academic sources discuss but that internet research typically misses. Viewers who watch for "mechanisms" (the channel's core audience) expect this depth.

---

### Mechanism Mapping — Macro/Micro/Stress-Test (Rule 29 expansion)

**When to use:** Your topic is about HOW a system works or fails. You need to extract the system's structure at three levels for the scriptwriter's Macro → Micro → Stress-Test pattern.

**Prompt:**
```
I'm building a video explaining HOW [SYSTEM/INSTITUTION/PROCESS] works (or failed). I need to map the system at three levels of detail:

**MACRO — The overarching design:**
1. What is this system supposed to do? What problem was it designed to solve?
2. What are the core assumptions it was built on? (e.g., "local governments will request resources" / "communication lines will stay open")
3. Who designed it, and what constraints were they working within?
4. What is the common public assumption about how it works that is WRONG? (This becomes my hook.)

**MICRO — The specific components:**
1. Name every specific asset, unit, document, clause, or piece of infrastructure the sources mention.
2. I need EXACT quantities: how many vehicles, how much water, how many personnel, what dollar amounts.
3. What are the named components? (Vehicle names, unit designations, treaty article numbers, specific locations)
4. What proper nouns and specific nomenclature do the sources use?

**STRESS-TEST — What broke it (or made it work):**
1. What was the variable the designers did NOT account for?
2. At what specific moment did the system encounter its breaking/proving point?
3. What was the cascade of failures/successes? (First A failed, which meant B couldn't work, which caused C...)
4. What was the human cost of the failure, or the human benefit of the success?

For each level, give EXACT quotes with page numbers. I need the specific data — not summaries.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example usage:**
- How FEMA's disaster relief system failed during Katrina (Macro: federalist pull system. Micro: MERS units, "Red October," 550K liters. Stress-Test: communication collapse)
- How the Berlin Conference divided Africa (Macro: uti possidetis juris. Micro: specific river-based boundaries, named surveyors. Stress-Test: arbitrary lines vs. ethnic geography)
- How the Panama Canal lock system works (Macro: gravity-fed elevation change. Micro: lock dimensions, water volume per transit. Stress-Test: Panamax vs. Neo-Panamax vessel limits)

**Why this matters:** Script-writer Rule 29 (expanded in v10.4) requires mechanism scripts to follow a Macro → Micro → Stress-Test structure. This prompt extracts exactly the three levels of information the scriptwriter needs. The MICRO level specifically targets the data density (exact quantities, proper nouns) that Wendover uses to carry viewers through technical exposition.

---

### Data Density Extraction — Specific Quantities and Proper Nouns

**When to use:** You have a mechanism/how topic and need the hyper-specific data that proves intellectual competence — exact numbers, named assets, precise measurements. This is the material that fills the "boring middle" of a mechanism explanation.

**Prompt:**
```
I need the most SPECIFIC data points in the uploaded sources about [SYSTEM/TOPIC]. Not summaries — I need granular operational detail.

Extract:
1. **Exact quantities:** Measurements, weights, distances, capacities, populations, dollar amounts, percentages, time durations. Every specific number the sources mention.
2. **Named components:** Specific names of vehicles, units, buildings, ships, treaties, articles, clauses, camps, bases, routes. Every proper noun that is part of the system.
3. **Scale comparisons:** Does any source compare the system's scale to something the reader already knows? (e.g., "enough to cover North America from California to Virginia" / "roughly the size of Belgium")
4. **Operational sequences:** Step-by-step descriptions of how the system physically operates. What happens first, second, third?
5. **Surprising data points:** Which numbers in the sources are counter-intuitive or would surprise a general audience?

Present as a numbered list, grouped by category. Include page numbers for every data point.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Example usage:**
- Extracting FEMA logistics data (275 vehicles, 550K liters water, Camp Bogard staging, "Red October" mobile command)
- Extracting Panama Canal transit data (85-foot elevation, 60,000-ton ships, lock dimensions, water volume)
- Extracting colonial administration data (specific administrators named, district sizes, tax revenues, troop numbers)

**Why this matters:** Wendover Productions keeps viewers engaged during technical exposition through "aggressive data density and hyper-specific nomenclature" — exact quantities and named components that act as implicit sourcing and prove intellectual competence (Wave 5 analysis, 2026-04-05). This prompt extracts the raw material for that technique. The data points feed directly into script-writer Rule 29's Micro level and Rule 47's data presentation rules.

---

## Packaging Intelligence Prompts

**Purpose:** Query a dedicated packaging notebook (competitor titles, views, thumbnail patterns, topic framing) to inform `/greenlight` decisions. These prompts work with a notebook loaded with competitor metadata — see `tools/PACKAGING-NOTEBOOK-GUIDE.md` for setup.

### Prompt P1: Competitive Landscape for a Topic

**When to use:** Before greenlighting a new topic. Part of `/greenlight --full` Step 0B.

**Prompt:**
```
I'm considering making a video about [TOPIC].

From the competitor data in this notebook:
1. Which channels have covered this topic or closely related topics?
2. What ANGLE did each take? (e.g., economic narrative, territorial dispute, myth-busting, document analysis)
3. Which videos on similar topics got the MOST views? What was their title and framing?
4. What angle is NOBODY covering? What's the gap?
5. Based on the data patterns, what title structure tends to perform best for this topic type ([territorial/ideological/colonial/mechanism])?

I need a specific packaging recommendation: what angle + title direction will differentiate from existing coverage AND match proven patterns.
```

---

### Prompt P2: Title Pattern Analysis by Topic Type

**When to use:** When generating titles for a specific topic type. Helps title_scorer recommendations land better.

**Prompt:**
```
Looking at the competitor data for [TOPIC TYPE: territorial / ideological / colonial / mechanism / fact-check] videos:

1. What title patterns appear in the top 20% by views? (list actual titles)
2. What title patterns appear in the bottom 20%? (list actual titles)
3. What WORDS or PHRASES appear repeatedly in high-performing titles for this type?
4. Are there any title structures that work for this type but NOT for others?
5. What's the average word count of top-performing titles for this type?

Give me 3 title FORMULAS (not specific titles) that I can fill in with my topic.
```

---

### Prompt P3: Hook & Framing Intelligence

**When to use:** After choosing a topic but before writing the hook. Informs scriptwriter's hook formula.

**Prompt:**
```
For videos about [TOPIC or TOPIC TYPE]:

1. How do the top-performing videos in this space open their first 60 seconds?
2. What HOOK TYPE do they use? (cold fact, myth contradiction, contextual opening, specificity bomb)
3. What's the common FRAMING? (economic angle, political angle, human cost angle, mechanism angle)
4. What framing do ALL competitors use that we could deliberately AVOID for differentiation?
5. Is there a surprising entry point that none of them use?

I want to find the hook angle that makes a viewer think "I've never seen THIS take before."
```

---

### Prompt P4: Packaging Post-Mortem

**When to use:** After publishing a video, to understand why packaging worked or didn't relative to competitors.

**Prompt:**
```
My video "[TITLE]" about [TOPIC] got [X views / Y% CTR / Z% retention].

Compare against competitor data:
1. How does my title compare to competitor titles on similar topics? What did theirs do differently?
2. Based on the patterns in this notebook, what was likely the strongest/weakest element of my packaging?
3. If I were to re-title this video today, what would the data suggest?
4. What can I learn from this result for future videos on [TOPIC TYPE]?
```

---

### Pre-Filming Script Audit

**When to use:** After script is drafted, before filming. Catches attribution errors, structural contradictions, and pronunciation risks that waste filming time. Run this with the SAME notebook used for research — it has the sources to verify against.

**Prompt:**
```
I have a near-final script for a video about [TOPIC]. I need you to audit it against the uploaded sources before I film. Here is the script structure with key claims:

[PASTE SCRIPT OUTLINE — section by section, with the specific claims in each]

Check three things:

**1. ATTRIBUTION ACCURACY:**
For every "According to X, [statistic]..." in the script — verify that X is the ORIGINATOR of that data, not someone citing it secondhand. If the chain is X cites Y who cites Z, tell me who originated it so I can attribute correctly. Wrong attribution on a primary-source channel is a credibility risk.

**2. CONCURRENT EVENT FRAMING:**
Are there sections that cover the SAME time period from different angles? If so, could they read as contradictions when presented sequentially? Flag any place where the script says "X happened" in one section and "the opposite of X happened" in another without explaining they occurred simultaneously.

**3. PRONUNCIATION RISKS:**
List every foreign name, place name, and technical/Latin term in the script. For each, tell me:
- The standard English pronunciation (phonetic)
- Whether a simpler alternative exists (e.g., "intertemporal law" → "a principle: you judge by the standards of the time")
- Any names the sources spell differently than my script

**4. AD-LIB RISK — FAMOUS QUOTES AND COMMON CLAIMS:**
Based on this topic and the sources in this notebook, what are the most commonly MISQUOTED or MISATTRIBUTED facts that someone might improvise during filming? Specifically:
- Famous quotes associated with this topic — give me the EXACT original wording with source and date, so I don't ad-lib a corrupted version
- Statistics or numbers that are widely repeated but trace to questionable origins
- Common framings that sound right but are historically wrong (e.g., calling someone "Prime Minister at the time" when they held a different title, or when they were dead by that date)

List up to 5 ad-lib traps. For each, give the CORRECT version I should use if I improvise.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**Why this matters:** Four production issues discovered in Bakassi (2026-04-12/16): (1) Ezeilo attributed as source of 73% figure when Omoigui/Baye originated it — caught post-recording. (2) Acts 3 and 4 presented contradictory facts about the same period without bridging — required structural rewrite. (3) "Intertemporal law" caused 8+ recording stumbles — had to be replaced post-recording. (4) Lord Salisbury quote ad-libbed during filming with wrong wording ("white man's foot" → actually "human foot"), wrong context (1890 Heligoland-Zanzibar Treaty, not 1913), and wrong title implication ("PM at the time" — he died 1903, agreement was 1913). Check 4 would have surfaced the correct quote and flagged the attribution trap.

---

### Citation Chain Audit — Primary Source Grounding

**When to use:** MANDATORY before filming. After the fact-check is complete and all claims are marked ✅. This is the gate that catches claims that "look verified" because multiple secondary sources repeat them, but no primary document actually contains the data. Run this with the SAME notebook used for research.

**Why it exists:** In Bakassi (2026-04-16), the claim "73% of voters in Bakassi polling stations chose Cameroon" was marked ✅ in the fact-check, sourced to Ezeilo 2016 and Baye 2010. Both sources traced back to a single personal website (Omoigui 2006) that cited "UN records" without page numbers. The ICJ judgment — the primary source in the notebook — contains zero Bakassi-specific voting data. A counter-source disputes whether voting even occurred on the Peninsula. Three sources repeating one unverified claim is not verification.

**Prompt:**
```
I have a list of factual claims that passed my fact-check for a video about [TOPIC]. Each claim has at least one source citation. But I need to know which claims are ACTUALLY grounded in primary documents versus which ones are secondary sources citing each other.

Here are the claims:

[PASTE EVERY ✅ CLAIM FROM YOUR FACT-CHECK TABLE, numbered, with the source citation]

For EACH claim, answer:

**PRIMARY SOURCE CHECK:**
Can you find this specific fact — this exact number, date, quote, or event — in any of the PRIMARY DOCUMENTS uploaded to this notebook (treaties, court judgments, official records, government documents)?
- If YES: Give me the exact location (document name, paragraph/page number, exact text).
- If NO: Say "NOT FOUND IN PRIMARY SOURCES" and tell me which uploaded source mentions it and whether THAT source cites a primary document for this specific claim.

**CITATION CHAIN:**
Trace the claim backward. Does the secondary source cite another secondary source? Does THAT source cite a primary document? Map the chain:
- Example: "Ezeilo 2016 p. 197 → cites Omoigui 2006 → cites 'UN records' (no page number) → DEAD END"
- Example: "Konings 2005 p. 282 → cites UN Plebiscite Commissioner Report 1961 → PRIMARY SOURCE FOUND"

**VERDICT for each claim:**
- 🟢 GROUNDED: Primary document in this notebook directly contains this data.
- 🟡 TRACEABLE: Secondary source cites a specific primary document with page/paragraph number, but that primary document is not in this notebook. I could verify it if I uploaded it.
- 🔴 UNGROUNDED: Citation chain dead-ends at a source that says "according to..." without specifying where. OR multiple secondary sources all trace back to one origin that doesn't cite a primary document.

Flag every 🔴 claim. These should NOT be stated as fact in the script — they need hedging ("according to [author]") or removal.

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
```

**How to use the results:**
- 🟢 claims: safe to state as fact
- 🟡 claims: safe if you trust the source, but consider uploading the cited primary document for confirmation
- 🔴 claims: either (a) hedge with attribution ("Omoigui claims..."), (b) replace with a grounded alternative, or (c) remove

**Example — what this would have caught in Bakassi:**
- Claim: "73% of voters in Bakassi stations chose Cameroon"
- NLM response: "NOT FOUND IN PRIMARY SOURCES. The ICJ Judgment does not contain Bakassi-specific voting data. Ezeilo 2016 p. 197 → cites Baye 2010 p. 16 → cites Omoigui 2006 → cites 'UN records' (no page) → DEAD END. 🔴 UNGROUNDED."
- Fix: Replace with overall Southern Cameroons result (70.5%) which IS in the UN Plebiscite Commissioner Report.

**Critical rule:** A claim sourced to three secondary authors who all cite the same unverified origin is ONE source, not three. This prompt forces NLM to trace the chain rather than count citations.

---

### Quote Verification — Original Source Confirmation

**When to use:** MANDATORY before filming. After the Citation Chain Audit passes. Run for every quote that will appear ON SCREEN as text overlay or be READ VERBATIM on camera. This catches word substitution, context drift, title inflation, and composite quote errors.

**Why it exists:** The Salisbury quote in Bakassi had three errors because it was taken from secondary sources that had already corrupted it. "White man's foot" (dramatic, racial) replaced "human foot" (original, neutral). The satirical preamble was cut. The quote was about the 1890 Heligoland-Zanzibar Treaty, not the 1913 Anglo-German Agreement. All three errors exist in 28 of 30 publications that cite this quote (Fourie & Lemon, "Colonialism Misquoted").

**Prompt:**
```
I need to verify every quote that will appear ON SCREEN or be READ VERBATIM in my video about [TOPIC]. For each quote below, I need you to find the ORIGINAL SOURCE — not a secondary source quoting it, but the actual document, speech, letter, or ruling where these words first appeared.

QUOTE 1: "[exact words]" — attributed to [person], [context]
QUOTE 2: "[exact words]" — attributed to [person], [context]
[etc.]

For EACH quote:

**1. ORIGINAL SOURCE:**
Can you find this EXACT wording in any uploaded primary document? If yes, give document name, page/paragraph, and confirm the wording matches word-for-word.

**2. WORDING CHECK:**
Does the wording in my script match the original exactly? Flag ANY differences — even single words. Quote corruption often happens one word at a time.

**3. CONTEXT CHECK:**
- When did the person say/write this? (exact date)
- What were they talking about? (specific event, not general topic)
- What title/role did they hold at that moment?
- Is there anything in the surrounding text that changes the meaning of the quote in isolation?

**4. CORRUPTION RISK:**
Is this a widely-circulated quote? If so, do any of the uploaded sources cite different versions of it? Flag any variation — even minor.

If you CANNOT find the original source in the uploaded documents, say so clearly: "ORIGINAL SOURCE NOT IN NOTEBOOK — cannot verify wording."

Use [1], [2] citation markers. Include a SOURCES section at the end formatted as:
1. Author Last, First. "Full Title." Publisher, Year. p. XX.
```

**How to use the results:**
- If wording matches original: safe to use on screen
- If wording differs: use the ORIGINAL wording on screen, even if you say the corrupted version on camera (text overlay is the correction layer)
- If "ORIGINAL SOURCE NOT IN NOTEBOOK": upload the original document (speech transcript, treaty text, ruling PDF) and re-run. If you can't find the original, don't put the quote on screen as text — paraphrase instead
- If corruption risk flagged: Google `"exact quote" + misquoted` as a final human check (Gate 4)

**Source investment rule:** If your script has N on-screen quotes, your NLM notebook should contain the original document for each one. Budget 1-3 extra source uploads specifically for quote originals — speeches, letters, newspaper reports of speeches. These are usually free (Hansard, Trove, Library of Congress).

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
1. Author Last, First. "Full Book Title." Publisher, Year. p. XX. [Translator: Name, if translated work]
2. Author Last, First. "Article Title." Journal Name, Vol(Issue), Year. pp. XX-YY.
3. Body/Institution. "Document Title." Repository, Year. para./art. XX.
```

**Why this matters:** The citation extractor tool looks for `[N]` markers in the text and matches them to a SOURCES section. This format allows automatic extraction into VERIFIED-RESEARCH.md format. **Including publisher and translator prevents downstream citation gaps** — without them, every citation needs manual backfilling later.

**For translated works:** If a source was originally written in another language (Latin, French, Arabic, Malay, etc.), the translator's name and the translation's publication year are essential. Different translators produce different readings — which translation you cite changes what you can claim.

---

### Example NotebookLM Output (Extractor-Compatible)

**Input prompt:** "What do the sources say about literacy rates in Roman vs. Medieval Europe? Include [N] citation markers and a SOURCES section."

**NotebookLM response:**
```
Roman literacy rates were approximately 10-15% of the population [1]. This estimate is based on analysis of inscriptions, graffiti, and documentary evidence from Pompeii and other sites. In Early Medieval Europe (500-800 CE), literacy rates dropped to around 1-5% [2]. The decline was particularly severe outside monastic communities, where literacy was preserved through manuscript copying [2].

However, Wickham notes that this comparison can be misleading, as Roman "literacy" often meant basic reading ability, while Medieval literacy meant Latin fluency [2]. The nature of literacy changed, not just the rates.

SOURCES:
1. Harris, William V. "Ancient Literacy." Harvard University Press, 1989. p. 22.
2. Wickham, Chris. "The Inheritance of Rome: A History of Europe from 400 to 1000." Penguin, 2009. p. 147.
```

**After running `python tools/citation_extractor.py response.txt`, you get:**

```markdown
### Claim 1
**Claim:** Roman literacy rates were approximately 10-15% of the population
**Source:** Harris, William V. Ancient Literacy. Harvard University Press, 1989. p. 22.
**Status:** NEEDS REVIEW

### Claim 2
**Claim:** In Early Medieval Europe (500-800 CE), literacy rates dropped to around 1-5%
**Source:** Wickham, Chris. The Inheritance of Rome. Penguin, 2009. p. 147.
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
*Updated: 2026-04-05 — Added Mechanism Mapping prompt (Macro/Micro/Stress-Test) and Data Density Extraction prompt. From Wave 5 Wendover/RealLifeLore analysis. Prior: 2026-03-28 citation format v2.*
*Integration: Phase 34 NotebookLM Research Bridge*

---

## Proposed / Backlog Prompts (not yet wired)

> Two prompt ideas surfaced in the 2026-04-14 workflow audit. Neither is currently invoked by any command — they live here as a backlog for future wiring. Migrated from `memory/workflow-audit.md` on 2026-05-26.

### Post-`/script` Structure Comparison

**Purpose:** Catch "correct but boring" — surface whether the script's hook + thesis + closing beat structure has been done many times before by larger channels, and what your variant adds (or doesn't).

**Wiring target:** `/script` (run after structure-checker-v2 produces its report, before final output).

**Notebook:** the 85-transcript competitor notebook.

**Prompt sketch:** "Here are the hook, thesis, and closing of a script: [pasted]. Compare against the competitor transcripts in this notebook. (a) How many transcripts open with a structurally similar hook (specificity bomb + named primary doc + viral-quote rebuttal)? List up to 5 by title. (b) For the closing, identify the 3 most similar closings and quote their final 2 sentences. (c) What structural delta does this script have that the most similar ones do not?"

**Status:** PROPOSED — no command currently invokes this.

### `/greenlight` Title Validation Against Competitor Outliers

**Purpose:** Score working titles against known competitor outlier patterns (front-loaded keyword, specificity bomb, two-sentence declarative, scale anchor, authority figure, date paradox). Extends existing P1–P4 prompts.

**Wiring target:** `/greenlight --full` Step 0 (after the existing P1–P4 prompts complete).

**Notebook:** the competitor outlier notebook (corpus used by `/greenlight`).

**Prompt sketch:** "Working title candidates: [list]. For each title, score 0–100 against these outlier patterns: (1) front-loaded high-volume keyword, (2) specificity bomb (named doc + named figure + concrete fact), (3) two-sentence declarative shape, (4) scale anchor (number that's unusual for the niche), (5) authority figure named, (6) date-paradox or year-collision. Cite the closest 2 competitor outliers per title with their titles + view counts. Rank candidates by composite score."

**Status:** PROPOSED — no command currently invokes this.
