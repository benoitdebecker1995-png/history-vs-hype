---
name: "source-command-help"
description: "Phase-organized command menu and capability discovery"
---

# source-command-help

Use this skill when the user asks to run the migrated source command `help`.

## Command Template

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
- Fixing auto-transcription errors → `/fix` (use this, not generic Codex)
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

Article-writer agent (`.Codex/agents/article-writer.md`) handles convert/write/edit/workshop modes directly. The command below evolves the agent.

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

**2026-05-03 consolidation:** Down from 28 commands. Archived to `.Codex/_ARCHIVE/commands-2026-05-03/`. Folded:
- `/discover --scan` → `/greenlight --scan`
- `/sources` → `/research --sources` / `--prompts` / `--format-sources`
- `/intel --score` / `--query` / `--algo` → `/patterns --score` / `--query` / `--intel`
- `/newsletter`, `/workshop` → `article-writer` agent (CONVERT / WRITE / EDIT / WORKSHOP modes)
- `/humanify` → article-writer Rule 1 (voice patterns from WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md)
- `/preflight`, `/deep-analytics`, `/think`, `/thesis-discovery` → archived (dead, redundant, or already executed)

---

## Tip

Just describe what you want to do. I'll route you to the right command.

Example: "I finished researching the Library of Alexandria video and want to write the script now." → I'll check your project status and suggest `/script --new 15-library-alexandria-2025`.
