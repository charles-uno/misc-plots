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
    "grizzly fate": {"name": "Grizzly Fate", "mana_cost": "{3}{G}{G}", "cmc": 5, "type_line": "Sorcery", "oracle_text": "Create two 2/2 green Bear creature tokens.\nThreshold — Create four 2/2 green Bear creature tokens instead if seven or more cards are in your graveyard.\nFlashback {5}{G}{G}", "color_identity": ["G"], "power": None, "toughness": None},
    "hero of the nyxborn": {"name": "Hero of the Nyxborn", "mana_cost": "{1}{R}{W}", "cmc": 3, "type_line": "Enchantment Creature — Human Soldier", "oracle_text": "When Hero of the Nyxborn enters, create a 1/1 white Human Soldier creature token.\nWhenever you cast a spell that targets Hero of the Nyxborn, creatures you control get +1/+0 until end of turn.", "color_identity": ["R", "W"], "power": "2", "toughness": "2"}
}
by_name.update(manual)

with open("uncommons-cube/list-nov5.txt") as f:
    raw_lines = [line.strip() for line in f if line.strip()]

unique_cards = [by_name[norm(l)] for l in raw_lines]
card_map = {c["name"]: c for c in unique_cards}

THEMES = {
    "WUB": {
        "title": "WUB — Thopters & Artifact Creatures (Affinity / Artifacts Matter)",
        "colors": ["W", "U", "B"],
        "payoffs": [
            # W (5)
            "Command Subadjunct", "Mandible Justiciar", "Paladin Danse, Steel Maverick", "Guidelight Synergist", "Plated Onslaught",
            # U (5)
            "Rescue, Pepper Potts", "Iron Lad, Diverging Destiny", "Thirst for Knowledge", "Whirler Rogue", "Valkyrie Aerial Unit",
            # B (5)
            "Etherium Pteramander", "Armix, Filigree Thrasher", "Arcbound Condor", "Pactdoll Terror", "Monoist Circuit-Feeder",
            # 2C (1)
            "Ethersworn Sphinx",
        ],
        "enablers": [
            # C (5)
            "Containment Construct", "Afterthought Sentry", "H.E.R.B.I.E. Scout Unit", "Traxos, Scourge Eternal", "Sphinx of the Guildpact",
            # W (9)
            "Command Subadjunct", "Market Gnome", "Sundial, Dawn Tyrant", "Attentive Sunscribe", "Mandible Justiciar", "Paladin Danse, Steel Maverick", "Hologram Janeway", "Guidelight Synergist", "Triplicate Spirits",
            # U (12)
            "Corridor Monitor", "Rescue, Pepper Potts", "Sweep the Skies", "Etherium Spinner", "Iron Lad, Diverging Destiny", "Rune-Sealed Wall", "Wingblade Disciple", "Launch Mishap", "Whirler Rogue", "Traxos, Academy Guardian", "Spikeshell Harrier", "Valkyrie Aerial Unit",
            # B (13)
            "Etherium Pteramander", "Monoist Sentry", "Ashnod's Harvester", "Osseous Sticktwister", "Wretched Doll", "MACH-1, Swooping Scoundrel", "Armix, Filigree Thrasher", "Flayed One", "Arcbound Condor", "Haunted Dead", "Pactdoll Terror", "Monoist Circuit-Feeder", "Voidforged Titan",
            # 2C (5)
            "Station Monitor", "Baleful Strix", "Lingering Souls", "Shuri, Vibranium Technologist", "Ethersworn Sphinx",
        ]
    },
    "WBG": {
        "title": "WBG — Lifegain & Drain",
        "colors": ["W", "B", "G"],
        "payoffs": [
            # W (5)
            "Ajani's Pridemate", "Angel of Vitality", "Doctor Jane Foster", "Star Charter", "Glorious Enforcer",
            # B (4)
            "Nightmare's Thirst", "MACH-1, Swooping Scoundrel", "Bloodthirsty Aerialist", "Foolish Fate",
            # G (4)
            "Fortifying Draught", "Tigra, Feline Fury", "Thornfist Striker", "Titanbones, Towering Heart",
            # 2C (2)
            "Trelasarra, Moon Dancer", "Starseer Mentor",
        ],
        "enablers": [
            # W (12)
            "Market Gnome", "Enter the Avatar State", "Joust Through", "Mardu Woe-Reaper", "Distinguished Conjurer", "Mandible Justiciar", "Battle Menu", "Paladin Danse, Steel Maverick", "Spider-UK", "Katara, Heroic Healer", "Bounding Felidar", "Glorious Enforcer",
            # B (11)
            "Dissection Practice", "Nightmare's Thirst", "Ravening Warg", "Osseous Sticktwister", "Mire Triton", "Cabal Initiate", "Foul-Tongue Invocation", "Flayed One", "Thrasher Brute", "Pactdoll Terror", "Sanguinary Priest",
            # G (8)
            "Virulent Emissary", "Fortifying Draught", "Eumidian Terrabotanist", "Devouring Tendrils", "Scout the City", "Luminollusk", "Titanbones, Towering Heart", "Snarl Song",
            # 2C (5)
            "Elas il-Kor, Sadistic Pilgrim", "Denethor, Ruling Steward", "Leyline Prowler", "Atlas, Sizable Stooge", "Wakandan Tusker",
        ]
    },
    "BRG": {
        "title": "BRG — Dragons, Behemoths & Ferocious (Power 4+)",
        "colors": ["B", "R", "G"],
        "payoffs": [
            # B (5)
            "Nighthowl Pursuer", "Caustic Exhale", "Ravening Warg", "Foul-Tongue Invocation", "Fearsome Awakening",
            # R (8)
            "Triumphant Chomp", "Channeled Dragonfire", "Boundary Lands Ranger", "Tiger-Dillo", "Firespitter Whelp", "Kolaghan Warmonger", "Dinosaur Stampede", "Bolt Bend",
            # G (6)
            "Nasty Little Rabbit", "Drover of the Mighty", "Owlbear Shepherd", "Savage Stomp", "Surrak, the Hunt Caller", "Earthshaker Dreadmaw",
            # 2C (5)
            "Itzquinth, Firstborn of Gishath", "Atlas, Sizable Stooge", "Strider, Ranger of the North", "Thrakkus the Butcher", "Bladewing the Risen",
        ],
        "enablers": [
            # C (1)
            "Traxos, Scourge Eternal",
            # B (8)
            "Monoist Sentry", "Kalakscion, Hunger Tyrant", "Flayed One", "Thrasher Brute", "Voidforged Titan", "Dreadhound", "Black Dragon", "Huskburster Swarm",
            # R (12)
            "Intrepid Ace", "Tiger-Dillo", "Gila Courser", "Firespitter Whelp", "Bonded Horncrest", "Glóin the Mighty // Easy Pickings", "Memorial Team Leader", "Raging Goblinoids", "Vaultguard Trooper", "Territorial Bruntar", "Dracosaur Auxiliary", "Rorix Bladewing",
            # G (16)
            "Patchwork Beastie", "Splinterfright", "Call of the Herd", "Surrak, the Hunt Caller", "Temur Sabertooth", "Titanbones, Towering Heart", "Elvish Regrower", "Hazard of the Dunes", "Terrian, World Tyrant", "Territory Culler", "Needletooth Pack", "Earthshaker Dreadmaw", "Prismabasher", "Autarch Mammoth", "Hologram Stalker", "Lashwhip Predator",
            # 2C (6)
            "Itzquinth, Firstborn of Gishath", "Garna, Bloodfist of Keld", "Atlas, Sizable Stooge", "Strider, Ranger of the North", "Thrakkus the Butcher", "Bladewing the Risen",
        ]
    },
    "BGU": {
        "title": "BGU — Stocked Graveyard (Threshold, Delirium, Undergrowth & Leaves-GY)",
        "colors": ["B", "G", "U"],
        "payoffs": [
            # B (5)
            "Cabal Initiate", "Osseous Sticktwister", "Graveblade Marauder", "Dreadhound", "Huskburster Swarm",
            # G (9)
            "Patchwork Beastie", "Stubborn Burrowfiend", "Kraul Harpooner", "Coati Scavenger", "Splinterfright", "Undercity Upheaval", "Grizzly Fate", "Hologram Stalker", "Ghoultree",
            # U (6)
            "Yuriko, Hope from the Shadows", "Shoreline Looter", "Master's Councillors", "Mindwhisker", "Picklock Prankster // Free the Fae", "Daring Waverider",
            # 2C (4)
            "Vilespawn Spider", "Dreadwing Scavenger", "Vash, Freelance Archaeologist", "Recursive Recruitment",
        ],
        "enablers": [
            # B (10)
            "Stitcher's Supplier", "Test of Loyalty", "Umbral Collar Zealot", "Mire Triton", "Wretched Doll", "MACH-1, Swooping Scoundrel", "Flayed One", "Nightblade Brigade", "Gathering of Darkness", "Dreadhound",
            # G (12)
            "Cenote Scout", "Molt Tender", "Patchwork Beastie", "Stubborn Burrowfiend", "Scout the City", "Marwyn, the Preserver", "Splinterfright", "Peerless Recycling", "Elvish Regrower", "Rite of Renewal", "Territory Culler", "Hologram Stalker",
            # U (13)
            "Cobbled Lancer", "Yuriko, Hope from the Shadows", "Hypnotic Grifter", "Shoreline Looter", "Picklock Prankster // Free the Fae", "Master's Councillors", "Test of Priorities", "Fear of Impostors", "Rune-Sealed Wall", "Mindwhisker", "Confounding Riddle", "Chemister's Insight", "Valkyrie Aerial Unit",
            # 2C (6)
            "Skull Prophet", "Vilespawn Spider", "Theorix Charm", "Primal Witchstalker", "Dreadwing Scavenger", "Vash, Freelance Archaeologist",
        ]
    },
    "GWU": {
        "title": "GWU — Blink, Self-Bounce & ETB / Leaves-Battlefield Value",
        "colors": ["G", "W", "U"],
        "payoffs": [
            # G (3)
            "Three Tree Scribe", "Rambling Possum", "Temur Sabertooth",
            # W (6)
            "That's Rough Buddy", "Distinguished Conjurer", "Shepherd of the Flock // Usher to Safety", "Stonecloaker", "Against All Odds", "Spider-UK",
            # U (6)
            "Nephalia Smuggler", "Rescue, Pepper Potts", "Imperial Cosmographer", "Rimekin Recluse", "Meneldor, Swift Savior", "Biblioplex Kraken",
            # 2C (3)
            "Soulherder", "Lilysplash Mentor", "Spider-Man India",
        ],
        "enablers": [
            # C (3)
            "H.E.R.B.I.E. Scout Unit", "Sundering Archaic", "Transcendent Archaic",
            # G (8)
            "Cenote Scout", "Clifftop Lookout", "Coati Scavenger", "Elvish Regrower", "Luminollusk", "Autarch Mammoth", "Earthshaker Dreadmaw", "Prismabasher",
            # W (8)
            "Wall of Omens", "Resolute Reinforcements", "Kinjalli's Dawnrunner", "Doctor Jane Foster", "Okoye, Dora Milaje Leader", "Star Charter", "Githzerai Monk", "Katara, Heroic Healer",
            # U (12)
            "Boomerang Basics", "Corridor Monitor", "Get Out", "Recalibrate", "Test of Priorities", "Fear of Impostors", "Whirler Rogue", "Spikeshell Harrier", "This Town Ain't Big Enough", "Lake-town Mariners // Gone Fishing", "Shinestriker", "Daring Waverider",
            # 2C (4)
            "Woodland Acolyte // Mend the Wilds", "Shuri, Vibranium Technologist", "Paradox Surveyor", "Spider-Man India",
        ]
    },
    "GUR": {
        "title": "GUR — Multicolor, Landfall & Big MV (Domain, Converge, Vivid, Landfall & MV 4+)",
        "colors": ["G", "U", "R"],
        "payoffs": [
            # C (2)
            "Sundering Archaic", "Transcendent Archaic",
            # G (6)
            "Eumidian Terrabotanist", "Emil, Vastlands Roamer", "Luminollusk", "Territory Culler", "Prismabasher", "Snarl Song",
            # U (8)
            "Muse Seeker", "Evasive Action", "Sweep the Skies", "Etherium Spinner", "Elven Raft-Steerer", "Tanufel Rimespeaker", "Shinestriker", "Cloak and Phaser",
            # R (5)
            "Thunderdrum Soloist", "Tribal Flames", "Superior Foes of Spider-Man", "Squawkroaster", "Territorial Bruntar",
            # 2C (6)
            "Paradox Surveyor", "Flaring Cinder", "Spectacular Skywhale", "Radha, Coalition Warlord", "Strider, Ranger of the North", "Glister Bairn",
        ],
        "enablers": [
            # Lands (15)
            "Vivid Meadow", "Vivid Creek", "Vivid Marsh", "Vivid Crag", "Vivid Grove",
            "Arcane Sanctum", "Crumbling Necropolis", "Savage Lands", "Jungle Shrine", "Seaside Citadel",
            "Mystic Monastery", "Opulent Palace", "Nomad Outpost", "Frontier Bivouac", "Sandsteppe Citadel",
            # C (4)
            "Energybending", "Definitely Not a Turtle", "H.E.R.B.I.E. Scout Unit", "Sphinx of the Guildpact",
            # G (12)
            "Molt Tender", "Adventurous Impulse", "Cenote Scout", "Drover of the Mighty", "Explore", "House Cartographer", "Marwyn, the Preserver", "White Tiger, Amulet Keeper", "Clifftop Lookout", "Supportive Parents", "Zimone's Experiment", "Lashwhip Predator",
            # U (9)
            "Omen Hawker", "Sweep the Skies", "Traxos, Academy Guardian", "Swat Away", "Gigastorm Titan", "This Town Ain't Big Enough", "Lake-town Mariners // Gone Fishing", "Valkyrie Aerial Unit", "Cloak and Phaser",
            # R (6)
            "Fire Magic", "Channeled Dragonfire", "Bolt Bend", "Stoke the Flames", "Witchstalker Frenzy", "Winter, Team Player",
            # 2C (3)
            "Skyserpent Seeker", "Wreck and Rebuild", "Paradox Surveyor",
        ]
    },
    "UBR": {
        "title": "UBR — Discard & Looting (Madness, Mayhem, Cycling & Jump-Start)",
        "colors": ["U", "B", "R"],
        "payoffs": [
            # C (1)
            "Containment Construct",
            # U (6)
            "Obsessive Search", "Recalibrate", "Scrounging Skyray", "Circular Logic", "Teo, Spirited Glider", "Ominous Sphinx",
            # B (5)
            "Asylum Visitor", "Sandman's Quicksand", "Gisa's Bidding", "Haunted Dead", "Sadistic Slash",
            # R (6)
            "Marauding Mako", "Blazing Rootwalla", "Hobgoblin, Mantled Marauder", "Violent Eruption", "Mad Ratter", "Raging Goblinoids",
            # 2C (3)
            "Lazotep Chancellor", "Scarlet Spider, Kaine", "Azra Oddsmaker",
        ],
        "enablers": [
            # U (8)
            "Hypnotic Grifter", "Shoreline Looter", "Muse Seeker", "Scrounging Skyray", "Thirst for Knowledge", "Chemister's Insight", "Teo, Spirited Glider", "Cloak and Phaser",
            # B (7)
            "Bone Shards", "Intimidation Tactics", "Cabal Initiate", "Iron-Shield Elf", "Bitter Triumph", "Armix, Filigree Thrasher", "Haunted Dead",
            # R (9)
            "Marauding Mako", "Greasewrench Goblin", "Lightning Axe", "Boundary Lands Ranger", "Goblin Lore", "Charging Strifeknight", "Reckless Racer", "Vaultguard Trooper", "Slice and Dice",
            # 2C (5)
            "Dreadwing Scavenger", "Ecstatic Electromancer", "Flaring Cinder", "Scarlet Spider, Kaine", "Azra Oddsmaker",
        ]
    },
    "URW": {
        "title": "URW — Spellslinger & Second Spell (Prowess / Flurry / Opus)",
        "colors": ["U", "R", "W"],
        "payoffs": [
            # U (9)
            "Pteramander", "Geist of Saint Thalia", "Muse Seeker", "Etherium Spinner", "Wingblade Disciple", "Tanufel Rimespeaker", "Traxos, Academy Guardian", "Gigastorm Titan", "Daring Waverider",
            # R (10)
            "Monastery Swiftspear", "Thermo-Alchemist", "Electrostatic Infantry", "Thunderdrum Soloist", "Young Pyromancer", "Firespitter Whelp", "Superior Foes of Spider-Man", "Reckless Bushwhacker", "Living Lightning", "Winter, Team Player",
            # W (5)
            "Monk of the Open Hand", "Seeker of the Way", "Danitha, Sword of Hope", "Quake, Agent of S.H.I.E.L.D.", "Sunstar Lightsmith",
            # 2C (8)
            "Station Monitor", "Sprite Dragon", "Slick Sequence", "Ecstatic Electromancer", "Flaring Cinder", "Hero of the Nyxborn", "Spectacular Skywhale", "Thor Odinson",
        ],
        "enablers": [
            # C (1)
            "Energybending",
            # U (14)
            "Boomerang Basics", "Distortion Strike", "Obsessive Search", "Miscast", "Spell Snare", "Stern Scolding", "Rapid Hybridization", "Picklock Prankster // Free the Fae", "Geist of Saint Thalia", "Recalibrate", "Test of Priorities", "Donatello's Technique", "This Town Ain't Big Enough", "Lake-town Mariners // Gone Fishing",
            # R (15)
            "Triumphant Chomp", "Channeled Dragonfire", "Lightning Axe", "Impolite Entrance", "Fire Magic", "Reckless Rage", "Invigorated Rampage", "Team Tactics", "Staggershock", "Reckless Bushwhacker", "Memorial Team Leader", "Glóin the Mighty // Easy Pickings", "Geological Appraiser", "Bolt Bend", "Stoke the Flames",
            # W (10)
            "Defiant Strike", "Cheeky House-Mouse // Squeak By", "Shepherd of the Flock // Usher to Safety", "Unwanted Remake", "Enter the Avatar State", "Purify the Grave", "To Arms!", "That's Rough Buddy", "Prismatic Ending", "Great Teacher's Decree",
            # 2C (2)
            "Slick Sequence", "Hero of the Nyxborn",
        ]
    },
    "RGW": {
        "title": "RGW — Tap/Untap Shenanigans (Becomes Tapped, Survival, Saddle, Convoke & Teamwork)",
        "colors": ["R", "G", "W"],
        "payoffs": [
            # R (4)
            "Reckless Racer", "Gila Courser", "Vaultguard Trooper", "Dracosaur Auxiliary",
            # G (7)
            "Hemosymbic Mite", "Bramblesnap", "House Cartographer", "Stubborn Burrowfiend", "Defiant Survivor", "Rambling Possum", "Autarch Mammoth",
            # W (4)
            "Attentive Sunscribe", "Spider-UK", "Unswerving Sloth", "Bounding Felidar",
            # 2C (5)
            "Wakandan Tusker", "Veteran Beastrider", "Radha, Coalition Warlord", "Sami, Ship's Engineer", "Spider-Man India",
        ],
        "enablers": [
            # R (7)
            "Intrepid Ace", "Channeled Dragonfire", "Team Tactics", "Gila Courser", "Stoke the Flames", "Winter, Team Player", "Dracosaur Auxiliary",
            # G (11)
            "Coordinated Clobbering", "Molt Tender", "Bramblesnap", "Stubborn Burrowfiend", "Synchronized Charge", "Drover of the Mighty", "Supportive Parents", "Rambling Possum", "Emil, Vastlands Roamer", "Storm the Seedcore", "Autarch Mammoth",
            # W (11)
            "Wanderbrine Trapper", "To Arms!", "Water Tribe Rallier", "Group Project", "Leo's Guidance", "Protective Response", "Quake, Agent of S.H.I.E.L.D.", "Spider-UK", "Unswerving Sloth", "Bounding Felidar", "Triplicate Spirits",
            # 2C (3)
            "Worf, Honor-Bound Warrior", "Veteran Beastrider", "Spider-Man India",
        ]
    },
    "RWB": {
        "title": "RWB — Go-Wide Fighters (Warriors, Soldiers, Knights, 1/1 Tokens & Aristocrats)",
        "colors": ["R", "W", "B"],
        "payoffs": [
            # R (7)
            "Freedom Fighter Recruit", "Reckless Bushwhacker", "Zurgo's Vanguard", "Dinosaur Stampede", "Memorial Team Leader", "Witchstalker Frenzy", "Winter, Team Player",
            # W (8)
            "Mardu Woe-Reaper", "Venerable Knight", "Water Tribe Rallier", "Hologram Janeway", "Spider-UK", "Okoye, Dora Milaje Leader", "Great Teacher's Decree", "Katara, Heroic Healer", "The Crystal's Chosen",
            # B (5)
            "Carrion Feeder", "Blood-Chin Rager", "Belle of the Brawl", "Thrasher Brute", "Sanguinary Priest",
            # 2C (8)
            "Chief of the Edge", "Rushblade Commander", "Elas il-Kor, Sadistic Pilgrim", "Worf, Honor-Bound Warrior", "Denethor, Ruling Steward", "Kargan Warleader", "Hero of the Nyxborn", "Garna, Bloodfist of Keld",
        ],
        "enablers": [
            # R (13)
            "Young Pyromancer", "Betrayer's Bargain", "Charging Strifeknight", "Kolaghan Warmonger", "Reckless Bushwhacker", "Snowslope Hunter", "Zurgo's Vanguard", "Hordeling Outburst", "Glóin the Mighty // Easy Pickings", "Memorial Team Leader", "Mad Ratter", "Vaultguard Trooper", "Winter, Team Player",
            # W (19)
            "Market Gnome", "Mardu Woe-Reaper", "Venerable Knight", "Usher of the Fallen", "Ajani's Pridemate", "Seeker of the Way", "Water Tribe Rallier", "Resolute Reinforcements", "Battle Menu", "Group Project", "Danitha, Sword of Hope", "Paladin Danse, Steel Maverick", "Dalkovan Packbeasts", "Dewdrop Cure", "Okoye, Dora Milaje Leader", "Destined Confrontation", "Katara, Heroic Healer", "Triplicate Spirits", "The Crystal's Chosen",
            # B (18)
            "Carrion Feeder", "Scorn-Blade Berserker", "Bone Shards", "Village Rites", "Killing Wave", "Iron-Shield Elf", "Umbral Collar Zealot", "Plumb the Forbidden", "Blood-Chin Rager", "Belle of the Brawl", "Graveblade Marauder", "Nightblade Brigade", "Bleeding Edge", "Thrasher Brute", "Haunted Dead", "Barter in Blood", "Salt Road Skirmish", "Voidforged Titan",
            # 2C (9)
            "Chief of the Edge", "Rushblade Commander", "Worf, Honor-Bound Warrior", "Denethor, Ruling Steward", "Lingering Souls", "Kargan Warleader", "Hero of the Nyxborn", "Garna, Bloodfist of Keld", "Thor Odinson",
        ]
    }
}

for tk, td in THEMES.items():
    for role in ("payoffs", "enablers"):
        for n in td[role]:
            if n not in card_map:
                print(f"MISSING in {tk} {role}: {n}")

print(f"{'Theme':<6} | {'Payoffs':<7} | {'Enablers':<8} | {'Unique (No Lands)':<17} | {'Payoff Colors':<32} | {'Enabler Colors (No Lands)':<32}")
print("-" * 120)
for t_key, t_data in THEMES.items():
    p_cards = [card_map[n] for n in t_data["payoffs"]]
    e_cards = [card_map[n] for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]
    u_names = list(dict.fromkeys(t_data["payoffs"] + [n for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]))
    u_cards = [card_map[n] for n in u_names]

    p_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in p_cards)
    e_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in e_cards)
    p_str = " ".join(f"{k}:{v}" for k, v in sorted(p_ci.items(), key=lambda x: (len(x[0]), x[0])))
    e_str = " ".join(f"{k}:{v}" for k, v in sorted(e_ci.items(), key=lambda x: (len(x[0]), x[0])))
    print(f"{t_key:<6} | {len(p_cards):<7} | {len(e_cards):<8} | {len(u_cards):<17} | {p_str:<32} | {e_str:<32}")
