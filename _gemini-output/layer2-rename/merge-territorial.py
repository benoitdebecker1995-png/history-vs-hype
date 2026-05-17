import re, json, os

raw = open(r"D:\History vs Hype\_gemini-output\layer2-rename\haiku-territorial-output.raw.txt", encoding="utf-8").read()
m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw, re.DOTALL)
if not m:
    m = re.search(r"(\[\s*\{.*\}\s*\])", raw, re.DOTALL)
if not m:
    raise SystemExit("NO JSON")
lookup = json.loads(m.group(1))
print(f"Lookup entries: {len(lookup)}")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\haiku-territorial-idxmap.json", encoding="utf-8") as f:
    idxmap = json.load(f)

# Build filename -> {y,p} from lookup
lookup_by_fname = {}
for r in lookup:
    fname = idxmap.get(str(r["i"]))
    if fname:
        lookup_by_fname[fname] = {"y": r.get("y", "0000"), "p": r.get("p", "Unknown")}

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json", encoding="utf-8") as f:
    meta = json.load(f)

# Merge: only overwrite y/p if currently unknown
updated = 0
for d in meta:
    fname = d["f"]
    if fname in lookup_by_fname:
        l = lookup_by_fname[fname]
        old_y = d.get("y","0000")
        old_p = (d.get("p") or "").strip()
        if old_y == "0000" and l["y"] not in ("0000", ""):
            d["y"] = l["y"]
            updated += 1
        if old_p.lower() in ("unknown","zlib","libgen","annaarchive","z-library","") and l["p"] not in ("Unknown",""):
            d["p"] = l["p"]
            updated += 1

print(f"Field updates: {updated}")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

# Now build canonical rename plan
def sanitise(s, maxlen=40):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", ""): return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

SRC_DIR = r"D:\History vs Hype\library\by-topic\territorial-disputes"
plan = []
for d in meta:
    f = d["f"]
    t = sanitise(d.get("t","Unknown"), 40)
    a = sanitise(d.get("a","Unknown"), 25)
    y = sanitise(d.get("y","0000"), 4)
    if y == "Unknown" or not re.match(r"^\d{4}$", y): y = "0000"
    p = sanitise(d.get("p","Unknown"), 30)
    ext = os.path.splitext(f)[1].lower()
    new_name = f"{t}-{a}-{y}-{p}{ext}"
    src = os.path.join(SRC_DIR, f)
    dst = os.path.join(SRC_DIR, new_name)
    try:
        size = os.path.getsize(src)
    except OSError:
        size = 0
    plan.append({"old": f, "new": new_name, "src": src, "dst": dst, "size": size})

# Group by dst for dedup
from collections import defaultdict
groups = defaultdict(list)
for p in plan:
    groups[p["dst"]].append(p)

dedup_winners = []
dedup_losers = []
for dst, ops in groups.items():
    if len(ops) == 1:
        dedup_winners.append(ops[0])
    else:
        # keep biggest
        winner = max(ops, key=lambda o: o["size"])
        dedup_winners.append(winner)
        for o in ops:
            if o is not winner:
                dedup_losers.append(o)

print(f"Rename plan: {len(plan)} ops -> {len(dedup_winners)} after dedup ({len(dedup_losers)} losers)")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\territorial-rename-plan.json", "w", encoding="utf-8") as f:
    json.dump({"winners": dedup_winners, "losers": dedup_losers}, f, indent=2, ensure_ascii=False)
print("Plan written.")
