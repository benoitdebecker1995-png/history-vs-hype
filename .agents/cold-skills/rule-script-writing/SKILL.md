---
name: rule-script-writing
description: "Voice, structure and language rules for every script in this repo — Calm Prosecutor register, the turn point, language to avoid, voice linting. Use when: opening, writing or editing SCRIPT.md, any *SCRIPT-DRAFT.md, FINAL-SCRIPT.md or 02-SCRIPT-*.md; drafting or revising any spoken line; or before running the script or polish workflows. Load it BEFORE writing, not after. Does NOT cover research filing (→ rule-research-verification) or titles and thumbnails (→ rule-packaging)."
---

> **Codex note.** Port of `.claude/rules/script-writing.md`, which stays canonical. On Claude Code
> this loads automatically whenever a script file is opened. Codex has no glob-scoped auto-load, so
> **load this yourself before touching a script** — a missed trigger means the voice rules silently
> don't apply. Governs: `**/SCRIPT.md`, `**/*SCRIPT-DRAFT.md`, `**/FINAL-SCRIPT.md`,
> `**/02-SCRIPT-*.md`.

# Script writing

**Authoritative reference:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — READ BEFORE WRITING ANY SCRIPT (PARTS 1-5 script-side).

**Voice:** "Calm Prosecutor" — emotionally low, intellectually high. Evidence-based referee.

**Key rules:** Real quotes with page numbers | Primary sources ON SCREEN | Define every term immediately | Contractions ("it's" not "it is") | Dates spoken ("On June 16th, 2014") | "Here's" max 2-4/script

**Structure:** Myth-first for non-territorial (30.3% vs 22.4% retention) | Turn at 15-25% runtime (3.2x, not 25-35% dead zone at 2.1x) | Modern relevance every 90s | Pattern interrupt every 2-3 min | Deep causal chains throughout

**Language to avoid:** "X is occupying Y" | "Z destroyed the culture" | absolutist language | conspiracy framing without documentation

**Templates:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`

**Write for spoken delivery** — contractions, natural phrasing. Deep causal chains: explain WHY with
spoken-register connectors (so, which is why, and that meant); formal "consequently/thereby" sparingly.

**Script from verified facts ONLY.** If a fact isn't in `01-VERIFIED-RESEARCH.md`, STOP and verify
first — see the `rule-research-verification` skill.

**Voice linting:** `tools/voice_lint.py` mechanizes `.claude/REFERENCE/VOICE-PROFILE.md`. Rules derive
FROM the profile, never the reverse (ADR-0006). Imported generic-LLM tells ship WARN, never HARD.
