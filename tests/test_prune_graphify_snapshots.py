"""Tests for graphify snapshot retention.

Each test pins a way this could delete something it shouldn't. The module
removes gigabytes, so the guards matter more than the happy path.
"""
import pytest

from tools.routines.prune_graphify_snapshots import find_snapshots, prune


def _snapshot(root, name, size=32):
    d = root / name
    d.mkdir(parents=True)
    (d / "graph.json").write_text("x" * size, encoding="utf-8")
    return d


def test_finds_only_dated_dirs(tmp_path):
    """research/, cache/ and loose files are live artifacts, never candidates."""
    _snapshot(tmp_path, "2026-06-12")
    _snapshot(tmp_path, "research")
    _snapshot(tmp_path, "cache")
    (tmp_path / "graph.json").write_text("live", encoding="utf-8")
    (tmp_path / "graph.full.json.bak").write_text("restore", encoding="utf-8")

    assert [p.name for p in find_snapshots(tmp_path)] == ["2026-06-12"]


def test_suffix_sorts_numerically_not_lexically(tmp_path):
    """'_2' is older than '_10'. String sort gets this backwards, which would
    silently retain the oldest snapshots and delete the newest."""
    for name in ("2026-06-12", "2026-06-12_2", "2026-06-12_10", "2026-06-12_9"):
        _snapshot(tmp_path, name)

    assert [p.name for p in find_snapshots(tmp_path)] == [
        "2026-06-12", "2026-06-12_2", "2026-06-12_9", "2026-06-12_10",
    ]


def test_keeps_the_newest_n(tmp_path):
    for name in ("2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04"):
        _snapshot(tmp_path, name)

    result = prune(keep=2, apply=True, graphify_dir=tmp_path)

    assert result["kept"] == ["2026-06-03", "2026-06-04"]
    assert result["deleted"] == ["2026-06-01", "2026-06-02"]
    assert not (tmp_path / "2026-06-01").exists()
    assert (tmp_path / "2026-06-04").exists()


def test_dry_run_deletes_nothing(tmp_path):
    _snapshot(tmp_path, "2026-06-01")
    _snapshot(tmp_path, "2026-06-02")

    result = prune(keep=1, apply=False, graphify_dir=tmp_path)

    assert result["deleted"] == ["2026-06-01"]      # reported
    assert (tmp_path / "2026-06-01").exists()        # but still on disk
    assert result["bytes_freed"] > 0                 # size still measured


def test_keep_zero_is_refused(tmp_path):
    """Guard: --keep 0 would wipe every snapshot including the live-adjacent one."""
    _snapshot(tmp_path, "2026-06-01")

    result = prune(keep=0, apply=True, graphify_dir=tmp_path)

    assert "error" in result
    assert (tmp_path / "2026-06-01").exists()


def test_keep_larger_than_population_deletes_nothing(tmp_path):
    _snapshot(tmp_path, "2026-06-01")

    result = prune(keep=10, apply=True, graphify_dir=tmp_path)

    assert result["deleted"] == []
    assert result["kept"] == ["2026-06-01"]


def test_missing_directory_is_not_an_error(tmp_path):
    """Read-side contract: never raise."""
    result = prune(keep=3, apply=True, graphify_dir=tmp_path / "does-not-exist")

    assert result["deleted"] == []
    assert "error" not in result
