# Phase 53: Integration Testing - Context

**Gathered:** 2026-02-28
**Status:** Ready for planning
**Source:** User decisions from conversation

<domain>
## Phase Boundary

This phase adds pytest infrastructure and integration tests for all 5 major pipelines. It also migrates 8 existing test files to remove sys.path hacks.

</domain>

<decisions>
## Implementation Decisions

### Plan Structure
- **2 plans total**
- Plan 1 (Wave 1): pytest config + conftest.py + fixtures + migrate existing 8 tests (TEST-01, TEST-07)
- Plan 2 (Wave 2, depends on Plan 1): all 5 pipeline integration tests (TEST-02 through TEST-06)

### Existing Test Migration
- Remove sys.path hacks from all 8 existing test files
- Move tests into tests/ directory structure discoverable by pytest
- Phase 48 already fixed package structure — imports should work cleanly

### Test Scope
- **Smoke tests** — verify each pipeline runs end-to-end with mocked externals
- ~5-10 test functions per pipeline
- No edge case or full coverage testing — just regression catch

### Claude's Discretion
- Exact mock strategy per pipeline (unittest.mock vs pytest fixtures)
- Fixture file formats and content
- conftest.py shared fixture organization
- Whether to use tmp_path or :memory: databases

</decisions>

<specifics>
## Specific Ideas

- Use in-memory SQLite for database fixtures (from audit)
- Mock external services: YouTube API, RSS feeds, Claude API, pyppeteer, spaCy
- Fixture files from audit: test_keywords.db, test_script.md, test_post_publish.md, test_french.txt, test_rss.xml
- pyproject.toml [tool.pytest.ini_options] for configuration

</specifics>

<deferred>
## Deferred Ideas

- Full coverage testing (edge cases, error paths, boundary conditions)
- CI/CD integration
- Performance benchmarks

</deferred>

---

*Phase: 53-integration-testing*
*Context gathered: 2026-02-28 via user conversation*
