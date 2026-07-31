"""
On-screen exhibits — render a source page and its provenance caption.

"Primary sources ON SCREEN" is the channel's non-negotiable, and until now every
exhibit was rendered by hand in a throwaway session. The 25 Bengal War Cabinet
pages took a bespoke script that was never committed; nothing about it was
reusable, and nothing recorded WHICH page of WHICH document each PNG came from
once the session ended.

This produces both halves together: the image, and a caption line carrying the
document, the page, and the quote the page is on screen to support. The caption
is the part that was always lost, and it is what makes an exhibit checkable
later by `tools/preflight/citation_check.py`.

CLI:
    python -m tools.production.exhibits render report.pdf --page 156 \\
        --out _research/exhibits/warcabinet-4aug1943.png \\
        --quote "the shortage of grain in India was not the result of physical deficiency"

    python -m tools.production.exhibits locate report.pdf \\
        --quote "the shortage of grain in India"     # which page is it on?
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from tools.logging_config import get_logger, setup_logging
from tools.pdf_source import DEFAULT_DPI, find_text, page_text, render_page

logger = get_logger(__name__)


def caption(pdf_path, page: int, quote: Optional[str] = None) -> str:
    """One-line provenance for an exhibit. This is what stops a PNG becoming an
    anonymous image three months later."""
    name = Path(pdf_path).name
    base = f"{name} — pdf p.{page}"
    return f'{base} — "{quote.strip()}"' if quote else base


def build(pdf_path, page: Optional[int] = None, out_path=None,
          quote: Optional[str] = None, dpi: int = DEFAULT_DPI) -> dict:
    """Render one exhibit. Returns {'png','caption','page'} or {'error': ...}.

    If `page` is omitted and a `quote` is given, the page is located from the
    quote — which is the normal case: you know the sentence you want on screen,
    not its page number.
    """
    if page is None:
        if not quote:
            return {"error": "need either --page or --quote"}
        hits = find_text(pdf_path, quote)
        if not hits:
            return {"error": f"quote not found in {Path(pdf_path).name}; "
                             "check wording, or the document may be image-only (needs OCR)"}
        if len({h.page for h in hits}) > 1:
            logger.warning("quote appears on pages %s — using the first",
                           [h.page for h in hits])
        page = hits[0].page

    if quote:
        # An exhibit whose quote is not on the rendered page is worse than no
        # exhibit: it is a document shown as proof of something it does not say.
        on_page = page_text(pdf_path, page)
        if on_page is None:
            return {"error": f"could not read page {page} of {Path(pdf_path).name}"}
        from tools.pdf_source import normalise
        if normalise(quote) not in normalise(on_page):
            found = [h.page for h in find_text(pdf_path, quote)]
            return {"error": f"quote is NOT on page {page}" +
                             (f" — it is on {found}" if found else " (not in this document)")}

    out = Path(out_path) if out_path else Path(
        f"{Path(pdf_path).stem}-p{page}.png")
    written = render_page(pdf_path, page, out, dpi)
    if written is None:
        return {"error": f"render failed for page {page}"}
    return {"png": str(written), "caption": caption(pdf_path, page, quote), "page": page}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render a source page as an on-screen exhibit, with provenance.",
        epilog=("Examples:\n"
                "  python -m tools.production.exhibits locate report.pdf --quote \"...\"\n"
                "  python -m tools.production.exhibits render report.pdf --quote \"...\" --out ex.png\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render", help="render a page to PNG")
    r.add_argument("pdf")
    r.add_argument("--page", type=int, help="1-based PDF page (omit to locate by --quote)")
    r.add_argument("--out", help="output PNG path")
    r.add_argument("--quote", help="the passage this exhibit is on screen to support")
    r.add_argument("--dpi", type=int, default=DEFAULT_DPI)

    l = sub.add_parser("locate", help="find which page holds a passage")
    l.add_argument("pdf")
    l.add_argument("--quote", required=True)

    for p in (r, l):
        g = p.add_mutually_exclusive_group()
        g.add_argument("--verbose", "-v", action="store_true")
        g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    if args.cmd == "locate":
        hits = find_text(args.pdf, args.quote)
        if not hits:
            print("not found — check wording, or the PDF may be image-only (needs OCR)")
            return 1
        for h in hits[:5]:
            print(f"pdf p.{h.page}: …{h.snippet}…")
        return 0

    result = build(args.pdf, args.page, args.out, args.quote, args.dpi)
    if "error" in result:
        print(f"exhibit failed: {result['error']}")
        return 1
    print(f"wrote {result['png']}")
    print(f"caption: {result['caption']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
