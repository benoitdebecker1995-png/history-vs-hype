"""
Triage `library/_stash-needs-id/` — identify what the filename could not.

`auto_rename_books.py` parses FILENAMES (Anna's Archive, Z-Library, libgen
shapes). 341 files defeated it because their names carry no author or title:
archive scan ids (`000199_000009_002585977`), DOIs (`10.2307@27709600`), ICJ case
codes (`061-19751016-ADV-01-00-EN`), bare numbers (`11675.pdf`).

The filename is not the only evidence. Measured 2026-07-31 across the stash:

    99  have BOTH PDF title metadata and readable page-1 text
    58  metadata only
    73  page-1 text only
    43  neither (image-only scans — need OCR, out of scope)
    15  broken: 14 are ZERO BYTES, 1 unreadable

So 84% are recoverable without a human reading them.

The stash is also not a pile of books. It holds treaties, ICJ judgments,
government reports, journal articles and Wikipedia dumps alongside monographs —
for this channel the primary sources are the more valuable half. `kind` records
that rather than forcing everything into the book convention.

The 14 zero-byte files are a separate problem with a different fix: their
filenames are perfect (`[Series] Anita Shapira - Israel: A History (2012,
Brandeis)`), they are simply failed downloads. Renaming them is pointless; they
need re-fetching, so they are quarantined with a list instead.

CLI:
    python -m tools.library_triage                 # report only
    python -m tools.library_triage --quarantine    # move broken files aside
    python -m tools.library_triage --apply         # + rename/file high-confidence
"""

import argparse
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
STASH = REPO_ROOT / "library" / "_stash-needs-id"
BROKEN = REPO_ROOT / "library" / "_stash-broken"
BY_TOPIC = REPO_ROOT / "library" / "by-topic"

# Document kinds, in check order — first match wins, so the specific legal and
# treaty patterns are tested before the generic ones.
KIND_PATTERNS = [
    ("judgment", r"\b(international court of justice|judgment of|advisory opinion|"
                 r"arbitral award|the court, ?\n?unanimously)\b"),
    ("treaty",   r"\b(trait[ée] de|treaty of|convention between|the high contracting parties|"
                 r"protocol to the)\b"),
    ("report",   r"\b(country reports? on|annual report|commission of inquiry|"
                 r"report of the|white paper)\b"),
    ("article",  r"\b(abstract|keywords:|journal of|vol\.\s?\d+,? no\.\s?\d+|doi:)\b"),
    ("wiki",     r"\b(from wikipedia|jump to navigation|\[edit\])\b"),
]

# Junk the PDF metadata title field routinely carries instead of a real title.
BAD_TITLE = re.compile(
    r"^(untitled|microsoft word|document\d*|print|scan|pdfdocument|"
    r".*\.(pdf|docx?|indd|qxd|tex)$|\d[\d\s._-]*)$", re.I)


# Filename shapes that carry MORE than the contents do. An ICJ scan's page 1 says
# "INTERNATIONAL COURT OF JUSTICE" and its PDF creationDate is the digitisation
# year (2017), while `045-19620615-JUD-01-00-EN` states the real date and kind.
ICJ_NAME = re.compile(r"^(\d{3})-(\d{4})(\d{2})(\d{2})-(JUD|ADV|ORD)-", re.I)
FILENAME_YEAR = re.compile(r"\b(1[6-9]\d{2}|20[0-2]\d)\b")

# An OCR-garbage title: too few vowels to be language. `DFOBiHtIS` produced the
# same proposed name for two different Karabakh scans, which would have collided.
def _is_garbage(title: str) -> bool:
    letters = [c for c in title.lower() if c.isalpha()]
    if len(letters) < 4:
        return True
    vowels = sum(c in "aeiouаеиоуыэюя" for c in letters)
    if vowels / len(letters) < 0.2:
        return True
    # Case thrashing inside a single word. Bad OCR of a scanned Cyrillic page
    # produced "DFOBiHtIS" -- which has enough vowels to pass the test above, and
    # named two different Karabakh scans identically. Real words switch case at
    # most once (initial capital); three switches is machine noise.
    for token in re.findall(r"[A-Za-zÀ-ÿ]{4,}", title):
        switches = sum(a.isupper() != b.isupper() for a, b in zip(token, token[1:]))
        if switches >= 3:
            return True
    return False


# Institution names are what a legal scan's first line says; they identify the
# publisher, not the document, and would name every ICJ case identically.
INSTITUTION = re.compile(
    r"^(international court of justice|cour internationale de justice|united nations|"
    r"nations unies|european court|supreme court|house of (commons|lords)|"
    # Series titles name the VOLUME, not the case — every ICJ scan opens with one.
    r"reports? of judgments|recueil des arr[êe]ts|summaries of judgments|"
    r"pleadings, oral arguments)\b", re.I)


@dataclass
class Candidate:
    path: Path
    title: str = ""
    author: str = ""
    year: str = ""
    kind: str = "book"
    evidence: str = ""      # where the metadata came from
    problem: str = ""       # set when the file itself is unusable

    @property
    def confident(self) -> bool:
        """Enough to rename without a human looking. Title AND year at minimum —
        an author-less name cannot be resolved by citation_check, but a titled,
        dated document is still far better than `11675.pdf`."""
        # `_camel` yields "Untitled" when the title has no word characters left
        # after cleaning. Two Karabakh scans both reduced to that and would have
        # been renamed identically — an unnamed file is not an identified one.
        return (bool(self.title) and bool(self.year) and not self.problem
                and _camel(self.title) != "Untitled")


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip(" .,-–—:")
    return text


def _camel(text: str, limit: int = 60) -> str:
    """`The Cultivation of a Nation` -> `TheCultivationOfANation`, matching the
    library's live convention."""
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", text)
    return "".join(w[:1].upper() + w[1:] for w in words)[:limit] or "Untitled"


def classify(text: str) -> str:
    low = (text or "").lower()
    for kind, pattern in KIND_PATTERNS:
        if re.search(pattern, low):
            return kind
    return "book"


def extract(path: Path) -> Candidate:
    """Best-effort identification. Never raises."""
    cand = Candidate(path=path)
    try:
        if path.stat().st_size == 0:
            cand.problem = "zero bytes — failed download, re-fetch it"
            return cand
    except OSError as exc:
        cand.problem = f"unstattable: {exc}"
        return cand

    if path.suffix.lower() != ".pdf":
        cand.problem = f"not a PDF ({path.suffix})"
        return cand

    try:
        import fitz
        doc = fitz.open(str(path))
    except Exception as exc:
        cand.problem = f"unreadable: {str(exc)[:60]}"
        return cand

    try:
        meta = doc.metadata or {}
        text = ""
        for i in range(min(3, doc.page_count)):
            try:
                text += doc[i].get_text() + "\n"
            except Exception:
                continue
    finally:
        doc.close()

    def _usable(t: str) -> bool:
        return (bool(t) and len(t) > 8 and not BAD_TITLE.match(t)
                and not INSTITUTION.match(t) and not _is_garbage(t))

    m_title = _clean(meta.get("title", ""))
    if _usable(m_title):
        cand.title, cand.evidence = m_title, "pdf-metadata"
    else:
        # First substantial line of the title page that is not the issuing body.
        for line in (l.strip() for l in text.splitlines()):
            line = _clean(line)
            if _usable(line) and not line.isdigit():
                cand.title, cand.evidence = line, "page-1-text"
                break

    m_author = _clean(meta.get("author", ""))
    if m_author and len(m_author) < 60 and not BAD_TITLE.match(m_author):
        cand.author = m_author.split(",")[0].split(" and ")[0].strip()

    # A structured filename beats the contents — see ICJ_NAME.
    icj = ICJ_NAME.match(path.name)
    if icj:
        cand.year = icj.group(2)
        cand.kind = "judgment" if icj.group(5).upper() == "JUD" else "opinion"
        cand.evidence = "filename-icj"
        # Always take the filename's identity here. The series title spans
        # several lines ("REPORTS OF JUDGMENTS / ADVISORY OPINIONS AND ORDERS"),
        # so skipping one line just picks up the next -- and none of them name
        # the case. The case number + date do identify it uniquely.
        cand.title = (f"ICJ {icj.group(5).upper()} {icj.group(2)}-{icj.group(3)}"
                      f"-{icj.group(4)} no{icj.group(1)}")

    if not cand.year:
        # Prefer a year stated in the document or its name. PDF creationDate is
        # the DIGITISATION date on a scan -- it dated a 1962 judgment to 2017.
        from_name = FILENAME_YEAR.search(path.stem)
        years = re.findall(r"\b(1[6-9]\d{2}|20[0-2]\d)\b", text[:3000])
        if years:
            cand.year = Counter(years).most_common(1)[0][0]
        elif from_name:
            cand.year = from_name.group(0)
        else:
            m = re.search(r"(19|20)\d{2}", meta.get("creationDate") or "")
            if m:
                cand.year = m.group(0)
                cand.evidence = (cand.evidence + "+creationDate").lstrip("+")

    if cand.kind == "book":
        cand.kind = classify(text)
    if not cand.title:
        cand.problem = cand.problem or "no title in metadata or page text (image-only? needs OCR)"
    return cand


def proposed_name(c: Candidate) -> str:
    author = _camel(c.author) if c.author else "Unknown"
    year = c.year or "Unknown"
    kind = "" if c.kind == "book" else f"-{c.kind}"
    return f"{_camel(c.title)}-{author}-{year}-Stash{kind}{c.path.suffix.lower()}"


def triage(stash=None) -> List[Candidate]:
    base = Path(stash) if stash else STASH
    if not base.is_dir():
        logger.warning("no stash at %s", base)
        return []
    return [extract(f) for f in sorted(base.iterdir()) if f.is_file()]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Identify files in library/_stash-needs-id/ from their contents.",
        epilog=("Examples:\n"
                "  python -m tools.library_triage\n"
                "  python -m tools.library_triage --quarantine\n"
                "  python -m tools.library_triage --apply\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--quarantine", action="store_true",
                    help="move zero-byte/unreadable files to library/_stash-broken/")
    ap.add_argument("--apply", action="store_true",
                    help="rename confidently-identified files in place (implies --quarantine)")
    ap.add_argument("--limit", type=int, default=0)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verbose", "-v", action="store_true")
    g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    cands = triage()
    if args.limit:
        cands = cands[:args.limit]
    if not cands:
        print("library_triage: nothing to triage")
        return 0

    broken = [c for c in cands if c.problem and "zero bytes" in c.problem or c.problem.startswith("unreadable")]
    confident = [c for c in cands if c.confident]
    partial = [c for c in cands if not c.confident and not c.problem]
    unidentified = [c for c in cands if c.problem and c not in broken]

    kinds = Counter(c.kind for c in confident)
    print(f"library_triage: {len(cands)} files — "
          f"{len(confident)} identified · {len(partial)} partial · "
          f"{len(unidentified)} unidentifiable · {len(broken)} broken")
    print(f"  kinds among identified: {dict(kinds)}")

    if args.quarantine or args.apply:
        BROKEN.mkdir(parents=True, exist_ok=True)
        moved = 0
        for c in broken:
            try:
                shutil.move(str(c.path), str(BROKEN / c.path.name))
                moved += 1
            except OSError as exc:
                logger.warning("could not move %s: %s", c.path.name, exc)
        print(f"  quarantined {moved} broken file(s) -> library/_stash-broken/")
        if moved:
            listing = BROKEN / "REFETCH.md"
            listing.write_text(
                "# Broken downloads — re-fetch these\n\n"
                "Zero-byte or unreadable. Their FILENAMES carry the citation, which is "
                "why they are kept: each line is what to search for again.\n\n"
                + "\n".join(f"- `{c.path.name}` — {c.problem}" for c in broken) + "\n",
                encoding="utf-8")
            print(f"  wrote {listing.relative_to(REPO_ROOT)}")

    if args.apply:
        renamed = 0
        taken = set()
        for c in confident:
            name = proposed_name(c)
            target = c.path.with_name(name)
            if target.exists() or name in taken:
                # Two files proposing one name means the identification is not
                # trustworthy for either. Leave both for a human.
                logger.warning("name collision, skipping: %s", name)
                continue
            taken.add(name)
            try:
                c.path.rename(target)
                renamed += 1
            except OSError as exc:
                logger.warning("could not rename %s: %s", c.path.name, exc)
        print(f"  renamed {renamed} identified file(s) in place")
    else:
        print("\n  sample proposals (dry run — pass --apply):")
        for c in confident[:8]:
            print(f"    {c.path.name[:38]:40} -> {proposed_name(c)[:60]}  [{c.evidence}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
