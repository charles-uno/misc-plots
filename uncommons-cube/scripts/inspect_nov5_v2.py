import sys
sys.path.insert(0, "uncommons-cube/cache")
from check_nov5_v2 import by_name, norm, lines
from collections import Counter

cards = [by_name[norm(l)] for l in lines]
ci_counts = Counter("".join(sorted(c["color_identity"])) or "C" for c in cards if "Land" not in c["type_line"])
print("Nonland color identity counts (total =", len(cards) - 15, "nonland + 15 lands =", len(cards), "):")
for k, v in sorted(ci_counts.items(), key=lambda x: (len(x[0]), x[0])):
    print(f"  {k}: {v}")

print("\nNew cards from line 330+ (plus Shoreline Looter & Hazard of the Dunes):")
extra = ["Shoreline Looter", "Hazard of the Dunes"] + lines[332:]
for name in extra:
    c = by_name[norm(name)]
    ci = "".join(c["color_identity"]) or "C"
    pt = f"{c.get('power')}/{c.get('toughness')}" if c.get("power") is not None else ""
    ot = c["oracle_text"].replace("\n", " | ")
    print(f"  [{ci}] {c['name']} ({c['mana_cost']}, MV={int(c['cmc'])}) {c['type_line']} {pt} -- {ot}")

