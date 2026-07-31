"""Regression pins for growth_data's dimensioned Analytics API fetches."""

import threading
import time

from tools.youtube_analytics import growth_data


class _Request:
    def __init__(self, response):
        self._response = response
        self.execute_calls = []

    def execute(self, **kwargs):
        self.execute_calls.append(kwargs)
        return self._response


class _Reports:
    def __init__(self, response):
        self._response = response
        self.calls = []
        self.requests = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        request = _Request(self._response)
        self.requests.append(request)
        return request


class _AnalyticsService:
    def __init__(self, response):
        self._reports = _Reports(response)

    def reports(self):
        return self._reports


def _stub_backfill_dependencies(monkeypatch, metrics, video_ids=None):
    """Keep run_backfill focused on the metrics-coverage contract."""
    video_ids = video_ids or ["video-a", "video-b"]
    monkeypatch.setattr(growth_data, "fetch_all_video_ids", lambda: video_ids)
    monkeypatch.setattr(
        growth_data,
        "fetch_video_metadata",
        lambda _ids: [{"id": video_id} for video_id in video_ids],
    )
    monkeypatch.setattr(
        growth_data,
        "fetch_video_metrics_bulk",
        lambda _ids: metrics,
    )
    monkeypatch.setattr(growth_data, "fetch_video_ctr_bulk", lambda _ids: {})
    monkeypatch.setattr(
        growth_data,
        "merge_ctr_with_snapshot_fallback",
        lambda ctr_data, _ids: ctr_data,
    )
    monkeypatch.setattr(growth_data, "store_videos", lambda *_args: len(video_ids))
    monkeypatch.setattr(growth_data, "fetch_traffic_sources_per_video", lambda _ids: {})
    monkeypatch.setattr(growth_data, "store_traffic_sources", lambda _rows: 0)
    monkeypatch.setattr(growth_data, "fetch_daily_channel_metrics", lambda **_kwargs: [])
    monkeypatch.setattr(growth_data, "store_daily_metrics", lambda _rows: 0)
    monkeypatch.setattr(growth_data, "fetch_retention_curves", lambda _ids: {})
    monkeypatch.setattr(growth_data, "store_retention_curves", lambda _rows: 0)
    monkeypatch.setattr(growth_data, "fetch_search_terms_per_video", lambda _ids: {})
    monkeypatch.setattr(growth_data, "store_search_terms", lambda _rows: 0)
    monkeypatch.setattr(growth_data, "fetch_subscribed_status_per_video", lambda _ids: {})
    monkeypatch.setattr(growth_data, "store_subscribed_status", lambda _rows: 0)


def test_run_backfill_reports_total_metrics_fetch_miss(monkeypatch, tmp_path):
    _stub_backfill_dependencies(monkeypatch, metrics={})

    result = growth_data.run_backfill(db_path=tmp_path / "analytics.db")

    assert result["errors"] == [
        "Video metrics fetch failed: returned 0 of 2 rows; "
        "last-known metrics preserved"
    ]


def test_run_backfill_reports_partial_metrics_fetch_miss(monkeypatch, tmp_path):
    _stub_backfill_dependencies(
        monkeypatch,
        metrics={"video-a": {"views": 101}},
    )

    result = growth_data.run_backfill(db_path=tmp_path / "analytics.db")

    assert result["errors"] == [
        "Video metrics fetch incomplete: returned 1 of 2 rows; "
        "last-known metrics preserved for 1 video"
    ]


def test_run_backfill_deduplicates_video_ids_before_coverage_check(
    monkeypatch,
    tmp_path,
):
    metrics = {
        "video-a": {"views": 101},
        "video-b": {"views": 202},
    }
    _stub_backfill_dependencies(
        monkeypatch,
        metrics=metrics,
        video_ids=["video-a", "video-a", "video-b"],
    )
    metric_requests = []
    stored_video_ids = []
    monkeypatch.setattr(
        growth_data,
        "fetch_video_metrics_bulk",
        lambda ids: metric_requests.extend(ids) or metrics,
    )
    monkeypatch.setattr(
        growth_data,
        "store_videos",
        lambda videos, *_args: stored_video_ids.extend(v["id"] for v in videos)
        or len(videos),
    )

    result = growth_data.run_backfill(db_path=tmp_path / "analytics.db")

    assert result["errors"] == []
    assert metric_requests == ["video-a", "video-b"]
    assert stored_video_ids == ["video-a", "video-b"]
    assert result["videos_stored"] == 2


def test_fetch_video_metrics_bulk_uses_one_dimensioned_query_and_keeps_shape(
    monkeypatch,
):
    response = {
        "columnHeaders": [
            {"name": "video"},
            {"name": "views"},
            {"name": "estimatedMinutesWatched"},
            {"name": "averageViewDuration"},
            {"name": "averageViewPercentage"},
            {"name": "subscribersGained"},
            {"name": "likes"},
            {"name": "comments"},
            {"name": "shares"},
        ],
        "rows": [
            ["video-a", 101, 202.5, 121, 42.25, 3, 9, 4, 2],
            ["video-b", 303, 404.5, 98, 37.75, 5, 12, 6, 1],
        ],
    }
    service = _AnalyticsService(response)
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: service,
    )

    result = growth_data.fetch_video_metrics_bulk(["video-a", "video-b"])

    assert result == {
        "video-a": {
            "views": 101,
            "watch_time_minutes": 202.5,
            "avg_view_duration_seconds": 121,
            "avg_view_percentage": 42.25,
            "subscribers_gained": 3,
            "likes": 9,
            "comments": 4,
            "shares": 2,
        },
        "video-b": {
            "views": 303,
            "watch_time_minutes": 404.5,
            "avg_view_duration_seconds": 98,
            "avg_view_percentage": 37.75,
            "subscribers_gained": 5,
            "likes": 12,
            "comments": 6,
            "shares": 1,
        },
    }
    assert len(service._reports.calls) == 1
    call = service._reports.calls[0]
    assert call["dimensions"] == "video"
    assert call["filters"] == "video==video-a,video-b"


def test_fetch_video_ctr_bulk_filters_the_dimensioned_query_to_requested_ids(
    monkeypatch,
):
    response = {
        "columnHeaders": [
            {"name": "video"},
            {"name": "views"},
            {"name": "videoThumbnailImpressions"},
            {"name": "videoThumbnailImpressionsClickRate"},
        ],
        "rows": [
            ["video-a", 101, 4000, 0.0525],
            ["video-b", 303, 9000, 0.03125],
        ],
    }
    service = _AnalyticsService(response)
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: service,
    )

    result = growth_data.fetch_video_ctr_bulk(["video-a", "video-b"])

    assert result == {
        "video-a": {"impressions": 4000, "ctr_percent": 5.25},
        "video-b": {"impressions": 9000, "ctr_percent": 3.12},
    }
    assert len(service._reports.calls) == 1
    call = service._reports.calls[0]
    assert call["dimensions"] == "video"
    assert call["filters"] == "video==video-a,video-b"


class _ActivityTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self.active = 0
        self.maximum = 0

    def enter(self):
        with self._lock:
            self.active += 1
            self.maximum = max(self.maximum, self.active)

    def leave(self):
        with self._lock:
            self.active -= 1


class _ConcurrentRequest:
    def __init__(self, tracker, response):
        self._tracker = tracker
        self._response = response

    def execute(self, **_kwargs):
        self._tracker.enter()
        try:
            time.sleep(0.05)
            return self._response
        finally:
            self._tracker.leave()


class _ConcurrentReports:
    def __init__(self, tracker, response):
        self._tracker = tracker
        self._response = response

    def query(self, **_kwargs):
        return _ConcurrentRequest(self._tracker, self._response)


class _ConcurrentService:
    def __init__(self, tracker, response):
        self._reports = _ConcurrentReports(tracker, response)

    def reports(self):
        return self._reports


def test_per_video_reports_use_bounded_concurrency_and_keep_shape(monkeypatch):
    tracker = _ActivityTracker()
    response = {
        "columnHeaders": [
            {"name": "insightTrafficSourceType"},
            {"name": "views"},
            {"name": "estimatedMinutesWatched"},
        ],
        "rows": [["YT_SEARCH", 17, 23.5]],
    }
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: _ConcurrentService(tracker, response),
    )
    video_ids = ["video-a", "video-b", "video-c", "video-d"]

    result = growth_data.fetch_traffic_sources_per_video(video_ids)

    expected_row = {
        "source_type": "YT_SEARCH",
        "views": 17,
        "watch_time_minutes": 23.5,
    }
    assert result == {video_id: [expected_row] for video_id in video_ids}
    assert tracker.maximum >= 2
    assert tracker.maximum <= growth_data.ANALYTICS_MAX_WORKERS


def test_retention_curve_concurrency_keeps_return_shape(monkeypatch):
    tracker = _ActivityTracker()
    response = {"rows": [[0.25, 0.8, None]]}
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: _ConcurrentService(tracker, response),
    )
    video_ids = ["video-a", "video-b"]

    result = growth_data.fetch_retention_curves(video_ids)

    expected_row = {
        "elapsed_ratio": 0.25,
        "audience_watch_ratio": 0.8,
        "relative_performance": None,
    }
    assert result == {video_id: [expected_row] for video_id in video_ids}
    assert 2 <= tracker.maximum <= growth_data.ANALYTICS_MAX_WORKERS


def test_search_term_concurrency_keeps_return_shape(monkeypatch):
    tracker = _ActivityTracker()
    response = {"rows": [["border treaty", 7, 8.5]]}
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: _ConcurrentService(tracker, response),
    )
    video_ids = ["video-a", "video-b"]

    result = growth_data.fetch_search_terms_per_video(video_ids)

    expected_row = {
        "term": "border treaty",
        "views": 7,
        "watch_time_minutes": 8.5,
    }
    assert result == {video_id: [expected_row] for video_id in video_ids}
    assert 2 <= tracker.maximum <= growth_data.ANALYTICS_MAX_WORKERS


def test_subscribed_status_concurrency_keeps_return_shape(monkeypatch):
    tracker = _ActivityTracker()
    response = {"rows": [["SUBSCRIBED", 9, 10.5, 44.4]]}
    monkeypatch.setattr(
        growth_data,
        "get_authenticated_service",
        lambda *_args: _ConcurrentService(tracker, response),
    )
    video_ids = ["video-a", "video-b"]

    result = growth_data.fetch_subscribed_status_per_video(video_ids)

    expected_row = {
        "status": "SUBSCRIBED",
        "views": 9,
        "watch_time_minutes": 10.5,
        "avg_view_percentage": 44.4,
    }
    assert result == {video_id: [expected_row] for video_id in video_ids}
    assert 2 <= tracker.maximum <= growth_data.ANALYTICS_MAX_WORKERS
