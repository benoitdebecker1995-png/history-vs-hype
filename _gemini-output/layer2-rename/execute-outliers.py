import json, os, re, hashlib
from collections import defaultdict

ROOT = r"D:\History vs Hype\library\by-topic"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outlier-meta.json", encoding="utf-8") as f:
    meta = json.load(f)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outlier-idxmap.json", encoding="utf-8") as f:
    idxmap = json.load(f)

def sanitise(s, maxlen=45):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", ""): return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

# Build rename plan, grouped by folder
plan = []
for d in meta:
    info = idxmap.get(str(d["i"]))
    if not info: continue
    folder = info["folder"]
    orig_f = info["f"]
    src = os.path.join(ROOT, folder, orig_f)
    if not os.path.exists(src): continue
    t = sanitise(d.get("t","Unknown"), 45)
    a = sanitise(d.get("a","Unknown"), 25)
    y = (d.get("y","0000") or "0000").strip()
    if not re.match(r"^\d{4}$", y): y = "0000"
    p = sanitise(d.get("p","Unknown"), 30)
    ext = os.path.splitext(orig_f)[1].lower()
    new_name = f"{t}-{a}-{y}-{p}{ext}"
    dst = os.path.join(ROOT, folder, new_name)
    plan.append({"folder": folder, "old": orig_f, "new": new_name, "src": src, "dst": dst, "size": os.path.getsize(src)})

# Group by dst per folder
groups = defaultdict(list)
for op in plan:
    groups[op["dst"]].append(op)

renamed = 0
dup_deleted = 0
disambiguated = 0
errors = []
existing_collision_skipped = 0

for dst, ops in groups.items():
    if len(ops) == 1:
        op = ops[0]
        if op["src"] == op["dst"]: continue
        if os.path.exists(op["dst"]):
            # Hash compare with existing canonical-named file
            try:
                with open(op["src"],"rb") as f: h1 = hashlib.md5(f.read()).hexdigest()
                with open(op["dst"],"rb") as f: h2 = hashlib.md5(f.read()).hexdigest()
                if h1 == h2:
                    os.remove(op["src"])
                    dup_deleted += 1
                    continue
                # Different content, disambiguate
                base, ext = os.path.splitext(op["new"])
                # find next available -vN
                n = 2
                while os.path.exists(os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")):
                    n += 1
                op["new"] = f"{base}-v{n}{ext}"
                op["dst"] = os.path.join(ROOT, op["folder"], op["new"])
                os.rename(op["src"], op["dst"])
                disambiguated += 1
                renamed += 1
            except OSError as e:
                errors.append(f"{op['old']}: {e}")
                existing_collision_skipped += 1
            continue
        try:
            os.rename(op["src"], op["dst"])
            renamed += 1
        except OSError as e:
            errors.append(f"{op['old']}: {e}")
        continue
    # Multiple ops -> same dst within outliers
    ops_sorted = sorted(ops, key=lambda o: -o["size"])
    biggest = ops_sorted[0]
    if not os.path.exists(biggest["dst"]):
        try:
            os.rename(biggest["src"], biggest["dst"])
            renamed += 1
        except OSError as e:
            errors.append(f"{biggest['old']}: {e}")
    # Rest: dedup by hash, else -vN
    try:
        with open(biggest["dst"],"rb") as f: bh = hashlib.md5(f.read()).hexdigest()
    except OSError:
        bh = None
    for o in ops_sorted[1:]:
        if not os.path.exists(o["src"]): continue
        try:
            with open(o["src"],"rb") as f: oh = hashlib.md5(f.read()).hexdigest()
            if bh and oh == bh:
                os.remove(o["src"])
                dup_deleted += 1
                continue
            base, ext = os.path.splitext(o["new"])
            n = 2
            while os.path.exists(os.path.join(ROOT, o["folder"], f"{base}-v{n}{ext}")):
                n += 1
            new_name = f"{base}-v{n}{ext}"
            os.rename(o["src"], os.path.join(ROOT, o["folder"], new_name))
            disambiguated += 1
            renamed += 1
        except OSError as e:
            errors.append(f"{o['old']}: {e}")

report = [
    "=== Outlier Rename Report (2026-05-12) ===",
    f"Planned: {len(plan)}",
    f"Renamed: {renamed}",
    f"Duplicates deleted (hash match): {dup_deleted}",
    f"Disambiguated -vN: {disambiguated}",
    f"Errors: {len(errors)}",
    "",
    "Errors:",
    *errors[:30],
]
report_text = "\n".join(report)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\outlier-rename-report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)
print(report_text)
