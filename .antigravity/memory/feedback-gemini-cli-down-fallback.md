---
name: Gemini CLI-down fallback — output paste-ready prompt, never silently re-route
description: When /gemini CLI fails or is unavailable, output a ready-to-paste prompt block for the user to run manually in Gemini's web UI instead of swapping to WebSearch or skipping the step
type: feedback
originSessionId: 04df0fee-bea6-4c35-9712-7ddaa2df6a0a
---
When a workflow step is routed to Gemini (per `feedback-gemini-model-default.md` and `~/.claude/wiki/preferences/tooling.md`) and the `/gemini` CLI fails, errors, or isn't available in the current environment, **do not silently fall back to WebSearch, Sonnet, Opus, or skip the step.**

Instead, output a ready-to-paste prompt block for the user to run manually in Gemini's web UI (gemini.google.com). Format:

```
=== PASTE INTO GEMINI (Flash) ===
[model: gemini-2.5-flash]
[task: <one-line description>]
[sources: <URLs or file paths the user needs to attach>]

<full prompt text>
=================================
```

User pastes, copies Gemini's reply back into the session, and the work item proceeds.

**Why:** The routing logic in `model-selection.md` and the Gemini-default rule exist for specific reasons — bulk reads should not burn Opus/Sonnet tokens, and WebSearch is not a substitute for source-grounded reading. Silent re-routing breaks the cost-discipline and quality-discipline that the model-routing rules enforce. The manual paste path preserves both even when automation is unavailable.

**How to apply:**
- Triggers: `/gemini` invocation fails OR Gemini CLI not installed OR network/auth error
- Default model in the paste block: `gemini-2.5-flash` unless the work item explicitly requires Pro
- Include any source URLs or file paths the user needs to attach to the Gemini session
- The prompt must be self-contained (user copy-pastes one block; no additional context required)
- Wait for user to paste Gemini's reply before proceeding to the next step

**When NOT to apply:** If the work item was originally fine to route through WebSearch (e.g., a single-page lookup, not a bulk read), proceed with WebSearch — this rule applies only to genuinely Gemini-routed work that the routing matrix sends there for a reason (bulk reads, scholarly source ingestion, multi-source synthesis).

**Origin:** 2026-05-12 — established during Video #56 (Asmongold/Destiny slavery clip) planning. User flagged that delegation matrix only works if Gemini-routed steps have a defined fallback when CLI is down.
