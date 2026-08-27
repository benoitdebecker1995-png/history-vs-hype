"""SessionStart hook for the minimum conversational front room."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.front_room import ActiveProjectError, resolve_active_project
from tools.sqlite_access import connect_readonly

REPO_ROOT = Path(__file__).resolve().parents[2]


def _freshness(path: Path, query: str) -> str:
    try:
        connection = connect_readonly(path)
        try:
            value = connection.execute(query).fetchone()[0]
        finally:
            connection.close()
        return str(value or "no valid record")
    except Exception as exc:
        return f"unavailable ({type(exc).__name__})"


def render_context(root: Path = REPO_ROOT) -> str:
    active = resolve_active_project(root)
    channel_path = root / "CHANNEL.md"
    if not channel_path.is_file():
        raise ActiveProjectError(f"missing CHANNEL.md in {root}")
    channel = channel_path.read_text(encoding="utf-8", errors="replace").strip()
    snapshot = active.project.read_text(encoding="utf-8", errors="replace").strip()
    analytics = _freshness(
        root / "tools" / "youtube_analytics" / "analytics.db",
        "SELECT MAX(metrics_fetched_at) FROM videos",
    )
    ctr = _freshness(
        root / "tools" / "discovery" / "keywords.db",
        "SELECT MAX(snapshot_date) FROM ctr_snapshots WHERE COALESCE(is_valid, 1)=1",
    )
    intel = _freshness(
        root / "tools" / "intel" / "intel.db",
        "SELECT MAX(last_refresh) FROM kb_meta",
    )
    return (
        "History vs Hype channel state (hot context):\n"
        f"{channel}\n\nCurrent video project (separate hot context):\n"
        f"Path: {active.path}\n\n{snapshot}\n\n"
        "Data freshness (report these dates when relevant):\n"
        f"- channel analytics: {analytics}\n- CTR: {ctr}\n- market intelligence: {intel}\n"
        "Use the relevant creator-model section for decisions. Opportunity, packaging, business "
        "and performance claims require the matching front-room evidence packet; never substitute "
        "a composite score.\n"
        "Keep channel instructions separate from video state. Infer the creator's intent "
        "conversationally; all implementation machinery remains internal."
    )


HOT_FILES = ("PROJECT.md", "RESEARCH.md", "SCRIPT.md")


def render_degraded(exc: Exception, root: Path = REPO_ROOT) -> str:
    """What to print when the active project cannot be resolved.

    WHY THIS EXISTS (2026-08-27). The bare `Front room unavailable: ...` line was
    technically loud but practically useless: render_context() raises before it
    returns anything, so a broken project pointer also cost the session CHANNEL.md
    and every freshness date. The session then ran with no channel state at all,
    and CLAUDE.md forbids falling back to `.claude/`.

    13 of the 15 folders in _IN_PRODUCTION are missing at least one hot file, so
    this is one edit to ACTIVE_PROJECT away at any time. Channel state does not
    depend on the project resolving — emit it regardless, name exactly what is
    missing, and list the folders that would work.
    """
    lines = [f"Front room DEGRADED — the active project could not be resolved: {exc}", ""]

    pointer = root / "ACTIVE_PROJECT"
    try:
        target = pointer.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        target = ""

    if target:
        project_dir = root / target
        missing = [f for f in HOT_FILES if not (project_dir / f).is_file()]
        lines.append(f"ACTIVE_PROJECT points at: {target}")
        if missing:
            lines.append(f"Missing hot file(s): {', '.join(missing)}")
    else:
        lines.append("ACTIVE_PROJECT is empty or unreadable.")

    in_production = root / "video-projects" / "_IN_PRODUCTION"
    if in_production.is_dir():
        ready = sorted(
            d.name for d in in_production.iterdir()
            if d.is_dir() and all((d / f).is_file() for f in HOT_FILES)
        )
        if ready:
            lines.append("")
            lines.append("Projects that WOULD resolve (all three hot files present):")
            lines.extend(f"  - {name}" for name in ready)

    lines += [
        "",
        "AGENTS.md: repair the hot files BEFORE any other work. Build them from what is",
        "already in the folder (a PROJECT-STATUS.md or the newest SCRIPT-V*), write them",
        "under the real names, and say in one line what was built and from what.",
        "",
    ]

    channel_path = root / "CHANNEL.md"
    if channel_path.is_file():
        channel = channel_path.read_text(encoding="utf-8", errors="replace").strip()
        lines.append("Channel state is unaffected and still applies:")
        lines.append("")
        lines.append(channel)
    else:
        lines.append("CHANNEL.md is ALSO missing — this session has no channel state either.")

    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        print(render_context())
    except (ActiveProjectError, OSError) as exc:
        print(render_degraded(exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
