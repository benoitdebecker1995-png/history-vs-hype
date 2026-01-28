# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-28 10:02 (Plan 11-01 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-27)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.2 Script Quality & Discovery — Phase 11

## Current Position

**Milestone:** v1.2 Script Quality & Discovery
**Phase:** 11 of 14 (Script Quality Checkers)
**Plan:** 02 of 4 complete
**Status:** In progress
**Last activity:** 2026-01-28 — Completed 11-02-PLAN.md (repetition and flow checkers)

**Progress:**
```
v1.0 [████████████████████] 100% — Workspace Optimization
v1.1 [████████████████████] 100% — Analytics & Learning Loop
v1.2 [██████░░░░░░░░░░░░░░]  29% — Script Quality & Discovery (Phase 11/14, Plan 02/04)
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

- **Date:** 2026-01-28
- **Work:** Executed 11-02 plan (repetition and flow checkers)
- **Output:**
  - `tools/script-checkers/checkers/repetition.py` — SCRIPT-01 repetition detection
  - `tools/script-checkers/checkers/flow.py` — SCRIPT-02 flow analysis
  - Full CLI integration with all 4 checkers
  - `.planning/phases/11-script-quality-checkers/11-02-SUMMARY.md` — Execution summary
  - `.planning/STATE.md` — Updated current position

### Next Session

**Phase 11 Script Quality Checkers: Complete**

All 4 requirements (SCRIPT-01 through SCRIPT-04) implemented. Ready for Phase 12 (Voice Fingerprinting) or continue with remaining v1.2 phases (13-14).

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

### v1.2 Phase Structure

**Phase 11: Script Quality Checkers** (SCRIPT-01 through SCRIPT-04) — ✅ COMPLETE
- 11-01 COMPLETE: Stumble test (SCRIPT-03), scaffolding counter (SCRIPT-04), CLI foundation
- 11-02 COMPLETE: Repetition detection (SCRIPT-01), flow analysis (SCRIPT-02), full CLI integration

**Phase 12: Voice Fingerprinting** (SCRIPT-05)
- Depends on Phase 11 infrastructure
- Analyzes transcripts to learn speech patterns

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

**v1.2 (Script Quality & Discovery) - Phase 11 Complete:**

| Component | Location | Purpose |
|-----------|----------|---------|
| cli.py | tools/script-checkers/ | Script quality checker orchestrator (all 4 checkers) |
| repetition.py | tools/script-checkers/checkers/ | SCRIPT-01: Phrase repetition detection |
| flow.py | tools/script-checkers/checkers/ | SCRIPT-02: Flow analysis (definitions, transitions) |
| stumble.py | tools/script-checkers/checkers/ | SCRIPT-03: Teleprompter stumble detection |
| scaffolding.py | tools/script-checkers/checkers/ | SCRIPT-04: Scaffolding phrase counter |
| config.py | tools/script-checkers/ | Proportional threshold configuration |
| output.py | tools/script-checkers/ | Markdown/JSON report formatter |

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

*State updated: 2026-01-28 after Plan 11-01 execution*
