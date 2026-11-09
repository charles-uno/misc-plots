import json

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

for c in legal_pool:
    if c["color_identity"] == ["U"]:
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["domain", "converge", "vivid", "number of colors", "basic land types", "elemental", "avatar", "incarnation"]):
            print(f"[{c['released_at'][:4]} {c['set']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:125]}")

