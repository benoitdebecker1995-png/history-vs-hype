"""
Pre-Flight Scorer — evaluates a video project before publishing.

Aggregates topic, script, title/metadata, and duration signals into
a single scorecard with a composite grade and actionable flags.
"""

from .scorer import run_preflight
from .formatter import format_preflight_report
from .demand_checker import run as run_demand_check

__all__ = ['run_preflight', 'format_preflight_report', 'run_demand_check']
