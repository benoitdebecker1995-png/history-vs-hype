# User Review Needed: Library Folder Cleanup

**Created:** 2026-01-20
**Phase:** 01-file-cleanup
**Priority:** Low (not blocking production)

## Summary

The `library/by-topic/general-history/` folder contains 728 files, many of which appear to be personal documents mixed with research materials. Automation cannot safely distinguish between personal and research files.

**Recommendation:** Manual review and cleanup by user.

## Files Identified for Review

### Personal Documents (High Confidence - Delete)

**CV Files (8+ copies):**
- `Unknown - CV-Europass-20200131-DeBecker-EN.pdf (n.d.).pdf` and variants
- These are personal CVs, not research materials

**Dutch Study Materials:**
- `Engels - Praktisch Engels (n.d.).pdf` (4+ copies)
- `Decloedt - Praktische info VTO NVA avond NVU (n.d.).pdf`
- `Becker - terecht bij professoren en assistenten voor (n.d.).pdf` (8+ copies based on RESEARCH.md)

**Gaming PDFs:**
- `Becker - Grim Hollow Subclasses in Etharis World Anvil (n.d.).pdf` (4+ copies)
- `Games - Grim Hollow The Monster Grimoire (n.d.).pdf`
- `grimhollow player guide.pdf (k).pdf`
- `grimhollow subclasses-1.pdf`
- `pdfcoffee.com-grim-hollow-campaign-guide-pdf-pdf-free.pdf`
- `pdfcoffee.com-grim-hollow-the-monster-grimoire-pdf-free.pdf`

**Financial/Administrative:**
- `Here in Brussels - energy certificates', which are certificates...` (energy certificate docs)

### Legitimate Research (Keep)

Based on RESEARCH.md, these types of files should be kept:
- Mitrokhin Archive volumes
- Cambridge Middle East Studies
- Oxford Medieval Texts
- Academic press publications on channel topics (colonialism, territorial disputes, history)

## Why Automated Cleanup Is Not Safe

1. **728 files is too many for safe bulk operations** - Risk of deleting research materials
2. **File naming is inconsistent** - Cannot reliably identify personal vs research by name pattern
3. **Some personal files have academic-looking names** - "Engels" could be Frederick Engels or Dutch study materials
4. **Sync folder risk** - This may be synced from another system; changes here might affect other devices

## Suggested Action

1. **Sort by file type and date** - Recent additions may be research, older files may be personal
2. **Search for obvious patterns:**
   - "Europass" or "CV" - Personal CVs
   - "Grim Hollow" or "grimhollow" - Gaming PDFs
   - "Praktisch" - Dutch study materials
   - "VTO" or "NVA" - Belgian/Dutch administrative
3. **Move to separate folder first** - Before deleting, move to `library/_to-delete/` for review
4. **Keep anything related to channel topics:** colonialism, territorial disputes, Middle East, Africa, crusades, medieval history

## Files Changed by Phase 01-04

This plan did NOT modify the library folder. All changes were to `video-projects/_IN_PRODUCTION/`:

### Script Consolidation (Task 1)
- 6 projects now have single FINAL-SCRIPT.md
- Old versions moved to `_old-versions/` subfolders
- Commit: `641eb9a`

### Folder Naming Fixes (Task 2)
- 7 folders renamed to match `[number]-[topic]-[year]` convention
- 1 empty duplicate folder deleted
- All projects now have unique numbers (1-29)
- Commit: `c603455`

### Naming Convention Reference

**Enforced pattern:** `^[0-9]+-[a-z0-9-]+-[0-9]{4}$`

**Examples:**
- `1-somaliland-2025`
- `24-iran-1953-coup-2025`
- `28-vance-part-2-review-2025`

**Current project numbers in use:**
1-13, 14-21, 23-29 (22 was removed as duplicate)

**Next available number:** 30

---

*This file documents items requiring manual user review that automation could not safely handle.*
