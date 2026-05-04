"""Unit tests for tools.logging_config.

Covers the E1 audit contract: setup_logging() must produce INFO by default,
DEBUG when verbose=True, ERROR when quiet=True, and reject the
mutually-exclusive verbose+quiet combo.
"""
import logging

import pytest

from tools.logging_config import setup_logging, get_logger


@pytest.fixture(autouse=True)
def _reset_tools_logger():
    """Reset the 'tools' parent logger between tests so each starts clean."""
    tools_logger = logging.getLogger("tools")
    saved_level = tools_logger.level
    saved_handlers = tools_logger.handlers[:]
    saved_propagate = tools_logger.propagate
    yield
    tools_logger.handlers.clear()
    tools_logger.handlers.extend(saved_handlers)
    tools_logger.setLevel(saved_level)
    tools_logger.propagate = saved_propagate


def test_setup_logging_default_is_info():
    """Default setup_logging() leaves the 'tools' logger at INFO."""
    setup_logging()
    assert logging.getLogger("tools").level == logging.INFO


def test_setup_logging_verbose_is_debug():
    """verbose=True drops the 'tools' logger to DEBUG."""
    setup_logging(verbose=True)
    assert logging.getLogger("tools").level == logging.DEBUG


def test_setup_logging_quiet_is_error():
    """quiet=True raises the 'tools' logger to ERROR."""
    setup_logging(quiet=True)
    assert logging.getLogger("tools").level == logging.ERROR


def test_setup_logging_verbose_and_quiet_rejected():
    """verbose=True and quiet=True together must raise ValueError."""
    with pytest.raises(ValueError):
        setup_logging(verbose=True, quiet=True)


def test_setup_logging_replaces_handlers_on_repeat_call():
    """Repeat calls clear prior handlers (no duplicate stderr output in tests)."""
    setup_logging()
    first_count = len(logging.getLogger("tools").handlers)
    setup_logging()
    setup_logging()
    second_count = len(logging.getLogger("tools").handlers)
    assert first_count == second_count == 1


def test_get_logger_returns_child_of_tools():
    """get_logger('tools.x.y') is a descendant of the 'tools' parent."""
    child = get_logger("tools.foo.bar")
    assert child.name == "tools.foo.bar"
    # Walk parent chain — must hit the 'tools' logger
    seen = []
    cur = child
    while cur is not None and cur.name != "root":
        seen.append(cur.name)
        cur = cur.parent
    assert "tools" in seen


def test_child_logger_inherits_level_after_setup():
    """A child logger emits at the parent's effective level after setup_logging()."""
    setup_logging(verbose=True)
    child = get_logger("tools.test_child")
    assert child.isEnabledFor(logging.DEBUG)

    setup_logging(quiet=True)
    assert not child.isEnabledFor(logging.INFO)
    assert child.isEnabledFor(logging.ERROR)
