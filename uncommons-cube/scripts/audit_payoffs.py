import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

from build_final_skeleton import THEMES_FINAL, check_legality

print("=== CURRENT 120 CARDS ORACLE AUDIT ===")
for t in THEMES_FINAL:
    print(f"\n### {t['title']}")
    for k, names in t["slots"].items():
        for n in names:
            c = by_name[n.lower()]
            print(f"  [{k} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')}")

print("\n=== CHECK FOUL-TONGUE INVOCATION & FEARSOME AWAKENING ===")
for n in ["Foul-Tongue Invocation", "Fearsome Awakening"]:
    c = by_name.get(n.lower())
    if c:
        print(f"  {c['name']} ({c['mana_cost']}, {c['rarity']}, {c['set']}): {c['oracle_text']} [Illegal={check_legality(c)}]")

