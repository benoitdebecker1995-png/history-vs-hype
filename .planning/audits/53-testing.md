# Phase 53 Audit: Integration Testing

## 1. Existing Test Files (8 files)

| File | What It Tests | Runner | Status |
|------|--------------|--------|--------|
| `script-checkers/tests/test_pacing.py` | PacingChecker | unittest-style, standalone | Has sys.path hack |
| `youtube-analytics/test_connection.py` | YouTube API auth | standalone | Requires credentials |
| `youtube-analytics/test_retention_mapper.py` | RetentionMapper | unittest-style | Has sys.path hack |
| `youtube-analytics/test_section_diagnostics.py` | SectionDiagnostics | standalone | Has sys.path hack |
| `youtube-analytics/test_retention_scorer.py` | RetentionScorer | standalone | Has sys.path hack |
| `youtube-analytics/test_transcript_analyzer.py` | TranscriptAnalyzer | standalone | Has sys.path hack |
| `youtube-analytics/test_pattern_synthesizer_v2.py` | PatternSynthesizer | standalone | Has sys.path hack |
| `translation/smoke_test.py` | Translation pipeline | standalone | E2E smoke test |

**All existing tests use sys.path hacks** — Phase 48 (package structure) must complete first.

## 2. pytest Configuration

**Currently missing:**
- No `pytest.ini` or `pyproject.toml [tool.pytest]`
- No `conftest.py` anywhere
- No test discovery configuration
- No fixtures for database setup/teardown

**Needed:**
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## 3. Pipeline Entry Points & Test Strategy

### Discovery Pipeline
- **Entry:** `tools/discovery/orchestrator.py` → `OpportunityOrchestrator.analyze(keyword)`
- **Inputs:** keyword string, database path
- **External deps:** pyppeteer (autocomplete), Google Trends API (trends)
- **Mockable:** autocomplete results, trend data, database queries
- **Fixture:** Pre-populated keywords.db with test data
- **Test:** `orchestrator.analyze("test topic")` returns structured opportunity dict

### Intel Pipeline
- **Entry:** `tools/intel/refresh.py` → 10-phase refresh pipeline
- **Inputs:** None (reads from RSS feeds, web sources)
- **External deps:** RSS feeds (feedparser), web scraping, YouTube API
- **Mockable:** feedparser.parse(), HTTP requests
- **Fixture:** Sample RSS XML, sample competitor data
- **Test:** `kb_store.query("algorithm")` returns results after mock refresh
- **Graceful degradation:** Already handles missing feedparser, missing API auth

### Translation Pipeline
- **Entry:** `tools/translation/cli.py` → full pipeline or individual steps
- **Inputs:** Source text file, target language
- **External deps:** Claude API (for translation), DeepL (for cross-check)
- **Mockable:** LLM response (fixed translation output)
- **Fixture:** Short French legal text (5-10 lines), expected translation
- **Test:** `translate + cross_check + annotate` chain completes, output has required sections
- **Existing:** smoke_test.py already tests imports and basic instantiation

### Production Pipeline
- **Entry:** `tools/production/parser.py --package`
- **Inputs:** Script markdown file
- **External deps:** spaCy model (for entity extraction)
- **Mockable:** spaCy NLP (or use test without entity extraction)
- **Fixture:** Minimal script markdown (3 sections, 200 words)
- **Test:** `parser.parse_script(fixture)` returns sections; `editguide`, `metadata`, `broll` all generate output

### Analytics Pipeline
- **Entry:** `tools/youtube-analytics/backfill.py` → backfill POST-PUBLISH files
- **Inputs:** POST-PUBLISH-ANALYSIS.md file, video ID
- **External deps:** YouTube Analytics API (for live data)
- **Mockable:** API responses, file system
- **Fixture:** Sample POST-PUBLISH-ANALYSIS.md, sample API response JSON
- **Test:** `backfill_from_files(fixture_dir)` populates in-memory DB; `patterns.analyze()` returns insights

## 4. Fixture Requirements

### Minimal keyword database (tests/fixtures/test_keywords.db)
```sql
INSERT INTO keywords (keyword, search_volume, competition) VALUES ('test topic', 1000, 0.5);
INSERT INTO video_performance (video_id, title, views) VALUES ('test123', 'Test Video', 1000);
```

### Minimal script fixture (tests/fixtures/test_script.md)
```markdown
## Introduction
This is a test script about historical events.

## Section 1: The Treaty
According to Smith in *The History*, page 42, the treaty was signed in 1916.

## Conclusion
This matters because it still affects borders today.
```

### Minimal POST-PUBLISH fixture (tests/fixtures/test_post_publish.md)
```markdown
# Post-Publish Analysis: Test Video

**Video ID:** test123
**Published:** 2026-01-15
**Views (48h):** 500
**CTR:** 5.2%
**Average View Duration:** 4:30
**Retention:** 35%
```

### Minimal translation fixture (tests/fixtures/test_french.txt)
```
Article 1. - Les personnes ci-après sont considérées comme juives.
```

### Minimal RSS fixture (tests/fixtures/test_rss.xml)
```xml
<?xml version="1.0"?>
<feed><entry><title>Test Video</title><published>2026-01-01</published></entry></feed>
```

## 5. Mocking Strategy

| Service | Mock Method | Graceful Degradation? |
|---------|------------|----------------------|
| YouTube Analytics API | `unittest.mock.patch` on auth.build() | Yes — returns empty data |
| YouTube Data API | `unittest.mock.patch` on googleapiclient | Yes — RSS fallback |
| RSS feeds | `unittest.mock.patch` on feedparser.parse() | Yes — FEEDPARSER_AVAILABLE flag |
| Claude API | `unittest.mock.patch` on anthropic client | No — translation fails |
| spaCy NLP | `unittest.mock.patch` on spacy.load() | Partial — entities empty |
| pyppeteer | `unittest.mock.patch` on browser launch | Yes — PYPPETEER_AVAILABLE flag |
| File system | `tmp_path` pytest fixture | N/A |
| SQLite | `:memory:` databases | N/A |

### In-memory database strategy:
```python
@pytest.fixture
def test_db():
    """Create in-memory keyword database with test data."""
    import sqlite3
    conn = sqlite3.connect(':memory:')
    # Execute schema.sql
    # Insert test data
    yield conn
    conn.close()
```

## 6. Proposed Test Structure

```
tests/
├── conftest.py              # Shared fixtures (db, script, paths)
├── fixtures/
│   ├── test_keywords.db     # Pre-populated test database
│   ├── test_script.md       # Minimal script
│   ├── test_post_publish.md # Minimal analysis
│   ├── test_french.txt      # Translation source
│   └── test_rss.xml         # Mock RSS feed
├── test_discovery.py        # Discovery pipeline integration
├── test_intel.py            # Intel pipeline integration
├── test_translation.py      # Translation pipeline integration
├── test_production.py       # Production pipeline integration
└── test_analytics.py        # Analytics pipeline integration
```

## Summary

| Pipeline | Entry Point | External Deps | Mock Complexity | Existing Tests |
|----------|------------|---------------|-----------------|---------------|
| Discovery | orchestrator.analyze() | pyppeteer, Google Trends | Medium | None |
| Intel | refresh + query | feedparser, HTTP, YouTube API | Medium | None |
| Translation | cli.py full | Claude API, DeepL | High (LLM) | smoke_test.py |
| Production | parser --package | spaCy | Low | None |
| Analytics | backfill + analyze | YouTube API | Medium | 5 unit tests |
