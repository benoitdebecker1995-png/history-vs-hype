# Phase 50 Audit: Error Handling

## 1. Bare Excepts (12 occurrences in 7 files)

### tools/youtube-analytics/feedback_queries.py (5 bare excepts)

```python
# Line 271 — mean() on empty list
try:
    return mean(rates), 'topic_average'
except:
    pass  # Fall through to channel average
```
**Fix:** `except StatisticsError:` — mean() raises StatisticsError on empty input

```python
# Line 279 — same pattern
try:
    return mean(rates), 'channel_average'
except:
    pass
```
**Fix:** `except StatisticsError:`

```python
# Line 532 — extract_winning_patterns()
try:
    winning = extract_winning_patterns()
except:
    winning = None
```
**Fix:** `except Exception as e:` + log warning

```python
# Line 608 — float conversion
try:
    drop_magnitude = float(words[i-1]) / 100
    break
except:
    pass
```
**Fix:** `except (ValueError, IndexError):`

```python
# Line 645 — complex parsing
try:
    ...
    break
except:
    pass  # Fail gracefully
```
**Fix:** `except (ValueError, KeyError, IndexError):`

### tools/youtube-analytics/pattern_synthesizer_v2.py (2 bare excepts)

```python
# Line 358 — JSON parsing
try:
    examples = json.loads(examples)
except:
    examples = []
```
**Fix:** `except (json.JSONDecodeError, TypeError):`

```python
# Line 496 — same pattern
try:
    examples = json.loads(examples)
except:
    examples = []
```
**Fix:** `except (json.JSONDecodeError, TypeError):`

### tools/youtube-analytics/retention_scorer.py (1 bare except)

```python
# Line 301 — JSON parsing
try:
    lessons = json.loads(lessons)
except:
    lessons = {}
```
**Fix:** `except (json.JSONDecodeError, TypeError):`

### tools/youtube-analytics/topic_strategy.py (1 bare except)

```python
# Line 146 — JSON parsing
try:
    observations = lessons_obj.get('observations', [])
    by_topic[topic]['observations'].extend(observations)
except:
    pass
```
**Fix:** `except (AttributeError, TypeError, KeyError):`

### tools/production/split_screen_guide.py (1 bare except)

```python
# Line 253 — file read
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    return None
```
**Fix:** `except (IOError, OSError, UnicodeDecodeError) as e:` + return `{'error': f'Failed to read {file_path}: {e}'}`

### tools/prompt_evaluation.py (1 bare except)

```python
# Line 754 — file search
try:
    content = full_path.read_text(encoding='utf-8').lower()
    return search_term.lower() in content
except:
    return False
```
**Fix:** `except (IOError, OSError, UnicodeDecodeError):`

### tools/history-clip-tool/launcher.py (1 bare except)

```python
# Line 128 — subprocess check
try:
    if result == 0:
        return True
except:
    pass
```
**Fix:** `except (OSError, subprocess.SubprocessError):` (out of main scope but easy fix)

## 2. Functions Returning None on Error (key cases)

| File | Function | Line | Trigger | Should Return |
|------|----------|------|---------|---------------|
| `split_screen_guide.py` | `_read_file()` | 254 | File read failure | `{'error': msg}` |
| `analyze.py` | `find_project_folder()` | 162 | No folder found | `None` is OK (search) |
| `patterns.py` | `_read_file_safe()` | 236 | File read failure | `None` is OK (internal) |
| `patterns.py` | `_find_project_folder()` | 298, 364 | No match | `None` is OK (search) |
| `patterns.py` | `calc_delta()` | 528, 852 | Division edge case | `None` is OK (math) |
| `kb_store.py` | `get_latest_snapshot()` | 214 | No data | `None` is OK (query) |
| `verification.py` | `_detect_language()` | 249 | Can't detect | `None` is OK (detection) |

**Assessment:** Most `return None` cases are legitimate (queries returning "not found"). The main offender is `split_screen_guide.py:_read_file()` which should return error dict.

## 3. Broad except Exception Handlers (notable cases)

Found ~85 `except Exception` blocks across tools/. Most are properly handled (logging the error, returning error dict). Key ones to tighten:

| File | Line | Current | Better |
|------|------|---------|--------|
| `dashboard/project_scanner.py` | 184 | `except Exception: return []` | `except (IOError, OSError): return []` |
| `discovery/competition.py` | 221 | `except (ImportError, Exception)` | `except (ImportError, OSError)` |

## 4. Good Error Dict Examples (templates for standardization)

### citation_extractor.py (best example):
```python
except Exception as e:
    return {'error': f'Failed to read file: {e}'}
```

### notebooklm_bridge.py (structured):
```python
except Exception as e:
    return {'error': f'Unexpected error: {str(e)}'}
```

### backfill.py (with context):
```python
except ImportError:
    return {'error': 'feedback_parser not available', 'processed': 0, 'skipped': 0, 'errors': 0}
```

### Proposed standardized format:
```python
return {
    'error': 'Human-readable message',
    'module': 'module_name',
    'operation': 'function_name',
    'details': str(e)  # original exception
}
```

## 5. Summary

| Module | Bare excepts | Broad Exception | None returns | Uses error dict |
|--------|-------------|-----------------|-------------|-----------------|
| feedback_queries.py | 5 | 0 | 0 | 0 |
| pattern_synthesizer_v2.py | 2 | 2 | 0 | 0 |
| retention_scorer.py | 1 | 3 | 0 | 0 |
| topic_strategy.py | 1 | 1 | 0 | 0 |
| split_screen_guide.py | 1 | 0 | 1 | 5 |
| prompt_evaluation.py | 1 | 1 | 0 | 0 |
| patterns.py | 0 | 14 | 6 | 0 |
| database.py | 0 | 14 | 0 | 34 |
| kb_store.py | 0 | 3 | 3 | 14 |
| **Totals** | **12** | **~85** | **~54** | **~198** |

The error dict pattern is already dominant (198 uses vs 54 None returns). Phase 50 needs to:
1. Fix 12 bare excepts (specific types)
2. Convert ~10 problematic None returns to error dicts
3. Add module/operation/details to error dicts that only have 'error' key
