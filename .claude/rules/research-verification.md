---
paths:
  - "**/01-VERIFIED-RESEARCH.md"
  - "**/03-FACT-CHECK-*.md"
  - "**/_research/**"
  - "research/**"
---

# Research and fact-checking

Loaded only when research or fact-check files are open. Moved out of CLAUDE.md 2026-07-31 — rules
unchanged.

## Two-phase approach (CRITICAL)

**Phase 1: Internet research** — map landscape, identify claims to verify (Wikipedia, news, Google Scholar). All findings marked ❓. Free, 2-4 hours.

**Phase 2: NotebookLM academic verification** — university press books ONLY (Cambridge, Oxford, etc.), top scholars, critical editions. Budget UNLIMITED. Upload 10-20 sources, use citation grounding for exact page numbers. Output: verified quotes ready for script.

**NEVER skip Phase 2.** That's the competitive advantage. See: `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

## Source hierarchy

See `.claude/REFERENCE/fact-checking-protocol.md`
- Tier 1: Primary documents, peer-reviewed (2010+), expert historians
- Tier 2: Journalists, intl org reports, declassified docs
- Tier 3: News sources (verify multiple), documentary evidence

**Red flags requiring immediate verification:**
- "The court ruled X..." → Which paragraph? Exact quote?
- "The treaty says..." → Which article? Exact language?
- Any quote without page number → Verify with primary source

**NEVER include unverified claims.** If you can't verify: don't include it, flag it, or ask user for source.

See: `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` for 8 anti-oversimplification rules

## Claim status is graded, not binary

`ASSERTED → SOURCED → INSPECTED → CORROBORATED/CONTESTED → SETTLED`. Verdict words
(REFUTED/PROVEN/RESOLVED) only at CORROBORATED+. Check with
`python -m tools.preflight.claim_status <file.md>`; `--frontier` says whether research is actually
finished. ADR-0021.

**Never assert absence without a direct check.** A search returning nothing proves nothing. If an ID
or URL was supplied, query THAT. ADR-0020.

**Intellectual honesty** — acknowledge what the opposing side gets right. Single source of truth is
`01-VERIFIED-RESEARCH.md`. Gate: 90% verified before writing; 100% cross-checked before filming.
