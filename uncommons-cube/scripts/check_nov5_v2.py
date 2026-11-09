import json
import unicodedata
from collections import Counter

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {}
for c in pool:
    by_name[norm(c["name"])] = c
    if " // " in c["name"]:
        for part in c["name"].split(" // "):
            by_name.setdefault(norm(part), c)

manual = {
    "fear of impostors": {"name": "Fear of Impostors", "mana_cost": "{1}{U}{U}", "cmc": 3, "type_line": "Enchantment Creature — Nightmare", "oracle_text": "Flash\nWhen Fear of Impostors enters, counter target spell. Its controller manifests dread.", "color_identity": ["U"], "power": "3", "toughness": "2"},
    "cloak and phaser": {"name": "Cloak and Phaser", "mana_cost": "{8}{U}", "cmc": 9, "type_line": "Sorcery", "oracle_text": "Strange new worlds — This spell costs {X} less to cast, where X is the number of differently named lands you control.\nCreate two 2/2 black Romulan creature tokens. Draw two cards, then discard a card.", "color_identity": ["U"], "power": None, "toughness": None},
    "grizzly fate": {"name": "Grizzly Fate", "mana_cost": "{3}{G}{G}", "cmc": 5, "type_line": "Sorcery", "oracle_text": "Create two 2/2 green Bear creature tokens.\nThreshold — Create four 2/2 green Bear creature tokens instead if seven or more cards are in your graveyard.\nFlashback {5}{G}{G}", "color_identity": ["G"], "power": None, "toughness": None}
}
by_name.update(manual)

with open("uncommons-cube/list-nov5.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

print("Total lines:", len(lines))
dups = [k for k, v in Counter(lines).items() if v > 1]
print("Duplicates:", dups)

missing = [name for name in lines if norm(name) not in by_name]
print("Missing:", len(missing), missing)

