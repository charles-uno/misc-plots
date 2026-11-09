import json
import unicodedata
from collections import Counter, defaultdict

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
    "fear of impostors": {"name": "Fear of Impostors", "mana_cost": "{1}{U}{U}", "cmc": 3, "type_line": "Enchantment Creature — Nightmare", "oracle_text": "Flash\nWhen Fear of Impostors enters, counter target spell. Its controller manifests dread.", "color_identity": ["U"], "power": "3", "toughness": "2", "rarity": "uncommon", "released_at": "2024-09-27"},
    "cloak and phaser": {"name": "Cloak and Phaser", "mana_cost": "{8}{U}", "cmc": 9, "type_line": "Sorcery", "oracle_text": "Strange new worlds — This spell costs {X} less to cast, where X is the number of differently named lands you control.\nCreate two 2/2 black Romulan creature tokens. Draw two cards, then discard a card.", "color_identity": ["U"], "power": None, "toughness": None, "rarity": "uncommon", "released_at": "2026-01-01"},
    "fiery conclusion": {"name": "Fiery Conclusion", "mana_cost": "{1}{R}", "cmc": 2, "type_line": "Instant", "oracle_text": "As an additional cost to cast this spell, sacrifice a creature.\nFiery Conclusion deals 5 damage to target creature.", "color_identity": ["R"], "power": None, "toughness": None, "rarity": "uncommon", "released_at": "2015-07-17"},
    "fear of exposure": {"name": "Fear of Exposure", "mana_cost": "{2}{G}", "cmc": 3, "type_line": "Enchantment Creature — Nightmare", "oracle_text": "As an additional cost to cast this spell, tap two untapped creatures and/or lands you control.\nTrample", "color_identity": ["G"], "power": "5", "toughness": "4", "rarity": "uncommon", "released_at": "2024-09-27"},
    "daxos, blessed by the sun": {"name": "Daxos, Blessed by the Sun", "mana_cost": "{W}{W}", "cmc": 2, "type_line": "Legendary Enchantment Creature — Demigod", "oracle_text": "Daxos's toughness is equal to your devotion to white.\nWhenever another creature you control enters or dies, you gain 1 life.", "color_identity": ["W"], "power": "2", "toughness": "*", "rarity": "uncommon", "released_at": "2020-01-24"},
    "hero of the nyxborn": {"name": "Hero of the Nyxborn", "mana_cost": "{1}{R}{W}", "cmc": 3, "type_line": "Enchantment Creature — Human Soldier", "oracle_text": "When Hero of the Nyxborn enters, create a 1/1 white Human Soldier creature token.\nWhenever you cast a spell that targets Hero of the Nyxborn, creatures you control get +1/+0 until end of turn.", "color_identity": ["R", "W"], "power": "2", "toughness": "2", "rarity": "uncommon", "released_at": "2020-01-24"},
    "pattern buffer preservation": {"name": "Pattern Buffer Preservation", "mana_cost": "{1}{B}", "cmc": 2, "type_line": "Sorcery", "oracle_text": "Look at the top two cards of your library. Put one of them into your hand and the other into your graveyard.\nBeam me up {1}{B} (You may cast this card from your graveyard for {1}{B} if you also return a creature you control to its owner's hand. Then exile this spell.)", "color_identity": ["B"], "power": None, "toughness": None, "rarity": "uncommon", "released_at": "2026-01-01"}
}
by_name.update(manual)

with open("uncommons-cube/list-nov4.txt") as f:
    raw_lines = [line.strip() for line in f if line.strip()]

cards = []
seen = set()
for name in raw_lines:
    c = by_name[norm(name)]
    cards.append(c)

print("Total slots:", len(cards))
ci_counts = Counter("".join(sorted(c["color_identity"])) or "C" for c in cards if "Land" not in c["type_line"])
print("Nonland color identity counts:", dict(sorted(ci_counts.items(), key=lambda x: (len(x[0]), x[0]))))
land_counts = Counter("".join(sorted(c["color_identity"])) or "C" for c in cards if "Land" in c["type_line"])
print("Land color identity counts:", dict(land_counts))

