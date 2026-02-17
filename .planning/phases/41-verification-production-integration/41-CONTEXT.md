# Phase 41: Verification & Production Integration - Context

**Gathered:** 2026-02-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Integration of the Phase 40 translation pipeline into existing production commands: `/verify --translation` for translation verification, script-writer-v2 document-structured mode for clause-by-clause scriptwriting, and `/prep` with split-screen edit guides. Input is Phase 40 translation output; output is verified translations, filmable scripts, and editor-ready staging guides.

</domain>

<decisions>
## Implementation Decisions

### Verification workflow
- **Verification modes:** Both "audit existing output" (default) and "re-run fresh" (`--fresh` flag). Default mode reads translation output and checks completeness (cross-check done, annotations present, no gaps). Fresh mode re-runs cross-checker + annotator from scratch
- **Scholarly comparison:** Both options available. `--scholarly-summary FILE` for user-provided scholarly descriptions; default uses Claude's training knowledge to compare translation against known scholarly interpretations. User input takes priority when provided
- **Report format:** Always save full report to TRANSLATION-VERIFICATION.md in project folder + print condensed summary to terminal
- **Quality gate:** Tiered verdict system — GREEN (no issues), YELLOW (minor discrepancies — proceed with caution), RED (significant problems — revise before filming)

### Document-structured scripting
- **Clause ordering:** Document order by default. `--group-thematic` flag allows thematic reordering (grouping related clauses). Most videos follow document order; some benefit from grouping
- **Surprise handling:** Both inline emphasis during walkthrough AND synthesis section recap. Major surprises appear twice — emphasized during clause walkthrough, then highlighted again in "What They Got Wrong" synthesis section
- **Original text in script:** Teleprompter-aware approach. Full script includes original-language text in visual staging notes. Teleprompter export (`--teleprompter`) strips them for clean reading flow
- **Translation input:** Auto-detect from project folder + explicit `--translation PATH` override. Script-writer looks for translation output automatically; `--translation` flag overrides. Explicit takes priority

### Split-screen edit guides
- **Timing granularity:** Both per-clause estimates AND section-level totals. Each clause gets breakdown (read original + translate + explain), nested inside section duration totals
- **Transition markers:** Hybrid approach — key talking-head ↔ document display transition points marked explicitly (e.g., "switch to document for Article 3"), plus overall ratio guidance per section (e.g., "40% talking head, 60% document display")
- **Asset sourcing:** Auto-generate from Phase 39 archive lookup where possible, leave [NEEDED] placeholders for non-document assets (maps, photos, context visuals). Combines automated archive URLs with manual supplement template
- **Highlight cues:** Surprise markers only — Major and Notable surprises flagged for editor emphasis. Legal terms and other moments left to editor judgment (avoids noise)

### Claude's Discretion
- Exact prompt engineering for document-structured script generation
- How to integrate with existing script-writer-v2 rules (new rule vs. mode flag)
- Verification report internal structure and scoring algorithm
- Edit guide markdown formatting and section headings

</decisions>

<specifics>
## Specific Ideas

- Tiered verdict (GREEN/YELLOW/RED) mirrors traffic light pattern — intuitive for quick filming decisions
- Surprise clauses appearing twice in script (inline + recap) mirrors the format guide's "synthesis" section pattern — reinforcement for the viewer
- Teleprompter-aware original text means the same script file works for both planning (see what goes on screen) and filming (clean spoken text)
- Auto-detect + override for translation input follows the same pattern as other slash commands (e.g., how /analyze auto-finds video data)
- Per-clause timing breakdown helps the creator plan filming sessions ("Articles 1-5 are about 12 minutes, good stopping point")

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 41-verification-production-integration*
*Context gathered: 2026-02-17*
