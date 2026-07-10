---
name: extending-safely
description: Standards for CHANGING the History vs Hype repo — the extend-don't-add acceptance test, seam-routing pre-change checklist (which seam, which tests, which docs), code conventions for new modules, test-first expectations, commit + secret-guard rules, and the agent-spawn digest. Use when: about to write or modify code under tools/; creating any NEW surface (module, command, skill, agent, REFERENCE doc, DB table, derived doc); planning a refactor or migration; about to commit, or the pre-commit hook just fired; spawning sub-agents for a build; tempted to mock, skip, or work around a failure. NOT for locating existing code (→ codebase-atlas), running tests (→ validation-standards), or DB schemas (→ data-stores).
---

# Extending Safely

How to change this repo without degrading it. Everything here was live-verified 2026-07-01/02 (files read, hooks read, commands run). Repo root: `D:\History vs Hype`; run everything from there.

## Owner context — read before framing any change

The owner is a **non-engineer** channel creator (terse/shorthand messages are how he thinks).

- **Frame code work as outcomes** — which command/report it affects, what breaks today, what improves. Never present architecture-option menus ("4 vs 6 fetches?" was rejected 2026-06-25 as "too technical"). Make the technical calls yourself; offer a plain-language go/no-go.
- **Workarounds only when explicitly time-boxed by the owner.** Otherwise: root cause. ADR-0012 is the house example — a dead clickbait gate was fixed IN `title_scorer.py`, not patched over in the new checker.
- **Surface real risks plainly** even so ("rearranging untested code first is how you break things").
- **When the owner corrects you, capture the rule immediately** — memory/wiki + `video-projects/_CORRECTIONS-LOG.md`, not just "noted". Live capture is a standing hard rule; the Stop hook is only the backstop.
- **Plans are executable docs**: persist any multi-step plan as a named in-repo markdown file with a top "How to execute" header (plans propose; the owner triggers). Origin: 2026-05-28, cloud sessions only see committed files.
- Full owner-communication profile (shorthand style, AskUserQuestion rules, no yes-manning) → **project-onboarding** skill; the bullets above are only the code-work subset.

## The extend-don't-add acceptance test

Before creating ANY new persistent surface (module, command, skill, agent, reference file):

1. **Three cheap greps first** (~2 tool calls; skipping them once cost ~30% of a build when `/fix` already did the proposed feature, 2026-05-11): Grep `.claude/commands/`, Grep `.claude/skills/`, Grep `.claude/REFERENCE/` for the capability keyword.
2. **If an existing surface can absorb it — extend that surface.** Create only if extension is impossible.
3. **New surface requires a named justification**, recorded where the work is documented (CONTEXT.md, the ADR, or the plan doc): "no existing surface carries this responsibility and here's the boundary." "We needed a place to put it" fails the test. (Planned monthly enforcement via `/status --surface` — ROADMAP Phase 79, NOT yet implemented; today the acceptance test is manual discipline.)
4. If only *adjacent* tooling exists, say so explicitly and state the differentiation.

Spec: `.claude/AGENT-ORCHESTRATION.md` § "Extend, Don't Add" (that doc caps itself at 400 lines as its own self-test).

## Module-depth heuristics (does a new seam earn its place?)

Three tests harvested from the `codebase-design` skill, for deciding whether a new module/seam pulls its weight instead of just adding surface — they sharpen the extend-don't-add call:

- **Depth as leverage.** A module earns its interface when a large amount of behaviour sits behind a small one. A wrapper that exposes about as much as it hides (pass-through) is negative-value: one more name to learn, nothing actually hidden.
- **The deletion test.** If deleting the module would spread its complexity across N callers, it earned its place; if deletion barely ripples, it was pass-through. Run this *before* adding a seam **and** before defending an existing thin one.
- **One adapter = hypothetical; two = real.** Don't build a seam/Protocol for variation that doesn't exist yet. `AnalysisSource` (ADR-0011) earned its shape because a *second* implementation genuinely needed it (Live + InMemory) — not "for flexibility".

## Touching X? → route through seam Y (pre-change checklist)

Action-side checklist. The descriptive seam catalog (what each seam IS) lives in codebase-atlas; the full ADRs are `docs/adr/0004..0014` — one line each here, read the ADR before arguing with it.

| Touching | Route through | Tests that must stay green (add yours beside them) | Also update |
|---|---|---|---|
| analytics.db read/write | `AnalyticsStore` (`tools/youtube_analytics/store.py`), `.open()` + explicit `.commit()` | `tests/test_analytics_store.py` | Schema change → `growth_data.ensure_schema()` (the ONE sanctioned raw conn); ADR-0004 |
| keywords.db | `KeywordStore` / `KeywordDB` (`tools/discovery/keyword_store.py`, `schema_manager.py`) | `tests/test_database_pin.py` — **pin return contracts BEFORE refactoring** | Migration → `tests/test_keywords_migration.py` |
| intel.db | `KBStore` (`tools/intel/kb_store.py`) — per-call connections: tests need a tmp FILE, never `:memory:` | `tests/test_intel.py`, `tests/test_intel_migration.py` | Competitor set → edit `tools/intel/competitor_channels.json` + rerun sync (ADR-0013) |
| POST-PUBLISH-ANALYSIS.md data | `from tools.post_publish import PostPublishStore` | `tests/test_post_publish_store.py` | New `PostPublishReport` field only when a SECOND consumer needs it (ADR-0005) |
| Project-folder resolution / lifecycle | `VideoProjectRepo` (`tools/video_projects/repo.py`) — read-only; NEVER add a mutation | `tests/test_video_projects.py` | Folder MOVES stay in `tools/reconcile/` (`tests/test_reconcile_mover.py`) |
| PROJECT-STATUS.md managed blocks | Register an `AutoZone` in `tools/video_projects/status_doc.py` — never hand-roll `<!-- AUTO:* -->` markers | `tests/test_status_doc.py` | ADR-0014 |
| SRT reading | `tools.subtitles.parse()` | `tests/test_subtitles.py` | ADR-0010 (the `srt` pip lib was REJECTED — don't reintroduce) |
| Title structure | `tools/title_features.py` — enrich `pattern()` + re-baseline, never fork | `tests/test_title_features.py`, `tools/tests/test_preflight_title_fallback.py` | Topic classifiers do NOT go here (ADR-0009) |
| A packaging rule that must BIND | Add a FILTER in `tools/preflight/packaging_lock.py` (code), never prose in a command file | `tests/test_packaging_lock.py` | ADR-0012; enrichment can never upgrade a filter FAIL |
| Any thumbnail check | Pass/fail necessary condition ONLY — a predictive pre-publish score is the forbidden failure mode | `tools/tests/test_thumbnail_filters.py` | ADR-0007 |
| /analyze external fetches | Extend the `AnalysisSource` Protocol + BOTH impls (Live + InMemory) | `tests/test_analyze.py` | ADR-0011 |
| Script-checker behavior | `tools/script_checkers/` — subclass `BaseChecker` (`checkers/__init__.py`), register in `registry.py::build_default_registry` | `tests/test_script_checkers.py` (subprocess pins), `tests/test_checker_registry.py` — **adding a checker legitimately re-baselines the exact-5 `list_all()` pin; update it deliberately, in the same change** | CLI wiring = argparse flag + `checker_flags` dicts (`cli.py`) + **the hardcoded `ordered` list in `cli.py::run_checkers` — a checker missing from `ordered` silently never runs, no error**. Voice rules derive FROM `.claude/REFERENCE/VOICE-PROFILE.md` → then re-derive `voice_lint` (ADR-0006, never the reverse) |
| Phase rule / slug parsing | Import `detect_phase` / `extract_topic_slug` from `tools/dashboard/project_scanner.py` — reuse, don't relocate | — | ADR-0008 deferred the move deliberately |
| A 4th store / new seam | Copy the ADR meta-shape: neutral peer package, frozen-dataclass returns, strict-single + lenient-bulk errors, staged migration, tests landed WITH the seam | new suite in `tests/` | **Write a new ADR** in `docs/adr/` (next number after 0014, `NNNN-slug.md`) |

**Two deliberately-unseamed dangerous writers** — the folder mover (`tools/reconcile/reconcile.py`) and the SRT rewriter (`tools/youtube_analytics/auto_srt_fixer.py`). "Defer the dangerous writer" is a named house pattern; do not "helpfully" wrap or relocate them. Every code ADR ends with "supersede rather than silently restructure" — changing a seam's decision means a NEW ADR, not a quiet refactor.

## Where new code goes

- **New module** → the existing domain package: channel analytics → `tools/youtube_analytics/`, discovery/packaging → `tools/discovery/`, pre-publish gates → `tools/preflight/`, script artifacts → `tools/production/`, competitor KB → `tools/intel/`, script QA → `tools/script_checkers/`. Top-level `tools/*.py` is reserved for cross-package seams (`title_features`, `subtitles`, `benchmark_store` pattern) — justify per the acceptance test.
- **Tests** → `tests/` (only dir default pytest collects), unit files in `tests/unit/`. `tools/tests/` is for regression PINS that run via explicit path only. **Never put a test file inside `tools/youtube_analytics/`** — that dir is pytest-poison (bare-import collection errors; the 6 broken files there have working twins in `tests/unit/`).
- **New ADR** (`docs/adr/`) when: creating a seam/store, adding a BINDING gate, adding a pip dependency to core, or rejecting a proposed consolidation so it stays rejected.
- **New scheduled routine** → workload in `tools/routines/`, registration via automation-ops skill.
- Filesystem for video work is owned by the lifecycle rules in CLAUDE.md — never invent folders under `video-projects/`.

## Code conventions a new module must follow

1. **Absolute `tools.` imports only.** Bare imports are the known collection-breaker (the youtube_analytics incident). Design for `python -m tools.<pkg>.<module>` from repo root; direct-script invocation is a bonus (add the `sys.path.insert(0, str(Path(__file__).resolve().parents[N]))` bootstrap), never the contract.
2. **Logging** via `tools/logging_config.py`: `logger = get_logger(__name__)` at module top; CLI mains call `setup_logging(args.verbose, args.quiet)` ONCE (it raises if both set — so make the flags a mutually-exclusive argparse group). It configures the `tools` logger → stderr, not root; never `print()` diagnostics, never `logging.basicConfig()`.
3. **Path anchoring**: `Path(__file__).resolve().parents[N]` — never cwd-relative (a bug class ADR-0008 eliminated).
4. **Error contract**: read-side helpers never raise (return `None`/defaults or `{'error': msg}`); strict single-item `load()` raises typed exceptions while bulk discovery logs-and-skips; typed returns are frozen dataclasses.
5. **Stdlib-only posture for seams/scanners.** A new pip dependency is an explicit decision (ADR-0010 rejected `srt` over exactly this); optional deps go in a pyproject extras group, and installing a missing dep beats mocking around it — always.
6. **CLI shape**: argparse, `--verbose/-v` + `--quiet/-q` exclusive pair, epilog with worked examples documenting the `-m` invocation.
7. **Dual-write pattern** for anything humans read: DB row is truth, markdown view is regenerated on every write (`swap_ledger` → `SWAP-LEDGER.md` model). Never make the .md the store.
8. **Slash-command frontmatter must NOT pin `model: sonnet`** — a command's model carries the whole session; on the owner's Pro plan that overflows long sessions (all 14 sonnet-pinned commands were repointed 2026-06-01). Agents are exempt (cold-start).

## Test-first expectations (which change needs which test)

| Change | Required test, before or with the change |
|---|---|
| Refactoring a store/module with callers | Behavior-pin its return contracts FIRST (`tests/test_database_pin.py` is the model — it pins even the `{'error': ...}` shapes) |
| New seam | Test suite lands WITH the seam, not after |
| CLI-visible behavior | Subprocess behavioral pin (`tests/test_script_checkers.py` model; set `PYTHONIOENCODING=utf-8` on Windows) |
| Bug fix | A regression test that reproduces the bug first |
| Schema migration | Migration test (`tests/test_keywords_migration.py`, `tests/test_intel_migration.py` models) |

Non-negotiables the principal enforced:
- **Fix ALL red tests, not just yours.** "Pre-existing failure" is never a reason to ship red; a missing dependency means `pip install`, not a mock, skip decorator, or `sys.modules` injection (owner had to manually order the fix of 6 dismissed failures — never again).
- **A change is not done on synthetic fixtures alone.** Run the tool against the live tree / real DBs / real CSVs and confirm a known-true fact. Exact commands, pytest paths, and the real-data verification procedure → **validation-standards** skill (don't guess at pytest flags; there are Windows-specific ones).
- Tests never touch the three live committed DBs — `:memory:`/tmp_path only (`tests/conftest.py` fixtures already do this; note `KBStore` needs a tmp FILE).

## Committing + the secret-guard hook

- **Commit only when the owner asks.** On the default branch, branch first. Subject style from live history: `type(scope): summary` — `feat` / `fix` / `chore` / `docs` / `test` / `refactor` / `research(#NN)`.
- **secret-guard pre-commit** (`.git/hooks/pre-commit`; tracked copy `tools/hooks/pre-commit`, reinstall via `sh tools/hooks/install.sh`) blocks staged credential files by filename (`token.json`, `client_secret*.json`, `*oauth*.json`, `credentials.json`, `secrets.json`, `*.pem/.key/.p12/.pfx`, `.env`) and private-key blocks in staged additions. Origin: 2026-06-03 — a gitignore path typo left a live OAuth `token.json` committable.
- **When it fires:** unstage the file (`git restore --staged <file>`) and rethink — the hook is nearly always right. `git commit --no-verify` only if you are CERTAIN it's a false positive, and say so in the commit body. If a real secret ever reaches history: **rotate the credential immediately**; history is forever. Never bypass hooks to make a commit pass — a failing hook is a bug to root-cause, not an obstacle.
- Expect the three committed SQLite DBs to show as modified after tool runs; that's normal (→ data-stores), not something to `git checkout --` away without checking what wrote them. When the owner asks for a commit, stage the DB files your tool run legitimately wrote (live history commits them with the work) — never commit DB changes you can't attribute.

## Agent-spawn digest (builds only — the spec is `.claude/AGENT-ORCHESTRATION.md`; read it before spawning)

- **Three triggers, any one → spawn instead of reading in main context:** (1) >500 lines to read (single file or cumulative), (2) reasoning >3 steps that won't collapse to a one-liner, (3) 2+ parallel independent tasks.
- **Spawn prompt = three blocks:** `<read_first>` with exact absolute paths · one-sentence imperative goal · the Return Contract pasted verbatim (grep the `<!-- RETURN-CONTRACT-V1 -->` marker in AGENT-ORCHESTRATION.md; changing it = bump to V2 + update callers, never silent edits). Contract core: ≤200-word summary, full output written to disk, no raw dumps >10 lines, final line `OUTPUT: <absolute-path>`.
- **Reference tiers:** Tier 0 = CLAUDE.md + MEMORY.md (always loaded, tiny on purpose); Tier 1 = declared in command frontmatter; Tier 2 = loaded ONLY by the sub-agent that names them in `<read_first>` — main context never opens them, not even "to check"; Tier 3 = on-demand. Every ref above Tier 0 needs a named caller.
- **Rate limits are expected, not exceptional:** on 429 / "rate limit" strings, serialize pending spawns, retry with 30s/60s/120s backoff (max 3), then AskUserQuestion checkpoint (retry once more [recommended] / paste-prompt fallback / abort). Never fail the command on a rate limit.
- Anti-pattern: reading a sub-agent's output file in full after return — the summary + `OUTPUT:` line is the contract; open it only for a specific quote/range.

## What the principal would not let slip

1. Greening a test by mocking, skipping, or disabling instead of installing the dep / fixing the cause.
2. Shipping with red tests dismissed as "pre-existing".
3. A silent workaround where a root-cause fix belongs (workarounds need an explicit owner time-box).
4. A new file/command/agent/ref without the named-justification acceptance test — or without the three discovery greps first.
5. Re-implementing what a seam owns (a second SRT parser, a fourth AUTO-fence surgery, a hardcoded lifecycle glob).
6. `git commit --no-verify` as a reflex, or any hook bypass to force a commit through.
7. Presenting the owner an architecture menu instead of a decision — or skipping the memory/wiki capture after he corrects course.
8. Declaring a change done without the real-data check (synthetic fixtures prove it runs, not that behavior survived).

## Related skills

- **codebase-atlas** — to find WHERE something lives, what a seam is, exact run commands, and graph/grep navigation before you plan the change.
- **data-stores** — before touching any DB table, AUTO zone, or derived markdown: schemas, dead-table traps, staleness semantics.
- **validation-standards** — to actually run the tests (exact pytest commands + Windows flags) and apply the real-data definition of done.
