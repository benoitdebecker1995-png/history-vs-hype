"""Tests for the INDEX.md / help.md generator."""
import pytest

from tools import docs_index as di


@pytest.fixture
def docs(tmp_path, monkeypatch):
    ref = tmp_path / "REFERENCE"
    cmd = tmp_path / "commands"
    ref.mkdir()
    cmd.mkdir()
    monkeypatch.setattr(di, "REFERENCE_DIR", ref)
    monkeypatch.setattr(di, "COMMANDS_DIR", cmd)
    monkeypatch.setattr(di, "INDEX_PATH", ref / "INDEX.md")
    monkeypatch.setattr(di, "HELP_PATH", cmd / "help.md")
    return ref, cmd


def test_frontmatter_stays_at_the_top_of_the_file(docs):
    """Regression: the first version wrote the AUTO fence above the frontmatter.
    YAML frontmatter is only frontmatter when it is the very first thing in the
    file, so /help's description became the HTML comment."""
    _, cmd = docs
    (cmd / "help.md").write_text(
        "---\ndescription: Command menu\nmodel: haiku\n---\n\n# Help\n\nProse.\n",
        encoding="utf-8")
    (cmd / "build.md").write_text("---\ndescription: Build it\n---\n# Build\n", encoding="utf-8")

    di._apply(di.HELP_PATH, di.HELP_ZONE, di.build_help_body(), write=True)
    text = (cmd / "help.md").read_text(encoding="utf-8")

    assert text.startswith("---\ndescription: Command menu\n")
    assert "<!-- AUTO:command-list" in text
    assert text.index("model: haiku") < text.index("<!-- AUTO:command-list")
    assert "Prose." in text                      # hand-written body survives


def test_file_without_frontmatter_is_untouched_at_top(docs):
    ref, _ = docs
    (ref / "INDEX.md").write_text("# REFERENCE Index\n\nCurated prose.\n", encoding="utf-8")
    (ref / "VOICE-PROFILE.md").write_text("# Voice\n\nThe voice doc.\n", encoding="utf-8")

    di._apply(di.INDEX_PATH, di.INDEX_ZONE, di.build_index_body(), write=True)
    text = (ref / "INDEX.md").read_text(encoding="utf-8")

    assert text.startswith("<!-- AUTO:reference-index")
    assert "Curated prose." in text


def test_regeneration_is_idempotent(docs):
    ref, _ = docs
    (ref / "A.md").write_text("# A\n\nAlpha doc.\n", encoding="utf-8")
    (ref / "INDEX.md").write_text("# Index\n", encoding="utf-8")

    assert di._apply(di.INDEX_PATH, di.INDEX_ZONE, di.build_index_body(), write=True) is True
    assert di._apply(di.INDEX_PATH, di.INDEX_ZONE, di.build_index_body(), write=True) is False


def test_index_lists_every_reference_doc(docs):
    ref, _ = docs
    for name in ("A.md", "B.md", "VOICE-PROFILE.md"):
        (ref / name).write_text(f"# {name}\n\nSummary line.\n", encoding="utf-8")
    (ref / "INDEX.md").write_text("# Index\n", encoding="utf-8")

    body = di.build_index_body()

    assert "(A.md)" in body and "(B.md)" in body and "(VOICE-PROFILE.md)" in body
    assert "(INDEX.md)" not in body          # the index does not index itself


def test_summary_prefers_frontmatter_description(docs):
    ref, _ = docs
    (ref / "X.md").write_text(
        "---\ndescription: The real summary\n---\n# X\n\nSome other line.\n", encoding="utf-8")

    assert di._summary(ref / "X.md") == "The real summary"


def test_drift_reports_unmentioned_commands(docs):
    _, cmd = docs
    (cmd / "help.md").write_text("# Help\n\nUse `/build` for things.\n", encoding="utf-8")
    (cmd / "build.md").write_text("# Build\n", encoding="utf-8")
    (cmd / "deploy.md").write_text("# Deploy\n", encoding="utf-8")

    ghosts, unmentioned = di.command_drift()

    assert ghosts == []
    assert unmentioned == ["deploy"]


def test_drift_ignores_the_deprecation_redirect_table(docs):
    """The consolidation list names retired commands on purpose. Scanning it
    reported 9 false ghosts on the first run."""
    _, cmd = docs
    (cmd / "help.md").write_text(
        "# Help\n\nUse `/build`.\n\n"
        "**2026-05-03 consolidation:** Down from 28 commands.\n"
        "- `/sources` -> `/research --sources`\n"
        "- `/intel` -> `/patterns --intel`\n",
        encoding="utf-8")
    (cmd / "build.md").write_text("# Build\n", encoding="utf-8")

    ghosts, _ = di.command_drift()

    assert ghosts == []          # /sources and /intel are history, not claims


def test_drift_still_catches_a_live_command_called_archived(docs):
    _, cmd = docs
    (cmd / "help.md").write_text("# Help\n\nUse `/build` and `/ghost`.\n", encoding="utf-8")
    (cmd / "build.md").write_text("# Build\n", encoding="utf-8")

    ghosts, _ = di.command_drift()

    assert ghosts == ["ghost"]
