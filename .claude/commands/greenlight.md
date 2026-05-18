---
description: Pre-work viability gate — checks demand, titles, and thumbnails BEFORE you invest time
model: sonnet
---

# /greenlight — Will This Get Views?

**Purpose:** Single gate that answers "should I make this video?" BEFORE research/scripting begins. Combines demand validation, title scoring, and thumbnail enforcement.

**Philosophy:** The old workflow asked "will this get views?" after 20+ hours of work. This command asks it FIRST.

## Usage

```
/greenlight "why is haiti so poor"           # Check a topic idea
/greenlight --project 21-haiti-debt          # Check existing project
/greenlight --full "scramble for africa"     # Full check: demand + title gen + thumbnail concept
/greenlight --scan                           # Proactive: scan for high-demand opportunities
```

## Flags

| Flag | Purpose |
|------|---------|
| *(default)* | Quick demand + title check |
| `--project` | Check existing project (reads YOUTUBE-METADATA.md) |
| `--full` | Packaging research + title gen + thumbnail concepts |
| `--compare A B` | Compare two topic ideas side by side |
| `--no-research` | Skip packaging research step (quick mode, algorithmic only) |
| `--scan` | Proactive opportunity scan (autocomplete + competitor gaps + Trends) |

---

## SCAN MODE (`--scan`) — Proactive Opportunity Discovery

**When to use:** Run weekly to surface high-demand topics matching channel DNA — instead of waiting for inspiration. Folded in from former `/discover --scan` (2026-05-03).

```bash
/greenlight --scan                  # Top 10 opportunities
/greenlight --scan --limit 20       # More results
/greenlight --scan --json           # Machine-readable
/greenlight --scan --verbose        # Per-seed progress
```

**Execution:**
```bash
python -m tools.discovery.discovery_scanner [--limit N] [--json] [--verbose]
```

**Runtime:** ~90-120s (browser automation + rate limiting between seed keywords).

**What it does:**
1. **Autocomplete mining** — runs 15 channel-DNA seeds through YouTube autocomplete; position 1 = demand 100, position 10 = 60.
2. **Competitor gap detection** — flags topics with competitor views ≥ 2× channel average that the channel hasn't covered.
3. **Google Trends pulse** — breakout (>5000% = +15) and rising (>100%) flags.
4. **Deduplication** — removes topics already in `_IN_PRODUCTION/`, `_ARCHIVED/`, or in `keywords.db` SCRIPTING/FILMED/PUBLISHED states.
5. **Extended Belize scoring** — demand (25%) + map angle (20%) + news hook (15%) + no competitor (20%) + conversion potential (20%).
6. **Writes** ranked report to `channel-data/DISCOVERY-FEED.md` — table + per-opportunity details + signal quality transparency.

After `--scan`, run `/greenlight "<top opportunity>"` on any candidate that catches your eye for the full demand + title + thumbnail check.

---

## WORKFLOW

### Step 0: Packaging Research (runs on `--full`, skipped on `--no-research`)

**Purpose:** Before generating titles in a vacuum, find out what already exists on this topic and what packaging worked. Titles informed by competitive intelligence beat titles generated algorithmically.

**0A. Competitor Landscape Scan (web search)**

Search for existing YouTube coverage:
```
"[topic]" site:youtube.com
"[topic]" explained OR history site:youtube.com
```

Extract the **top 5 results**:
- Title (exact text)
- Channel name
- View count (from snippet)
- Upload date (estimate from snippet)

**Display:**
```
COMPETITOR LANDSCAPE:
  1. "How France Made Haiti Pay" — Knowing Better — 1.2M views
  2. "Haiti's Debt to France Explained" — Vox — 3.8M views
  3. "Why Is Haiti So Poor?" — RealLifeLore — 2.1M views
  ---
  MOST-VIEWED TITLE PATTERN: How/Why question (2 of top 3)
  COMMON ANGLE: economic exploitation narrative
  GAP: Nobody covers the specific treaty clauses or original documents
```

**0B. NotebookLM Packaging Intelligence (if packaging notebook exists)**

Query the packaging intelligence notebook (see setup guide: `tools/PACKAGING-NOTEBOOK-GUIDE.md`):

```
What angles and framing have worked for [TOPIC TYPE: territorial/ideological/colonial]
topics in this niche? Which title patterns got the most views? What's the gap
in how this topic type is usually covered?
```

If no packaging notebook exists, skip this step and note: "Set up packaging notebook for richer insights — see `tools/PACKAGING-NOTEBOOK-GUIDE.md`"

**0C. Angle Recommendation**

Based on 0A + 0B, recommend the packaging angle BEFORE title generation:

```
PACKAGING INTEL:
  Competitors: 5 videos found, best at 3.8M views
  Common angle: economic exploitation narrative (4 of 5)
  Gap: No one shows the actual treaty text or payment receipts
  Your edge: Primary source documents on screen (unique in niche)
  
  RECOMMENDED ANGLE: "Document reveal" — show the actual receipts France collected
  TITLE DIRECTION: Declarative with evidence promise (e.g., "France Collected from Haiti for 122 Years. We Found Every Receipt.")
```

This angle recommendation feeds directly into Step 2 (Title Generation) — titles should be generated FROM the angle, not in a vacuum.

---

### Step 1: Demand Check (HARD GATE)

Run demand_checker first. If it returns CAUTION with "No matching keywords" (i.e., the topic isn't in keywords.db), fall back to the composite demand_scorer which uses YouTube autocomplete + pytrends + YouTube API:

```python
from tools.preflight.demand_checker import run as demand_check
result = demand_check("topic keywords here")

# If DB has no data, use composite scorer (free sources, no VidIQ needed)
if result["verdict"] == "CAUTION" and not result["keyword_matches"]:
    from tools.preflight.demand_scorer import composite_score
    scored = composite_score("topic keywords here")
    # Use scored["verdict"], scored["estimated_volume"], scored["reasons"]
```

**Decision:**
- **GO** (≥1,000/mo search volume): Proceed to Step 2
- **CAUTION** (200-999/mo): Warn user — "This topic has marginal demand. Proceed only if you have a strong angle."
- **STOP** (<200/mo or no data): **HARD BLOCK** — "Do not invest time in this topic. Find a higher-demand angle."

**If STOP:** Suggest related keywords from keywords.db that DO have volume. Show the user what people actually search for. Reference `.claude/REFERENCE/vidiq-unicorn-keywords.md` for pre-vetted keyword opportunities.

**News hook check (auto-run after demand):**
```python
import subprocess
result = subprocess.run(
    ['python', '-m', 'tools.discovery.news_hook_monitor', '--topic', topic_keywords],
    capture_output=True, text=True
)
# If URGENT or TRENDING, upgrade CAUTION→GO or add "TIMELY" badge
```
A strong news hook can upgrade a marginal-demand topic: "CAUTION + URGENT news hook = GO (timely)."

**Display:**
```
DEMAND: GO ✓ (4,299/mo — "why is haiti so poor")
NEWS HOOK: TRENDING (3 articles this week)
```

### Step 2: Title Viability Check

If the user provided a specific title, score it using DB-enriched scoring:

```python
from tools.title_scorer import score_title
from tools.discovery.database import KeywordDB

db = KeywordDB()
title = "Why Is Haiti So Poor? France Collected for 122 Years"
result = score_title(title, db_path=db.db_path)
db.close()
```

**Curiosity Check:** After running the mechanical `title_scorer`, you MUST run `/curiosity "[Title]"` to get the emotional hook score.

If no title provided, generate candidates using:
1. The topic + search keywords
2. **The packaging research angle from Step 0** (if available) — titles MUST reflect the recommended angle, not generic framings
3. Competitor title patterns from Step 0A — differentiate from what already exists

**Outlier pattern check:** Run `python -m tools.benchmark.outlier_title_dissector --score "Title"` to score against proven niche outlier patterns (scale words, specificity, country names = higher lift).

**Title generation rules (from PACKAGING_MANDATE.md):**
1. Title MUST include the exact search keyword (or close variant)
2. Title MUST use versus, declarative, or how/why pattern
3. Title MUST score 65+ on `title_scorer.py` AND 60+ on the `/curiosity` check (The Emotional Hook check)
4. Title MUST NOT contain years, colons, or "The X That Y"
5. Title MUST set up a clear paradox (Specific Subject + Common Belief + Contradiction) that can be resolved in the first 5 seconds of the video.

**Traffic-optimized title selection (from TRAFFIC-SOURCE-ANALYSIS.md):**
- **Search-optimized topics** (evergreen, high search volume): Prefer **How/Why** pattern — gets 26.4% search traffic (2x declarative)
- **Browse-optimized topics** (trending, algorithm push): Prefer **Declarative** pattern — 3.8% CTR maximizes Browse clicks
- **Territorial topics** are 42% subscriber-dependent. For new viewer reach, optimize description first 2 lines for geographic search keywords.

Generate 5-8 candidates, score all, present ranked. Show DB enrichment status:

```
TITLE CANDIDATES:
  85/A  France vs Haiti. 122 Years of Forced Payments.        (versus, DB-enriched)
  65/B  Why Is Haiti So Poor? France Collected for 122 Years.  (how_why, static scores)
  75/B  Haiti Paid France for 122 Years. Here's Every Receipt. (declarative, DB-enriched)
```

**If no candidate scores 65+:** Flag as REVIEW — "Title needs work before proceeding."

### Step 3: Thumbnail Concept Check

If checking an existing project (`--project`), read YOUTUBE-METADATA.md:

```python
from tools.preflight.thumbnail_checker import check_project
result = check_project("video-projects/_IN_PRODUCTION/21-haiti-independence-debt-2025")
```

If checking a new topic (`--full`), generate 3 thumbnail concepts following PACKAGING_MANDATE:

**Template (auto-generate for any topic):**

```
**Concept A: Map + Text** (for territorial topics)
- [Geographic view showing the two sides of the story]
- Color contrast: [Side A color] vs [Side B color]
- Bold text overlay: 2-4 word declarative phrase (e.g. "BORDER ERASED")
- No talking-head face

**Concept B: Historical Visual + Text** (for myth-busting topics)
- [Historical photo, document close-up, or conceptual visual]
- Bold text overlay: topic word or short phrase (e.g. "THE MEMO")
- No talking-head face

**Concept C: Document + Text**
- [Primary source document or evidence visual]
- Text overlay highlighting the key claim/revelation
- No talking-head face
```

Then run the checker on the generated concepts.

### Step 3b: Audience Segment + Format Tag (New — 2026-03-29)

After demand, title, and thumbnail checks, classify the video:

**Audience Segment (from Gemini research, mapped to channel data):**

| Segment | Description | Your Content Type | Sub Conversion | Signal |
|---------|-------------|-------------------|----------------|--------|
| **Correctionist** | Wants to debunk myths, share truth | Ideological/fact-check | **2.31%** (best) | Subscriber engine |
| **Lifelong Learner** | Seeking knowledge, evidence density | Territorial/mechanism | 0.65% | View engine |
| **Identity-Seeker** | Connection to heritage, marginalized voices | Colonial/untranslated | 0.67% | Niche loyalty |
| **Inspiration-Seeker** | Emotional resonance, human resilience | Person-centered | Unknown | Untested |

Tag the video with its primary segment. Display in verdict:
```
AUDIENCE: Correctionist (myth-busting → high sub conversion expected)
```

**Format Template Match:**

Check against FORMAT-TEMPLATES.md. If the topic fits a template, recommend it:
```
FORMAT: PILOT EPISODE (testing new geographic audience — use 8-10 min strict cap)
```

If testing a new topic/audience/genre, ALWAYS recommend PILOT EPISODE format.

**Pilot Flag:**

If this is the channel's FIRST video in this topic area or geographic audience, add:
```
⚡ PILOT MODE: First video targeting [audience/region]. Use PILOT EPISODE format.
   Phase 1 research only. No book purchases until pilot proves demand.
   Success criteria: >30% retention AND >2x avg views after 2 weeks.
```

### Step 4: Composite Verdict

Combine all checks into a single verdict:

```
╔══════════════════════════════════════════════════╗
║  GREENLIGHT VERDICT: GO / REVIEW / STOP          ║
╠══════════════════════════════════════════════════╣
║  Packaging: 5 competitors, gap found ✓           ║
║  Angle:     "Document reveal — original receipts" ║
║  Demand:    GO ✓  (4,299/mo)                     ║
║  Title:     GO ✓  (85/A — versus, DB-enriched)   ║
║  Thumbnail: GO ✓  (90/100 — map-based)           ║
╠══════════════════════════════════════════════════╣
║  → Proceed to /research --new                    ║
╚══════════════════════════════════════════════════╝
```

When DB enrichment is unavailable (no CTR data ingested yet), display:
```
║  Title:     GO ✓  (85/A — versus, static scores) ║
```

**Verdict logic:**
- **GO:** Demand ≥ GO AND best title ≥ 65 AND thumbnail ≥ 60
- **REVIEW:** Any component is CAUTION/REVIEW but none is STOP/FAIL
- **STOP:** Demand = STOP OR best title < 40 OR thumbnail = FAIL

### Step 5: Next Action

Based on verdict, tell the user exactly what to do:

- **GO:** "Run `/research --new [topic]` to start the project. Use title '[best title]' as your working title."
- **REVIEW:** "Fix these issues first: [list]. Then re-run `/greenlight`."
- **STOP:** "Don't make this video. Here are higher-demand alternatives: [suggest 3 from keywords.db]"

---

## FOR EXISTING PROJECTS (`--project`)

When checking an existing project:

1. Read YOUTUBE-METADATA.md for titles and thumbnail concepts
2. Read PROJECT-STATUS.md for current phase
3. Run all 3 checks against what exists
4. If the project is past research phase and fails demand check, warn: "You've already invested time. Consider pivoting the title/angle to capture search demand rather than abandoning."

---

## COMPARE MODE (`--compare`)

Side-by-side comparison of two topic ideas:

```
/greenlight --compare "scramble for africa" "why is africa poor"
```

Output:
```
                    | scramble for africa | why is africa poor
--------------------|--------------------|-----------------
Demand              | 21,792/mo GO       | 4,855/mo GO
Competition         | Low                | Medium
Best title score    | 85/A               | 75/B
Recommendation      | ← START HERE       |
```

---

## INTEGRATION WITH OTHER COMMANDS

- `/greenlight` → GO → `/research --new` (project creation)
- `/greenlight --project` → after scripting, before filming
- `/preflight` → after scripting, final quality gate (more comprehensive)
- `/greenlight` is the FIRST check. `/preflight` is the LAST check.

---

*This command enforces PACKAGING_MANDATE.md. No video should begin production without passing greenlight.*
