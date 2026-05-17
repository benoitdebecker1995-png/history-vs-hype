import os, re, json
ROOT = r"D:\History vs Hype\library\by-topic"
HAS_YEAR = re.compile(r'-\d{4}-')

outliers = []
for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        full = os.path.join(p, f)
        if not os.path.isfile(full): continue
        if ' ' in f or '(' in f or '[' in f or '{' in f or not HAS_YEAR.search(f):
            outliers.append({"folder": folder, "f": f, "size": os.path.getsize(full)})

print(f"Outliers: {len(outliers)}")

# Heuristic flag for off-topic content
OFFTOPIC_KEYWORDS = [
    "Drakkenheim", "Grim Hollow", "Etharis", "World Anvil",  # D&D
    "ministère", "Région wallonne",  # Belgian regional gov
    "Sebastian Crowe", "Monty Martin",  # D&D / gaming
]
flagged = []
to_rename = []
for o in outliers:
    f_low = o["f"].lower()
    if any(kw.lower() in f_low for kw in OFFTOPIC_KEYWORDS):
        flagged.append(o)
    else:
        to_rename.append(o)

print(f"Flagged off-topic: {len(flagged)}")
print(f"To rename via Gemini: {len(to_rename)}")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outliers-flagged-offtopic.json", "w", encoding="utf-8") as f:
    json.dump(flagged, f, indent=2, ensure_ascii=False)

# Build Gemini prompt (numbered list, includes folder for context)
lines = []
for idx, o in enumerate(to_rename, 1):
    lines.append(f"{idx}. [{o['folder']}] {o['f']}")

prompt = """You will receive a numbered list of PDF filenames from an academic library on history (territorial disputes, colonialism, African history, Middle East, etc.). Each line has folder prefix.

Parse each filename and extract metadata.

OUTPUT FORMAT: a single JSON array. NO markdown fences, JSON only.

Each object:
{"i": N, "f": "<original filename>", "a": "AuthorSurname", "y": "YYYY", "t": "ShortTitleSlug", "p": "PublisherAbbrev"}

RULES:
- a: Author last name capitalised, max 25 chars. Multi-author -> first author. Treaty/UN/Govt -> issuing body abbrev (UN, ICJ, UK, etc.). Unknown -> "Unknown"
- y: 4-digit year. If unknown -> "0000". Extract from filename if present.
- t: Key meaningful title words, CamelCase, no spaces, no special chars, max 45 chars. Strip "The"/"A"/"An" prefix. Strip piracy markers (z-library, libgen, Anna's Archive).
- p: Real publisher only. Use abbreviations: CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP, EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave, Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill, Springer, DaCapo, FreePress, Granta, WeidenfeldNicolson, Cornell-UP, Stanford-UP, Harvard-UP, Liverpool-UP. If piracy source only -> "Unknown".

ENTRIES:
"""
prompt += "\n".join(lines)

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outlier-gemini-input.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

# Save index map: i -> {folder, f}
idx_map = {idx: {"folder": o["folder"], "f": o["f"]} for idx, o in enumerate(to_rename, 1)}
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outlier-idxmap.json", "w", encoding="utf-8") as f:
    json.dump(idx_map, f, indent=2, ensure_ascii=False)

print(f"Wrote outlier-gemini-input.txt with {len(to_rename)} entries")
