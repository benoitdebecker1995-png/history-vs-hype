"""
Regression for the reach-report double-count (found by Codex 2026-07-22).

YouTube regenerates reach reports for the same day, so the reports list can hold
multiple objects per (startTime, endTime) interval. The aggregation loop SUMS
impressions across whatever it is handed, so duplicates inflate the total — #59's
30-day rolling impressions came out at 20,919 vs a lifetime Studio total of
10,925, which is impossible. `_dedup_reports_by_interval` collapses to one report
(newest createTime) per interval before windowing.
"""

import unittest

from tools.youtube_analytics.ctr_tracker import _dedup_reports_by_interval


class TestDedupReportsByInterval(unittest.TestCase):
    def test_collapses_duplicate_intervals_keeping_newest_createtime(self):
        reports = [
            {"startTime": "2026-07-23", "endTime": "2026-07-24", "createTime": "2026-07-24T01:00", "id": "a"},
            {"startTime": "2026-07-23", "endTime": "2026-07-24", "createTime": "2026-07-24T09:00", "id": "b"},
            {"startTime": "2026-07-23", "endTime": "2026-07-24", "createTime": "2026-07-24T05:00", "id": "c"},
            {"startTime": "2026-07-22", "endTime": "2026-07-23", "createTime": "2026-07-23T09:00", "id": "d"},
        ]
        out = _dedup_reports_by_interval(reports)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0]["id"], "b")   # newest createTime for the 07-23 interval
        self.assertEqual(out[1]["id"], "d")

    def test_newest_date_first(self):
        reports = [
            {"startTime": "2026-07-01", "endTime": "2026-07-02", "createTime": "x"},
            {"startTime": "2026-07-20", "endTime": "2026-07-21", "createTime": "x"},
        ]
        out = _dedup_reports_by_interval(reports)
        self.assertEqual(out[0]["endTime"], "2026-07-21")

    def test_no_duplicates_is_identity_count(self):
        reports = [
            {"startTime": f"2026-07-{d:02d}", "endTime": f"2026-07-{d+1:02d}", "createTime": "x"}
            for d in range(1, 11)
        ]
        self.assertEqual(len(_dedup_reports_by_interval(reports)), 10)

    def test_thirty_objects_but_eighteen_unique_dates(self):
        # The real failure shape: 30 report objects, only 18 unique intervals.
        reports = []
        for d in range(1, 19):  # 18 unique dates
            reports.append({"startTime": f"d{d}", "endTime": f"e{d}", "createTime": "1"})
        for d in range(1, 13):  # 12 regenerated duplicates of the first 12
            reports.append({"startTime": f"d{d}", "endTime": f"e{d}", "createTime": "2"})
        self.assertEqual(len(reports), 30)
        out = _dedup_reports_by_interval(reports)
        self.assertEqual(len(out), 18)
        # regenerated (createTime "2") won for the duplicated intervals
        won = {(r["startTime"], r["createTime"]) for r in out}
        self.assertIn(("d1", "2"), won)

    def test_empty(self):
        self.assertEqual(_dedup_reports_by_interval([]), [])


if __name__ == "__main__":
    unittest.main()
