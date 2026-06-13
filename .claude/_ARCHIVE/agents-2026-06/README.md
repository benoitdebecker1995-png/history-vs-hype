# Archived agents — 2026-06-12 (UPGRADE-PLAN W2)

These three agents were archived because **no current command or flow spawns them** (verified by ref-grep + 164-session-log invocation scan, `docs/AUDIT-COMMANDS-2026-06.md`). They are preserved here, not deleted — restore by `git mv` back to `.claude/agents/` if a future flow needs them.

| Agent | Size | Why archived |
|---|---|---|
| `fact-checker` | 32 KB | `/verify` does its fact-check work inline; only listed `fact-checker.md` as a "Reference Files" pointer, never spawned it. |
| `claims-extractor` | 16 KB | Pure orphan — zero inbound references, zero spawns in retained logs. `/verify --extract` extracts inline. |
| `research-organizer` | 57 KB | Live references existed only in the **parked** `.antigravity/` config + old planning docs. Current `/research` flow uses `wiki-researcher` + `notebook-researcher`. |

**Live references cleaned on archive (W2):**
- `.claude/commands/verify.md` — removed the fact-checker agent pointer in Reference Files.
- `.claude/REFERENCE/primary-sources.md` — "Referenced by" line trimmed to `script-writer-v2`.
- `.brain/methodology/gemini-routing.md` — removed the three model-routing rows.
- `.claude/agents/competitor-gap.contract.md` — removed the `research-organizer` consumer row.

`.antigravity/agents/content-script.md` still names `research-organizer`, left as-is (Antigravity is parked — `memory/project-antigravity-parked.md`).
