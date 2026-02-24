# Voice Fingerprinting Setup

## Installation

The voice fingerprinting module requires the `srt` library for parsing subtitle files.

### Install dependencies:

```bash
pip install -r tools/script_checkers/requirements.txt
```

If `srt` fails to install automatically, install it manually:

```bash
pip install srt
```

### Verify installation:

```bash
python -c "import srt; print('srt version:', srt.__version__)"
```

## Usage

### Build pattern library from existing videos:

```python
import sys
sys.path.insert(0, 'tools/script_checkers')
from pathlib import Path
from voice import build_pattern_library

patterns = build_pattern_library(
    projects_dir=Path('../../video-projects'),
    output_path=Path('voice-patterns.json')
)
print(f'Analyzed {patterns[\"metadata\"][\"videos_analyzed\"]} videos')
"
```

This will:
1. Scan `video-projects/_IN_PRODUCTION` and `_READY_TO_FILM` for script+SRT pairs
2. Compare each script to its transcript
3. Extract word-level modifications
4. Identify patterns that occur >= 3 times
5. Generate `voice-patterns.json` with:
   - Word substitutions (formal → casual)
   - Anti-patterns (consistently deleted phrases)
   - Additions (consistently added phrases)

### View pattern library:

```bash
python -c "
import json
with open('voice-patterns.json') as f:
    data = json.load(f)
    print(json.dumps(data['metadata'], indent=2))
    print(f\"\\nWord substitutions: {len(data['patterns']['word_substitutions'])}\")
    print(f\"Anti-patterns: {len(data['patterns']['anti_patterns'])}\")
"
```

## Expected Output

After analyzing 11 video pairs, you should see:

```json
{
  "metadata": {
    "generated": "2026-01-28T...",
    "videos_analyzed": 11,
    "video_list": ["1-somaliland-2025", "3-fuentes-fact-check-2025", ...],
    "confidence_note": "Patterns from 11 videos - good corpus size for reliable patterns"
  },
  "patterns": {
    "word_substitutions": [
      {"formal": "utilize", "casual": "use", "frequency": 7, "confidence": "HIGH"}
    ],
    "anti_patterns": ["it should be noted that", "in order to"],
    "additions": ["actually", "here is the thing"]
  }
}
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'srt'"

Install the srt library:
```bash
pip install srt
```

### "Warning: Only X video pairs found"

The pattern extractor needs minimum 5 video pairs for statistical significance.
Check that you have SCRIPT.md + *.srt in your video project folders.

### "Insufficient corpus for pattern detection"

This means modifications across videos are too context-specific (no patterns >= 3 frequency).
This is valid - user's edits may be highly contextual rather than systematic.

## Next Steps

After generating voice-patterns.json:
- Phase 12 Plan 02 will integrate patterns into scriptwriter
- Patterns will be automatically applied during script generation
- Optional `--show-voice-changes` flag will show where patterns were applied
