"""PostPublishStore — single seam over POST-PUBLISH-ANALYSIS.md files.

Peer to tools.youtube_analytics.store.AnalyticsStore and
tools.discovery.keyword_store.KeywordStore. Owns:

  - discovery of post-publish reports across the four canonical roots
  - parsing the markdown into a typed PostPublishReport dataclass
  - the error contract (raise on parse failure; swallow-and-log in bulk helper)

See CONTEXT.md "Post-publish report" for the domain definition. See ADR-0005
(post-publish report seam) for the architectural decision.

Usage:

    from tools.post_publish import PostPublishStore

    store = PostPublishStore()                 # uses repo root, auto-discovered
    for report in store.discover_and_load_all():
        print(report.video_id, report.avg_retention_pct)

    # strict mode — raises on malformed/missing
    report = store.load(Path("channel-data/analyses/POST-PUBLISH-ANALYSIS-XYZ.md"))
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from tools.logging_config import get_logger

from tools.post_publish import _parser

logger = get_logger(__name__)

# Two levels up from tools/post_publish/store.py
_REPO_ROOT = Path(__file__).resolve().parents[2]


# ── error contract ────────────────────────────────────────────────────────────


class PostPublishParseError(Exception):
    """Base class for post-publish parse failures."""


class PostPublishMissingError(PostPublishParseError):
    """Raised when the file cannot be read (missing, permissions, encoding)."""


class PostPublishMalformedError(PostPublishParseError):
    """Raised when the file is readable but cannot yield a video_id."""


# ── return shape ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class PostPublishReport:
    """Typed representation of one POST-PUBLISH-ANALYSIS.md file.

    Field-name and unit contract:

      - Retention values are PERCENTS (e.g. 28.1), matching the source markdown.
        Use `avg_retention_fraction` / `final_retention_fraction` if you need
        the 0–1 form. NOTE: the legacy parser in patterns.py stored
        `avg_retention` as a fraction (0.281); migrating callers must update.
      - CTR is a PERCENT (e.g. 4.2). `ctr` property exposes the legacy name.
      - Drop points: list of dicts {position_pct, viewers_lost_pct, location}.
      - Body sections (observations, actionable, drop_points, discovery)
        default to empty / None when the report doesn't contain them yet.
    """

    video_id: str
    source_path: Path

    # Header
    title: Optional[str] = None
    analyzed_date: Optional[str] = None

    # Metrics (all percents stored as percents, not fractions)
    avg_retention_pct: Optional[float] = None
    final_retention_pct: Optional[float] = None
    ctr_percent: Optional[float] = None
    impressions: Optional[int] = None
    views: Optional[int] = None
    watch_time_minutes: Optional[float] = None
    subscribers_gained: Optional[int] = None

    # Body
    observations: List[str] = field(default_factory=list)
    actionable: List[str] = field(default_factory=list)
    drop_points: List[Dict[str, Any]] = field(default_factory=list)
    discovery: Optional[Dict[str, Optional[str]]] = None

    # ── derived / aliases ────────────────────────────────────────────────────

    @property
    def ctr(self) -> Optional[float]:
        """Legacy name for ctr_percent (used by feedback_parser callers)."""
        return self.ctr_percent

    @property
    def avg_retention_fraction(self) -> Optional[float]:
        """avg_retention_pct expressed as a 0–1 fraction (legacy patterns.py form)."""
        return self.avg_retention_pct / 100 if self.avg_retention_pct is not None else None

    @property
    def final_retention_fraction(self) -> Optional[float]:
        return (
            self.final_retention_pct / 100
            if self.final_retention_pct is not None
            else None
        )

    @property
    def biggest_drop_position(self) -> Optional[int]:
        """Position (as percent of runtime) of the drop with the largest viewer loss."""
        if not self.drop_points:
            return None
        biggest = max(self.drop_points, key=lambda d: d["viewers_lost_pct"])
        return biggest["position_pct"]


# ── store ─────────────────────────────────────────────────────────────────────


class PostPublishStore:
    """Discover, load, and iterate post-publish reports.

    Callers either:
      - call discover_and_load_all() for the common "iterate every report,
        skip malformed ones with a warning" loop, or
      - call discover() + load(path) for strict handling where a malformed
        report should crash the calling routine.
    """

    DEFAULT_GLOBS = (
        "video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md",
        "video-projects/_READY_TO_FILM/*/POST-PUBLISH-ANALYSIS.md",
        "video-projects/_ARCHIVED/*/POST-PUBLISH-ANALYSIS.md",
        "video-projects/_ARCHIVED/published/*/POST-PUBLISH-ANALYSIS.md",
        "channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md",
    )

    def __init__(self, project_root: Path = _REPO_ROOT) -> None:
        self._project_root = Path(project_root)

    # ── discovery ────────────────────────────────────────────────────────────

    def discover(self) -> List[Path]:
        """Return all post-publish report paths under the project root, sorted."""
        files: List[Path] = []
        for glob in self.DEFAULT_GLOBS:
            files.extend(self._project_root.glob(glob))
        return sorted(set(files))

    # ── single-file load (strict) ────────────────────────────────────────────

    def load(self, path: Path) -> PostPublishReport:
        """Parse one report. Raise on missing or malformed.

        Raises:
            PostPublishMissingError: file cannot be read.
            PostPublishMalformedError: file exists but yields no video_id.
        """
        path = Path(path)
        try:
            content = path.read_text(encoding="utf-8")
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
            raise PostPublishMissingError(f"Cannot read {path}: {exc}") from exc

        video_id = _parser.extract_video_id(content, str(path))
        if not video_id:
            raise PostPublishMalformedError(f"No video_id found in {path}")

        metrics = _parser.extract_metrics(content)
        lessons = _parser.extract_lessons(content)

        return PostPublishReport(
            video_id=video_id,
            source_path=path,
            title=_parser.extract_title(content),
            analyzed_date=_parser.extract_analyzed_date(content),
            observations=lessons["observations"],
            actionable=lessons["actionable"],
            drop_points=_parser.extract_drop_points(content),
            discovery=_parser.extract_discovery_diagnosis(content),
            **metrics,
        )

    # ── bulk load (lenient) ──────────────────────────────────────────────────

    def discover_and_load_all(self) -> Iterator[PostPublishReport]:
        """Yield every parseable report. Skip malformed ones with a warning log.

        This is what most callers want — preserves the silent-skip behaviour
        the previous ad-hoc readers depended on (news_hook_monitor, dashboard,
        patterns, retitle_audit), without forcing them to wrap try/except.
        """
        for path in self.discover():
            try:
                yield self.load(path)
            except PostPublishMalformedError as exc:
                logger.warning("Skipping malformed post-publish report: %s", exc)
            except PostPublishMissingError as exc:
                # Shouldn't happen — discover() just listed it — but be defensive.
                logger.warning("Skipping unreadable post-publish report: %s", exc)