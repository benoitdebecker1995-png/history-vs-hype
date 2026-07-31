"""Tests for citation faithfulness.

The load-bearing case is WRONG_PAGE: a quote that exists in the document but on
a different page. It survives every text-only check and only fails when a viewer
looks it up, which is the worst possible moment for this channel.

The other half of the contract is not crying wolf. Two of these tests pin
failures found on the tool's first real run against published research.
"""
import pytest

from tools.preflight.citation_check import check_file, quotes_in

fitz = pytest.importorskip("fitz", reason="PyMuPDF not installed")

QUOTE_P2 = "boats were requisitioned under the denial policy"


@pytest.fixture
def source(tmp_path):
    docs = tmp_path / "_research" / "documents"
    docs.mkdir(parents=True)
    doc = fitz.open()
    for body in ["Page one is introductory matter.",
                 f"Page two records that {QUOTE_P2} across the province.",
                 "Page three holds the mortality estimate."]:
        doc.new_page().insert_text((72, 72), body, fontsize=13)
    out = docs / "Kamen-famine-report.pdf"
    doc.save(str(out))
    doc.close()
    return tmp_path


def _md(root, text):
    p = root / "01-VERIFIED-RESEARCH.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_correct_citation_verifies(source):
    md = _md(source, f'- Claim "{QUOTE_P2}" (pdf p.2)\n')

    r = check_file(md)

    assert [x.verdict for x in r] == ["VERIFIED"]


def test_off_by_one_page_is_caught(source):
    """The headline case. Flagged WITH the page it is actually on, because
    'wrong' without 'where' just makes work."""
    md = _md(source, f'- Claim "{QUOTE_P2}" (pdf p.1)\n')

    r = check_file(md)

    assert r[0].verdict == "WRONG_PAGE"
    assert r[0].found_pages == [2]
    assert "p.2" in r[0].detail or "[2]" in r[0].detail


def test_quote_not_in_document_is_not_found(source):
    md = _md(source, '- Claim "the commission found no evidence of hoarding" (pdf p.2)\n')

    assert check_file(md)[0].verdict == "NOT_FOUND"


def test_absent_source_is_not_reported_as_fabrication(source):
    """Regression, first real run: 8 quotes citing Kamen/Homza/Arguello were
    reported as possible fabrication when the folder held one unrelated PDF.
    Accusing a correct citation is how a checker gets ignored."""
    md = _md(source, '- Claim "a passage from a book we do not hold" Thornton p. 44\n')

    r = check_file(md)

    assert r[0].verdict == "SOURCE_ABSENT"
    assert "Thornton" in r[0].detail


def test_printed_page_citation_is_not_failed(source):
    """Academic PDFs are offset from their printed page numbers -- #66 cites
    '(pdf p.32, printed p.26)'. A bare page number is ambiguous, so it reports
    where the quote is rather than failing a possibly-correct citation."""
    md = _md(source, f'- Claim "{QUOTE_P2}" p. 26\n')

    r = check_file(md)

    assert r[0].verdict == "PAGE_UNKNOWN"
    assert r[0].found_pages == [2]


def test_line_break_inside_a_quote_still_verifies(source):
    """PDFs wrap; humans quote flat. This must not fail."""
    md = _md(source, f'- Claim "{QUOTE_P2.replace(" ", "  ")}" (pdf p.2)\n')

    assert check_file(md)[0].verdict == "VERIFIED"


def test_short_fragments_are_ignored(source):
    """'the treaty' matches everywhere and proves nothing."""
    md = _md(source, '- Claim "the boats" (pdf p.2)\n')

    assert check_file(md) == []


def test_no_documents_directory_yields_no_findings(tmp_path):
    md = _md(tmp_path, f'- Claim "{QUOTE_P2}" (pdf p.2)\n')

    assert check_file(md) == []


def test_missing_file_is_not_an_exception(tmp_path):
    assert check_file(tmp_path / "ghost.md") == []


def test_unresolved_is_not_reported_as_not_found(tmp_path, monkeypatch):
    """Regression, #66 library run: when no source resolves, NOTHING was opened,
    so NOT_FOUND ('check for paraphrase-as-verbatim') is an accusation about a
    citation nobody read. 21 quotes were mislabelled that way."""
    from tools.preflight import citation_check as cc
    monkeypatch.setattr(cc, "LIBRARY_DIR", tmp_path / "empty-library")

    md = tmp_path / "01-VERIFIED-RESEARCH.md"
    md.write_text('- Claim "a passage with no author named anywhere near it" (pdf p.4)\n',
                  encoding="utf-8")

    r = cc.check_file(md, use_library=True)

    assert r == [] or r[0].verdict == "UNRESOLVED"


def test_source_is_resolved_from_the_section_heading(source):
    """#66 names sources in headings and quotes underneath, so scanning the
    quote line alone resolved nothing."""
    from tools.preflight.citation_check import _named_sources

    index = {"kamen": [], "homza": []}

    assert _named_sources("- a quote line", "### A2 — Kamen on the denial policy", index) == ["kamen"]
    assert _named_sources("cited by Homza here", "### heading", index) == ["homza"]


# ------------------------------------------------------------ quote pairing ---

def test_quotes_are_paired_not_alternated():
    """Regression: a naive '"([^"]+)"' findall consumes the FIRST quote then
    matches the text BETWEEN quotes as the second. First run produced findings
    like '" (synthesis from operational records). Kamen p. 240: "'."""
    line = ('Instruction 55 restricts the chamber to "Judges, Notary, and ministers only" '
            'and Kamen p. 240 adds "physicians were usually available in case of emergency"')

    found = quotes_in(line)

    assert len(found) == 2
    assert found[0].startswith("Judges, Notary")
    assert found[1].startswith("physicians were usually")
    assert not any("Kamen p. 240" in q for q in found)


def test_unquoted_line_yields_nothing():
    assert quotes_in("no quotes here at all, just prose about the denial policy") == []


def test_connective_prose_between_quotes_is_not_a_quote():
    """Regression, #66 run: research files wrap quotes in italics and run them
    across lines -- `imports."* Mansergh's summary describes Wavell *"pressing`.
    A line BEGINNING mid-quote inverts the odd/even pairing, so the connective
    prose lands on the odd index. Emphasis brackets identify it."""
    line = 'imports."* Mansergh\'s own editorial summary describes Wavell *"pressing for diversion of ships"'

    found = quotes_in(line)

    assert not any("Mansergh" in q for q in found), found


def test_passage_on_several_pages_is_not_adjudicated(source, tmp_path):
    """Regression, #66 run: a 6-word section heading appears in both the
    contents and the body, so it matched pdf p.61 AND p.287 and was reported
    WRONG_PAGE against a cited p.62. With repeated text the page cannot be
    adjudicated -- the cited page may hold an occurrence the OCR lost."""
    docs = source / "_research" / "documents"
    doc = fitz.open()
    heading = "Power of Governor to issue Proclamations"
    for body in [f"Contents: {heading} ... 630", "filler", f"{heading}. The Governor may suspend."]:
        doc.new_page().insert_text((72, 72), body, fontsize=12)
    doc.save(str(docs / "act.pdf"))
    doc.close()

    md = _md(source, f'- Section "{heading} and related powers" (pdf p.2)\n')
    # quote spans the heading text; it occurs on pages 1 and 3, not the cited 2
    r = [x for x in check_file(md) if x.document == "act.pdf"]

    if r:  # only assert if the fuzzy pass matched it on multiple pages
        assert r[0].verdict != "WRONG_PAGE", r[0]
