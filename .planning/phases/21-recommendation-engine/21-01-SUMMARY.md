---
phase: 21
plan: 01
subsystem: discovery
tags: [recommendation-engine, topic-suggestions, pattern-matching, python]

dependency-graph:
  requires:
    - phase-20 (pattern_extractor.py, extract_winning_patterns)
    - phase-18 (opportunity scoring, lifecycle states)
    - phase-15-16 (KeywordDB)
  provides:
    - recommender.py with TopicRecommender class
    - /next command for topic recommendations
    - Folder scanning for existing topics
    - Pattern-weighted scoring
  affects:
    - /discover command workflow (links to research)
    - User topic selection decisions

tech-stack:
  added: []
  patterns:
    - folder scanning via Path.iterdir()
    - word-level matching for topic deduplication
    - pattern multiplier calculation (1.0-1.5x boost)

file-tracking:
  created:
    - tools/discovery/recommender.py
    - .claude/commands/next.md
  modified: []

decisions:
  - pattern: topic-matching
    choice: word-level comparison, not substring
    reason: Prevents false positives ("iranian" shouldn't match "iran")
  - pattern: multiplier-cap
    choice: Maximum 1.5x boost
    reason: Prevents pattern match from overwhelming opportunity score
  - pattern: exclusion-sources
    choice: Scan _IN_PRODUCTION/ and _ARCHIVED/ folders
    reason: These are the canonical locations for existing work

metrics:
  duration: 5 minutes
  completed: 2026-02-02
---

# Phase 21 Plan 01: Recommendation Engine Summary

**One-liner:** Topic recommender that combines winning patterns with opportunity scores to suggest NEW topics not already in production.

## What Was Built

### 1. Topic Recommender Module (recommender.py)

Created `tools/discovery/recommender.py` with:

| Function/Class | Purpose | Output |
|----------------|---------|--------|
| `get_existing_topics()` | Scan production folders | List of topic slugs |
| `topic_matches_existing()` | Word-level match check | True/False |
| `calculate_pattern_multiplier()` | Boost based on winning patterns | (multiplier, reasons) |
| `TopicRecommender` | Main recommendation class | Full recommendation dict |
| `TopicRecommender.recommend()` | Generate ranked recommendations | Dict with recommendations |
| `TopicRecommender.format_report()` | Generate markdown report | String |

### 2. /next Command Documentation

Created `.claude/commands/next.md` with:
- Usage examples for all flags
- Output explanation and scoring interpretation
- Pattern multiplier breakdown table
- Integration with workflow (links to /research, /discover)
- Requirements section

### 3. CLI Interface

```bash
python recommender.py                  # Default 5 recommendations
python recommender.py --limit 10       # More recommendations
python recommender.py --json           # JSON output
python recommender.py --topic-type territorial  # Filter by topic
python recommender.py --save report.md  # Save markdown report
```

## Requirements Satisfied

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| RECD-01 | DONE | `/next` command via recommender.py CLI |
| RECD-02 | DONE | `get_existing_topics()` + `topic_matches_existing()` |
| RECD-03 | DONE | `calculate_pattern_multiplier()` returns reasons list |
| RECD-04 | DONE | Uses `opportunity_score_final` from Phase 18 database |
| INTG-02 | DONE | Integrates with discovery tools via KeywordDB |
| INTG-03 | DONE | Respects `is_production_blocked` from Phase 17 |

## Key Algorithms

### Folder Scanning
```python
# Parse "{number}-{topic-slug-year}" format
for item in folder.iterdir():
    parts = item.name.lower().split('-')
    if parts[0].isdigit():
        parts = parts[1:]  # Remove number
    if len(parts[-1]) == 4 and parts[-1].isdigit():
        parts = parts[:-1]  # Remove year
    topic = ' '.join(parts)
```

### Topic Matching
```python
# Word-level matching, not substring
keyword_words = set(keyword.lower().split())
for topic in existing:
    topic_words = set(topic.lower().split())
    if topic_words.issubset(keyword_words):  # All topic words in keyword
        return True
    if len(keyword_words & topic_words) >= 2:  # 2+ common words
        return True
```

### Pattern Multiplier
```python
# Boost topics matching winning patterns
multiplier = 1.0
if topic_type == patterns['dominant_topic']:
    multiplier += 0.3  # Matches dominant topic
if any(angle in patterns['dominant_angles']):
    multiplier += 0.2  # Matches top angles
if channel_strengths[topic_mapping] > 70:
    multiplier += 0.1  # High channel strength
return min(1.5, multiplier)  # Cap at 1.5x
```

### Final Score Calculation
```python
final_score = min(100, opportunity_score * pattern_multiplier)
```

## Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `tools/discovery/recommender.py` | Recommendation engine | 487 |
| `.claude/commands/next.md` | Command documentation | 180 |

## Commits

| Hash | Type | Description |
|------|------|-------------|
| (pending) | feat | Create topic recommender with folder scanning and pattern matching |
| (pending) | docs | Add /next command documentation |

## Usage Examples

### Quick Recommendations (CLI)
```bash
cd tools/discovery
python recommender.py --limit 5
```

Output:
```
============================================================
  TOPIC RECOMMENDATIONS
============================================================

Analyzed: 45 keywords
Excluded: 12 (already in production)

Winning Pattern Match:
  Dominant topic: territorial
  Top angles: legal, historical

------------------------------------------------------------
Rank | Score |  Mult | Keyword
------------------------------------------------------------
   1 |  94.3 |  1.30 | treaty of versailles territorial
   2 |  87.5 |  1.20 | sykes picot agreement
...
```

### JSON Output
```bash
python recommender.py --json --limit 2
```

### Python API
```python
from recommender import TopicRecommender
from database import KeywordDB

db = KeywordDB()
recommender = TopicRecommender(db)
result = recommender.recommend(limit=5)

for r in result['recommendations']:
    print(f"{r['rank']}. {r['keyword']}: {r['final_score']:.1f}")
```

## Edge Cases Handled

1. **No ANALYZED keywords** - Returns error with helpful message to run orchestrator
2. **Pattern extraction fails** - Proceeds with multiplier=1.0 (graceful degradation)
3. **Missing folders** - Returns empty list, no crash
4. **Production-blocked topics** - Excluded from recommendations
5. **No topic classification** - Skipped when topic filter applied

## Integration Points

### Upstream (Phase 20)
- Uses `extract_winning_patterns()` for pattern multiplier calculation
- Accesses `top_converter_profile`, `channel_strengths`

### Upstream (Phase 18)
- Uses `get_keywords_by_lifecycle('ANALYZED')` for keyword list
- Uses `opportunity_score_final` and `opportunity_category` from database

### Downstream (User Workflow)
- Recommendation action links to `python orchestrator.py "keyword" --report`
- Integrates with `/research --new "keyword"` for next step

## Deviations from Plan

None - plan executed exactly as written.

## Success Criteria Verified

- [x] `python recommender.py` shows ranked recommendations
- [x] No topics from `_IN_PRODUCTION/` or `_ARCHIVED/` appear
- [x] Each recommendation shows: opportunity score, pattern multiplier, reasons
- [x] `--json` flag outputs valid JSON
- [x] `.claude/commands/next.md` documents the command with examples
- [x] Integration with existing opportunity scoring confirmed

---

*Summary generated after 21-01-PLAN.md completion*
