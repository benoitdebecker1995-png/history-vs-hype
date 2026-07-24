# VidIQ MCP — setup + usage (enrichment evaluator, NEVER a gate)

> **Full tool map:** `docs/VIDIQ-MCP-CAPABILITY-MAP.md` classes every one of the ~55 live tools
> WIRE / GUARDED / REJECT. **Authority:** ADR-0013 (scope + competitor source-of-truth), ADR-0012
> (packaging lock). This file is setup/auth + how it's wired; the map is the inventory.

The official VidIQ MCP server gives Claude access to VidIQ's YouTube data. VidIQ has **no public REST API** — this MCP is the only way to automate what was previously done by pasting prompts into the VidIQ app. The **research/scoring** surface is effectively read-only; the server ALSO exposes a **generation suite** (AI video/voiceover/b-roll/thumbnails/motion-graphics) and one competitor **write** (`vidiq_update_competitors`) — see the identity-guard section below.

## Identity guard — the generation suite is fenced off

The live server can *generate* assets (`vidiq_generate_video`, `_broll`, `_clips`, `_thumbnail`, `_titles`, `vidiq_voiceover_*`, `vidiq_compose`). **All REJECT** for on-channel use: AI-fabricated sources, figures, footage, or narrator voice contradict the channel's identity ("primary sources on screen") and remove the read-aloud QA gate ([[feedback-read-aloud-catches-logic]]). `vidiq_motion_graphics` is a narrow GUARDED exception (non-figurative kinetic text only; prefer the in-repo HTML-deck b-roll pipeline). Using any generation tool on-channel requires a new ADR. The scorers (`vidiq_score_title/_thumbnail`) stay GUARDED enrichment — clickbait-guarded, never a decider.

## Why it's positioned BELOW the channel's own gates

VidIQ's own tool list includes **"title/thumbnail scoring"** — the exact kind of confident number ("VidIQ 95/100") that displaced the CTR audit on #62. And VidIQ tends toward clickbait suggestions. So the rule is hard:

- **VidIQ output is ENRICHMENT, never a FILTER.** It lands on the `ENRICHMENT` line of the packaging lock (`tools/preflight/packaging_lock.py`) and **cannot override a filter FAIL**.
- **Clickbait guard:** if a VidIQ title suggestion trips the `title_scorer` brand gate (`detect_clickbait` / `hard_rejects`) or the CTR kill-list, it's **rejected and logged**, not adopted.
- **Per-variant CTR still comes from post-publish Studio files**, not VidIQ (the MCP is read-only *channel* data, not native Test & Compare).
- Use VidIQ for what we have **no tool for**: competitor/trend research and the **"Video Watch"** retention diagnostic. Do NOT use its title score as a decision.

## Setup (one-time, needs the user's OAuth)

**Claude Code:**
```bash
claude mcp add --transport http vidiq https://mcp.vidiq.com/mcp
# then complete the OAuth login in the browser window that opens
```
**claude.ai / Desktop:** Settings → Connectors → Add Custom Connector → `https://mcp.vidiq.com/mcp` → Connect → authenticate with your vidIQ account.

- Auth: OAuth 2.0 (your vidIQ password is never shared). Claude and vidIQ emails need not match.
- Read-only: cannot post, edit metadata, or change settings.

## Plan / credits

- Available on all plans (Free / **Boost** / Max). **User is on Boost** → credit headroom for gate-time calls **plus** ad-hoc use during research.
- Credit cost: **5 credits** per standard call (channel research, competitor analysis, title/thumbnail scoring, comment sentiment, trend discovery); **10 credits** for **"Video Watch"** (frame-by-frame retention diagnostics). Free utility calls: credit balance, connected channels, trend categories.
- Credits refresh at the start of each billing cycle. If out of credits or the MCP is down → **fall back to manual in-app VidIQ** (paste-ready prompts).

## Where it's wired

- **`/greenlight --full`** (+ ad-hoc in research) — `vidiq_outliers` (competitor breakout mining, feeds Step 0D) + `vidiq_keyword_research` (demand enrichment, Step 1) + competitor/trend research feed Step 0; any title/thumbnail score goes to the packaging-lock ENRICHMENT line only. **Never on quick checks.**
- **`/retitle`** — the "Video Watch" retention diagnostic on underperformers + an enrichment column on swap candidates (never the decider; `title_scorer` + live CTR stay authoritative).
- **Competitor set** — `tools/intel/vidiq_competitor_sync.py` mirrors `tools/intel/competitor_channels.json` (`style-match` + `broad-history` tiers) into VidIQ's tracked competitors via `vidiq_update_competitors`. Repo = source of truth; re-run by hand when the repo set changes (ADR-0013).

## Tool surface

Research/scoring (effectively read-only): channel & competitor analysis · `vidiq_outliers` breakout mining · `vidiq_keyword_research` · video/reel performance · title & thumbnail scoring (advisory only) · comment sentiment · trend discovery · Instagram creator audits (public) · **Video Watch** (retention, 10cr) · utility (0cr). **Write:** `vidiq_update_competitors` (competitor sync). **Generation suite (REJECT — identity guard):** AI video/voiceover/b-roll/thumbnail/titles/compose. Full per-tool verdicts: `docs/VIDIQ-MCP-CAPABILITY-MAP.md`.
