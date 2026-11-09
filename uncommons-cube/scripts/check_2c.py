import sys
sys.path.insert(0, "uncommons-cube/cache")
from analyze_list_nov4 import THEMES, unique_cards, card_map
from collections import defaultdict

pairs = defaultdict(list)
for c in unique_cards:
    if len(c["color_identity"]) == 2:
        pairs["".join(sorted(c["color_identity"]))].append(c)

for p, clist in sorted(pairs.items()):
    triads = [tk for tk, td in THEMES.items() if set(p).issubset(set(td["colors"]))]
    print(f"=== {p} ({len(clist)} cards) | Triads: {triads} ===")
    for c in clist:
        roles = []
        for tk, td in THEMES.items():
            if c["name"] in td["payoffs"] and c["name"] in td["enablers"]:
                roles.append(f"{tk}:P+E")
            elif c["name"] in td["payoffs"]:
                roles.append(f"{tk}:P")
            elif c["name"] in td["enablers"]:
                roles.append(f"{tk}:E")
        print(f"  - {c['name']} (MV={int(c['cmc'])}): {roles}")

