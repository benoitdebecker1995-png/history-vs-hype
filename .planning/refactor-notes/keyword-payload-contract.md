# KeywordPayload Contract (K1)

**Date:** 2026-05-05  
**Status:** DONE  
**Tests:** All 93 pass (90 original + 3 new KeywordPayload tests)

## Implementation

### KeywordPayload Dataclass
Created frozen dataclass in `tools/discovery/keyword_store.py` with fields:
- `keyword: str` (required)
- `source: str = 'manual'`
- `search_volume: Optional[int] = None`
- `competition: Optional[float] = None`

Matches the implicit dict contract previously expected by `add_keyword()`.

### from_dict Classmethod
Backward compatibility bridge for remote sources:
```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'KeywordPayload':
    return cls(
        keyword=data['keyword'],
        source=data.get('source', 'manual'),
        search_volume=data.get('search_volume'),
        competition=data.get('competition'),
    )
```

Enables safe migration of remote callers without forcing immediate refactoring.

### add_keyword Signature Update
Now accepts `Union[KeywordPayload, str]`:
```python
def add_keyword(
    self,
    keyword: Union[KeywordPayload, str],
    source: str = 'manual',
    search_volume: Optional[int] = None,
    competition: Optional[float] = None,
) -> Dict[str, Any]:
```

Normalizes both forms internally:
- Direct KeywordPayload: uses as-is
- String + params (legacy): constructs KeywordPayload internally

All existing callers (keywords.py, demand.py) continue to work without changes.

### Export
Added to `tools/discovery/__init__.py`:
```python
from .keyword_store import KeywordPayload
__all__ = ['KeywordDB', 'init_database', 'KeywordPayload']
```

## Callers Status

| File | Pattern | Migration |
|------|---------|-----------|
| `tools/discovery/keywords.py` | `db.add_keyword(keyword, source, search_volume, competition)` | Backward compat — no change needed |
| `tools/discovery/demand.py` | `self.db.add_keyword(keyword, source='demand_analysis')` | Backward compat — no change needed |
| `tests/test_database_pin.py` | Mixed (string + new KeywordPayload tests) | Added 3 pinning tests |
| `tools/production/intake_parser.py` | No direct calls to add_keyword | N/A |

## Pinning Tests

Added to `TestAddKeyword`:
1. `test_add_keyword_with_payload()` — Direct KeywordPayload construction
2. `test_payload_from_dict()` — from_dict with all fields
3. `test_payload_from_dict_with_defaults()` — from_dict with minimal dict

All pass; total test count: 93 (90 original + 3 new).

## Notes

- intake_parser.py does not call add_keyword() directly; it parses into JSON format for EXTERNAL-INTELLIGENCE.json
- K1 establishes the contract; K2 will migrate specific call sites that benefit from direct KeywordPayload construction
- Backward compat ensures no breaking changes during gradual migration
