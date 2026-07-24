---
name: "source-command-research"
description: "Start new video project OR conduct topic research (Pre-production Phase 1)"
---

# source-command-research

Use this skill when the user asks to run the migrated source command `research`.

## Command Template

# /research - Pre-production Research Entry Point

Start a new video project or research an existing topic. This command consolidates project setup, topic research, and NotebookLM preparation.

**Competitive Integration:** This workflow includes competitor analysis and technique selection.

> **Historian Mode:** This command activates the `historian` skill at workflow entry (Stage A and beyond). The skill is dormant during Stage 0 project mechanics (demand gate, folder creation, title pre-gen). See `.Codex/skills/historian/SKILL.md`.

## Usage

```
/research                    # Interactive: asks what you need
/research --new [topic]      # Create new project folder + start research
/research --topic-only       # Research without creating project
/research --existing [path]  # Research for existing project
/research --sources [topic]  # Generate academic source list (folded from /sources)
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--new` | Create project folder + full setup | `/research --new "Library of Alexandria"` |
| `--brief` | Generate Wikipedia pre-research brief only | `/research --brief "Treaty of Tordesillas"` |
| `--competitors` | Competitor gap analysis for a topic/project | `/research --competitors "Treaty of Tordesillas"` |
| `--topic-only` | Research only, no project creation | `/research --topic-only "Chagos Islands"` |
| `--existing` | Add research to existing project | `/research --existing 19-flat-earth-medieval-2025` |
| `--ingest` | Ingest NLM output into verified research | `/research --ingest --existing 31-bermeja-island-2025` |
| `--apply-review` | Apply reviewed claims to VERIFIED-RESEARCH.md | `/research --apply-review path/to/review.md` |
| `--sources` | Generate Tier 1/2/3 academic source list via Codex API | `/research --sources "Library of Alexandria"` |
| `--prompts` | Generate NotebookLM verification prompts for a project | `/research --prompts 19-flat-earth-medieval-2025` |
| `--format-sources` | Format source list for YouTube description | `/research --format-sources` |

---

## SOURCE WORKFLOWS (folded from /sources, 2026-05-03)

### `--sources` — Automated source-list generation

Generates an academic source list using `tools/notebooklm_bridge.py` (Codex API-backed).

```bash
python tools/notebooklm_bridge.py "TOPIC" --type TYPE --output DIR
```

**Args:** `topic` (required), `--type` (territorial/ideological/fact-check/general, default general), `--output` (default current dir), `--sources` (10-20, default 15), `--dry-run`.

**Requires:** `ANTHROPIC_API_KEY` env var. `pip install anthropic>=0.40.0`.

**Output:** `NOTEBOOKLM-SOURCE-LIST.md` with:
- SOURCE QUALITY CHECK table (primary/academic counts)
- Tier 1: Primary Sources `[P1]`, `[P2]`...
- Tier 2: Academic Monographs `[A1]`, `[A2]`...
- Tier 3: Supplementary Sources
- Full citation details (title, author, publisher, ISBN, price, purchase link)

### `--prompts` — NotebookLM verification prompts

Generate NotebookLM chat prompts tailored to a project's verified-claims gaps. References `.Codex/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` for the prompt library.

### `--format-sources` — YouTube description formatter

Formats a source list (from `01-VERIFIED-RESEARCH.md` or `NOTEBOOKLM-SOURCE-LIST.md`) into the description block style used in YouTube metadata.

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

**For /research --new:** Focus on topic opportunity insights (what topic types perform well, what's underexplored)

---

## NEW PROJECT WORKFLOW (`--new` or default)

### Stage 0 — Project Setup (historian skill dormant)

### Step 0: YouTube Intelligence KB Staleness Check

Before starting research, check whether the YouTube Intelligence knowledge base is current:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.kb_store import KBStore
from pathlib import Path

if Path('tools/intel/intel.db').exists():
    s = KBStore()
    status = 'STALE' if s.is_stale() else 'CURRENT'
    print(status)
else:
    print('NOT_INITIALIZED')
```

**If STALE or NOT_INITIALIZED:** Inform user and run refresh automatically:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.refresh import run_refresh, get_refresh_summary
result = run_refresh(force=True)
print(get_refresh_summary(result))
```

Show a brief refresh summary to the user before continuing. This ensures competitor and algorithm data is current before planning research angles.

**If CURRENT:** Continue silently (no output).

### Step 1: Demand Validation (HARD GATE)

**Before asking ANY questions, check search demand:**

```python
import sys
sys.path.insert(0, '.')
from tools.preflight.demand_checker import run as demand_check
result = demand_check("topic keywords here")
```

**Decision tree:**
- **GO** (≥1,000/mo): Display `DEMAND: GO ✓ (X,XXX/mo — "keyword")` and proceed
- **CAUTION** (200-999/mo): Warn user — "Marginal demand. Proceed only with a strong search-intent title."
- **STOP** (<200/mo): **BLOCK PROJECT CREATION.** Tell user:
  - "This topic has insufficient search demand (<200/mo)"
  - Suggest 3 related keywords from keywords.db that DO have volume
  - "Run `/greenlight --compare` to evaluate alternatives"
  - Do NOT create the project folder

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

**If user insists on a STOP topic:** Require explicit override — "I understand this has low search demand and am proceeding anyway." Log this in PROJECT-STATUS.md as `DEMAND_OVERRIDE: true`.

### Step 1b: Gather Project Information

Ask the user:
1. **Topic:** What's the video about?
2. **Hook Type:** Territorial (colonial → conflict) OR Ideological (myth → belief)?
3. **Modern hook:** What 2024-2026 event makes this relevant?
4. **Opponent (if fact-check):** Who are you fact-checking?

### Step 1c: Title Pre-Generation

**Generate working title candidates BEFORE creating the project** using local Ollama (zero quota cost), then score them all.

**Step 1 — Ollama brainstorm (automatic):**

```bash
PYTHONPATH=. python tools/ollama_brainstorm.py "[topic]" --topic [territorial|ideological|colonial|general] --count 10
```

This generates 10 raw candidates locally via gemma3:4b. Fast, free, no Pro quota.

**Step 2 — Score everything:**

Take the Ollama candidates plus 2-3 of your own that include the exact high-volume keyword from Step 1. Score all of them together:

```bash
PYTHONPATH=. python tools/title_scorer.py [title1] [title2] ... --topic [type]
```

**Step 3 — Present and pick:**

Show the ranked list. User picks a working title. This frames the research angle.

```
WORKING TITLES (pick one to frame research):
  95/A  Argentina vs Britain. The Islands Nobody Can Legally Claim.
  85/A  The Falklands Sovereignty Dispute. Britain Used a Loophole.
  80/A  Britain Expelled Argentina from the Falklands. The Legal Basis Does Not Exist.
```

**If Ollama is not running** (check with `curl -s http://localhost:11434/api/tags`): skip the brainstorm step and generate 5 candidates manually before scoring.

Store the chosen working title in PROJECT-STATUS.md.

### Step 2: Check Claims Database FIRST

Before creating anything, check for existing verified research:

1. **Read:** `.Codex/VERIFIED-CLAIMS-DATABASE.md`
2. **Search for:** Topic keywords, related subjects, overlapping time periods
3. **If claims found:**
   - Note which claims are already verified
   - These go directly into 01-VERIFIED-RESEARCH.md
   - Mark as "Previously verified: [date], [video]"
   - Only research claims NOT already in database
4. **If no claims found:** Proceed with full research

### Step 3: Create Project Folder

**Location:** `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`

**Auto-detect next number:** Check highest existing number in `_IN_PRODUCTION/`

**Create structure:**
```
[number]-[topic-slug-year]/
  01-VERIFIED-RESEARCH.md      (from template)
  SCRIPT.md                     (placeholder)
  03-FACT-CHECK-VERIFICATION.md (placeholder)
  PROJECT-STATUS.md             (track progress)
  _research/                    (for NotebookLM outputs)
    00-NOTEBOOKLM-SOURCE-LIST.md
    01-PRELIMINARY-RESEARCH.md
    02-NOTEBOOKLM-PROMPTS.md
```

### Step 4: Initialize Research Files

**01-VERIFIED-RESEARCH.md** - Copy from `.Codex/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- Fill in project name, date, topic categories
- Pre-populate with any claims from VERIFIED-CLAIMS-DATABASE

**PROJECT-STATUS.md** - Create with phase tracking:
- Phase 1: Research (current)
- Phase 2: Script (locked until 90% verified)
- Phase 3: Fact-check (locked until script complete)

### Stage A — Historiographical Baseline

### Step 5: Wikipedia Pre-Research Brief (Auto-run)

**Automatically generate a structured brief using the `wiki-researcher` agent.**

Launch the agent with:
- `topic`: The video topic from Step 1
- `project_path`: The project folder created in Step 3
- `hook_type`: territorial or ideological (from Step 1)
- `modern_hook`: The modern relevance connection (from Step 1)

The agent fetches Wikipedia + related articles + recent news + competitor videos and outputs a structured brief to `_research/00-PRELIMINARY-BRIEF.md`.

**Output includes:**
- Chronological timeline with verification flags
- Key figures and their roles
- Claims ranked by script priority (Critical vs Supporting)
- Standard narrative (what competitors will say)
- Underexplored angles (your edge)
- Modern relevance hooks (2024-2026 news)
- Academic sources extracted from Wikipedia's own references
- Competitor video landscape with gap analysis
- Pre-verified claims from existing channel projects

**Time:** ~2-3 minutes (replaces 2-4 hours of manual browsing)

> **Note:** This brief is Phase 1 only. Every claim is marked unverified and needs Phase 2 academic confirmation via NotebookLM.

### Step 6: Conduct Additional Preliminary Research

Using the brief as a foundation, fill any remaining gaps:
- Claims the brief flagged as "Verify?" that aren't covered by Wikipedia
- Academic sources not in Wikipedia's references
- Modern relevance connections (2023-2026 news) beyond what the brief found
- Opposing viewpoints to address

**Output to:** `_research/01-PRELIMINARY-RESEARCH.md`

### Step 6.5: Topic Viability Gate (P11.1a)

> **Companion to `/greenlight`** (packaging viability — will it get clicks). This gate covers substantive viability — can we research this topic at the channel's standard. Run after the Phase 1 wiki-researcher brief (Step 5 output: `_research/00-PRELIMINARY-BRIEF.md`). See `feedback-auditors-edge.md` §'tier-vibe' for T-tier accessibility, `feedback-topic-vs-angle-ordering.md` for the angle-locks-at-research principle, and `.Codex/REFERENCE/THESIS-DISCIPLINE.md` for throughline drafting.
>
> **Distinction from `/greenlight`:** `/greenlight` = will this title/thumbnail get clicks (packaging). This gate = can we produce it with primary-source integrity (substantive). They run in parallel, not redundantly.
>
> **Distinction from Step 1c title pre-generation:** Step 1c brainstorms title candidates via Ollama (packaging layer). This gate surfaces T-tier distribution + specificity bombs + thesis discipline (content layer). No overlap.

**Trigger condition:** Fires once per topic after Step 5 wiki-researcher brief is complete. Cannot be skipped — `/research` cannot enter Step 7 without a PROCEED or VIABILITY_OVERRIDE verdict.

**Three viability checks** (mechanism-word check is deferred to P11.1b — needs the NLM notebook, which isn't populated until after Step 8):

#### Check A: Primary-source accessibility map (T-tier projection)

From the brief's "Academic Sources" table and "Claims" section, project a T-tier distribution across load-bearing claims:

- **T1-projected:** Count of claims where a primary document is plausibly accessible — digitized or in a verifiable language per `user-languages.md` (French, Spanish, German, Latin, Greek, Dutch).
- **T2-projected:** Count of claims where the primary exists but only via Anglophone scholar quotation.
- **T3-only:** Count of claims where only scholarly interpretation is available; primary is inaccessible or in an unverifiable language.

Thresholds (v1 calibration — re-evaluate after 3-4 videos run through the gate):
- **PROCEED:** T3-only < 15% of load-bearing claims.
- **SHARPEN:** T3-only 15–30%, OR T3-only > 30% but primaries are in verifiable languages (acquisition is feasible).
- **DEFER:** T3-only > 30% AND the inaccessible primaries are in a language the channel cannot verify.

#### Check B: Specificity-bomb count

Per niche-wide data (5.4x retention lift), the topic needs ≥3 specificity bombs available — specific named documents + dates + figures + concrete factual claims. Source from the brief's Claims section and Wikipedia's primary-source references.

Thresholds (v1 calibration):
- **PROCEED:** ≥3 specificity bombs identifiable, each with a credible source path.
- **SHARPEN:** Exactly 2 specificity bombs — possibly enough but thin.
- **DEFER:** Fewer than 2 specificity bombs identifiable from the brief.

#### Check C: Thesis-discipline pre-check

Per `THESIS-DISCIPLINE.md`, attempt to draft a ≤12-word throughline from the brief.

Thresholds:
- **PROCEED:** Throughline forms with a specific action verb that names what historical actors did.
- **SHARPEN:** Throughline forms but feels generic — could apply to other topics.
- **DEFER:** No throughline forms; the brief reads as a fact-list without a sharp claim.

**Verdict logic:**
- **PROCEED** — All three checks PROCEED. Topic is substantively viable. Continue to Step 6.6 (if needed) then Step 7.
- **SHARPEN** — One or two checks at SHARPEN, none at DEFER. Output a specific punch-list of what's missing. Topic stays in the project folder; user iterates and re-runs the gate.
- **DEFER** — One or more checks at DEFER. Topic is not viable at the channel's current standard. Output a deferral note (what would need to change). Move to `channel-data/TOPIC-PIPELINE.md` backlog.

**Override mechanism:** If user explicitly overrides a DEFER verdict, require this acknowledgment:
```
I understand this topic is at the channel's substantive-viability ceiling.
I am proceeding with VIABILITY_OVERRIDE: true.
Reason: [user-supplied rationale]
```
Log to `PROJECT-STATUS.md` as `VIABILITY_OVERRIDE: true` with reason. The override is honest — it doesn't pretend the topic is viable; it acknowledges acceptance of the risk.

**Output: `RESEARCH-VIABILITY.md` in the project folder.** Structure:
```markdown
# Research Viability — [Topic]
**Date:** [YYYY-MM-DD]
**Verdict:** PROCEED / SHARPEN / DEFER

## Check A: T-tier projection
- T1-projected: [N] claims ([list])
- T2-projected: [N] claims ([list])
- T3-only: [N] claims ([list] — language accessibility: [verifiable / unverifiable])
- Result: PROCEED / SHARPEN / DEFER

## Check B: Specificity-bomb count
- Bombs identified: [N]
- Evidence: [list with source path for each]
- Result: PROCEED / SHARPEN / DEFER

## Check C: Thesis-discipline pre-check
- Draft throughline: "[≤12 words]"
- Action verb: [verb]
- Result: PROCEED / SHARPEN / DEFER

## Verdict: [PROCEED / SHARPEN / DEFER]
[If SHARPEN: punch-list of what's missing]
[If DEFER: deferral note + trigger Step 6.6 acquisition queue]
[If VIABILITY_OVERRIDE: flag + reason]

## Mechanism-word candidates (for P11.1b — resolved after first NLM ingestion)
- Candidate 1: [word] — projected confidence: [HIGH / MEDIUM / LOW based on brief]
- Candidate 2: [word] — projected confidence: [HIGH / MEDIUM / LOW]
```

**Gate behavior:** `/research` cannot enter Step 7 until `RESEARCH-VIABILITY.md` shows verdict PROCEED or VIABILITY_OVERRIDE: true. If SHARPEN, user must address the punch-list and re-run this gate.

### Step 6.6: Source Acquisition Queue Generation (P11.3)

> **Companion artifact to `_research/00-NOTEBOOKLM-SOURCE-LIST.md`** (which tracks what sources exist for the topic). This queue tracks what specific acquisitions would upgrade T3 claims to T2/T1 — a different shape. See `feedback-auditors-edge.md` §'tier-vibe' for T-tier upgrades; `feedback-research-audit.md` for the existing P/S/S→P system this queue feeds.

**Trigger condition:** Runs ONLY when Step 6.5 returns SHARPEN with T-tier accessibility gaps. PROCEED skips (no gaps to queue); DEFER skips (topic not viable, acquisition queue is moot).

**Per-gap analysis:** For each T3-only claim flagged in Step 6.5:
1. Identify the primary document that would close the gap (what source turns this T3 into T2/T1).
2. Identify access path: JSTOR / library catalogue / ILL request / archive contact / online repository / scholar-quoted alternative.
3. Estimate effort and cost.
4. Assign priority based on load-bearing-ness for the locked thesis.

**Output: `SOURCE-ACQUISITION-QUEUE.md` in the project folder.** Structure:

```markdown
# Source Acquisition Queue — [Project Name]

**Purpose:** Track primary-source acquisitions that would upgrade T3 claims to T2/T1.
**Generated from:** RESEARCH-VIABILITY.md gap analysis ([date]).
**Status legend:** TARGETED / ATTEMPTING / ACQUIRED / UNAVAILABLE / DEFERRED

## Queue Summary
- Total acquisitions targeted: [N]
- Priority 1 (blocks viability re-evaluation): [N]
- Priority 2 (load-bearing for scene): [N]
- Priority 3 (nice-to-have): [N]
- Acquired: [N] | Unavailable: [N]

## Acquisitions

### [Source name]
- **Upgrades claim:** [Specific claim in 01-VERIFIED-RESEARCH.md that gets upgraded]
- **Current tier:** [T3 / T2]
- **Target tier:** [T2 / T1]
- **Source type:** [Primary document / Critical edition / Manuscript scan / Archival reference]
- **Access path:** [JSTOR URL / Library catalogue / ILL request / Archive contact / Online repository]
- **Estimated effort:** [Low / Medium / High] — [free / paywall / ILL turnaround / archive trip]
- **Estimated cost:** [€ amount or "free"]
- **Priority:** [1 / 2 / 3]
- **Status:** TARGETED / ATTEMPTING / ACQUIRED / UNAVAILABLE / DEFERRED
- **Notes:** [Why this matters, blockers, contact info]
```

**Re-evaluation hook:** After Priority 1 acquisitions are marked ACQUIRED, re-run Step 6.5 viability gate. PROCEED becomes reachable once the T3-only ratio drops below the DEFER threshold.

**Integration with `00-NOTEBOOKLM-SOURCE-LIST.md`:** Cross-reference both files but do not duplicate content. The source list tracks what to acquire for the topic broadly; the acquisition queue tracks what specific acquisitions unlock specific claim-tier upgrades. Different shapes; both useful.

### Step 7: Competitive Intelligence Check

After preliminary research, before deep research:

1. **Check what competitors covered:**
   - Search YouTube for "[topic]" - who has videos?
   - Note their angle, length, and apparent sources
   - What's missing from their coverage?

2. **Check for applicable techniques:**
   - Skim `WRITING-VOICE-AND-STYLE-P5-TECHNIQUES.md` for relevant techniques
   - Which opening hook fits this topic?
   - What evidence presentation style works here?
   - Note intended techniques in PROJECT-STATUS.md

3. **Check gap database:**
   - Is this topic in `GAP-DATABASE.md`?
   - If new, add it with preliminary scores
   - If existing, update status to "Researching"

> **Proactive:** "I've checked competitor coverage of [topic]. The main videos are [list]. Your unique angle could be [suggestion based on channel DNA]."

### Stage A Lock

Surface conversationally: *"Stage A (Historiographical Baseline) complete — ready for Stage B (Source Criticism)?"*

Run the Stage A→B checklist in `.Codex/skills/historian/STAGE-AUDITS.md` before confirming. On user confirm, append to `PROJECT-STATUS.md` **below** `<!-- /AUTO:reconcile -->`:

```
## Historian Stage State
**Current stage:** Stage A — Historiographical Baseline (locked [YYYY-MM-DD])
**Next stage:** Stage B — Source Criticism
**Outstanding flags:** [None / list]
**Stage A locked:** [YYYY-MM-DD]
**Stage B locked:** pending
**Stage C locked:** pending
```

### Stage B — Source Criticism

### Step 8: Create NotebookLM Source List

Based on preliminary research and the brief's Academic Sources table, create:
- `_research/00-NOTEBOOKLM-SOURCE-LIST.md`

**Standards (from NOTEBOOKLM-SOURCE-STANDARDS.md):**
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard)
- Top-tier scholars (endowed chairs, major universities)
- Critical editions of primary sources
- Budget is UNLIMITED - recommend best sources regardless of price

**IGNORANT SWEEP — build this list BLIND to the library.** Recommend the best sources for the topic regardless of cost OR whether we already own them. Do NOT pre-filter to owned/free sources — that biases selection toward the shelf and defeats the breadth mandate (`memory/feedback-source-selection-breadth.md`, `feedback-choice-ignorant-rerun.md`). Ownership is resolved in Step 8.5, AFTER the ideal list exists.

#### Provenance Check (per source)

For each source in `00-NOTEBOOKLM-SOURCE-LIST.md`, record inline:
- **Author / year / edition / translator / publisher** (bibliographic anchor)
- **Bias / proximity / intent** (internal-criticism note — who wrote it, when, for what audience)

Example format:
```
[A1] McIntosh, Gregory C. *The Piri Reis Map of 1513*. University of Georgia Press, 2000.
- Provenance: Academic monograph, 2000 edition; McIntosh is the primary Anglophone specialist
- Bias/proximity: Contemporary scholar (487 years after map creation); working from 16th-c scholarly apparatus
- Intent: Academic reassessment correcting Hapgood and Kahle errors
```

### Step 8.5: Library Intersection + Auto-Upload (owned-source check)

Runs AFTER the ignorant sweep (Step 8). Resolves which swept sources we already own and seeds the topic notebook from them. The owned-source check is retrieval/routing, NOT a selection filter — it never changes what's on the list, only acquire-vs-upload (`memory/feedback-check-owned-library.md`).

1. **Intersect** the sweep against the owned library at `library/by-topic/` (filenames are canonical `Title-Author-Year-Publisher.ext`, grep-friendly):
   ```bash
   cd "library/by-topic" && for term in <author-surnames + title-keywords from the sweep>; do
     hits=$(find . -type f -iname "*${term}*"); [ -n "$hits" ] && { echo "### $term"; echo "$hits"; }; done
   ```
   Filter false positives by hand (same surname, wrong author/work). De-duplicate (one edition per work).
2. **Tag each sweep entry** in `00-NOTEBOOKLM-SOURCE-LIST.md`: `[OWNED → uploaded: <path>]` or `[ACQUIRE: <access path>]`.
3. **Auto-upload owned matches** to a fresh topic notebook:
   - `mcp__notebooklm__notebook_create(title="#<N> <Topic> — <angle>")`
   - For each owned file: `mcp__notebooklm__source_add(notebook_id, source_type="file", file_path=<abs path>, wait=True)`
   - Free primary documents (the on-screen spine) go in the same pass as `source_type="url"`.
   - Record the notebook UUID in `PROJECT-STATUS.md` Historian Stage State.
   - If NLM auth is expired (`Authentication expired`), STOP and ask the user to run `nlm login` (interactive — Codex cannot run it); stage the upload list and resume on their confirm.
4. **The `[ACQUIRE]` remainder** is the acquisition queue — only sources the sweep wants that we don't own.
5. **Drive mirror (Layer 3, wired 2026-06-12):** `library/by-topic/` is mirrored to Google Drive at `HvH-library/by-topic/` (rclone remote `gdrive`, same Google account as NotebookLM).
   - **Upload fallback:** if a local `source_add(source_type="file")` fails (size/timeout), find the file's Drive copy via `mcp__notebooklm__source_list_drive` (search by canonical filename) and add it with `source_add(source_type="drive", document_id=...)`. Drive-sourced notebook sources can later be refreshed with `mcp__notebooklm__source_sync_drive`.
   - **Keep mirror fresh:** after new PDFs land in `library/by-topic/`, run `powershell tools/drive_sync.ps1` (wraps `rclone sync`; `-Check` verifies without transferring).
   - **SKIP path:** if rclone is missing or its auth is expired, continue with local-file uploads only — the mirror is a convenience, never a gate.

**Note:** Owned sources upload automatically (above). For the `[ACQUIRE]` remainder, Codex surfaces the Stage B→C checklist; user confirms acquisition/upload before Stage C begins.

### Stage B Lock

Surface conversationally: *"Stage B (Source Criticism) complete — ready for Stage C (Corroboration)?"*

Run the Stage B→C checklist in `.Codex/skills/historian/STAGE-AUDITS.md` before confirming. On user confirm, update `## Historian Stage State` in `PROJECT-STATUS.md`:

```
## Historian Stage State
**Current stage:** Stage B — Source Criticism (locked [YYYY-MM-DD])
**Next stage:** Stage C — Corroboration
**Outstanding flags:** [None / list]
**Stage A locked:** [date]
**Stage B locked:** [YYYY-MM-DD]
**Stage C locked:** pending
```

### Step 9: Report and Next Steps

```
Project created: video-projects/_IN_PRODUCTION/[folder]/

Files created:
- 01-VERIFIED-RESEARCH.md (start here)
- SCRIPT.md (placeholder - locked until research 90% verified)
- 03-FACT-CHECK-VERIFICATION.md (placeholder)
- PROJECT-STATUS.md
- _research/00-PRELIMINARY-BRIEF.md (Wikipedia pre-research — auto-generated)
- _research/00-NOTEBOOKLM-SOURCE-LIST.md (sources to download)
- _research/01-PRELIMINARY-RESEARCH.md (internet research)

Claims from database: [X claims pre-populated / None found]
Brief: [N] Wikipedia sources fetched, [N] claims flagged for verification,
       [N] academic sources identified from Wikipedia references

NEXT STEPS:
1. Review 00-PRELIMINARY-BRIEF.md — check the "Underexplored Angles" section
2. Download sources from 00-NOTEBOOKLM-SOURCE-LIST.md (brief's Academic Sources table helps prioritize)
3. Upload to NotebookLM
4. Run /sources to generate verification prompts
5. Verify claims and update 01-VERIFIED-RESEARCH.md
6. When 90%+ verified, run /script to write
```

---

## COMPETITOR GAP ANALYSIS (`--competitors`)

Analyze what competing YouTube videos cover on a topic and identify gaps.

### Usage

```
/research --competitors "Treaty of Tordesillas"
/research --competitors 42-why-brazil-speaks-portuguese-2026
```

### Process

1. Launch `competitor-gap` agent with the topic
2. Agent WebSearches YouTube for top competing videos
3. Fetches transcripts via `get-transcript.py`
4. Extracts topics, figures, dates, sources from each
5. Compares against your planned coverage (if project exists)
6. Outputs gap report with unique angles and recommendations

### Output

If a project path is detected: saves to `_research/COMPETITOR-GAP-ANALYSIS.md`
If standalone topic: displays report directly

**Key insight the report provides:** "All competitors tell the same story about X. None of them show the actual document / cover the Y angle / cite academic sources. That's your edge."

### When to use

- **Before scripting:** Run after `/research --brief` to know what angle to take
- **During revision:** If your script feels generic, run this to find what makes it different
- **Before filming:** Final check that your video adds something competitors don't

---

## BRIEF-ONLY WORKFLOW (`--brief`)

Generate a Wikipedia pre-research brief without creating a full project:

1. Launch `wiki-researcher` agent with the topic
2. Agent fetches Wikipedia + related articles + news + competitors
3. Output displayed directly (not saved to a project folder)

**Use when:** Evaluating a topic before committing. "Is there enough here for a video?"

**If topic looks viable:** Run `/research --new [topic]` to create the project (the brief will auto-run again inside the project folder).

**Example:**
```
/research --brief "Scramble for Africa"
```

Produces a structured brief with timeline, claims, competitor landscape, and academic sources — all in ~2-3 minutes. No project folder created.

---

## TOPIC-ONLY WORKFLOW (`--topic-only`)

Skip project creation, just research a topic:

1. Check VERIFIED-CLAIMS-DATABASE for existing research
2. Conduct preliminary internet research
3. Identify academic sources needed
4. Generate NotebookLM source recommendations
5. Output research summary (not saved to project folder)

**Use when:** Exploring topic viability before committing to video

---

## EXISTING PROJECT WORKFLOW (`--existing`)

### Migration Inference (for projects without Stage markers)

On entry, check `PROJECT-STATUS.md` for a `## Historian Stage State` section. If absent, infer stage from artifacts:

| Evidence | Inferred stage |
|---|---|
| 20+ ✅ claims in `01-VERIFIED-RESEARCH.md` + notebook ID present | Stage C — Corroboration |
| `_research/00-NOTEBOOKLM-SOURCE-LIST.md` exists + NLM notebook populated + <5 ✅ claims | Stage B — Source Criticism |
| `_research/00-PRELIMINARY-BRIEF.md` exists + no NLM notebook | Stage A — Historiographical Baseline |

Surface to user: *"I infer Stage C based on [evidence]. Confirm?"* Write the `## Historian Stage State` section to `PROJECT-STATUS.md` **below** `<!-- /AUTO:reconcile -->` only after user confirms.

Then apply the historian skill continuously from the inferred stage forward. Flag audit on existing claims: scan `01-VERIFIED-RESEARCH.md` for verbatim quotes without NLM source IDs and single-source [S] on-screen claims — surface any `[FLAG: *]` findings before proceeding with new research.

Add research to an existing project:

1. **Find project:** Use glob to locate folder
2. **Check current state:** What research exists?
3. **Identify gaps:** What claims need verification?
4. **Conduct targeted research** for gaps
5. **Update 01-VERIFIED-RESEARCH.md** with new findings

**Use when:** Adding research to in-progress project

---

## Stage C — Corroboration (`--ingest`, `--apply-review`)

Ingest NotebookLM chat output into structured verified claims.

### Prerequisites
- Project must exist (use `/research --new` first)
- `01-VERIFIED-RESEARCH.md` must exist in the project folder

### Step 1: Get NLM Output

Ask the user for NotebookLM output:
1. **Paste directly** — for short outputs (< 50 lines), ask user to paste into chat
2. **File path** — for long outputs, ask user to save as a `.txt` or `.md` file and provide the path

### Step 2: Locate Project Folder

Use Glob to find the project folder, then verify `01-VERIFIED-RESEARCH.md` exists inside it.

### Step 3: Parse and Extract

Run `nlm_ingest.ingest()` with the input text and project path:

```python
import sys
sys.path.insert(0, 'tools/research')
from nlm_ingest import ingest
result = ingest(input_text=text, project_path=project_folder)
```

Or, if user saved NLM output to a file:
```python
result = ingest(input_file=file_path, project_path=project_folder)
```

Display extraction stats to the user:
```
Parsed NLM output: 45 lines → 12 claims extracted

By type:
- Statistics: 4
- Quotes: 3
- Events: 3
- Definitions: 1
- General Claims: 1

Review file created: video-projects/_IN_PRODUCTION/31-bermeja-island-2025/_research/_NLM-REVIEW-2026-02-20-1342.md
```

### Step 4: User Reviews Claims

Tell the user:

> "I've created a review file at `[path]`. Open it and:
> - Check `[x]` next to claims you want to approve
> - Leave `[ ]` next to claims you want to reject
> - Edit any text or citation text directly before approving
>
> When done, run `/research --apply-review [path]`"

### Step 5: Apply Approved Claims (`--apply-review`)

When the user returns with the reviewed file path:

```python
import sys
sys.path.insert(0, 'tools/research')
from nlm_ingest import apply_review
result = apply_review(
    review_path=path,
    verified_research_path=vr_path
)
```

Display results to the user:
```
Applied 8/12 claims to 01-VERIFIED-RESEARCH.md

Sections updated:
- KEY STATISTICS: 3 claims added
- KEY QUOTES: 2 claims added
- TIMELINE: 2 claims added
- INGESTED CLAIMS (Unsorted): 1 claim added

Rejected: 4 claims skipped
```

**IMPORTANT:** This command orchestrates the flow but actual parsing and writing happens in `tools/research/nlm_ingest.py`. Codex reads this command, then runs the Python tool via Bash. Do NOT attempt to import Python directly from the command file — run it as a subprocess or Bash execution.

### Step 6 (post-apply): Mechanism-Word Lock Gate (P11.1b)

> **Post-NLM half of the viability gate** (other half: Step 6.5 Topic Viability Gate, Phase 1). Required because mechanism-word grounding can only be checked against an actual NLM notebook, not against a Phase 1 brief. See `feedback-notebook-citation-grounding.md` §'mechanism claims' for the canonical NLM-confidence query. See `feedback-auditors-edge.md` title-extension for why mechanism words in titles must be grounded at T1/T2.

**Trigger condition:** Fires automatically the first time `--apply-review` ingests claims into a project where `RESEARCH-VIABILITY.md` exists with mechanism-word candidates flagged for post-ingestion check. Subsequent `--apply-review` passes skip this gate if all candidates already have a verdict (LOCK / SOFTEN / SWAP recorded in `RESEARCH-VIABILITY.md`).

**Single check: mechanism-word NLM-confidence.** For each mechanism-word candidate listed in `RESEARCH-VIABILITY.md` "Mechanism-word candidates" section:
1. Run a NotebookLM confidence query using the notebook for this project. Use `feedback-notebook-citation-grounding.md` scope-b rules: query must be bidirectional — confirm both that the source uses the term AND that the source is the originator, not citing another scholar.
2. Returns: HIGH / MEDIUM / LOW confidence per candidate.

**Verdict logic (per candidate):**
- **LOCK** — Candidate returns HIGH confidence. Mechanism word is defensible at title stage. Record in `RESEARCH-VIABILITY.md`.
- **SOFTEN** — Candidate returns MEDIUM. Either soften the language (e.g., "translation ambiguity" instead of "forgery") OR acquire more sources to raise confidence. Re-check after source acquisition.
- **SWAP** — Candidate returns LOW. Drop this candidate; try the next one on the list. If all candidates return LOW, escalate to user — this topic may lack a defensible mechanism word, which may invalidate the original viability verdict.

**Output: append to `RESEARCH-VIABILITY.md`.** Append section titled "## Mechanism-Word Lock Gate (post-NLM)":
```markdown
## Mechanism-Word Lock Gate (post-NLM)
**Date:** [YYYY-MM-DD]
**Notebook ID:** [NLM project notebook ID]

| Candidate | NLM confidence | Action | Notes |
|---|---|---|---|
| [word] | HIGH / MEDIUM / LOW | LOCK / SOFTEN / SWAP | [source + page if LOCK; soften version if SOFTEN; reason if SWAP] |

**Locked mechanism word:** [word] — or "NONE — escalating to user" if all candidates SWAPped.
```

**Gate behavior:** Title locking (in `/script` or `/greenlight` final pass) cannot proceed until at least one mechanism-word candidate has LOCKED. If all SWAP'd and no fallback candidate exists, return the topic to viability assessment (the lack of a defensible mechanism word is a substantive-viability failure).

### Step 7 (post-apply): Angle-Discovery Pass (P11.2)

> **Routes specificity discipline upstream of script-write.** Fires after `--apply-review` has ingested claims AND P11.1b has LOCKED at least one mechanism-word candidate. Skips if no claims were ingested (nothing new to mine) or if mechanism-word gate hasn't produced a LOCK yet. See `THESIS-DISCIPLINE.md` for the thesis-verb framework, `feedback-auditors-edge.md` tier-vibe for hook quote tiering, `script-writer-v2` Rules 17/36/32G for downstream consumers.
>
> **Distinction from Step 1c title pre-generation:** Step 1c brainstorms title candidates via Ollama (packaging layer). Angle-discovery surfaces hook quotes + thesis verbs + closing payoffs from the NLM notebook (content layer). No overlap.

**Trigger condition:** Fires after `--apply-review` successfully ingests claims AND P11.1b shows at least one LOCK in `RESEARCH-VIABILITY.md`. Skips if the mechanism-word gate has not yet run or has no LOCK.

**Three angle-discovery NLM queries** (canonical prompts in `.Codex/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` — see section "Angle-Discovery Prompts (P11.2)"):

- **Query AD-1 — Candidate Hook Quotes (specificity-ranked).** Top 5 most specific, surprising, anchor-able quotes from the notebook. Each must contain ≥1 named person + ≥1 named document or date + ≥1 concrete fact. Rank by specificity-bomb score. Output: quote + source + page + T-tier + score.
- **Query AD-2 — Candidate Thesis Verbs.** Top 3 verbs describing what historical actors actually did in this topic, with quote evidence supporting each. Pairs with the locked mechanism word from P11.1b. Output: verb + evidence + NLM-confidence.
- **Query AD-3 — Candidate Closing Payoffs.** Top 3 most surprising or anchoring facts that could carry the script's closing beat. Rank by surprise + concreteness + memorability. Output: fact + source + suggested phrasing.

**Output to `01-VERIFIED-RESEARCH.md`** — section titled `## CANDIDATE ANGLES`. **OVERWRITE behavior (locked U4):** each `--apply-review` run that ingests claims REPLACES this entire section with fresh output. Do NOT append dated sub-sections; the section is always current-as-of-latest-pass. The dated header records when the latest pass ran.

Format:
```markdown
## CANDIDATE ANGLES (NLM-discovered, --apply-review pass [YYYY-MM-DD])

### Hook Quote Candidates (specificity-ranked)
1. **Score 95** | T1 | "[quote]" | [Author], *[Title]*, p. [X]
2. **Score 88** | T2 | "[quote]" | [Author], *[Title]*, p. [X]
3. ...

### Thesis Verb Candidates
1. [verb] | NLM HIGH | evidence: "[...]" | [source], p. [X]
2. [verb] | NLM MEDIUM | evidence: "[...]" | [source], p. [X]
3. [verb] | NLM HIGH | evidence: "[...]" | [source], p. [X]

### Closing Payoff Candidates
1. [fact] | [source], p. [X] | suggested closing: "[draft phrasing]"
2. ...
```

**Downstream consumption:** When `/script` starts, it reads this section. The writer (or `script-writer-v2` agent) picks from candidates or explicitly rejects with reason. Enforced at script-stage via `script-writer-v2` Rules 17 (hook anchoring), 36 (thesis discipline), and 32G (closer specificity).

### Stage C Lock

Surface conversationally after all `--apply-review` passes are complete and angle-discovery has run: *"Stage C (Corroboration) complete — ready to script?"*

Run the Stage C→Ready-to-Script checklist in `.Codex/skills/historian/STAGE-AUDITS.md` before confirming. On user confirm, update `## Historian Stage State` in `PROJECT-STATUS.md`:

```
## Historian Stage State
**Current stage:** Stage C — Corroboration (locked [YYYY-MM-DD])
**Next stage:** Phase 2 — Script (/script)
**Outstanding flags:** [None / list of any deferred flags with logged rationale]
**Stage A locked:** [date]
**Stage B locked:** [date]
**Stage C locked:** [YYYY-MM-DD]
```

Update `01-VERIFIED-RESEARCH.md` status line to `READY TO WRITE SCRIPT`.

---

## Quality Gates (Enforced)

**Gate 1: Research → Script**
Cannot proceed to scripting until:
- [ ] 90%+ claims verified
- [ ] All major quotes word-for-word exact
- [ ] All archival refs precise
- [ ] All numbers have 2+ sources
- [ ] 01-VERIFIED-RESEARCH.md status: "READY TO WRITE SCRIPT"

---

## Reference Files

- **Templates:** `.Codex/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- **Research subfolder:** `.Codex/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md`
- **Source standards:** `.Codex/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`
- **Claims database:** `.Codex/VERIFIED-CLAIMS-DATABASE.md`
- **Technique library:** `.Codex/REFERENCE/WRITING-VOICE-AND-STYLE-P5-TECHNIQUES.md`
- **Gap database:** `.Codex/REFERENCE/GAP-DATABASE.md`

---

## After Completion

When project setup is complete, suggest:

> "Project created! Your next step: Load sources into NotebookLM and verify claims in 01-VERIFIED-RESEARCH.md.
> When research is 90%+ verified, run `/script` to write from verified facts."

**If topic-only mode:** Suggest creating full project if topic looks viable:

> "Research complete. This topic has [X] key claims to verify.
> Ready to commit? Run `/research --new` to create the project folder."

---

## Absorbed Commands

This command consolidates functionality from:
- `/new-video` - Project creation and setup
- `/find-topic` - Topic research and validation
- `/deep-research` - Comprehensive topic research

All original functionality preserved through flags and workflow stages.
