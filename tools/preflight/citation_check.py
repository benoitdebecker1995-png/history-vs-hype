"""
Citation faithfulness — open the source and check the quote is really there.

`claim_status.py` R3 enforces that an INSPECTED-or-above claim *has* a locator.
It cannot check the locator is TRUE — it never opens the source. So INSPECTED
("we opened the source and read the passage") has always been an honour system.
This makes it machine-checkable, which is the natural next rung under ADR-0021.

What it catches, in order of how often it bites:

  WRONG_PAGE  the quote exists in the document but on a different page. The most
              common real citation error, and the most damaging: it survives
              every text-only check and only fails when a viewer looks it up.
  NOT_FOUND   the quote is not in the document at all — paraphrase presented as
              verbatim, or a quote attributed to the wrong source.
  VERIFIED    the quote is on the cited page.

Two things it deliberately does NOT do:

1. It does not fail a citation for whitespace, curly quotes, ligatures or a line
   break inside the quote. `pdf_source.normalise` folds those. A checker that
   rejected true citations would be trained away in a week.
2. It does not treat a bare "p. 26" as a PDF page index. Academic PDFs are
   routinely offset from their printed page numbers — #66 cites "(pdf p.32,
   printed p.26)" for one passage. A bare page number is reported as
   PAGE_UNKNOWN with the pages the quote WAS found on, rather than failed.
   Write `pdf p.N` when you mean the PDF index and the check becomes exact.

CLI:
    python -m tools.preflight.citation_check <file.md>
    python -m tools.preflight.citation_check <file.md> --documents path/to/pdfs
    python -m tools.preflight.citation_check <file.md> --json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from tools.logging_config import get_logger, setup_logging
from tools.pdf_source import find_text

logger = get_logger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]

def quotes_in(line: str) -> List[str]:
    """Quoted spans on a line, correctly paired.

    A naive `"([^"]+)"` findall is wrong on a line with two quotes: after
    consuming `"q1"` it matches the text BETWEEN the quotes as if it were the
    next one. That produced garbage findings like
    `" (synthesis from operational records). Kamen p. 240: "` on first run.
    Splitting on the delimiter pairs them properly — odd indices are inside.
    """
    parts = line.split('"')
    if len(parts) < 3:
        return []
    return [p for p in parts[1::2] if 25 <= len(p) <= 400]

# "pdf p.32" / "pdf page 32" — an explicit PDF index, checkable exactly.
PDF_PAGE = re.compile(r"\bpdf\s+p(?:age|p?)?\.?\s*(\d+)", re.I)
# "p. 26" / "pp. 188-189" — ambiguous: printed page or PDF index, unknowable.
ANY_PAGE = re.compile(r"\bpp?\.\s*(\d+)", re.I)

MIN_WORDS = 5

# "Kamen p. 188" / "Homza pp. 61-68" — the surname immediately before a page ref
# is the cited work, and that is enough to tell whether we even hold the source.
CITED_SOURCE = re.compile(r"\b([A-Z][a-zà-ÿ]{2,20})\s+pp?\.\s*\d+")


def _cited_source(line: str) -> Optional[str]:
    m = CITED_SOURCE.search(line)
    return m.group(1) if m else None


@dataclass
class Result:
    line: int
    verdict: str            # VERIFIED | WRONG_PAGE | PAGE_UNKNOWN | NOT_FOUND
    quote: str
    cited_page: Optional[int]
    found_pages: List[int]
    document: Optional[str]
    detail: str


def _documents(explicit, md_path: Path) -> List[Path]:
    """PDFs to search. Defaults to the project's own _research/documents/."""
    if explicit:
        base = Path(explicit)
        return sorted(base.rglob("*.pdf")) if base.is_dir() else [base]
    for cand in (md_path.parent / "_research" / "documents",
                 md_path.parent / "_research",
                 md_path.parent / "documents"):
        if cand.is_dir():
            found = sorted(cand.rglob("*.pdf"))
            if found:
                return found
    return []


def check_file(md_path, documents=None, max_quotes: int = 0) -> List[Result]:
    """Verify every quote+locator pair in a markdown file. Never raises."""
    md = Path(md_path)
    if not md.is_file():
        logger.warning("not a file: %s", md)
        return []

    pdfs = _documents(documents, md)
    if not pdfs:
        logger.warning("no source PDFs found for %s — nothing to check against", md.name)
        return []
    logger.info("checking against %d PDF(s)", len(pdfs))

    results: List[Result] = []
    for n, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for quote in quotes_in(line):
            if len(quote.split()) < MIN_WORDS:
                continue

            pdf_hit = PDF_PAGE.search(line)
            any_hit = ANY_PAGE.search(line)
            cited = int(pdf_hit.group(1)) if pdf_hit else (
                int(any_hit.group(1)) if any_hit else None)
            exact = pdf_hit is not None

            where, doc_name = [], None
            for pdf in pdfs:
                hits = find_text(pdf, quote)
                if hits:
                    where = [h.page for h in hits]
                    doc_name = pdf.name
                    break

            if not where:
                # Distinguish "the quote is wrong" from "that book is not here".
                # On the first real run, 8 quotes citing Kamen/Homza/Argüello were
                # reported as possible fabrication when the folder held exactly one
                # unrelated PDF. Accusing a correct citation is how a checker gets
                # ignored, so name the likelier cause when the source is absent.
                cited_name = _cited_source(line)
                have_it = cited_name and any(
                    cited_name.lower() in p.name.lower() for p in pdfs)
                if cited_name and not have_it:
                    verdict = "SOURCE_ABSENT"
                    detail = (f"cites '{cited_name}', which is not among the "
                              f"{len(pdfs)} PDF(s) here — cannot verify, not a failure")
                else:
                    verdict = "NOT_FOUND"
                    detail = (f"quote not found in the {len(pdfs)} PDF(s) present — "
                              "check for paraphrase-as-verbatim or a wrong attribution")
            elif cited is None:
                verdict, detail = "PAGE_UNKNOWN", f"no page cited; quote is on p.{where[0]}"
            elif not exact:
                verdict = "VERIFIED" if cited in where else "PAGE_UNKNOWN"
                detail = ("printed-page citation matches the PDF index"
                          if cited in where else
                          f"cited p.{cited} is not a PDF index for this quote "
                          f"(found on {where}); if that was a PRINTED page this may be "
                          f"correct — write 'pdf p.N' to make it checkable")
            elif cited in where:
                verdict, detail = "VERIFIED", f"quote is on pdf p.{cited}"
            else:
                verdict, detail = "WRONG_PAGE", (
                    f"cited pdf p.{cited}, but the quote is on {where}")

            results.append(Result(
                line=n, verdict=verdict, quote=quote[:90],
                cited_page=cited, found_pages=where, document=doc_name, detail=detail,
            ))
            if max_quotes and len(results) >= max_quotes:
                return results
    return results


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verify quoted passages really appear in the cited source PDFs.",
        epilog=("Examples:\n"
                "  python -m tools.preflight.citation_check 01-VERIFIED-RESEARCH.md\n"
                "  python -m tools.preflight.citation_check FILE.md --documents _research/documents\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("file")
    ap.add_argument("--documents", help="PDF file or directory (default: the project's _research/documents/)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N quotes (0 = all)")
    ap.add_argument("--json", action="store_true")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verbose", "-v", action="store_true")
    g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    results = check_file(args.file, args.documents, args.limit)

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        if not results:
            print("citation_check: no checkable quote+locator pairs found")
            return 0
        counts = {}
        for r in results:
            counts[r.verdict] = counts.get(r.verdict, 0) + 1
        print(f"citation_check: {len(results)} quote(s) — " +
              " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
        for r in results:
            if r.verdict == "VERIFIED":
                continue
            print(f"  L{r.line} [{r.verdict}] {r.detail}")
            print(f'      "{r.quote}…"' + (f"  ({r.document})" if r.document else ""))

    # Only a provably wrong page is a failure. NOT_FOUND is often a quote from a
    # source that simply is not in the folder, and PAGE_UNKNOWN is usually a
    # printed-page citation — neither should block on this evidence alone.
    return 1 if any(r.verdict == "WRONG_PAGE" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
