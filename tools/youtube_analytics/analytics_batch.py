"""
Batched YouTube Analytics queries.

The Analytics API accepts a comma-separated video filter and will return a
`video` dimension alongside the one you actually want, so N videos cost ONE
request instead of N. Three analysis modules were looping one request per video
(58 videos = 58 round-trips each, ~110s of wall time for geography + traffic
alone) before 2026-07-30.

This module owns the two fiddly parts that would otherwise be copy-pasted three
times: chunking the video filter, and paging rows within a chunk.

    from tools.youtube_analytics.analytics_batch import query_grouped_by_video

    grouped = query_grouped_by_video(
        analytics,
        video_ids=ids,
        dimensions='country',                 # 'video' is prepended for you
        metrics='views,estimatedMinutesWatched,subscribersGained',
        start_date='2024-01-01', end_date='2026-12-31',
    )
    # -> {video_id: [[country, views, watch, subs], ...]}   (video column stripped)

Every requested id is present as a key, even when the API returns no rows for
it — the per-video loops this replaces always wrote an entry, and callers rely
on that.
"""

from typing import Dict, List, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

# The API documents up to 500 ids in a filter. 200 keeps the query string well
# clear of URL length limits (~12 chars per id) while still collapsing this
# channel's whole catalogue into a single request.
VIDEO_CHUNK = 200

# Rows per response page. The channel currently returns ~111 rows for 58 videos,
# so this pages exactly once — but a growing catalogue must not silently truncate.
PAGE_SIZE = 200


_METRIC_FIELDS = (
    ('views',                     'views',                  int),
    ('watch_time_minutes',        'estimatedMinutesWatched', float),
    ('avg_view_duration_seconds', 'averageViewDuration',    int),
    ('likes',                     'likes',                  int),
    ('dislikes',                  'dislikes',               int),
    ('comments',                  'comments',               int),
    ('shares',                    'shares',                 int),
    ('subscribers_gained',        'subscribersGained',      int),
    ('subscribers_lost',          'subscribersLost',        int),
)

METRIC_NAMES = ','.join(api for _, api, _ in _METRIC_FIELDS)


def fetch_metrics_for_videos(
    analytics,
    *,
    video_ids: List[str],
    start_date: str,
    end_date: str,
) -> Dict[str, dict]:
    """Core engagement metrics for many videos in one request.

    Mirrors `metrics.get_video_metrics()`'s snake_case output, minus `title`,
    `date_range` and `fetched_at`. Title is deliberately excluded: it costs a
    separate Data API call per video, and the only batch caller (channel
    averages) never reads it.

    Videos the API returns no row for are simply absent from the result — the
    caller decides what that means, as it did with the old per-video error dict.
    """
    if not video_ids:
        return {}

    out: Dict[str, dict] = {}
    for start in range(0, len(video_ids), VIDEO_CHUNK):
        chunk = video_ids[start:start + VIDEO_CHUNK]
        try:
            response = analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics=METRIC_NAMES,
                dimensions="video",
                filters="video==" + ",".join(chunk),
                maxResults=len(chunk),
            ).execute()
        except Exception as exc:
            logger.warning("Batched metrics query failed for %d videos: %s", len(chunk), exc)
            continue

        headers = [h["name"] for h in response.get("columnHeaders", [])]
        for row in response.get("rows", []):
            data = dict(zip(headers, row))
            vid = data.get("video")
            if not vid:
                continue
            out[vid] = {"video_id": vid, **{
                key: cast(data.get(api, 0)) for key, api, cast in _METRIC_FIELDS
            }}

    return out


def query_grouped_by_video(
    analytics,
    *,
    video_ids: List[str],
    dimensions: str,
    metrics: str,
    start_date: str,
    end_date: str,
    sort: Optional[str] = None,
    extra_filters: str = "",
) -> Dict[str, List[list]]:
    """Run a batched report and group rows by video id.

    `dimensions` must NOT include 'video' — it is prepended, and stripped back
    out of each returned row so callers see the same column layout their
    per-video query produced.

    Never raises: on API failure the affected chunk is logged and skipped, and
    its videos come back with empty lists (matching the old per-video
    try/except, which logged and moved on).
    """
    if not video_ids:
        return {}

    # Pre-seed every id. The per-video loops assigned result[vid] on success even
    # when the row list was empty, so a video with no data must still be a key.
    grouped: Dict[str, List[list]] = {vid: [] for vid in video_ids}

    # Deterministic ordering is required for correct paging: without a sort the
    # API may order rows differently between pages and rows could be lost or
    # duplicated at the boundary.
    sort_spec = sort or f"video,{dimensions.split(',')[0]}"

    for start in range(0, len(video_ids), VIDEO_CHUNK):
        chunk = video_ids[start:start + VIDEO_CHUNK]
        filters = "video==" + ",".join(chunk)
        if extra_filters:
            filters = f"{filters};{extra_filters}"

        index = 1
        while True:
            try:
                response = analytics.reports().query(
                    ids="channel==MINE",
                    startDate=start_date,
                    endDate=end_date,
                    metrics=metrics,
                    dimensions=f"video,{dimensions}",
                    filters=filters,
                    sort=sort_spec,
                    maxResults=PAGE_SIZE,
                    startIndex=index,
                ).execute()
            except Exception as exc:
                logger.warning(
                    "Batched query failed for %d videos (startIndex=%d): %s",
                    len(chunk), index, exc,
                )
                break

            rows = response.get("rows", [])
            for row in rows:
                vid = row[0]
                if vid in grouped:
                    grouped[vid].append(row[1:])

            if len(rows) < PAGE_SIZE:
                break
            index += PAGE_SIZE

    return grouped
