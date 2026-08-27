import sqlite3

from tools.discovery.database import KeywordDB


def test_package_history_records_chronological_versions(tmp_path):
    db_path = tmp_path / "keywords.db"
    db = KeywordDB(str(db_path))
    first = db.record_package_version(
        project_slug="67-donation",
        kind="title",
        value="Constantine's Charter Failed",
        effective_at="2026-08-13T10:00:00+00:00",
        reason="initial migration",
    )
    second = db.record_package_version(
        project_slug="67-donation",
        kind="title",
        value="They Changed the Test",
        effective_at="2026-08-13T11:00:00+00:00",
        supersedes_id=first["version_id"],
        experiment_id="title-swap-1",
    )
    rows = db.get_package_versions("67-donation")
    db.close()

    assert first["status"] == "inserted"
    assert second["status"] == "inserted"
    assert [row["value"] for row in rows] == [
        "Constantine's Charter Failed",
        "They Changed the Test",
    ]
    assert rows[1]["supersedes_id"] == first["version_id"]
    assert rows[1]["experiment_id"] == "title-swap-1"


def test_package_history_rejects_unknown_kind(tmp_path):
    db = KeywordDB(str(tmp_path / "keywords.db"))
    result = db.record_package_version(
        project_slug="67-donation", kind="score", value="91.3"
    )
    db.close()
    assert "error" in result


def test_package_history_table_is_idempotent(tmp_path):
    db_path = tmp_path / "keywords.db"
    KeywordDB(str(db_path)).close()
    KeywordDB(str(db_path)).close()
    con = sqlite3.connect(db_path)
    count = con.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='package_versions'"
    ).fetchone()[0]
    con.close()
    assert count == 1


def test_recommendation_ledger_preserves_prediction_then_outcome(tmp_path):
    db = KeywordDB(str(tmp_path / "keywords.db"))
    created = db.record_recommendation(
        project_slug="67-donation",
        decision_kind="package",
        recommendation="Keep the changed-test title.",
        rationale="It frames the mechanism the script actually proves.",
        predicted_mechanism="The unresolved change creates curiosity without a false promise.",
        expected_observation="The package receives a meaningful impressions test after launch.",
        decision_status="accepted",
        evidence_limitations="No thumbnail or exposure data exists yet.",
        recorded_at="2026-08-14T12:00:00+00:00",
    )
    updated = db.record_recommendation_outcome(
        created["recommendation_id"],
        "The package received sufficient exposure and CTR remained above its comparison cohort.",
        "More confident in mechanism-led titles; still uncertain about the thumbnail contribution.",
        outcome_as_of="2026-09-14T12:00:00+00:00",
    )
    rows = db.get_recommendations("67-donation")
    db.close()

    assert created["status"] == "inserted"
    assert updated["status"] == "updated"
    assert rows[0]["decision_status"] == "reviewed"
    assert rows[0]["predicted_mechanism"].startswith("The unresolved change")
    assert rows[0]["outcome_as_of"] == "2026-09-14T12:00:00+00:00"
    assert "thumbnail contribution" in rows[0]["revised_confidence"]


def test_recommendation_ledger_rejects_scores_as_a_decision_kind(tmp_path):
    db = KeywordDB(str(tmp_path / "keywords.db"))
    result = db.record_recommendation(
        project_slug="67-donation",
        decision_kind="score",
        recommendation="Pick the highest number.",
        rationale="It is highest.",
        predicted_mechanism="A score predicts success.",
    )
    db.close()
    assert "error" in result
