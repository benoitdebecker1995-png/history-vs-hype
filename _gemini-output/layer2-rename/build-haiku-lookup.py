import json, re

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json", encoding="utf-8") as f:
    data = json.load(f)

# Build lookup batch: entries where year=0000 OR publisher is unknown-ish AND author isn't already an institution
INSTITUTION_AUTHORS = {"ICJ", "UN", "PhilippinesGov", "Manila", "Pereyaslav", "AngloGerman", "Unknown"}
PIRACY = {"unknown","zlib","libgen","annaarchive","z-library","",None}

lookups = []
for d in data:
    a = (d.get("a") or "").strip()
    y = (d.get("y") or "0000").strip()
    p = (d.get("p") or "").strip()
    p_low = p.lower()
    needs = (y == "0000") or (p_low in PIRACY)
    # If author is an institution like ICJ, don't ask Haiku - we know the publisher
    if a in INSTITUTION_AUTHORS:
        if a == "ICJ" and (p_low in PIRACY or p == ""):
            d["p"] = "ICJ"
        if a == "UN" and (p_low in PIRACY or p == ""):
            d["p"] = "UN"
        if a == "PhilippinesGov" and (p_low in PIRACY or p == ""):
            d["p"] = "PhilippinesGov"
        continue
    if needs:
        lookups.append(d)

print(f"Need lookup: {len(lookups)}")

# Re-save updated data with institution publishers filled
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Build numbered prompt for Haiku
lines = []
for idx, d in enumerate(lookups, 1):
    a = d.get("a", "Unknown")
    y = d.get("y", "0000")
    t = d.get("t", "Unknown")
    f_name = d.get("f", "")
    lines.append(f"{idx}. a={a} y={y} t={t} | {f_name}")

prompt = """You are looking up missing year and publisher for academic books on territorial disputes (Bakassi, Cyprus, Kosovo, Sabah, Belize-Guatemala, Armenia-Azerbaijan, India Partition, Preah Vihear, etc.).

For each numbered entry, output ONLY year and publisher. Use your training knowledge of these academic works.

OUTPUT FORMAT: JSON array, one object per entry, NO markdown fences, JSON only.
[{"i":1,"y":"YYYY","p":"Publisher"},{"i":2,"y":"YYYY","p":"Publisher"},...]

PUBLISHER ABBREVIATIONS (use these):
CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP, EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave, Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks

If you genuinely don't know, use "Unknown" for that field. Keep the existing year if already given (e.g., y=2019 in the input).

ENTRIES:
"""
prompt += "\n".join(lines)

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\haiku-territorial-input.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

# Save index map so we can match output back
idx_map = {idx: d["f"] for idx, d in enumerate(lookups, 1)}
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\haiku-territorial-idxmap.json", "w", encoding="utf-8") as f:
    json.dump(idx_map, f, indent=2, ensure_ascii=False)

print(f"Wrote haiku-territorial-input.txt ({len(lines)} entries)")
