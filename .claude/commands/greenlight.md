---
description: Pre-work viability gate — checks demand, titles, and thumbnails BEFORE you invest time
model: opus
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

### Step −1: Collision pre-flight (ALWAYS — runs first, before anything else)

**Have we already done this?** Runs on every invocation including quick checks. Costs one command.

```bash
python -m tools.preflight.candidate_preflight "<topic>"
```

- **`COLLISION`** (published-title match, exit 1) → **STOP.** Report the video ID and date and ask
  whether this is a deliberate revisit. Do not proceed to demand checks.
- **`FLAG`** (existing project in `_IN_PRODUCTION` / `_READY_TO_FILM` / `_BACKLOG` / `_ARCHIVED`) →
  continue, but **say so in the verdict**. Existing projects are eligible on merit; banked research
  lowers cost. Silence about a collision is the failure mode.
- **`CLEAR`** → continue to Step 0.

*Why this is a code step and not a reminder: the rule already existed in prose in
`.claude/PROMPTS/blind-next-video-discovery.md` and was ignored twice on 2026-07-30 — once on a topic
that was already published (`499YLd1BHZ4`). ADR-0021.*

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

**0A-bis. VidIQ MCP competitor/trend enrichment (`--full` + ad-hoc; skip on quick checks)**

If the VidIQ MCP is connected (`docs/VIDIQ-MCP-SETUP.md`), use it for what we have no other tool for: competitor/channel research and trend discovery. This is **enrichment** — it sharpens Step 0's landscape, it does **not** decide anything. Any VidIQ title/thumbnail score it volunteers goes to the packaging-lock ENRICHMENT line only and is **clickbait-guarded** (rejected if it trips `title_scorer`'s brand gate or the CTR kill-list). Costs 5 credits/call (Boost tier — headroom). If unreachable/out of credits, fall back to the 0A web scan + manual in-app VidIQ; note it and continue.

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

**0D. Competitor Outlier-Mining (growth lever — is the algorithm boosting this cluster NOW?)**

A topic YouTube is actively pushing for small channels gets the impression test that Gate-2 packaging needs. Surface what's breaking out in the niche *right now* and whether this topic-cluster is among it:

**VidIQ refresh (preferred — official API, not bot-walled):** if the VidIQ MCP is connected, first refresh the outlier cache from the official API (the tracked competitor set is the repo's `style-match` + `broad-history` tiers, synced 2026-07-01 — ADR-0013). Call `vidiq_outliers(channelIds=<tracked or a broad-history subset>, contentType="long", publishedWithin="threeMonths", minOutlierScore=2)`, save the JSON, and upsert it into intel.db so the scanners below read fresh data:

```bash
python -m tools.packaging_intel --refresh-from-vidiq <saved-vidiq-outliers.json>
```

This replaces the yt-dlp scrape that gets 429/botcheck-walled. If the MCP is unreachable/out of credits, skip it and fall back to the scraped cache (note it and continue).

```bash
python -m tools.packaging_intel --scan-competitors        # recent niche-wide 2x+ outliers (last 90 days)
python -m tools.packaging_intel "<topic>"                 # topic-specific: competitor outlier_count + top match
```

The scanner is recency-filtered (last 90 days) — these are live boosts, not all-time hits. `get_topic_viability`'s `competitor_signal.outlier_count` tells you if *this* topic-cluster has recent outliers. **Lens choice (ADR-0013):** use the `broad-history` channels for "is this topic hot for viewers like mine" (demand), the `style-match` peers for "has a real peer covered this, and how" (craft/differentiation).

```
OUTLIER SIGNAL:
  Niche-wide hot now: "the Iran war is SO much worse..." (40.8x), "the rotating villain theory" (13.3x)
  This topic-cluster: 2 recent 3x+ outliers (top: "..." 310K) → outlier: YES
```

Carry **`outlier: YES/NO`** into the Step 4 composite verdict. An active cluster boost is a strong GO signal; no recent outliers isn't a STOP, but means you're relying on demand + hook alone.

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

**Decision (thresholds = PACKAGING_MANDATE V1):**
- **GO** (≥1,000/mo search volume): Proceed to Step 2
- **CAUTION** (500-999/mo): Passes the V1 floor. Warn user — "Marginal demand. Proceed only with a strong angle or live news hook."
- **STOP** (<500/mo or no data): **HARD BLOCK** unless a verified live news hook exists (V1's alternative path — verify date AND content, don't trust prior briefs). Otherwise: "Do not invest time in this topic. Find a higher-demand angle."

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

**VidIQ keyword enrichment (optional, `--full`):** the demand gate above uses free sources (autocomplete + pytrends + API). If the VidIQ MCP is connected, also call `vidiq_keyword_research(keyword="<plain topic>", mode="research")` for real YouTube search volume + competition + the **Overall** score, and record it as **enrichment** beside the free-source verdict. It sharpens the read and feeds the TOPIC-RUBRIC's "30% VidIQ Overall" (Step 1b) — but it does **not** replace the V1 gate and cannot upgrade a STOP (ADR-0012). If unreachable, note it and proceed on the free-source verdict.

### Step 1b: Composite Topic Rubric (when comparing fresh candidates)

When this is a FRESH topic choice with 2+ candidates (`--compare`, or ranking pipeline entries), score through **`tools/TOPIC-RUBRIC.md`** (v2, 2026-06-11): identity + demand gates, then 30% VidIQ Overall / 20% topicality / 25% whitespace / 10% title-format CTR / 10% rankability / 5% source access, plus the symmetric POCKET flag. Whitespace requires a live SERP scan (`serp_title_study.py`), not the static intel corpus. Skip for series episodes and already-decided revivals — the rubric is for fresh selection only.

### Step 1c: Cluster opportunity (2026-06-27 — validated 4–7× Suggested lever)

Per-video Suggested-surface CTR shows a topical **cluster** pulls **4–7%** vs **0.5–1%** for
isolated one-offs (the Guatemala×2 + Venezuela-Guyana dispute family; see PACKAGING_MANDATE
§2026-06-27). Videos in a tight topical neighborhood feed each other's Suggested traffic.
⚠ **Re-verified 2026-07-23:** cluster median Suggested CTR **4.15% vs 0.97%** (n=15 others) — a
4.3× gap. But the source (`surface_ctr`) is Feb-stale AND topic-confounded (the family shares an
audience), so this is **directional, not proof**. The mechanism is sound regardless (Up Next runs
on the currently-watched video, so a neighborhood hands YouTube real co-watch candidates instead
of an isolated niche upload) — the neighborhood is the channel's best distribution architecture
*because you can't earn a push after publishing* (PACKAGING_MANDATE §2026-07-23, distribution null).

Check whether this topic **extends an existing cluster** or could **seed one**:
- Glob `_ARCHIVED/published/` + `_IN_PRODUCTION/` for same-family topics (same dispute, region,
  grifter/myth, or scholar). If 1–2 already exist and performed, this is a **CLUSTER EXTEND** —
  strong GO signal (it inherits Suggested adjacency).
- If none exist but the topic is a famous dispute with obvious siblings, flag **CLUSTER SEED**.
  **Prefer to greenlight the whole neighborhood as a batch — three angles up front, before
  producing the first**, published within ~2–4 weeks. A working structure: (1) the central
  claim/dispute, (2) the document/mechanism behind it, (3) a neighboring case. Each stands alone
  (own demand + title gates), but they share an audience identity and each points to the next
  (wire the one-destination end screen at `/prep`).
- A famous one-off with no cluster path isn't a STOP, but note it gets no Suggested tailwind.

Carry **cluster: EXTEND / SEED / NONE** into the Step 4 verdict. On SEED, the next-action should
name the other two angles, not just this one.

### Step 2: Title Viability Check

**Step 2a: Live title shelf (SERP positioning) — runs by default, skipped on `--no-research`.**

`title_scorer` grades a candidate against a frozen own-CTR snapshot + static niche aggregate — it has no live read of what's actually ranking for this query *now*. Run the title shelf study to see the real shelf and find the positioning whitespace (cheap: scrapetube only, no Gemini, ~5s):

```bash
python -m tools.preflight.serp_title_study --slug <topic-slug> --query "<plain topic query>" [--query "<variant>"] --top 12
```

Derive 1–2 plain-topic queries from the topic (what a viewer would type, not the channel's framing). Read `channel-data/serp-studies/titles/<slug>-<date>.md` → extract the **Positioning whitespace** levers (e.g. "two-sentence Claim.Evidence. is 0% — open whitespace"; "shelf is question-heavy — go declarative").

**Feed into generation:** the candidates in this step MUST occupy ≥1 whitespace lever the shelf leaves open (prefer the two-sentence "Claim. Evidence." formula when it's absent — it's the channel's top-retention brand signal). Name, per chosen title, which shelf saturation it breaks.

**Stop condition:** if the tool errors (scrapetube/network), surface a one-line warning, note "title shelf unavailable — generating from title_scorer + Step 0 competitor scan only" and continue. Enrichment, not a gate.

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

**Filter basis (model C):** `title_scorer` encodes the CTR audit (`channel-data/CTR-TITLE-FORMULA-2026-06.md` — recognition/fame + the kill-list: no abstract-noun lead, no obscure-proper-noun lead, no homework framing). Under the packaging-lock model, the **binary** parts are the filters (`has_search_anchor` → head-term anchor; `hard_rejects` → clickbait brand-gate). The composite **score (65) and `/curiosity` (60) are enrichment**, not gates — record them, nudge if low, never block on them.

If no title provided, generate candidates using:
1. The topic + search keywords
2. **The packaging research angle from Step 0** (if available) — titles MUST reflect the recommended angle, not generic framings
3. Competitor title patterns from Step 0A — differentiate from what already exists

**Outlier pattern check:** Run `python -m tools.benchmark.outlier_title_dissector --score "Title"` to score against proven niche outlier patterns (scale words, specificity, country names = higher lift).

**Title generation rules (from PACKAGING_MANDATE.md):**
1. Title MUST include the exact search keyword (or close variant)
2. Title MUST use versus, declarative, or how/why pattern
3. Title MUST score 65+ on `title_scorer.py` AND 60+ on the `/curiosity` check (The Emotional Hook check)
4. Style hedges (years, colons, "The X That Y") are graded penalties, NOT bans — per the re-tiered `PACKAGING_MANDATE.md` Tier 2 (the hard-reject policy is RETIRED; the channel's #1 and #3 videos both have colons). A/B-testable per BREAKOUT-HYPOTHESES.
5. Title MUST set up a clear paradox (Specific Subject + Common Belief + Contradiction) that can be resolved in the first 5 seconds of the video.

**Keyword-ladder GATE (MANDATE V2 — now a PASS/FAIL gate, not just a scorer bonus):**
The best title MUST anchor a **famous parent keyword with real search volume**, and that keyword must **begin** within the first ~40 characters (it may run past that edge) — a 515-sub channel has no ranking power for a bare obscure proper noun. Verify with `python -m tools.title_scorer --anchor "<title>"`, which prints the matched term, its position and its provenance. The obscure entity is the *reveal* (the second punch), never the lead.

⚠ **A FAIL is not automatically a verdict on the title** (ADR-0023). The recognizer accepts a term on a curated list *or* on a verified search volume ≥1,000/mo in `keywords.db`, so a FAIL means either the title genuinely leads with something obscure — regenerate — **or** the lead term is famous and nobody has measured it yet. Check demand before rewriting: if the term clears 1,000/mo, record it and re-run the gate.

```bash
python -m tools.title_scorer --record-anchor "<term>" --volume <n> --anchor-source vidiq-YYYY-MM-DD
```

**Never trade a title down for a vaguer one to clear a data gap** — #67 lost five candidates that way before this was fixed. If no candidate anchors after that check, the title FAILS this gate — regenerate, don't proceed (carry the result into Step 4).

**Title ↔ thumbnail division of labor:** the title carries the **searched keyword + curiosity**; the thumbnail carries the **evidence/emotional payload**. They must NOT duplicate each other (this is the same curiosity-gap necessary condition `thumbnail_checker` enforces in Step 3) — if the title already says it, the thumbnail overlay must raise the question or name the charge, not restate it.

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

### Step 2c: NLM Title Validation (packaging notebook) — runs on `--full`

**Purpose:** Validate the scored title shortlist against the competitor outlier corpus before the composite verdict — patterns the mechanical scorers can't see (closest real competitor matches, differentiation risk).

**Run:** Query the packaging intelligence notebook with **Prompt P5** (`.claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` § Packaging Intelligence Prompts), passing the top 3–5 candidates from Step 2 with their scores. Use the notebook-researcher agent for a full session, or a direct `mcp__notebooklm__notebook_query` for the single P5 query (cheaper — preferred when Step 0B already ran this session).

**Display:**
```
NLM TITLE VALIDATION (P5):
  1. "France vs Haiti. 122 Years of Forced Payments."  — composite 82
     closest outliers: "How France Made Haiti Pay" (1.2M) · "Haiti's Debt Explained" (3.8M)
     ⚠ differentiation risk: framing near-identical to 1M+ video
  2. ...
```

Feed the composite ranking + any differentiation flags into Step 4 (Composite Verdict).

**SKIP path:** if the packaging notebook is unreachable (MCP auth expired and `nlm login` retry fails, notebook missing, or query errors twice), emit one line — "NLM title validation skipped: packaging notebook unreachable — verdict uses title_scorer + /curiosity + Step 0 scan only" — and proceed. This step is enrichment, not a gate.

### Step 3: Thumbnail Concept Check

If checking an existing project (`--project`), read YOUTUBE-METADATA.md:

```python
from tools.preflight.thumbnail_checker import check_project
result = check_project("video-projects/_IN_PRODUCTION/21-haiti-independence-debt-2025")
```

If checking a new topic (`--full`), generate 3 thumbnail concepts by **operation** (not by static layout). Each concept performs ONE visual operation; pick the operations that fit the video's payload. See `.claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md` for the full recipe and `/thumbnail` for grounded concept generation.

**Operation taxonomy (auto-generate for any topic):**

```
**Concept A — COMPRESSION**: collapse the whole video into one image the eye reads in <1s
  (the single fact/contrast that IS the video). 2-4 word overlay naming the charge, not the title.

**Concept B — DOSSIER METAPHOR**: the evidence object as the hero — real document/map/artifact,
  cut-out + saturation pop + ONE red accent at the focal point. The auditor's-edge moat made visual.
  (Raw sepia documents are a LIABILITY untreated — they must be cut out + saturated, not pasted flat.)
  ⚠ 2026-06-27 DATA: a document/page as the FOCAL POINT is the channel's CTR floor (−0.71 overall,
  −2.11 within famous topics; body text doesn't resolve at feed size). If you use this concept,
  the hero must be the ONE legible line/number/seal the document reveals — never the page. A clean
  map or famous-face concept (A/C) usually out-clicks a document hero; prefer them on famous topics.

**Concept C — VISUAL ANSWER or MECHANISM REFRAME**: a simple map that answers a question (one red
  contested zone, for territorial), OR a diagram that reframes the mechanism (for HOW/system topics).
```

**Every concept MUST satisfy the necessary conditions** (these are filters, not predictors — ADR 0007): legible at 160px, ≤3 huge words, real subject (NO AI-generated figure — invisible polish of real material only), no talking-head face, and a **curiosity gap** (overlay must not duplicate the title). Then run the checker on the generated concepts; on the rendered PNG, gate with `thumbnail_image_audit` (feed-size legibility).

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
║  Fame:      HIGH — famous parent (Browse +2.23%)  ║
║  Cluster:   EXTEND — 2 in family already live     ║
║  Outlier:   YES — cluster boosted now (2 recent)  ║
║  Title:     GO ✓  (85 enrichment — versus)        ║
║  Keyword:   PASS ✓ — anchors "Haiti" (head term)  ║
║  Thumbnail: PASS ✓ — necessary conditions met     ║
║  Lock:      VALID ✓ — 4 filters recorded (Step 4b)║
╠══════════════════════════════════════════════════╣
║  → Proceed to /research --new                    ║
╚══════════════════════════════════════════════════╝
```

When DB enrichment is unavailable (no CTR data ingested yet), display:
```
║  Title:     GO ✓  (85/A — versus, static scores) ║
```

**Verdict logic (model C — filters decide, scores are enrichment):**
- **GO:** Demand ≥ GO AND all four **packaging FILTERS** PASS (search-anchor · clickbait brand-gate · title↔thumbnail curiosity gap · thumbnail conditions — thumbnail may be PENDING). Outlier YES strengthens GO.
- **REVIEW:** All filters PASS but an **enrichment** score is below its nudge (`title_scorer` <65 or `/curiosity` <60), or thumbnail = REVIEW. A nudge means *eyeball it*, not *stop*.
- **STOP:** Demand = STOP OR any mechanical filter FAILS (no search anchor, clickbait brand-gate reject, thumbnail FAIL) OR the title↔thumbnail gap judgment is blank.

**Note (ADR 0007 + the packaging-lock ADR — filters, not predictors):** the packaging verdict is **PASS/FAIL on necessary conditions**, never a clickability score. `title_scorer`'s 65 and `/curiosity`'s 60 are **recorded enrichment**, not gates — a low composite that clears the four filters is REVIEW, never STOP (the composite is confounded; see `channel-data/CTR-TITLE-FORMULA-2026-06.md`). VidIQ/NLM are enrichment and **cannot** upgrade a filter FAIL. No pre-publish number predicts the click; the only verdicts are demand (Gate 1) and live CTR (Gate 2, post-publish).

### Step 4b: Write the Packaging Lock (HARD GATE — code-enforced)

The verdict above is not real until it's **recorded by the checker**. #62 failed because a written rule didn't bind — so this is a code gate, not an instruction. Run:

```bash
python -m tools.preflight.packaging_lock --project <path> --title "<best title>" \
  --curiosity <N> --vidiq "<score/note — or 'not queried'>" --nlm "<P5 note>" \
  --gap "<why the thumbnail overlay does NOT restate the title — REQUIRED judgment>" \
  [--territorial] [--person-focused] --write
```

This writes the `<!-- AUTO:packaging-lock -->` block into `PROJECT-STATUS.md` (below the reconcile zone) recording the four FILTERS + the ENRICHMENT scores. **The lock is INVALID (BLOCKED) if:** any mechanical filter FAILS, or the `--gap` judgment is blank. `/research` calls `packaging_lock --validate` before advancing a new project and refuses if BLOCKED. A blank `--gap` is not a shortcut — fill it or mark PENDING with a reason.

### Step 5: Next Action

Based on verdict, tell the user exactly what to do:

- **GO:** "Run `/research --new [topic]` to start the project. Use title '[best title]' as your working title." If `cluster: SEED`, add: "Plan 2–3 follow-ups in the same dispute family within ~2–4 weeks (validated 4–7× Suggested lift — they feed each other)."
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

## Optional: red-team the locked packaging

Everything above decides whether the packaging *passes*. It does not ask why the
target viewer would scroll **past** it in a feed full of competitors. Once the
title + thumbnail are locked, the `packaging-adversary` agent attacks them
against the LIVE SERP and returns ranked scroll-past hypotheses, each shaped as a
single-variable A/B swap:

```
Agent({ subagent_type: "packaging-adversary",
        description: "Red-team locked packaging",
        prompt: "Red-team this locked title + thumbnail against the live SERP
                 for <query>. Return ranked scroll-past hypotheses as
                 single-variable swap candidates." })
```

It is **not** a gate and returns no binding score — the filters in
`packaging_lock.py` decide (ADR-0012). Use it when a topic matters enough to
want a second, hostile opinion. For scoring *concepts* before they are locked,
use `thumbnail-critic` via `/thumbnail --critique` instead.

---

*This command enforces PACKAGING_MANDATE.md. No video should begin production without passing greenlight.*
