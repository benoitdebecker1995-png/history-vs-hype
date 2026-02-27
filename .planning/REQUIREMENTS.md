# Requirements: History vs Hype Workspace

**Defined:** 2026-02-24
**Core Value:** Every video shows sources on screen

## v5.1 Requirements

Requirements for v5.1 Codebase Hardening. Each maps to roadmap phases.

### Error Handling

- [x] **ERR-01**: All bare `except:` and `except Exception: pass` replaced with specific exception types and error dict returns
- [x] **ERR-02**: All tool modules return `{'error': msg}` on failure (not None, not exceptions for expected errors)
- [x] **ERR-03**: Error dicts include structured context (module name, operation, details)

### Logging

- [x] **LOG-01**: Logging module configured with module-level loggers across all tool directories
- [x] **LOG-02**: All print() calls in tool modules replaced with appropriate log level (DEBUG/INFO/WARNING/ERROR)
- [x] **LOG-03**: Log output goes to stderr with configurable verbosity (--verbose/--quiet flags)

### Testing

- [ ] **TEST-01**: pytest configuration at repo root with conftest.py and test discovery
- [ ] **TEST-02**: Integration test for discovery pipeline (orchestrator end-to-end)
- [ ] **TEST-03**: Integration test for intel pipeline (refresh, query, KB operations)
- [ ] **TEST-04**: Integration test for translation pipeline (translate, cross-check, annotate)
- [ ] **TEST-05**: Integration test for production pipeline (parser, edit guide, metadata)
- [ ] **TEST-06**: Integration test for analytics pipeline (backfill, analyze, patterns)
- [ ] **TEST-07**: DB fixtures for test setup/teardown (in-memory SQLite)

### Package Structure

- [x] **PKG-01**: `__init__.py` files added to all tool directories
- [x] **PKG-02**: All `sys.path.insert` hacks eliminated via proper package imports
- [x] **PKG-03**: Tools importable as `tools.discovery`, `tools.intel`, etc.

### Dependencies

- [x] **DEP-01**: `pyproject.toml` at repo root with all production dependencies pinned
- [x] **DEP-02**: Optional dependency groups defined (dev, test)
- [x] **DEP-03**: All actually-imported packages listed (feedparser, anthropic, spacy, etc.)

### Database

- [ ] **DB-01**: intel.db has PRAGMA user_version schema tracking matching keywords.db pattern
- [ ] **DB-02**: analytics.db has PRAGMA user_version schema tracking
- [ ] **DB-03**: Migration functions are atomic (transaction-wrapped, rollback on failure)

### CLI

- [x] **CLI-01**: All CLI entry points use argparse with --help
- [x] **CLI-02**: Consistent error output format across all tools (stderr, exit code 1)
- [x] **CLI-03**: Standard --verbose/--quiet flags wired to logging levels

### Cleanup

- [x] **CLEAN-01**: Dead code files removed (_csv_backfill.py, _competitor_fetch.py, _longform_*.json, _backfill_ids.txt)
- [x] **CLEAN-02**: Unused functions identified and removed from active modules
- [x] **CLEAN-03**: datetime.utcnow() deprecation warnings fixed

## Future Requirements

### Linting & Formatting

- **LINT-01**: Pre-commit hooks for linting (flake8/ruff, isort, black)
- **LINT-02**: Consistent docstring format across modules

### Configuration

- **CFG-01**: Central config.yaml or settings module replacing hardcoded constants
- **CFG-02**: Externalized voice pattern count, WPM rate, confidence thresholds

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full unit test coverage | Diminishing returns for solo creator tooling — integration tests provide safety net |
| CI/CD pipeline | No deployment target; tests run locally |
| Type checking (mypy) | Large retrofit cost, low ROI for scripts |
| Code reformatting (black) | Cosmetic churn on 47K lines, deferred to v6.0 |
| Performance optimization | Not a bottleneck; correctness first |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| ERR-01 | Phase 50 | Complete |
| ERR-02 | Phase 50 | Complete |
| ERR-03 | Phase 50 | Complete |
| LOG-01 | Phase 51 | Complete |
| LOG-02 | Phase 51 | Complete |
| LOG-03 | Phase 51 | Complete |
| TEST-01 | Phase 53 | Pending |
| TEST-02 | Phase 53 | Pending |
| TEST-03 | Phase 53 | Pending |
| TEST-04 | Phase 53 | Pending |
| TEST-05 | Phase 53 | Pending |
| TEST-06 | Phase 53 | Pending |
| TEST-07 | Phase 53 | Pending |
| PKG-01 | Phase 48 | Complete |
| PKG-02 | Phase 48 | Complete |
| PKG-03 | Phase 48 | Complete |
| DEP-01 | Phase 48 | Complete |
| DEP-02 | Phase 48 | Complete |
| DEP-03 | Phase 48 | Complete |
| DB-01 | Phase 52 | Pending |
| DB-02 | Phase 52 | Pending |
| DB-03 | Phase 52 | Pending |
| CLI-01 | Phase 51 | Complete |
| CLI-02 | Phase 51 | Complete |
| CLI-03 | Phase 51 | Complete |
| CLEAN-01 | Phase 49 | Complete |
| CLEAN-02 | Phase 49 | Complete |
| CLEAN-03 | Phase 49 | Complete |

**Coverage:**
- v5.1 requirements: 28 total
- Mapped to phases: 28
- Unmapped: 0

---
*Requirements defined: 2026-02-24*
*Last updated: 2026-02-24 after roadmap creation — all 28 requirements mapped*
