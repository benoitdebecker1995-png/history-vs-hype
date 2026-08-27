"""Pins for the doc-truth checker (tools/preflight/doc_truth.py).

Origin: 2026-08-04. `NEXT-VIDEO-DISCOVERY-HANDOFF.md` — the file CLAUDE.md points every session at
for next-video work — put `impressions_daily` in analytics.db (it is in keywords.db) and
`thumbnail_features` in keywords.db (it is in analytics.db). An agent following that queries a
table that does not exist and reads the empty result as an answer, which is the exact failure
ADR-0020 exists to prevent.

Two suites: behaviour on synthetic docs, and a live assertion that the real repo is clean.
"""

import sqlite3

import pytest

from tools.preflight import doc_truth


@pytest.fixture
def repo(tmp_path):
    """A miniature repo: two databases and the top-level dirs the checker keys off."""
    (tmp_path / "channel-data").mkdir()
    (tmp_path / "tools").mkdir()
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "_research").mkdir()  # leading underscore => ambiguous, must be ignored
    return tmp_path


@pytest.fixture
def tables():
    return {
        "analytics.db": {"videos", "thumbnail_features"},
        "keywords.db": {"impressions_daily", "ctr_snapshots"},
        "intel.db": {"comment_signals"},
    }


class TestTableClaims:
    def test_wrong_database_is_caught(self, tables):
        """The bug this module was written for."""
        text = "State: `analytics.db.impressions_daily` has per-day grain."
        findings = doc_truth.check_tables(text, "doc.md", tables)
        assert [f.kind for f in findings] == ["WRONG_DB"]
        assert "keywords.db" in findings[0].detail

    def test_the_mirror_image_error_is_caught(self, tables):
        findings = doc_truth.check_tables("see `keywords.db.thumbnail_features`", "d.md", tables)
        assert findings[0].kind == "WRONG_DB"
        assert "analytics.db" in findings[0].detail

    def test_correct_reference_is_silent(self, tables):
        assert doc_truth.check_tables("`keywords.db.impressions_daily`", "d.md", tables) == []

    def test_unknown_table_is_reported(self, tables):
        findings = doc_truth.check_tables("`analytics.db.no_such_table`", "d.md", tables)
        assert findings[0].kind == "NO_TABLE"

    def test_absence_is_not_claimed_when_no_database_could_be_read(self):
        """ADR-0020: an unreadable database must not become 'the table does not exist'."""
        empty = {"analytics.db": set(), "keywords.db": set(), "intel.db": set()}
        assert doc_truth.check_tables("`analytics.db.videos`", "d.md", empty) == []

    def test_line_number_points_at_the_claim(self, tables):
        text = "intro\n\nsee `analytics.db.impressions_daily`\n"
        assert doc_truth.check_tables(text, "d.md", tables)[0].line == 3


class TestPathClaims:
    def test_missing_repo_rooted_path_is_caught(self, repo):
        top = doc_truth._repo_top_level(repo)
        findings = doc_truth.check_paths("see `channel-data/gone.md`", "d.md", repo, top)
        assert [f.kind for f in findings] == ["MISSING_PATH"]

    def test_existing_path_is_silent(self, repo):
        (repo / "channel-data" / "here.md").write_text("x", encoding="utf-8")
        top = doc_truth._repo_top_level(repo)
        assert doc_truth.check_paths("see `channel-data/here.md`", "d.md", repo, top) == []

    @pytest.mark.parametrize(
        "path",
        [
            "memory/feedback-talk-first-scripting.md",  # user-memory store, not a repo path
            "_research/00-PRELIMINARY-BRIEF.md",        # relative to the project in hand
            "historian/SKILL.md",                       # relative to the skills directory
            "scratchpad/results.json",                  # session scratchpad
        ],
    )
    def test_paths_that_are_not_repo_rooted_are_left_alone(self, repo, path):
        """Only a path whose first segment is a real top-level dir is claiming a repo location."""
        top = doc_truth._repo_top_level(repo)
        assert doc_truth.check_paths(f"see `{path}`", "d.md", repo, top) == []

    def test_underscore_directories_stay_ambiguous_even_when_they_exist(self, repo):
        assert "_research" not in doc_truth._repo_top_level(repo)

    def test_a_doc_saying_the_file_is_gone_is_not_a_finding(self, repo):
        top = doc_truth._repo_top_level(repo)
        text = "`channel-data/stats.md` | RETIRED — never existed. Don't create it"
        assert doc_truth.check_paths(text, "d.md", repo, top) == []

    def test_absence_cue_on_the_following_line_also_exempts(self, repo):
        """ADR style: the path is proposed on one line and rejected on the next."""
        top = doc_truth._repo_top_level(repo)
        text = "- **A neutral `tools/auto_zone.py`** module.\n  Rejected — one concept home.\n"
        assert doc_truth.check_paths(text, "d.md", repo, top) == []

    def test_adrs_are_exempt_from_path_checks(self, repo):
        """A dated decision record was true when written; editing it falsifies the record."""
        top = doc_truth._repo_top_level(repo)
        text = "see `tools/moved_away.py`"
        assert doc_truth.check_paths(text, "docs/adr/0010-thing.md", repo, top) == []
        assert doc_truth.check_paths(text, "channel-data/note.md", repo, top) != []

    def test_expected_absent_entries_carry_a_reason(self):
        assert doc_truth.EXPECTED_ABSENT
        for path, reason in doc_truth.EXPECTED_ABSENT.items():
            assert reason.strip(), f"{path} is exempted without a reason"


class TestLiveDatabases:
    def test_live_tables_reads_the_three_stores(self):
        tables = doc_truth.live_tables()
        assert set(tables) == {"analytics.db", "keywords.db", "intel.db"}

    def test_the_two_tables_that_started_this_are_where_we_say_they_are(self):
        tables = doc_truth.live_tables()
        if not any(tables.values()):
            pytest.skip("no live databases in this checkout")
        assert "impressions_daily" in tables["keywords.db"]
        assert "thumbnail_features" in tables["analytics.db"]

    def test_a_missing_database_yields_an_empty_set_not_an_exception(self, monkeypatch, tmp_path):
        monkeypatch.setattr(
            doc_truth, "DATABASES", {"analytics.db": tmp_path / "nope.db"}
        )
        assert doc_truth.live_tables() == {"analytics.db": set()}

    def test_a_corrupt_database_is_survived(self, monkeypatch, tmp_path):
        bad = tmp_path / "bad.db"
        bad.write_text("not a database", encoding="utf-8")
        monkeypatch.setattr(doc_truth, "DATABASES", {"analytics.db": bad})
        with pytest.raises(sqlite3.DatabaseError):
            sqlite3.connect(bad).execute("SELECT name FROM sqlite_master")
        assert doc_truth.live_tables() == {"analytics.db": set()}


class TestRepoIsClean:
    def test_no_doc_names_a_table_or_path_that_does_not_resolve(self):
        findings = doc_truth.audit()
        assert findings == [], "\n".join(
            f"{f.kind} {f.doc}:{f.line} {f.named} -> {f.detail}" for f in findings
        )

    def test_cli_reports_clean_as_exit_zero(self, capsys):
        assert doc_truth.main([]) == 0
        assert "clean" in capsys.readouterr().out


def test_legacy_recovery_docs_are_not_active_truth_surfaces(tmp_path):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "AGENTS.legacy.md").write_text(
        "see `tools/does-not-exist.py`", encoding="utf-8"
    )
    assert list(doc_truth._iter_docs(tmp_path)) == []
