import json, os, hashlib

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\territorial-rename-plan.json", encoding="utf-8") as f:
    plan = json.load(f)

renamed = 0
skipped_same = 0
skipped_missing = 0
skipped_collision = 0
errors = []

# Step 1: rename winners
for op in plan["winners"]:
    src = op["src"]
    dst = op["dst"]
    if not os.path.exists(src):
        skipped_missing += 1
        continue
    if os.path.normcase(src) == os.path.normcase(dst):
        skipped_same += 1
        continue
    if os.path.exists(dst):
        skipped_collision += 1
        continue
    try:
        os.rename(src, dst)
        renamed += 1
    except OSError as e:
        errors.append(f"RENAME FAIL: {op['old']} -> {op['new']}: {e}")

# Step 2: delete true duplicates
deleted = 0
for op in plan["duplicates_to_delete"]:
    src = op["src"]
    if not os.path.exists(src):
        continue
    try:
        os.remove(src)
        deleted += 1
    except OSError as e:
        errors.append(f"DELETE FAIL: {op['old']}: {e}")

# Step 3: hash-based dedup pass on -vN stragglers
SRC_DIR = r"D:\History vs Hype\library\by-topic\territorial-disputes"
all_files = os.listdir(SRC_DIR)
hashes = {}
extra_deleted = 0
for fname in all_files:
    path = os.path.join(SRC_DIR, fname)
    if not os.path.isfile(path): continue
    try:
        with open(path, "rb") as fh:
            h = hashlib.md5(fh.read()).hexdigest()
    except OSError:
        continue
    if h in hashes:
        # Decide which to keep: prefer name WITHOUT -vN suffix
        existing = hashes[h]
        existing_has_v = bool(__import__('re').search(r'-v\d+\.[a-z]+$', existing))
        new_has_v = bool(__import__('re').search(r'-v\d+\.[a-z]+$', fname))
        if new_has_v and not existing_has_v:
            os.remove(path)
            extra_deleted += 1
        elif existing_has_v and not new_has_v:
            os.remove(os.path.join(SRC_DIR, existing))
            extra_deleted += 1
            hashes[h] = fname
        else:
            # Both have -v or neither - keep first, delete current
            os.remove(path)
            extra_deleted += 1
    else:
        hashes[h] = fname

# Step 4: write report
report = [
    f"=== Layer 2 Territorial-Disputes Rename Report ===",
    f"Plan winners:            {len(plan['winners'])}",
    f"  Renamed:               {renamed}",
    f"  Already correct (same):{skipped_same}",
    f"  Source missing:        {skipped_missing}",
    f"  Dst collision skip:    {skipped_collision}",
    f"True duplicates deleted: {deleted}",
    f"Hash-dedup deleted (-vN):{extra_deleted}",
    f"Errors:                  {len(errors)}",
    "",
    "Errors:",
    *errors[:50],
    "",
    f"Final file count: {len([f for f in os.listdir(SRC_DIR) if os.path.isfile(os.path.join(SRC_DIR, f))])}",
]
report_text = "\n".join(report)
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\territorial-rename-report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)
print(report_text)
