# Research: Phase 8 - Data Pull Scripts

**Researched:** 2026-01-24
**Phase Goal:** Scripts can pull all key metrics from YouTube Analytics API on demand

## 1. Available Metrics

### Core Engagement (Readily Available)

| Metric | API Field | Description |
|--------|-----------|-------------|
| Views | `views` | Total video views |
| Watch Time | `estimatedMinutesWatched` | Minutes users watched |
| Avg View Duration | `averageViewDuration` | Average playback length (seconds) |
| Likes | `likes` | Positive ratings |
| Dislikes | `dislikes` | Negative ratings |
| Comments | `comments` | Comment count |
| Shares | `shares` | Share button clicks |
| Subscribers Gained | `subscribersGained` | New subscriptions |
| Subscribers Lost | `subscribersLost` | Unsubscriptions |

### CTR / Impressions (Limited Availability)

| Metric | API Field | Notes |
|--------|-----------|-------|
| Thumbnail Impressions | `videoThumbnailImpressions` | Times thumbnail was shown (>1s, >50% visible) |
| Thumbnail CTR | `videoThumbnailImpressionsClickRate` | Clicks / Impressions percentage |

**CTR Limitation:** Per [Google Issue Tracker #254665034](https://issuetracker.google.com/issues/254665034), CTR metrics may not be available in all report types. Testing needed to confirm availability for channel reports.

### Audience Retention (Special Report)

| Metric | API Field | Description |
|--------|-----------|-------------|
| Absolute Retention | `audienceWatchRatio` | % of viewers at each point |
| Relative Retention | `relativeRetentionPerformance` | 0-1 score vs similar-length videos |
| Video Position | `elapsedVideoTimeRatio` | 0.0 to 1.0 (start to end) |

## 2. API Query Patterns

### Basic Video Stats Query

```python
response = youtube_analytics.reports().query(
    ids='channel==MINE',
    startDate='2025-01-01',
    endDate='2026-01-24',
    metrics='views,estimatedMinutesWatched,averageViewDuration,likes,comments,shares,subscribersGained',
    dimensions='video',
    filters='video==VIDEO_ID',
    maxResults=1
).execute()
```

### CTR Query (if available)

```python
response = youtube_analytics.reports().query(
    ids='channel==MINE',
    startDate='2025-01-01',
    endDate='2026-01-24',
    metrics='views,videoThumbnailImpressions,videoThumbnailImpressionsClickRate',
    dimensions='video',
    filters='video==VIDEO_ID',
    maxResults=1
).execute()
```

### Retention Curve Query

```python
response = youtube_analytics.reports().query(
    ids='channel==MINE',
    startDate='2025-01-01',
    endDate='2026-01-24',
    metrics='audienceWatchRatio,relativeRetentionPerformance',
    dimensions='elapsedVideoTimeRatio',
    filters='video==VIDEO_ID;audienceType==ORGANIC',
    maxResults=200,  # Required: max 200 data points
    sort='elapsedVideoTimeRatio'  # Required for retention reports
).execute()
```

**Retention Report Constraints:**
- Single video ID only (no batch)
- `maxResults` must be ≤ 200
- `sort` parameter is required
- Returns ~100 data points (video divided into segments)

## 3. Error Handling

### Common API Errors

| Error | Cause | Handling |
|-------|-------|----------|
| 403 Forbidden | API not enabled, quota exceeded, or scope issue | Check API status, retry with backoff |
| 400 Bad Request | Invalid video ID or date range | Validate inputs before query |
| 401 Unauthorized | Token expired | Refresh token automatically |
| 429 Too Many Requests | Rate limit hit | Exponential backoff |

### Quota Considerations

- Default quota: 10,000 units/day
- Basic query: ~1 unit
- Retention query: Higher cost (more data points)
- Recommendation: Cache results, don't re-fetch same data

## 4. Output Format Recommendation

### JSON Structure (for downstream processing)

```json
{
  "video_id": "ABC123",
  "title": "Video Title",
  "published": "2025-12-01",
  "metrics": {
    "views": 19767,
    "watch_time_minutes": 8017,
    "avg_view_duration_seconds": 243,
    "likes": 542,
    "comments": 87,
    "shares": 23,
    "subscribers_gained": 15,
    "ctr_percent": 4.2,
    "impressions": 470643
  },
  "retention": {
    "data_points": 100,
    "avg_retention_percent": 35.2,
    "drop_off_points": [
      {"position": 0.15, "retention": 0.62, "note": "15% mark"},
      {"position": 0.50, "retention": 0.35, "note": "midpoint"}
    ]
  },
  "fetched_at": "2026-01-24T10:30:00Z"
}
```

### Markdown Structure (for human reading)

```markdown
# Video Analysis: [Title]

**Video ID:** ABC123
**Published:** 2025-12-01
**Data fetched:** 2026-01-24

## Performance Metrics

| Metric | Value |
|--------|-------|
| Views | 19,767 |
| Watch Time | 133.6 hours |
| Avg Duration | 4:03 |
| CTR | 4.2% |

## Retention Curve

[Key drop-off points identified]
```

## 5. Script Architecture

### Recommended Structure

```
tools/youtube-analytics/
├── auth.py              # Already exists (Phase 7)
├── metrics.py           # Core metrics fetcher
├── retention.py         # Retention curve fetcher
├── video_report.py      # Combined report generator
└── utils/
    ├── cache.py         # Result caching
    └── format.py        # JSON/Markdown formatters
```

### Separation of Concerns

1. **metrics.py** — Fetches views, watch time, engagement (INTEG-05)
2. **retention.py** — Fetches retention curve with drop-offs (INTEG-04)
3. **ctr.py** — Attempts CTR fetch, falls back gracefully (INTEG-03)
4. **video_report.py** — Orchestrates all three, outputs combined report

## 6. CTR Fallback Strategy

Since CTR may not be available via API:

1. **Try API first** — Query `videoThumbnailImpressionsClickRate`
2. **If 400/403** — Log "CTR not available via API"
3. **Fallback** — Prompt user to input CTR from YouTube Studio manually
4. **Document** — Note in output that CTR was manually entered

## 7. Date Range Handling

- **Default:** Last 30 days from today
- **Custom:** Accept `--start-date` and `--end-date` flags
- **Video lifetime:** From publish date to today
- **Format:** YYYY-MM-DD (API requirement)

## Sources

- [YouTube Analytics API Metrics](https://developers.google.com/youtube/analytics/metrics)
- [Sample API Requests](https://developers.google.com/youtube/analytics/sample-requests)
- [Python Code Samples](https://github.com/youtube/api-samples/blob/master/python/yt_analytics_report.py)
- [Reports Query Reference](https://developers.google.com/youtube/analytics/reference/reports/query)

---

*Research complete: 2026-01-24*
