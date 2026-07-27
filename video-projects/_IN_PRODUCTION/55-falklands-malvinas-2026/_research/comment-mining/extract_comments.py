import json, glob
videos = [
 ("BiDvLshi9CY","29.7M EN OverSimplified - MiniWars"),
 ("gLpNJNMYohs","4.5M ES Memorias de Pez - Malvinas en 7 min"),
 ("jLR7-hJZEBc","3.7M EN IWM - Why the Falklands Conflict happened"),
 ("Fdq-O2oSLGc","1.12M EN Joe Ham - banner (7k subs, 6 days)"),
 ("b56_1ikeufY","1.7M EN Geography By Geoff - Why Anyone Lives There"),
 ("_fg5amio4jU","1.97M EN Binkov - Could Argentina take it today"),
 ("TV0h-aLrOCg","3.98M EN Simple History"),
 ("RNjKfVH6XDI","13.6M EN Yarnhub - Skyhawks"),
 ("x16MvpDphaU","342K EN Sky News - what's going on"),
 ("Ug2QAVoj9WY","179K EN TLDR - Petrostate"),
]
out=[]
for vid,label in videos:
    m=glob.glob(f"*{vid}*.info.json")
    if not m: out.append(f"MISSING {vid}"); continue
    d=json.load(open(m[0],encoding="utf-8",errors="replace"))
    cs=sorted(d.get("comments",[]),key=lambda c:c.get("like_count") or 0,reverse=True)
    out.append(f"\n{'='*88}\n=== {label} [{vid}] {len(cs)} comments ===")
    for i,c in enumerate(cs):
        t=(c.get("text") or "").replace("\n"," ")[:300]
        out.append(f"[{i+1}]({c.get('like_count') or 0}L) {t}")
r="\n".join(out)
open("comments.txt","w",encoding="utf-8").write(r)
print(len(r),"chars")
