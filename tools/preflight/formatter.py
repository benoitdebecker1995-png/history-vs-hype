"""
Pre-Flight Formatter — renders a scorecard dict as a markdown report.
"""

from typing import Dict, Any


def _bar(score: int, width: int = 20) -> str:
    """Render a simple text progress bar."""
    filled = round(score / 100 * width)
    return f"[{'=' * filled}{' ' * (width - filled)}] {score}/100"


def _gate_icon(score: int) -> str:
    if score >= 70:
        return 'PASS'
    if score >= 50:
        return 'WARN'
    return 'FAIL'


def format_preflight_report(result: Dict[str, Any]) -> str:
    """
    Render a pre-flight scorecard as a markdown report.

    Args:
        result: Output from run_preflight()

    Returns:
        Formatted markdown string
    """
    if 'error' in result:
        return f"**Pre-Flight Error:** {result['error']}"

    composite = result.get('composite_score', 0)
    grade = result.get('grade', '?')
    verdict = result.get('verdict', '?')
    gates = result.get('gates', {})
    flags = result.get('flags', [])
    pred = result.get('predicted_range', {})
    ch_avg = result.get('channel_avg', {})

    lines = []
    lines.append(f"# PRE-FLIGHT SCORECARD")
    lines.append('')
    lines.append(f"**Composite:** {composite}/100 ({grade})  ")
    lines.append(f"**Verdict:** {verdict}  ")
    lines.append(f"**Bar:** {_bar(composite)}")
    lines.append('')

    # --- Gate breakdown ---
    lines.append('---')
    lines.append('')
    lines.append('## Gate Breakdown')
    lines.append('')

    # Topic
    t = gates.get('topic', {})
    lines.append(f"### 1. Topic — {t.get('score', 0)}/100 [{_gate_icon(t.get('score', 0))}]")
    lines.append(f"- Type: **{t.get('topic_type', '?')}**")
    for n in t.get('notes', []):
        lines.append(f"- {n}")
    lines.append('')

    # Script
    s = gates.get('script', {})
    lines.append(f"### 2. Script — {s.get('score', 0)}/100 [{_gate_icon(s.get('score', 0))}]")
    lines.append(f"- Pacing: **{s.get('pacing_verdict', 'SKIPPED')}**")
    lines.append(f"- Evidence density: **{s.get('evidence_density', 0)}** markers/100 words")
    for iss in s.get('issues', []):
        lines.append(f"- {iss}")
    for n in s.get('notes', []):
        lines.append(f"- _{n}_")
    lines.append('')

    # Title
    ti = gates.get('title', {})
    lines.append(f"### 3. Title/Metadata — {ti.get('score', 0)}/100 [{_gate_icon(ti.get('score', 0))}]")
    if ti.get('best_title'):
        lines.append(f"- Best title: **{ti['best_title']}**")
    if ti.get('predicted_ctr'):
        lines.append(f"- Predicted CTR: **{ti['predicted_ctr']}**")
    if ti.get('formulas'):
        lines.append(f"- Formulas: {', '.join(ti['formulas'])}")
    for iss in ti.get('issues', []):
        lines.append(f"- {iss}")
    for n in ti.get('notes', []):
        lines.append(f"- _{n}_")
    lines.append('')

    # Duration
    d = gates.get('duration', {})
    lines.append(f"### 4. Duration/Format — {d.get('score', 0)}/100 [{_gate_icon(d.get('score', 0))}]")
    lines.append(f"- Estimated: **{d.get('estimated_minutes', 0)} min** ({d.get('word_count', 0)} words)")
    lines.append(f"- B-roll ratio: **{d.get('broll_ratio', 0):.0%}**")
    for iss in d.get('issues', []):
        lines.append(f"- {iss}")
    lines.append('')

    # --- Flags ---
    if flags:
        lines.append('---')
        lines.append('')
        lines.append('## Action Items')
        lines.append('')
        for f in flags:
            lines.append(f"- [ ] {f}")
        lines.append('')

    # --- Predicted range ---
    if pred:
        lines.append('---')
        lines.append('')
        lines.append('## Predicted View Range')
        lines.append('')
        lines.append(f"**{pred.get('views_low', '?')} – {pred.get('views_high', '?')} views**")
        lines.append(f"Based on: {pred.get('based_on', '?')}")
        if ch_avg.get('avg_views'):
            lines.append(f"Channel average: {ch_avg['avg_views']} views (n={ch_avg.get('sample_size', '?')})")
        lines.append('')
        lines.append('_Note: predictions are rough estimates based on limited channel data._')

    return '\n'.join(lines)
