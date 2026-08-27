"""Unit tests for tools.logging_config.

Covers the E1 audit contract: setup_logging() must produce INFO by default,
DEBUG when verbose=True, ERROR when quiet=True, and reject the
mutually-exclusive verbose+quiet combo.

Also covers the console-encoding contract added 2026-08-02: a tools CLI must be
able to print its report under a narrow console codepage (cp1252 on Windows)
instead of dying with UnicodeEncodeError.
"""
import codecs
import io
import logging
import sys

import pytest

from tools.logging_config import (
    configure_console_output,
    get_logger,
    safe_print,
    setup_logging,
)

# U+26D4 NO ENTRY / U+2B50 STAR / U+2705 CHECK MARK BUTTON — used by convention
# throughout the repo's research files. None of them exists in cp1252.
NON_CP1252 = "⛔ ⭐ ✅"


def _cp1252_stdout():
    """A strict cp1252 text stream over a byte buffer — stands in for a piped
    Windows stdout, where Python falls back to the ANSI codepage."""
    buf = io.BytesIO()
    return buf, io.TextIOWrapper(buf, encoding="cp1252", errors="strict", write_through=True)


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


class TestConsoleEncoding:
    """A report must never be able to kill the check that produced it.

    Regression: `claim_status --frontier` crashed with UnicodeEncodeError on a
    cp1252 stdout because it echoes claim lines containing ⛔. The tool's exit code
    is the /research completion gate, so the crash's exit 1 was indistinguishable
    from a genuine "research is not finished" verdict.
    """

    def test_strict_stream_raises_without_the_fix(self):
        """Pins the underlying platform behaviour this module exists to absorb."""
        _, out = _cp1252_stdout()
        with pytest.raises(UnicodeEncodeError):
            print(NON_CP1252, file=out)

    def test_configure_console_output_makes_a_strict_stream_lenient(self):
        buf, out = _cp1252_stdout()
        assert configure_console_output(out) is True
        print(NON_CP1252, file=out)  # must not raise
        out.flush()
        assert buf.getvalue().decode("cp1252").strip() == "? ? ?"

    def test_configure_console_output_keeps_the_streams_encoding(self):
        """Left at cp1252 on purpose: re-encoding to UTF-8 for a cp1252 consumer
        trades a crash for mojibake. Replacement chars stay readable."""
        _, out = _cp1252_stdout()
        configure_console_output(out)
        assert out.encoding.lower().replace("-", "") == "cp1252"
        assert out.errors == "replace"

    def test_configure_console_output_reports_streams_it_cannot_fix(self):
        """A codecs.getwriter() wrapper has no .reconfigure() — say so, don't raise."""
        writer = codecs.getwriter("cp1252")(io.BytesIO(), "strict")
        assert configure_console_output(writer) is False

    def test_configure_console_output_tolerates_a_closed_stream(self):
        _, out = _cp1252_stdout()
        out.close()
        assert configure_console_output(out) is False

    def test_setup_logging_hardens_stdout_and_stderr(self, monkeypatch):
        """The one-line fix for every tools CLI: they all call setup_logging()."""
        _, out = _cp1252_stdout()
        _, err = _cp1252_stdout()
        monkeypatch.setattr(sys, "stdout", out)
        monkeypatch.setattr(sys, "stderr", err)
        setup_logging()
        assert out.errors == "replace"
        assert err.errors == "replace"

    def test_safe_print_degrades_on_a_stream_that_cannot_be_reconfigured(self):
        """Second layer: safe_print still prints where configure_console_output can't help."""
        buf = io.BytesIO()
        writer = codecs.getwriter("cp1252")(buf, "strict")
        assert configure_console_output(writer) is False
        safe_print(f"VERDICT: OPEN {NON_CP1252}", stream=writer)  # must not raise
        assert "VERDICT: OPEN" in buf.getvalue().decode("cp1252")

    def test_safe_print_writes_encodable_text_verbatim(self):
        buf, out = _cp1252_stdout()
        safe_print("café — VERDICT: COMPLETE", stream=out)
        out.flush()
        assert buf.getvalue().decode("cp1252").strip() == "café — VERDICT: COMPLETE"

    def test_safe_print_defaults_to_stdout(self, monkeypatch):
        buf, out = _cp1252_stdout()
        monkeypatch.setattr(sys, "stdout", out)
        safe_print(NON_CP1252)
        out.flush()
        assert buf.getvalue().decode("cp1252").strip() == "? ? ?"

    def test_safe_print_swallows_a_dead_stream(self):
        """Losing the report is survivable; taking down the caller's verdict is not."""
        _, out = _cp1252_stdout()
        out.close()
        safe_print("anything", stream=out)  # must not raise
