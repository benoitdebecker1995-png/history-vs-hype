"""Pass 1: Extract PDF metadata dict for all files. Output diff vs canonical name.
Pass 2 (apply): only run after diff is approved."""
import os, re, json
import fitz  # PyMuPDF
from collections import defaultdict

ROOT = r"D:\History vs Hype\library\by-topic"
OUT = r"D:\History vs Hype\_gemini-output\layer2-rename"

def normalize_year(s):
    if not s: return None
    m = re.search(r'(1[5-9]\d{2}|20\d{2})', str(s))
    return m.group(1) if m else None

def normalize_author(s):
    if not s: return None
    s = str(s).strip()
    if not s or s.lower() in ("unknown","none","null","n/a","anonymous","admin","user","author"): return None
    # If "Last, First" -> Last
    if "," in s:
        s = s.split(",")[0].strip()
    # If "First Middle Last" -> Last
    elif " " in s:
        s = s.split()[-1].strip()
    # Strip non-letter punctuation
    s = re.sub(r"[^\w'-]", "", s)
    if len(s) < 2 or len(s) > 25: return None
    return s.capitalize()

# Publisher detection from Producer/Creator strings
PUB_HINTS = {
    "cambridge": "CambridgeUP", "cup": "CambridgeUP",
    "oxford university press": "OxfordUP", "oup": "OxfordUP",
    "yale university press": "YaleUP", "princeton university press": "PrincetonUP",
    "columbia university press": "ColumbiaUP", "harvard university press": "HarvardUP",
    "cornell university press": "CornellUP", "stanford university press": "StanfordUP",
    "edinburgh university press": "EdinburghUP", "indiana university press": "IndianaUP",
    "nyu press": "NYUPress", "uc press": "UCPress",
    "johns hopkins": "JohnsHopkinsUP", "duke university press": "DukeUP",
    "syracuse university press": "SyracuseUP", "chicago press": "ChicagoUP",
    "routledge": "Routledge", "taylor & francis": "Routledge", "tandfonline": "Routledge",
    "palgrave": "Palgrave", "springer": "Springer", "wiley": "WileyBlackwell",
    "sage": "SAGEPub", "brill": "Brill", "verso": "VersoBooks", "pluto": "PlutoPress",
    "zed books": "ZedBooks", "i.b. tauris": "ITauris", "i.b.tauris": "ITauris",
    "bloomsbury": "Bloomsbury", "hurst": "HurstCo", "penguin": "Penguin",
    "random house": "RandomHouse", "basic books": "BasicBooks", "norton": "NortonCo",
    "weidenfeld": "WeidenfeldNicolson", "macmillan": "MacmillanUK", "free press": "FreePress",
    "granta": "Granta", "da capo": "DaCapo", "mit press": "MITPress",
    "elsevier": "Elsevier", "jstor": "JSTOR", "doi.org": None, "redalyc": "Redalyc",
}
def detect_publisher(meta):
    blob = " ".join(filter(None, [meta.get("producer",""), meta.get("creator",""), meta.get("subject","")])).lower()
    for hint, pub in PUB_HINTS.items():
        if hint in blob:
            return pub
    return None

def short_title_slug(title, maxlen=45):
    if not title: return None
    t = str(title).strip()
    if not t or t.lower() in ("unknown","none","null","untitled"): return None
    t = re.sub(r'^\s*(The|A|An)\s+', '', t, flags=re.I)
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'\[[^\]]*\]', '', t)
    words = re.findall(r'[A-Za-z0-9]+', t)
    if not words or len(words) < 2: return None  # require at least 2 words to be useful
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

        new_t_slug = short_title_slug(md.get("title")) if md.get("title") else None
        new_a = normalize_author(md.get("author"))
        new_y = normalize_year(md.get("creationDate") or md.get("modDate") or md.get("title"))
        new_p = detect_publisher(md)

        # Determine what's upgrade-able (current is Unknown/0000 AND metadata has real value)
        upgrade_t = (old_t.lower() in ("unknown",) and new_t_slug)
        upgrade_a = (old_a.lower() in ("unknown",) and new_a)
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
                "raw_creator": md.get("creator",""),
                "raw_producer": md.get("producer",""),
            })
            if upgrade_t: stats["upgrade_title"] += 1
            if upgrade_a: stats["upgrade_author"] += 1
            if upgrade_y: stats["upgrade_year"] += 1
            if upgrade_p: stats["upgrade_pub"] += 1
        else:
            stats["no_upgrade"] += 1

with open(os.path.join(OUT, "pdf-metadata-diff.json"), "w", encoding="utf-8") as f:
    json.dump({"diffs": diffs, "stats": dict(stats), "errors": errors}, f, indent=2, ensure_ascii=False)

print(f"=== PDF Metadata Pass — Diff Summary ===")
print(f"Total scanned:    {stats['total']}")
print(f"With upgrades:    {len(diffs)}")
print(f"  Title upgrades: {stats['upgrade_title']}")
print(f"  Author upgrades:{stats['upgrade_author']}")
print(f"  Year upgrades:  {stats['upgrade_year']}")
print(f"  Pub upgrades:   {stats['upgrade_pub']}")
print(f"No upgrade:       {stats['no_upgrade']}")
print(f"Errors:           {len(errors)}")
print()
print("=== Sample diffs (first 20) ===")
for d in diffs[:20]:
    upgrades = []
    if d['new_t']: upgrades.append(f"t={d['old_t'][:25]}→{d['new_t'][:30]}")
    if d['new_a']: upgrades.append(f"a={d['old_a']}→{d['new_a']}")
    if d['new_y']: upgrades.append(f"y={d['old_y']}→{d['new_y']}")
    if d['new_p']: upgrades.append(f"p={d['old_p'][:10]}→{d['new_p']}")
    print(f"  [{d['folder']}] {d['old'][:50]}")
    print(f"    {' | '.join(upgrades)}")
    print(f"    raw_title={d['raw_title'][:80]!r}")
