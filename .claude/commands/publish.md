---
description: YouTube metadata, title testing, clip suggestions (Post-production Phase 1)
model: sonnet
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

**Before generating final metadata, run validation checks:**

### Metadata Consistency Check

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

#### 1. Title Options (3 variations)

**Requirements:**
- 50-60 characters (mobile-friendly)
- Factually accurate
- Documentary tone
- Include main hook/myth

**SEO Keyword Pivoting:**
- If primary keyword has zero search volume, pivot to related high-volume terms
- Put dead keywords in description/tags, not title
- Example: "Crusades fact-check" (0 volume) → "Jerusalem 1099: What Crusaders Really Wrote"

#### 2. Description

**First 3 Lines (Frontload Keywords):**
- Line 1: Primary keyword + video format
- Line 2: Specific event/topic with keywords
- Line 3: Method/sources used

**Rest of Description:**
- Structured breakdown with timestamps
- ALL sources cited with specific references
- Academic sources, primary documents
- Natural language (NOT keyword stuffing)
- CTA for subscription

**Example opening:**
```
A primary-source fact-check of viral claims that the Crusades were "awesome."
Using only what crusaders themselves wrote about the 1099 siege of Jerusalem.
We read the medieval chronicles (Fulcher of Chartres, Raymond d'Aguilers) to see what really happened.
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

#### 5. Thumbnail Strategy Notes

**For VidIQ thumbnail generation, document:**

1. Core topic (specific event/dispute)
2. Video format (Short or longform)
3. Visual assets available:
   - Maps (which regions)
   - Primary documents
   - Modern hooks
   - Face vs. no face preference
4. Working title/main keywords
5. Channel's thumbnail style:
   - Best performers
   - Clean documentary aesthetic
   - Color palette

**DO NOT generate actual thumbnail mockups.**

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
1. [Title] (XX characters)
   - Hook: [Why this works]
   - Risk: [Potential issue]

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

## TITLE + THUMBNAIL ALIGNMENT

**Title implies:** [What viewer expects]
**Thumbnail must show:** [Visual that matches]
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

### Session Flow

1. System prompts: "Paste your VidIQ/Gemini response"
2. User pastes raw text
3. System auto-detects type (keyword data, titles, thumbnails, description, tags)
4. System shows preview: "Detected: keyword data (8 keywords). First: 'gibraltar history (12,000 vol)'. Confirm? [y/n]"
5. User confirms -> saved to EXTERNAL-INTELLIGENCE.json
6. System prompts for next paste, or user types 'done'
7. On 'done': auto-runs synthesis engine

### Workflow

```python
from tools.production.intake_parser import classify_paste, save_session, load_or_create_intelligence
from tools.production.synthesis_engine import synthesize

# For each paste:
classified = classify_paste(pasted_text)
# Show preview to user, get confirmation
save_session(project_path, source='vidiq_pro_coach', classified=classified, raw_text=pasted_text)

# After 'done':
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

3 title+thumbnail pairings designed for A/B testing:

| Variant | Test Hypothesis | Optimized For |
|---------|-----------------|---------------|
| A: Keyword-Optimized | Search discoverability | VidIQ keyword data |
| B: Curiosity Gap | Click-through intrigue | Gemini creative angles |
| C: Authority Angle | Intellectual credibility | Script entities + evidence |

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

## Reference Files

- **Thumbnail framework:** `.claude/REFERENCE/THUMBNAIL-EVALUATION-FRAMEWORK.md`
- **VidIQ filter:** `.claude/REFERENCE/VIDIQ-CHANNEL-DNA-FILTER.md`
- **Title database:** `channel-data/COMPETITOR-TITLE-DATABASE.md`
- **Technique library:** `.claude/REFERENCE/PROVEN-TECHNIQUES-LIBRARY.md`
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
   - List techniques from PROVEN-TECHNIQUES-LIBRARY.md used in this video
   - Note which script sections used which techniques

2. **How did they perform?**
   - Check retention graph in YouTube Studio
   - Note retention % at sections where techniques were applied
   - Rate each technique 1-5 (see scale in TECHNIQUE-USAGE-LOG.md)

3. **Update the log:**
   - Add row(s) to `channel-data/TECHNIQUE-USAGE-LOG.md`
   - Include: date, video slug, technique, section, retention %, rating, notes

4. **Update the library (optional):**
   - If technique worked well, update "Effectiveness" in PROVEN-TECHNIQUES-LIBRARY.md
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
