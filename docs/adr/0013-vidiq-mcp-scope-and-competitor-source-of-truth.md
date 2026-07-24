# 0013 — VidIQ MCP scope + competitor source-of-truth

**Status:** Accepted (2026-07-01)

## Context

The VidIQ MCP was reconnected and its live tool surface turned out to be ~55 tools — far larger than
the `docs/VIDIQ-MCP-SETUP.md` doc (written for a small "read-only" surface) described. It now includes
a full **generation suite** (`vidiq_generate_video`, `_broll`, `_clips`, `_thumbnail`, `_titles`,
`vidiq_voiceover_*`, `vidiq_motion_graphics`, `vidiq_compose`) that spends credits and produces assets.
Nothing in the repo governed those — a gap given the channel's identity guard ("history through primary
sources"; no AI-generated figures/footage/voice).

Separately, resolving VidIQ's 20 auto-tracked competitor IDs to names exposed that the tracked set was
**off-brand**: 3 weren't history at all (Andrei Jikh = finance, Extra Credits = video games,
CrashCourse = gen-ed), ~6 were anti-brand (Forgotten History "false flags/coverups," StormClouds,
Pyotr Kurzin geopolitics, Nutty History, War Tribe, History Abridged), and **none** of the channel's 12
documented style-peers were present. Only 2 of 20 (Kings & Generals, HistoryMarche) also appeared in the
repo's curated `tools/intel/competitor_channels.json`. Since `vidiq_outliers(channelIds=tracked)` drives
the outlier/demand signal, the standing set was mining finance + conspiracy clickbait as the channel's
"demand." The repo already held the correct set, curated and category-tagged.

Extends ADR-0012 (packaging advancement is code-gated; VidIQ is enrichment, never a gate) and ADR-0007
(pre-publish checks are filters, not predictors).

## Decision

- **VidIQ MCP is an enrichment/research surface, never a gate.** Every tool is classed WIRE / GUARDED /
  REJECT in `docs/VIDIQ-MCP-CAPABILITY-MAP.md`. Scores land on the packaging-lock ENRICHMENT line and
  are clickbait-guarded (ADR-0012).
- **The generation suite is fenced off by the identity guard.** `generate_video/_broll/_clips/
  _thumbnail/_titles`, `voiceover_*`, and `compose` are REJECT — AI-fabricated sources, figures,
  footage, or narrator voice contradict "primary sources on screen" and remove the read-aloud QA gate.
  `motion_graphics` is a narrow GUARDED exception (non-figurative kinetic text only; prefer the in-repo
  HTML-deck b-roll pipeline). Using any generation tool on-channel requires a future ADR.
- **The repo is the source of truth for competitors; VidIQ mirrors it.** `competitor_channels.json`
  (version-controlled, category-tagged) is canonical. VidIQ's tracked set = the `style-match` +
  `broad-history` tiers (18 channels); the `geopolitics` tier is excluded from the standing default
  outlier lens. Sync is a one-time write now, re-run by hand when the repo set changes — no scheduled
  routine (the set churns rarely). Tool: `tools/intel/vidiq_competitor_sync.py` +
  `vidiq_update_competitors`.

## Consequences

- **Good:** outlier/demand mining becomes trustworthy (history peers, not finance/conspiracy); the
  powerful generation tools are explicitly governed rather than silently available; the competitor set
  has one canonical home with version history.
- **Cost:** the repo↔VidIQ sync is manual — if `competitor_channels.json` changes and no one re-runs the
  sync, VidIQ drifts stale (acceptable; the set rarely changes, and drift only dulls enrichment, never
  gates anything). Revisit an auto-sync routine only if churn increases.
- **Reversible by** re-following the old channels (the pre-sync 20 IDs are recorded in the session /
  plan file), but there's no reason to — they were off-brand.

See: ADR 0012, ADR 0007, `docs/VIDIQ-MCP-CAPABILITY-MAP.md`, `docs/VIDIQ-MCP-SETUP.md`,
CONTEXT.md (Competitor set / outlier lens terms), `tools/intel/vidiq_competitor_sync.py`.
