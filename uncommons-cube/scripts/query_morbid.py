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
        return "split/adventure/omen/prepare layout"
    tl = c["type_line"].lower()
    if any(t in tl for t in ["artifact", "enchantment", "planeswalker", "battle", "land"]):
        if "artifact creature" not in tl:
            return "bad type"
    ol = c["oracle_text"].lower()
    if re.search(r"exile .* until .* leaves the battlefield", ol):
        return "temp exile"
    for w in bad_words:
        if w in ol:
            return f"contains banned term '{w}'"
    for m in re.finditer(r"([a-z0-9+/-]+) counters? on", ol):
        ctype = m.group(1)
        if ctype not in ("+1/+1", "charge", "a", "more", "that", "each", "any", "no", "all", "those", "two", "three", "four", "five", "x", "had", "have", "with", "put", "move", "remove", "distribute", "double"):
            return f"contains illegal counter '{ctype}'"
    return None

legal_pool = [c for c in pool if check_legality(c) is None]

def dump(label, ci_list, pattern, only_uncommon=True, limit=18):
    rx = re.compile(pattern, re.I)
    res = []
    for c in legal_pool:
        if c["color_identity"] == sorted(ci_list):
            if only_uncommon and c["rarity"] != "uncommon":
                continue
            if rx.search(c["oracle_text"]):
                res.append(c)
    res.sort(key=lambda x: (x.get("released_at", "") or ""), reverse=True)
    print(f"\n--- {label} ({''.join(ci_list)}) ---")
    for c in res[:limit]:
        ol = c["oracle_text"].replace("\n", " / ")
        print(f"  [MV={int(c['cmc'])}] {c['name']} ({c['set']},{c['rarity']}, {c['type_line']}): {ol[:120]}")

for col in [["G"], ["B","G"], ["B","R"], ["R","G"]]:
    dump("BRG Morbid/Sacrifice", col, r"died this turn|whenever .* dies|sacrifice a creature|sacrifice another|morbid", only_uncommon=True, limit=18)

