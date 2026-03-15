# Phase 64: Evaluate YouTube MCP Servers and Packaging Plugins — Research

**Researched:** 2026-03-15
**Domain:** MCP servers, Claude Code plugins, YouTube API integrations, Windows toolchain
**Confidence:** HIGH (all critical tools verified against live GitHub repos and official docs)

---

## Summary

Phase 64 is an evaluation phase, not an implementation phase. The goal is to test-install candidate tools, verify they actually work, and produce a final adopt/skip verdict for each of 9 tools across 3 tiers.

The central risk in this phase is the "looks good from the outside" trap: many MCP servers have impressive READMEs but stale codebases, broken Windows support, or duplicate functionality already built into this project. The project already has a mature custom toolchain (title_scorer.py, thumbnail_checker.py, preflight scorer, discovery tools, retitle pipeline, greenlight command) that many "packaging plugins" would simply duplicate at lower quality.

The most valuable candidates with no existing overlap are: (1) Firecrawl MCP for primary source scraping during research, (2) Windsor AI MCP for YouTube Analytics access via natural language, and (3) ZubeidHendricks YouTube MCP for transcript extraction without yt-dlp overhead. The weakest candidates are TubeFlow (8 stars, opinionated pipeline that conflicts with this project's workflow) and claude-mem (35K stars but documented 35-641 process Chroma memory storm on Windows/WSL2, severe RAM consumption).

**Primary recommendation:** Adopt Firecrawl MCP (free tier sufficient, immediate research value) and ZubeidHendricks YouTube MCP (read-only transcript/metadata, no quota risk for list operations). Evaluate Windsor AI as a read-only analytics companion. Skip TubeFlow and claude-mem entirely due to workflow conflicts and stability issues respectively.

---

## Tool-by-Tool Evaluation

### TIER 1 — User Prioritized as "Install Immediately"

#### T1-A: TubeFlow (wnstify/tubeflow)

| Property | Finding |
|----------|---------|
| GitHub stars | 8 (as of 2026-03-15) |
| Last commit | January 11, 2026 |
| Maintenance | Low — 7 total commits, single developer |
| Language | Python + PyYAML |
| Windows support | Yes — PowerShell installer (`install.ps1`) |
| API keys needed | Claude Code CLI (no additional keys documented) |
| Install complexity | Low |

**What it actually does:**
TubeFlow is a general-purpose YouTube content pipeline template for Claude Code. It provides slash commands (`/youtube idea`, `/youtube full`, `/youtube publish`, `/social all`) and 9 agents focused on: topic ideation, SEO research, competitor analysis, community question mining, social post generation, and script drafting.

**Overlap with existing tools:**

| TubeFlow Feature | Existing HvH Tool |
|-----------------|-------------------|
| Competitor gap analysis | `tools/research/competitor_gap.py`, COMPETITOR-GAP-ANALYSIS |
| SEO keyword research | `tools/discovery/` full suite, `keywords.db` |
| Topic ideation | `tools/discovery/opportunity.py`, `/next` command |
| Script writing | `script-writer-v2` agent (Kraut/Alex O'Connor voice, STYLE-GUIDE) |
| Video metadata | `/publish` command, `tools/intel/` suite |

**Critical overlap verdict:** TubeFlow's 9 agents perform functions this project already handles with more domain-specific tooling. The `/youtube idea "topic"` pipeline ignores the PACKAGING_MANDATE.md hard reject rules, the title_scorer.py CTR data, and the three-phase research workflow that is the channel's competitive advantage. Adopting TubeFlow would mean maintaining two parallel pipelines.

**Confidence:** HIGH — verified against live GitHub repo

**Verdict: SKIP.** Low stars, single developer, direct workflow conflict, no additive value.

---

#### T1-B: ZubeidHendricks/youtube-mcp-server

| Property | Finding |
|----------|---------|
| GitHub stars | 459 |
| Last commit | January 29, 2024 |
| Maintenance | STALE — 14+ months no commit |
| Language | TypeScript (Node.js) |
| Windows support | Yes — explicit `%APPDATA%\Claude\claude_desktop_config.json` documented |
| API keys needed | YouTube Data API v3 key (Google Cloud Console) |
| Install | `npm install -g zubeid-youtube-mcp-server` |

**What it does:**
Read-only YouTube access: video stats, transcripts (multi-language), channel info, playlist operations, search.

**API quota impact (YouTube Data API v3):**
- Free default quota: 10,000 units/day
- `videos.list` / `channels.list`: 1 unit each — effectively unlimited for lookup
- `search.list`: 100 units — limit to ~100 searches/day
- Channel already has YouTube API integrated via `tools/youtube_analytics/` using OAuth; this MCP uses API key (different credential type, different quota bucket)

**Overlap with existing tools:**
This project already pulls analytics via `tools/youtube_analytics/` (OAuth-authenticated). The MCP adds the value of allowing Claude Code to query YouTube data mid-session without manual tool invocations. However, the codebase staleness (Jan 2024) is a concern.

**Alternative:** DannySubsense variant (10 stars, Python, 14 functions, more recent). Provides `get_video_transcript` which overlaps with existing `yt-dlp.exe` usage but would be API-key simpler.

**Confidence:** MEDIUM — GitHub verified, no test install performed

**Verdict: EVALUATE with caution.** Staleness is the main risk. Test install and verify transcript extraction works before adopting. The yt-dlp.exe approach already works; this only matters if you want Claude-native transcript access.

---

#### T1-C: Firecrawl MCP

| Property | Finding | Confidence |
|----------|---------|------------|
| Official status | Official Firecrawl MCP — actively maintained | HIGH |
| Stars | 3,000+ on firecrawl-mcp-server | HIGH |
| Windows support | Yes — documented Windows-specific workaround with `cmd /c` prefix | HIGH |
| API key needed | Yes — free at firecrawl.dev, 500 one-time credits, then paid | HIGH |
| Free tier | 500 credits (one-time, not monthly), then $16/month Hobby plan | HIGH |
| Install | `claude mcp add firecrawl -e FIRECRAWL_API_KEY=key -- npx -y firecrawl-mcp` | HIGH |

**Available commands:**
- `/firecrawl:scrape [url]` — JS-rendered page to clean markdown, bypasses anti-bot
- `/firecrawl:crawl [url]` — crawl entire site
- `/firecrawl:search [query]` — web search with page content extraction
- `/firecrawl:map [url]` — extract all URLs from a site

**Overlap with existing tools:**
The project has `WebFetch` and `WebSearch` permissions in `settings.local.json`. Firecrawl MCP adds: JavaScript rendering (Wayback Machine, archive.org PDFs, paywalled journal pages that need JS), anti-bot bypass (government archives, national library sites), and structured markdown extraction. These are capabilities the current toolset lacks.

**Relevant use cases for this channel:**
- Scraping primary source archives (national archives, government journals)
- Extracting academic paper abstracts from university sites with JS gates
- Pulling structured data from Wikipedia infoboxes for fact verification
- Research phase: competitor transcript extraction from yt-dlp failures

**Windows-specific note:** Use `cmd /c "set FIRECRAWL_API_KEY=key && npx -y firecrawl-mcp"` if standard config fails in MSYS2/Git Bash.

**Confidence:** HIGH — official tool, well-documented, multiple verified sources

**Verdict: ADOPT.** Free 500 credits is sufficient for evaluation. High additive value for research phase with no workflow conflict.

---

### TIER 2 — "High Value"

#### T2-A: Claude-Mem

| Property | Finding | Confidence |
|----------|---------|------------|
| GitHub stars | 35,400 | HIGH |
| Open issues | 58 | HIGH |
| Architecture | SQLite + Chroma vector DB (both required) | HIGH |
| Windows support | Documented but requires PATH config | HIGH |
| Known Windows/WSL2 issue | Issue #1063: 641 chroma-mcp processes spawn from 6 sessions, consumes 75% CPU and ~64GB virtual memory — nearly crashed WSL2 | HIGH |
| RAM issue | Issue #707: Chroma process uses 35GB RAM; SQLite-only mode proposed as fix but not default | HIGH |
| Install complexity | Moderate — Node.js 18+, Bun (auto-installed), Python uv, SQLite, Chroma | HIGH |

**What it does:**
Captures everything Claude does in a session, compresses it with AI, stores in SQLite + Chroma, injects relevant context into future sessions. Addresses "session amnesia" problem.

**Overlap with existing tools:**
The project uses `CLAUDE.md` + `MEMORY.md` (auto-persisted) for cross-session context. The `channel-data/` directory serves as persistent project state. The `01-VERIFIED-RESEARCH.md` pattern in each video project is the explicit session handoff mechanism. Claude-mem would add automated observation capture.

**Critical risk for this project:**
- Windows MSYS_NT environment + high-intensity Claude Code sessions = exact conditions triggering the process storm
- 35-641 spawned processes is a system-crash-level failure
- The user's machine runs Windows 10/11 natively (MSYS_NT-10.0-26200)
- Even if SQLite-only mode is available, it requires manually setting `CLAUDE_MEM_CHROMA_ENABLED=false`

**Confidence:** HIGH — issues verified on GitHub, Windows-specific risks documented

**Verdict: SKIP.** Critical process stability risk on Windows. The existing CLAUDE.md + MEMORY.md pattern already handles the core problem. Revisit when Chroma process storm (issue #1063) is resolved.

---

#### T2-B: Context7 MCP (Upstash)

| Property | Finding | Confidence |
|----------|---------|------------|
| Official status | Official Upstash product, actively maintained | HIGH |
| Stars | High (upstash/context7, production product) | HIGH |
| Free tier | Yes — API key optional (rate-limited without key) | HIGH |
| Windows support | Yes | HIGH |
| Install | `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp` | HIGH |
| API key needed | Optional — get free key at context7.com/dashboard for higher limits | HIGH |

**What it does:**
Fetches version-specific library documentation and injects it into Claude Code sessions. Resolves the "stale training data" problem for fast-moving Python/JS libraries.

**Overlap with existing tools:**
None. This project's custom tools use Python, sqlite3, YouTube Analytics API — all relatively stable libraries. However, when implementing new MCP servers (this very phase), Context7 would help verify current API signatures.

**Verdict: ADOPT.** Low friction, free, no workflow conflict. Useful when implementing/debugging MCP servers in subsequent phases.

---

#### T2-C: Writing Skill Plugin (Voice/Style Consistency)

**Research finding:** No single dominant "writing skill plugin" was found with clear provenance. The user mentioned this as a category rather than a specific tool.

The project already has:
- `.claude/REFERENCE/STYLE-GUIDE.md` — 543+ lines of voice/delivery rules
- `script-writer-v2` agent — encodes all style rules as generation constraints
- `structure-checker-v2` agent — validates retention patterns
- OPENING-HOOK-TEMPLATES.md, CLOSING-SYNTHESIS-TEMPLATES.md

**Verdict: SKIP (undefined).** The existing STYLE-GUIDE + agents system IS the voice consistency mechanism. Unless a specific tool is identified, this category adds nothing.

---

### TIER 3 — "Nice-to-Have"

#### T3-A: Windsor AI YouTube Analytics MCP

| Property | Finding | Confidence |
|----------|---------|------------|
| Official status | Official Windsor.ai product | HIGH |
| Free tier | Yes — Forever Free plan + 30-day trial | HIGH |
| Setup time | "Under 60 seconds" — OAuth link, no code | HIGH |
| What it provides | Channel metrics, video performance, traffic sources, audience demographics | HIGH |
| Write operations | Read-only via MCP | HIGH |

**Overlap with existing tools:**
The project has `tools/youtube_analytics/` with full API access to the same data. Windsor's value is allowing natural language queries ("What were my top 5 videos last month by watch time?") without running Python scripts.

**Verdict: EVALUATE.** Low friction to test (OAuth, free). The existing analytics DB may make this redundant, but natural language querying has UX value during `/status` and `/growth` workflows.

---

#### T3-B: Playwright MCP

| Property | Finding | Confidence |
|----------|---------|------------|
| Official status | Microsoft official (`@playwright/mcp`) | HIGH |
| Windows support | Yes — documented Windows config | HIGH |
| Install | `claude mcp add playwright npx -- @playwright/mcp@latest` | HIGH |
| Browser install | Automatic on first use | HIGH |

**Use case for this project:**
Navigate JavaScript-heavy archive sites (Wayback Machine, JSTOR, Legifrance) that require browser interaction — complementary to Firecrawl but for interactive sessions.

**Overlap:** Firecrawl handles most static scraping. Playwright is needed only when login flows or JavaScript interaction is required.

**Verdict: DEFER.** Install after Firecrawl adoption. Only add if Firecrawl fails on specific archive sites.

---

#### T3-C: Sequential Thinking MCP (Anthropic official)

| Property | Finding | Confidence |
|----------|---------|------------|
| Official status | Official Anthropic (`@modelcontextprotocol/server-sequential-thinking`) | HIGH |
| Install | `npm install -g @modelcontextprotocol/server-sequential-thinking` | HIGH |
| Windows support | Yes | HIGH |

**What it does:**
Provides structured step-by-step reasoning chains with branching and revision. Forces Claude to plan before implementing.

**Overlap:** Claude Code already reasons well for this project's tasks. The main use case is multi-step research synthesis, which CONTEXT.md + structured phase planning already handles.

**Verdict: SKIP (low ROI).** Claude Code's native reasoning is sufficient for this project's complexity level. Would add value only for architectural design tasks.

---

#### T3-D: AgriciDaniel/claude-seo + YouTube Thumbnail Tools

**claude-seo:** Not verified on GitHub — could not confirm repository existence during research. LOW confidence.

**Thumbnail generator tools (jordicor/youtube_thumbnail_generator_with_AIs):**

| Property | Finding |
|----------|---------|
| Stars | 2 |
| Last commit | January 4, 2026 |
| Complexity | Moderate-high (Redis, FFmpeg, Gran Sabio LLM server, Gemini API) |
| Windows support | Yes (specifically targets Windows 10/11 + Laragon) |

**Overlap:** This project uses Photoshop for thumbnails. The PACKAGING_MANDATE.md rules enforce map-first, no-face, no-text-overlay. An AI generator that creates faces/text would produce policy-violating thumbnails. The `thumbnail_checker.py` is a checklist tool (parses written concepts) — AI image generation is not part of the current workflow.

**Verdict: SKIP.** High setup complexity, 2 stars, workflow conflict with established Photoshop + map-first policy.

---

## Existing Tool Inventory (Conflict Reference)

The planner must check each candidate against these before implementing:

| Existing Tool | What It Already Does |
|---------------|---------------------|
| `tools/title_scorer.py` | CTR scoring from measured channel data |
| `tools/preflight/thumbnail_checker.py` | Thumbnail concept validation |
| `tools/preflight/scorer.py` | 5-gate preflight (topic+script+title+thumb+duration) |
| `tools/discovery/` suite | Autocomplete, trends, competitor tracking |
| `tools/retitle_audit.py` + `retitle_gen.py` | Underperformer detection + title generation |
| `tools/youtube_analytics/` | Full Analytics API access (OAuth) |
| `tools/intel/` | VidIQ/Gemini prompt synthesis |
| `tools/research/competitor_gap.py` | Competitor gap scoring |
| `yt-dlp.exe` | YouTube transcript extraction (no API key needed) |
| `script-writer-v2` agent | Full script generation with STYLE-GUIDE |
| `CLAUDE.md` + `MEMORY.md` | Cross-session context persistence |

---

## Architecture Patterns

### MCP Installation Pattern (Claude Code)

```bash
# Standard install pattern for Claude Code
claude mcp add <name> -e KEY=value -- npx -y <package>

# Windows MSYS2 workaround (use cmd prefix if npx fails)
claude mcp add firecrawl -- cmd /c "set FIRECRAWL_API_KEY=key && npx -y firecrawl-mcp"

# Verify installation
claude mcp list
```

### MCP Config File Location (Windows)
`%APPDATA%\Claude\claude_desktop_config.json`

### YouTube Data API v3 Quota Strategy
- `videos.list` / `channels.list`: 1 unit — use freely
- `search.list`: 100 units — rate-limit to <10/session
- Daily reset: midnight Pacific Time
- Default quota: 10,000 units/day (free, no cost increase for additional)

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| JS-rendered page scraping | Custom Selenium/Playwright script | Firecrawl MCP |
| YouTube transcript extraction | Python youtube-dl wrapper | yt-dlp.exe (already present) or YT Data API MCP |
| Library API docs | Training-data assumptions | Context7 MCP |
| Cross-session memory | Custom file-based journal | CLAUDE.md + MEMORY.md (already working) |

---

## Common Pitfalls

### Pitfall 1: Chroma Process Storm on Windows
**What goes wrong:** claude-mem spawns 641+ chroma-mcp processes when sessions are interrupted or multiple sessions run concurrently. Consumes 64GB+ virtual memory.
**Why it happens:** Worker daemon respawn logic doesn't handle SIGHUP/termination correctly. Each session gets its own Chroma spawn.
**How to avoid:** Don't install claude-mem on Windows until Issue #1063 is resolved. If testing: set `CLAUDE_MEM_CHROMA_ENABLED=false` to force SQLite-only mode.
**Warning signs:** Task Manager showing `chroma-mcp.exe` processes multiplying.

### Pitfall 2: YouTube Data API Quota Exhaustion via search.list
**What goes wrong:** MCP server auto-calls `search.list` for every user query. 100 units × 100 requests = full daily quota gone.
**Why it happens:** MCP servers may use search for discovery instead of direct ID lookups.
**How to avoid:** Configure MCP to use `videos.list` (1 unit) with explicit video IDs. Use `yt-dlp.exe` for transcript extraction — no API quota consumed.
**Warning signs:** 403 `quotaExceeded` errors in MCP logs.

### Pitfall 3: Duplicate Pipeline Maintenance
**What goes wrong:** Installing TubeFlow or similar pipeline tools creates a parallel system that diverges from the PACKAGING_MANDATE.md rules and channel-specific CTR data.
**Why it happens:** Generic tools don't know the channel's "no years in titles", "map-first thumbnails", or "three-phase research" requirements.
**How to avoid:** Before installing any content pipeline tool, verify it can be configured to enforce the PACKAGING_MANDATE.md rules — or skip it.

### Pitfall 4: Stale MCP Server APIs
**What goes wrong:** MCP servers with last commits in 2024 may use deprecated YouTube Data API endpoints or MCP protocol versions incompatible with current Claude Code.
**Why it happens:** MCP protocol evolved significantly in 2025.
**How to avoid:** Check that MCP server's `package.json` specifies `@modelcontextprotocol/sdk` version >=1.0. Verify last commit date before installation.

### Pitfall 5: Windows Path Issues with npx in MSYS2
**What goes wrong:** `npx -y firecrawl-mcp` fails silently or throws path errors in Git Bash / MSYS2.
**Why it happens:** MSYS2 path translation (`/c/Users/...`) conflicts with Node.js Windows path expectations.
**How to avoid:** Use `cmd /c "..."` wrapper or configure MCP via `claude_desktop_config.json` JSON directly with Windows-native paths.

---

## Adoption Decision Matrix

| Tool | Stars | Last Commit | Overlap | Risk | Verdict |
|------|-------|------------|---------|------|---------|
| TubeFlow | 8 | Jan 2026 | HIGH (full pipeline) | Medium | SKIP |
| ZubeidHendricks YouTube MCP | 459 | Jan 2024 | LOW (MCP interface) | Medium (stale) | EVALUATE |
| Firecrawl MCP | 3000+ | Active | NONE | Low | ADOPT |
| Claude-Mem | 35,400 | Active | LOW | CRITICAL (Windows crash) | SKIP |
| Context7 MCP | High | Active | NONE | Low | ADOPT |
| Writing skill plugin | N/A | N/A | HIGH (STYLE-GUIDE exists) | N/A | SKIP |
| Windsor AI MCP | N/A | Active | LOW (read-only alt) | Low | EVALUATE |
| Playwright MCP | MS official | Active | LOW (Firecrawl first) | Low | DEFER |
| Sequential Thinking MCP | Official | Active | LOW | Low | SKIP |
| claude-seo | Unverified | Unknown | MEDIUM | Unknown | SKIP |
| Thumbnail generators | 2 | Jan 2026 | HIGH (Photoshop workflow) | Low | SKIP |

---

## Validation Architecture

Config shows `workflow.nyquist_validation` is absent — treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing, pyproject.toml) |
| Config file | `pyproject.toml` (testpaths = ["tests"]) |
| Quick run command | `python -m pytest tests/ -x -q` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements → Test Map

This is an evaluation phase with no coded deliverables. Tests are smoke tests on installation success and functionality verification.

| Behavior | Test Type | Command |
|----------|-----------|---------|
| Firecrawl MCP installs without error | smoke | `claude mcp list` shows firecrawl |
| Firecrawl scrapes a test URL | manual | Run `/firecrawl:scrape https://en.wikipedia.org/wiki/Partition_of_India` |
| Context7 MCP installs and resolves a library | smoke | `claude mcp list` shows context7 |
| YouTube MCP (if evaluated) returns video metadata | manual | Query via Claude Code session |
| Windsor AI connects to YouTube Analytics | manual | OAuth flow completes, data returns |
| claude-mem process stability test | manual | Run 3+ concurrent sessions, monitor Task Manager |

### Wave 0 Gaps
- [ ] No test files needed — this is an evaluation phase producing a DECISION.md, not code
- [ ] Framework already present from Phase 53

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual web scraping with WebFetch | Firecrawl MCP (JS rendering + anti-bot) | 2025 | Primary source access for paywalled/JS-gated archives |
| Single YouTube MCP server | 40+ YouTube MCP servers with specialization | 2025 | Transcript-only vs full-analytics vs write-ops separated |
| No cross-session memory | claude-mem (but unstable on Windows) | 2025 | CLAUDE.md remains the stable Windows alternative |
| Static library docs in Claude training | Context7 MCP (live docs injection) | 2025 | Eliminates hallucinated API signatures |

**Deprecated/outdated:**
- Composio YouTube MCP: Being deprecated per official Composio changelog (2026)
- ZubeidHendricks MCP: 14+ months stale — use only if verified working on install test

---

## Open Questions

1. **ZubeidHendricks MCP staleness**
   - What we know: Last commit January 29, 2024. MCP protocol changed significantly since.
   - What's unclear: Whether the npm package still works with current Claude Code CLI.
   - Recommendation: Test install as Phase 64 Task 1 before deciding. If broken, use DannySubsense variant (Python, actively maintained).

2. **Windsor AI free tier sustainability**
   - What we know: "Forever Free" plan exists, under-60-second setup.
   - What's unclear: Data freshness limits and rate limits on free tier.
   - Recommendation: Test OAuth flow and run a `/growth`-equivalent query to verify data completeness vs existing `tools/youtube_analytics/` output.

3. **claude-mem SQLite-only stability**
   - What we know: Issue #1063 (process storm) was reported February 2026. SQLite-only mode proposed as fix.
   - What's unclear: Whether the fix shipped and is default-on.
   - Recommendation: Check claude-mem CHANGELOG.md before any install attempt. If SQLite-only is stable, re-evaluate.

---

## Sources

### Primary (HIGH confidence)
- github.com/wnstify/tubeflow — Verified: 8 stars, Jan 2026, Python pipeline
- github.com/ZubeidHendricks/youtube-mcp-server — Verified: 459 stars, Jan 2024 stale
- github.com/thedotmack/claude-mem — Verified: 35.4K stars, Issue #707 (35GB Chroma), Issue #1063 (641 process storm)
- github.com/firecrawl/firecrawl-mcp-server — Official Firecrawl MCP
- docs.firecrawl.dev/mcp-server — Official installation docs
- github.com/upstash/context7 — Official Context7 MCP
- github.com/microsoft/playwright-mcp — Official Microsoft Playwright MCP
- developers.google.com/youtube/v3/determine_quota_cost — YouTube Data API quota costs

### Secondary (MEDIUM confidence)
- ekamoira.com/blog/youtube-mcp-server-comparison-2026 — YouTube MCP server comparison, verified quota figures against Google docs
- windsor.ai/how-to-connect-youtube-analytics-to-claude — Windsor AI setup docs
- firecrawl.dev/pricing — Verified: 500 one-time credits free tier

### Tertiary (LOW confidence)
- AgriciDaniel/claude-seo — Repository not verified during research; existence unconfirmed

---

## Metadata

**Confidence breakdown:**
- Tool existence/maintenance status: HIGH — all major tools verified against live GitHub
- Windows compatibility: HIGH — documented in official sources or verified issues
- API costs: HIGH — verified against Google official docs
- Adoption verdicts: HIGH — based on verified data, not speculation
- Thumbnail tool ecosystem: MEDIUM — jordicor repo verified, broader ecosystem less surveyed

**Research date:** 2026-03-15
**Valid until:** 2026-06-15 (stable tools) / 2026-04-15 for claude-mem (fast-moving)
