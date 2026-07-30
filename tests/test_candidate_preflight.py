"""Tests for tools/preflight/candidate_preflight.py (ADR-0021 amendment).

Pins the 2026-07-30 failure: a "NATO promised not to expand" video was proposed and
screened at length before the owner pointed out it was already published.
"""

import sqlite3

from tools.preflight.candidate_preflight import _match, _terms, check


def _db(tmp_path, rows):
    p = tmp_path / "a.db"
    conn = sqlite3.connect(p)
    conn.execute("CREATE TABLE videos (video_id TEXT, title TEXT, published_at TEXT)")
    conn.executemany("INSERT INTO videos VALUES (?,?,?)", rows)
    conn.commit()
    conn.close()
    return str(p)


class TestTerms:
    def test_stopwords_and_short_words_dropped(self):
        assert _terms("Why did the NATO not expand") == ["nato", "expand"]

    def test_empty_topic_is_an_error(self, tmp_path):
        res = check("the a of and", db_path=_db(tmp_path, []))
        assert "error" in res

    def test_match_is_substring_based(self):
        assert _match(["nato", "expand"], "Putin Says NATO Promised Not to Expand") == [
            "nato",
            "expand",
        ]


class TestPublishedCollision:
    def test_the_nato_failure_is_caught(self, tmp_path):
        db = _db(
            tmp_path,
            [("499YLd1BHZ4", "Putin Says NATO Promised Not to Expand. The Documents Disagree.", "2025-09-10")],
        )
        res = check("NATO promised not to expand eastward", db_path=db)
        assert res["verdict"] == "COLLISION"
        assert res["hard"] == 1
        assert res["collisions"][0]["where"] == "499YLd1BHZ4"

    def test_unrelated_topic_is_clear_of_published(self, tmp_path):
        db = _db(tmp_path, [("x1", "Guatemala vs Belize Dispute", "2025-01-01")])
        res = check("Enigma Polish cipher Rejewski", db_path=db)
        assert res["hard"] == 0

    def test_single_shared_word_is_not_a_collision(self, tmp_path):
        db = _db(tmp_path, [("x1", "The Dark Ages Myth", "2025-01-01")])
        res = check("Bengal famine mortality", db_path=db, min_terms=2)
        assert res["hard"] == 0

    def test_missing_db_warns_but_does_not_raise(self, tmp_path):
        res = check("some topic here", db_path=str(tmp_path / "nope.db"))
        assert "error" not in res
        assert res["warnings"] >= 1
