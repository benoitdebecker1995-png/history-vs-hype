"""Apply year+publisher lookup results."""
import json, os, re, hashlib

ROOT = r"D:\History vs Hype\library\by-topic"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\year-lookup-output.json", encoding="utf-8") as f:
    results = json.load(f)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\year-lookup-idxmap.json", encoding="utf-8") as f:
    idxmap = json.load(f)

def sanitise(s, maxlen=30):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s: return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

ops = []
for r in results:
    info = idxmap.get(str(r["i"]))
    if not info: continue
    new_y = (r.get("y","0000") or "0000").strip()
    new_p_raw = r.get("p","Unknown") or "Unknown"
    if not re.match(r"^\d{4}$", new_y) and new_p_raw == "Unknown":
        continue
    if not re.match(r"^\d{4}$", new_y): new_y = "0000"
    folder = info["folder"]
    old_name = info["f"]
    src = os.path.join(ROOT, folder, old_name)
    if not os.path.exists(src): continue
    m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$', old_name)
    if not m: continue
    t, a, y, old_pub, tail = m.groups()
    # Update year only if currently 0000
    use_y = new_y if y == "0000" and new_y != "0000" else y
    # Update pub only if currently Unknown-ish
    use_p = old_pub
    if old_pub.lower() in ("unknown","zlib","libgen","annaarchive") and new_p_raw not in ("Unknown",""):
        use_p = sanitise(new_p_raw, 30)
    new_name = f"{t}-{a}-{use_y}-{use_p}{tail}"
    if new_name == old_name: continue
    dst = os.path.join(ROOT, folder, new_name)
    ops.append({"folder":folder,"old":old_name,"new":new_name,"src":src,"dst":dst})

print(f"Rename ops: {len(ops)}")

renamed = 0; dup_deleted = 0; disambiguated = 0; errors = []
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
            disambiguated += 1
            renamed += 1
        except OSError as e:
            errors.append(str(e))
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(str(e))

print(f"Renamed: {renamed}, Dup-deleted: {dup_deleted}, Disambiguated: {disambiguated}, Errors: {len(errors)}")
