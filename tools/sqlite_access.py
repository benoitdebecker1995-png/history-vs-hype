"""Safe read-only SQLite access across local and lockless workspace drives.

Normal SQLite read-only mode still acquires filesystem locks. Some workspace-mounted
Windows drives allow ordinary file reads but reject those lock handles with
``OperationalError: unable to open database file``. In that narrow case, an immutable
connection is the correct read-only fallback *only* when no WAL/journal sidecar exists.

This module is deliberately read-only. Database writers continue through their owning
stores and normal SQLite connections.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union

from tools.logging_config import get_logger

logger = get_logger(__name__)

PathLike = Union[str, Path]


def readonly_uri(db_path: PathLike, *, immutable: bool = False) -> str:
    """Return a correctly encoded SQLite file URI for an existing path."""
    path = Path(db_path).resolve()
    uri = f"{path.as_uri()}?mode=ro"
    return f"{uri}&immutable=1" if immutable else uri


def _has_live_sidecar(path: Path) -> bool:
    """True when immutable mode could hide uncheckpointed database changes."""
    for suffix in ("-wal", "-journal"):
        sidecar = path.with_name(path.name + suffix)
        try:
            if sidecar.exists() and sidecar.stat().st_size > 0:
                return True
        except OSError:
            return True
    return False


def connect_readonly(db_path: PathLike, *, timeout: float = 0.1) -> sqlite3.Connection:
    """Open an existing SQLite database read-only, with a guarded lockless fallback.

    The normal ``mode=ro`` connection is always attempted first with a short probe
    timeout. Immutable mode is
    retried only for SQLite's "unable to open" failure and only when no WAL/journal
    sidecar exists. The returned connection also has ``query_only`` enabled as a
    second guard against accidental writes.
    """
    path = Path(db_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"SQLite database not found: {path}")

    conn = None
    try:
        conn = sqlite3.connect(readonly_uri(path), uri=True, timeout=timeout)
        conn.execute("PRAGMA query_only=ON")
        # sqlite3.connect() may return before Windows actually opens the file. Force
        # one schema read so a lock-handle failure is caught here and can fall back.
        conn.execute("SELECT 1 FROM sqlite_schema LIMIT 1").fetchone()
    except sqlite3.OperationalError as exc:
        if conn is not None:
            conn.close()
        if "unable to open database file" not in str(exc).lower() or _has_live_sidecar(path):
            raise
        logger.debug("SQLite lockless read fallback: %s", path)
        conn = sqlite3.connect(
            readonly_uri(path, immutable=True), uri=True, timeout=timeout
        )
        conn.execute("PRAGMA query_only=ON")
        conn.execute("SELECT 1 FROM sqlite_schema LIMIT 1").fetchone()
    return conn
