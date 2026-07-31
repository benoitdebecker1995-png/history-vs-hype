"""
Calibration regression for the thumbnail FILTERS (ADR 0007).

Pins the necessary-condition behaviour so the hand-calibrated thresholds and the
curiosity-gap heuristic can't silently regress:

  - thumbnail_image_audit._legibility(): a near-uniform "blob" is below
    LEGIBILITY_MIN; a high-detail image is above the blob; the real clean
    Kurdistan renders clear LEGIBILITY_MIN (the actual recipe calibration).
  - thumbnail_checker curiosity-gap: an overlay that duplicates the title is
    flagged; a charged, non-duplicating overlay passes.
  - thumbnail_checker overlay floor: a concept with no text requires REVIEW,
    grounded in the n=650 niche corpus rather than the n=17 own-channel cohort.
  - render.headline(): the size-floor warning fires when an overlay can't fit at
    the legibility floor (too many words).

These assert NECESSARY CONDITIONS only — never a "this will get the click"
prediction. Clickability is decided live (ADR 0007), not by any of these.
"""
from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw

from tools.preflight import thumbnail_image_audit as tia
from tools.preflight.thumbnail_checker import check_thumbnail

_KURD = Path("video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/thumbnails")


# --------------------------------------------------------------------------- #
# 1. Feed-size legibility gate (the one image-computable click-killer)
# --------------------------------------------------------------------------- #
def _flat_blob() -> Image.Image:
    """Near-uniform mid-grey = a mushy low-detail blob (won't read at 160px)."""
    rng = np.random.default_rng(0)
    arr = np.full((720, 1280, 3), 128, dtype=np.int16)
    arr += rng.integers(-3, 4, arr.shape)  # faint noise that averages out at 160px
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGB")


def _high_detail() -> Image.Image:
    """Coarse high-contrast checkerboard = strong large-scale detail at 160px."""
    img = Image.new("RGB", (1280, 720), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cell = 128
    for y in range(0, 720, cell):
        for x in range(0, 1280, cell):
            if (x // cell + y // cell) % 2 == 0:
                d.rectangle([x, y, x + cell, y + cell], fill=(255, 255, 255))
    return img


def test_blob_is_below_legibility_min():
    assert tia._legibility(_flat_blob()) < tia.LEGIBILITY_MIN


def test_detail_beats_blob():
    assert tia._legibility(_high_detail()) > tia._legibility(_flat_blob())


@pytest.mark.parametrize(
    "name", ["comboB_v2_proof.png", "comboB_v2_kings.png", "comboB_v2_ruled.png"]
)
def test_real_clean_renders_clear_the_floor(name):
    """The recipe calibration: legible renders survive feed size (skip if absent)."""
    p = _KURD / name
    if not p.exists():
        pytest.skip(f"{name} not present in repo")
    assert tia._legibility(Image.open(p).convert("RGB")) >= tia.LEGIBILITY_MIN


# --------------------------------------------------------------------------- #
# 2. Curiosity-gap necessary condition (overlay must not duplicate the title)
# --------------------------------------------------------------------------- #
_TITLE = "They Minted Their Own Coins"


def test_overlay_duplicating_title_is_flagged():
    res = check_thumbnail('coin photo, bold text overlay "THEIR COINS"', title=_TITLE)
    assert any("DUPLICATES TITLE" in i for i in res["issues"])
    assert res["score"] == 75
    assert res["verdict"] == "REVIEW"


def test_non_duplicating_overlay_passes_gap():
    res = check_thumbnail('coin photo, bold text overlay "PROOF OF A STATE"', title=_TITLE)
    assert not any("DUPLICATES TITLE" in i for i in res["issues"])
    assert any("Curiosity gap OK" in p for p in res["passes"])
    assert res["score"] == 100
    assert res["verdict"] == "PASS"


# --------------------------------------------------------------------------- #
# 3. Niche structural norm: a text-free concept requires REVIEW (ADR 0019)
# --------------------------------------------------------------------------- #
def test_no_text_concept_does_not_pass_at_100():
    res = check_thumbnail(
        "a photo of me talking to camera, no text, cluttered background, stock photo"
    )

    assert any("NO TEXT OVERLAY" in item for item in res["issues"])
    assert res["score"] == 75
    assert res["verdict"] == "REVIEW"


# --------------------------------------------------------------------------- #
# 4. Own-channel unvalidated features are informational (ADR 0007 / ADR 0019)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("concept", "note"),
    [
        ('talking head presenter, bold text overlay "THE SECRET"', "TALKING HEAD"),
        ('stock photo, bold text overlay "THE SECRET"', "STOCK IMAGERY"),
        ('document only, bold text overlay "THE SECRET"', "DOCUMENT AS FOCAL POINT"),
        ('busy collage, bold text overlay "THE SECRET"', "BUSY COMPOSITION"),
    ],
)
def test_unvalidated_concept_features_are_notes_without_score_impact(concept, note):
    res = check_thumbnail(concept)

    assert any(note in item for item in res["issues"])
    assert res["score"] == 100
    assert res["verdict"] == "PASS"


# --------------------------------------------------------------------------- #
# 5. Render headline size-floor warning (too many words to read at feed size)
# --------------------------------------------------------------------------- #
def test_headline_warns_when_overlay_cannot_fit_floor():
    render = pytest.importorskip("tools.thumbnail.render")
    if not Path(render.IMPACT).exists():
        pytest.skip("Impact font not available on this runner")
    base = Image.new("RGB", (render.W, render.H), (20, 20, 20))
    # one very long unbreakable word in a narrow column => can't fit at the floor
    warns, _ = render.headline(base, [("SUPERCALIFRAGILISTICEXPIALIDOCIOUS", render.WHITE)],
                               (render.EDGE_MARGIN, 300), max_w=240)
    assert warns, "expected a size-floor warning for an overlay that can't fit"
