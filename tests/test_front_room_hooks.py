from tools.front_room import ActiveProjectError
from tools.hooks.session_context import render_context, render_degraded
from tools.hooks.utterance_triggers import check


def test_session_context_contains_project_but_no_command_menu(tmp_path):
    project = tmp_path / "video-projects" / "_IN_PRODUCTION" / "67-donation"
    project.mkdir(parents=True)
    (tmp_path / "ACTIVE_PROJECT").write_text(
        "video-projects/_IN_PRODUCTION/67-donation", encoding="utf-8"
    )
    (tmp_path / "CHANNEL.md").write_text(
        "# Channel\n\nTalk normally and keep channel strategy separate.", encoding="utf-8"
    )
    for name, text in {
        "PROJECT.md": "# Project\n\nNext unresolved problem: creator bridge.",
        "RESEARCH.md": "# Research",
        "SCRIPT.md": "# Script",
    }.items():
        (project / name).write_text(text, encoding="utf-8")
    rendered = render_context(tmp_path)
    assert "Talk normally" in rendered
    assert "Next unresolved problem" in rendered
    assert "/status" not in rendered
    assert "command menu" not in rendered.casefold()


def test_package_choice_is_captured_without_user_command_language():
    reminders = check("Let's use this title. It is final.")
    assert any("record" in reminder.casefold() for reminder in reminders)
    assert all("command" not in reminder.casefold() for reminder in reminders)


def test_material_recommendation_acceptance_prompts_prediction_record():
    reminders = check("Let's do that strategy. I accept the recommendation.")
    assert any("predicted mechanism" in reminder.casefold() for reminder in reminders)


def test_degraded_session_still_carries_channel_state(tmp_path):
    """A broken ACTIVE_PROJECT must not also cost the session its channel state.

    Regression guard for the 2026-08-27 finding: render_context() raises before it
    returns anything, so the old bare "Front room unavailable" line left the session
    with no CHANNEL.md, no freshness dates, and CLAUDE.md forbidding a .claude/
    fallback. 13 of 15 _IN_PRODUCTION folders are one ACTIVE_PROJECT edit away from
    triggering this.
    """
    broken = tmp_path / "video-projects" / "_IN_PRODUCTION" / "55-falklands"
    broken.mkdir(parents=True)
    (broken / "PROJECT.md").write_text("# Project", encoding="utf-8")  # RESEARCH/SCRIPT absent

    healthy = tmp_path / "video-projects" / "_IN_PRODUCTION" / "62-volhynia"
    healthy.mkdir(parents=True)
    for name in ("PROJECT.md", "RESEARCH.md", "SCRIPT.md"):
        (healthy / name).write_text(f"# {name}", encoding="utf-8")

    (tmp_path / "ACTIVE_PROJECT").write_text(
        "video-projects/_IN_PRODUCTION/55-falklands", encoding="utf-8"
    )
    (tmp_path / "CHANNEL.md").write_text(
        "# Channel\n\nReach roughly EUR 2,000 per month.", encoding="utf-8"
    )

    rendered = render_degraded(ActiveProjectError("missing RESEARCH.md"), tmp_path)

    # It says something is wrong, and what.
    assert "DEGRADED" in rendered
    assert "55-falklands" in rendered
    assert "RESEARCH.md" in rendered
    assert "SCRIPT.md" in rendered

    # It names a folder that would actually work.
    assert "62-volhynia" in rendered

    # And the channel state survives regardless.
    assert "EUR 2,000" in rendered


def test_degraded_says_so_when_channel_state_is_gone_too(tmp_path):
    (tmp_path / "ACTIVE_PROJECT").write_text("video-projects/_IN_PRODUCTION/nope", encoding="utf-8")
    rendered = render_degraded(ActiveProjectError("no such project"), tmp_path)
    assert "CHANNEL.md is ALSO missing" in rendered
