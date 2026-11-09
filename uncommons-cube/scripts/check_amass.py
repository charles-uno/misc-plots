import json

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

print("=== AMASS UNCOMMONS IN POOL ===")
for c in pool:
    if "amass " in c["oracle_text"].lower() and c["rarity"] == "uncommon" and "//" not in c["name"]:
        print(f"  [{c['set']} {''.join(c['color_identity']) or 'C'} MV={int(c['cmc'])}] {c['name']}: {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

