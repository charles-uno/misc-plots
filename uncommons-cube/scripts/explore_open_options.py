import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

print("Sample keys:", list(pool[0].keys()))

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
    ol = c["oracle_text"].lower()
    for w in bad_words:
        if w in ol:
            return f"contains banned term '{w}'"
    for m in re.finditer(r"([a-z0-9+/-]+) counters? on", ol):
        ctype = m.group(1)
        if ctype not in ("+1/+1", "charge", "a", "more", "that", "each", "any", "no", "all", "those", "two", "three", "four", "five", "x", "had", "have", "with", "put", "move", "remove", "distribute", "double"):
            return f"contains illegal counter '{ctype}'"
    return None

targets = [
    "Kinjalli's Caller", "Osseous Exhale", "Legion Lieutenant", "Stromkirk Captain",
    "Rushblade Commander", "Kargan Warleader", "Chief of the Edge", "The Chief Warg",
    "Nighthowl", "Pursuer", "Caustic Exhale", "Kalakscion", "Captain America, Living Legend"
]
print("=== USER MENTIONED CARDS ===")
for t in targets:
    matches = [c for c in pool if t.lower() in c["name"].lower()]
    for m in matches[:8]:
        print(f"  {m['name']} (ci={m['color_identity']}, MV={m['cmc']}, {m['type_line']}, set={m.get('set')}, r={m.get('rarity')}): {m['oracle_text']!r} [Illegal={check_legality(m)}]")

