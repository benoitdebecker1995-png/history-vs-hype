---
description: Mine YouTube competitor comments to measure audience demand for thesis angles
model: opus
---

# /comment-mine — YouTube Comment Mining

Mine competitor YouTube videos to surface which thesis angle has the most unmet audience demand. Use this BEFORE locking angle/thesis, after brainstorming ≥2 candidate angles.

> **You already have a topic and ≥2 angles?** This command. **You have neither, and want candidates
> generated from unprompted demand?** That's the inversion — sweep the whole tracked competitor set
> instead of one topic:
> ```
> python -m tools.discovery.gap_hunter --sweep --digest
> ```
> It stores tagged signals in `intel.db.comment_signals` and regenerates
> `channel-data/gap-hunter/HARVEST-DIGEST.md`. Spec: `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` §5.

## Usage

```
/comment-mine                        # Interactive: asks for video IDs and angles
/comment-mine --videos ID1,ID2,ID3   # Mine specific video IDs
/comment-mine --topic "X"            # Auto-find top 3 competitor videos on topic
```

---

## CRITICAL: Use yt-dlp, NOT WebFetch or Playwright

**WebFetch cannot access YouTube comments** (JavaScript-rendered, login-gated).
**Playwright agents for comment scraping are slow, unreliable, and hit rate limits.**

**Always use the yt-dlp route below.** It's fast (seconds), offline-safe, and returns structured JSON.

---

## Step 1: Find Competitor Videos

If video IDs are not provided, search for them:

```python
# WebSearch for top YouTube results on topic
# Extract video IDs from URLs (11-char alphanumeric after /watch?v= or youtu.be/)
# Target: 2-4 videos with 50K+ views covering the same topic space
# Prefer: revisionist angle, sensationalist angle, BBC/documentary angle
# Avoid: your own channel
```

Record each video as: `VIDEO_ID — "Title" (view count)`

---

## Step 2: Download Comments via yt-dlp

**Output directory:** `[project-folder]/_research/comment-mining/`

Create the directory first, then run for each video:

```powershell
# Change to project comment-mining folder first
cd "G:\History vs Hype\video-projects\_IN_PRODUCTION\[project-folder]\_research\comment-mining"

yt-dlp `
  --skip-download `
  --write-comments `
  --write-info-json `
  --extractor-args "youtube:max_comments=50" `
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Flags explained:**
- `--skip-download` — no video file, metadata only
- `--write-comments` — fetches comments into the JSON
- `--write-info-json` — writes `VIDEO_ID.info.json`
- `--extractor-args "youtube:max_comments=50"` — caps at 50 comments (NOT `--max-comments`, which doesn't exist)

**Output:** `VIDEO_ID.info.json` in the current directory.

Run all videos in sequence (not parallel — avoids rate limiting):

```powershell
$videos = @("ID1", "ID2", "ID3")
foreach ($id in $videos) {
    yt-dlp --skip-download --write-comments --write-info-json `
      --extractor-args "youtube:max_comments=50" `
      "https://www.youtube.com/watch?v=$id"
    Start-Sleep -Seconds 2
}
```

---

## Step 3: Extract Comments to Text File

**MANDATORY: Use `encoding='utf-8', errors='replace'`** — YouTube comments contain emoji and non-ASCII characters that will crash `cp1252` (Windows default) with `UnicodeDecodeError`. Also use `errors='replace'` on print/write to handle output encoding.

```python
import json

videos = [
    ("VIDEO_ID_1", "VIEW_COUNT — Title of Video 1"),
    ("VIDEO_ID_2", "VIEW_COUNT — Title of Video 2"),
    ("VIDEO_ID_3", "VIEW_COUNT — Title of Video 3"),
]

output = []
for vid_id, label in videos:
    try:
        with open(f"{vid_id}.info.json", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        comments = data.get("comments", [])
        output.append(f"\n=== {label} ({vid_id}) ===")
        output.append(f"Total comments in file: {len(comments)}")
        for i, c in enumerate(comments[:50]):
            text = c.get("text", "").replace("\n", " ")[:300]
            likes = c.get("like_count", 0)
            output.append(f"  [{i+1}] ({likes} likes) {text}")
    except Exception as e:
        output.append(f"ERROR on {vid_id}: {e}")

result = "\n".join(output)
with open("comments-extracted.txt", "w", encoding="utf-8") as f:
    f.write(result)
print(f"Done. {len(output)} lines, {len(result)} chars → comments-extracted.txt")
```

Save as `extract_comments.py` in the comment-mining folder and run:
```powershell
python extract_comments.py
```

---

## Step 4: Categorize by Angle Signal

Read `comments-extracted.txt` and scan for comments that signal demand for each thesis angle.

**Angle signal = a comment that:**
- Asks a question your angle answers
- Expresses frustration that existing videos don't address X
- Names a specific claim/mechanism that your angle covers
- Engages with the exact hook your angle uses
- Points to a gap ("nobody talks about...")

**NOT a signal:** Monty Python jokes, religious/political rants, off-topic arguments.

For each signal comment, note: `V[video_number][comment_number]: quote — relevance to angle`

---

## Step 5: Count and Decide

Build a signal table:

| Angle | Signals | Notes |
|-------|---------|-------|
| A — [name] | N | keyword fit, format fit |
| B — [name] | N | originality gap |
| C — [name] | N | formula repeat risk? |

**Decision rule:**
1. Angle with most signals wins — IF no disqualifying risk
2. Near-tie (≤2 signal difference): apply tiebreakers in order:
   - Keyword fit (does the angle serve the primary keyword?)
   - Format fit (does it work with Format C / talking head + B-roll?)
   - Channel formula repeat risk (did we recently do the same framing?)
3. Angle with zero signals but high originality: treat as gap opportunity, not winner — flag for user decision

**Output:**
```
ANGLE LOCKED: [A/B/C] — [name]
Signals: A=[n], B=[n], C=[n]
Key signal: "[most compelling comment quote]"
Reasoning: [1-2 sentences]
```

---

## Step 6: Update Project Files

After angle is locked:

1. **`01-VERIFIED-RESEARCH.md`** — Add "Angle decision — LOCKED" section with signal counts and key insight
2. **Memory file** (`~/.claude/projects/D--History-vs-Hype/memory/[video]-production-state.md`) — Update status, add locked angle and thesis
3. **`MEMORY.md`** — Update production state entry to reflect angle locked

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `UnicodeDecodeError` reading JSON | Add `errors='replace'` to `open()` — `open(file, encoding='utf-8', errors='replace')` |
| `UnicodeEncodeError` printing output | Write to file with `encoding='utf-8'` instead of printing to stdout |
| `--max-comments` not recognized | Use `--extractor-args "youtube:max_comments=50"` instead |
| JSON has 0 comments | Video may have comments disabled, or yt-dlp version is old — try `pip install -U yt-dlp` |
| Rate limited | Add `Start-Sleep -Seconds 3` between videos |
| `comments` key missing from JSON | Some yt-dlp versions need `--write-comments` explicitly; confirm it's in the command |

---

## File Artifacts

After running, the comment-mining folder contains:
- `VIDEO_ID.info.json` — raw yt-dlp output (keep; source of truth)
- `comments-extracted.txt` — human-readable comment dump
- `extract_comments.py` — reusable extraction script

These stay in `_research/comment-mining/` and are NOT committed unless user asks.
