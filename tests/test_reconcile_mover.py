"""Tests for reconcile's mover — the one operation that can lose work.

Covers apply_proposals (folder moves + AUTO-block edits + .pre-diff backups),
the conflict skip, and the full undo round-trip (moves reversed first so the
backup paths — which travel with the folder — resolve again, then file
restores). Everything runs on a fake tree: the module-level bucket paths and
.brain inbox are monkeypatched, so the real video-projects/ is never touched.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tools.reconcile.reconcile as rc  # noqa: E402
from tools.video_projects import RECONCILE_ZONE, StatusDoc  # noqa: E402

NARRATIVE = "# 10 Test\n\nHand-written narrative that must survive undo.\n"


@pytest.fixture
def fake_tree(tmp_path, monkeypatch):
    """Sandboxed bucket paths + brain inbox; returns the tmp root."""
    vp = tmp_path / "video-projects"
    monkeypatch.setattr(rc, "VIDEO_PROJECTS", vp)
    monkeypatch.setattr(rc, "IN_PRODUCTION", vp / "_IN_PRODUCTION")
    monkeypatch.setattr(rc, "READY_TO_FILM", vp / "_READY_TO_FILM")
    monkeypatch.setattr(rc, "ARCHIVED_PUBLISHED", vp / "_ARCHIVED" / "published")
    monkeypatch.setattr(rc, "BRAIN_INBOX", tmp_path / ".brain" / "_inbox")
    for p in (vp / "_IN_PRODUCTION", vp / "_READY_TO_FILM", vp / "_ARCHIVED" / "published"):
        p.mkdir(parents=True)
    return tmp_path


def make_project(bucket_dir: Path, name: str, status_text: str | None = NARRATIVE) -> Path:
    folder = bucket_dir / name
    folder.mkdir()
    if status_text is not None:
        (folder / "PROJECT-STATUS.md").write_text(status_text, encoding="utf-8")
    return folder


def make_state(folder: Path, *, bucket="_READY_TO_FILM", phase="filmed",
               video_id="abc123XYZ_0", published_at="2026-06-30T12:00:00Z"):
    return rc.FolderState(
        path=folder, bucket=bucket, slug=folder.name, files=set(),
        phase=phase, video_id=video_id, published_at=published_at,
    )


# ---------------------------------------------------------------------------
# apply_proposals — moves
# ---------------------------------------------------------------------------

def test_move_relocates_folder_and_records_it(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026")
    proposals = [rc.ProposedChange(kind="move", folder=folder,
                                   target_bucket="_ARCHIVED/published")]
    backups, moves, _ = rc.apply_proposals(proposals, "2026-07-01", {folder: make_state(folder)})

    dst = rc.ARCHIVED_PUBLISHED / "10-test-2026"
    assert not folder.exists()
    assert (dst / "PROJECT-STATUS.md").read_text(encoding="utf-8") == NARRATIVE
    assert moves == [(str(folder), str(dst))]
    assert backups == []  # no edit proposals


def test_move_conflict_skips_without_data_loss(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026")
    conflicting = make_project(rc.ARCHIVED_PUBLISHED, "10-test-2026",
                               status_text="OTHER PROJECT — must not be overwritten\n")
    proposals = [rc.ProposedChange(kind="move", folder=folder,
                                   target_bucket="_ARCHIVED/published")]
    _, moves, conflicts = rc.apply_proposals(proposals, "2026-07-01", {folder: make_state(folder)})

    assert moves == []
    assert conflicts == [(str(folder), str(rc.ARCHIVED_PUBLISHED / "10-test-2026"))]
    assert folder.exists()  # source untouched
    assert (conflicting / "PROJECT-STATUS.md").read_text(encoding="utf-8").startswith("OTHER PROJECT")


def test_conflict_skips_the_auto_block_edit_too(fake_tree):
    """A move blocked by a conflict must ALSO skip that project's AUTO-block
    edit, so PROJECT-STATUS.md never claims a bucket the folder isn't in."""
    folder = make_project(rc.READY_TO_FILM, "10-test-2026")
    make_project(rc.ARCHIVED_PUBLISHED, "10-test-2026",
                 status_text="OTHER PROJECT\n")
    proposals = [
        rc.ProposedChange(kind="edit-auto-block", folder=folder),
        rc.ProposedChange(kind="move", folder=folder, target_bucket="_ARCHIVED/published"),
    ]
    backups, moves, conflicts = rc.apply_proposals(
        proposals, "2026-07-01", {folder: make_state(folder)})

    assert moves == [] and len(conflicts) == 1
    assert backups == []  # AUTO-block edit skipped -> no .pre-diff written
    # Source status doc still the untouched hand-written narrative (no AUTO zone).
    assert (folder / "PROJECT-STATUS.md").read_text(encoding="utf-8") == NARRATIVE
    assert not (folder / "PROJECT-STATUS.md.pre-diff").exists()


# ---------------------------------------------------------------------------
# apply_proposals — AUTO-block edits
# ---------------------------------------------------------------------------

def test_edit_writes_auto_zone_and_pre_diff_backup(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026")
    state = make_state(folder)
    proposals = [rc.ProposedChange(kind="edit-auto-block", folder=folder)]
    backups, _, _ = rc.apply_proposals(proposals, "2026-07-01", {folder: state})

    doc = StatusDoc.load(folder / "PROJECT-STATUS.md")
    fields = doc.zone_fields(RECONCILE_ZONE)
    assert fields["Status"] == rc.target_status_label(state)
    assert fields["Lifecycle"] == rc.target_bucket(state)
    assert fields["Video ID"] == "abc123XYZ_0"
    assert doc.text.endswith(NARRATIVE)  # narrative preserved below the zone

    pre_diff = folder / "PROJECT-STATUS.md.pre-diff"
    assert pre_diff.read_text(encoding="utf-8") == NARRATIVE
    assert backups == [(str(folder / "PROJECT-STATUS.md"), str(pre_diff))]


def test_edit_on_missing_status_file_writes_sentinel_backup(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026", status_text=None)
    proposals = [rc.ProposedChange(kind="edit-auto-block", folder=folder)]
    rc.apply_proposals(proposals, "2026-07-01", {folder: make_state(folder)})

    assert (folder / "PROJECT-STATUS.md").exists()  # created
    sentinel = (folder / "PROJECT-STATUS.md.pre-diff").read_text(encoding="utf-8")
    assert sentinel == "__RECONCILE_DID_NOT_EXIST__"


# ---------------------------------------------------------------------------
# Undo round-trip
# ---------------------------------------------------------------------------

def test_full_undo_round_trip_restores_everything(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026")
    state = make_state(folder)
    proposals = [
        rc.ProposedChange(kind="edit-auto-block", folder=folder),
        rc.ProposedChange(kind="move", folder=folder, target_bucket="_ARCHIVED/published"),
    ]
    backups, moves, _ = rc.apply_proposals(proposals, "2026-07-01", {folder: state})
    assert len(moves) == 1 and len(backups) == 1
    rc.write_diff_log(rc.diff_log_path(), proposals, backups, moves)

    ops = rc.undo_latest()

    assert ops == 2  # one move reversed + one file restored
    assert folder.exists()
    assert not (rc.ARCHIVED_PUBLISHED / "10-test-2026").exists()
    # Content byte-restored, backup consumed, diff log marked undone
    assert (folder / "PROJECT-STATUS.md").read_text(encoding="utf-8") == NARRATIVE
    assert not (folder / "PROJECT-STATUS.md.pre-diff").exists()
    assert list(rc.BRAIN_INBOX.glob("*.diff")) == []
    assert len(list(rc.BRAIN_INBOX.glob("*.diff.undone"))) == 1


def test_undo_removes_files_reconcile_created(fake_tree):
    folder = make_project(rc.READY_TO_FILM, "10-test-2026", status_text=None)
    proposals = [rc.ProposedChange(kind="edit-auto-block", folder=folder)]
    backups, moves, _ = rc.apply_proposals(proposals, "2026-07-01", {folder: make_state(folder)})
    rc.write_diff_log(rc.diff_log_path(), proposals, backups, moves)

    assert (folder / "PROJECT-STATUS.md").exists()
    rc.undo_latest()
    assert not (folder / "PROJECT-STATUS.md").exists()  # sentinel → created file removed


def test_undo_with_no_diff_logs_is_a_noop(fake_tree):
    assert rc.undo_latest() == 0
