# Stack Research: v1.4 Learning Loop

**Researched:** 2026-02-02
**Python Version:** 3.14.2
**Context:** Adding performance pattern extraction and subscriber conversion analysis to existing YouTube Analytics infrastructure

## Recommendation

**Add pandas for correlation analysis, keep everything else standard library.** The existing infrastructure already has YouTube Analytics API integration, SQLite database, and pattern collection via `patterns.py`. For 20+ videos, simple correlation analysis is sufficient—ML overkill would add complexity without value. Use pandas for correlation coefficients, scipy for statistical significance, and extend existing SQLite schema for caching learned patterns.

## Libraries to Add

| Library | Version | Purpose | Why This One |
|---------|---------|---------|--------------|
| pandas | >=2.3.3 | Correlation analysis between video features and subscriber conversion | Industry standard for data analysis, excellent correlation methods (pearsonr, spearmanr), works with Python 3.14. Version 2.3.3 released Jan 2026 supports Python 3.14. |
| scipy | >=1.14.0 | Statistical significance testing (p-values for correlations) | Pandas doesn't provide p-values. Scipy's `scipy.stats.pearsonr()` returns both coefficient and p-value. Essential for determining if patterns are statistically significant or noise. |
| Jinja2 | >=3.1.6 | Template rendering for recommendation reports | Already used in Phase 18 orchestrator. Consistent with existing tooling. Latest version 3.1.6 (2026). |

**What NOT to add:**
- ❌ **scikit-learn** - Overkill for 20 videos. Simple correlation > ML models at this scale. Would add 50MB+ dependency for features we don't need.
- ❌ **numpy** - Pandas and scipy already depend on it. No need to specify separately.
- ❌ **matplotlib/seaborn** - No visualization needed. Reports are markdown tables, not charts.
- ❌ **statsmodels** - More complex than needed. Scipy.stats provides sufficient statistical testing.

## Integration Points

### 1. Data Source: Existing `patterns.py`

**Already available** (no code changes needed):
- `collect_video_data()` - Parses POST-PUBLISH-ANALYSIS.md files
- `enrich_video_data()` - Adds tags, title structure, thumbnail metadata
- Subscriber data: Already captured in `engagement.subscribers_gained` field from `analyze.py`

**NEW function needed in `patterns.py`:**
```python
def extract_subscriber_features(videos: list[dict]) -> pd.DataFrame:
    """
    Convert video data to pandas DataFrame with features:
    - subscribers_per_100_views (target metric)
    - topic tags (territorial, ideological, etc.)
    - title attributes (has_colon, has_question, has_country, etc.)
    - thumbnail type (map, face, document)
    - video length, retention, CTR

    Returns DataFrame ready for correlation analysis.
    """
```

### 2. Correlation Analysis: New `learning.py` module

**Location:** `tools/youtube-analytics/learning.py`

**Key functions:**
```python
def analyze_subscriber_patterns(df: pd.DataFrame) -> dict:
    """
    Calculate correlation between features and subscriber conversion.

    Uses:
    - pandas.DataFrame.corr() for correlation matrix
    - scipy.stats.pearsonr() for p-values

    Returns dict with:
    - correlations: feature -> (coefficient, p_value)
    - top_positive: features most correlated with subs
    - top_negative: features to avoid
    """

def build_winning_profile(videos: list[dict], threshold: float = 0.5) -> dict:
    """
    Identify common attributes of high-converting videos.

    "High converting" = subscribers_per_100_views > channel median

    Returns profile with:
    - common_topics: topics appearing in 60%+ of winners
    - common_title_attributes: title features in 60%+ of winners
    - common_thumbnail_type: most frequent thumbnail type
    - avg_metrics: retention, CTR averages for winners
    """
```

### 3. Topic Recommendation: Enhancement to `discovery/orchestrator.py`

**NEW method in OpportunityOrchestrator:**
```python
def score_topic_fit_to_profile(self, keyword: str, profile: dict) -> float:
    """
    Score how well a discovered topic matches winning profile.

    Args:
        keyword: Topic to evaluate
        profile: Output from build_winning_profile()

    Returns:
        fit_score: 0-100 based on:
        - Topic classification match (territorial, ideological, etc.)
        - Inferred title structure potential
        - Historical performance of similar topics
    """
```

**Updated `analyze_opportunity()` to include:**
```python
# Step 8: Calculate profile fit score (NEW)
from tools.youtube_analytics.learning import get_winning_profile
profile = get_winning_profile()  # Cached in SQLite
if profile:
    fit_score = self.score_topic_fit_to_profile(keyword, profile)
    score_result['profile_fit'] = fit_score
    # Boost opportunity_score by 0-20 points based on fit
```

### 4. Work Deduplication: Filesystem scan

**NEW function in `learning.py`:**
```python
def get_existing_topics() -> set[str]:
    """
    Scan video-projects/ folders to identify topics already in production.

    Search locations:
    - video-projects/_IN_PRODUCTION/*
    - video-projects/_READY_TO_FILM/*
    - video-projects/_ARCHIVED/* (published or cancelled)

    Returns set of normalized topic slugs to filter against.
    """
```

**Integration:** Filter keywords in `orchestrator.py` AFTER demand/competition analysis, BEFORE opportunity scoring.

### 5. Caching: Extend SQLite schema

**NEW table in `tools/discovery/keywords.db`:**
```sql
CREATE TABLE IF NOT EXISTS learned_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT NOT NULL,  -- 'winning_profile', 'correlation_matrix'
    data_json TEXT NOT NULL,     -- JSON serialized pattern data
    sample_size INTEGER,          -- Number of videos pattern is based on
    computed_at TEXT NOT NULL,    -- ISO timestamp
    UNIQUE(pattern_type)
);
```

**Purpose:** Cache winning profile to avoid recomputing correlation matrix on every `/discover` call. Invalidate when new videos analyzed (check via max analyzed_date).

## Data Flow

```
1. User publishes video
   └─> Run `/analyze VIDEO_ID --save`
       └─> Creates POST-PUBLISH-ANALYSIS.md with subscribers_gained

2. Pattern extraction (automatic on next /discover call)
   └─> patterns.py: collect_video_data()
       └─> learning.py: extract_subscriber_features()
           └─> pandas.DataFrame with all features
               └─> learning.py: analyze_subscriber_patterns()
                   └─> scipy.stats.pearsonr() for p-values
                       └─> Cache winning_profile in SQLite

3. Topic discovery
   └─> User runs: /discover "dark ages myth" --opportunity
       └─> orchestrator.py: analyze_opportunity()
           ├─> demand.py: search volume
           ├─> competition.py: video count
           ├─> opportunity.py: SAW score
           └─> learning.py: score_topic_fit_to_profile()  [NEW]
               └─> Boost score +0-20 points for profile match
                   └─> Filter if topic in existing work
                       └─> Generate recommendation report
```

## Statistical Validity Considerations

**Sample Size: 20+ videos**

From statistical research:
- Pearson correlation: Requires n≥10 for basic validity, n≥20 for moderate confidence
- With 20 videos: Can detect large correlations (r>0.5) reliably
- With 30+ videos: Can detect medium correlations (r>0.3) with confidence

**Approach:**
1. Report correlation strength AND p-value
2. Flag patterns with p>0.05 as "needs more data"
3. Require minimum 10 videos per topic tag for topic-level patterns
4. Use channel-wide patterns (all videos) for title/thumbnail analysis

**No cross-validation needed:** We're identifying patterns, not building predictive models. Simple correlation with significance testing is sufficient.

## Implementation Priority

**Phase 1: Pattern extraction (Week 1)**
- Add pandas/scipy to requirements.txt
- Create `learning.py` with `extract_subscriber_features()` and `analyze_subscriber_patterns()`
- CLI: `python learning.py --analyze` to see correlation table

**Phase 2: Profile building (Week 1)**
- Add `build_winning_profile()` to learning.py
- Extend SQLite schema with learned_patterns table
- CLI: `python learning.py --profile` to see winning attributes

**Phase 3: Integration with orchestrator (Week 2)**
- Add `score_topic_fit_to_profile()` to orchestrator.py
- Update opportunity scoring to include profile_fit component
- Test: `/discover "new topic" --opportunity` shows fit score

**Phase 4: Work deduplication (Week 2)**
- Add `get_existing_topics()` filesystem scan
- Filter keywords before scoring in orchestrator
- CLI: `python learning.py --existing` to see what's already in progress

## Validation Tests

1. **Correlation sanity check:** Known high-subscriber video (Somaliland: 19 subs) should show positive correlation with its attributes
2. **Profile consistency:** Re-run profile building with same data should produce identical results
3. **Score impact:** Topic matching winning profile should score 10-20 points higher than non-matching topic with same demand/competition
4. **Deduplication:** Searching for topic with existing project folder should return "already in progress" flag

## Sources

- [NumPy, SciPy, and pandas: Correlation With Python – Real Python](https://realpython.com/numpy-scipy-pandas-correlation-python/)
- [Exploring Correlation in Python: Pandas, SciPy - Re-thought](https://www.re-thought.com/blog/exploring-correlation-in-python)
- [pandas 2.3.3 documentation - Release notes](https://pandas.pydata.org/docs/whatsnew/index.html)
- [pandas 3.0.0 released January 21, 2026](https://pandas.pydata.org/docs/dev/whatsnew/v3.0.0.html)
- [Jinja2 3.1.6 · PyPI](https://pypi.org/project/Jinja2/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) (reviewed, determined as overkill for this use case)
