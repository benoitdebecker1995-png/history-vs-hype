"""Audit Step 2: Three analyses on the inventory.

A) Publisher slug clustering — build canonical map
B) Duplicate detection — by (author, year, title overlap)
C) Truncation candidates — titles likely cut mid-word
"""
import os, re, json
from collections import defaultdict, Counter

INV = r"D:\History vs Hype\_gemini-output\layer2-rename\library-inventory.json"
records = json.load(open(INV, encoding="utf-8"))["records"]

# ============================================================
# A) PUBLISHER SLUG CANONICALIZATION
# ============================================================
# Group raw slugs by normalized form: lowercase + strip dashes + strip "press"/"books"/"university"/"UP"
def normalize_pub(slug: str) -> str:
    s = slug.lower().replace("-", "").replace("_", "")
    # strip trailing "press"/"books"/"co"/"inc"
    s = re.sub(r'(press|books|booksinc|co|inc|publishers|publishing|publications|edition|editions)$', '', s)
    # strip "universityof", "universite", "univ" prefixes/suffixes
    s = s.replace("universityof", "")
    s = re.sub(r'universit[eya]?$', '', s)
    s = s.replace("university", "")
    s = re.sub(r'up$', '', s)
    return s.strip()

pub_clusters = defaultdict(list)
for r in records:
    key = normalize_pub(r["publisher"])
    if key:
        pub_clusters[key].append(r["publisher"])

# Pick canonical: most-frequent slug per cluster, unless we have a hand-fixed override
# Hand overrides for clean-form canonical slugs:
CANONICAL_OVERRIDES = {
    "oxford": "OxfordUP",
    "cambridge": "CambridgeUP",
    "princeton": "PrincetonUP",
    "yale": "YaleUP",
    "harvard": "HarvardUP",
    "stanford": "StanfordUP",
    "cornell": "CornellUP",
    "columbia": "ColumbiaUP",
    "chicago": "ChicagoUP",
    "berkeley": "BerkeleyUP",
    "michigan": "MichiganUP",
    "nyu": "NYU",
    "newyork": "NYUP",
    "pennsylvania": "PennUP",
    "edinburgh": "EdinburghUP",
    "manchester": "ManchesterUP",
    "rutgers": "RutgersUP",
    "indiana": "IndianaUP",
    "minnesota": "MinnesotaUP",
    "californialosangeles": "UCLAUP",
    "california": "UCalifUP",
    "wisconsin": "WisconsinUP",
    "northcarolina": "UNCUP",
    "georgia": "GeorgiaUP",
    "syracuse": "SyracuseUP",
    "liverpool": "LiverpoolUP",
    "routledge": "Routledge",
    "palgrave": "Palgrave",
    "palgravemacmillan": "Palgrave",
    "macmillan": "Macmillan",
    "wiley": "Wiley",
    "wileyblackwell": "WileyBlackwell",
    "johnwiley": "Wiley",
    "johnwiley&sons": "Wiley",
    "blackwell": "Blackwell",
    "springer": "Springer",
    "brill": "Brill",
    "verso": "Verso",
    "penguin": "Penguin",
    "vintage": "Vintage",
    "randomhouse": "RandomHouse",
    "simon&schuster": "SimonSchuster",
    "simonschuster": "SimonSchuster",
    "harpercollins": "HarperCollins",
    "norton": "Norton",
    "wwnorton": "Norton",
    "ww": "Norton",
    "basic": "Basic",
    "basicbooks": "Basic",
    "bloomsbury": "Bloomsbury",
    "duke": "DukeUP",
    "polity": "Polity",
    "polityress": "Polity",
    "hurst": "Hurst",
    "icj": "ICJ",
    "internationalcourtofjustice": "ICJ",
    "un": "UN",
    "unitednations": "UN",
    "zlib": "ZLib",
    "zlibrary": "ZLib",
    "annaarchive": "AnnaArchive",
    "libgen": "Libgen",
    "annasarchive": "AnnaArchive",
    "unknown": "Unknown",
    "": "Unknown",
}

canonical_map = {}  # raw_slug -> canonical_slug
for raw_slug in set(r["publisher"] for r in records):
    key = normalize_pub(raw_slug)
    if key in CANONICAL_OVERRIDES:
        canonical_map[raw_slug] = CANONICAL_OVERRIDES[key]
    else:
        # pick most common form in this cluster; or itself
        cluster = pub_clusters.get(key, [raw_slug])
        cnt = Counter(cluster)
        # prefer shorter form when tied
        canonical_map[raw_slug] = sorted(cnt.most_common(), key=lambda x: (-x[1], len(x[0])))[0][0]

# Identify which raw slugs need renaming
slug_renames = {raw: canon for raw, canon in canonical_map.items() if raw != canon}

# Files needing slug rename
pub_rename_files = []
for r in records:
    if r["publisher"] in slug_renames:
        new_pub = slug_renames[r["publisher"]]
        new_name = f"{r['title']}-{r['author']}-{r['year']}-{new_pub}.{r['ext']}"
        pub_rename_files.append({
            "folder": r["folder"],
            "old": r["filename"],
            "new": new_name,
            "old_pub": r["publisher"],
            "new_pub": new_pub,
        })

# ============================================================
# B) DUPLICATE DETECTION
# ============================================================
# Group by (author_lower, year). Within group, cluster by title 3-word-overlap.
def title_words(t: str):
    # Split CamelCase into words
    parts = re.findall(r'[A-Z][a-z]*|[0-9]+', t)
    parts = [p.lower() for p in parts if len(p) >= 3]
    return set(parts)

groups = defaultdict(list)
for r in records:
    key = (r["author"].lower(), r["year"], r["ext"])  # include ext: pdf vs epub kept separate
    if r["author"].lower() in ("unknown", ""):
        continue  # skip Unknown author dupe detection — too noisy
    groups[key].append(r)

dupe_clusters = []
for (author, year, ext), members in groups.items():
    if len(members) < 2:
        continue
    # Within group, cluster by word overlap
    clusters = []
    for m in members:
        m_words = title_words(m["title"])
        placed = False
        for cluster in clusters:
            for cm in cluster:
                cm_words = title_words(cm["title"])
                shared = m_words & cm_words
                if len(shared) >= 3 or (len(m_words) >= 2 and m_words.issubset(cm_words)) or (len(cm_words) >= 2 and cm_words.issubset(m_words)):
                    cluster.append(m)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            clusters.append([m])
    for c in clusters:
        if len(c) >= 2:
            dupe_clusters.append({
                "author": author, "year": year,
                "members": c,
            })

# ============================================================
# C) TRUNCATION CANDIDATES
# ============================================================
# Title len >= 40 AND ends with suspicious cut: 1-2 lowercase letters OR ends in syllable boundary
truncation_candidates = []
for r in records:
    t = r["title"]
    if len(t) < 38:
        continue
    # Get last "word" (run of letters before end)
    # CamelCase: split into words
    parts = re.findall(r'[A-Z][a-z]*|[0-9]+', t)
    if not parts:
        continue
    last = parts[-1]
    # Suspicious: last word is 1-2 letters (cut mid-word) OR a single capital
    if 1 <= len(last) <= 2 and last[0].isupper():
        truncation_candidates.append({"file": f"{r['folder']}/{r['filename']}", "title": t, "last_word": last})
    elif len(last) <= 4 and not last[0].isupper():
        truncation_candidates.append({"file": f"{r['folder']}/{r['filename']}", "title": t, "last_word": last})

# ============================================================
# WRITE OUTPUTS
# ============================================================
OUT_DIR = r"D:\History vs Hype\_gemini-output\layer2-rename"

with open(os.path.join(OUT_DIR, "audit-publisher-slug-map.json"), "w", encoding="utf-8") as f:
    json.dump({"canonical_map": canonical_map, "slug_renames": slug_renames}, f, indent=2, ensure_ascii=False)

with open(os.path.join(OUT_DIR, "audit-publisher-rename-plan.json"), "w", encoding="utf-8") as f:
    json.dump(pub_rename_files, f, indent=2, ensure_ascii=False)

with open(os.path.join(OUT_DIR, "audit-dupe-clusters.json"), "w", encoding="utf-8") as f:
    json.dump(dupe_clusters, f, indent=2, ensure_ascii=False)

with open(os.path.join(OUT_DIR, "audit-truncation-candidates.json"), "w", encoding="utf-8") as f:
    json.dump(truncation_candidates, f, indent=2, ensure_ascii=False)

# ============================================================
# STATS
# ============================================================
print("=" * 60)
print("A) PUBLISHER SLUG NORMALIZATION")
print("=" * 60)
print(f"Distinct raw slugs: {len(canonical_map)}")
print(f"Slugs that change: {len(slug_renames)}")
print(f"Files needing rename: {len(pub_rename_files)}")
print()
# Show top changes
slug_change_counts = Counter()
for fr in pub_rename_files:
    slug_change_counts[(fr["old_pub"], fr["new_pub"])] += 1
print("Top 15 publisher slug changes (old -> new, count):")
for (old, new), cnt in slug_change_counts.most_common(15):
    print(f"  {cnt:3d}  {old:40s} -> {new}")

print()
print("=" * 60)
print("B) DUPLICATE CLUSTERS")
print("=" * 60)
total_dupes = sum(len(c["members"]) - 1 for c in dupe_clusters)
print(f"Clusters with 2+ members: {len(dupe_clusters)}")
print(f"Total potentially-redundant copies: {total_dupes}")
print()
print("Top 15 clusters (member count):")
for c in sorted(dupe_clusters, key=lambda x: -len(x["members"]))[:15]:
    print(f"  [{c['author']} {c['year']}] {len(c['members'])} copies:")
    for m in c["members"]:
        print(f"    {m['folder']}/{m['filename']}")
    print()

print("=" * 60)
print("C) TRUNCATION CANDIDATES")
print("=" * 60)
print(f"Candidates: {len(truncation_candidates)}")
print()
print("Top 20:")
for t in truncation_candidates[:20]:
    print(f"  [.../{t['last_word']:>4s}]  {t['file']}")
