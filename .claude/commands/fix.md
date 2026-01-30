---
description: Fix subtitle errors from auto-transcription (Post-production Phase 2)
model: haiku
---

# /fix - Subtitle Correction

Fix common subtitle (.srt) errors from auto-transcription. Focused single-purpose command.

## Usage

```
/fix                         # Auto-find SRT in current project
/fix [project]               # Fix subtitles for specific project
/fix [file.srt]              # Fix specific SRT file
```

---

## CRITICAL RULE: NEVER CHANGE WORDS

**ONLY fix spelling/transcription errors. NEVER change the actual words spoken.**

Examples:
- CORRECT: "demi-tax" → "dhimmi tax" (same words, fixed spelling)
- WRONG: "demi-tax" → "jizya" (different word entirely)
- CORRECT: "Godwills it" → "God wills it" (spacing fix)
- WRONG: Changing any phrasing or word choice

**The subtitle must match what was actually said in the video, word-for-word.**

---

## Common Issues in Auto-Generated Subtitles

### 1. Timestamp Errors

**Problem:** Timestamps start at 01:00:00 instead of 00:00:00 (1 hour offset)

**Fix:** Replace all `01:0` with `00:0`

### 2. Name Misspellings

Common auto-transcription errors in historical names:

| Wrong | Correct |
|-------|---------|
| McMehan | McMahon |
| Rochhild | Rothschild |
| Francois-Jacques-Picot | Francois Georges-Picot |
| even South | Ibn Saud |
| Ataturk | Ataturk |

### 3. Treaty/Place Names

| Wrong | Correct |
|-------|---------|
| Seyver | Sevres |
| Lausan | Lausanne |
| Nasht | Najd |
| Sun Remo | San Remo |
| Sykes-Bikko | Sykes-Picot |

### 4. Date Errors

- Check dates against script for accuracy
- Common: October 23 vs. October 24 (verify from script)

---

## Fixing Process

### Step 1: Find the Subtitle File

```
Use Glob: video-projects/**/*.srt
Usually in: video-projects/_READY_TO_FILM/[project]/
```

### Step 2: Read and Identify Errors

- Note all name misspellings
- Check timestamp format (01: vs 00:)
- Verify dates against script

### Step 3: Fix Systematically

1. **Timestamp offset:** Use replace_all for 01:0 → 00:0
2. **Name errors:** Fix each misspelling individually
3. **Treaty names:** Check historical accuracy
4. **Verify:** Read corrected sections to confirm

### Step 4: Common Replacement Patterns

```
Replace all: 01:0 → 00:0
Replace all: Sykes-Bikko → Sykes-Picot
Replace all: Seyver → Sevres
Individual: McMehan → McMahon (check context)
```

---

## Output

After fixing, report:
- Number of timestamp corrections
- List of name corrections
- Any date fixes
- File is ready for upload

---

## BONUS: Extract Chapter Timestamps

**If asked to update YouTube metadata, extract chapter timestamps from SRT files.**

### Process

1. Read the SRT file
2. Note timestamp offset (often starts at 01:00:00)
3. Identify topic transitions by reading content
4. Convert SRT timestamps to video timestamps (subtract offset)
5. Create chapter list for YOUTUBE-METADATA.md

### Example

```
SRT shows: 01:05:02 → "The Carolingians provided the ambition"
Actual video timestamp: 5:02 (subtract 1 hour offset)
Chapter: "5:02 - Charlemagne's cultural revolution"
```

**This saves manual chapter timestamp creation during editing.**

---

## User Preferences

**Be efficient:**
- Don't ask "what file?" - find it with Glob
- Don't ask "what to fix?" - read and identify errors
- Just do the fixes and report what you corrected

---

## Why This Command Stays Focused

Subtitle fixing is a distinct, quick task that doesn't benefit from being combined with other workflows. Keep it simple, keep it fast.

---

## Reference Files

- **Project scripts:** `video-projects/[project]/SCRIPT.md` (for verification)
- **SRT files:** `video-projects/[project]/*.srt`
