# GRAPHIFY-OPS.md — Operating manual + session handoff

Built 2026-05-25/26 across one long session. This file captures the current state, how to use it, and what's still on the table. Read this first when picking up graphify work later.

> **2026-07-31 — REPAIRED after a silent outage.** graphify had been dead for an unknown period:
> it was installed under `C:\Users\Benoi\AppData\Local\Programs\Python\Python312\python.exe`, that
> interpreter was uninstalled, and nothing noticed — the MCP servers simply stopped resolving and
> sessions fell back to grep. Fixed by installing `graphifyy` 0.9.31 on the live interpreter
> (Python 3.14.2), repointing `graphify-out/.graphify_python`, and moving the server declarations
> out of user-level `~/.claude.json` into the repo's version-controlled **`.mcp.json`** so the next
> machine change is visible in a diff instead of silent.
>
> Live counts differ from the 2026-05 figures below: **code graph 90,745 nodes / 97,940 edges**
> (not 54,135), **research graph 169 nodes** (not 110). Both servers smoke-tested over MCP stdio —
> research starts in 2.0s, code in 11.1s (80 MB graph).

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
- `~/.claude.json` — both project-path variants (`G:\History vs Hype` and `D:/History vs Hype`) now have `graphify-code` and `graphify-research` MCP servers. Backup at `~/.claude.json.bak.before-graphify-mcp-1779796087`.
- `.claude/commands/reconcile.md` — archive transition now touches `graphify-out/research/.needs_refresh` with the new slug.

## Health checks (run if something feels off)

```bash
# 1. AST hook still installed?
ls .git/hooks/post-commit .git/hooks/post-checkout

# 2. MCP servers configured?  (moved to the repo's .mcp.json on 2026-07-31 —
#    user-level config is what silently died when Python 3.12 was uninstalled)
python -c "import json; print(list(json.load(open('.mcp.json'))['mcpServers']))"
# Expect: ['notebooklm', 'graphify-code', 'graphify-research']

# 2b. Does the server actually start? (rc=0 and a JSON-RPC result on stdout)
python -m graphify --help >/dev/null && echo "graphify CLI OK"

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

1. **Research-graph densification — scope A:** ⛔ **VERDICT: NOTEBOOK-SUFFICIENT (R3 pilot, 2026-06-12). Densification (UPGRADE-PLAN R4) is BLOCKED — the coverage notebook makes the graph work redundant for coverage queries.**

   **Pilot:** NotebookLM notebook **`HvH-coverage-corpus`** (id `f3bc649e-b90e-4832-92d7-e1d4b9932dc4`) built with all 26 `01-VERIFIED-RESEARCH.md` files (archived + active + backlog), sources renamed to project slugs. 10 representative coverage queries run head-to-head against `mcp__graphify-research__query_graph`:

   | # | Coverage query | Notebook (HvH-coverage-corpus) | Graph (graphify-research) |
   |---|---|---|---|
   | 1 | Cited Mamdani? | ✅ #40, both works, page-anchored claims | ❌ no nodes |
   | 2 | Treaty of Lausanne? | ✅ #58 full role + "only project" scoping | ❌ wrong treaties (Zaragoza/Utrecht/Tripoli) |
   | 3 | McDowall as source? | ✅ #58, 17 claim clusters incl. retired-quote audit trail | ❌ matched "David Lindberg" |
   | 4 | uti possidetis? | ✅ 4 videos (#41/#40/#55/#01) with per-video role | ⚠️ 1 video (#01 only) |
   | 5 | ICJ rulings? | ✅ 5 videos with named cases | ⚠️ 1 thin hit (Chagos–UK edge) |
   | 6 | Radcliffe commission? | ✅ #43 with full detail | ⚠️ correct but thin (1 node + 1 edge) |
   | 7 | Promised plebiscite never held? | ✅ 3 videos, conceptually apt | ❌ no nodes |
   | 8 | Ottoman-script primary docs? | ✅ 3 videos (#57/#58/#51) | ❌ no nodes |
   | 9 | Sykes-Picot mentions? | ✅ #58 with role nuance (foil / saturated-lane) | ❌ no nodes |
   | 10 | Oil drives a border/legal decision? (thematic) | ✅ 5-video cross-corpus synthesis | ⚠️ 1 edge (APOC–Iran) |

   **Score: notebook 10/10, graph 0/10** (3 partials, 7 misses/wrong). Latency: graph <2s vs notebook ~20–60s/query — but per the R3 spec both paths are zero marginal cost and the judgment is quality-only, and the quality gap is total. The graph's 169-entity extraction misses scholars, treaties, and concepts wholesale; the notebook handles entity, concept, AND thematic queries with per-video roles and page-anchored citations.

   **Operational consequence:** for "have we covered X" questions, query `HvH-coverage-corpus` via `notebook_query` (NOT the research graph). Keep the notebook current: add each new project's `01-VERIFIED-RESEARCH.md` at archive time (candidate /reconcile backstop). The research graph stays as-is for visualization; do not invest further extraction effort. ~~Ollama full-22.5M-word extraction~~ RETIRED — Ollama is a verified dead end on this laptop (gemma3:4b fails JSON, qwen2.5:7b too slow on CPU; smoke-tested 2026-05-26).
2. **`graphify install --project`** — moves the graphify skill from `~/.claude/skills/` (user-global) into `.claude/skills/` (project-tracked). Worth doing if you ever want to reproduce the setup on another machine.
3. **`graphify watch .` in background** — real-time AST updates while editing. Redundant with the post-commit hook unless you want sub-commit refresh.
4. **`uv tool install graphifyy`** — cleaner install than current system-Python `site-packages`. Migrate only if you hit conflicts. Path detection in the hook and MCP config uses absolute paths, so a reinstall under `uv` will require updating `graphify-out/.graphify_python` and the two MCP entries in `~/.claude.json`.

*(Removed 2026-06-12: "Restart Claude Code" — done long since; MCP servers are live.)*

## Recovery / rollback

| To undo | Run |
|---|---|
| Git hooks | `python -m graphify hook uninstall` |
| MCP servers | Declared in the repo's `.mcp.json` — edit or delete the entries there. (The old recovery pointer named `~/.claude.json.bak.before-graphify-mcp-1779796087`; that backup no longer exists.) |
| Slim code graph (back to 96 MB) | `cp graphify-out/graph.full.json.bak graphify-out/graph.json` |
| Research graph | Delete `graphify-out/research/` and re-run `tools/refresh-research-graph.py` |
| Everything graphify | `python -m graphify uninstall --purge` (also deletes `graphify-out/`) |

## Disk retention

The post-commit hook writes a new dated snapshot into `graphify-out/` on every
commit and never removes the old one. Unchecked, that reached **65 snapshots /
4.2 GB** by 2026-07-30 — nothing in the repo reads any of them. Live artifacts
are `graph.json`, `graph.full.json.bak`, `cache/`, and the tracked `research/`
subtree; the dated dirs are pure history.

```bash
python -m tools.routines.prune_graphify_snapshots            # dry run
python -m tools.routines.prune_graphify_snapshots --apply    # keep newest 3
```

Dry-run by default; only ever touches directories matching `YYYY-MM-DD[_N]`, so
`research/` and `cache/` can't be hit. First run (2026-07-30) deleted 62
snapshots and reclaimed 3.6 GB, taking `graphify-out/` to 644 MB. Not yet
scheduled — run it after a heavy commit stretch, or register it via
**automation-ops** if it starts needing a babysitter.

## Known caveats (don't re-discover these)

- **Worktree duplication** — RESOLVED 2026-06-12: bridge-cse worktree pruned, branch deleted (bundle: `D:\backups\bridge-cse-flight-deals-2026-06-12.bundle`; working copy: `D:\flight-deals`). `.graphifyignore` entry is now inert but harmless.
- **Gemini Flash repeats output** — the research-extraction Gemini call has duplicated its full JSON twice in one of our runs. The refresh script handles this via balanced-brace JSON truncation, but if you ever bypass it, check for `}{` near the end of raw output.
- **Citation slug attribution** — Gemini got 0/22 wrong in the JSON pass but 2/20 wrong in the markdown pass. Always verify quote→video attribution against the original `01-VERIFIED-RESEARCH.md` before script use. Same rule as `[[feedback-notebook-citation-grounding]]`.
- **Stub entities** — 4 nodes in `RESEARCH-GRAPH.json` have `role` starting with `[stub: ...]`. They exist because Gemini emitted edges pointing to ids it forgot to declare. Treat as low-confidence.
- **Community labels collapse on duplicates** — graphify can produce two communities with the same hand-label (e.g. "Source library / publisher registry" appears as #0 AND #4). Harmless but visible in the report.

## Why this session existed

The original `/graphify` run did AST-only extraction (token cost: 0) — semantic step skipped, communities unlabeled, no HTML. We replicated the missing pieces using Gemini Flash for the doc-content extraction (instead of Claude subagents) and did Step 5 + Step 6 manually. Total cost: 2 Gemini Flash calls (~pennies on Google AI Plus), zero Anthropic semantic-extraction dispatches. The artifacts in this manual replace what a full `/graphify --mode deep .` run would have produced, at ~100× lower cost.
