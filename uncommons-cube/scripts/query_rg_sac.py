import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

for c in pool:
    if c["color_identity"] == ["G", "R"]:
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["sacrifice", "dies", "died", "devour", "graveyard"]):
            if "//" not in c["name"]:
                print(f"[MV={int(c['cmc'])}] {c['name']} ({c['set']},{c['rarity']}, {c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

