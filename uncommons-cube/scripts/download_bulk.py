import gzip
import json
import os
import urllib.request

CACHE_DIR = "/Users/charles/Desktop/misc-plots/uncommons-cube/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

headers = {
    "User-Agent": "UncommonsCubeBrainstorm/1.0",
    "Accept": "application/json",
}

req = urllib.request.Request("https://api.scryfall.com/bulk-data", headers=headers)
with urllib.request.urlopen(req) as resp:
    meta = json.loads(resp.read().decode("utf-8"))

target = next(item for item in meta["data"] if item["type"] == "oracle_cards")
uri = target.get("jsonl_download_uri") or target.get("download_uri")
print("Streaming compressed JSONL from:", uri)

req2 = urllib.request.Request(uri, headers=headers)
pool = []
with urllib.request.urlopen(req2) as resp2:
    with gzip.GzipFile(fileobj=resp2) as gz:
        for line in gz:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line.decode("utf-8"))
            if "paper" not in c.get("games", []):
                continue
            if c.get("layout") in ("transform", "modal_dfc", "meld", "double_faced_token", "art_series", "reversible_card"):
                continue
            if c.get("set_type") in ("funny", "memorabilia", "token", "minigame", "vanguard", "planechase", "archenemy"):
                continue
            tl = c.get("type_line", "")
            if any(bad in tl for bad in ("Enchantment", "Planeswalker", "Battle", "Equipment", "Vehicle", "Contraption", "Attraction", "Scheme", "Conspiracy", "Dungeon", "Phenomenon", "Plane")):
                continue
            if "Artifact" in tl and "Creature" not in tl:
                continue
            if not any(good in tl for good in ("Creature", "Instant", "Sorcery", "Land")):
                continue
            oracle = c.get("oracle_text", "")
            ol = oracle.lower()
            if "search your library" in ol or "search their library" in ol:
                continue
            if "gain control of" in ol:
                continue
            if any(mg in ol for mg in ("the monarch", "venture into", "take the initiative", "start your engines", "open an attraction", "put a sticker")):
                continue

            pool.append({
                "name": c["name"],
                "mana_cost": c.get("mana_cost", ""),
                "cmc": c.get("cmc", 0),
                "type_line": tl,
                "oracle_text": oracle,
                "colors": c.get("colors", []),
                "color_identity": c.get("color_identity", []),
                "rarity": c.get("rarity", ""),
                "set": c.get("set", ""),
                "released_at": c.get("released_at", ""),
                "power": c.get("power"),
                "toughness": c.get("toughness"),
                "keywords": c.get("keywords", []),
                "edhrec_rank": c.get("edhrec_rank", 999999),
            })

out_path = os.path.join(CACHE_DIR, "cube-pool.json")
with open(out_path, "w") as out:
    json.dump(pool, out)

print(f"Saved {len(pool)} filtered cards to {out_path} ({os.path.getsize(out_path) // 1024} KB)")
