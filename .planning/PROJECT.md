# History vs Hype Workspace

## What This Is

A content production workspace for History vs Hype, a YouTube channel focused on evidence-based history and myth-busting. The channel uses academic sources and primary documents to debunk historical myths that shape modern beliefs and conflicts. The core differentiator is showing sources on screen — viewers see the evidence, not just hear citations.

## Core Value

Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation. This is what separates the channel from competitors who just narrate over stock footage.

## Current State (v1.1 Shipped)

**Shipped:** 2026-01-26

The workspace now includes a complete analytics and learning loop:

- **Analytics:** YouTube Analytics API integration for automated metrics pulls
- **Analysis:** `/analyze VIDEO_ID` for comprehensive post-publish analysis
- **Patterns:** `/patterns` for cross-video pattern recognition
- **Commands:** 12 commands total (added /analyze, /patterns)

**Entry points:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/analyze VIDEO_ID` — post-publish video analysis
- `/patterns` — cross-video pattern recognition

## Requirements

### Validated (v1.1)

- YouTube Analytics API integration for automated data pulls — v1.1
- Post-publish learning loop (CTR, retention, audience signals) — v1.1
- Cross-video pattern recognition system — v1.1
- Comment fetching and categorization — v1.1

### Validated (v1.0)

- Clean up outdated and duplicate files — v1.0
- Establish one canonical script file per video — v1.0
- Organize per-video research with clear source attribution — v1.0
- Create cross-video verified facts database — v1.0
- Simplify workflow (fewer commands) — v1.0
- Consolidate style notes into single authoritative reference — v1.0
- Scriptwriter produces spoken-delivery scripts — v1.0
- Competitive intelligence tracking — v1.0

### Out of Scope

- Building a new channel or brand — improving existing workspace
- Changing the core format (talking head + B-roll evidence) — optimizing execution
- Multi-person workflow — solo creator optimization
- Video editing automation — out of scope for this workspace
- Predictive analytics — focus on learning, not prediction
- VidIQ API integration — no API available

## Context

**What works:**
- Verified workflow produces videos
- Academic sourcing approach is the competitive advantage
- Style is now consistent (STYLE-GUIDE.md authoritative)
- Commands are discoverable (/help, /status)
- Analytics integration provides learning feedback
- Pattern recognition surfaces what's working

**Known tech debt:**
- Library folder (728 files) needs manual cleanup
- Some deprecated commands still in _DEPRECATED/ folder
- Title pattern "Why ... Has ..." not detected (minor)

**Tech stack:**
- ~5,000 lines Python (tools/youtube-analytics/)
- YouTube Analytics API v2 + YouTube Data API v3
- OAuth2 authentication with token refresh

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
| Desktop app OAuth type | Simpler flow for CLI tools | ✓ Good (v1.1) |
| Error dict pattern | Return {error: msg} instead of exceptions | ✓ Good (v1.1) |
| CTR fallback strategy | Graceful response when API unavailable | ✓ Good (v1.1) |
| Insights-first reports | Actionable insights before data tables | ✓ Good (v1.1) |

---

*Last updated: 2026-01-27 after v1.1 milestone shipped*
