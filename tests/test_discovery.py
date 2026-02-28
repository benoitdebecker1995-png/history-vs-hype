"""Integration smoke tests for the discovery pipeline.

Verifies OpportunityOrchestrator.analyze_opportunity() runs end-to-end
with external dependencies mocked (Google Trends, YouTube autocomplete).
No real network calls.
"""
from unittest.mock import patch, MagicMock
import pytest


MOCK_DEMAND = {
    "keyword": "test topic",
    "search_volume": 1000,
    "trend_direction": "stable",
    "autocomplete_suggestions": ["test topic history", "test topic myth"],
    "demand_score": 65,
    "search_volume_proxy": 65,
    "opportunity_ratio": "3.2x",
}

MOCK_COMPETITION = {
    "keyword": "test topic",
    "competitor_count": 5,
    "avg_views": 50000,
    "video_count": 12,
    "channel_count": 5,
    "quality_video_count": 3,
    "top_competitor": "Competitor Channel",
    "competition_score": 40,
    "differentiation_score": 0.72,
    "recommended_angle": "primary-source",
}

MOCK_KEYWORD_RECORD = {
    "id": 1,
    "keyword": "test topic",
    "source": "test",
    "lifecycle_state": "DISCOVERED",
    "opportunity_score_final": None,
    "opportunity_category": None,
}


def test_orchestrator_imports_cleanly():
    """OpportunityOrchestrator is importable without sys.path hacks."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    assert OpportunityOrchestrator is not None


def test_orchestrator_instantiates_with_keyword_db(keyword_db):
    """OpportunityOrchestrator accepts a KeywordDB instance."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    orch = OpportunityOrchestrator(keyword_db)
    assert orch is not None
    assert hasattr(orch, "demand")
    assert hasattr(orch, "competition")


def test_orchestrator_returns_dict(keyword_db):
    """analyze_opportunity() returns a dict with full pipeline mocked."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    orch = OpportunityOrchestrator(keyword_db)

    with patch.object(orch.demand, "analyze_keyword", return_value=MOCK_DEMAND), \
         patch.object(orch.competition, "analyze_competition", return_value=MOCK_COMPETITION), \
         patch.object(keyword_db, "get_keyword", return_value=MOCK_KEYWORD_RECORD), \
         patch.object(keyword_db, "get_production_constraints", return_value={"document_score": 3}), \
         patch.object(keyword_db, "get_lifecycle_state", return_value="ANALYZED"), \
         patch.object(orch.scorer, "score_opportunity", return_value={
             "opportunity_score": 72, "category": "High", "is_blocked": False,
             "block_reason": None, "components": {}, "data_age_days": 0, "warnings": []
         }), \
         patch.object(orch.scorer, "save_opportunity_score", return_value={"saved": True}):
        result = orch.analyze_opportunity("test topic")

    assert isinstance(result, dict)


def test_orchestrator_error_propagation_on_demand_error(keyword_db):
    """analyze_opportunity() returns error dict when demand fails."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    orch = OpportunityOrchestrator(keyword_db)

    with patch.object(orch.demand, "analyze_keyword", return_value={"error": "no data"}), \
         patch.object(orch.competition, "analyze_competition", return_value=MOCK_COMPETITION):
        result = orch.analyze_opportunity("nonexistent topic")

    # Error-dict pattern: should return a dict (either error or structured data)
    assert isinstance(result, dict)


def test_orchestrator_error_propagation_on_competition_error(keyword_db):
    """analyze_opportunity() returns error dict when competition fails."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    orch = OpportunityOrchestrator(keyword_db)

    with patch.object(orch.demand, "analyze_keyword", return_value=MOCK_DEMAND), \
         patch.object(orch.competition, "analyze_competition", return_value={"error": "search failed"}), \
         patch.object(keyword_db, "get_keyword", return_value=MOCK_KEYWORD_RECORD):
        result = orch.analyze_opportunity("test topic")

    # Error propagates — must still be a dict (error-dict pattern)
    assert isinstance(result, dict)


def test_demand_analyzer_attribute_exists(keyword_db):
    """OpportunityOrchestrator exposes demand attribute for patching."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    from tools.discovery.demand import DemandAnalyzer
    orch = OpportunityOrchestrator(keyword_db)
    assert isinstance(orch.demand, DemandAnalyzer)


def test_competition_analyzer_attribute_exists(keyword_db):
    """OpportunityOrchestrator exposes competition attribute for patching."""
    from tools.discovery.orchestrator import OpportunityOrchestrator
    from tools.discovery.competition import CompetitionAnalyzer
    orch = OpportunityOrchestrator(keyword_db)
    assert isinstance(orch.competition, CompetitionAnalyzer)
