"""Parse Gemini's web-lookup table from WEB-LOOKUP-PROMPT.md and apply renames."""
import re, os, json, hashlib

MD_PATH = r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT.md"
ROOT = r"D:\History vs Hype\library\by-topic"

with open(MD_PATH, encoding="utf-8") as f:
    md = f.read()

# Re-derive the index mapping from the prompt section.
# The prompt lists entries like: "N. [folder] title_slug | a=... | y=... | p=..."
# AND the "Reference: original filenames" section lists "N. `library/by-topic/folder/filename`"
# Use the reference section because it has exact filenames.

ref_pattern = re.compile(r'^\s*(\d+)\.\s+`library/by-topic/([^/]+)/(.+?)`\s*$', re.MULTILINE)
ref_map = {}
for m in ref_pattern.finditer(md):
    idx = int(m.group(1))
    folder = m.group(2)
    fname = m.group(3)
    ref_map[idx] = (folder, fname)
print(f"Reference map: {len(ref_map)} entries")

# Parse the Gemini result table
# Format: | file_index | title_slug (verified) | author_surname | year | publisher_abbrev | source_url |
table_rows = re.findall(
    r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d{4}|N/A|n/a)\s*\|\s*([^|]+?)\s*\|\s*[^|]*\|\s*$',
    md, re.MULTILINE
)
print(f"Table rows parsed: {len(table_rows)}")

# Build rename plan
def sanitise(s, maxlen=40):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", "n/a", "n/a (treaty)", "n/a (forgery)"): return "Unknown"
    # Remove parenthetical disambiguators
    s = re.sub(r'\s*\([^)]*\)\s*', '', s)
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'[\s_]+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

def to_camel_slug(title, maxlen=45):
    """Convert 'A Modern History of the Somali' -> 'ModernHistoryOfSomali'."""
    if not title or title.lower() in ("unknown","n/a"): return "Unknown"
    title = re.sub(r'^\s*(The|A|An)\s+', '', title, flags=re.I)
    # Strip parentheticals and bracketed text
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^\]]*\]', '', title)
    # Keep alphanumerics, split on non-alphanumerics
    words = re.findall(r'[A-Za-z0-9]+', title)
    if not words: return "Unknown"
    out = ''.join(w[0].upper() + w[1:].lower() if len(w) > 1 else w.upper() for w in words)
    return out[:maxlen]

PUB_MAP = {
    "n/a": "Unknown",
    "h.m.s.o.": "HMSO",
    "mcgrawhill": "McGrawHill",
}

ops = []
unresolved_in_table = []
for idx_s, title, author, year, pub in table_rows:
    idx = int(idx_s)
    info = ref_map.get(idx)
    if not info:
        unresolved_in_table.append((idx, "NO REF MAP"))
        continue
    folder, old_name = info
    src = os.path.join(ROOT, folder, old_name)
    if not os.path.exists(src):
        unresolved_in_table.append((idx, f"FILE GONE: {old_name}"))
        continue
    # Parse current canonical name
    m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$', old_name)
    if not m:
        unresolved_in_table.append((idx, f"NO CANON MATCH: {old_name}"))
        continue
    old_t, old_a, old_y, old_p, tail = m.groups()
    # New fields
    new_t = to_camel_slug(title, 45) if title.strip().lower() not in ("","unresolved") else old_t
    new_a = sanitise(author, 25)
    new_y = year if re.match(r"^\d{4}$", year) else old_y
    pub_l = pub.strip().lower()
    new_p = PUB_MAP.get(pub_l, sanitise(pub, 30))
    if new_p == "Unknown" and old_p != "Unknown":
        new_p = old_p  # don't downgrade

    new_name = f"{new_t}-{new_a}-{new_y}-{new_p}{tail}"
    if new_name == old_name:
        continue
    dst = os.path.join(ROOT, folder, new_name)
    ops.append({"folder":folder,"old":old_name,"new":new_name,"src":src,"dst":dst,"idx":idx})

print(f"Rename ops: {len(ops)}")

renamed = 0; dup_deleted = 0; disambig = 0; errors = []
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
            disambig += 1
            renamed += 1
        except OSError as e:
            errors.append(f"{op['old']}: {e}")
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(f"{op['old']}: {e}")

print(f"Renamed: {renamed}, Dup-deleted: {dup_deleted}, Disambig: {disambig}, Errors: {len(errors)}")
for e in errors[:10]: print(f"  {e}")

# Sample 10 renames
print("\n=== Sample renames ===")
for op in ops[:10]:
    print(f"  [{op['folder']}] {op['old'][:50]} -> {op['new']}")
