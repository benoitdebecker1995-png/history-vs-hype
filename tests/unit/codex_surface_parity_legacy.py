"""Drift guard for the hand-maintained Codex port of the Claude Code surface.

`.claude/` is canonical. `.agents/skills/` + `.codex/` are the Codex mirror, ported by hand, so
nothing keeps them in step automatically. This suite is the alarm: it reports drift, it never
authors content.

Origin: 2026-08-04. An earlier mirror (2026-07-22) went stale unnoticed — 12 files still named
`D:\\History vs Hype`, a drive that no longer held the repo, and four commands were never mirrored
at all. Every assertion below corresponds to something that had actually rotted.
"""

import json
import tomllib
from pathlib import Path

import pytest
import yaml

# gpt-5.6's reasoning ladder (models_cache.json). `sol` defaults to "low", so every agent pins
# its own effort — an unpinned heavyweight agent silently runs shallow.
REASONING_LEVELS = {"low", "medium", "high", "xhigh", "max", "ultra"}

REPO_ROOT = Path(__file__).resolve().parents[2]
CLAUDE = REPO_ROOT / ".claude"
AGENT_SKILLS = REPO_ROOT / ".agents" / "skills"
CODEX = REPO_ROOT / ".codex"

DEAD_ROOT = "D:\\History vs Hype"


def _commands():
    return sorted(p.stem for p in (CLAUDE / "commands").glob("*.md"))


def _project_skills():
    return sorted(p.name for p in (CLAUDE / "skills").iterdir() if p.is_dir())


def _agents():
    return sorted(
        p.stem
        for p in (CLAUDE / "agents").glob("*.md")
        if not p.name.endswith(".contract.md") and "CHANGELOG" not in p.name
    )


class TestCommandsHaveSkills:
    @pytest.mark.parametrize("cmd", _commands())
    def test_every_command_has_a_codex_skill(self, cmd):
        assert (AGENT_SKILLS / f"source-command-{cmd}" / "SKILL.md").is_file(), (
            f"/{cmd} has no Codex skill — run the port for .agents/skills/source-command-{cmd}/"
        )

    @pytest.mark.parametrize("cmd", _commands())
    def test_description_is_trigger_shaped(self, cmd):
        """Codex fires skills implicitly off the description. A label never fires."""
        text = (AGENT_SKILLS / f"source-command-{cmd}" / "SKILL.md").read_text(encoding="utf-8")
        head = text.split("---")[1] if text.startswith("---") else ""
        assert "description:" in head, f"source-command-{cmd} has no description"
        assert "Use when:" in head, (
            f"source-command-{cmd} description is a label, not a trigger — add 'Use when: ...'"
        )

    def test_no_orphan_command_skills(self):
        ported = {
            p.name[len("source-command-"):]
            for p in AGENT_SKILLS.glob("source-command-*")
            if p.is_dir()
        }
        assert ported - set(_commands()) == set(), "Codex skill for a command that no longer exists"


class TestFrontmatterIsValidYaml:
    """A skill whose frontmatter doesn't parse doesn't load.

    Claude Code's frontmatter reader is lenient; a strict YAML parser is not. All 11 project
    skills and 2 agents shipped `description: ... Use when: ...` unquoted — a mapping-value
    error — which would have made them dead weight on Codex.
    """

    @staticmethod
    def _frontmatter(path: Path):
        text = path.read_text(encoding="utf-8", errors="replace")
        assert text.startswith("---"), f"{path} has no frontmatter"
        return yaml.safe_load(text.split("---", 2)[1])

    @pytest.mark.parametrize(
        "path",
        sorted(AGENT_SKILLS.glob("*/SKILL.md")),
        ids=lambda p: p.parent.name,
    )
    def test_codex_skill_frontmatter_parses(self, path):
        meta = self._frontmatter(path)
        assert meta.get("name") and meta.get("description")
        assert meta["name"] == path.parent.name, "Codex identifies a skill by its `name` field"

    @pytest.mark.parametrize(
        "path",
        sorted(CLAUDE.glob("skills/*/SKILL.md")) + sorted(CLAUDE.glob("commands/*.md")),
        ids=lambda p: p.parent.name if p.name == "SKILL.md" else p.stem,
    )
    def test_canonical_frontmatter_parses(self, path):
        assert self._frontmatter(path).get("description")

    @pytest.mark.parametrize("name", _agents())
    def test_agent_frontmatter_parses(self, name):
        assert self._frontmatter(CLAUDE / "agents" / f"{name}.md").get("description")


class TestProjectSkillsMirrored:
    @pytest.mark.parametrize("name", _project_skills())
    def test_every_project_skill_is_mirrored(self, name):
        src = CLAUDE / "skills" / name
        if not (src / "SKILL.md").is_file():  # e.g. the README index
            pytest.skip(f"{name} is not a skill folder")
        assert (AGENT_SKILLS / name / "SKILL.md").is_file(), f"{name} missing from .agents/skills"

    @pytest.mark.parametrize("name", _project_skills())
    def test_mirror_matches_canonical(self, name):
        src = CLAUDE / "skills" / name / "SKILL.md"
        dst = AGENT_SKILLS / name / "SKILL.md"
        if not src.is_file():
            pytest.skip(f"{name} is not a skill folder")
        assert dst.read_text(encoding="utf-8") == src.read_text(encoding="utf-8"), (
            f"{name}/SKILL.md has drifted from .claude/skills — re-copy it"
        )


class TestAgentsPorted:
    @pytest.mark.parametrize("name", _agents())
    def test_every_agent_has_a_toml(self, name):
        assert (CODEX / "agents" / f"{name}.toml").is_file(), f"{name} has no .codex/agents TOML"

    @pytest.mark.parametrize("name", _agents())
    def test_toml_parses_with_required_fields(self, name):
        data = tomllib.loads((CODEX / "agents" / f"{name}.toml").read_text(encoding="utf-8"))
        for field in ("name", "description", "developer_instructions"):
            assert data.get(field), f"{name}.toml is missing required field `{field}`"
        assert data["model"].startswith("gpt-5.6-"), f"{name}.toml pins a non-5.6 model"
        effort = data.get("model_reasoning_effort")
        assert effort in REASONING_LEVELS, (
            f"{name}.toml effort {effort!r} is not a gpt-5.6 level — sol defaults to 'low', so an "
            f"unpinned or misspelled effort makes this agent run shallow"
        )

    @pytest.mark.parametrize("name", _agents())
    def test_instructions_carry_the_current_body(self, name):
        """The TOML embeds the agent body verbatim; a `.claude` edit must be re-ported."""
        src = (CLAUDE / "agents" / f"{name}.md").read_text(encoding="utf-8")
        body = src.split("---", 2)[2].strip() if src.startswith("---") else src.strip()
        data = tomllib.loads((CODEX / "agents" / f"{name}.toml").read_text(encoding="utf-8"))
        assert body in data["developer_instructions"], (
            f"{name}.toml has drifted from .claude/agents/{name}.md — re-port it"
        )


class TestRulesPorted:
    """Three rules are glob-scoped and become skills; python-tools becomes nested AGENTS.md."""

    @pytest.mark.parametrize("rule", ["script-writing", "packaging", "research-verification"])
    def test_glob_scoped_rule_has_a_skill(self, rule):
        assert (AGENT_SKILLS / f"rule-{rule}" / "SKILL.md").is_file()

    @pytest.mark.parametrize("directory", ["tools", "tests"])
    def test_directory_scoped_rule_has_nested_agents_md(self, directory):
        assert (REPO_ROOT / directory / "AGENTS.md").is_file()

    def test_root_agents_md_exists(self):
        assert (REPO_ROOT / "AGENTS.md").is_file()

    def test_every_rule_is_accounted_for(self):
        rules = {p.stem for p in (CLAUDE / "rules").glob("*.md")}
        handled = {"script-writing", "packaging", "research-verification", "python-tools"}
        assert rules <= handled, f"unported rule(s): {sorted(rules - handled)}"


class TestCodexConfig:
    def test_config_parses(self):
        tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))

    def test_mcp_servers_match_mcp_json(self):
        declared = tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))["mcp_servers"]
        canonical = json.loads((REPO_ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
        assert set(canonical) <= set(declared), (
            f"missing from .codex/config.toml: {sorted(set(canonical) - set(declared))}"
        )

    def test_mcp_paths_are_absolute_and_present(self):
        """Codex does not interpolate ${APPDATA}; a stale absolute path is a silent dead server."""
        servers = tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))["mcp_servers"]
        for name, spec in servers.items():
            command = spec.get("command")
            if not command or "\\" not in command:  # url-based or bare-name (npx) servers
                continue
            assert Path(command).is_file(), f"{name}: {command} does not exist"

    def test_graph_paths_point_at_this_repo(self):
        servers = tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))["mcp_servers"]
        for name in ("graphify-code", "graphify-research"):
            arg = servers[name]["args"][0]
            assert Path(arg).is_relative_to(REPO_ROOT), f"{name} points outside this repo: {arg}"


class TestCodexHooks:
    def _hooks(self):
        return json.loads((CODEX / "hooks.json").read_text(encoding="utf-8"))["hooks"]

    def test_same_events_as_claude(self):
        claude = json.loads((CLAUDE / "settings.json").read_text(encoding="utf-8"))["hooks"]
        assert set(claude) <= set(self._hooks()), (
            f"events not ported: {sorted(set(claude) - set(self._hooks()))}"
        )

    def test_pretooluse_matches_apply_patch_not_claude_tool_names(self):
        """Codex routes every file edit through apply_patch; Edit|Write|NotebookEdit never fires."""
        matcher = self._hooks()["PreToolUse"][0]["matcher"]
        assert "apply_patch" in matcher, f"PreToolUse matcher {matcher!r} will not fire on Codex"

    def test_hook_scripts_exist(self):
        for event, groups in self._hooks().items():
            for group in groups:
                for handler in group["hooks"]:
                    command = handler["commandWindows"]
                    script = command.split('"')[1]
                    assert Path(script).is_file(), f"{event}: hook script missing at {script}"

    def test_pinned_windows_root_is_this_repo(self):
        """The absolute pin is deliberate (no $CLAUDE_PROJECT_DIR on Codex) — this catches a move."""
        for groups in self._hooks().values():
            for group in groups:
                for handler in group["hooks"]:
                    script = Path(handler["commandWindows"].split('"')[1])
                    assert script.is_relative_to(REPO_ROOT), (
                        f"hooks.json pins {script}, but the repo is at {REPO_ROOT}"
                    )


def _ported_files():
    roots = [REPO_ROOT / ".agents", CODEX]
    return [p for root in roots for p in root.rglob("*") if p.is_file() and p.suffix in {".md", ".toml", ".json"}]


class TestNoStalePaths:
    def test_no_dead_drive_root_anywhere_in_the_port(self):
        stale = [
            str(p.relative_to(REPO_ROOT))
            for p in _ported_files()
            if DEAD_ROOT in p.read_text(encoding="utf-8", errors="ignore")
        ]
        assert stale == [], f"files still naming the dead {DEAD_ROOT} root: {stale}"
