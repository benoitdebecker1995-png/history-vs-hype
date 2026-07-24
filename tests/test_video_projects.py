"""Tests for the VideoProjectRepo resolver.

Builds a fake video-projects/ tree under tmp_path — no real project folders
touched. Covers the canonicalization wins the resolver exists for: stage
discovery, _ARCHIVED/old-* and _BACKLOG exclusion, published-vs-abandoned
discrimination, phase classification (previously untested), and by_slug.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.video_projects import (  # noqa: E402
    AmbiguousSlugError,
    Stage,
    VideoProjectRepo,
)


@pytest.fixture
def repo(tmp_path: Path) -> VideoProjectRepo:
    """A fake project tree exercising every stage + every excluded sibling."""
    vp = tmp_path / "video-projects"

    def make(rel: str, files=()):
        d = vp / rel
        d.mkdir(parents=True, exist_ok=True)
        for name in files:
            (d / name).write_text("x", encoding="utf-8")
        return d

    # live stages
    make("_IN_PRODUCTION/36-panama-canal-2026", ["SCRIPT.md", "01-VERIFIED-RESEARCH.md"])
    make("_IN_PRODUCTION/59-israel-partition-2026", ["01-VERIFIED-RESEARCH.md"])
    make("_READY_TO_FILM/58-kurdistan-2026", ["FINAL-SCRIPT.md"])
    make("_ARCHIVED/published/1-somaliland-2025", ["POST-PUBLISH-ANALYSIS.md"])

    # outside the lifecycle — must NEVER show up
    make("_ARCHIVED/old-belize", ["SCRIPT.md"])          # abandoned draft
    make("_ARCHIVED/old-kosovo/drafts")                  # abandoned, nested
    make("_BACKLOG/99-parked-2026", ["01-VERIFIED-RESEARCH.md"])

    # non-project noise in a live stage
    make("_IN_PRODUCTION/README-notes")                  # README* skip
    (vp / "_IN_PRODUCTION" / "stray.md").write_text("x", encoding="utf-8")

    return VideoProjectRepo(repo_root=tmp_path)


def slugs(projects):
    return {p.slug for p in projects}


def test_all_returns_only_live_stages(repo):
    assert slugs(repo.all()) == {
        "36-panama-canal-2026",
        "59-israel-partition-2026",
        "58-kurdistan-2026",
        "1-somaliland-2025",
    }


def test_archived_old_and_backlog_excluded(repo):
    found = slugs(repo.all())
    assert "old-belize" not in found
    assert "old-kosovo" not in found
    assert "99-parked-2026" not in found
    # the literal 'published' folder is not itself a project
    assert "published" not in found


def test_readme_and_stray_files_skipped(repo):
    in_prod = slugs(repo.in_stage(Stage.IN_PRODUCTION))
    assert in_prod == {"36-panama-canal-2026", "59-israel-partition-2026"}


def test_in_stage_published_only_archived_published(repo):
    pub = repo.in_stage(Stage.PUBLISHED)
    assert slugs(pub) == {"1-somaliland-2025"}
    assert pub[0].is_published


def test_phase_classification(repo):
    by = {p.slug: p.phase for p in repo.all()}
    assert by["36-panama-canal-2026"] == "scripting"      # SCRIPT.md, no verification
    assert by["59-israel-partition-2026"] == "research"   # 01-VERIFIED only
    assert by["58-kurdistan-2026"] == "filming-ready"     # FINAL-SCRIPT.md
    assert by["1-somaliland-2025"] == "published"         # POST-PUBLISH present


def test_stage_assigned_from_path(repo):
    by = {p.slug: p.stage for p in repo.all()}
    assert by["36-panama-canal-2026"] == Stage.IN_PRODUCTION
    assert by["58-kurdistan-2026"] == Stage.READY_TO_FILM
    assert by["1-somaliland-2025"] == Stage.PUBLISHED


def test_by_slug_exact(repo):
    p = repo.by_slug("36-panama-canal-2026")
    assert p is not None and p.slug == "36-panama-canal-2026"


def test_by_slug_partial(repo):
    # finds a published video across stages — the retitle_gen fix
    p = repo.by_slug("1-somaliland")
    assert p is not None and p.stage == Stage.PUBLISHED


def test_by_slug_miss_returns_none(repo):
    assert repo.by_slug("does-not-exist") is None


def test_by_slug_ambiguous_raises(tmp_path):
    vp = tmp_path / "video-projects" / "_IN_PRODUCTION"
    (vp / "40-berlin-conference-2026").mkdir(parents=True)
    (vp / "40-berlin-congo-2026").mkdir(parents=True)
    repo = VideoProjectRepo(repo_root=tmp_path)
    with pytest.raises(AmbiguousSlugError):
        repo.by_slug("40-berlin")


def test_by_slug_stage_restriction(repo):
    assert repo.by_slug("1-somaliland", stage=Stage.IN_PRODUCTION) is None
    assert repo.by_slug("1-somaliland", stage=Stage.PUBLISHED) is not None


def test_content_paths(repo):
    panama = repo.by_slug("36-panama-canal-2026")
    assert panama.script_path.name == "SCRIPT.md"
    assert panama.post_publish_path is None
    assert panama.research_path.name == "01-VERIFIED-RESEARCH.md"

    somaliland = repo.by_slug("1-somaliland-2025")
    assert somaliland.post_publish_path.name == "POST-PUBLISH-ANALYSIS.md"


def test_missing_projects_dir_is_empty(tmp_path):
    repo = VideoProjectRepo(repo_root=tmp_path)
    assert repo.all() == []
