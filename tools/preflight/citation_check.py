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

from tools.logging_config import get_logger, safe_print, setup_logging
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
    out = []
    for seg in parts[1::2]:
        if not 25 <= len(seg) <= 400:
            continue
        # Parity guard. Odd indices are inside the quotes ONLY if the line
        # starts outside one. Research files wrap quotes in italics and run them
        # across lines -- `imports."* Mansergh's summary describes Wavell *"…` --
        # so a line beginning mid-quote inverts the pairing and the CONNECTIVE
        # prose lands on the odd index instead. Such a segment is bracketed by
        # emphasis markers, which a real quotation is not.
        stripped = seg.strip()
        if stripped.startswith(("*", "_")) and stripped.endswith(("*", "_")):
            continue
        out.append(seg)
    return out

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


WORD = re.compile(r"[A-Za-zÀ-ÿ]{3,}")


def _named_sources(line: str, heading: str, index: dict) -> List[str]:
    """Library keys named by this citation, from the line or its section heading.

    #66 names its sources in headings ("### A2 — THE KEY FINDING … (pdf p.32)")
    and quotes underneath, so scanning the quote line alone resolved nothing and
    every quote came back NOT_FOUND against zero PDFs searched.
    """
    found = []
    for word in WORD.findall(f"{line} {heading}"):
        key = word.casefold()
        if key in index and key not in found:
            found.append(key)
    return found


@dataclass
class Result:
    line: int
    verdict: str            # VERIFIED | WRONG_PAGE | PAGE_UNKNOWN | NOT_FOUND
    quote: str
    cited_page: Optional[int]
    found_pages: List[int]
    document: Optional[str]
    detail: str


LIBRARY_DIR = REPO_ROOT / "library"


def library_index(library=None) -> dict:
    """{surname: [pdf paths]} from the persistent library's filenames.

    `library/` holds 1,600+ PDFs / 23 GB, so scanning it per quote is not an
    option — a 5-PDF run already takes two minutes. The library's own naming
    convention (`TitleWords-Author-Year-Publisher.pdf`) carries the author, and
    a citation says "Behrens p. 240", so the surname resolves a quote to one or
    two files instead of sixteen hundred.
    """
    base = Path(library) if library else LIBRARY_DIR
    index: dict = {}
    if not base.is_dir():
        return index
    # Same parser as the index generator, deliberately: a second copy here drifted
    # immediately -- both took parts[1] as the author and truncated hyphenated
    # surnames (Maddy-Weitzman -> "Maddy"), making 65 books unresolvable.
    from tools.library_index import parse_name
    for pdf in base.rglob("*.pdf"):
        book = parse_name(pdf.stem)
        index.setdefault(book.author.casefold(), []).append(pdf)
        # Hyphenated surnames are cited by either barrel in practice.
        for barrel in book.author.split("-"):
            if len(barrel) > 2:
                index.setdefault(barrel.casefold(), []).append(pdf)
    return index


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


def check_file(md_path, documents=None, max_quotes: int = 0,
               use_library: bool = False) -> List[Result]:
    """Verify every quote+locator pair in a markdown file. Never raises.

    `use_library` additionally resolves each citation against the persistent
    `library/` by the surname it names, so a source does not have to be copied
    into the project to be checkable.
    """
    md = Path(md_path)
    if not md.is_file():
        logger.warning("not a file: %s", md)
        return []

    pdfs = _documents(documents, md)
    index = library_index() if use_library else {}
    if not pdfs and not index:
        logger.warning("no source PDFs found for %s — nothing to check against", md.name)
        return []
    logger.info("checking against %d local PDF(s)%s", len(pdfs),
                f" + library ({sum(len(v) for v in index.values())} indexed)" if index else "")

    results: List[Result] = []
    heading = ""
    for n, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.lstrip().startswith("#"):
            heading = line
        for quote in quotes_in(line):
            if len(quote.split()) < MIN_WORDS:
                continue

            pdf_hit = PDF_PAGE.search(line)
            any_hit = ANY_PAGE.search(line)
            cited = int(pdf_hit.group(1)) if pdf_hit else (
                int(any_hit.group(1)) if any_hit else None)
            exact = pdf_hit is not None

            # Local documents first (small, project-specific), then the library
            # narrowed to the source this citation names.
            candidates = list(pdfs)
            if index:
                # A surname can appear as "Behrens p. 240" on the line, or -- as
                # #66 does throughout -- only in the section heading above the
                # quote ("### A2 ... (pdf p.32)"). Carry the heading down.
                for name in _named_sources(line, heading, index):
                    candidates += index[name]

            where, doc_name, ocr_score = [], None, None
            for pdf in candidates:
                hits = find_text(pdf, quote)
                if hits:
                    where = [h.page for h in hits]
                    doc_name = pdf.name
                    # Scanned sources match through OCR noise; say so rather
                    # than presenting a fuzzy match as an exact one.
                    if not hits[0].exact:
                        ocr_score = hits[0].score
                    break

            if not where and not candidates:
                # Searched nothing, so say nothing. Reporting NOT_FOUND here
                # would accuse a citation whose source was never opened.
                verdict = "UNRESOLVED"
                detail = ("no source could be resolved for this citation — name the "
                          "author on the line or in its heading, or pass --documents")
            elif not where:
                # Distinguish "the quote is wrong" from "that book is not here".
                # On the first real run, 8 quotes citing Kamen/Homza/Argüello were
                # reported as possible fabrication when the folder held exactly one
                # unrelated PDF. Accusing a correct citation is how a checker gets
                # ignored, so name the likelier cause when the source is absent.
                cited_name = _cited_source(line)
                have_it = cited_name and any(
                    cited_name.lower() in p.name.lower() for p in candidates)
                if cited_name and not have_it:
                    verdict = "SOURCE_ABSENT"
                    detail = (f"cites '{cited_name}', which is not among the "
                              f"{len(candidates)} PDF(s) searched — cannot verify, not a failure")
                else:
                    verdict = "NOT_FOUND"
                    detail = (f"quote not found in the {len(candidates)} PDF(s) searched — "
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
                if ocr_score is not None:
                    verdict = "VERIFIED_OCR"
                    detail = (f"on pdf p.{cited}, matched through OCR noise "
                              f"({ocr_score}% — the scan is dirty, the citation is not)")
                else:
                    verdict, detail = "VERIFIED", f"quote is on pdf p.{cited}"
            elif len(where) > 1:
                # The passage appears on several pages -- a section heading in
                # both the contents and the body, a running head, an index entry.
                # "Wrong page" is then not provable: the cited page may hold a
                # further occurrence the OCR lost. Report, do not fail.
                verdict = "PAGE_UNKNOWN"
                detail = (f"cited pdf p.{cited}; the passage appears on {where} — "
                          "repeated text (heading/index), so the page cannot be adjudicated")
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
    ap.add_argument("--library", action="store_true",
                    help="also resolve citations against the persistent library/ by author surname")
    ap.add_argument("--limit", type=int, default=0, help="stop after N quotes (0 = all)")
    ap.add_argument("--json", action="store_true")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verbose", "-v", action="store_true")
    g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    results = check_file(args.file, args.documents, args.limit, use_library=args.library)

    # safe_print, not print: the failure lines below echo verbatim quotes lifted from
    # the source PDFs, and this CLI's exit code is a gate (1 == WRONG_PAGE). A quote
    # containing a character the console codepage lacks must not read as a bad page.
    if args.json:
        safe_print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        if not results:
            safe_print("citation_check: no checkable quote+locator pairs found")
            return 0
        counts = {}
        for r in results:
            counts[r.verdict] = counts.get(r.verdict, 0) + 1
        safe_print(f"citation_check: {len(results)} quote(s) — " +
                   " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
        for r in results:
            if r.verdict == "VERIFIED":
                continue
            safe_print(f"  L{r.line} [{r.verdict}] {r.detail}")
            safe_print(f'      "{r.quote}…"' + (f"  ({r.document})" if r.document else ""))

    # Only a provably wrong page is a failure. NOT_FOUND is often a quote from a
    # source that simply is not in the folder, and PAGE_UNKNOWN is usually a
    # printed-page citation — neither should block on this evidence alone.
    return 1 if any(r.verdict == "WRONG_PAGE" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
