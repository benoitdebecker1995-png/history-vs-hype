"""
CTA Placement Checker — is the subscribe ask where anyone can hear it?

Measured 2026-07-29 on `analytics.db` (58 videos, `retention_curves`):

    elapsed   2%    10%    20%    30%    50%    80%    99%
    watching  82.6% 45.3%  37.3%  31.2%  25.5%  22.4%  16.5%

Half the audience is gone by the 10% mark, and from 30% onward the curve is
almost flat — only 8.8 points are lost between 30% and 80%. Across the 14
published scripts the subscribe ask sat at **57-94% of the script body**
(median ~80%), and three scripts had no ask at all.

So the median CTA was heard by ~22% of viewers. Moving it to ~30% raises that
to ~31% (+39% relative reach) and to ~37% at the 20% mark, at no retention cost
worth the name — the audience present at 30% is essentially the audience that
will ever exist for that video.

Placement also wants to land just AFTER the turn (the style guide puts the turn
at 15-25% runtime), because approval is the only measured correlate of
subscribing: subs/1k vs likes/1k r=+0.50, vs retention r=+0.29, vs comments
r=0.00. Ask at the moment the viewer has just been given something.

⚠ SCOPE — two rules, deliberately unequal in force:

  * `cta_missing`  — BINDING (severity high). Grounded: three published scripts
    shipped with no spoken ask, and 98.4% of views come from non-subscribers.
    A video that never asks cannot convert. Nothing contests this.

  * `cta_too_late` — INFORMATIONAL ONLY (severity info), and it must stay that
    way until an A/B settles it. `channel-data/calibration/OPENER-RETENTION-DIAGNOSIS.md`
    (2026-06-26) recommends the OPPOSITE — CTA in the final 5% — because a
    mid-video CTA "reads as 'the new info is over'" and one video (Kashmir) lost
    ~9% of remaining viewers at its CTA. That is n=1 and was never holdout-tested,
    which breaks that document's own stated rule; but the +39%-reach figure here
    is arithmetic on a retention curve, not a measured subscriber effect. Two
    unvalidated claims in opposition. Per ADR-0007/ADR-0012 an unvalidated rule
    does not bind.

This is a necessary-condition FILTER, never a predictor of how many subscribers a
script will earn.
"""

import re
from typing import Any, Dict, List

from tools.script_checkers.checkers import BaseChecker

# Position in the script body past which an ask reaches a materially smaller
# audience. 0.35 sits just after the flat part of the curve begins (~30%) with
# a little slack for scripts whose turn runs long.
DEFAULT_MAX_POSITION = 0.35

# Where we'd rather it landed — right after the turn.
IDEAL_WINDOW = (0.15, 0.30)

_CTA_RE = re.compile(r"\bsubscrib\w*", re.IGNORECASE)

# Production scaffolding that isn't spoken. A CTA that exists only inside an
# "## END SCREEN / CTA" heading or a [VISUAL: ...] block is not an ask the
# viewer hears, so those regions are stripped before measuring.
_NONSPOKEN_PATTERNS = [
    r"^\s{0,3}#{1,6}[^\n]*$",           # markdown headings
    r"\[[^\]]*\]",                       # [VISUAL: ...], [ON SCREEN: ...]
    r"\*\*\[[^\]]*\]\*\*",
    r"^\s*>\s?",                         # blockquote markers
]


def _strip_nonspoken(text: str) -> str:
    """Blank out non-spoken regions, preserving offsets so positions stay true."""
    out = text
    for pat in _NONSPOKEN_PATTERNS:
        out = re.sub(pat, lambda m: " " * len(m.group(0)), out, flags=re.MULTILINE)
    return out


class CTAPlacementChecker(BaseChecker):
    """Flags a missing subscribe ask, or one placed too late to be heard."""

    @property
    def name(self) -> str:
        return "cta"

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze subscribe-CTA presence and position.

        Args:
            text: Script text to analyze.

        Returns:
            {'issues': [...], 'stats': {...}} — never raises.
        """
        issues: List[Dict[str, Any]] = []

        max_position = getattr(self.config, "cta_max_position", DEFAULT_MAX_POSITION)
        spoken = _strip_nonspoken(text or "")
        body_len = len(spoken.strip())

        if body_len == 0:
            return {
                "issues": [],
                "stats": {"cta_count": 0, "first_cta_position": None, "empty": True},
            }

        matches = list(_CTA_RE.finditer(spoken))

        if not matches:
            issues.append({
                "type": "cta_missing",
                "severity": "high",
                "message": (
                    "NO SUBSCRIBE ASK in the spoken script. Three published scripts shipped "
                    "without one. 98.4% of this channel's views come from non-subscribers — "
                    "if the script never asks, the video cannot convert."
                ),
                "suggestion": (
                    f"Add one ask just after the turn, at {IDEAL_WINDOW[0]:.0%}-"
                    f"{IDEAL_WINDOW[1]:.0%} of the script."
                ),
            })
            return {
                "issues": issues,
                "stats": {"cta_count": 0, "first_cta_position": None},
            }

        first = matches[0].start() / len(spoken)

        if first > max_position:
            # Reach estimates from the measured median retention curve.
            reach_here = 22.4 if first >= 0.70 else 25.5 if first >= 0.45 else 31.2
            issues.append({
                "type": "cta_too_late",
                "severity": "info",  # ⚠ INFORMATIONAL — see CONTESTED note below. Must not bind.
                "message": (
                    f"CTA AT {first:.0%} (INFORMATIONAL — no verdict impact) — roughly "
                    f"{reach_here:.0f}% of viewers are still watching by then, so ~"
                    f"{100 - reach_here:.0f}% never hear it."
                ),
                "suggestion": (
                    f"CONTESTED, do not treat as a rule. Reach argument: 31.2% still watching at "
                    f"30% elapsed vs 22.4% at 80% (+39% reach), curve flat between. Against it: "
                    "OPENER-RETENTION-DIAGNOSIS.md (2026-06-26) recommends the final 5%, on the "
                    "grounds that a mid-video CTA reads as 'the new info is over' and cost Kashmir "
                    "~9% of remaining viewers. That is n=1 and was never holdout-tested; the reach "
                    "figure is arithmetic, not a measured subscriber effect. Neither side is "
                    "validated — settle it by A/B, not by this checker."
                ),
                "position": round(first, 3),
            })

        return {
            "issues": issues,
            "stats": {
                "cta_count": len(matches),
                "first_cta_position": round(first, 3),
                "in_ideal_window": IDEAL_WINDOW[0] <= first <= IDEAL_WINDOW[1],
                "max_position": max_position,
            },
        }
