"""Behavioral pins for the secret-guard pre-commit hook (tools/hooks/pre-commit).

Runs the *tracked* hook the way git runs it — installed into a throwaway repo's
.git/hooks/ and triggered by a real `git commit`, so the test exercises git's
own bundled `sh` (no dependency on `sh` being on the Windows PATH).

Origin: 2026-07-23 audit found the hook had ZERO tests, only caught private-key
blocks (a live Google API key had sat in a tracked file since the first commit),
and split staged filenames on spaces. These pins lock the hardened behavior.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKED_HOOK = REPO_ROOT / "tools" / "hooks" / "pre-commit"

# Structurally-valid-shaped but fake credentials (not real secrets).
GOOGLE_KEY = "AIza" + "Sy" + "A" * 33          # AIza + 35 chars
GITHUB_PAT = "ghp_" + "b" * 36
SLACK_TOKEN = "xoxb-" + "1" * 12 + "-" + "2" * 12 + "-" + "c" * 24
STRIPE_KEY = "sk_live_" + "d" * 30
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None, reason="git is required to exercise the hook"
)


def _run(args, cwd):
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def _make_repo(tmp_path):
    """Fresh git repo with the tracked secret-guard hook installed."""
    repo = tmp_path
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "t@example.com"], repo)
    _run(["git", "config", "user.name", "Test"], repo)
    _run(["git", "config", "commit.gpgsign", "false"], repo)
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    dst = hooks_dir / "pre-commit"
    dst.write_text(TRACKED_HOOK.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    dst.chmod(0o755)
    return repo


def _commit_attempt(repo, rel_path, content):
    """Stage a file and attempt a commit; return the CompletedProcess."""
    target = repo / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    _run(["git", "add", "-A"], repo)
    return _run(["git", "commit", "-m", "test"], repo)


def _blocked(result):
    combined = (result.stdout or "") + (result.stderr or "")
    return result.returncode != 0 and "secret-guard" in combined


# --- Content-scan: credential tokens in added lines must block ---------------

@pytest.mark.parametrize(
    "secret",
    [GOOGLE_KEY, GITHUB_PAT, SLACK_TOKEN, STRIPE_KEY, PRIVATE_KEY],
    ids=["google", "github", "slack", "stripe", "privatekey"],
)
def test_token_in_content_is_blocked(tmp_path, secret):
    repo = _make_repo(tmp_path)
    result = _commit_attempt(repo, "notes.md", f"config value: {secret}\n")
    assert _blocked(result), f"expected block, got rc={result.returncode}\n{result.stdout}{result.stderr}"


def test_token_in_path_with_spaces_is_blocked(tmp_path):
    """The old `for f in $STAGED` split paths on spaces, letting a secret in a
    space-containing directory slip past the content scan."""
    repo = _make_repo(tmp_path)
    result = _commit_attempt(repo, "sub dir/config.md", f"key = {GOOGLE_KEY}\n")
    assert _blocked(result)


# --- Filename-scan: credential filenames must block --------------------------

def test_credential_filename_is_blocked(tmp_path):
    repo = _make_repo(tmp_path)
    result = _commit_attempt(repo, "token.json", '{"access_token": "x"}\n')
    assert _blocked(result)


def test_credential_filename_with_spaces_is_blocked(tmp_path):
    repo = _make_repo(tmp_path)
    result = _commit_attempt(repo, "prod secrets.json", '{"a": 1}\n')
    assert _blocked(result)


# --- Negatives: ordinary content must pass (no false positives) --------------

def test_ordinary_content_passes(tmp_path):
    repo = _make_repo(tmp_path)
    # A 40-char git SHA and normal prose must NOT trip the token patterns.
    content = "commit deadbeefcafe0123456789abcdef0123456789 fixes the parser.\n"
    result = _commit_attempt(repo, "README.md", content)
    assert result.returncode == 0, f"false positive:\n{result.stdout}{result.stderr}"
