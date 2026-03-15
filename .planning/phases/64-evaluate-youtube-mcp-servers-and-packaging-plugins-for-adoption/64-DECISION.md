# Phase 64: Final Tool Adoption Decisions

**Evaluation date:** 2026-03-15
**Platform:** Windows MSYS_NT-10.0-26200 (MSYS2 / Git Bash / Claude Code)
**Total tools evaluated:** 12 (11 original candidates + Playwright promoted from DEFER after Firecrawl substitution)
**Evidence sources:** 64-RESEARCH.md (research verdicts), 64-INSTALL-LOG.md (install test results)

---

## Summary

| Verdict | Count | Tools |
|---------|-------|-------|
| ADOPT | 2 | Context7 MCP, Playwright MCP |
| SKIP | 9 | TubeFlow, ZubeidHendricks YouTube MCP, Firecrawl MCP, Claude-Mem, Writing Skill Plugin, Windsor AI, Sequential Thinking, claude-seo, Thumbnail generators |
| DEFER | 0 | — |
| BROKEN | 1 | DannySubsense youtube-mcp-server (malformed wheel) |

**Key deviation from plan:** Firecrawl MCP changed from ADOPT to SKIP (500 lifetime credits unsustainable). Playwright MCP changed from DEFER to ADOPT (replaces Firecrawl, free unlimited local scraping).

---

## Per-Tool Verdict Table

| # | Tool | Category | Verdict | Evidence Source | Action Taken |
|---|------|----------|---------|----------------|--------------|
| 1 | TubeFlow (wnstify/tubeflow) | Content pipeline | SKIP | Research | Not installed |
| 2 | ZubeidHendricks YouTube MCP | Transcript/metadata | SKIP | Install test | Installed + removed (broken) |
| 3 | DannySubsense youtube-mcp-server | Transcript extraction | SKIP | Install test | Installed + removed (broken wheel) |
| 4 | Firecrawl MCP | Web scraping | SKIP | User decision | Never installed |
| 5 | Claude-Mem | Cross-session memory | SKIP | Research | Not installed |
| 6 | Context7 MCP | Library docs | ADOPT | Install test | Installed, connected, verified |
| 7 | Writing Skill Plugin | Voice consistency | SKIP | Research | Not applicable (undefined tool) |
| 8 | Windsor AI YouTube Analytics | Analytics queries | SKIP | Evaluation | Not installed (cloud-only, no MCP package) |
| 9 | Playwright MCP | JS browser scraping | ADOPT | Install test | Installed, connected, verified |
| 10 | Sequential Thinking MCP | Reasoning chains | SKIP | Research | Not installed |
| 11 | claude-seo | SEO optimization | SKIP | Research | Not installed (repo unverified) |
| 12 | Thumbnail generators | Thumbnail creation | SKIP | Research | Not installed |

---

## Adopted Tools — Full Detail

### 1. Context7 MCP

**What it does:** Fetches version-specific library documentation and injects it into Claude Code sessions. Eliminates hallucinated API signatures for fast-moving libraries.

**Installation command (tested, working):**
```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

**Scope:** User-global (available in all projects via `--scope user`)

**Configuration requirements:**
- No API key required for basic usage
- Optional: free Upstash API key at context7.com/dashboard for higher rate limits

**What it provides that existing tools do NOT:**
- Live documentation injection for any npm/PyPI library
- Version-specific API signatures (avoids training data staleness)
- Particularly useful when implementing new MCP servers or testing YouTube API endpoints

**Usage examples for this channel's workflow:**
```
# During MCP implementation work
use context7 for @playwright/mcp — get current API docs
use context7 for youtube-data-v3 — verify current endpoint signatures
use context7 for fastmcp — get current Python MCP SDK patterns
```

**Verification:**
```
context7: npx -y @upstash/context7-mcp - ✓ Connected
```

---

### 2. Playwright MCP

**What it does:** Local headless browser automation for JS-rendered pages. Navigates sites that require JavaScript execution, login flows, or dynamic content loading that WebFetch/WebSearch cannot handle.

**Installation command (tested, working):**
```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest --headless
```

**Scope:** Project-local (D:\History vs Hype only)

**Configuration requirements:**
- No API key required
- No environment variables needed
- Browsers install automatically on first use

**What it provides that existing tools do NOT:**
- Full browser automation (click, scroll, wait for JS, fill forms)
- JS-rendered page content extraction (Wayback Machine, archive.org, Legifrance, JSTOR)
- Interactive navigation (multi-step flows, login-then-scrape)
- `WebFetch` only gets HTML; Playwright gets what a real browser sees after JS execution

**Usage examples for this channel's workflow:**
```
# Research phase: primary source archives
playwright_navigate — https://gallica.bnf.fr/search — for Vichy-era documents
playwright_navigate — https://web.archive.org/web/*/legifrance.gouv.fr — archived law texts
playwright_get_visible_text — extract readable content from JS-rendered archive pages

# Fact verification: paywall preview pages
playwright_navigate — https://www.jstor.org/stable/[article-id] — get abstract + preview
```

**Why Playwright over Firecrawl:**
- Firecrawl: 500 lifetime credits free, then $16/month. Not sustainable for weekly research.
- Playwright: Unlimited, free, local, no API key. Minor tradeoff: no Cloudflare bypass (Firecrawl had this).

**Verification:**
```
playwright: npx -y @playwright/mcp@latest --headless - ✓ Connected
```

---

## Skipped Tools — Evidence Summary

### 1. TubeFlow (wnstify/tubeflow)

**Verdict: SKIP**

**Evidence:**
- 8 GitHub stars, single developer, 7 total commits
- Direct workflow conflict: 9 agents performing functions this project already handles (topic discovery, SEO research, script writing, metadata generation)
- Ignores PACKAGING_MANDATE.md hard reject rules and measured CTR data from title_scorer.py
- Adopting TubeFlow would create a parallel pipeline that diverges from channel-specific tooling

**Reference:** 64-RESEARCH.md § T1-A

---

### 2. ZubeidHendricks YouTube MCP

**Verdict: SKIP**

**Evidence (install test):**
- npm package installs without errors but crashes immediately
- Root cause: package expects `@modelcontextprotocol/sdk/dist/cjs/index.js` which no longer exists after SDK restructured to sub-path exports
- Package was last updated January 2024 — 14+ months stale, incompatible with current MCP SDK
- DannySubsense Python fallback also broken: malformed wheel, dist-info installs but no Python module files
- Existing yt-dlp.exe handles transcript extraction without API quota

**Commands run:**
```bash
npm install -g zubeid-youtube-mcp-server  # installs but broken
npx zubeid-youtube-mcp-server              # crashes: MODULE_NOT_FOUND
npm uninstall -g zubeid-youtube-mcp-server # cleaned up
```

**Reference:** 64-INSTALL-LOG.md § Step 4

---

### 3. Firecrawl MCP

**Verdict: SKIP**

**Evidence (user decision, Plan 01):**
- Free tier: 500 one-time lifetime credits (not monthly)
- At ~5 scrapes per research session × weekly videos = depleted in 2 months
- Playwright MCP provides equivalent JS-rendered scraping locally for free

**What was adopted instead:** Playwright MCP (identical use case, unlimited, free)

**Reference:** 64-INSTALL-LOG.md § Deviation: Firecrawl → Playwright

---

### 4. Claude-Mem

**Verdict: SKIP**

**Evidence:**
- GitHub Issue #1063: 641 chroma-mcp processes spawn from 6 sessions on Windows/WSL2, consuming 75% CPU and ~64GB virtual memory — system-crash-level failure
- GitHub Issue #707: Chroma process uses 35GB RAM; SQLite-only mode proposed but not default
- This machine runs Windows MSYS_NT — exact trigger conditions for the process storm
- Existing CLAUDE.md + MEMORY.md + channel-data/ pattern already handles cross-session context without risk

**Reference:** 64-RESEARCH.md § T2-A

---

### 5. Writing Skill Plugin

**Verdict: SKIP (category undefined)**

**Evidence:**
- No specific tool identified with clear provenance
- Project already has STYLE-GUIDE.md (543+ lines), script-writer-v2 agent, structure-checker-v2 agent, OPENING-HOOK-TEMPLATES.md, CLOSING-SYNTHESIS-TEMPLATES.md
- The existing voice consistency system IS the writing skill mechanism

**Reference:** 64-RESEARCH.md § T2-C

---

### 6. Windsor AI YouTube Analytics MCP

**Verdict: SKIP**

**Evidence (evaluation, Plan 02):**
- No installable MCP package exists: npm search for `windsor-ai`, `@windsor.ai/mcp`, `windsor-mcp` all return 404
- Windsor AI is a cloud-based dashboard with an OAuth connector, not a Claude Code MCP server
- Data coverage: channel metrics, video performance, traffic sources, audience demographics — identical to existing `tools/youtube_analytics/` (OAuth-authenticated)
- Natural language query UX benefit is achievable by asking Claude Code to query the analytics DB directly

**Reference:** 64-INSTALL-LOG.md § Step 5

---

### 7. Sequential Thinking MCP

**Verdict: SKIP**

**Evidence:**
- Claude Code's native reasoning is sufficient for this project's complexity
- The main use case (multi-step research synthesis) is already handled by CONTEXT.md + structured phase planning
- Would add value only for architectural design tasks — occasional edge case doesn't justify permanent installation

**Reference:** 64-RESEARCH.md § T3-C

---

### 8. claude-seo

**Verdict: SKIP**

**Evidence:**
- Repository `AgriciDaniel/claude-seo` could not be verified on GitHub during research
- LOW confidence — existence unconfirmed
- Even if it exists: project has `title_scorer.py` (measured CTR data), `tools/discovery/` suite, `tools/preflight/scorer.py` (5-gate system) — SEO tooling is custom and data-backed

**Reference:** 64-RESEARCH.md § T3-D

---

### 9. Thumbnail Generators (jordicor/youtube_thumbnail_generator_with_AIs)

**Verdict: SKIP**

**Evidence:**
- 2 GitHub stars, January 4, 2026
- High setup complexity: Redis, FFmpeg, Gran Sabio LLM server, Gemini API
- Direct policy conflict: PACKAGING_MANDATE.md enforces map-first, no-face, no-text thumbnails; AI generators produce face/text thumbnails
- Existing workflow: Photoshop + thumbnail_checker.py (concept validation) is established and policy-compliant

**Reference:** 64-RESEARCH.md § T3-D

---

## Impact on Existing Workflow

### Slash Commands Gaining New Capabilities

| Command | New Capability | Via |
|---------|---------------|-----|
| `/research` | JS-rendered archive scraping (Wayback Machine, Legifrance, JSTOR previews) | Playwright MCP |
| Any command with code/tool implementation | Live library documentation injection | Context7 MCP |

### CLAUDE.md Tool Stack Section — Recommended Update

Add to the Tool Stack section:
```
- **Context7 MCP** — Live library documentation injection into Claude Code sessions
- **Playwright MCP** — Local headless browser for JS-rendered archive pages during research
```

Note: CLAUDE.md update is deferred to a future phase (not done in this plan).

### Existing Tools That Remain Active

No existing tools become redundant from this evaluation:
- `yt-dlp.exe` — still preferred for transcript extraction (no API quota)
- `tools/youtube_analytics/` — still the analytics layer (Windsor AI is not an alternative)
- `title_scorer.py`, `thumbnail_checker.py`, preflight scorer — packaging tools unaffected
- `script-writer-v2` agent — writing system unaffected

---

## Deferred Items

No tools are in DEFER status. All candidates are either ADOPT or SKIP.

### Future Re-evaluation Triggers

**Claude-Mem (currently SKIP):**
- Re-evaluate when GitHub Issue #1063 (Chroma process storm) is marked resolved
- Check: does `CHANGELOG.md` show SQLite-only mode as default?
- Target date: 2026-09-15 (6 months — allow time for fix to stabilize)

**YouTube MCP server (currently SKIP):**
- Re-evaluate if a new well-maintained YouTube MCP server appears (>100 stars, <3 months old, MCP SDK >= 1.5)
- The use case (Claude-native transcript access without yt-dlp invocation) has value — the existing implementations are just broken
- Monitor: modelcontextprotocol/servers official registry

---

## Decisions Locked

1. **Playwright over Firecrawl:** Free, unlimited, local browser scraping. No API credits.
2. **No YouTube transcript MCP:** Both tested packages broken. yt-dlp.exe is the stable path.
3. **No analytics MCP:** Windsor AI has no installable package; existing tools cover the same data.
4. **No memory MCP:** Claude-Mem is a Windows stability risk. CLAUDE.md + MEMORY.md is the safe alternative.
5. **Context7 is the only "quality of life" addition:** Low friction, no workflow changes, free.

---

*Decision log locked: 2026-03-15. Valid until 2026-06-15 for stable tools; 2026-09-15 for claude-mem re-evaluation.*
