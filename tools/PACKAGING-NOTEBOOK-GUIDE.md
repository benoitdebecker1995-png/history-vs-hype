# Packaging Intelligence Notebook — Setup Guide

**Purpose:** A dedicated NotebookLM notebook that makes competitor packaging data queryable in natural language. Instead of running scorers and hoping, you ASK the data: "What works for colonial topics? What title patterns get views? What angle is nobody covering?"

**Used by:** `/greenlight --full` Step 0B, Packaging Intelligence Prompts (P1-P4) in `NOTEBOOKLM-RESEARCH-PROMPTS.md`

---

## What Goes In This Notebook

Upload these as **text sources** (not URLs — text is more queryable):

### Source 1: Your Channel Performance Data

Create a text file with your video data. Format:

```
HISTORY VS HYPE — VIDEO PERFORMANCE DATA (updated YYYY-MM-DD)

VIDEO 1:
- Title: "Spain vs Portugal. They Split the World in Half."
- Type: territorial
- Views: 170,000
- CTR: 4.2%
- Retention: 32%
- Duration: 10:14
- Hook type: cold_fact
- Title pattern: versus
- Upload date: 2025-08-15

VIDEO 2:
- Title: "France Bankrupted Haiti. The Documents Prove It."
...
```

**Source:** Export from `analytics.db` or compile from POST-PUBLISH-ANALYSIS files.

### Source 2: Competitor Channel Data

For each competitor channel (Kraut, Knowing Better, WonderWhy, Shaun, etc.), create a text file:

```
COMPETITOR: Kraut (604K subs)

TOP 10 VIDEOS BY VIEWS:
1. "Trump's Biggest Failure" — 9.3x channel avg — Type: ideological
   - Title pattern: declarative (possessive + noun)
   - Why it worked: [your assessment]
2. "How Vodka Ruined Russia" — 8.3x — Type: mechanism
   - Title pattern: how/why
   - Why it worked: cultural hook, short (9 min)
...

BOTTOM 10 VIDEOS BY VIEWS:
1. "Title" — 0.3x — Type: X
   - Title pattern: Y
   - Why it underperformed: [assessment]
...

TITLE PATTERNS USED:
- Declarative: 45% (avg performance: X)
- How/Why: 30% (avg performance: Y)
- Versus: 10% (avg performance: Z)
...
```

**Source:** YouTube channel pages, Social Blade, or your intel DB (`tools/intel/`).

### Source 3: Outlier Analysis

Upload the existing outlier analysis:

```
NICHE OUTLIER PATTERNS (870 videos, 9 channels)

TITLE PATTERNS IN OUTLIER VIDEOS (3x+ channel average):
- Two-sentence declarative: 11% outlier rate (3x baseline)
- Scale words ("every", "all", "entire", "century"): 1.33x lift
- Country names in title: 1.2x lift
- Specificity (numbers, dates in title): 1.15x lift

TITLE PATTERNS IN UNDERPERFORMERS (<0.5x channel average):
- Colon structure: -28% CTR
- Years in title: -46% CTR
- "The X That Y": worst performing pattern (1.2% CTR)
- Questions: -36% CTR (small sample)
...
```

**Source:** `tools/benchmark/outlier_title_dissector.py` output + `PACKAGING_MANDATE.md` data.

### Source 4: Topic Type Packaging Patterns

```
PACKAGING PATTERNS BY TOPIC TYPE

TERRITORIAL:
- Best title pattern: versus (4.0% CTR)
- Best thumbnail: map with color contrast + 2-4 word overlay
- Best hook: cold_fact / map anomaly
- Avg views: 2,449
- Sub conversion: 0.65%
- Traffic: 42% subscriber-dependent
- Example winners: [list top 3 with titles]

IDEOLOGICAL:
- Best title pattern: declarative (3.8% CTR)
- Best thumbnail: historical visual + text overlay
- Best hook: myth_contradiction (36.7% retention)
- Avg views: 179 (but 2.31% sub conversion — best)
- Example winners: [list]

COLONIAL:
...

MECHANISM/HOW:
...
```

**Source:** Your channel data + competitor data cross-referenced.

### Source 5: Thumbnail Pattern Data (optional)

```
THUMBNAIL PATTERNS (650 thumbnails analyzed)

RULES:
- Text overlay: mandatory (87% of niche uses it)
- No face: 0% face usage in niche
- Maps: required for territorial topics
- Color contrast: red vs blue or warm vs cool for versus topics

TOP PATTERNS:
1. Map + bold text (territorial): [examples]
2. Historical photo + text (ideological): [examples]
3. Document close-up + text (untranslated): [examples]
...
```

---

## How to Create the Notebook

1. **Go to** notebooklm.google.com
2. **Create new notebook** named "HvH Packaging Intelligence"
3. **Add sources** as text (paste each source above as a new text source)
4. **Tag the notebook** for easy retrieval

Or via MCP:
```
mcp__notebooklm__notebook_create(title="HvH Packaging Intelligence")
mcp__notebooklm__source_add(source_type="text", text="[paste source content]")
```

---

## How to Use It

### During `/greenlight --full`

The greenlight command's Step 0B queries this notebook automatically using Prompt P1 from `NOTEBOOKLM-RESEARCH-PROMPTS.md`:

```
mcp__notebooklm__notebook_query(
    notebook_id="[packaging notebook ID]",
    query="What angles and title patterns work for [TOPIC TYPE] topics?"
)
```

### Manual Queries

Open the notebook in NotebookLM and ask:
- "What title patterns get the most views for territorial topics?"
- "How did channels package videos about [specific topic]?"
- "What's the gap in how [topic] is usually covered?"
- "If I'm making a video about [topic], what should my title look like?"

### After Publishing

Use Prompt P4 to run a packaging post-mortem against the data.

---

## Keeping It Current

**Update frequency:** After every `/analyze` run (post-publish), add the new video's data to Source 1. After every `/intel --refresh`, update Source 2 with new competitor data.

**The goal:** Every time you run `/greenlight`, you're not just scoring titles algorithmically — you're querying the accumulated packaging intelligence of 870+ videos, 9 channels, and your own 47+ video performance history.

---

*Created: 2026-04-08*
*Related: `/greenlight` Step 0B, `NOTEBOOKLM-RESEARCH-PROMPTS.md` Prompts P1-P4*
