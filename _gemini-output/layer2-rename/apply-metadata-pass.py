"""Apply PDF metadata upgrades:
- All publisher, year, title upgrades (9 + 30 + 5)
- Author upgrades filtered to clean real-looking last names
"""
import json, os, re, hashlib

ROOT = r"D:\History vs Hype\library\by-topic"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\pdf-metadata-diff-v2.json", encoding="utf-8") as f:
    data = json.load(f)
diffs = data["diffs"]

# Author junk filter — reject these
AUTHOR_REJECT_EXACT = {"games","service","states","resources","group","admin","author",
                       "research","examination","palestine","tierra","windows",
                       "geography","games","blackwell","blackburn"}
AUTHOR_REJECT_PATTERNS = [
    re.compile(r'^[a-z]{1,3}$', re.I),   # too short / initials like "Lr"
    re.compile(r'\d'),                    # contains digits
    re.compile(r'^[A-Z]{4,}$'),           # all-caps acronyms
    re.compile(r'^dufp', re.I),
    re.compile(r'^unicaf', re.I),
    re.compile(r'^zmfr', re.I),
    re.compile(r'^eurospeak', re.I),
    re.compile(r'lap$', re.I),            # system handle suffix
]

def author_clean(a):
    if not a: return False
    a_low = a.lower()
    if a_low in AUTHOR_REJECT_EXACT: return False
    for pat in AUTHOR_REJECT_PATTERNS:
        if pat.search(a): return False
    return len(a) >= 4

# Title junk filter
def title_clean(t):
    if not t: return False
    # All-digits or near-digits is bad (e.g., "1892010118921231")
    if re.match(r'^\d{6,}$', t): return False
    if len(t) < 4: return False
    return True

def sanitise(s, maxlen=30):
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', str(s))
    s = re.sub(r"['']", "", s)
    s = re.sub(r'[\s_]+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    return s.strip('-')[:maxlen]

CANON_RE = re.compile(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$')

ops = []
filtered_authors = []
filtered_titles = []
for d in diffs:
    folder = d["folder"]; old_name = d["old"]
    src = os.path.join(ROOT, folder, old_name)
    if not os.path.exists(src): continue
    m = CANON_RE.match(old_name)
    if not m: continue
    old_t, old_a, old_y, old_p, tail = m.groups()
    new_t = old_t; new_a = old_a; new_y = old_y; new_p = old_p
    if d["new_t"]:
        if title_clean(d["new_t"]):
            new_t = sanitise(d["new_t"], 45)
        else:
            filtered_titles.append((folder, old_name, d["new_t"]))
    if d["new_a"]:
        if author_clean(d["new_a"]):
            new_a = sanitise(d["new_a"], 25)
        else:
            filtered_authors.append((folder, old_name, d["new_a"]))
    if d["new_y"]:
        new_y = d["new_y"]
    if d["new_p"]:
        new_p = sanitise(d["new_p"], 30)
    new_name = f"{new_t}-{new_a}-{new_y}-{new_p}{tail}"
    if new_name == old_name: continue
    ops.append({"folder":folder,"old":old_name,"new":new_name,
                "src":src,"dst":os.path.join(ROOT,folder,new_name)})

print(f"Rename ops:        {len(ops)}")
print(f"Filtered authors:  {len(filtered_authors)} (rejected as junk)")
for f, o, a in filtered_authors:
    print(f"  REJECTED a={a!r} for {o[:60]}")
print(f"Filtered titles:   {len(filtered_titles)}")
for f, o, t in filtered_titles:
    print(f"  REJECTED t={t!r} for {o[:60]}")

# Apply
renamed = 0; dup_del = 0; disamb = 0; errors = []
for op in ops:
    if not os.path.exists(op["src"]): continue
    if os.path.exists(op["dst"]):
        try:
            with open(op["src"],"rb") as fh: h1 = hashlib.md5(fh.read()).hexdigest()
            with open(op["dst"],"rb") as fh: h2 = hashlib.md5(fh.read()).hexdigest()
            if h1 == h2:
                os.remove(op["src"])
                dup_del += 1
                continue
            base, ext = os.path.splitext(op["new"])
            n = 2
            while os.path.exists(os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")):
                n += 1
            os.rename(op["src"], os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}"))
            disamb += 1; renamed += 1
        except OSError as e:
            errors.append(str(e))
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(str(e))

print(f"\nRenamed: {renamed}, Dedup: {dup_del}, Disambig: {disamb}, Errors: {len(errors)}")
for e in errors[:10]: print(f"  {e}")
