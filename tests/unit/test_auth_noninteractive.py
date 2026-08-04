"""Pins for the YouTube OAuth headless guard and the loopback port.

Origin: 2026-08-04. `HvH-GrowthRefresh` failed at its 07:45 scheduled run on 2026-08-03 with
`[WinError 10048] Only one usage of each socket address ... is normally permitted`, then succeeded
when the morning-catchup chain re-ran it at 10:31. Two defects behind that:

1. `run_local_server(port=8080)` pinned one loopback port, so a re-auth attempt collided with
   whatever already held 8080 — here HvH-CtrTracker (07:30, terminated at its PT20M limit).
   The OAuth client is an `installed`/Desktop type, for which Google accepts any loopback port,
   so the fixed port bought nothing.
2. A scheduled run with a dead token tried to open a browser nobody could answer — it can only
   hang until the task's execution-time limit kills it. The claude-CLI routines already fail fast
   with an actionable code (78) for exactly this; the YouTube path did not.

No network: every test drives the pure helpers or monkeypatches the flow.
"""

import os

import pytest

from tools.youtube_analytics import auth


class TestLoopbackPort:
    def test_port_is_ephemeral(self):
        """0 = let the OS pick. A fixed port is what collided."""
        assert auth.OAUTH_LOOPBACK_PORT == 0

    def test_client_is_an_installed_app(self):
        """Any-port loopback is only valid for the `installed` client type."""
        import json

        if not auth.CLIENT_SECRET_PATH.exists():
            pytest.skip("client_secret.json not present in this checkout")
        secret = json.loads(auth.CLIENT_SECRET_PATH.read_text(encoding="utf-8"))
        assert "installed" in secret, (
            "port=0 is only safe for a Desktop/installed client; a web client needs its exact "
            "registered redirect URI"
        )


class TestNoninteractiveDetection:
    @pytest.fixture(autouse=True)
    def _clear_env(self, monkeypatch):
        monkeypatch.delenv(auth.NONINTERACTIVE_ENV_VAR, raising=False)

    @pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", " yes "])
    def test_env_var_forces_noninteractive(self, monkeypatch, value):
        monkeypatch.setenv(auth.NONINTERACTIVE_ENV_VAR, value)
        assert auth._is_noninteractive() is True

    @pytest.mark.parametrize("value", ["0", "false", "no", "NO"])
    def test_env_var_forces_interactive(self, monkeypatch, value):
        """`--login` sets this; the tty inference must not veto an explicit request."""
        monkeypatch.setenv(auth.NONINTERACTIVE_ENV_VAR, value)
        assert auth._is_noninteractive() is False

    def test_no_tty_on_either_stream_is_noninteractive(self, monkeypatch):
        monkeypatch.setattr(auth.sys, "stdin", _FakeStream(False))
        monkeypatch.setattr(auth.sys, "stdout", _FakeStream(False))
        assert auth._is_noninteractive() is True

    def test_terminal_stdin_stays_interactive_when_output_is_redirected(self, monkeypatch):
        """`python -m ... > out.txt` from a real shell must still be able to re-auth."""
        monkeypatch.setattr(auth.sys, "stdin", _FakeStream(True))
        monkeypatch.setattr(auth.sys, "stdout", _FakeStream(False))
        assert auth._is_noninteractive() is False

    def test_detached_streams_are_noninteractive(self, monkeypatch):
        monkeypatch.setattr(auth.sys, "stdin", None)
        monkeypatch.setattr(auth.sys, "stdout", None)
        assert auth._is_noninteractive() is True


class TestGuardBehaviour:
    def test_headless_reauth_raises_instead_of_opening_a_browser(self, monkeypatch, tmp_path):
        """The failure that used to hang until the task limit killed it."""
        monkeypatch.setenv(auth.NONINTERACTIVE_ENV_VAR, "1")
        monkeypatch.setattr(auth, "TOKEN_PATH", tmp_path / "token.json")  # absent => needs consent

        def _explode(*_args, **_kwargs):
            raise AssertionError("run_local_server must not be reached in a headless run")

        monkeypatch.setattr(auth.InstalledAppFlow, "from_client_secrets_file", _explode)

        if not auth.CLIENT_SECRET_PATH.exists():
            pytest.skip("client_secret.json not present in this checkout")

        with pytest.raises(auth.InteractiveAuthRequired) as excinfo:
            auth.get_credentials()

        message = str(excinfo.value)
        assert "--login" in message, "the message must name the command that fixes it"
        assert "NOT run" in message

    def test_message_names_a_real_entry_point(self):
        """The old failure mode was advice pointing at something that does not exist."""
        assert callable(auth.main)

    def test_cli_reports_the_actionable_code(self, monkeypatch, capsys):
        def _needs_consent():
            raise auth.InteractiveAuthRequired("needs consent --login")

        monkeypatch.setattr(auth, "get_credentials", _needs_consent)
        assert auth.main([]) == 78
        assert "--login" in capsys.readouterr().out

    def test_login_flag_overrides_the_headless_inference(self, monkeypatch):
        monkeypatch.setenv(auth.NONINTERACTIVE_ENV_VAR, "1")
        seen = {}

        def _fake_creds():
            seen["noninteractive"] = auth._is_noninteractive()

            class _Creds:
                expiry = "2026-12-31"

            return _Creds()

        monkeypatch.setattr(auth, "get_credentials", _fake_creds)
        assert auth.main(["--login"]) == 0
        assert seen["noninteractive"] is False
        # don't leak the override into the rest of the session
        os.environ.pop(auth.NONINTERACTIVE_ENV_VAR, None)


class _FakeStream:
    def __init__(self, is_tty: bool):
        self._is_tty = is_tty

    def isatty(self) -> bool:
        return self._is_tty
