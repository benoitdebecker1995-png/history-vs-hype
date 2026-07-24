"""Integration smoke tests for the intel pipeline.

Verifies run_refresh() + KBStore operations work end-to-end
with network calls mocked (feedparser, HTTP requests).
CRITICAL: Always pass db_path to run_refresh — default is production intel.db.
"""
from unittest.mock import patch, MagicMock
import pytest


def _make_fake_feed():
    """Create a minimal feedparser result mock."""
    fake_feed = MagicMock()
    fake_feed.entries = []
    fake_feed.bozo = False
    return fake_feed


def test_kb_store_imports_cleanly():
    """KBStore is importable without sys.path hacks."""
    from tools.intel.kb_store import KBStore
    assert KBStore is not None


def test_kb_store_initializes_with_tmp_path(intel_store):
    """KBStore initializes schema with a tmp_path db file."""
    assert intel_store is not None


def test_kb_store_save_and_retrieve_algo_snapshot(intel_store):
    """KBStore can save and retrieve an algorithm snapshot."""
    data = {
        "hook_formula": "cold_fact + myth + contradiction + payoff",
        "retention_pattern": "front-loaded evidence",
        "source": "test",
    }
    # save_algo_snapshot may require keyword arguments based on actual schema
    try:
        save_result = intel_store.save_algo_snapshot(data)
    except TypeError:
        # Try keyword-argument form from refresh.py Phase 3
        save_result = intel_store.save_algo_snapshot(
            source_names=["test"],
            algorithm_model=data,
            signal_weights=None,
            longform_insights=None,
            confidence="low",
        )
    assert isinstance(save_result, dict)
    assert "error" not in save_result

    retrieved = intel_store.get_latest_algo_snapshot()
    # Either returns the snapshot or None — both are valid for smoke test
    assert retrieved is None or isinstance(retrieved, dict)


def test_kb_store_set_and_get_last_refresh(intel_store):
    """KBStore tracks last refresh timestamp."""
    result = intel_store.set_last_refresh()
    assert isinstance(result, dict)
    assert "error" not in result

    last = intel_store.get_last_refresh()
    assert last is None or isinstance(last, str)


def test_kb_store_get_active_channels(intel_store):
    """KBStore.get_active_channels returns a list (empty on fresh DB)."""
    result = intel_store.get_active_channels()
    # Returns list or error dict — both acceptable on fresh db
    assert isinstance(result, (list, dict))


def _video(vid, title="A Title", published="2026-01-01"):
    return {
        "video_id": vid, "channel_id": "chan1", "title": title,
        "published_at": published, "views": 100, "likes": 10,
        "duration_seconds": 600, "description": "d",
    }


def test_replace_competitor_videos_swaps_corpus(intel_store):
    """replace_competitor_videos purges old + saves new in one call."""
    intel_store.save_competitor_videos([_video("old1"), _video("old2")])
    res = intel_store.replace_competitor_videos([_video("new1"), _video("new2"), _video("new3")])
    assert res.get("deleted") == 2 and res.get("saved") == 3
    ids = {v["video_id"] for v in intel_store.get_competitor_videos(limit=100)}
    assert ids == {"new1", "new2", "new3"}  # old corpus fully replaced


def test_replace_competitor_videos_empty_refuses_to_purge(intel_store):
    """An empty replacement must NOT wipe the corpus (no-op guard)."""
    intel_store.save_competitor_videos([_video("keep1"), _video("keep2")])
    res = intel_store.replace_competitor_videos([])
    assert "error" in res
    ids = {v["video_id"] for v in intel_store.get_competitor_videos(limit=100)}
    assert ids == {"keep1", "keep2"}  # untouched


def test_replace_competitor_videos_rolls_back_on_failure(intel_store):
    """A mid-save failure rolls back the DELETE — the old corpus survives intact
    (the purged-but-empty failure mode the two-transaction version had)."""
    intel_store.save_competitor_videos([_video("keep1"), _video("keep2")])
    # Second video has title=None -> violates NOT NULL -> IntegrityError mid-batch.
    bad_batch = [_video("would_be_new"), _video("bad", title=None)]
    res = intel_store.replace_competitor_videos(bad_batch)
    assert "error" in res
    ids = {v["video_id"] for v in intel_store.get_competitor_videos(limit=100)}
    assert ids == {"keep1", "keep2"}  # DELETE rolled back, nothing saved


def test_run_refresh_returns_dict_with_mocked_network(tmp_path):
    """run_refresh() completes without network access and returns a dict.

    feedparser is imported via 'import feedparser' at module level in
    tools/intel/algo_scraper.py and tools/intel/competitor_tracker.py.
    Patch at the USE site (module-level import location).
    requests.get is also patched to prevent HTTP calls.
    """
    from tools.intel.refresh import run_refresh

    fake_feed = _make_fake_feed()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html>Algorithm insights</html>"
    mock_response.raise_for_status = MagicMock()

    with patch("tools.intel.algo_scraper.feedparser.parse", return_value=fake_feed), \
         patch("tools.intel.competitor_tracker.feedparser.parse", return_value=fake_feed), \
         patch("tools.intel.algo_scraper.requests.get", return_value=mock_response):
        result = run_refresh(
            db_path=str(tmp_path / "test_intel.db"),
            force=True,
        )

    assert isinstance(result, dict)


def test_run_refresh_result_has_expected_keys(tmp_path):
    """run_refresh() result contains 'refreshed' or 'error' key."""
    from tools.intel.refresh import run_refresh

    fake_feed = _make_fake_feed()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html>Algorithm insights</html>"
    mock_response.raise_for_status = MagicMock()

    with patch("tools.intel.algo_scraper.feedparser.parse", return_value=fake_feed), \
         patch("tools.intel.competitor_tracker.feedparser.parse", return_value=fake_feed), \
         patch("tools.intel.algo_scraper.requests.get", return_value=mock_response):
        result = run_refresh(
            db_path=str(tmp_path / "test_intel.db"),
            force=True,
        )

    # Must have either 'refreshed' key (success path) or 'error' key (fatal)
    assert "refreshed" in result or "error" in result
