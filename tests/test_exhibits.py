"""Tests for on-screen exhibit rendering.

The rule this enforces: an exhibit must actually contain the passage it is on
screen to support. Showing a document as proof of something it does not say is
worse than showing no document — it is the failure the whole "primary sources ON
SCREEN" discipline exists to prevent.
"""
import pytest

from tools.production.exhibits import build, caption

fitz = pytest.importorskip("fitz", reason="PyMuPDF not installed")

QUOTE = "the shortage of grain was not the result of physical deficiency"


@pytest.fixture
def report(tmp_path):
    doc = fitz.open()
    for body in ["Cover page.",
                 "Minutes record that " + QUOTE + " but of hoarding.",
                 "Appendix tables."]:
        doc.new_page().insert_text((72, 72), body, fontsize=12)
    out = tmp_path / "warcabinet.pdf"
    doc.save(str(out))
    doc.close()
    return out


def test_page_is_located_from_the_quote(report, tmp_path):
    """The normal case: you know the sentence you want on screen, not its page."""
    r = build(report, quote=QUOTE, out_path=tmp_path / "ex.png")

    assert r.get("page") == 2, r
    assert (tmp_path / "ex.png").exists()


def test_render_produces_a_real_png(report, tmp_path):
    r = build(report, page=2, out_path=tmp_path / "ex.png")

    assert (tmp_path / "ex.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert "error" not in r


def test_refuses_to_render_a_page_that_lacks_its_own_quote(report, tmp_path):
    """The load-bearing guard, and it names the right page rather than just
    saying no."""
    r = build(report, page=3, quote=QUOTE, out_path=tmp_path / "bad.png")

    assert "error" in r
    assert "NOT on page 3" in r["error"]
    assert "[2]" in r["error"]
    assert not (tmp_path / "bad.png").exists()


def test_quote_absent_from_document_is_reported_clearly(report, tmp_path):
    r = build(report, quote="a sentence that appears nowhere in this report",
              out_path=tmp_path / "x.png")

    assert "error" in r and "not found" in r["error"].lower()
    # names the likely cause rather than leaving the user guessing
    assert "OCR" in r["error"]


def test_caption_carries_document_page_and_quote(report):
    c = caption(report, 2, QUOTE)

    assert "warcabinet.pdf" in c and "pdf p.2" in c and QUOTE in c


def test_caption_without_a_quote_still_identifies_the_source(report):
    """A PNG with no caption is an anonymous image three months later."""
    c = caption(report, 7)

    assert "warcabinet.pdf" in c and "pdf p.7" in c


def test_needs_a_page_or_a_quote(report, tmp_path):
    assert "error" in build(report, out_path=tmp_path / "x.png")


def test_missing_pdf_is_not_an_exception(tmp_path):
    r = build(tmp_path / "ghost.pdf", page=1, out_path=tmp_path / "x.png")

    assert "error" in r
