"""Parse Gemini round 2 table from WEB-LOOKUP-PROMPT-ROUND2.md.

Rules:
- title == "OFF-TOPIC" AND author == "OFF-TOPIC" -> flag for stash
- title is real title -> rename (even if pub is OFF-TOPIC, treat pub as Unknown)
- title == "UNRESOLVED" -> skip
"""
import re, os, json, hashlib

MD2 = r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT-ROUND2.md"
MD1 = r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT.md"
ROOT = r"D:\History vs Hype\library\by-topic"

with open(MD2, encoding="utf-8") as f:
    md2 = f.read()
with open(MD1, encoding="utf-8") as f:
    md1 = f.read()

# Reuse round 1 reference map (idx -> folder, fname)
ref_pattern = re.compile(r'^\s*(\d+)\.\s+`library/by-topic/([^/]+)/(.+?)`\s*$', re.MULTILINE)
ref_map = {int(m.group(1)): (m.group(2), m.group(3)) for m in ref_pattern.finditer(md1)}
print(f"Ref map: {len(ref_map)}")

# Parse the round 2 results table
table_rows = re.findall(
    r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d{4}|N/A|n/a|UNRESOLVED|OFF-TOPIC)\s*\|\s*([^|]+?)\s*\|\s*[^|]*\|\s*$',
    md2, re.MULTILINE
)
print(f"Round 2 rows: {len(table_rows)}")

def sanitise(s, maxlen=40):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none","unknown","?","n/a","unresolved","off-topic"): return "Unknown"
    s = re.sub(r'\s*\([^)]*\)\s*', '', s)
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r"['']", "", s)
    s = re.sub(r'[\s_]+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

def to_camel_slug(title, maxlen=45):
    if not title or title.lower() in ("","unknown","n/a","unresolved","off-topic"): return None
    title = re.sub(r'^\s*(The|A|An)\s+', '', title, flags=re.I)
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^\]]*\]', '', title)
    words = re.findall(r'[A-Za-z0-9]+', title)
    if not words: return None
    out = ''.join(w[0].upper() + w[1:].lower() if len(w) > 1 else w.upper() for w in words)
    return out[:maxlen]

PUB_NORMALIZE = {
    "n/a":"Unknown","hmso":"HMSO","h.m.s.o.":"HMSO","mcgrawhill":"McGrawHill",
    "off-topic":"Unknown","unresolved":"Unknown",
}

stash_candidates = []
ops = []
skipped_unresolved = 0
errors = []

for idx_s, title, author, year, pub in table_rows:
    idx = int(idx_s)
    info = ref_map.get(idx)
    if not info: continue
    folder, old_name = info
    src = os.path.join(ROOT, folder, old_name)
    if not os.path.exists(src):
        continue
    title_clean = title.strip()
    author_clean = author.strip()
    pub_clean = pub.strip()

    title_off = title_clean.upper() == "OFF-TOPIC"
    title_unres = title_clean.upper() == "UNRESOLVED"
    author_off = author_clean.upper() == "OFF-TOPIC"

    # Pure off-topic: stash candidate
    if title_off and author_off:
        stash_candidates.append({"idx":idx,"folder":folder,"fname":old_name})
        continue
    # Title unresolved: nothing to apply
    if title_unres:
        skipped_unresolved += 1
        continue

    # Treat OFF-TOPIC title as "primary doc" with title from cell
    # Build new canonical
    new_t = to_camel_slug(title_clean, 45)
    if not new_t:
        # title is OFF-TOPIC/UNRESOLVED but author may be real
        skipped_unresolved += 1
        continue

    m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$', old_name)
    if not m:
        continue
    old_t, old_a, old_y, old_p, tail = m.groups()

    new_a = sanitise(author_clean, 25) if author_clean.upper() not in ("UNRESOLVED","OFF-TOPIC") else old_a
    new_y = year if re.match(r"^\d{4}$", year) else old_y
    pub_lc = pub_clean.lower()
    if pub_lc in PUB_NORMALIZE:
        norm = PUB_NORMALIZE[pub_lc]
        new_p = norm if norm != "Unknown" else old_p
    else:
        san = sanitise(pub_clean, 30)
        new_p = san if san != "Unknown" else old_p

    new_name = f"{new_t}-{new_a}-{new_y}-{new_p}{tail}"
    if new_name == old_name:
        continue
    dst = os.path.join(ROOT, folder, new_name)
    ops.append({"folder":folder,"old":old_name,"new":new_name,"src":src,"dst":dst,"idx":idx})

print(f"Rename ops:           {len(ops)}")
print(f"Stash candidates:     {len(stash_candidates)}")
print(f"Skipped UNRESOLVED:   {skipped_unresolved}")

# Apply renames
renamed = 0; dup_deleted = 0; disambig = 0
for op in ops:
    if not os.path.exists(op["src"]): continue
    if os.path.exists(op["dst"]):
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
            os.rename(op["src"], os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}"))
            disambig += 1; renamed += 1
        except OSError as e:
            errors.append(f"{op['old']}: {e}")
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(f"{op['old']}: {e}")

print(f"Renamed: {renamed}, Dup-deleted: {dup_deleted}, Disambig: {disambig}, Errors: {len(errors)}")

# Save stash candidates JSON
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\round2-stash-candidates.json", "w", encoding="utf-8") as f:
    json.dump(stash_candidates, f, indent=2, ensure_ascii=False)
print(f"\nStash candidates saved to round2-stash-candidates.json")
print("Sample:")
for s in stash_candidates[:10]:
    print(f"  [{s['folder']}] {s['fname']}")
