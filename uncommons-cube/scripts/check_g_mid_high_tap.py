import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

for c in legal_pool:
    if c["color_identity"] == ["G"] and int(c["cmc"]) >= 3:
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["untap ", "becomes tapped", "tapped creature", "survival", "convoke", "tap an untapped", "tap two untapped"]):
            if c["rarity"] in ("uncommon", "rare") and (c.get("released_at", "") or "") >= "2018":
                print(f"[{c['released_at'][:4]} {c['set']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']} ({c.get('power')}/{c.get('toughness')}, {c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:135]}")

