# Correction / Receipt Format — Research Prompts

**Purpose:** Validate whether a 5-7 min "Correction" format (one myth + one primary source, side-by-side) has viable topics and YouTube demand for History vs Hype.

**Format definition:**
- 5-7 min total
- ONE widespread misconception (not a compound)
- ONE primary source document that contradicts it, shown on screen
- Origin story of the myth (who started it, when, why it spread)
- Editing complexity: static document comparison + talking head. No map tours, no B-roll chains.

**Use order:**
1. Run **GEMINI PROMPT A** → get 20-30 candidate misconceptions
2. Run **GEMINI PROMPT B** against the top 10 → stress-test each for format fit
3. Run **VIDIQ QUERIES** → validate demand + competition
4. Score via decision rubric at bottom → pick the test topic

---

## GEMINI PROMPT A — Topic Discovery

Paste into Gemini (use Deep Research mode if available). Replace nothing — ready to run.

```
I'm a YouTuber running a channel called "History vs Hype" that debunks historical misconceptions using primary sources. Target audience: males 25-44, UK/DE/CA/US. Channel covers colonial history, border disputes, treaties, and ideological narratives.

I'm testing a new short-format video concept:
- 5-7 minutes
- ONE widely-held historical misconception
- ONE primary source document that directly contradicts it (shown on screen)
- Origin story: where the myth came from (Wagner, Hollywood, specific textbook, politician, viral meme)
- Intellectually honest — explain what the received story gets right, then show what the document says

I need you to surface 25 CANDIDATE MISCONCEPTIONS that fit this format. For each, return:

1. **The claim** (how people commonly state it, in plain English — one sentence)
2. **The contradicting primary source** (specific document, author, date — must be real and citable)
3. **The one-line debunk** (what the document actually says, paraphrased)
4. **Myth origin** (who/what popularized the wrong version — if known)
5. **Primary-source accessibility** (PUBLIC_DOMAIN / PAYWALLED / MUSEUM_ONLY / UNCLEAR)
6. **Fit score 1-10** for this channel's format (how document-first the story is)

SELECTION CRITERIA — only include candidates that meet ALL of these:
- The misconception is widely held (not just niche academic debate)
- A SINGLE primary source cleanly contradicts it (not "scholarly consensus" — a document)
- The primary source exists in English OR has a published academic translation
- The story is TELL-ABLE in 5-7 minutes (not a decade-long context dump)
- Not the usual YouTube misconceptions (horned Viking helmets, Napoleon's height, Columbus and the flat earth — these are saturated)

BIAS TOWARDS:
- Treaties, laws, speeches with ONE misquoted line or mistranslated clause
- Statements attributed to historical figures that they never actually said (with documented real quote)
- Numbers widely cited but wrong in a traceable way (census figures, casualty counts, dates)
- Colonial-era documents where the received textbook framing omits what the document actually ordered
- Myths that have a CLEAR origin point (a specific Victorian historian, Cold War pamphlet, Hollywood film)

AVOID:
- Misconceptions that require showing 10+ documents to untangle
- Claims that are "debated" rather than "documented vs undocumented"
- Misconceptions where the "correct" version is itself contested by historians
- Topics that are politically radioactive in 2026 (Israel/Palestine, Russia/Ukraine current — historical equivalents fine)

FORMAT your response as a ranked table (best fit first), then a second section called "ALSO CONSIDERED" with 5 runner-ups that almost fit but missed one criterion — note which criterion.

Include working links to the primary sources where possible.
```

---

## GEMINI PROMPT B — Top 10 Stress Test

Run this after Prompt A. Paste top 10 candidates from Prompt A into the brackets.

```
From the candidate list below, I need deeper vetting of each before I commit to filming. For each candidate, return:

1. **Primary source verification status**
   - Does the document I'd cite ACTUALLY say what the summary claims?
   - Quote the exact contradicting passage (with page/section reference)
   - Flag any translation uncertainty or disputed readings

2. **Myth origin verification**
   - Is the "where the myth came from" story documented, or folk knowledge?
   - If documented, cite the academic source that traces it
   - If folk knowledge, flag as HYPOTHESIS

3. **Steelman check**
   - What's the strongest version of the "wrong" claim?
   - Is there ANY primary source that supports the received story, even partially?
   - What does academic consensus currently say (not populist consensus)?

4. **5-minute tellability**
   - Can the full story — claim, document, origin — be delivered in 5 minutes WITHOUT skipping context?
   - If no, what gets cut?
   - If yes, what's the 30-second version?

5. **Competition check (YouTube)**
   - Search YouTube for the exact claim. What comes up?
   - Are there videos with 100K+ views already covering this angle?
   - Is there a gap (e.g. no video shows the primary source on screen, or nobody has the translation angle)?

6. **Red flags**
   - Anything that would get pushback in comments you need to preempt?
   - Any fringe-adjacent associations to avoid?
   - Any recent news that would complicate the framing in 2026?

CANDIDATES TO STRESS TEST:
[1] [PASTE CANDIDATE 1 FROM PROMPT A]
[2] [PASTE CANDIDATE 2]
[3] [PASTE CANDIDATE 3]
[4] [PASTE CANDIDATE 4]
[5] [PASTE CANDIDATE 5]
[6] [PASTE CANDIDATE 6]
[7] [PASTE CANDIDATE 7]
[8] [PASTE CANDIDATE 8]
[9] [PASTE CANDIDATE 9]
[10] [PASTE CANDIDATE 10]

At the end, give me a FINAL RANKING with these 10 re-ordered by viability for a 5-7 min document-first video. Call out the top 3 as "production-ready" and the bottom 3 as "drop."
```

---

## GEMINI PROMPT C — Format Viability (run this ONCE, separately)

Before committing to the format itself, validate it works on YouTube.

```
I'm testing a new video format for my history/myth-busting YouTube channel:
- 5-7 minutes (shorter than typical educational content)
- ONE misconception + ONE primary document on screen
- Forensic close-read of the document
- Minimal B-roll, no map tours, no news clips

I want you to analyze whether this SHORT DOCUMENT-FIRST format works on YouTube in the history/education niche. Specifically:

1. **Precedent analysis:** Name 5-10 YouTube channels that have shipped similar short, single-source, document-first history videos. Include subscriber count, typical view count, and what specifically they do right/wrong. Examples might include: Knowing Better, Historia Civilis, Extra Credits, Kraut, Invicta, Atun-Shei, specific Nebula creators.

2. **Runtime analysis:** In the history/education niche on YouTube in 2025-2026, how do 5-7 min videos perform versus 10-15 min versus 20+ min? What's the retention vs reach tradeoff? Cite any public data (VidIQ studies, Tubular reports, YouTube creator interviews).

3. **Format fatigue check:** Is "debunk ONE thing with ONE document" a saturated format, an emerging format, or an underused format? Who's doing it well right now?

4. **Algorithm fit:** Does the YouTube algorithm in 2025-2026 reward short educational content, or does it still favor the 10-20 min sweet spot? How have the AVD and session-start metrics evolved?

5. **Mobile viewing consideration:** 70%+ of YouTube viewing is mobile. Does a document-on-screen format work on mobile, or does the text become unreadable? Any best practices for document-heavy videos on vertical/small screens?

6. **Risk assessment:** What are the 3 most likely failure modes for this format?

Respond with sourced observations — cite creators, videos, studies where possible. Avoid vague generalities.
```

---

## VIDIQ QUERIES — Demand + Competition Validation

**Constraint:** VidIQ is only used for **keyword search volume + competition score**. Nothing else.

### How to run

For each candidate from Prompt A/B, run the EXACT CLAIM as a keyword search. Record:
- Monthly search volume
- Competition score (0-100, lower = more opportunity)
- Related keywords VidIQ suggests

### Scoring thresholds (based on own channel performance)

| Metric | HARD PASS | SOFT PASS | STOP |
|--------|-----------|-----------|------|
| Search volume | 500+/mo | 250-499/mo | <250/mo |
| Competition | <40 | 40-60 | 60+ |
| VidIQ score | 60+ | 40-59 | <40 |

A topic must HARD PASS on at least 2 of 3 metrics to move forward.

### Query list template

Copy this to a scratchpad while reviewing Gemini output. Fill in top 10 candidates.

```
Candidate 1: [claim]
  - VidIQ keyword tried: "___________"
  - Search volume: ___
  - Competition: ___
  - VidIQ overall score: ___
  - Related keywords worth testing: ___, ___, ___
  - Verdict: HARD PASS / SOFT PASS / STOP

Candidate 2: [claim]
  ... (repeat)
```

### Secondary VidIQ checks

After primary keyword, test these variants for each HARD PASS:

1. **"[figure] actually said"** — tests misattribution angle
2. **"[document] mistranslation"** — tests linguistic angle
3. **"myth of [topic]"** — tests general debunk demand
4. **"real story [topic]"** — tests authenticity framing

Note which framing has the strongest volume-to-competition ratio. That's your title hint.

---

## DECISION RUBRIC — Picking the Test Topic

After running all prompts, score each surviving candidate on this:

| Factor | Weight | Score (1-5) | Notes |
|--------|--------|-------------|-------|
| Primary-source accessibility | 3x | | Must be public domain or openly translated |
| Document tells the story in 60 sec | 3x | | If not, format breaks |
| Myth origin has a clear story | 2x | | Wagner / Hollywood / textbook / politician |
| VidIQ HARD PASS count (0-3) | 2x | | From volume, competition, overall |
| Competitor gap (no 100K+ YT video) | 2x | | From Prompt B #5 |
| Politically neutral in 2026 | 1x | | Avoid radioactive framings |
| Fits own channel DNA (history > geopolitics) | 2x | | 10-year relevance test |

**Minimum score to film:** 55/75

**If NOTHING scores 55+:** the format itself isn't the problem — widen the topic net with a second Gemini Prompt A run targeting different historical eras/regions.

---

## AFTER VALIDATION — What to Save

If a topic clears the rubric:

1. Create project folder: `video-projects/_IN_PRODUCTION/XX-correction-[topic-slug]-2026/`
2. Save Gemini outputs into `_research/00-gemini-discovery.md` and `_research/01-gemini-stress-test.md`
3. Save VidIQ scores into `_research/02-vidiq-demand.md`
4. Run `/greenlight` on the top-scoring title before any NotebookLM work

If NOTHING passes: save all outputs into `channel-data/FORMAT-EXPERIMENTS/correction-format-FAILED-[date].md` with a one-paragraph retro on WHY. That data still has value for the next format experiment.
