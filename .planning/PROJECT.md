# History vs Hype Workspace

## What This Is

A content production workspace for History vs Hype, a YouTube channel focused on evidence-based history and myth-busting. The channel uses academic sources and primary documents to debunk historical myths that shape modern beliefs and conflicts. The core differentiator is showing sources on screen — viewers see the evidence, not just hear citations.

## Core Value

Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation. This is what separates the channel from competitors who just narrate over stock footage.

## Current State: v1.6 Shipped

**Last milestone:** v1.6 Click & Keep (shipped 2026-02-09)

Systematic CTR and retention improvement system — track what works across thumbnails, titles, and script structure so each video is better than the last.

- **Database Foundation:** Variant tables, CTR snapshots, section feedback columns
- **Script Pacing Analysis:** PacingChecker with sentence variance, readability delta, entity density, sparkline energy arc
- **Thumbnail & Title A/B Tracking:** CLI for registering variants, recording CTR, trend analysis, `/analyze` integration
- **CTR Benchmarks Engine:** Verdict calculator with impression thresholds, channel-specific benchmarks by topic category
- **Feedback Loop Integration:** Auto-parse POST-PUBLISH-ANALYSIS files, store insights, surface in `/script`, `/prep`, `/publish`
- **Model Assignment Refresh:** 14 commands and 6 agents verified on Claude 4.x, documentation updated

**Entry points:**
- `/analyze VIDEO_ID` — full variant tracking + CTR analysis + feedback insights
- `python tools/script-checkers/cli.py script.md --pacing` — pacing analysis before filming
- `python tools/youtube-analytics/variants.py register-thumb VIDEO_ID A path.jpg` — register thumbnail variant
- `python tools/youtube-analytics/feedback.py backfill` — import POST-PUBLISH-ANALYSIS data

## Requirements

### Validated (v1.6)

- Database schema for CTR tracking and feedback storage — v1.6
- Script pacing analysis (sentence variance, readability delta, entity density) — v1.6
- Energy arc visualization showing pacing rhythm across full script — v1.6
- Thumbnail variant registration with file paths and visual pattern tags — v1.6
- Title variant registration with formula tags — v1.6
- CTR snapshot tracking at meaningful intervals per variant — v1.6
- Statistical significance calculation between variants with impression thresholds — v1.6
- Channel-specific CTR benchmarks by topic category — v1.6
- POST-PUBLISH-ANALYSIS parsing and structured database storage — v1.6
- Past performance insight queries for similar topics — v1.6
- Success/failure pattern extraction from high/low performers — v1.6
- Automatic insight surfacing during /script, /prep, /publish generation — v1.6
- Model assignment refresh for Claude 4.x lineup (14 commands, 6 agents) — v1.6

### Validated (v1.5)

- Script parsing with entity extraction (treaties, places, people, documents) — v1.5
- B-roll shot list generation with source URLs — v1.5
- Edit guide with section timing and B-roll cue markers — v1.5
- Metadata draft with 3 title variants, description, tags — v1.5
- Teleprompter export (clean text, no markdown) — v1.5
- Single `--package` command for all production outputs — v1.5

### Validated (v1.4)

- Subscriber conversion tracking per video — v1.4
- Topic type correlation analysis (territorial, legal, ideological) — v1.4
- Angle correlation analysis (document-heavy, academic, legal) — v1.4
- Winning pattern extraction from top performers — v1.4
- Channel strength scores (0-100 by category) — v1.4
- `/next` command for ranked topic recommendations — v1.4
- Folder scanning to exclude existing work — v1.4
- Pattern-weighted scoring (1.0-1.5x multiplier) — v1.4
- Integration with v1.3 opportunity scoring — v1.4

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
- Script quality checkers catch issues before filming (including pacing analysis)
- Voice fingerprinting learns personal delivery patterns
- A/B tracking for thumbnails and titles with CTR trend analysis
- Feedback loop auto-surfaces past insights during content creation
- Model assignments verified for Claude 4.x lineup

**Known tech debt:**
- Library folder (728 files) needs manual cleanup
- Python 3.14 + spaCy compatibility (use Python 3.11-3.13 for now)
- datetime.utcnow() deprecation warning in intent_mapper.py
- Voice patterns empty until user runs --rebuild-voice
- Discovery diagnostics standalone (not auto-integrated into /analyze)

**Tech stack:**
- ~12,300 lines Python (tools/youtube-analytics/) — includes variants.py, benchmarks.py, feedback.py
- ~3,200 lines Python (tools/script-checkers/) — includes pacing_checker.py
- ~1,800 lines Python (tools/discovery/) — includes recommender.py
- YouTube Analytics API v2 + YouTube Data API v3
- OAuth2 authentication with token refresh
- SQLite database for keywords, performance, variants, CTR, and feedback

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
| Conversion formula (subs/views × 100) | Percentage makes comparison intuitive | Good (v1.4) |
| Word-level topic matching | Prevents false positives in exclusion | Good (v1.4) |
| Pattern multiplier cap (1.5x) | Prevents overwhelming opportunity score | Good (v1.4) |
| JSON angle storage | SQLite lacks native array type | Good (v1.4) |
| Auto-migration with PRAGMA user_version | Schema version tracking, zero breaking changes | Good (v1.6) |
| Composite pacing score (100 - penalties) | Intuitive 0-100 scale with capped deductions | Good (v1.6) |
| Sparkline energy arc visualization | Quick pacing rhythm check without verbose output | Good (v1.6) |
| Heuristic CTR verdicts (not statistical tests) | Appropriate for small channel (~10 videos) | Good (v1.6) |
| Feature flags (VARIANTS/BENCHMARKS/FEEDBACK_AVAILABLE) | Graceful degradation when modules unavailable | Good (v1.6) |
| Regex-based markdown parsing for feedback | All-stdlib, no external dependencies | Good (v1.6) |
| Short model aliases (opus/sonnet/haiku) | Auto-map to latest versions, no version churn | Good (v1.6) |

---

*Last updated: 2026-02-09 after v1.6 milestone shipped*
