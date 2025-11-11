# NotebookLM Prompt Generator Skill - History vs Hype

Generate fully customized NotebookLM research prompts tailored to a specific topic and sources. These prompts extract evidence, identify patterns, and find smoking gun sources.

## When to Use

- User runs `/notebooklm-prompts` command
- Part of `/create-video` workflow at Stage 4

## Your Task

Create 8-11 copy-paste ready prompts that will extract exactly the research needed for a History vs Hype video.

**Core prompts (1-8):** Use for all topics
**Specialized prompts (9-11):** Use for religious/political topics, position changes, or duration claims

## Step 1: Gather Context

You need:
1. **Topic and thesis:** What myth is being debunked? What's the argument?
2. **Sources:** What has been uploaded to NotebookLM? (Or use the source recommendation list)
3. **Research gaps:** What specific questions need answers? (From deep research report)
4. **Modern hook:** What current event makes this timely?

If not provided, ask the user for these details.

## Step 2: Generate Custom Prompts

Create these prompts in order (fully customized for the topic):

### Prompt 1: Topic-Specific Research Organization

**Purpose:** Get NotebookLM to organize all sources around the specific myth/thesis

**Template Structure:**
```
Based on all uploaded sources about [SPECIFIC TOPIC], analyze the evidence regarding [SPECIFIC MYTH/CLAIM].

Generate 5 essential questions that capture:
1. What is the origin of the myth that [SPECIFIC FALSE NARRATIVE]?
2. What primary sources (treaties, documents, official records) directly address [SPECIFIC CLAIM]?
3. What do academic historians conclude about [SPECIFIC ASPECT]?
4. How has this myth been used politically/culturally from [RELEVANT TIME PERIOD] to present?
5. What counter-evidence exists that defenders of the myth cite?

For each question:
- Provide specific source titles and page references
- Extract relevant quotes (verbatim)
- Identify contradictions between sources
- Note which claims have strongest/weakest support
```

**Customization:** Replace bracketed sections with specifics from the user's topic.

### Prompt 2: Smoking Gun Evidence Extraction

**Purpose:** Find the most undeniable primary source evidence

**Template Structure:**
```
Extract smoking gun evidence from primary sources that proves/disproves: "[SPECIFIC CLAIM BEING TESTED]"

Focus on:

PRIMARY DOCUMENTS (treaties, official records, court rulings):
- Exact text of [SPECIFIC DOCUMENT NAME if known, or type if not]
- Direct quotes that explicitly address [SPECIFIC CLAIM]
- Dating and authenticity verification
- What each document definitively proves or disproves

STATISTICAL EVIDENCE:
- [SPECIFIC DATA TYPE - e.g., casualty figures, territory sizes, economic data]
- Original sources of statistics (not secondary citations)
- Methodology of data collection
- How this data contradicts the myth

CONTEMPORARY TESTIMONY:
- Accounts from [RELEVANT TIME PERIOD] about [SPECIFIC EVENTS]
- Witnesses or participants with firsthand knowledge
- Officials' statements or correspondence

For each piece of evidence:
- Exact quote with source title and page number
- Date of document/statement
- Author/issuer and their position
- Why this is "smoking gun" level (impossible to dispute)
- Any known counter-arguments to this evidence
```

### Prompt 3: Pattern Recognition

**Purpose:** Identify systematic issues (3+ interconnected incidents)

**Template Structure:**
```
Identify a systematic pattern in the sources showing that [GENERAL PATTERN HYPOTHESIS - e.g., "colonial powers repeatedly used similar legal justifications for expansion" or "the myth has been deployed at key political moments"].

Find:

INCIDENT/EXAMPLE 1:
- Date and location
- What happened (specific details)
- Who was involved (names, positions)
- Primary source evidence (quote + citation)

INCIDENT/EXAMPLE 2:
- [Same structure]

INCIDENT/EXAMPLE 3:
- [Same structure]

[Continue through 5-7 if sources support]

SYSTEMATIC NATURE:
- What connects these incidents?
- What does the pattern reveal about [SPECIFIC ASPECT]?
- Are there exceptions to the pattern? If so, why?
- How does this pattern undermine [SPECIFIC MYTH]?

Provide chronological timeline with specific dates.
```

### Prompt 4: Counter-Evidence Analysis (Steel-Manned)

**Purpose:** Find strongest opposing arguments (academic balance)

**Template Structure:**
```
What are the 5-7 strongest arguments IN SUPPORT of the claim that [STATE THE MYTH AS IF TRUE]?

**CRITICAL: Steel-man these arguments - find the MOST sophisticated versions, not weak strawmen.**

For each counter-argument:

ARGUMENT:
- What is the claim?
- Who makes this argument? (specific scholars, political figures, etc.)
- What's the most sophisticated version of this argument?

EVIDENCE CITED:
- What sources do they cite?
- What quotes or data do they use?
- Are these sources present in our uploaded materials?
- Are their sources credible?

CREDIBILITY ASSESSMENT:
- Is this argument made by credible scholars or fringe voices?
- What's the academic consensus on this counter-argument?
- Where is the counter-evidence strongest?
- What are the legitimate points in this argument?

WEAKNESSES:
- What evidence contradicts this counter-argument?
- What are the gaps or flaws in their reasoning?
- What do they ignore or downplay?
- Why did this position lose/become minority (if applicable)?

FAIR PRESENTATION:
- What valid points MUST be acknowledged in the video?
- How to address this counter-argument fairly but effectively?
- How long should this counter-argument get in the video? (8 lines? 30 lines?)

STEEL-MANNED VERSION:
- If you were defending this position, what's the strongest case you could make?
- What evidence would you emphasize?
- What would you argue our sources miss or misinterpret?

For religious/political topics:
- If claiming "Christianity" opposed X, search for Christian reformers who supported X
- If claiming practice was universal, search for exceptions and dissent
```

### Prompt 5: Modern Relevance Mapping

**Purpose:** Connect historical events to 2024-2025 impact

**Template Structure:**
```
How does the myth that [SPECIFIC FALSE NARRATIVE] affect politics, culture, or society TODAY (2020-2025)?

Identify:

POLITICAL USAGE (2020-2025):
- Which politicians, parties, or movements invoke this myth?
- Specific speeches, statements, or policies (with dates)
- What political goals does the myth serve?
- Quotes showing how the myth is deployed

CULTURAL IMPACT:
- How is this taught in schools? (curricula, textbooks, standards)
- Media representations (films, documentaries, popular books)
- Public commemorations or memorials
- Social media debates or viral content

POLICY CONSEQUENCES:
- Current laws or policies based on this historical narrative
- International disputes or tensions fueled by the myth
- Groups affected by the myth's propagation
- Material consequences (deaths, displacement, rights restrictions)

RECENT DEVELOPMENTS ([LAST 6 MONTHS]):
- News events connected to this history
- Academic research challenging the myth
- Political figures making claims based on the myth

For each example: Source, date, specific quote/reference, why it matters.
```

### Prompt 6: Script Hook Generation

**Purpose:** Find the most compelling opening hooks

**Template Structure:**
```
Based on all sources, identify 3-5 potential opening hooks for a video debunking [SPECIFIC MYTH].

For each hook:

HOOK OPTION:
- Exact quote, statistic, or event (verbatim from sources)
- Source citation with page number
- Date (if applicable)

EMOTIONAL/INTELLECTUAL APPEAL:
- Why does this grab attention?
- What makes it surprising or dramatic?
- Does it create immediate tension or question?

CONNECTION TO MAIN NARRATIVE:
- How does this hook lead into the full argument?
- What does it foreshadow about the evidence?
- Does it establish modern stakes immediately?

VIRAL POTENTIAL:
- Is this shareable? (shocking stat, dramatic quote, concrete action)
- Does it work in 8-15 seconds?
- Clear visual potential?

Prioritize hooks that:
- Involve concrete actions or specific numbers
- Connect to current events ([LAST 3 MONTHS])
- Reveal hypocrisy or contradiction
- Show immediate human stakes
```

### Prompt 7: Academic Consensus Summary

**Purpose:** Understand what historians actually agree on

**Template Structure:**
```
What is the academic historical consensus on [SPECIFIC TOPIC]?

MAINSTREAM VIEW:
- What do most credible historians conclude?
- Key scholars and their positions (names, universities, major works)
- Core evidence that mainstream historians cite
- How strong is the consensus? (unanimous, strong majority, divided)

CONTESTED AREAS:
- What aspects do historians still debate?
- Different schools of thought (with named representatives)
- Why is this contested? (evidence gaps, interpretation, politics)

FRINGE VS. MAINSTREAM:
- What positions are considered fringe or discredited?
- Why are they rejected by most scholars?
- Who still promotes fringe views and why?

RECENT DEVELOPMENTS:
- Any new research (last 5-10 years) changing the consensus?
- Archival discoveries or new evidence?
- Methodological advances reshaping understanding?

HISTORIOGRAPHICAL EVOLUTION:
- How has scholarly understanding changed over time?
- What did historians believe in [EARLIER ERA] vs. now?
- What caused the shifts?

Provide specific scholar names, book titles, and key publications.
```

### Prompt 8: Fact-Check Preparation

**Purpose:** Create a pre-filming verification checklist

**Template Structure:**
```
I'm writing a script claiming: [BRIEF SUMMARY OF MAIN THESIS]

Extract from all sources:

STATISTICS & NUMBERS to verify:
[List each number mentioned in preliminary research]
- [Statistic]: Source title, page number, exact context

DIRECT QUOTES to verify:
[List each quote planned for the script]
- "[Quote]": Source title, page number, full context, date if applicable

KEY CLAIMS to verify:
[List major interpretive claims]
- [Claim]: Which sources support this? Page numbers. Any contradictions?

CONTESTED OR UNCERTAIN CLAIMS:
- What claims do sources disagree about?
- What requires hedging language ("most historians," "evidence suggests")?
- What absolutely cannot be stated as definitive fact?

POTENTIAL ERRORS TO AVOID:
- Common misconceptions even among scholars
- Disputed dates or figures
- Attribution errors (quotes misattributed)
- Oversimplifications that distort truth

Provide: source title, page number, exact quote for each verification item.
```

### Prompt 9: Ambiguity & Position Changes Detection

**Purpose:** Identify where institutions changed positions or groups were divided

**Template Structure:**
```
Analyze all sources for AMBIGUITY and POSITION CHANGES regarding [SPECIFIC TOPIC].

POSITION CHANGES OVER TIME:
For each institution/group mentioned (churches, governments, political movements):
- What was their position on [ISSUE] in [EARLIER PERIOD]?
- What is their position on [ISSUE] in [LATER PERIOD] or today?
- When did the change occur? (Exact date/event)
- What triggered the reversal? (Vatican II, social pressure, war, etc.)
- How long did they hold the original position?
- Source citations for both positions

Examples to look for:
- Catholic Church on religious freedom (pre-Vatican II vs. post-Vatican II)
- Protestant denominations on slavery (defense → abolition)
- Political parties on [relevant issue]
- Academic consensus shifts

"BOTH SIDES" SCENARIOS:
Identify where [GROUP] was divided on [ISSUE]:
- What was the majority position? (Evidence and percentage if available)
- What was the minority/reform position? (Evidence)
- Why was the minority marginalized? (Theological, political, social reasons)
- When did positions flip (if ever)?
- Were both sides using same sources (Bible, Constitution, etc.)?

Examples to look for:
- Christians on both sides of slavery debate
- Catholics supporting vs. opposing human rights
- Americans defending vs. opposing colonialism
- [Topic-specific divisions]

TIMELINE PRECISION:
For each "X years" claim in preliminary research:
- Verify starting date: [Event/person] - [Year] - Source
- Verify ending date: [Event/person] - [Year] - Source
- Calculate actual years: [End] - [Start] = [X years]
- Is the claim accurate or inflated?

RED FLAGS TO REPORT:
- Position changes NOT mentioned in sources (script will be attacked)
- "Both sides" scenarios oversimplified as unified position
- Timeline claims that don't add up mathematically
- Vague "centuries" when exact dates available

Provide exact citations for each finding.
```

### Prompt 10: Source Balance Verification (For Religious/Political Topics)

**Purpose:** Ensure multiple perspectives represented, not just one tradition

**Template Structure:**
```
CRITICAL REVIEW: Source Balance for [RELIGIOUS/POLITICAL TOPIC]

**For claims about "Christianity":**

CATHOLIC SOURCES in uploaded materials:
- List all Catholic sources (papal documents, Catholic theologians, etc.)
- What do they say about [TOPIC]?
- Time periods covered?

PROTESTANT SOURCES in uploaded materials:
- List all Protestant sources (Luther, Calvin, denominational statements, etc.)
- What do they say about [TOPIC]?
- Time periods covered?

ORTHODOX SOURCES (if relevant):
- Any Eastern Orthodox perspectives?

BALANCE ASSESSMENT:
- Do we have BOTH Catholic AND Protestant perspectives?
- If claiming "Christianity" did X, do both traditions support this?
- Where do Catholic and Protestant positions differ?
- Are we treating one denomination as representative of all?

GAPS TO FILL:
- Missing Protestant sources on [specific claim]?
- Missing Catholic sources on [specific claim]?
- Denominations not represented?

**For claims about "the West" or "Western civilization":**

NATIONAL PERSPECTIVES:
- Which countries' sources are represented?
- British colonial policy vs. French vs. Spanish vs. Dutch?
- American position vs. European?
- Are we generalizing from one nation to all?

**For claims about "historians agree":**

SCHOLARLY DIVERSITY:
- List historians by institutional affiliation
- List historians by national origin
- List historians by time period
- Any dissenting scholars?

RED FLAGS:
❌ Only Catholic sources for "Christianity" claims
❌ Only British sources for "Western" claims
❌ Only American scholars for international topics
❌ No acknowledgment of denomination/national differences

Recommend specific sources to add if balance is lacking.
```

### Prompt 11: Timeline Math Verification

**Purpose:** Calculate actual years to prevent inflated claims

**Template Structure:**
```
TIMELINE PRECISION CHECK for [TOPIC]

For each duration claim in preliminary research:

CLAIM: "[X years of Y]"

CALCULATION:
- Starting point: [Event/document/person] - Year: [YYYY]
  - Source: [Title, page]
  - Why this starting point? [Justification]

- Ending point: [Event/document/person] - Year: [YYYY]
  - Source: [Title, page]
  - Why this ending point? [Justification]

- MATH: [End Year] - [Start Year] = [X] years

- VERIFICATION: Is claim accurate?
  - If YES: Confirmed at [X] years
  - If NO: Actual is [X] years, claimed is [Y] years (difference: [Z] years)

AMBIGUITY CHECKS:
- Was practice continuous throughout period or intermittent?
- Were there significant gaps or exceptions?
- Did intensity/nature change over time?
- Should claim be "up to X years" or "approximately X years"?

EXAMPLES TO CHECK:
- "1,800 years of Christian support for slavery"
  - Starting point: Augustine (~400 AD)?
  - Ending point: Brazil abolition (1888)?
  - Calculation: 1888 - 400 = 1,488 years (NOT 1,800)

- "[X] centuries of [practice]"
  - Convert to specific years
  - Verify continuous vs. intermittent

For each timeline claim:
1. Calculate actual years
2. Flag if math is off by >50 years
3. Provide corrected wording if needed
4. Cite sources for start and end dates

```

## Step 3: Format for Copy-Paste

Present all prompts in a clean, numbered format:

```markdown
# CUSTOM NOTEBOOKLM PROMPTS: [Topic]

**Topic:** [Full description]
**Thesis:** [What you're arguing]
**Sources Uploaded:** [Number] sources
**Date:** [Date]

---

## How to Use These Prompts

1. Make sure all recommended sources are uploaded to NotebookLM
2. Copy each prompt below (one at a time)
3. Paste into NotebookLM chat
4. Wait for complete response
5. Copy NotebookLM's response into a document
6. Move to next prompt
7. When all prompts are complete, provide all responses for script generation

**Priority order:**
- Run Prompts 1-8 for all topics
- Run Prompts 9-11 for religious/political topics or topics involving duration claims

---

## PROMPT 1: Research Organization

[Full customized prompt text - copy-paste ready]

---

## PROMPT 2: Smoking Gun Evidence

[Full customized prompt text]

---

## PROMPT 3: Pattern Recognition

[Full customized prompt text]

---

## PROMPT 4: Counter-Evidence Analysis (Steel-Manned)

[Full customized prompt text]

---

## PROMPT 5: Modern Relevance Mapping

[Full customized prompt text]

---

## PROMPT 6: Script Hook Generation

[Full customized prompt text]

---

## PROMPT 7: Academic Consensus

[Full customized prompt text]

---

## PROMPT 8: Fact-Check Preparation

[Full customized prompt text]

---

## PROMPT 9: Ambiguity & Position Changes Detection

[Full customized prompt text]

**When to use:** Topics involving institutional position changes (Vatican II, denomination splits, policy reversals) or "X years of Y" claims

---

## PROMPT 10: Source Balance Verification

[Full customized prompt text]

**When to use:** Claims about "Christianity," "the West," or any broad category where sub-groups may have different positions

---

## PROMPT 11: Timeline Math Verification

[Full customized prompt text]

**When to use:** Any claim involving "X years," "centuries," or duration of a practice/belief

---

## After Running All Prompts

Collect all NotebookLM responses into one document and provide them for script generation via `/script` command.

Save responses to: `video-projects/[topic-slug]/05-notebooklm-output.md`
```

## Quality Standards

### Good Prompts:
- Specific to the exact topic (not generic)
- Ask for source citations and page numbers
- Request exact quotes (not paraphrases)
- Designed to extract evidence for the specific thesis
- Acknowledge potential counter-evidence
- Focus on actionable script material

### Red Flags in Your Prompts:
- Too generic (could apply to any topic)
- Don't ask for citations
- Lead NotebookLM to confirm bias (ask what sources say, not "prove X")
- Too complex (NotebookLM has length limits)
- Redundant (asking same question multiple ways)

## Optimization Notes

**NotebookLM works best when:**
- Questions are specific and focused
- You request exact quotes with citations
- You ask about patterns across sources
- You acknowledge complexity (contested claims, counter-evidence)

**NotebookLM struggles with:**
- Very broad questions
- Requests to synthesize beyond the sources
- Highly technical jargon
- Multi-part questions with 10+ sub-questions

Keep prompts focused and citation-oriented.

## Output Location

Save prompt set to: `video-projects/[topic-slug]/04-notebooklm-prompts.md`

## After Generation

Ask user:
1. Do these prompts cover your research needs?
2. Should I generate Prompts 9-11 (for religious topics, position changes, or timeline claims)?
3. Any specific questions I should add?
4. Are your sources uploaded to NotebookLM?
5. Ready to start running these prompts?
6. Want me to explain any prompt in more detail?

## Integration with Other Skills

**After prompts are run in NotebookLM:**
- User provides NotebookLM output → Run **script-generator** skill
- Script generated → Run **script-reviewer** skill for credibility check
- Reviewer identifies issues → Fix and run **fact-checker** skill
- Fact-checker validates → Script ready for production
