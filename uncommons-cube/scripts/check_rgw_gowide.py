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

print("=== GREEN NON-KINDRED GO-WIDE / TOKEN / CONVOKE UNCOMMONS ===")
for c in legal_pool:
    if c["color_identity"] == ["G"] and c["rarity"] == "uncommon":
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["for each creature you control", "creatures you control get", "convoke", "one or more tokens", "each token", "number of creatures you control", "two 1/1", "three 1/1", "x 1/1"]):
            if not any(k in ol for k in ["other elf", "other elves", "each elf"]):
                print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:125]}")

print("\n=== RG GO-WIDE / TOKEN / ATTACKING UNCOMMONS ===")
for c in legal_pool:
    if c["color_identity"] == ["G", "R"] and c["rarity"] == "uncommon":
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["creatures you control", "attacking creatures", "1/1", "token", "convoke", "for each creature"]):
            print(f"  [{c['released_at'][:4]} {c['set']} MV={int(c['cmc'])}] {c['name']} ({c['type_line']}): {c['oracle_text'].replace(chr(10), ' / ')[:125]}")

