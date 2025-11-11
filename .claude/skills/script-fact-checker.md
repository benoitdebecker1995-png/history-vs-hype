# Script Fact-Checker Skill

## Description
Systematically reviews video scripts to identify all factual claims, verify sources, and flag unsupported statements. Implements the Quote Verification Protocol and fact-checking best practices.

## When to Use
- After completing script draft
- Before filming begins
- When editing/revising scripts
- To create source documentation

## What This Skill Does
1. Reads your script
2. Identifies all factual claims:
   - Specific numbers/statistics
   - Historical events and dates
   - Quotes from historical figures
   - Cause-and-effect relationships
   - Legal/treaty provisions
3. Checks if each claim is sourced
4. Verifies quote attributions
5. Flags red flags (vague dates, unsupported claims)
6. Creates source tracking document
7. Generates list of missing sources

## Output Format

### Claim Analysis Report
```
TOTAL CLAIMS FOUND: X
FULLY SOURCED: X
NEEDS SOURCES: X
QUOTES TO VERIFY: X

---

UNSOURCED CLAIMS (Priority to fix):
1. [Line 45] "40,000 executed for witchcraft"
   STATUS: ⚠️ Number needs citation
   REQUIRED: Academic source with estimate range

2. [Line 127] "Thornwell in 1850s says..."
   STATUS: ❌ Vague attribution
   REQUIRED: Specific sermon/document, date, page

---

QUOTE VERIFICATION NEEDED:
1. "Tools with voice" - attributed to Luther
   STATUS: 🚨 COMMON MISATTRIBUTION
   ACTUAL: Aristotle, Politics Book I

---

WELL-SOURCED CLAIMS: ✅
- Mirari Vos (1832) Section 14 ✓ papalencyclicals.net
- Treaty of Tripoli Article 11 ✓ founders.archives.gov
- Dum Diversas (1452) ✓ papal bull documented
```

### Source Tracking Spreadsheet
Creates CSV with:
| Line | Claim | Source Status | Citation | Verification |
|------|-------|---------------|----------|--------------|

## Verification Checklist Applied
For each claim:
- [ ] Specific source identified?
- [ ] 2+ independent sources?
- [ ] Primary source when possible?
- [ ] Quote has specific citation (work, year, page)?
- [ ] Not a common misattribution?
- [ ] Contested info clearly labeled?

## Red Flags Detected
- Absolutist language ("always," "never," "all historians agree")
- Suspiciously precise numbers without source
- Vague attributions ("1850s," "around that time")
- Claims only found in secondary sources
- Cross-cultural anachronisms

## Integration with Production
**Before filming:**
- All claims must be ✅ Verified
- No ⚠️ or ❌ flags remaining
- Source tracking complete

**Generates for video description:**
- Complete source list
- Formatted citations
- Links to primary sources

## Example Usage
**You paste:** Your complete video script

**Skill generates:**
1. Full claim analysis report
2. List of 12 unsourced claims to fix
3. 3 quotes flagged for verification
4. Source tracking spreadsheet
5. Pre-production verification checklist

**Before you film:** Fix all flagged issues

---

*This skill prevents attribution errors, ensures every claim is backed by sources, and maintains channel credibility.*
