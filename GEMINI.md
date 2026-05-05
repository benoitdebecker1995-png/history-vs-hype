# Project Instructions: History vs Hype

This project follows a strict **Verified Workflow** for YouTube content production.

## Architectural Mandates
- **Packaging First:** Do not start research or scripting until a topic is `/greenlight`-ed.
- **Academic Grounding:** All claims must be verified via academic sources (University Presses) with page numbers and exact quotes.
- **Voice:** "Calm Prosecutor" (intellectually high, emotionally low).
- **Tooling:** Use the Python tools in `tools/` for titles, thumbnails, and analytics.

## Custom Skills (Procedural Triggers)

### `/grill` - The Socratic Interrogator
When the user invokes `/grill` (or asks for intent clarification), you MUST:
1. **STOP** all implementation or research.
2. Identify 3-5 "Hard Questions" that challenge the user's assumptions.
3. Focus on: Edge cases, "Channel DNA" alignment (Systems > Narratives), and constraints (12-min cap).
4. Do not proceed until the user has resolved these branches.

### `/synthesis` - The Requirement Manifest
After a grilling session or complex request, you MUST:
1. Summarize the agreed-upon requirements into a concise "Manifest".
2. Explicitly list what is IN-SCOPE and OUT-OF-SCOPE.
3. Wait for user confirmation (✅) before proceeding.

### `/handoff` - Dual-AI Coordination
When moving between Gemini and Claude, you MUST:
1. Update `HANDOFF.md` with the current state.
2. State exactly what was completed and what the *other* AI needs to do next.
3. Use a clear "Baton" signal: `READY FOR [CLAUDE/GEMINI]`.

## Folder Conventions
- Use lifecycle folders in `video-projects/`: `_IN_PRODUCTION`, `_READY_TO_FILM`, `_ARCHIVED`.
- No loose folders in `video-projects/`.
- Standard project file naming: `01-VERIFIED-RESEARCH.md`, `02-SCRIPT-DRAFT.md`, `03-FACT-CHECK-VERIFICATION.md`.

## Quality Gates
- 90% verification threshold for `01-VERIFIED-RESEARCH.md` before starting `02-SCRIPT-DRAFT.md`.
- 100% match required in `03-FACT-CHECK-VERIFICATION.md` before filming.

## References
- See `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` for authoritative style rules.
- See `CLAUDE.md` and `AGENTS.md` for legacy agent instructions.
