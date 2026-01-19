# Testing Patterns

**Analysis Date:** 2025-01-19

## Test Framework

**Runner:**
- Not detected - No test framework configured
- No `pytest.ini`, `conftest.py`, `jest.config.*`, or `vitest.config.*` found
- No `*.test.*` or `*.spec.*` files found

**Assertion Library:**
- Not applicable (no tests exist)

**Run Commands:**
```bash
# No test commands configured
# Recommendation: Add pytest for Python code
pip install pytest pytest-asyncio pytest-cov
pytest                     # Run all tests
pytest --cov=src           # Run with coverage
pytest -v                  # Verbose output
```

## Test File Organization

**Location:**
- Tests do not currently exist
- Recommended pattern: `tests/` directory at project root, mirroring `src/` structure

**Naming (Recommended):**
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

**Recommended Structure:**
```
tools/history-clip-tool/
├── src/
│   ├── api/
│   ├── core/
│   ├── models/
│   └── scoring/
└── tests/
    ├── conftest.py           # Shared fixtures
    ├── test_api/
    │   ├── test_projects.py
    │   ├── test_clips.py
    │   └── test_transcribe.py
    ├── test_core/
    │   ├── test_clip_detector.py
    │   ├── test_transcriber.py
    │   └── test_video_processor.py
    └── test_scoring/
        ├── test_rules.py
        └── test_patterns.py
```

## Test Structure

**Suite Organization (Recommended):**
```python
import pytest
from scoring.rules import ClipScorer
from scoring.patterns import contains_any_keyword, count_pattern_matches


class TestClipScorer:
    """Tests for ClipScorer class."""

    @pytest.fixture
    def scorer(self):
        """Create scorer instance for tests."""
        return ClipScorer()

    def test_score_segment_with_primary_source(self, scorer):
        """Test scoring increases for primary source references."""
        result = scorer.score_segment(
            text="According to the treaty of 1916, the borders were drawn...",
            start=0.0,
            end=10.0
        )
        assert result['score'] > 0
        assert any('primary source' in r.lower() for r in result['reasons'])

    def test_score_segment_penalizes_clickbait(self, scorer):
        """Test scoring decreases for clickbait language."""
        result = scorer.score_segment(
            text="SHOCKING SECRETS they don't want you to know!",
            start=0.0,
            end=10.0
        )
        assert any('clickbait' in r.lower() for r in result['reasons'])
```

**Patterns:**
- Setup: Use pytest fixtures (`@pytest.fixture`)
- Teardown: Use fixture `yield` pattern or `request.addfinalizer`
- Assertion: Use plain `assert` statements

## Mocking

**Framework (Recommended):** `pytest-mock` or `unittest.mock`

**Patterns:**
```python
from unittest.mock import Mock, patch, MagicMock

class TestTranscriber:
    """Tests for Transcriber class."""

    @patch('core.transcriber.WhisperModel')
    def test_transcribe_loads_model(self, mock_model_class):
        """Test that WhisperModel is loaded with correct parameters."""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        transcriber = Transcriber(model_size="base", device="cpu")

        mock_model_class.assert_called_once_with(
            "base",
            device="cpu",
            compute_type="int8",
            download_root=pytest.approx(ANY)
        )

    @patch('core.video_processor.ffmpeg')
    def test_extract_audio_calls_ffmpeg(self, mock_ffmpeg):
        """Test audio extraction uses correct FFmpeg parameters."""
        processor = VideoProcessor("test-project-id")
        # ... setup mock ...
        processor.extract_audio("/path/to/video.mp4")
        # ... assertions ...
```

**What to Mock:**
- External services (FFmpeg, WhisperModel, Google Books API)
- File system operations for unit tests
- Database sessions for isolated tests
- Network requests

**What NOT to Mock:**
- Pure functions (scoring logic, pattern matching)
- Data transformations
- Pydantic model validation

## Fixtures and Factories

**Test Data (Recommended):**
```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import json


@pytest.fixture
def temp_project_dir():
    """Create temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test-project"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def sample_transcript():
    """Sample transcript data for testing."""
    return {
        "language": "en",
        "duration": 120.0,
        "segments": [
            {"start": 0.0, "end": 5.0, "text": "According to the treaty..."},
            {"start": 5.0, "end": 10.0, "text": "This evidence shows..."},
            {"start": 10.0, "end": 15.0, "text": "SHOCKING revelation!"},
        ]
    }


@pytest.fixture
def sample_project(temp_project_dir, sample_transcript):
    """Create sample project with transcript."""
    transcript_path = temp_project_dir / "transcript.json"
    with open(transcript_path, 'w') as f:
        json.dump(sample_transcript, f)
    return temp_project_dir


@pytest.fixture
def db_session():
    """Create in-memory database session for testing."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.database import Base

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
```

**Location:**
- Shared fixtures: `tests/conftest.py`
- Module-specific fixtures: Within test files

## Coverage

**Requirements:** Not enforced (no CI/CD pipeline detected)

**View Coverage (Recommended):**
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

**Recommended Targets:**
- Core scoring logic: 90%+
- API routes: 80%+
- Utilities: 70%+
- Overall: 80%+

## Test Types

**Unit Tests:**
- Scope: Individual functions and classes
- Approach: Mock external dependencies
- Location: `tests/test_*/` mirroring `src/`
- Priority areas:
  - `src/scoring/rules.py` - ClipScorer scoring logic
  - `src/scoring/patterns.py` - Pattern matching utilities
  - `src/models/schemas.py` - Pydantic validation

**Integration Tests:**
- Scope: Component interactions
- Approach: Use test database, mock external services
- Priority areas:
  - API route handlers with database
  - ClipDetector with transcript files
  - Exporter pipeline

**E2E Tests:**
- Framework: Not used
- Recommendation: Consider Playwright or Selenium for frontend wizard
- Priority: Low (frontend is simple vanilla JS)

## Common Patterns

**Async Testing:**
```python
import pytest
from httpx import AsyncClient
from api.main import app


@pytest.mark.asyncio
async def test_create_project():
    """Test project creation endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/projects/",
            params={"name": "Test Project"},
            files={"video": ("test.mp4", b"fake video content", "video/mp4")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Project"
```

**Error Testing:**
```python
def test_score_segment_rejects_too_short():
    """Test that segments below minimum duration are rejected."""
    scorer = ClipScorer()
    result = scorer.score_segment(
        text="Short clip",
        start=0.0,
        end=2.0  # Below min_viable_duration
    )
    assert result['score'] == 0
    assert any('TOO SHORT' in r for r in result['reasons'])


def test_clip_detector_raises_on_missing_transcript():
    """Test appropriate error when transcript doesn't exist."""
    detector = ClipDetector("nonexistent-project")
    with pytest.raises(FileNotFoundError, match="Transcript not found"):
        detector.detect_clips()
```

**Parameterized Testing:**
```python
@pytest.mark.parametrize("text,expected_match", [
    ("according to the treaty", True),
    ("page 147 states", True),
    ("some random text", False),
    ("the historian wrote", True),
])
def test_citation_pattern_detection(text, expected_match):
    """Test citation pattern matching."""
    from scoring.patterns import CITATION_COMPILED, count_pattern_matches
    match_count = count_pattern_matches(text, CITATION_COMPILED)
    assert (match_count > 0) == expected_match
```

## Evaluation Framework

**Note:** `tools/prompt_evaluation.py` exists as a prompt evaluation suite, not a traditional test framework.

**Purpose:**
- Evaluate AI prompt quality for script generation
- Compare prompt variants
- Check voice consistency with channel style

**Usage:**
```bash
python tools/prompt_evaluation.py           # Show prompt templates
python tools/prompt_evaluation.py health    # Run project health check
```

**Available Evaluations:**
- Script generation prompts (baseline, kraut_style, alex_oconnor_style)
- Fact-check prompts (tiered_verification, simplification_detection)
- Claim extraction prompts
- Voice check prompts

**Metrics:**
```python
def evaluate_script_quality(response: str) -> dict:
    scores = {
        "has_modern_hook": "[MODERN HOOK]" in response,
        "has_both_extremes": "extreme" in response.lower(),
        "has_document_markers": "[DOCUMENT:" in response,
        "has_timestamps": any(f"{i}:" in response for i in range(0, 15)),
        "has_causal_language": any(w in response.lower() for w in ["consequently", "thereby"]),
        "has_academic_quotes": "page" in response.lower(),
        "word_count": len(response.split()),
    }
    return scores
```

## Testing Gaps

**High Priority (No Tests Exist):**
- `src/scoring/rules.py` - Critical scoring logic
- `src/scoring/patterns.py` - Pattern matching functions
- `src/api/routes/*.py` - API endpoints
- `src/core/clip_detector.py` - Clip detection orchestration

**Medium Priority:**
- `src/models/schemas.py` - Pydantic validation
- `src/core/transcriber.py` - Transcription wrapper
- `src/utils/config.py` - Configuration loading

**Low Priority:**
- `src/core/video_processor.py` - FFmpeg wrapper (integration tests)
- Frontend JavaScript - Simple UI code

## Recommendations

1. **Add pytest and pytest-asyncio** to `requirements.txt`
2. **Create `tests/conftest.py`** with shared fixtures
3. **Start with scoring module tests** - highest value, pure functions
4. **Add API integration tests** using FastAPI TestClient
5. **Set up coverage reporting** in CI pipeline
6. **Consider property-based testing** for pattern matching with Hypothesis

---

*Testing analysis: 2025-01-19*
