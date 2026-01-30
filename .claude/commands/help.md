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

## Pre-production

Start new projects and gather research.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/research` | Start new video, topic research | `--new`, `--topic-only`, `--existing` |
| `/sources` | Source recommendations, NotebookLM prompts | - |

**When to use:**
- Starting a new video idea
- Researching a topic before committing
- Setting up NotebookLM for academic verification

---

## Production

Write scripts and verify accuracy.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/script` | Write, revise, or review scripts | `--new`, `--revise`, `--review`, `--teleprompter` |
| `/verify` | Fact-check verification | `--script`, `--extract`, `--simplify`, `--from-transcript` |
| `/prep` | Filming preparation | `--edit-guide`, `--assets` |

**When to use:**
- Writing script from verified research
- Reviewing script for quality issues
- Fact-checking before filming
- Creating edit guide and B-roll checklist

---

## Post-production

Publish, fix issues, and engage with audience.

| Command | Purpose | Flags |
|---------|---------|-------|
| `/publish` | YouTube metadata, titles, clips | `--titles`, `--clips` |
| `/fix` | Fix subtitle errors | - |
| `/engage` | Comment response, corrections | `--respond`, `--correction`, `--save` |

**When to use:**
- Creating YouTube title, description, tags
- Generating title variants for A/B testing
- Fixing auto-transcription errors in .srt files
- Responding to viewer comments
- Publishing corrections for errors

---

## Meta

Navigation and help.

| Command | Purpose |
|---------|---------|
| `/status` | Project state, next action suggestion |
| `/help` | This command menu |

**When to use:**
- "What should I do next?"
- Finding the right command for a task

---

## Natural Language Routing

You don't need to remember commands. Just describe what you want:

| You Say | I Suggest |
|---------|-----------|
| "I want to start a video about X" | `/research --new "X"` |
| "I need to write a script" | `/script --new [project]` |
| "The script is done" | `/verify` |
| "I need to fact-check this" | `/verify --script [project]` |
| "Ready to film" | `/prep --edit-guide` |
| "Need YouTube metadata" | `/publish` |
| "Fix my subtitles" | `/fix` |
| "Someone left a comment" | `/engage --respond` |
| "I made a mistake in a video" | `/engage --correction` |
| "What should I do?" | `/status` |

---

## Quick Reference

### Full Workflow (New Video)

```
1. /research --new "Topic"     # Create project, start research
2. /sources                     # Get NotebookLM prompts
3. [Manual: Upload to NotebookLM, verify claims]
4. /script --new                # Write from verified research
5. /verify                      # Fact-check script
6. /prep                        # Edit guide + B-roll
7. [Manual: Film and edit]
8. /publish                     # YouTube metadata
9. /fix                         # Fix subtitles if needed
10. /engage                     # Handle comments
```

### Common Tasks

| Task | Command |
|------|---------|
| Check project status | `/status` |
| Review script quality | `/script --review` |
| Export for teleprompter | `/script --teleprompter` |
| Extract claims from video | `/verify --extract [file]` |
| Generate title variants | `/publish --titles` |
| Find clip-worthy moments | `/publish --clips` |

---

## Getting Context-Specific Help

If you provide a topic, I'll show relevant commands with more detail:

```
/help fact-check     # Show verification commands in detail
/help script         # Show script-related commands in detail
/help publishing     # Show post-production commands in detail
```

---

## Command Count

**Total commands:** 10
- Pre-production: 2
- Production: 3
- Post-production: 3
- Meta: 2

All commands consolidated from previous ~20+ commands with flags preserving full functionality.

---

## Tip

Just describe what you want to do. I'll route you to the right command.

Example: "I finished researching the Library of Alexandria video and want to write the script now."

I'll check your project status and suggest `/script --new 15-library-alexandria-2025`.
