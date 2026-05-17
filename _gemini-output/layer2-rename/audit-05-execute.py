"""Audit Step 5: Execute the three audit passes.

Order matters:
1. Truncation fixes first (rename in place)
2. Dedup stash second (move losers to _stash-duplicates/)
3. Publisher slug rename last (over what remains)

Reports all actions to audit-execute-report.txt.
"""
import json, os, shutil
from collections import Counter

LIBRARY = r"D:\History vs Hype\library"
TOPIC_ROOT = os.path.join(LIBRARY, "by-topic")
DUP_STASH = os.path.join(LIBRARY, "_stash-duplicates")
OUT_DIR = r"D:\History vs Hype\_gemini-output\layer2-rename"

os.makedirs(DUP_STASH, exist_ok=True)

trunc_map = json.load(open(os.path.join(OUT_DIR, "audit-truncation-fixes-map.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(OUT_DIR, "audit-execution-plan.json"), encoding="utf-8"))

log_lines = []
counts = Counter()


def resolve_dest_path(folder: str, filename: str, target_root: str = TOPIC_ROOT) -> str:
    if folder == "_stash-duplicates":
        base = DUP_STASH
    else:
        base = os.path.join(target_root, folder)
    os.makedirs(base, exist_ok=True)
    candidate = os.path.join(base, filename)
    if os.path.exists(candidate):
        name, ext = os.path.splitext(filename)
        for n in range(2, 30):
            alt = os.path.join(base, f"{name}-v{n}{ext}")
            if not os.path.exists(alt):
                return alt
        raise RuntimeError(f"Too many collisions for {filename}")
    return candidate


# ===== Step 1: truncation fixes =====
# These should be applied BEFORE dedup so dedup sees the corrected names
# But since plan is built from inventory (pre-truncation), we need to map old->new.
# We'll rename truncated files in place first, then translate plan entries.
trunc_renames = {}  # (folder, old_filename) -> (folder, new_filename)
for old_filename, fix in trunc_map.items():
    # Find which folder contains this file
    found = False
    for folder in os.listdir(TOPIC_ROOT):
        fpath = os.path.join(TOPIC_ROOT, folder)
        if not os.path.isdir(fpath):
            continue
        src = os.path.join(fpath, old_filename)
        if os.path.exists(src):
            dest = resolve_dest_path(folder, fix["new"])
            shutil.move(src, dest)
            counts["truncation-fix"] += 1
            log_lines.append(f"TRUNCATION\t{folder}/{old_filename}\t->\t{folder}/{os.path.basename(dest)}\t{fix['reason']}")
            trunc_renames[(folder, old_filename)] = (folder, os.path.basename(dest))
            found = True
            break
    if not found:
        log_lines.append(f"TRUNCATION-MISSING\t{old_filename}\tnot found in any folder")
        counts["truncation-missing"] += 1


# ===== Step 2: dedup stash =====
# Translate plan entries through trunc_renames in case a stash-dupe was truncated first
for p in plan:
    if p["action"] != "stash-dupe":
        continue
    folder = p["folder"]
    filename = p["filename"]
    # Resolve if it was truncation-renamed
    key = (folder, filename)
    if key in trunc_renames:
        folder, filename = trunc_renames[key]
    src = os.path.join(TOPIC_ROOT, folder, filename)
    if not os.path.exists(src):
        log_lines.append(f"DUPE-MISSING\t{folder}/{filename}\tnot found")
        counts["dupe-missing"] += 1
        continue
    dest = resolve_dest_path("_stash-duplicates", filename)
    shutil.move(src, dest)
    counts["stash-dupe"] += 1
    log_lines.append(f"STASH-DUPE\t{folder}/{filename}\t->\t_stash-duplicates/{os.path.basename(dest)}\t{p['reason']}")


# ===== Step 3: publisher slug rename =====
# Translate plan entries through trunc_renames
for p in plan:
    if p["action"] != "rename-pub":
        continue
    folder = p["folder"]
    filename = p["filename"]
    key = (folder, filename)
    if key in trunc_renames:
        # truncation already renamed AND normalized publisher in the new name
        log_lines.append(f"PUBRENAME-SKIP\t{folder}/{filename}\talready handled by truncation fix")
        counts["pub-rename-skipped"] += 1
        continue
    src = os.path.join(TOPIC_ROOT, folder, filename)
    if not os.path.exists(src):
        log_lines.append(f"PUBRENAME-MISSING\t{folder}/{filename}\tnot found (may be already stashed as dupe)")
        counts["pub-rename-missing"] += 1
        continue
    dest = resolve_dest_path(folder, p["new_filename"])
    if src == dest:
        counts["pub-rename-noop"] += 1
        continue
    shutil.move(src, dest)
    counts["pub-rename"] += 1
    log_lines.append(f"PUB-RENAME\t{folder}/{filename}\t->\t{folder}/{os.path.basename(dest)}\t{p['reason']}")


# ===== Write report =====
report_path = os.path.join(OUT_DIR, "audit-execute-report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print("Execution summary:")
for k, v in counts.most_common():
    print(f"  {k}: {v}")
print(f"\nReport: {report_path}")
