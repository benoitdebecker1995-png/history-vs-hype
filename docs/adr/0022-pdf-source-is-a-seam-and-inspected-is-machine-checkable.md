# ADR-0022 — `pdf_source` is a seam, and INSPECTED becomes machine-checkable

**Date:** 2026-07-31 · **Status:** Accepted · **Supersedes:** nothing · **Extends:** ADR-0021

## Context

"Primary sources ON SCREEN" and "real quotes with page numbers" are the channel's stated
competitive advantage. Two things were true anyway:

1. **No module in this repo opened a PDF.** `grep` across `tools/` found zero imports of any PDF
   library on 2026-07-31, while 71 source PDFs sat in `video-projects/`. Every exhibit ever
   produced — the 25 Bengal War Cabinet pages, the Vichy scans — was rendered by a throwaway
   script in a session that ended, leaving the PNGs but no way to regenerate them and no record of
   which page of which document each came from.

2. **`INSPECTED` was an honour system.** ADR-0021's ladder defines it as "we opened the source and
   read the passage", and `claim_status.py` R3 enforces that such a claim *has* a locator. It
   cannot check the locator is *true*, because it never opens the source. A citation can name a
   real book, a plausible page, and a quote that is on a different page — or in no book at all —
   and pass every check this repo has.

The second is the more dangerous: a wrong page survives every text-only gate and fails only when a
viewer looks it up.

## Decision

**One seam, two consumers, and a new dependency extra.**

`tools/pdf_source.py` is the only place this repo opens a PDF. It sits in the top-level
cross-package slot alongside `tools/subtitles.py` and `tools/title_features.py`, because both a
`production/` tool and a `preflight/` tool need it and neither should own the wrapper (a
`preflight` module importing from `production` would be the wrong direction).

- `tools/production/exhibits.py` — renders a page as an on-screen exhibit **plus a provenance
  caption**. The caption is the half that was always lost.
- `tools/preflight/citation_check.py` — opens the cited source and verifies the quote is on the
  cited page. This is what makes `INSPECTED` checkable.

`pymupdf` is declared in a new `[documents]` extra, not core: `pdf_source` logs and returns
`None`/`[]` when it is missing, so the rest of the repo is unaffected and the tests skip.

### Three deliberate constraints

**Page numbers are 1-based at every public boundary**, because that is what a citation says.
PyMuPDF is 0-based; the conversion happens once, inside the seam.

**Normalisation is generous.** A quote typed from a page will never match a PDF byte-for-byte —
PDFs break lines mid-sentence, use curly quotes, ligatures and en dashes. `normalise()` folds all
of it. A checker that rejected *true* citations would be trained away within a week, which is a
worse outcome than not having one.

**A bare page number is not treated as a PDF index.** Academic PDFs are routinely offset from their
printed page numbers — #66 cites "(pdf p.32, printed p.26)" for a single passage. A bare `p. 26` is
reported as `PAGE_UNKNOWN` with the pages the quote *was* found on, never as a failure. Write
`pdf p.N` and the check becomes exact.

### Verdicts, and what gates

| Verdict | Meaning | Exit 1? |
|---|---|---|
| `VERIFIED` | quote is on the cited PDF page | no |
| `WRONG_PAGE` | quote is in the document, on a **different** page | **yes** |
| `NOT_FOUND` | quote is in none of the PDFs present | no |
| `SOURCE_ABSENT` | the cited work is not in the folder — cannot verify | no |
| `PAGE_UNKNOWN` | bare page number; reports where the quote actually is | no |

Only `WRONG_PAGE` fails, because only `WRONG_PAGE` is *provably* wrong from the evidence to hand.
`NOT_FOUND` and `SOURCE_ABSENT` usually mean the book simply is not in `_research/documents/`.

## Consequences

- `INSPECTED` can now be *demonstrated* rather than asserted, closing the gap ADR-0021 left open.
- Exhibits are reproducible and self-describing; `exhibits.py` refuses to render a page that does
  not contain the quote it is being rendered to support.
- A new pip dependency, isolated behind an extra and a graceful-degradation path.
- **Not built:** OCR. An image-only PDF yields no text and reports "not found — may need OCR".
  Adding OCR means tesseract, a much heavier dependency, and it should be a separate decision made
  when a real source forces it.

## First-run findings (why two behaviours exist)

Run against published research before the tests were written, and both fixes are pinned by
regression tests:

- On a line with two quotes, a naive `"([^"]+)"` findall consumed the first quote and then matched
  the text *between* the quotes as the second, producing findings like
  `" (synthesis from operational records). Kamen p. 240: "`. Quotes are now paired by splitting on
  the delimiter.
- Eight quotes citing Kamen, Homza and Argüello were reported as possible fabrication when the
  folder held exactly one unrelated PDF. `SOURCE_ABSENT` now separates "we do not hold that book"
  from "that quote is wrong" — accusing a correct citation is how a checker gets ignored.
