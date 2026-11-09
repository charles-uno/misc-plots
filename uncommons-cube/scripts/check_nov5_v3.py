import sys
sys.path.insert(0, "uncommons-cube/cache")
from check_nov5_v2 import by_name, norm
from collections import Counter

with open("uncommons-cube/list-nov5.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

print("Total lines:", len(lines))
dups = [k for k, v in Counter(norm(l) for l in lines).items() if v > 1]
print("Duplicates:", dups)

missing = [name for name in lines if norm(name) not in by_name]
print("Missing:", len(missing), missing)

cards = [by_name[norm(l)] for l in lines if norm(l) in by_name]
ci_counts = Counter("".join(sorted(c["color_identity"])) or "C" for c in cards if "Land" not in c["type_line"])
print("Nonland color identity counts (total =", len(cards) - 15, "nonland + 15 lands =", len(cards), "):")
for k, v in sorted(ci_counts.items(), key=lambda x: (len(x[0]), x[0])):
    print(f"  {k}: {v}")

for name in lines[356:]:
    c = by_name.get(norm(name))
    if c:
        ci = "".join(c["color_identity"]) or "C"
        pt = f"{c.get('power')}/{c.get('toughness')}" if c.get("power") is not None else ""
        ot = c["oracle_text"].replace("\n", " | ")
        print(f"  [{ci}] {c['name']} ({c['mana_cost']}, MV={int(c['cmc'])}) {c['type_line']} {pt} -- {ot}")

