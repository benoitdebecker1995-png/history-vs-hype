"""
Tests for validate_rolling_against_lifetime (Codex spec §1.A, 2026-07-22).

Guards the collector double-count: rolling (≤30-day) impressions can never
exceed lifetime. Regression anchor: #59 rolling 20,919 vs lifetime 10,925.
"""
import unittest
from datetime import date

from tools.youtube_analytics.ctr_tracker import validate_rolling_against_lifetime

WIN_END = date(2026, 7, 23)
FRESH = date(2026, 7, 23)   # studio_as_of >= window end -> compare
STALE = date(2026, 2, 23)   # studio predates window -> skip


class TestValidator(unittest.TestCase):
    def test_rolling_below_or_equal_lifetime_passes(self):
        r = {"a": {"impression_count": 900, "ctr_percent": 2.0},
             "b": {"impression_count": 500, "ctr_percent": 1.0}}
        life = {"a": {"impressions": 1000}, "b": {"impressions": 500}}  # equal ok
        res = validate_rolling_against_lifetime(r, life, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertTrue(res.ok)
        self.assertEqual(res.failures, [])

    def test_rolling_above_lifetime_fails(self):
        r = {"a": {"impression_count": 1200, "ctr_percent": 2.0}}
        life = {"a": {"impressions": 1000}}
        res = validate_rolling_against_lifetime(r, life, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertFalse(res.ok)
        self.assertTrue(any("double-count" in f for f in res.failures))

    def test_stale_studio_skips_lifetime_comparison_with_warning(self):
        r = {"a": {"impression_count": 99999, "ctr_percent": 2.0}}  # would fail if compared
        life = {"a": {"impressions": 1000}}
        res = validate_rolling_against_lifetime(r, life, studio_as_of=STALE, reporting_window_end=WIN_END)
        self.assertTrue(res.ok)                      # not compared
        self.assertTrue(res.warnings)

    def test_missing_video_ids_are_unverified_not_failed(self):
        r = {"a": {"impression_count": 500, "ctr_percent": 2.0}}
        life = {}  # no lifetime rows
        res = validate_rolling_against_lifetime(r, life, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertTrue(res.ok)
        self.assertIn("a", res.unverified)

    def test_59_regression_fixture_fails(self):
        r = {"OHWq4jY8iAY": {"impression_count": 20919, "ctr_percent": 1.54}}
        life = {"OHWq4jY8iAY": {"impressions": 10925}}
        res = validate_rolling_against_lifetime(r, life, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertFalse(res.ok)

    def test_internal_invariants_run_without_lifetime(self):
        r = {"a": {"impression_count": -5, "ctr_percent": 150.0}}
        res = validate_rolling_against_lifetime(r, {}, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertFalse(res.ok)
        self.assertEqual(len(res.failures), 2)  # negative impressions + CTR out of range


if __name__ == "__main__":
    unittest.main()
