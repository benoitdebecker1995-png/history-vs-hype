"""Pins for the thumbnail accent colour plumbing (tools/thumbnail/render.py).

Origin: 2026-08-04. `dossier_document` accepted an `accent` argument and never read it — the focal
bar and seal were hard-coded red while the CLI coloured the headline with the chosen accent. A
default render therefore shipped TWO accent colours (yellow headline, red bar, red seal), against
the module's own Tier-1 rule of ONE accent colour, and `--accent` was a no-op for the two templates
that declare it.

The colour claim behind the hard-coding was also retired by the channel's own data:
`CTR-THUMBNAIL-FINDINGS-2026-06.md` concludes red is "neither a winner rule nor a poison rule".

No fonts and no disk writes: the drawing primitives are exercised directly and the templates are
checked through a captured call.
"""

import pytest

from PIL import Image

from tools.thumbnail import render


class TestAccentPrimitives:
    def test_bar_defaults_to_red(self):
        img = Image.new("RGB", (40, 40), (0, 0, 0))
        render.accent_bar(img, (0, 0), w=20, h=10)
        assert img.getpixel((5, 5)) == render.RED

    def test_bar_honours_an_explicit_colour(self):
        img = Image.new("RGB", (40, 40), (0, 0, 0))
        render.accent_bar(img, (0, 0), w=20, h=10, color=render.YELLOW)
        assert img.getpixel((5, 5)) == render.YELLOW

    def test_seal_honours_an_explicit_colour(self):
        img = Image.new("RGB", (120, 120), (0, 0, 0))
        render.accent_seal(img, (60, 60), r=40, color=render.YELLOW)
        # centre of the disc carries the accent, not red
        assert img.getpixel((60, 60))[:3] != render.RED
        assert img.getpixel((60, 60))[0] > 200  # yellow is bright in R

    def test_seal_outline_is_a_darker_shade_of_the_accent(self):
        assert render._darken((200, 100, 50)) == (110, 55, 27)
        assert all(c == 0 for c in render._darken((0, 0, 0)))


class TestTemplatePlumbing:
    """`--accent` must actually reach the focal elements."""

    @pytest.fixture
    def captured(self, monkeypatch):
        seen = {}
        monkeypatch.setattr(
            render, "accent_bar",
            lambda img, xy, w, h=14, color=render.RED: seen.update(bar=color),
        )
        monkeypatch.setattr(
            render, "accent_seal",
            lambda img, center, r=46, color=render.RED: seen.update(seal=color),
        )
        monkeypatch.setattr(render, "headline", lambda *a, **k: ([], (0, 0, 10, 10)))
        monkeypatch.setattr(render, "save", lambda img, out: out)
        monkeypatch.setattr(render, "load_rgb", lambda path: Image.new("RGB", (600, 600), (9, 9, 9)))
        return seen

    @pytest.mark.parametrize("accent", ["yellow", "red", "white"])
    def test_dossier_passes_the_named_accent_to_bar_and_seal(self, captured, accent):
        render.dossier_document("asset.png", [], "out.png", accent=accent)
        assert captured["bar"] == render.ACCENTS[accent]
        assert captured["seal"] == render.ACCENTS[accent]

    def test_bar_and_seal_share_one_colour(self, captured):
        """The whole point of the Tier-1 rule: one accent, not two."""
        render.dossier_document("asset.png", [], "out.png", accent="yellow")
        assert captured["bar"] == captured["seal"]

    def test_mechanism_reframe_forwards_its_accent(self, captured):
        render.mechanism_reframe("asset.png", [], "out.png", accent="white")
        assert captured["bar"] == render.ACCENTS["white"]
        assert "seal" not in captured, "mechanism_reframe renders without the seal"

    def test_an_rgb_tuple_is_accepted_as_well_as_a_name(self, captured):
        render.dossier_document("asset.png", [], "out.png", accent=(1, 2, 3))
        assert captured["bar"] == (1, 2, 3)


class TestNoChannelRedLaw:
    def test_module_docstring_does_not_claim_red_is_the_look_here_signal(self):
        """The own-channel data retired that claim; the renderer must not re-assert it."""
        doc = render.__doc__ or ""
        assert "look-here" not in doc.lower() or "not necessarily red" in doc.lower()

    def test_red_is_still_available_as_a_choice(self):
        assert "red" in render.ACCENTS
