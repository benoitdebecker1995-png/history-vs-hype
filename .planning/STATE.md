# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-29 (Phase 12 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-27)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.2 Script Quality & Discovery — Phase 13

## Current Position

**Milestone:** v1.2 Script Quality & Discovery
**Phase:** 12 of 14 (Voice Fingerprinting)
**Plan:** 2 of 2
**Status:** Phase complete
**Last activity:** 2026-01-29 — Completed 12-02-PLAN.md (pattern application and CLI integration)

**Progress:**
```
v1.0 [████████████████████] 100% — Workspace Optimization
v1.1 [████████████████████] 100% — Analytics & Learning Loop
v1.2 [███████████░░░░░░░░░]  50% — Script Quality & Discovery (Phase 12/14)
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

## Session Continuity

### Last Session

- **Date:** 2026-01-29
- **Work:** Executed 12-02 plan (pattern application and CLI integration)
- **Output:**
  - `tools/script-checkers/voice/pattern_applier.py` — Apply learned patterns to new scripts
  - Updated `tools/script-checkers/voice/__init__.py` — Lazy imports for optional dependencies
  - Updated `tools/script-checkers/cli.py` — CLI integration with --voice flags
  - `.planning/phases/12-voice-fingerprinting/12-02-SUMMARY.md` — Execution summary
  - `.planning/STATE.md` — Updated current position

### Next Session

**Phase 12 Voice Fingerprinting: Complete**

Both plans complete. Voice fingerprinting infrastructure ready for use in scriptwriting workflow.

Next phase: Phase 13 (Discovery Tools) or Phase 14 (NotebookLM Workflow) per roadmap.

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

### v1.2 Phase Structure

**Phase 11: Script Quality Checkers** (SCRIPT-01 through SCRIPT-04) — ✅ COMPLETE 2026-01-28
- 11-01 COMPLETE: Stumble test (SCRIPT-03), scaffolding counter (SCRIPT-04), CLI foundation
- 11-02 COMPLETE: Repetition detection (SCRIPT-01), flow analysis (SCRIPT-02), full CLI integration
- Verification: PASSED 8/8 must-haves

**Phase 12: Voice Fingerprinting** (SCRIPT-05) — ✅ COMPLETE 2026-01-29
- 12-01 COMPLETE: Corpus builder, pattern extractor, initial pattern library structure
- 12-02 COMPLETE: Pattern applier, CLI integration with --voice flags
- Verification: CLI accepts --voice, --show-voice-changes, --rebuild-voice flags

**Phase 13: Discovery Tools** (DISC-01 through DISC-04)
- Can run parallel to Phase 12
- Keyword research, search intent, impression diagnostics

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

**v1.2 (Script Quality & Discovery) - Phases 11-12 Complete:**

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

*State updated: 2026-01-28 after Phase 11 completion*
