import re, json, os
from collections import defaultdict

# Load merged meta
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\meta-territorial-disputes-v2.json", encoding="utf-8") as f:
    meta = json.load(f)

def sanitise(s, maxlen=40):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", ""): return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

# ICJ filename pattern: 094-20021010-JUD-01-00-EN.pdf
# 185-20221116-APP-01-00-EN.pdf  185-20231211-pre-01-00-en.pdf  185-20260319-ord-01-00-en.pdf
ICJ_RE = re.compile(r'^(\d{3})-(\d{8})-(JUD|APP|pre|ord|PRE|ORD|jud|app)-(\d{2})-(\d{2})-(EN|en)\.pdf$', re.IGNORECASE)

def icj_descriptor(f):
    m = ICJ_RE.match(f)
    if not m: return None
    case, date, doctype, p1, p2, lang = m.groups()
    doctype = doctype.upper()
    case_map = {
        "094": "CameroonNigeria",
        "185": "GuyanaVenezuela",
    }
    case_name = case_map.get(case, f"Case{case}")
    doc_name = {"JUD":"Judgment","APP":"Application","PRE":"Order","ORD":"Order"}.get(doctype, doctype)
    # include document number suffix to distinguish multiple docs from same case+date
    return f"{case_name}{doc_name}-{p1}{p2}"

SRC_DIR = r"D:\History vs Hype\library\by-topic\territorial-disputes"
plan = []
for d in meta:
    f = d["f"]
    # Override title for ICJ docs with full descriptor
    icj_t = icj_descriptor(f)
    if icj_t:
        t_raw = icj_t
        d["a"] = "ICJ"; d["p"] = "ICJ"
        m = ICJ_RE.match(f)
        d["y"] = m.group(2)[:4]
    else:
        t_raw = d.get("t","Unknown")
    t = sanitise(t_raw, 45)
    a = sanitise(d.get("a","Unknown"), 25)
    y = (d.get("y","0000") or "0000").strip()
    if not re.match(r"^\d{4}$", y): y = "0000"
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

# Collision handling: group by dst, keep all but disambiguate
groups = defaultdict(list)
for p_op in plan:
    groups[p_op["dst"]].append(p_op)

final_winners = []
true_dupes_to_delete = []
disambiguated = []
for dst, ops in groups.items():
    if len(ops) == 1:
        final_winners.append(ops[0])
        continue
    # Sort by size desc
    ops_sorted = sorted(ops, key=lambda o: -o["size"])
    biggest = ops_sorted[0]
    # Within 5% of biggest = treated as duplicate of biggest
    dupes = []
    distinct = [biggest]
    for o in ops_sorted[1:]:
        if biggest["size"] > 0 and abs(o["size"] - biggest["size"]) / biggest["size"] < 0.05:
            dupes.append(o)
        else:
            distinct.append(o)
    # Winner = biggest, gets canonical name
    final_winners.append(biggest)
    true_dupes_to_delete.extend(dupes)
    # Other distinct copies: append size-based suffix to disambiguate
    for i, o in enumerate(distinct[1:], 1):
        base, ext = os.path.splitext(o["new"])
        # add -v2 / -v3 suffix
        suffix = f"-v{i+1}"
        new_name = f"{base}{suffix}{ext}"
        o["new"] = new_name
        o["dst"] = os.path.join(SRC_DIR, new_name)
        final_winners.append(o)
        disambiguated.append(o)

print(f"Total ops: {len(plan)}")
print(f"Winners (rename): {len(final_winners)}")
print(f"True duplicates (delete): {len(true_dupes_to_delete)}")
print(f"Disambiguated with -vN: {len(disambiguated)}")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\territorial-rename-plan.json", "w", encoding="utf-8") as f:
    json.dump({
        "winners": final_winners,
        "duplicates_to_delete": true_dupes_to_delete,
        "disambiguated": disambiguated,
    }, f, indent=2, ensure_ascii=False)
print("Plan v2 written.")
