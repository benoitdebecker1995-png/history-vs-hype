# History Clip Tool

**Local-only, zero-cost video clipping optimized for evidence-based historical content.**

This tool converts long-form educational history videos into short vertical clips (YouTube Shorts, Instagram Reels, TikTok) while preserving academic integrity. Unlike commercial tools like OpusClips, this runs entirely on your machine with **zero runtime cost** and **no cloud dependencies**.

## Features

- ✅ **100% Free to Run** - No paid APIs, no subscriptions, no hidden costs
- ✅ **Fully Offline** - Works without internet after initial setup
- ✅ **Academic-Optimized** - Prioritizes evidence-based content over clickbait
- ✅ **Explainable AI** - Every clip score includes transparent reasoning
- ✅ **Local Transcription** - faster-whisper (4x faster than vanilla Whisper)
- ✅ **Heuristic Scoring** - Detects historical claims, primary sources, causal explanations
- ✅ **Custom Captions** - Academic preset by default (clean, no emojis)
- ✅ **9:16 Vertical Export** - Mobile-optimized MP4 output

## System Requirements

- **Python 3.10+**
- **FFmpeg** (for video processing)
- **4GB+ RAM** (8GB+ recommended for medium/large Whisper models)
- **Storage**: ~2-5GB for Whisper models + project files
- **OS**: Windows, macOS, or Linux

## Installation

### 1. Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Install Python Dependencies

```bash
cd tools/history-clip-tool

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** This will download PyTorch CPU-only version (~100MB) and other dependencies.

### 3. First-Time Model Download

On first run, faster-whisper will automatically download the selected Whisper model:

- `tiny`: ~75MB (fastest, least accurate)
- `base`: ~142MB (recommended balance)
- `small`: ~466MB (better accuracy)
- `medium`: ~1.5GB (high accuracy)
- `large`: ~2.9GB (best accuracy, slowest)

Models are cached in `tools/history-clip-tool/models/whisper/` and only downloaded once.

## Usage

### 1. Start the Server

```bash
python run.py
```

This starts the local server at `http://localhost:8000`

The web interface will be available at the same URL.

### 2. Create a Project

1. Open `http://localhost:8000` in your browser
2. Enter a project name (e.g., "Dark Ages Myth-Busting")
3. Upload your video file (supports mp4, mkv, mov, etc.)
4. Click "Create Project"

The tool will:
- Copy the video to `data/projects/{project_id}/source.*`
- Extract metadata (duration, resolution, fps)
- Create a database entry

### 3. Transcribe the Video

1. Click "Load Projects" to see your projects
2. Select your project from the list
3. Choose a Whisper model size (default: `base`)
4. Click "Start Transcription"

This runs in the background. Transcription time varies:
- **10-minute video** with `base` model: ~2-5 minutes
- **1-hour video** with `base` model: ~12-25 minutes

Refresh the project list to see when `Transcribed: ✓` appears.

### 4. Detect High-Value Clips

1. Set minimum score threshold (default: 30)
2. Set maximum clips to detect (default: 20)
3. Click "Detect Clips"

The scoring engine analyzes every transcript segment for:

**Evidence Markers (+points):**
- Primary source references (treaties, archives, documents)
- Date references (specific years, date ranges)
- Citation language ("according to X", "page Y")
- Quantitative data (statistics, percentages)
- Legal/technical terminology

**Argument Structure (+points):**
- Causal explanations ("consequently", "thereby", "which meant that")
- Myth-debunking patterns ("actually", "contrary to belief")
- Comparative analysis ("while in X, in Y")
- Conclusion signals ("this is why", "what this means")

**Penalties (-points):**
- Clickbait language ("SHOCKING", "SECRET")
- Emotional exaggeration
- Vague attribution ("some say", "many believe")
- Incomplete sentences

Every clip includes a full explanation of its score.

### 5. Review & Export Clips

1. Click "Load Detected Clips" to see results
2. Each clip shows:
   - Score with full reasoning
   - Timestamp and duration
   - Transcript text
   - Scoring breakdown
3. Click "Export (Academic)" for clean documentary-style captions
4. Or "Export (Shorts)" for mobile-optimized styling

Exported clips are saved to:
```
data/projects/{project_id}/exports/clip_001.mp4
```

With metadata saved alongside:
```
data/projects/{project_id}/exports/clip_001_metadata.json
```

## Configuration

### Scoring Rules

Edit `config/scoring_rules.toml` to adjust:

```toml
[evidence_markers]
primary_source_reference = 20  # Adjust point values
date_reference = 10
citation_language = 15
# ...

[penalties]
clickbait_words = -25  # Increase penalty for clickbait
# ...

[segment_quality]
optimal_duration_min = 20  # Change ideal clip length
optimal_duration_max = 90
```

Changes take effect immediately (restart server to reload).

### Caption Styles

Edit `config/caption_presets.toml` to customize:

```toml
[academic]
font = "Arial"
font_size = 24
font_color = "white"
background_color = "black"
# ...
```

Create new presets by copying existing sections.

## API Endpoints

The tool provides a REST API if you want to build custom workflows:

### Projects
- `POST /projects/` - Create project (multipart/form-data)
- `GET /projects/` - List all projects
- `GET /projects/{id}` - Get project details
- `DELETE /projects/{id}` - Delete project

### Transcription
- `POST /transcribe/{project_id}?model_size=base` - Start transcription
- `GET /transcribe/{project_id}` - Get transcript

### Clip Detection
- `POST /clips/{project_id}/detect?min_score=30&max_clips=20` - Detect clips
- `GET /clips/{project_id}` - Get detected clips
- `GET /clips/clip/{clip_id}` - Get specific clip

### Export
- `POST /export/clip/{clip_id}` - Export clip with captions
- `GET /export/clip/{clip_id}/download` - Download exported clip
- `POST /export/project/{project_id}/batch` - Batch export all clips

Full API documentation: `http://localhost:8000/docs` (when server is running)

## File Structure

```
history-clip-tool/
├── src/
│   ├── api/              # FastAPI routes
│   ├── core/             # Video processing, transcription, export
│   ├── scoring/          # Heuristic clip detection engine
│   ├── models/           # Database models
│   └── utils/            # Config, logging
├── frontend/             # Web UI
├── config/               # Scoring rules, caption presets
├── data/                 # User data (gitignored)
│   ├── projects/         # Project files
│   └── projects.db       # SQLite database
├── models/               # Downloaded Whisper models (gitignored)
├── logs/                 # Clip detection logs with reasoning
└── run.py                # Launch script
```

## How Clip Scoring Works

Unlike black-box ML systems, this tool uses **transparent heuristic rules**:

1. **Pattern Matching**: Scans text for academic language patterns (regex + keyword lists)
2. **Point Assignment**: Awards points based on configurable rules
3. **Penalty Application**: Deducts points for clickbait/vague language
4. **Duration Check**: Ensures clips are complete thoughts within optimal length
5. **Merge Nearby**: Combines adjacent high-scoring segments into coherent clips

**Every decision is logged** in `logs/clip_detection_{timestamp}.log` with full reasoning.

Example log entry:
```
CLIP SCORE: 87/100
Duration: 45.2s
Scoring reasons:
  - Contains primary source reference (+20)
  - References specific date: 1916 (+10)
  - Citation language detected: 2 instances (+15)
  - Causal explanation: 1 instances (+15)
  - Myth-debunking pattern detected (+20)
  - Complete sentence boundary (+10)
  - Optimal duration: 45.2s (+10)
```

## Limitations

### What This Tool Cannot Do:

❌ **Understand context like a human** - It detects patterns, not meaning
❌ **See visual cues** - Scoring is transcript-only (doesn't analyze B-roll)
❌ **Auto-adapt to new styles** - Patterns must be manually configured
❌ **Match viral optimization** - Optimizes for accuracy, not engagement

### What This Tool CAN Do:

✅ **Find evidence-based segments** - Reliably detects historical claims with sources
✅ **Preserve academic integrity** - Filters out clickbait and exaggeration
✅ **Run 100% offline** - No data leaves your machine
✅ **Explain every decision** - Full transparency in scoring logic
✅ **Cost $0 to operate** - No usage fees, ever

## Troubleshooting

### FFmpeg Not Found
```
FileNotFoundError: FFmpeg not found
```
**Solution:** Install FFmpeg and ensure it's in your system PATH.

### Out of Memory
```
RuntimeError: out of memory
```
**Solution:** Use a smaller Whisper model (`tiny` or `base`) or process shorter videos.

### Transcription Too Slow
**Solution:**
- Use `tiny` or `base` model
- faster-whisper is already optimized for CPU
- GPU acceleration: Change `device="cpu"` to `device="cuda"` in `src/core/transcriber.py` (requires CUDA-capable GPU)

### No Clips Detected
**Solution:**
- Lower `min_score` threshold (try 20 instead of 30)
- Check if transcript contains academic language patterns
- Review logs in `logs/` to see what scores segments received
- Adjust `config/scoring_rules.toml` if your content uses different language

### Port 8000 Already in Use
```
uvicorn.exceptions.PortInUseError
```
**Solution:** Change port in `run.py`:
```python
uvicorn.run(..., port=8001)
```

## Privacy & Security

- **No telemetry** - This tool does not phone home
- **No analytics** - No usage tracking of any kind
- **No accounts** - No login, no registration
- **Local-only server** - Binds to `127.0.0.1` (not accessible from network)
- **No cloud processing** - All inference happens on your machine
- **No data sharing** - Your videos never leave your computer

## License

This tool is built with:
- **FastAPI** (MIT License)
- **faster-whisper** (MIT License)
- **FFmpeg** (LGPL 2.1+)
- **PyTorch** (BSD License)

All dependencies use permissive open-source licenses.

## Credits

Built for the **History vs Hype** YouTube channel to create evidence-based short-form content without compromising academic standards.

**Design Philosophy:**
- Boring code > clever code
- Transparency > black-box ML
- Academic integrity > viral optimization
- Free forever > subscription model

---

**Questions or Issues?**

Check the logs in `logs/` for detailed error messages and scoring explanations.
