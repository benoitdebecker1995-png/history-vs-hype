---
description: Fix subtitle errors from auto-transcription (Post-production Phase 2)
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

## Fixing Process (MANDATORY ORDER)

**DO NOT skip steps. DO NOT jump to pattern-matching. The script cross-reference IS the process.**

### Step 0: Auto-Scan with SRT Fixer

Before manual review, run the auto-fixer to catch known transcription errors:

```python
import subprocess
result = subprocess.run(
    ['python', '-m', 'tools.youtube_analytics.auto_srt_fixer', '--project', PROJECT_SLUG, '--dry-run'],
    capture_output=True, text=True
)
print(result.stdout)
```

This matches against a corrections dictionary built from all past SRT-FIXES.md files. Use its output as your starting point — then verify and extend with manual cross-reference below.

### Step 1: Find and Read BOTH Files

1. Find the SRT file (Glob if needed)
2. Find the SCRIPT.md in the same project folder
3. **Read the ENTIRE script first** — this is your ground truth
4. Read the ENTIRE SRT file

**If no script exists:** Flag to user — you cannot reliably fix an SRT without a reference. Proceed with caution, fixing only obvious misspellings.

### Step 2: Cross-Reference Section by Section

**This is the core of the fix process. Do NOT skip it.**

1. Reconstruct the spoken text from consecutive SRT entries (strip `<b>` tags, join lines)
2. Compare against the corresponding script section
3. Flag EVERY discrepancy:
   - Wrong words ("crayon" vs "crown", "felt" vs "spoken")
   - Missing negations ("is" vs "isn't")
   - Wrong names ("Bombal" vs "Pombal", "Aveline" vs "Avalon")
   - Wrong numbers ("two or three" vs "two to four")
   - Wrong foreign terms ("Utipos de detes" vs "uti possidetis")
   - Extra/missing words ("perfect and north-south" vs "perfect north-south")
   - Stray commas that change meaning

**Use an agent for thoroughness** — spawn a general-purpose agent to do the full cross-reference if the SRT is longer than 100 subtitles. The agent reads both files and returns a complete error list. Then apply fixes from the list.

### Step 3: Fix Timestamps

**Do NOT use blind bulk replace like `01:0` → `00:0`.** That creates collateral damage (e.g., turning `00:01:09` into `00:00:09`).

Instead:
1. Check if timestamps start at `01:00:00` (1-hour offset)
2. If yes, fix the HOUR digit only: replace `01:XX:` with `00:XX:` at line start positions
3. After fixing, run a validation check:

```python
# Verify no timestamp has end <= start
python3 -c "
import re
with open('FILE.srt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    m = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', line.strip())
    if m:
        start, end = m.group(1), m.group(2)
        if end <= start:
            print(f'Line {i}: {start} --> {end}  (BROKEN - end <= start)')
"
```

4. Fix any broken timestamps individually

### Step 4: Apply Content Fixes

Using the error list from Step 2:
1. Fix each error with targeted Edit calls
2. Use `replace_all` only for terms that are ALWAYS wrong (e.g., a consistently misspelled name)
3. For ambiguous terms, fix individually with context

### Step 5: Final Validation

1. Run the timestamp validator again (Step 3 check)
2. Grep for any remaining instances of the original misspellings
3. Report all fixes made

---

## Common Auto-Transcription Errors

These are EXAMPLES, not an exhaustive list. Step 2 (script cross-reference) catches everything.

### Foreign Terms (most common failures)
- Portuguese/Spanish/Latin terms get mangled: "Volta Domar" → "Volta do Mar", "Utipos de detes" → "uti possidetis"
- Proper nouns with diacritics: "Giau" → "João", "Bombal" → "Pombal"
- Legal/academic terms: "Diritorio" → "Diretorio", "Lingua Guerral" → "Lingua Geral"

### Wrong Words (sounds similar)
- "crayon" / "crown", "felt" / "spoken", "Creme" / "crown", "share" / "shared"
- Missing negations: "is" vs "isn't" (critical — changes meaning entirely)
- "of" / "off" (preposition errors)

### Names and Places
- Historical names: "Banderantes" → "Bandeirantes", "Aveline" → "Avalon"
- Scholar names: "Zaccuto" → "Zacuto", "Carricero" → "Caicedo"

### Timestamp Issues
- 1-hour offset (01:00:00 start instead of 00:00:00)
- Broken timestamps from careless bulk replace

---

## Output

After fixing, report:
- Total fixes by category (timestamps, names, wrong words, foreign terms)
- Any lines where the SRT diverges from the script in a way that might be intentional (spoken ad-lib vs script)
- Confirmation that timestamp validation passed
- File is ready for upload

---

## BONUS: Extract Chapter Timestamps

**If asked to update YouTube metadata, extract chapter timestamps from SRT files.**

1. Read the SRT file
2. Note timestamp offset (often starts at 01:00:00)
3. Identify topic transitions by reading content
4. Convert SRT timestamps to video timestamps (subtract offset)
5. Create chapter list for YOUTUBE-METADATA.md

---

## Reference Files

- **Project scripts:** `video-projects/[project]/SCRIPT.md` (for verification)
- **SRT files:** `video-projects/[project]/*.srt`
