# Phase 64: MCP Installation Log

**Date:** 2026-03-15
**Platform:** Windows MSYS_NT-10.0-26200 (MSYS2 / Git Bash)

---

## Status Summary

| Tool | Status | Notes |
|------|--------|-------|
| Context7 MCP | ✓ INSTALLED — Connected | Scope: user (global) |
| Playwright MCP | ✓ INSTALLED — Connected | Scope: project (replaces Firecrawl) |
| Firecrawl MCP | SKIPPED | Free tier = 500 lifetime scrapes, not sustainable |
| ZubeidHendricks YouTube MCP | TESTED — FAILED | npm package broken: SDK dist/cjs/index.js missing after MCP SDK restructure |
| DannySubsense youtube-mcp-server | TESTED — FAILED | PyPI package malformed: dist-info installs but no module files |
| Windsor AI MCP | EVALUATED — SKIP | No installable package; cloud-only OAuth connector; data duplicates existing tools |

---

## Deviation: Firecrawl → Playwright

**Original plan:** Install Firecrawl MCP (cloud-based JS scraping, 500 free credits).
**User decision:** Skip Firecrawl — 500 lifetime credits too limited, wants to stay free.
**Replacement:** Playwright MCP (`@playwright/mcp`) — free, unlimited, local browser automation. Handles JS-rendered pages without API costs.

**Trade-offs:**
- Playwright runs a local headless browser (heavier than API call)
- No anti-bot bypass (Firecrawl handles Cloudflare etc.)
- Unlimited usage, zero cost, no API key needed
- Official Playwright team package (Microsoft-maintained)

---

## Step 1: Pre-flight Checks

### Existing MCP Servers (before install)

```bash
claude mcp list
```

Output:
```
claude.ai Gmail: https://gmail.mcp.claude.com/mcp - ! Needs authentication
claude.ai Google Calendar: https://gcal.mcp.claude.com/mcp - ! Needs authentication
youtube-data: npx -y @anthropic-ai/claude-code-mcp-youtube-data - ✗ Failed to connect
```

---

## Step 2: Context7 MCP Installation

### Command

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

### Output

```
Added stdio MCP server context7 with command: npx -y @upstash/context7-mcp to user config
File modified: C:\Users\Benoi\.claude.json
```

### Verification

```
context7: npx -y @upstash/context7-mcp - ✓ Connected
```

**Result: PASS**

### Notes

- `--scope user` = global (available in all projects)
- No API key required for basic usage (rate-limited without Upstash key)

---

## Step 3: Playwright MCP Installation

### Attempt 1 (wrong package)

```bash
claude mcp add playwright -- npx -y @anthropic-ai/mcp-playwright
# Result: FAILED — package does not exist on npm (404)
```

### Attempt 2 (correct package)

```bash
claude mcp remove playwright
claude mcp add playwright -- npx -y @playwright/mcp@latest --headless
```

### Output

```
Added stdio MCP server playwright with command: npx -y @playwright/mcp@latest --headless to local config
File modified: C:\Users\Benoi\.claude.json [project: D:\History vs Hype]
```

### Verification

```
playwright: npx -y @playwright/mcp@latest --headless - ✓ Connected
```

**Result: PASS**

### Notes

- Project-scoped (local config, not user-global)
- `--headless` flag = no browser window pops up
- Official package by Playwright team (v0.0.68, published 2026-02-14)

---

## Final MCP List (Post-Install)

```
context7: npx -y @upstash/context7-mcp - ✓ Connected
playwright: npx -y @playwright/mcp@latest --headless - ✓ Connected
```

Both tools connected and functional.

---

---

## Step 4: ZubeidHendricks YouTube MCP (EVALUATE tier — Plan 02)

### Attempt: npm install

```bash
npm install -g zubeid-youtube-mcp-server
# Result: installed 122 packages (no errors)
```

### Smoke Test

```bash
npx zubeid-youtube-mcp-server
```

**Output:**
```
Error: Cannot find module '...node_modules/@modelcontextprotocol/sdk/dist/cjs/index.js'
    at createEsmNotFoundErr (node:internal/modules/cjs/loader:1458:15)
```

**Root cause:** The package was built against `@modelcontextprotocol/sdk ^1.1.1` and expects `dist/cjs/index.js` at the package root. The current SDK (1.x) restructured to sub-path exports — `dist/cjs/` contains `client/`, `server/`, `shared/` subdirectories but no top-level `index.js`. The package's require path is permanently broken against any installed SDK version.

**Verdict: BROKEN — cannot proceed to Claude MCP registration.**

### Fallback: DannySubsense Python variant

```bash
pip install --user youtube-mcp-server
# Result: dist-info installed, module not available
```

**Verification:**
```bash
python -c "import youtube_mcp_server"
# ModuleNotFoundError: No module named 'youtube_mcp_server'
```

**Root cause:** PyPI wheel for `youtube-mcp-server 0.1.0` installs dist-info only — no Python module files. Package is malformed at distribution level.

**Verdict: BROKEN — module files missing from wheel.**

### Cleanup

```bash
npm uninstall -g zubeid-youtube-mcp-server  # removed 122 packages
pip uninstall -y youtube-mcp-server          # uninstalled
```

**Final verdict for YouTube MCP tools: SKIP.** Both tested options (ZubeidHendricks npm + DannySubsense pip) are broken. The existing `yt-dlp.exe` handles transcript extraction without API quota. No YouTube MCP server is needed.

---

## Step 5: Windsor AI YouTube Analytics MCP (EVALUATE tier — Plan 02)

### Research Findings

Windsor AI is a cloud-based analytics connector, not an installable MCP server. No npm or pip package exists:

```bash
npm show windsor-ai         # 404 Not Found
npm show @windsor.ai/mcp    # 404 Not Found
npm show windsor-mcp        # 404 Not Found
```

The Windsor AI integration requires:
1. Browser-based OAuth flow at windsor.ai
2. Connecting YouTube Analytics account
3. Using their proprietary dashboard — not a Claude Code MCP server

**Data overlap with existing tools:** Windsor AI provides channel metrics, video performance, traffic sources, audience demographics. The existing `tools/youtube_analytics/` provides identical data via OAuth (already authenticated). `tools/youtube_analytics/analyze.py` pulls per-video analytics. `tools/youtube_analytics/performance.py` handles historical tracking.

**UX delta assessment:** Windsor offers natural language queries ("top 5 videos last month") but this pattern is already achievable by asking Claude Code to query the analytics DB directly. No standalone MCP package = no Claude Code integration path.

**Verdict: SKIP.** No installable MCP package. Cloud-only OAuth connector. Data coverage is identical to existing `tools/youtube_analytics/`. No additive value over running analytics tools in-session.

---

*Log updated: 2026-03-15 — EVALUATE tier testing complete. ZubeidHendricks + DannySubsense both broken; Windsor AI has no MCP package. All three removed/not installed.*
