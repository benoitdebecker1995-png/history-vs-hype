"""Comment-mine driver for #62 — uses YouTube Data API (OAuth), not yt-dlp (bot-blocked)."""
import sys, json
sys.path.insert(0, r"D:\History vs Hype")
from tools.youtube_analytics.comments import fetch_and_categorize_comments

VIDEOS = [
    ("1iFh0gviWGI", "868K — Execution of Stepan Bandera: Ukrainian Nazi Who Killed 1000s [sensationalist/history]"),
    ("luFVfcW7yAE", "104K — Stepan Bandera & UPA: How Ukrainian Nationalism led to Polish Genocide [history/genocide-frame]"),
    ("G07olJjO4Y4", "76K — Poland slams Zelenskyy for honouring Nazi-linked militia [CURRENT controversy]"),
    ("iwocrIzlLtQ", "102K — Concert Chaos in Warsaw: Polish-Ukrainian Firestorm [CURRENT/street-level]"),
    ("FsVyd002Dos", "2.3M — Ludobojstwo na Wolyniu (Historia Bez Cenzury) [POLISH-language, biggest]"),
]

out = []
alljson = {}
for vid, label in VIDEOS:
    out.append(f"\n{'='*90}\n=== {label}\n=== https://youtube.com/watch?v={vid}\n{'='*90}")
    res = fetch_and_categorize_comments(vid, max_comments=80)
    if "error" in res:
        out.append(f"  !! ERROR: {res['error']} — {res.get('details','')[:160]}")
        alljson[vid] = res
        continue
    alljson[vid] = res
    cc = res["category_counts"]
    out.append(f"  fetched: {res['total_fetched']} | Q={cc['questions']} Objections={cc['objections']} Requests={cc['requests']} Other={cc['other']}")
    for cat in ("questions", "objections", "requests", "other"):
        items = sorted(res["categories"][cat], key=lambda c: c.get("likes", 0), reverse=True)
        if not items:
            continue
        out.append(f"\n  --- {cat.upper()} ({len(items)}) ---")
        for c in items:
            txt = " ".join(c["text"].split())[:320]
            out.append(f"   [{c.get('likes',0)}♥ {c.get('reply_count',0)}↩] {txt}")

text = "\n".join(out)
with open("comments-extracted.txt", "w", encoding="utf-8") as f:
    f.write(text)
with open("comments-raw.json", "w", encoding="utf-8") as f:
    json.dump(alljson, f, ensure_ascii=False, indent=1)
# stdout summary only (avoid unicode crash on console)
print("DONE. videos:", len(VIDEOS))
for vid, label in VIDEOS:
    r = alljson[vid]
    if "error" in r:
        print(f"  {vid}: ERROR {r['error']}")
    else:
        print(f"  {vid}: {r['total_fetched']} comments")
print(f"chars written: {len(text)} -> comments-extracted.txt")
