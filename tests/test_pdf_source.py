"""Tests for the PDF source seam.

The fixture PDF is generated in-test rather than committed: these must not break
when someone reorganises `_research/documents/`, and a binary fixture in git for
this would be dead weight.
"""
import pytest

from tools import pdf_source
from tools.pdf_source import (
    find_text, normalise, page_count, page_text, render_page,
)

fitz = pytest.importorskip("fitz", reason="PyMuPDF not installed")


@pytest.fixture
def sample(tmp_path):
    """3-page PDF with known text on known pages."""
    doc = fitz.open()
    for n, body in enumerate([
        "Page one speaks of the shortage of grain in India.",
        "Page two is about boats and the denial policy.",
        "Page three mentions the Famine Inquiry Commission.",
    ], 1):
        page = doc.new_page()
        page.insert_text((72, 72), body, fontsize=14)
    out = tmp_path / "sample.pdf"
    doc.save(str(out))
    doc.close()
    return out


def test_page_count(sample):
    assert page_count(sample) == 3


def test_page_numbers_are_one_based(sample):
    """A citation says 'p. 1', not 'p. 0'. The 0-based conversion happens once,
    inside the seam, so no caller has to remember it."""
    assert "one" in page_text(sample, 1)
    assert "three" in page_text(sample, 3)


def test_find_text_reports_the_page_a_citation_would_use(sample):
    hits = find_text(sample, "boats and the denial policy")

    assert [h.page for h in hits] == [2]
    assert "denial" in hits[0].snippet


def test_find_text_searches_the_whole_document(sample):
    """The useful answer to 'is this on p.1' is often 'no, it is on p.3'."""
    assert [h.page for h in find_text(sample, "Famine Inquiry Commission")] == [3]


def test_missing_file_returns_empty_not_an_exception(tmp_path):
    """Read-side contract: a citation check that crashes on a bad path tells you
    nothing about the citation."""
    ghost = tmp_path / "nope.pdf"

    assert page_count(ghost) == 0
    assert page_text(ghost, 1) is None
    assert find_text(ghost, "anything") == []
    assert render_page(ghost, 1, tmp_path / "x.png") is None


def test_out_of_range_page_returns_none(sample):
    assert page_text(sample, 0) is None
    assert page_text(sample, 99) is None


def test_empty_needle_finds_nothing(sample):
    """An empty search must not match every page."""
    assert find_text(sample, "") == []
    assert find_text(sample, "   ") == []


def test_render_writes_a_real_png(sample, tmp_path):
    out = render_page(sample, 1, tmp_path / "sub" / "p1.png", dpi=100)

    assert out is not None and out.exists()
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


# ------------------------------------------------------------- normalise ---

@pytest.mark.parametrize("raw,expect_equal", [
    ("the shortage of grain", "The  shortage\nof   grain"),   # line break + case
    ("don't", "don’t"),                                        # curly apostrophe
    ('say "this"', "say “this”"),                              # curly quotes
    ("a-b", "a–b"),                                            # en dash
])
def test_normalise_folds_what_pdfs_break(raw, expect_equal):
    """A quote typed from the page will never match a PDF byte-for-byte. If this
    folding failed, the checker would reject TRUE citations -- the one failure
    that would make the tool worth ignoring."""
    assert normalise(raw) == normalise(expect_equal)


def test_normalise_still_distinguishes_different_text():
    assert normalise("grain shortage") != normalise("grain surplus")
