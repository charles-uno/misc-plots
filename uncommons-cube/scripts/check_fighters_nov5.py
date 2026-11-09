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
    "fear of impostors": {"name": "Fear of Impostors", "mana_cost": "{1}{U}{U}", "cmc": 3, "type_line": "Enchantment Creature — Nightmare", "oracle_text": "Flash\nWhen Fear of Impostors enters, counter target spell. Its controller manifests dread.", "color_identity": ["U"], "power": "3", "toughness": "2"},
    "cloak and phaser": {"name": "Cloak and Phaser", "mana_cost": "{8}{U}", "cmc": 9, "type_line": "Sorcery", "oracle_text": "Strange new worlds — This spell costs {X} less to cast, where X is the number of differently named lands you control.\nCreate two 2/2 black Romulan creature tokens. Draw two cards, then discard a card.", "color_identity": ["U"], "power": None, "toughness": None},
    "fiery conclusion": {"name": "Fiery Conclusion", "mana_cost": "{1}{R}", "cmc": 2, "type_line": "Instant", "oracle_text": "As an additional cost to cast this spell, sacrifice a creature.\nFiery Conclusion deals 5 damage to target creature.", "color_identity": ["R"], "power": None, "toughness": None},
    "fear of exposure": {"name": "Fear of Exposure", "mana_cost": "{2}{G}", "cmc": 3, "type_line": "Enchantment Creature — Nightmare", "oracle_text": "As an additional cost to cast this spell, tap two untapped creatures and/or lands you control.\nTrample", "color_identity": ["G"], "power": "5", "toughness": "4"},
    "daxos, blessed by the sun": {"name": "Daxos, Blessed by the Sun", "mana_cost": "{W}{W}", "cmc": 2, "type_line": "Legendary Enchantment Creature — Demigod", "oracle_text": "Daxos's toughness is equal to your devotion to white.\nWhenever another creature you control enters or dies, you gain 1 life.", "color_identity": ["W"], "power": "2", "toughness": "*"},
    "hero of the nyxborn": {"name": "Hero of the Nyxborn", "mana_cost": "{1}{R}{W}", "cmc": 3, "type_line": "Enchantment Creature — Human Soldier", "oracle_text": "When Hero of the Nyxborn enters, create a 1/1 white Human Soldier creature token.\nWhenever you cast a spell that targets Hero of the Nyxborn, creatures you control get +1/+0 until end of turn.", "color_identity": ["R", "W"], "power": "2", "toughness": "2"},
    "pattern buffer preservation": {"name": "Pattern Buffer Preservation", "mana_cost": "{1}{B}", "cmc": 2, "type_line": "Sorcery", "oracle_text": "Look at the top two cards of your library. Put one of them into your hand and the other into your graveyard.\nBeam me up {1}{B} (You may cast this card from your graveyard for {1}{B} if you also return a creature you control to its owner's hand. Then exile this spell.)", "color_identity": ["B"], "power": None, "toughness": None},
    "grizzly fate": {"name": "Grizzly Fate", "mana_cost": "{3}{G}{G}", "cmc": 5, "type_line": "Sorcery", "oracle_text": "Create two 2/2 green Bear creature tokens.\nThreshold — Create four 2/2 green Bear creature tokens instead if seven or more cards are in your graveyard.\nFlashback {5}{G}{G}", "color_identity": ["G"], "power": None, "toughness": None}
}
by_name.update(manual)

with open("uncommons-cube/list-nov5.txt") as f:
    raw_lines = [line.strip() for line in f if line.strip()]

cards5 = [by_name[norm(l)] for l in raw_lines]
card_map = {c["name"]: c for c in cards5}

# Check Fighter count (Warrior, Soldier, Knight, Samurai) across colors!
fighter_types = ("Warrior", "Soldier", "Knight", "Samurai")
for col in ["W", "B", "R", "U", "G"]:
    f_cards = [c["name"] for c in cards5 if c["color_identity"] == [col] and any(ft in c["type_line"] for ft in fighter_types)]
    print(f"Printed Fighters in {col} ({len(f_cards)}): {f_cards}")

f_2c = [f"{c['name']} ({''.join(c['color_identity'])})" for c in cards5 if len(c["color_identity"]) > 1 and any(ft in c["type_line"] for ft in fighter_types)]
print(f"Printed Fighters in 2C ({len(f_2c)}): {f_2c}")

