"""Build Gemini batch from text-extracted PDFs."""
import json, os

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\unknown-pdf-extracts.json", encoding="utf-8") as f:
    extracted = json.load(f)

text_files = [e for e in extracted if len(e["text"].strip()) >= 100 and not e["text"].startswith("ERROR")]
image_files = [e for e in extracted if len(e["text"].strip()) < 100 or e["text"].startswith("ERROR")]

print(f"Text-extractable: {len(text_files)}")
print(f"Image-only / errors: {len(image_files)}")

prompt = """You will receive PDF first-2-pages text extracts from totally-unidentified academic library files. For each, identify the work.

OUTPUT FORMAT: JSON array, NO markdown fences, JSON only.
[{"i":N, "f":"<filename>", "t":"ShortTitleSlug", "a":"AuthorSurname", "y":"YYYY", "p":"PublisherAbbrev", "confidence":"high|medium|low"}]

RULES:
- t: CamelCase title slug, max 45 chars, strip "The"/"A"/"An"
- a: First author last name capitalised, max 25 chars
- y: 4-digit year. "0000" if not visible in text
- p: Publisher abbreviated. Use: CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP, EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave, Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill, Springer, DaCapo, FreePress, Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP, LiverpoolUP, etc.
- confidence: "high" if title page clearly states all fields; "medium" if some inference; "low" if mostly guessing
- If you genuinely cannot identify, use "Unknown" — confidence "low"

EXTRACTS:

"""

for idx, e in enumerate(text_files, 1):
    prompt += f"\n=== ENTRY {idx} ===\nFILENAME: {e['f']}\nFOLDER: {e['folder']}\nTEXT:\n{e['text']}\n"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\content-id-input.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

idx_map = {idx: e["f"] for idx, e in enumerate(text_files, 1)}
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\content-id-idxmap.json", "w", encoding="utf-8") as f:
    json.dump(idx_map, f, indent=2, ensure_ascii=False)

# Also save image-only list for separate user handling
folder_map = {e["folder"] + "/" + e["f"]: e for e in image_files}
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\image-only-pdfs.json", "w", encoding="utf-8") as f:
    json.dump(image_files, f, indent=2, ensure_ascii=False)

print(f"Wrote content-id-input.txt ({os.path.getsize(r'D:/History vs Hype/_gemini-output/layer2-rename/content-id-input.txt')//1024} KB)")
print(f"Image-only files saved separately")
