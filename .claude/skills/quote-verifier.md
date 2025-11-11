# Historical Quote Verification Skill

## Description
Verifies historical quotes and attributions to prevent errors like the Luther/Aristotle mixup. Checks quotes against primary sources and flags common misattributions.

## When to Use
- During script writing when you include historical quotes
- Before filming to verify all attributions
- When fact-checking research documents
- If viewer challenges an attribution

## What This Skill Does
1. Takes a quote and claimed attribution
2. Searches for primary source verification
3. Checks common misattribution databases
4. Flags red flags (vague dates, cross-cultural attribution, etc.)
5. Provides correct attribution with specific citation
6. Suggests alternative verified quotes if original is misattributed

## Red Flags Automatically Detected
- Vague attribution ("Luther in the 1520s...")
- Cross-cultural attribution (Greek concepts → Medieval theologians)
- Only found in secondary sources
- Suspiciously perfect/convenient quotes
- Anachronistic language

## Verification Process
1. **Check claimed source** - Does it exist in their writings?
2. **Search primary databases** - founders.archives.gov, papalencyclicals.net, etc.
3. **Check misattribution lists** - Quote Investigator, fact-check sites
4. **Verify exact wording** - Not paraphrased or out of context
5. **Document citation** - Specific work, year, page/section

## Output Format
For each quote checked:
```
QUOTE: "[exact quote]"
CLAIMED ATTRIBUTION: [Person, vague source]
VERIFICATION STATUS: ✅ Verified / ⚠️ Needs Correction / ❌ Misattributed

PRIMARY SOURCE:
- Work: [specific document/book]
- Date: [year]
- Location: [page/section/article]
- Link: [URL if available]

NOTES: [Context, common misattributions, alternatives]
```

## Common Misattributions Database
Includes known errors like:
- "Tools with voice" (Aristotle, not Luther)
- Einstein quotes (many fabricated)
- Jefferson quotes (often out of context)
- Burke quotes (famous ones often misattributed)

## Integration with Workflow
Creates quote tracking spreadsheet:
| Quote | Person | Source Claimed | Verified? | Citation | Notes |
|-------|--------|----------------|-----------|----------|-------|

**Before filming:** Every row must show ✅ Verified

## Example Usage
**You say:** "Verify this: 'Martin Luther called slaves tools with voice'"

**Skill output:**
```
❌ MISATTRIBUTED

This quote is from Aristotle's Politics (Book I, Part 4, 350 BCE),
not Martin Luther. Aristotle described slaves as "living tools" or
"animate instruments."

CORRECT ATTRIBUTION:
Aristotle, Politics, Book I, Part 4 (350 BCE)

WHAT LUTHER ACTUALLY SAID:
For positions on social hierarchy, see:
- "Admonition to Peace" (1525) - condemned peasant rebellions
- Argued Christians must submit to earthly authorities

RECOMMENDATION: Use Luther's verified position or use Aristotle
with correct attribution.
```

---

*This skill prevents credibility-destroying attribution errors and ensures every quote has specific, verifiable citation.*
