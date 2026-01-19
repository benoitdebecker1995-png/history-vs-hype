# Coding Conventions

**Analysis Date:** 2025-01-19

## Naming Patterns

**Files:**
- Python files: `snake_case.py` (e.g., `clip_detector.py`, `video_processor.py`)
- JavaScript files: `snake_case.js` or `camelCase.js` (e.g., `app.js`, `wizard.js`)
- Configuration: `snake_case.toml` or `snake_case.txt`
- Modules: lowercase directories (e.g., `api/`, `core/`, `scoring/`)

**Functions:**
- Python: `snake_case` (e.g., `detect_clips()`, `get_video_metadata()`)
- JavaScript: `camelCase` (e.g., `loadProjects()`, `showStatus()`)

**Variables:**
- Python: `snake_case` (e.g., `project_id`, `source_video_path`)
- JavaScript: `camelCase` (e.g., `selectedProjectId`, `API_BASE`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DATA_DIR`, `CONFIG_DIR`, `CATEGORIES`)

**Classes:**
- `PascalCase` (e.g., `ClipDetector`, `VideoProcessor`, `BookMetadata`)
- Pydantic models: `PascalCase` with descriptive suffixes (e.g., `ProjectCreate`, `ClipResponse`)

**Types:**
- Pydantic schemas use descriptive suffixes: `*Create`, `*Response`, `*Request`
- SQLAlchemy models: singular noun (`Project`, `Clip`)

## Code Style

**Formatting:**
- No automated formatter detected (no .prettierrc, eslint, black config)
- Indentation: 4 spaces (Python), 4 spaces (JavaScript)
- Line length: ~100 characters observed (not strictly enforced)

**Linting:**
- No automated linter configuration detected
- Implicit type hints used throughout Python code

## Import Organization

**Order (Python):**
1. Standard library imports (`json`, `os`, `re`, `sys`, `shutil`)
2. Third-party imports (`fastapi`, `pydantic`, `ffmpeg`, `sqlalchemy`)
3. Local imports (`from utils.logger import logger`, `from models.database import get_session`)

**Path Aliases:**
- No path aliases configured
- Relative imports within packages: `from scoring import patterns`
- Absolute imports from package root: `from utils.config import DATA_DIR`

**JavaScript:**
- No module bundler (vanilla JS with direct script includes)
- API base URL as constant: `const API_BASE = 'http://localhost:8000';`

## Error Handling

**Patterns:**

**FastAPI Routes Pattern:**
```python
try:
    # Main logic
    session = get_session()
    # ... operations ...
    session.close()
    return result
except HTTPException:
    raise  # Re-raise HTTP exceptions as-is
except Exception as e:
    logger.error(f"Error [operation]: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

**File Operations Pattern:**
```python
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
except Exception as e:
    logger.error(f"FFmpeg error: {e.stderr.decode()}")
    raise
```

**Optional Dependency Pattern:**
```python
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("ERROR: youtube-transcript-api not installed")
    sys.exit(1)
```

**Validation Pattern:**
```python
if not project:
    raise HTTPException(status_code=404, detail="Project not found")
if not project.transcribed:
    raise HTTPException(status_code=400, detail="Project must be transcribed first")
```

## Logging

**Framework:** Python `logging` module

**Setup Pattern:**
```python
from utils.logger import logger

logger.info(f"Operation starting: {details}")
logger.error(f"Error [context]: {e}")
logger.debug(f"Debug info: {variable}")
```

**Logger Configuration:**
- Located at `tools/history-clip-tool/src/utils/logger.py`
- Dual output: file handler + console handler
- Log files: `{LOGS_DIR}/clip_detection_{timestamp}.log`
- Format: `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`

**When to Log:**
- Operation start/completion
- Error conditions with full context
- Key decision points in scoring/detection
- All clip scoring reasons (for transparency)

## Comments

**When to Comment:**
- Module docstrings: Required for all Python files
- Class docstrings: Required with purpose description
- Function docstrings: Google-style with Args, Returns sections
- Inline comments: Explain "why" for non-obvious logic

**Docstring Style:**
```python
"""
Module description.
Purpose and context.
"""

class ClipScorer:
    """
    Scores transcript segments based on academic/historical content quality.
    All scoring decisions are logged with reasoning.
    """

def score_segment(self, text: str, start: float, end: float) -> Dict:
    """
    Score a transcript segment for clip worthiness.

    Args:
        text: Transcript text
        start: Start timestamp in seconds
        end: End timestamp in seconds

    Returns:
        Dictionary with score, reasons, duration, and text
    """
```

**Inline Comments:**
```python
# Step 1: Create temporary clip without captions
temp_clip = self.export_dir / f"clip_{clip_number:03d}_temp.mp4"

# Quantized for faster CPU inference
compute_type="int8",
```

## Function Design

**Size:**
- Functions typically 10-50 lines
- Complex operations broken into private methods (prefixed with `_`)
- Single responsibility principle observed

**Parameters:**
- Type hints on all parameters
- Default values for optional parameters
- Complex parameters documented in docstring

**Return Values:**
- Type hints on return values (`-> Dict`, `-> Path`, `-> List[Dict]`)
- Consistent dictionary structures for complex returns
- HTTP routes return Pydantic models

## Module Design

**Exports:**
- Classes exported at module level
- Global instances for singletons: `config = Config()`, `logger = setup_logger()`

**Barrel Files:**
- `__init__.py` files contain module docstrings only
- No explicit `__all__` exports

**Package Structure:**
```
src/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app initialization
│   └── routes/          # Route handlers by resource
│       ├── projects.py
│       ├── clips.py
│       └── transcribe.py
├── core/                # Business logic
│   ├── transcriber.py
│   ├── clip_detector.py
│   └── exporter.py
├── models/              # Data models
│   ├── database.py      # SQLAlchemy models
│   └── schemas.py       # Pydantic schemas
├── scoring/             # Scoring algorithms
│   ├── rules.py
│   └── patterns.py
└── utils/               # Shared utilities
    ├── config.py
    └── logger.py
```

## Configuration Pattern

**TOML Configuration:**
- External config files in `config/` directory
- Loaded at module initialization
- Example: `scoring_rules.toml`, `caption_presets.toml`

**Environment-Based Paths:**
```python
DATA_DIR = Path(os.environ.get('APP_DATA_DIR', BASE_DIR / "data"))
MODELS_DIR = Path(os.environ.get('APP_MODELS_DIR', BASE_DIR / "models"))
```

**Hardcoded Paths (Standalone Scripts):**
```python
DOWNLOADS_DIR = Path(r"C:\Users\benoi\Downloads")
LIBRARY_DIR = Path(r"C:\Users\benoi\Documents\History vs Hype\library\by-topic")
```

## Database Patterns

**SQLAlchemy Session Management:**
```python
session = get_session()
try:
    # Query operations
    project = session.query(Project).filter(Project.id == project_id).first()
    session.commit()
finally:
    session.close()
```

**Model Definition:**
```python
class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    clips = relationship("Clip", back_populates="project", cascade="all, delete-orphan")
```

## API Design Patterns

**Router Organization:**
```python
router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse)
@router.get("/", response_model=List[ProjectResponse])
@router.get("/{project_id}", response_model=ProjectResponse)
@router.delete("/{project_id}")
```

**Response Models:**
- Use Pydantic `response_model` for type safety
- `from_orm()` / `from_attributes` for SQLAlchemy model conversion

## JavaScript Patterns

**Event Handlers:**
```javascript
document.getElementById('createProjectForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    // Handler logic
});
```

**Async/Fetch Pattern:**
```javascript
try {
    const response = await fetch(`${API_BASE}/endpoint`, {
        method: 'POST',
        body: formData
    });
    if (!response.ok) {
        throw new Error('Request failed');
    }
    const data = await response.json();
    // Handle success
} catch (error) {
    showStatus('elementId', `Error: ${error.message}`, 'error');
}
```

---

*Convention analysis: 2025-01-19*
