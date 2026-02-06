# YouTube Transcript Setup & Workflow

**Created:** 2025-01-16
**Purpose:** Extract claims from YouTube videos for fact-checking

---

## WHAT WE SET UP

### 1. ✅ Created `.mcp.json`
Remote YouTube MCP server configuration (may require Claude Desktop instead of Claude Code)

### 2. ✅ Created `/extract-claims` Command
Slash command to extract factual claims from video transcripts

**Usage:**
```
/extract-claims
```

Then provide the YouTube URL and transcript.

---

## RECOMMENDED: Python Script (NEW)

**File:** `get-transcript.py` in project root

### Setup (One Time)
```bash
pip install youtube-transcript-api
```

### Usage
```bash
# From any YouTube URL format
python get-transcript.py https://www.youtube.com/watch?v=6aFkoX6g1fE
python get-transcript.py "https://youtu.be/6aFkoX6g1fE"
python get-transcript.py 6aFkoX6g1fE

# Options
python get-transcript.py [URL] --no-timestamps    # Plain text, no timestamps
python get-transcript.py [URL] --no-save          # Print only, don't save file
```

### What It Does
1. Extracts video ID from any YouTube URL format
2. Fetches transcript (prefers manual captions, falls back to auto-generated)
3. Saves to `transcripts/[video-title].txt` with metadata header
4. Prints transcript to console for quick copy/paste
5. Shows word count and duration summary

### Output Format
```
# Video Title Here
# Video ID: 6aFkoX6g1fE
# URL: https://www.youtube.com/watch?v=6aFkoX6g1fE
# Transcript source: auto-generated
# ---

[0:00] First line of transcript
[0:05] Second line continues...
```

**Time:** ~5 seconds per video

---

## FALLBACK: Manual Transcript Extraction

### Method 1: YouTube's Built-In Feature (FREE)
1. Open video on YouTube
2. Click "..." (three dots) below video
3. Select "Show transcript"
4. Click three dots in transcript panel → "Toggle timestamps" (off)
5. Copy all text
6. Paste into conversation or save as `.txt` file

**Time:** ~30 seconds per video

---

### Method 2: Browser Extension (FASTER)
Install **YouTube Transcript** extension:
- Chrome: https://chrome.google.com/webstore (search "YouTube Transcript")
- Firefox: https://addons.mozilla.org (search "YouTube Transcript")

**Features:**
- One-click download
- Includes timestamps
- Multiple format options

**Time:** ~5 seconds per video

---

### Method 3: yt-dlp Command-Line (BULK)
If you need many transcripts:

```bash
# Install yt-dlp
pip install yt-dlp

# Download transcript only
yt-dlp --write-auto-sub --skip-download [VIDEO_URL]

# Or specify language
yt-dlp --write-auto-sub --sub-lang en --skip-download [VIDEO_URL]
```

**Outputs:** `.vtt` or `.srt` file with timestamps

---

## RECOMMENDED WORKFLOW

### For Single Videos (Your Current Use Case):

**Option A: Use Browser Extension** (Recommended)
1. Install YouTube Transcript extension
2. Watch video you want to fact-check
3. Click extension icon → Download transcript
4. Save as `[video-name]-transcript.txt`
5. Run `/extract-claims`
6. Paste transcript when prompted
7. Get organized CLAIMS-TO-VERIFY.md

**Time:** ~2 minutes total

---

**Option B: Manual Copy/Paste**
1. Open YouTube video
2. Show transcript → Copy
3. Run `/extract-claims`
4. Paste transcript
5. Get CLAIMS-TO-VERIFY.md

**Time:** ~3 minutes total

---

### For Multiple Videos (Batch Processing):

1. Create `transcripts/` folder in project
2. Use yt-dlp to download all transcripts:
   ```bash
   yt-dlp --write-auto-sub --skip-download \
     --output "transcripts/%(title)s.%(ext)s" \
     [URL1] [URL2] [URL3]
   ```
3. For each transcript:
   - Run `/extract-claims`
   - Reference transcript file
   - Get CLAIMS-TO-VERIFY.md

---

## EXAMPLE USAGE

### Pax Tube Crusades Video:

**Step 1:** Get transcript
```
Method: YouTube's "Show transcript" feature
URL: https://youtube.com/watch?v=6aFkoX6g1fE
Action: Copy transcript to clipboard
```

**Step 2:** Extract claims
```
/extract-claims
[Paste transcript]
```

**Step 3:** Review output
```
File created: CLAIMS-TO-VERIFY.md
- Priority 1: 5 major claims
- Priority 2: 12 supporting claims
- Priority 3: 8 minor details
Total: 25 claims to fact-check
```

**Step 4:** Begin fact-checking
```
Open CLAIMS-TO-VERIFY.md
Start with Priority 1 claims
Use NotebookLM for verification
```

---

## FUTURE ENHANCEMENT OPTIONS

### Option 1: MCP Server (If Using Claude Desktop)
The `.mcp.json` file is ready. If you switch to Claude Desktop:
1. Restart Claude Desktop
2. Approve the YouTube MCP server
3. You'll be able to say: "Get transcript from [URL]"
4. Automatic fetching will work

### Option 2: YouTube Data API
If you get a YouTube API key:
- 10,000 free requests/day
- Can fetch video metadata + captions
- Requires API key setup

### Option 3: Python Script ✅ DONE
Created `get-transcript.py` - see "RECOMMENDED: Python Script" section above.

---

## WHAT'S WORKING NOW

✅ `/extract-claims` command created
✅ Structured claim extraction template
✅ Clear output format (CLAIMS-TO-VERIFY.md)
✅ Manual workflow documented
✅ **`get-transcript.py` script** - automatic transcript extraction

⏳ MCP server (requires Claude Desktop)

---

## NEXT STEPS

**For Your Next Video:**
1. Run: `python get-transcript.py [YouTube URL]`
2. Transcript auto-saves to `transcripts/`
3. Run: `/extract-claims`
4. Reference the saved transcript file
5. Review extracted claims
6. Begin fact-checking with NotebookLM

**Estimated time:** ~2 minutes total (vs 15-20 minutes manual)

---

## SUMMARY

**Goal:** Extract YouTube video claims for fact-checking
**Challenge:** YouTube blocks automatic scraping
**Solution:** Manual transcript + automated claim extraction
**Result:** Structured fact-checking workflow

**You now have:** A systematic way to extract and organize factual claims from any YouTube video for verification.
