import html
import json
import re

with open("/Users/charles/Desktop/misc-plots/uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

bad_words = [
    "treasure", "food", "clue", "blood token", "eldrazi", "map token", "powerstone", "junk token", "lander",
    "mutate", "regenerate ", "regenerates", "protection from", "omen", "prepare", "retrace",
    "stun counter", "oil counter", "shield counter", "finality counter", "lore counter", "rad counter",
    "time counter", "spore counter", "energy counter", "{e}", "-1/-1 counter", "flying counter",
    "vigilance counter", "menace counter", "trample counter", "lifelink counter", "deathtouch counter",
    "first strike counter", "double strike counter", "hexproof counter", "reach counter", "indestructible counter",
    "role token", "incubate"
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
        if ctype not in ("+1/+1", "charge", "a", "more", "that", "each", "any", "no", "all", "those", "two", "three", "four", "five", "x"):
            return f"contains illegal counter '{ctype}'"
    return None

THEMES_BOTTOM_UP = [
    {
        "code": "WBG",
        "colors": ["W", "B", "G"],
        "title": "Lifegain (Infusion & Drain)",
        "slots": {
            "W": ["Ajani's Pridemate", "MJ, Rising Star", "Attended Healer"],
            "B": ["Starscape Cleric", "Bloodthirsty Aerialist", "Vampire Scrivener"],
            "G": ["Tigra, Feline Fury", "Thornfist Striker", "Titanbones, Towering Heart"],
            "2C": ["Elas il-Kor, Sadistic Pilgrim", "Dina, Soul Steeper", "Trelasarra, Moon Dancer"]
        }
    },
    {
        "code": "GUR",
        "colors": ["G", "U", "R"],
        "title": "Multicolor, Primordials & Big Spells (Vivid / Converge / MV 4+)",
        "slots": {
            "G": ["Nishoba Brawler", "Luminollusk", "Prismabasher"],
            "U": ["Sweep the Skies", "Tanufel Rimespeaker", "Shinestriker"],
            "R": ["Explosive Prodigy", "Squawkroaster", "Archaic's Agony"],
            "2C": ["Risen Reef", "Twinflame Travelers", "Wandertale Mentor"]
        }
    },
    {
        "code": "UBR",
        "colors": ["U", "B", "R"],
        "title": "Discard & Looting (Madness / Mayhem / Cycling)",
        "slots": {
            "U": ["Scrounging Skyray", "Circular Logic", "Teo, Spirited Glider"],
            "B": ["Asylum Visitor", "Big Game Hunter", "Gisa's Bidding"],
            "R": ["Marauding Mako", "Fiery Temper", "Raging Goblinoids"],
            "2C": ["Lazotep Chancellor", "Glacial Dragonhunt", "Terminal Agony"]
        }
    },
    {
        "code": "URW",
        "colors": ["U", "R", "W"],
        "title": "Second Spell & Spellslinger (Flurry / Prowess)",
        "slots": {
            "U": ["Muse Seeker", "Wingblade Disciple", "Eddymurk Crab"],
            "R": ["Coruscation Mage", "Guttersnipe", "Longshot, Rebel Bowman"],
            "W": ["Monk of the Open Hand", "Clarion Spirit", "Sunstar Lightsmith"],
            "2C": ["Balmor, Battlemage Captain", "Cori Mountain Stalwart", "Raff, Weatherlight Stalwart"]
        }
    },
    {
        "code": "WUB",
        "colors": ["W", "U", "B"],
        "title": "Artifact Creatures & Thopters (Affinity)",
        "slots": {
            "W": ["Ingenious Smith", "Losheel, Clockwork Scholar", "Plated Onslaught"],
            "U": ["Thopter Mechanic", "Whirler Rogue", "Memory Guardian"],
            "B": ["Marionette Apprentice", "Armix, Filigree Thrasher", "Monoist Circuit-Feeder"],
            "2C": ["Tidus, Blitzball Star", "Haunt the Network", "Bartolomé del Presidio"]
        }
    },
    {
        "code": "RWB",
        "colors": ["R", "W", "B"],
        "title": "Token Aristocrats & Mobilize (1/1 Swarm & Sacrifice)",
        "slots": {
            "R": ["Battle Cry Goblin", "General Kreat, the Boltbringer", "Stoke the Flames"],
            "W": ["Starry-Eyed Skyrider", "Goldnight Commander", "Cloudgoat Ranger"],
            "B": ["Zulaport Cutthroat", "Gravelighter", "Venerated Stormsinger"],
            "2C": ["Heroic Reinforcements", "Garna, Bloodfist of Keld", "Hardened Tactician"]
        }
    },
    {
        "code": "GWU",
        "colors": ["G", "W", "U"],
        "title": "+1/+1 Counters, Modified & Proliferate",
        "slots": {
            "G": ["Wildwood Scourge", "Meltstrider Eulogist", "Michelangelo, Mutant BFF"],
            "W": ["Metastatic Evangel", "Abzan Falconer", "Dr. McCoy, Surly Surgeon"],
            "U": ["Thrummingbird", "Flux Channeler", "Tezzeret's Gambit"],
            "2C": ["Botanical Brawler", "Plumecreed Mentor", "Sharktocrab"]
        }
    },
    {
        "code": "RGW",
        "colors": ["R", "G", "W"],
        "title": "Tap Shenanigans: Saddle, Survival & Convoke",
        "slots": {
            "R": ["Gila Courser", "Reckless Velocitaur", "Dracosaur Auxiliary"],
            "G": ["Hemosymbic Mite", "Rambling Possum", "Autarch Mammoth"],
            "W": ["Canyon Vaulter", "Savior of the Small", "Bounding Felidar"],
            "2C": ["Shrewd Storyteller", "Sami, Ship's Engineer", "Radha, Coalition Warlord"]
        }
    },
    {
        "code": "BRG",
        "colors": ["B", "R", "G"],
        "title": "Stocked Graveyard (Delirium, Descend & Threshold)",
        "slots": {
            "B": ["Osseous Sticktwister", "Stinging Cave Crawler", "Chupacabra Echo"],
            "R": ["Dragon's Rage Channeler", "Gibbering Fiend", "Fledgling Dragon"],
            "G": ["Patchwork Beastie", "Coati Scavenger", "Wickerfolk Thresher"],
            "2C": ["Zoyowa Lava-Tongue", "Akawalli, the Seething Tower", "Wildfire Wickerfolk"]
        }
    },
    {
        "code": "BGU",
        "colors": ["B", "G", "U"],
        "title": "ETB Value (Self-Bounce, Ninjutsu & Recursion)",
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

for t in THEMES_BOTTOM_UP:
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
            leg = check_legality(c)
            if leg:
                errors.append(f"[{t['code']} {slot_key}] ILLEGAL ({leg}): {name}")
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

if not errors:
    with open("/Users/charles/Desktop/misc-plots/uncommons-cube/template.html") as f:
        tpl = f.read()

    head_part = tpl.split("<div class=\"theme-card\">")[0]
    head_part = head_part.replace("Uncommons Cube — Autocard Demo", "Uncommons Cube — Bottom-Up Configuration (2021–2026 Draft Sets)")
    foot_part = "  <!-- Floating Card Image Tooltip -->" + tpl.split("<!-- Floating Card Image Tooltip -->")[1]

    cards_html = []
    for t in THEMES_BOTTOM_UP:
        pips = "\n".join(f"          <img class=\"mana-sym\" src=\"https://svgs.scryfall.io/card-symbols/{c}.svg\" alt=\"{{{c}}}\">" for c in t["colors"])
        cols_html = []
        for k in t["colors"] + ["2C"]:
            if k == "2C":
                h3 = "<h3>Two-Color</h3>"
            else:
                h3 = f"<h3><img class=\"mana-sym\" src=\"https://svgs.scryfall.io/card-symbols/{k}.svg\" alt=\"{{{k}}}\"> Payoffs</h3>"
            lis = "\n".join(f"          <li><span class=\"autocard\" data-card=\"{html.escape(c)}\">{html.escape(c)}</span></li>" for c in t["slots"][k])
            cols_html.append(f"""      <div class="slot-group">
        {h3}
        <ul class="card-list">
{lis}
        </ul>
      </div>""")
        grid_inner = "\n\n".join(cols_html)
        cards_html.append(f"""  <div class="theme-card">
    <div class="theme-header">
      <h2 class="theme-title">
        <span class="pips">
{pips}
        </span>
        <span>{html.escape(t["title"])}</span>
      </h2>
    </div>

    <div class="skeleton-grid">
{grid_inner}
    </div>
  </div>""")

    full_html = head_part + "\n\n".join(cards_html) + "\n\n" + foot_part
    out_file = "/Users/charles/Desktop/misc-plots/uncommons-cube/themes-bottom-up.html"
    with open(out_file, "w") as f:
        f.write(full_html)
    print("Wrote", out_file)
