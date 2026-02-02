# History vs Hype Workspace

## What This Is

A content production workspace for History vs Hype, a YouTube channel focused on evidence-based history and myth-busting. The channel uses academic sources and primary documents to debunk historical myths that shape modern beliefs and conflicts. The core differentiator is showing sources on screen — viewers see the evidence, not just hear citations.

## Core Value

Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation. This is what separates the channel from competitors who just narrate over stock footage.

## Current State: v1.3 Shipped

**Shipped:** 2026-02-02

The workspace now includes a complete niche discovery pipeline:

- **Demand Analysis:** Position scoring from autocomplete, trend detection, 7-day caching
- **Competition Analysis:** Format classification (animation/documentary), angle detection (5 categories), quality tiers
- **Production Constraints:** Animation requirement detection, document-friendliness scoring (0-4)
- **Opportunity Scoring:** SAW formula (demand × gap × fit), Channel DNA filtering, clickbait/news-first detection
- **Discovery Command:** `/discover TOPIC` runs full pipeline with Jinja2 reports

**Entry points:**
- `/discover TOPIC` — full niche discovery pipeline
- `/status` — project state and next action
- `/help` — phase-organized command list

## Next Milestone Goals

*To be defined via `/gsd:new-milestone`*

**Production constraints (inputs to filtering):**
- Visual style: Documents, maps, footage, text overlays (no animation)
- Research depth: Academic sources required
- Solo creator: Variable timeline based on topic complexity

## Previous State (v1.2 Shipped)

**Shipped:** 2026-01-30

The workspace includes script quality tools and discovery optimization:

- **Script Quality:** 4 automated checkers (repetition, flow, stumble, scaffolding) + voice fingerprinting
- **Discovery:** Keyword research, intent classification, pre-publish metadata validation
- **Token Optimization:** Model assignments for cost-effective AI usage
- **NotebookLM:** 17 prompt templates, session logging, citation extraction
- **Commands:** 13 commands total

**Entry points:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/analyze VIDEO_ID` — post-publish video analysis
- `/discover TOPIC` — keyword research and metadata validation
- `python tools/script-checkers/cli.py script.md --all` — script quality check

## Requirements

### Validated (v1.3)

- Demand research with position scoring and trend detection — v1.3
- Competition analysis with format/angle classification — v1.3
- Production constraint filtering (animation vs document-friendly) — v1.3
- Opportunity scoring with SAW formula — v1.3
- Channel DNA filtering (clickbait/news-first detection) — v1.3
- `/discover` command for full niche discovery pipeline — v1.3

### Validated (v1.2)

- Repetition detection for scripts — v1.2
- Flow analysis (undefined terms, transitions) — v1.2
- Stumble test (sentence complexity) — v1.2
- Scaffolding counter (filler language) — v1.2
- Voice fingerprinting (learn patterns from transcripts) — v1.2
- Keyword extraction from YouTube autocomplete — v1.2
- Search intent classification (6 categories) — v1.2
- Discovery diagnostics (impressions vs CTR analysis) — v1.2
- Pre-publish metadata validation — v1.2
- Model assignments for skills/agents — v1.2
- NotebookLM prompt templates (17 use cases) — v1.2
- NotebookLM session logging format — v1.2
- Citation extraction from NotebookLM output — v1.2

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
- Retention heatmap prediction — requires 30+ videos with data
- NotebookLM API automation — waiting for Enterprise API

## Context

**What works:**
- Verified workflow produces videos
- Academic sourcing approach is the competitive advantage
- Style is now consistent (STYLE-GUIDE.md authoritative)
- Commands are discoverable (/help, /status)
- Analytics integration provides learning feedback
- Pattern recognition surfaces what's working
- Script quality checkers catch issues before filming
- Voice fingerprinting learns personal delivery patterns

**Known tech debt:**
- Library folder (728 files) needs manual cleanup
- Python 3.14 + spaCy compatibility (use Python 3.11-3.13 for now)
- datetime.utcnow() deprecation warning in intent_mapper.py
- Voice patterns empty until user runs --rebuild-voice
- Discovery diagnostics standalone (not auto-integrated into /analyze)

**Tech stack:**
- ~5,000 lines Python (tools/youtube-analytics/)
- ~2,600 lines Python (tools/script-checkers/)
- ~1,300 lines Python (tools/discovery/)
- YouTube Analytics API v2 + YouTube Data API v3
- OAuth2 authentication with token refresh
- SQLite database for keywords

**Existing codebase map:** `.planning/codebase/` (7 documents, 1600+ lines)

## Constraints

- **Solo creator**: Everything must be manageable by one person
- **Teleprompter workflow**: Need single final script file to read from
- **Source verifiability**: Every claim must trace to a citable source
- **Spoken delivery**: Scripts must sound natural when read aloud

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Git for script versioning | Tracks style evolution without file sprawl | Good (v1.0) |
| Two-tier research (per-video + database) | Organized for fact-checking + reusable facts | Good (v1.0) |
| History in general (not just geopolitics) | Broader niche, more topic flexibility | Good |
| STYLE-GUIDE.md as authoritative | Single source of truth for style | Good (v1.0) |
| 10 phase-organized commands | Fewer to remember, flags for variants | Good (v1.0) |
| Gap scoring formula (max 16) | Demand + Competition + Fit + Hook | Good (v1.0) |
| Two-tier creator system | Style models (500K+) vs breakout (1K-50K) | Good (v1.0) |
| Desktop app OAuth type | Simpler flow for CLI tools | Good (v1.1) |
| Error dict pattern | Return {error: msg} instead of exceptions | Good (v1.1) |
| CTR fallback strategy | Graceful response when API unavailable | Good (v1.1) |
| Insights-first reports | Actionable insights before data tables | Good (v1.1) |
| Proportional thresholds | 0.002 per word scales with script length | Good (v1.2) |
| Word-level diff | Avoids O(n^2) character-level performance | Good (v1.2) |
| 6-category intent classification | Tailored to history niche | Good (v1.2) |
| Haiku/Sonnet/Opus model tiering | Cost optimization without quality loss | Good (v1.2) |

---

*Last updated: 2026-02-02 after v1.3 shipped*
