# Quick Start Guide

Get the History Clip Tool running in 5 minutes.

## Prerequisites

1. **Python 3.10+** installed
2. **FFmpeg** installed (see README.md for instructions)

## Installation

```bash
# Navigate to the tool directory
cd tools/history-clip-tool

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## First Run

```bash
# Start the server
python run.py
```

You should see:
```
================================================================================
History Clip Tool
================================================================================
Local-only video clipping for evidence-based historical content

Starting server at: http://localhost:8000
Press Ctrl+C to stop
================================================================================
```

Open `http://localhost:8000` in your browser.

## Basic Workflow

### 1. Create Project
- Enter project name: "Test Video"
- Upload a video file (MP4, MKV, MOV, etc.)
- Click "Create Project"

### 2. Transcribe
- Click "Load Projects"
- Select your project
- Choose model size (start with "Base")
- Click "Start Transcription"
- **Wait 2-5 minutes** for 10-min video

### 3. Detect Clips
- Set min score: 30 (default)
- Set max clips: 20 (default)
- Click "Detect Clips"
- Review the results (each clip shows its score and reasoning)

### 4. Export
- Click "Export (Academic)" on any clip
- Find the exported video in:
  ```
  data/projects/{project-id}/exports/clip_001.mp4
  ```

## Tips for Best Results

### For Historical Content

Your videos should ideally contain:
- ✅ Specific dates and time periods
- ✅ Primary source references (treaties, documents, archives)
- ✅ Citations ("according to historian X", "page Y")
- ✅ Statistics and quantitative data
- ✅ Causal explanations ("consequently", "this led to")
- ✅ Myth-debunking language ("actually", "contrary to belief")

### Adjusting Sensitivity

**If you get too few clips:**
- Lower min_score to 20 or 25
- Increase max_clips to 30+
- Check `logs/` to see what scores your content received

**If you get too many low-quality clips:**
- Raise min_score to 40 or 50
- Edit `config/scoring_rules.toml` to increase evidence marker weights

### Model Selection

| Model | When to Use |
|-------|-------------|
| **tiny** | Very fast testing, low accuracy acceptable |
| **base** | **Recommended** - Good balance |
| **small** | Better accuracy, still reasonably fast |
| **medium** | High accuracy, slower (1-hour video = ~30 min) |
| **large** | Best accuracy, very slow (not recommended for MVP) |

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg:
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### "Out of memory"
Use a smaller Whisper model (tiny or base).

### "No clips detected"
- Lower the min_score threshold
- Check if your video contains academic language patterns
- Review the log file in `logs/` to see segment scores

### "Port 8000 already in use"
Change the port in `run.py`:
```python
uvicorn.run(..., port=8001)
```

## What's Next?

- **Customize scoring:** Edit `config/scoring_rules.toml`
- **Add caption styles:** Edit `config/caption_presets.toml`
- **Review logs:** Check `logs/` for detailed scoring explanations
- **Read full docs:** See `README.md` and `ARCHITECTURE.md`

## Common Questions

**Q: Can I use GPU acceleration?**
A: Yes. Edit `src/core/transcriber.py` and change `device="cpu"` to `device="cuda"` (requires CUDA-capable GPU).

**Q: Can I process multiple videos at once?**
A: Not in MVP. Transcription is sequential. You can create multiple projects and queue them manually.

**Q: Why are my clip scores different from what I expected?**
A: Check `logs/clip_detection_*.log` to see the exact reasoning. You can adjust weights in `config/scoring_rules.toml`.

**Q: Can I edit clips after export?**
A: No automatic editing. You can manually trim the timestamps and re-export, or edit the MP4 in video editing software.

**Q: Is this really free forever?**
A: Yes. Zero runtime costs. All processing is local. No subscriptions, ever.

---

**Need help?** Check the logs in `logs/` for detailed error messages.
