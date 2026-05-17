"""PDF metadata pass v2 — tightened filters.

Fixes:
- Publisher detection uses word boundaries (no 'oup' in 'Group')
- Author filter excludes user's Windows username (Benoit De Becker variants)
- Year filter: skip recent dates (>= 2018 unless year is clearly publication date)
"""
import os, re, json
import fitz
from collections import defaultdict

ROOT = r"D:\History vs Hype\library\by-topic"
OUT = r"D:\History vs Hype\_gemini-output\layer2-rename"

# User's name contamination patterns
USER_NAME_BLOCKLIST = {"becker", "benoit", "debecker", "de becker", "benoit de becker", "benoitdebecker"}

# Generic/junk author values
JUNK_AUTHORS = {"unknown","none","null","n/a","anonymous","admin","user","author","research",
                "owner","windows user","microsoft office user","temp","temporary","guest"}

def normalize_year(s, max_publication_year=2016):
    """Extract year. Return None if year > max_publication_year (likely scan date, not pub date)."""
    if not s: return None
    m = re.search(r'(1[5-9]\d{2}|20\d{2})', str(s))
    if not m: return None
    y = int(m.group(1))
    if y > max_publication_year: return None  # Suspect scan/save date
    return str(y)

def normalize_author(s):
    if not s: return None
    s = str(s).strip()
    if not s: return None
    s_low = s.lower()
    if s_low in JUNK_AUTHORS: return None
    # Check user name contamination
    for blocked in USER_NAME_BLOCKLIST:
        if blocked in s_low: return None
    # Handle "Last, First" -> Last
    if "," in s:
        last = s.split(",")[0].strip()
    elif " " in s:
        last = s.split()[-1].strip()
    else:
        last = s
    last = re.sub(r"[^\w'-]", "", last)
    if len(last) < 2 or len(last) > 25: return None
    last_low = last.lower()
    if last_low in JUNK_AUTHORS: return None
    for blocked in USER_NAME_BLOCKLIST:
        if blocked == last_low: return None
    return last.capitalize()

# Publisher hints — match as words/phrases with word boundaries
# Format: (regex_pattern, abbreviation)
PUB_PATTERNS = [
    (r'\bcambridge\s+university\s+press\b', "CambridgeUP"),
    (r'\bcambridge\s+up\b', "CambridgeUP"),
    (r'\boxford\s+university\s+press\b', "OxfordUP"),
    (r'\byale\s+university\s+press\b', "YaleUP"),
    (r'\bprinceton\s+university\s+press\b', "PrincetonUP"),
    (r'\bcolumbia\s+university\s+press\b', "ColumbiaUP"),
    (r'\bharvard\s+university\s+press\b', "HarvardUP"),
    (r'\bcornell\s+university\s+press\b', "CornellUP"),
    (r'\bstanford\s+university\s+press\b', "StanfordUP"),
    (r'\bedinburgh\s+university\s+press\b', "EdinburghUP"),
    (r'\bindiana\s+university\s+press\b', "IndianaUP"),
    (r'\bnyu\s+press\b', "NYUPress"),
    (r'\bnew\s+york\s+university\s+press\b', "NYUPress"),
    (r'\buniversity\s+of\s+california\s+press\b', "UCPress"),
    (r'\bjohns\s+hopkins\b', "JohnsHopkinsUP"),
    (r'\bduke\s+university\s+press\b', "DukeUP"),
    (r'\bsyracuse\s+university\s+press\b', "SyracuseUP"),
    (r'\bunc\s+press\b|\buniversity\s+of\s+north\s+carolina\s+press\b', "UNCPress"),
    (r'\buniversity\s+of\s+chicago\s+press\b', "ChicagoUP"),
    (r'\broutledge\b', "Routledge"),
    (r'\btaylor\s+&\s+francis\b|\btandfonline\b', "Routledge"),
    (r'\bpalgrave\b', "Palgrave"),
    (r'\bspringer\b', "Springer"),
    (r'\bwiley\b', "WileyBlackwell"),
    (r'\bsage\s+publications\b|\bsage\s+pub\b', "SAGEPub"),
    (r'\bbrill\b', "Brill"),
    (r'\bverso\s+books\b|\bverso\b(?=\W*$)', "VersoBooks"),
    (r'\bpluto\s+press\b', "PlutoPress"),
    (r'\bzed\s+books\b', "ZedBooks"),
    (r'\bi\.?b\.?\s*tauris\b', "ITauris"),
    (r'\bbloomsbury\b', "Bloomsbury"),
    (r'\bhurst\s+(co|publishers)\b', "HurstCo"),
    (r'\bpenguin\b', "Penguin"),
    (r'\brandom\s+house\b', "RandomHouse"),
    (r'\bbasic\s+books\b', "BasicBooks"),
    (r'\bnorton\b', "NortonCo"),
    (r'\bweidenfeld\b', "WeidenfeldNicolson"),
    (r'\bmacmillan\b', "MacmillanUK"),
    (r'\bda\s+capo\b', "DaCapo"),
    (r'\bmit\s+press\b', "MITPress"),
    (r'\belsevier\b', "Elsevier"),
    (r'\bjstor\b', "JSTOR"),
    (r'\bredalyc\b', "Redalyc"),
]

def detect_publisher(meta):
    blob = " ".join(filter(None, [
        meta.get("producer",""), meta.get("creator",""),
        meta.get("subject",""), meta.get("keywords","")
    ])).lower()
    for pattern, pub in PUB_PATTERNS:
        if re.search(pattern, blob):
            return pub
    return None

def short_title_slug(title, maxlen=45):
    if not title: return None
    t = str(title).strip()
    if not t or t.lower() in ("unknown","none","null","untitled","x"): return None
    # Reject titles that are file system fragments
    if t.startswith("Microsoft Word") or t.startswith("untitled"): return None
    if t.lower().endswith(".pdf"): return None
    t = re.sub(r'^\s*(The|A|An)\s+', '', t, flags=re.I)
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'\[[^\]]*\]', '', t)
    t = re.sub(r'<[^>]*>', '', t)  # strip HTML
    words = re.findall(r'[A-Za-z0-9]+', t)
    if len(words) < 2: return None
    out = ''.join(w[0].upper() + w[1:].lower() if len(w) > 1 else w.upper() for w in words)
    return out[:maxlen]

CANON_RE = re.compile(r'^(.+?)-(.+?)-(\d{4})-(.+?)((?:-v\d+)?\.[a-z0-9]+)$')

diffs = []
errors = []
stats = defaultdict(int)

for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p): continue
    for fname in os.listdir(p):
        full = os.path.join(p, fname)
        if not os.path.isfile(full) or not fname.lower().endswith(".pdf"): continue
        m = CANON_RE.match(fname)
        if not m: continue
        old_t, old_a, old_y, old_p, tail = m.groups()
        try:
            doc = fitz.open(full)
            md = doc.metadata or {}
            doc.close()
        except Exception as e:
            errors.append(f"{folder}/{fname}: {e}")
            continue
        stats["total"] += 1

        new_t_slug = short_title_slug(md.get("title"))
        new_a = normalize_author(md.get("author"))
        new_y = normalize_year(md.get("creationDate"))
        new_p = detect_publisher(md)

        upgrade_t = (old_t.lower() == "unknown" and new_t_slug)
        upgrade_a = (old_a.lower() == "unknown" and new_a)
        upgrade_y = (old_y == "0000" and new_y)
        upgrade_p = (old_p.lower() in ("unknown","zlib","libgen","annaarchive","z-library") and new_p)

        if upgrade_t or upgrade_a or upgrade_y or upgrade_p:
            diffs.append({
                "folder": folder, "old": fname,
                "old_t": old_t, "old_a": old_a, "old_y": old_y, "old_p": old_p,
                "new_t": new_t_slug if upgrade_t else None,
                "new_a": new_a if upgrade_a else None,
                "new_y": new_y if upgrade_y else None,
                "new_p": new_p if upgrade_p else None,
                "raw_title": md.get("title",""),
                "raw_author": md.get("author",""),
                "raw_producer": md.get("producer",""),
            })
            if upgrade_t: stats["upgrade_title"] += 1
            if upgrade_a: stats["upgrade_author"] += 1
            if upgrade_y: stats["upgrade_year"] += 1
            if upgrade_p: stats["upgrade_pub"] += 1
        else:
            stats["no_upgrade"] += 1

with open(os.path.join(OUT, "pdf-metadata-diff-v2.json"), "w", encoding="utf-8") as f:
    json.dump({"diffs": diffs, "stats": dict(stats), "errors": errors}, f, indent=2, ensure_ascii=False)

print(f"=== PDF Metadata Pass v2 — Tightened ===")
print(f"Total scanned:    {stats['total']}")
print(f"With upgrades:    {len(diffs)}")
print(f"  Title:    {stats['upgrade_title']}")
print(f"  Author:   {stats['upgrade_author']}")
print(f"  Year:     {stats['upgrade_year']} (only years ≤ 2016)")
print(f"  Pub:      {stats['upgrade_pub']}")
print(f"No upgrade:       {stats['no_upgrade']}")
print(f"Errors:           {len(errors)}")
print()
print("=== Sample diffs (first 25) ===")
for d in diffs[:25]:
    upgrades = []
    if d['new_t']: upgrades.append(f"t→{d['new_t'][:30]}")
    if d['new_a']: upgrades.append(f"a→{d['new_a']}")
    if d['new_y']: upgrades.append(f"y→{d['new_y']}")
    if d['new_p']: upgrades.append(f"p→{d['new_p']}")
    print(f"  [{d['folder']}] {d['old'][:55]}")
    print(f"    {' | '.join(upgrades)}")
    rt = d.get('raw_title','')[:70]
    if rt: print(f"    raw_title={rt!r}")
