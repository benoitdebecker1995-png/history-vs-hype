# Architecture Patterns: Niche Discovery Integration

**Domain:** YouTube content optimization workspace
**Researched:** 2026-01-31
**Milestone:** v1.3 - Niche Discovery
**Confidence:** HIGH (existing codebase analysis + integration point verification)

---

## Executive Summary

This architecture research addresses how to integrate niche discovery capabilities into the existing YouTube analytics workspace without disrupting established workflows.

**New capabilities:**
1. **Demand research** - Search volume, trending topics, audience questions
2. **Competition analysis** - Who covers what, quality assessment, gap identification
3. **Competitor learning** - What works for big channels (techniques to adapt)
4. **Format filtering** - Flag topics needing animation vs document-friendly
5. **Opportunity scoring** - Rank topics by (demand × gap × fit) / effort

**Key finding:** The existing architecture (SQLite database + Python modules + error dict pattern) is well-suited for niche discovery additions. Integration points are clear. No major structural changes needed.

**Recommendation:** Extend existing components (keywords.db, discovery tools) rather than building parallel systems. Follow established patterns for consistency.

---

## Existing Architecture Analysis

### Current Data Flow

```
POST-PUBLISH ANALYTICS (current):
1. Video Published
   ↓
2. /analyze VIDEO_ID
   ↓
3. YouTube Analytics API → metrics.py → video_report.py
   ↓
4. Comments API → comments.py (categorization)
   ↓
5. patterns.py (cross-video aggregation)
   ↓
6. POST-PUBLISH-ANALYSIS.md (saved to project folder)
```

```
PRE-PUBLISH DISCOVERY (current):
1. User explores topic manually
   ↓
2. /discover TOPIC (keyword extraction)
   ↓
3. autocomplete.py → YouTube autocomplete suggestions
   ↓
4. intent_mapper.py → classify intent (6 categories)
   ↓
5. keywords.db (store keywords with intent)
```

### Existing Components (Verified)

**Database Layer:**
- `tools/discovery/keywords.db` (SQLite)
  - Tables: keywords, keyword_intents, keyword_performance
  - Pattern: Error dict returns (`{'error': 'msg'}` on failure)
  - ~50KB current size

**Discovery Tools:**
- `autocomplete.py` - YouTube autocomplete suggestions (browser automation)
- `intent_mapper.py` - 6-category intent classification
- `database.py` - KeywordDB class with CRUD operations
- `keywords.py` - CLI for keyword management

**Analytics Tools:**
- `analyze.py` - Post-publish orchestrator
- `patterns.py` - Cross-video pattern recognition
- `diagnostics.py` - Discovery issue diagnosis (impressions/CTR)

**Data Structures:**
- POST-PUBLISH-ANALYSIS.md files (scattered across project folders)
- keywords.db (centralized keyword storage)
- TOPIC-ANALYSIS.md (pattern aggregation)
- TITLE-PATTERNS.md (title/thumbnail correlation)

### Integration Points Identified

| New Feature | Natural Integration Point | Why |
|-------------|--------------------------|-----|
| Demand research | Extend keywords.db with `keyword_trends` table | Centralizes all keyword data, enables JOINs |
| Competition analysis | Extend keywords.db with `competitors`, `competitor_videos` | Relates competition to keywords |
| Opportunity scoring | Extend keywords.db with `opportunities` table | Connects demand + competition + format |
| Post-publish validation | Modify analyze.py to check opportunity scores | Closes learning loop |
| Pattern correlation | Modify patterns.py to compare predictions vs outcomes | Validates scoring accuracy |

---

## Recommended Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EXISTING SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐                    │
│  │  YouTube     │     │  Discovery   │                    │
│  │  Analytics   │     │  Tools       │                    │
│  │  API         │     │  (current)   │                    │
│  └──────────────┘     └──────────────┘                    │
│       ↓                     ↓                               │
│  ┌──────────────────────────────────┐                     │
│  │  Post-Publish Analytics          │                     │
│  │  - /analyze VIDEO_ID             │                     │
│  │  - Pattern recognition            │                     │
│  │  - Comment analysis               │                     │
│  └──────────────────────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                NEW NICHE DISCOVERY LAYER                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────┐ │
│  │  Demand      │     │  Competition │     │  Competitor│ │
│  │  Research    │     │  Analysis    │     │  Learning  │ │
│  └──────────────┘     └──────────────┘     └────────────┘ │
│       ↓                     ↓                     ↓         │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Opportunity Scoring Engine                 │   │
│  │    (Demand × Gap × Fit / Effort)                   │   │
│  └────────────────────────────────────────────────────┘   │
│                            ↓                                │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Format Filtering                           │   │
│  │    (Document-friendly topics)                      │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With | Data Store |
|-----------|---------------|-------------------|------------|
| **Existing: YouTube Analytics API** | Post-publish metrics (views, retention, watch time) | analyze.py, patterns.py | YouTube servers |
| **Existing: Discovery Tools** | Keyword extraction, intent classification, diagnostics | keywords.py, database.py | keywords.db (SQLite) |
| **Existing: Post-Publish Analytics** | Video performance, pattern recognition, lessons | channel_averages.py, comments.py | POST-PUBLISH-ANALYSIS.md files |
| **NEW: Demand Research** | Search volume, trending topics, audience questions | YouTube autocomplete, Google Trends API | keywords.db (extend) |
| **NEW: Competition Analysis** | Who covers what, quality assessment, gap identification | YouTube Data API v3 | keywords.db (extend) |
| **NEW: Competitor Learning** | Extract techniques from successful channels | Video transcripts, metadata analysis | keywords.db (extend) |
| **NEW: Format Filtering** | Flag animation-heavy vs document-friendly topics | All niche discovery components | In-memory (no persistence) |
| **NEW: Opportunity Scorer** | Rank topics by (demand × gap × fit) / effort | All niche discovery components | keywords.db (extend) |

### Database Schema Extensions

**Current schema (keep as-is):**
```sql
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT UNIQUE NOT NULL,
    search_volume INTEGER,
    competition_score REAL,
    source TEXT,
    first_discovered DATE,
    last_updated DATE
);

CREATE TABLE keyword_intents (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER REFERENCES keywords(id),
    intent_category TEXT NOT NULL,
    confidence REAL,
    is_primary BOOLEAN DEFAULT 0
);

CREATE TABLE keyword_performance (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER REFERENCES keywords(id),
    video_id TEXT NOT NULL,
    impressions INTEGER,
    ctr REAL,
    views INTEGER,
    watch_time_minutes INTEGER,
    measured_date DATE
);
```

**NEW tables (add to same database):**
```sql
CREATE TABLE keyword_trends (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER REFERENCES keywords(id),
    trend_direction TEXT,  -- 'rising', 'falling', 'stable'
    volume_change_pct REAL,
    measured_date DATE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

CREATE TABLE competitors (
    id INTEGER PRIMARY KEY,
    channel_id TEXT UNIQUE NOT NULL,
    channel_name TEXT,
    subscriber_count INTEGER,
    avg_views INTEGER,
    niche_category TEXT,  -- 'history', 'geopolitics', 'education'
    added_date DATE
);

CREATE TABLE competitor_videos (
    id INTEGER PRIMARY KEY,
    competitor_id INTEGER REFERENCES competitors(id),
    video_id TEXT UNIQUE NOT NULL,
    title TEXT,
    views INTEGER,
    published_date DATE,
    covers_keyword_id INTEGER REFERENCES keywords(id),
    quality_score REAL,  -- 0-10 based on views, retention proxy
    FOREIGN KEY (competitor_id) REFERENCES competitors(id),
    FOREIGN KEY (covers_keyword_id) REFERENCES keywords(id)
);

CREATE TABLE opportunities (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER REFERENCES keywords(id),
    demand_score REAL,      -- 0-10 (search volume normalized)
    gap_score REAL,         -- 0-10 (low competition = high score)
    fit_score REAL,         -- 0-10 (document-friendly format)
    effort_estimate TEXT,   -- 'low', 'medium', 'high'
    overall_score REAL,     -- (demand × gap × fit) / effort
    calculated_date DATE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

CREATE TABLE opportunity_validations (
    id INTEGER PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    video_id TEXT NOT NULL,
    predicted_score REAL,
    actual_views INTEGER,
    actual_ctr REAL,
    actual_retention REAL,
    prediction_accurate BOOLEAN,  -- TRUE if predicted_high == actual_high
    validated_date DATE,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);

-- Indexes for performance
CREATE INDEX idx_keyword_trends_date ON keyword_trends(measured_date DESC);
CREATE INDEX idx_competitor_videos_keyword ON competitor_videos(covers_keyword_id);
CREATE INDEX idx_opportunities_score ON opportunities(overall_score DESC);
CREATE INDEX idx_validations_date ON opportunity_validations(validated_date DESC);
```

---

## Patterns to Follow

### Pattern 1: Database Schema Extensions (Not Replacements)
**What:** Extend existing keywords.db with new tables, don't create parallel databases

**When:** Adding demand research, competition data, or opportunity scoring

**Why:**
- Avoid data fragmentation
- Leverage existing KeywordDB class patterns
- Enable JOIN queries across old/new data

**Example:**
```python
# GOOD: Extend existing database
class KeywordDB:
    def add_trend(self, keyword_id: int, trend_direction: str, volume_change: float):
        """Add trend data to existing keyword"""
        cursor = self._conn.cursor()
        cursor.execute(
            """INSERT INTO keyword_trends (keyword_id, trend_direction, volume_change_pct, measured_date)
               VALUES (?, ?, ?, ?)""",
            (keyword_id, trend_direction, volume_change, datetime.utcnow().date())
        )
        self._conn.commit()

# BAD: Create separate database
class TrendsDB:
    def __init__(self):
        self._conn = sqlite3.connect('trends.db')  # Separate database!
```

### Pattern 2: Error Dict Returns (Match Existing)
**What:** All new modules return `{'error': 'msg'}` on failure, not exceptions

**When:** Writing demand_research.py, competition_analysis.py, etc.

**Why:**
- Consistent with existing codebase (video_report.py, database.py, autocomplete.py)
- CLI tools can print helpful messages instead of stack traces
- Enables graceful degradation (one component fails, others continue)

**Example:**
```python
# GOOD (matches existing pattern)
def fetch_search_volume(keyword: str) -> Dict[str, Any]:
    """Fetch search volume for keyword"""
    try:
        # ... API call
        return {
            'keyword': keyword,
            'volume': 1500,
            'trend': 'rising'
        }
    except Exception as e:
        return {
            'error': f'Search volume fetch failed: {type(e).__name__}',
            'details': str(e)
        }

# BAD (breaks existing pattern)
def fetch_search_volume(keyword: str) -> int:
    # ... API call (raises exception)
    return 1500  # Caller must catch exceptions
```

### Pattern 3: CLI + Python API Dual Interface
**What:** Every module provides both CLI usage and Python import API

**When:** Creating new tools (demand_research.py, competition_analysis.py)

**Why:**
- Matches existing pattern (autocomplete.py, keywords.py, analyze.py, patterns.py)
- CLI for manual exploration
- Python API for orchestrator scripts

**Example:**
```python
# Python API (for orchestrator)
from demand_research import get_search_volume, get_trending_topics

volume = get_search_volume('dark ages myth')
trending = get_trending_topics(category='history')

# CLI (for manual exploration)
# $ python demand_research.py "dark ages myth"
# $ python demand_research.py --trending --category history

if __name__ == '__main__':
    # CLI interface following existing pattern
    pass
```

### Pattern 4: Orchestrator Command Pattern
**What:** Create `/discover` orchestrator that coordinates parallel sub-components

**When:** Implementing niche discovery workflow

**Why:**
- Matches existing `/analyze` pattern (analyze.py orchestrates video_report, comments, channel_averages)
- User runs ONE command, not five separate scripts
- Enables intelligent fallback if one component fails

**Example:**
```python
# tools/discovery/discover.py (new orchestrator)

def run_niche_discovery(topic: str) -> Dict[str, Any]:
    """
    Orchestrate all niche discovery components for a topic.

    Similar to analyze.py for post-publish analysis.
    """
    errors = []

    # 1. Demand research
    demand = get_search_volume(topic)
    if 'error' in demand:
        errors.append({'source': 'demand', 'message': demand['error']})
        demand = {'volume': None, 'trend': None}

    # 2. Competition analysis
    competitors = analyze_competition(topic)
    if 'error' in competitors:
        errors.append({'source': 'competition', 'message': competitors['error']})
        competitors = {'count': None, 'quality': None}

    # 3. Format filtering
    format_check = assess_format_requirements(topic)

    # 4. Opportunity scoring
    score = calculate_opportunity_score(
        demand=demand,
        competition=competitors,
        format_fit=format_check
    )

    return {
        'topic': topic,
        'demand': demand,
        'competition': competitors,
        'format': format_check,
        'opportunity_score': score,
        'errors': errors
    }
```

### Pattern 5: Markdown Report Outputs
**What:** Generate `.md` files for human review, not just JSON

**When:** Reporting niche discovery results

**Why:**
- Matches existing pattern (POST-PUBLISH-ANALYSIS.md, TOPIC-ANALYSIS.md, TITLE-PATTERNS.md)
- Easy to version control and review
- Human-readable with structured data

**Example:**
```markdown
# Niche Opportunity Report: Dark Ages Myth

**Topic:** dark ages myth
**Analyzed:** 2026-01-31
**Overall Score:** 7.2 / 10

## Recommendation
**GOOD OPPORTUNITY** - High demand, low competition, excellent format fit

## Demand Assessment
- **Search volume:** 1,500/month
- **Trend:** Rising (+15% past 3 months)
- **Related queries:** "dark ages myth debunked", "medieval literacy rates"

## Competition Analysis
- **Videos ranking:** 12 competitors
- **Average quality:** Medium (4.2/10)
- **Gap identified:** No video uses primary source manuscripts as evidence
- **Top competitor:** "Medieval Misconceptions" (850K views, 6min runtime)

## Format Fit
- **Document availability:** HIGH (✓)
  - Carolingian manuscripts available on Wikimedia Commons
  - Chris Wickham's "Inheritance of Rome" has statistical tables
- **Animation requirement:** LOW (✓)
  - Topic can be explained with documents + maps
- **Production complexity:** MEDIUM
  - Need to source manuscript images
  - Timeline graphics helpful but not essential

## Opportunity Score Breakdown
| Factor | Score | Weight | Contribution |
|--------|-------|--------|--------------|
| Demand | 6/10 | 30% | 1.8 |
| Gap | 8/10 | 40% | 3.2 |
| Format Fit | 9/10 | 30% | 2.7 |
| **Total** | **7.7/10** | | |
| Effort Penalty | Medium | -0.5 | |
| **Final Score** | **7.2/10** | | |

## Recommended Action
✓ Add to video pipeline - This topic aligns with channel strengths

## Next Steps
1. Download manuscript images from Wikimedia Commons
2. Purchase "Inheritance of Rome" for statistics
3. Verify "dark ages" search volume with Google Trends
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Separate Database Per Component
**What goes wrong:** Creating competitors.db, opportunities.db, trends.db as separate files

**Why it's bad:**
- Data fragmentation (can't JOIN across databases easily in SQLite)
- Inconsistent schemas across files
- Breaks existing KeywordDB patterns
- Multiple connection management

**Instead:** Extend keywords.db with new tables (see Pattern 1)

### Anti-Pattern 2: Synchronous Serial Execution
**What goes wrong:** Running demand → competition → learning → scoring sequentially

**Why it's bad:**
- Slow (demand research 10s + competition 15s + learning 20s = 45s total)
- Blocks on API rate limits
- One failure blocks everything downstream

**Instead:**
```python
# GOOD: Parallel execution where possible
import concurrent.futures

def run_niche_discovery(topic: str):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Run demand and competition in parallel
        demand_future = executor.submit(get_search_volume, topic)
        competition_future = executor.submit(analyze_competition, topic)

        demand = demand_future.result()
        competition = competition_future.result()

    # Then run dependent components
    format_check = assess_format_requirements(topic)
    score = calculate_opportunity_score(demand, competition, format_check)
```

### Anti-Pattern 3: Tight Coupling to External APIs
**What goes wrong:** Hardcoding YouTube Data API calls without abstraction layer

**Why it's bad:**
- API changes break entire system
- Can't test without hitting real API
- Rate limiting affects all components

**Instead:**
```python
# GOOD: Abstraction layer
class CompetitorVideoFetcher:
    """Abstract interface for fetching competitor videos"""

    def fetch_videos_for_keyword(self, keyword: str) -> List[Dict]:
        """Override this in subclasses"""
        raise NotImplementedError

class YouTubeAPIFetcher(CompetitorVideoFetcher):
    """YouTube Data API v3 implementation"""
    def fetch_videos_for_keyword(self, keyword: str):
        # ... API call
        pass

class MockFetcher(CompetitorVideoFetcher):
    """Mock implementation for testing"""
    def fetch_videos_for_keyword(self, keyword: str):
        return [{'video_id': 'test123', 'title': 'Test Video'}]
```

### Anti-Pattern 4: Reimplementing Intent Classification
**What goes wrong:** Creating separate topic classifier when intent_mapper.py already exists

**Why it's bad:**
- Duplicates existing work
- Classifications may conflict
- Wastes development time

**Instead:** Extend intent_mapper.py with niche-specific categories if needed

### Anti-Pattern 5: Ignoring Post-Publish Feedback Loop
**What goes wrong:** Niche discovery scores topics, but never learns if scores were accurate

**Why it's bad:**
- No way to improve opportunity scoring over time
- Can't validate "high demand + low competition" claims
- Breaks learning loop

**Instead:**
```python
# After video published, compare prediction to reality
def validate_opportunity_score(topic: str, video_id: str):
    """
    Compare niche discovery prediction to actual performance.

    Updates opportunity scoring weights based on accuracy.
    """
    # 1. Fetch original opportunity score
    db = KeywordDB()
    opportunity = db.get_opportunity_for_keyword(topic)

    # 2. Fetch actual performance
    actual_performance = get_video_metrics(video_id)

    # 3. Calculate prediction accuracy
    predicted_high = opportunity['overall_score'] > 7.0
    actual_high = actual_performance['views'] > channel_avg_views

    accurate = predicted_high == actual_high

    # 4. Store validation result
    db.add_opportunity_validation(
        opportunity_id=opportunity['id'],
        video_id=video_id,
        predicted_score=opportunity['overall_score'],
        actual_views=actual_performance['views'],
        prediction_accurate=accurate
    )

    # 5. Adjust scoring weights if pattern emerges
    if db.get_validation_count() > 10:
        recalibrate_opportunity_weights(db)
```

---

## Integration Points with Existing System

### Integration Point 1: Keywords Database Extension
**Existing:** keywords.db with tables: `keywords`, `keyword_intents`, `keyword_performance`

**Modification:** Add tables to same database
- `keyword_trends` (demand research data)
- `competitors` (channel metadata)
- `competitor_videos` (video coverage analysis)
- `opportunities` (scored topics)
- `opportunity_validations` (prediction accuracy tracking)

**Migration:**
```python
# tools/discovery/migrate_v2.py
def migrate_keywords_db_v2():
    """Add niche discovery tables to existing keywords.db"""
    db = KeywordDB()

    # Read new schema
    schema_path = Path(__file__).parent / 'schema_v2.sql'
    new_tables_sql = schema_path.read_text()

    # Apply migration
    db._conn.executescript(new_tables_sql)
    db._conn.commit()

    return {'status': 'migrated', 'version': 2}
```

### Integration Point 2: Post-Publish Validation
**Existing:** analyze.py runs after video published

**Modification:** Add opportunity validation to analyze.py

```python
# tools/youtube-analytics/analyze.py (modify existing)

def run_analysis(video_id_or_url: str, manual_ctr: float = None) -> dict:
    # ... existing code ...

    # NEW: Check if this video was based on a scored opportunity
    from tools.discovery.database import KeywordDB
    db = KeywordDB()
    opportunity = db.find_opportunity_for_video(video_id)

    if opportunity:
        from tools.discovery.opportunity_scorer import validate_opportunity_score
        validation = validate_opportunity_score(
            opportunity_id=opportunity['id'],
            actual_views=engagement['views'],
            actual_ctr=ctr['ctr_percent'],
            actual_retention=retention['avg_retention']
        )

        analysis['opportunity_validation'] = validation

    return analysis
```

### Integration Point 3: Pattern Recognition Enhancement
**Existing:** patterns.py aggregates performance by topic tags

**Modification:** Cross-reference with opportunity scores

```python
# tools/youtube-analytics/patterns.py (modify existing)

def generate_topic_report() -> str:
    """Generate TOPIC-ANALYSIS.md with opportunity score correlation"""

    # ... existing code ...

    # NEW: For each topic, show if opportunity score was predictive
    from tools.discovery.database import KeywordDB
    db = KeywordDB()

    for topic, stats in topic_stats.items():
        # Find videos tagged with this topic
        topic_videos = [v for v in videos if topic in v.get('tags', [])]

        # Check if opportunity scores correlated with performance
        prediction_accuracy = []
        for video in topic_videos:
            opportunity = db.find_opportunity_for_video(video['video_id'])
            if opportunity:
                predicted_high = opportunity['overall_score'] > 7.0
                actual_high = video['views'] > stats['avg_views']
                prediction_accuracy.append(predicted_high == actual_high)

        if prediction_accuracy:
            accuracy_rate = sum(prediction_accuracy) / len(prediction_accuracy)
            # Add to report: "Opportunity scoring accuracy: {accuracy_rate:.1%}"
```

### Integration Point 4: Command Orchestration
**Existing:** Slash commands route to specific tools

**New Commands:**
```bash
/discover TOPIC              # Run niche discovery analysis
/discover --trending         # Show trending topics in niche
/discover --validate VIDEO   # Validate opportunity score vs actual
```

**Implementation:**
```python
# .claude/commands/discover.py (new)

def discover_command(args: List[str]):
    """
    Niche discovery orchestrator command.

    Usage:
        /discover "dark ages myth"
        /discover --trending
        /discover --validate VIDEO_ID
    """
    if '--trending' in args:
        from tools.discovery.demand_research import get_trending_topics
        trending = get_trending_topics(category='history')
        return format_trending_report(trending)

    elif '--validate' in args:
        video_id = args[args.index('--validate') + 1]
        from tools.discovery.opportunity_scorer import validate_opportunity_score
        validation = validate_opportunity_score(video_id)
        return format_validation_report(validation)

    else:
        topic = args[0]
        from tools.discovery.discover import run_niche_discovery
        analysis = run_niche_discovery(topic)

        # Save report
        save_niche_opportunity_report(analysis)

        return format_opportunity_report(analysis)
```

---

## Build Order Recommendation

### Phase 1: Core Infrastructure (Week 1)
**Goal:** Extend database, create base patterns

**Components:**
1. Migrate keywords.db schema v2 (add tables for trends, competitors, opportunities)
2. Create base classes following error dict pattern
3. Set up CLI + Python API structure for new modules

**Validation:**
- Schema migration runs without errors
- New tables appear in keywords.db
- Base classes return proper error dicts

**Dependencies:** None (pure additions to existing system)

### Phase 2: Demand Research (Week 2)
**Goal:** Measure search volume and trends

**Components:**
1. `demand_research.py` - Fetch search volume (YouTube autocomplete volume proxy)
2. `trends_tracker.py` - Track keyword trends over time
3. Integration with keywords.db (store trend data)

**Validation:**
- `python demand_research.py "dark ages myth"` returns volume estimate
- Trend data saves to `keyword_trends` table
- Error handling works (API down → graceful error dict)

**Dependencies:** Phase 1 complete (database schema ready)

### Phase 3: Competition Analysis (Week 3)
**Goal:** Identify who covers what, assess quality

**Components:**
1. `competition_analysis.py` - Find competitor videos for keyword
2. `competitor_scorer.py` - Assess video quality (views, retention proxy)
3. Integration with keywords.db (store competitor data)

**Validation:**
- `python competition_analysis.py "dark ages myth"` returns competitor list
- Quality scores reasonable (high-view videos score higher)
- Data saves to `competitors` and `competitor_videos` tables

**Dependencies:** Phase 1 complete, YouTube Data API v3 credentials

### Phase 4: Format Filtering (Week 4)
**Goal:** Flag animation-heavy vs document-friendly topics

**Components:**
1. `format_filter.py` - Assess if topic requires animation
2. Document availability checker (can we find primary sources?)
3. Production complexity estimator

**Validation:**
- "Battle of Waterloo tactics" → flags as animation-heavy
- "Sykes-Picot treaty" → flags as document-friendly
- Complexity estimates align with manual assessment

**Dependencies:** None (operates on topic text only)

### Phase 5: Opportunity Scoring (Week 5)
**Goal:** Rank topics by (demand × gap × fit) / effort

**Components:**
1. `opportunity_scorer.py` - Combines demand, competition, format fit
2. Scoring formula with configurable weights
3. Integration with all previous components

**Validation:**
- Score formula produces reasonable results (7.2 / 10 for good opportunities)
- Scores save to `opportunities` table
- Can retrieve top opportunities with `get_top_opportunities(limit=10)`

**Dependencies:** Phases 2, 3, 4 complete

### Phase 6: Orchestrator & Reports (Week 6)
**Goal:** Wrap everything in `/discover` command

**Components:**
1. `discover.py` - Orchestrator (like analyze.py)
2. Markdown report generator (NICHE-OPPORTUNITY-REPORT.md)
3. `/discover` command integration

**Validation:**
- `/discover "dark ages myth"` runs all components
- Report saves to `.planning/topics/NICHE-OPPORTUNITY-dark-ages-myth.md`
- Graceful degradation (one component fails, others continue)

**Dependencies:** Phases 1-5 complete

### Phase 7: Post-Publish Validation Loop (Week 7)
**Goal:** Learn from actual performance

**Components:**
1. Modify analyze.py to check for opportunity scores
2. `validate_opportunity.py` - Compare prediction vs reality
3. Weight recalibration based on validation results

**Validation:**
- After publishing video, `/analyze VIDEO_ID` includes validation section
- Prediction accuracy tracked over time
- Weights adjust when validation count > 10

**Dependencies:** Phase 6 complete + 3+ videos published from niche discovery

---

## Scalability Considerations

### At 100 videos analyzed
**Current approach:** SQLite keywords.db (~50KB)
- Fast queries (<10ms)
- No performance issues
- Continue with SQLite

**Niche discovery additions:**
- keywords.db grows to ~500KB (trends, competitors, opportunities)
- Still well within SQLite performance envelope
- No changes needed

### At 1,000 videos analyzed
**Current approach:** SQLite keywords.db (~500KB)
- Query performance still <50ms
- POST-PUBLISH-ANALYSIS.md files scattered across folders
- patterns.py collects and aggregates (takes ~2-3 seconds)

**Niche discovery additions:**
- keywords.db grows to ~5MB (larger competitor dataset)
- Consider indexing:
  ```sql
  CREATE INDEX idx_keyword_trends_date ON keyword_trends(measured_date DESC);
  CREATE INDEX idx_competitor_videos_keyword ON competitor_videos(covers_keyword_id);
  CREATE INDEX idx_opportunities_score ON opportunities(overall_score DESC);
  ```
- Add caching layer for expensive queries (search volume lookups)

### At 10,000+ videos (unlikely for solo creator)
**If channel grows beyond solo operation:**
- Consider PostgreSQL migration for complex JOINs
- Add Redis cache for API responses (search volume, competitor data)
- Implement background job queue for slow operations (competitor learning)
- Current architecture supports migration path (abstraction layers enable swapping)

---

## Summary

**Core architectural decisions:**
1. ✅ Extend keywords.db schema, don't create parallel databases
2. ✅ Follow error dict pattern consistently
3. ✅ Provide CLI + Python API for all modules
4. ✅ Create `/discover` orchestrator matching `/analyze` pattern
5. ✅ Generate Markdown reports for human review
6. ✅ Integrate with post-publish analytics for validation loop

**Build order:**
1. Phase 1: Database schema v2 (1 week)
2. Phase 2: Demand research (1 week)
3. Phase 3: Competition analysis (1 week)
4. Phase 4: Format filtering (1 week)
5. Phase 5: Opportunity scoring (1 week)
6. Phase 6: Orchestrator (1 week)
7. Phase 7: Validation loop (1 week)

**Integration strategy:**
- New components extend existing patterns (don't replace)
- Database extensions (not new databases)
- Post-publish validation closes learning loop
- Pattern recognition correlates predictions with outcomes

**Technical risks:**
- LOW: Architecture follows established workspace patterns
- LOW: SQLite handles expected data volume (<5MB)
- MEDIUM: API rate limiting (YouTube Data API 10,000 units/day)
- MEDIUM: Search volume proxies may be inaccurate (validation loop mitigates)

---

*This architecture enables niche discovery without disrupting existing workflows. New components plug into established patterns (error dicts, CLI/API dual interface, Markdown reports). Post-publish validation ensures opportunity scores improve over time.*
