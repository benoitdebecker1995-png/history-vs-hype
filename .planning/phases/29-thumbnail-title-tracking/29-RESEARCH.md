# Phase 29: Thumbnail & Title Tracking - Research

**Researched:** 2026-02-06
**Domain:** Manual CTR tracking, perceptual hashing, variant management
**Confidence:** HIGH

## Summary

Phase 29 enables thumbnail/title A/B testing for a solo creator with manual CTR entry. This phase builds on Phase 27's database schema (already complete) and integrates with existing `/analyze` command patterns.

The standard approach combines: (1) ImageHash library for thumbnail pattern analysis via perceptual hashing, (2) CLI prompt-based manual CTR entry (YouTube API doesn't reliably provide CTR), (3) JSON tag storage in SQLite TEXT columns for flexible variant categorization, and (4) snapshot-based tracking at meaningful intervals (48h, 7d, 14d).

This research identifies proven libraries (ImageHash 4.3.2), established CLI input patterns from the existing codebase, and SQLite best practices for tag storage and timezone handling. All findings verified against official documentation and 2026 sources.

**Primary recommendation:** Use ImageHash phash for thumbnail similarity detection, store tags as JSON TEXT in SQLite (matching Phase 16-19 pattern), prompt for manual CTR entry when API unavailable (matching existing ctr.py behavior), and leverage existing KeywordDB class patterns for CRUD operations.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| ImageHash | 4.3.2 | Perceptual hashing for thumbnail pattern analysis | Most popular Python perceptual hashing library (3.5k+ stars), actively maintained, supports multiple algorithms (phash, dhash, whash) |
| Pillow (PIL) | Latest | Image loading for ImageHash | Required dependency for ImageHash, standard Python image library |
| sqlite3 | Built-in | Database storage | Already used throughout project, Phase 27 schema complete |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json | Built-in | Tag serialization for visual_pattern_tags and formula_tags | Already used in database.py (lines 837, 890, 1758), matches existing pattern |
| datetime | Built-in | Timestamp management with UTC | Already used throughout project, SQLite date handling |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| ImageHash | Manual pixel comparison | ImageHash provides battle-tested algorithms; custom solution prone to errors |
| JSON TEXT tags | Normalized tag tables | JSON TEXT matches Phase 16-19 pattern, simpler for low tag volume (4-6 tags total), easier querying with LIKE |
| Manual CTR entry | YouTube API only | API CTR unreliable (Google Issue Tracker #254665034), manual entry is necessary fallback |

**Installation:**
```bash
pip install imagehash pillow
```

## Architecture Patterns

### Recommended Project Structure
```
tools/
├── youtube-analytics/
│   ├── ctr.py                    # Existing - graceful CTR fallback pattern
│   ├── analyze.py                # Existing - CLI integration point with --ctr flag
│   └── variants.py               # NEW - variant management CLI
└── discovery/
    └── database.py               # Extend with Phase 29 CRUD methods
```

### Pattern 1: Manual CTR Entry with Validation
**What:** Prompt user for CTR when API returns `ctr_available: False`
**When to use:** Every CTR snapshot (48h, 7d, 14d intervals)
**Example:**
```python
# Source: Existing ctr.py pattern (lines 141-150) + input validation best practices
from ctr import get_ctr_metrics

result = get_ctr_metrics(video_id)

if not result['ctr_available']:
    # Prompt for manual entry
    while True:
        try:
            ctr_input = input("CTR not available via API. Enter CTR from YouTube Studio (e.g., 4.5): ").strip()
            ctr_percent = float(ctr_input)

            if 0 <= ctr_percent <= 100:
                result['ctr_percent'] = ctr_percent
                result['ctr_source'] = 'manual_entry'
                result['is_late_entry'] = True  # Mark as manually entered
                break
            else:
                print("Error: CTR must be between 0 and 100")
        except ValueError:
            print("Error: Please enter a valid number (e.g., 4.5)")
```

### Pattern 2: Perceptual Hash Generation and Storage
**What:** Generate phash for thumbnails to enable pattern analysis
**When to use:** When registering new thumbnail variant
**Example:**
```python
# Source: ImageHash official docs (https://pypi.org/project/ImageHash/)
from PIL import Image
import imagehash

def generate_thumbnail_hash(file_path: str) -> str:
    """Generate perceptual hash for thumbnail pattern analysis"""
    try:
        img = Image.open(file_path)
        hash_value = imagehash.phash(img)  # Perceptual hash recommended for visual similarity
        return str(hash_value)  # Returns hex string (e.g., 'ffd7918181c9ffff')
    except Exception as e:
        print(f"Error generating hash: {e}")
        return None
```

### Pattern 3: JSON Tag Storage (Matching Existing Pattern)
**What:** Store visual patterns and title formulas as JSON TEXT in SQLite
**When to use:** Storing visual_pattern_tags and formula_tags columns
**Example:**
```python
# Source: Existing database.py pattern (lines 837-839, 1758-1767)
import json

# Store tags as JSON (matches competitor_videos.angles pattern)
visual_patterns = ['map', 'face', 'text']
visual_pattern_json = json.dumps(visual_patterns)

cursor.execute(
    "INSERT INTO thumbnail_variants (video_id, variant_letter, file_path, perceptual_hash, visual_pattern_tags, created_at) VALUES (?, ?, ?, ?, ?, ?)",
    (video_id, 'A', '/path/to/thumb_a.jpg', hash_value, visual_pattern_json, datetime.utcnow().date().isoformat())
)

# Retrieve and parse
cursor.execute("SELECT * FROM thumbnail_variants WHERE video_id = ?", (video_id,))
row = cursor.fetchone()
visual_patterns = json.loads(row['visual_pattern_tags'])  # ['map', 'face', 'text']
```

### Pattern 4: UTC Timestamp Storage (Existing Best Practice)
**What:** Store all timestamps as UTC DATE in ISO format
**When to use:** All created_at, recorded_at, snapshot_date columns
**Example:**
```python
# Source: Existing database.py pattern (lines 139, 384, 1764)
from datetime import datetime

# Always use UTC for consistency
now = datetime.utcnow().date().isoformat()  # '2026-02-06'

cursor.execute(
    "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, recorded_at) VALUES (?, ?, ?, ?)",
    (video_id, now, ctr_percent, now)
)
```

### Pattern 5: KeywordDB Class Extension (Established Migration Pattern)
**What:** Add Phase 29 CRUD methods to existing KeywordDB class
**When to use:** All database operations for variants and snapshots
**Example:**
```python
# Source: Existing database.py Phase 16-19 method structure (lines 802-861, 978-1054)
class KeywordDB:
    # ... existing methods ...

    def add_thumbnail_variant(self, video_id: str, variant_letter: str,
                              file_path: str, visual_patterns: List[str]) -> Dict[str, Any]:
        """
        Register thumbnail variant with perceptual hash.

        Args:
            video_id: YouTube video ID
            variant_letter: 'A', 'B', 'C'
            file_path: Absolute path to thumbnail file
            visual_patterns: List of pattern tags ['map', 'face', 'document']

        Returns:
            {'status': 'inserted', 'variant_id': int} on success
            {'error': msg} on failure
        """
        try:
            # Generate perceptual hash
            hash_value = self._generate_thumbnail_hash(file_path)

            # Store with JSON tags
            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()
            patterns_json = json.dumps(visual_patterns)

            cursor.execute(
                """INSERT INTO thumbnail_variants
                   (video_id, variant_letter, file_path, perceptual_hash, visual_pattern_tags, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (video_id, variant_letter, file_path, hash_value, patterns_json, now)
            )

            self._conn.commit()
            return {'status': 'inserted', 'variant_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}
```

### Anti-Patterns to Avoid
- **Cryptographic hashing for thumbnails:** ImageHash phash is for visual similarity; don't use SHA256/MD5
- **Local time without timezone:** Always store UTC timestamps, convert to local in presentation layer only
- **Separate tag tables for 4-6 tags:** JSON TEXT is simpler and matches existing codebase pattern (angles, constraints)
- **Assuming API CTR availability:** Always implement manual entry fallback (API is unreliable per ctr.py)
- **Batch inserts without user confirmation:** Solo creator enters 1-2 videos/month, confirm before persisting

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Perceptual hashing algorithm | Custom pixel comparison logic | ImageHash phash | Battle-tested algorithms (average, perceptual, difference, wavelet), handles edge cases (rotation, scaling, brightness) |
| Input validation for percentages | Manual try/except per prompt | Reusable validation function | DRY principle, consistent error messages, handles edge cases (whitespace, negative, >100) |
| Hamming distance calculation | Custom hash comparison | ImageHash subtraction | Built-in hash comparison via subtraction operator returns Hamming distance |
| Thumbnail file existence check | Manual os.path.exists | Path.exists() from pathlib | More robust, cross-platform, better error handling |
| Tag searching in JSON | LIKE '%pattern%' | SQLite JSON functions (json_each) | Avoids false positives from substring matches in other fields |

**Key insight:** Solo creator workflow (1-2 videos/month, manual entry) allows simpler patterns. Don't optimize prematurely for batch operations that won't happen.

## Common Pitfalls

### Pitfall 1: Assuming CTR API Availability
**What goes wrong:** Code expects CTR from API, crashes when unavailable
**Why it happens:** Google Issue Tracker #254665034 - CTR metrics inconsistently available via API
**How to avoid:** Always check `ctr_available` boolean before accessing `ctr_percent`, provide manual entry fallback
**Warning signs:** API returns 400 error, ctr_percent is None, existing ctr.py returns `ctr_available: False`

### Pitfall 2: Storing Hash as BLOB Instead of TEXT
**What goes wrong:** Hash comparison breaks, can't search by prefix
**Why it happens:** Confusion with binary hashing (cryptographic) vs hex string representation
**How to avoid:** ImageHash returns hex string (e.g., 'ffd7918181c9ffff'), store as TEXT for easy comparison and indexing
**Warning signs:** Hash queries fail, can't use LIKE for similarity search, indexes don't work

### Pitfall 3: JSON Tag Querying Without Escaping
**What goes wrong:** False positives when searching tags (e.g., searching 'map' matches 'mapper')
**Why it happens:** LIKE '%map%' matches anywhere in JSON string
**How to avoid:** Use exact match pattern: `angles LIKE '%"map"%'` (include quotes) to match JSON array element
**Warning signs:** Phase 16 already uses this pattern (database.py line 2007), follow established approach

### Pitfall 4: Timezone Confusion on Snapshot Dates
**What goes wrong:** Snapshots recorded with local time cause inconsistent interval calculations
**Why it happens:** Developer uses datetime.now() instead of datetime.utcnow()
**How to avoid:** Always use `datetime.utcnow().date().isoformat()` for SQLite DATE columns, matches existing codebase
**Warning signs:** Existing code uses utcnow() consistently (lines 139, 384, 1764), don't deviate

### Pitfall 5: Not Marking Manual vs API CTR Source
**What goes wrong:** Can't distinguish data quality or validate trends
**Why it happens:** Forgetting to set `ctr_source` and `is_late_entry` fields
**How to avoid:** Set `ctr_source='manual_entry'` and `is_late_entry=True` when prompting user
**Warning signs:** All snapshots look identical in source, can't filter by data quality

### Pitfall 6: Validating File Path After Hash Generation
**What goes wrong:** Generate hash for non-existent file, silently fails
**Why it happens:** Not checking Path.exists() before opening with PIL
**How to avoid:** Validate file existence BEFORE calling imagehash, return error dict immediately
**Warning signs:** PIL raises FileNotFoundError, hash generation succeeds but stores None

## Code Examples

Verified patterns from official sources:

### ImageHash: Generating and Comparing Perceptual Hashes
```python
# Source: https://pypi.org/project/ImageHash/ official examples
from PIL import Image
import imagehash

# Generate perceptual hash (recommended for visual similarity)
hash_a = imagehash.phash(Image.open('thumbnail_a.jpg'))
hash_b = imagehash.phash(Image.open('thumbnail_b.jpg'))

# Compare hashes (returns Hamming distance)
distance = hash_a - hash_b  # 0 = identical, <10 = very similar, >10 = different

# Convert to string for storage
hash_str = str(hash_a)  # 'ffd7918181c9ffff' (hex representation)

# Reconstruct from string
hash_from_db = imagehash.hex_to_hash(hash_str)
```

### Manual CTR Entry with Validation
```python
# Source: Combine existing ctr.py pattern with input validation best practices
# https://automatetheboringstuff.com/2e/chapter8/

def prompt_for_ctr(video_id: str) -> float:
    """
    Prompt user for manual CTR entry with validation.

    Returns:
        CTR as float (0-100 range)
    """
    print(f"\nCTR not available via API for video {video_id}")
    print("Check YouTube Studio > Analytics > Reach > Impressions click-through rate")

    while True:
        try:
            ctr_input = input("Enter CTR percentage (e.g., 4.5): ").strip()

            if not ctr_input:
                print("Error: CTR cannot be empty")
                continue

            ctr_percent = float(ctr_input)

            if ctr_percent < 0:
                print("Error: CTR cannot be negative")
            elif ctr_percent > 100:
                print("Error: CTR cannot exceed 100%")
            else:
                return ctr_percent

        except ValueError:
            print("Error: Please enter a valid number (e.g., 4.5)")
```

### Storing and Retrieving JSON Tags
```python
# Source: Existing database.py pattern (Phase 16-19)
import json

# Storing tags (matches competitor_videos.angles pattern)
visual_patterns = ['map', 'document', 'face']
formula_tags = ['mechanism', 'paradox']

cursor.execute(
    """INSERT INTO thumbnail_variants
       (video_id, variant_letter, file_path, visual_pattern_tags, created_at)
       VALUES (?, ?, ?, ?, ?)""",
    (video_id, 'A', file_path, json.dumps(visual_patterns), datetime.utcnow().date().isoformat())
)

# Retrieving and parsing tags
cursor.execute("SELECT * FROM thumbnail_variants WHERE video_id = ?", (video_id,))
row = cursor.fetchone()
patterns = json.loads(row['visual_pattern_tags'])  # ['map', 'document', 'face']

# Searching with JSON (exact match to avoid false positives)
cursor.execute(
    "SELECT * FROM thumbnail_variants WHERE visual_pattern_tags LIKE ?",
    ('%"map"%',)  # Include quotes to match JSON array element exactly
)
```

### UTC Timestamp Handling
```python
# Source: Existing database.py pattern + SQLite datetime best practices
# https://blog.sqlite.ai/handling-timestamps-in-sqlite
from datetime import datetime

# Always store UTC for consistency
snapshot_date = datetime.utcnow().date().isoformat()  # '2026-02-06'
recorded_at = datetime.utcnow().date().isoformat()

cursor.execute(
    """INSERT INTO ctr_snapshots
       (video_id, snapshot_date, ctr_percent, recorded_at)
       VALUES (?, ?, ?, ?)""",
    (video_id, snapshot_date, ctr_percent, recorded_at)
)

# Query by date range (SQLite handles ISO format natively)
cursor.execute(
    """SELECT * FROM ctr_snapshots
       WHERE video_id = ? AND snapshot_date BETWEEN ? AND ?
       ORDER BY snapshot_date ASC""",
    (video_id, '2026-01-01', '2026-01-31')
)
```

### Complete Variant Registration Pattern
```python
# Source: Combine ImageHash, validation, and database patterns
from pathlib import Path
from PIL import Image
import imagehash
import json
from datetime import datetime

def register_thumbnail_variant(db, video_id: str, variant_letter: str,
                                file_path: str, visual_patterns: List[str]) -> Dict[str, Any]:
    """
    Register thumbnail variant with full validation.

    Args:
        db: KeywordDB instance
        video_id: YouTube video ID
        variant_letter: 'A', 'B', 'C'
        file_path: Absolute path to thumbnail file
        visual_patterns: List of pattern tags ['map', 'face', 'document']

    Returns:
        {'status': 'inserted', 'variant_id': int, 'hash': str} on success
        {'error': msg} on failure
    """
    # Validate file exists
    thumb_path = Path(file_path)
    if not thumb_path.exists():
        return {'error': f'Thumbnail file not found: {file_path}'}

    # Generate perceptual hash
    try:
        img = Image.open(thumb_path)
        hash_value = imagehash.phash(img)
        hash_str = str(hash_value)
    except Exception as e:
        return {'error': f'Failed to generate hash: {e}'}

    # Store in database
    cursor = db._conn.cursor()
    now = datetime.utcnow().date().isoformat()
    patterns_json = json.dumps(visual_patterns)

    try:
        cursor.execute(
            """INSERT INTO thumbnail_variants
               (video_id, variant_letter, file_path, perceptual_hash, visual_pattern_tags, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (video_id, variant_letter, str(thumb_path.absolute()), hash_str, patterns_json, now)
        )
        db._conn.commit()

        return {
            'status': 'inserted',
            'variant_id': cursor.lastrowid,
            'hash': hash_str,
            'patterns': visual_patterns
        }
    except sqlite3.Error as e:
        return {'error': f'Database operation failed: {e}'}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Third-party A/B testing tools | YouTube native "Test & Compare" | 2024-2025 rollout | Native tool available but optimizes for watch time, not CTR. Solo creators still need manual CTR tracking for impressions/CTR analysis |
| Binary hash storage (BLOB) | Hex string storage (TEXT) | ImageHash 4.0 (2018) | Breaks compatibility with pre-4.0 hashes, but enables indexing and LIKE queries |
| Local datetime storage | UTC ISO format | SQLite best practice (ongoing) | Eliminates DST bugs, simplifies calculations, matches Python datetime.utcnow() |
| Normalized tag tables | JSON TEXT for low-volume tags | Modern SQLite (3.38+) with JSON functions | Simpler schema, matches existing codebase, SQLite JSON support mature |

**Deprecated/outdated:**
- **ImageHash <4.0 binary format:** Pre-4.0 hashes stored as binary, incompatible with current hex format. Use `old_hex_to_hash()` migration function if needed.
- **YouTube Analytics API for reliable CTR:** Google Issue Tracker #254665034 confirms CTR inconsistently available. Manual entry is not a workaround, it's the primary method.
- **Complex tag normalization for 4-6 tags:** Modern SQLite JSON functions make TEXT storage with json_each() more performant for small tag sets.

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal hash similarity threshold for "visually similar" thumbnails**
   - What we know: ImageHash docs say "adjust the hashsize or require some manhattan distance" but don't specify thresholds
   - What's unclear: What Hamming distance (0-64) should trigger "similar pattern detected" warning?
   - Recommendation: Start with threshold of 10 (based on community usage patterns), make configurable, validate with user's actual thumbnails

2. **Automated snapshot scheduling mechanism**
   - What we know: Requirements specify 48h, 7d, 14d snapshots, but no scheduling infrastructure exists
   - What's unclear: Should this be cron-based, manual CLI commands, or integrated into `/analyze`?
   - Recommendation: Phase 29 provides CLI commands for manual snapshots, defer automated scheduling to Phase 30 (which needs statistical validation anyway)

3. **Handling thumbnail file moves/renames**
   - What we know: file_path stored as absolute path in database
   - What's unclear: What happens if user reorganizes thumbnails directory?
   - Recommendation: Store relative path from project root OR validate file_path on retrieval and warn if missing (don't block operations)

4. **Tag vocabulary standardization**
   - What we know: visual_pattern_tags and formula_tags are freeform JSON arrays
   - What's unclear: Should there be a predefined tag vocabulary or let user define?
   - Recommendation: Start with suggested tags (map, face, text, document for visual; mechanism, paradox, document for formula) but allow custom tags, add CLI `--list-tags` to show common patterns

## Sources

### Primary (HIGH confidence)
- ImageHash official PyPI page - https://pypi.org/project/ImageHash/ - version 4.3.2, installation, API examples
- ImageHash GitHub repository - https://github.com/JohannesBuchner/imagehash - hash algorithms, comparison methods
- SQLite JSON functions documentation - https://sqlite.org/json1.html - JSON storage and querying
- Existing codebase (database.py) - Phase 16-19 patterns for JSON storage, UTC timestamps, KeywordDB class structure
- Existing codebase (ctr.py) - Graceful CTR fallback pattern, API unavailability handling
- SQLite datetime best practices - https://blog.sqlite.ai/handling-timestamps-in-sqlite - UTC storage recommendations

### Secondary (MEDIUM confidence)
- Beekeeper Studio SQLite JSON guide - https://www.beekeeperstudio.io/blog/sqlite-json - JSON vs normalized tables tradeoff analysis
- Python input validation patterns - https://automatetheboringstuff.com/2e/chapter8/ - try/except validation loops
- YouTube Test & Compare feature - https://influencermarketinghub.com/youtube-test-compare/ - native A/B testing context (watch time optimization, not CTR)

### Tertiary (LOW confidence)
- Generic thumbnail A/B testing strategies - flagged for validation, not Phase 29-specific
- Third-party CTR tracking tools - out of scope (manual entry is requirement)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - ImageHash is clear choice (most popular, actively maintained), existing codebase uses sqlite3/json
- Architecture: HIGH - All patterns verified against existing codebase (Phases 16-19), official ImageHash docs, SQLite datetime best practices
- Pitfalls: HIGH - Drawn from existing ctr.py graceful fallback, Phase 16 JSON tag pattern, SQLite datetime guidance

**Research date:** 2026-02-06
**Valid until:** 2026-03-06 (30 days - stable domain, ImageHash mature library)
