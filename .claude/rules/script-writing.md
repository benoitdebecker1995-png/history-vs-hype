---
paths:
  - "**/SCRIPT.md"
  - "**/*SCRIPT-DRAFT.md"
  - "**/FINAL-SCRIPT.md"
  - "**/02-SCRIPT-*.md"
---

# Script writing

Loaded only when a script file is open. Moved out of CLAUDE.md 2026-07-31 — the rules are
unchanged, they just no longer cost context on sessions that never touch a script.

**Authoritative reference:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — READ BEFORE WRITING ANY SCRIPT (PARTS 1-5 script-side).

**Voice:** "Calm Prosecutor" — emotionally low, intellectually high. Evidence-based referee.

**Key rules:** Real quotes with page numbers | Primary sources ON SCREEN | Define every term immediately | Contractions ("it's" not "it is") | Dates spoken ("On June 16th, 2014") | "Here's" max 2-4/script

**Structure:** Myth-first for non-territorial (30.3% vs 22.4% retention) | Turn at 15-25% runtime (3.2x, not 25-35% dead zone at 2.1x) | Modern relevance every 90s | Pattern interrupt every 2-3 min | Deep causal chains throughout

**Language to avoid:** "X is occupying Y" | "Z destroyed the culture" | absolutist language | conspiracy framing without documentation

**Templates:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`

**Write for spoken delivery** — contractions, natural phrasing. Deep causal chains: explain WHY with
spoken-register connectors (so, which is why, and that meant); formal "consequently/thereby" sparingly.

**Script from verified facts ONLY.** If a fact isn't in `01-VERIFIED-RESEARCH.md`, STOP and verify
first — see the `research-verification` rule.

**Voice linting:** `tools/voice_lint.py` mechanizes `.claude/REFERENCE/VOICE-PROFILE.md`. Rules derive
FROM the profile, never the reverse (ADR-0006). Imported generic-LLM tells ship WARN, never HARD.
