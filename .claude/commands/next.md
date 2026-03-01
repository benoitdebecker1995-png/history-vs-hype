---
description: Get ranked topic recommendations based on winning patterns
model: haiku
---

# /next

Get ranked topic recommendations combining opportunity scores with winning patterns from your best-performing videos.

## What It Does

The `/next` command analyzes your ANALYZED keywords and recommends NEW topics by:

1. **Loading winning patterns** from Phase 20 (dominant topic, angles, channel strengths)
2. **Filtering existing work** from `_IN_PRODUCTION/` and `_ARCHIVED/` folders
3. **Calculating pattern multiplier** for topics matching your proven success formula
4. **Ranking by final score** = opportunity_score × pattern_multiplier

## Usage

```bash
# Default: Show top 5 recommendations
/next

# Show more recommendations
/next --limit 10

# Filter by topic type
/next --topic-type territorial
/next --topic-type ideological

# JSON output for automation
/next --json

# Save full report to file
/next --save report.md
```

## Flags Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--limit N` | Number of recommendations | 5 |
| `--topic-type TYPE` | Filter by topic (territorial, ideological, etc.) | None |
| `--json` | Output machine-readable JSON | false |
| `--save PATH` | Save markdown report to file | None |
| `--refresh` | Force refresh patterns (reserved) | false |

## Output Explanation

### Final Score Calculation

```
# With Intel Engine available:
blended_base = opportunity_score × 0.6 + intel_score × 0.4
final_score  = blended_base × pattern_multiplier

# Without Intel Engine:
final_score  = opportunity_score × pattern_multiplier
```

- **Opportunity Score** (0-100): From Phase 18 analysis (demand, competition, production feasibility)
- **Intel Score** (0-100): From YouTube Intelligence Engine (competitor outlier rates, algo alignment, trending, gaps)
- **Pattern Multiplier** (1.0-1.5): Boost based on winning pattern match

The Intel Score is automatically included when `intel.db` exists. It adds competitor signal data, algorithm alignment heuristics, trending topic overlap, and gap opportunity analysis to each recommendation.

### Pattern Multiplier Breakdown

| Condition | Boost | Example |
|-----------|-------|---------|
| Matches dominant topic | +0.30 | Topic is "territorial" when top converters are territorial |
| Matches dominant angles | +0.20 | Has "legal" angle when top converters use legal |
| High channel strength | +0.10 | Topic maps to strength score > 70/100 |
| **Maximum** | **1.50** | Base score boosted by 50% |

### Exclusion Logic

Keywords are filtered out if:
- Already in `video-projects/_IN_PRODUCTION/` folder
- Already in `video-projects/_ARCHIVED/` folder
- Marked as production-blocked (requires animation)

Matching uses **word-level comparison**, not substring:
- "iran coup" matches "iran 1953 coup" folder ✓
- "iranian revolution" does NOT match "iran" folder ✓

## Example Output

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
Rank | Score | Mult  | Keyword
------------------------------------------------------------
   1 |  94.3 |  1.30 | treaty of versailles territorial
   2 |  87.5 |  1.20 | sykes picot agreement
   3 |  82.1 |  1.10 | partition of india borders
   4 |  78.9 |  1.00 | library of alexandria destruction
   5 |  76.2 |  1.00 | viking settlement greenland
------------------------------------------------------------

TOP RECOMMENDATION: treaty of versailles territorial
  Score: 94.3/100 (Excellent)
  Pattern Match: Matches dominant topic: territorial, Legal angle: +20%

  Next: python orchestrator.py "treaty of versailles territorial" --report
```

## Scoring Interpretation

| Score Range | Category | Recommendation |
|-------------|----------|----------------|
| 90-100 | Excellent | Immediate priority - strong pattern match + high opportunity |
| 70-89 | Good | High priority - proceed to research phase |
| 50-69 | Fair | Consider - verify sources before committing |
| 30-49 | Low | Low priority - skip or reframe significantly |
| Below 30 | Poor | Not recommended - find alternatives |

## Competitor Gap Analysis (Auto-run)

After showing keyword-based recommendations, surface competitor gap opportunities:

```python
from tools.youtube_analytics.gap_analyzer import GapAnalyzer

ga = GapAnalyzer()
gaps = ga.get_gap_recommendations(limit=5)
# Each gap includes: topic, angle, gap_score, reasoning, competitor_videos, own_videos
```

**Display as a separate section after the main recommendations:**

```
------------------------------------------------------------
COMPETITOR GAPS — uncovered topic-angle combinations
------------------------------------------------------------
#1  war / document-first (score: 85.0)
    No competitor covers war from document-first angle.
    101 competitor videos exist. Strong channel advantage (1.5x).

#2  archaeological / document-first (score: 81.0)
    ...
```

**Integration with keyword scores:**
- If a keyword recommendation overlaps with a high-scoring gap, note the alignment
- Gaps with channel_advantage > 1.2x should be flagged as "strong fit"

If the gap analyzer module is unavailable (import error), skip silently.

## Integration with Workflow

After `/next`, typical workflow:

1. **Review recommendations** and select topic
2. **Start research**: `/research --new "topic name"`
3. **Deep dive**: Topic moves from ANALYZED → RESEARCHING
4. **Continue production cycle**

## Related Commands

| Command | Purpose |
|---------|---------|
| `/discover --opportunity "topic"` | Re-analyze specific topic |
| `/patterns` | View winning patterns used for scoring |
| `/status` | See current project state |

## Requirements

Before `/next` works, you need:

1. **ANALYZED keywords in database**
   ```bash
   cd tools/discovery && python orchestrator.py "your topic"
   ```

2. **Performance data for pattern extraction**
   ```bash
   python -m tools.youtube_analytics.performance --fetch-all
   ```

## Execution

```bash
cd tools/discovery && python recommender.py [flags]
```

---

*Phase 21 - Recommendation Engine*
