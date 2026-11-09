import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

print("=== RED & RG/RW +1/+1 COUNTER / MODIFIED UNCOMMONS ===")
for ci in [["R"], ["G","R"], ["R","W"]]:
    print(f"\n--- {''.join(ci)} ---")
    res = []
    for c in pool:
        if c["color_identity"] == ci and c["rarity"] == "uncommon" and "//" not in c["name"]:
            tl = c["type_line"].lower()
            if any(t in tl for t in ["artifact", "enchantment", "planeswalker", "battle", "land"]) and "artifact creature" not in tl:
                continue
            ol = c["oracle_text"].lower()
            if "+1/+1 counter" in ol or "modified" in ol or "proliferate" in ol:
                if any(w in ol for w in ["each creature you control with a +1/+1", "modified", "proliferate", "whenever one or more +1/+1", "additional +1/+1", "counters on it"]):
                    res.append(c)
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    for c in res[:15]:
        print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']}: {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

