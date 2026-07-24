"""Tests for tools.subtitles — the canonical SRT parser seam.

The 5 parsers it replaces had no shared tests. Covers the union behaviors that
differed between them: indexed vs unindexed cues, tag stripping, encoding
fallback, variable fractional-second digits, the projections, and the opt-in
+1h-offset correction.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import subtitles  # noqa: E402

STD = """1
00:00:01,000 --> 00:00:04,000
<i>Hello</i> world.

2
00:00:04,500 --> 00:00:07,000
A second cue
spanning two lines

3
00:00:07,200 --> 00:00:09,000
And the end!
"""


def test_parse_standard_cues():
    track = subtitles.parse_text(STD)
    assert len(track) == 3
    c = track.cues[0]
    assert c.start == 1.0 and c.end == 4.0
    assert c.text == "Hello world."          # tags stripped
    assert c.raw_text == "<i>Hello</i> world."
    assert c.index == 1
    assert c.raw_start == "00:00:01,000"


def test_multiline_text_joined_and_normalized():
    track = subtitles.parse_text(STD)
    assert track.cues[1].text == "A second cue spanning two lines"


def test_unindexed_cues_parse_positionally():
    # no integer index lines — positional '-->' detection must still work
    content = "00:00:02,000 --> 00:00:03,000\nNo index here.\n\n00:00:03,000 --> 00:00:05,000\nSecond."
    track = subtitles.parse_text(content)
    assert len(track) == 2
    assert track.cues[0].text == "No index here."
    assert track.cues[0].index == 1  # falls back to position


def test_variable_fractional_digits():
    # "40" hundredths must read as 0.4s, not 0.04s (the legacy int(x)/1000 bug)
    content = "1\n00:00:01,40 --> 00:00:02,5\nTick."
    c = subtitles.parse_text(content).cues[0]
    assert c.start == 1.4 and c.end == 2.5


def test_dot_separator_accepted():
    content = "1\n00:00:01.000 --> 00:00:02.000\nDot ms."
    assert subtitles.parse_text(content).cues[0].end == 2.0


def test_empty_text_block_skipped():
    content = "1\n00:00:01,000 --> 00:00:02,000\n<i></i>\n\n2\n00:00:02,000 --> 00:00:03,000\nReal."
    track = subtitles.parse_text(content)
    assert len(track) == 1 and track.cues[0].text == "Real."


def test_text_projection():
    assert subtitles.parse_text(STD).text() == "Hello world. A second cue spanning two lines And the end!"


def test_sentences_grouping():
    track = subtitles.parse_text(STD)
    sents = track.sentences()
    # cue 1 ends a sentence; cues 2+3 join into one ending at "!"
    assert [s.text for s in sents] == [
        "Hello world.",
        "A second cue spanning two lines And the end!",
    ]
    assert sents[1].start == 4.5 and sents[1].end == 9.0


def test_window_overlap():
    track = subtitles.parse_text(STD)
    win = track.window(center=4.0, half=1.0)  # [3.0, 5.0]
    assert {c.index for c in win} == {1, 2}


def test_at_lookup():
    track = subtitles.parse_text(STD)
    assert track.at(5.0).index == 2
    assert track.at(100.0) is None


def test_fix_hour_offset_applied_when_near_3600():
    content = "1\n01:00:05,000 --> 01:00:08,000\nShould shift."
    track = subtitles.parse_text(content, fix_hour_offset=True)
    c = track.cues[0]
    assert c.start == 5.0 and c.end == 8.0
    assert c.raw_start == "00:00:05,000"   # raw recomputed after shift


def test_fix_hour_offset_not_applied_when_off():
    content = "1\n01:00:05,000 --> 01:00:08,000\nNo shift."
    assert subtitles.parse_text(content, fix_hour_offset=False).cues[0].start == 3605.0


def test_fix_hour_offset_ignored_when_not_near_3600():
    content = "1\n00:00:05,000 --> 00:00:08,000\nNormal start."
    assert subtitles.parse_text(content, fix_hour_offset=True).cues[0].start == 5.0


def test_encoding_fallback(tmp_path):
    p = tmp_path / "latin.srt"
    p.write_bytes("1\n00:00:01,000 --> 00:00:02,000\ncaf\xe9\n".encode("latin-1"))
    track = subtitles.parse(p)
    assert track.cues[0].text == "café"


def test_empty_input():
    assert len(subtitles.parse_text("")) == 0
    assert not subtitles.parse_text("")
