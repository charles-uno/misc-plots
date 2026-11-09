import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

for n in ["Guarded Heir", "Blood-Chin Rager", "Thrasher Brute", "Belle of the Brawl"]:
    c = by_name[n.lower()]
    print(f"{c['name']} ({c['mana_cost']}, {c.get('power')}/{c.get('toughness')}, {c['type_line']}, {c['set']} {c['released_at']}): {c['oracle_text']}")

print("\n=== ALL BLACK CARDS (ANY RARITY) REFERENCING WARRIOR / KNIGHT / SOLDIER / SAMURAI / BERSERKER / MERCENARY / OUTLAW ===")
for c in pool:
    if c["color_identity"] == ["B"] and "//" not in c["name"]:
        tl = c["type_line"].lower()
        if any(t in tl for t in ["artifact", "enchantment", "planeswalker", "battle", "land"]) and "artifact creature" not in tl:
            continue
        ol = c["oracle_text"].lower()
        if re.search(r"\b(warrior|knight|soldier|samurai|berserker|mercenary|outlaw|party)s?\b", ol):
            print(f"  [{c['released_at'][:4]} {c['set']} {c['rarity'][0].upper()}] {c['name']} ({c['mana_cost']}, {c.get('power')}/{c.get('toughness')}, {c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')}")

