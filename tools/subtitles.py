"""Subtitles — the one place an SRT file becomes typed cues.

Canonical parser for the channel's .srt transcripts. Five call sites used to
hand-roll their own `parse_srt` (three regex variants returning three different
dict shapes, plus one using a third-party lib that isn't installed). This module
replaces them: `parse(path) -> SubtitleTrack`, with projections (`text`,
`sentences`, `window`, `at`) the callers need.

Stdlib only — no third-party dependency (the project's posture; see ADR-0010).
The engine is the union of the three regex parsers' robustness:
  - 4-encoding ladder (utf-8-sig, utf-8, cp1252, latin-1) + lossy fallback,
  - positional `-->` detection (handles indexed AND unindexed cues),
  - HTML-tag stripping + whitespace normalization,
  - opt-in +1h-offset correction for the known YouTube export bug.

`Cue` keeps the raw timestamp strings and raw text so a rewriter can round-trip.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import List, Optional

_ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")
_TS = r"(\d+):(\d+):(\d+)[,.](\d+)"
_TS_LINE = re.compile(rf"{_TS}\s*-->\s*{_TS}")
_TAG = re.compile(r"<[^>]+>")
_SENTENCE_END = re.compile(r"[.!?][\"']*\s*$")


@dataclass(frozen=True)
class Cue:
    """One subtitle block. `start`/`end` are seconds; `raw_*` preserve the
    source for round-trip rewriting."""

    start: float
    end: float
    text: str          # tag-stripped, whitespace-normalized
    index: int
    raw_start: str      # e.g. "00:00:12,400"
    raw_end: str
    raw_text: str       # before tag-stripping

    @property
    def duration(self) -> float:
        return self.end - self.start


def _ts_to_seconds(h: str, m: str, s: str, frac: str) -> float:
    # frac may be any digit length; interpret as a fraction of a second so
    # "400" -> 0.4 and "40" -> 0.4 (vs the legacy int(frac)/1000 bug).
    return int(h) * 3600 + int(m) * 60 + int(s) + int(frac) / (10 ** len(frac))


def _seconds_to_ts(seconds: float) -> str:
    seconds = max(0.0, seconds)
    ms = round((seconds - int(seconds)) * 1000)
    s = int(seconds)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d},{ms:03d}"


class SubtitleTrack:
    """An ordered list of cues plus the read projections callers need."""

    def __init__(self, cues: List[Cue]):
        self.cues = cues

    def __iter__(self):
        return iter(self.cues)

    def __len__(self) -> int:
        return len(self.cues)

    def __bool__(self) -> bool:
        return bool(self.cues)

    def text(self) -> str:
        """Whole transcript as continuous text."""
        return " ".join(c.text for c in self.cues)

    def sentences(self) -> List[Cue]:
        """Cues re-grouped into sentences by terminal punctuation.

        Each returned Cue spans from the start of its first source cue to the
        end of its last; `index` is the first source cue's index.
        """
        out: List[Cue] = []
        buf: List[Cue] = []
        for cue in self.cues:
            buf.append(cue)
            if _SENTENCE_END.search(cue.text):
                out.append(self._merge(buf))
                buf = []
        if buf:
            out.append(self._merge(buf))
        return out

    def window(self, center: float, half: float = 15.0) -> List[Cue]:
        """Cues overlapping [center-half, center+half] seconds."""
        return [
            c for c in self.cues
            if c.end >= center - half and c.start <= center + half
        ]

    def at(self, t: float) -> Optional[Cue]:
        """The cue covering time `t` seconds, or None."""
        return next((c for c in self.cues if c.start <= t <= c.end), None)

    @staticmethod
    def _merge(cues: List[Cue]) -> Cue:
        first, last = cues[0], cues[-1]
        return Cue(
            start=first.start,
            end=last.end,
            text=" ".join(c.text for c in cues).strip(),
            index=first.index,
            raw_start=first.raw_start,
            raw_end=last.raw_end,
            raw_text=" ".join(c.raw_text for c in cues).strip(),
        )


def _read(path: Path) -> str:
    for enc in _ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_text(content: str, *, fix_hour_offset: bool = False) -> SubtitleTrack:
    """Parse SRT text into a SubtitleTrack. See `parse` for options."""
    cues: List[Cue] = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for i, block in enumerate(blocks):
        lines = block.strip().split("\n")
        ts_line = next((ln for ln in lines if "-->" in ln), None)
        if ts_line is None:
            continue
        m = _TS_LINE.search(ts_line)
        if not m:
            continue
        start = _ts_to_seconds(*m.group(1, 2, 3, 4))
        end = _ts_to_seconds(*m.group(5, 6, 7, 8))
        raw_start, raw_end = (p.strip() for p in ts_line.split("-->")[:2])

        # index: the line above the timestamp if it's an integer, else position
        try:
            index = int(lines[0].strip())
        except (ValueError, IndexError):
            index = i + 1

        body = lines[lines.index(ts_line) + 1:]
        raw_text = " ".join(body)
        text = re.sub(r"\s+", " ", _TAG.sub("", raw_text)).strip()
        if not text:
            continue
        cues.append(Cue(start, end, text, index, raw_start, raw_end, raw_text))

    if fix_hour_offset and cues and 3500 <= cues[0].start <= 3700:
        cues = [
            replace(
                c,
                start=max(0.0, c.start - 3600.0),
                end=max(0.0, c.end - 3600.0),
                raw_start=_seconds_to_ts(max(0.0, c.start - 3600.0)),
                raw_end=_seconds_to_ts(max(0.0, c.end - 3600.0)),
            )
            for c in cues
        ]

    return SubtitleTrack(cues)


def parse(path, *, fix_hour_offset: bool = False) -> SubtitleTrack:
    """Parse an .srt file into a SubtitleTrack.

    Tries an encoding ladder then a lossy fallback, so it never raises on a
    decode error. `fix_hour_offset=True` applies the +1h export-bug correction
    when the first cue starts near 3600s (the legacy retention behavior).
    """
    return parse_text(_read(Path(path)), fix_hour_offset=fix_hour_offset)
