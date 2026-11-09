import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

for col in ["B", "G", "U"]:
    print(f"\n=== {col} BLINK / SELF-BOUNCE / NINJA / LEAVES-GRAVEYARD PAYOFFS ===")
    for c in legal_pool:
        if c["color_identity"] == [col] and c["rarity"] == "uncommon":
            ol = c["oracle_text"].lower()
            if any(w in ol for w in ["ninjutsu", "sneak", "web-slinging", "leaves the battlefield without dying", "return another", "return up to one other", "exile target creature you control, then return", "exile another target creature you control, then return", "leave your graveyard", "enters from a graveyard", "without paying its mana cost"]):
                print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:130]}")

