import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

for ci in [["R"], ["R", "W"]]:
    print(f"=== {ci} SACRIFICE / DIES ===")
    for c in pool:
        if c["color_identity"] == ci and c["rarity"] == "uncommon" and "//" not in c["name"]:
            tl = c["type_line"].lower()
            if any(t in tl for t in ["artifact", "enchantment", "planeswalker", "battle", "land"]) and "artifact creature" not in tl:
                continue
            ol = c["oracle_text"].lower()
            if any(w in ol for w in ["sacrifice a creature", "sacrifice another", "whenever a creature you control dies", "whenever another creature you control dies", "mobilize"]):
                if not any(b in ol for b in ["treasure", "food", "clue", "blood token", "eldrazi"]):
                    print(f"  [MV={int(c['cmc'])}] {c['name']} ({c['set']}): {c['oracle_text'].replace(chr(10), ' / ')[:110]}")

