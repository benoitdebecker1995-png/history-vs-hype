"""VideoProjectRepo — read-only resolver over the lifecycle folders.

The deep seam that ends the per-site re-derivation of "where do projects live"
and "what phase is this one." It owns:

  - The canonical layout: three *live* stages (_IN_PRODUCTION, _READY_TO_FILM,
    _ARCHIVED/published). `_BACKLOG/` and `_ARCHIVED/old-*` are outside the
    lifecycle and never appear in `all()`.
  - Path resolution, REPO_ROOT-anchored (no cwd-relative globbing).
  - `phase`, reusing `project_scanner.detect_phase` (its one home), exposed as a
    property of the resolved project.

It is **read-only**. Folder moves between stages stay in `tools/reconcile/`
(shutil.move + .pre-diff backups + reversible diff log); reconcile asks this
resolver for paths but keeps owning the mutation. See ADR-0008.

Rich, but lazy: `.script` / `.post_publish` / `.status` compose the existing
typed readers (`production.ScriptParser`, `post_publish.PostPublishStore`,
`status_doc.StatusDoc`) only when read, so identity stays cheap. `.research`
awaits its typed reader and for now exposes a resolved path.
"""
from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import List, Optional

# Reuse the existing phase rule and slug parser — do not re-implement them.
from tools.dashboard.project_scanner import detect_phase, extract_topic_slug

_DEFAULT_ROOT = Path(__file__).resolve().parents[2]

# Script file names, best-first. A project may carry several; the resolver
# picks the most production-advanced one present.
_SCRIPT_NAMES = ("FINAL-SCRIPT.md", "SCRIPT.md", "02-SCRIPT-DRAFT.md")

_POST_PUBLISH_NAME = "POST-PUBLISH-ANALYSIS.md"
_STATUS_NAME = "PROJECT-STATUS.md"
_RESEARCH_NAME = "01-VERIFIED-RESEARCH.md"


class Stage:
    """The three live lifecycle stages (folder a project sits in).

    Tokens, not raw folder names — `_STAGE_DIRS` maps each to its relative path
    under `video-projects/`. `_BACKLOG` and `_ARCHIVED/old-*` are intentionally
    absent: they are outside the lifecycle.
    """

    IN_PRODUCTION = "in_production"
    READY_TO_FILM = "ready_to_film"
    PUBLISHED = "published"

    #: Ordered most-active to least-active.
    ALL = (IN_PRODUCTION, READY_TO_FILM, PUBLISHED)


_STAGE_DIRS = {
    Stage.IN_PRODUCTION: ("_IN_PRODUCTION",),
    Stage.READY_TO_FILM: ("_READY_TO_FILM",),
    Stage.PUBLISHED: ("_ARCHIVED", "published"),
}


class AmbiguousSlugError(ValueError):
    """Raised when `by_slug` matches more than one project.

    Mirrors the reconcile rule: if a slug is ambiguous, surface it rather than
    silently picking one.
    """

    def __init__(self, slug: str, matches: List[str]) -> None:
        self.slug = slug
        self.matches = matches
        super().__init__(
            f"slug {slug!r} matched {len(matches)} projects: {', '.join(matches)}"
        )


class VideoProject:
    """One project folder — identity is cheap, contents are lazy.

    Identity (`slug`, `path`, `stage`) is set at construction and never mutated.
    `files`, `phase`, `topic_slug`, and the content readers are computed on first
    access and cached.
    """

    def __init__(self, slug: str, path: Path, stage: str) -> None:
        self.slug = slug
        self.path = path
        self.stage = stage

    # --- identity-derived, lazy -------------------------------------------

    @cached_property
    def files(self) -> set:
        """Top-level file names (no subdirectory contents)."""
        try:
            return {f.name for f in self.path.iterdir() if f.is_file()}
        except OSError:
            return set()

    @cached_property
    def phase(self) -> str:
        """Fine-grained production state from the file set (`detect_phase`)."""
        return detect_phase(self.files)

    @cached_property
    def topic_slug(self) -> str:
        """Folder name with numeric prefix and trailing year stripped."""
        return extract_topic_slug(self.slug)

    @property
    def is_published(self) -> bool:
        return self.stage == Stage.PUBLISHED

    # --- content paths -----------------------------------------------------

    @property
    def script_path(self) -> Optional[Path]:
        """Most production-advanced script file present, or None."""
        for name in _SCRIPT_NAMES:
            p = self.path / name
            if p.exists():
                return p
        return None

    @property
    def post_publish_path(self) -> Optional[Path]:
        p = self.path / _POST_PUBLISH_NAME
        return p if p.exists() else None

    @property
    def status_path(self) -> Optional[Path]:
        p = self.path / _STATUS_NAME
        return p if p.exists() else None

    @property
    def research_path(self) -> Optional[Path]:
        p = self.path / _RESEARCH_NAME
        return p if p.exists() else None

    # --- composed readers (lazy; imports kept local to avoid a cycle) ------

    @cached_property
    def script(self):
        """Parsed script sections, or None. Composes `production.ScriptParser`."""
        path = self.script_path
        if path is None:
            return None
        from tools.production.parser import ScriptParser

        return ScriptParser().parse_file(path)

    @cached_property
    def post_publish(self):
        """Parsed post-publish report, or None. Composes `PostPublishStore`."""
        path = self.post_publish_path
        if path is None:
            return None
        from tools.post_publish import PostPublishStore

        return PostPublishStore().load(path)

    @cached_property
    def status(self):
        """Typed PROJECT-STATUS.md reader (AUTO zones + shared fields).
        Composes `StatusDoc`; an absent file loads as an empty doc."""
        from tools.video_projects.status_doc import StatusDoc

        return StatusDoc.load(self.path / _STATUS_NAME)

    # --- dunders -----------------------------------------------------------

    def __eq__(self, other) -> bool:
        return isinstance(other, VideoProject) and other.path == self.path

    def __hash__(self) -> int:
        return hash(self.path)

    def __repr__(self) -> str:
        return f"VideoProject(slug={self.slug!r}, stage={self.stage!r})"


class VideoProjectRepo:
    """Discovers and resolves video projects across the three live stages."""

    def __init__(self, repo_root: Optional[Path] = None) -> None:
        self.repo_root = Path(repo_root) if repo_root is not None else _DEFAULT_ROOT
        self.projects_dir = self.repo_root / "video-projects"

    def _stage_dir(self, stage: str) -> Path:
        return self.projects_dir.joinpath(*_STAGE_DIRS[stage])

    def in_stage(self, stage: str) -> List[VideoProject]:
        """All projects in one stage, sorted by folder name."""
        if stage not in _STAGE_DIRS:
            raise ValueError(f"unknown stage {stage!r}; expected one of {Stage.ALL}")
        root = self._stage_dir(stage)
        if not root.exists():
            return []
        out = []
        for folder in sorted(root.iterdir()):
            if not folder.is_dir():
                continue
            # README dirs and infra folders (leading _ or .) are not projects.
            if folder.name.startswith(("README", "_", ".")):
                continue
            out.append(VideoProject(folder.name, folder, stage))
        return out

    def all(self) -> List[VideoProject]:
        """Every project across the three live stages."""
        return [p for stage in Stage.ALL for p in self.in_stage(stage)]

    def by_slug(self, slug: str, stage: Optional[str] = None) -> Optional[VideoProject]:
        """Resolve a project by folder name.

        Exact folder-name match wins; otherwise a single prefix/substring match
        is returned. Multiple matches raise `AmbiguousSlugError`; no match
        returns None. Pass `stage` to restrict the search.
        """
        stages = (stage,) if stage is not None else Stage.ALL
        target = slug.lower()
        exact: List[VideoProject] = []
        partial: List[VideoProject] = []
        for s in stages:
            for p in self.in_stage(s):
                name = p.slug.lower()
                if name == target:
                    exact.append(p)
                elif name.startswith(target) or target in name:
                    partial.append(p)
        hits = exact or partial
        if not hits:
            return None
        if len(hits) > 1:
            raise AmbiguousSlugError(slug, [p.slug for p in hits])
        return hits[0]
