"""Stage 2B: Render page 1 of each needs_ocr PDF to PNG, prepare for Gemini multimodal.

Output: ocr-page1/{idx}_{safe_filename}.png + ocr-batch.json with file paths.
"""
import json, os, re
import fitz

ROOT = r"D:\History vs Hype\library\by-topic"
RESULTS = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-results.json"
IDXMAP = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-idxmap.json"
OUT_DIR = r"D:\History vs Hype\_gemini-output\layer2-rename\ocr-page1"
OUT_BATCH = r"D:\History vs Hype\_gemini-output\layer2-rename\ocr-batch.json"

os.makedirs(OUT_DIR, exist_ok=True)
results = json.load(open(RESULTS, encoding="utf-8"))
idxmap = json.load(open(IDXMAP, encoding="utf-8"))

needs_ocr = [r for r in results if r.get("needs_ocr")]
print(f"Files needing OCR: {len(needs_ocr)}")

batch = []
for r in needs_ocr:
    info = idxmap[str(r["idx"])]
    src = os.path.join(ROOT, info["folder"], info["f"])
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        continue
    safe = re.sub(r'[^\w\-]', '_', info["f"])[:60]
    out_png = os.path.join(OUT_DIR, f"{r['idx']:03d}_{safe}.png")
    try:
        doc = fitz.open(src)
        page = doc[0]
        # Render at ~150 DPI for OCR-friendly quality, cap width to control size
        mat = fitz.Matrix(1.5, 1.5)
        pix = page.get_pixmap(matrix=mat)
        pix.save(out_png)
        doc.close()
        batch.append({
            "idx": r["idx"],
            "folder": info["folder"],
            "f": info["f"],
            "png": out_png,
            "size_kb": round(os.path.getsize(out_png)/1024, 1),
        })
        print(f"  [{r['idx']:3d}] {info['f'][:60]:60s} -> {batch[-1]['size_kb']} KB")
    except Exception as e:
        print(f"  ERROR [{r['idx']}] {info['f']}: {e}")

with open(OUT_BATCH, "w", encoding="utf-8") as f:
    json.dump(batch, f, indent=2, ensure_ascii=False)
print(f"\nWrote {OUT_BATCH} ({len(batch)} entries)")
