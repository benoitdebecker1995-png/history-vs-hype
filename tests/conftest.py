"""Shared pytest fixtures for History vs Hype test suite."""
import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def keyword_db():
    """In-memory KeywordDB with schema auto-initialized."""
    from tools.discovery.database import KeywordDB
    db = KeywordDB(db_path=":memory:")
    yield db
    db.close()


@pytest.fixture
def intel_store(tmp_path):
    """KBStore with temp file db (NOT :memory: — KBStore uses per-call connections)."""
    from tools.intel.kb_store import KBStore
    store = KBStore(db_path=tmp_path / "test_intel.db")
    yield store


@pytest.fixture
def tmp_script(tmp_path):
    """Copy test_script.md fixture to tmp_path and return its Path."""
    src = FIXTURES_DIR / "test_script.md"
    dst = tmp_path / "test_script.md"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


@pytest.fixture
def tmp_post_publish(tmp_path):
    """Create POST-PUBLISH-ANALYSIS.md in correct subdirectory structure.

    Returns tmp_path (project_root) — import_from_analysis_files scans
    project_root/video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md
    """
    src = FIXTURES_DIR / "test_post_publish.md"
    video_dir = tmp_path / "video-projects" / "_IN_PRODUCTION" / "test-video-2026"
    video_dir.mkdir(parents=True)
    (video_dir / "POST-PUBLISH-ANALYSIS.md").write_text(
        src.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return tmp_path
