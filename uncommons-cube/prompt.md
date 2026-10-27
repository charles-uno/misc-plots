
# Cube Brainstorming

We are creating a cube in the game Magic: The Gathering. The cube is mostly made of uncommons.

## Emphasize the Uncommons

Uncommons are the most satisfying part of a booster draft. They're in the sweet spot between power and complexity. They're the enablers and payoffs for the set's featured themes and synergies. When a draft goes well, and all the pieces of your deck fit together perfectly, it's the uncommons that really shine. 

This cube leans into that feeling. No bombs that steal a game solo. No forgettable filler. Every card is a role-player that invites you to build your deck around it. There are a million different ways to connect the dots. 

Commons and rares *are* allowed. But the bulk of the cube is uncommons, and they set the vibe.

## Card Selection

The cube is mostly uncommons, but not stictly. Sometimes we'll include a common or rare to fill an empty niche.

### Hard Limitations

MTG is a big game with decades of expansions (and baggage). We are mindful about what we include. Right now that looks like:

- Creatures, lands, instants, and sorceries. No equipment, planeswalkers, etc
- Charge counters on lands, +1/+1 counters on creatures. No other counters
- No searching libraries. It slows down games too much
- No double-faced cards. Bad for draft logistics
- No control or timeout effects. Easy to accidentally switch cards between decks
- No external minigames: monarch, dungeons, speed, etc
- Maximum of ~6 different types of token (see house rules)

We may tweak this over time. In particular, I could see coming back for equipment. But for the moment, these are hard rules. 

## Power Creep

The power level of creatures in MTG has consistently increased over the years. Most uncommon creatures printed 5+ years ago are no longer suitable for the cube. They've just fallen too far behind compared to recent sets. 

This is not a hard rule. There are some old uncommons that were *extremely* overpowered at the time, which now are appropriately powerful.

## House Rules

We tweak a few cards for convenience and to deepen sparse themes. We use small stickers to ensure that modifications are visible on each affected card.

We stick to subtypes. Otherwise it's a *big* can of worms. 

### Token Consolidation

We consolidate tokens based on size:

- All vanilla 1/1 tokens are Goblins
- All vanilla 2/2 tokens are Zombies
- All vanilla 3/3 tokens are Dinosaurs
- All 1/1 flying tokens are Thopters

These types are not set in stone. The important thing is that they are all the same. For example, if convenient, we could say that all vanilla 1/1 tokens are Elves instead. 

Open question: do we treat Amass 1 like a 1/1 token, Amass 2 like a 2/2 token, etc? Or do we use the Army token as printed? We could go either way based on what better lines up with the themes (eg, whether +1/+1 counters are on-theme for these colors)

### Kindred Batches

Some creature types are batched, like Outlaws from OTJ. This can combine two sparse themes into a viable one. Examples:

- Skeletons, Vampires, and Zombies are *Undead* 
- Dinosaurs, Dragons, and Wurms are *Behemoths*
- Faeries, Goblins, and Kithkin are *Fey*
- Knights, Soldiers, and Warriors are *Fighters*
- Avatars, Elementals, and Incarnations are *Primordials*

In each case, buffs and debuffs from the specific creature type are updated to cover the whole batch. For example, [[Legion Lieutenant]] would be updated from "Vampires get +1/+1" to "Undead get +1/+1"

Again, we are not married to these specific batches. They may be tweaked (eg, Fey could include Elves or Merfolk) or we could use different batches entirely.

### Domain Tri-Lands

Finally, we append the relevant basic land types to the shard and wedge tri-lands. For example, we update [[Arcane Sanctum]] to be a Plains Island Swamp. 

This is relevant for a handful of cards, most notably domain cards like [[Tribal Flames]]

## Themes

In an ordinary set, you typically see a theme for each two-color combination (eg UR Spellslinger). Two-color themes can get repetitive in a cube due to the fixed card pool. They can be doubly repetitive in an uncommons cube, since uncommons are so good at emphasizing themes. 

To keep things interesting, we instead use overlapping three-color themes. A given UR deck may pull from the URW, URB, and/or URG themes. 

The themes themselves are also "fuzzier" than you would see in an ordinary set. For example, in OTJ, there are several payoffs for controlling a creature with power 4 or greater. In TDM, there were payoffs for beholding a dragon. Here, those would likely be clumped into the same theme. 

Figuring out the themes themselves is the difficult (and interesting) part of designing the cube! Once the themes are set, everything else pretty much falls into place.

### Fixed Themes

We have a few easy ones to get us started. Mechanically novel, well supported, and no wiggle room as far as which colors to use:

- WBG Lifegain. U and R rarely deal with lifegain
- GUR Multicolor (Domain/Converge/Vivid). Notably: SOS archaics are batched together with ECL elementals for the sake of [[Risen Reef]], [[Twinflame Travelers]], etc
- UBR Discard (Madness/Mayhem)

### Likely Themes

These ones are likely, but not set in stone:

- Thopters. We don't have any noncreature artifacts, so "artifact" is a de facto creature type. Affinity is mechanically novel as a kindred payoff
- Goblins or some other type that uses 1/1 tokens
- Zombies, Knights, or some other type that uses 2/2 tokens
- Dinosaurs or some other type that uses 3/3 tokens 
- +1/+1 Counters
- ETB value. Blink or graveyard nonsense
- Spellslinger. Prowess or heroic, probably not both

### Theme Skeleton

In order for a theme to be viable, we need:

- Three payoffs in each color that pull a drafter into thse theme
- At least one enabler or payoff in each two-color combination

For example, for UBR, we have a discard theme. Our skeleton could look like:

- U payoffs: [[Scrounging Skyray]], [[Circular Logic]], [[Ominous Sphinx]]
- B payoffs: [[Asylum Visitor]], [[Gisa's Bidding]], [[Big Game Hunter]]
- R payoffs: [[Marauding Mako]], [[Fiery Temper]], [[Raging Goblinoids]]
- Multicolor payoffs: [[Terminal Agony]], [[Lazotep Chancellor]], [[Izzet Charm]]

## Scryfall Usage

Scryfall is a took for searching existing MTG cards. 

API docs: https://scryfall.com/docs/api

Query syntax docs: https://scryfall.com/docs/syntax

### Rate Limiting

Scryfall has a rate limits! Be a good consumer. Be attentive to error messages

