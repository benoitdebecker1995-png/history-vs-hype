---
description: Channel growth dashboard — velocity, ROI, traffic, monetization countdown
model: haiku
---

# /growth - Growth Dashboard

Show channel growth trajectory, per-video ROI, traffic source breakdown, and monetization countdown projections.

## Usage

```
/growth                    # Full dashboard
/growth --velocity         # Subscriber velocity trend only
/growth --roi [sort]       # Per-video ROI (sort: views, subs, conversion_rate, ctr, retention)
/growth --traffic          # Traffic source breakdown
/growth --countdown        # Monetization countdown only
/growth --subs N           # Override current subscriber count for projections
```

## Execution

```python
from tools.youtube_analytics.growth_dashboard import GrowthDashboard

gd = GrowthDashboard()

# Full report (text output)
print(gd.full_report(current_subs=471))

# Or individual sections:
velocity = gd.subscriber_velocity()
roi = gd.per_video_roi('conversion_rate')
traffic = gd.traffic_breakdown()
countdown = gd.monetization_countdown(current_subs=471)
```

## CLI Alternative

```bash
python -m tools.youtube_analytics.growth_dashboard --subs 471
python -m tools.youtube_analytics.growth_dashboard --roi views
python -m tools.youtube_analytics.growth_dashboard --countdown --json
```

## Dashboard Sections

### 1. Monetization Countdown (GROW-04)
- Progress bars for subscribers (1K target) and watch hours (4K target)
- Monthly growth rates
- Projected YPP eligibility date

### 2. Subscriber Velocity (GROW-01)
- Monthly net subscribers with trend detection (accelerating/decelerating/stable)
- Best and worst months
- Visual bar chart

### 3. Per-Video ROI (GROW-02)
- Every video ranked by conversion rate (subs/views)
- Shows: views, subs gained, conversion %, CTR %, retention %
- Sortable by any metric

### 4. Traffic Sources (GROW-03)
- Channel-wide traffic breakdown with percentages
- Visual bars showing relative contribution
- Per-video drill-down available

## Data Requirements

Requires `analytics.db` populated by Phase 55 (`growth_data.py`).

To refresh data:
```bash
python -m tools.youtube_analytics.growth_data --refresh
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/status` | Project status and next action |
| `/next` | Topic recommendations |
| `/patterns` | Cross-video pattern analysis |
| `/analyze` | Post-publish analysis for specific video |

---

*Phase 59 - Growth Dashboard (v5.2)*
