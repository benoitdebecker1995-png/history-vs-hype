"""
Thumbnail Image Audit — pixel-level QC of a RENDERED thumbnail.

Complements `thumbnail_checker.py` (which scores the *concept text* pre-render).
This tool verifies the image NECESSARY conditions the concept checker can't see.
It is a FILTER, not a clickability predictor (clickability is decided by native A/B):

  1. Technical compliance    (>=1280x720, ~16:9, <2MB, JPG/PNG)
  2. Feed-size legibility     (COMPUTED detail gate at 160px + preview render) — the
                              one image-computable failure: a mushy blob that won't
                              read in feed. This drives the verdict. Calibrated on real
                              winners/losers 2026-06-14 (blob=2103, winners>=4255).
  3. SERP differentiation     (CLIP cosine vs the actual shelf) — INFORMATIONAL ONLY.
                              Differentiation is NOT clickability (a low-info blob is
                              "distinct"); the old +5/-20 scoring was a false-confidence
                              bug and has been removed.

Curiosity-gap (title vs overlay), single-focal-point, and AI-figure are SEMANTIC —
handled by thumbnail_checker, thumbnail-critic, and native A/B, not here.
See .claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md.

Adapted from deeployCO/youtube-seo-skills (analyze_thumbnail.py / SKILL.md), with
two improvements for this repo:
  - Competitor thumbnails auto-download by video ID from i.ytimg.com (public, no
    auth) instead of requiring a pre-downloaded folder.
  - OpenCV face detection dropped (the concept checker already gates faces; our
    thumbnails are maps/documents). Net deps: Pillow + numpy, optional open_clip.

CLIP differentiation requires `open_clip_torch` (torch already vendored). Without
it, falls back to an RGB-histogram cosine proxy (directional only, flagged).

Usage:
    # Audit a rendered thumbnail against named competitor video IDs:
    python -m tools.preflight.thumbnail_image_audit my_thumb.jpg --serp-ids dQw4w9WgXcQ,oHg5SJYRHA0

    # Or against a folder of pre-downloaded competitor thumbnails:
    python -m tools.preflight.thumbnail_image_audit my_thumb.jpg --serp-dir competitors/

    # Tech + legibility only (no differentiation):
    python -m tools.preflight.thumbnail_image_audit my_thumb.jpg
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# --- thresholds --------------------------------------------------------------
MIN_WIDTH = 1280
MIN_HEIGHT = 720
TARGET_RATIO = 16 / 9
RATIO_TOLERANCE = 0.05          # +/- 5% of 16:9
MAX_BYTES = 2 * 1024 * 1024     # YouTube hard cap 2MB
MOBILE_SIZES = [(120, 68), (246, 138), (480, 270)]  # feed / search / mid

# Feed-size legibility gate (4-neighbour Laplacian variance at 160x90).
# Calibrated 2026-06-14 on REAL thumbnails: the one known mushy-blob failure
# (old Combo B coin) = 2103; every winner + clean render observed >= 4255.
# Below MIN = likely illegible at feed size. This is the #1 image-computable failure.
LEGIBILITY_MIN = 3000

# SERP differentiation bands (CLIP cosine). INFORMATIONAL ONLY — differentiation is
# NOT clickability (a low-info blob is "distinct" precisely because it's empty).
# Does NOT affect the score; the old +5/-20 scoring was the false-confidence bug.
DIFF_DISTINCT = 0.55
DIFF_SIMILAR = 0.70

CLIP_MODEL = "ViT-B-32"
CLIP_PRETRAINED = "openai"

YTIMG = "https://i.ytimg.com/vi/{vid}/{res}.jpg"


# ---------------------------------------------------------------------------
# Image loading / basic metrics
# ---------------------------------------------------------------------------
def _load_pil(path: Path):
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError(
            "Pillow not installed. Run:  pip install pillow"
        )
    return Image.open(path).convert("RGB")


def _tech_metrics(path: Path, img) -> Dict:
    w, h = img.size
    size_bytes = path.stat().st_size
    ratio = w / h if h else 0
    return {
        "width": w,
        "height": h,
        "ratio": ratio,
        "size_bytes": size_bytes,
        "format": (path.suffix.lstrip(".") or "?").upper(),
    }


def _dominant_colors(img, k: int = 3, sample: int = 4000) -> List[Tuple[str, float]]:
    """Tiny numpy k-means for dominant colors. Returns [(hex, share), ...]."""
    arr = np.asarray(img, dtype=np.float32).reshape(-1, 3)
    if len(arr) > sample:
        idx = np.random.default_rng(0).choice(len(arr), sample, replace=False)
        arr = arr[idx]
    # init centroids from quantiles for determinism
    centroids = arr[np.linspace(0, len(arr) - 1, k).astype(int)]
    for _ in range(8):
        d = np.linalg.norm(arr[:, None, :] - centroids[None, :, :], axis=2)
        labels = d.argmin(axis=1)
        new = np.array([arr[labels == i].mean(axis=0) if np.any(labels == i)
                        else centroids[i] for i in range(k)])
        if np.allclose(new, centroids, atol=1.0):
            centroids = new
            break
        centroids = new
    shares = [float(np.mean(labels == i)) for i in range(k)]
    order = np.argsort(shares)[::-1]
    out = []
    for i in order:
        r, g, b = centroids[i].astype(int).clip(0, 255)
        out.append((f"#{r:02x}{g:02x}{b:02x}", round(shares[i], 2)))
    return out


def _contrast(img) -> float:
    """Luminance std-dev as a visual-pop proxy (0-255 scale)."""
    arr = np.asarray(img, dtype=np.float32)
    lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    return float(lum.std())


def _legibility(img) -> float:
    """Detail retained at feed size (160x90), via 4-neighbour Laplacian variance.
    Low = mushy blob that won't read in the feed — the one image-computable failure.
    (Does NOT see curiosity-gap, single-focal-point, or AI-figure; those are semantic.)"""
    from PIL import Image
    s = np.asarray(img.resize((160, 90), Image.LANCZOS).convert("L"), dtype=np.float32)
    c = s[1:-1, 1:-1]
    lap = s[:-2, 1:-1] + s[2:, 1:-1] + s[1:-1, :-2] + s[1:-1, 2:] - 4 * c
    return float(lap.var())


def _write_mobile_previews(img, stem: str) -> Path:
    from PIL import Image
    out_dir = Path("tmp") / "thumb_previews"
    out_dir.mkdir(parents=True, exist_ok=True)
    for w, h in MOBILE_SIZES:
        small = img.resize((w, h), Image.LANCZOS)
        small.save(out_dir / f"{stem}_{w}x{h}.png")
    return out_dir


# ---------------------------------------------------------------------------
# Competitor SERP differentiation
# ---------------------------------------------------------------------------
def _download_serp(video_ids: List[str]) -> List[Path]:
    """Download maxresdefault (fallback hqdefault) competitor thumbs by ID."""
    import requests
    cache = Path("tmp") / "serp_thumbs"
    cache.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    for vid in video_ids:
        vid = vid.strip()
        if not vid:
            continue
        dest = cache / f"{vid}.jpg"
        if dest.exists() and dest.stat().st_size > 0:
            paths.append(dest)
            continue
        for res in ("maxresdefault", "hqdefault"):
            try:
                r = requests.get(YTIMG.format(vid=vid, res=res), timeout=15)
                if r.ok and len(r.content) > 1000:
                    dest.write_bytes(r.content)
                    paths.append(dest)
                    break
            except requests.RequestException as e:
                logger.debug("fetch %s/%s failed: %s", vid, res, e)
        else:
            logger.warning("Could not fetch thumbnail for video id: %s", vid)
    return paths


def _clip_embed(paths: List[Path]) -> Optional[np.ndarray]:
    """Embed images with open_clip. Returns (n, d) L2-normalized or None."""
    try:
        import torch
        import open_clip
        from PIL import Image
    except ImportError:
        return None
    model, _, preprocess = open_clip.create_model_and_transforms(
        CLIP_MODEL, pretrained=CLIP_PRETRAINED
    )
    model.eval()
    vecs = []
    with torch.no_grad():
        for p in paths:
            img = preprocess(Image.open(p).convert("RGB")).unsqueeze(0)
            v = model.encode_image(img)
            v = v / v.norm(dim=-1, keepdim=True)
            vecs.append(v.cpu().numpy()[0])
    return np.vstack(vecs)


def _hist_embed(paths: List[Path]) -> np.ndarray:
    """Fallback: normalized 8-bin-per-channel RGB histogram (directional only)."""
    from PIL import Image
    vecs = []
    for p in paths:
        arr = np.asarray(Image.open(p).convert("RGB").resize((128, 72)))
        h = np.concatenate([
            np.histogram(arr[..., c], bins=8, range=(0, 255))[0]
            for c in range(3)
        ]).astype(np.float32)
        n = np.linalg.norm(h)
        vecs.append(h / n if n else h)
    return np.vstack(vecs)


def _differentiation(target: Path, serp: List[Path]) -> Dict:
    """Mean cosine similarity of target vs each competitor + 3 closest."""
    all_paths = [target] + serp
    emb = _clip_embed(all_paths)
    method = "CLIP ViT-B/32"
    if emb is None:
        emb = _hist_embed(all_paths)
        method = "RGB-histogram (fallback — directional only)"
    t, comps = emb[0], emb[1:]
    sims = comps @ t  # both L2-normalized -> cosine
    mean_sim = float(sims.mean())
    order = np.argsort(sims)[::-1][:3]
    closest = [(serp[i].stem, round(float(sims[i]), 3)) for i in order]
    if mean_sim < DIFF_DISTINCT:
        band = "DISTINCT"
    elif mean_sim < DIFF_SIMILAR:
        band = "TYPICAL"
    else:
        band = "SIMILAR to shelf"
    return {
        "method": method,
        "mean_sim": round(mean_sim, 3),
        "band": band,
        "n_competitors": len(serp),
        "closest": closest,
    }


# ---------------------------------------------------------------------------
# Orchestration + scoring
# ---------------------------------------------------------------------------
def audit(thumb_path: str, serp_ids: Optional[str] = None,
          serp_dir: Optional[str] = None) -> Dict:
    path = Path(thumb_path)
    if not path.exists():
        return {"score": 0, "verdict": "MISSING",
                "issues": [f"Thumbnail not found: {thumb_path}"], "passes": [],
                "tech": {}, "diff": None}

    img = _load_pil(path)
    tech = _tech_metrics(path, img)
    issues: List[str] = []
    passes: List[str] = []
    score = 100

    # --- technical compliance ---
    if tech["width"] < MIN_WIDTH or tech["height"] < MIN_HEIGHT:
        issues.append(f"LOW RES — {tech['width']}x{tech['height']} "
                      f"(min {MIN_WIDTH}x{MIN_HEIGHT})")
        score -= 25
    else:
        passes.append(f"Resolution {tech['width']}x{tech['height']} OK")

    if abs(tech["ratio"] - TARGET_RATIO) > TARGET_RATIO * RATIO_TOLERANCE:
        issues.append(f"ASPECT RATIO {tech['ratio']:.2f} (need ~16:9 / 1.78)")
        score -= 10
    else:
        passes.append("16:9 aspect ratio OK")

    if tech["size_bytes"] > MAX_BYTES:
        issues.append(f"FILE TOO BIG — {tech['size_bytes']/1024/1024:.1f}MB "
                      f"(max 2MB; YouTube rejects)")
        score -= 15
    else:
        passes.append(f"File size {tech['size_bytes']/1024:.0f}KB OK")

    if tech["format"] not in ("JPG", "JPEG", "PNG"):
        issues.append(f"FORMAT {tech['format']} — use JPG or PNG")
        score -= 5

    # --- contrast / color ---
    contrast = _contrast(img)
    if contrast < 45:
        issues.append(f"LOW CONTRAST — luminance std {contrast:.0f} (<45 = flat). "
                      "Add tonal separation so it pops in feed.")
        score -= 10
    else:
        passes.append(f"Contrast (lum std {contrast:.0f}) OK")
    colors = _dominant_colors(img)
    passes.append("Dominant colors: " +
                  ", ".join(f"{hx} ({sh:.0%})" for hx, sh in colors))

    # --- feed-size legibility (the one image-computable failure: mushy blob) ---
    leg = _legibility(img)
    if leg < LEGIBILITY_MIN:
        issues.append(f"ILLEGIBLE AT FEED SIZE — detail {leg:.0f} < {LEGIBILITY_MIN} "
                      "(mushy/low-detail at 160px; the subject won't read in feed). "
                      "Fix: bigger subject, sharper cutout, heavier stroked text.")
        score -= 35
    else:
        passes.append(f"Feed-size legibility (detail {leg:.0f} >= {LEGIBILITY_MIN}) OK")

    # --- mobile previews ---
    preview_dir = _write_mobile_previews(img, path.stem)
    passes.append(f"Mobile previews written -> {preview_dir} "
                  "(eyeball the 120x68: is the subject readable?)")

    # --- SERP differentiation ---
    diff = None
    serp_paths: List[Path] = []
    if serp_dir:
        d = Path(serp_dir)
        serp_paths = [p for p in d.glob("*")
                      if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
        if not serp_paths:
            issues.append(f"--serp-dir {serp_dir} had no images")
    elif serp_ids:
        serp_paths = _download_serp(serp_ids.split(","))

    if serp_paths:
        diff = _differentiation(path, serp_paths)
        # INFORMATIONAL ONLY — differentiation is not clickability; no score impact.
        passes.append(f"SERP differentiation {diff['mean_sim']} — {diff['band']} "
                      f"({diff['method']}). Informational only — NOT a clickability signal.")
    else:
        passes.append("No competitors supplied — differentiation skipped "
                      "(informational only; pass --serp-ids id1,id2 to enable)")

    # Honest scope: this gate verifies image NECESSARY conditions only.
    passes.append("SCOPE: catches illegibility + tech only. Curiosity-gap (title vs "
                  "overlay), single-focal-point, and AI-figure are NOT image-computable "
                  "— use thumbnail_checker (duplication) + thumbnail-critic + native A/B.")

    score = max(0, min(100, score))
    verdict = "PASS" if score >= 80 else "REVIEW" if score >= 60 else "FAIL"
    return {"score": score, "verdict": verdict, "issues": issues,
            "passes": passes, "tech": tech, "diff": diff}


def print_report(result: Dict) -> None:
    verdict, score = result["verdict"], result["score"]
    colors = {"PASS": "\033[32m", "REVIEW": "\033[33m",
              "FAIL": "\033[31m", "MISSING": "\033[31m"}
    reset = "\033[0m"
    v = (f"{colors.get(verdict,'')}{verdict}{reset}"
         if sys.stderr.isatty() else verdict)
    print(f"\n{'=' * 60}\n  THUMBNAIL IMAGE FILTER  (feed-size legibility + tech — NOT clickability)\n{'=' * 60}")
    print(f"\n  Verdict: {v} ({score}/100 — filter score, not a clickability prediction)")
    if result.get("diff"):
        d = result["diff"]
        print(f"\n  DIFFERENTIATION ({d['method']}):")
        print(f"    mean similarity {d['mean_sim']} -> {d['band']} "
              f"vs {d['n_competitors']} competitors")
        for name, sim in d["closest"]:
            print(f"    closest: {name}  ({sim})")
    if result["passes"]:
        print("\n  PASSES:")
        for p in result["passes"]:
            print(f"    + {p}")
    if result["issues"]:
        print("\n  ISSUES:")
        for i in result["issues"]:
            print(f"    ! {i}")
    print(f"\n{'=' * 60}\n")


def main():
    ap = argparse.ArgumentParser(
        description="Audit a RENDERED thumbnail (tech, legibility, SERP differentiation)")
    ap.add_argument("thumbnail", help="Path to the rendered thumbnail image")
    ap.add_argument("--serp-ids",
                    help="Comma-separated competitor YouTube video IDs to compare against")
    ap.add_argument("--serp-dir",
                    help="Folder of pre-downloaded competitor thumbnails")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose, args.quiet)

    result = audit(args.thumbnail, args.serp_ids, args.serp_dir)
    print_report(result)
    sys.exit({"PASS": 0, "REVIEW": 1, "FAIL": 2, "MISSING": 2}.get(result["verdict"], 2))


if __name__ == "__main__":
    main()
