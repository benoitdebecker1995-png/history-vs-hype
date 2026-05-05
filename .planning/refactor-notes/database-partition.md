# Database Partition Design (Phase H)

**Status:** Design-only. No code changes in this step.

3,023 lines of `tools/discovery/database.py` → 3 focused store classes + lifecycle management seam.

---

## Method-to-Store Mapping

### KeywordStore (16 methods)
Owns the keyword discovery lifecycle and intent classification.

| Method | Responsibility |
|--------|-----------------|
| `add_keyword` | Insert/update keywords |
| `get_keyword` | Fetch keyword by exact match |
| `search_keywords` | Pattern search on keywords |
| `get_keywords_by_source` | Filter keywords by source (autocomplete, vidiq, etc.) |
| `get_keywords_by_intent` | Join keywords + intents table |
| `set_intent` | Store intent classification + confidence |
| `add_performance` | Track keyword performance in videos |
| `get_keyword_stats` | Aggregate counts: total keywords, by source, with intents, with performance |
| `add_opportunity_score` | Historical opportunity records |
| `get_opportunity_score` | Fetch cached opportunity score with age check |
| `save_opportunity_score` | Save final score + lifecycle transition (DISCOVERED → ANALYZED) |
| `store_production_constraints` | Store animation requirements + document score |
| `get_production_constraints` | Fetch constraints with age check |
| `set_lifecycle_state` | Validate + transition keyword state (DISCOVERED → ANALYZED → ...) |
| `get_lifecycle_state` | Query current state (default DISCOVERED) |
| `get_keywords_by_lifecycle` | Filter keywords by state |

**Tables owned:**
- `keywords` (read/write)
- `keyword_intents` (read/write)
- `keyword_performance` (read/write)
- `opportunity_scores` (read/write)
- `lifecycle_history` (read/write)

**Tables read (no write):**
- None (self-contained)

---

### IntentClassifier (4 methods)
Owns competitor intelligence and content classification.

| Method | Responsibility |
|--------|-----------------|
| `add_competitor_video` | Track competitor video appearances for a keyword |
| `get_competition_count` | Aggregate video + channel count with freshness check |
| `update_video_classification` | Store format (animation/documentary), angles, quality tier |
| `get_classified_videos` | Query with optional format/quality filters + age validation |

**Tables owned:**
- `competitor_channels` (read/write)
- `competitor_videos` (read/write)

**Tables read (no write):**
- `keywords` (resolve keyword_id references)

---

### PerformanceTracker (21 methods)
Owns video performance metrics, variant testing, and CTR analysis.

| Method | Responsibility |
|--------|-----------------|
| `add_video_performance` | Insert/update video metadata + performance metrics |
| `get_video_performance` | Fetch full video record |
| `search_video_performance_by_title` | Fuzzy match on title prefix |
| `get_all_video_performance` | Paginated list with limit |
| `get_performance_by_topic` | Filter by topic_type (territorial, ideological, etc.) |
| `get_performance_by_angle` | Filter by angle tags (legal, historical, etc.) |
| `get_top_converters` | Rank by conversion_rate DESC |
| `add_thumbnail_variant` | Register thumbnail A/B test variant |
| `add_title_variant` | Register title A/B test variant |
| `add_ctr_snapshot` | Record monthly CTR snapshot |
| `get_thumbnail_variants` | List all thumbnails for a video |
| `get_title_variants` | List all titles for a video |
| `get_ctr_snapshots` | List all CTR history for a video |
| `get_variant_summary` | Count thumbnails/titles/snapshots |
| `get_latest_ctr` | Most recent CTR snapshot for a video |
| `get_variant_ctr_summary` | Aggregate CTR by variant (attribution analysis) |
| `get_channel_ctr_benchmarks` | Channel-wide CTR stats by category |
| `store_video_feedback` | Store retention drop + observations + actionable |
| `get_video_feedback` | Fetch feedback record |
| `get_feedback_by_topic` | List videos with feedback by category |
| `has_feedback` | Boolean check for feedback existence |

**Tables owned:**
- `video_performance` (read/write)
- `thumbnail_variants` (read/write)
- `title_variants` (read/write)
- `ctr_snapshots` (read/write)
- `section_feedback` (read/write)

**Tables read (no write):**
- `keywords` (resolve video_id references, if needed for topic context)

---

### AmbiguousReview (7 methods)
Infrastructure concerns: initialization, cleanup, schema versioning, trend tracking.

**Methods pending decision:**

| Method | Status | Rationale |
|--------|--------|-----------|
| `init_database` | TBD | Database initialization — does not fit store pattern. Option 1: factory method on a MasterStore. Option 2: standalone function. Decision pending. |
| `close` | TBD | Connection cleanup — does not fit store pattern. Option 1: implement `__del__` on each store. Option 2: make stores auto-close via context manager. Decision pending. |
| `add_trend` | TBD | Trend tracking is demand research — separate domain from keywords/performance. Option 1: new TrendStore. Option 2: move to a separate module `demand_research.py`. Decision pending. |
| `get_cached_trend` | TBD | See `add_trend`. |
| `get_latest_trend` | TBD | See `add_trend`. |
| `get_schema_version` | TBD | Schema migration is infrastructure. Option 1: new SchemaManager. Option 2: keep as module-level function. Decision pending. |
| `set_schema_version` | TBD | See `get_schema_version`. |

**Note:** These 7 methods are NOT assigned to KeywordStore/IntentClassifier/PerformanceTracker. They require architectural discussion before coding begins (H3+).

---

## Shared Schema & Table Ownership

```
TABLE                    | Owned by          | Read by          | Purpose
─────────────────────────┼───────────────────┼──────────────────┼──────────────────
keywords                 | KeywordStore      | IntentClassifier  | Keyword master table
keyword_intents          | KeywordStore      | —                 | Search intent classification
keyword_performance      | KeywordStore      | —                 | Keyword-video usage tracking
opportunity_scores       | KeywordStore      | —                 | Historical opportunity calc
lifecycle_history        | KeywordStore      | —                 | Audit trail for state transitions
─────────────────────────┼───────────────────┼──────────────────┼──────────────────
competitor_channels      | IntentClassifier  | —                 | Competitor metadata
competitor_videos        | IntentClassifier  | —                 | Competitor video tracking
─────────────────────────┼───────────────────┼──────────────────┼──────────────────
video_performance        | PerformanceTracker| —                 | Video metrics (views, CTR, etc.)
thumbnail_variants       | PerformanceTracker| —                 | A/B test variants
title_variants           | PerformanceTracker| —                 | A/B test variants
ctr_snapshots            | PerformanceTracker| —                 | Monthly CTR history
section_feedback         | PerformanceTracker| —                 | Retention feedback by section
─────────────────────────┼───────────────────┼──────────────────┼──────────────────
trends                   | AmbiguousReview   | —                 | Google Trends / demand data
vidiq_predictions        | —                 | —                 | (legacy, unused)
validations              | —                 | —                 | (legacy, unused)
```

---

## Constructor Pattern

Each store follows the **Dependency Injection** pattern:

```python
class KeywordStore:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
    
    def add_keyword(self, keyword: str, source: str, ...) -> Dict[str, Any]:
        cursor = self._conn.cursor()
        cursor.execute(...)
        self._conn.commit()
        return {...}

class IntentClassifier:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
    # ...

class PerformanceTracker:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
    # ...
```

**Benefits:**
- Testability: inject `:memory:` for unit tests
- No shared state: each instance has its own cursor lifecycle
- Composability: orchestrator can instantiate all three with one connection

**Usage pattern:**
```python
# In orchestrator or entry point
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

keyword_store = KeywordStore(conn)
intent_classifier = IntentClassifier(conn)
performance_tracker = PerformanceTracker(conn)

# Use...

conn.close()
```

---

## Open Questions for H2 → H3 Handoff

1. **AmbiguousReview methods** — Trends (add_trend, get_cached_trend, get_latest_trend) and schema management (get_schema_version, set_schema_version):
   - Move trends to a separate `DemandResearchStore`?
   - Keep schema methods as module-level functions?
   - Create a `SchemaManager` class?

2. **init_database & close**:
   - Factory pattern (static method on a coordinator)?
   - Context manager support?
   - Auto-cleanup on `__del__`?

3. **Error handling standardization**:
   - All stores inherit from a base class with `_err()` method?
   - Or duplicate the error dict pattern per store?

4. **Migration methods** (_ensure_*):
   - Do these move into stores, or stay as module-level helpers?

---

## Verification Checklist

- [x] 48 public methods assigned to exactly one bucket
- [x] No method appears in multiple buckets
- [x] Table ownership is explicit (owned vs. read-only)
- [x] Constructor pattern is DI-based (no db_path in __init__)
- [x] AmbiguousReview items are documented with rationale
- [x] No code changes in this document — design only
