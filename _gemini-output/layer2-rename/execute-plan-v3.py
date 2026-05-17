"""Stage 4: Execute rename-plan-v3.json.

- Operates inside library/by-topic/ and library/_stash-offtopic/
- Handles filename collisions by appending -v2/-v3
- Writes execute-report-v3.txt with per-action results
"""
import json, os, shutil, sys

LIBRARY = r"D:\History vs Hype\library"
TOPIC_ROOT = os.path.join(LIBRARY, "by-topic")
STASH_ROOT = os.path.join(LIBRARY, "_stash-offtopic")
PLAN = r"D:\History vs Hype\_gemini-output\layer2-rename\rename-plan-v3.json"
REPORT = r"D:\History vs Hype\_gemini-output\layer2-rename\execute-report-v3.txt"

os.makedirs(STASH_ROOT, exist_ok=True)

plan = json.load(open(PLAN, encoding="utf-8"))

def resolve_dest(folder: str, filename: str) -> str:
    """Place into TOPIC_ROOT/<folder>/ unless folder == _stash-offtopic."""
    if folder == "_stash-offtopic":
        base = STASH_ROOT
    else:
        base = os.path.join(TOPIC_ROOT, folder)
    os.makedirs(base, exist_ok=True)
    candidate = os.path.join(base, filename)
    # Collision handling
    if os.path.exists(candidate):
        name, ext = os.path.splitext(filename)
        for n in range(2, 20):
            alt = os.path.join(base, f"{name}-v{n}{ext}")
            if not os.path.exists(alt):
                return alt
        raise RuntimeError(f"Too many collisions for {filename}")
    return candidate

counts = {"rename": 0, "move": 0, "move+rename": 0, "stash": 0, "noop": 0, "skip-missing": 0, "error": 0}
lines = []
for p in plan:
    src = p["current_path"]
    action = p["action"]
    if not os.path.exists(src):
        lines.append(f"SKIP-MISSING\t{src}")
        counts["skip-missing"] += 1
        continue
    if action == "noop":
        counts["noop"] += 1
        continue
    try:
        dest = resolve_dest(p["new_folder"], p["new_filename"])
        shutil.move(src, dest)
        counts[action] += 1
        lines.append(f"OK {action}\t{src} -> {dest}")
    except Exception as e:
        counts["error"] += 1
        lines.append(f"ERROR {action}\t{src}: {e}")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Plan entries: {len(plan)}")
for k, v in counts.items():
    print(f"  {k}: {v}")
print(f"\nReport: {REPORT}")
