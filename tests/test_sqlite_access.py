"""Regression tests for SQLite reads on Windows/workspace paths."""

import sqlite3

import pytest

from tools import sqlite_access


def _make_db(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE facts (value TEXT NOT NULL)")
    conn.execute("INSERT INTO facts VALUES ('known true')")
    conn.commit()
    conn.close()


def test_readonly_uri_encodes_a_path_with_spaces(tmp_path):
    db = tmp_path / "folder with spaces" / "sample.db"
    _make_db(db)

    uri = sqlite_access.readonly_uri(db)

    assert uri.startswith("file:")
    assert "%20" in uri
    assert uri.endswith("?mode=ro")


def test_connect_readonly_reads_but_cannot_write(tmp_path):
    db = tmp_path / "folder with spaces" / "sample.db"
    _make_db(db)

    conn = sqlite_access.connect_readonly(db)
    try:
        assert conn.execute("SELECT value FROM facts").fetchone()[0] == "known true"
        with pytest.raises(sqlite3.OperationalError):
            conn.execute("INSERT INTO facts VALUES ('must fail')")
    finally:
        conn.close()


def test_connect_readonly_retries_lockless_workspace_as_immutable(tmp_path, monkeypatch):
    db = tmp_path / "folder with spaces" / "sample.db"
    _make_db(db)
    real_connect = sqlite3.connect
    calls = []

    class DeferredOpenFailure:
        """sqlite3.connect can succeed before the first statement opens the file."""

        def execute(self, *_args, **_kwargs):
            raise sqlite3.OperationalError("unable to open database file")

        def close(self):
            return None

    def lockless_drive_connect(target, *args, **kwargs):
        calls.append(str(target))
        if len(calls) == 1:
            return DeferredOpenFailure()
        return real_connect(target, *args, **kwargs)

    monkeypatch.setattr(sqlite_access.sqlite3, "connect", lockless_drive_connect)

    conn = sqlite_access.connect_readonly(db)
    try:
        assert conn.execute("SELECT value FROM facts").fetchone()[0] == "known true"
    finally:
        conn.close()

    assert len(calls) == 2
    assert calls[0].endswith("?mode=ro")
    assert calls[1].endswith("?mode=ro&immutable=1")


def test_connect_readonly_refuses_immutable_fallback_with_wal(tmp_path, monkeypatch):
    db = tmp_path / "sample.db"
    _make_db(db)
    db.with_name(db.name + "-wal").write_bytes(b"active wal")

    def fail_open(*_args, **_kwargs):
        raise sqlite3.OperationalError("unable to open database file")

    monkeypatch.setattr(sqlite_access.sqlite3, "connect", fail_open)

    with pytest.raises(sqlite3.OperationalError, match="unable to open database file"):
        sqlite_access.connect_readonly(db)


def test_connect_readonly_rejects_missing_database(tmp_path):
    with pytest.raises(FileNotFoundError):
        sqlite_access.connect_readonly(tmp_path / "missing.db")
