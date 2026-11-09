import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

print("=== U MULTICOLOR / DOMAIN / CONVERGE / VIVID / ELEMENTAL PAYOFFS ===")
for c in legal_pool:
    if c["color_identity"] == ["U"] and c["rarity"] == "uncommon":
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["domain", "converge", "vivid", "for each color", "multicolored", "elemental", "avatar", "incarnation"]):
            print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']}: {c['oracle_text'].replace(chr(10), ' / ')[:125]}")

print("\n=== W GO-WIDE PAYOFFS (REWARDING HAVING MANY CREATURES / TOKENS) ===")
for c in legal_pool:
    if c["color_identity"] == ["W"] and c["rarity"] == "uncommon":
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["for each creature you control", "creatures you control get +", "attacking tokens", "convoke", "for each token", "whenever another creature you control enters"]):
            if int(c["cmc"]) in (1, 2, 5, 6):
                print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']}: {c['oracle_text'].replace(chr(10), ' / ')[:125]}")

