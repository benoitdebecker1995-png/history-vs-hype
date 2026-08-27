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


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        print(render_context())
    except (ActiveProjectError, OSError) as exc:
        print(f"Front room unavailable: {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
