# Summary: 17-02 Source Hint Generation

**Status:** Complete
**Date:** 2026-02-01

## What Was Built

### format_filters.py Extensions

**PUBLISHER_PATTERNS dict:**
- university_press: cambridge.org, oup.com, press.princeton.edu, etc.
- academic_databases: jstor.org, academia.edu, scholar.google.com, worldcat.org
- archives: nationalarchives.gov.uk, archives.gov, europeana.eu, loc.gov

**SOURCE_TYPE_INDICATORS dict:**
- Maps topic keywords to expected source types (primary, monograph, journal)

**get_source_hints(title, description=''):**
- Generates search queries ready to copy-paste into Google Scholar, JSTOR, etc.
- Returns dict with:
  - queries: list of search strings with site: filters
  - expected_types: ['primary', 'monograph', 'journal'] based on topic
  - publisher_sites: recommended academic publishers
  - confidence: 0-1 based on topic specificity

**evaluate_production_constraints() updated:**
- Now includes source_hints in output

**CLI added (main()):**
- `python format_filters.py "topic"` shows formatted output
- `python format_filters.py "topic" --json` for JSON output
- `python format_filters.py "topic" -v` for verbose details
- Shows: verdict, document score, animation risk, source hints, notes

### database.py Extensions

**store_production_constraints() updated:**
- Added source_hints parameter (optional Dict)
- source_hints stored in production_constraints JSON

**get_production_constraints() docstring updated:**
- Documents source_hints in return value

## Verification Results

### Source Hint Tests
- get_source_hints("Treaty of Versailles") → 3 queries, expected_types=['primary']
- High-specificity topics get higher confidence (0.7-0.9)
- Low-specificity topics get lower confidence (0.3-0.5)

### CLI Tests
- Treaty topic shows PROCEED verdict with document score 4/4
- Quantum topic shows SKIP verdict with BLOCKED message
- JSON output includes full source_hints dict

### Database Tests
- store_production_constraints() accepts source_hints parameter
- get_production_constraints() returns source_hints

## Key Decisions

1. **Query generation, not API calls** — No HTTP requests; generates search strings for manual use
2. **Site-filtered searches** — Queries include site: filters for academic publishers
3. **Confidence based on specificity** — More document-friendly keywords = higher confidence
4. **ASCII-safe CLI output** — Avoids Unicode issues on Windows console
5. **Backwards compatible** — Existing stored constraints without source_hints return empty dict

## Files Modified

- `tools/discovery/format_filters.py` (extended, ~150 lines added)
- `tools/discovery/database.py` (updated store/get signatures)

## Why Query Generation vs. API Calls

Per 17-RESEARCH.md:
- No official Google Scholar API exists
- SERP APIs cost $50-100/month
- Academic database APIs require institutional access
- Manual pre-screening with cached results is the practical approach

The source hints give users ready-to-use search queries they can run in Google Scholar, JSTOR, or WorldCat. This provides enough signal for pre-research screening without expensive API integrations.

## Example Output

```
======================================================================
  Production Constraints: The Treaty of Versailles
======================================================================

VERDICT: PROCEED
  Document Score:     4/4  [####################]
  Animation Risk:     LOW  (confidence: 0.90)

SOURCE HINTS:
  Expected types: primary

  Try these searches:
  1. "The Treaty of Versailles" site:cambridge.org OR site:oup.com
  2. "The Treaty of Versailles" site:jstor.org peer-reviewed
  3. "The Treaty of Versailles" primary source archive

NOTES:
  - Look for treaty texts, court documents, historical maps
```

## Phase 17 Complete

With 17-02 done, all three success criteria are met:
- ✅ FMT-01: Animation detection as hard blocks
- ✅ FMT-02: Document-friendliness scoring (0-4)
- ✅ FMT-03: Academic source hints for pre-research screening
