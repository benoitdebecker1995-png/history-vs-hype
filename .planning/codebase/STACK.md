# Technology Stack

**Analysis Date:** 2026-01-19

## Languages

**Primary:**
- Python 3.x - All automation tools, transcription, video processing, utilities

**Secondary:**
- JavaScript (ES6+) - Frontend UI for History Clip Tool (`tools/history-clip-tool/frontend/public/app.js`)
- PowerShell - VTT/subtitle conversion utilities (`tools/convert-vtt*.ps1`, `tools/fix-*.ps1`)
- Markdown - Documentation, scripts, research files

## Runtime

**Environment:**
- Python 3.x (version not pinned - no `.python-version` or `pyproject.toml`)
- Node.js not required (JavaScript is vanilla, no npm/yarn)

**Package Manager:**
- pip (standard Python package manager)
- Lockfile: Missing - no `requirements-lock.txt` or `pip freeze` output

## Frameworks

**Core:**
- FastAPI 0.109.0 - REST API for History Clip Tool (`tools/history-clip-tool/src/api/main.py`)
- Pydantic 2.5.3 - Data validation and settings (`tools/history-clip-tool/requirements.txt`)

**AI/ML:**
- faster-whisper >=1.0.0 - Local audio transcription (`tools/history-clip-tool/src/core/transcriber.py`)
- PyTorch >=2.1.2 - ML backend for Whisper (CPU-only)
- torchaudio >=2.1.2 - Audio processing

**Testing:**
- None detected - No pytest, unittest, or test files found

**Build/Dev:**
- PyInstaller 6.3.0 - Packaging clip tool as standalone executable
- pywebview 4.4.1 - Native window wrapper for desktop app

## Key Dependencies

**Critical (History Clip Tool):**
- `uvicorn[standard]` 0.27.0 - ASGI server for FastAPI
- `sqlalchemy` 2.0.25 - Database ORM
- `ffmpeg-python` 0.2.0 - Video processing wrapper
- `opencv-python` 4.9.0.80 - Face detection (optional)
- `toml` 0.10.2 - Configuration file parsing
- `aiofiles` 23.2.1 - Async file operations
- `python-multipart` 0.0.6 - File upload handling

**External Tools (Transcript Extraction):**
- `youtube-transcript-api` - YouTube transcript fetching (`.claude/tools/get-transcript.py`)

**Prompt Evaluation:**
- `anthropic` - Anthropic Claude API client (optional, for live evaluation)

## Configuration

**Environment:**
- `ANTHROPIC_API_KEY` - Required for prompt evaluation tool (`tools/prompt_evaluation.py`)
- `APP_DATA_DIR` - Override data directory for clip tool executable
- `APP_MODELS_DIR` - Override models directory for clip tool executable
- `APP_LOGS_DIR` - Override logs directory for clip tool executable

**Build:**
- `tools/history-clip-tool/config/scoring_rules.toml` - Clip detection scoring weights
- `tools/history-clip-tool/config/caption_presets.toml` - Caption style presets (academic, minimal, shorts_friendly, documentary)
- `.claude/settings.local.json` - Claude Code permissions and allowed tools

**Sensitive Files:**
- `.env` files - gitignored
- `secrets.json` - gitignored
- `credentials.json` - gitignored

## Database

**Type:** SQLite
- Location: `tools/history-clip-tool/data/projects.db`
- ORM: SQLAlchemy 2.0.25
- Schema: `Project` and `Clip` tables (`tools/history-clip-tool/src/models/database.py`)

## Platform Requirements

**Development:**
- Windows (primary development environment - Windows paths throughout)
- Python 3.x with pip
- FFmpeg installed and in PATH (or portable copy in `tools/ffmpeg/`)
- yt-dlp.exe for transcript extraction (`tools/yt-dlp.exe`)

**Production:**
- Local execution only - no cloud deployment
- History Clip Tool can be packaged as Windows executable via PyInstaller

## External Tools (Non-Code)

**Video Production:**
- DaVinci Resolve - Video editing (`.drp` files gitignored)
- Photoshop - Thumbnail creation (`.psd~` gitignored)

**Research:**
- NotebookLM (Google) - Academic source-grounded research
- VidIQ Pro - YouTube optimization and topic research

**Content:**
- Claude Code (Anthropic) - Fact-checking, research, scripting assistance

## File Types Managed

**Content:**
- `.md` - Scripts, research, documentation
- `.vtt` / `.srt` - Subtitle files
- `.pdf` - Academic sources (organized via `library/organize_books.py`)

**Media (gitignored):**
- `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv` - Video files
- `.wav`, `.aiff` - Large audio files

---

*Stack analysis: 2026-01-19*
