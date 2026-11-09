import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

from build_final_skeleton import check_legality

legal_pool = [c for c in pool if check_legality(c) is None]

pattern = re.compile(
    r"becomes tapped|becomes untapped|if this creature is tapped|tapped creatures? you control|for each tapped|two or more tapped|while .* is tapped|whenever you tap|inspired|survival|\{q\}|web-slinging|conspire|harmonize|saddled",
    re.I
)

for ci in [["G"], ["W"], ["U"], ["G","W"], ["U","W"], ["G","U"]]:
    print(f"\n=== {''.join(ci)} TAP/UNTAP PAYOFFS (ALL RARITIES) ===")
    res = [c for c in legal_pool if c["color_identity"] == sorted(ci) and pattern.search(c["oracle_text"])]
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    for c in res[:40]:
        print(f"  [{c['released_at'][:4]} {c['set']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:135]}")

