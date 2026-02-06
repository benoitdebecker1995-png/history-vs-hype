# Phase 28: Pacing Analysis - Context

**Gathered:** 2026-02-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Detect script complexity and pacing issues before filming. Integrates into existing script-checkers CLI (`tools/script-checkers/cli.py`) as a new checker following the established pattern. Quantitative metrics per section with an energy arc visualization across the full script. Does NOT change the script — reports problems for the user to fix manually.

</domain>

<decisions>
## Implementation Decisions

### Warning presentation
- **Default mode:** Problems-only summary (skip clean sections, show only flagged sections)
- **Verbose mode:** `--verbose` flag shows full section-by-section breakdown with all metrics
- **Root cause explanations:** Each warning includes WHY it's a problem (e.g., "high entity density (0.6) — too many proper nouns in sequence"), but NOT fix suggestions
- **Severity:** Score-based per section (0-100), no label categories (no WARNING/CRITICAL labels)
- **Final verdict:** PASS / NEEDS WORK / FAIL based on critical score thresholds — clear go/no-go before filming

### Threshold calibration
- **Source:** Generic defaults from readability/pacing research (not calibrated to user's corpus)
- **Strictness:** Moderate — use the planned thresholds as-is (sentence variance >15, Flesch delta >20, entity density >0.4)
- **Configurability:** Claude's discretion — fit the existing checker architecture pattern
- **Section length:** NOT a scoring factor — length is a style choice for this channel (Kraut runs 30-45 min). Only flag internal pacing issues within sections.

### Energy arc visualization
- **Format:** ASCII sparkline chart showing energy/complexity per section (e.g., `▇▅▃▆█▄▂`)
- **Flat zone detection:** Flag monotone stretches — 3+ consecutive sections with similar scores trigger "energy plateau, consider pattern interrupt" advisory
- **Ideal arc comparison:** Claude's discretion — determine if a reference arc adds value
- **Placement in output:** Claude's discretion — place where it flows best with the rest of the report

### Modern relevance / pattern interrupt detection
- **Enforcement level:** Advisory only — note the guidelines but don't score or flag as errors. These are creative choices, not mechanical rules.
- **Hook detection method:** Combined keyword heuristic + B-roll marker proxy (time markers like "today", "2024", "still", "currently" + B-roll markers like [NEWS CLIP], [MODERN MAP])
- **Pattern interrupt detection:** Claude's discretion — pick the most reliable approach
- **Severity:** Claude's discretion — determine how to weight missing hooks (separate advisory line vs integrated into score)

### Claude's Discretion
- Configurability approach (config file vs hardcoded vs CLI flags)
- Energy arc placement in output
- Ideal arc comparison inclusion
- Pattern interrupt detection method
- Hook/interrupt severity weighting
- Exact score thresholds for PASS/NEEDS WORK/FAIL verdict

</decisions>

<specifics>
## Specific Ideas

- Must integrate with existing `cli.py` following the established checker pattern (like stumble, scaffolding, repetition, flow checkers)
- The `--pacing` flag on cli.py should invoke this checker
- Section parsing should reuse the production parser from Phase 22 (`tools/production/parser.py`) for consistent section detection
- Channel writes long-form scripts (10-45 min videos) — the checker must handle scripts of any length without false-flagging length itself

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 28-pacing-analysis*
*Context gathered: 2026-02-06*
