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


class TestValidationRanAtAll(unittest.TestCase):
    """`ok=True` used to mean either 'checked, clean' or 'checked nothing'.

    Those are different facts and the caller must be able to tell them apart —
    otherwise a total failure to load reference data reads as a clean pass, which
    is exactly how the double-count guard sat silently disabled.
    """

    def test_compared_counts_real_comparisons(self):
        r = {"a": {"impression_count": 900, "ctr_percent": 2.0},
             "b": {"impression_count": 500, "ctr_percent": 1.0}}
        life = {"a": {"impressions": 1000}, "b": {"impressions": 500}}
        res = validate_rolling_against_lifetime(r, life, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertEqual(res.compared, 2)
        self.assertTrue(res.lifetime_check_ran)

    def test_empty_lifetime_is_ok_but_did_not_run(self):
        r = {"a": {"impression_count": 500, "ctr_percent": 2.0}}
        res = validate_rolling_against_lifetime(r, {}, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertTrue(res.ok)                      # no invariant was breached
        self.assertEqual(res.compared, 0)
        self.assertFalse(res.lifetime_check_ran)     # ...but nothing was verified
        self.assertTrue(any("verified 0/" in w for w in res.warnings))

    def test_stale_studio_also_reports_zero_compared(self):
        r = {"a": {"impression_count": 99999, "ctr_percent": 2.0}}
        life = {"a": {"impressions": 1000}}
        res = validate_rolling_against_lifetime(r, life, studio_as_of=STALE, reporting_window_end=WIN_END)
        self.assertFalse(res.lifetime_check_ran)

    def test_no_spurious_warning_when_nothing_to_check(self):
        res = validate_rolling_against_lifetime({}, {}, studio_as_of=FRESH, reporting_window_end=WIN_END)
        self.assertTrue(res.ok)
        self.assertEqual(res.warnings, [])


class TestRollingVsDaily(unittest.TestCase):
    """The always-on guard.

    The lifetime check depends on a hand-made Studio export, so in practice it
    almost never ran. This one compares two numbers the collector produces itself
    in the same pass — the rolling aggregate and the per-day rows — which must be
    equal over the same window. A duplicated report inflates the first and not the
    second, so this catches the original bug class on every run, with no manual
    input at all.
    """

    def _conn(self, rows):
        import sqlite3
        c = sqlite3.connect(":memory:")
        c.execute(
            "CREATE TABLE impressions_daily (video_id TEXT, metric_date DATE, "
            "traffic_source TEXT DEFAULT 'ALL', impressions INTEGER, clicks INTEGER, "
            "ctr_percent REAL, report_create_time TEXT, ingested_at TEXT, "
            "PRIMARY KEY (video_id, metric_date, traffic_source))"
        )
        c.executemany(
            "INSERT INTO impressions_daily VALUES (?,?,'ALL',?,0,0,'t','t')", rows
        )
        c.commit()
        return c

    WS, WE = date(2026, 6, 26), date(2026, 7, 26)

    def test_agreement_passes(self):
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60), ("A", "2026-07-02", 40)])
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 100}}, c, window_start=self.WS, window_end=self.WE)
        self.assertTrue(res.ok)
        self.assertEqual(res.compared, 1)
        c.close()

    def test_double_counted_rolling_fails(self):
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60), ("A", "2026-07-02", 40)])
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 200}}, c, window_start=self.WS, window_end=self.WE)
        self.assertFalse(res.ok)
        self.assertIn("double-counted", res.failures[0])
        c.close()

    def test_rolling_below_daily_is_a_warning_not_a_failure(self):
        """The benign direction. Regression guard for the 2026-07-28..08-27 outage.

        A rolling figure BELOW the stored daily sum means the store holds days this
        fetch did not return — late-arriving or revised reach rows. Nothing is
        double-counted. Failing on it aborted every snapshot for a month while all
        14 real-world mismatches were in this direction and none was a double-count.
        """
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60), ("A", "2026-07-02", 40)])
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 89}}, c, window_start=self.WS, window_end=self.WE)
        self.assertTrue(res.ok, "rolling < daily-sum must not abort the snapshot")
        self.assertFalse(res.failures)
        self.assertTrue(any("superset" in w for w in res.warnings))
        self.assertEqual(res.compared, 1)
        c.close()

    def test_days_outside_the_window_are_not_counted(self):
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60), ("A", "2026-05-01", 999)])
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 60}}, c, window_start=self.WS, window_end=self.WE)
        self.assertTrue(res.ok)
        c.close()

    def test_video_with_no_daily_rows_is_unverified_not_failed(self):
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60)])
        res = validate_rolling_against_daily(
            {"B": {"impression_count": 5}}, c, window_start=self.WS, window_end=self.WE)
        self.assertTrue(res.ok)
        self.assertIn("B", res.unverified)
        c.close()

    def test_missing_bounds_skip_cleanly(self):
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = self._conn([("A", "2026-07-01", 60)])
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 60}}, c, window_start=None, window_end=None)
        self.assertTrue(res.ok)
        self.assertEqual(res.compared, 0)
        c.close()

    def test_missing_table_does_not_crash_the_run(self):
        import sqlite3
        from tools.youtube_analytics.ctr_tracker import validate_rolling_against_daily
        c = sqlite3.connect(":memory:")
        res = validate_rolling_against_daily(
            {"A": {"impression_count": 60}}, c, window_start=self.WS, window_end=self.WE)
        self.assertTrue(res.ok)
        self.assertTrue(res.warnings)
        c.close()


if __name__ == "__main__":
    unittest.main()
