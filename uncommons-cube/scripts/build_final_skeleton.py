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

# Default ordering per prompt.md: WUB, WBG, BRG, BGU, GWU, GUR, UBR, URW, RGW, RWB
THEMES_FINAL = [
    {
        "code": "WUB",
        "colors": ["W", "U", "B"],
        "title": "WUB — Thopters & Artifact Creatures (Affinity)",
        "slots": {
            "W": ["Ingenious Smith", "Losheel, Clockwork Scholar", "Plated Onslaught"],
            "U": ["Donatello, Way with Machines", "Whirler Rogue", "Memory Guardian"],
            "B": ["Collective Drone", "Armix, Filigree Thrasher", "Monoist Circuit-Feeder"],
            "2C": ["Tidus, Blitzball Star", "Haunt the Network", "Locutus, the One Who Speaks"]
        }
    },
    {
        "code": "WBG",
        "colors": ["W", "B", "G"],
        "title": "WBG — Lifegain & Drain",
        "slots": {
            "W": ["Ajani's Pridemate", "MJ, Rising Star", "Attended Healer"],
            "B": ["Starscape Cleric", "Bloodthirsty Aerialist", "Vampire Scrivener"],
            "G": ["Tigra, Feline Fury", "Thornfist Striker", "Titanbones, Towering Heart"],
            "2C": ["Elas il-Kor, Sadistic Pilgrim", "Dina, Soul Steeper", "Trelasarra, Moon Dancer"]
        }
    },
    {
        "code": "BRG",
        "colors": ["B", "R", "G"],
        "title": "BRG — Dragons, Behemoths & Ferocious (Power 4+ Matters)",
        "slots": {
            "B": ["Nighthowl Pursuer", "Foul-Tongue Invocation", "Fearsome Awakening"],
            "R": ["Tiger-Dillo", "Firespitter Whelp", "Bolt Bend"],
            "G": ["Nasty Little Rabbit", "Goreclaw, Terror of Qal Sisma", "Wilderland Scrounger"],
            "2C": ["Bladewing the Risen", "The Chief Warg", "Thrakkus the Butcher"]
        }
    },
    {
        "code": "BGU",
        "colors": ["B", "G", "U"],
        "title": "BGU — ETB Value (Blink, Recursion & Ninjas)",
        "slots": {
            "B": ["Dokuchi Silencer", "Shredder's Technique", "Tormod, the Desecrator"],
            "G": ["Three Tree Scribe", "Attuned Hunter", "Temur Sabertooth"],
            "U": ["Splash Portal", "Zephyr Sentinel", "Imperial Cosmographer"],
            "2C": ["Honest Rutstein", "Lilysplash Mentor", "Ingenious Infiltrator"]
        }
    },
    {
        "code": "GWU",
        "colors": ["G", "W", "U"],
        "title": "GWU — Tap/Untap Shenanigans (Becomes Tapped, Survival & Untappers)",
        "slots": {
            "G": ["Hemosymbic Mite", "Traveling Botanist", "Rootwise Survivor"],
            "W": ["Sunstar Chaplain", "Savior of the Small", "Dawnstrike Vanguard"],
            "U": ["Gran-Gran", "Mechan Navigator", "Pestered Wellguard"],
            "2C": ["Shrewd Storyteller", "Captain America, Living Legend", "Kiora's Follower"]
        }
    },
    {
        "code": "GUR",
        "colors": ["G", "U", "R"],
        "title": "GUR — Multicolor & Primordials (Domain / Converge / Vivid)",
        "slots": {
            "G": ["Nishoba Brawler", "Luminollusk", "Prismabasher"],
            "U": ["Sweep the Skies", "Allied Strategies", "Shinestriker"],
            "R": ["Tribal Flames", "Squawkroaster", "Archaic's Agony"],
            "2C": ["Risen Reef", "Twinflame Travelers", "Wandertale Mentor"]
        }
    },
    {
        "code": "UBR",
        "colors": ["U", "B", "R"],
        "title": "UBR — Discard & Looting (Madness / Mayhem / Cycling)",
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
        "title": "URW — Spellslinger & Second Spell (Prowess / Flurry)",
        "slots": {
            "U": ["Muse Seeker", "Wingblade Disciple", "Eddymurk Crab"],
            "R": ["Coruscation Mage", "Guttersnipe", "Longshot, Rebel Bowman"],
            "W": ["Monk of the Open Hand", "Clarion Spirit", "Sunstar Lightsmith"],
            "2C": ["Balmor, Battlemage Captain", "Cori Mountain Stalwart", "Raff, Weatherlight Stalwart"]
        }
    },
    {
        "code": "RGW",
        "colors": ["R", "G", "W"],
        "title": "RGW — Go Wide (1/1 Tokens & Team Pump)",
        "slots": {
            "R": ["Battle Cry Goblin", "General Kreat, the Boltbringer", "Stoke the Flames"],
            "G": ["Get a Leg Up", "Woodland Champion", "Overrun"],
            "W": ["Pride of Conquerors", "Starry-Eyed Skyrider", "Goldnight Commander"],
            "2C": ["Targ Nar, Demon-Fang Gnoll", "Queen Allenal of Ruadach", "Heroic Reinforcements"]
        }
    },
    {
        "code": "RWB",
        "colors": ["R", "W", "B"],
        "title": "RWB — Sacrifice & Aristocrats (Mobilize & Death Triggers)",
        "slots": {
            "R": ["Blood Aspirant", "Snowslope Hunter", "Skirsdag Cultist"],
            "W": ["Duty Beyond Death", "Rayblade Trooper", "Odric's Outrider"],
            "B": ["Zulaport Cutthroat", "Gravelighter", "Venerated Stormsinger"],
            "2C": ["Brion Stoutarm", "Hardened Tactician", "Garna, Bloodfist of Keld"]
        }
    }
]

seen = set()
errors = []

for t in THEMES_FINAL:
    cols = t["colors"]
    pairs_seen = set()
    for slot_key, card_names in t["slots"].items():
        cmcs = []
        for name in card_names:
            c = by_name.get(name.lower())
            if not c:
                errors.append(f"[{t['code']} {slot_key}] MISSING: {name}")
                continue
            if c["name"] in seen:
                errors.append(f"[{t['code']} {slot_key}] DUPLICATE ACROSS CUBE: {c['name']}")
            seen.add(c["name"])
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
            errors.append(f"[{t['code']} {slot_key}] POOR CMC DIVERSITY: {cmcs} ({card_names})")
    if len(pairs_seen) < 3:
        errors.append(f"[{t['code']} 2C] MISSING TWO-COLOR PAIR COVERAGE: {pairs_seen}")

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print("  -", e)
    raise SystemExit(1)

print(f"SUCCESS: All {len(seen)} unique cards across 10 themes validated cleanly!")

def render_card_li(name):
    c = by_name[name.lower()]
    escaped = html.escape(c["name"], quote=True)
    return f'<li class="card-link" data-card-name="{escaped}">{html.escape(c["name"])}</li>'

sections_html = []
for t in THEMES_FINAL:
    cols_html = []
    for k in t["colors"] + ["2C"]:
        lis = "\n            ".join(render_card_li(n) for n in t["slots"][k])
        cols_html.append(f"""        <div class="color-column">
          <div class="color-header color-{k}">{k}</div>
          <ul class="card-list">
            {lis}
          </ul>
        </div>""")
    grid = "\n".join(cols_html)
    sections_html.append(f"""    <section class="theme-section">
      <div class="theme-title">{html.escape(t["title"])}</div>
      <div class="columns">
{grid}
      </div>
    </section>""")

full_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MTG Uncommons Cube — Full 10-Theme Skeleton</title>
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
    <h1>MTG Uncommons Cube — Full 10-Theme Skeleton</h1>
    <p class="subtitle">120 unique payoffs across all 10 shard and wedge themes (ordered WUB, WBG, BRG, BGU, GWU, GUR, UBR, URW, RGW, RWB). Hover over any card name to preview it from Scryfall.</p>

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

with open("/Users/charles/Desktop/misc-plots/uncommons-cube/themes-final.html", "w") as f:
    f.write(full_html)
print("Wrote /Users/charles/Desktop/misc-plots/uncommons-cube/themes-final.html")
