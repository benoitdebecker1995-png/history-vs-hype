"""
Audio Loudness QC — pre-publish gate against YouTube's -14 LUFS normalization.

YouTube normalizes every upload toward -14 LUFS integrated. If your master is
quieter, viewers reach for the volume; louder, YouTube turns you down (and any
headroom you fought for is gone). True-peak above -1 dBTP risks audible clipping
after lossy transcode. This catches all three before you upload.

Adapted from deeployCO/youtube-seo-skills (audio_loudness.py). Measures via
ffmpeg's `loudnorm` analysis filter (EBU R128). Works on a local render (your
exported .mp4/.wav) or, with yt-dlp, a competitor URL for reference.

Requires ffmpeg on PATH:
    winget install Gyan.FFmpeg        # Windows
    (or: choco install ffmpeg)

Usage:
    python -m tools.preflight.audio_loudness FINAL-CUT.mp4
    python -m tools.preflight.audio_loudness https://youtu.be/<id>   # needs yt-dlp
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# YouTube target band and risk thresholds (LUFS / dBTP / LU)
LUFS_TARGET = -14.0
LUFS_QUIET = -16.0    # below = viewers turn up
LUFS_LOUD = -12.0     # above = YouTube normalizes down
TP_CLIP = -1.0        # above = clipping risk
LRA_HIGH = 15.0       # above = volume-hunting (too dynamic for spoken VO)
LRA_LOW = 4.0         # below = over-compressed / lifeless

LOUDNORM_FILTER = "loudnorm=I=-14:TP=-1:LRA=11:print_format=json"


def _has(tool: str) -> bool:
    return shutil.which(tool) is not None


def _resolve_input(src: str) -> Optional[Path]:
    """Local path -> as-is. URL -> yt-dlp bestaudio to a temp m4a."""
    if not re.match(r"^https?://", src):
        p = Path(src)
        return p if p.exists() else None
    if not _has("yt-dlp"):
        logger.error("URL given but yt-dlp not installed (pip install yt-dlp)")
        return None
    tmp = Path(tempfile.gettempdir()) / "loudness_probe.m4a"
    subprocess.run(
        ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "m4a",
         "-o", str(tmp.with_suffix("")), src],
        check=True, capture_output=True, text=True,
    )
    return tmp if tmp.exists() else None


def measure(src: str) -> Dict:
    if not _has("ffmpeg"):
        return {"verdict": "MISSING", "error":
                "ffmpeg not found. Install:  winget install Gyan.FFmpeg"}

    path = _resolve_input(src)
    if path is None:
        return {"verdict": "MISSING", "error": f"Input not found: {src}"}

    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", LOUDNORM_FILTER, "-f", "null", "-"],
        capture_output=True, text=True,
    )
    # loudnorm prints its JSON block to stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", proc.stderr, re.S)
    if not m:
        return {"verdict": "MISSING",
                "error": "Could not parse loudnorm output (no audio track?)",
                "raw": proc.stderr[-400:]}
    data = json.loads(m.group(0))
    lufs = float(data["input_i"])
    tp = float(data["input_tp"])
    lra = float(data["input_lra"])

    issues, passes = [], []
    if lufs < LUFS_QUIET:
        issues.append(f"QUIET — {lufs:.1f} LUFS (<{LUFS_QUIET}). "
                      "Viewers will turn up; YouTube won't boost you to target.")
    elif lufs > LUFS_LOUD:
        issues.append(f"LOUD — {lufs:.1f} LUFS (>{LUFS_LOUD}). "
                      "YouTube normalizes down; you lose any headroom you mastered for.")
    else:
        passes.append(f"Integrated {lufs:.1f} LUFS — in YouTube's {LUFS_TARGET} band")

    if tp > TP_CLIP:
        issues.append(f"PEAKS — true peak {tp:.1f} dBTP (>{TP_CLIP}). "
                      "Clipping risk after transcode; add a limiter.")
    else:
        passes.append(f"True peak {tp:.1f} dBTP OK")

    if lra > LRA_HIGH:
        issues.append(f"DYNAMIC — loudness range {lra:.1f} LU (>{LRA_HIGH}). "
                      "Quiet parts vanish; compress the VO.")
    elif lra < LRA_LOW:
        issues.append(f"FLAT — loudness range {lra:.1f} LU (<{LRA_LOW}). "
                      "Over-compressed; let it breathe.")
    else:
        passes.append(f"Loudness range {lra:.1f} LU OK")

    verdict = "PASS" if not issues else ("REVIEW" if len(issues) == 1 else "FAIL")
    return {"verdict": verdict, "lufs": lufs, "tp": tp, "lra": lra,
            "issues": issues, "passes": passes, "input": str(path)}


def print_report(r: Dict) -> None:
    if r.get("error"):
        print(f"\n  AUDIO LOUDNESS: {r['verdict']} — {r['error']}\n")
        return
    colors = {"PASS": "\033[32m", "REVIEW": "\033[33m", "FAIL": "\033[31m"}
    reset = "\033[0m"
    v = (f"{colors.get(r['verdict'],'')}{r['verdict']}{reset}"
         if sys.stderr.isatty() else r["verdict"])
    print(f"\n{'=' * 60}\n  AUDIO LOUDNESS QC\n{'=' * 60}")
    print(f"\n  Verdict: {v}")
    print(f"  Integrated: {r['lufs']:.1f} LUFS  |  True peak: {r['tp']:.1f} dBTP"
          f"  |  Range: {r['lra']:.1f} LU   (target -14 LUFS)")
    if r["passes"]:
        print("\n  PASSES:")
        for p in r["passes"]:
            print(f"    + {p}")
    if r["issues"]:
        print("\n  ISSUES:")
        for i in r["issues"]:
            print(f"    ! {i}")
    print(f"\n{'=' * 60}\n")


def main():
    ap = argparse.ArgumentParser(
        description="Check audio loudness against YouTube's -14 LUFS target")
    ap.add_argument("input", help="Local media file, or a YouTube URL (needs yt-dlp)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    r = measure(args.input)
    print_report(r)
    sys.exit({"PASS": 0, "REVIEW": 1, "FAIL": 2, "MISSING": 2}.get(r["verdict"], 2))


if __name__ == "__main__":
    main()
