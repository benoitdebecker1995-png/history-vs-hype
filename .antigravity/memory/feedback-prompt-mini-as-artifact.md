---
name: /prompt-mini Wants Artifact, Not Execution
description: When user invokes /prompt-mini and explicitly asks for a prompt deliverable, produce the forged prompt as a file artifact (slash command) — do NOT execute the workflow inline.
type: feedback
originSessionId: d3dc5941-267d-45b0-ac54-5e193d574584
---
When user invokes `/prompt-mini` AND the request explicitly frames the deliverable as a prompt ("give me a prompt to do X," "generate a prompt that asks me Y," "write me a prompt I can run later") — produce the FORGED PROMPT AS A FILE ARTIFACT, save it to `.claude/commands/<slug>.md` so the user can invoke it as a slash command later, and tell them where it landed.

Override prompt-mini's default "EXECUTE IT IMMEDIATELY" instruction in this case. The user is asking for a reusable artifact, not a one-shot execution.

**Why:** User pushed back twice on 2026-04-28 ("i just asked you to generate a prompt, idk why you are claling notebooklm right now"). They wanted a slash-command they could run later as part of their workflow — `/thesis-discovery` for the Socratic thesis-discipline discovery loop. Executing inline destroyed the artifact value (they'd have to re-prompt next time).

**How to apply:** When `/prompt-mini` fires, check whether the user's natural-language request is for the prompt itself (artifact-shaped: "give me," "write me," "generate") versus for the outcome of running it (execution-shaped: "do X," "fix Y"). If artifact-shaped, save to `.claude/commands/<name>.md`. If execution-shaped, follow prompt-mini's default and execute immediately. When in doubt, ask.

**Format conventions for saved prompts:**
- Path: `.claude/commands/<kebab-case-name>.md`
- Top of file: purpose, when to run, hard rules
- Phases numbered (Phase 1 / Phase 2 / etc.)
- Constraints + success condition at the bottom
- Auto-load context block at the top (file paths to read first)
