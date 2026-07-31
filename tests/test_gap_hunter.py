"""Tests for tools.discovery.gap_hunter — the comment-sweep candidate generator.

Pins the two pure units (tag_comment, aggregate_signals) and the intel.db v3
storage round-trip. Network fetching is not exercised here; the real-data check
is the live `--sweep --dry-run` run recorded in the digest.
"""
import json

import pytest

from tools.discovery.gap_hunter import (
    aggregate_barriers,
    aggregate_signals,
    classify_demand,
    reclassify_stored_signals,
    select_seed_videos,
    tag_comment,
    write_digest,
)
from tools.intel.kb_store import CURRENT_SCHEMA_VERSION, KBStore


# ---------------------------------------------------------------------------
# tag_comment
# ---------------------------------------------------------------------------

def test_short_comment_carries_no_signal():
    assert tag_comment("Great video!") == ([], [])
    assert tag_comment("") == ([], [])


def test_unmet_supply_fires_on_omission_language():
    patterns, matched = tag_comment(
        "Good overview but he skips the part where the treaty was actually renegotiated, "
        "which is the whole story."
    )
    assert "unmet_supply" in patterns
    assert matched  # the phrase that fired is retained as evidence


def test_pocket_fires_on_self_identification():
    patterns, _ = tag_comment(
        "As a Panamanian I never expected to see this covered properly by an English channel."
    )
    assert "pocket" in patterns


def test_pocket_requires_a_capitalised_demonym():
    """'as a kid' must not count as a national pocket."""
    patterns, _ = tag_comment(
        "as a kid i always wondered about these things and it stuck with me ever since honestly"
    )
    assert "pocket" not in patterns


def test_question_needs_a_real_question_not_a_lone_mark():
    patterns, _ = tag_comment(
        "So how did Panama actually get the canal back after all of that? Nobody explains it."
    )
    assert "question" in patterns

    patterns, _ = tag_comment("what? " * 12)
    assert "question" not in patterns


def test_a_comment_can_carry_several_patterns():
    patterns, matched = tag_comment(
        "As a Guyanese, why does nobody ever talk about how the Essequibo border was drawn? "
        "Every video skips it."
    )
    assert set(patterns) >= {"pocket", "unmet_supply", "question"}
    assert len(matched) == len(patterns)


# ---------------------------------------------------------------------------
# classify_demand — the barrier axis
# ---------------------------------------------------------------------------

def test_enclosure_fires_on_nobody_told_me():
    assert "enclosure" in classify_demand(
        "Why is this never taught in school? I did a history degree and had no idea about any of it."
    )


def test_language_fires_on_the_evidence_isnt_in_english():
    assert "language" in classify_demand(
        "The original text is in Dutch and there is no English translation anywhere, which is the "
        "whole problem with this debate."
    )


def test_ideology_fires_on_the_story_i_was_taught():
    assert "ideology" in classify_demand(
        "We were taught this in school as straight fact and it turns out to be nationalist "
        "propaganda from the 1930s."
    )


def test_method_fires_on_how_do_you_know():
    assert "method" in classify_demand(
        "Genuine question, how do we know any of this actually happened? What is the evidence base here?"
    )


def test_a_comment_can_hit_two_barriers_at_once():
    got = classify_demand(
        "We were taught the Latin says one thing but the original text says something else entirely, "
        "and nobody has ever translated it properly."
    )
    assert {"ideology", "language"} <= set(got)


def test_praise_carries_no_barrier():
    assert classify_demand("This was such a well made video, thank you so much for your work here.") == []


def test_short_comment_carries_no_barrier():
    assert classify_demand("propaganda") == []


# ---------------------------------------------------------------------------
# aggregate_barriers
# ---------------------------------------------------------------------------

def _bsignal(demand, likes, video_id="v1", channel="Chan A"):
    return {
        "text": "x" * 60, "likes": likes, "video_id": video_id,
        "channel_name": channel, "video_title": "T", "demand_types": demand,
    }


def test_barrier_ranking_is_empty_without_tags():
    assert aggregate_barriers([_bsignal([], 10)]) == []


def test_barrier_ranking_orders_by_likes_weight():
    signals = [
        _bsignal(["enclosure"], 500, "v1"),
        _bsignal(["enclosure"], 400, "v2"),
        _bsignal(["archive"], 2, "v3"),
    ]
    out = aggregate_barriers(signals)
    assert [b["barrier"] for b in out] == ["enclosure", "archive"]
    assert out[0]["videos"] == 2


def test_barrier_row_reports_share_and_like_distribution():
    signals = [_bsignal(["language"], 100), _bsignal(["ideology"], 10), _bsignal([], 0)]
    rows = {b["barrier"]: b for b in aggregate_barriers(signals)}
    assert rows["language"]["share_of_signals"] == pytest.approx(33.3, abs=0.1)
    assert rows["language"]["median_likes"] == 100


def test_median_not_mean_is_what_survives_an_outlier():
    """The real corpus had a single 10,104-like comment drag 'archive' to a mean
    of 176 on a median of 4. Barrier rows must expose that gap, not hide it."""
    signals = [_bsignal(["archive"], 1, f"v{i}") for i in range(9)] + [_bsignal(["archive"], 10_000, "v9")]
    row = aggregate_barriers(signals)[0]
    assert row["median_likes"] == 1
    assert row["mean_likes"] > 900          # the mean is wrecked
    assert row["median_likes"] < row["mean_likes"] / 100


def test_barriers_rank_by_frequency_not_by_likes():
    """One heavily-liked comment must not outrank a barrier voiced far more often."""
    signals = [_bsignal(["archive"], 50_000, "v0")] + [
        _bsignal(["language"], 1, f"v{i}") for i in range(1, 30)
    ]
    assert [b["barrier"] for b in aggregate_barriers(signals)] == ["language", "archive"]


def test_a_comment_on_two_barriers_counts_for_both():
    out = aggregate_barriers([_bsignal(["language", "ideology"], 50)])
    assert {b["barrier"] for b in out} == {"language", "ideology"}


# ---------------------------------------------------------------------------
# aggregate_signals
# ---------------------------------------------------------------------------

def _signal(text, likes=10, video_id="v1", channel="Chan A"):
    return {
        "text": text, "likes": likes, "video_id": video_id,
        "channel_name": channel, "video_title": "T", "patterns": ["question"],
    }


def test_terms_below_the_video_floor_are_dropped():
    signals = [_signal("The Essequibo question is never answered here.", video_id="v1")]
    assert aggregate_signals(signals, min_videos=2) == []


def test_term_recurring_across_videos_survives_and_ranks():
    signals = [
        _signal("The Essequibo border was never explained properly.", video_id="v1"),
        _signal("Nobody covers Essequibo at all.", video_id="v2", channel="Chan B"),
    ]
    out = aggregate_signals(signals, min_videos=2)
    terms = {t["term"] for t in out}
    assert "Essequibo" in terms
    row = next(t for t in out if t["term"] == "Essequibo")
    assert row["videos"] == 2
    assert row["channels"] == 2
    assert row["rank"] > 0


def test_stoplisted_openers_are_not_treated_as_topics():
    signals = [
        _signal("This is why the thing happened here.", video_id="v1"),
        _signal("Great explanation of what happened there.", video_id="v2"),
    ]
    terms = {t["term"] for t in aggregate_signals(signals, min_videos=2)}
    assert not ({"This", "Great", "Video"} & terms)


def test_cross_video_recurrence_outranks_a_single_busy_thread():
    """A question asked under several channels beats one loud thread — by design."""
    spread = [
        _signal("Ceuta and Melilla are never discussed.", likes=50, video_id="v1"),
        _signal("Why does nobody explain Ceuta?", likes=50, video_id="v2", channel="B"),
        _signal("Ceuta deserves its own video.", likes=50, video_id="v3", channel="C"),
    ]
    concentrated = [
        _signal("Kaliningrad is never discussed.", likes=50, video_id="v9"),
        _signal("Why does nobody explain Kaliningrad?", likes=50, video_id="v9b"),
    ]
    out = {t["term"]: t["rank"] for t in aggregate_signals(spread + concentrated, min_videos=2)}
    assert out["Ceuta"] > out["Kaliningrad"]


# ---------------------------------------------------------------------------
# intel.db v3 storage
# ---------------------------------------------------------------------------

def test_schema_version_reaches_v4(tmp_path):
    KBStore(tmp_path / "intel.db")
    assert CURRENT_SCHEMA_VERSION >= 4


def test_demand_types_survive_the_roundtrip(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    store.save_comment_signals([{
        "comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
        "text": "Why is this never taught in school? I had no idea.",
        "likes": 5, "reply_count": 0, "published_at": None,
        "patterns": ["question"], "matched_phrases": [],
        "demand_types": ["enclosure"],
    }])
    rows = store.get_comment_signals()
    assert rows[0]["demand_types"] == ["enclosure"]
    assert [r["comment_id"] for r in store.get_comment_signals(demand_type="enclosure")] == ["c1"]
    assert store.get_comment_signals(demand_type="language") == []


def test_reclassify_backfills_barriers_onto_stored_text(tmp_path):
    """A v3-era row has no demand_types; reclassify derives them from stored text."""
    store = KBStore(tmp_path / "intel.db")
    store.save_comment_signals([{
        "comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
        "text": "We were taught this as fact in school and it turns out to be pure propaganda.",
        "likes": 9, "reply_count": 0, "published_at": None,
        "patterns": ["question"], "matched_phrases": [], "demand_types": [],
    }])
    assert store.get_comment_signals()[0]["demand_types"] == []

    assert reclassify_stored_signals(store) == {"reclassified": 1}
    assert "ideology" in store.get_comment_signals()[0]["demand_types"]


def test_reclassify_errors_cleanly_on_an_empty_store(tmp_path):
    assert "error" in reclassify_stored_signals(KBStore(tmp_path / "intel.db"))


def test_reclassify_refuses_to_half_finish(tmp_path):
    """Hitting the row ceiling must fail loudly — a half-reclassified corpus
    mixes old and new tags and silently corrupts every cross-tab built on it."""
    store = KBStore(tmp_path / "intel.db")
    store.save_comment_signals([
        {"comment_id": f"c{i}", "video_id": "v1", "channel_id": "ch1", "author": "A",
         "text": "We were taught this in school and it was propaganda, plainly." + "x" * 20,
         "likes": i, "reply_count": 0, "published_at": None,
         "patterns": ["question"], "matched_phrases": [], "demand_types": []}
        for i in range(3)
    ])
    result = reclassify_stored_signals(store, batch=2)
    assert "error" in result and "partial reclassify" in result["error"]
    assert reclassify_stored_signals(store, batch=50) == {"reclassified": 3}


def test_comment_signal_roundtrip(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    saved = store.save_comment_signals([{
        "comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
        "text": "As a Belizean, why does nobody explain the ICJ case?",
        "likes": 42, "reply_count": 3, "published_at": "2026-01-01T00:00:00Z",
        "patterns": ["pocket", "question"], "matched_phrases": ["As a Belizean"],
    }])
    assert saved == {"saved": 1}

    rows = store.get_comment_signals()
    assert len(rows) == 1
    assert rows[0]["patterns"] == ["pocket", "question"]
    assert rows[0]["likes"] == 42


def test_resweeping_updates_rather_than_duplicates(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    base = {
        "comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
        "text": "t" * 50, "likes": 1, "reply_count": 0,
        "published_at": "2026-01-01T00:00:00Z", "patterns": ["question"],
        "matched_phrases": [],
    }
    store.save_comment_signals([base])
    store.save_comment_signals([{**base, "likes": 99}])

    rows = store.get_comment_signals()
    assert len(rows) == 1
    assert rows[0]["likes"] == 99


def test_sweep_ledger_lets_a_rerun_skip_swept_videos(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    assert store.get_swept_video_ids() == []
    store.record_comment_sweep("v1", "ch1", comments_fetched=100, signals_found=7)
    assert store.get_swept_video_ids() == ["v1"]


def test_pattern_filter_selects_only_that_tag(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    store.save_comment_signals([
        {"comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
         "text": "x" * 50, "likes": 1, "reply_count": 0, "published_at": None,
         "patterns": ["pocket"], "matched_phrases": []},
        {"comment_id": "c2", "video_id": "v1", "channel_id": "ch1", "author": "B",
         "text": "y" * 50, "likes": 1, "reply_count": 0, "published_at": None,
         "patterns": ["question"], "matched_phrases": []},
    ])
    assert [r["comment_id"] for r in store.get_comment_signals(pattern="pocket")] == ["c1"]


# ---------------------------------------------------------------------------
# seed selection + digest
# ---------------------------------------------------------------------------

def _seed_competitor_video(store, video_id, views, published_at, duration=600):
    conn = store._connect()
    conn.execute(
        "INSERT OR REPLACE INTO competitor_channels "
        "(channel_id, channel_name, added_at) VALUES ('ch1', 'Chan A', '2026-01-01')"
    )
    conn.execute(
        """INSERT OR REPLACE INTO competitor_videos
           (video_id, channel_id, title, published_at, views, duration_seconds,
            outlier_ratio, fetched_at)
           VALUES (?, 'ch1', 'T', ?, ?, ?, 2.0, '2026-01-01')""",
        (video_id, published_at, views, duration),
    )
    conn.commit()
    conn.close()


def test_seed_selection_skips_shorts_and_low_view_videos(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    _seed_competitor_video(store, "big", 500_000, "2026-01-01T00:00:00Z")
    _seed_competitor_video(store, "small", 100, "2026-01-01T00:00:00Z")
    _seed_competitor_video(store, "short", 500_000, "2026-01-01T00:00:00Z", duration=45)

    ids = [v["video_id"] for v in select_seed_videos(store, min_views=50_000, published_after="2025-01-01")]
    assert ids == ["big"]


def test_seed_selection_skips_already_swept(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    _seed_competitor_video(store, "big", 500_000, "2026-01-01T00:00:00Z")
    store.record_comment_sweep("big", "ch1", 10, 1)
    assert select_seed_videos(store, published_after="2025-01-01") == []
    assert len(select_seed_videos(store, published_after="2025-01-01", skip_swept=False)) == 1


def test_digest_errors_cleanly_on_an_empty_harvest(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    result = write_digest(store, tmp_path / "digest.md")
    assert "error" in result


def test_digest_writes_a_readable_file(tmp_path):
    store = KBStore(tmp_path / "intel.db")
    _seed_competitor_video(store, "v1", 500_000, "2026-01-01T00:00:00Z")
    _seed_competitor_video(store, "v2", 500_000, "2026-01-01T00:00:00Z")
    store.save_comment_signals([
        {"comment_id": "c1", "video_id": "v1", "channel_id": "ch1", "author": "A",
         "text": "As a Belizean, why does nobody ever explain the Sarstoon river dispute?",
         "likes": 300, "reply_count": 0, "published_at": None,
         "patterns": ["pocket", "question"], "matched_phrases": ["As a Belizean"]},
        {"comment_id": "c2", "video_id": "v2", "channel_id": "ch1", "author": "B",
         "text": "Every video skips the Sarstoon and it is the actual live dispute right now.",
         "likes": 120, "reply_count": 0, "published_at": None,
         "patterns": ["unmet_supply"], "matched_phrases": ["skips"]},
    ])
    out = tmp_path / "digest.md"
    result = write_digest(store, out)
    assert result["signals"] == 2

    text = out.read_text(encoding="utf-8")
    assert "GAP-HUNTER HARVEST DIGEST" in text
    assert "Sarstoon" in text
    assert "Rank informs, it does not decide" in text
