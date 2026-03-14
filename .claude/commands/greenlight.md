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
```

## Flags

| Flag | Purpose |
|------|---------|
| *(default)* | Quick demand + title check |
| `--project` | Check existing project (reads YOUTUBE-METADATA.md) |
| `--full` | Generate title candidates + thumbnail concepts |
| `--compare A B` | Compare two topic ideas side by side |

---

## WORKFLOW

### Step 1: Demand Check (HARD GATE)

Run demand_checker against the topic:

```python
from tools.preflight.demand_checker import run as demand_check
result = demand_check("topic keywords here")
```

**Decision:**
- **GO** (≥1,000/mo search volume): Proceed to Step 2
- **CAUTION** (200-999/mo): Warn user — "This topic has marginal demand. Proceed only if you have a strong angle."
- **STOP** (<200/mo or no data): **HARD BLOCK** — "Do not invest time in this topic. Find a higher-demand angle."

**If STOP:** Suggest related keywords from keywords.db that DO have volume. Show the user what people actually search for.

**Display:**
```
DEMAND: GO ✓ (4,299/mo — "why is haiti so poor")
```

### Step 2: Title Viability Check

If the user provided a specific title, score it using DB-enriched scoring:

```python
from tools.title_scorer import score_title
from tools.discovery.database import KeywordDB

db = KeywordDB()
result = score_title("Why Is Haiti So Poor? France Collected for 122 Years", db_path=db.db_path)
db.close()
```

If no title provided, generate candidates using the topic + search keywords:

**Title generation rules (from PACKAGING_MANDATE.md):**
1. Title MUST include the exact search keyword (or close variant)
2. Title MUST use versus, declarative, or how/why pattern
3. Title MUST score 65+ on title_scorer.py
4. Title MUST NOT contain years, colons, or "The X That Y"

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
**Concept A: Split-Map**
- [Geographic view showing the two sides of the story]
- Color contrast: [Side A color] vs [Side B color]
- No text, no face

**Concept B: Arrow/Flow Map**
- [Map showing movement, extraction, influence, or control]
- Bold arrows or lines showing direction of action
- No text, no face

**Concept C: Document on Map**
- [Geographic map as background]
- Key document overlaid at angle
- Highlight on the critical text/number
```

Then run the checker on the generated concepts.

### Step 4: Composite Verdict

Combine all three checks into a single verdict:

```
╔══════════════════════════════════════════════════╗
║  GREENLIGHT VERDICT: GO / REVIEW / STOP          ║
╠══════════════════════════════════════════════════╣
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
