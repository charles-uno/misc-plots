import json

with open("/Users/charles/Desktop/misc-plots/uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

THEMES_V3 = [
    {
        "code": "WBG",
        "colors": ["W", "B", "G"],
        "title": "Lifegain (Infusion & Drain)",
        "note": "Fixed Theme • Incremental lifegain triggers, +1/+1 counters & drain",
        "slots": {
            "W": ["Ajani's Pridemate", "MJ, Rising Star", "Attended Healer"],
            "B": ["Starscape Cleric", "Bloodthirsty Aerialist", "Nazar, the Velvet Fang"],
            "G": ["Fortifying Draught", "Voracious Wurm", "Thornfist Striker"],
            "2C": ["Elas il-Kor, Sadistic Pilgrim", "Dina, Soul Steeper", "Trelasarra, Moon Dancer"]
        }
    },
    {
        "code": "GUR",
        "colors": ["G", "U", "R"],
        "title": "Multicolor & Primordials (Domain / Converge / Vivid)",
        "note": "Fixed Theme • Basic land types, colors spent & batched Primordials (Elementals/Avatars/Archaics)",
        "slots": {
            "G": ["Nishoba Brawler", "Territorial Maro", "Prismabasher"],
            "U": ["Evasive Action", "Allied Strategies", "Shinestriker"],
            "R": ["Explosive Prodigy", "Incandescent Soulstoke", "Squawkroaster"],
            "2C": ["Risen Reef", "Twinflame Travelers", "Creeping Trailblazer"]
        }
    },
    {
        "code": "UBR",
        "colors": ["U", "B", "R"],
        "title": "Discard (Madness / Mayhem / Cycling)",
        "note": "Fixed Theme • Looting, Rummaging & Discard payoffs",
        "slots": {
            "U": ["Scrounging Skyray", "Circular Logic", "Ominous Sphinx"],
            "B": ["Asylum Visitor", "Big Game Hunter", "Gisa's Bidding"],
            "R": ["Marauding Mako", "Fiery Temper", "Raging Goblinoids"],
            "2C": ["Lazotep Chancellor", "Izzet Charm", "Terminal Agony"]
        }
    },
    {
        "code": "URW",
        "colors": ["U", "R", "W"],
        "title": "Spellslinger (Prowess & Second Spell)",
        "note": "Keeps U in Spellslinger • Token makers create consolidated 1/1 Goblins & 1/1 flying Thopters",
        "slots": {
            "U": ["Wingblade Disciple", "Whispering Wizard", "Eddymurk Crab"],
            "R": ["Young Pyromancer", "Guttersnipe", "Longshot, Rebel Bowman"],
            "W": ["Clever Lumimancer", "Clarion Spirit", "Sunstar Lightsmith"],
            "2C": ["Balmor, Battlemage Captain", "Cori Mountain Stalwart", "Raff, Weatherlight Stalwart"]
        }
    },
    {
        "code": "WUB",
        "colors": ["W", "U", "B"],
        "title": "Thopters & Artifact Creatures (Affinity)",
        "note": "All 1/1 flying tokens are Blue Artifact Thopters • Artifacts act as a kindred batch",
        "slots": {
            "W": ["Ingenious Smith", "Losheel, Clockwork Scholar", "Guidelight Synergist"],
            "U": ["Shuri, Wakandan Inventor", "Whirler Rogue", "Cerebral Download"],
            "B": ["Marionette Apprentice", "Armix, Filigree Thrasher", "Monoist Circuit-Feeder"],
            "2C": ["Bartolomé del Presidio", "Haunt the Network", "Voyage Home"]
        }
    },
    {
        "code": "RWB",
        "colors": ["R", "W", "B"],
        "title": "1/1 Goblin Swarm (Fey / Mobilize / Go-Wide)",
        "note": "All vanilla 1/1 tokens are Red Goblins (batched as Fey with Faeries & Kithkin) • Go-wide & kindred pump",
        "slots": {
            "R": ["Battle Cry Goblin", "General Kreat, the Boltbringer", "Volley Veteran"],
            "W": ["Dauntless Veteran", "Goldnight Commander", "Cloudgoat Ranger"],
            "B": ["Mudbutton Cursetosser", "Mad Auntie", "Sling-Gang Lieutenant"],
            "2C": ["Heroic Reinforcements", "Boggart Cursecrafter", "Hardened Tactician"]
        }
    },
    {
        "code": "GWU",
        "colors": ["G", "W", "U"],
        "title": "+1/+1 Counters & Proliferate",
        "note": "Gives W & G their +1/+1 counter payoffs across the curve alongside U proliferate & evasion",
        "slots": {
            "G": ["Wildwood Scourge", "Kami of Whispered Hopes", "Michelangelo, Mutant BFF"],
            "W": ["Metastatic Evangel", "Abzan Falconer", "Dr. McCoy, Surly Surgeon"],
            "U": ["Thrummingbird", "Flux Channeler", "Skatewing Spy"],
            "2C": ["Conclave Mentor", "Plumecreed Mentor", "Sharktocrab"]
        }
    },
    {
        "code": "RGW",
        "colors": ["R", "G", "W"],
        "title": "Behemoths & Power 4+ (Dinosaurs, Dragons & Wurms)",
        "note": "Dinosaurs, Dragons & Wurms batched as Behemoths • No blinkable ETB bombs in R or W",
        "slots": {
            "R": ["Triumphant Chomp", "Otepec Huntmaster", "Kolaghan Warmonger"],
            "G": ["Nessian Hornbeetle", "Goreclaw, Terror of Qal Sisma", "Challenger Troll"],
            "W": ["Imperial Lancer", "Dragon's Disciple", "Majestic Heliopterus"],
            "2C": ["Itzquinth, Firstborn of Gishath", "Atzocan Seer", "Regal Leosaur"]
        }
    },
    {
        "code": "BRG",
        "colors": ["B", "R", "G"],
        "title": "Morbid & Sacrifice (Creatures Dying & Devour)",
        "note": "Focused strictly on creatures dying on the battlefield & sacrificing fodder • Zero graveyard-size conflict",
        "slots": {
            "B": ["Zulaport Cutthroat", "Gravelighter", "Morkrut Banshee"],
            "R": ["Slumbering Cerberus", "Brimstone Volley", "Havoc Jester"],
            "G": ["Fungal Rebirth", "Lumberknot", "Skullmulcher"],
            "2C": ["Mayhem Devil", "Host of the Hereafter", "Rulik Mons, Warren Chief"]
        }
    },
    {
        "code": "BGU",
        "colors": ["B", "G", "U"],
        "title": "ETB Value (Self-Bounce, Ninjutsu & Recursion)",
        "note": "Rebuying ETBs via BLB Frogs, Ninjas & Gravedigger loops • Keeps ETB abuse out of R",
        "slots": {
            "B": ["Dokuchi Silencer", "Graveshifter", "Young Necromancer"],
            "G": ["Three Tree Scribe", "Eternal Witness", "Temur Sabertooth"],
            "U": ["Splash Portal", "Zephyr Sentinel", "Long River Lurker"],
            "2C": ["Honest Rutstein", "Lilysplash Mentor", "Ingenious Infiltrator"]
        }
    }
]

seen = set()
errors = []

for t in THEMES_V3:
    cols = t["colors"]
    pairs_seen = set()
    for slot_key, card_names in t["slots"].items():
        cmcs = []
        for name in card_names:
            c = by_name.get(name.lower())
            if not c:
                errors.append(f"[{t['code']} {slot_key}] MISSING: {name}")
                continue
            if name in seen:
                errors.append(f"[{t['code']} {slot_key}] DUPLICATE: {name}")
            seen.add(name)
            cmcs.append(int(c["cmc"]))
            if slot_key in ("W", "U", "B", "R", "G"):
                if c["color_identity"] != [slot_key]:
                    errors.append(f"[{t['code']} {slot_key}] WRONG COLOR IDENTITY: {name} has ci={c['color_identity']}")
            else:
                if len(c["color_identity"]) != 2 or not set(c["color_identity"]).issubset(set(cols)):
                    errors.append(f"[{t['code']} {slot_key}] WRONG 2C IDENTITY: {name} has ci={c['color_identity']}")
                pairs_seen.add(tuple(sorted(c["color_identity"])))
        if slot_key in ("W", "U", "B", "R", "G") and len(set(cmcs)) < 3:
            errors.append(f"[{t['code']} {slot_key}] DUPLICATE CMC IN MONO SLOT: {cmcs} for {card_names}")
    if len(pairs_seen) != 3:
        errors.append(f"[{t['code']} 2C] MISSING PAIR COVERAGE: {pairs_seen}")

print("Total unique cards:", len(seen))
print("Errors:", len(errors))
for e in errors:
    print(" ", e)

