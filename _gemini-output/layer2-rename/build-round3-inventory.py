"""Round 3: build inventory of incomplete library files.

Walks library/by-topic/**/*.pdf, parses canonical filenames
(Title-Author-Year-Publisher.ext), flags those with any Unknown / 0000
field, excludes image-only PDFs (from image-only-pdfs.json).

Output: round3-incomplete-inventory.json
"""
import json, os, re
from pathlib import Path

ROOT = Path(r"D:\History vs Hype\library\by-topic")
OUT_DIR = Path(r"D:\History vs Hype\_gemini-output\layer2-rename")
IMAGE_ONLY_JSON = OUT_DIR / "image-only-pdfs.json"

# Canonical pattern: Title-Author-Year-Publisher.ext
# Title can contain dashes (rare) but most are CamelCase single token.
# Author is surname (single word, possibly with hyphen).
# Year is 4-digit or "0000".
# Publisher is alphanumeric token, possibly hyphenated.
# Ext: pdf, epub, mobi, azw3.
# Year-anchored parser: split on dashes, find the rightmost token that is exactly
# 4 digits (the year). Author is the token to its left, title is everything left
# of that joined with dashes, publisher is everything to the right (before .ext).
EXT_RE = re.compile(r"\.(pdf|epub|mobi|azw3)$", re.IGNORECASE)
YEAR_TOKEN_RE = re.compile(r"^\d{4}$")

# Load image-only exclusion list. Match by (folder, filename) pair.
image_only_set = set()
if IMAGE_ONLY_JSON.exists():
    with open(IMAGE_ONLY_JSON, encoding="utf-8") as f:
        for entry in json.load(f):
            image_only_set.add((entry.get("folder", ""), entry.get("f", "")))
print(f"Image-only exclusions: {len(image_only_set)}")


def parse_canonical(fname: str):
    ext_m = EXT_RE.search(fname)
    if not ext_m:
        return None
    ext = ext_m.group(1).lower()
    stem = fname[: ext_m.start()]
    # Reject double-dash variants (legacy non-canonical) — they're separate cleanup.
    if "--" in stem:
        return None
    parts = stem.split("-")
    if len(parts) < 4:
        return None
    # Find rightmost year token.
    year_idx = None
    for i in range(len(parts) - 1, -1, -1):
        if YEAR_TOKEN_RE.match(parts[i]):
            year_idx = i
            break
    if year_idx is None or year_idx < 1 or year_idx >= len(parts) - 1:
        return None
    title = "-".join(parts[:year_idx - 1])
    author = parts[year_idx - 1]
    year = parts[year_idx]
    publisher = "-".join(parts[year_idx + 1:])
    if not title or not author or not publisher:
        return None
    return {
        "title": title,
        "author": author,
        "year": year,
        "publisher": publisher,
        "ext": ext,
    }


def missing_fields(parsed: dict) -> list:
    missing = []
    if parsed["title"].lower() == "unknown":
        missing.append("title")
    if parsed["author"].lower() == "unknown":
        missing.append("author")
    if parsed["year"] == "0000":
        missing.append("year")
    if parsed["publisher"].lower() == "unknown":
        missing.append("publisher")
    return missing


inventory = []
unparseable = []
total_files = 0
complete_count = 0
image_only_skipped = 0
idx = 0

for folder_dir in sorted(ROOT.iterdir()):
    if not folder_dir.is_dir():
        continue
    folder = folder_dir.name
    for fp in sorted(folder_dir.iterdir()):
        if not fp.is_file():
            continue
        if fp.suffix.lower() not in (".pdf", ".epub", ".mobi", ".azw3"):
            continue
        total_files += 1
        fname = fp.name

        parsed = parse_canonical(fname)
        if parsed is None:
            unparseable.append({"folder": folder, "filename": fname})
            continue

        missing = missing_fields(parsed)
        if not missing:
            complete_count += 1
            continue

        # Has at least one missing field. Skip if image-only.
        if (folder, fname) in image_only_set:
            image_only_skipped += 1
            continue

        idx += 1
        inventory.append({
            "idx": idx,
            "folder": folder,
            "filename": fname,
            "title": parsed["title"],
            "author": parsed["author"],
            "year": parsed["year"],
            "publisher": parsed["publisher"],
            "ext": parsed["ext"],
            "missing_fields": missing,
            "size_bytes": fp.stat().st_size,
        })

# Distribution
by_folder = {}
by_missing_field = {"title": 0, "author": 0, "year": 0, "publisher": 0}
for e in inventory:
    by_folder[e["folder"]] = by_folder.get(e["folder"], 0) + 1
    for fld in e["missing_fields"]:
        by_missing_field[fld] += 1

summary = {
    "total_files_scanned": total_files,
    "complete": complete_count,
    "image_only_skipped": image_only_skipped,
    "unparseable_filenames": len(unparseable),
    "incomplete_in_inventory": len(inventory),
    "by_folder": by_folder,
    "by_missing_field": by_missing_field,
}

out_path = OUT_DIR / "round3-incomplete-inventory.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"summary": summary, "unparseable": unparseable, "inventory": inventory}, f, indent=2)

print(json.dumps(summary, indent=2))
print(f"\nWrote {out_path}")
