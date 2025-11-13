---
description: Fix common subtitle (.srt) errors from auto-transcription
---

You are fixing subtitle files for History vs Hype videos.

## Common Issues in Auto-Generated Subtitles

### 1. Timestamp Errors
- **Problem:** Timestamps start at 01:00:00 instead of 00:00:00 (1 hour offset)
- **Fix:** Replace all `01:0` with `00:0`

### 2. Name Misspellings
Common auto-transcription errors in historical names:
- McMehan → McMahon
- Rochhild → Rothschild
- Francois-Jacques-Picot → François Georges-Picot
- even South → Ibn Saud
- MacMehan → McMahon
- Ataturk → Atatürk

### 3. Treaty/Place Names
- Seyver → Sèvres
- Lausan → Lausanne
- Nasht → Najd
- Sun Remo → San Remo
- Sykes-Bikko → Sykes-Picot (common misrecognition)

### 4. Date Errors
- Check dates against script for accuracy
- Common: October 23 vs. October 24 (verify from script)

## Fixing Process

**Step 1: Find the subtitle file**
```
Use Glob: video-projects/**/*.srt
Usually in: video-projects/_READY_TO_FILM/[project]/
```

**Step 2: Read the file to identify errors**
- Note all name misspellings
- Check timestamp format (01: vs 00:)
- Verify dates against script

**Step 3: Fix systematically**
1. **Timestamp offset:** Use replace_all for 01:0 → 00:0
2. **Name errors:** Fix each misspelling individually
3. **Treaty names:** Check historical accuracy
4. **Verify:** Read corrected sections to confirm

**Step 4: Common replacement patterns**
```
Replace all: 01:0 → 00:0
Replace all: Sykes-Bikko → Sykes-Picot
Replace all: Seyver → Sèvres
Individual: McMehan → McMahon (check context)
```

## User Preference

**Be efficient:**
- Don't ask "what file?" - find it with Glob
- Don't ask "what to fix?" - read and identify errors
- Just do the fixes and report what you corrected

## Output

After fixing, report:
- Number of timestamp corrections
- List of name corrections
- Any date fixes
- File is ready for upload
