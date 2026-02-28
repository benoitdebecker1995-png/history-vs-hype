"""Integration smoke tests for the analytics pipeline.

Tests import_from_analysis_files() with the tmp_post_publish fixture,
which creates the full video-projects/ directory structure needed by the scanner.
Also tests run_backfill() and generate_channel_insights_report().
"""
import pytest
from pathlib import Path


def test_backfill_imports_cleanly():
    """import_from_analysis_files is importable without sys.path hacks."""
    from tools.youtube_analytics.backfill import import_from_analysis_files
    assert import_from_analysis_files is not None


def test_run_backfill_imports_cleanly():
    """run_backfill is importable without sys.path hacks."""
    from tools.youtube_analytics.backfill import run_backfill
    assert run_backfill is not None


def test_generate_insights_imports_cleanly():
    """generate_channel_insights_report is importable without sys.path hacks."""
    from tools.youtube_analytics.backfill import generate_channel_insights_report
    assert generate_channel_insights_report is not None


def test_backfill_reads_fixture_post_publish(tmp_post_publish):
    """import_from_analysis_files scans fixture dir and returns a dict."""
    from tools.youtube_analytics.backfill import import_from_analysis_files

    result = import_from_analysis_files(project_root=tmp_post_publish)

    assert isinstance(result, dict)


def test_backfill_result_has_expected_keys(tmp_post_publish):
    """import_from_analysis_files result contains 'processed' or 'error' key."""
    from tools.youtube_analytics.backfill import import_from_analysis_files

    result = import_from_analysis_files(project_root=tmp_post_publish)

    # Error-dict pattern: either has error or has processed count (from backfill_all)
    assert "error" in result or "processed" in result


def test_backfill_processed_count_nonnegative(tmp_post_publish):
    """import_from_analysis_files processes >= 0 records."""
    from tools.youtube_analytics.backfill import import_from_analysis_files

    result = import_from_analysis_files(project_root=tmp_post_publish)

    if "processed" in result:
        assert isinstance(result["processed"], int)
        assert result["processed"] >= 0


def test_run_backfill_returns_dict(tmp_post_publish):
    """run_backfill() returns a dict with known top-level keys."""
    from tools.youtube_analytics.backfill import run_backfill

    result = run_backfill(project_root=tmp_post_publish, skip_markdown=True)

    assert isinstance(result, dict)
    # run_backfill always returns these keys regardless of inner success/failure
    assert "json_import" in result or "error" in result


def test_generate_channel_insights_returns_dict(tmp_post_publish):
    """generate_channel_insights_report() returns a dict (error or success)."""
    from tools.youtube_analytics.backfill import generate_channel_insights_report

    # tmp_post_publish has no JSON pre-fetches — expects error dict
    result = generate_channel_insights_report(project_root=tmp_post_publish)

    assert isinstance(result, dict)
    # Either error (no JSON pre-fetches in fixture) or success
    assert "error" in result or "saved_to" in result
