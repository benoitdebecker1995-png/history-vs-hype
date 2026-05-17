"""Stage 2 prep: Build Gemini Flash classification input + prompt from residual extracts."""
import json, os

EXTRACTS = r"D:\History vs Hype\_gemini-output\layer2-rename\residual-extracts-v3.json"
OUT_INPUT = r"D:\History vs Hype\_gemini-output\layer2-rename\classify-input.txt"
OUT_IDXMAP = r"D:\History vs Hype\_gemini-output\layer2-rename\classify-idxmap.json"

d = json.load(open(EXTRACTS, encoding="utf-8"))
text_extractable = [e for e in d if not e.get("image_only") and not e.get("error") and e.get("text")]
print(f"Text-extractable: {len(text_extractable)}")

# Build idxmap so we can resolve idx -> (folder, filename) later
idxmap = {}
lines = []
for i, e in enumerate(text_extractable):
    idxmap[str(i)] = {"folder": e["folder"], "f": e["f"]}
    txt = e["text"].replace("---PAGE---", " | ").strip()
    txt = " ".join(txt.split())[:2500]  # collapse whitespace, cap
    lines.append(f"=== [{i}] folder={e['folder']} | filename={e['f']} ===\n{txt}\n")

with open(OUT_INPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
with open(OUT_IDXMAP, "w", encoding="utf-8") as f:
    json.dump(idxmap, f, indent=2, ensure_ascii=False)

size = os.path.getsize(OUT_INPUT)
print(f"Wrote {OUT_INPUT} ({size/1024:.1f} KB)")
print(f"Wrote {OUT_IDXMAP}")
