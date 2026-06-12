# GRAPHIFY-OPS.md — Operating manual + session handoff

Built 2026-05-25/26 across one long session. This file captures the current state, how to use it, and what's still on the table. Read this first when picking up graphify work later.

## What exists right now

**Code graph (`graphify-out/`)** — AST extraction of the whole repo, slimmed and labeled.
- `graph.json` (48 MB, 54,135 nodes, 54,076 edges) — slimmed from the original 93,914-node AST run.
- `graph.html` (3.4 MB) — interactive viz of the top 60 communities (3,353 nodes). Open in any browser.
- `GRAPH_REPORT.md` (1.5 MB) — god nodes, surprising connections, suggested questions. Communities are hand-labeled where there's a clear structural trigger (KeywordDB, AnalyticsStore, ScriptParser, etc.).
- `graph.full.json.bak` (96 MB) — backup of the pre-slim original. Restore with `cp graph.full.json.bak graph.json` if needed.

**Research graph (`graphify-out/research/`)** — Gemini-extracted graph from the 15 archived `01-VERIFIED-RESEARCH.md` files.
- `graph.json`, `graph.html`, `GRAPH_REPORT.md` — 110 nodes / 55 edges / 2 hyperedges. Top clusters: Chagos, Iran 1953, Somaliland, Vichy/Statut des Juifs, Flat Earth, Berlin Conference.
- `query.py` — BFS subgraph helper. Token-saving entry point until MCP is active.
- `build.py` + `extract-prompt.txt` — regenerate everything from `RESEARCH-GRAPH.json`.
- `.needs_refresh` — touched by `/reconcile` after each archive; lists slugs awaiting Gemini re-extraction.

**Reference layer (`.claude/REFERENCE/`)** — distilled, human-readable maps.
- `CODE-MAP.md` — god nodes, real code communities, noise to ignore, worktree-duplication caveat.
- `RESEARCH-CONCEPT-MAP.md` — entities/scholars/quotes/bridges/gaps. Python query cheatsheet at the bottom.
- `RESEARCH-GRAPH.json` — structured-JSON companion (88 entities, 22 scholars, 55 edges, 22 citations, 2 bridges, 15 videos). Source of truth for `build.py`.
- `INDEX.md` — points to all of the above.

**Infrastructure changes**
- `.graphifyignore` (32 lines) — excludes worktrees, `_ARCHIVE/`, `_inbox/`, yt-dlp dumps from future runs.
- `tools/refresh-research-graph.py` — one-shot doc-graph refresh (Gemini Flash → cleanup → graphify build → marker clear). Use `--skip-gemini` to rebuild from existing JSON without re-extracting.
- `.git/hooks/post-commit` + `post-checkout` — auto-rebuild AST graph in background after every commit/branch-switch. Free, no LLM. Log at `~/.cache/graphify-rebuild.log`. Uninstall: `python -m graphify hook uninstall`.
- `~/.claude.json` — both project-path variants (`D:\History vs Hype` and `D:/History vs Hype`) now have `graphify-code` and `graphify-research` MCP servers. Backup at `~/.claude.json.bak.before-graphify-mcp-1779796087`.
- `.claude/commands/reconcile.md` — archive transition now touches `graphify-out/research/.needs_refresh` with the new slug.

## Health checks (run if something feels off)

```bash
# 1. AST hook still installed?
ls .git/hooks/post-commit .git/hooks/post-checkout

# 2. MCP servers configured?
python -c "import json; d=json.load(open(r'C:\Users\Benoi\.claude.json')); proj=d['projects'].get('D:/History vs Hype') or d['projects'].get(r'D:\History vs Hype'); print(list(proj['mcpServers'].keys()))"
# Expect: ['playwright', 'notebooklm', 'graphify-code', 'graphify-research'] (or with youtube-data on the backslash variant)

# 3. Both graphs queryable?
python graphify-out/research/query.py "uti possidetis" --max-nodes 5
ls -lh graphify-out/graph.json graphify-out/research/graph.json

# 4. Doc-graph staleness behind?
cat graphify-out/research/.needs_refresh 2>/dev/null
# If non-empty, run: python tools/refresh-research-graph.py
```

## Workflow patterns

| Question type | Use this |
|---|---|
| "Where does X live in the codebase?" | `CODE-MAP.md` (don't grep) |
| "Tell me about scholar/topic/treaty X" | MCP `query_graph` if active, else `python graphify-out/research/query.py "X"` |
| "Have I cited Y before? Which videos?" | MCP `get_node` / `query_graph`, else `RESEARCH-GRAPH.json` via Python (cheatsheet in concept-map footer) |
| "What connects A to B?" | MCP `shortest_path` if active, else `python graphify-out/research/query.py "A" --depth 3` and look at edges |
| "Suggest a new video angle from existing research" | Read `graphify-out/research/GRAPH_REPORT.md` § Suggested Questions + § Bridges |
| Refresh after archiving a new video | `python tools/refresh-research-graph.py` (full Gemini round-trip) |

## Open work (none auto-executed — pick what you want)

Ranked by impact:

1. **Research-graph densification — scope A (UPGRADE-PLAN Phase 2.3, decided 2026-06-12):** research corpus only — all `01-VERIFIED-RESEARCH.md` (archived + active) + `.brain/` quote threads + `tools/benchmark/` playbooks — via **Gemini Flash CLI** (existing sub, zero marginal cost), extending `tools/refresh-research-graph.py`. Before building, check whether a NotebookLM coverage notebook (same corpus via `notebook_query`) answers "have we covered X" well enough to make the graph work redundant. ~~Ollama full-22.5M-word extraction~~ RETIRED — Ollama is a verified dead end on this laptop (gemma3:4b fails JSON, qwen2.5:7b too slow on CPU; smoke-tested 2026-05-26).
2. **`graphify install --project`** — moves the graphify skill from `~/.claude/skills/` (user-global) into `.claude/skills/` (project-tracked). Worth doing if you ever want to reproduce the setup on another machine.
3. **`graphify watch .` in background** — real-time AST updates while editing. Redundant with the post-commit hook unless you want sub-commit refresh.
4. **`uv tool install graphifyy`** — cleaner install than current system-Python `site-packages`. Migrate only if you hit conflicts. Path detection in the hook and MCP config uses absolute paths, so a reinstall under `uv` will require updating `graphify-out/.graphify_python` and the two MCP entries in `~/.claude.json`.

*(Removed 2026-06-12: "Restart Claude Code" — done long since; MCP servers are live.)*

## Recovery / rollback

| To undo | Run |
|---|---|
| Git hooks | `python -m graphify hook uninstall` |
| MCP servers | Restore `~/.claude.json.bak.before-graphify-mcp-1779796087` |
| Slim code graph (back to 96 MB) | `cp graphify-out/graph.full.json.bak graphify-out/graph.json` |
| Research graph | Delete `graphify-out/research/` and re-run `tools/refresh-research-graph.py` |
| Everything graphify | `python -m graphify uninstall --purge` (also deletes `graphify-out/`) |

## Known caveats (don't re-discover these)

- **Worktree duplication** — RESOLVED 2026-06-12: bridge-cse worktree pruned, branch deleted (bundle: `D:\backups\bridge-cse-flight-deals-2026-06-12.bundle`; working copy: `D:\flight-deals`). `.graphifyignore` entry is now inert but harmless.
- **Gemini Flash repeats output** — the research-extraction Gemini call has duplicated its full JSON twice in one of our runs. The refresh script handles this via balanced-brace JSON truncation, but if you ever bypass it, check for `}{` near the end of raw output.
- **Citation slug attribution** — Gemini got 0/22 wrong in the JSON pass but 2/20 wrong in the markdown pass. Always verify quote→video attribution against the original `01-VERIFIED-RESEARCH.md` before script use. Same rule as `[[feedback-notebook-citation-grounding]]`.
- **Stub entities** — 4 nodes in `RESEARCH-GRAPH.json` have `role` starting with `[stub: ...]`. They exist because Gemini emitted edges pointing to ids it forgot to declare. Treat as low-confidence.
- **Community labels collapse on duplicates** — graphify can produce two communities with the same hand-label (e.g. "Source library / publisher registry" appears as #0 AND #4). Harmless but visible in the report.

## Why this session existed

The original `/graphify` run did AST-only extraction (token cost: 0) — semantic step skipped, communities unlabeled, no HTML. We replicated the missing pieces using Gemini Flash for the doc-content extraction (instead of Claude subagents) and did Step 5 + Step 6 manually. Total cost: 2 Gemini Flash calls (~pennies on Google AI Plus), zero Anthropic semantic-extraction dispatches. The artifacts in this manual replace what a full `/graphify --mode deep .` run would have produced, at ~100× lower cost.
