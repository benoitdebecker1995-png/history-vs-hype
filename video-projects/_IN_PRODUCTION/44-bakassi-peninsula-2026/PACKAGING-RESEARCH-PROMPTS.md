# Packaging Research Prompts — Bakassi Peninsula (#44)

**Purpose:** Copy-paste prompts for VidIQ keyword research and Gemini Deep Research to optimize packaging before filming.
**Date:** 2026-04-09

---

## VIDIQ PROMPT (Keyword Research)

Paste into VidIQ keyword research tool. Run each keyword separately and record: monthly search volume, competition score, overall score.

### Keywords to Research

```
bakassi peninsula
nigeria cameroon border
nigeria cameroon dispute
cameroon vs nigeria
nigeria lost territory
ICJ ruling
international court of justice
bakassi oil
colonial borders africa
african border disputes
nigeria territory
bakassi war
cameroon nigeria war
greentree agreement
old calabar
efik people
biafra
stateless people
border dispute explained
colonial treaty
```

### What to Record

For each keyword, note:
- Monthly search volume
- Competition score (0-100)
- Overall VidIQ score
- Related keywords VidIQ suggests

### What to IGNORE from VidIQ

- Strategy suggestions ("optimize your title by...") — these are generic AI text
- "Trending" labels without volume numbers
- Any recommendation that contradicts the channel's data patterns (see CLAUDE.md)

### What to USE from VidIQ

- Raw search volume numbers — these are reliable
- Competition scores — useful for identifying blue ocean keywords
- Related keyword suggestions — can reveal demand angles you missed

---

## GEMINI DEEP RESEARCH PROMPT

Paste into Gemini with Deep Research enabled. This generates a competitor landscape and packaging strategy report.

```
I'm a small YouTube history channel (515 subscribers, 219K+ views, 47 videos). I'm making a video about the Bakassi Peninsula dispute between Nigeria and Cameroon. I need a packaging analysis. Here is my context:

MY VIDEO ANGLE: "Nigeria Was Right About 1884 — And Still Lost." The ICJ gave Bakassi to Cameroon in 2002 (13-3 vote). Nigeria's reading of the 1884 Treaty of Protection was correct — the ICJ agreed it didn't transfer sovereignty. But Britain signed the 1913 Anglo-German Agreement anyway, and Nigeria itself spent 30 years after independence treating Bakassi as Cameroonian territory. The video reads primary sources on camera: the ICJ judgment, three dissenting opinions, and six treaties/agreements.

MY CURRENT TITLE OPTIONS:
A: "Nigeria vs Cameroon. 150000 People. One Colonial Treaty." (scored 90/100)
B: "Nigeria vs Cameroon. How 150000 People Lost Their Country" (scored 90/100)
C: "Nigeria vs Cameroon. The Verdict Nobody Fixed" (scored 80/100)

MY THUMBNAIL CONCEPTS:
A: Map split with Nigerian/Cameroonian flags over Bakassi, text "BAKASSI"
B: ICJ courtroom, text "13 vs 3"
C: 1884 treaty / displaced residents split, text "150,000"

RESEARCH TASKS:

1. COMPETITOR SCAN: Find every YouTube video about:
   - Bakassi Peninsula
   - Nigeria Cameroon border dispute
   - ICJ ruling Cameroon v Nigeria
   For each video found, record: title, channel, view count, upload date, video length, like count if visible. Note the dominant framing (colonial theft? legal explainer? geopolitics?).

2. TITLE ANALYSIS: Which of my three title options is strongest based on:
   - Keyword placement (what terms have the most search volume?)
   - Emotional vs analytical framing
   - Competitor differentiation (does anyone else use this structure?)
   - What SPECIFIC title changes would you recommend?

3. THUMBNAIL ANALYSIS: For every competitor video found, describe their thumbnail (colors, text, imagery). What's the dominant visual pattern? Which of my three concepts would stand out most?

4. AUDIENCE ANALYSIS: Who searches for Bakassi content? Nigerian diaspora? African history enthusiasts? International law students? General history buffs? What does the audience composition suggest about packaging?

5. DEMAND SIGNALS: Are there Reddit threads, forum posts, Quora questions, or social media discussions about Bakassi that indicate unmet demand? What specific questions do people ask?

6. GAP ANALYSIS: What angle does NO existing video cover? What question does nobody answer? That's my opportunity.

IMPORTANT — What I need from you vs what I'll ignore:
- I NEED: Raw data (view counts, upload dates, titles, thumbnail descriptions, search volumes)
- I NEED: Observations about patterns you actually see in the data
- I WILL IGNORE: Made-up metrics (don't invent "Creator Trust scores" or "estimated CTR")
- I WILL IGNORE: Generic strategy advice ("optimize for SEO" — I know)
- I WILL IGNORE: Historical claims (you're not a historian, don't fact-check my angle)
- DO NOT fabricate view counts or subscriber numbers — if you can't find them, say so

Format your response as:
1. Competitor inventory (table: title, channel, views, date, length, angle)
2. Title recommendation (with specific reasoning tied to data)
3. Thumbnail recommendation (with specific reasoning tied to competitor patterns)
4. Audience profile
5. Demand signals
6. Gap analysis
```

---

## NOTEBOOKLM VERIFICATION PROMPTS

Run these in the Bakassi NotebookLM notebook to verify the ⚠️ claims from the fact-check before filming.

### Prompt 1: Greentree Article 3 — Exact Rights Listed

```
I need the EXACT TEXT of Article 3 of the Greentree Agreement (2006) between Cameroon and Nigeria regarding the Bakassi Peninsula.

Specifically, does Article 3 explicitly guarantee ALL of the following?
1. Property rights
2. Fishing rights
3. Freedom from forced nationality change
4. Language and cultural protections

For each one: quote the exact words from Article 3 that cover it, or tell me it's NOT in the text. I need to know which of these four protections are explicitly stated versus which I'm inferring.

Include citation markers [1], [2] for every quote.
```

### Prompt 2: Oil Rivers Protectorate Timeline

```
What was the administrative entity that Old Calabar was folded into after the 1884 Treaty of Protection? 

Specifically:
- Was it called the "Oil Rivers Protectorate" and when was that established?
- When did it become the "Niger Coast Protectorate"?
- When did it become the "Protectorate of Southern Nigeria"?
- What does the ICJ judgment call this entity?

I need the ICJ's exact terminology with paragraph numbers. The script currently says "Oil Rivers Protectorate, later the Niger Coast Protectorate" — is that accurate?

Include citation markers [1], [2] for every quote.
```

### Prompt 3: Nigerian Maps Duration

```
The ICJ judgment discusses Nigerian maps that showed Bakassi inside Cameroon. 

1. What specific maps does the judgment cite?
2. Over what time period were these maps published?
3. Does the judgment say "thirty years" or give a specific duration?
4. What paragraphs discuss this?

I'm trying to verify whether "for decades, Nigerian official maps showed Bakassi inside Cameroon" is accurate and whether I can be more specific about the timeframe.

Include citation markers [1], [2] for every quote.
```

### Prompt 4: HMS Flirt Location

```
Where exactly was HMS Flirt anchored when the 1884 Treaty of Protection was signed? The script says "in the Old Calabar River." 

1. Does any source specify the exact location?
2. Is "Old Calabar River" the correct waterway name, or should it be "Cross River" or "Calabar River"?

Include citation markers [1], [2] for every quote.
```

---

*Created: 2026-04-09*
*Status: Ready to run. VidIQ and Gemini prompts are standalone. NotebookLM prompts require re-authentication first.*
