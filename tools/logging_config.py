"""
Shared logging configuration for History vs Hype tools.

All tools/ CLI entry points call setup_logging() once in their main() function.
All tools/ modules use get_logger(__name__) for their module-level logger.

The 'tools' logger is configured as the root of the tools hierarchy.
All tools.discovery.*, tools.youtube_analytics.*, tools.intel.* child loggers
inherit the configuration automatically through Python's propagation mechanism.

Usage in CLI entry points:
    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

Usage in modules:
    from tools.logging_config import get_logger
    logger = get_logger(__name__)
"""

import logging
import sys


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging for History vs Hype tools.

    Called once in main() of each CLI entry point.
    All tools.* child loggers inherit this configuration automatically.

    Configures the 'tools' logger (NOT the root Python logger) to avoid
    interfering with third-party library logging.

    Args:
        verbose: If True, show DEBUG messages with module name prefix.
        quiet:   If True, show only ERROR messages.

    Raises:
        ValueError: If both verbose and quiet are True (they are mutually exclusive).
    """
    if verbose and quiet:
        raise ValueError("verbose and quiet are mutually exclusive")

    root = logging.getLogger("tools")

    # Set log level
    if quiet:
        root.setLevel(logging.ERROR)
    elif verbose:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)

    # Clear any handlers added by previous calls (prevents duplicate output in tests)
    root.handlers.clear()

    # Create handler pointing to stderr
    handler = logging.StreamHandler(sys.stderr)

    # Use color formatter when stderr is a TTY, plain formatter otherwise
    use_color = sys.stderr.isatty()
    if use_color:
        try:
            import colorama
            colorama.init()
            formatter = _ColorFormatter(_verbose_fmt() if verbose else _default_fmt())
        except ImportError:
            formatter = logging.Formatter(_verbose_fmt() if verbose else _default_fmt())
    else:
        formatter = logging.Formatter(_verbose_fmt() if verbose else _default_fmt())

    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Don't propagate to the root Python logger
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a module-level logger.

    Usage in any tools/ module:
        from tools.logging_config import get_logger
        logger = get_logger(__name__)

    The returned logger is a child of the 'tools' root logger and inherits
    its configuration automatically through Python's propagation mechanism.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        logging.Logger instance.
    """
    return logging.getLogger(name)


def _default_fmt() -> str:
    """Return the default log format string (level + message only)."""
    return "%(levelname)s: %(message)s"


def _verbose_fmt() -> str:
    """Return the verbose log format string (adds module name prefix)."""
    return "[%(name)s] %(levelname)s: %(message)s"


_VALID_FRESHNESS_TABLES = {
    'keywords': {'last_updated', 'updated_at', 'created_at'},
    'competitor_videos': {'fetched_at', 'updated_at'},
    'ctr_snapshots': {'snapshot_date', 'updated_at'},
    'video_performance': {'updated_at', 'fetched_at'},
    'algo_snapshots': {'created_at'},
    'niche_snapshots': {'created_at'},
}


def check_db_freshness(db_path: str, table: str = 'keywords',
                       date_column: str = 'updated_at',
                       warn_days: int = 7) -> dict:
    """Check how stale a database table is and warn if old.

    Args:
        db_path: Path to SQLite database
        table: Table name to check (must be in _VALID_FRESHNESS_TABLES)
        date_column: Column containing last-updated timestamp
        warn_days: Number of days before warning

    Returns:
        {'days_old': int, 'is_stale': bool, 'last_updated': str}
        {'error': msg} if check fails
    """
    import sqlite3
    from pathlib import Path
    from datetime import datetime, timezone

    if table not in _VALID_FRESHNESS_TABLES:
        return {'error': f'Invalid table: {table!r} (allowed: {sorted(_VALID_FRESHNESS_TABLES)})'}
    if date_column not in _VALID_FRESHNESS_TABLES[table]:
        return {'error': f'Invalid column: {date_column!r} for table {table!r}'}

    path = Path(db_path)
    if not path.exists():
        return {'error': f'Database not found: {db_path}'}

    try:
        conn = sqlite3.connect(str(path))
        cur = conn.cursor()
        # table and date_column are validated against _VALID_FRESHNESS_TABLES above
        cur.execute(f"SELECT MAX({date_column}) FROM {table}")
        row = cur.fetchone()
        conn.close()

        if not row or not row[0]:
            return {'days_old': 999, 'is_stale': True, 'last_updated': 'never'}

        last = row[0][:10]  # Take date part only
        last_dt = datetime.strptime(last, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_old = (now - last_dt).days

        return {
            'days_old': days_old,
            'is_stale': days_old > warn_days,
            'last_updated': last,
        }
    except (sqlite3.Error, ValueError) as e:
        return {'error': str(e)}


class _ColorFormatter(logging.Formatter):
    """Adds ANSI colors to levelname when stderr is a TTY.

    Creates a copy of the log record to avoid mutating the original,
    which could affect other handlers sharing the same record.
    """

    _COLORS = {
        "DEBUG":    "\033[36m",    # cyan
        "INFO":     "\033[32m",    # green
        "WARNING":  "\033[33m",    # yellow
        "ERROR":    "\033[31m",    # red
        "CRITICAL": "\033[31;1m",  # bold red
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelname, "")
        # Make a copy to avoid mutating the original record
        colored_record = logging.makeLogRecord(record.__dict__)
        if color:
            colored_record.levelname = f"{color}{record.levelname}{self._RESET}"
        return super().format(colored_record)
