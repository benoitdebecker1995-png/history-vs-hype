"""Backward-compat shim. Business logic moved to KeywordStore, IntentClassifier, PerformanceTracker.
Infrastructure moved to schema_manager.py."""
from tools.discovery.schema_manager import KeywordDB, init_database  # noqa: F401
