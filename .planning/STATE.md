# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-07 (Phase 28.1 Plan 01 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-06)

**Core value:** Every video shows sources on screen
**Current focus:** v1.6 Click & Keep — Phase 28.1: Multi-Model Token Optimization (in progress)

## Current Position

**Milestone:** v1.6 Click & Keep
**Phase:** Phase 28.1: Multi-Model Token Optimization (1/2 plans complete)
**Plan:** 28.1-01 complete, 28.1-02 next
**Status:** Token audit complete, ready for routing validation
**Last activity:** 2026-02-07 — Completed 28.1-01 (token audit + routing classification)

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [███████             ]  33% — Click & Keep (6 phases: 27-32)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |
| v1.3 | Niche Discovery | 15-18 | 2026-02-02 |
| v1.4 | Learning Loop | 19-21 | 2026-02-02 |
| v1.5 | Production Acceleration | 22-26 | 2026-02-05 |
| v1.6 | Click & Keep | 27-32 | In progress |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/next` — get ranked topic recommendations based on winning patterns

**Analytics commands (v1.1):**
- `/analyze VIDEO_ID` — post-publish video analysis
- `/patterns` — cross-video pattern recognition

**Discovery commands (v1.2 + v1.3):**
- `/discover TOPIC` — keyword research workflow
- `/discover --demand "keyword"` — demand analysis with opportunity scoring
- `/discover --opportunity "topic"` — complete opportunity analysis (demand + competition + production)
- `/discover --check FILE` — pre-publish metadata validation
- `python tools/discovery/orchestrator.py "keyword"` — complete niche discovery with Markdown reports
- `python tools/discovery/competition.py "keyword"` — competition analysis with differentiation

**Performance analysis (v1.4):**
- `python tools/youtube-analytics/performance.py --fetch-all` — fetch performance data for all videos
- `python tools/youtube-analytics/performance.py --patterns` — extract winning patterns
- `python tools/youtube-analytics/performance.py --strengths` — show channel strength scores
- `python tools/discovery/recommender.py` — get topic recommendations

**Script quality tools (v1.2):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --pacing` — pacing analysis (sentence variance, readability, entity density)
- `python tools/script-checkers/cli.py script.md --pacing --verbose` — full section-by-section pacing breakdown
- `python tools/script-checkers/cli.py script.md --voice` — apply voice patterns

**Production tools (v1.5):**
- `python tools/production/parser.py script.md` — parse script, show sections and entities
- `python tools/production/parser.py script.md --broll` — generate B-roll checklist from script
- `python tools/production/parser.py script.md --edit-guide` — generate EDITING-GUIDE.md with timing
- `python tools/production/parser.py script.md --metadata` — generate METADATA-DRAFT.md with titles/tags
- `python tools/production/parser.py script.md --teleprompter` — export clean text for filming (no markdown)
- `python tools/production/parser.py script.md --package` — generate all outputs in one command

## Session Continuity

### Last Session

- **Date:** 2026-02-07
- **Work:** Completed Phase 28.1-01 (Token Audit + Routing Classification)
- **Output:** TOKEN-AUDIT.md (Opus = 84.9% of costs), ROUTING-CLASSIFICATION.md (10 routable tasks)

### Next Session

**Current work:** v1.6 Click & Keep — Phase 28.1: Multi-Model Token Optimization
**Next action:** Execute 28.1-02 (Routing validation: test free models on 10 routable tasks)

## Accumulated Context

### v1.6 Architecture (Phase 27-32)

**Phase 27 Decisions (Database Foundation - COMPLETE):**
- Extends existing keywords.db with auto-migration pattern (zero breaking changes)
- Schema version tracking via PRAGMA user_version (version 27 set)
- Automatic database backup before migration (timestamped backups/ directory)
- thumbnail_variants table: stores file paths, visual pattern tags, perceptual hashes
- title_variants table: stores title text, character count, formula tags
- ctr_snapshots table: stores monthly CTR data with variant foreign keys
- section_feedback table: stores section-level retention notes
- Feedback columns in video_performance: retention_drop_point, discovery_issues, lessons_learned (JSON)
- Migration guard prevents duplicate migrations (idempotent)
- Backup logic inline to avoid recursive connection reopening

**Phase 28 Decisions (Pacing Analysis):**

Plan 01 (Engine - COMPLETE):
- TDD workflow: RED commit (tests) then GREEN commit (implementation) following proper TDD protocol
- PacingChecker implements BaseChecker interface with check(text) -> dict
- Lazy-loaded dependencies: spaCy for NLP, textstat for Flesch Reading Ease
- B-roll marker stripping before all NLP analysis (reuses ScriptParser.MARKER_PATTERNS)
- Composite scoring: Start at 100, deduct capped penalties (variance 30pts, delta 35pts, density 35pts)
- Sparkline visualization: Inverts scores to complexity (low score = high complexity = tall bar)
- Flat zone detection: 3+ consecutive sections within 10 points = energy plateau
- Hook detection: Advisory-only (time keywords + B-roll markers), not included in composite score
- Single-section scripts return SKIPPED verdict gracefully
- Config thresholds accessed via getattr() with defaults for standalone testing
- Module-level functions (generate_sparkline, detect_flat_zones) for independent testing
- Verdict thresholds: PASS >= 75, NEEDS WORK 50-74, FAIL < 50, SKIPPED = 1 section
- Python 3.14 limitation: spaCy 3.8 depends on Pydantic v1 (incompatible), works on Python 3.11-3.13

Plan 02 (CLI Integration - COMPLETE):
- Problems-only default: --pacing shows only flagged sections unless --verbose passed
- Standalone vs. appended: pacing-only run uses pacing format exclusively, mixed runs append pacing report
- Exit code mapping: pacing verdict (PASS/NEEDS WORK/FAIL) maps to standard exit codes (0/1/2)
- Verdict-first layout: verdict and energy arc displayed before section details for immediate go/no-go
- Advisories separate from scores: hook and B-roll advisories shown as separate section, not scored
- Config thresholds: 7 fields in Config dataclass (variance, delta, density, pass/fail, flat zone window/tolerance)
- Checker-specific output: specialized formatters for checkers with unique report structures

**Phase 29 Design (Thumbnail & Title Tracking):**
- Manual CTR entry UI (API doesn't provide CTR)
- ImageHash perceptual hashing for pattern analysis
- Test window snapshots: 48h, 7d, 14d per variant
- Integrates with existing /analyze command

**Phase 30 Strategy (CTR Analysis):**
- Statistical significance calculator prevents false positives
- Minimum impression thresholds (1,000+) before declaring winner
- Channel-specific CTR benchmarks by topic category (territorial, ideological, legal)
- Confidence intervals and sample size recommendations

**Phase 31 Integration (Feedback Loop):**
- Parses existing POST-PUBLISH-ANALYSIS markdown files
- Extracts structured data (CTR, retention drops, SEO issues) to database
- /script command queries feedback automatically during generation
- Success/failure pattern extraction from top/bottom performers

**Phase 32 Refresh (Model Assignment):**
- Update 13 slash command files from Claude 3.5 names to 4.x IDs
- Model IDs: claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-6
- YAML frontmatter updates in .claude/commands/*.md files
- Agent model assignments update in .claude/agents/

### Roadmap Evolution

- Phase 28.1 inserted after Phase 28: Multi-Model Token Optimization (IN PROGRESS)
  - Plan 01 COMPLETE: Token audit + routing classification
  - Plan 02 NEXT: Routing validation and implementation

**Phase 28.1-01 Decisions (Token Optimization - COMPLETE):**
- Routing strategy: Native /model command for manual routing (68 invocations/month too low for automation)
- OpenRouter free tier sufficient: 2 req/day usage vs 50/day limit (25x headroom)
- Local models rejected: 14.9GB RAM insufficient for Qwen 32B (20-24GB) or Llama 70B (40GB)
- Hardware: AMD Radeon integrated GPU (not NVIDIA), blocks local model routing
- Opus dominance: 84.9% of costs ($473.51/month) from /script and script-writer-v2
- Pareto analysis: Top 3 commands (script, script-writer-v2, research) = 65% of tokens
- 10 of 19 tasks routable: All Haiku-tier mechanical tasks (status, help, fix, sources, prep, discover + 3 agents)
- 9 tasks stay Claude-Only: Opus quality-critical + Sonnet reasoning tasks
- Estimated savings: $12-21/month (2-4% of costs, main benefit is friction removal not cost)
- Free model targets: google/gemini-2.0-flash-exp:free (primary), meta-llama/llama-3.3-70b-instruct:free (secondary)
- Validation approach: 3-week rollout (high-frequency simple → mechanical → agents)

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema extended in Phase 15-01 with 5 demand tables
- External packages (trendspyg, scrapetube) optional - graceful degradation

### Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus

**External Package Dependencies (Plan 15-02):**
- trendspyg, scrapetube not installed — demand analysis degrades gracefully
- Unicode arrows may cause encoding issues on Windows cp1252 console

### v1.4 Architecture Decisions

**Phase 19-01 Decisions:**
- **Conversion formula:** (subscribers_gained / views) * 100, returns percentage
- **Topic classification:** Reuse TAG_VOCABULARY pattern from patterns.py for consistency
- **Angle classification:** Reuse classify_angles from Phase 16 (code reuse)
- **JSON angle storage:** Store angles as JSON TEXT (SQLite lacks native array type)
- **Auto-migration:** _ensure_performance_table() creates table on first access

**Phase 20-01 Decisions:**
- **Strength normalization formula:** min(100, (category_avg / overall_avg) * 50)
- **Dominant extraction:** Counter.most_common() for finding dominant topics/angles
- **Insight generation:** Compare best vs average, best vs worst for actionable insights
- **ASCII progress bars:** # for filled, - for empty (Windows cp1252 safe)

**Phase 21-01 Decisions:**
- **Topic matching:** Word-level comparison, not substring (prevent false positives)
- **Multiplier cap:** Maximum 1.5x boost (prevent overwhelming opportunity score)
- **Exclusion sources:** Scan _IN_PRODUCTION/ and _ARCHIVED/ folders
- **Graceful degradation:** Proceed with multiplier=1.0 if pattern extraction fails

### Technical Notes (v1.4)

- video_performance table with indexes on conversion_rate, topic_type, fetched_at
- performance.py integrates metrics.py + channel_averages.py for conversion tracking
- pattern_extractor.py provides winning patterns for recommendation scoring
- recommender.py scans video-projects/ folders and excludes existing topics
- `/next` command documentation at `.claude/commands/next.md`

### v1.5 Architecture Decisions

**Phase 22-01 Decisions:**
- **Module location:** tools/production/ for all production acceleration tools
- **Entity extraction approach:** Hybrid regex + optional spaCy (use_spacy=True)
- **Section type inference:** Position-based (first=intro, last=conclusion) with keyword override
- **Word count calculation:** Strip all B-roll markers before counting spoken words
- **Entity deduplication:** Normalize (lowercase, strip "the ", collapse whitespace), merge by key
- **Person blocklist:** Filter marker-derived false positives (talking head, text on screen, etc.)

**Phase 22-01 Patterns Established:**
- Lazy spaCy loading with graceful fallback to regex-only
- Domain-specific keyword dictionaries for classification
- Marker stripping before both word count and entity extraction

**Phase 23-01 Decisions:**
- **Source URLs:** Use search URLs instead of fabricated file paths (safe, always valid)
- **Archive hierarchy:** Organized by topic category (holocaust, legal, medieval, colonial, general)
- **Priority thresholds:** 3+ mentions for documents, 5+ mentions for maps/portraits → Priority 1
- **DIY instructions:** MapChart.net for maps (free, zero-budget friendly)
- **Visual type classification:** Keyword detection (maritime → strategic_map, territory → map)

**Phase 23-01 Patterns Established:**
- Shot dataclass pattern: entity + visual_type + priority + source_urls + diy_instructions + section_references
- Topic detection: Aggregate entity text, check keyword matches, return category
- Priority assignment: Type-specific thresholds based on mention counts
- Markdown output: Group by visual type, include DIY instructions, priority checklist at end

**Phase 24-01 Decisions:**
- **150 WPM timing standard:** Industry standard speaking rate for video narration
- **10-second minimum:** Prevents unrealistic sub-10-second estimates for brief transitions
- **MM:SS formatting:** Matches video editing software conventions
- **UTF-8 encoding on Windows:** Platform-specific stdout setup to handle unicode characters
- **Section-to-shot mapping:** Uses BRollGenerator section_references field for logical grouping

**Phase 24-01 Patterns Established:**
- SectionTiming dataclass tracks cumulative start/end times for each section
- Shot-by-shot breakdown groups shots by section for logical flow
- Visual assets checklist auto-generated from shot priorities
- Edit guide format matches existing EDITING-GUIDE.md structure
- calculate_duration_seconds(word_count) → estimated seconds at 150 WPM
- format_time(seconds) → MM:SS string

**Phase 25-01 Decisions:**
- **3 title variants:** Mechanism (A), document (B), paradox (C) for A/B/C testing
- **Documentary tone filter:** Automated rejection of clickbait patterns from VIDIQ-CHANNEL-DNA-FILTER.md
- **60-70 char title length:** Mobile-first optimization with word-boundary truncation
- **Tag filtering:** Reject entities >50 chars, parentheses, brackets (sentence fragments)
- **Allowed acronyms:** ICJ, UN, CIA, etc. can be all-caps without triggering clickbait filter

**Phase 25-01 Patterns Established:**
- TitleVariant dataclass: variant letter + title + focus description + length
- Clickbait pattern matching with allowed acronym exceptions
- Title generation from opening hook (first 2-3 sentences)
- Description template: hook + KEY DOCUMENTS + SOURCES + hashtags
- Tag generation: entity names (primary) + section keywords (secondary)
- Chapter generation from SectionTiming cumulative times

**Phase 26-01 Decisions:**
- **Single parse pass:** Sections/entities computed once before mode handlers, reused by all generators
- **Package mode writes files:** Files written to project folder (not stdout) for convenience
- **Teleprompter preserves pacing:** Paragraph breaks maintained (3+ newlines → 2 newlines)
- **Comprehensive marker stripping:** All bracketed markers, markdown formatting, code blocks removed

**Phase 26-01 Patterns Established:**
- strip_for_teleprompter(): Module-level utility for clean text export
- Package summary format: File list, runtime estimate, next steps
- Single entry point for all production outputs (`--package` flag)

---

*State updated: 2026-02-06 after Phase 28 completion*
