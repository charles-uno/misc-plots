import json

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

for c in pool:
    if c["color_identity"] == ["W"] and c["rarity"] == "uncommon" and "//" not in c["name"]:
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["creatures you control get", "attacking token", "convoke", "for each creature you control", "1/1"]):
            if "when this creature enters, create" not in ol:
                print(f"[{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

