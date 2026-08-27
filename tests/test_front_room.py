import json
import sqlite3
import zipfile
from pathlib import Path

import pytest

from tools.front_room import (
    ActiveProjectError,
    build_context,
    create_snapshot,
    resolve_active_project,
    scan_claim_risks,
    select_voice_examples,
)


def _active_tree(tmp_path: Path) -> Path:
    project = tmp_path / "video-projects" / "_IN_PRODUCTION" / "67-donation"
    project.mkdir(parents=True)
    (tmp_path / "ACTIVE_PROJECT").write_text(
        "video-projects/_IN_PRODUCTION/67-donation\n", encoding="utf-8"
    )
    (tmp_path / "CHANNEL.md").write_text(
        "# Channel\n\nCurrent unresolved channel problem: make normal chat useful.\n",
        encoding="utf-8",
    )
    (project / "PROJECT.md").write_text(
        "# Project\n\nNext unresolved problem: rewrite the bridge.\n", encoding="utf-8"
    )
    (project / "RESEARCH.md").write_text(
        "# Research\n\n## E01 — Manuscripts\nTwenty-five survive.\n\n"
        "## E02 — Steuco\nSteuco printed and dated the colophon.\n",
        encoding="utf-8",
    )
    (project / "SCRIPT.md").write_text(
        '# Script\n\nSetz says "twenty-five manuscripts survive."\n'
        "The law made denial a crime.\n[SHOW: manuscript]\n",
        encoding="utf-8",
    )
    return project


def test_resolve_active_project_requires_three_hot_files(tmp_path):
    project = _active_tree(tmp_path)
    active = resolve_active_project(tmp_path)
    assert active.path == project.resolve()
    assert active.project.name == "PROJECT.md"
    assert active.research.name == "RESEARCH.md"
    assert active.script.name == "SCRIPT.md"


def test_resolve_active_project_rejects_cold_pointer(tmp_path):
    project = _active_tree(tmp_path)
    cold = project / "_cold"
    cold.mkdir()
    (tmp_path / "ACTIVE_PROJECT").write_text(
        "video-projects/_IN_PRODUCTION/67-donation/_cold\n", encoding="utf-8"
    )
    with pytest.raises(ActiveProjectError):
        resolve_active_project(tmp_path)


def test_status_context_loads_only_project_snapshot(tmp_path):
    _active_tree(tmp_path)
    packet = build_context("status", root=tmp_path)
    assert [item["file"] for item in packet["loaded"]] == ["PROJECT.md"]
    assert all("_cold" not in value for value in packet["excluded"])
    assert "legacy control plane" in packet["excluded"]


def test_channel_context_does_not_turn_current_video_into_channel_strategy(tmp_path):
    _active_tree(tmp_path)
    packet = build_context("channel_status", root=tmp_path)
    assert [item["file"] for item in packet["loaded"]] == ["CHANNEL.md"]
    assert "67-donation" not in packet["loaded"][0]["content"]


def test_safe_claim_context_scans_full_script_and_selects_research(tmp_path):
    _active_tree(tmp_path)
    packet = build_context("safe_claim", query="manuscripts", root=tmp_path)
    names = [item["file"] for item in packet["loaded"]]
    assert names == ["PROJECT.md", "SCRIPT.md", "RESEARCH.md (selected sections)"]
    assert any(risk["category"] == "quotation" for risk in packet["claim_risks"])
    assert "E01" in packet["loaded"][2]["content"]
    assert "E02" not in packet["loaded"][2]["content"]


def test_claim_risk_scan_catches_distinct_failure_classes():
    risks = scan_claim_risks(
        'Motyka says "70,000".\nThe statute made denial illegal.\n'
        "Historians never dispute the number.\n[SHOW: translated document]\n"
        "The copy descends from a Latin source because the translator changed it.\n"
    )
    categories = {item["category"] for item in risks}
    assert {
        "quotation", "number_or_date", "legal", "absolute", "showability",
        "source_content", "translation", "causal_or_motive",
    } <= categories


def test_voice_retrieval_prefers_spontaneous_and_approved_evidence(tmp_path):
    project = _active_tree(tmp_path)
    adlib = project / "_adlib"
    adlib.mkdir()
    (adlib / "readthrough.md").write_text(
        "SPONTANEOUS: countries remember the part of the past they need.\n",
        encoding="utf-8",
    )
    calibration = tmp_path / "channel-data" / "calibration"
    calibration.mkdir(parents=True)
    (calibration / "CALIBRATION-CORPUS.md").write_text(
        "APPROVED: They changed what the document was supposed to prove.\n",
        encoding="utf-8",
    )
    results = select_voice_examples(
        "the document changed what people needed from the past", root=tmp_path
    )
    assert results
    assert {row["evidence"] for row in results} <= {"spontaneous", "approved"}


def test_voice_retrieval_does_not_return_analysis_about_voice(tmp_path):
    _active_tree(tmp_path)
    calibration = tmp_path / "channel-data" / "calibration"
    calibration.mkdir(parents=True)
    (calibration / "CALIBRATION-CORPUS.md").write_text(
        "### 62-15 APPROVED\nHarvest share predicts phrasing quality in the script. "
        'His actual wording was "The document changed what the claim could prove."\n',
        encoding="utf-8",
    )
    results = select_voice_examples("the document changed what the claim could prove", root=tmp_path)
    assert [row["text"] for row in results] == [
        "The document changed what the claim could prove."
    ]


def test_voice_context_carries_relevant_primary_examples(tmp_path):
    project = _active_tree(tmp_path)
    adlib = project / "_adlib"
    adlib.mkdir()
    (adlib / "readthrough.md").write_text(
        "SPONTANEOUS: The document changed what the claim could prove.", encoding="utf-8"
    )
    packet = build_context(
        "sounds_like_ai", query="the document changed what the claim could prove", root=tmp_path
    )
    assert packet["voice_examples"]
    assert packet["voice_examples"][0]["evidence"] == "spontaneous"


def test_voice_retrieval_searches_v3_raw_corpus_without_returning_labels(tmp_path):
    _active_tree(tmp_path)
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    (model / "VOICE-EVIDENCE.md").write_text(
        "# Evidence\n\nSPONTANEOUS [A2-007]: If you look at the document, "
        "the wording changes what the claim can prove.\n",
        encoding="utf-8",
    )
    results = select_voice_examples("document wording changes the claim", root=tmp_path)
    assert results[0]["text"].startswith("If you look at the document")
    assert results[0]["locator"] == "A2-007"
    assert results[0]["factual_scope"] == "voice_only"


def test_voice_retrieval_centers_long_raw_entry_on_matching_sentences(tmp_path):
    _active_tree(tmp_path)
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    filler = "This is unrelated setup language. " * 80
    (model / "VOICE-EVIDENCE.md").write_text(
        "SPONTANEOUS [A1-099]: " + filler
        + "If you look at the manuscript, the wording changes the legal claim. "
        + filler,
        encoding="utf-8",
    )
    results = select_voice_examples("manuscript wording legal claim", root=tmp_path)
    assert "manuscript" in results[0]["text"]
    assert len(results[0]["text"]) <= 1200


def test_decision_context_routes_relevant_creator_model_section(tmp_path):
    _active_tree(tmp_path)
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    (model / "OPERATING-MODEL.md").write_text(
        "# Model\n\n## Decisions\nSet criteria before searching.\n\n"
        "## Voice\nUse ordinary words.\n",
        encoding="utf-8",
    )
    packet = build_context("decision", query="criteria searching", root=tmp_path)
    assert [item["file"] for item in packet["loaded"]] == [
        "CHANNEL.md",
        "OPERATING-MODEL.md (selected sections)",
        "RECOMMENDATION-LEDGER.json",
    ]
    assert "Set criteria" in packet["loaded"][1]["content"]
    assert "Use ordinary words" not in packet["loaded"][1]["content"]


def test_strategy_intents_do_not_fall_through_to_historical_risk_packet(tmp_path):
    _active_tree(tmp_path)
    model = tmp_path / "channel-data" / "creator-model"
    model.mkdir(parents=True)
    (model / "OPERATING-MODEL.md").write_text(
        "# Model\n\n## Growth\nUse public evidence.\n\n"
        "## Packaging\nPromise only what the script supports.\n",
        encoding="utf-8",
    )

    expected = {
        "opportunity": {"OPERATING-MODEL.md (selected sections)", "MARKET-EVIDENCE.json",
                        "RECOMMENDATION-LEDGER.json"},
        "packaging": {"SCRIPT.md", "OPERATING-MODEL.md (selected sections)",
                      "PACKAGE-HISTORY.json", "RECOMMENDATION-LEDGER.json",
                      "MARKET-EVIDENCE.json"},
        "business": {"OPERATING-MODEL.md (selected sections)",
                     "CHANNEL-BUSINESS-EVIDENCE.json", "RECOMMENDATION-LEDGER.json"},
        "performance": {"OPERATING-MODEL.md (selected sections)", "PACKAGE-HISTORY.json",
                        "RECOMMENDATION-LEDGER.json", "PERFORMANCE-EVIDENCE.json"},
    }
    for intent, required in expected.items():
        packet = build_context(intent, query="Constantine package", root=tmp_path)
        names = {item["file"] for item in packet["loaded"]}
        assert required <= names
        assert packet["claim_risks"] == []
        assert "composite scores are never verdicts" in packet["decision_policy"]


def test_strategy_context_reports_missing_data_instead_of_substituting_scores(tmp_path):
    _active_tree(tmp_path)
    packet = build_context("opportunity", query="Constantine", root=tmp_path)
    market = next(item for item in packet["loaded"] if item["file"] == "MARKET-EVIDENCE.json")
    ledger = next(
        item for item in packet["loaded"] if item["file"] == "RECOMMENDATION-LEDGER.json"
    )
    assert "database missing" in market["content"]
    assert "database missing" in ledger["content"]
    assert "opportunity_score" not in market["content"]


def test_snapshot_contains_hot_state_but_not_cold_material(tmp_path):
    project = _active_tree(tmp_path)
    cold = project / "_cold"
    cold.mkdir()
    (cold / "old-research.md").write_text("stale", encoding="utf-8")
    snapshot = create_snapshot("script-lock", root=tmp_path, now="2026-08-13T120000Z")
    with zipfile.ZipFile(snapshot) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("MANIFEST.json"))
    assert {"PROJECT.md", "RESEARCH.md", "SCRIPT.md", "MANIFEST.json"} <= names
    assert not any("cold" in name.lower() for name in names)
    assert manifest["label"] == "script-lock"
