# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-30 (Phase 13.1 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-27)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.2 Script Quality & Discovery — Phase 14

## Current Position

**Milestone:** v1.2 Script Quality & Discovery
**Phase:** 14 of 14+ (NotebookLM Workflow)
**Plan:** 0 of TBD
**Status:** Not started
**Last activity:** 2026-01-30 — Phase 13.1 complete (Token Optimization)

**Progress:**
```
v1.0 [████████████████████] 100% — Workspace Optimization
v1.1 [████████████████████] 100% — Analytics & Learning Loop
v1.2 [████████████████░░░░]  80% — Script Quality & Discovery (Phase 14/14)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-6 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 7-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | In progress |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project

**Analytics commands (v1.1):**
- `/analyze VIDEO_ID` — post-publish video analysis
- `/patterns` — cross-video pattern recognition

**Discovery commands (v1.2 Phase 13):**
- `/discover TOPIC` — keyword research workflow
- `/discover --check FILE` — pre-publish metadata validation

## Session Continuity

### Last Session

- **Date:** 2026-01-30
- **Work:** Completed Phase 13.1 (Token Optimization) - all 2 plans executed
- **Output:**
  - 13 skill files updated with `model:` field in YAML frontmatter
  - 4 agent files updated with optimized model assignments
  - `.claude/REFERENCE/MODEL-ASSIGNMENT-GUIDE.md` — Complete reference documentation

### Next Session

**Phase 13.1 Complete:** Token optimization via model assignment

- **Skill assignments:** 6 Haiku, 6 Sonnet, 1 Opus (13 total)
- **Agent assignments:** 3 Haiku, 2 Sonnet, 1 Opus (6 total)
- **Reference doc:** Decision framework for future assignments

Next: Begin Phase 14 (NotebookLM Workflow) - research-to-script pipeline.

## Roadmap Evolution

- Phase 13.1 inserted after Phase 13: Token Optimization via Model Assignment (URGENT)
  - Rationale: Reduce token costs by assigning cheaper models to simpler tasks
  - Haiku for: /status, /help, /fix, /sources, /prep, /discover
  - Sonnet for: /verify, /publish, /engage, /analyze, /patterns, /research
  - Opus for: script-writer-v2 agent (complex creative writing)

## Accumulated Context

### Technical Decisions

**Script Quality Checkers (Phase 11-01 + 11-02):**
- **Proportional thresholds:** Base rate 0.002 per word scales naturally (500 words = 1 allowed, 3000 words = 6)
- **Lazy-load spaCy:** Import at first use, not module load time (faster CLI startup)
- **Signature phrase exemption:** "Here's what X actually says" is channel pattern, not filler
- **Sentence-initial detection:** Only flag "so," and "now," at sentence start to reduce false positives
- **BaseChecker pattern:** All checkers implement `check()` returning `{issues: [], stats: {}}`
- **Repetition: 2-4 word phrases:** Catches both common 2-word repetitions and 3-4 word patterns
- **Rhetorical detection:** Requires clustering (all within proximity) + fragments, not just adjacent occurrences
- **Exact match only:** Fuzzy matching with difflib was O(n²), simplified to exact matches for performance
- **Flow 80% accuracy:** High-confidence flagging with user decision, not 100% automatic blocking
- **Checker execution order:** flow -> repetition -> stumble -> scaffolding (definitions first, delivery last)

**Voice Fingerprinting (Phase 12-01 + 12-02):**
- **Word-level diff:** Uses difflib.SequenceMatcher on word arrays, not character-level (avoids O(n²) on long texts)
- **Minimum frequency:** Pattern must occur >= 3 times to distinguish from ad-libs
- **Temporal weighting:** Exponential decay (0.95^months) gives recent videos more influence
- **Confidence levels:** HIGH (freq >= 5), MEDIUM (freq >= 3) based on corpus linguistics standards
- **Manual srt install:** pip install commands hang in automation, documented in VOICE-SETUP.md for user
- **Lazy imports:** Use __getattr__ to avoid srt dependency blocking pattern_applier (only needed for corpus analysis)
- **Case-preserving replacement:** Capitalize replacement if original word was capitalized (sentence-initial)
- **HIGH-confidence only:** Only apply patterns with freq >= 5 (skip MEDIUM to avoid over-applying)
- **Transform-then-check:** Voice patterns applied BEFORE quality checkers analyze script

**Discovery Tools (Phase 13-01 through 13-03):**
- **Error dict pattern:** Return `{'error': msg}` instead of exceptions (consistent with youtube-analytics, script-checkers)
- **Lazy database init:** Auto-create tables on first KeywordDB() instantiation (no separate setup step needed)
- **Pyppeteer over Node.js:** Use Python port to stay in Python ecosystem (easier integration with existing tools)
- **Rate limiting:** 2s base delay + 1-3s random jitter, exponential backoff on errors (1s → 2s → 4s → 8s max)
- **Database location:** tools/discovery/keywords.db (relative to module, persists across sessions)
- **Confidence scoring:** 1 match = 0.33, 2 = 0.66, 3+ = 1.0 (not ratio-based, allows single strong matches)
- **DNA fit weighting:** Positive signals +0.2 each, negative -0.3 each, base 0.5 (penalty > bonus)
- **Impressions threshold:** 50% of channel average = LOW_IMPRESSIONS (channel-specific, not absolute)
- **Graceful degradation:** DISCOVERY_AVAILABLE flag in analyze.py (works without discovery module)
- **Metadata validation:** Keyword density > 2% = HIGH severity stuffing, description < 200 words = WARNING
- **VidIQ guided workflow:** Manual prompts (no API available), project-specific storage in vidiq-data.json
- **Pre-publish gate:** /publish integrates metadata check as required step before upload

### v1.2 Phase Structure

**Phase 11: Script Quality Checkers** (SCRIPT-01 through SCRIPT-04) — ✅ COMPLETE 2026-01-28
- 11-01 COMPLETE: Stumble test (SCRIPT-03), scaffolding counter (SCRIPT-04), CLI foundation
- 11-02 COMPLETE: Repetition detection (SCRIPT-01), flow analysis (SCRIPT-02), full CLI integration
- Verification: PASSED 8/8 must-haves

**Phase 12: Voice Fingerprinting** (SCRIPT-05) — ✅ COMPLETE 2026-01-29
- 12-01 COMPLETE: Corpus builder, pattern extractor, initial pattern library structure
- 12-02 COMPLETE: Pattern applier, CLI integration with --voice flags
- Verification: CLI accepts --voice, --show-voice-changes, --rebuild-voice flags

**Phase 13: Discovery Tools** (DISC-01 through DISC-04) — ✅ COMPLETE 2026-01-29
- 13-01 COMPLETE: Keyword extraction foundation (database + autocomplete + CLI)
- 13-02 COMPLETE: Intent classification + discovery diagnostics (6 categories + /analyze integration)
- 13-03 COMPLETE: Metadata checker + VidIQ workflow + /discover command + /publish integration
- Verification: PASSED 4/4 requirements

**Phase 14: NotebookLM Workflow** (NBLM-01 through NBLM-03)
- Final phase: research-to-script pipeline
- Prompt templates, session logging, citation extraction

### Key Deliverables

**v1.1 (Analytics & Learning Loop):**

| Component | Location | Purpose |
|-----------|----------|---------|
| auth.py | tools/youtube-analytics/ | OAuth2 authentication |
| metrics.py | tools/youtube-analytics/ | Views, watch time, engagement |
| retention.py | tools/youtube-analytics/ | Retention curves, drop-offs |
| ctr.py | tools/youtube-analytics/ | CTR with graceful fallback |
| video_report.py | tools/youtube-analytics/ | Combined report generator |
| comments.py | tools/youtube-analytics/ | Comment fetching & categorization |
| channel_averages.py | tools/youtube-analytics/ | Channel benchmarks |
| analyze.py | tools/youtube-analytics/ | Analysis orchestrator |
| patterns.py | tools/youtube-analytics/ | Pattern recognition |
| /analyze | .claude/commands/ | Post-publish analysis command |
| /patterns | .claude/commands/ | Pattern recognition command |

**v1.2 (Script Quality & Discovery) - Phases 11-13 Complete:**

| Component | Location | Purpose |
|-----------|----------|---------|
| cli.py | tools/script-checkers/ | Script quality checker orchestrator (all 4 checkers + voice) |
| repetition.py | tools/script-checkers/checkers/ | SCRIPT-01: Phrase repetition detection |
| flow.py | tools/script-checkers/checkers/ | SCRIPT-02: Flow analysis (definitions, transitions) |
| stumble.py | tools/script-checkers/checkers/ | SCRIPT-03: Teleprompter stumble detection |
| scaffolding.py | tools/script-checkers/checkers/ | SCRIPT-04: Scaffolding phrase counter |
| config.py | tools/script-checkers/ | Proportional threshold configuration |
| output.py | tools/script-checkers/ | Markdown/JSON report formatter |
| corpus_builder.py | tools/script-checkers/voice/ | SCRIPT-05: Script-to-transcript diff analysis |
| pattern_extractor.py | tools/script-checkers/voice/ | SCRIPT-05: Frequency analysis with temporal weighting |
| pattern_applier.py | tools/script-checkers/voice/ | SCRIPT-05: Apply patterns to new scripts |
| voice-patterns.json | tools/script-checkers/ | SCRIPT-05: Learned pattern library |
| database.py | tools/discovery/ | DISC-01: SQLite keyword database with CRUD |
| autocomplete.py | tools/discovery/ | DISC-01: YouTube autocomplete scraper |
| keywords.py | tools/discovery/ | DISC-01: Keyword management CLI |
| intent_mapper.py | tools/discovery/ | DISC-02: 6-category intent classification + DNA fit |
| diagnostics.py | tools/discovery/ | DISC-03: Discovery diagnostics (impressions/CTR analysis) |
| analyze.py (extended) | tools/youtube-analytics/ | DISC-03: Includes Discovery Diagnostics section |
| metadata_checker.py | tools/discovery/ | DISC-04: Pre-publish metadata consistency validation |
| vidiq_workflow.py | tools/discovery/ | DISC-04: Guided VidIQ data collection prompts |
| discover.md | .claude/commands/ | DISC-01-04: Unified keyword research command |
| publish.md (extended) | .claude/commands/ | DISC-04: Metadata check gate integration |

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- Reports saved to project folders or channel-data/analyses/ fallback

### Known Issues

**Python 3.14 Compatibility (Phase 11-01):**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble checker code correct but untestable in current environment
- Resolution: Use Python 3.11-3.13, or wait for spaCy Python 3.14 support
- Scaffolding checker works perfectly (no spaCy dependency)

---

*State updated: 2026-01-29 after Phase 13 completion*
