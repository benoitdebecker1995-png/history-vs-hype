---
description: Keyword research and metadata validation for discovery optimization
model: haiku
---

# /discover - Discovery & Keyword Research

Comprehensive keyword research workflow and metadata validation for YouTube discoverability.

## Usage

```
/discover TOPIC                   # Full keyword research workflow
/discover --autocomplete "phrase" # Extract autocomplete suggestions
/discover --intent "query"        # Classify search intent
/discover --check FILE            # Pre-publish metadata validation
/discover --vidiq "topic"         # VidIQ guided workflow
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--autocomplete` | YouTube autocomplete suggestions | `/discover --autocomplete "medieval history"` |
| `--intent` | Classify search intent | `/discover --intent "dark ages myth"` |
| `--check` | Validate metadata consistency | `/discover --check YOUTUBE-METADATA.md` |
| `--vidiq` | VidIQ data collection guide | `/discover --vidiq "crusades"` |
| `--save` | Save results to database | `/discover TOPIC --save` |
| `--json` | Output JSON format | `/discover --autocomplete "topic" --json` |
| `-q` | Quiet mode (no status messages) | `/discover TOPIC -q` |

---

## FULL KEYWORD RESEARCH (Default)

**When to use:** Planning new video, optimizing metadata pre-publish

### Step 1: Autocomplete Extraction

Extract YouTube autocomplete suggestions for seed phrase.

**What it finds:**
- Real searches people are typing
- Long-tail variations
- Related topics
- Question patterns ("why...", "how...", "what...")

**Execution:**
```bash
cd tools/discovery && python autocomplete.py "seed phrase"
```

### Step 2: Search Intent Classification

Analyze what type of content searchers expect.

**Intent types:**
- **Educational** - "Explain", "History of", "What is"
- **Comparison** - "vs", "difference between"
- **Verification** - "Is X true", "Did Y happen", "Fact check"
- **Opinion** - "Best", "Worst", "Should"
- **Tutorial** - "How to", "Guide"

**Why it matters:** Your content format must match search intent or viewers bounce.

**Execution:**
```bash
cd tools/discovery && python intent_mapper.py "search query"
```

### Step 3: VidIQ Research (Manual)

Guided workflow for VidIQ data collection.

**Data to collect:**
- Search volume
- Competition score
- Related keywords
- Competitor analysis

**Since VidIQ has no API, this generates prompts for manual collection.**

**Execution:**
```bash
cd tools/discovery && python vidiq_workflow.py "topic"
```

### Step 4: Keyword Selection

Combine data from Steps 1-3 to choose:

**Primary keyword (title):**
- High volume (>1000/month)
- Low competition (<50)
- Matches your content

**Secondary keywords (description):**
- Related terms
- Long-tail variations
- Question formats

**Tags:**
- Mix of high/medium/low volume
- Include exact matches from autocomplete
- Add related topics

### Output

Full keyword research saved to project folder or `channel-data/keyword-research/`.

---

## AUTOCOMPLETE EXTRACTION (`--autocomplete`)

Extract YouTube autocomplete suggestions for a seed phrase.

### How It Works

Uses browser automation (pyppeteer) to:
1. Load YouTube search
2. Type seed phrase
3. Capture autocomplete dropdown
4. Extract all suggestions

**Rate limits:** 2-5 second delays between requests (YouTube may block if too fast)

### Usage

```bash
# Basic extraction
/discover --autocomplete "medieval history"

# Save to database
/discover --autocomplete "dark ages" --save

# JSON output
/discover --autocomplete "crusades" --json --save
```

### Example Output

```markdown
# Autocomplete Suggestions: medieval history

**Seed phrase:** medieval history
**Suggestions found:** 12
**Timestamp:** 2026-01-29T18:00:00

## Suggestions

1. medieval history documentary
2. medieval history podcast
3. medieval history explained
4. medieval history myths
5. medieval history primary sources
6. medieval history vs reality
...
```

### Execution

```bash
cd tools/discovery && python autocomplete.py "seed phrase" [--save] [--json]
```

**Requirements:**
- pyppeteer installed: `pip install pyppeteer`
- Chromium auto-downloads on first run

---

## SEARCH INTENT CLASSIFICATION (`--intent`)

Classify search intent to match content format to user expectations.

### Intent Categories

| Intent | User Wants | Video Format | Example |
|--------|-----------|--------------|---------|
| Educational | Learn concept | Explainer | "What is the dark ages" |
| Verification | Confirm/deny | Fact-check | "Did crusades defend Europe" |
| Comparison | Contrast options | Comparative analysis | "Medieval vs Renaissance" |
| Opinion | Perspective | Commentary | "Best medieval battle" |
| Tutorial | Step-by-step | How-to | "How to read medieval manuscripts" |

### Why It Matters

**Mismatch = Bounce:**
- User searches "Is X true" → expects definitive answer
- Video provides "History of X" → user leaves (retention drops)

**Match = Retention:**
- User searches "Dark ages myth" → expects debunking
- Video provides "Fact-checking dark ages claims" → user stays

### Usage

```bash
# Classify single query
/discover --intent "medieval history facts"

# Batch classification
/discover --intent "dark ages myth" --intent "crusades defensive" --intent "medieval literacy"

# Save to database
/discover --intent "query" --save
```

### Example Output

```markdown
# Search Intent: medieval history facts

**Query:** medieval history facts
**Primary Intent:** Educational
**Confidence:** High
**Secondary Intent:** Verification (low confidence)

## Analysis

**User Expectations:**
- Learn factual information about medieval period
- Structured presentation of key facts
- Credible sources

**Content Format Match:**
- ✓ Educational explainer
- ✓ Documentary style
- ~ Fact-check (if challenging common beliefs)
- ✗ Opinion/commentary

**Recommendation:**
Structure as educational content with clear sections, primary sources, and factual presentation. Consider including myth-busting if addressing misconceptions.
```

### Execution

```bash
cd tools/discovery && python intent_mapper.py "search query" [--save] [--json]
```

**Note:** Requires NLP model (spaCy or lightweight alternative).

---

## METADATA VALIDATION (`--check`)

**CRITICAL PRE-PUBLISH GATE**

Validate metadata consistency before uploading to YouTube. Catches common issues that hurt discoverability.

### What It Checks

**HIGH Priority (Blocks publish if failed):**
1. Primary keyword in title
2. Primary keyword in description (first 200 chars)
3. Keyword stuffing detection (>2% density = spam)

**MEDIUM Priority:**
4. Primary keyword in tags
5. Title-tag overlap (consistency check)

**WARNING Priority:**
6. Description length (200+ words recommended)
7. Tag count (5-30 recommended)

### Usage

```bash
# Check YOUTUBE-METADATA.md file
/discover --check video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025/YOUTUBE-METADATA.md

# Check from command line
/discover --check --title "Title" --description "Desc" --tags "tag1,tag2,tag3"

# Specify primary keyword
/discover --check YOUTUBE-METADATA.md --keyword "medieval history"

# JSON output
/discover --check YOUTUBE-METADATA.md --json
```

### Example Output

```markdown
# Metadata Consistency Check

**Status:** [PASS] Metadata is consistent (2 warnings)

## Statistics

- **Primary keyword:** medieval history
- **Title length:** 58 characters
- **Description length:** 247 words
- **Tag count:** 12
- **Title keyword density:** 10.3%
- **Description keyword density:** 1.2%
- **Title-tag overlap:** 4 words (medieval, history, myths, europe)

## Issues Found

### WARNING Priority

**Description length**
- Problem: Description has 247 words (recommended: 200+)
- Fix: Expand description for better context and SEO

**Tag count**
- Problem: Only 12 tags (recommended: 5-30)
- Fix: Add more relevant tags
```

### Execution

```bash
cd tools/discovery && python metadata_checker.py --file YOUTUBE-METADATA.md
```

**Integration with /publish:**
Metadata check runs automatically before publishing (see `/publish` command).

---

## VIDIQ WORKFLOW (`--vidiq`)

**Since VidIQ has no public API**, this provides guided prompts for manual data collection.

### 3-Step Workflow

**Step 1: Primary Keyword Research**
- Go to VidIQ Keyword Inspector
- Search for your topic
- Record: search volume, competition, overall score, trend

**Step 2: Related Keywords**
- Find related keywords with:
  - High volume (>1000/month)
  - Low competition (<50)
  - Relevance to your topic

**Step 3: Competitor Analysis**
- Search YouTube for your topic
- Use VidIQ extension on top videos
- Record: titles, tags, view counts, VidIQ scores

### Usage

```bash
# Generate research prompts
/discover --vidiq "medieval history"

# Save to specific project
/discover --vidiq "dark ages myth" --project-folder "video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025"

# Interactive data collection
/discover --vidiq "crusades" --save
```

### Example Output

```markdown
# VidIQ Research Workflow: medieval history

**Topic:** medieval history
**Started:** 2026-01-29T18:00:00

---

## Step 1: Search Primary Keyword

1. Go to VidIQ Keyword Inspector
2. Search for: "medieval history"
3. Record the following data:

### Data to Collect

**Search Volume** (`search_volume`)
- Monthly searches
- Example: `12000`

**Competition Score** (`competition`)
- VidIQ competition rating (0-100)
- Example: `67`

...
```

### Execution

```bash
cd tools/discovery && python vidiq_workflow.py "topic" [--save] [--project-folder "path"]
```

**Output:** Markdown prompts or saved JSON data (if using `--save`).

---

## INTEGRATION WITH WORKFLOW

### Pre-Production (Topic Planning)

```
/discover "potential topic"
  → Extract autocomplete suggestions
  → Classify search intent
  → Generate VidIQ research prompts
  → Choose primary keyword based on volume/competition
```

### Pre-Publish (Quality Gate)

```
/discover --check YOUTUBE-METADATA.md
  → Validate keyword consistency
  → Check for keyword stuffing
  → Verify title-tag overlap
  → [PASS] or [FAIL] with specific issues
```

### Post-Publish (Performance Tracking)

```
# Keywords stored in database for later analysis
# Compare search volume vs actual traffic
# Identify which keywords drove views
```

---

## DATABASE TRACKING

All keyword research saved to `tools/discovery/keywords.db`.

**Schema:**
- `keywords` - Autocomplete suggestions with frequency
- `intents` - Search intent classifications
- `performance` - Post-publish keyword performance

**Query database:**
```bash
cd tools/discovery && python keywords.py search "medieval"
cd tools/discovery && python keywords.py export --format csv
```

---

## REQUIREMENTS

**Python packages:**
```bash
pip install pyppeteer  # Autocomplete extraction
pip install spacy      # Intent classification (optional)
```

**Browser:**
- Chromium auto-downloads on first pyppeteer run
- Alternatively: use existing Chrome/Chromium installation

**VidIQ:**
- VidIQ Pro account (for search volume data)
- VidIQ browser extension installed

---

## RELATED COMMANDS

- `/publish` - Uses metadata checker as pre-publish gate
- `/research` - Topic research (uses autocomplete for validation)
- `/analyze` - Post-publish performance (compares keyword predictions vs actual)

---

## REFERENCE FILES

- **Keyword database:** `tools/discovery/keywords.db`
- **VidIQ channel filter:** `.claude/REFERENCE/VIDIQ-CHANNEL-DNA-FILTER.md`
- **Title database:** `channel-data/COMPETITOR-TITLE-DATABASE.md`
- **Topic patterns:** `.claude/OUTLIER-TOPIC-IDEAS.md`

---

## NOTES

**Why manual VidIQ workflow?**
- VidIQ has no public API
- Browser automation would violate TOS
- Manual collection ensures accuracy and compliance

**Keyword stuffing threshold:**
- 2% density is industry standard
- YouTube penalizes excessive repetition
- Checker flags both title and description separately
