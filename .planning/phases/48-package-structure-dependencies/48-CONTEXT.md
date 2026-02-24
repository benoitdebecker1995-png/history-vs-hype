# Phase 48: Package Structure & Dependencies - Context

**Gathered:** 2026-02-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Make all tool packages properly structured Python packages with explicit dependency declarations. Rename hyphenated directories, add missing __init__.py files, replace all sys.path hacks with proper imports, create a single pyproject.toml, and remove per-package requirements.txt files.

</domain>

<decisions>
## Implementation Decisions

### Rename Strategy
- Rename `youtube-analytics/` → `youtube_analytics/` AND `script-checkers/` → `script_checkers/` in the same pass
- One atomic commit: directory rename + all reference updates (Python imports, .claude/commands/, skill files, CLAUDE.md, etc.)
- Sweep ALL references — Python files, command files, skill files, documentation. Nothing left pointing to old names.

### pyproject.toml
- Single root `pyproject.toml` at repo root (not per-package)
- Full metadata: name `history-vs-hype-tools`, version `5.1.0`, `python_requires >= "3.11"`
- Extras groups by feature: `[youtube]` (google-api), `[intel]` (feedparser, requests), `[nlp]` (spacy, textstat), `[discovery]` (pyppeteer), etc.
- `pip install -e .` installs core deps; `pip install -e .[youtube,intel,nlp]` adds optional groups
- Remove all per-package `requirements.txt` files (discovery/, youtube-analytics/, script-checkers/) — pyproject.toml is single source of truth

### Import Convention
- **Cross-package:** Absolute imports from tools root: `from tools.discovery.database import get_db`
- **Same-package:** Relative imports: `from .metrics import get_metrics`
- **Invocation:** Module-only: `python -m tools.youtube_analytics.backfill`. Update command files to use `-m` invocation. No more direct `python tools/youtube_analytics/backfill.py`.
- **database.py stays in discovery** — other packages import `from tools.discovery.database`. No shared/ package (that's scope creep).

### __init__.py Files
- All __init__.py files are **empty** (just mark directories as packages)
- No re-exports — imports are always explicit to the module level
- Add missing __init__.py to: `tools/`, `tools/youtube_analytics/`, `tools/script_checkers/`, `tools/script_checkers/tests/`

### Circular Import Handling
- Use **lazy imports** (import inside the function) for the youtube_analytics ↔ discovery cycle
- Specifically: `discovery/diagnostics.py` and `discovery/recommender.py` import youtube_analytics at function level, not module level
- No architectural restructuring needed

### Feature Flag Imports
- **Keep existing try/except ImportError pattern** with feature flags (FEEDPARSER_AVAILABLE, SPACY_AVAILABLE, etc.)
- pyproject.toml extras make them installable, but code continues to handle their absence gracefully

### Claude's Discretion
- Exact extras group names and composition
- Order of operations within the atomic rename commit
- How to handle edge cases in the 37 sys.path hacks
- Migration safety: any intermediate verification steps

</decisions>

<specifics>
## Specific Ideas

- The rename should be mechanical and scriptable — planner can use sed/grep patterns
- `discovery/database.py` is imported by 14+ files across 3 packages — this is the critical import to get right
- Self-imports (7 files importing their own package via sys.path) should become relative imports
- Dead file hacks (_competitor_fetch.py, _csv_backfill.py) will be removed in Phase 49, but their sys.path lines can be left as-is for now

</specifics>

<deferred>
## Deferred Ideas

- "Run knowledge tools to get better understanding about making good videos" — noted for content workflow, not this phase
- Moving database.py to a shared/ package — future architectural cleanup
- Reorganizing package structure beyond rename — future phase

</deferred>

---

*Phase: 48-package-structure-dependencies*
*Context gathered: 2026-02-24*
