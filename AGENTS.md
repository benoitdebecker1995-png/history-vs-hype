# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

**History vs Hype** is a YouTube channel content production repository for evidence-based, myth-busting history videos. The channel uses academic sources and primary documents displayed on screen—the key competitive advantage over commentary channels.

**Channel DNA:** History-first with modern relevance. The historical source/event is the core content (60-80%), modern relevance is the hook (20-40%). NOT geopolitics with historical background.

## Quick Commands

| Phase | Command | Purpose |
|-------|---------|---------|
| Pre-production | `/research --new` | Start new video project |
| Pre-production | `/sources --recommend` | Source recommendations for NotebookLM |
| Production | `/script` | Generate script from verified research |
| Production | `/script --teleprompter` | Export for teleprompter |
| Production | `/verify --script` | Fact-check verification |
| Post-production | `/publish --metadata` | YouTube metadata package |
| Post-production | `/fix` | Fix subtitle errors |
| Navigation | `/status` | Current project state + next action |
| Navigation | `/help` | Full command list |

## Architecture

### Folder Structure

```
video-projects/
├── _IN_PRODUCTION/     # Active research and scripting
├── _READY_TO_FILM/     # Finalized scripts ready for filming
└── _ARCHIVED/          # Published or cancelled projects

.claude/
├── agents/             # Agent configurations (fact-checker, script-writer-v2, etc.)
├── commands/           # Slash command definitions
├── REFERENCE/          # Style guides, fact-checking protocols
│   ├── STYLE-GUIDE.md  # Authoritative voice/delivery reference
│   └── fact-checking-protocol.md
└── USER-PREFERENCES.md # Working style, efficiency expectations

tools/
├── youtube-analytics/  # Channel analytics tools
└── script-checkers/    # Script validation
```

### Standard Project Files

```
[project-folder]/
├── 01-VERIFIED-RESEARCH.md       # Single source of truth (✅/⏳/❌ markers)
├── 02-SCRIPT-DRAFT.md            # Script from verified facts only
├── 03-FACT-CHECK-VERIFICATION.md # Final quality gate
├── PROJECT-STATUS.md             # Progress tracking
├── NOTEBOOKLM-SOURCE-LIST.md     # Academic sources to download
├── NOTEBOOKLM-PROMPTS.md         # Research prompts
├── FINAL-SCRIPT.md               # Ready for filming
├── YOUTUBE-METADATA.md           # Title, description, tags, chapters
└── EDITING-GUIDE-SHOT-BY-SHOT.md # Visual staging
```

## Critical Workflows

### Two-Phase Research (The Competitive Advantage)

**Phase 1: Preliminary Internet Research** — Map the landscape, identify claims to verify (Wikipedia, Google Scholar previews, news). Mark all findings as ❓ until verified.

**Phase 2: NotebookLM Academic Verification** — Download 10-20 academic sources from university presses (Cambridge, Oxford, Chicago, Harvard). Upload to NotebookLM. Run targeted prompts. Extract exact quotes with page numbers.

**NEVER skip Phase 2.** This is what sets the channel apart from commentary YouTubers.

### Three-Phase Verified Workflow

1. **Research + Verify** → `01-VERIFIED-RESEARCH.md` (90%+ verified before proceeding)
2. **Write Script** → `02-SCRIPT-DRAFT.md` (ONLY from verified facts)
3. **Cross-Check** → `03-FACT-CHECK-VERIFICATION.md` (100% match required)

**Result:** 5.5 hours vs. 9 hours (old workflow), zero errors vs. 2+ per video.

## Key Principles

1. **Real quotes with page numbers** — "According to Chris Wickham in *The Inheritance of Rome*, page 147..." not "historians say..."
2. **Primary sources displayed on screen** — Show the treaty document, manuscript, or court ruling visually
3. **Academic-level sources only** — University press publications, top scholars, critical editions. Budget is unlimited.
4. **Scripts for spoken delivery** — Teleprompter reading. Use contractions, ordinal dates ("On June 16th, 2014,"), natural flow.
5. **Verify before including** — If you can't cite the specific source with timestamp/page number, don't include the claim.
6. **Check existing research first** — Search `**/RESEARCH*.md`, `**/VERIFIED*.md` before any web search.

## Style Quick Reference

See `.claude/REFERENCE/STYLE-GUIDE.md` for complete rules.

| Rule | Wrong | Right |
|------|-------|-------|
| Dates | "June 16, 2014." | "On June 16th, 2014," |
| Contractions | "it is" | "it's" |
| Technical terms | "estoppel" | "estoppel — a legal rule that..." |
| Lists (info) | "Britain. France. Egypt." | "Britain, France, Egypt" |
| "Here's" usage | 10+ per script | 2-4 max |
| Abbreviations | "The AU" (first use) | "The African Union" |

**Voice:** "Calm Prosecutor" — emotionally low, intellectually high. Evidence-based referee.

## Tool Stack

- **VidIQ Pro** — Topic research, script generation, clipping
- **NotebookLM (Gemini 2.0 Flash)** — Source-grounded academic research (2M token context)
- **DaVinci Resolve** — Video editing
- **Photoshop** — Thumbnail creation

## Working Style Expectations

- **Read files first, ask questions later** — Use Glob to find context before asking
- **Parallel tool calls** — When multiple independent reads/searches needed
- **Direct and efficient** — No unnecessary pleasantries, minimize questions
- **Never create loose folders** — Always use lifecycle folders (_IN_PRODUCTION, etc.)
- **Check COMPLETE-PERFORMANCE-DATABASE.md** — Before suggesting topics (user may have already covered them)

## For Complete Documentation

- **Full channel context:** `CLAUDE.md`
- **Working style details:** `.claude/USER-PREFERENCES.md`
- **Style rules:** `.claude/REFERENCE/STYLE-GUIDE.md`
- **Folder system:** `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md`
- **Fact-checking:** `.claude/REFERENCE/fact-checking-protocol.md`
