"""Tests for StatusDoc / AutoZone — the one owner of the AUTO-fence grammar.

Pins the fence surgery that previously lived in three copies (reconcile's
write_auto_block + write_root_status, packaging_lock's write_lock_block) and
the shared field reads (working title, fuzzy status label). See ADR-0014.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.video_projects import (  # noqa: E402
    PACKAGING_LOCK_ZONE,
    RECONCILE_DASHBOARD_ZONE,
    RECONCILE_ZONE,
    StatusDoc,
    StatusDocError,
    VideoProject,
)

NARRATIVE = "# 62 Test Project\n\nHand-written narrative that must survive.\n"


# ---------------------------------------------------------------------------
# Fence grammar
# ---------------------------------------------------------------------------

def test_marker_strings_are_the_historical_ones():
    """The exact markers already present in ~50 real PROJECT-STATUS.md files."""
    assert RECONCILE_ZONE.open_marker == (
        '<!-- AUTO:reconcile — do not edit manually, regenerated each run -->')
    assert RECONCILE_ZONE.close_marker == '<!-- /AUTO:reconcile -->'
    assert PACKAGING_LOCK_ZONE.open_marker == (
        '<!-- AUTO:packaging-lock — managed by packaging_lock.py, do not hand-edit -->')
    assert PACKAGING_LOCK_ZONE.close_marker == '<!-- /AUTO:packaging-lock -->'
    assert RECONCILE_DASHBOARD_ZONE.open_marker == (
        '<!-- AUTO:reconcile-dashboard — regenerated each run, do not edit -->')
    assert RECONCILE_DASHBOARD_ZONE.close_marker == '<!-- /AUTO:reconcile-dashboard -->'


def test_wrap_frames_body_with_trailing_newline():
    assert RECONCILE_ZONE.wrap("Status: X") == (
        RECONCILE_ZONE.open_marker + "\nStatus: X\n" + RECONCILE_ZONE.close_marker + "\n")


# ---------------------------------------------------------------------------
# Zone reads
# ---------------------------------------------------------------------------

def test_read_returns_inner_text_and_none_when_absent():
    text = RECONCILE_ZONE.wrap("Status: PUBLISHED") + NARRATIVE
    assert RECONCILE_ZONE.read(text) == "\nStatus: PUBLISHED\n"
    assert PACKAGING_LOCK_ZONE.read(text) is None


def test_fields_parse_key_values_and_strip_inline_comments():
    body = ("Status: PUBLISHED — uploaded\n"
            "Lifecycle: _ARCHIVED/published\n"
            "Published: 2026-05-01 (only when published)\n"
            "no colon line\n")
    fields = RECONCILE_ZONE.fields(RECONCILE_ZONE.wrap(body))
    assert fields == {
        "Status": "PUBLISHED — uploaded",
        "Lifecycle": "_ARCHIVED/published",
        "Published": "2026-05-01",
    }


def test_fields_none_when_zone_absent():
    assert RECONCILE_ZONE.fields(NARRATIVE) is None


# ---------------------------------------------------------------------------
# Surgery: reconcile zone (claims the top of the file)
# ---------------------------------------------------------------------------

def test_reconcile_write_prepends_on_fresh_doc_preserving_narrative():
    out = RECONCILE_ZONE.write(NARRATIVE, "Status: NEW")
    assert out == RECONCILE_ZONE.wrap("Status: NEW") + "\n" + NARRATIVE


def test_reconcile_write_on_empty_doc_has_no_separator():
    assert RECONCILE_ZONE.write("", "Status: NEW") == RECONCILE_ZONE.wrap("Status: NEW")


def test_reconcile_rewrite_replaces_zone_and_claims_top():
    text = "stray line above\n" + RECONCILE_ZONE.wrap("Status: OLD") + NARRATIVE
    out = RECONCILE_ZONE.write(text, "Status: NEW")
    assert out == RECONCILE_ZONE.wrap("Status: NEW") + NARRATIVE
    assert "stray line above" not in out
    assert "Status: OLD" not in out


def test_reconcile_rewrite_is_idempotent():
    once = RECONCILE_ZONE.write(NARRATIVE, "Status: X")
    twice = RECONCILE_ZONE.write(once, "Status: X")
    assert once == twice


# ---------------------------------------------------------------------------
# Surgery: packaging-lock zone (in place → below reconcile → prepend)
# ---------------------------------------------------------------------------

def test_lock_write_inserts_below_reconcile_zone():
    text = RECONCILE_ZONE.wrap("Status: X") + NARRATIVE
    out = PACKAGING_LOCK_ZONE.write(text, "title: \"T\"")
    assert out == (RECONCILE_ZONE.wrap("Status: X") + "\n"
                   + PACKAGING_LOCK_ZONE.wrap('title: "T"') + NARRATIVE)


def test_lock_rewrite_replaces_in_place_preserving_above_and_below():
    text = (RECONCILE_ZONE.wrap("Status: X") + "\n"
            + PACKAGING_LOCK_ZONE.wrap("VERDICT: OLD") + NARRATIVE)
    out = PACKAGING_LOCK_ZONE.write(text, "VERDICT: NEW")
    assert out == (RECONCILE_ZONE.wrap("Status: X") + "\n"
                   + PACKAGING_LOCK_ZONE.wrap("VERDICT: NEW") + NARRATIVE)


def test_lock_write_prepends_when_no_reconcile_zone():
    out = PACKAGING_LOCK_ZONE.write(NARRATIVE, "VERDICT: NEW")
    assert out == PACKAGING_LOCK_ZONE.wrap("VERDICT: NEW") + "\n" + NARRATIVE


def test_lock_rewrite_does_not_touch_reconcile_zone():
    text = (RECONCILE_ZONE.wrap("Status: KEEP") + "\n"
            + PACKAGING_LOCK_ZONE.wrap("VERDICT: OLD") + NARRATIVE)
    out = PACKAGING_LOCK_ZONE.write(text, "VERDICT: NEW")
    assert RECONCILE_ZONE.fields(out) == {"Status": "KEEP"}


# ---------------------------------------------------------------------------
# StatusDoc: load / save / shared fields
# ---------------------------------------------------------------------------

def test_load_missing_file_is_empty_doc(tmp_path):
    doc = StatusDoc.load(tmp_path / "PROJECT-STATUS.md")
    assert doc.text == ""
    assert doc.zone_fields(RECONCILE_ZONE) is None
    assert doc.working_title is None
    assert doc.status_label is None


def test_save_creates_file_and_returns_previous_content(tmp_path):
    path = tmp_path / "sub" / "PROJECT-STATUS.md"
    doc = StatusDoc.load(path)
    doc.write_zone(RECONCILE_ZONE, "Status: NEW")
    assert doc.save() == ""  # nothing existed before
    assert path.read_text(encoding="utf-8") == RECONCILE_ZONE.wrap("Status: NEW")

    doc2 = StatusDoc.load(path)
    doc2.write_zone(RECONCILE_ZONE, "Status: NEWER")
    previous = doc2.save()
    assert previous == RECONCILE_ZONE.wrap("Status: NEW")


def test_working_title_variants():
    assert StatusDoc('Working title: "The Quoted One"\n').working_title == "The Quoted One"
    assert StatusDoc("Working title: Bare Title\n").working_title == "Bare Title"
    # Bold-style lines keep the historical quirk (the ** prefix survives) —
    # parity with the old packaging_lock regex; change deliberately if it bites.
    assert StatusDoc("**Working title:** Bold Style\n").working_title == "** Bold Style"
    assert StatusDoc(NARRATIVE).working_title is None


def test_status_label_fuzzy_read():
    assert StatusDoc("Status: PUBLISHED\n").status_label == "PUBLISHED"
    assert StatusDoc("**Status:** RESEARCH IN PROGRESS\n").status_label == "RESEARCH IN PROGRESS"
    assert StatusDoc(NARRATIVE).status_label is None
    # only the head of the doc is scanned (first 500 chars)
    assert StatusDoc(("x" * 600) + "\nStatus: PUBLISHED\n").status_label is None


# ---------------------------------------------------------------------------
# VideoProject composition
# ---------------------------------------------------------------------------

def test_video_project_status_composes_statusdoc(tmp_path):
    folder = tmp_path / "62-test-2026"
    folder.mkdir()
    (folder / "PROJECT-STATUS.md").write_text(
        RECONCILE_ZONE.wrap("Status: SCRIPTING") + NARRATIVE, encoding="utf-8")
    proj = VideoProject("62-test-2026", folder, "in_production")
    assert proj.status.zone_fields(RECONCILE_ZONE) == {"Status": "SCRIPTING"}
    assert proj.status.status_label == "SCRIPTING"


def test_video_project_status_on_missing_file_is_empty_doc(tmp_path):
    folder = tmp_path / "63-test-2026"
    folder.mkdir()
    proj = VideoProject("63-test-2026", folder, "in_production")
    assert proj.status.text == ""
    assert proj.status.status_label is None


# ---------------------------------------------------------------------------
# Fail-closed on unreadable existing file (2026-07 audit — no destructive rewrite)
# ---------------------------------------------------------------------------

def test_undecodable_existing_file_refuses_write_and_survives(tmp_path):
    """An existing file with invalid UTF-8 must NOT be silently loaded as empty
    and then overwritten by an AUTO-block update — the hand-written narrative
    (and the raw bytes) survive because write/save fail closed."""
    p = tmp_path / "PROJECT-STATUS.md"
    raw = b"# 62 Project\n\x8f invalid-utf8 byte\nHand-written narrative.\n"
    p.write_bytes(raw)

    doc = StatusDoc.load(p)
    # Read-only field access still degrades gracefully (no crash).
    assert doc.status_label is None

    with pytest.raises(StatusDocError):
        doc.write_zone(RECONCILE_ZONE, "Status: PUBLISHED")
    with pytest.raises(StatusDocError):
        doc.save()

    assert p.read_bytes() == raw  # file untouched, not clobbered to empty


def test_absent_file_loads_writable_and_saves(tmp_path):
    """An absent file is a legitimate new doc — writable, and save creates it."""
    p = tmp_path / "PROJECT-STATUS.md"
    doc = StatusDoc.load(p)
    doc.write_zone(RECONCILE_ZONE, "Status: SCRIPTING")
    doc.save()
    assert p.exists()
    assert StatusDoc.load(p).zone_fields(RECONCILE_ZONE) == {"Status": "SCRIPTING"}


def test_save_preserves_handwritten_narrative_and_returns_previous(tmp_path):
    """A normal AUTO-zone update keeps the hand-written narrative and returns
    the prior on-disk content (the backup contract)."""
    p = tmp_path / "PROJECT-STATUS.md"
    original = RECONCILE_ZONE.wrap("Status: SCRIPTING") + NARRATIVE
    p.write_text(original, encoding="utf-8")

    doc = StatusDoc.load(p)
    previous = doc.save()  # no-op re-save
    assert previous == original
    assert "Hand-written narrative that must survive." in p.read_text(encoding="utf-8")
