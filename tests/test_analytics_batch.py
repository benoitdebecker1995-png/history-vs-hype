"""Tests for batched YouTube Analytics queries.

These pin the behaviours that the per-video loops had implicitly and that a
batched query does NOT get for free: every id present as a key, a per-video
row cap, correct paging, and never raising on API failure.
"""
from unittest.mock import MagicMock

from tools.youtube_analytics import analytics_batch as ab
from tools.youtube_analytics.analytics_batch import (
    fetch_metrics_for_videos,
    query_grouped_by_video,
)


def _analytics(pages):
    """Mock whose reports().query().execute() returns each page in turn."""
    analytics = MagicMock()
    analytics.reports.return_value.query.return_value.execute.side_effect = list(pages)
    return analytics


def _query_kwargs(analytics, call=0):
    return analytics.reports.return_value.query.call_args_list[call].kwargs


def test_groups_rows_and_strips_video_column():
    a = _analytics([{"rows": [["v1", "US", 10, 5.0, 1], ["v1", "GB", 3, 1.0, 0],
                              ["v2", "DE", 7, 2.0, 2]]}])

    out = query_grouped_by_video(a, video_ids=["v1", "v2"], dimensions="country",
                                 metrics="views,estimatedMinutesWatched,subscribersGained",
                                 start_date="2024-01-01", end_date="2026-12-31")

    assert out == {"v1": [["US", 10, 5.0, 1], ["GB", 3, 1.0, 0]],
                   "v2": [["DE", 7, 2.0, 2]]}


def test_video_with_no_rows_still_gets_a_key():
    """The per-video loop wrote result[vid] even when the row list was empty.
    Callers index by video id, so a missing key would be a KeyError."""
    a = _analytics([{"rows": [["v1", "US", 10, 5.0, 1]]}])

    out = query_grouped_by_video(a, video_ids=["v1", "v2"], dimensions="country",
                                 metrics="views", start_date="x", end_date="y")

    assert out["v2"] == []
    assert set(out) == {"v1", "v2"}


def test_prepends_video_dimension_and_sorts_deterministically():
    a = _analytics([{"rows": []}])

    query_grouped_by_video(a, video_ids=["v1"], dimensions="country",
                           metrics="views", start_date="x", end_date="y")

    kw = _query_kwargs(a)
    assert kw["dimensions"] == "video,country"
    assert kw["sort"] == "video,country"      # paging is unsafe without a sort
    assert kw["filters"] == "video==v1"


def test_extra_filters_are_semicolon_joined():
    a = _analytics([{"rows": []}])

    query_grouped_by_video(a, video_ids=["v1"], dimensions="d", metrics="views",
                           start_date="x", end_date="y",
                           extra_filters="insightTrafficSourceType==YT_SEARCH")

    assert _query_kwargs(a)["filters"] == "video==v1;insightTrafficSourceType==YT_SEARCH"


def test_pages_until_short_page(monkeypatch):
    """A full page means there may be more; a short page ends it."""
    monkeypatch.setattr(ab, "PAGE_SIZE", 2)
    a = _analytics([
        {"rows": [["v1", "US", 1], ["v1", "GB", 2]]},   # full -> keep going
        {"rows": [["v1", "DE", 3]]},                    # short -> stop
    ])

    out = query_grouped_by_video(a, video_ids=["v1"], dimensions="country",
                                 metrics="views", start_date="x", end_date="y")

    assert out["v1"] == [["US", 1], ["GB", 2], ["DE", 3]]
    assert _query_kwargs(a, 0)["startIndex"] == 1
    assert _query_kwargs(a, 1)["startIndex"] == 3


def test_chunks_large_id_lists(monkeypatch):
    monkeypatch.setattr(ab, "VIDEO_CHUNK", 2)
    a = _analytics([{"rows": []}, {"rows": []}])

    query_grouped_by_video(a, video_ids=["v1", "v2", "v3"], dimensions="country",
                           metrics="views", start_date="x", end_date="y")

    assert _query_kwargs(a, 0)["filters"] == "video==v1,v2"
    assert _query_kwargs(a, 1)["filters"] == "video==v3"


def test_api_failure_returns_empty_lists_not_an_exception():
    a = MagicMock()
    a.reports.return_value.query.return_value.execute.side_effect = RuntimeError("boom")

    out = query_grouped_by_video(a, video_ids=["v1"], dimensions="country",
                                 metrics="views", start_date="x", end_date="y")

    assert out == {"v1": []}


def test_empty_video_list_short_circuits():
    a = MagicMock()

    assert query_grouped_by_video(a, video_ids=[], dimensions="country",
                                  metrics="views", start_date="x", end_date="y") == {}
    a.reports.assert_not_called()


# ---------------------------------------------------------------- metrics ---

def test_metrics_maps_api_names_to_snake_case_with_casts():
    a = _analytics([{
        "columnHeaders": [{"name": n} for n in (
            "video", "views", "estimatedMinutesWatched", "averageViewDuration",
            "likes", "dislikes", "comments", "shares",
            "subscribersGained", "subscribersLost")],
        "rows": [["v1", 100, 250.5, 42, 6, 0, 1, 2, 3, 1]],
    }])

    out = fetch_metrics_for_videos(a, video_ids=["v1"], start_date="x", end_date="y")

    assert out["v1"] == {
        "video_id": "v1", "views": 100, "watch_time_minutes": 250.5,
        "avg_view_duration_seconds": 42, "likes": 6, "dislikes": 0,
        "comments": 1, "shares": 2, "subscribers_gained": 3, "subscribers_lost": 1,
    }
    assert isinstance(out["v1"]["watch_time_minutes"], float)


def test_metrics_omits_videos_the_api_returned_no_row_for():
    """Unlike query_grouped_by_video, absence is meaningful here: the caller
    counts these as failed_videos and excludes them from the average."""
    a = _analytics([{
        "columnHeaders": [{"name": "video"}, {"name": "views"}],
        "rows": [["v1", 5]],
    }])

    out = fetch_metrics_for_videos(a, video_ids=["v1", "v2"], start_date="x", end_date="y")

    assert set(out) == {"v1"}


def test_metrics_failure_is_not_fatal():
    a = MagicMock()
    a.reports.return_value.query.return_value.execute.side_effect = RuntimeError("boom")

    assert fetch_metrics_for_videos(a, video_ids=["v1"], start_date="x", end_date="y") == {}
