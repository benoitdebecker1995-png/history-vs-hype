# HvH-Reconcile ABORTED — analytics.db stale (168.7h)

The refresher — Routine 7 HvH-GrowthRefresh (07:45, `python -m tools.youtube_analytics.growth_data --refresh`) — likely failed; it, not channel-health, writes analytics.db.
Check `tools/youtube_analytics/` auth (YouTube OAuth token) and retry.
