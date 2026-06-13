# Command / Skill / Agent Audit — 2026-06

> **UPGRADE-PLAN W1.** Inventory + usage signal + overlap shortlist. **No merges or retirements executed** — the user picks from § Shortlist (grill-locked: audit-report first). W2 records decisions in the § Decision log. W3 (routine health) may append its table here.

## Method + caveats (read before trusting numbers)

- **Invocations** = count across the 164 retained session logs in `~/.claude/projects/D--History-vs-Hype/*.jsonl` (~220 MB), summing `<command-name>` tags + `Skill` tool calls + `subagent_type` spawns. **These UNDERCOUNT real usage**: logs rotate, and much of the workflow fires via natural language ("I uploaded X" → /reconcile, "script locked" → calibration mine) or inside other commands without a logged invocation tag. Zero invocations ≠ dead — it means *no direct invocation in retained logs*.
- **Inbound refs** = number of files under `.claude/`, `CLAUDE.md`, `docs/`, `tools/` mentioning `/name` or `name.md` (excluding self). **Common-word names are inflated** (`patterns` 72, `historian` 155, `analyze` 30, `status` 24 match prose, not just the command). Distinctive names are accurate.
- **Reads** = distinct `.claude/REFERENCE|templates|skills|agents`, `memory/*.md`, `tools/*` paths the file instructs to read — a proxy for total context cost beyond its own size.

## Commands (`.claude/commands/`, 30 active + `_DEPRECATED/`)

| Command | Size (KB) | Inbound refs | Reads | Invocations | Note |
|---|---|---|---|---|---|
| script | 55.6 | 80 | 16 | 1 | Biggest command; canonical v18 flow |
| verify | 46.8 | 28 | 9 | 4 | incl. ambiguous `verify` Skill hits (built-in /verify collision) |
| research | 41.6 | 56 | 16 | 5 | absorbed /sources 2026-05-03 |
| publish | 34.2 | 33 | 9 | 0 | |
| thumbnail | 21.1 | 30 | 3 | 3 | |
| greenlight | 18.9 | 21 | 4 | 3 | |
| prep | 18.9 | 17 | 3 | 0 | |
| retitle | 18.2 | 8 | 6 | 1 | |
| polish | 15.3 | 3 | 3 | 3 | overlap → shortlist #3 |
| analyze | 13.5 | 30* | 0 | 0 | *common-word inflation |
| opener | 12.7 | 1 | 2 | 1 | |
| learn-from-paper | 11.6 | 2 | 4 | 0 | |
| editing-guide | 10.2 | 8 | 0 | 1 | |
| translate | 10.0 | 19 | 2 | 0 | Untranslated Evidence series |
| next | 9.6 | 17 | 0 | 0 | |
| status | 9.1 | 24* | 1 | 1 | |
| engage | 8.5 | 7 | 1 | 0 | |
| reconcile | 8.3 | 10 | 5 | 4 | + NL-triggered (undercounted) |
| script-research-pass | 7.4 | 0 | 3 | 1 | overlap → shortlist #2 |
| help | 7.1 | 6 | 1 | 0 | |
| comment-mine | 6.9 | 4 | 0 | 2 | |
| refactor | 6.4 | 7 | 0 | 17 | plan executor (this plan) |
| preflight | 6.4 | 12 | 2 | 0 | |
| fix | 5.9 | 11 | 0 | 4 | |
| verify-flow-nlm | 5.6 | 1 | 1 | 2 | overlap → shortlist #2 |
| gemini | 5.4 | 18 | 0 | 2 | dispatch utility |
| patterns | 5.4 | 72* | 0 | 0 | *heavy common-word inflation |
| growth | 2.4 | 8 | 0 | 1 | overlap → shortlist #4 |
| voice | 2.5 | 13 | 5 | 4 | +1 voice-discovery +1 voice-tooling (legacy names, already folded in) |
| curiosity | 1.4 | 8 | 0 | 2 | overlap → shortlist #1 |

`_DEPRECATED/README.md`: migration table only. **Stale pointer finding:** it routes 3 old commands to `/sources`, which was itself folded into `/research` (2026-05-03) — table needs a one-line update if touched in W2.

User-level command: `wiki-ingest` (2.8 KB, 1 invocation) — wiki triage, fine standalone.

## Agents (`.claude/agents/`, 11 + 6 contracts + 1 changelog)

| Agent | Size (KB) | Inbound refs | Reads | Spawns | Note |
|---|---|---|---|---|---|
| script-writer-v2 | 154.1 | 52 | 12 | 5 | v18.0; + 20.9 KB CHANGELOG |
| structure-checker-v2 | 114.1 | 23 | 4 | 3 | Wave 12 |
| research-organizer | 57.2 | 14 | 5 | 0 | shortlist #5 |
| article-writer | 52.7 | 20 | 5 | 0 | invoked directly per CLAUDE.md; newsletter lane |
| fact-checker | 31.6 | 26* | 1 | 0 | *name matches "fact-check" prose |
| notebook-researcher | 18.7 | 3 | 3 | 3 | NLM MCP lane, active |
| claims-extractor | 15.7 | 8 | 0 | 0 | shortlist #6 |
| diy-asset-creator | 15.1 | 9 | 0 | 0 | wired via /prep --assets |
| wiki-researcher | 12.2 | 8 | 0 | 3 | /research Step 5, active |
| thumbnail-critic | 8.3 | 3 | 5 | 0 | 2-stage thumbnail gate (gut-check first → critic only if unsure, so low spawn rate is by design) |
| competitor-gap | 8.1 | 4 | 2 | 6 | most-spawned specialist |

Built-in agent usage for scale: `general-purpose` 35, `Explore` 10.

## Skills

**Project:** `historian` — 5 files, 37.4 KB total, 8 invocations, deeply wired (/research stages A–C, stop-flags, web policy). Healthy; no action.

**User-level (relevance to this repo varies):**

| Skill | Size (KB) | Invocations | Note |
|---|---|---|---|
| grill-with-docs | 11.4 | 30 | most-used skill overall |
| graphify | 68.9 | 2 | MCP graphs do the daily work; skill = rebuild path |
| improve-codebase-architecture | 14.4 | 3 | |
| triage / to-issues / to-prd | 15.8 / 3.3 / 2.9 | 0 | issue-tracker lane documented in CLAUDE.md, unused so far |
| setup-matt-pocock-skills | 13.6 | 0 | one-shot installer, likely spent |
| diagnose | 8.5 | 0 | |
| write-a-skill | 3.2 | 0 | |
| caveman | 2.0 | 0 | |
| zoom-out | 0.4 | 0 | |

User-level files cost nothing in this repo's context until invoked; listed for completeness, not as merge candidates.

## Shortlist — merge / retire candidates (user picks; nothing executed)

1. **Fold `/curiosity` into `/greenlight`** as a scoring lens/flag. It evaluates exactly the decision /greenlight owns (title viability), is 1.4 KB, and both get invoked around the same moment. Risk: none visible. Counter-argument: it's also used ad-hoc on single titles mid-conversation, where a 1.4 KB standalone is cheaper than loading 18.9 KB of greenlight.
2. **Consolidate the deep-verification trio** — `/verify` (46.8 KB) vs `/verify-flow-nlm` (5.6 KB, self-described as "the deeper pass /verify --script skips") vs `/script-research-pass` (7.4 KB, paragraph-by-paragraph NLM + flow + polish, **0 inbound refs**). Three entry points to overlapping NLM-backed script checking. Options: (a) make verify-flow-nlm a `/verify --flow` flag and keep script-research-pass as the editor-pass; (b) merge script-research-pass and verify-flow-nlm (their NLM-query cores intersect heavily); (c) leave as-is — they were deliberately split for context economy (loading 47 KB verify.md to run a 5 KB pass is the thing the split avoids). Needs your call on which pass you actually reach for.
3. **`/polish` vs `/script --review` + voice_lint** — /polish (15.3 KB, 3 invocations) does the final AI-pattern pass; v18 flow already ends with a heavy gate + zero-feedback read-through, and voice_lint covers fingerprint checks. Question for W2: is /polish still a distinct stage in the v18 flow, or absorbed?
4. **Analytics family** — `/growth` (2.4 KB) and `/patterns` (5.4 KB) could become `/analyze --growth` / `--patterns`. Low value, low risk; mostly menu-decluttering.
5. **`research-organizer` agent (57.2 KB, 0 spawns in retained logs)** — /research's current flow spawns wiki-researcher + notebook-researcher; research-organizer's 14 inbound refs need a live-wiring check (refs may be stale docs). If nothing current spawns it: archive candidate (preserve under `.claude/_ARCHIVE/`).
6. **`claims-extractor` agent (15.7 KB, 0 spawns)** — /verify --extract territory; check whether verify.md still delegates to it or does extraction inline. If inline: archive candidate.
7. **`fact-checker` agent (31.6 KB, 0 spawns)** — same question as #6 for /verify's main path. Its 26 inbound refs are partly prose inflation ("fact-checker"/"fact-checking").

## Decision log (W2 fills this in)

*(empty — no decisions made in W1)*
