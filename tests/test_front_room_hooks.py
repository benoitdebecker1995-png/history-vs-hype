from tools.hooks.session_context import render_context
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
