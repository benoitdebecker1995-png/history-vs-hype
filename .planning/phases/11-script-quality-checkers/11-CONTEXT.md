# Phase 11: Script Quality Checkers - Context

**Gathered:** 2026-01-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated quality checks for spoken-delivery scripts. Four checkers that scan scripts to flag issues BEFORE filming:
1. Repetition detection — flag repeated phrases with counts
2. Flow analysis — verify terms defined before use, smooth transitions
3. Stumble test — identify teleprompter stumble risks (long sentences, complex clauses)
4. Scaffolding counter — count "Here's", "So", "Now" and alert when exceeded

This phase builds the quality gates. Learning from user patterns is Phase 12 (Voice Fingerprinting).

</domain>

<decisions>
## Implementation Decisions

### Output Format
- **Both inline + summary** — Annotated script with flags inline, plus summary report
- **Summary at top** — See all issues first, then the annotated script below
- Severity levels: Claude's discretion (research best practices)

### Thresholds & Limits
- **Proportional to script length** — Limits should scale with video length, not be absolute
- Repetition threshold: Claude's discretion (research best practices)
- Scaffolding limit: Claude's discretion, but respect STYLE-GUIDE.md's 2-4 guideline as baseline
- Sentence length for stumble risk: Claude's discretion (research teleprompter best practices)
- Configurability: Claude's discretion

### Detection Scope
- Repetition matching (exact vs near-match): Claude's discretion
- Rhetorical repetition handling: Claude's discretion (research patterns in educational scripts)
- Term definition detection: Claude's discretion (research how educational creators handle this)
- Domain awareness (history/geopolitics terms): Claude's discretion based on feasibility

### Integration & Invocation
- **Automatic execution** — Checkers run automatically whenever /script generates output
- Manual script checking: Claude's discretion on whether to support
- Checker selectability: Claude's discretion
- Blocking behavior on issues: Claude's discretion

### Claude's Discretion
User explicitly delegated most implementation details to Claude's judgment. Key guidance:
- Research AI scriptwriting best practices in the history/educational niche
- Learn from competitor creators (Kraut, Knowing Better, etc.)
- The goal is scripts that don't need checking because they're already good
- Phase 12 handles learning from user's personal patterns — Phase 11 sets sensible defaults

</decisions>

<specifics>
## Specific Ideas

- "I want to make the best videos possible so learn from others"
- "Research best AI scriptwriting practices and learn from me"
- Thresholds should depend on video length AND topic
- The scriptwriter should continuously improve — these checkers are the safety net, not the primary quality source

**Research focus for researcher agent:**
- AI scriptwriting best practices in history/educational YouTube niche
- How top creators (Kraut, Knowing Better, Shaun, Alex O'Connor) structure scripts
- Teleprompter delivery best practices
- Repetition patterns that work vs. ones that don't in spoken content

</specifics>

<deferred>
## Deferred Ideas

- **Learning from user's personal patterns** — Phase 12 (Voice Fingerprinting)
- **Continuous improvement from edits during recording/editing** — Phase 12
- These checkers set defaults; Phase 12 personalizes them

</deferred>

---

*Phase: 11-script-quality-checkers*
*Context gathered: 2026-01-28*
