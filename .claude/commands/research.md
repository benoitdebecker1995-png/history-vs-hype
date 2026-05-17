---
description: Start new video project OR conduct topic research (Pre-production Phase 1)
model: sonnet
---

# /research - Pre-production Research Entry Point

Start a new video project or research an existing topic. This command consolidates project setup, topic research, and NotebookLM preparation.

**Competitive Integration:** This workflow includes competitor analysis and technique selection.

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
| `--sources` | Generate Tier 1/2/3 academic source list via Claude API | `/research --sources "Library of Alexandria"` |
| `--prompts` | Generate NotebookLM verification prompts for a project | `/research --prompts 19-flat-earth-medieval-2025` |
| `--format-sources` | Format source list for YouTube description | `/research --format-sources` |

---

## SOURCE WORKFLOWS (folded from /sources, 2026-05-03)

### `--sources` — Automated source-list generation

Generates an academic source list using `tools/notebooklm_bridge.py` (Claude API-backed).

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

Generate NotebookLM chat prompts tailored to a project's verified-claims gaps. References `.claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` for the prompt library.

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

1. **Read:** `.claude/VERIFIED-CLAIMS-DATABASE.md`
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

**01-VERIFIED-RESEARCH.md** - Copy from `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- Fill in project name, date, topic categories
- Pre-populate with any claims from VERIFIED-CLAIMS-DATABASE

**PROJECT-STATUS.md** - Create with phase tracking:
- Phase 1: Research (current)
- Phase 2: Script (locked until 90% verified)
- Phase 3: Fact-check (locked until script complete)

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

### Step 7: Competitive Intelligence Check

After preliminary research, before deep research:

1. **Check what competitors covered:**
   - Search YouTube for "[topic]" - who has videos?
   - Note their angle, length, and apparent sources
   - What's missing from their coverage?

2. **Check for applicable techniques:**
   - Skim `WRITING-VOICE-AND-STYLE.md` PART 5 (Techniques Toolkit) for relevant techniques
   - Which opening hook fits this topic?
   - What evidence presentation style works here?
   - Note intended techniques in PROJECT-STATUS.md

3. **Check gap database:**
   - Is this topic in `GAP-DATABASE.md`?
   - If new, add it with preliminary scores
   - If existing, update status to "Researching"

> **Proactive:** "I've checked competitor coverage of [topic]. The main videos are [list]. Your unique angle could be [suggestion based on channel DNA]."

### Step 8: Create NotebookLM Source List

Based on preliminary research and the brief's Academic Sources table, create:
- `_research/00-NOTEBOOKLM-SOURCE-LIST.md`

**Standards (from NOTEBOOKLM-SOURCE-STANDARDS.md):**
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard)
- Top-tier scholars (endowed chairs, major universities)
- Critical editions of primary sources
- Budget is UNLIMITED - recommend best sources regardless of price

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

Add research to an existing project:

1. **Find project:** Use glob to locate folder
2. **Check current state:** What research exists?
3. **Identify gaps:** What claims need verification?
4. **Conduct targeted research** for gaps
5. **Update 01-VERIFIED-RESEARCH.md** with new findings

**Use when:** Adding research to in-progress project

---

## NLM INGESTION WORKFLOW (`--ingest`)

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

**IMPORTANT:** This command orchestrates the flow but actual parsing and writing happens in `tools/research/nlm_ingest.py`. Claude reads this command, then runs the Python tool via Bash. Do NOT attempt to import Python directly from the command file — run it as a subprocess or Bash execution.

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

- **Templates:** `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- **Research subfolder:** `.claude/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md`
- **Source standards:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`
- **Claims database:** `.claude/VERIFIED-CLAIMS-DATABASE.md`
- **Technique library:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` PART 5 (Techniques Toolkit)
- **Gap database:** `.claude/REFERENCE/GAP-DATABASE.md`

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
