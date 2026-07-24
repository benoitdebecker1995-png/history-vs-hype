"""AnalysisSource — the data-fetch seam for run_analysis.

`run_analysis` (analyze.py) used to call eight data-fetching functions directly:
four YouTube-API calls plus two database reads, each gated by optional imports
and wrapped in partial-failure handling. That made the whole analysis impossible
to test without live API access — so a silent wrong number or a dropped data
source in a post-publish report had no safety net.

This module collects every external fetch behind one small interface with two
implementations:

  - `LiveAnalysisSource` — the real thing (YouTube API + keywords.db), the
    default in production. Behavior is identical to the old inline calls.
  - `InMemoryAnalysisSource` — fed known data (or made to raise) in tests, so
    `run_analysis` and every one of its partial-failure branches can be checked
    against expected output without touching the network.

The synthesis on top (generate_lessons, diagnose_discovery) stays in analyze.py
and is unchanged — only the fetching moved behind this seam. See ADR-0011.
"""
from __future__ import annotations

from typing import Optional, Protocol


class AnalysisSource(Protocol):
    """The six external fetches run_analysis depends on.

    Methods may raise on failure (the YouTube/DB calls do); run_analysis owns the
    try/except and error collection. `variant_data` and `ctr_analysis` return
    None when their optional subsystem is unavailable or has no data.
    """

    def video_report(self, video_id: str) -> dict: ...
    def comments(self, video_id: str) -> dict: ...
    def channel_averages(self) -> dict: ...
    def video_metrics(self, video_id: str) -> dict: ...
    def variant_data(self, video_id: str) -> Optional[dict]: ...
    def ctr_analysis(self, video_id: str) -> Optional[dict]: ...


class LiveAnalysisSource:
    """Production source — real YouTube API + keywords.db.

    Imports are kept lazy so the optional subsystems (variant tracking, CTR
    benchmarks) degrade to None exactly as the old `_AVAILABLE` import gating did.
    """

    def video_report(self, video_id: str) -> dict:
        from .video_report import generate_video_report
        return generate_video_report(video_id)

    def comments(self, video_id: str) -> dict:
        from .comments import fetch_and_categorize_comments
        return fetch_and_categorize_comments(video_id)

    def channel_averages(self) -> dict:
        from .channel_averages import get_channel_averages
        return get_channel_averages()

    def video_metrics(self, video_id: str) -> dict:
        from .metrics import get_video_metrics
        return get_video_metrics(video_id)

    def variant_data(self, video_id: str) -> Optional[dict]:
        try:
            from tools.discovery.performance_tracker import PerformanceTracker
        except ImportError:
            return None
        db = PerformanceTracker.connect()
        try:
            summary = db.get_variant_summary(video_id)
            if summary['thumbnails'] > 0 or summary['titles'] > 0 or summary['snapshots'] > 0:
                return {
                    'summary': summary,
                    'thumbnails': db.get_thumbnail_variants(video_id),
                    'titles': db.get_title_variants(video_id),
                    'snapshots': db.get_ctr_snapshots(video_id),
                }
            return None
        finally:
            db.close()

    def ctr_analysis(self, video_id: str) -> Optional[dict]:
        try:
            from .benchmarks import compare_variants_for_video, get_benchmarks_report
        except ImportError:
            return None
        benchmarks_data = get_benchmarks_report()
        overall = benchmarks_data.get('overall', {})
        return {
            'thumbnail_verdict': compare_variants_for_video(video_id, 'thumbnail', overall),
            'title_verdict': compare_variants_for_video(video_id, 'title', overall),
            'benchmarks': benchmarks_data,
        }


# Default fetch results for InMemoryAnalysisSource — minimal valid shapes so a
# bare fake doesn't crash run_analysis; tests override what they care about.
_DEFAULTS = {
    'video_report': lambda: {
        'title': None, 'engagement': None, 'retention': None,
        'ctr': None, 'errors': [],
    },
    'comments': lambda: {'total_fetched': 0, 'categories': {}},
    'channel_averages': lambda: {},
    'video_metrics': lambda: {},
    'variant_data': lambda: None,
    'ctr_analysis': lambda: None,
}


class InMemoryAnalysisSource:
    """Test double — returns canned data, or raises a configured exception.

    Pass any of the six results as keyword args; omitted ones use a minimal
    valid default. Pass `raises={'comments': RuntimeError('boom')}` to drive a
    fetch failure and exercise run_analysis's error-collection branch.
    """

    def __init__(self, *, raises: Optional[dict] = None, **results):
        unknown = set(results) - set(_DEFAULTS)
        if unknown:
            raise TypeError(f"unknown source result(s): {sorted(unknown)}")
        self._results = results
        self._raises = raises or {}

    def _get(self, name: str):
        if name in self._raises:
            raise self._raises[name]
        if name in self._results:
            return self._results[name]
        return _DEFAULTS[name]()

    def video_report(self, video_id: str) -> dict:
        return self._get('video_report')

    def comments(self, video_id: str) -> dict:
        return self._get('comments')

    def channel_averages(self) -> dict:
        return self._get('channel_averages')

    def video_metrics(self, video_id: str) -> dict:
        return self._get('video_metrics')

    def variant_data(self, video_id: str) -> Optional[dict]:
        return self._get('variant_data')

    def ctr_analysis(self, video_id: str) -> Optional[dict]:
        return self._get('ctr_analysis')
