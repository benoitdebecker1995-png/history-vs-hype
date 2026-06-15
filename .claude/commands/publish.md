---
description: YouTube metadata, title testing, clip suggestions (Post-production Phase 1)
model: opus
---

# /publish - Publishing Preparation Entry Point

Generate YouTube metadata, test titles, or identify clip-worthy moments. Everything needed to publish effectively.

## Usage

```
/publish                     # Interactive: full metadata generation
/publish --metadata [project] # Generate title, description, tags, timestamps
/publish --titles [project]  # Generate title variants for A/B testing
/publish --clips [project]   # Identify clip-worthy moments for Shorts
/publish --full [project]    # All publishing preparation
/publish --prompts [project]     # Generate VidIQ/Gemini prompts from script
/publish --intake [project]      # Parse tool responses into structured data
/publish --synthesize [project]  # Re-run synthesis on existing intake data
```

**Post-publish step:** After upload, fix auto-transcription errors with `/fix [project]` (single-purpose subtitle correction). Treat `/fix` as the documented next step in the publish flow — don't drop into a generic Claude conversation for it.

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--metadata` | Full YouTube metadata package | `/publish --metadata 19-flat-earth-medieval-2025` |
| `--titles` | Title variants for VidIQ testing | `/publish --titles 19-flat-earth-medieval-2025` |
| `--clips` | Clip suggestions for Shorts/TikTok | `/publish --clips 19-flat-earth-medieval-2025` |
| `--full` | All three workflows | `/publish --full 19-flat-earth-medieval-2025` |
| `--evaluate` | Technique effectiveness evaluation | `/publish --evaluate somaliland-2025` |
| `--prompts` | Generate external tool prompts | `/publish --prompts 35-gibraltar-treaty-utrecht-2026` |
| `--intake` | Parse VidIQ/Gemini responses | `/publish --intake 35-gibraltar-treaty-utrecht-2026` |
| `--synthesize` | Re-run synthesis engine | `/publish --synthesize 35-gibraltar-treaty-utrecht-2026` |
| `--topic` | Override topic type for thumbnail pattern selection and coherence check | `/publish --metadata 41-treaty-tordesillas-2026 --topic territorial` |
| `--thumbs` | Generate thumbnail concepts only | `/publish --thumbs 41-treaty-tordesillas-2026` |

---

## Channel Insights Context (Auto-run)

Before generating output, check for own-channel performance context:

1. Read `channel-data/channel-insights.md` if it exists
2. Use as **internal context** for decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- Channel Performance Context ---
[Extract 2-3 most relevant lines from channel-insights.md for this workflow]
Example: Top format: territorial (avg 1,950 views). Best retention: 42.0%.
Low signal: ~15 videos — experiment freely.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing analytics
5. Insights are advisory — guide experimentation, never dictate choices

**For /publish:** Focus on title patterns and topic performance (what titles/topics get highest CTR/views)

---

## YouTube Intelligence Context (Auto-run)

Before generating output, check for YouTube algorithm and niche intelligence:

1. Read `channel-data/youtube-intelligence.md` if it exists
2. Use as **internal context** for metadata decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- YouTube Intelligence Context ---
[Extract 2-3 most relevant lines from youtube-intelligence.md for this workflow]
Example: Title pattern from outliers: specific mechanism titles ("How X deleted Y") > vague framing.
Algorithm: CTR weight is "high" — thumbnail/title alignment critical.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing intelligence
5. If last refresh date is >30 days old, add note: "(Intel last refreshed [date] — consider running /intel --refresh)"
6. Intelligence is advisory — inform title and metadata decisions, never dictate

**For /publish:** Focus on:
- **Title patterns:** What title formulas are working in outlier videos (mechanism titles, question titles, etc.)
- **CTR signals:** What the algorithm currently weights for CTR and how it affects discovery
- **Competitor title trends:** What title patterns competitors are using (avoid/differentiate)
- **Niche topic clusters:** What topics are trending in the niche (tag relevance)

---

## PRE-PUBLISH QUALITY GATES

**Before generating final metadata, run validation checks.**

### Gate 0: Metadata-Drift Gate (post-rough-cut, pre-publish)

> See `memory/feedback-earn-your-inclusion.md` §'metadata-level earned-inclusion' for the three tests baked into this gate, and the Hijab #52 origin.

Run this gate **first** — before title scoring, tag refinement, or clip selection. `YOUTUBE-METADATA.md` authored pre-filming may have drifted from the finished cut on timestamps, source list, title promises, or description completeness. The gate re-derives metadata against the actual SRT.

#### Inputs required

1. `YOUTUBE-METADATA.md` — the file being checked
2. The finished-cut SRT — locate via Glob for `*.srt` in the project folder; prefer the most recent / "finished cut" / "final" named file. This is the source of truth.
3. The locked `SCRIPT.md` — supplementary context only, not authority.

#### Four drift checks

**a. Chapter-timestamp grounding**

Parse the SRT for structural pivots (scene changes, major topic transitions). For each chapter in `YOUTUBE-METADATA.md`:
- If the chapter timestamp falls **outside** the SRT's actual runtime: flag as `[CHAPTER-DRIFT: chapter "<name>" timestamp <T> exceeds SRT runtime <R>]`.
- If the chapter timestamp doesn't correspond to a structural pivot in the SRT (±5s tolerance): flag as `[CHAPTER-DRIFT-PIVOT: chapter "<name>" timestamp <T> doesn't match any SRT pivot]`.

Output a proposed re-derivation: a new chapter list with timestamps grounded in actual SRT pivots.

**b. Source-list earned-inclusion**

Extract scholar names from the description's source list. Grep the SRT for each name:
- Scholar in source list but **not named** in SRT: flag as `[SOURCE-LIST-UNUSED: scholar "<Name>" listed but not named in finished cut]`. Default action: cut from list.
- Scholar **named in SRT** but not in source list (heuristic: capitalized first-name + last-name pairs preceded by "Historian," "Per," "Scholar," "according to," or in citation-tag positions): flag as `[SOURCE-LIST-MISSING: scholar "<Name>" named in cut but not in description]`. Default action: add to list.

**c. Title-promise earned-inclusion**

Parse the title and all A/B variants for promise patterns:
- Numeric claims ("Three Medieval Scholars," "Two Countries," "229 Ethnic Groups")
- Named-entity claims ("Lord Cromer," "Ibn al-Jawzi")
- Mechanism-word claims ("Forbidden," "Mandatory," "Forged")

For each promise, check the SRT delivers it. If "Three Medieval Scholars" is promised but only one is named in the cut: flag as `[TITLE-PROMISE-UNFULFILLED: variant "<title>" promises <claim> but cut delivers <actual>]`.

**d. Dangling-text grep**

Grep the description body for:
- Sentences ending in em-dash, en-dash, or hyphen without trailing punctuation
- Sentences cut mid-clause (line ends with a preposition, conjunction, or bare auxiliary verb)
- Unclosed parentheses, quotes, or em-dash pairs

Flag each as `[DESCRIPTION-DANGLING: line N — "<text>"]`.

#### Output: `YOUTUBE-METADATA-DRIFT.md`

Write to the project folder. Contains:
1. Summary count of each flag class
2. Detailed flag list with proposed remediation per flag
3. Final section: **"Override decisions"** — user accepts or overrides each flag with rationale

#### Gate behavior

`/publish` cannot proceed past Gate 0 until either:
- All flags have been remediated (metadata file edited), **or**
- All flags have been explicitly overridden in `YOUTUBE-METADATA-DRIFT.md` with a one-line rationale per override.

An empty flag list (zero flags across all four checks) counts as automatic pass — proceed to Gate 1.

---

### Gate 1: Title Score Gate (HARD BLOCK)

**Run BEFORE finalizing any title candidates.** Every title option must pass `title_scorer.py` AND `outlier_title_dissector.py`.

```python
import sys, subprocess
sys.path.insert(0, '.')
from tools.title_scorer import score_title
from tools.discovery.database import KeywordDB

# Use live CTR (DB-enriched) by default — static PATTERN_SCORES are only a fallback.
db = KeywordDB()
db_path = db.db_path
candidates = ["Title Option A", "Title Option B", "Title Option C"]
for t in candidates:
    result = score_title(t, db_path=db_path)
    print(f"  {result['score']}/{result['grade']}  {t}")
    if result.get('snapshot_date'):
        print(f"    live CTR as of {result['snapshot_date']} ({result['staleness_days']}d old)")
    if result.get('penalties'):
        for p in result['penalties']:
            print(f"    PENALTY: {p}")
db.close()

# Also run outlier pattern check for niche-validated signals
for t in candidates:
    r = subprocess.run(
        ['python', '-m', 'tools.benchmark.outlier_title_dissector', '--score', t],
        capture_output=True, text=True
    )
    print(r.stdout)
```

**Rules:**
- **Score < 65 → BLOCKED.** Do not include in YOUTUBE-METADATA.md. Generate a replacement.
- **Grade = REJECTED → HARD BLOCK.** REJECTED now fires ONLY on the clickbait brand-gate (e.g. "SHOCKING", "You won't believe") — NOT on year/colon/"The X That Y" (those are graded HEDGE style penalties per `PACKAGING_MANDATE.md` Tier 2/3; the hard-reject policy is RETIRED — the channel's #1/#3 videos both use colons). Review `style_warnings`, don't treat them as fatal.
- **All 3 title options must score 65+.** If none pass, keep generating until 3 do.
- **Display scores to user** (incl. the live-CTR staleness line) so they can make an informed pick.

**Output format in YOUTUBE-METADATA.md:**

```
### Title Options

| # | Title | Score | Grade |
|---|-------|-------|-------|
| 1 | India vs Pakistan. Britain Drew the Border in 5 Weeks. | 85 | A |
| 2 | Britain Split India in 5 Weeks. The Map That Started 4 Wars. | 75 | B |
| 3 | How One Lawyer Split 88 Million People in 5 Weeks. | 70 | B |
```

### Gate 2: Metadata Consistency Check

```bash
/discover --check YOUTUBE-METADATA.md
```

**What it validates:**
- Primary keyword in title (HIGH priority)
- Primary keyword in description opening (HIGH priority)
- Keyword stuffing detection (>2% = fail)
- Title-tag overlap (consistency)
- Description length (200+ words)
- Tag count (5-30 recommended)

**Required status:** [PASS] before publishing

**If [FAIL]:**
1. Review issues list
2. Fix HIGH priority issues
3. Re-run check until [PASS]

**See:** `/discover --check` documentation for full details

### Gate 3: Rendered-Asset QC (the exported thumbnail + final audio)

Gates 0–2 check metadata *text*. They cannot see the actual files the viewer encounters. Gate 3 audits the rendered assets — the only stage where they exist.

**Skip cleanly** if the assets aren't exported yet (this gate is advisory at metadata-draft time, mandatory before upload). Locate the exported thumbnail (Glob the project folder for `*.png` / `*.jpg` not under `_research/`) and the final cut (`*.mp4`).

**a. Thumbnail image audit** — runs only if a rendered thumbnail exists:

```bash
python -m tools.preflight.thumbnail_image_audit "<thumb.png>"            # legibility + tech gate (hard)
python -m tools.preflight.thumbnail_image_audit "<thumb.png>" --serp-ids <id1>,<id2>,<id3>   # + informational shelf line
```

The **hard gate is feed-size legibility** — a mushy/low-detail thumbnail that won't resolve in the ~160px feed (the one image-computable click-killer), plus tech compliance (res / ratio / size). **SERP differentiation (CLIP) is INFORMATIONAL ONLY** — per ADR 0007, differentiation ≠ clickability (a low-info blob is trivially "distinct"). Pass `--serp-ids` only if you want the informational DISTINCT/TYPICAL/SIMILAR line; it does **not** affect the verdict.

- **ILLEGIBLE AT FEED SIZE / sub-spec resolution / oversize file** → BLOCK. Won't read (or won't upload); fix before publishing.
- **Legibility + tech PASS** → proceed.
- Differentiation, when computed, is reported DISTINCT/TYPICAL/SIMILAR — a note for context, never a gate. (`open_clip_torch` missing → RGB-histogram proxy, even more directional; still informational.)

**b. Audio loudness QC** — runs only if a final cut exists (and ffmpeg is installed):

```bash
python -m tools.preflight.audio_loudness "<final-cut.mp4>"
```

Checks integrated LUFS / true-peak / loudness-range against YouTube's −14 LUFS normalization. (Usually already cleared at `/editing-guide` time — this is the last-line backstop.)

- Integrated outside −16…−12 LUFS, or true peak > −1 dBTP → FLAG, remaster.
- `MISSING` (ffmpeg not installed) → note it, don't block: `winget install Gyan.FFmpeg`.

**Gate behavior:** A thumbnail that's **illegible at feed size** (or sub-spec resolution / oversize) blocks like a failing title (Gate 1). Differentiation is informational, never a block. Audio findings are advisory flags, not hard blocks. If neither asset exists yet, record "Gate 3 deferred — assets not exported" and proceed.

---

## Feedback Insights (Automatic)

Before generating metadata, surface past CTR and title insights.

**Run automatically:**
```python
import sys
sys.path.insert(0, 'tools/youtube_analytics')
from feedback_queries import get_insights_preamble
topic = '{topic_type}'
preamble = get_insights_preamble(topic, 'publish')
if preamble:
    print(preamble)
else:
    print('No past performance insights available. Run: python -m tools.youtube_analytics.feedback backfill')
```

**Display the insights preamble** before generating metadata. If no insights, skip silently.

**Insight types for /publish:** CTR and title insights (which title formulas worked, thumbnail styles, metadata patterns).

---

## METADATA GENERATION (`--metadata` or default)

### Step 1: Read Context FIRST

**Before asking questions:**

1. **Find the script:** `video-projects/**/SCRIPT.md`
2. **Read script:** Understand content, extract structure
3. **Find project location:** Confirm folder path
4. **Check for VidIQ data:** If user mentions, ask for analysis

### Step 2: Generate Metadata

#### 1. Title Options (3 variations — ALL must pass Gate 1)

**Requirements:**
- 50-60 characters (mobile-friendly)
- Factually accurate
- Documentary tone
- Include main hook/myth
- **Score 65+ on title_scorer.py** (run Gate 1 before finalizing)
- **Years, colons, "The X That Y" = graded style penalties, NOT auto-rejects** (per `tools/PACKAGING_MANDATE.md` Tier 2 HEDGE — the hard-reject policy is RETIRED; the channel's #1/#3 videos both use colons. Review warnings, don't treat as fatal.)

**SEO Keyword Pivoting:**
- If primary keyword has zero search volume, pivot to related high-volume terms
- Put dead keywords in description/tags, not title
- Example: "Crusades fact-check" (0 volume) → "Jerusalem 1099: What Crusaders Really Wrote"

#### 2. Description

> **Niche-benchmarked formula** (150 descriptions, 14 channels — see `METADATA-CHECKLIST.md` for full checklist):

**Follow this structure exactly:**

```
LINE 1: Thesis statement or strongest specific claim (shows in search results)
LINE 2: What this video examines / unique angle (second search-visible line)

2-4 sentence summary with main keyword 2-3x.

TIMESTAMPS (scale to video length: 5-7 for <10min, 7-10 for 10-20min, 10-15 for 20+min)
0:00 - [Chapter]
X:XX - [Chapter]

SOURCES
[Academic citations: author, title, publisher, year, pages]

Subscribe for evidence-based history analysis.

#Hashtag1 #Hashtag2 #Hashtag3
```

**Key rules:**
- **First line = thesis/hook, NOT generic topic.** "In 1494, the Pope drew a line..." beats "This video covers the Treaty of Tordesillas." (Fall of Civilizations leads with evocative hooks even in descriptions — 38M views on top video)
- **Subscribe CTA = mandatory.** 94% of niche includes one. We only have 44%. Close this gap.
- **Hashtags at END only.** YouTube shows first 3 hashtags above title if placed in first lines.
- **Sources = competitive advantage.** We cite in 73% vs 43% niche avg. Keep this.
- **Timestamps = keep doing.** We include in 84% vs 29% niche. Sets us apart.
- **No links in first 2 lines.** Kraut/CaspianReport waste first lines on sponsor links. Don't do this.
- **Target 1,000-2,000 chars** (niche avg: 2,030. Ours: 2,011. On target.)
- **Run description keyword gap filler** for missing high-value search terms:
  ```python
  import subprocess
  result = subprocess.run(
      ['python', '-m', 'tools.youtube_analytics.description_gap_filler', '--project', project_slug],
      capture_output=True, text=True
  )
  # Shows search terms bringing traffic but missing from description
  ```

#### 3. Timestamps

- Extract from script structure
- Clear section names
- Match actual video flow

#### 4. Tags (20-30)

- Primary (high volume search terms)
- Secondary (specific discovery)
- Long-tail (niche)
- If VidIQ data available, prioritize their recommendations

#### 5. Thumbnail Concepts (Auto-Generated)

Thumbnail concepts are now **auto-generated** from script content via `MetadataGenerator._generate_thumbnail_concepts()`.

**Each concept is validated** with a ✅/⚠️ badge (score/100) from `thumbnail_checker.py`. A PASS badge confirms the concept follows PACKAGING_MANDATE rules (map/geographic signal, no face, no text overlay).

**Bridge analysis is MANDATORY.** After generating concepts, read the script hook (first 30 seconds) and run the bridge test from `THUMBNAIL-EVALUATION-FRAMEWORK.md` Tier 5. Each concept must be paired with a specific title and checked against the hook. Priority is determined by bridge tightness, not individual thumbnail score.

**Output format — title/thumbnail pairings (not standalone concepts):**

```
### Pairing 1: [Name] (PRIMARY — tightest bridge)
**Thumbnail:** [Visual + overlay]
**Title:** [Exact title]
**Score:** [N/100]
**Bridge:** TIGHT — [overlay] delivered in hook at [timestamp]
**The Handoff:** [How thumbnail → title → hook connects for the viewer]

### Pairing 2: [Name] (Rotation)
...
```

**To override topic type for pattern selection:**
```
/publish --metadata [project] --topic territorial
/publish --metadata [project] --topic ideological
/publish --metadata [project] --topic political_fact_check
```

Valid topic types: `territorial`, `ideological`, `political_fact_check` (default: auto-detected from script).

**To generate thumbnail concepts only:**
```
/publish --thumbs [project]
```

#### 6. Coherence Check (Auto-Generated)

The metadata bundle now includes an automatic coherence check in the title table and a detail section.

**What it checks:** Whether the primary script entity (e.g., "Spain") appears in:
- Each title candidate
- The description first line
- At least one thumbnail concept

**Title table coherence column:**

| # | Title | Score | Grade | Pattern | Coherence | Bridge |
|---|-------|-------|-------|---------|-----------|--------|
| 1 | Spain vs Portugal | 78 | B+ | versus | 3/3 ✅ | TIGHT |
| 2 | How Two Countries... | 71 | B | how_why | 2/3 ⚠️ | GAP |
| 3 | The Pope Drew... | 68 | B- | declarative | 1/3 ❌ | ADEQUATE |

**Ranking impact:** Bridge verdict IS a ranking factor — TIGHT bridge titles are preferred over higher-scoring titles with a GAP. Entity coherence remains annotation only.

### Output Location

`video-projects/[project]/YOUTUBE-METADATA.md`

---

## TITLE TESTING (`--titles`)

Generate 5-10 title variants optimized for VidIQ A/B testing.

### Channel Title Standards

**DO:**
- 60-70 characters (mobile-friendly)
- Factually accurate
- Documentary tone
- Include the controversy/hook

**DON'T:**
- Clickbait ("You won't BELIEVE...")
- ALL CAPS words
- Excessive punctuation
- Misleading promises

### CTR Intelligence (Auto-run)

Before presenting title variants, run CTR predictions on all candidates:

```python
from tools.youtube_analytics.title_intelligence import TitleIntelligence

ti = TitleIntelligence()
# Rank all candidate titles by predicted CTR
ranked = ti.rank_title_variants(["Title A", "Title B", ...], topic="territorial")
# Each result includes: predicted_ctr, vs_avg, confidence, factors
```

**Display alongside each title:**
- Predicted CTR and vs channel avg (e.g., "Predicted: 5.3% CTR (+1.2%)")
- Key factors driving prediction (format, length, features)
- Flag titles with negative CTR signals (questions, starting with "The", years in title)

**Also run keyword gap check:**
```python
gaps = ti.keyword_gaps()
# Check if any high-demand keywords could be woven into titles
```

If the title intelligence module is unavailable (import error), skip silently and generate titles without predictions.

### Output: 10 Title Variants

**Category 1: Fact-Check Frame (3 titles)**
Format: "Fact-Checking [Person/Claim]: [What Evidence Shows]"
- Best for: Political figures, viral claims

**Category 2: Myth-Bust Frame (3 titles)**
Format: "The [Myth] Myth: [Reality]"
- Best for: Historical misconceptions

**Category 3: Documentary Frame (2 titles)**
Format: "[Topic]: [Specific Aspect] Explained"
- Best for: Complex historical topics

**Category 4: Question/Curiosity Frame (2 titles)**
Format: "Did [X] Really [Y]?"
- Best for: SEO, search discovery

### Output Format

```markdown
# TITLE VARIANTS: [Topic]

**Video Length:** [X min]
**Target CTR:** 6%+

## RECOMMENDED TITLES

### Category 1: Fact-Check Frame
1. [Title] (XX characters) — **Predicted CTR: X.X% (+X.X%)**
   - Hook: [Why this works]
   - Risk: [Potential issue]
   - CTR factors: [key positive/negative signals]

[Continue for all categories...]

## TOP 3 RECOMMENDATIONS

**Best for CTR:** #[X] - [Reason]
**Best for SEO:** #[X] - [Reason]
**Best for Brand:** #[X] - [Reason]

## VIDIQ TESTING INSTRUCTIONS

1. Go to VidIQ Title Tester
2. Paste top 4 titles
3. Compare scores (70+ good, 80+ excellent)
4. Pick winner balancing search volume + competition

## TITLE + THUMBNAIL BRIDGE ANALYSIS

For each title/thumbnail pairing, trace the full viewer pipeline:

```
PAIRING [N]: [Concept Name]
  THUMBNAIL: [Visual description + overlay text]
  TITLE: [Exact title]
  HOOK (first 15s): [What the viewer hears — quote from script]
  BRIDGE: TIGHT / ADEQUATE / GAP
  HANDOFF: [1-2 sentences explaining how thumbnail → title → hook connects]
```

**Bridge verdicts:**
- **TIGHT:** Thumbnail overlay appears in hook within 15 seconds
- **ADEQUATE:** Connection within 30 seconds
- **GAP:** Thumbnail visual connects to minute 2+ but not hook
- **NONE:** No connection — reject

**Priority rule:** TIGHT bridge > higher scorer score. A seamless pipeline retains viewers after the click.

**Always generate 3 pairings** (each thumbnail matched to its best title) for YouTube native A/B rotation.
```

---

## CLIP SUGGESTIONS (`--clips`)

Identify 3-5 clip-worthy moments for YouTube Shorts and TikTok.

### What Makes a Good Clip

**All must apply:**
1. **Self-contained** - Makes sense without full video
2. **Hook in first 2 seconds** - Grabs attention immediately
3. **Single clear point** - One fact, one reveal
4. **30-60 seconds** - Sweet spot for shorts
5. **Strong ending** - Ends on impact

### Best Clip Types for History vs Hype

| Type | Example | Why It Works |
|------|---------|--------------|
| **Smoking Gun Reveal** | "Here's what the document says..." | Evidence on screen = shareable |
| **Myth Bust Moment** | "You've heard X. It's wrong." | Controversy drives engagement |
| **Shocking Statistic** | "Not 300,000. The records show 1.27 million." | Numbers stick |
| **Quote Takedown** | "[Person] claimed X. The source says Y." | Debate format works |
| **Map Comparison** | "Look at 1916. Now look at today." | Visual proof is compelling |

### Output Format

```markdown
# CLIP SUGGESTIONS: [Video Title]

**Source Video:** [Title]
**Video Length:** [X:XX]
**Clips Identified:** [X]

## CLIP 1: [Clip Title]
**Timestamp:** [X:XX - X:XX]
**Duration:** [XX seconds]
**Type:** [Smoking Gun / Myth Bust / etc.]

### Script Excerpt
> [Exact text from script]

### Why This Works
- [Reason 1]
- [Reason 2]

### Hook (First 2 Seconds)
"[Opening line]"

### Suggested Clip Title
"[Short, punchy title]"

### Visual Notes
- [What to show]
- [Text overlay suggestion]

### Hashtags
#[tag1] #[tag2] #[tag3]

[Continue for all clips...]

## CLIP PRIORITY RANKING

| Rank | Clip | Viral Potential | Why |
|------|------|-----------------|-----|
| 1 | [Title] | High/Medium/Low | [Reason] |

## POSTING SCHEDULE

| Day | Clip | Platform | Best Time |
|-----|------|----------|-----------|
| Day 1 | Clip 1 | YouTube Shorts | Same as main |
| Day 2 | Clip 2 | TikTok | 7 PM EST |
```

---

## FULL WORKFLOW (`--full`)

Run complete publishing preparation:

1. Generate YOUTUBE-METADATA.md
2. Generate title variants section
3. Generate clip suggestions section

**All in one file** for easy reference.

---

## EXTERNAL INTELLIGENCE PROMPTS (`--prompts`)

Generate tailored, copy-paste-ready prompts for VidIQ Pro Coach and Google Gemini.

### How It Works

1. Reads the project script (02-SCRIPT-DRAFT.md or FINAL-SCRIPT.md)
2. Analyzes topic, entities (places, people, documents), and script structure
3. Loads competitor context from intel.db (if available — run /intel --refresh first for best results)
4. Generates 4 sequenced VidIQ Pro Coach prompts + 1 Gemini creative brief
5. Saves to EXTERNAL-PROMPTS.md in the project folder

### Workflow

```python
from tools.production.prompt_generator import generate_prompts
result = generate_prompts(project_path, script_path)
# Returns {'output_path': str} or {'error': str}
```

### Output: EXTERNAL-PROMPTS.md

Numbered prompts with explicit instructions:
- Step 1: Keyword Research -> VidIQ Pro Coach
- Step 2: Title Optimization -> VidIQ Pro Coach
- Step 3: Tag Strategy -> VidIQ Pro Coach
- Step 4: Description -> VidIQ Pro Coach
- Step 5: Creative Brief -> Google Gemini

Each prompt is copy-paste ready. Follow the numbered sequence — each builds on the previous response.

### After Running --prompts

Follow the steps in EXTERNAL-PROMPTS.md, then run `/publish --intake` to parse the responses.

---

## INTAKE PARSING (`--intake`)

Parse pasted VidIQ/Gemini responses into structured data for synthesis.

### Session Flow (Bulk Mode — Recommended)

1. System prompts: "Paste all your VidIQ/Gemini responses at once (or type 'single' for one-at-a-time mode)"
2. User pastes all responses (separated by step headers or --- dividers)
3. System auto-splits into segments and classifies each independently
4. System shows summary: "Detected 5 segments: keyword_data, title_suggestions, tag_set, description_draft, thumbnail_concepts. Confirm? [y/n]"
5. User confirms -> all saved to EXTERNAL-INTELLIGENCE.json
6. Auto-runs synthesis engine

### Session Flow (Single Mode — Fallback)

1. User types 'single' when prompted
2. System prompts: "Paste your VidIQ/Gemini response"
3-7. (Same as before: classify, preview, confirm, next or done)

### Workflow

```python
from tools.production.intake_parser import classify_bulk_paste, save_batch, classify_paste, save_session
from tools.production.synthesis_engine import synthesize

# Bulk mode (recommended):
results = classify_bulk_paste(pasted_text)
segments = split_bulk_paste(pasted_text)
# Show summary to user, get confirmation
save_batch(project_path, source='vidiq_pro_coach', classifications=results, segments=segments)

# Single mode (fallback):
classified = classify_paste(pasted_text)
save_session(project_path, source='vidiq_pro_coach', classified=classified, raw_text=pasted_text)

# After either mode:
result = synthesize(project_path, script_path)
```

### Auto-Detection Types

| Type | Detected By | Example Signal |
|------|-------------|----------------|
| keyword_data | Volume/competition numbers | "search volume: 12,000" |
| title_suggestions | Numbered title lists (40-70 chars) | "1. Spain's 300-Year Trap..." |
| thumbnail_concepts | Visual/compositional language | "Split screen with map overlay" |
| description_draft | Multi-paragraph YouTube prose | Paragraphs with hashtags |
| tag_set | Comma-separated keyword phrases | "gibraltar, treaty, spain, ..." |

### Source Labeling

When prompting for paste, ask which tool the response came from:
- "vidiq_pro_coach" (Steps 1-4 from --prompts)
- "gemini" (Step 5 from --prompts)

---

## SYNTHESIS (`--synthesize`)

Re-run synthesis on existing EXTERNAL-INTELLIGENCE.json (e.g., after adding more intake data).

### Workflow

```python
from tools.production.synthesis_engine import synthesize
result = synthesize(project_path, script_path)
# Returns {'output_path': str} or {'error': str}
```

### Output: METADATA-SYNTHESIS.md

3 title+thumbnail pairings designed for A/B testing, each with bridge analysis:

| Variant | Test Hypothesis | Optimized For | Bridge |
|---------|-----------------|---------------|--------|
| A: Keyword-Optimized | Search discoverability | VidIQ keyword data | Check vs hook |
| B: Curiosity Gap | Click-through intrigue | Gemini creative angles | Check vs hook |
| C: Authority Angle | Intellectual credibility | Script entities + evidence | Check vs hook |

**Each pairing must include:** thumbnail concept, paired title, hook excerpt, bridge verdict, and handoff description. Priority ordered by bridge tightness, not variant label.

Plus: one optimized description, one tag set, moderation scoring, thumbnail blueprints.

---

## Integration with Production Workflow

### Typical Sequence

```
[User edits video, exports final]
/publish --metadata [project]  # Generate metadata
/publish --titles [project]    # Title variants for testing
[User uploads to YouTube]
/publish --clips [project]     # Identify clips for promotion
```

### External Intelligence Workflow (NEW)

```
[Script is ready]
/publish --prompts [project]     # Generate VidIQ/Gemini prompts
[User follows EXTERNAL-PROMPTS.md steps, copies responses]
/publish --intake [project]      # Parse responses -> auto-synthesizes
[Review METADATA-SYNTHESIS.md — 3 variants ready for A/B testing]
/publish --metadata [project]    # Generate final metadata (now informed by synthesis)
```

### VidIQ Integration

- Use VidIQ title tester with generated variants
- Use VidIQ thumbnail generator with documented assets
- Use VidIQ keywords with generated tags
- User clips tool with identified moments

---

## POST-PUBLISH: Community Distribution Checklist (New — 2026-03-29)

**After uploading to YouTube, distribute to earned channels for search-to-browse conversion.**

Your content has academic citations and primary source analysis — it meets the quality bar for communities that reject typical YouTube history content. This is a free traffic source targeting the "Correctionist" audience segment (2.31% sub conversion).

### Distribution Template

After each publish, post to **2-3 relevant communities** using the document/evidence as the value proposition (NOT "watch my video"):

**Reddit (Primary — frame as contribution, not promotion):**

| Subreddit | When to Post | Framing |
|-----------|--------------|---------|
| r/AskHistorians | Untranslated/document topics | "I translated [document] that's never been in English. Here's what it says." + link |
| r/badhistory | Myth-busting/fact-check topics | "[Common myth] is wrong. Here's the primary source evidence." + summary + link |
| r/history | Any well-researched topic | Brief summary of the most surprising finding + link |
| r/geopolitics | Territorial disputes | Evidence-based analysis of [dispute] + link |
| r/MapPorn | Any video with map content | Map image from video + context in comment |
| **Topic-specific subs** | Country/region topics | e.g., r/Nigeria for Bakassi, r/Philippines for Sabah |

**Format for Reddit posts:**
```
Title: [Surprising finding from the video — NOT the YouTube title]
Body: [2-3 paragraph summary of the key evidence/finding]
       [Link to video at the END, framed as "full analysis here"]
```

**Key rules:**
- NEVER post just a link — provide substantive content in the post itself
- Frame as "I found/translated/read [source]" not "I made a video about"
- The DOCUMENT or FINDING is the value, not the video
- Wait 24h after YouTube publish (gives algorithm time to index)
- Max 2-3 subreddits per video — don't spam

**Newsletter cross-post (if article exists):**
- Publish Substack article within 48h of YouTube upload
- Add YouTube embed at the top of the article
- Substack Notes with the most surprising quote + link

**Add to YOUTUBE-METADATA.md:**
```
## Distribution Plan
- Reddit: [subreddit 1] — [framing angle]
- Reddit: [subreddit 2] — [framing angle]
- Newsletter: [article ready? Y/N]
- Topic-specific: [community if applicable]
```

---

## Reference Files

- **Thumbnail framework:** `.claude/REFERENCE/THUMBNAIL-EVALUATION-FRAMEWORK.md`
- **VidIQ filter:** `.claude/REFERENCE/VIDIQ-CHANNEL-DNA-FILTER.md`
- **Title database:** `channel-data/COMPETITOR-TITLE-DATABASE.md`
- **Technique library:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` PART 5 (Techniques Toolkit)
- **Technique log:** `channel-data/TECHNIQUE-USAGE-LOG.md`
- **Metadata checker:** `tools/discovery/metadata_checker.py`
- **Prompt generator:** `tools/production/prompt_generator.py`
- **Intake parser:** `tools/production/intake_parser.py`
- **Synthesis engine:** `tools/production/synthesis_engine.py`

---

## POST-PUBLISH: Technique Evaluation (`--evaluate`)

**When to run:** 7-14 days after publishing (when retention data is available)

### Evaluate Technique Effectiveness

1. **What techniques did you use?**
   - List techniques from WRITING-VOICE-AND-STYLE.md PART 5 used in this video
   - Note which script sections used which techniques

2. **How did they perform?**
   - Check retention graph in YouTube Studio
   - Note retention % at sections where techniques were applied
   - Rate each technique 1-5 (see scale in TECHNIQUE-USAGE-LOG.md)

3. **Update the log:**
   - Add row(s) to `channel-data/TECHNIQUE-USAGE-LOG.md`
   - Include: date, video slug, technique, section, retention %, rating, notes

4. **Update the library (optional):**
   - If technique worked well, update "Effectiveness" in WRITING-VOICE-AND-STYLE.md PART 5
   - If technique failed, note why in the library entry

> **Proactive:** "It's been [X] days since [video] published. Ready to evaluate technique effectiveness? I can help you log which techniques worked."

### Evaluation Workflow

```
/publish --evaluate [video-slug]
```

This prompts for:
1. Which techniques were used
2. Retention data at technique points
3. 1-5 rating for each
4. Auto-updates TECHNIQUE-USAGE-LOG.md

---

## Absorbed Commands

This command consolidates functionality from:
- `/youtube-metadata` - Full metadata generation
- `/test-titles` - Title variant generation
- `/clip-suggestions` - Clip identification for Shorts

All original functionality preserved through flags.
