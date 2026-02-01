# Summary: 17-01 Production Constraint Foundation

**Status:** Complete
**Date:** 2026-02-01

## What Was Built

### format_filters.py (New Module)
Created production constraint detection module with:

**is_animation_required(title, description)**
- Detects topics that require animation format (hard blocks)
- Uses ANIMATION_REQUIRED_KEYWORDS (35+ terms: quantum, molecular, cellular, algorithm, etc.)
- Uses DOCUMENTARY_SAFE_KEYWORDS (40+ terms: treaty, map, document, court, etc.)
- Returns dict with: is_blocked, reason, confidence (0-1), matched_keywords
- Handles mixed signals with reduced confidence

**calculate_document_score(title, description)**
- Returns 0-4 document-friendliness score
- Uses DOCUMENT_FRIENDLY_KEYWORDS with point values (+3 for treaty/court, +2 for law/colonial, +1 for war/history)
- Uses CONCEPT_HEAVY_KEYWORDS with negative values (-2 for philosophy/theory, -1 for ideology/belief)
- Baseline 2, adds/subtracts, clamps to 0-4

**evaluate_production_constraints(title, description)**
- Combines both checks into comprehensive evaluation
- Returns: is_viable, animation_check, document_score, recommendation, production_notes

### schema.sql Extension
Added Phase 17 production constraint columns:
- `production_constraints TEXT` — JSON storage for animation_required, document_score, sources_found
- `constraint_checked_at DATE` — When constraint was evaluated
- `is_production_blocked BOOLEAN DEFAULT 0` — Quick filter for blocked topics
- Index: `idx_keywords_blocked ON keywords(is_production_blocked, constraint_checked_at DESC)`

### database.py Extension
Added three methods to KeywordDB class:

**_ensure_production_columns()**
- Auto-migration for existing databases
- Called from _ensure_connection() after classification columns

**store_production_constraints(keyword_id, animation_required, document_score, sources_found, source_examples)**
- Stores constraint JSON to keywords table
- Sets is_production_blocked flag for animation-required topics
- Returns {'status': 'stored', 'keyword_id': id} or error dict

**get_production_constraints(keyword_id, max_age_days=90)**
- Retrieves constraint data with staleness check
- Returns None if not found or too old
- Parses JSON and adds runtime fields (is_production_blocked, data_age_days)

## Verification Results

### Animation Detection Tests
- "How Quantum Mechanics Work" → is_blocked=True (correct)
- "The Treaty That Changed Europe" → is_blocked=False (correct)
- Mixed signals handled with reduced confidence

### Document Scoring Tests
- "The Treaty That Split a Country" → score=4/4 (correct)
- "The Philosophy of Freedom" → score=0/4 (correct)
- "The Border Dispute Between Nations" → score=4/4 (correct)

### Database Tests
- store_production_constraints() → {'status': 'stored'}
- get_production_constraints() → Returns full constraint dict
- Auto-migration works for existing databases

## Key Decisions

1. **Keyword-based detection over ML** — Simple, deterministic, no external dependencies
2. **Confidence scoring for mixed signals** — Lower confidence (0.5-0.6) when both animation and documentary keywords present
3. **90-day default staleness** — Production constraints change slowly, longer cache than demand data
4. **JSON storage for flexibility** — Can extend constraint fields without schema changes
5. **is_production_blocked flag** — Quick boolean filter for animation-required topics

## Files Modified

- `tools/discovery/format_filters.py` (new, 230 lines)
- `tools/discovery/schema.sql` (extended, 11 lines added)
- `tools/discovery/database.py` (extended, ~120 lines added)

## Dependencies

- None (uses only Python stdlib)
- Follows Phase 16 patterns (error dict returns, graceful degradation, JSON storage)

## What's Next

Phase 17 may need additional plans for:
- Academic source availability verification (FMT-03)
- CLI integration for format filtering
- Integration with competition analysis pipeline
