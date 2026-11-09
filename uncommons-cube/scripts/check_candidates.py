import json
import re

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

check_names = [
    # RGW Go Wide
    "Battle Cry Goblin", "Hordeling Outburst", "Stoke the Flames",
    "Get a Leg Up", "Imperious Perfect", "Overrun", "Overwhelm", "Scatter the Seeds", "Sprout Swarm",
    "Raise the Alarm", "Starry-Eyed Skyrider", "Goldnight Commander", "Cloudgoat Ranger",
    "Targ Nar, Demon-Fang Gnoll", "Queen Allenal of Ruadach", "Heroic Reinforcements",
    # RGW Tap/Untap
    "Gila Courser", "Reckless Velocitaur", "Dracosaur Auxiliary",
    "Hemosymbic Mite", "Rambling Possum", "Autarch Mammoth",
    "Canyon Vaulter", "Savior of the Small", "Bounding Felidar", "Dawnstrike Vanguard",
    "Radha, Coalition Warlord", "Shrewd Storyteller", "Sami, Ship's Engineer",
    # RGW Dragons / Behemoths
    "Firespitter Whelp", "Bolt Bend", "Kiora of Fire and Ashes", "Sarkhan's Triumph", "Dragon's Fire", "Spit Flame",
    "Nasty Little Rabbit", "Moon-Boy, Dino Rider", "Wilderland Scrounger", "Ghalta the Unstoppable", "Goreclaw, Terror of Qal Sisma", "Garruk's Uprising", "migratory greathorn", "Topiary Stomper", "Drover of the Mighty", "Otepec Huntmaster", "Knight of the Stampede",
    "Kinjalli's Caller", "Osseous Exhale", "Dragon's Disciple", "Majestic Heliopterus", "Imperial Aerosaur", "Cherished Hatchling", "Pterodon Knight",
    "Ruby, Daring Tracker", "Thrakkus the Butcher", "Itzquinth, Firstborn of Gishath", "Atzocan Seer", "Enduring Scalelord", "Swathcutter Giant", "Relentless Raptor", "Sky Terror",
    # RWB Little Guys
    "Sneaking Guide", "Irreverent Gremlin", "Subira, Tulzidi Caravanner", "Underfoot Underdogs",
    "Helping Hand", "Neighborhood Guardian", "Scout for Survivors", "Savior of the Small", "Sun-Blessed Healer",
    "Fatal Push", "Eliminate", "Slimy Dualleech", "No One Left Behind", "Unearth", "Call of the Death-Dweller",
    "Arabella, Abandoned Doll", "Wispdrinker Vampire", "Balduvian Atrocity",
    # RWB Goblins / Fey
    "Goblin Negotiation", "General Kreat, the Boltbringer", "Volley Veteran", "Hordeling Outburst", "Battle Cry Goblin",
    "Goldmeadow Stalwart", "Wizened Cenn", "Cloudgoat Ranger", "Kinsbaile Aspirant", "Thoughtweft Imbuer",
    "Mudbutton Cursetosser", "Miara, Thorn of the Glade", "Marsh Flitter", "Sling-Gang Lieutenant", "Weirding Shaman",
    "Frontline Rush", "Giott, King of the Dwarves", "Lingering Souls", "Baron Bertram Graywater", "Boggart Cursecrafter", "Munitions Expert",
    # RWB Sacrifice / Aristocrats
    "Goblin Bombardment", "Reinforced Ronin", "Makeshift Munitions", "Mayhem Devil", "Lagomos, Hand of Hatred", "Juri, Master of the Revue", "Weaponize the Monsters", "Reckless Abandon", "Fling", "Collateral Damage", "Village Rites", "Corrupted Conviction", "Deadly Dispute",
    "Zulaport Cutthroat", "Gravelighter", "Syr Konrad, the Grim", "Venerated Stormsinger", "Morbid Opportunist", "Blood Artist", "Vindictive Vampire",
    "Garrison Warden", "Ministrant of Obligation", "Faramir, Field Commander", "Duty Beyond Death", "Nested Shambler",
    "Garna, Bloodfist of Keld", "Hardened Tactician", "Elas il-Kor, Sadistic Pilgrim", "Cruel Celebrant", "Hidden Stockpile", "Rite of Oblivion",
    # RWB Undead
    "Voldaren Ambusher", "Rakish Heir", "Dreadhorde Twins", "Markov Retribution", "Gut, True Soul Zealot", "Falkenrath Perforator", "Bloodcrazed Neonate", "Insolent Neonate",
    "Duskborne Skymarcher", "Clarion Spirit", "Mausoleum Guard", "Unconventional Tactics", "Binding Mummy",
    "Indulgent Aristocrat", "Archghoul of Thraben", "Bloodline Necromancer", "Carrion Feeder", "Lazotep Reaver",
    "Quintorius, Field Historian", "Legion Lieutenant", "Stromkirk Captain",
    # RWB Warriors / Fighters
    "Goma Fada Vanguard", "Zurgo's Vanguard", "Iraxxa, Empress of Mars", "Mardu Scout", "Battle-Rattle Shaman",
    "Resolute Reinforcements", "Dalkovan Packbeasts", "Okoye, Dora Milaje Leader", "Mardu Woe-Reaper", "Timely Hordemate",
    "Blood-Chin Rager", "Belle of the Brawl", "Thrasher Brute", "Mardu Skullhunter", "Merciless Executioner", "Raiders' Spoils",
    "Kargan Warleader", "Chief of the Edge", "Rushblade Commander",
    # BRG Graveyard
    "Osseous Sticktwister", "Stinging Cave Crawler", "Chupacabra Echo",
    "Dragon's Rage Channeler", "Gibbering Fiend", "Fledgling Dragon",
    "Patchwork Beastie", "Coati Scavenger", "Wickerfolk Thresher",
    "Zoyowa Lava-Tongue", "Akawalli, the Seething Tower", "Wildfire Wickerfolk",
    # BRG Morbid / Sacrifice
    "Infuse with Vitality", "Skull Prophet", "Golgari Findbroker", "Winding Constrictor", "Dina, Soul Steeper", "Ravenous Squirrel", "Cankerbloom", "Moldervine Reclamation", "Festering Gulch", "rotshambler", "tukatongue thallid", "blisterpod", "young wolf", "Brindle Shoat", "Sprouting Thrinax", " Tukatongue Thallid",
    # BRG Ferocious / Dragons
    "Nighthowl Pursuer", "Caustic Exhale", "Kalakscion, Hunger Tyrant", "Grendel, Spawn of Knull", "Carrion Grub", "Consumed by Greed", "Foul-Tongue Invocation",
    "The Chief Warg", "Bladewing the Risen", "Swift Warkite", "Savage Ventmaw",
    # GWU Tap/Untap
    "Gran-Gran", "Mechan Navigator", "Pestered Wellguard", "Fallowsage",
    "Captain America, Living Legend", "D'Vana Tendi, Optimistic Ensign", "Bounding Krasis", "Kiora's Follower",
    # GWU Proliferate
    "Wildwood Scourge", "Meltstrider Eulogist", "Michelangelo, Mutant BFF", "Evolution Sage",
    "Metastatic Evangel", "Abzan Falconer", "Dr. McCoy, Surly Surgeon", "Grateful Apparition",
    "Thrummingbird", "Flux Channeler", "Tezzeret's Gambit",
    "Botanical Brawler", "Plumecreed Mentor", "Sharktocrab"
]

for n in check_names:
    c = by_name.get(n.lower())
    if not c:
        print(f"MISSING: {n}")
    else:
        print(f"OK: {c['name']} (ci={c['color_identity']}, MV={int(c['cmc'])}, {c['rarity']}, {c['type_line']})")

