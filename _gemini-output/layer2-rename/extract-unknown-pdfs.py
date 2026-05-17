"""Extract first 2 pages of 90 totally-unknown PDFs for content-based identification."""
import os, re, json
import fitz  # PyMuPDF

ROOT = r"D:\History vs Hype\library\by-topic"
targets = []
for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        full = os.path.join(p, f)
        if not os.path.isfile(full): continue
        m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)(?:-v\d+)?\.[a-z0-9]+$', f)
        if not m: continue
        t, a, y, pub = m.groups()
        if a.lower() == 'unknown' and y == '0000' and pub.lower() in ('unknown','zlib','libgen','annaarchive','z-library'):
            targets.append({"folder": folder, "f": f, "size": os.path.getsize(full)})

print(f"Targets: {len(targets)}")

extracted = []
for t in targets:
    path = os.path.join(ROOT, t["folder"], t["f"])
    try:
        doc = fitz.open(path)
        n_pages = min(2, doc.page_count)
        text = ""
        for i in range(n_pages):
            text += doc[i].get_text() + "\n---PAGE---\n"
        doc.close()
        text = text[:3000]  # cap per file
        extracted.append({"folder": t["folder"], "f": t["f"], "size": t["size"], "text": text})
    except Exception as e:
        extracted.append({"folder": t["folder"], "f": t["f"], "size": t["size"], "text": f"ERROR: {e}"})

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\unknown-pdf-extracts.json", "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=2, ensure_ascii=False)
print(f"Extracted: {len(extracted)} -> unknown-pdf-extracts.json")
empty = sum(1 for e in extracted if len(e["text"].strip()) < 100)
print(f"Files with <100 chars extracted (likely image-only PDFs): {empty}")
