# Deprecated Commands

These commands were consolidated in Phase 5 (Workflow Simplification) on 2026-01-22.

## Migration Table

| Old Command | Replaced By | Notes |
|-------------|-------------|-------|
| /new-video | /research --new | Full project setup with 3-phase workflow |
| /find-topic | /research --topic | Topic research and VidIQ integration |
| /deep-research | /research --existing | Deep research on existing project |
| /suggest-sources | /sources --recommend | Source recommendations for NotebookLM |
| /notebooklm-prompts | /sources --prompts | NotebookLM prompt generation |
| /format-sources | /sources --format | Source list formatting for video description |
| /fact-check | /verify --script | Full fact-check verification |
| /extract-claims | /verify --extract | Extract claims from transcript |
| /edit-guide | /prep --edit-guide | Shot-by-shot editing guide |
| /zero-budget-assets | /prep --assets | DIY B-roll guide with free tools |
| /youtube-metadata | /publish --metadata | Full metadata package |
| /test-titles | /publish --titles | Title variants for A/B testing |
| /clip-suggestions | /publish --clips | Clip-worthy moments for Shorts |
| /respond-to-comment | /engage --respond | Comment response with research |
| /publish-correction | /engage --correction | Document and publish corrections |
| /save-comment | /engage --save | Save insightful comments |
| /teleprompter | /script --teleprompter | Export clean teleprompter text |
| /review-script | /script --review | Comprehensive script analysis |
| /fix-subtitles | /fix | Subtitle error correction |
| /evaluate-feedback | (removed) | Rarely used - feedback now auto-filtered |
| /analyze-interview | (removed) | Rarely used - use /verify --extract instead |

## Why Deprecated?

The 20+ command system was difficult to remember. User workflow analysis showed:
- User describes what they want in natural language
- User relies on Claude to know the system
- Commands organized by phase make more mental sense

## Current Command System

**Run `/help` to see the current command list.**

Phase organization:
- **Pre-production:** /research, /sources
- **Production:** /script, /verify, /prep
- **Post-production:** /publish, /fix, /engage
- **Navigation:** /status, /help

---

**Do not use these deprecated commands.** They are preserved for reference only.
