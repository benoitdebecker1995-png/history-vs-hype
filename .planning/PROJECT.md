# History vs Hype Workspace

## What This Is

A content production workspace for History vs Hype, a YouTube channel focused on evidence-based history and myth-busting. The channel uses academic sources and primary documents to debunk historical myths that shape modern beliefs and conflicts. The core differentiator is showing sources on screen — viewers see the evidence, not just hear citations.

## Core Value

Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation. This is what separates the channel from competitors who just narrate over stock footage.

## Current State (v1.0 Shipped)

**Shipped:** 2026-01-23

The workspace has been optimized for solo creator efficiency:

- **Commands:** 10 phase-organized commands (research, sources, script, verify, prep, publish, fix, engage, status, help)
- **Style:** STYLE-GUIDE.md is authoritative reference (543 lines, 6 parts)
- **Research:** Claims database, standardized templates, 30-day cleanup rules
- **Scripts:** Single SCRIPT.md per project, git tracks versions
- **Intelligence:** Technique tracking, gap database (7 scored topics), creator watchlist

**Entry points:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project

## Current Milestone: v1.1 Analytics & Learning Loop

**Goal:** Build a feedback system that helps learn what works from each video, with automated YouTube Analytics integration.

**Target features:**
- YouTube Analytics API integration (CTR, retention, watch time pulls)
- Post-publish learning loop (7-day analysis, lessons logged)
- Cross-video pattern recognition (monthly insights)
- Experiment mode preserved (no pressure to always optimize)

## Requirements

### Validated (v1.0)

- Clean up outdated and duplicate files — v1.0
- Establish one canonical script file per video — v1.0
- Organize per-video research with clear source attribution — v1.0
- Create cross-video verified facts database — v1.0
- Simplify workflow (fewer commands) — v1.0
- Consolidate style notes into single authoritative reference — v1.0
- Scriptwriter produces spoken-delivery scripts — v1.0
- Competitive intelligence tracking — v1.0

### Active (v1.1)

- YouTube Analytics API integration for automated data pulls
- Post-publish learning loop (CTR, retention, audience signals)
- Cross-video pattern recognition system
- Experiment/strategic balance (gap database maintained, no optimization pressure)

### Out of Scope

- Building a new channel or brand — improving existing workspace
- Changing the core format (talking head + B-roll evidence) — optimizing execution
- Multi-person workflow — solo creator optimization
- Video editing automation — out of scope for this workspace

## Context

**What works:**
- Verified workflow produces videos
- Academic sourcing approach is the competitive advantage
- Style is now consistent (STYLE-GUIDE.md authoritative)
- Commands are discoverable (/help, /status)
- Technique tracking enables learning loop

**Known tech debt:**
- Library folder (728 files) needs manual cleanup
- Some deprecated commands still in _DEPRECATED/ folder

**Existing codebase map:** `.planning/codebase/` (7 documents, 1600+ lines)

## Constraints

- **Solo creator**: Everything must be manageable by one person
- **Teleprompter workflow**: Need single final script file to read from
- **Source verifiability**: Every claim must trace to a citable source
- **Spoken delivery**: Scripts must sound natural when read aloud

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Git for script versioning | Tracks style evolution without file sprawl | ✓ Good (v1.0) |
| Two-tier research (per-video + database) | Organized for fact-checking + reusable facts | ✓ Good (v1.0) |
| History in general (not just geopolitics) | Broader niche, more topic flexibility | ✓ Good |
| STYLE-GUIDE.md as authoritative | Single source of truth for style | ✓ Good (v1.0) |
| 10 phase-organized commands | Fewer to remember, flags for variants | ✓ Good (v1.0) |
| Gap scoring formula (max 16) | Demand + Competition + Fit + Hook | ✓ Good (v1.0) |
| Two-tier creator system | Style models (500K+) vs breakout (1K-50K) | ✓ Good (v1.0) |

---

*Last updated: 2026-01-23 after v1.1 milestone start*
