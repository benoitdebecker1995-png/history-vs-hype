"""Stage 2A: Build filename-only classification input for image-only PDFs + errored files."""
import json, os

EXTRACTS = r"D:\History vs Hype\_gemini-output\layer2-rename\residual-extracts-v3.json"
OUT_INPUT = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-input.txt"
OUT_IDXMAP = r"D:\History vs Hype\_gemini-output\layer2-rename\imgonly-idxmap.json"

d = json.load(open(EXTRACTS, encoding="utf-8"))
targets = [e for e in d if e.get("image_only") or e.get("error")]
print(f"Image-only + errored: {len(targets)}")

idxmap = {}
lines = []
for i, e in enumerate(targets):
    idxmap[str(i)] = {"folder": e["folder"], "f": e["f"], "image_only": bool(e.get("image_only")), "size_mb": e.get("size_mb", 0)}
    err = f" [ERROR: {e.get('error','')}]" if e.get("error") else ""
    lines.append(f"[{i}] folder={e['folder']} | filename={e['f']} | size={e.get('size_mb',0)}MB{err}")

with open(OUT_INPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
with open(OUT_IDXMAP, "w", encoding="utf-8") as f:
    json.dump(idxmap, f, indent=2, ensure_ascii=False)

print(f"Wrote {OUT_INPUT} ({os.path.getsize(OUT_INPUT)/1024:.1f} KB)")
