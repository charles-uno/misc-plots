import sys
sys.path.insert(0, "uncommons-cube/cache")
from analyze_list_nov4 import THEMES, unique_cards, card_map
from collections import Counter

assigned = set()
for t_key, t_data in THEMES.items():
    assigned.update(t_data["payoffs"])
    assigned.update(t_data["enablers"])

unassigned = [c for c in unique_cards if c["name"] not in assigned]
print(f"Unassigned cards ({len(unassigned)}):")
for c in unassigned:
    ci = "".join(c["color_identity"]) or "C"
    ot = c["oracle_text"].replace("\n", " | ")
    print(f"  [{ci}] {c['name']} (MV={int(c['cmc'])}) -- {c['type_line']} -- {ot}")

