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

# Archive/scan cruft carrying no meaning: long digit runs, hex hashes, DOI
# prefixes, "pdf_1-293" page ranges, libgen/z-lib tails. Stripping these leaves
# whatever human words the filename still holds.
FILENAME_CRUFT = re.compile(
    r"(\b\d{5,}\b|\b[0-9a-f]{8,}\b|10\.\d{4}[@/][^\s-]+|pdf[_ ]?\d+[-–]\d+"
    r"|z-?lib(rary)?(\.\w+)?|libgen(\.\w+)?|anna.?s archive|_compre\w*)", re.I)

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


def _from_epub(path: Path, cand: Candidate) -> Candidate:
    """Read Dublin Core metadata out of an EPUB.

    An EPUB is a zip whose OPF package file carries `dc:title`, `dc:creator` and
    `dc:date` — better metadata than most PDFs have, and reachable with the
    standard library alone. 22 of the stash's stragglers are EPUBs; OCR, which
    this was added alongside, rescued only 2 files in total.
    """
    import xml.etree.ElementTree as ET
    import zipfile

    DC = "{http://purl.org/dc/elements/1.1/}"
    try:
        with zipfile.ZipFile(path) as z:
            opf = next((n for n in z.namelist() if n.lower().endswith(".opf")), None)
            if not opf:
                cand.problem = "epub with no OPF package file"
                return cand
            root = ET.fromstring(z.read(opf))
    except Exception as exc:
        cand.problem = f"unreadable epub: {str(exc)[:50]}"
        return cand

    def _first(tag: str) -> str:
        el = root.find(f".//{DC}{tag}")
        return _clean(el.text) if el is not None and el.text else ""

    title = _first("title")
    if title and not BAD_TITLE.match(title) and not _is_garbage(title):
        cand.title, cand.evidence = title, "epub-opf"
    creator = _first("creator")
    if creator and len(creator) < 60:
        cand.author = creator.split(",")[0].split(" and ")[0].strip()
    m = re.search(r"(1[6-9]\d{2}|20[0-2]\d)", _first("date") or path.stem)
    if m:
        cand.year = m.group(0)
    if not cand.title:
        cand.problem = "epub without a usable dc:title"
    return cand


def extract(path: Path, ocr: bool = False) -> Candidate:
    """Best-effort identification. Never raises.

    `ocr` enables the last-resort image pass; it is off by default because it
    costs seconds per file against milliseconds for the other routes.
    """
    cand = Candidate(path=path)
    try:
        if path.stat().st_size == 0:
            cand.problem = "zero bytes — failed download, re-fetch it"
            return cand
    except OSError as exc:
        cand.problem = f"unstattable: {exc}"
        return cand

    if path.suffix.lower() == ".epub":
        return _from_epub(path, cand)

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

    # Fallback 1: the filename minus its archive cruft. Cheap, and on the
    # Karabakh scans it beat OCR outright -- "000199_000009_002585977-1823
    # karabach census" carries a title and a year, while OCR of that 1823 print
    # returned "6OMMCAHIE".
    if not cand.title:
        remnant = FILENAME_CRUFT.sub(" ", path.stem)
        remnant = _clean(re.sub(r"[_+]+", " ", remnant))
        if len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", remnant)) >= 2 and not _is_garbage(remnant):
            cand.title, cand.evidence = remnant, "filename-remnant"

    # Fallback 2: OCR the first pages. Only now, because it costs seconds per
    # page against nothing for the two checks above.
    if not cand.title and ocr:
        from tools.pdf_source import ocr_page_text
        scanned = ""
        for i in (1, 2):
            got = ocr_page_text(path, i)
            if got:
                scanned += got + "\n"
            if len(scanned) > 200:
                break
        if scanned:
            for line in (l.strip() for l in scanned.splitlines()):
                line = _clean(line)
                if _usable(line) and not line.isdigit():
                    cand.title, cand.evidence = line, "ocr"
                    break
            if not cand.year:
                years = re.findall(r"\b(1[6-9]\d{2}|20[0-2]\d)\b", scanned[:2000])
                if years:
                    cand.year = Counter(years).most_common(1)[0][0]
            if cand.kind == "book":
                cand.kind = classify(scanned)

    if not cand.title:
        cand.problem = cand.problem or "no title in metadata, text, filename or OCR"
    return cand


def proposed_name(c: Candidate) -> str:
    author = _camel(c.author) if c.author else "Unknown"
    year = c.year or "Unknown"
    kind = "" if c.kind == "book" else f"-{c.kind}"
    return f"{_camel(c.title)}-{author}-{year}-Stash{kind}{c.path.suffix.lower()}"


STOPWORDS = set(
    "the of and in a to for an on at from with its their his her by as is are was "
    "were new history historical study studies vol volume edition unknown press "
    "university book books text texts introduction chapter part page pages".split())

# Never a filing TARGET: general-history is the catch-all, 605 of 1,151 books.
# Sending ambiguous items there is how a library becomes a pile.
CATCHALL = "general-history"

# A topic must win by this multiple over the runner-up. Below it the evidence is
# split, and a wrong shelf is worse than the stash: in the stash you know it is
# unfiled, on the wrong shelf you think it is filed.
MARGIN = 1.6
MIN_SCORE = 0.6


def topic_vocabulary(library=None) -> dict:
    """{topic: {term: distinctiveness}} learned from books already filed.

    Weighting is deliberately by DISTINCTIVENESS, not frequency: "world" and
    "empire" appear across most topics and must not decide anything, while
    "bakassi", "moche" and "crusading" are near-conclusive on their own.
    """
    from tools.library_index import collect
    data = collect(library)
    per_topic = {}
    doc_freq: Counter = Counter()
    for topic, books in data["topics"].items():
        terms = Counter()
        for b in books:
            for w in re.findall(r"[a-zà-ÿ]{4,}", b.title.lower()):
                if w not in STOPWORDS:
                    terms[w] += 1
        per_topic[topic] = terms
        for w in terms:
            doc_freq[w] += 1
    vocab = {}
    for topic, terms in per_topic.items():
        total = sum(terms.values()) or 1
        vocab[topic] = {
            w: (c / total) * (1.0 / doc_freq[w])   # frequency x distinctiveness
            for w, c in terms.items() if c >= 2
        }
    return vocab


def classify_topic(text: str, vocab: dict):
    """(topic, score, runner_up_score). topic is None when the evidence is split."""
    words = [w for w in re.findall(r"[a-zà-ÿ]{4,}", (text or "").lower())
             if w not in STOPWORDS]
    if not words:
        return None, 0.0, 0.0
    seen = set(words)
    scores = {
        topic: sum(weights.get(w, 0.0) for w in seen) * 100
        for topic, weights in vocab.items() if topic != CATCHALL
    }
    if not scores:
        return None, 0.0, 0.0
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    (best, top), (_, second) = ranked[0], (ranked[1] if len(ranked) > 1 else ("", 0.0))
    if top < MIN_SCORE or top < second * MARGIN:
        return None, top, second
    return best, top, second


def triage(stash=None, ocr: bool = False) -> List[Candidate]:
    base = Path(stash) if stash else STASH
    if not base.is_dir():
        logger.warning("no stash at %s", base)
        return []
    return [extract(f, ocr=ocr) for f in sorted(base.iterdir()) if f.is_file()]


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
    ap.add_argument("--file", action="store_true",
                    help="move identified files into library/by-topic/<topic>/ when the "
                         "topic is unambiguous (abstains otherwise — they stay in the stash)")
    ap.add_argument("--ocr", action="store_true",
                    help="OCR image-only scans as a last resort (slow: seconds per file)")
    ap.add_argument("--limit", type=int, default=0)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verbose", "-v", action="store_true")
    g.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    cands = triage(ocr=args.ocr)
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

    if args.file:
        # Validated 2026-07-31 against 167 already-filed books: 92% correct when
        # it commits, abstaining on 34%. Abstentions stay in the stash, because a
        # wrong shelf is worse than an obvious backlog.
        vocab = topic_vocabulary()
        moved: Counter = Counter()
        abstained = 0
        for path in sorted(p for p in STASH.iterdir() if p.is_file()):
            book = None
            try:
                from tools.library_index import parse_name
                book = parse_name(path.stem)
            except Exception:
                pass
            evidence = f"{book.title if book else ''} {path.stem}"
            topic, top, second = classify_topic(evidence, vocab)
            if not topic:
                abstained += 1
                continue
            dest_dir = BY_TOPIC / topic
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / path.name
            if dest.exists():
                abstained += 1
                continue
            try:
                shutil.move(str(path), str(dest))
                moved[topic] += 1
            except OSError as exc:
                logger.warning("could not file %s: %s", path.name, exc)
        print(f"\n  filed {sum(moved.values())} into by-topic/ "
              f"({abstained} abstained — evidence split, left in the stash)")
        for topic, n in moved.most_common():
            print(f"    {topic:24} +{n}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
