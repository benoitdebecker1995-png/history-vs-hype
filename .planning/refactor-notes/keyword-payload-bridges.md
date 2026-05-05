# KeywordPayload Bridges (K2)

**Date:** 2026-05-05  
**Status:** DONE  
**Finding:** All call sites already backward-compatible; no migrations needed.

## Call Site Analysis

| File | Line | Pattern | Source | Bridge? |
|------|------|---------|--------|---------|
| `tools/discovery/autocomplete.py` | 271 | `db.add_keyword(suggestion, source='autocomplete')` | Local (user input) | ✅ Ready to migrate — no bridge needed |
| `tools/discovery/keywords.py` | 65 | `db.add_keyword(keyword, source, search_volume, competition)` | CLI wrapper | ✅ Ready to migrate — no bridge needed |
| `tools/discovery/keywords.py` | 99 | `db.add_keyword(keyword, source)` | Batch handler | ✅ Ready to migrate — no bridge needed |
| `tools/discovery/demand.py` | 94 | `self.db.add_keyword(keyword, source='demand_analysis')` | Analysis flow | ✅ Ready to migrate — no bridge needed |
| `tools/discovery/schema_manager.py` | docstring | `db.add_keyword('dark ages myth', source='autocomplete')` | Example only | N/A |

## Finding

All add_keyword call sites are **already using the backward-compatible string + params interface**. No dict construction patterns found.

This means:
- K1 (introduce KeywordPayload) achieved its goal of establishing a seam
- K2 (migrate to direct KeywordPayload use) is optional for performance, not critical
- No `from_dict()` bridges are actively in use

## Remaining Bridges

**Count:** 0 active bridges  
**Reason:** All callers already adapted to the union signature during K1

## Next Steps (K3+)

When performance optimization warrants:
1. Replace each string + params call with direct KeywordPayload construction
2. Example: `db.add_keyword(KeywordPayload(keyword, source='autocomplete'))`
3. Changes are backward-compatible; can be done incrementally

## Decision

Mark K2 complete with finding: **no dict bridges needed at present.**
