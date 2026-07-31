# Next Video Discovery Plan — Research Assistant Pipeline

**Purpose:** Find the next breakout video by combining LLM ideation, VidIQ demand data, Gemini deep research, and YouTube coverage analysis. Six phases, executable in ~3-4 hours total.

**Created:** 2026-05-26
**Replaces:** ad-hoc "what's next" conversations

---

## THE FILTER (read this first — kill criteria)

> ### ⚠ CRITERION 1 IS WITHDRAWN — 2026-07-29, owner interview
> Asked directly whether the pre-1900 rule was his or something a tool invented, the owner chose
> **"No constraint — the topic decides."** The rule below was never his; it was inferred here on
> 2026-05-26 and then hardened into a kill criterion. **Do not apply it.** A 1969 UN report and a
> 1494 treaty compete on equal terms; the test is whether showable primary evidence exists.
>
> The "modern exception (NARROW)" clause below is therefore also void — there is nothing to except.
>
> Criteria 2–5 stand. The auto-kill list stands **except** that "20th-century declassified files"
> is a *performance* observation (Condor/Iran/Vichy averaged 34–40 views), not an identity rule —
> treat it as a caution to package harder, not a ban. Current-affairs commentary stays killed:
> the owner's line is *"i do want to show why it is relevant but i want to specialize in history."*
>
> Live identity definition: `tools/PACKAGING_MANDATE.md` § Identity guard (restated 2026-07-29).

A candidate must satisfy ALL of:

1. ~~**Primary document is PRE-1900**~~ — **WITHDRAWN, see box above.** Replaced by: **the topic clears at least one access barrier** (enclosure · language · ideology · archive) for the viewer.
2. **High demand** — parent search term ≥2,000/mo OR cultural-moment spike (NYT viral series, court case ruling, anniversary).
3. **Public misconception OR English coverage gap** — most existing accounts get it wrong, OR no English long-form video covers it well.
4. **Document is visually presentable** — text, treaty, manuscript, deed, decree, letter. Not just "an account of."
5. **10-year evergreen test passes** — will this still matter regardless of who's in power?

**Modern exception (NARROW):** A post-1950 document only qualifies if (a) it's still legally operative AND (b) virtually nobody knows it exists. Default = reject modern.

**Auto-kills:**
- ❌ 20th-century declassified intelligence files (Operation Condor / Iran 1953 / Vichy pattern — averaging 34-40 views)
- ❌ Current geopolitics commentary (Trump-Greenland, Trump-Panama drift)
- ❌ Topics already saturated by RealLifeLore / Wendover / Money & Macro at high quality
- ❌ Anything in the channel-DNA-fail bucket: "geopolitics with historical background" rather than "history with modern relevance"

---

## PHASE 1 — Candidate Generation (45 min)

**Goal:** Produce 20-30 candidate topics matching the filter.

### 1A. Reload the topic pipeline
```
Read: channel-data/TOPIC-PIPELINE.md
Read: video-projects/PROJECT_STATUS.md (lifecycle dashboard)
Read: .brain/index.md §3 Active Topics
```
Extract any pre-1900-document candidates already in the system but not yet committed. Carry these into the candidate list.

### 1B. LLM ideation — three angles

Run these as three SEPARATE Claude/Gemini queries (don't merge — each produces different output):

**Prompt A — Famous-battle / treaty / law where the document says something different:**
```
List 20 pre-1900 events where:
- The popular narrative is widely believed
- The actual primary document (treaty, law, decree, letter, manuscript) contradicts or significantly complicates that narrative
- The document is accessible (published translation or transcription exists)
- The story has visual interest (two-language treaty, side-by-side maps, ornate manuscript)

For each: (1) event/topic, (2) popular belief, (3) what document actually shows, (4) where document is published, (5) 1-sentence hook.

Exclude: WWII, US Civil War, Holocaust (saturated). Prefer non-US-centric topics.
```

**Prompt B — Missing translations / linguistic deceptions:**
```
List 15 pre-1900 treaties, laws, or contracts that were signed in two or more languages, where the versions differ substantively. For each: which languages, what the discrepancy was, what happened because of it.

Examples seed: Wuchale 1889 (Italian/Amharic), Waitangi 1840 (English/Maori), Treaty of Tripoli 1796 (Arabic/English).
```

**Prompt C — Suppressed / forgotten primary sources:**
```
List 15 pre-1900 primary documents that:
- Are published and accessible today
- Were ignored or actively suppressed for most of the 20th century
- Contradict a major historical narrative still taught or popularly believed
- Have not been the subject of a >100K-view YouTube video

Include: where the document is housed, key passage, what mainstream narrative it complicates.
```

### 1C. Competitor reverse-scan

Run via `/gemini` skill (deep research mode) — Gemini CLI command:
```
gemini -p "@channel-data/channel-insights.md @video-projects/_ARCHIVED/

Scan the channel's published winners (Hijab, Spanish Inquisition, Manhattan, Treaty of Tripoli, Thermopylae). What do their primary-source documents have in common structurally? Identify the structural pattern and propose 10 new candidate topics that match the same pattern but have NOT been covered by this channel."
```

Output: append to candidate list.

### 1D. Dedupe + filter

Merge all outputs. Drop any candidate that:
- Has document dated 1900 or later (unless narrow exception applies)
- Is already in `_IN_PRODUCTION/` or `_ARCHIVED/published/`
- Fails the visual-document test

**Phase 1 deliverable:** `candidates-RAW.md` with 20-30 topics, each with: topic, document date, document name, popular narrative, what document actually shows.

---

## PHASE 2 — Demand Test (30 min)

**Goal:** Drop candidates with no measurable search demand.

### 2A. VidIQ batch query

For each candidate, query VidIQ Keyword tool with 3 variants:
1. The TOPIC name (e.g., "Wuchale Treaty")
2. The PARENT term (e.g., "Battle of Adwa")
3. The MISCONCEPTION term (e.g., "Ethiopia colonization")

Record for each: search volume, competition score, Overall Score.

**Pass threshold:** parent term ≥2,000/mo VidIQ search vol OR topic itself ≥800/mo.

### 2B. YouTube native search check

For top 10 surviving candidates, manually search YouTube:
- Long-form video count (>8min) for the topic name
- Top 3 videos' views and publish dates
- Last 12 months activity

**Red flag if:** 3+ recent (last 12mo) long-form videos with >100K views on the topic. That's saturation — move on.
**Green flag if:** Top result is <50K views, or top result is >3 years old, or no long-form English exists.

### 2C. Cultural-moment scan

For each surviving candidate, WebSearch:
- `"<topic>" news` (last 6 months)
- `"<topic>" anniversary OR commemoration 2026`
- `"<topic>" reddit OR twitter` (discussion volume)

Flag any topic with active cultural attention.

**Phase 2 deliverable:** `candidates-FILTERED.md` — 5-10 candidates surviving the demand test. Each row: topic, VidIQ scores, YouTube competition state, cultural-moment flag.

---

## PHASE 3 — Coverage Gap Deep Research (45 min)

**Goal:** For each surviving candidate, prove whether English coverage is thin or wrong.

### 3A. Gemini deep research per candidate

For each of the 5-10 candidates, run via `/gemini`:

```
gemini -p "Deep research task:

TOPIC: <candidate topic>
PRIMARY DOCUMENT: <document name and date>

(1) Find the 5 best English-language long-form video treatments of this topic on YouTube. List title, channel, views, publish year.

(2) For each, summarize what they say happened. Quote any factual claims about the primary document.

(3) Compare those claims to the academic consensus on what the document actually says. Cite 2-3 university press sources.

(4) Identify SPECIFIC factual errors or omissions in the popular video coverage.

(5) Score 1-10: how big is the gap between popular accounts and the primary document? 10 = nobody who hasn't read the document would get the story right.

Output a structured report."
```

### 3B. NotebookLM scholarly grounding (top 3 only)

For the top 3 candidates by Phase 3A gap score, upload 5-10 university-press sources to NotebookLM and query:

```
What does <primary document> actually say about <key contested claim>? Quote verbatim with citations.

What is the academic consensus on <misinterpretation>? List the 3 strongest counter-arguments to the popular narrative.

What primary-source evidence is available for the operative claim, and where is it published?
```

**Phase 3 deliverable:** `candidates-COVERAGE-GAP.md` with gap scores and verified-misconception evidence for top 3-5 candidates.

---

## PHASE 4 — Comment Mining (30 min)

**Goal:** Validate that misconception is alive in the audience right now.

Run `/comment-mine` against the top 2-3 video treatments of each candidate topic:

```
/comment-mine <YouTube URL of top video on topic>
```

Extract:
- Top 50 most-liked comments
- Count: how many repeat the misconception vs how many question it
- Count: how many ask follow-up questions the video didn't answer

**Pass criteria:** at least 30% of top comments either repeat the misconception, or ask questions the video didn't answer. This is your audience-demand proof.

**Phase 4 deliverable:** `candidates-AUDIENCE-DEMAND.md` — comment-mining evidence per candidate.

---

## PHASE 5 — Primary-Source Accessibility (30 min)

**Goal:** Confirm the document is actually obtainable in usable form.

For top 2-3 candidates, verify:

1. **Document is published** — citable edition exists (university press, archive, government gazette).
2. **English translation exists** OR original language is gettable (Latin/French/Spanish/Italian/German — you can verify per [verifiable-languages](memory/user-languages.md)).
3. **Document is visually striking** — manuscript image, ornate decree, bilingual text columns, official seal.
4. **NotebookLM can host the source** — PDF or scanned text available.

**Auto-disqualify** any candidate where the document is paraphrased in scholarly literature but not directly accessible.

**Phase 5 deliverable:** `candidates-DOCUMENT-VERIFIED.md` — 2-3 finalists with source manifests ready to feed into `/greenlight`.

---

## PHASE 6 — Decision (15 min)

### 6A. Score matrix

Build a table with weighted columns:

| Candidate | Demand (25) | Coverage Gap (25) | Comment Demand (20) | Document Visual (15) | DNA Fit (15) | TOTAL |

Weights:
- **Demand 25%** — VidIQ + YouTube vs saturation
- **Coverage Gap 25%** — how wrong existing English coverage is
- **Comment Demand 20%** — proof the audience cares now
- **Document Visual 15%** — can the document carry on-screen narrative
- **DNA Fit 15%** — territorial/colonial/ideological + 10-year evergreen test

### 6B. Run /greenlight on the top candidate

```
/greenlight <topic>
```

If `/greenlight` passes, commit. If it fails on packaging, drop to candidate #2 and re-run.

### 6C. Update memory + topic pipeline

- Append decision to `memory/feedback-content.md` (or relevant file) with reasoning
- Update `channel-data/TOPIC-PIPELINE.md` with new entry
- Move chosen candidate folder to `_IN_PRODUCTION/` if not already there
- Save the rejected candidates with rationale to `channel-data/RESERVE-CANDIDATES.md` — next time, start Phase 2 from this list

**Phase 6 deliverable:** committed topic + scaffolded project folder.

---

## TIME BUDGET

| Phase | Duration | Mode |
|---|---|---|
| 1 — Candidate generation | 45 min | Mixed (Claude + Gemini deep research) |
| 2 — Demand test | 30 min | Manual VidIQ + YouTube |
| 3 — Coverage gap | 45 min | Gemini deep research (parallel per candidate) |
| 4 — Comment mining | 30 min | `/comment-mine` skill |
| 5 — Document accessibility | 30 min | Manual + NotebookLM |
| 6 — Decision | 15 min | Score + `/greenlight` |
| **TOTAL** | **~3 hr 15 min** | |

---

## EXECUTION CHECKLIST

When ready to run, copy this checklist into a fresh chat:

- [ ] Phase 1A — Read topic pipeline + project status + brain index
- [ ] Phase 1B — Run Prompts A, B, C in separate queries
- [ ] Phase 1C — Run Gemini competitor reverse-scan
- [ ] Phase 1D — Dedupe → `candidates-RAW.md`
- [ ] Phase 2A — VidIQ batch query (3 variants per candidate)
- [ ] Phase 2B — YouTube native search for top 10
- [ ] Phase 2C — Cultural-moment WebSearch
- [ ] Phase 2D — Produce `candidates-FILTERED.md`
- [ ] Phase 3A — Gemini deep research per surviving candidate
- [ ] Phase 3B — NotebookLM scholarly grounding (top 3)
- [ ] Phase 3C — Produce `candidates-COVERAGE-GAP.md`
- [ ] Phase 4 — `/comment-mine` on competitor videos → `candidates-AUDIENCE-DEMAND.md`
- [ ] Phase 5 — Verify document accessibility → `candidates-DOCUMENT-VERIFIED.md`
- [ ] Phase 6A — Build score matrix
- [ ] Phase 6B — `/greenlight <winner>`
- [ ] Phase 6C — Update memory + topic pipeline + reserve list

---

## SEED CANDIDATES (start Phase 2 with these — already partial Phase 1 work done)

Pre-existing candidates that match the OLD-document filter, ready to feed into demand-test:

| # | Topic | Document | Date | Pipeline state |
|---|---|---|---|---|
| 39 | Wuchale Treaty | Italian/Amharic bilingual Article 17 | 1889 | In scripting (`_IN_PRODUCTION/`) |
| 21 | Haiti Independence Debt | Charles X ordinance, 150M francs | 1825 | Script-ready but flagged "parked" — investigate why |
| 3 | Monroe Doctrine | Annual presidential message | 1823 | Idea stage |
| 20 | Guadalupe Hidalgo | Treaty + Articles VIII-X | 1848 | Idea stage |
| 16 | Merer Diary | Workers' papyrus | ~2560 BCE | Idea stage — discovered 2013 |
| 38 | Recopilación de Indias | Spanish colonial code | 1680 | Research phase |
| 49 | Code Noir | Louis XIV ordinance | 1685 | Idea stage (greenlight queue) — too close to Slave Trade? |
| 8 | Medieval Women | TBD — needs document anchor | Medieval | Brief only |

Also worth fresh-generating in Phase 1:
- Treaty of Sèvres / Lausanne (1920/1923 — borderline modern, but legally operative)
- Battle of Plassey treaties (1757)
- Belgian Congo Free State charter (1885) — channel did Berlin Conference
- Treaty of Tianjin / Unequal Treaties (1858) — Opium Wars aftermath
- Treaty of Brest-Litovsk (1918 — borderline)
- The Bull of Donation / Inter Caetera (1493) — precedes Tordesillas but separate angle
- Maximilian's Mexican Empire decrees (1864-67)
- The Adams-Onís Treaty (1819) — US-Spain Florida
- The Treaty of Hünkâr İskelesi (1833) — Russia-Ottoman secret article
- The Treaty of Nerchinsk (1689) — first Sino-Russian, mostly forgotten

---

## NOTES ON USING THIS PLAN

- **Don't skip Phase 4 (comment mining).** Demand can look strong in VidIQ but be dead in audience activity. Comments are the truth.
- **Phase 3 is the slowest but most valuable.** The Gemini deep-research output is what proves "people get it wrong" — this is the foundation of the video's thesis statement.
- **Run Phases 2, 3, 4 in parallel where possible.** They're per-candidate independent.
- **Reserve candidates matter.** Phase 2-5 filter heavily. Don't throw away the rejected ones — they're your starting point for the NEXT next-video search.
- **The filter is non-negotiable.** If a candidate is exciting but the document is post-1900, kill it. The channel's data is clear.
