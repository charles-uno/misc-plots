import sys
sys.path.insert(0, "uncommons-cube/cache")
from analyze_list_nov5 import THEMES, unique_cards

assigned = set()
for tk, td in THEMES.items():
    assigned.update(td["payoffs"])
    assigned.update(td["enablers"])

unassigned = [c for c in unique_cards if c["name"] not in assigned]
print(f"Unassigned ({len(unassigned)}):")
for c in unassigned:
    ci = "".join(c["color_identity"]) or "C"
    ot = c["oracle_text"].replace("\n", " | ")
    print(f"  [{ci}] {c['name']} (MV={int(c['cmc'])}) -- {c['type_line']} -- {ot}")

