---
name: "source-command-thumbnail"
description: "Generate 3 ranked thumbnail concepts grounded in the close-match outlier corpus + per-channel playbook"
---

# source-command-thumbnail

Use this skill when the user asks to run the migrated source command `thumbnail`.

## Command Template

# /thumbnail — Outlier-Grounded Thumbnail Recommender

**Purpose:** Generate 3 ranked thumbnail concepts for the active video project, grounded in the verified outlier corpus (n=30 outliers across 8 close-match channels) and per-channel playbook. Replaces guesswork with operation-named, outlier-cited, channel-anchored concepts.

**What it does NOT do:** It does not score thumbnails. Two checkers exist for that, at two different stages:
- **Concept text** (pre-render): `tools/preflight/thumbnail_checker.py` — niche-rule compliance on the written concept.
- **Rendered image** (post-export): `tools/preflight/thumbnail_image_audit.py` — tech compliance, mobile-legibility previews, and **SERP differentiation** (CLIP cosine vs this query's actual competitors). Run it once you've exported the PNG; it's also wired into `/publish` Gate 3.

It does not generate image mockups. It outputs concept specs only — visual, overlay text, operation, evidence — to chat.

## Usage

```
/thumbnail                              # Auto-detect active project from _IN_PRODUCTION
/thumbnail [project-folder-name]        # Explicit project (e.g., 21-haiti-debt-2025)
/thumbnail --title "..." --thesis "..." # No project; ad-hoc title + script thesis
```

## Flags

| Flag | Purpose |
|------|---------|
| *(default)* | Auto-detect single in-production project. If multiple, list and ask. |
| `[project-folder]` | Use specific project from `video-projects/_IN_PRODUCTION/` or `_READY_TO_FILM/` |
| `--title "..."` | Override title (skip YOUTUBE-METADATA.md lookup) |
| `--thesis "..."` | Override script thesis (skip SCRIPT.md lookup) |
| `--save` | Append the output as `THUMBNAIL-CONCEPTS.md` in the project folder (default: chat only) |
| `--study` | Before generating concepts, run `serp_thumb_study.py` to classify the topic's LIVE ranking shelf (per-topic, current) and feed its composition + whitespace into the concept query. Stronger than the static corpus alone. |
| `--critique` | After concepts, spawn `thumbnail-critic` agent to score concepts on operation-fit / DIY feasibility / mobile legibility / curiosity payload |
| `--diy [N]` | After concepts, spawn `diy-asset-creator` agent to produce a zero-budget production guide for Concept N (defaults to N=1, the Top pick). Mutually compatible with `--critique` (critic runs first, DIY runs last). |
| `--force` | Bypass Step 1.5 title pre-gate (use only when intentionally testing concepts on a HARD-REJECTED title) |

---

## WORKFLOW

### Step 1: Resolve inputs

**Auto-detect mode (no args):**

1. Glob `video-projects/_IN_PRODUCTION/*/` and `video-projects/_READY_TO_FILM/*/` for project folders.
2. If exactly 1 in-production project, use it.
3. If multiple, list them with their working titles and ask which one. Do not guess.
4. If zero, ask user to specify `--title` and `--thesis` or run `/research --new` first.

**Explicit project mode (`[project-folder-name]`):**

Glob for a folder ending with that name across `_IN_PRODUCTION/` and `_READY_TO_FILM/`. Read it.

**Ad-hoc mode (`--title` + `--thesis`):**

Skip file reads. Use the supplied strings directly.

### Step 1.5: Title pre-gate

Before reading project files or generating concepts, verify the title isn't HARD-REJECTED by `title_scorer.py`. The recommender should not waste tokens on a title YouTube won't show — reverse-validation showed 5 of HvH's 8 lowest-CTR videos were killed by title structure (year / colon / "the X that Y"), not thumbnail.

**Run:**

```bash
python -m tools.title_scorer "<resolved title from Step 1>"
```

**Decide:**

- If output contains "REJECTED" status OR score < 65: **HALT.** Surface the rejection reason (year / colon / the_x_that / question / score), tell the user the title is dead-on-arrival per `tools/PACKAGING_MANDATE.md` rules, and recommend running `/greenlight` to regenerate the title before generating thumbnail concepts. Do NOT proceed to Step 2.
- If score ≥ 65 and not REJECTED: continue to Step 2.

**Override:** if `--force` was passed, log the gate result as a warning but continue. Use only when intentionally testing concepts on a known-rejected title.

**Stop condition:** if `python -m tools.title_scorer` errors (tool missing, syntax error), surface the error and ask user to fix or pass `--force`. Do not silently skip the gate.

### Step 2: Read project files

Read in this priority order. Stop reading when you have enough to build the prompt:

| Field | Primary source | Fallback |
|---|---|---|
| Title | `YOUTUBE-METADATA.md` (look for `Title:` or `# Title` or H1) | folder name (parse out numeric prefix, year suffix) |
| Script thesis | `SCRIPT.md` (read first 500 lines; extract the explicit thesis statement, usually in the opening 90 seconds) | `01-VERIFIED-RESEARCH.md` opening summary |
| Topic shape signals | `01-VERIFIED-RESEARCH.md` (skim section headers) | folder name keywords |
| Site visitability | `SCRIPT.md` (mentions of border / archive / specific physical location) | none — assume false |

If `SCRIPT.md` doesn't exist yet, note "no script — concepts use title only" and continue. Concepts grounded in title-only are weaker (MECHANISM REFRAME requires a known thesis).

### Step 2.5: Topic-comparable scan (read if present)

The notebook's outlier corpus is **niche-wide aggregate** data from 8 close-match general channels. It does not know what's already winning *on the specific topic of this video*. If the project has prior `/comment-mine` output, that data captures topic-conditional winners and should feed into the query.

**Read:**

```bash
ls "<project-folder>/_research/comment-mining/"*.info.json 2>/dev/null
```

**If files exist:** parse each JSON for `title`, `channel` (or `uploader`), `view_count`, `duration`, `id`. One-liner:

```bash
for f in <project-folder>/_research/comment-mining/*.info.json; do
  python -c "import json; d=json.load(open('$f', encoding='utf-8')); print(f\"{d.get('view_count',0)}|{d.get('duration',0)}|{d.get('id')}|{d.get('uploader') or d.get('channel')}|{d.get('title')}\")"
done | sort -rn -t'|' -k1 | head -5
```

Take the top 5 by view count. Format each as one line:
```
- [Channel] "[Title]" — [view_count] views, [duration_min] min
```

**If no JSONs OR the directory is missing:** set the variable to the literal string `none — no comment-mining data available` and continue. Do NOT halt; this step is enrichment, not a gate.

**Stop condition:** if the parsing throws (corrupted JSON, unexpected schema), surface a one-line warning, set the variable to `none — comment-mining parse failed` and continue. The thumbnail recommender should not fail because of a stale JSON.

### Step 2.6: Live SERP shelf study (`--study` flag only)

The notebook corpus is niche-wide aggregate (n=30, 8 channels). It cannot see what *this topic's* shelf looks like *today*. `serp_thumb_study.py` classifies the actual ranking thumbnails per-topic via Gemini Flash vision — operation, face, map, framing, overlay words, colors — and derives which operations are ABSENT (the whitespace to attack).

**If `--study` was passed:**

1. Derive 1–2 plain-topic search queries from the title/topic keywords — strip the channel's framing, use what a viewer would actually type (e.g. title "China Claims the Entire South China Sea" → `"south china sea dispute"`, `"nine dash line"`).
2. Run:

```bash
python -m tools.preflight.serp_thumb_study --slug <project-slug> --query "<query 1>" --query "<query 2>" --top 8
```

3. **Check the exit code first.** Non-zero means fewer than half the shelf classified; the report carries a `⛔ STUDY FAILED` block and deliberately has **no** composition or whitespace section. Do not read numbers out of it. Set both SERP blocks to `none — SERP study unavailable` and continue.
4. On exit 0, read the generated `channel-data/serp-studies/<slug>-<date>.md`. Extract two things for the query in Step 3:
   - **Shelf composition** — face %, map %, dominant framing, dominant colors, most-common operations (what convention to break, or strategically keep if it's a hard topic convention like a map).
   - **Whitespace** — the "operations ABSENT from this shelf" line (the gap to occupy). If the report carries the partial-coverage caveat (`read off N of M`), pass the absent list through as *"absent from the tagged sample"* — never as *"absent from the shelf"*.

**Stop condition:** if the tool errors or exits non-zero (scrapetube / gemini / network / under-tagged shelf), surface a one-line warning, set the SERP block to `none — SERP study unavailable` and continue. This is enrichment, not a gate. **Never synthesize a whitespace line yourself to fill the gap** — an unclassified shelf lists every operation as absent, which is the strongest possible claim from zero evidence (ADR-0020; the 2026-07-30 #65 run).

### Step 3: Build the notebook query

Construct the query string with this exact structure. Do not paraphrase the bracketed sections.

```
Apply THUMBNAIL-RECOMMEND-PROTOCOL.md exactly. Generate 3 ranked thumbnail concepts.

Title: [exact title from YOUTUBE-METADATA.md]
Script thesis: [1–3 sentence thesis from SCRIPT.md, naming the actual mechanism the video proves — not the title's surface claim]
Topic-shape signals: [bullet list of 2–4 signals from research: territorial / treaty / mechanism / site-visitable / etc.]
Topic-comparable winners (from /comment-mine — same-topic videos already winning views; use to identify what visual conventions the topic already has and where HvH should differentiate vs cannibalize):
[bullet list of top 5 from Step 2.5, OR "none — no comment-mining data available"]
Live SERP shelf (this topic, today — from serp_thumb_study; classify your concepts against the ACTUAL ranking thumbnails, not just the niche corpus):
[shelf composition from Step 2.6: face %, map %, dominant framing, dominant colors, top operations — OR "none — SERP study not run"]
Whitespace operations ABSENT from this shelf (prioritize concepts that occupy this gap):
[absent-operations line from Step 2.6, OR "none"]
HvH constraint: 515 subs, evidence-based myth-busting, "intellectual competence" trigger, format = 8–12 min talking-head + B-roll. Do not propose assets HvH cannot produce.
VALIDATED CTR RULES (own data, all 56 thumbnails, 2026-06-27 — see PACKAGING_MANDATE §2026-06-27): (1) NO document-as-focal-point — a page of body text is the CTR floor (−0.71 overall, −2.11 within famous topics); show the ONE legible line/number the document reveals, never the page. (2) NO clutter — one focal point only (busy −0.52). (3) A clean map (one contested zone) or a famous/emoting face works; a blank creator face does NOT help. (4) Do NOT rely on a "red pop" — it tested NEGATIVE on the full set (confounded with the cluttered-document style), so red is not a clickability lever. (5) Verdict-overlay wording: "FACT CHECKED" beat its synonyms in 2 independent A/B tests; existential questions ("DOES X EXIST?") beat flat framings — prefer these, but they're directional (A/B-confirm).

When topic-comparable winners are present, your concepts must explicitly position against them: name which topic-comparable convention each concept either differentiates from or strategically copies, and cite the specific video by channel + view count. Do not generate concepts that ignore an established topic convention without naming why.

When a Live SERP shelf is present: at least one of your 3 concepts MUST occupy a whitespace (absent) operation, and every concept must name which dominant shelf convention (face / map / framing / color / operation) it breaks or strategically keeps. Do not propose a concept that lands inside the shelf's dominant operation+color without a stated reason.

**HUMAN CURIOSITY CONSTRAINT:** Do NOT generate literal historical depictions (e.g., "A map and a treaty"). You MUST generate concepts based on **Visual Contradictions** or **Emotional Stakes** (e.g., "A modern drone next to a 500-year-old crumbling document", "A bright red censored stamp over a king's face") to trigger human curiosity. Make the viewer feel the tension.

Follow the protocol's Steps 1–6. Output exactly 3 concepts in the required format. End with the mandatory closing summary.
```

### Step 4: Query the notebook

Use the `Packaging Intelligence — History vs Hype` notebook (id: `98973069-020b-41f4-b3cd-795864b5cada`). Tool: `mcp__notebooklm__notebook_query`.

If the query returns an authentication error, halt and tell the user to run `nlm login`. Do not retry blindly.

If the query returns successfully but the output does NOT include all 6 required fields per concept, retry once with: "The output above is missing required fields. Re-run following THUMBNAIL-RECOMMEND-PROTOCOL.md Step 3 exactly. Each concept must include all 6 fields."

### Step 5: Structured field validation

Parse the response into a per-concept structure. For each of the 3 expected concepts, check all 6 required fields. Produce a per-concept verdict (PASS / BLOCK) plus a list of which fields are missing.

**Per-concept fields (all 6 required):**

| Field | Validation rule |
|---|---|
| Header | `### Concept N:` line with descriptive name |
| Visual | `* **Visual:**` line, ≥20 chars descriptive content |
| Text overlay | `* **Text overlay:** "…"` with quotes; char count parenthetical present (e.g., `(N chars)`) |
| (a) Operation | `* **(a) Overlay operation:**` line; operation name in CAPS, drawn from THUMBNAIL-RECOMMEND-PROTOCOL.md Step 4 allowed list (COMPRESSION / TITLE REPETITION / MECHANISM REFRAME / VISUAL ANSWER / NO OVERLAY / LOCATION PROOF / AESTHETIC HOOK + variants) |
| (b) Outlier evidence | `* **(b) Outlier evidence` line, followed by 2–3 cited entries each containing a verbatim title in *italics* + an `Nx` ratio |
| (c) Channel exemplar | `* **(c) Channel exemplar` line; channel name + a specific rule reference (not just the channel name alone) |
| Risk | `* **Risk / when this concept fails:**` line with ≥1 sentence |

**Document-level checks:**

- Exactly 3 concepts (not 2, not 4 — `--alternative` 4th is allowed only when explicitly produced as the protocol's optional 4th)
- Closing block contains BOTH `**Top pick:**` AND `**Risk if all 3 fail:**` lines

**Verdict:** Each concept is PASS (all 6 fields valid) or BLOCK (≥1 field missing or invalid).

**On any BLOCK:**

1. **Retry once** with an explicit per-concept missing-field list. Example retry prompt:
   > "Concept 2 is missing the **Risk / when this concept fails** field. Concept 3's outlier evidence has only 1 cited example (need 2-3). Re-run following THUMBNAIL-RECOMMEND-PROTOCOL.md Step 3 exactly. Each concept must include all 6 fields."
2. **If retry also produces BLOCK:** surface the raw output to the user AND list which fields failed per concept. Do NOT silently accept a bad response. Do NOT retry a third time (token budget).

**On all PASS:** continue to Step 6.

### Step 6: Present the output

Display the notebook's response verbatim in chat.

After the response, append a one-line execution summary:

```
---
Generated for: [project folder] | Title: "..." | Notebook: Packaging Intelligence — History vs Hype | 3 concepts.
```

If `--save` flag was passed, also write the response to `video-projects/[lifecycle]/[project]/THUMBNAIL-CONCEPTS.md` with a header:

```markdown
# Thumbnail Concepts

**Generated:** [date]
**Title:** [title used]
**Source:** Packaging Intelligence — History vs Hype notebook
**Protocol:** THUMBNAIL-RECOMMEND-PROTOCOL.md

---

[notebook response verbatim]
```

### Step 7: Optional concept critique (--critique flag only)

If `--critique` was passed, after Step 6 displays the concepts, spawn the `thumbnail-critic` agent with the 3 concepts as input. The critic scores each concept on 4 dimensions (operation-fit / DIY feasibility / mobile legibility / curiosity payload, 0–2 each, total /8) and returns one critical fix per concept.

**Spawn pattern:**

```
Agent({
  description: "Critique 3 thumbnail concepts",
  subagent_type: "thumbnail-critic",
  prompt: "Score these 3 thumbnail concepts produced by /thumbnail. Read PER-CHANNEL-THUMBNAIL-PLAYBOOK.md, OUTLIER-THUMBNAIL-CORPUS.md, and TITLE-TO-OVERLAY-OPERATION-MAP.md as ground truth. Apply the rubric in your agent definition. Output the structured score block per concept.

  Concepts:
  [paste verbatim notebook response from Step 6]

  Title: <title>
  Script thesis: <thesis>
  HvH constraint: 515 subs, evidence-based myth-busting, zero budget."
})
```

**After the agent returns:**

Display the critic's per-concept score block verbatim under a header:

```
---

## Critic verdict

[agent output verbatim]
```

If `--save` flag was passed, append the critic verdict to the same `THUMBNAIL-CONCEPTS.md` file under the same header.

**Stop conditions:**
- If the critic returns an error (fewer than 3 concepts, missing operation tags, etc.), surface the error and skip the critique block. Do not retry — the input was malformed.
- If the critic and `/thumbnail`'s "Top pick" disagree, the critic flags it. Display both rankings — let the user decide.

### Step 8: Optional DIY production guide (--diy flag only)

If `--diy` was passed, after Step 6 (and Step 7 if applicable) spawn the `diy-asset-creator` agent with the chosen concept (Concept N where N defaults to 1).

**Resolve N:**
- `--diy` alone → N = 1 (the Top pick from /thumbnail's recommender output)
- `--diy 2` / `--diy 3` → N = the explicit number
- `--diy 4` or out-of-range → error: "Only 3 concepts produced. Use --diy 1, 2, or 3."

**Spawn pattern:**

```
Agent({
  description: "DIY production guide for Concept N",
  subagent_type: "diy-asset-creator",
  prompt: "Build a single-asset zero-budget production guide for ONE thumbnail concept. This is NOT a B-roll checklist — it's one thumbnail.

  Concept (verbatim from /thumbnail Step 6 output):
  [paste Concept N's full block: Visual / Text overlay / Operation / Outlier evidence / Channel exemplar / Risk]

  Output a focused single-asset DIY guide covering:
  1. **Wikimedia Commons search terms** — exact queries to find the primary visual (or 'not applicable' if visual = creator-on-location, custom diagram, etc.)
  2. **MapChart.net steps** — only if concept uses a map. Specify region, color-coding, export settings.
  3. **Canva template** — exact template name to search ('parchment quote', 'dossier folder', etc.) + free-account download settings (PNG, standard quality).
  4. **PowerPoint composition** — element layering, text overlay placement, font + size at 1280×720 export.
  5. **Exact text overlay spec** — verbatim overlay text from the concept, font recommendation, size, color contrast, placement (rule-of-thirds anchor).
  6. **Estimated time** — total minutes for a first build of this thumbnail.
  7. **Fallback** — if the primary asset can't be sourced (missing Wikimedia hit, etc.), name the substitution path.

  HvH constraint: 515 subs, evidence-based myth-busting, zero budget. Free tools only. Do not propose AI image generation (the creator prefers real materials).

  Output a single markdown block, ≤300 words. Do not output a multi-day plan — this is one thumbnail."
})
```

**After the agent returns:**

Display the DIY guide verbatim under a header:

```
---

## DIY production guide — Concept N

[agent output verbatim]
```

If `--save` flag was passed, append the DIY guide to the same `THUMBNAIL-CONCEPTS.md` file under the same header.

**Stop conditions:**
- If the agent's output exceeds 500 words, surface a warning — DIY guide should be focused, not exhaustive.
- If the agent proposes an **AI-generated subject/figure** (a fake person/artifact the thumbnail asks the viewer to believe), flag it: the evidentiary subject must be REAL (Wikimedia/Unsplash/Pexels). AI *polish* of real material and *atmospheric backdrops* are fine — the test is "does it read as AI / fake the evidence?" (per `feedback-thumbnail-process.md` R7 refinement + ADR 0007). Re-run once reinforcing a real subject; if still violated, surface the raw output.

---

## Failure modes — when to halt and report

- **Auth expired:** Tell user to run `nlm login`. Do not retry.
- **Notebook empty / no protocol source:** Tell user the THUMBNAIL-RECOMMEND-PROTOCOL.md source is missing from the notebook. Do not generate concepts without it.
- **Project folder ambiguous:** List candidates, ask which.
- **No SCRIPT.md AND no `--thesis` flag:** Warn that title-only concepts are weaker. Proceed but flag in output.
- **Validation fails twice:** Surface raw output + which checks failed. Let user decide whether to retry, fix the protocol source, or accept.

---

## Integration with other commands

- **`/greenlight`** still uses `tools/preflight/thumbnail_checker.py` for fast yes/no gates pre-research. `/thumbnail` is the post-script version that produces actual concepts.
- **`serp_thumb_study.py`** (`--study` flag, Step 2.6) is the live per-topic shelf classifier — fetches + Gemini-tags the actual ranking thumbnails and derives whitespace operations. Complements (does not replace) the static notebook corpus: corpus = what wins generally, SERP study = what *this* shelf looks like now. Distinct from `thumbnail_image_audit.py`, which is the post-render CLIP differentiation gate.
- **`/comment-mine`** is the upstream topic-conditional input. If run, its output JSONs in `_research/comment-mining/` are read by Step 2.5 and feed topic-comparable winners into the notebook query. Without this, /thumbnail relies only on niche-wide aggregate data and may miss visual conventions the specific topic already has (e.g., 100% inquisitor-figure rate on Spanish Inquisition outliers, which the n=30 close-match corpus does not capture).
- **`/prep`** consumes the thumbnail concepts when building asset/B-roll lists. Run `/thumbnail --save` first so `/prep` can read THUMBNAIL-CONCEPTS.md.

**Typical sequence:**
```
/script              # Write script
/verify              # Fact-check
/comment-mine        # Pull same-topic competitor videos (feeds /thumbnail Step 2.5)
/thumbnail --study --save   ← classify live SERP shelf (Step 2.6) + generate + save concepts
# then BUILD IN PHOTOSHOP to the craft checklist (HUMAN builds — "Codex specs, user builds") + FILTER:
#   checklist: cut-out + saturation pop + ONE red accent at focal point + <=3 huge words +
#   REAL subject (no AI-generated figure) + 160px proof + voice gate  (THUMBNAIL-CRAFT-RECIPE)
python -m tools.preflight.thumbnail_checker <project> --title "<title>"   # concept filter: curiosity-gap (title != overlay)
python -m tools.preflight.thumbnail_image_audit thumb.png                 # image filter: feed-size legibility (HARD); CLIP INFORMATIONAL only
# tools.thumbnail.render is OPTIONAL (fast draft / spec ref), NOT the pipeline.
# at current traffic: pick the winner by a SINGLE-VARIABLE before/after swap; native A/B (Test & Compare) once reach grows. ADR 0007
/prep --full         # Asset + edit guides (reads THUMBNAIL-CONCEPTS.md)
```

---

## Reference sources (in the live notebook)

- `THUMBNAIL-RECOMMEND-PROTOCOL.md` — output format + decision tree (the house prompt)
- `OUTLIER-THUMBNAIL-CORPUS.md` — n=30 verified outliers with ratios + operations
- `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` — channel-anchored decision rules (8 channels)
- `TITLE-TO-OVERLAY-OPERATION-MAP.md` — 5 operations + 4 variants

Notebook ID: `98973069-020b-41f4-b3cd-795864b5cada`
