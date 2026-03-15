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

*Log updated: 2026-03-15 — Context7 + Playwright installed. Firecrawl skipped (free tier too limited).*
