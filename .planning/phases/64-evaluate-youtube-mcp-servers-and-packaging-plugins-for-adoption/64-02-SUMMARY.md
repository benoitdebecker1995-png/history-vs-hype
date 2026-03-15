---
phase: 64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption
plan: 02
subsystem: tooling
tags: [mcp, youtube-api, playwright, context7, decision-log]

# Dependency graph
requires:
  - phase: 64-01
    provides: Context7 + Playwright MCP installed and verified; Firecrawl substitution decision locked
provides:
  - Final DECISION.md with adopt/skip verdicts for all 12 evaluated MCP tools
  - Evidence-based documentation of why ZubeidHendricks and Windsor AI were skipped
  - Install test results proving both YouTube MCP options are broken (not just stale)
affects:
  - Any future phase adding MCP servers (check 64-DECISION.md first)
  - CLAUDE.md Tool Stack section (pending update in future phase)
  - /research command workflow (Playwright available for JS-rendered archive pages)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Evaluate before committing: test-install EVALUATE-tier tools, clean up failures, document root cause"
    - "Two-tier evidence: research verdict + install test result for each tool"

key-files:
  created:
    - .planning/phases/64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption/64-DECISION.md
  modified:
    - .planning/phases/64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption/64-INSTALL-LOG.md

key-decisions:
  - "ZubeidHendricks YouTube MCP SKIP: broken npm package — MCP SDK restructured dist/cjs/index.js path, package incompatible with current SDK"
  - "DannySubsense youtube-mcp-server SKIP: malformed PyPI wheel, dist-info installs but no module files"
  - "Windsor AI SKIP: cloud-only OAuth connector, no installable MCP package, identical data coverage to existing tools/youtube_analytics/"
  - "No YouTube transcript MCP needed: yt-dlp.exe is the stable extraction path, all MCP alternatives are broken"
  - "Playwright ADOPT (confirmed): free unlimited local browser automation replaces Firecrawl"

patterns-established:
  - "Install-test-remove pattern: install EVALUATE tools, smoke test, remove if broken or redundant, document root cause"

requirements-completed:
  - EVAL-EVALUATE-01
  - EVAL-EVALUATE-02
  - EVAL-DECISION

# Metrics
duration: 35min
completed: 2026-03-15
---

# Phase 64 Plan 02: EVALUATE-Tier Testing and Final Decision Lock

**DECISION.md locked with 12 tool verdicts — 2 adopted (Context7 + Playwright), 9 skipped, both YouTube MCP options confirmed broken via install test**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-03-15T21:45:00Z
- **Completed:** 2026-03-15T22:24:37Z
- **Tasks:** 3 (including checkpoint approval)
- **Files modified:** 2

## Accomplishments

- Confirmed ZubeidHendricks YouTube MCP is broken: npm package installs but crashes immediately due to MCP SDK restructuring breaking its dist/cjs/index.js path
- Confirmed DannySubsense Python fallback is also broken: malformed PyPI wheel with dist-info only, no module files
- Evaluated Windsor AI: no installable MCP package exists, cloud-only connector, data duplicates existing tools
- Cleaned up all failed installs (npm uninstall + pip uninstall)
- Created DECISION.md with evidence-based verdicts for all 12 tools

## Task Commits

1. **Task 1: Test-install EVALUATE-tier YouTube MCP tools** — `48d9094` (chore)
2. **Task 2: Write final DECISION.md with all verdicts** — `9e35ed2` (feat)
3. **Task 3: Checkpoint approval** — user approved, no code changes

## Files Created/Modified

- `.planning/phases/64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption/64-DECISION.md` — Final adoption verdicts with evidence for all 12 tools, installation commands for adopted tools, re-evaluation triggers
- `.planning/phases/64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption/64-INSTALL-LOG.md` — Updated with Steps 4 and 5: ZubeidHendricks test (BROKEN), DannySubsense test (BROKEN), Windsor AI evaluation (SKIP)

## Decisions Made

- **ZubeidHendricks SKIP:** The npm package `zubeid-youtube-mcp-server` installs 122 packages but immediately throws `MODULE_NOT_FOUND` for `@modelcontextprotocol/sdk/dist/cjs/index.js`. Root cause: MCP SDK restructured to sub-path exports sometime after January 2024; the expected `dist/cjs/index.js` path no longer exists in any installed SDK version. Not fixable without package update.
- **DannySubsense SKIP:** The pip package `youtube-mcp-server 0.1.0` installs dist-info but no Python module files. `import youtube_mcp_server` fails with `ModuleNotFoundError`. Malformed at distribution level.
- **Windsor AI SKIP:** Searched npm for `windsor-ai`, `@windsor.ai/mcp`, `windsor-mcp` — all 404. Windsor AI is a cloud dashboard with an OAuth connector, not a Claude Code MCP server. Data coverage identical to existing `tools/youtube_analytics/`.
- **No YouTube transcript MCP:** Both tested options are broken. `yt-dlp.exe` is the established, working transcript path. Re-evaluate only if a new, well-maintained YouTube MCP server appears.

## Deviations from Plan

### Plan 02 vs. Executed

**1. [Plan deviation] DannySubsense tested as additional fallback**
- **Context:** Plan specified ZubeidHendricks (npm) as primary, DannySubsense (pip) as fallback "if the npm package fails"
- **Action:** npm package failed → tested DannySubsense fallback as specified → also failed
- **Impact:** Both options exhausted; SKIP verdict confirmed by double failure

**2. [Carried from Plan 01] Firecrawl SKIP / Playwright ADOPT**
- **Context:** Plan 02 template listed Firecrawl as ADOPT and Playwright as DEFER
- **Reality:** User decided in Plan 01 to skip Firecrawl (500 lifetime credits unsustainable) and adopt Playwright instead
- **DECISION.md reflects:** Firecrawl = SKIP, Playwright = ADOPT — matches actual installed state

---

**Total deviations:** 2 (1 expected per plan, 1 carried from Plan 01). No scope creep.

## Issues Encountered

- `pip install youtube-mcp-server` initially failed with `WinError 32` (file lock from another process). Resolved with `--user` flag. Ultimately irrelevant as the package was broken regardless.
- Windsor AI OAuth evaluation not possible without browser interaction — evaluated via API package search instead. Evidence sufficient for SKIP verdict.

## User Setup Required

None — no external service configuration required. Adopted tools (Context7, Playwright) are already installed and connected from Plan 01.

## Next Phase Readiness

Phase 64 evaluation complete. Decisions locked:
- **Playwright MCP** available for JS-rendered archive page scraping during research (`/research` workflow)
- **Context7 MCP** available for library documentation injection during any implementation work
- **CLAUDE.md Tool Stack** section can be updated in a future phase if desired (not done here per plan spec)
- **YouTube transcript extraction:** yt-dlp.exe remains the path — no MCP alternative available

---
*Phase: 64-evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption*
*Completed: 2026-03-15*
