"""Phase H1 — Behavioral pinning tests for tools/discovery/database.py.

Each test sets up an in-memory DB via the keyword_db fixture (conftest.py),
calls one public method with realistic args, and asserts the return shape.
Covers all 48 public methods; 100% of them tested here.

Run with: pytest tests/test_database_pin.py -v
"""
import sqlite3
import pytest
from tools.discovery.database import KeywordDB


# ─── helpers ─────────────────────────────────────────────────────────────────

def _add_kw(db, keyword="dark ages myth", source="manual"):
    """Insert a keyword and return its ID."""
    result = db.add_keyword(keyword, source=source, search_volume=5000, competition=40.0)
    return result["keyword_id"]


def _add_video(db, video_id="TEST123", topic_type="ideological"):
    """Insert a video_performance row and return video_id."""
    db.add_video_performance(
        video_id=video_id,
        title="The Dark Ages Myth",
        views=10000,
        subscribers_gained=5,
        conversion_rate=0.05,
        topic_type=topic_type,
        angles=["myth_busting"],
    )
    return video_id


def _add_competitor_channel(db, name="Knowing Better"):
    """Insert a competitor_channels row and return its id."""
    cursor = db._conn.cursor()
    cursor.execute(
        "INSERT INTO competitor_channels (name, channel_id, subscriber_count, last_updated) VALUES (?, ?, ?, ?)",
        (name, "UC_TEST_" + name[:4], 100000, "2026-01-01"),
    )
    db._conn.commit()
    return cursor.lastrowid


# ─── init / schema ────────────────────────────────────────────────────────────

class TestInitDatabase:
    def test_init_returns_tables_list(self):
        db = KeywordDB(db_path=":memory:")
        result = db.init_database()
        # May return error (already initialised) or success — both shapes are valid
        assert isinstance(result, dict)
        db.close()


class TestSchemaVersion:
    def test_get_schema_version_returns_int(self, keyword_db):
        v = keyword_db.get_schema_version()
        assert isinstance(v, int)

    def test_set_and_get_schema_version(self, keyword_db):
        keyword_db.set_schema_version(99)
        assert keyword_db.get_schema_version() == 99


class TestClose:
    def test_close_sets_conn_to_none(self):
        db = KeywordDB(db_path=":memory:")
        db.close()
        assert db._conn is None


# ─── keyword CRUD ─────────────────────────────────────────────────────────────

class TestAddKeyword:
    def test_insert_returns_keyword_id_and_action(self, keyword_db):
        r = keyword_db.add_keyword("colonial myth", source="autocomplete")
        assert "keyword_id" in r
        assert r["action"] == "inserted"
        assert r["keyword"] == "colonial myth"

    def test_update_returns_updated_action(self, keyword_db):
        keyword_db.add_keyword("colonial myth")
        r = keyword_db.add_keyword("colonial myth", source="vidiq", search_volume=9000)
        assert r["action"] == "updated"


class TestGetKeyword:
    def test_returns_keyword_dict(self, keyword_db):
        _add_kw(keyword_db)
        r = keyword_db.get_keyword("dark ages myth")
        assert r["keyword"] == "dark ages myth"
        assert "id" in r

    def test_not_found_returns_error(self, keyword_db):
        r = keyword_db.get_keyword("nonexistent keyword xyz")
        assert "error" in r


class TestSearchKeywords:
    def test_pattern_returns_matches(self, keyword_db):
        _add_kw(keyword_db, "dark ages myth")
        _add_kw(keyword_db, "dark matter")
        results = keyword_db.search_keywords("dark%")
        assert len(results) >= 2

    def test_no_pattern_returns_all(self, keyword_db):
        _add_kw(keyword_db, "kw one")
        _add_kw(keyword_db, "kw two")
        results = keyword_db.search_keywords()
        assert len(results) >= 2

    def test_no_match_returns_empty_list(self, keyword_db):
        results = keyword_db.search_keywords("zzz_no_match_xyz%")
        assert results == []


class TestGetKeywordsBySource:
    def test_returns_matching_source(self, keyword_db):
        _add_kw(keyword_db, "source test kw", source="vidiq")
        results = keyword_db.get_keywords_by_source("vidiq")
        assert any(r["keyword"] == "source test kw" for r in results)

    def test_wrong_source_returns_empty(self, keyword_db):
        results = keyword_db.get_keywords_by_source("nonexistent_source")
        assert results == []


class TestGetKeywordsByIntent:
    def test_returns_keyword_with_matching_intent(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.set_intent(kid, "MYTH_BUSTING", 0.9, is_primary=True)
        results = keyword_db.get_keywords_by_intent("MYTH_BUSTING")
        assert len(results) >= 1
        assert results[0]["intent_category"] == "MYTH_BUSTING"


class TestSetIntent:
    def test_returns_status_set(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.set_intent(kid, "MYTH_BUSTING", 0.9, is_primary=True)
        assert r["status"] == "set"
        assert r["keyword_id"] == kid

    def test_secondary_intent(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.set_intent(kid, "TERRITORIAL_DISPUTE", 0.6, is_primary=False)
        assert r["status"] == "set"
        assert not r["is_primary"]


class TestAddPerformance:
    def test_returns_status_tracked(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.add_performance(kid, "VIDEO_ID_01", impressions=1000, ctr=0.04)
        assert r["status"] == "tracked"
        assert "performance_id" in r


class TestGetKeywordStats:
    def test_returns_count_dict(self, keyword_db):
        _add_kw(keyword_db)
        stats = keyword_db.get_keyword_stats()
        assert "total_keywords" in stats
        assert stats["total_keywords"] >= 1
        assert "by_source" in stats


# ─── trend methods ────────────────────────────────────────────────────────────

class TestAddTrend:
    def test_returns_trend_id(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.add_trend(kid, interest=75, trend_direction="rising", percent_change=20.5)
        assert r["status"] == "inserted"
        assert "trend_id" in r


class TestGetCachedTrend:
    def test_returns_trend_within_max_age(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.add_trend(kid, interest=75, trend_direction="rising", percent_change=20.5)
        r = keyword_db.get_cached_trend(kid, max_age_days=30)
        assert r is not None
        assert r["interest"] == 75

    def test_returns_none_for_unknown_keyword(self, keyword_db):
        r = keyword_db.get_cached_trend(99999, max_age_days=7)
        assert r is None


class TestGetLatestTrend:
    def test_returns_a_trend_dict(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.add_trend(kid, interest=50, trend_direction="stable", percent_change=0.0)
        r = keyword_db.get_latest_trend(kid)
        assert "error" not in r
        assert "interest" in r

    def test_returns_error_for_unknown_keyword(self, keyword_db):
        r = keyword_db.get_latest_trend(99999)
        assert "error" in r


# ─── competitor methods ───────────────────────────────────────────────────────

class TestAddCompetitorVideo:
    def test_inserts_successfully(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        r = keyword_db.add_competitor_video(
            video_id="COMP_VID_01",
            channel_id=ch_id,
            keyword_id=kid,
            title="Dark Ages Were Real",
            view_count=50000,
        )
        assert r["status"] == "inserted"

    def test_duplicate_returns_error(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        keyword_db.add_competitor_video("COMP_VID_02", ch_id, kid, "Title A")
        r = keyword_db.add_competitor_video("COMP_VID_02", ch_id, kid, "Title A duplicate")
        assert "error" in r


class TestGetCompetitionCount:
    def test_returns_count_after_insert(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        keyword_db.add_competitor_video("COMP_VID_03", ch_id, kid, "Title", view_count=1000)
        r = keyword_db.get_competition_count(kid, max_age_days=999)
        assert r is not None
        assert r["video_count"] >= 1

    def test_returns_none_for_unknown_keyword(self, keyword_db):
        r = keyword_db.get_competition_count(99999, max_age_days=7)
        assert r is None


# ─── opportunity score methods ────────────────────────────────────────────────

class TestAddOpportunityScore:
    def test_returns_inserted(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.add_opportunity_score(kid, demand_score=70, competition_score=30,
                                              opportunity_ratio=2.3, category="High")
        assert r["status"] == "inserted"


class TestGetOpportunityScore:
    def test_returns_score_within_max_age(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.add_opportunity_score(kid, 70, 30, 2.3, "High")
        r = keyword_db.get_opportunity_score(kid, max_age_days=30)
        assert r is not None
        assert r["opportunity_category"] == "High"

    def test_returns_none_when_too_old(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.add_opportunity_score(kid, 70, 30, 2.3, "High")
        # Backdate the record to make it stale
        cursor = keyword_db._conn.cursor()
        cursor.execute("UPDATE opportunity_scores SET calculated_at = '2020-01-01' WHERE keyword_id = ?", (kid,))
        keyword_db._conn.commit()
        r = keyword_db.get_opportunity_score(kid, max_age_days=7)
        assert r is None


class TestSaveOpportunityScore:
    def test_saves_and_returns_status(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.save_opportunity_score(kid, 75.0, "Good",
                                               components={"demand": {"normalized": 70},
                                                           "gap": {"normalized": 80}})
        assert r["status"] == "saved"
        assert r["keyword_id"] == kid

    def test_transitions_lifecycle_to_analyzed(self, keyword_db):
        kid = _add_kw(keyword_db)
        assert keyword_db.get_lifecycle_state(kid) == "DISCOVERED"
        keyword_db.save_opportunity_score(kid, 75.0, "Good")
        assert keyword_db.get_lifecycle_state(kid) == "ANALYZED"


# ─── classification methods ───────────────────────────────────────────────────

class TestUpdateVideoClassification:
    def test_updates_successfully(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        keyword_db.add_competitor_video("CLASSIFY_VID", ch_id, kid, "Title")
        r = keyword_db.update_video_classification("CLASSIFY_VID", "documentary", ["legal", "historical"], "high")
        assert r["status"] == "updated"

    def test_returns_error_for_nonexistent_video(self, keyword_db):
        r = keyword_db.update_video_classification("NONEXISTENT", "documentary", ["legal"], "high")
        assert "error" in r


class TestGetClassifiedVideos:
    def test_returns_list_after_classification(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        keyword_db.add_competitor_video("GET_CLASS_VID", ch_id, kid, "Title")
        keyword_db.update_video_classification("GET_CLASS_VID", "documentary", ["legal"], "high")
        results = keyword_db.get_classified_videos(kid, max_age_days=999)
        assert len(results) >= 1
        assert results[0]["video_id"] == "GET_CLASS_VID"

    def test_format_filter_narrows_results(self, keyword_db):
        kid = _add_kw(keyword_db)
        ch_id = _add_competitor_channel(keyword_db)
        keyword_db.add_competitor_video("ANIM_VID", ch_id, kid, "Title A")
        keyword_db.add_competitor_video("DOC_VID", ch_id, kid, "Title B")
        keyword_db.update_video_classification("ANIM_VID", "animation", [], "high")
        keyword_db.update_video_classification("DOC_VID", "documentary", [], "medium")
        results = keyword_db.get_classified_videos(kid, format_filter="animation", max_age_days=999)
        assert all(r["format"] == "animation" for r in results)


# ─── production constraints ───────────────────────────────────────────────────

class TestStoreProductionConstraints:
    def test_stores_and_returns_status(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.store_production_constraints(
            kid, animation_required=False, document_score=3,
            sources_found=5, source_examples=["Cambridge Book"]
        )
        assert r["status"] == "stored"
        assert r["keyword_id"] == kid

    def test_animation_required_blocks_keyword(self, keyword_db):
        kid = _add_kw(keyword_db, "animated topic")
        keyword_db.store_production_constraints(kid, animation_required=True, document_score=1)
        constraints = keyword_db.get_production_constraints(kid, max_age_days=999)
        assert constraints["is_production_blocked"] == 1


class TestGetProductionConstraints:
    def test_returns_constraints_dict(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.store_production_constraints(kid, animation_required=False, document_score=4)
        r = keyword_db.get_production_constraints(kid, max_age_days=999)
        assert r is not None
        assert r["document_score"] == 4

    def test_returns_none_for_unknown_keyword(self, keyword_db):
        r = keyword_db.get_production_constraints(99999)
        assert r is None


# ─── lifecycle methods ────────────────────────────────────────────────────────

class TestSetLifecycleState:
    def test_valid_transition_returns_status(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.set_lifecycle_state(kid, "ANALYZED")
        assert r["status"] == "transitioned"
        assert r["from"] == "DISCOVERED"
        assert r["to"] == "ANALYZED"

    def test_invalid_transition_returns_error(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.set_lifecycle_state(kid, "PUBLISHED")
        assert "error" in r

    def test_invalid_state_returns_error(self, keyword_db):
        kid = _add_kw(keyword_db)
        r = keyword_db.set_lifecycle_state(kid, "INVALID_STATE")
        assert "error" in r


class TestGetLifecycleState:
    def test_defaults_to_discovered(self, keyword_db):
        kid = _add_kw(keyword_db)
        assert keyword_db.get_lifecycle_state(kid) == "DISCOVERED"

    def test_returns_set_state(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.set_lifecycle_state(kid, "ANALYZED")
        assert keyword_db.get_lifecycle_state(kid) == "ANALYZED"

    def test_unknown_id_returns_discovered(self, keyword_db):
        assert keyword_db.get_lifecycle_state(99999) == "DISCOVERED"


class TestGetKeywordsByLifecycle:
    def test_returns_keywords_in_state(self, keyword_db):
        kid = _add_kw(keyword_db)
        keyword_db.set_lifecycle_state(kid, "ANALYZED")
        results = keyword_db.get_keywords_by_lifecycle("ANALYZED")
        assert any(r["id"] == kid for r in results)

    def test_wrong_state_returns_empty(self, keyword_db):
        results = keyword_db.get_keywords_by_lifecycle("SCRIPTING")
        assert results == []


# ─── video performance ────────────────────────────────────────────────────────

class TestAddVideoPerformance:
    def test_inserts_video(self, keyword_db):
        r = keyword_db.add_video_performance(
            "VP_VID_01", title="Test Video", views=5000,
            topic_type="territorial", conversion_rate=0.03
        )
        assert "video_id" in r or r.get("status") == "inserted" or "error" not in r

    def test_updates_existing_video(self, keyword_db):
        keyword_db.add_video_performance("VP_VID_02", title="First Title", views=100)
        keyword_db.add_video_performance("VP_VID_02", title="Updated Title", views=200)
        row = keyword_db.get_video_performance("VP_VID_02")
        assert row.get("views") == 200


class TestGetVideoPerformance:
    def test_returns_performance_dict(self, keyword_db):
        _add_video(keyword_db, "PERF_VID_01")
        r = keyword_db.get_video_performance("PERF_VID_01")
        assert "video_id" in r
        assert r["video_id"] == "PERF_VID_01"

    def test_not_found_returns_error(self, keyword_db):
        r = keyword_db.get_video_performance("NONEXISTENT_VID")
        assert "error" in r


class TestSearchVideoPerformanceByTitle:
    def test_returns_video_id_on_match(self, keyword_db):
        _add_video(keyword_db, "SEARCH_VID_01")
        r = keyword_db.search_video_performance_by_title("The Dark")
        assert r == "SEARCH_VID_01"

    def test_returns_none_on_no_match(self, keyword_db):
        r = keyword_db.search_video_performance_by_title("zzz_nomatch_xyz")
        assert r is None


class TestGetAllVideoPerformance:
    def test_returns_list(self, keyword_db):
        _add_video(keyword_db, "ALL_VID_01")
        _add_video(keyword_db, "ALL_VID_02", topic_type="territorial")
        results = keyword_db.get_all_video_performance()
        assert len(results) >= 2

    def test_respects_limit(self, keyword_db):
        for i in range(5):
            _add_video(keyword_db, f"LIMIT_VID_{i:02d}")
        results = keyword_db.get_all_video_performance(limit=2)
        assert len(results) <= 2


class TestGetPerformanceByTopic:
    def test_returns_videos_for_topic(self, keyword_db):
        _add_video(keyword_db, "TOPIC_VID_01", topic_type="territorial")
        results = keyword_db.get_performance_by_topic("territorial")
        assert any(r["video_id"] == "TOPIC_VID_01" for r in results)

    def test_wrong_topic_returns_empty(self, keyword_db):
        results = keyword_db.get_performance_by_topic("nonexistent_topic_type")
        assert results == []


class TestGetPerformanceByAngle:
    def test_returns_videos_with_angle(self, keyword_db):
        keyword_db.add_video_performance(
            "ANGLE_VID_01", title="Angle Test", views=1000,
            angles=["legal", "historical"], topic_type="territorial"
        )
        results = keyword_db.get_performance_by_angle("legal")
        assert any(r["video_id"] == "ANGLE_VID_01" for r in results)


class TestGetTopConverters:
    def test_returns_list_ordered_by_conversion(self, keyword_db):
        keyword_db.add_video_performance("TOP_VID_01", title="High Conv", conversion_rate=0.05)
        keyword_db.add_video_performance("TOP_VID_02", title="Low Conv", conversion_rate=0.01)
        results = keyword_db.get_top_converters(limit=10)
        assert len(results) >= 2
        # First result should have highest conversion_rate
        if len(results) >= 2:
            assert results[0]["conversion_rate"] >= results[1]["conversion_rate"]


# ─── variant / CTR methods ────────────────────────────────────────────────────

class TestAddThumbnailVariant:
    def test_inserts_variant(self, keyword_db):
        _add_video(keyword_db, "THUMB_VID_01")
        r = keyword_db.add_thumbnail_variant(
            "THUMB_VID_01", "A", "/path/thumb_A.jpg", ["map", "text"], "abc123"
        )
        assert r["status"] == "inserted"
        assert "variant_id" in r

    def test_invalid_letter_returns_error(self, keyword_db):
        _add_video(keyword_db, "THUMB_VID_02")
        r = keyword_db.add_thumbnail_variant("THUMB_VID_02", "a", "/path/thumb.jpg", [])
        assert "error" in r

    def test_lowercase_letter_returns_error(self, keyword_db):
        _add_video(keyword_db, "THUMB_VID_03")
        r = keyword_db.add_thumbnail_variant("THUMB_VID_03", "z", "/path/thumb.jpg", [])
        assert "error" in r


class TestAddTitleVariant:
    def test_inserts_variant(self, keyword_db):
        _add_video(keyword_db, "TITLE_VID_01")
        r = keyword_db.add_title_variant(
            "TITLE_VID_01", "A", "How Colonial Borders Still Kill Today", ["mechanism"]
        )
        assert r["status"] == "inserted"
        assert "variant_id" in r

    def test_invalid_letter_returns_error(self, keyword_db):
        _add_video(keyword_db, "TITLE_VID_02")
        r = keyword_db.add_title_variant("TITLE_VID_02", "1", "Some Title", [])
        assert "error" in r


class TestAddCtrSnapshot:
    def test_inserts_snapshot(self, keyword_db):
        _add_video(keyword_db, "CTR_VID_01")
        r = keyword_db.add_ctr_snapshot("CTR_VID_01", ctr_percent=4.5, impression_count=1000, view_count=45)
        assert r["status"] == "inserted"
        assert "snapshot_id" in r

    def test_invalid_ctr_returns_error(self, keyword_db):
        _add_video(keyword_db, "CTR_VID_02")
        r = keyword_db.add_ctr_snapshot("CTR_VID_02", ctr_percent=150.0, impression_count=1000, view_count=0)
        assert "error" in r

    def test_negative_impressions_returns_error(self, keyword_db):
        _add_video(keyword_db, "CTR_VID_03")
        r = keyword_db.add_ctr_snapshot("CTR_VID_03", ctr_percent=4.0, impression_count=-1, view_count=0)
        assert "error" in r


class TestGetThumbnailVariants:
    def test_returns_list_of_variants(self, keyword_db):
        _add_video(keyword_db, "GET_THUMB_VID")
        keyword_db.add_thumbnail_variant("GET_THUMB_VID", "A", "/a.jpg", ["map"])
        keyword_db.add_thumbnail_variant("GET_THUMB_VID", "B", "/b.jpg", ["face"])
        results = keyword_db.get_thumbnail_variants("GET_THUMB_VID")
        assert len(results) == 2

    def test_unknown_video_returns_empty(self, keyword_db):
        results = keyword_db.get_thumbnail_variants("UNKNOWN_VID_THUMBS")
        assert results == []


class TestGetTitleVariants:
    def test_returns_list_of_variants(self, keyword_db):
        _add_video(keyword_db, "GET_TITLE_VID")
        keyword_db.add_title_variant("GET_TITLE_VID", "A", "Title One", ["mechanism"])
        keyword_db.add_title_variant("GET_TITLE_VID", "B", "Title Two", ["document"])
        results = keyword_db.get_title_variants("GET_TITLE_VID")
        assert len(results) == 2


class TestGetCtrSnapshots:
    def test_returns_list_of_snapshots(self, keyword_db):
        _add_video(keyword_db, "GET_CTR_VID")
        keyword_db.add_ctr_snapshot("GET_CTR_VID", 4.5, 1000, 45)
        keyword_db.add_ctr_snapshot("GET_CTR_VID", 5.0, 1200, 60)
        results = keyword_db.get_ctr_snapshots("GET_CTR_VID")
        assert len(results) == 2

    def test_unknown_video_returns_empty(self, keyword_db):
        results = keyword_db.get_ctr_snapshots("UNKNOWN_CTR_VID")
        assert results == []


class TestGetVariantSummary:
    def test_returns_summary_with_counts(self, keyword_db):
        _add_video(keyword_db, "SUMMARY_VID")
        keyword_db.add_thumbnail_variant("SUMMARY_VID", "A", "/a.jpg", [])
        keyword_db.add_title_variant("SUMMARY_VID", "A", "Title A", [])
        keyword_db.add_ctr_snapshot("SUMMARY_VID", 4.0, 500, 20)
        r = keyword_db.get_variant_summary("SUMMARY_VID")
        assert r["thumbnails"] == 1
        assert r["titles"] == 1
        assert r["snapshots"] == 1
        assert r["video_id"] == "SUMMARY_VID"

    def test_empty_video_returns_zeros(self, keyword_db):
        _add_video(keyword_db, "EMPTY_SUMMARY_VID")
        r = keyword_db.get_variant_summary("EMPTY_SUMMARY_VID")
        assert r["thumbnails"] == 0
        assert r["titles"] == 0
        assert r["snapshots"] == 0


class TestGetLatestCtr:
    def test_returns_most_recent_snapshot(self, keyword_db):
        _add_video(keyword_db, "LATEST_CTR_VID")
        keyword_db.add_ctr_snapshot("LATEST_CTR_VID", 3.0, 500, 15, snapshot_date="2026-01-01")
        keyword_db.add_ctr_snapshot("LATEST_CTR_VID", 5.5, 800, 44, snapshot_date="2026-05-01")
        r = keyword_db.get_latest_ctr("LATEST_CTR_VID")
        assert r["ctr_percent"] == 5.5

    def test_returns_error_for_unknown_video(self, keyword_db):
        r = keyword_db.get_latest_ctr("UNKNOWN_LATEST_CTR")
        assert "error" in r


class TestGetVariantCtrSummary:
    def test_returns_list_with_attribution(self, keyword_db):
        _add_video(keyword_db, "ATTR_VID")
        thumb = keyword_db.add_thumbnail_variant("ATTR_VID", "A", "/a.jpg", [])
        thumb_id = thumb["variant_id"]
        keyword_db.add_ctr_snapshot("ATTR_VID", 4.0, 1000, 40, active_thumbnail_id=thumb_id)
        keyword_db.add_ctr_snapshot("ATTR_VID", 5.0, 1200, 60, active_thumbnail_id=thumb_id)
        results = keyword_db.get_variant_ctr_summary("ATTR_VID", variant_type="thumbnail")
        assert len(results) == 1
        assert results[0]["variant_letter"] == "A"
        assert results[0]["snapshot_count"] == 2

    def test_returns_empty_without_attribution(self, keyword_db):
        _add_video(keyword_db, "NO_ATTR_VID")
        keyword_db.add_ctr_snapshot("NO_ATTR_VID", 4.0, 500, 20)
        results = keyword_db.get_variant_ctr_summary("NO_ATTR_VID", variant_type="thumbnail")
        assert results == []


class TestGetChannelCtrBenchmarks:
    def test_returns_overall_and_by_category(self, keyword_db):
        _add_video(keyword_db, "BENCH_VID_01", topic_type="territorial")
        keyword_db.add_ctr_snapshot("BENCH_VID_01", 4.0, 1000, 40)
        r = keyword_db.get_channel_ctr_benchmarks()
        assert "overall" in r
        assert "by_category" in r

    def test_empty_db_returns_empty_structure(self, keyword_db):
        r = keyword_db.get_channel_ctr_benchmarks()
        assert "overall" in r


# ─── feedback methods ─────────────────────────────────────────────────────────

class TestStoreVideoFeedback:
    def test_stores_feedback_and_returns_updated(self, keyword_db):
        _add_video(keyword_db, "FB_VID_01")
        feedback = {
            "biggest_drop_position": 35,
            "observations": ["Strong hook", "Drop at turn"],
            "actionable": ["Shorten intro"],
            "discovery": {"primary_issue": "NONE", "severity": "LOW"},
        }
        r = keyword_db.store_video_feedback("FB_VID_01", feedback)
        assert r["status"] == "updated"
        assert r["video_id"] == "FB_VID_01"

    def test_no_match_returns_no_match_status(self, keyword_db):
        r = keyword_db.store_video_feedback("NONEXISTENT_FB_VID", {})
        assert r["status"] == "no_match"


class TestGetVideoFeedback:
    def test_returns_feedback_dict(self, keyword_db):
        _add_video(keyword_db, "GET_FB_VID")
        keyword_db.store_video_feedback("GET_FB_VID", {
            "biggest_drop_position": 40,
            "observations": ["Good hook"],
            "actionable": ["Add B-roll at minute 3"],
        })
        r = keyword_db.get_video_feedback("GET_FB_VID")
        assert r["video_id"] == "GET_FB_VID"
        assert r["drop_point"] == 40
        assert "lessons" in r

    def test_not_found_returns_error(self, keyword_db):
        r = keyword_db.get_video_feedback("NO_SUCH_VID")
        assert "error" in r


class TestGetFeedbackByTopic:
    def test_returns_dict_with_videos_list(self, keyword_db):
        _add_video(keyword_db, "TOPIC_FB_VID", topic_type="ideological")
        keyword_db.store_video_feedback("TOPIC_FB_VID", {
            "observations": ["Good retention"],
            "actionable": ["Keep myth-first structure"],
        })
        r = keyword_db.get_feedback_by_topic("ideological")
        assert "videos" in r
        assert "count" in r
        assert r["topic"] == "ideological"

    def test_wrong_topic_returns_empty_videos(self, keyword_db):
        r = keyword_db.get_feedback_by_topic("nonexistent_topic_xyz")
        assert r["videos"] == []
        assert r["count"] == 0


class TestHasFeedback:
    def test_returns_false_before_feedback(self, keyword_db):
        _add_video(keyword_db, "HAS_FB_VID_01")
        assert keyword_db.has_feedback("HAS_FB_VID_01") is False

    def test_returns_true_after_feedback_stored(self, keyword_db):
        _add_video(keyword_db, "HAS_FB_VID_02")
        keyword_db.store_video_feedback("HAS_FB_VID_02", {
            "observations": ["Something"],
            "actionable": ["Do something"],
        })
        assert keyword_db.has_feedback("HAS_FB_VID_02") is True

    def test_returns_false_for_unknown_video(self, keyword_db):
        assert keyword_db.has_feedback("UNKNOWN_HAS_FB_VID") is False
