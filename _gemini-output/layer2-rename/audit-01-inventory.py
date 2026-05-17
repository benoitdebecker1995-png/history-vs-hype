"""Audit Step 1: Inventory entire library/by-topic/, parse Title-Author-Year-Publisher.ext."""
import os, re, json
from collections import Counter

ROOT = r"D:\History vs Hype\library\by-topic"
OUT = r"D:\History vs Hype\_gemini-output\layer2-rename\library-inventory.json"

FNAME_RE = re.compile(r'^(.+?)-(.+?)-(\d{4})-(.+?)(?:-v\d+)?\.([a-z0-9]+)$', re.IGNORECASE)

records = []
unparseable = []

for folder in sorted(os.listdir(ROOT)):
    folder_path = os.path.join(ROOT, folder)
    if not os.path.isdir(folder_path):
        continue
    for f in os.listdir(folder_path):
        full = os.path.join(folder_path, f)
        if not os.path.isfile(full):
            continue
        m = FNAME_RE.match(f)
        if not m:
            unparseable.append({"folder": folder, "f": f})
            continue
        title, author, year, pub, ext = m.groups()
        # Detect -v2/-v3 suffix on full name
        m2 = re.match(r'^(.+?)-v(\d+)$', os.path.splitext(f)[0])
        v = int(m2.group(2)) if m2 else 1
        records.append({
            "folder": folder,
            "filename": f,
            "title": title,
            "author": author,
            "year": year,
            "publisher": pub,
            "ext": ext.lower(),
            "size": os.path.getsize(full),
            "version_suffix": v,
        })

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"records": records, "unparseable": unparseable}, f, indent=2, ensure_ascii=False)

print(f"Total files: {len(records) + len(unparseable)}")
print(f"  Parseable:   {len(records)}")
print(f"  Unparseable: {len(unparseable)}")
print()
print("By folder:")
for k, v in Counter(r["folder"] for r in records).most_common():
    print(f"  {k}: {v}")
print()
print("Top 20 publishers (raw slugs):")
for k, v in Counter(r["publisher"] for r in records).most_common(20):
    print(f"  {v:4d}  {k}")
print()
print("Top 20 authors:")
for k, v in Counter(r["author"] for r in records).most_common(20):
    print(f"  {v:4d}  {k}")
if unparseable:
    print()
    print("Unparseable sample:")
    for u in unparseable[:10]:
        print(f"  {u['folder']}/{u['f']}")
