# Verified Workflow - Quick Reference

**Last Updated:** 2026-01-22
**Purpose:** Zero-error scriptwriting workflow for History vs Hype videos

---

## THE PROBLEM WE SOLVED

**Old workflow:**
```
Research -> Write -> Fact-check -> Find errors -> Rewrite -> Re-check
Time: 9 hours | Errors: 2+ per video
```

**New workflow:**
```
Research + Verify -> Write from verified facts -> Quick cross-check -> Film
Time: 5.5 hours | Errors: 0
```

---

## QUICK START: YOUR NEXT VIDEO

### Phase 1: Research + Verify (3-4 hours)

```
/research --new     # Create project structure
```

**File:** `01-VERIFIED-RESEARCH.md` (single source of truth)

As you research in NotebookLM, verify each fact:
- ✅ VERIFIED - Ready for script
- ⏳ RESEARCHING - Still checking
- ❌ UNVERIFIABLE - Don't use

**Don't proceed until:** 90%+ claims verified

---

### Phase 2: Write Script (1-1.5 hours)

```
/script             # Generate from verified research
```

**File:** `02-SCRIPT-DRAFT.md`

**RULE:** Only use facts from `01-VERIFIED-RESEARCH.md`

If you need a fact that's not verified -> STOP -> Verify it first

---

### Phase 3: Cross-Check (30 minutes)

```
/verify --script    # Cross-check against research
```

**File:** `03-FACT-CHECK-VERIFICATION.md`

Compare every script claim to verified research:
- All quotes word-for-word exact?
- All numbers match?
- All archive refs precise?

**Result:** ✅ APPROVED FOR FILMING or ❌ NEEDS REVISION

---

## COMMAND REFERENCE

| Phase | Command | Purpose |
|-------|---------|---------|
| Pre-production | `/research --new` | Start new project |
| Pre-production | `/sources --recommend` | Source recommendations for NotebookLM |
| Production | `/script` | Generate script from research |
| Production | `/script --teleprompter` | Export for teleprompter |
| Production | `/verify --script` | Fact-check verification |
| Production | `/prep --edit-guide` | Shot-by-shot editing guide |
| Post-production | `/publish --metadata` | YouTube metadata package |
| Post-production | `/fix` | Fix subtitle errors |
| Navigation | `/status` | Where am I? What's next? |
| Navigation | `/help` | Full command list |

---

## THE 3 FILES

### 01-VERIFIED-RESEARCH.md
**Purpose:** Single source of truth for verified facts
**When:** During research phase
**Status:** ✅ VERIFIED, ⏳ RESEARCHING, ❌ UNVERIFIABLE

### 02-SCRIPT-DRAFT.md
**Purpose:** Script written from verified facts
**When:** After 90%+ research verified
**Rule:** Every claim references verified research

### 03-FACT-CHECK-VERIFICATION.md
**Purpose:** Final quality gate before filming
**When:** After script complete
**Goal:** 100% match between script and research

---

## QUALITY GATES

### Gate 1: Research -> Script
- [ ] 90%+ claims verified
- [ ] All quotes word-for-word exact
- [ ] All numbers have 2+ sources

### Gate 2: Script -> Filming
- [ ] 100% claims cross-checked
- [ ] Zero errors found
- [ ] Read-aloud test passed

---

## PREVENTING COMMON ERRORS

### Wrong Archive Reference
```markdown
# In 01-VERIFIED-RESEARCH.md:
**Exact Reference:** HW 16/23
**Common errors:** NOT HW 16/32
```

### Wrong Numbers
```markdown
| Claim | Number | Source | Verified |
|-------|--------|--------|----------|
| Rome deportations | 1,023 | Hofle Telegram | ✅ |
```

### Paraphrased Quotes
```markdown
**Exact text:**
> "About ten thousand were beheaded."
**Verified:** ✅ Word-for-word (Krey 1921)
```

---

## TIME BREAKDOWN

| Old Workflow | New Workflow |
|--------------|--------------|
| Research: 3h | Research + Verify: 4h |
| Write: 2h | Write from verified: 1h |
| Fact-check: 2h | Cross-check: 30min |
| Fix errors: 1h | - |
| Re-check: 1h | - |
| **Total: 9h** | **Total: 5.5h** |

---

## KEY PRINCIPLES

1. **Single Source of Truth** - One research document, not multiple
2. **Verify First, Write Second** - Don't write then fact-check
3. **No Placeholders** - No [QUOTE TK] or [DATA TK] in script
4. **90% Rule** - Wait until 90%+ verified before writing
5. **100% Cross-Check** - Verify every claim before filming

---

## NEED HELP?

```
/status    # See current project state and suggested next action
/help      # See all available commands
```

**For detailed documentation:** See `CLAUDE.md`
