---
description: YouTube metadata, title testing, clip suggestions (Post-production Phase 1)
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
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--metadata` | Full YouTube metadata package | `/publish --metadata 19-flat-earth-medieval-2025` |
| `--titles` | Title variants for VidIQ testing | `/publish --titles 19-flat-earth-medieval-2025` |
| `--clips` | Clip suggestions for Shorts/TikTok | `/publish --clips 19-flat-earth-medieval-2025` |
| `--full` | All three workflows | `/publish --full 19-flat-earth-medieval-2025` |

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

## Integration with Production Workflow

### Typical Sequence

```
[User edits video, exports final]
/publish --metadata [project]  # Generate metadata
/publish --titles [project]    # Title variants for testing
[User uploads to YouTube]
/publish --clips [project]     # Identify clips for promotion
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

---

## Absorbed Commands

This command consolidates functionality from:
- `/youtube-metadata` - Full metadata generation
- `/test-titles` - Title variant generation
- `/clip-suggestions` - Clip identification for Shorts

All original functionality preserved through flags.
