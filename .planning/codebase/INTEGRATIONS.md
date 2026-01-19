# External Integrations

**Analysis Date:** 2026-01-19

## APIs & External Services

**YouTube (Read-Only):**
- YouTube Transcript API - Fetches auto-generated transcripts
  - Client: `youtube-transcript-api` Python package
  - Usage: `.claude/tools/get-transcript.py`
  - Auth: None required (public API)
  - Rate limits: Standard YouTube API limits

- yt-dlp - Video/subtitle downloading
  - Binary: `tools/yt-dlp.exe`
  - Usage: Download transcripts, video metadata
  - Auth: Browser cookies (Edge) for age-restricted content

**Anthropic Claude:**
- Claude API - AI-powered prompt evaluation
  - SDK: `anthropic` Python package
  - Auth: `ANTHROPIC_API_KEY` environment variable
  - Usage: `tools/prompt_evaluation.py` for script quality evaluation
  - Model: claude-sonnet-4-20250514

## Data Storage

**Databases:**
- SQLite (local only)
  - Location: `tools/history-clip-tool/data/projects.db`
  - Client: SQLAlchemy 2.0.25
  - Tables: `projects`, `clips`
  - Purpose: Video project and clip metadata storage

**File Storage:**
- Local filesystem only
  - Academic PDFs: `library/by-topic/` (organized by category)
  - Transcripts: `transcripts/`
  - Video projects: `video-projects/_IN_PRODUCTION/`, `_READY_TO_FILM/`, `_ARCHIVED/`
  - Models: `tools/history-clip-tool/models/whisper/`

**Caching:**
- Library metadata: `library/metadata_cache.json`
- No Redis/Memcached - all caching is file-based

## Authentication & Identity

**Auth Provider:**
- None - local-only tools with no user authentication
- API keys stored as environment variables (not in code)

**OAuth/SSO:**
- None implemented

## AI/ML Services

**Local (No API):**
- faster-whisper - Audio transcription
  - Model sizes: tiny, base (default), small, medium, large
  - Download location: `tools/history-clip-tool/models/whisper/`
  - Runs entirely on CPU
  - No cloud inference - 100% local

**Cloud (Optional):**
- Anthropic Claude API - Optional prompt evaluation
  - Only used when `ANTHROPIC_API_KEY` is set
  - Purpose: Script quality scoring, project health checks

## External Research Tools (Non-API)

**Google NotebookLM:**
- 2M token context window
- Customized Audio Overviews
- Interactive Mode for clarification
- Citation grounding with page numbers
- Manual workflow - no API integration

**VidIQ Pro:**
- YouTube optimization research
- Topic research and title testing
- Manual workflow - no API integration

## Monitoring & Observability

**Error Tracking:**
- None - console logging only

**Logs:**
- History Clip Tool: Custom logger in `tools/history-clip-tool/src/utils/logger.py`
- Log directory: configurable via `APP_LOGS_DIR` env var
- Format: Standard Python logging

## CI/CD & Deployment

**Hosting:**
- Local execution only
- No cloud deployment
- PyInstaller for Windows executable packaging

**CI Pipeline:**
- None detected
- No GitHub Actions, Jenkins, or similar

## Environment Configuration

**Required env vars:**
- None strictly required (all tools work without API keys)

**Optional env vars:**
- `ANTHROPIC_API_KEY` - For prompt evaluation AI features
- `APP_DATA_DIR` - Override clip tool data directory
- `APP_MODELS_DIR` - Override clip tool models directory
- `APP_LOGS_DIR` - Override clip tool logs directory

**Secrets location:**
- Environment variables only
- `.env` files gitignored
- No secrets management service

## Webhooks & Callbacks

**Incoming:**
- None - local tools only

**Outgoing:**
- None - all external API calls are synchronous

## Web Access (Claude Code Permissions)

**Allowed domains (from `.claude/settings.local.json`):**
- `i.imgur.com` - Image hosting
- `penelope.uchicago.edu` - Perseus Digital Library (classics)
- `www.perseus.tufts.edu` - Perseus Digital Library
- `www.newadvent.org` - Catholic Encyclopedia (historical reference)
- `archive.org` - Internet Archive
- `en.wikisource.org` - Primary source texts
- `www.youtube.com` - Video research
- `youtubetranscript.com` - Transcript extraction
- `www.googleapis.com` - Google APIs
- `en.wikipedia.org` - General reference
- `legal.un.org` - UN legal documents
- `www.archives.gov` - US National Archives
- Various news sites (Al Jazeera, CNN, NPR, CBS News, etc.)

## Video Processing Dependencies

**FFmpeg:**
- Location: `tools/ffmpeg/` (portable) or system PATH
- Usage: Video/audio processing for clip export
- Wrapper: `ffmpeg-python` 0.2.0

**OpenCV:**
- Package: `opencv-python` 4.9.0.80
- Usage: Optional face detection for clip cropping

## Integration Architecture

```
[Local Tools]
    |
    +-- History Clip Tool (FastAPI + SQLite)
    |       |-- faster-whisper (local transcription)
    |       |-- FFmpeg (video processing)
    |       +-- OpenCV (face detection)
    |
    +-- Transcript Extractor
    |       +-- youtube-transcript-api
    |       +-- yt-dlp.exe
    |
    +-- Prompt Evaluation (optional)
    |       +-- Anthropic Claude API
    |
    +-- Library Organizer
            +-- Local PDF processing
```

**Key principle:** All core functionality runs 100% locally. Cloud APIs (Anthropic) are optional enhancements.

---

*Integration audit: 2026-01-19*
