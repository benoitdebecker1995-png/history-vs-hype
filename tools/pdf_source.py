"""
PDF source access — the one place this repo opens a PDF.

"Primary sources ON SCREEN" is the channel's stated competitive advantage, yet
before 2026-07-31 not a single module imported a PDF library. Every exhibit ever
produced (the 25 Bengal War Cabinet pages, the Vichy translation scans) was
rendered ad hoc in a throwaway session and left nothing reusable behind.

This is a cross-package seam, in the same slot as `tools/subtitles.py` and
`tools/title_features.py`: `tools/production/exhibits.py` renders on-screen
exhibits with it, and `tools/preflight/citation_check.py` verifies quotes with
it. Neither owns a second PDF wrapper.

Page numbering: every public function takes a **1-based** page number, because
that is what a citation says ("p. 42"). PyMuPDF is 0-based internally; the
conversion happens here exactly once.

Error contract (read side): never raises for a missing file, an unreadable PDF
or an out-of-range page — returns None or an empty result. A citation check that
crashes on a bad path tells you nothing about the citation.

CLI:
    python -m tools.pdf_source text  <file.pdf> --page 42
    python -m tools.pdf_source find  <file.pdf> "verbatim phrase"
"""

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Rendering default. 200 DPI on a typical A4/letter scan is ~1700px wide — enough
# for a 1920-wide frame with room to crop, without producing 20 MB exhibit files.
DEFAULT_DPI = 200


# Fuzzy-match floor. Measured on the #66 corpus: a true quote whose page OCR
# reads "at the end -of november 1942" scores 98.9, while a sentence genuinely
# absent from the same page scores 58.3. 90 sits in the gap with room either way.
FUZZY_FLOOR = 90.0


@dataclass(frozen=True)
class Hit:
    """One occurrence of a search phrase."""
    page: int          # 1-based, as a citation would write it
    snippet: str       # surrounding text, for eyeballing the match
    score: float = 100.0   # 100 = exact; lower = matched through OCR noise

    @property
    def exact(self) -> bool:
        return self.score >= 100.0


def _open(pdf_path):
    """Open a PDF, or return None. Import is function-local so importing this
    module (e.g. from a fast linter) does not pull in PyMuPDF."""
    path = Path(pdf_path)
    if not path.is_file():
        logger.warning("PDF not found: %s", path)
        return None
    try:
        import fitz  # PyMuPDF
        return fitz.open(str(path))
    except ImportError:
        logger.warning("PyMuPDF not installed — pip install -e .[documents]")
        return None
    except Exception as exc:
        logger.warning("Could not open %s: %s", path.name, exc)
        return None


def page_count(pdf_path) -> int:
    doc = _open(pdf_path)
    if doc is None:
        return 0
    try:
        return doc.page_count
    finally:
        doc.close()


def page_text(pdf_path, page: int) -> Optional[str]:
    """Text of a 1-based page. None if the file or page does not exist."""
    doc = _open(pdf_path)
    if doc is None:
        return None
    try:
        if not 1 <= page <= doc.page_count:
            logger.warning("page %d out of range (1..%d) in %s",
                           page, doc.page_count, Path(pdf_path).name)
            return None
        return doc[page - 1].get_text()
    except Exception as exc:
        logger.warning("Could not read page %d of %s: %s", page, pdf_path, exc)
        return None
    finally:
        doc.close()


def normalise(text: str) -> str:
    """Fold the differences a PDF introduces but a human quoting it will not.

    Real academic PDFs break a quote across lines, use curly quotes and en/em
    dashes, and insert ligatures. A verbatim quote typed from the page will not
    match byte-for-byte, and a checker that demands that would reject true
    citations — the worst possible failure for this tool, since it would train
    the user to ignore it.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-"), ("‐", "-"), ("­", "")):
        text = text.replace(a, b)
    # Markdown emphasis. Research files quote WITH formatting —
    # "**Less than one-third, however, of the Indian demand...**" is a real line
    # from #66, and on 2026-07-31 the `**` alone made a TRUE citation report as
    # NOT_FOUND (the passage is on top4.pdf p.265). The PDF side never carries
    # these, so stripping both sides is safe.
    text = re.sub(r"[*_`]+", "", text)
    text = re.sub(r"\s+", " ", text)          # line breaks inside a quote
    return text.casefold().strip()


# Academic quoting elides: "an import of 50,000 tons… maintained for a year."
# Such a quote is never contiguous in the source, so each fragment is matched
# separately and a page must contain them all.
ELLIPSIS = re.compile(r"\s*(?:\.{3}|…)\s*")


def split_elision(quote: str) -> List[str]:
    """Fragments of an elided quote. A single-element list when there is no
    elision. Fragments under 4 words are dropped — they match everywhere."""
    parts = [p.strip() for p in ELLIPSIS.split(quote or "")]
    kept = [p for p in parts if len(p.split()) >= 4]
    return kept or ([quote] if quote else [])


def find_text(pdf_path, needle: str, max_hits: int = 25,
              fuzzy: bool = True, threshold: float = FUZZY_FLOOR) -> List[Hit]:
    """Every page whose text contains `needle` (normalised comparison).

    Searches the WHOLE document, not one page, because the useful answer to "is
    this quote on p. 42" is often "no — it is on p. 41".

    Exact matches are returned when they exist. Only if there are none does a
    fuzzy pass run, so a clean source never pays for OCR tolerance and a hit's
    `score` says which kind of match it was.
    """
    doc = _open(pdf_path)
    if doc is None or not (needle or "").strip():
        if doc is not None:
            doc.close()
        return []
    fragments = [normalise(f) for f in split_elision(needle)]
    fragments = [f for f in fragments if f]
    if not fragments:
        doc.close()
        return []
    hits: List[Hit] = []
    pages: List[str] = []
    try:
        for idx in range(doc.page_count):
            try:
                flat = normalise(doc[idx].get_text())
            except Exception:
                flat = ""
            pages.append(flat)
            if not flat:
                continue
            # Every fragment of an elided quote must be on the same page.
            positions = [flat.find(f) for f in fragments]
            if any(p == -1 for p in positions):
                continue
            pos, span = min(positions), len(fragments[0])
            start, end = max(0, pos - 60), min(len(flat), pos + span + 60)
            hits.append(Hit(page=idx + 1, snippet=flat[start:end]))
            if len(hits) >= max_hits:
                break
    finally:
        doc.close()

    if hits or not fuzzy:
        return hits
    return _fuzzy_scan(pages, fragments, threshold, max_hits)


def _fuzzy_scan(pages, fragments, threshold: float, max_hits: int) -> List[Hit]:
    """Second pass for OCR noise. Only runs when the exact pass found nothing.

    Scanned 1940s documents are the norm here, not the exception: the Famine
    Inquiry Commission's own OCR renders "boats" as "boots" and splits "end of"
    into "end -of". Exact matching alone would report those true citations as
    NOT_FOUND, and a checker that rejects real citations gets ignored.
    """
    try:
        from rapidfuzz import fuzz
    except ImportError:
        logger.debug("rapidfuzz not installed — exact matching only")
        return []

    out: List[Hit] = []
    for idx, flat in enumerate(pages):
        if not flat:
            continue
        scores = [fuzz.partial_ratio(f, flat) for f in fragments]
        worst = min(scores)
        if worst < threshold:
            continue
        anchor = flat.find(fragments[0][:20])
        start = max(0, anchor - 60) if anchor != -1 else 0
        out.append(Hit(page=idx + 1, snippet=flat[start:start + 200], score=round(worst, 1)))
        if len(out) >= max_hits:
            break
    return out


def render_page(pdf_path, page: int, out_path, dpi: int = DEFAULT_DPI) -> Optional[Path]:
    """Render a 1-based page to PNG. Returns the path written, or None."""
    doc = _open(pdf_path)
    if doc is None:
        return None
    try:
        if not 1 <= page <= doc.page_count:
            logger.warning("page %d out of range (1..%d)", page, doc.page_count)
            return None
        import fitz
        pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(out))
        return out
    except Exception as exc:
        logger.warning("Could not render page %d of %s: %s", page, pdf_path, exc)
        return None
    finally:
        doc.close()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Read and render pages from a source PDF.",
        epilog=("Examples:\n"
                "  python -m tools.pdf_source text report.pdf --page 42\n"
                '  python -m tools.pdf_source find report.pdf "shortage of grain"\n'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("text", help="print the text of one page")
    t.add_argument("pdf"); t.add_argument("--page", type=int, required=True)
    f = sub.add_parser("find", help="find which pages contain a phrase")
    f.add_argument("pdf"); f.add_argument("phrase")
    for p in (t, f):
        g = p.add_mutually_exclusive_group()
        g.add_argument("--verbose", "-v", action="store_true")
        g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(getattr(args, "verbose", False), getattr(args, "quiet", False))

    if args.cmd == "text":
        text = page_text(args.pdf, args.page)
        if text is None:
            print("could not read that page")
            return 1
        print(text)
        return 0

    hits = find_text(args.pdf, args.phrase)
    if not hits:
        print(f'not found in {Path(args.pdf).name}: "{args.phrase[:60]}"')
        return 1
    print(f"found on {len(hits)} page(s): {', '.join(str(h.page) for h in hits)}")
    for h in hits[:5]:
        print(f"  p.{h.page}: …{h.snippet}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
