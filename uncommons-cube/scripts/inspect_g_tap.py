import json

with open("uncommons-cube/cache/cube-pool.json") as f:
    pool = json.load(f)

by_name = {c["name"].lower(): c for c in pool}

names = [
    "Hemosymbic Mite", "Traveling Botanist", "House Cartographer", "Spiders-Man, Heroic Horde",
    "Saryth, the Viper's Fang", "Dionus, Elvish Archdruid", "Rootwise Survivor", "Autumn Willow, Harmony",
    "Crash the Party", "Kona, Rescue Beastie", "Adept Watershaper", "Sunstar Chaplain",
    "Spider-UK", "Dawnstrike Vanguard", "Savior of the Small", "Brad Boimler, Eager Ensign",
    "Wylie Duke, Atiin Hero", "Emmara, Soul of the Accord", "Shrewd Storyteller", "Spider-Man India"
]
for n in names:
    c = by_name.get(n.lower())
    if c:
        print(f"[{c['color_identity']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']} ({c['set']}, {c.get('power')}/{c.get('toughness')}): {c['oracle_text'].replace(chr(10), ' / ')}")

print("\n=== GREEN HARMONIZE / CONVOKE / TAPPED CREATURES ===")
for c in pool:
    if c["color_identity"] == ["G"] and "//" not in c["name"]:
        ol = c["oracle_text"].lower()
        if any(w in ol for w in ["harmonize", "convoke", "for each tapped", "tapped creature"]):
            print(f"  [{c['set']} {c['rarity'][0].upper()} MV={int(c['cmc'])}] {c['name']}: {c['oracle_text'].replace(chr(10), ' / ')[:130]}")

