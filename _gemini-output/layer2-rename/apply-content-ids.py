"""Apply Gemini content-id results to rename files."""
import re, json, os, hashlib
from collections import defaultdict

raw = open(r"D:\History vs Hype\_gemini-output\layer2-rename\content-id-output.raw.txt", encoding="utf-8").read()
m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw, re.DOTALL)
if not m:
    m = re.search(r"(\[\s*\{.*\}\s*\])", raw, re.DOTALL)
if not m: raise SystemExit("NO JSON")
data = json.loads(m.group(1))
print(f"Content-id entries: {len(data)}")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\content-id-idxmap.json", encoding="utf-8") as f:
    idxmap = json.load(f)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\unknown-pdf-extracts.json", encoding="utf-8") as f:
    extracts = json.load(f)
folder_lookup = {e["f"]: e["folder"] for e in extracts}

def sanitise(s, maxlen=45):
    if s is None: return "Unknown"
    s = str(s).strip()
    if not s or s.lower() in ("none", "unknown", "?", ""): return "Unknown"
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:maxlen].strip('-') or "Unknown"

ROOT = r"D:\History vs Hype\library\by-topic"

high_conf_plan = []
medium_conf_plan = []
low_conf = []

for d in data:
    f_orig = idxmap.get(str(d["i"]))
    if not f_orig: continue
    folder = folder_lookup.get(f_orig)
    if not folder: continue
    src = os.path.join(ROOT, folder, f_orig)
    if not os.path.exists(src):
        continue
    conf = d.get("confidence", "low").lower()
    t = sanitise(d.get("t","Unknown"), 45)
    a = sanitise(d.get("a","Unknown"), 25)
    y = (d.get("y","0000") or "0000").strip()
    if not re.match(r"^\d{4}$", y): y = "0000"
    p = sanitise(d.get("p","Unknown"), 30)
    if t == "Unknown" and a == "Unknown":
        low_conf.append({"folder":folder,"old":f_orig,"reason":"all unknown"})
        continue
    ext = os.path.splitext(f_orig)[1].lower()
    new_name = f"{t}-{a}-{y}-{p}{ext}"
    dst = os.path.join(ROOT, folder, new_name)
    op = {"folder":folder,"old":f_orig,"new":new_name,"src":src,"dst":dst,"conf":conf}
    if conf == "high":
        high_conf_plan.append(op)
    elif conf == "medium":
        medium_conf_plan.append(op)
    else:
        low_conf.append({"folder":folder,"old":f_orig,"reason":f"conf=low → {new_name}"})

print(f"High conf: {len(high_conf_plan)}")
print(f"Medium conf: {len(medium_conf_plan)}")
print(f"Low conf / skipped: {len(low_conf)}")

# Execute high + medium (medium files at least improve over Unknown-Unknown)
renamed = 0
dup_deleted = 0
errors = []
for op in high_conf_plan + medium_conf_plan:
    if os.path.normcase(op["src"]) == os.path.normcase(op["dst"]):
        continue
    if not os.path.exists(op["src"]):
        continue
    if os.path.exists(op["dst"]):
        # hash compare
        try:
            with open(op["src"],"rb") as f: h1 = hashlib.md5(f.read()).hexdigest()
            with open(op["dst"],"rb") as f: h2 = hashlib.md5(f.read()).hexdigest()
            if h1 == h2:
                os.remove(op["src"])
                dup_deleted += 1
                continue
            # disambig
            base, ext = os.path.splitext(op["new"])
            n = 2
            while os.path.exists(os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")):
                n += 1
            op["dst"] = os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")
            os.rename(op["src"], op["dst"])
            renamed += 1
        except OSError as e:
            errors.append(f"{op['old']}: {e}")
        continue
    try:
        os.rename(op["src"], op["dst"])
        renamed += 1
    except OSError as e:
        errors.append(f"{op['old']}: {e}")

report = [
    "=== Content-ID Rename Report (2026-05-12) ===",
    f"Gemini identified: {len(data)}",
    f"High confidence:   {len(high_conf_plan)}",
    f"Medium confidence: {len(medium_conf_plan)}",
    f"Low / unresolved:  {len(low_conf)}",
    "",
    f"Renamed: {renamed}",
    f"Hash-dedup deleted: {dup_deleted}",
    f"Errors: {len(errors)}",
    "",
    "Low confidence files (still need user review):",
    *[f"  [{e['folder']}] {e['old']}  -- {e['reason']}" for e in low_conf[:30]],
]
report_text = "\n".join(report)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\content-id-report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)
print()
print(report_text)
