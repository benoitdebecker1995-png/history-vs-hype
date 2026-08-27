from pathlib import Path

from tools.front_room import select_voice_examples
from tools.voice_lint import lint_file, mask_comments, scan_patterns


def _active_tree(tmp_path: Path) -> None:
    project = tmp_path / "video-projects" / "_IN_PRODUCTION" / "current"
    project.mkdir(parents=True)
    (tmp_path / "ACTIVE_PROJECT").write_text(
        "video-projects/_IN_PRODUCTION/current", encoding="utf-8"
    )
    (tmp_path / "CHANNEL.md").write_text("# Channel\n", encoding="utf-8")
    for name in ("PROJECT.md", "RESEARCH.md", "SCRIPT.md"):
        (project / name).write_text(f"# {name}\n", encoding="utf-8")


def test_v3_documentary_anti_examples_are_flagged_at_stated_strength(tmp_path):
    script = tmp_path / "script.md"
    script.write_text(
        "That changes everything.\n"
        "Beneath the surface, the truth was more complicated.\n"
        "This wasn't merely a forgery; it was a new legal strategy.\n",
        encoding="utf-8",
    )
    findings = lint_file(str(script))
    by_rule = {finding.rule: finding.severity for finding in findings}
    assert by_rule["changed-everything"] == "HARD"
    assert by_rule["v3-beneath-surface"] == "WARN"
    assert by_rule["v3-truth-complicated"] == "WARN"
    assert by_rule["v3-not-merely-correction"] == "WARN"


def test_v3_functional_spoken_connectors_are_not_hard_banned():
    lines = mask_comments(
        [
            "Of course, that does not prove the claim.",
            "If you look at the document, it actually says something else.",
            "What we do have is a copy, so we can test the wording.",
        ]
    )
    assert not scan_patterns("test.md", lines)


def test_current_project_adlib_outranks_general_v3_corpus(tmp_path):
    _active_tree(tmp_path)
    project = tmp_path / "video-projects" / "_IN_PRODUCTION" / "current"
    adlib = project / "_adlib"
    adlib.mkdir()
    (adlib / "readthrough.md").write_text(
        "SPONTANEOUS: The document changes what this claim can prove.",
        encoding="utf-8",
    )
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    (model / "VOICE-EVIDENCE.md").write_text(
        "SPONTANEOUS [A1-001]: The document changes what the legal claim can prove.",
        encoding="utf-8",
    )
    results = select_voice_examples("document changes what claim can prove", root=tmp_path)
    assert results[0]["source"].endswith("readthrough.md")


def test_assistant_audit_locator_is_excluded_from_voice_evidence(tmp_path):
    _active_tree(tmp_path)
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    (model / "VOICE-EVIDENCE.md").write_text(
        "SPONTANEOUS [A2-105]: Requirements audit says normal conversation repository.\n\n"
        "SPONTANEOUS [A2-106]: I want normal conversation for the repository.\n",
        encoding="utf-8",
    )
    results = select_voice_examples("normal conversation repository", root=tmp_path)
    assert results
    assert {row.get("locator") for row in results} == {"A2-106"}
