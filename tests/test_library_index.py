"""Tests for the source-library index generator.

`parse_name` is load-bearing beyond the catalogue: `citation_check --library`
resolves a citation to a file by the Author field, so a parsing bug does not just
produce an ugly row — it makes the book unverifiable.
"""
import pytest

from tools.library_index import CONFORMING, apply, build_body, collect, parse_name


@pytest.mark.parametrize("stem,author,year,publisher", [
    ("SomaliaSomalilandHistory-Lewis-2008-IndianaUP", "Lewis", "2008", "Indiana UP"),
    # Hyphenated surnames: taking parts[1] truncated 65 of 1,151 books to their
    # first barrel and made them unresolvable.
    # publisher stays "UTexas": _spaced splits on lower->upper, and there is no
    # lowercase before the T, so nothing to break.
    ("BerberIdentityMovement-Maddy-Weitzman-2011-UTexas", "Maddy-Weitzman", "2011", "UTexas"),
    ("ColonialityPowerPostcolonialAfrica-Ndlovu-Gatsheni-2013-CODESRIA",
     "Ndlovu-Gatsheni", "2013", "CODESRIA"),
    # A title that is itself a year: anchoring on parts[0] left these year-less
    # and wrongly flagged them as malformed.
    ("1491-Mann-2011-Libgen", "Mann", "2011", "Libgen"),
    ("1776-McCullough-2005-RandomHouse", "McCullough", "2005", "Random House"),
])
def test_parses_the_live_convention(stem, author, year, publisher):
    b = parse_name(stem)

    assert b.author == author
    assert b.year == year
    assert b.publisher == publisher


def test_title_is_spaced_for_searchability():
    """The README tells you to Ctrl+F this file, so CamelCase must break."""
    assert parse_name("SomaliaSomalilandHistory-Lewis-2008-X").title == "Somalia Somaliland History"


def test_malformed_names_are_flagged_not_silently_wrong():
    """A book whose author will not parse cannot be reached by
    citation_check --library, so it must surface as a worklist item."""
    for bad in ("AfonsoIKingOfKongo-Article", "ChimuCulture-JimenezBorja-Unknown"):
        b = parse_name(bad)
        assert not (CONFORMING.fullmatch(b.author) and b.year), b


def _library(tmp_path, names, stash=0):
    topic = tmp_path / "by-topic" / "general-history"
    topic.mkdir(parents=True)
    for n in names:
        (topic / f"{n}.pdf").write_bytes(b"%PDF-1.4\n")
    if stash:
        s = tmp_path / "_stash-needs-id"
        s.mkdir()
        for i in range(stash):
            (s / f"x{i}.pdf").write_bytes(b"%PDF-1.4\n")
    return tmp_path


def test_collect_counts_filed_and_stashed(tmp_path):
    lib = _library(tmp_path, ["A-Smith-1990-OUP", "B-Jones-1991-CUP"], stash=3)

    data = collect(lib)

    assert len(data["topics"]["general-history"]) == 2
    assert data["stashes"]["_stash-needs-id"] == 3


def test_body_lists_every_book(tmp_path):
    lib = _library(tmp_path, ["A-Smith-1990-OUP", "B-Jones-1991-CUP"])

    body = build_body(collect(lib))

    assert "Smith" in body and "Jones" in body
    assert "2 books filed" in body


def test_regeneration_is_idempotent(tmp_path):
    lib = _library(tmp_path, ["A-Smith-1990-OUP"])
    (lib / "LIBRARY-INDEX.md").write_text("# Library\n\nHand-written intro.\n", encoding="utf-8")

    assert apply(write=True, library=lib) is True
    assert apply(write=True, library=lib) is False


def test_hand_written_prose_outside_the_fence_survives(tmp_path):
    lib = _library(tmp_path, ["A-Smith-1990-OUP"])
    (lib / "LIBRARY-INDEX.md").write_text("# Library\n\nHand-written intro.\n", encoding="utf-8")

    apply(write=True, library=lib)

    assert "Hand-written intro." in (lib / "LIBRARY-INDEX.md").read_text(encoding="utf-8")


def test_missing_library_is_not_an_exception(tmp_path):
    data = collect(tmp_path / "does-not-exist")

    assert data == {"topics": {}, "stashes": {}}
