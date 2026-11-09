import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

bad_words = [
    "treasure", "food", "clue", "blood token", "eldrazi", "map token", "powerstone", "junk token", "lander",
    "mutate", "regenerate ", "regenerates", "protection from", "omen", "prepare", "retrace",
    "morph", "megamorph", "manifest", "disguise", "cloak", "face down", "face-down",
    "stun counter", "oil counter", "shield counter", "finality counter", "lore counter", "rad counter",
    "time counter", "spore counter", "energy counter", "{e}", "-1/-1 counter", "flying counter",
    "vigilance counter", "menace counter", "trample counter", "lifelink counter", "deathtouch counter",
    "first strike counter", "double strike counter", "hexproof counter", "reach counter", "indestructible counter",
    "role token", "incubate", "search your library", "monarch", "dungeon", "initiative", "start your engines", "max speed", "gain control of"
]

def check_legality(c):
    if "//" in c["name"]:
        return "split"
    tl = c["type_line"].lower()
    if any(t in tl for t in ["artifact", "enchantment", "planeswalker", "battle", "land"]) and "artifact creature" not in tl:
        return "type"
    ol = c["oracle_text"].lower()
    if re.search(r"exile .* until .* leaves the battlefield", ol):
        return "temp exile"
    for w in bad_words:
        if w in ol:
            return w
    for m in re.finditer(r"([a-z0-9+/-]+) counters? on", ol):
        ctype = m.group(1)
        if ctype not in ("+1/+1", "charge", "a", "more", "that", "each", "any", "no", "all", "those", "two", "three", "four", "five", "x", "had", "have", "with", "put", "move", "remove", "distribute", "double"):
            return ctype
    return None

legal_pool = [c for c in pool if check_legality(c) is None]

print("=== 2/2 TOKEN MAKERS IN R, W, B, RW, WB, BR ===")
for ci in [["R"], ["W"], ["B"], ["R","W"], ["B","W"], ["B","R"]]:
    print(f"\n--- {''.join(ci)} 2/2 tokens ---")
    res = [c for c in legal_pool if c["color_identity"] == ci and c["rarity"] == "uncommon" and "2/2" in c["oracle_text"]]
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    for c in res[:20]:
        print(f"  [MV={int(c['cmc'])}] {c['name']} ({c['set']}, {c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

print("\n=== NON-TOKEN FIGHTER (WARRIOR/KNIGHT/SOLDIER/SAMURAI/MERCENARY) PAYOFFS IN R, W, B, RW, WB, BR ===")
for ci in [["R"], ["W"], ["B"], ["R","W"], ["B","W"], ["B","R"]]:
    print(f"\n--- {''.join(ci)} Fighter payoffs ---")
    res = [c for c in legal_pool if c["color_identity"] == ci and c["rarity"] == "uncommon" and re.search(r"\b(warrior|knight|soldier|samurai|berserker)s?\b", c["oracle_text"], re.I) and "1/1" not in c["oracle_text"]]
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    for c in res[:20]:
        print(f"  [MV={int(c['cmc'])}] {c['name']} ({c['set']}, {c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:120]}")

