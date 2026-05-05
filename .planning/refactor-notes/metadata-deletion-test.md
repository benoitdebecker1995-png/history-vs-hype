# metadata.py Deletion Test (J3)

**Date:** 2026-05-05
**Verdict:** KEEP metadata.py

## Callers

| File | Usage | Verdict |
|------|-------|---------|
| `tools/production/script_analysis.py` | `MetadataGenerator` in `generate_metadata()` — core orchestration | (b) neutral — already the seam |
| `tools/production/synthesis_engine.py` (×2) | `MetadataGenerator()._apply_tone_filter()` + `._extract_hook()` — **private APIs** | (c) increases complexity |
| `tools/production/parser.py` (`__main__`) | CLI output mode only | (b) neutral |
| `tools/production/__init__.py` | Re-export for backward compat | N/A |

## Reasoning

`synthesis_engine.py` calls two private methods (`_apply_tone_filter`, `_extract_hook`) that belong to metadata generation logic.
Inlining them into `ScriptAnalysis` would spread private API coupling and inflate the seam class.

2/3 non-trivial callers are verdict **(c)**. Below the 70% inline threshold.

## Decision

Keep `metadata.py`. The module earns its place as a standalone class with unique private API (`_apply_tone_filter`, `_extract_hook`) used by `synthesis_engine.py` for title/description work that is separate from the main script analysis seam.
