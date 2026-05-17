"""Audit Step 3: Build the consolidated cleanup plan.

For dupe clusters: pick the WINNER per cluster using heuristic ranking. Other members -> _stash-duplicates/.
For non-dupe files: apply canonical publisher slug rename.
For truncation: flag candidates that are real cuts (exclude Bj.581 / Vol2-style false positives).

Output: audit-execution-plan.json (the master plan), audit-execution-plan.tsv (human-readable).
"""
import json, os, re
from collections import defaultdict, Counter

OUT_DIR = r"D:\History vs Hype\_gemini-output\layer2-rename"

records = json.load(open(os.path.join(OUT_DIR, "library-inventory.json"), encoding="utf-8"))["records"]
slug_map = json.load(open(os.path.join(OUT_DIR, "audit-publisher-slug-map.json"), encoding="utf-8"))["canonical_map"]
dupe_clusters = json.load(open(os.path.join(OUT_DIR, "audit-dupe-clusters.json"), encoding="utf-8"))
truncation_candidates = json.load(open(os.path.join(OUT_DIR, "audit-truncation-candidates.json"), encoding="utf-8"))

# Index records by (folder, filename) for lookup
rec_index = {(r["folder"], r["filename"]): r for r in records}

# ============================================================
# Dupe winner picker
# ============================================================
PIRACY_SLUGS = {"ZLib", "AnnaArchive", "Libgen", "Unknown"}

def score_member(r: dict) -> tuple:
    """Higher tuple wins. Sort descending by this."""
    # 1) Avoid piracy/unknown publisher
    pub_canon = slug_map.get(r["publisher"], r["publisher"])
    pub_score = 0 if pub_canon in PIRACY_SLUGS else 1
    # 2) Title length (more descriptive)
    title_len = len(r["title"])
    # 3) Avoid -v2/-v3 suffix
    version_score = 1 if r["version_suffix"] == 1 else 0
    # 4) Prefer specific topic folder over general-history when same book exists in both
    folder_score = 0 if r["folder"] == "general-history" else 1
    # 5) Prefer non-Unknown year
    year_score = 1 if r["year"] != "0000" else 0
    # 6) File size (larger usually = book vs partial chapter, when same content)
    size_score = r["size"]
    return (pub_score, year_score, version_score, folder_score, title_len, size_score)


dupe_winners = set()    # set of (folder, filename) of winners
dupe_losers = []        # list of (folder, filename, winner_path, reason)
for cluster in dupe_clusters:
    members = cluster["members"]
    ranked = sorted(members, key=score_member, reverse=True)
    winner = ranked[0]
    dupe_winners.add((winner["folder"], winner["filename"]))
    for loser in ranked[1:]:
        reason_parts = []
        pub_w = slug_map.get(winner["publisher"], winner["publisher"])
        pub_l = slug_map.get(loser["publisher"], loser["publisher"])
        if pub_l in PIRACY_SLUGS and pub_w not in PIRACY_SLUGS:
            reason_parts.append(f"loser-publisher={pub_l}")
        if loser["version_suffix"] > 1:
            reason_parts.append(f"-v{loser['version_suffix']} suffix")
        if loser["folder"] == "general-history" and winner["folder"] != "general-history":
            reason_parts.append(f"misfiled in general-history (winner: {winner['folder']})")
        if len(loser["title"]) < len(winner["title"]):
            reason_parts.append(f"shorter title ({len(loser['title'])} vs {len(winner['title'])} chars)")
        reason = "; ".join(reason_parts) or "tied; lower score"
        dupe_losers.append({
            "folder": loser["folder"],
            "filename": loser["filename"],
            "winner": f"{winner['folder']}/{winner['filename']}",
            "reason": reason,
        })

# ============================================================
# Truncation candidates: filter false positives
# ============================================================
# Keep titles where the cut is a real word cut, not a real volume number, grave number, or year
FALSE_POSITIVE_LASTS = {"Vol2", "Vol1", "Vol3", "Vol4", "Vol5", "Bj581"}
real_truncations = []
for t in truncation_candidates:
    last = t["last_word"]
    title = t["title"]
    # Exclude obvious volume/grave numbers
    if last in FALSE_POSITIVE_LASTS:
        continue
    # Exclude pure digits >= 3 chars (likely year boundary like "1492-1763" cut to "149")
    # — actually keep digit cuts: "Caribs149" should probably be "Caribs1492" (date range cut)
    real_truncations.append(t)

# ============================================================
# Consolidated execution plan
# ============================================================
plan = []
for r in records:
    key = (r["folder"], r["filename"])
    canonical_pub = slug_map.get(r["publisher"], r["publisher"])
    new_pub = canonical_pub if canonical_pub != r["publisher"] else r["publisher"]

    # Determine action
    if any(l["folder"] == r["folder"] and l["filename"] == r["filename"] for l in dupe_losers):
        # Dupe loser
        loser_info = next(l for l in dupe_losers if l["folder"] == r["folder"] and l["filename"] == r["filename"])
        plan.append({
            "action": "stash-dupe",
            "folder": r["folder"],
            "filename": r["filename"],
            "new_folder": "_stash-duplicates",
            "new_filename": r["filename"],
            "reason": f"duplicate of {loser_info['winner']} ({loser_info['reason']})",
        })
        continue

    # Publisher slug rename only?
    if new_pub != r["publisher"]:
        new_name = f"{r['title']}-{r['author']}-{r['year']}-{new_pub}.{r['ext']}"
        plan.append({
            "action": "rename-pub",
            "folder": r["folder"],
            "filename": r["filename"],
            "new_folder": r["folder"],
            "new_filename": new_name,
            "reason": f"publisher slug {r['publisher']} -> {new_pub}",
        })
        continue

    # Noop
    plan.append({
        "action": "noop",
        "folder": r["folder"],
        "filename": r["filename"],
        "new_folder": r["folder"],
        "new_filename": r["filename"],
        "reason": "",
    })

# Save
with open(os.path.join(OUT_DIR, "audit-execution-plan.json"), "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)
with open(os.path.join(OUT_DIR, "audit-real-truncations.json"), "w", encoding="utf-8") as f:
    json.dump(real_truncations, f, indent=2, ensure_ascii=False)

# Human-readable TSV
with open(os.path.join(OUT_DIR, "audit-execution-plan.tsv"), "w", encoding="utf-8") as f:
    f.write("action\tfolder\tfilename\tnew_folder\tnew_filename\treason\n")
    for p in plan:
        if p["action"] == "noop":
            continue
        f.write(f"{p['action']}\t{p['folder']}\t{p['filename']}\t{p['new_folder']}\t{p['new_filename']}\t{p['reason']}\n")

# Stats
print(f"Total files in plan: {len(plan)}")
print()
print("By action:")
for k, v in Counter(p["action"] for p in plan).most_common():
    print(f"  {k}: {v}")
print()
print(f"Real truncations to fix: {len(real_truncations)}")
for t in real_truncations:
    print(f"  [.../{t['last_word']:>4s}]  {t['file']}")
