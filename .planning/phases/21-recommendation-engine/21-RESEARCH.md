# Phase 21 Research: Recommendation Engine & `/next` Command

**Date:** 2026-02-02
**Phase Goal:** User gets ranked NEW topic recommendations via `/next` command

## Problem Statement

From user conversation:
> "When I ask for the next best video for me to make it starts recommending me projects I already did some work on instead of analyzing what works, where I have an advantage and what I could produce."

**Goal:** "Based on your best performers, here are untapped topics that fit the pattern"

The current system can:
- Score individual keywords via `orchestrator.py` (opportunity analysis)
- Extract winning patterns via `pattern_extractor.py` (what works)
- Track lifecycle state of keywords in database

But it lacks:
1. A way to filter out topics already in production
2. A way to combine winning patterns with opportunity scoring
3. A unified `/next` command that orchestrates all of this

## Existing Components (What We Have)

### Phase 20 - Pattern Extraction

**File:** `tools/youtube-analytics/pattern_extractor.py`

Key functions:
- `extract_winning_patterns()` - Returns complete winning profile
- `extract_topic_ranking()` - Topics ranked by conversion rate
- `extract_angle_ranking()` - Angles ranked by conversion rate
- `calculate_channel_strengths()` - Returns `{document_heavy, academic, legal_territorial}` scores
- `extract_top_converter_profile()` - Dominant topic/angles of top converters

**Output structure:**
```python
{
    'topic_ranking': [{'topic': 'territorial', 'avg_conversion': 0.85, ...}],
    'angle_ranking': [{'angle': 'legal', 'avg_conversion': 0.92, ...}],
    'channel_strengths': {'document_heavy': 85, 'academic': 90, 'legal_territorial': 95},
    'insights': ['Territorial topics convert 1.4x better than average', ...],
    'top_converter_profile': {'dominant_topic': 'territorial', 'dominant_angles': ['legal', 'historical']}
}
```

### Phase 18 - Opportunity Scoring

**File:** `tools/discovery/orchestrator.py`

Key methods:
- `OpportunityOrchestrator.analyze_opportunity(keyword)` - Full pipeline
- `OpportunityOrchestrator.list_by_state(state)` - Get keywords by lifecycle

**Opportunity score formula:** `demand * 0.33 + gap * 0.33 + fit * 0.34`

**Returns:**
```python
{
    'opportunity_score': 72.5,  # 0-100 or None if blocked
    'category': 'Excellent',    # Excellent/Good/Fair/Poor/Blocked
    'demand': {'search_volume_proxy': 70, 'trend_direction': 'rising'},
    'competition': {'differentiation_score': 0.8, 'recommended_angle': 'legal'},
    'production': {'document_score': 3, 'is_animation_blocked': False}
}
```

### Phase 17 - Production Constraints

**File:** `tools/discovery/format_filters.py`

Key functions:
- `is_animation_required(title)` - Hard block detection
- `calculate_document_score(title)` - 0-4 document-friendliness
- `evaluate_production_constraints(title)` - Combined evaluation

### Existing Work Folders

**Locations:**
- `video-projects/_IN_PRODUCTION/` - ~30 active projects
- `video-projects/_ARCHIVED/` - ~7 archived/published projects

**Folder naming convention:** `{number}-{topic-slug-year}/`

Examples:
- `1-somaliland-2025/`
- `14-chagos-islands-2025/`
- `19-flat-earth-medieval-2025/`

## Integration Design

### 1. Existing Work Scanner

**Purpose:** Scan `_IN_PRODUCTION/` and `_ARCHIVED/` to build exclusion list

**Approach:**
1. List all folders in both lifecycle directories
2. Extract topic slugs from folder names (e.g., `somaliland`, `chagos-islands`, `flat-earth-medieval`)
3. Build keyword patterns for matching (handle variations like "flat earth" vs "flat-earth-medieval")

**Simple implementation:**
```python
def get_existing_topics() -> List[str]:
    """Get list of topics already in production or archived."""
    topics = []
    for folder in Path('video-projects/_IN_PRODUCTION').iterdir():
        if folder.is_dir():
            # Extract slug: "14-chagos-islands-2025" -> "chagos islands"
            slug = folder.name.split('-', 1)[1].rsplit('-', 1)[0].replace('-', ' ')
            topics.append(slug)
    # Same for _ARCHIVED
    return topics
```

### 2. Pattern-Weighted Recommendation Scoring

**Purpose:** Boost topics that match winning patterns

**Formula:**
```
final_score = opportunity_score * pattern_multiplier

where pattern_multiplier:
  - 1.3 if topic matches dominant topic of top converters
  - 1.2 if angle matches dominant angles
  - 1.1 if channel strength score > 70 for this topic type
  - 1.0 baseline
```

**Maximum multiplier:** 1.5 (caps stacking)

### 3. Recommendation Pipeline

**Steps:**
1. Load winning patterns from `extract_winning_patterns()`
2. Get all ANALYZED keywords from database (`list_by_state('ANALYZED')`)
3. Filter out topics matching existing work (fuzzy match on topic slug)
4. For each remaining topic:
   - Get cached opportunity score (already calculated)
   - Apply pattern multiplier
   - Calculate final_score
5. Sort by final_score descending
6. Return top N recommendations with reasoning

### 4. `/next` Command Output Format

**Example output:**
```markdown
## Top 5 Recommendations

### 1. Treaty of Versailles Analysis (Score: 94.3)

**Why this fits:**
- Matches your dominant pattern: legal + territorial
- Competition gap in legal angle (0.91)
- Document-heavy format (score 4/4) matches channel strength (95/100)

| Factor | Value | Impact |
|--------|-------|--------|
| Opportunity Score | 72.5 | Excellent |
| Pattern Match | territorial + legal | +30% |
| Channel Strength | legal_territorial: 95 | +15% |
| Competition Gap | legal angle: 0.91 | High |
| Document Score | 4/4 | Perfect fit |

**Get started:**
```bash
/research --new "treaty of versailles"
```

---

### 2. Library of Alexandria Myth (Score: 87.2)
...
```

### 5. CLI Design

**Command:** `/next`

**Flags:**
- `--limit N` - Number of recommendations (default 5)
- `--json` - JSON output for automation
- `--refresh` - Refresh winning patterns from database
- `--include-analyzed` - Include topics already scored but not in production
- `--topic-type TYPE` - Filter by topic type (territorial, ideological, etc.)

**Execution:**
```bash
python tools/discovery/recommender.py              # Default 5 recommendations
python tools/discovery/recommender.py --limit 10   # Top 10
python tools/discovery/recommender.py --json       # For automation
```

## File Structure

New files to create:
```
tools/discovery/
  recommender.py        # TopicRecommender class + CLI

.claude/commands/
  next.md               # /next command documentation
```

Files to modify:
```
tools/discovery/database.py  # Add get_analyzed_keywords() method if needed
```

## Requirements Coverage

| Requirement | Implementation |
|-------------|----------------|
| RECD-01 | `/next` command via `recommender.py` CLI |
| RECD-02 | `get_existing_topics()` scans `_IN_PRODUCTION/` and `_ARCHIVED/` |
| RECD-03 | Each recommendation shows factors: opportunity + pattern match + channel fit |
| RECD-04 | Integrates with `OpportunityScorer` via cached database scores |
| INTG-02 | Uses `competition.py` data via cached opportunity scores |
| INTG-03 | Uses `format_filters.py` constraints via cached opportunity scores |

## Task Breakdown

### Task 1: Create TopicRecommender Module

**Files:** `tools/discovery/recommender.py`

**Functions:**
- `get_existing_topics()` - Scan folders for exclusion
- `calculate_pattern_multiplier()` - Apply winning pattern boost
- `TopicRecommender.recommend()` - Main recommendation logic
- `TopicRecommender.format_recommendation()` - Create readable output
- CLI with argparse

**Lines:** ~300

### Task 2: Create /next Command Documentation

**Files:** `.claude/commands/next.md`

**Content:**
- Usage examples
- Flag documentation
- Output format explanation
- Integration with workflow

**Lines:** ~150

## Verification

**Manual tests:**
1. `python recommender.py` shows 5 recommendations not in production
2. Recommendations sorted by score descending
3. Each recommendation shows reasoning components
4. `--json` outputs valid JSON
5. Existing production topics are filtered out

**Automated check:**
```bash
# Verify no production topics appear
python recommender.py --json | python -c "
import json, sys
recs = json.load(sys.stdin)
existing = ['somaliland', 'chagos', 'flat earth', 'iran']
for r in recs['recommendations']:
    for e in existing:
        if e.lower() in r['keyword'].lower():
            print(f'ERROR: {r[\"keyword\"]} matches existing topic {e}')
            sys.exit(1)
print('PASS: No existing topics in recommendations')
"
```

## Scope Estimate

- **Task 1:** ~45 min (new module with 6 functions + CLI)
- **Task 2:** ~15 min (command documentation)
- **Total:** ~60 min (1 plan, 2 tasks)

Fits within single plan context budget (~50%).
