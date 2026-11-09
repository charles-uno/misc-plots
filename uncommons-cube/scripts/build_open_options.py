import html
import json
import re

with open("/Users/charles/Desktop/misc-plots/uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

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
            return f"banned type '{c['type_line']}'"
    ol = c["oracle_text"].lower()
    if re.search(r"exile .* until .* leaves the battlefield", ol):
        return "temporary exile"
    for w in bad_words:
        if w in ol:
            return f"contains banned term '{w}'"
    for m in re.finditer(r"([a-z0-9+/-]+) counters? on", ol):
        ctype = m.group(1)
        if ctype not in ("+1/+1", "charge", "a", "more", "that", "each", "any", "no", "all", "those", "two", "three", "four", "five", "x", "had", "have", "with", "put", "move", "remove", "distribute", "double"):
            return f"contains illegal counter '{ctype}'"
    return None

OPEN_OPTIONS = [
    # ==================== RGW ====================
    {
        "triad": "RGW",
        "colors": ["R", "G", "W"],
        "option_id": "RGW-1",
        "verdict": "STRONG",
        "title": "RGW Option A: Go Wide (1/1 Tokens, Convoke & Team Pump)",
        "verdict_note": "Holds up cleanly. Every color has deep token generation and team-wide payoffs across the curve, though RG's two-color signpost slot leans on Pack Tactics (Targ Nar) rather than pure token text.",
        "slots": {
            "R": ["Battle Cry Goblin", "General Kreat, the Boltbringer", "Stoke the Flames"],
            "G": ["Get a Leg Up", "Imperious Perfect", "Overrun"],
            "W": ["Starry-Eyed Skyrider", "Goldnight Commander", "Cloudgoat Ranger"],
            "2C": ["Targ Nar, Demon-Fang Gnoll", "Queen Allenal of Ruadach", "Heroic Reinforcements"]
        }
    },
    {
        "triad": "RGW",
        "colors": ["R", "G", "W"],
        "option_id": "RGW-2",
        "verdict": "STRONG",
        "title": "RGW Option B: Tap/Untap Shenanigans (Saddle, Survival & Convoke)",
        "verdict_note": "Very cohesive thanks to OTJ/DFT Mounts, DSK Survivors, and EOE tap triggers. Red's tap payoffs are mostly Mounts/Pilots, so it plays like an aggressive creature-combo deck.",
        "slots": {
            "R": ["Gila Courser", "Reckless Velocitaur", "Dracosaur Auxiliary"],
            "G": ["Hemosymbic Mite", "Rambling Possum", "Autarch Mammoth"],
            "W": ["Canyon Vaulter", "Savior of the Small", "Dawnstrike Vanguard"],
            "2C": ["Radha, Coalition Warlord", "Shrewd Storyteller", "Sami, Ship's Engineer"]
        }
    },
    {
        "triad": "RGW",
        "colors": ["R", "G", "W"],
        "option_id": "RGW-3",
        "verdict": "SHAKY",
        "title": "RGW Option C: Dragons & Behemoths (Dinosaurs / Dragons / Power 4+)",
        "verdict_note": "Strains in White and RW. Even with Kinjalli's Caller and Osseous Exhale, White mostly wants to destroy power 4+ creatures rather than reward you for controlling them, and RW lacks an uncommon payoff that rewards big creatures/Dragons/Dinosaurs (Swathcutter Giant / Relentless Raptor are just standalone bodies).",
        "slots": {
            "R": ["Otepec Huntmaster", "Firespitter Whelp", "Bolt Bend"],
            "G": ["Nasty Little Rabbit", "Goreclaw, Terror of Qal Sisma", "Ghalta the Unstoppable"],
            "W": ["Kinjalli's Caller", "Osseous Exhale", "Majestic Heliopterus"],
            "2C": ["Ruby, Daring Tracker", "Atzocan Seer", "Swathcutter Giant"]
        }
    },

    # ==================== RWB ====================
    {
        "triad": "RWB",
        "colors": ["R", "W", "B"],
        "option_id": "RWB-1",
        "verdict": "MODERATE",
        "title": "RWB Option A: Little Guys (Power ≤ 2 Matter & MV ≤ 3 Recursion)",
        "verdict_note": "White and WB/RW are fantastic (Arabella, Wispdrinker Vampire, Scout for Survivors), but mono-Red and mono-Black are thin on true uncommon payoffs: Red mostly grants unblockability to power ≤ 2, and Black's MV ≤ 3 text is mostly reanimation or removal rather than ongoing engines.",
        "slots": {
            "R": ["Sneaking Guide", "Irreverent Gremlin", "Subira, Tulzidi Caravanner"],
            "W": ["Helping Hand", "Neighborhood Guardian", "Scout for Survivors"],
            "B": ["Unearth", "Slimy Dualleech", "No One Left Behind"],
            "2C": ["Arabella, Abandoned Doll", "Wispdrinker Vampire", "Balduvian Atrocity"]
        }
    },
    {
        "triad": "RWB",
        "colors": ["R", "W", "B"],
        "option_id": "RWB-2",
        "verdict": "FALLS APART",
        "title": "RWB Option B: Goblins / Fey Kindred (Goblin + Kithkin + Elf + Faerie + Dwarf)",
        "verdict_note": "Splits along the seams. Even if you batch Goblins, Kithkin, Elves, Faeries, and Dwarves into 'Fey' (or treat all 1/1 tokens as Goblins), WB has zero Fey-kindred signposts (Baron Bertram Graywater only cares about tokens generally) and the cards read like three separate Lorwyn tribes.",
        "slots": {
            "R": ["Goblin Negotiation", "General Kreat, the Boltbringer", "Volley Veteran"],
            "W": ["Kinsbaile Aspirant", "Wizened Cenn", "Cloudgoat Ranger"],
            "B": ["Mudbutton Cursetosser", "Miara, Thorn of the Glade", "Marsh Flitter"],
            "2C": ["Frontline Rush", "Baron Bertram Graywater", "Boggart Cursecrafter"]
        }
    },
    {
        "triad": "RWB",
        "colors": ["R", "W", "B"],
        "option_id": "RWB-3",
        "verdict": "STRONG",
        "title": "RWB Option C: Sacrifice & Aristocrats (1/1 Fodder & Death Triggers)",
        "verdict_note": "Rock-solid and deep in all three colors and all three guild pairs, especially with TDM's Mobilize mechanics bridging attacking tokens and end-step sacrifice triggers.",
        "slots": {
            "R": ["Rob the Archives", "Gut, True Soul Zealot", "Skirsdag Cultist"],
            "W": ["Duty Beyond Death", "Ministrant of Obligation", "Faramir, Field Commander"],
            "B": ["Zulaport Cutthroat", "Gravelighter", "Venerated Stormsinger"],
            "2C": ["Flamewright", "Hardened Tactician", "Garna, Bloodfist of Keld"]
        }
    },
    {
        "triad": "RWB",
        "colors": ["R", "W", "B"],
        "option_id": "RWB-4",
        "verdict": "MODERATE",
        "title": "RWB Option D: Undead Kindred (Vampires, Zombies, Skeletons & Spirits)",
        "verdict_note": "WB (Legion Lieutenant) and BR (Stromkirk Captain) are great Vampire lords, and RW has Spirit lords (Quintorius), but unless you batch Vampires + Zombies + Spirits + Skeletons as 'Undead', the three pairs pull toward different creature types (Vampires in WB/BR vs. Spirits in RW).",
        "slots": {
            "R": ["Insolent Neonate", "Rakish Heir", "Dreadhorde Twins"],
            "W": ["Duskborne Skymarcher", "Unconventional Tactics", "Mausoleum Guard"],
            "B": ["Indulgent Aristocrat", "Archghoul of Thraben", "Bloodline Necromancer"],
            "2C": ["Quintorius, Field Historian", "Legion Lieutenant", "Stromkirk Captain"]
        }
    },
    {
        "triad": "RWB",
        "colors": ["R", "W", "B"],
        "option_id": "RWB-5",
        "verdict": "STRONG",
        "title": "RWB Option E: Warriors & Fighters Kindred (Warriors, Knights & Soldiers)",
        "verdict_note": "Surprisingly clean! All three two-color signposts literally say 'Warriors' (Kargan Warleader, Chief of the Edge, Rushblade Commander), and TDM's Mobilize creates 1/1 red Warrior tokens in all three colors. If you batch Warriors/Soldiers/Knights as 'Fighters', it gets even deeper.",
        "slots": {
            "R": ["Goma Fada Vanguard", "Zurgo's Vanguard", "Iraxxa, Empress of Mars"],
            "W": ["Resolute Reinforcements", "Dalkovan Packbeasts", "Okoye, Dora Milaje Leader"],
            "B": ["Blood-Chin Rager", "Belle of the Brawl", "Thrasher Brute"],
            "2C": ["Kargan Warleader", "Chief of the Edge", "Rushblade Commander"]
        }
    },

    # ==================== BRG ====================
    {
        "triad": "BRG",
        "colors": ["B", "R", "G"],
        "option_id": "BRG-1",
        "verdict": "STRONG",
        "title": "BRG Option A: Stocked Graveyard (Delirium, Descend & Threshold)",
        "verdict_note": "Every card wants your graveyard to stay full and never exiles from it. Supported heavily by LCI (Descend), DSK (Delirium), and MH2/MH3.",
        "slots": {
            "B": ["Osseous Sticktwister", "Stinging Cave Crawler", "Chupacabra Echo"],
            "R": ["Dragon's Rage Channeler", "Gibbering Fiend", "Fledgling Dragon"],
            "G": ["Patchwork Beastie", "Coati Scavenger", "Wickerfolk Thresher"],
            "2C": ["Zoyowa Lava-Tongue", "Akawalli, the Seething Tower", "Wildfire Wickerfolk"]
        }
    },
    {
        "triad": "BRG",
        "colors": ["B", "R", "G"],
        "option_id": "BRG-2",
        "verdict": "SHAKY",
        "title": "BRG Option B: Morbid & Sacrifice",
        "verdict_note": "B, R, BR, and BG are overflowing with morbid/sacrifice payoffs, but RG has a glaring hole at uncommon: Gruul almost never gets creature-sacrifice or morbid signposts, forcing you to dip into a rare (Gimli, Mournful Avenger) or an old common (Gorger Wurm).",
        "slots": {
            "B": ["Nested Shambler", "Morbid Opportunist", "Syr Konrad, the Grim"],
            "R": ["Thud", "Snowslope Hunter", "Diversion Specialist"],
            "G": ["Meltstrider Eulogist", "Lumberknot", "Needletooth Pack"],
            "2C": ["Judith, the Scourge Diva", "Wardens of the Cycle", "Gimli, Mournful Avenger"]
        }
    },
    {
        "triad": "BRG",
        "colors": ["B", "R", "G"],
        "option_id": "BRG-3",
        "verdict": "STRONG",
        "title": "BRG Option C: Ferocious, Dragons & Behemoths (Power 4+ Matters)",
        "verdict_note": "Works much better in BRG than RGW! HOB gives Black and BG legitimate Ferocious cards (Nighthowl Pursuer, Ravening Warg, The Chief Warg), TDM gives Black Caustic Exhale, DFT gives Kalakscion (a 3-mana 7/2 'Behemoth' / honorary Dragon), and BR has Dragon signposts like Swift Warkite / Bladewing the Risen.",
        "slots": {
            "B": ["Nighthowl Pursuer", "Ravening Warg", "Kalakscion, Hunger Tyrant"],
            "R": ["Tiger-Dillo", "Firespitter Whelp", "Bolt Bend"],
            "G": ["Nasty Little Rabbit", "Goreclaw, Terror of Qal Sisma", "Wilderland Scrounger"],
            "2C": ["Swift Warkite", "The Chief Warg", "Thrakkus the Butcher"]
        }
    },

    # ==================== GWU ====================
    {
        "triad": "GWU",
        "colors": ["G", "W", "U"],
        "option_id": "GWU-1",
        "verdict": "STRONG",
        "title": "GWU Option A: Tap/Untap Shenanigans (Becomes Tapped, Convoke & Untappers)",
        "verdict_note": "Fits like a glove. Blue brings Gran-Gran (TLA), Mechan Navigator (EOE), and Pestered Wellguard (ECL), WU has Captain America, Living Legend (MSH), GW has Shrewd Storyteller (DSK), and GU has Kiora's Follower / Bounding Krasis to untap your tap-triggers repeatedly.",
        "slots": {
            "G": ["Hemosymbic Mite", "Supportive Parents", "Autarch Mammoth"],
            "W": ["Wanderbrine Trapper", "Protective Response", "Dawnstrike Vanguard"],
            "U": ["Gran-Gran", "Mechan Navigator", "Pestered Wellguard"],
            "2C": ["Shrewd Storyteller", "Captain America, Living Legend", "Kiora's Follower"]
        }
    },
    {
        "triad": "GWU",
        "colors": ["G", "W", "U"],
        "option_id": "GWU-2",
        "verdict": "STRONG",
        "title": "GWU Option B: +1/+1 Counters & Proliferate",
        "verdict_note": "Also bullet-proof. Every color has multiple proliferate engines and +1/+1 counter payoffs across distinct mana values, and all three guild pairs have premier signposts.",
        "slots": {
            "G": ["Wildwood Scourge", "Evolution Sage", "Michelangelo, Mutant BFF"],
            "W": ["Metastatic Evangel", "Abzan Falconer", "Dr. McCoy, Surly Surgeon"],
            "U": ["Thrummingbird", "Flux Channeler", "Tezzeret's Gambit"],
            "2C": ["Botanical Brawler", "Plumecreed Mentor", "Sharktocrab"]
        }
    }
]

errors = []
for opt in OPEN_OPTIONS:
    cols = opt["colors"]
    pairs_seen = set()
    for slot_key, names in opt["slots"].items():
        cmcs = []
        for n in names:
            c = by_name.get(n.lower())
            if not c:
                errors.append(f"[{opt['option_id']} {slot_key}] MISSING: {n}")
                continue
            leg = check_legality(c)
            if leg:
                errors.append(f"[{opt['option_id']} {slot_key}] ILLEGAL ({leg}): {n}")
            cmcs.append(int(c["cmc"]))
            if slot_key in ("W", "U", "B", "R", "G"):
                if c["color_identity"] != [slot_key]:
                    errors.append(f"[{opt['option_id']} {slot_key}] WRONG CI ({c['color_identity']}): {n}")
            else:
                if len(c["color_identity"]) != 2 or not set(c["color_identity"]).issubset(set(cols)):
                    errors.append(f"[{opt['option_id']} {slot_key}] WRONG 2C CI ({c['color_identity']}): {n}")
                pairs_seen.add(tuple(sorted(c["color_identity"])))
        if slot_key in ("W", "U", "B", "R", "G") and len(set(cmcs)) < 3:
            errors.append(f"[{opt['option_id']} {slot_key}] CMCs not all distinct: {cmcs} ({names})")
    if len(pairs_seen) < 3:
        errors.append(f"[{opt['option_id']} 2C] Missing pair coverage: {pairs_seen}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print("  -", e)
    raise SystemExit(1)
else:
    print("ALL 13 OPEN OPTION SKELETONS PASSED VALIDATION!")

# Generate HTML
def render_card_li(name):
    c = by_name[name.lower()]
    escaped = html.escape(c["name"], quote=True)
    rarity_badge = ""
    if c["rarity"] != "uncommon":
        rarity_badge = f' <span style="font-size:0.7rem;color:#6b7280;">({c["rarity"][0].upper()})</span>'
    return f'<li class="card-link" data-card-name="{escaped}">{html.escape(c["name"])}{rarity_badge}</li>'

verdict_colors = {
    "STRONG": ("#dcfce7", "#166534"),
    "MODERATE": ("#fef9c3", "#854d0e"),
    "SHAKY": ("#ffedd5", "#9a3412"),
    "FALLS APART": ("#fee2e2", "#991b1b"),
}

sections_html = []
current_triad = None
for opt in OPEN_OPTIONS:
    if opt["triad"] != current_triad:
        current_triad = opt["triad"]
        sections_html.append(f'<h2 style="margin: 28px 0 12px; font-size: 1.35rem; border-bottom: 2px solid #cbd5e1; padding-bottom: 6px;">{current_triad} Open Options</h2>')
    bg, fg = verdict_colors[opt["verdict"]]
    cols_html = []
    for k in opt["colors"] + ["2C"]:
        lis = "\n            ".join(render_card_li(n) for n in opt["slots"][k])
        cols_html.append(f"""        <div class="color-column">
          <div class="color-header color-{k}">{k}</div>
          <ul class="card-list">
            {lis}
          </ul>
        </div>""")
    grid = "\n".join(cols_html)
    sections_html.append(f"""    <section class="theme-section">
      <div class="theme-title" style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
        <span>{html.escape(opt["title"])}</span>
        <span style="background:{bg};color:{fg};padding:2px 10px;border-radius:999px;font-size:0.78rem;font-weight:700;letter-spacing:0.04em;">{opt["verdict"]}</span>
      </div>
      <div style="padding:10px 18px;font-size:0.88rem;color:#374151;background:#f8fafc;border-bottom:1px solid #e5e7eb;">
        {html.escape(opt["verdict_note"])}
      </div>
      <div class="columns">
{grid}
      </div>
    </section>""")

full_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MTG Uncommons Cube — Open Triad Options Stress-Test</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --surface: #ffffff;
      --border: #d8dce3;
      --text: #1c2026;
      --muted: #5c6470;
      --accent: #2d5be3;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 32px 24px 64px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}

    .container {{
      max-width: 1100px;
      margin: 0 auto;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 1.75rem;
      font-weight: 700;
    }}

    .subtitle {{
      margin: 0 0 28px;
      color: var(--muted);
      font-size: 0.95rem;
    }}

    .theme-section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 20px;
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }}

    .theme-title {{
      padding: 12px 18px;
      font-size: 1.05rem;
      font-weight: 600;
      background: #eef1f6;
      border-bottom: 1px solid var(--border);
    }}

    .columns {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
    }}

    .color-column {{
      padding: 14px 16px 18px;
      border-right: 1px solid var(--border);
    }}

    .color-column:last-child {{
      border-right: none;
    }}

    .color-header {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 5px;
      display: inline-block;
      margin-bottom: 10px;
    }}

    .color-W {{ background: #fdf6d8; color: #6b5600; border: 1px solid #e6d89c; }}
    .color-U {{ background: #dcebfa; color: #0f4c81; border: 1px solid #aacbef; }}
    .color-B {{ background: #e3dfe8; color: #2d2536; border: 1px solid #bdb5c7; }}
    .color-R {{ background: #fadcd6; color: #8a2511; border: 1px solid #f0b1a4; }}
    .color-G {{ background: #d9f0df; color: #195c2d; border: 1px solid #a7d9b4; }}
    .color-2C {{ background: #f3e8c8; color: #5c4308; border: 1px solid #dbc48a; }}

    .card-list {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}

    .card-link {{
      padding: 5px 8px;
      margin: 2px -8px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 0.92rem;
      color: var(--accent);
      transition: background 0.12s ease;
      user-select: none;
    }}

    .card-link:hover {{
      background: #eef3fd;
      text-decoration: underline;
    }}

    #card-preview {{
      position: fixed;
      z-index: 1000;
      pointer-events: none;
      display: none;
      width: 260px;
      border-radius: 13px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.32);
      background: #111;
      overflow: hidden;
    }}

    #card-preview img {{
      display: block;
      width: 100%;
      height: auto;
    }}

    #card-preview .status {{
      padding: 16px;
      color: #fff;
      font-size: 0.85rem;
      text-align: center;
    }}

    @media (max-width: 768px) {{
      .columns {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .color-column:nth-child(2) {{
        border-right: none;
      }}
      .color-column:nth-child(1),
      .color-column:nth-child(2) {{
        border-bottom: 1px solid var(--border);
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>MTG Uncommons Cube — Open Triad Options Stress-Test</h1>
    <p class="subtitle">12-card skeletons for all 13 open candidates across RGW, RWB, BRG, and GWU. Hover over any card name to preview it from Scryfall. Note: for BRG Option C, <em>Caustic Exhale</em> (MV=1) is also a great fit alongside <em>Nighthowl Pursuer</em> if two 1-drops are desired.</p>

{chr(10).join(sections_html)}
  </div>

  <div id="card-preview" role="tooltip" aria-hidden="true">
    <div class="status">Loading…</div>
    <img alt="" />
  </div>

  <script>
    (() => {{
      const preview = document.getElementById('card-preview');
      const img = preview.querySelector('img');
      const status = preview.querySelector('.status');
      const imageCache = new Map();
      let activeCard = null;

      function scryfallImageUrl(cardName) {{
        const params = new URLSearchParams({{
          exact: cardName,
          format: 'image',
          version: 'normal',
        }});
        return `https://api.scryfall.com/cards/named?${{params.toString()}}`;
      }}

      function positionPreview(event) {{
        const pad = 18;
        const rect = preview.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        let x = event.clientX + pad;
        let y = event.clientY + pad;

        if (x + rect.width + pad > vw) {{
          x = event.clientX - rect.width - pad;
        }}
        if (y + rect.height + pad > vh) {{
          y = Math.max(pad, vh - rect.height - pad);
        }}

        preview.style.left = `${{x}}px`;
        preview.style.top = `${{y}}px`;
      }}

      function showCard(cardName, event) {{
        activeCard = cardName;
        preview.style.display = 'block';
        preview.setAttribute('aria-hidden', 'false');

        const url = scryfallImageUrl(cardName);

        if (imageCache.get(cardName) === 'loaded') {{
          status.style.display = 'none';
          img.style.display = 'block';
          img.src = url;
          positionPreview(event);
          return;
        }}

        img.style.display = 'none';
        status.style.display = 'block';
        status.textContent = 'Loading…';
        positionPreview(event);

        const loader = new Image();
        loader.onload = () => {{
          imageCache.set(cardName, 'loaded');
          if (activeCard !== cardName) return;
          img.src = url;
          status.style.display = 'none';
          img.style.display = 'block';
        }};
        loader.onerror = () => {{
          imageCache.set(cardName, 'error');
          if (activeCard !== cardName) return;
          status.textContent = `Could not load "${{cardName}}"`;
        }};
        loader.src = url;
      }}

      function hideCard() {{
        activeCard = null;
        preview.style.display = 'none';
        preview.setAttribute('aria-hidden', 'true');
      }}

      document.querySelectorAll('.card-link').forEach((el) => {{
        const name = (el.dataset.cardName || el.textContent).trim();
        el.addEventListener('mouseenter', (e) => showCard(name, e));
        el.addEventListener('mousemove', positionPreview);
        el.addEventListener('mouseleave', hideCard);
      }});
    }})();
  </script>
</body>
</html>
"""

with open("/Users/charles/Desktop/misc-plots/uncommons-cube/open-options.html", "w") as f:
    f.write(full_html)
print("Wrote /Users/charles/Desktop/misc-plots/uncommons-cube/open-options.html")

