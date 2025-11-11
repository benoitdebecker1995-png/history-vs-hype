# SRT Subtitle File Corrector Skill

## Description
Fixes spelling, grammar, capitalization, and formatting errors in SRT subtitle files. Optimized for historical/political content with proper nouns, Latin terms, and academic language.

## When to Use
- After auto-generating subtitles from video
- Before uploading final video
- When preparing YouTube chapters from transcript
- To create clean transcripts for documentation

## What This Skill Does
1. Reads SRT file
2. Fixes common transcription errors:
   - Proper names (Vance, not Wens)
   - Latin phrases (Mirari Vos, Dum Diversas)
   - Historical figures (Servetus, not Cervitus)
   - Document titles (Syllabus of Errors)
   - Place names (Charlestown, Massachusetts)
3. Corrects capitalization:
   - Declaration of Independence
   - Catholic Church, Protestant
   - Treaty of Tripoli
4. Fixes grammar and punctuation
5. Maintains original timing
6. Preserves formatting tags (<b>, etc.)

## Specialized for History vs Hype
Knows common terms:
- Papal documents (bulls, encyclicals)
- Founding Fathers names
- Historical locations
- Academic terminology
- Political figures
- Latin/Greek terms

## Output
Creates two files:
1. **[filename]_CORRECTED.srt** - Clean subtitle file
2. **Corrections_Log.txt** - List of all changes made

## Example Corrections
```
Before: "Wens made claims"
After:  "Vance made claims"

Before: "pope gregory xvi publishes mirarivos"
After:  "Pope Gregory XVI publishes Mirari Vos"

Before: "the declaration of independence"
After:  "the Declaration of Independence"

Before: "michael cervitus"
After:  "Michael Servetus"

Before: "dumdiversas"
After:  "Dum Diversas"
```

## Quality Checks
- Verifies timing format (HH:MM:SS,mmm)
- Ensures sequential numbering
- Preserves line breaks
- Maintains subtitle synchronization
- Flags uncertain corrections for review

## Integration with YouTube
Corrected SRT can be:
- Uploaded as subtitles
- Used to generate chapters
- Converted to transcript
- Added to video description

---

*This skill ensures professional, error-free subtitles that maintain credibility and improve SEO.*
