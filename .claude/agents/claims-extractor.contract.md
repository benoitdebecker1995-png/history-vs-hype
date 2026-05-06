# Contract: claims-extractor

**Version locked:** 2026-05-05  
**Agent file:** `.claude/agents/claims-extractor.md`  
**Assigned model:** Haiku (per `.brain/methodology/gemini-routing.md`)  

---

## Input shape

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `source_material` | string | YES | `"[Full video transcript or article text]"` |
| `source_type` | enum: `video` \| `article` \| `book` | YES | `"video"` |
| `source_title` | string | YES | `"Pax Tube: Why The Crusades Were Awesome"` |
| `project_path` | string | NO | `"video-projects/_IN_PRODUCTION/55-crusades-check-2026"` |

**Caller:** `.claude/agents/fact-checker.md` (for source analysis) or direct via `/verify` command.

---

## Output shape

**File written to:** `{project_path}/_research/01-EXTRACTED-CLAIMS.md` (if project_path provided)  
**Fallback:** `CLAIMS-TO-VERIFY.md` in current directory.

**Required H2 sections (exact strings — schema contract):**

```
## SOURCE METADATA
## THESIS SUMMARY
## CLAIM CATEGORIZATION
## CHRONOLOGICAL CLAIM MAP
## STATISTICAL & QUANTITATIVE CLAIMS
## QUOTES & ATTRIBUTIONS
## CAUSE-EFFECT ASSERTIONS
## MAJOR OMISSIONS (What is missing?)
## VERIFICATION PRIORITY
## PRELIMINARY RED FLAGS
## NOTEBOOKLM RESEARCH PROMPTS
## RECOMMENDED NEXT STEPS
```

**Required header block:**
```
# Claims to Verify: [Source Title]

**Generated:** [date]
**Source Type:** [Format]
**Total Claims:** [N]
**Priority level:** [High/Medium/Low]
```

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| `fact-checker` | `01-EXTRACTED-CLAIMS.md` | Populates the verification grid with raw claims to be checked. |
| `research-organizer` | Same file | Maps claims to specific academic sources during Phase 2. |

**Breaking change definition:** Missing any required H2 section or failure to extract specific timestamps for video sources.

---

## Canonical baseline

**Source:** YouTube Transcript (12 mins).  
**Result:** 24 claims extracted, 3 "Critical" red flags identified regarding primary source misinterpretation.
