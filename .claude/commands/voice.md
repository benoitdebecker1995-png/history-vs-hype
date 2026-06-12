---
description: Voice work — one command, three modes. grill (recurring calibration, default) · discover (full bootstrap) · tooling (build/extend linter). Sharpens the creator's canonical voice profile.
model: opus
---

# /voice — the single entry for all voice work

Dispatches to one of three mode-playbooks by the first arg. **Default mode = `grill`** (the recurring loop). Consolidated from three separate slash-commands into one `/voice` on 2026-06-07.

| Invocation | Mode | When | Playbook |
|---|---|---|---|
| `/voice grill` (or bare `/voice`) | **grill** | recurring — a script has off beats or an open queue | `.claude/REFERENCE/voice-modes/grill.md` |
| `/voice discover` | **discover** | rare — first bootstrap, or the drift sensor fired | `.claude/REFERENCE/voice-modes/discovery.md` |
| `/voice tooling` | **tooling** | rare — build/extend the linter & few-shot exemplars | `.claude/REFERENCE/voice-modes/tooling.md` |

## Dispatch
1. Parse the first token of the args as the mode (`grill` | `discover` | `tooling`). No arg → `grill`. Unrecognized → ask which mode (one `AskUserQuestion`).
2. **Read the matching playbook in full and follow it.** The playbooks are the detailed instructions; this file is only the router.
3. Pass any remaining args (e.g. a project slug) through to the playbook.

## Shared invariants (every mode obeys)
- **Canonical artifact = `.claude/REFERENCE/VOICE-PROFILE.md`** — the ONE home for voice rules. Topic-specific rules stage in its "Pending / topic-specific (un-promoted)" section and promote into the body only after recurring across ≥2 topics (the generality gate).
- **His LIVE picks are ground truth** — a pick that contradicts the profile rewrites the profile.
- **Concrete line options in CHAT for line drills — never the truncating `AskUserQuestion` box.**
- **Update the profile inline; DO NOT COMMIT; voice only** (preserve `[SOURCE]`/`[SHOW]`/`[NLM]` tags + verbatim quotes; NotebookLM for phrasing, never fabricate).
- **Lock-state gate:** edit `SCRIPT.md` only when unlocked; on a locked script (read-aloud done / teleprompter exists) → **profile-only mode** ([[feedback-teleprompter-after-lock]]).

## How the modes relate
`grill` sharpens the profile incrementally and logs ROT13 prediction hit-rate; when that hit-rate craters (or a new format/corpus appears), it triggers `discover` (full re-bootstrap). `tooling` is mostly spent (linter `tools/voice_lint.py` + exemplars built 2026-06-05) — re-run only to extend detection.
