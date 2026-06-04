---
name: Metadata extraction order — cheap signals first
description: Canonical 5-step order for any PDF/document labeling task. Run cheap signals before expensive LLM/web calls.
type: feedback
originSessionId: 2897bf93-7e31-4c8d-a562-25e334835f6e
---
For ANY task that extracts metadata from PDFs (renaming libraries, building citations, classifying sources, labeling files), follow this order:

**1. PDF embedded metadata** (`doc.metadata` via PyMuPDF/pikepdf)
- Free, ~30s for 1000 files.
- Often pre-filled by publisher portals (Brill, Springer, Cambridge, OUP, JSTOR).
- Fields: `Title`, `Author`, `Subject`, `Producer`, `Creator`, `CreationDate`, `Keywords`.
- **Filters required:**
  - Reject user's Windows username (`Benoit De Becker`, `Becker`) — auto-filled by "Microsoft Print to PDF".
  - Reject org/handle placeholders (`Games`, `Service`, `States`, `Resources`, `Lr`, system handles like `Dufp001-lap`, `Unicafpc`, `Zmfr`).
  - Publisher detection MUST use word-boundary regex (`\boup\b`, NOT `oup` — otherwise matches "Group").
  - `CreationDate` year capped at ≤2016 unless title clearly hints at recent pub date — PDF CreationDate is often scan/save date, not publication year.

**2. Filename parsing** (regex on existing filename)
- Free.
- Many academic PDFs from libgen/z-lib/Anna's-Archive have `(Year, Publisher)` or `Author - Title (Year)` patterns in filename.

**3. Manual web-lookup prompt for user** (markdown file with structured entries)
- Builds prompt the user pastes into Gemini/ChatGPT/Perplexity.
- For files where steps 1+2 left fields as Unknown.
- Each entry: known fields + original filename for context.
- Format: markdown table output for easy parse-back.

**4. PDF page-text content extraction** (PyMuPDF first 1-2 pages → LLM)
- Most expensive step (LLM tokens + processing time).
- Only for files where steps 1-3 didn't resolve.
- ~30% of scanned PDFs are image-only (no extractable text) — separate workflow needed (OCR or manual).

**5. Manual review**
- Final pass on residuals.
- User decides what to stash as off-topic, what to keep as-is.

**Why:** I (Claude) ran this in the WRONG order the first time — filename → LLM batches → PDF text extract → user web lookup → finally PDF metadata pass at the very end. The metadata pass should have been step 1: it's free, fast, and resolved 55 fields that LLMs had already burned tokens on (or labeled "Unknown"). Wasted ~3 Haiku batch calls and ~5 Gemini Flash calls.

**How to apply:** When user asks to label/rename/classify any folder of documents, FIRST proposal must be the metadata-first plan. Default to running step 1 immediately; only escalate to LLMs (step 4) for the residual. Origin: 2026-05-12 library Layer 2 rename project.
