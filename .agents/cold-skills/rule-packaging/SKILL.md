---
name: rule-packaging
description: "Title, thumbnail and demand rules — the graded demand gate, title penalties as scores not bans, mandatory text overlay, the collision check. Use when: opening or editing YOUTUBE-METADATA.md, any THUMBNAIL-*.md, channel-data/serp-studies/**, tools/title_scorer.py or tools/PACKAGING_MANDATE.md; generating or judging a title; designing a thumbnail; or proposing a new video. Load it BEFORE proposing packaging. Does NOT cover script voice (→ rule-script-writing)."
---

> **Codex note.** Port of `.claude/rules/packaging.md`, which stays canonical. On Claude Code this
> loads automatically whenever a packaging file is opened. Codex has no glob-scoped auto-load, so
> **load this yourself before proposing a title or thumbnail**. Governs:
> `**/YOUTUBE-METADATA.md`, `**/THUMBNAIL-*.md`, `channel-data/serp-studies/**`,
> `tools/title_scorer.py`, `tools/PACKAGING_MANDATE.md`.

# Packaging

1. **Search demand** — graded gate, NOT a hard stop: GO ≥1,000/mo · CAUTION 500–999 · STOP <500, and a **verified live news hook overrides a STOP**. Authority: `.claude/commands/greenlight.md` Step 1.
2. **Title generation** — `title_scorer.py`. Front-load keyword. Declarative = default (3.8% CTR). **Years and colons are graded penalties, not bans** — `YEAR_PENALTY -15`, `COLON_PENALTY -10`, `COLON_PENALTY_VERSUS 0` (`tools/title_scorer.py:308-313`, authoritative). The old −46%/−28% "hard rule" was topic-confounded and is **retired**; the channel's #1 and #3 videos both use colons.
3. **Thumbnail concept** — text overlay MANDATORY (87% niche), no face (0% niche), maps for territorial. `thumbnail_checker.py`
4. **THEN research** — only after the greenlight gate passes

**Text overlay on thumbnails** — 2-4 words, not the full title. Maps for territorial topics.

**Filters decide, scores inform (ADR-0012).** A rule that must bind is a filter in
`tools/preflight/packaging_lock.py` — code, not prose in a command file. Enrichment can never
upgrade a filter FAIL.

**Collision-check before proposing a video:** `python -m tools.preflight.candidate_preflight "<topic>"`.
A published match is a stop. Run it *before* the pitch, not after.

See: `tools/PACKAGING_MANDATE.md` | `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md`
