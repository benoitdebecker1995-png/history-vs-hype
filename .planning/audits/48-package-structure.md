# Phase 48 Audit: Package Structure & Dependencies

## 1. Missing __init__.py Files

These directories have .py files but NO __init__.py:

| Directory | Status | Action |
|-----------|--------|--------|
| `tools/` (root) | Missing | Add — exposes sub-packages |
| `tools/youtube-analytics/` | Missing | Add — 30+ modules, most-imported package |
| `tools/script-checkers/` | Missing | Add — has sub-dirs with __init__.py but root missing |
| `tools/script-checkers/tests/` | Missing | Add — pytest needs it for discovery |

**Already have __init__.py (no action):**
- tools/discovery/, tools/production/, tools/intel/, tools/translation/
- tools/document_discovery/, tools/dashboard/, tools/research/
- tools/script-checkers/checkers/, tools/script-checkers/voice/
- tools/history-clip-tool/src/ (full tree)

## 2. sys.path.insert Hacks (37 occurrences in 27 files)

### Cross-directory imports (the main problem):

| File | Line | Imports From | Clean Import |
|------|------|-------------|--------------|
| `youtube-analytics/analyze.py` | 55 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/analyze.py` | 87 | production/ | `from tools.production import parser` |
| `youtube-analytics/backfill.py` | 46 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/backfill.py` | 55 | youtube-analytics/ (self) | Remove (use relative) |
| `youtube-analytics/benchmarks.py` | 27 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/feedback.py` | 27-28 | youtube-analytics/, discovery/ | Relative + `from tools.discovery` |
| `youtube-analytics/feedback_queries.py` | 31 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/feedback_parser.py` | 320 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/pattern_extractor.py` | 42 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/pattern_synthesizer_v2.py` | 39 | youtube-analytics/ (self) | Remove (use relative) |
| `youtube-analytics/performance.py` | 46 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/performance_report.py` | 39 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/playbook_synthesizer.py` | 34 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/retention_mapper.py` | 26 | production/ | `from tools.production import parser` |
| `youtube-analytics/retention_scorer.py` | 41, 651 | discovery/, production/ | Both cross-package |
| `youtube-analytics/topic_strategy.py` | 38 | discovery/ | `from tools.discovery import database` |
| `youtube-analytics/variants.py` | 29 | discovery/ | `from tools.discovery import database` |
| `discovery/diagnostics.py` | 35 | youtube-analytics/ | `from tools.youtube_analytics import ...` |
| `discovery/recommender.py` | 37, 53 | youtube-analytics/, root | Cross-package |
| `production/parser.py` | 391 | project root | Add tools to path via pyproject.toml |
| `translation/structure_detector.py` | 110 | document_discovery/ | `from tools.document_discovery import ...` |
| `translation/smoke_test.py` | 24 | translation/ (self) | Remove (use relative) |
| `translation/cli.py` | 36 | translation/ (self) | Remove (use relative) |
| `document_discovery/cli.py` | 27 | document_discovery/ (self) | Remove (use relative) |
| `discovery/backfill_gaps.py` | 27 | discovery/ (self) | Remove (use relative) |
| `discovery/orchestrator.py` | 33 | discovery/ (self) | Remove (use relative) |
| `script-checkers/checkers/pacing.py` | 27 | tools/ root | `from tools.discovery import database` |
| `script-checkers/tests/test_pacing.py` | 26 | script-checkers/ | `from tools.script_checkers.checkers import pacing` |

### Self-imports (module importing its own package — fixable with relative imports):
- backfill.py:55, pattern_synthesizer_v2.py:39, smoke_test.py:24, cli.py:36 (translation), cli.py:27 (document_discovery), backfill_gaps.py:27, orchestrator.py:33

### Dead file hacks (will be removed in Phase 49):
- _competitor_fetch.py:27, _csv_backfill.py:19+24

## 3. Import Dependency Graph

```
youtube-analytics/ ──imports──> discovery/database.py (14 files!)
youtube-analytics/ ──imports──> production/parser.py (3 files)
discovery/ ──imports──> youtube-analytics/ (2 files: diagnostics, recommender)
translation/ ──imports──> document_discovery/ (1 file: structure_detector)
script-checkers/ ──imports──> discovery/database.py (1 file: pacing)
production/ ──imports──> tools root (1 file: parser)
```

**Critical dependency:** `discovery/database.py` is imported by 14+ files across 3 packages. This is the most-imported module.

**Note:** `youtube-analytics` has a hyphen — Python can't import `tools.youtube-analytics`. Options:
1. Rename to `tools/youtube_analytics/` (breaking, but clean)
2. Keep hyphen and use `__init__.py` with explicit path registration

## 4. Third-Party Dependencies

### Required (always imported):
| Package | Used By | Listed In |
|---------|---------|-----------|
| `google-api-python-client` | auth.py, metrics.py, retention.py, comments.py, channel_averages.py | youtube-analytics/requirements.txt |
| `google-auth-oauthlib` | auth.py | youtube-analytics/requirements.txt |
| `google-auth-httplib2` | auth.py | youtube-analytics/requirements.txt |

### Required (imported with fatal error if missing):
| Package | Used By | Listed In |
|---------|---------|-----------|
| `anthropic` | notebooklm_bridge.py | NOT listed anywhere |

### Optional (behind try/except ImportError):
| Package | Used By | Feature Flag | Listed In |
|---------|---------|-------------|-----------|
| `feedparser` | intel/algo_scraper.py, intel/competitor_tracker.py | FEEDPARSER_AVAILABLE | NOT listed |
| `spacy` | production/entities.py, script-checkers/flow.py | RuntimeError on missing | script-checkers/requirements.txt |
| `textstat` | script-checkers/pacing.py | RuntimeError on missing | script-checkers/requirements.txt |
| `srt` | script-checkers/voice/corpus_builder.py | ImportError handled | script-checkers/requirements.txt |
| `pyppeteer` | discovery/autocomplete.py | PYPPETEER_AVAILABLE | discovery/requirements.txt |
| `pyppeteer-stealth` | discovery/autocomplete.py | With pyppeteer | discovery/requirements.txt |
| `scrapetube` | discovery/competition.py | SCRAPETUBE_AVAILABLE | NOT listed |
| `trendspyg` | discovery/trends.py | TRENDSPYG_AVAILABLE | NOT listed |
| `requests` | intel/algo_scraper.py, translation/cross_checker.py | REQUESTS_AVAILABLE | NOT listed |
| `googletrans` | translation/cross_checker.py | GOOGLETRANS_AVAILABLE | NOT listed |
| `deep-translator` | translation/cross_checker.py | DEEP_TRANSLATOR_AVAILABLE | NOT listed |
| `imagehash` | youtube-analytics/variants.py | IMAGEHASH_AVAILABLE | NOT listed |
| `jinja2` | discovery/orchestrator.py | Fallback to simple report | NOT listed |

## 5. Existing Dependency Files

### tools/discovery/requirements.txt
```
pyppeteer>=1.0.2
pyppeteer-stealth>=2.7.4
```

### tools/youtube-analytics/requirements.txt
```
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
```

### tools/script-checkers/requirements.txt
```
spacy>=3.8
textstat>=0.7.3
srt>=3.5.0
```

### tools/history-clip-tool/requirements.txt
Full pinned deps (separate tool, not in scope).

**No pyproject.toml exists anywhere.**

## 6. youtube-analytics Hyphen Problem

The directory `tools/youtube-analytics/` has a hyphen which is illegal in Python package names. Two options:

**Option A: Rename to youtube_analytics/** (recommended)
- Clean Python imports: `from tools.youtube_analytics import analyze`
- Requires updating all 30+ files and all slash command references
- One-time pain, permanent benefit

**Option B: Keep hyphen, use importlib**
- Add `tools/__init__.py` with custom import logic
- More complex, less standard
- Risk of confusing future developers

**Recommendation:** Option A. The rename is mechanical and the planner can script it.
