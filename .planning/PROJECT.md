# History vs Hype Workspace

## What This Is

A content production workspace for History vs Hype, a YouTube channel focused on evidence-based history and myth-busting. The channel uses academic sources and primary documents to debunk historical myths that shape modern beliefs and conflicts. The core differentiator is showing sources on screen — viewers see the evidence, not just hear citations.

## Core Value

Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation. This is what separates the channel from competitors who just narrate over stock footage.

## Current State

**Shipped:** v7.0 Packaging & Hooks Overhaul (2026-03-18)
**Previous milestones:** v1.0-v6.0 (shipped 2026-01-19 to 2026-03-16)
**Archives:** `.planning/milestones/`

v7.0 researched what actually drives clicks/impressions on edu/history YouTube (388 videos across 8 channels), then rewrote tooling to match proven niche patterns. Title scorer now anchored to niche benchmarks, hook generator recommends by topic type (territorial→cold_fact, ideological→myth_contradiction), metadata enforces description templates + thumbnail concepts + coherence checks. 5 phases, 9 plans, 75 commits, 191 new tests, 348 total green.

## Requirements

### Validated (v4.0)

- Document discovery with translation gap verification (academic DBs, sourcebooks, archives) — v4.0
- Document structure assessment (article/clause count, video length estimation) — v4.0
- Archive lookup for digitized originals (Légifrance, Wikisource, Internet Archive) — v4.0
- Untranslated Evidence format reference guide (series standards) — v4.0
- AI translation via Claude with clause-by-clause accuracy and full-document context — v4.0
- Cross-check against DeepL/free fallback with discrepancy detection — v4.0
- Legal/technical term annotation with dictionary definitions — v4.0
- Surprise clause detection (narrative contradiction analysis, three-tier severity) — v4.0
- Split-screen formatted output (paired original/translation) — v4.0
- Translation verification with audit/fresh modes and GREEN/YELLOW/RED verdicts — v4.0
- Key term verification against legal/historical dictionaries — v4.0
- Scholarly comparison for translation accuracy — v4.0
- Document-structured script generation (clause-by-clause backbone, Rule 18) — v4.0
- 5-element clause pattern (context → read → translate → explain → connect) — v4.0
- Split-screen edit guide with per-clause timing and transition markers — v4.0
- Asset sourcing from Phase 39 archive lookup integration — v4.0

### Validated (v3.0)

- Retention playbook synthesized from channel data as STYLE-GUIDE.md Part 9 — v3.0
- Script sections scored for predicted retention (evidence, relevance, length) — v3.0
- Retention drop patterns encoded as warnings during /script generation — v3.0
- Transcript analysis pipeline parses 80+ transcripts for structural patterns — v3.0
- Cross-creator synthesis identifies universal patterns across 3+ creators as Part 8 — v3.0
- Creator technique library stored in DB, searchable by type — v3.0
- Script-writer-v2 reads Part 8 techniques via Rule 17 during generation — v3.0
- 2-3 opening hook variants generated with --variants flag — v3.0
- 2 structural approaches proposed per video — v3.0
- Hook and structure choices logged to database with project context — v3.0
- After 5+ choices, system recommends preferred option based on patterns — v3.0
- /script supports --variants flag for variant generation — v3.0
- Database migrated to schema v29 with script_choices table — v3.0
- Agent prompt consolidated to 788 lines (43.6% reduction) — v3.0

### Validated (v2.0)

- Voice pattern extraction from top-performing transcripts (29 patterns) — v2.0
- STYLE-GUIDE.md Part 6 Voice Pattern Library with formulas, examples, templates — v2.0
- Script-writer-v2 applies Part 6 voice patterns via Rule 14 — v2.0
- Script validation for forbidden phrases, missing definitions, DNA violations — v2.0
- Academic source list generation with ISBNs and purchase links — v2.0
- NotebookLM citation extraction to VERIFIED-RESEARCH.md format — v2.0
- Structured NotebookLM prompts for fact extraction — v2.0
- Retention drops mapped to script sections with root cause analysis — v2.0
- Concrete fix recommendations referencing specific sections and Part 6 patterns — v2.0
- Topic strategy analysis with confidence flags and concrete next steps — v2.0
- Pre-script intelligence surfaces automatically before /script generation — v2.0

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

### Validated (v6.0)

- `/retitle` pipeline: audit underperformers, generate candidates, SWAP-CHECKLIST, 7-day CTR measurement — v6.0
- Data-driven title scoring: live CTR from keywords.db via TitleCTRStore, greenlight/preflight DB-enriched — v6.0
- CTR ingestion from CROSS-VIDEO-SYNTHESIS.md into keywords.db — v6.0
- Proactive topic discovery: autocomplete mining, competitor gaps, Google Trends pulse, `/discover --scan` — v6.0
- MCP server evaluation: Context7 + Playwright adopted, 9 tools skipped with evidence — v6.0
- Automated CTR feedback loop: ctr_tracker.py + YouTube Analytics API + Windows Task Scheduler — v6.0

### Validated (v5.1)

- Unified error handling across all tool modules — v5.1
- Structured logging replacing print() statements — v5.1
- Integration test suite with pytest — v5.1
- Clean package structure with __init__.py — v5.1
- Pinned dependency management (pyproject.toml) — v5.1
- DB schema versioning for all databases — v5.1
- Standardized CLI interfaces — v5.1
- Dead code and artifact cleanup — v5.1
- External intelligence synthesis (/publish --prompts, --intake, synthesis engine) — v5.1

### Validated (v5.0)

- Translation pipeline hardened with .env + refactored to Claude Code native LLM (no API key) — v5.0
- NLM paste-to-verified-research flow with approve/reject per claim — v5.0
- YouTube Intelligence Engine: algorithm KB, niche patterns, competitor tracking, automated refresh — v5.0
- Intelligence auto-surfaces during /script, /prep, /publish with workflow-specific advisories — v5.0
- Rule 19 algorithm-aware hooks (4-beat formula with retention triggers) — v5.0
- Analytics backfill from existing POST-PUBLISH-ANALYSIS files and YouTube API — v5.0
- Channel-specific insights surface automatically during production commands — v5.0
- Multi-project dashboard in /status with priority ranking and trending topic flags — v5.0

### Validated (v7.0)

- Title scorer anchors passing to 4%+ CTR based on edu/history competitor norms — v7.0
- Scorer flags <5 examples, falls back to competitor benchmarks — v7.0
- Different CTR targets by topic type (territorial 3%+, political 5%+) — v7.0
- `/publish --titles` extracts specific material from script for title candidates — v7.0
- Versus + declarative variants generated by default — v7.0
- Penalty patterns scored heavily, shown last with warnings — v7.0
- Hook scorer verifies title-fulfillment match — v7.0
- Hook style recommended by topic type (cold_fact, myth_contradiction, specificity_bomb) — v7.0
- `/publish` enforces description template with SEO + citations — v7.0
- Thumbnail concept generator outputs 3 script-grounded concepts — v7.0
- Coherence check: title + thumbnail + description alignment — v7.0

### Active

(Next milestone not yet started — run `/gsd:new-milestone`)

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
- Style is now consistent (STYLE-GUIDE.md authoritative, Part 6 voice patterns)
- Commands are discoverable (/help, /status)
- Full production pipeline exists (research → script → production → publish → analyze)
- Database infrastructure for performance, variants, CTR, feedback
- Script generation matches creator voice (29 Part 6 patterns via Rule 14)
- NotebookLM research bridge generates source lists and extracts citations
- Analytics map retention drops to script sections with concrete fix recommendations
- Pre-script intelligence surfaces automatically before /script generation
- Retention playbook (Part 9) + scorer predict section-level risk before filming
- Creator technique library (Part 8) from 83 transcripts feeds script generation
- Variant generation offers hook/structure choices that learn from user patterns
- Agent prompt consolidated to 788 lines (43.6% reduction, all functionality preserved)
- Translation pipeline: gap check → archive lookup → translate → cross-check → annotate → format
- Translation verification with scholarly comparison before filming
- Document-structured scriptwriting (Rule 18) for clause-by-clause videos
- Split-screen edit guides with per-clause timing and asset sourcing
- YouTube Intelligence Engine with automated refresh from 5+ authoritative sources
- Channel insights and YouTube intelligence auto-surface during all production commands
- Rule 19 algorithm-aware hooks with 4-beat formula informed by intelligence data
- NLM paste-to-research flow (paste → parse → review → approve → write to VERIFIED-RESEARCH)
- Multi-project dashboard in /status ranks 38+ projects by priority with stale/trending flags
- Niche benchmark store (388 videos, 8 channels) anchors title scorer to edu/history norms
- Topic-type hook recommendations: territorial→cold_fact, ideological→myth_contradiction, untranslated→specificity_bomb
- Title generation extracts specific material from scripts (numbers, documents, contradictions)
- Metadata coherence check verifies title + thumbnail + description alignment
- Description template enforced with SEO first line + citation block
- Thumbnail concept generator outputs 3 script-grounded concepts with coherence badges

**Known tech debt:**
- Library folder (728 files) needs manual cleanup
- Python 3.14 + spaCy compatibility (use Python 3.11-3.13 for now)
- Voice patterns empty until user runs --rebuild-voice
- token.json absent — YouTube API enrichment falls back to RSS-only
- classify_topic() may over-classify non-history topics as "colonial" (upstream)
- Nyquist validation incomplete for phases 61, 62

**Tech stack:**
- ~48K+ lines Python total across tools/
- YouTube Analytics API v2 + YouTube Data API v3
- Anthropic SDK for notebooklm_bridge.py (Claude Sonnet 4 for source generation)
- OAuth2 authentication with token refresh
- SQLite databases: keywords.db (schema v29), intel.db (schema v2)
- MCP servers: Context7 (library docs), Playwright (browser automation)
- Windows Task Scheduler: weekly CTR refresh via ctr_tracker.py

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
| Reference doc expansion over code proliferation | Voice patterns as STYLE-GUIDE Part 6, not new Python modules | Good (v2.0) |
| Claude API for source generation | Claude has academic knowledge without needing external APIs | Good (v2.0) |
| Regex-based citation extraction (not LLM) | NotebookLM output is predictable; regex is fast, free, deterministic | Good (v2.0) |
| Static prompt library as reference doc | Prompts are stable templates, always available without dynamic generation | Good (v2.0) |
| Hardcoded voice patterns in diagnostics | 29 patterns are stable; avoids runtime markdown parsing complexity | Good (v2.0) |
| 150 WPM fixed rate for retention mapping | Good enough for diagnostic section boundaries | Good (v2.0) |
| Confidence flags on topic strategy | Small dataset (~15 videos) requires explicit confidence signaling | Good (v2.0) |
| DIAGNOSTICS_AVAILABLE feature flag | Graceful degradation if retention mapper not available | Good (v2.0) |
| 3-video threshold for topic baselines | Falls back to channel avg if insufficient topic data | Good (v3.0) |
| Word boundaries for relevance markers | Prevents false positives in modern relevance detection | Good (v3.0) |
| Exponential decay for choice weighting (0.9) | Tracks preference shifts better than linear weighting | Good (v3.0) |
| Three-tier recommendation fallback | Topic-specific (3+) → global (5+) → Part 8 creator_count | Good (v3.0) |
| Sequential choice flow (hooks then structure) | Reduces cognitive load vs simultaneous 6-option presentation | Good (v3.0) |
| Merge rules by function not keywords | Preserves nuance when consolidating overlapping agent rules | Good (v3.0) |
| STYLE-GUIDE cross-references over inline duplication | Keeps agent prompt lean while referencing authoritative source | Good (v3.0) |
| Clause-by-clause translation (one API call per article) | Accuracy over token cost; full document context per call | Good (v4.0) |
| Auto-detection with --dry-run confirmation | Prevents accidental API spend; user confirms before translating | Good (v4.0) |
| Lower temperature (0.3) for translation | Consistency over creativity for legal/historical text | Good (v4.0) |
| Language-agnostic design from start | Works for French, Spanish, Latin, German without refactoring | Good (v4.0) |
| Hybrid transition markers (explicit + ratio) | Tactical timestamps + strategic section guidance for editors | Good (v4.0) |
| Surprise emphasis only for Major/Notable | Avoids noise — minor surprises left to editor judgment | Good (v4.0) |
| Three-tier severity for surprises (Major/Notable/Minor) | Graduated emphasis prevents every clause feeling "surprising" | Good (v4.0) |
| Claude Code native LLM for translation | Eliminates API key requirement for Pro plan users | Good (v5.0) |
| Hybrid NLM parsing (structured + freeform fallback) | Handles both NLM output modes without config | Good (v5.0) |
| feedparser as only new dependency for intel | No BeautifulSoup — LLM synthesis handles messy text | Good (v5.0) |
| Graceful RSS-only fallback for competitors | Works without YouTube API auth; enrichment non-fatal | Good (v5.0) |
| 10-phase refresh orchestrator for intel | Errors collected, pipeline continues on individual failure | Good (v5.0) |
| time.time() - st_mtime for dashboard activity | Avoids timezone-aware/naive mixing on Windows | Good (v5.0) |
| Rule 19 supersedes Rule 9 Section A for hooks | 4-beat formula is superset of old hook selection | Good (v5.0) |
| pyproject.toml as single dependency source | Deleted 3 per-package requirements.txt files | Good (v5.1) |
| Lazy imports to break circular dependencies | discovery/diagnostics.py, recommender.py, title_ctr_store.py | Good (v5.1) |
| logging.getLogger("tools") not root logger | Library-safe hierarchy; NullHandler prevents warnings | Good (v5.1) |
| PRAGMA user_version for all DBs | intel.db v2, keywords.db v29 — atomic migrations | Good (v5.1) |
| Retention weighting for retitle priority | priority = wasted_impressions × (1 + retention_bonus) | Good (v6.0) |
| SWAP-CHECKLIST ephemeral, SWAP LOG permanent | Regenerated each run vs persistent in POST-PUBLISH-ANALYSIS | Good (v6.0) |
| score = min(100, max(0, int(ctr_percent * 17))) | Maps 3.8% CTR to 64, near static declarative baseline of 65 | Good (v6.0) |
| 15 autocomplete seeds for scan balance | <90s runtime vs 3+ min for 20-30 seeds | Good (v6.0) |
| Context7 + Playwright MCP adoption | Free, unlimited, local — skipped 9 broken/cloud-only tools | Good (v6.0) |
| Weekly Task Scheduler for CTR refresh | Automated without user intervention; logs to logs/ | Good (v6.0) |
| Niche benchmark advisory, not hard gate | Own-channel score primary, niche percentile additive | Good (v7.0) |
| authority_challenge removed from all paths | 0/42 hooks in 8-channel niche — pattern doesn't exist here | Good (v7.0) |
| versus reframed as "differentiation bet" | 1/388 niche videos (0.26%) — rare, unproven, not default | Good (v7.0) |
| Declarative as default title choice | n=139 niche, 3.8% own CTR, most reliable pattern | Good (v7.0) |
| Topic-to-hook mapping | territorial→cold_fact, ideological→myth_contradiction, untranslated→specificity_bomb | Good (v7.0) |
| Hook scoring after agent generation | Avoids circular feedback loop; agent writes, scorer evaluates | Good (v7.0) |
| CLICKBAIT_PATTERNS consolidated to title_scorer.py | Single source imported by metadata.py; eliminates duplication | Good (v7.0) |

---

*Last updated: 2026-03-18 after v7.0 milestone archived*
