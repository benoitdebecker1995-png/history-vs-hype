# Architecture Documentation

## System Overview

The History Clip Tool is a local-only video clipping system designed to extract high-value segments from educational historical videos. Unlike commercial tools (OpusClips, Clippah), this system prioritizes academic integrity over viral engagement.

### Core Principles

1. **No External Dependencies** - Runs entirely on user's machine
2. **Explainable Decisions** - Every clip score includes full reasoning
3. **Zero Runtime Cost** - No API calls, no subscriptions
4. **Academic Optimization** - Detects evidence-based content, penalizes clickbait
5. **Transparent Logic** - Heuristic rules, not black-box ML

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      WEB INTERFACE                           │
│              (FastAPI + HTML/JS Frontend)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   CORE PIPELINE                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Video      │  │  Clip        │  │   Export     │      │
│  │   Ingestion  ├─►│  Detection   ├─►│   Assembly   │      │
│  │   + Whisper  │  │  & Scoring   │  │   (FFmpeg)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               LOCAL DATA LAYER                               │
│  • SQLite (projects, clips, scores)                         │
│  • File system (videos, transcripts, exports)               │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Video Ingestion

**Input:** User uploads video file (MP4, MKV, MOV, etc.)

**Process:**
```
1. Generate unique project ID (UUID)
2. Create project directory: data/projects/{uuid}/
3. Copy video file to: data/projects/{uuid}/source.{ext}
4. Extract metadata with FFprobe:
   - Duration
   - FPS
   - Resolution
5. Create database entry (SQLite)
```

**Output:** Project record in database, video file stored locally

**Key Files:**
- `src/core/video_processor.py` - FFmpeg wrapper
- `src/api/routes/projects.py` - API endpoint
- `src/models/database.py` - Database schema

### 2. Audio Transcription

**Input:** Source video file

**Process:**
```
1. Extract audio track with FFmpeg:
   - Convert to WAV (16kHz mono, 16-bit PCM)
   - Optimal format for Whisper
   - Saved to: data/projects/{uuid}/audio.wav

2. Run faster-whisper transcription:
   - Model: tiny/base/small/medium/large (user choice)
   - Device: CPU (default) or CUDA
   - Compute type: int8 (quantized for speed)
   - VAD filter: enabled (removes silence)
   - Word timestamps: enabled (precise boundaries)

3. Save transcript:
   - Format: JSON
   - Contains: segments with start/end times, text, words
   - Location: data/projects/{uuid}/transcript.json
```

**Output:** Transcript JSON with word-level timestamps

**Key Files:**
- `src/core/transcriber.py` - faster-whisper wrapper
- `src/api/routes/transcribe.py` - API endpoint

**Performance:**
- 10-minute video: ~2-5 minutes (base model, CPU)
- 1-hour video: ~12-25 minutes (base model, CPU)

### 3. Clip Detection & Scoring

**Input:** Transcript JSON

**Process:**

#### A. Segment Analysis

For each transcript segment (sentence-level):

```python
score = 0
reasons = []

# Evidence markers (academic language)
if contains_primary_source_keywords(text):
    score += 20
    reasons.append("Contains primary source reference (+20)")

if contains_date_references(text):
    score += 10
    reasons.append("References specific date (+10)")

if contains_citation_language(text):
    score += 15
    reasons.append("Citation language detected (+15)")

if contains_quantitative_data(text):
    score += 15
    reasons.append("Quantitative data (+15)")

if contains_legal_keywords(text):
    score += 10
    reasons.append("Legal/technical terminology (+10)")

# Argument structure
if contains_causal_language(text):
    score += 15
    reasons.append("Causal explanation (+15)")

if contains_debunk_patterns(text):
    score += 20
    reasons.append("Myth-debunking pattern (+20)")

if contains_comparison(text):
    score += 10
    reasons.append("Comparative analysis (+10)")

if contains_conclusion_signal(text):
    score += 10
    reasons.append("Conclusion signal (+10)")

# Completeness
if is_complete_sentence(text):
    score += 10
    reasons.append("Complete sentence (+10)")
else:
    score -= 20
    reasons.append("Incomplete thought (-20)")

# Penalties
clickbait_count = count_clickbait_words(text)
if clickbait_count > 0:
    score -= 25
    reasons.append(f"Clickbait language ({clickbait_count} instances) (-25)")

# Duration check
if duration < min_viable:
    score = 0  # Hard reject
elif optimal_min <= duration <= optimal_max:
    score += 10
    reasons.append("Optimal duration (+10)")

# Normalize to 0-100
final_score = clamp(score, 0, 100)
```

#### B. Pattern Matching

All patterns are regex-based and documented:

**Primary Source Keywords:**
```python
["treaty", "census", "archival", "manuscript", "document",
 "court", "ruling", "statute", "proclamation", ...]
```

**Citation Patterns:**
```regex
r"\baccording to\b"
r"\bpage\s+\d+"
r"\bin\s+[A-Z][a-z]+(?:'s)?\s+(?:book|study|work)"
```

**Date Patterns:**
```regex
r"\b\d{3,4}\s*(?:CE|BCE|AD|BC)\b"
r"\b(?:1|2)\d{3}\b"
```

**Clickbait Detection:**
```python
["SHOCKING", "SECRET", "HIDDEN", "you won't believe", ...]
```

#### C. Nearby Segment Merging

After scoring, merge adjacent high-scoring segments:

```python
def merge_nearby_clips(clips, max_gap=2.0):
    # Sort by time
    sorted_clips = sorted(clips, key=lambda x: x['start_time'])

    merged = []
    current = sorted_clips[0]

    for next_clip in sorted_clips[1:]:
        gap = next_clip['start_time'] - current['end_time']

        if gap <= max_gap:
            # Merge: extend current clip
            current['end_time'] = next_clip['end_time']
            current['text'] += " " + next_clip['text']
            current['reasons'].extend(next_clip['reasons'])
            current['score'] = (current['score'] + next_clip['score']) / 2
        else:
            # Save current, start new
            merged.append(current)
            current = next_clip

    merged.append(current)
    return merged
```

**Output:** Top N clips with scores and reasoning

**Key Files:**
- `src/scoring/patterns.py` - Pattern definitions
- `src/scoring/rules.py` - Scoring engine
- `src/core/clip_detector.py` - Orchestrator
- `config/scoring_rules.toml` - Configurable weights

### 4. Video Export

**Input:** Clip data (start time, end time, text)

**Process:**

#### A. Extract Video Segment

```python
# Use FFmpeg to extract clip
ffmpeg.input(source_video, ss=start_time, t=duration) \
      .output(temp_clip, vcodec='libx264', ...) \
      .run()
```

#### B. Crop to 9:16 Vertical

```python
# Calculate crop dimensions
target_aspect = 9 / 16
if source_width / source_height > target_aspect:
    # Crop width (landscape to portrait)
    crop_width = height * target_aspect
    x_offset = (width - crop_width) // 2  # Center
else:
    # Crop height (already portrait or square)
    crop_height = width / target_aspect
    y_offset = (height - crop_height) // 2

# Apply crop filter
stream = input_stream.video.crop(x_offset, y_offset, crop_width, crop_height)
```

#### C. Generate Subtitles

```python
# Create SRT file
wrapped_lines = textwrap.wrap(text, width=max_chars_per_line)
for i, line in enumerate(wrapped_lines):
    start_time = i * (duration / num_lines)
    end_time = (i + 1) * (duration / num_lines)

    srt_content += f"{i+1}\n"
    srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
    srt_content += f"{line}\n\n"
```

#### D. Burn Subtitles

```python
# Use FFmpeg subtitles filter
ffmpeg.input(temp_clip) \
      .video.filter('subtitles', srt_path) \
      .output(final_clip, vcodec='libx264', acodec='aac', ...) \
      .run()
```

**Output:** MP4 file (9:16, H.264, burned captions)

**Saved to:** `data/projects/{uuid}/exports/clip_{id}.mp4`

**Key Files:**
- `src/core/video_processor.py` - Video extraction & cropping
- `src/core/caption_renderer.py` - Subtitle generation
- `src/core/exporter.py` - Export orchestrator
- `config/caption_presets.toml` - Style configuration

## Database Schema

```sql
-- Projects table
CREATE TABLE projects (
    id TEXT PRIMARY KEY,           -- UUID
    name TEXT NOT NULL,
    source_video_path TEXT NOT NULL,
    duration REAL,
    fps REAL,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transcribed BOOLEAN DEFAULT FALSE,
    clips_detected BOOLEAN DEFAULT FALSE
);

-- Clips table
CREATE TABLE clips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    start_time REAL NOT NULL,
    end_time REAL NOT NULL,
    duration REAL NOT NULL,
    transcript_text TEXT NOT NULL,
    score REAL NOT NULL,
    score_reasons TEXT,           -- JSON array of reasons
    exported BOOLEAN DEFAULT FALSE,
    export_path TEXT,
    caption_preset TEXT DEFAULT 'academic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

## API Endpoints

### Projects

**POST /projects/?name={name}**
- Upload video file
- Create project
- Returns: ProjectResponse

**GET /projects/**
- List all projects
- Returns: List[ProjectResponse]

**GET /projects/{id}**
- Get project details
- Returns: ProjectResponse

**DELETE /projects/{id}**
- Delete project and all files
- Returns: Success message

### Transcription

**POST /transcribe/{project_id}?model_size=base**
- Start background transcription task
- Returns: Status message

**GET /transcribe/{project_id}**
- Get transcription results
- Returns: TranscriptionResponse

### Clip Detection

**POST /clips/{project_id}/detect?min_score=30&max_clips=20**
- Detect high-value clips
- Saves to database
- Returns: List[DetectedClipResponse]

**GET /clips/{project_id}**
- Get all clips for project
- Returns: List[ClipResponse]

**GET /clips/clip/{clip_id}**
- Get specific clip
- Returns: ClipResponse

**DELETE /clips/clip/{clip_id}**
- Delete clip
- Returns: Success message

### Export

**POST /export/clip/{clip_id}**
- Export clip with captions
- Body: ClipExportRequest (caption_preset, crop_mode)
- Returns: Export result

**GET /export/clip/{clip_id}/download**
- Download exported video
- Returns: FileResponse (MP4)

**POST /export/project/{project_id}/batch**
- Batch export all clips
- Returns: Batch export summary

## Configuration System

### Scoring Rules (TOML)

`config/scoring_rules.toml`

```toml
[evidence_markers]
primary_source_reference = 20
date_reference = 10
citation_language = 15
quantitative_data = 15
legal_language = 10

[argument_structure]
causal_explanation = 15
myth_debunk_pattern = 20
comparison = 10
conclusion_signal = 10

[penalties]
clickbait_words = -25
emotional_exaggeration = -15
vague_attribution = -10
incomplete_thought = -20

[segment_quality]
optimal_duration_min = 20
optimal_duration_max = 90
min_viable_duration = 15
max_silence_gap = 2.0

[weights]
evidence_weight = 0.40
argument_weight = 0.35
completeness_weight = 0.25
```

### Caption Presets (TOML)

`config/caption_presets.toml`

```toml
[academic]
font = "Arial"
font_size = 24
font_color = "white"
background_color = "black"
background_opacity = 0.7
position = "bottom"
margin = 50
max_chars_per_line = 42
all_caps = false
emojis = false
```

## Performance Characteristics

### Transcription Speed

| Model Size | Accuracy | Speed (10min video) | Memory |
|-----------|----------|---------------------|--------|
| tiny      | Low      | ~1-2 min            | ~1GB   |
| base      | Good     | ~2-5 min            | ~1GB   |
| small     | Better   | ~4-8 min            | ~2GB   |
| medium    | High     | ~8-15 min           | ~5GB   |
| large     | Best     | ~15-30 min          | ~10GB  |

### Clip Detection Speed

- **1-hour transcript**: ~5-10 seconds
- **Bottleneck**: Pattern matching (pure Python)
- **Optimization**: Compiled regex patterns

### Export Speed

- **30-second clip**: ~10-20 seconds
  - Extract: 5s
  - Crop: 3s
  - Subtitle burn: 5s
- **Bottleneck**: FFmpeg encoding (H.264)

## Security & Privacy

### Local-Only Design

- Server binds to `127.0.0.1` (localhost only)
- No external network access required
- No telemetry or analytics
- No user accounts

### Data Storage

- All data in `data/` directory (gitignored)
- SQLite database (local file)
- No cloud backups

### No Third-Party Services

- Transcription: local faster-whisper
- Video processing: local FFmpeg
- Scoring: local heuristics (no API calls)

## Extensibility

### Adding New Scoring Patterns

1. Add pattern to `src/scoring/patterns.py`:
```python
NEW_PATTERN = [r"\bnew_keyword\b", ...]
NEW_COMPILED = compile_patterns(NEW_PATTERN)
```

2. Add scoring logic to `src/scoring/rules.py`:
```python
if count_pattern_matches(text, patterns.NEW_COMPILED) > 0:
    score += 15
    reasons.append("New pattern detected (+15)")
```

3. Add config entry to `config/scoring_rules.toml`:
```toml
[new_category]
new_pattern = 15
```

### Adding Caption Styles

Edit `config/caption_presets.toml`:

```toml
[my_custom_style]
font = "Comic Sans MS"  # (please don't)
font_size = 28
font_color = "yellow"
# ...
```

Use in export:
```python
POST /export/clip/{id}
Body: {"caption_preset": "my_custom_style"}
```

## Testing Strategy

### Unit Tests

- Pattern matching (regex correctness)
- Scoring logic (point calculations)
- Duration validation
- Merge logic

### Integration Tests

- End-to-end pipeline
- FFmpeg operations
- Database operations

### Manual Testing

- Upload various video formats
- Test different Whisper models
- Verify exported clip quality
- Check scoring accuracy on real transcripts

## Future Enhancements (Out of Scope for MVP)

1. **Face Tracking** - OpenCV-based intelligent crop
2. **GPU Acceleration** - CUDA support for faster transcription
3. **Batch Processing** - Queue multiple videos
4. **React Frontend** - Rich UI with timeline visualization
5. **Advanced Filters** - Audio normalization, color grading
6. **Multi-Language** - Support non-English content
7. **Export Formats** - Additional aspect ratios (1:1, 16:9)

## Dependencies & Licenses

| Dependency | Version | License | Purpose |
|-----------|---------|---------|---------|
| FastAPI | 0.109.0 | MIT | Web framework |
| faster-whisper | 1.0.0 | MIT | Transcription |
| ffmpeg-python | 0.2.0 | Apache 2.0 | Video processing wrapper |
| SQLAlchemy | 2.0.25 | MIT | Database ORM |
| PyTorch | 2.1.2 | BSD | ML backend for Whisper |
| uvicorn | 0.27.0 | BSD | ASGI server |

All dependencies use permissive open-source licenses (no GPL/AGPL).

## Known Limitations

### Technical

- **CPU-bound transcription** - No GPU acceleration in MVP
- **Single-threaded export** - One clip at a time
- **No video preview** - Must export to see result
- **Simple crop** - Center-crop only (no face tracking)

### Functional

- **Pattern-based scoring** - Not context-aware like human
- **English-only** - Patterns assume English text
- **No undo** - Once exported, must re-export to change
- **No A/B testing** - Can't compare caption styles side-by-side

### By Design

- **No viral optimization** - Intentionally prioritizes accuracy
- **No engagement metrics** - No analytics on clip performance
- **Manual review required** - Scores are suggestions, not gospel

---

**Last Updated:** 2025-01-07
