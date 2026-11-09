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

unique_cards = []
seen = set()
for line in raw_lines:
    k = norm(line)
    if k not in seen:
        seen.add(k)
        unique_cards.append(by_name[k])

card_map = {c["name"]: c for c in unique_cards}

THEMES = {
    "WUB": {
        "title": "WUB — Thopters & Artifact Creatures (Affinity / Artifacts Matter)",
        "colors": ["W", "U", "B"],
        "payoffs": [
            # W (5)
            "Command Subadjunct", "Mandible Justiciar", "Paladin Danse, Steel Maverick", "Guidelight Synergist", "Plated Onslaught",
            # U (4)
            "Rescue, Pepper Potts", "Thirst for Knowledge", "Iron Lad, Diverging Destiny", "Whirler Rogue",
            # B (5)
            "Etherium Pteramander", "Armix, Filigree Thrasher", "Arcbound Condor", "Pactdoll Terror", "Monoist Circuit-Feeder",
            # 2C (1)
            "Ethersworn Sphinx",
            # C (1 - Sanctuary Raptor rewards 3+ tokens and is an artifact flyer)
            "Sanctuary Raptor",
        ],
        "enablers": [
            # C (6)
            "Containment Construct", "Three Tree Mascot", "Sanctuary Raptor", "H.E.R.B.I.E. Scout Unit", "Traxos, Scourge Eternal", "Sphinx of the Guildpact",
            # W (6)
            "Command Subadjunct", "Market Gnome", "Sundial, Dawn Tyrant", "Mandible Justiciar", "Paladin Danse, Steel Maverick", "Guidelight Synergist",
            # U (11)
            "Mechan Navigator", "Rescue, Pepper Potts", "Corridor Monitor", "Sweep the Skies", "Rune-Sealed Wall", "Launch Mishap", "Etherium Spinner", "Iron Lad, Diverging Destiny", "Whirler Rogue", "Traxos, Academy Guardian", "Spikeshell Harrier",
            # B (9)
            "Etherium Pteramander", "Monoist Sentry", "Nezumi Prowler", "Armix, Filigree Thrasher", "Weaponcraft Enthusiast", "Arcbound Condor", "Pactdoll Terror", "Voidforged Titan", "Monoist Circuit-Feeder",
            # 2C (3)
            "Station Monitor", "Baleful Strix", "Ethersworn Sphinx",
        ]
    },
    "WBG": {
        "title": "WBG — Lifegain & Drain",
        "colors": ["W", "B", "G"],
        "payoffs": [
            # W (4)
            "Ajani's Pridemate", "Angel of Vitality", "Star Charter", "Glorious Enforcer",
            # B (2)
            "Nightmare's Thirst", "Bloodthirsty Aerialist",
            # G (4)
            "Fortifying Draught", "Tigra, Feline Fury", "Thornfist Striker", "Titanbones, Towering Heart",
            # 2C (3)
            "Dina, Soul Steeper", "Trelasarra, Moon Dancer", "Starseer Mentor",
        ],
        "enablers": [
            # W (13)
            "Ruin-Lurker Bat", "Enter the Avatar State", "Joust Through", "Lay Down Arms", "Market Gnome", "Battle Menu", "Daxos, Blessed by the Sun", "Mandible Justiciar", "Paladin Danse, Steel Maverick", "Falcon, Joaquin Torres", "Dawnstrike Vanguard", "Bounding Felidar", "Glorious Enforcer",
            # B (10)
            "Dream Beavers", "Dissection Practice", "Nightmare's Thirst", "Nezumi Prowler", "Ravening Warg", "Foul-Tongue Invocation", "Arnyn, Deathbloom Botanist", "Sanguinary Priest", "Pactdoll Terror", "Shimmercreep",
            # G (9)
            "Virulent Emissary", "Fortifying Draught", "Eumidian Terrabotanist", "Scout the City", "Devouring Tendrils", "Luminollusk", "Cautious Survivor", "Titanbones, Towering Heart", "Snarl Song",
            # 2C (5)
            "Elas il-Kor, Sadistic Pilgrim", "Denethor, Ruling Steward", "Social Snub", "Leyline Prowler", "Wakandan Tusker",
        ]
    },
    "BRG": {
        "title": "BRG — Dragons, Behemoths & Ferocious (Power 4+)",
        "colors": ["B", "R", "G"],
        "payoffs": [
            # B (5)
            "Nighthowl Pursuer", "Caustic Exhale", "Ravening Warg", "Foul-Tongue Invocation", "Fearsome Awakening",
            # R (6)
            "Triumphant Chomp", "Boundary Lands Ranger", "Firespitter Whelp", "Kolaghan Warmonger", "Dinosaur Stampede", "Bolt Bend",
            # G (6)
            "Nasty Little Rabbit", "Drover of the Mighty", "Owlbear Shepherd", "Savage Stomp", "Surrak, the Hunt Caller", "Earthshaker Dreadmaw",
            # 2C (4)
            "Itzquinth, Firstborn of Gishath", "The Chief Warg", "Thrakkus the Butcher", "Bladewing the Risen",
        ],
        "enablers": [
            # C (2)
            "Three Tree Mascot", "Traxos, Scourge Eternal",
            # B (8)
            "Monoist Sentry", "Kalakscion, Hunger Tyrant", "Graveshifter", "Shredder, Unrelenting", "Voidforged Titan", "Phyrexian Gargantua", "Death-Rattle Oni", "Black Dragon",
            # R (10)
            "Slumbering Cerberus", "Firespitter Whelp", "Bonded Horncrest", "Memorial Team Leader", "Glóin the Mighty // Easy Pickings", "Raging Goblinoids", "Hurler Cyclops", "Territorial Bruntar", "Rorix Bladewing", "Fang Dragon // Forktail Sweep",
            # G (16)
            "Fear of Exposure", "Call of the Herd", "Surrak, the Hunt Caller", "Temur Sabertooth", "Titanbones, Towering Heart", "Colossadactyl", "Elvish Regrower", "Elegant Entourage", "Cautious Survivor", "Terrian, World Tyrant", "Earthshaker Dreadmaw", "Prismabasher", "Autarch Mammoth", "Hologram Stalker", "Great Oak Guardian", "Lashwhip Predator",
            # 2C (6)
            "Itzquinth, Firstborn of Gishath", "Grumgully, the Generous", "Garna, Bloodfist of Keld", "Cactusfolk Sureshot", "Thrakkus the Butcher", "Bladewing the Risen",
        ]
    },
    "BGU": {
        "title": "BGU — ETB Value (Blink, Self-Bounce, Recursion, Ninjas & Leaves-Battlefield)",
        "colors": ["B", "G", "U"],
        "payoffs": [
            # B (6 - Leaves-battlefield/Void + Ninjas/Sneak)
            "Hymn of the Faller", "Nezumi Prowler", "Dokuchi Silencer", "Shredder's Technique", "Shredder, Unrelenting", "Voidforged Titan",
            # G (4 - Leaves-battlefield/graveyard + repeatable bounce)
            "Three Tree Scribe", "Thoughtweft Charge", "Temur Sabertooth", "Hologram Stalker",
            # U (8 - Leaves-battlefield + Blink/Bounce engines + Sneak)
            "Nephalia Smuggler", "Rescue, Pepper Potts", "Imperial Cosmographer", "Arni, Humble Scribe", "Donatello's Technique", "Meneldor, Swift Savior", "Biblioplex Kraken", "Lake-town Mariners // Gone Fishing",
            # 2C (3)
            "Risen Reef", "Lilysplash Mentor", "Ingenious Infiltrator",
        ],
        "enablers": [
            # C (3)
            "H.E.R.B.I.E. Scout Unit", "Sundering Archaic", "Transcendent Archaic",
            # B (12 - Bounce/recursion/Warp + ETB/evasive targets)
            "Etherium Pteramander", "Dream Beavers", "Pattern Buffer Preservation", "Timeline Culler", "Faller's Faithful", "Tinybones, Pocket Nuisance", "Weaponcraft Enthusiast", "Back for Seconds", "Graveshifter", "Shimmercreep", "Phyrexian Gargantua", "Black Dragon",
            # G (15 - Self-bounce/recursion + ETB targets)
            "Cenote Scout", "Wall of Blossoms", "Dundoolin Weaver", "Peerless Recycling", "Scout the City", "Rambling Possum", "Clifftop Lookout", "Under the Skin", "Elvish Regrower", "Luminollusk", "Rydia's Return", "Great Oak Guardian", "Autarch Mammoth", "Earthshaker Dreadmaw", "Prismabasher",
            # U (15 - Bounce/blink spells + cheap ETB/evasive targets)
            "Boomerang Basics", "Pteramander", "Get Out", "Test of Priorities", "Corridor Monitor", "Recalibrate", "Fear of Impostors", "Kishla Trawlers", "Rimekin Recluse", "Repulse", "Whirler Rogue", "Spikeshell Harrier", "This Town Ain't Big Enough", "Shinestriker", "Daring Waverider",
            # 2C (5)
            "Baleful Strix", "Theorix Charm", "Soul Manipulation", "Primal Witchstalker", "Back for More",
        ]
    },
    "GWU": {
        "title": "GWU — Tap/Untap Shenanigans (Becomes Tapped, Survival & Untappers)",
        "colors": ["G", "W", "U"],
        "payoffs": [
            # G (5)
            "Hemosymbic Mite", "Bramblesnap", "House Cartographer", "Defiant Survivor", "Cautious Survivor",
            # W (5)
            "Orphans of the Wheat", "Glimmer Seeker", "Lulu, Loyal Hollyphant", "Dawnstrike Vanguard", "Bounding Felidar",
            # U (4)
            "Gran-Gran", "Mechan Navigator", "Katara, Bending Prodigy", "Pestered Wellguard",
            # 2C (3)
            "Wakandan Tusker", "Captain America, Living Legend", "Veteran Beastrider",
        ],
        "enablers": [
            # G (12)
            "Coordinated Clobbering", "Oviya Pashiri, Sage Lifecrafter", "Molt Tender", "Bramblesnap", "Synchronized Charge", "Drover of the Mighty", "Fear of Exposure", "Supportive Parents", "Rambling Possum", "Emil, Vastlands Roamer", "Autarch Mammoth", "Great Oak Guardian",
            # W (11)
            "Wanderbrine Trapper", "Orphans of the Wheat", "To Arms!", "Water Tribe Rallier", "Group Project", "Guardian of the Great Door", "Protective Response", "Leo's Guidance", "Quake, Agent of S.H.I.E.L.D.", "Lulu, Loyal Hollyphant", "Bounding Felidar",
            # U (6)
            "Corridor Monitor", "We Say Thee Nay!", "Arni, Humble Scribe", "Iron Lad, Diverging Destiny", "Timeline Inquiry", "Whirler Rogue",
            # 2C (4)
            "Runic Shot", "Kiora's Follower", "Captain America, Living Legend", "Veteran Beastrider",
        ]
    },
    "GUR": {
        "title": "GUR — Multicolor & Primordials (Domain, Converge, Vivid & Elementals)",
        "colors": ["G", "U", "R"],
        "payoffs": [
            # C (2)
            "Sundering Archaic", "Transcendent Archaic",
            # G (4)
            "Emil, Vastlands Roamer", "Luminollusk", "Prismabasher", "Snarl Song",
            # U (5)
            "Evasive Action", "Sweep the Skies", "Tanufel Rimespeaker", "Shinestriker", "Cloak and Phaser",
            # R (3)
            "Flamebraider", "Tribal Flames", "Squawkroaster",
            # 2C (4)
            "Eclipsed Flamekin", "Twinflame Travelers", "Risen Reef", "Glister Bairn",
        ],
        "enablers": [
            # Lands (15 - listed separately in stats if needed, included here for fixing count)
            "Vivid Meadow", "Vivid Creek", "Vivid Marsh", "Vivid Crag", "Vivid Grove",
            "Arcane Sanctum", "Crumbling Necropolis", "Savage Lands", "Jungle Shrine", "Seaside Citadel",
            "Mystic Monastery", "Opulent Palace", "Nomad Outpost", "Frontier Bivouac", "Sandsteppe Citadel",
            # C (7)
            "Energybending", "Three Tree Mascot", "Definitely Not a Turtle", "H.E.R.B.I.E. Scout Unit", "Sphinx of the Guildpact", "Sundering Archaic", "Transcendent Archaic",
            # G (12)
            "Molt Tender", "Adventurous Impulse", "Cenote Scout", "Drover of the Mighty", "Explore", "House Cartographer", "Bramblesnap", "Supportive Parents", "Clifftop Lookout", "Zimone's Experiment", "Luminollusk", "Prismabasher",
            # U (4)
            "Rimekin Recluse", "Tanufel Rimespeaker", "Gigastorm Titan", "Shinestriker",
            # R (3)
            "Flamebraider", "Squawkroaster", "Living Lightning",
            # 2C (5)
            "Skyserpent Seeker", "Wreck and Rebuild", "Eclipsed Flamekin", "Twinflame Travelers", "Risen Reef",
        ]
    },
    "UBR": {
        "title": "UBR — Discard & Looting (Madness, Mayhem & Cycling)",
        "colors": ["U", "B", "R"],
        "payoffs": [
            # C (1)
            "Containment Construct",
            # U (6)
            "Obsessive Search", "Recalibrate", "Scrounging Skyray", "Circular Logic", "Teo, Spirited Glider", "Ominous Sphinx",
            # B (6)
            "Asylum Visitor", "Big Game Hunter", "Tinybones, Pocket Nuisance", "Sandman's Quicksand", "Sadistic Slash", "Haunted Dead",
            # R (7)
            "Marauding Mako", "Blazing Rootwalla", "Hobgoblin, Mantled Marauder", "Fiery Temper", "Violent Eruption", "Mad Ratter", "Raging Goblinoids",
            # 2C (3)
            "Lazotep Chancellor", "Scarlet Spider, Kaine", "Azra Oddsmaker",
        ],
        "enablers": [
            # U (11)
            "Gran-Gran", "Hypnotic Grifter", "Mechan Navigator", "Scrounging Skyray", "Muse Seeker", "Atlantean Skirmisher", "Arni, Humble Scribe", "Thirst for Knowledge", "Teo, Spirited Glider", "Timeline Inquiry", "Cloak and Phaser",
            # B (8)
            "Bone Shards", "Intimidation Tactics", "Iron-Shield Elf", "Dokuchi Silencer", "Bitter Triumph", "Tinybones, Pocket Nuisance", "Armix, Filigree Thrasher", "Haunted Dead",
            # R (7)
            "Marauding Mako", "Lightning Axe", "Greasewrench Goblin", "Boundary Lands Ranger", "Goblin Lore", "Charging Strifeknight", "Slice and Dice",
            # 2C (3)
            "Ecstatic Electromancer", "Scarlet Spider, Kaine", "Azra Oddsmaker",
        ]
    },
    "URW": {
        "title": "URW — Spellslinger & Second Spell (Prowess / Flurry / Opus)",
        "colors": ["U", "R", "W"],
        "payoffs": [
            # U (9)
            "Pteramander", "Geist of Saint Thalia", "Muse Seeker", "Etherium Spinner", "Wingblade Disciple", "Tanufel Rimespeaker", "Traxos, Academy Guardian", "Gigastorm Titan", "Daring Waverider",
            # R (8)
            "Monastery Swiftspear", "Young Pyromancer", "Electrostatic Infantry", "Thunderdrum Soloist", "Firespitter Whelp", "Reckless Bushwhacker", "Living Lightning", "Ravenous Cosmozoan",
            # W (4)
            "Monk of the Open Hand", "Seeker of the Way", "Quake, Agent of S.H.I.E.L.D.", "Sunstar Lightsmith",
            # 2C (5)
            "Station Monitor", "Sprite Dragon", "Slick Sequence", "Ecstatic Electromancer", "Thor Odinson",
        ],
        "enablers": [
            # C (1)
            "Energybending",
            # U (13 - 1-mana spells, cantrips, rebound, cost-reduced/adventure/free spells, spell recursion)
            "Gran-Gran", "Boomerang Basics", "Distortion Strike", "Obsessive Search", "Miscast", "Spell Snare", "Stern Scolding", "Rapid Hybridization", "Geist of Saint Thalia", "Recalibrate", "Test of Priorities", "Donatello's Technique", "Kishla Trawlers", "Repulse", "This Town Ain't Big Enough", "Lake-town Mariners // Gone Fishing",
            # R (15 - 1-mana spells, cantrips, rebound, adventure, warp, surge, discover)
            "Triumphant Chomp", "Lightning Axe", "Impolite Entrance", "Fire Magic", "Reckless Rage", "Plasma Bolt", "Playful Shove", "Invigorated Rampage", "Staggershock", "Reckless Bushwhacker", "Memorial Team Leader", "Glóin the Mighty // Easy Pickings", "Geological Appraiser", "Bolt Bend", "Fang Dragon // Forktail Sweep",
            # W (9 - 1-mana spells, cantrips, adventure, rebound)
            "Defiant Strike", "Cheeky House-Mouse // Squeak By", "Unwanted Remake", "You're Not Alone", "Enter the Avatar State", "Lay Down Arms", "Joust Through", "To Arms!", "That's Rough Buddy", "Great Teacher's Decree",
            # 2C (3)
            "Stand // Deliver", "Slick Sequence", "Hero of the Nyxborn",
        ]
    },
    "RGW": {
        "title": "RGW — Go Wide (Tokens, Creature Count & Team Pump)",
        "colors": ["R", "G", "W"],
        "payoffs": [
            # C (1)
            "Sanctuary Raptor",
            # R (7)
            "Phoenix Chick", "Freedom Fighter Recruit", "Zurgo's Vanguard", "Dinosaur Stampede", "Reckless Bushwhacker", "Memorial Team Leader", "Witchstalker Frenzy",
            # G (8)
            "Oviya Pashiri, Sage Lifecrafter", "Woodland Champion", "Dundoolin Weaver", "Thornfist Striker", "Bristlebane Outrider", "Elegant Entourage", "Rydia's Return", "Prismabasher", "Great Oak Guardian",
            # W (11)
            "You're Not Alone", "Orphans of the Wheat", "Guardian of the Great Door", "Collision Course", "Falcon, Joaquin Torres", "Goldnight Commander", "Great Teacher's Decree", "Plated Onslaught", "Syr Alin, the Lion's Claw", "Bounding Felidar", "Dawnstrike Vanguard", "The Crystal's Chosen",
            # 2C (7)
            "Sunblade Elf", "Frontline Rush", "Hero of the Nyxborn", "Grumgully, the Generous", "Veteran Beastrider", "Sun Warriors", "Maja, Bretagard Protector",
        ],
        "enablers": [
            # R (5)
            "Young Pyromancer", "Zurgo's Vanguard", "Hordeling Outburst", "Reckless Bushwhacker", "Mad Ratter",
            # G (8)
            "Oviya Pashiri, Sage Lifecrafter", "Defiant Survivor", "Under the Skin", "Call of the Herd", "Emil, Vastlands Roamer", "Spore Swarm", "Snarl Song", "Autarch Mammoth",
            # W (11)
            "Cheeky House-Mouse // Squeak By", "Invasion Reinforcements", "Group Project", "Battle Menu", "Glimmer Seeker", "Dalkovan Packbeasts", "Dewdrop Cure", "Release the Dogs", "Dragonback Lancer", "Spectral Procession", "The Crystal's Chosen",
            # 2C (5)
            "Frontline Rush", "Hero of the Nyxborn", "Sun Warriors", "Maja, Bretagard Protector", "Old Hob, Alleycat Blues",
        ]
    },
    "RWB": {
        "title": "RWB — Sacrifice & Aristocrats (Mobilize, Sac Outlets & Death Triggers)",
        "colors": ["R", "W", "B"],
        "payoffs": [
            # R (4)
            "Plasma Bolt", "Slumbering Cerberus", "Spiteful Prankster", "Brimstone Volley",
            # W (7)
            "Ruin-Lurker Bat", "Daxos, Blessed by the Sun", "Furious Forebear", "That's Rough Buddy", "Vengeful Townsfolk", "Lulu, Loyal Hollyphant", "G'raha Tia",
            # B (7)
            "Cult Conscript", "Hymn of the Faller", "Morbid Opportunist", "Arnyn, Deathbloom Botanist", "Sanguinary Priest", "Voidforged Titan", "Death-Rattle Oni",
            # 2C (3)
            "Elas il-Kor, Sadistic Pilgrim", "Denethor, Ruling Steward", "Garna, Bloodfist of Keld",
        ],
        "enablers": [
            # C (1)
            "Definitely Not a Turtle",
            # R (9)
            "Phoenix Chick", "Fiery Conclusion", "Young Pyromancer", "Zurgo's Vanguard", "Hordeling Outburst", "Snowslope Hunter", "Memorial Team Leader", "Mad Ratter", "Hurler Cyclops",
            # W (12)
            "Market Gnome", "Invasion Reinforcements", "Duty Beyond Death", "Furious Forebear", "Group Project", "Dalkovan Packbeasts", "Glorifier of Suffering", "Dewdrop Cure", "Release the Dogs", "Dragonback Lancer", "Destined Confrontation", "Spectral Procession",
            # B (14)
            "Carrion Feeder", "Bone Shards", "Village Rites", "Cult Conscript", "Umbral Collar Zealot", "Wriggling Grub", "Timeline Culler", "Plumb the Forbidden", "Weaponcraft Enthusiast", "Back for Seconds", "Foul-Tongue Invocation", "Salt Road Skirmish", "Barter in Blood", "Haunted Dead",
            # 2C (8)
            "Frontline Rush", "Callous Sell-Sword // Burn Together", "Denethor, Ruling Steward", "Lingering Souls", "Hero of the Nyxborn", "Social Snub", "Sun Warriors", "Old Hob, Alleycat Blues",
        ]
    }
}

print(f"{'Theme':<6} | {'Payoffs':<7} | {'Enablers':<8} | {'Unique (No Lands)':<17} | {'Payoff Colors':<30} | {'Enabler Colors (No Lands)':<30}")
print("-" * 115)
for t_key, t_data in THEMES.items():
    p_cards = [card_map[n] for n in t_data["payoffs"]]
    e_cards = [card_map[n] for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]
    u_names = list(dict.fromkeys(t_data["payoffs"] + [n for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]))
    u_cards = [card_map[n] for n in u_names]

    p_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in p_cards)
    e_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in e_cards)
    p_str = " ".join(f"{k}:{v}" for k, v in sorted(p_ci.items(), key=lambda x: (len(x[0]), x[0])))
    e_str = " ".join(f"{k}:{v}" for k, v in sorted(e_ci.items(), key=lambda x: (len(x[0]), x[0])))
    print(f"{t_key:<6} | {len(p_cards):<7} | {len(e_cards):<8} | {len(u_cards):<17} | {p_str:<30} | {e_str:<30}")

print("\nMANA CURVES (Payoffs / Enablers / Combined Unique Nonland):")
for t_key, t_data in THEMES.items():
    p_cards = [card_map[n] for n in t_data["payoffs"]]
    e_cards = [card_map[n] for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]
    u_names = list(dict.fromkeys(t_data["payoffs"] + [n for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]))
    u_cards = [card_map[n] for n in u_names]
    
    def curve_str(clist):
        cnt = Counter(min(6, max(1, int(c["cmc"]))) for c in clist)
        return " ".join(f"{mv}{'+' if mv==6 else ''}:{cnt.get(mv,0)}" for mv in range(1, 7))
    
    print(f"  {t_key}: P=[{curve_str(p_cards)}] | E=[{curve_str(e_cards)}] | All=[{curve_str(u_cards)}]")

