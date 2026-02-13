# Research Summary: v3.0 Adaptive Scriptwriter

**Synthesized:** 2026-02-12
**Sources:** STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md

---

## Key Findings

### Stack Additions
- **Minimal new dependencies.** Python stdlib (difflib, re, json) handles most work. Claude API for edit classification. No new external libraries needed.
- **New module:** `tools/script-analysis/` (~1,200-2,000 LOC) with transcript_analyzer.py, edit_tracker.py, technique_library.py
- **DB migration:** user_version 27→28, 3 new tables (script_edits, script_choices, creator_techniques)
- **Hybrid storage:** SQLite for structured data, JSON for preference model, markdown for technique library (agent reads markdown directly)

### Feature Table Stakes
1. **Retention science** — Synthesize existing analytics into prescriptive rules (STYLE-GUIDE Part 9)
2. **Creator analysis** — Parse 80+ existing transcripts, extract techniques, build searchable library (Part 8)
3. **Choice architecture** — 2-3 hook/structure variants, user picks, choices logged
4. **Edit learning** — Compare generated vs edited scripts, classify edits, build preference model

### Watch Out For
1. **Prompt bloat** — Agent is 1,284 lines. Budget max 1,500. Consolidate, don't accumulate.
2. **Learning from noise** — Accuracy fixes ≠ voice preferences. Classify edits before learning.
3. **Setup friction** — v1.2 voice fingerprinting went unused. Design for zero-setup.
4. **Variant fatigue** — Max 3 options, always recommend one, make optional.
5. **Formulaic scripts** — Retention rules as playbook, not rulebook.

### Build Order (Dependency-Aware)
1. **Phase 36: Retention Science** — Quick win, no new code, immediate improvement
2. **Phase 37: Creator Transcript Analysis** — Builds technique library
3. **Phase 38: Structured Choice Architecture** — Low effort, starts generating choice data
4. **Phase 39: Edit-Based Learning Loop** — Most complex, benefits from other phases' data

### Critical Design Decisions
- Agent "learning" = evolving reference docs + preference context, not ML training
- Preferences require 3+ consistent edits to become confirmed (prevent over-fitting)
- Quality rules (1-14) always override learned preferences (15)
- Zero-setup: analyze existing transcripts/ folder as-is, no reorganization required

---

*Synthesis complete: 2026-02-12*
