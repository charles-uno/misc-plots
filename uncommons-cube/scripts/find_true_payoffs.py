import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

def search_specific(label, ci, pattern, rarities=("uncommon",), limit=25):
    rx = re.compile(pattern, re.I)
    res = []
    for c in legal_pool:
        if c["color_identity"] == sorted(ci) and c["rarity"] in rarities:
            if rx.search(c["oracle_text"]):
                res.append(c)
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    print(f"\n=== {label} ({''.join(ci)}) ===")
    for c in res[:limit]:
        print(f"  [{c['released_at'][:4]} {c['set']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:130]}")

# 1. WUB: U, B, WB cards that specifically reward ARTIFACTS (not "creature or artifact")
search_specific("U Artifact Payoffs", ["U"], r"artifact.*you control|affinity for artifacts|whenever an artifact|artifact creature.*get|for each artifact", ("uncommon",))
search_specific("B Artifact Payoffs", ["B"], r"artifact.*you control|affinity for artifacts|whenever an artifact|artifact creature.*get|for each artifact|sacrifice an artifact", ("uncommon", "common", "rare"))
search_specific("WB Artifact Payoffs", ["W","B"], r"artifact", ("uncommon", "common", "rare"))

# 2. BRG: B and BR Dragon / Behemoth / Power 4+ payoffs
search_specific("B Dragon/Ferocious/Power 4+ Payoffs", ["B"], r"power 4 or greater|ferocious|dragon|greatest power|dinosaur|wurm", ("uncommon", "common", "rare"))
search_specific("BR Dragon/Ferocious/Power 4+ Payoffs", ["B","R"], r"power 4 or greater|ferocious|dragon|greatest power|dinosaur|wurm", ("uncommon", "common", "rare"))

# 3. RWB: R, W, RW Sacrifice / Dies payoffs
search_specific("R Sacrifice/Dies Payoffs", ["R"], r"whenever .* dies|sacrifice a creature|sacrifice another creature|casualty|mobilize", ("uncommon", "common", "rare"))
search_specific("W Sacrifice/Dies Payoffs", ["W"], r"whenever .* dies|died this turn|sacrifice a creature|sacrifice another", ("uncommon", "common", "rare"))
search_specific("RW Sacrifice/Dies Payoffs", ["R","W"], r"whenever .* dies|died this turn|sacrifice a|leaves the battlefield", ("uncommon", "common", "rare"))

