import re, json, sys

raw = open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.raw.txt", encoding="utf-8").read()
m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw, re.DOTALL)
if not m:
    m = re.search(r"(\[\s*\{.*\}\s*\])", raw, re.DOTALL)
if not m:
    print("NO JSON BLOCK FOUND"); sys.exit(1)
data = json.loads(m.group(1))
print(f"Parsed {len(data)} entries")
out = r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Written {out}")

unknown_pub = [d for d in data if d.get("p","").lower() in ("unknown","zlib","libgen","annaarchive","z-library","")]
unknown_year = [d for d in data if d.get("y","0000") == "0000"]
print(f"Publisher unknown: {len(unknown_pub)}")
print(f"Year unknown: {len(unknown_year)}")
