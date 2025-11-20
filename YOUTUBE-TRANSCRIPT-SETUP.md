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

## CURRENT LIMITATION

**YouTube blocks direct web scraping** - Claude Code cannot automatically fetch transcripts from YouTube URLs.

---

## WORKAROUND: Manual Transcript Extraction

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

### Option 3: Python Script
Create a local Python script that:
1. Takes YouTube URL
2. Uses `youtube-transcript-api` library
3. Outputs clean transcript
4. Calls `/extract-claims` automatically

---

## WHAT'S WORKING NOW

✅ `/extract-claims` command created
✅ Structured claim extraction template
✅ Clear output format (CLAIMS-TO-VERIFY.md)
✅ Manual workflow documented

⏳ Automatic YouTube fetching (blocked by YouTube)
⏳ MCP server (requires Claude Desktop)

---

## NEXT STEPS

**For Your Next Video:**
1. Watch the video you want to fact-check
2. Get transcript (30 seconds with extension)
3. Run: `/extract-claims`
4. Paste transcript
5. Review extracted claims
6. Begin fact-checking with NotebookLM

**Estimated time savings:** 15-20 minutes per video (vs manual claim extraction)

---

## SUMMARY

**Goal:** Extract YouTube video claims for fact-checking
**Challenge:** YouTube blocks automatic scraping
**Solution:** Manual transcript + automated claim extraction
**Result:** Structured fact-checking workflow

**You now have:** A systematic way to extract and organize factual claims from any YouTube video for verification.
