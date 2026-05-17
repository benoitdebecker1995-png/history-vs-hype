"""Apply publisher-lookup results to rename files."""
import json, os, re, hashlib
from collections import defaultdict

ROOT = r"D:\History vs Hype\library\by-topic"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\publisher-lookup-output.json", encoding="utf-8") as f:
    results = json.load(f)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\publisher-lookup-idxmap.json", encoding="utf-8") as f:
    idxmap = json.load(f)

def sanitise(s, maxlen=30):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", ""): return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

# Build rename ops
ops = []
for r in results:
    new_pub = r.get("p","Unknown")
    if new_pub == "Unknown": continue
    info = idxmap.get(str(r["i"]))
    if not info: continue
    folder = info["folder"]
    old_name = info["f"]
    src = os.path.join(ROOT, folder, old_name)
    if not os.path.exists(src): continue
    # Replace publisher segment in filename
    m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$', old_name)
    if not m: continue
    t, a, y, old_pub, tail = m.groups()
    new_pub_s = sanitise(new_pub, 30)
    new_name = f"{t}-{a}-{y}-{new_pub_s}{tail}"
    if new_name == old_name: continue
    dst = os.path.join(ROOT, folder, new_name)
    ops.append({"folder":folder,"old":old_name,"new":new_name,"src":src,"dst":dst})

print(f"Rename ops: {len(ops)}")

renamed = 0
dup_deleted = 0
disambiguated = 0
errors = []

for op in ops:
    if not os.path.exists(op["src"]): continue
    if os.path.exists(op["dst"]):
        # Hash compare
        try:
            with open(op["src"],"rb") as fh: h1 = hashlib.md5(fh.read()).hexdigest()
            with open(op["dst"],"rb") as fh: h2 = hashlib.md5(fh.read()).hexdigest()
            if h1 == h2:
                os.remove(op["src"])
                dup_deleted += 1
                continue
            base, ext = os.path.splitext(op["new"])
            n = 2
            while os.path.exists(os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")):
                n += 1
            new_dst = os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")
            os.rename(op["src"], new_dst)
            disambiguated += 1
            renamed += 1
        except OSError as e:
            errors.append(f"{op['old']}: {e}")
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(f"{op['old']}: {e}")

print(f"Renamed:      {renamed}")
print(f"Dup-deleted:  {dup_deleted}")
print(f"Disambiguated:{disambiguated}")
print(f"Errors:       {len(errors)}")
for e in errors[:10]: print(f"  {e}")

report = [
    "=== Publisher Lookup Report (2026-05-12) ===",
    f"Haiku resolved publishers: {sum(1 for r in results if r.get('p','Unknown') != 'Unknown')} / {len(results)}",
    f"Applied renames: {renamed}",
    f"Hash-dedup deleted: {dup_deleted}",
    f"Disambiguated -vN: {disambiguated}",
    f"Errors: {len(errors)}",
]
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\publisher-lookup-report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
