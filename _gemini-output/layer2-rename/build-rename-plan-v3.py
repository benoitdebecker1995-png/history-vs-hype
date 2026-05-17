"""Stage 3: Merge all three classification sources into a single rename plan.

Inputs:
  - classify-results.json    (148 text-extractable Gemini Flash classifications)
  - imgonly-results.json     (44 image-only filename-based + manual OCR overrides)
  - ocr-results-manual.json  (14 overrides where filename-only confidence was low; manual page-1 image reads)

For each file, produce:
  {
    "current_path": "...",
    "current_filename": "...",
    "action": "rename" | "move+rename" | "stash",
    "new_folder": "...",
    "new_filename": "...",
    "confidence": "high|medium|low",
    "rationale": "..."
  }

Filename convention: ShortTitle-Author-Year-Publisher.ext (matches canonical Layer 2 format).
"""
import json, os, re

ROOT = r"D:\History vs Hype\library\by-topic"
STASH_DIR = r"_stash-offtopic"  # relative to library root

CLASSIFY_RESULTS = r"D:\History vs Hype\_gemini-output\layer2-rename\classify-results.json"
CLASSIFY_IDXMAP = r"D:\History vs Hype\_gemini-output\layer2-rename\classify-idxmap.json"
IMGONLY_RESULTS = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-results.json"
IMGONLY_IDXMAP = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-idxmap.json"
OCR_OVERRIDES = r"D:\History vs Hype\_gemini-output\layer2-rename\ocr-results-manual.json"

OUT_PLAN = r"D:\History vs Hype\_gemini-output\layer2-rename\rename-plan-v3.json"
OUT_HUMAN = r"D:\History vs Hype\_gemini-output\layer2-rename\rename-plan-v3.tsv"


def sanitize_title(s: str) -> str:
    s = re.sub(r'[^A-Za-z0-9]', '', s)
    return s[:50] if len(s) > 50 else s


def sanitize_author(s: str) -> str:
    s = re.sub(r'[^A-Za-z0-9\-]', '', s)
    return s if s else "Unknown"


def sanitize_pub(s: str) -> str:
    s = re.sub(r'[^A-Za-z0-9\-]', '', s)
    return s if s else "Unknown"


def build_new_filename(rec: dict, original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1].lower()
    t = sanitize_title(rec.get("title") or "Unknown")
    a = sanitize_author(rec.get("author") or "Unknown")
    y = rec.get("year") or "0000"
    if not re.match(r'^\d{4}$', y):
        y = "0000"
    p = sanitize_pub(rec.get("publisher") or "Unknown")
    return f"{t}-{a}-{y}-{p}{ext}"


# Load all data
classify = json.load(open(CLASSIFY_RESULTS, encoding="utf-8"))
classify_idx = json.load(open(CLASSIFY_IDXMAP, encoding="utf-8"))
imgonly = json.load(open(IMGONLY_RESULTS, encoding="utf-8"))
imgonly_idx = json.load(open(IMGONLY_IDXMAP, encoding="utf-8"))
ocr_overrides = {r["idx"]: r for r in json.load(open(OCR_OVERRIDES, encoding="utf-8"))}

plan = []
seen_paths = set()

# Stage A: text-extractable
for r in classify:
    info = classify_idx[str(r["idx"])]
    current_path = os.path.join(ROOT, info["folder"], info["f"])
    seen_paths.add(current_path)
    if r["keep"]:
        new_folder = r["topic"]
        new_filename = build_new_filename(r, info["f"])
        if info["folder"] != new_folder:
            action = "move+rename" if new_filename != info["f"] else "move"
        else:
            action = "rename" if new_filename != info["f"] else "noop"
    else:
        new_folder = STASH_DIR
        # keep current filename in stash (preserve audit trail)
        new_filename = info["f"]
        action = "stash"
    plan.append({
        "stage": "text-extract",
        "idx": r["idx"],
        "current_path": current_path,
        "current_folder": info["folder"],
        "current_filename": info["f"],
        "action": action,
        "new_folder": new_folder,
        "new_filename": new_filename,
        "confidence": r["conf"],
        "rationale": r.get("note", ""),
    })

# Stage B: image-only (with OCR overrides)
for r in imgonly:
    info = imgonly_idx[str(r["idx"])]
    current_path = os.path.join(ROOT, info["folder"], info["f"])
    seen_paths.add(current_path)
    # Apply OCR override if present
    if r["idx"] in ocr_overrides:
        r = ocr_overrides[r["idx"]]
        stage = "image-ocr"
    else:
        stage = "image-filename"
    if r["keep"]:
        new_folder = r["topic"]
        new_filename = build_new_filename(r, info["f"])
        if info["folder"] != new_folder:
            action = "move+rename" if new_filename != info["f"] else "move"
        else:
            action = "rename" if new_filename != info["f"] else "noop"
    else:
        new_folder = STASH_DIR
        new_filename = info["f"]
        action = "stash"
    plan.append({
        "stage": stage,
        "idx": r["idx"],
        "current_path": current_path,
        "current_folder": info["folder"],
        "current_filename": info["f"],
        "action": action,
        "new_folder": new_folder,
        "new_filename": new_filename,
        "confidence": r["conf"],
        "rationale": r.get("note", ""),
    })

# Write JSON
with open(OUT_PLAN, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

# Write human-readable TSV
with open(OUT_HUMAN, "w", encoding="utf-8") as f:
    f.write("action\tconf\tcurrent_folder\tnew_folder\tcurrent_filename\tnew_filename\trationale\n")
    for p in sorted(plan, key=lambda x: (x["action"], x["current_folder"], x["current_filename"])):
        f.write(f"{p['action']}\t{p['confidence']}\t{p['current_folder']}\t{p['new_folder']}\t{p['current_filename']}\t{p['new_filename']}\t{p['rationale']}\n")

# Stats
from collections import Counter
print(f"Total plan entries: {len(plan)}")
print()
print("By action:")
for k, v in Counter(p["action"] for p in plan).most_common():
    print(f"  {k}: {v}")
print()
print("By confidence:")
for k, v in Counter(p["confidence"] for p in plan).most_common():
    print(f"  {k}: {v}")
print()
print("New-folder distribution (keepers):")
keepers = [p for p in plan if p["action"] != "stash"]
for k, v in Counter(p["new_folder"] for p in keepers).most_common():
    print(f"  {k}: {v}")
print(f"\nWrote {OUT_PLAN}")
print(f"Wrote {OUT_HUMAN}")
