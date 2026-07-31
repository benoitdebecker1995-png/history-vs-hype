---
description: Phase-organized command menu and capability discovery
model: haiku
---


# /help - History vs Hype Commands

Display available commands organized by production phase. Use this to discover capabilities or get help with specific tasks.

## Usage

```
/help                        # Show full command menu
/help [topic]                # Show relevant commands for topic
```

---

## Pre-production (5)

Pick topics, validate viability, set up the project.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/grill-angle` | Interrogate a topic's ANGLE before research — one-at-a-time grill → GO/REFRAME/KILL verdict | - |
| `/greenlight` | Pre-work viability gate (demand + title + thumbnail) | `--full`, `--scan`, `--project`, `--compare` |
| `/research` | Start new video, topic research, source list | `--new`, `--topic-only`, `--existing`, `--sources`, `--prompts` |
| `/next` | Ranked topic recommendations from winning patterns | - |
| `/translate` | Translation pipeline for "Untranslated Evidence" series | clause-by-clause translation |

**When to use:**
- Chosen a topic, unsure the angle is strong → `/grill-angle "topic"` (before `/greenlight`)
- "Should I make this video?" → `/greenlight "topic"`
- Weekly opportunity scan → `/greenlight --scan`
- Starting a new project → `/research --new "Topic"`
- "What should I make next?" → `/next`

---

## Production (4)

Write scripts, verify accuracy, prep for filming, design the package.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/script` | Write, revise, review, export scripts | `--new`, `--revise`, `--review`, `--teleprompter` |
| `/verify` | Fact-check script, extract claims, detect simplifications | `--script`, `--extract`, `--simplify` |
| `/prep` | Filming prep — edit guides, B-roll planning | `--edit-guide`, `--assets` |
| `/thumbnail` | Generate 3 ranked thumbnail concepts (outlier-grounded) | - |

**When to use:**
- Writing script from verified research → `/script --new`
- Fact-checking before filming → `/verify --script`
- Building edit guide / B-roll list → `/prep`
- Designing thumbnail concept → `/thumbnail`

---

## Post-production (4)

Publish, correct, engage, retitle.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/publish` | YouTube metadata, titles, clips | `--metadata`, `--titles`, `--clips`, `--full`, `--evaluate` |
| `/fix` | Fix subtitle errors from auto-transcription | - |
| `/engage` | Comment responses, corrections, feedback management | `--respond`, `--correction`, `--save` |
| `/retitle` | Retitle underperforming videos with audit + candidate generation | - |

**When to use:**
- Generating YouTube metadata → `/publish --metadata`
- Fixing auto-transcription errors → `/fix` (use this, not generic Claude)
- Responding to comments → `/engage --respond`
- Underperforming video → `/retitle`

---

## Analytics (3)

Diagnose what worked and why.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/analyze` | Per-video post-publish analysis (retention drops + recommendations) | `--script`, `--video-id` |
| `/growth` | Channel growth dashboard — velocity, ROI, traffic, monetization | - |
| `/patterns` | Cross-video pattern analysis + intelligence KB queries | `--topic`, `--title`, `--monthly`, `--score`, `--query`, `--intel`, `--outliers` |

**When to use:**
- After every published video → `/analyze VIDEO_ID --script PATH`
- Monthly health check → `/growth`
- Cross-video patterns and outliers → `/patterns`
- Score a topic idea 0-100 → `/patterns --score "title"`

---

## Article writing (1)

Article-writer agent (`.claude/agents/article-writer.md`) handles convert/write/edit/workshop modes directly. The command below evolves the agent.

| Command | Purpose |
|---------|---------|
| `/learn-from-paper` | Mine an academic paper for transferable techniques; output diff proposals for article-writer (and tagged crossovers for script-writer-v2) |

**Note:** If you want to write an article, invoke the article-writer agent directly — no command wrapper needed.

---

## Meta (2)

| Command | Purpose |
|---------|---------|
| `/status` | Project state, next action suggestion |
| `/help` | This command menu |

---

## Natural Language Routing

You don't need to remember commands. Just describe what you want:

| You Say | I Suggest |
|---------|-----------|
| "Should I make a video about X?" | `/greenlight "X"` |
| "What's a good topic this week?" | `/greenlight --scan` or `/next` |
| "I want to start a video about X" | `/research --new "X"` |
| "I need to write a script" | `/script --new [project]` |
| "The script is done" | `/verify` |
| "I need to fact-check this" | `/verify --script [project]` |
| "Ready to film" | `/prep --edit-guide` |
| "Need a thumbnail" | `/thumbnail` |
| "Need YouTube metadata" | `/publish` |
| "Fix my subtitles" | `/fix` |
| "Someone left a comment" | `/engage --respond` |
| "I made a mistake in a video" | `/engage --correction` |
| "Why did this video flop?" | `/analyze VIDEO_ID --script SCRIPT.md` |
| "Channel performance check" | `/growth` |
| "What patterns are working?" | `/patterns` |
| "Score this topic idea" | `/patterns --score "title"` |
| "Underperforming video — retitle?" | `/retitle` |
| "What should I do?" | `/status` |

---

## Full Workflow (New Video)

```
1. /greenlight "Topic"          # Will this earn the click?
2. /research --new "Topic"      # Create project, start research
3. /research --sources "Topic"  # Generate Tier 1/2/3 source list
4. [Manual: Upload to NotebookLM, verify claims]
5. /script --new                # Write from verified research
6. /verify                      # Fact-check script
7. /prep                        # Edit guide + B-roll
8. /thumbnail                   # 3 ranked concepts
9. [Manual: Film and edit]
10. /publish                    # YouTube metadata
11. /fix                        # Fix subtitles
12. /engage                     # Handle comments
13. /analyze VIDEO_ID --script  # Post-publish diagnosis
```

---

## Command Count

**Total: 18 commands**
- Pre-production: 4 (greenlight, research, next, translate)
- Production: 4 (script, verify, prep, thumbnail)
- Post-production: 4 (publish, fix, engage, retitle)
- Analytics: 3 (analyze, growth, patterns)
- Article writing: 1 (learn-from-paper)
- Meta: 2 (status, help)

**2026-05-03 consolidation:** Down from 28 commands. Archived to `.claude/_ARCHIVE/commands-2026-05-03/`. Folded:
- `/discover --scan` → `/greenlight --scan`
- `/sources` → `/research --sources` / `--prompts` / `--format-sources`
- `/intel --score` / `--query` / `--algo` → `/patterns --score` / `--query` / `--intel`
- `/newsletter`, `/workshop` → `article-writer` agent (CONVERT / WRITE / EDIT / WORKSHOP modes)
- `/humanify` → article-writer Rule 1 (voice patterns from WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md)
- `/deep-analytics`, `/think`, `/thesis-discovery` → archived (dead, redundant, or already executed)
  *(`/preflight` was listed here as archived until 2026-07-30, but it exists and is live —
  see the full command index below. It was rebuilt after the 2026-05-03 consolidation.)*

---

## Tip

Just describe what you want to do. I'll route you to the right command.

Example: "I finished researching the Library of Alexandria video and want to write the script now." → I'll check your project status and suggest `/script --new 15-library-alexandria-2025`.

---

## Full command index

<!-- AUTO:command-list generated by tools/docs_index.py — do not hand-edit -->
*33 commands, generated from `.claude/commands/`. Regenerate with `python -m tools.docs_index --write`.*

| Command | Purpose |
|---|---|
| `/analyze` | Run complete post-publish analysis on any video |
| `/comment-mine` | Mine YouTube competitor comments to measure audience demand for thesis angles |
| `/curiosity` | Evaluate a title's human psychology, curiosity gap, and emotional stakes |
| `/editing-guide` | Generate a segment-by-segment editing playbook from a rough cut SRT (Post-production Phase 3) |
| `/engage` | Comment responses, corrections, and feedback management (Post-production Phase 3) |
| `/fix` | Fix subtitle errors from auto-transcription (Post-production Phase 2) |
| `/gemini` | Dispatch a bulk-read task to Gemini CLI (headless) and capture output to a file. Use for transcripts, source digestion, competitor scans, brain ingestion. |
| `/greenlight` | Pre-work viability gate — checks demand, titles, and thumbnails BEFORE you invest time |
| `/grill-angle` | Pre-research angle interrogation — grills a video's thesis/hook one question at a time BEFORE /greenlight, then writes a GO / REFRAME / KILL verdict with the sharpened angle. Use before sinking research hours into a topic. |
| `/growth` | Channel growth dashboard — velocity, ROI, traffic, monetization countdown |
| `/learn-from-paper` | Mine an academic article for transferable structural/voice/evidence/limitation-handling lessons via NotebookLM, filter through audience-fit skepticism, output diff proposals for article-writer (and tagged crossovers for script-writer-v2). Does NOT edit agent files — produces a proposal you approve. |
| `/next` | Get ranked topic recommendations based on winning patterns |
| `/opener` | Cold-open decision system — generates 3 candidate 30-second openers from project artifacts, scores them on 4 dimensions, writes ranked verdict to OPENER-DECISION.md |
| `/patterns` | Cross-Video Pattern Analysis |
| `/polish` | Final AI-pattern pass on a locked script before filming |
| `/preflight` | Full pre-upload scorecard — 5 script-stage gates + conditional rendered-asset QC (topic/script/title/thumb/duration + image + audio) |
| `/prep` | Filming preparation - edit guides, B-roll planning, asset creation (Production Phase 3) |
| `/publish` | YouTube metadata, title testing, clip suggestions (Post-production Phase 1) |
| `/reconcile` | Reconcile project state — folder lifecycle, AUTO blocks, derived docs. Auto-fires when user says "I uploaded/released/published X". |
| `/refactor` | Run the next eligible step in UPGRADE-PLAN.md (one step, then stop) |
| `/referee-retrofit` | Apply the #61 Black Legend research method to an existing INPRODUCTION project: $ARGUMENTS |
| `/research` | Start new video project OR conduct topic research (Pre-production Phase 1) |
| `/retitle` | Retitle underperforming videos — audit, generate candidates, output swap checklist |
| `/script-research-pass` | Full editor + head-of-research pass on a draft script — paragraph-by-paragraph NotebookLM verification (no context-economy skip), expository/predicate-drift, quote-card provenance, completeness, flow, writing polish, and script↔teleprompter lock discipline. |
| `/script` | Write, revise, review, or export scripts (Production Phase 1) |
| `/status` | Smart project status and next action suggestion (responds to "what should I do?") |
| `/thumbnail` | Generate 3 ranked thumbnail concepts grounded in the close-match outlier corpus + per-channel playbook |
| `/translate` | Translate legal/historical documents clause-by-clause with cross-checking, legal annotations, and surprise detection (Untranslated Evidence series) |
| `/verify-flow-nlm` | Run narrative-flow verification + NotebookLM claim-query verification on a script (the deeper pass /verify --script skips for context-economy) |
| `/verify` | Fact-check scripts, extract claims, detect simplifications (Production Phase 2) |
| `/voice-clickdrill` | Click-based voice calibration — the grill loop with an AskUserQuestion click UI instead of chat A/B, so the creator just clicks options. Low-effort. |
| `/voice-readthrough` | AI dry-run of the creator read-aloud on an UNLOCKED draft SCRIPT.md — read every beat in his voice, flag stumbles with concrete rewrites, and sharpen VOICE-PROFILE.md from what the read surfaces. Precedes the human T1 read-aloud; goal = zero feedback when he reads it. |
| `/voice` | Voice work — one command, three modes. grill (recurring calibration, default) · discover (full bootstrap) · tooling (build/extend linter). Sharpens the creator's canonical voice profile. |
<!-- /AUTO:command-list -->
