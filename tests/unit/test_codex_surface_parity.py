"""Pins the migration retrieval boundary for the minimum Codex front room."""

import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_legacy_skills_are_outside_codex_discovery_path():
    assert not (ROOT / ".agents" / "skills").exists()
    assert (ROOT / ".agents" / "cold-skills").is_dir()


def test_legacy_agents_are_outside_codex_discovery_path():
    assert not (ROOT / ".codex" / "agents").exists()
    assert (ROOT / ".codex" / "cold-agents").is_dir()


def test_nested_legacy_agents_files_no_longer_apply():
    assert not (ROOT / "tools" / "AGENTS.md").exists()
    assert not (ROOT / "tests" / "AGENTS.md").exists()
    assert (ROOT / "tools" / "AGENTS.legacy.md").is_file()
    assert (ROOT / "tests" / "AGENTS.legacy.md").is_file()


def test_active_instruction_surface_names_hot_memory():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "ACTIVE_PROJECT" in text
    assert all(name in text for name in ("PROJECT.md", "RESEARCH.md", "SCRIPT.md"))
    assert "source-command-" not in text


def test_codex_config_and_hooks_parse():
    tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
    hooks = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    assert {"SessionStart", "UserPromptSubmit", "PreToolUse"} <= set(hooks["hooks"])


def test_active_pointer_resolves_to_real_project():
    relative = (ROOT / "ACTIVE_PROJECT").read_text(encoding="utf-8").strip()
    project = ROOT / relative
    assert project.is_dir()
    assert all((project / name).is_file() for name in ("PROJECT.md", "RESEARCH.md", "SCRIPT.md"))

