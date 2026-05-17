"""Stage 1: Extract first 2 pages of all 177 residuals for Gemini Flash classification.

Targets: any file where author=Unknown OR year=0000 (broader than v2 which required all three).
"""
import os, re, json, sys
import fitz  # PyMuPDF

ROOT = r"D:\History vs Hype\library\by-topic"

def is_residual(filename: str) -> bool:
    """Match pattern Title-Author-Year-Publisher.ext where author=Unknown or year=0000."""
    m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)(?:-v\d+)?\.[a-z0-9]+$', filename, re.IGNORECASE)
    if not m:
        return False
    title, author, year, pub = m.groups()
    return (author.lower() == 'unknown' or year == '0000')

targets = []
for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p):
        continue
    for f in os.listdir(p):
        full = os.path.join(p, f)
        if not os.path.isfile(full):
            continue
        if not is_residual(f):
            continue
        targets.append({"folder": folder, "f": f, "size": os.path.getsize(full)})

print(f"Targets: {len(targets)}")

extracted = []
for i, t in enumerate(targets, 1):
    path = os.path.join(ROOT, t["folder"], t["f"])
    try:
        doc = fitz.open(path)
        n_pages = min(2, doc.page_count)
        text = ""
        for j in range(n_pages):
            text += doc[j].get_text() + "\n---PAGE---\n"
        n_total = doc.page_count
        doc.close()
        text = text[:3500]  # cap per file
        is_image_only = len(text.strip().replace("---PAGE---", "")) < 100
        extracted.append({
            "folder": t["folder"],
            "f": t["f"],
            "size_mb": round(t["size"] / 1024 / 1024, 2),
            "n_pages": n_total,
            "image_only": is_image_only,
            "text": text if not is_image_only else "",
        })
    except Exception as e:
        extracted.append({
            "folder": t["folder"], "f": t["f"], "size_mb": round(t["size"]/1024/1024, 2),
            "n_pages": 0, "image_only": False, "text": "", "error": str(e),
        })
    if i % 20 == 0:
        print(f"  {i}/{len(targets)}...", flush=True)

out = r"D:\History vs Hype\_gemini-output\layer2-rename\residual-extracts-v3.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=2, ensure_ascii=False)

n_text = sum(1 for e in extracted if not e.get("image_only") and not e.get("error") and e.get("text"))
n_img = sum(1 for e in extracted if e.get("image_only"))
n_err = sum(1 for e in extracted if e.get("error"))
print(f"\nDONE. {len(extracted)} files extracted -> {out}")
print(f"  Text-extractable: {n_text}")
print(f"  Image-only:       {n_img}")
print(f"  Errors:           {n_err}")
