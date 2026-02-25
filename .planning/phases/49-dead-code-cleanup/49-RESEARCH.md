# Phase 49: Dead Code Cleanup - Research

**Researched:** 2026-02-25
**Domain:** Python dead code removal, static caller analysis, git history preservation
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Unused function audit depth:**
- Full audit of every public function in large modules (database.py, patterns.py, prompt_evaluation.py at minimum)
- Document caller count for each public function; remove those with zero callers
- No separate audit report file — just delete dead code, commit messages document what was removed

**prompt_evaluation.py disposition:**
- If deleted, commit message must describe what the module did and why it was removed (descriptive commit)

**Deletion method:**
- Standard `git rm` — no archive folders. Git history preserves everything
- Clean all stale references when removing a function: imports in other files, docstring mentions, comments
- After each deletion pass, run import checks on affected modules to verify nothing breaks

### Claude's Discretion
- Which modules beyond database.py and patterns.py warrant full audit (based on size and refactor history)
- Whether 1-caller functions should be flagged or left alone
- prompt_evaluation.py: read it, decide keep vs delete based on future value
- tools/discovery/backups/: check if anything still writes to it, then delete or .gitignore accordingly
- Whether to add .gitignore rules for scratch file patterns (e.g., `_*.json`, `backups/`)
- How to organize commits (logical groupings at Claude's discretion)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CLEAN-01 | Dead code files removed (_csv_backfill.py, _competitor_fetch.py, _longform_*.json, _backfill_ids.txt) | All 7 files confirmed present in tools/youtube_analytics/ under new underscore names; `git rm` is the correct removal method |
| CLEAN-02 | Unused functions identified and removed from active modules | Caller analysis shows database.py (2,927 lines, 55+ methods) and patterns.py (2,070 lines) are the primary targets; patterns.py is actively used by /patterns command, database.py methods all have callers in the active tool chain |
| CLEAN-03 | datetime.utcnow() deprecation warnings fixed | Already fixed (zero occurrences across codebase) — requirement is pre-satisfied; mark done immediately |
</phase_requirements>

---

## Summary

Phase 49 is primarily a deletion phase. The audit has already identified the exact files to remove, and two of the three requirements are essentially pre-resolved: CLEAN-03 (datetime.utcnow()) has zero occurrences remaining, and CLEAN-01's seven dead files are confirmed present and unimported.

The substantive work is CLEAN-02: auditing public functions in large modules for zero-caller dead code. Research reveals three key findings that change the audit scope: (1) `patterns.py` is actively invoked by the `/patterns` slash command, so it is not a deletion candidate as a whole — only individual unused helper functions within it need checking; (2) `prompt_evaluation.py` is referenced by two active skills (`notebooklm-prompt-generator.md`, `script-reviewer.md`) as a voice-check tool, making it a keep-or-remove judgment call; (3) `_longform_enriched.json` and `_longform_metrics.json` are read at runtime by `backfill.py`'s `import_from_json_prefetch()` and `_load_own_channel_ids()` functions — deleting them is fine (the code falls back gracefully when files are absent), but this dependency must be understood before deletion. The `backups/` directory is untracked, and database.py's `_backup_database()` and `_ensure_variant_tables()` still write to it during v27 schema migration — adding it to `.gitignore` is the correct handling since the migration has already run on production.

**Primary recommendation:** Execute CLEAN-01 and CLEAN-03 first (mechanical deletions), then audit `prompt_evaluation.py` for keep/delete decision, then do targeted caller-count audits on database.py and patterns.py to identify any zero-caller functions — leaving 1-caller functions alone unless they are clearly superseded.

---

## Standard Stack

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `git rm` | system git | Delete tracked files, preserve history | Removes from working tree and staging in one step; history accessible via `git log -- <path>` |
| `grep -rn` / Grep tool | — | Caller-count analysis (search function names across codebase) | Fastest way to count callers for each public function |
| Python import check | python -c "import tools.X" | Verify no broken imports after deletion | Catches missing references that grep might miss |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| `git status` | — | Verify staged deletions before commit | After each `git rm` pass |
| `.gitignore` | — | Prevent re-tracking of generated files | For backups/ directory and scratch JSON patterns |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| grep-based caller analysis | `vulture` (static dead code finder) | vulture is faster at scale but requires pip install and produces false positives for dynamically-called functions; grep is more reliable for this codebase's patterns |
| manual audit | `ast.parse` + walk | AST walk is more precise but overkill for a codebase with clear naming conventions |

---

## Architecture Patterns

### Deletion Workflow (Per Batch)

```
1. git rm <files>
2. grep -rn "<function_name>" tools/ — confirm zero callers
3. Edit any files containing stale imports or docstring mentions
4. python -c "from tools.<module> import <class>" — smoke test
5. git add <edited_files>
6. git commit -m "chore(49): descriptive message"
```

### Commit Grouping (Recommended)

**Wave 1 — Mechanical deletions (CLEAN-01 + CLEAN-03 mark):**
- Delete 7 dead files from `tools/youtube_analytics/`
- Mark CLEAN-03 complete (no code changes needed)
- Add `tools/discovery/backups/` to `.gitignore`

**Wave 2 — prompt_evaluation.py decision:**
- Read the file, decide keep vs. delete
- If delete: `git rm`, update skill references in `.claude/skills/`
- Commit with descriptive message describing what the module did

**Wave 3 — Function-level dead code:**
- Audit database.py methods (zero-caller check)
- Audit patterns.py functions (zero-caller check)
- Audit any other large modules at Claude's discretion
- Remove dead functions, clean stale imports, commit

### Anti-Patterns to Avoid
- **Deleting files before checking runtime consumers:** `backfill.py` reads `_longform_enriched.json` and `_longform_metrics.json` at runtime (with graceful fallback when absent). Deletion is safe but the dependency must be acknowledged.
- **git rm without checking git status first:** Confirm files are tracked before using git rm (all 7 dead files ARE tracked — confirmed by git status output showing them as untracked in git status... actually they appear as `??` in git status which means they are UNTRACKED — see critical finding below).
- **Removing 1-caller functions without tracing the caller:** A function with one caller is probably still needed. Flag, don't delete.
- **Leaving stale `sys.path.insert` references in dead files:** The dead scripts (`_csv_backfill.py`, `_competitor_fetch.py`) contain old `sys.path.insert` hacks — these disappear with the file, no extra cleanup needed.

---

## Critical Findings

### Finding 1: Dead Files Are Untracked, Not Tracked
**What this means:** The 7 dead files appear as `??` (untracked) in `git status`, NOT as tracked files. They were never committed to the repository.

**Implication:** `git rm` will fail with "pathspec did not match any files" for untracked files. The correct command is simply `rm` (or `del` on Windows) followed by verifying they don't appear in future `git status` output. No git staging needed — git already ignores them.

**Verification command:**
```bash
cd "G:/History vs Hype" && git status tools/youtube_analytics/_csv_backfill.py
```
Expected: `?? tools/youtube_analytics/_csv_backfill.py` — confirms untracked.

**Action:** Use `rm` to delete the files from disk. Then optionally add `.gitignore` patterns to prevent them from being accidentally added later.

### Finding 2: backfill.py Runtime Dependency on _longform JSON Files
`tools/youtube_analytics/backfill.py` reads `_longform_enriched.json` and `_longform_metrics.json` at runtime in two functions:
- `_load_own_channel_ids()` (line 82): iterates both files if present, graceful fallback to empty set if absent
- `import_from_json_prefetch()` (line 165-166): uses enriched if exists, falls back to metrics, returns error dict if neither exists

**Implication:** Deleting these JSON files is safe — `backfill.py` handles absence gracefully. However, deleting them means running `backfill.py` without pre-fetched data will return `{'error': 'No JSON pre-fetch found', ...}` from Stage 1. This is acceptable since the backfill has already been completed (the data is in keywords.db). Document in commit message.

### Finding 3: backups/ Is Untracked but Still Written To
`tools/discovery/backups/` is untracked (confirmed by `git status` showing `??`). However, `database.py`'s `_backup_database()` and `_ensure_variant_tables()` still create files there during the v27 schema migration. Since the v27 migration has already run on production (schema is at v29), this path is only triggered for fresh databases. The directory should be added to `.gitignore` rather than deleted, so future migration backups don't litter git status.

**Current .gitignore:** Does not contain `backups/` or `tools/discovery/backups/`.

### Finding 4: prompt_evaluation.py Has Active Skill References
Two active skill files reference `prompt_evaluation.py`:
- `.claude/skills/notebooklm-prompt-generator.md:666` — mentions `tools/prompt_evaluation.py channel_voice_check`
- `.claude/skills/script-reviewer.md:655` — mentions `tools/prompt_evaluation.py channel_voice_check`

**Content assessment:** The module contains prompt templates (SCRIPT_PROMPTS, FACT_CHECK_PROMPTS, VOICE_CHECK_PROMPTS), an `evaluate_script_quality()` heuristic scorer, a project health check runner, and a `run_live_comparison()` function that calls the Anthropic API. It was last meaningfully updated before v3.0 (references old file paths like `.claude/SCRIPTWRITING-STYLE-GUIDE.md` which no longer exist). The voice_check prompt it advertises is a string in the VOICE_CHECK_PROMPTS dict, not a CLI argument — the `channel_voice_check` subcommand advertised in the skills doesn't actually exist as a flag.

**Recommendation:** Delete. The skill references are aspirational/stale — the `channel_voice_check` subcommand they cite doesn't exist as an actual CLI argument. The voice check functionality is superseded by the agent system (script-writer-v2 has 19 rules covering voice). If deleted, update the two skill file references and write a descriptive commit message.

### Finding 5: patterns.py Is Actively Used
`patterns.py` is the backend for the `/patterns` slash command (`.claude/commands/patterns.md`). The command calls `python -m tools.youtube_analytics.patterns --all`, `--topic-report`, `--title-report`, `--monthly`. The module is a keeper; only individual dead functions within it (those with zero callers across the codebase) should be removed.

### Finding 6: database.py Methods All Have Active Callers
A cross-reference audit of KeywordDB methods against all tool files found that every method group has at least one caller:
- CRUD methods (add_keyword, get_keyword, search_keywords): called from keywords.py, autocomplete.py, demand.py, orchestrator.py
- Performance/trend methods: called from backfill_gaps.py, demand.py
- Lifecycle methods (set_lifecycle_state, get_lifecycle_state, get_keywords_by_lifecycle): called from opportunity.py, orchestrator.py, recommender.py
- Production constraints: called from orchestrator.py
- Classification methods: called from competition.py
- The standalone `init_database()` function at line 2914: called only from `__init__.py` export — it is a thin wrapper around `KeywordDB().init_database()`, and exported in `__all__`. This is a public API wrapper, not dead code.

**Implication:** database.py may have zero dead methods. The audit should still scan for any private helpers (`_ensure_*` methods) that may be called nowhere except from within the class itself but are no longer triggered by any public method.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Caller analysis | Custom AST walker | grep -rn "function_name" tools/ | grep is sufficient for this scale; AST walkers add complexity with no benefit here |
| Safe file deletion | Archive/copy logic | rm + .gitignore | git history is the archive; no need for backup folders |
| Import verification | Custom import checker | python -c "from tools.X import Y" | Standard Python import system catches all breakage |

---

## Common Pitfalls

### Pitfall 1: git rm on Untracked Files
**What goes wrong:** Running `git rm tools/youtube_analytics/_csv_backfill.py` on an untracked file fails with "pathspec did not match any files known to git."
**Why it happens:** The dead files were scratch files never committed.
**How to avoid:** Use `rm` (PowerShell: `Remove-Item` or `del`) for untracked files. Verify with `git status` after.
**Warning signs:** `git status` shows `??` prefix, not `M` or `D`.

### Pitfall 2: Deleting _longform JSON Without Understanding backfill.py
**What goes wrong:** Developer deletes `_longform_enriched.json` and `_longform_metrics.json`, then tries to run `python -m tools.youtube_analytics.backfill` and gets an error dict with `'No JSON pre-fetch found'`.
**Why it happens:** backfill.py Stage 1 depends on these files for its primary import path.
**How to avoid:** Document in commit that Stage 1 import is intentionally disabled (data already in DB). The fallback behavior is by design.

### Pitfall 3: Removing a Function While Leaving Stale Import in __init__.py
**What goes wrong:** A function is deleted from a module but still exported in `__init__.py`, causing `ImportError` at module load time.
**Why it happens:** `__init__.py` files were added in Phase 48 and explicitly import symbols.
**How to avoid:** After removing any function, check the module's `__init__.py` (and `tools/discovery/__init__.py`) for stale exports.

### Pitfall 4: Missing Skill References After Deleting prompt_evaluation.py
**What goes wrong:** The two skill files still instruct Claude to run `tools/prompt_evaluation.py channel_voice_check`, causing confusion in production sessions.
**Why it happens:** Skill files are not automatically updated when source files are deleted.
**How to avoid:** If prompt_evaluation.py is deleted, immediately edit `.claude/skills/notebooklm-prompt-generator.md:666` and `.claude/skills/script-reviewer.md:655` to remove the stale references.

### Pitfall 5: Adding Overly Broad .gitignore Pattern
**What goes wrong:** Adding `_*.json` to .gitignore accidentally suppresses legitimate JSON files elsewhere.
**Why it happens:** Glob patterns in .gitignore apply to the whole repo unless scoped to a path.
**How to avoid:** Use path-scoped patterns: `tools/youtube_analytics/_longform_*.json` and `tools/discovery/backups/` rather than broad `_*.json`.

---

## Code Examples

### Correct Deletion of Untracked Files (Windows bash)
```bash
# These files are UNTRACKED — use rm, not git rm
rm "G:/History vs Hype/tools/youtube_analytics/_csv_backfill.py"
rm "G:/History vs Hype/tools/youtube_analytics/_competitor_fetch.py"
rm "G:/History vs Hype/tools/youtube_analytics/_backfill_ids.txt"
rm "G:/History vs Hype/tools/youtube_analytics/_longform_all.json"
rm "G:/History vs Hype/tools/youtube_analytics/_longform_enriched.json"
rm "G:/History vs Hype/tools/youtube_analytics/_longform_ids.json"
rm "G:/History vs Hype/tools/youtube_analytics/_longform_metrics.json"
# Verify clean
cd "G:/History vs Hype" && git status tools/youtube_analytics/
```

### Caller-Count Analysis Pattern
```bash
# Count callers of a function across the codebase (exclude definition line)
grep -rn "function_name" "G:/History vs Hype/tools/" --include="*.py" | grep -v "def function_name\|#"
# Zero results = dead code
```

### Import Smoke Test After Deletion
```bash
cd "G:/History vs Hype"
python -c "from tools.youtube_analytics.patterns import generate_topic_report; print('OK')"
python -c "from tools.discovery.database import KeywordDB; print('OK')"
```

### .gitignore Addition for Scratch File Patterns
```
# Scratch/temporary files in youtube_analytics (backfill artifacts)
tools/youtube_analytics/_longform_*.json
tools/youtube_analytics/_backfill_ids.txt
# Database migration backups (auto-generated, not source)
tools/discovery/backups/
```

---

## Audit Scope Recommendations

### Modules Warranting Full Public-Function Audit

| Module | Lines | Reason to Audit | Expected Outcome |
|--------|-------|----------------|------------------|
| `tools/youtube_analytics/patterns.py` | 2,070 | Large, long history; references internal self-imports from early milestones | A few helper functions may have zero external callers — audit functions not called by `__main__` block |
| `tools/discovery/database.py` | 2,927 | 55+ methods; spans v1.0 through v5.0; some early CRUD methods might be superseded | All checked methods found to have callers; focus on `_ensure_*` private methods for completeness |
| `tools/prompt_evaluation.py` | 953 | No callers in Python code; only referenced in skill markdown files; references deleted file paths | Decision: delete (see Finding 4) |

### Modules to Skip (Low Risk)
- `analyze.py` (1,429 lines) — actively called by `/analyze` command
- `feedback_queries.py` (1,112 lines) — actively called by feedback pipeline
- `technique_library.py` (1,085 lines) — actively called by transcript_analyzer
- `backfill.py` (971 lines) — actively called by `/analyze` and analytics pipeline
- All modules under 700 lines — low complexity, lower refactor history

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Archive dead files in `_ARCHIVE/` subfolder | `git rm` and rely on git history | Phase 49 decision | Cleaner working tree; git log recovers any file |
| Keep scratch files with `_` prefix | Delete them; add .gitignore patterns | Phase 49 decision | Prevents `??` entries polluting git status |

**Pre-satisfied:**
- `datetime.utcnow()`: Already migrated to `datetime.now(timezone.utc)` — CLEAN-03 requires no code changes, just a note in the plan marking it done.

---

## Open Questions

1. **Which patterns.py functions have zero external callers?**
   - What we know: The module has 20+ top-level functions. The `/patterns` command invokes it via `python -m tools.youtube_analytics.patterns` with CLI flags, which calls the `generate_*_report()` functions through `__main__`.
   - What's unclear: Whether helper functions like `collect_video_data()`, `parse_analysis_file()`, `find_project_folder_for_video()`, `get_youtube_metadata()` have callers outside patterns.py itself.
   - Recommendation: During execution, run grep caller check for each function. Functions only called within patterns.py (self-referential) count as having callers — don't delete them.

2. **Does backups/ directory need to stay for future fresh installs?**
   - What we know: `_backup_database()` and `_ensure_variant_tables()` create the directory during v27 migration. Current production DB is at v29.
   - What's unclear: Whether a fresh install scenario would re-trigger the v27 migration (unlikely — schema starts at v27+ now).
   - Recommendation: Add to `.gitignore`. The directory auto-creates on first migration run if ever needed. The two existing `.db` backup files in it can be deleted.

---

## Sources

### Primary (HIGH confidence)
- Direct file inspection: `tools/youtube_analytics/backfill.py` lines 73-95, 149-177 — confirmed runtime dependency on _longform JSON files
- Direct file inspection: `tools/discovery/database.py` lines 1466-1543 — confirmed backups/ directory creation during v27 migration
- `git status` output — confirmed all 7 dead files are **untracked** (not tracked), requiring `rm` not `git rm`
- Grep caller analysis across all tools/ Python files — confirmed patterns.py is used by /patterns command; database.py methods all have active callers

### Secondary (MEDIUM confidence)
- `.claude/skills/notebooklm-prompt-generator.md:666` and `.claude/skills/script-reviewer.md:655` — skill references to prompt_evaluation.py (active but pointing to non-existent CLI flag)
- `.planning/audits/49-dead-code.md` — audit pre-work (note: paths use old `youtube-analytics` hyphen, corrected to `youtube_analytics` after Phase 48 rename)

---

## Metadata

**Confidence breakdown:**
- CLEAN-01 (dead file deletion): HIGH — all 7 files confirmed present, untracked, safely removable
- CLEAN-02 (unused functions): MEDIUM — database.py methods all appear to have callers; patterns.py audit needed during execution; prompt_evaluation.py delete decision is HIGH confidence
- CLEAN-03 (datetime.utcnow): HIGH — zero occurrences confirmed, requirement pre-satisfied

**Research date:** 2026-02-25
**Valid until:** Stable — no external dependencies; valid until codebase changes
