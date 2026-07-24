"""Tests for the packaging lock — the ADR-0012 code-enforced hard gate.

The gate exists because prose rules didn't bind; until now nothing verified
the gate itself binds. Covers the pure verdict logic, the four filters run
offline against a tmp project, title resolution, and validate_lock including
its anti-tamper recompute (a hand-edited PASS on a bad title must not fool it).

Fixture titles (probed against the real recognizers, 2026-07-01):
  ANCHORED   — "France" hits HEAD_TERMS, clickbait-clean
  ANCHORLESS — no famous head term in the first 40 chars
  CLICKBAIT  — anchored but trips the SHOCKING brand-gate pattern
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.preflight.packaging_lock import (  # noqa: E402
    _verdict,
    render_lock_block,
    resolve_title,
    run_filters,
    validate_lock,
    write_lock_block,
)
from tools.video_projects import PACKAGING_LOCK_ZONE, RECONCILE_ZONE, StatusDoc  # noqa: E402

ANCHORED = "France Lost the Treaty That Drew Its Borders"
ANCHORLESS = "An Obscure Cartographer Made a Strange Map"
CLICKBAIT = "France Hid a SHOCKING Map Secret"


# ---------------------------------------------------------------------------
# _verdict — pure decision logic
# ---------------------------------------------------------------------------

def _filters(**overrides):
    base = {
        'search_anchor': {'status': 'PASS', 'detail': ''},
        'clickbait_gate': {'status': 'PASS', 'detail': ''},
        'title_thumb_gap': {'status': 'PASS', 'detail': ''},
        'thumbnail': {'status': 'PASS', 'detail': ''},
    }
    base.update(overrides)
    return base


def _enrichment(ts_nudge=False, cur_nudge=False):
    return {
        'title_scorer': {'value': '70/100', 'nudge': ts_nudge},
        'curiosity': {'value': 'not run', 'nudge': cur_nudge},
        'vidiq': {'value': 'not queried', 'nudge': False},
        'nlm': {'value': 'not queried', 'nudge': False},
    }


def test_verdict_all_pass_is_valid():
    verdict, reasons = _verdict(_filters(), _enrichment())
    assert verdict == 'LOCK VALID'
    assert reasons == []


@pytest.mark.parametrize('key', ['search_anchor', 'clickbait_gate'])
def test_verdict_mechanical_filter_fail_blocks(key):
    verdict, reasons = _verdict(_filters(**{key: {'status': 'FAIL', 'detail': 'x'}}), _enrichment())
    assert verdict == 'BLOCKED'
    assert any(key in r for r in reasons)


def test_verdict_thumbnail_fail_blocks_but_pending_does_not():
    verdict, _ = _verdict(_filters(thumbnail={'status': 'FAIL', 'detail': 'x'}), _enrichment())
    assert verdict == 'BLOCKED'
    verdict, reasons = _verdict(_filters(thumbnail={'status': 'PENDING', 'detail': 'x'}), _enrichment())
    assert verdict == 'LOCK VALID'
    assert reasons == []


def test_verdict_unfilled_judgment_blocks():
    verdict, reasons = _verdict(
        _filters(title_thumb_gap={'status': 'UNFILLED', 'detail': 'x'}), _enrichment())
    assert verdict == 'BLOCKED'
    assert any('judgment' in r for r in reasons)


def test_verdict_enrichment_nudges_review_never_block():
    verdict, reasons = _verdict(_filters(), _enrichment(ts_nudge=True))
    assert verdict == 'REVIEW'
    assert any('nudge, not a block' in r for r in reasons)
    # A nudge can never upgrade/override a FAIL either way round:
    verdict, _ = _verdict(
        _filters(search_anchor={'status': 'FAIL', 'detail': 'x'}), _enrichment(ts_nudge=True))
    assert verdict == 'BLOCKED'


def test_verdict_thumbnail_review_is_nonblocking_nudge():
    verdict, reasons = _verdict(_filters(thumbnail={'status': 'REVIEW', 'detail': 'x'}), _enrichment())
    assert verdict == 'REVIEW'
    assert any('thumbnail REVIEW' in r for r in reasons)


# ---------------------------------------------------------------------------
# run_filters — the four filters against a tmp project (offline)
# ---------------------------------------------------------------------------

def test_run_filters_good_title_advances(tmp_path):
    result = run_filters(ANCHORED, str(tmp_path), gap_note='overlay shows the map, title names the loss')
    f = result['filters']
    assert f['search_anchor']['status'] == 'PASS'
    assert 'France' in f['search_anchor']['detail']
    assert f['clickbait_gate']['status'] == 'PASS'
    assert f['title_thumb_gap']['status'] == 'PASS'
    assert f['thumbnail']['status'] == 'PENDING'  # empty project dir, no concept yet
    assert result['verdict'] != 'BLOCKED'


def test_run_filters_anchorless_title_blocks(tmp_path):
    result = run_filters(ANCHORLESS, str(tmp_path), gap_note='filled')
    assert result['filters']['search_anchor']['status'] == 'FAIL'
    assert result['verdict'] == 'BLOCKED'


def test_run_filters_clickbait_title_blocks(tmp_path):
    result = run_filters(CLICKBAIT, str(tmp_path), gap_note='filled')
    assert result['filters']['clickbait_gate']['status'] == 'FAIL'
    assert 'SHOCKING' in result['filters']['clickbait_gate']['detail']
    assert result['verdict'] == 'BLOCKED'


def test_run_filters_blank_judgment_blocks(tmp_path):
    result = run_filters(ANCHORED, str(tmp_path))
    assert result['filters']['title_thumb_gap']['status'] == 'UNFILLED'
    assert result['verdict'] == 'BLOCKED'


# ---------------------------------------------------------------------------
# resolve_title
# ---------------------------------------------------------------------------

def test_resolve_title_explicit_wins_and_unquotes(tmp_path):
    assert resolve_title(str(tmp_path), explicit='"Quoted Title"') == 'Quoted Title'


def test_resolve_title_prefers_lock_zone_over_working_title(tmp_path):
    doc = StatusDoc.load(tmp_path / 'PROJECT-STATUS.md')
    doc.text = 'Working title: "Fallback Title"\n'
    doc.write_zone(PACKAGING_LOCK_ZONE, 'title: "Locked Title"')
    doc.save()
    assert resolve_title(str(tmp_path)) == 'Locked Title'


def test_resolve_title_falls_back_to_working_title_line(tmp_path):
    (tmp_path / 'PROJECT-STATUS.md').write_text(
        'Working title: "Fallback Title"\n', encoding='utf-8')
    assert resolve_title(str(tmp_path)) == 'Fallback Title'


def test_resolve_title_none_when_nothing(tmp_path):
    assert resolve_title(str(tmp_path)) is None


# ---------------------------------------------------------------------------
# validate_lock — the hard gate downstream commands call
# ---------------------------------------------------------------------------

def _write_real_lock(tmp_path, title, gap='overlay differs from the title'):
    result = run_filters(title, str(tmp_path), gap_note=gap)
    write_lock_block(str(tmp_path), render_lock_block(title, result, today='2026-07-01'))
    return result


def test_validate_no_block_is_invalid(tmp_path):
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('no packaging-lock block' in r for r in reasons)


def test_validate_real_lock_round_trips(tmp_path):
    _write_real_lock(tmp_path, ANCHORED)
    valid, reasons = validate_lock(str(tmp_path))
    assert valid, reasons


def test_validate_recomputes_anchor_anti_tamper(tmp_path):
    """A hand-edited block claiming PASS on an anchorless title must not fool the gate."""
    body = '\n'.join([
        '## Packaging Lock (2026-07-01)',
        f'title: "{ANCHORLESS}"',
        'FILTERS (pass/fail):',
        '  search-anchor:        PASS  (hand-edited lie)',
        '  clickbait brand-gate: PASS  (x)',
        '  title<->thumb gap:    PASS  (x)',
        '  thumbnail conditions: PENDING  (x)',
        'VERDICT: LOCK VALID',
    ])
    write_lock_block(str(tmp_path), body)
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('search-anchor FAILS' in r for r in reasons)


def test_validate_recomputes_clickbait_anti_tamper(tmp_path):
    body = '\n'.join([
        f'title: "{CLICKBAIT}"',
        '  search-anchor:        PASS  (x)',
        '  clickbait brand-gate: PASS  (hand-edited lie)',
        '  title<->thumb gap:    PASS  (x)',
        '  thumbnail conditions: PENDING  (x)',
    ])
    write_lock_block(str(tmp_path), body)
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('clickbait brand-gate FAILS' in r for r in reasons)


def test_validate_unfilled_judgment_is_invalid(tmp_path):
    body = '\n'.join([
        f'title: "{ANCHORED}"',
        '  search-anchor:        PASS  (x)',
        '  clickbait brand-gate: PASS  (x)',
        '  title<->thumb gap:    UNFILLED  (blank)',
        '  thumbnail conditions: PENDING  (x)',
    ])
    write_lock_block(str(tmp_path), body)
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('BLANK' in r for r in reasons)


def test_validate_recorded_thumbnail_fail_is_invalid(tmp_path):
    body = '\n'.join([
        f'title: "{ANCHORED}"',
        '  search-anchor:        PASS  (x)',
        '  clickbait brand-gate: PASS  (x)',
        '  title<->thumb gap:    PASS  (x)',
        '  thumbnail conditions: FAIL  (unreadable at feed size)',
    ])
    write_lock_block(str(tmp_path), body)
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('thumbnail conditions FAIL' in r for r in reasons)


def test_validate_missing_title_line_is_invalid(tmp_path):
    write_lock_block(str(tmp_path), 'VERDICT: LOCK VALID')
    valid, reasons = validate_lock(str(tmp_path))
    assert not valid
    assert any('no title line' in r for r in reasons)


def test_lock_zone_coexists_with_reconcile_zone(tmp_path):
    """The gate writes below the reconcile zone and neither clobbers the other."""
    doc = StatusDoc.load(tmp_path / 'PROJECT-STATUS.md')
    doc.write_zone(RECONCILE_ZONE, 'Status: SCRIPTING')
    doc.save()
    _write_real_lock(tmp_path, ANCHORED)
    final = StatusDoc.load(tmp_path / 'PROJECT-STATUS.md')
    assert final.zone_fields(RECONCILE_ZONE) == {'Status': 'SCRIPTING'}
    assert final.zone(PACKAGING_LOCK_ZONE) is not None
    valid, reasons = validate_lock(str(tmp_path))
    assert valid, reasons
