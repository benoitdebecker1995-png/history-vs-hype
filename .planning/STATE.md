# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-30 (v1.2 milestone archived)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-30)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.2 ARCHIVED — Ready for v1.3 planning or production use

## Current Position

**Milestone:** v1.2 Script Quality & Discovery — ARCHIVED
**Phase:** All phases complete
**Status:** Ready for next milestone
**Last activity:** 2026-01-30 — v1.2 archived

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [                    ]   0% — Not started
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |

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

**Discovery commands (v1.2):**
- `/discover TOPIC` — keyword research workflow
- `/discover --check FILE` — pre-publish metadata validation

**Script quality tools (v1.2):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --voice` — apply voice patterns

## Session Continuity

### Last Session

- **Date:** 2026-01-30
- **Work:** Archived v1.2 milestone
- **Output:**
  - milestones/v1.2-ROADMAP.md
  - milestones/v1.2-REQUIREMENTS.md
  - milestones/v1.2-MILESTONE-AUDIT.md
  - Updated MILESTONES.md, PROJECT.md, ROADMAP.md

### Next Session

**Options:**
1. **Production use** — Use tools for video production
2. **v1.3 planning** — Run `/gsd:new-milestone` to define next milestone

**v1.2 Deliverables (now available):**
- Script quality checkers: `tools/script-checkers/`
- Voice fingerprinting: `tools/script-checkers/voice/`
- Discovery tools: `tools/discovery/`
- NotebookLM templates: `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md`
- Model assignments: `.claude/REFERENCE/MODEL-ASSIGNMENT-GUIDE.md`

## Accumulated Context

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate

### Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus

---

*State updated: 2026-01-30 after v1.2 milestone archived*
