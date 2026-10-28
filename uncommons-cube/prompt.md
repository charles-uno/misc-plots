
# Cube Brainstorming

We are creating a cube in the game Magic: The Gathering. The cube is mostly made of uncommons.

## The Big Picture

Uncommons are the most satisfying part of a booster draft. They're in the sweet spot between power and complexity. They're the enablers and payoffs for the set's featured themes and synergies. When a draft goes well, and all the pieces of your deck fit together perfectly, it's the uncommons that really shine. 

This cube leans into that feeling. No bombs that steal a game solo. No forgettable filler. Every card is a role-player that invites you to build your deck around it. There are a million different ways to connect the dots. 

Commons and rares *are* allowed. But the bulk of the cube is uncommons, and they set the vibe.

### Cube Size

360 cards. We may drop it to 270 if we have trouble filling pods. Definitely no bigger

## Themes

In an ordinary set, you typically two-color themes (eg UR Spellslinger). Uncommons are good at emphasizing themes, and we have a fixed card pool, so I'm worried this will lead to repetitive play. Let's try three-color themes instead. One for each shard, one for each wedge. A given UR deck can pull from the URW, URB, and/or URG themes. 

Our themes are "fuzzier" than what you would see in an ordinary set. For example, in OTJ, there are several payoffs for controlling a creature with power 4 or greater. In TDM, there were payoffs for beholding a dragon. Here, those would likely be clumped into the same theme. 

Figuring out the themes themselves is the difficult (and interesting) part of designing the cube! Once the themes are set, everything else pretty much falls into place.

### Fixing

The themes are three colors, but we do *not* want three-color decks to be the norm. Themes are spread across three colors to muddy the waters and ensure that the UR deck doesn't always look the same. 

In terms of fixing, we probably want about the same density as BLB or ONE. These are formats where decks typically stuck to two colors. We do *not* want to follow the example of TDM, where players often played three colors. 

The tentative plan is to include five shard lands (eg [[Seaside Citadel]]), five wedge lands (eg [[Sandsteppe Citadel]]), five vivid lands (eg [[Vivid Creek]]), and a few one-offs. 

### Fixed Themes

We have a few easy ones to get us started. I like these themes, they are well-supported in recent sets, and there is no ambiguity about which triad they belong to:

- WBG Lifegain
- GUR Multicolor (Domain/Converge/Vivid)
- UBR Discard (Madness/Mayhem)

### Possible Themes

These ones are at least plausible. None are set in stone.

- Thopters. We don't have any noncreature artifacts, so "artifact" is a de facto creature type. Affinity is mechanically novel as a kindred payoff
- Goblins or some other type that uses 1/1 tokens
- Zombies, Knights, or some other type that uses 2/2 tokens
- Some type that uses 3/3 tokens
- Thopters, Spirits, or some other type that uses 1/1 flying tokens
- Fatties: Dinosaurs, Dragons, Ferocious
- Little guys. Power/MV 2 or less. Possibly focused on nontoken creatures to be distinct from Goblins
- ETB value. Blink or recursion
- Raid, Bloodthirst, Morbid, and/or sacrifice
- Tap/untap shenanigans. Convoke, Saddle, Web-slinging and/or tapping their stuff
- Spellslinger. Prowess and/or Heroic/Repartee/crimes
- Flash, playing on an opponent's turn
- Drawing extra cards
- Big mana value spells. Might get squished together with Vivid
- +1/+1 Counters. I don't love this one, honestly, since counters are a common bookkeeping tool across all colors. But there is plenty of support if we need it
- Graveyard. Wary of this one since I think it's tedious if players have to babysit each others' graveyards

Be careful not to mix conflicting sub-themes. For example, BG Forage (which wants to eat the graveyard) would not fit under the same umbrella as RG Delirium (which wants to make the graveyard big). 

### Theme Skeleton

In order for a theme to be viable, we need:

- Three payoffs in each color (judged by color identity) that pull a drafter into this theme specifically. These should *not* overlap between themes.
- At least one enabler or payoff in each two-color combination. These *may* overlap between themes.

For example, for UBR, we have a discard theme. Our skeleton could look like:

- U payoffs: [[Scrounging Skyray]], [[Circular Logic]], [[Ominous Sphinx]]
- B payoffs: [[Asylum Visitor]], [[Gisa's Bidding]], [[Big Game Hunter]]
- R payoffs: [[Marauding Mako]], [[Fiery Temper]], [[Raging Goblinoids]]
- Two-color payoffs: [[Terminal Agony]], [[Lazotep Chancellor]] (also relevant to Zombies), [[Izzet Charm]]

Notably, we are not married to any card in particular! If a card in here plays into an off-color theme awkwardly, we can swap it out.

When assembling a skeleton, make sure to get some mana value diversity in there. For example, we don't want the G payoffs for +1/+1 counters to be [[Kami of Whispered Hopes]], [[Evolution Sage]], and [[Meltstrider Eulogist]] -- those things all sit on the same spot in the mana curve!



### Theme-Aware Card Choices

We want the themes to be prominent, but we also want to make sure that each color is doing the stuff that it's supposed to do. 

For example, B is supposed to get creatures back from the graveyard. If ETB value shenanigans are on-theme for B, we may include [[Graveshifter]]. If not, we should try to avoid easily-blinked ETB abilities in B; something like [[Gathering Darkness]] might be a better fit for that slot.

### Respect the Card Pool

We can, without too much trouble, assemble a BRG Goblins theme. We can also easily assemble a +1/+1 Counters theme in BGU. However, if we do, we'll have trouble finding things to do with W. A large portion of the W cards we would play, especially at high mana value, are about +1/+1 counters and/or 1/1 tokens!

Here are a few of the constraints I have run into. These are not hard limits, but they issues to flag and avoid if possible:

- W really likes to do 1/1 tokens and +1/+1 counters
- U really likes to do stuff with noncreature spells. Spellslinger *can* be RGW Heroic or RWB Repartee, but those take a lot of wind out of U's sails

## Card Selection

Consider the following when selecting individual cards.

### Rarity

The cube is mostly uncommons. Any card that has ever been printed at uncommon is allowed, even if it has also been printed at another rarity.

The rarity constraint is *not* strict. We may include commons here and there to patch a hole. Rares are likewise allowed, provided they match the vibe in terms of power level and complexity.

### Hard Limitations

MTG is a big game with decades of expansions (and baggage). We are mindful about what we include and exclude. Right now that looks like:

- Creatures, lands, instants, and sorceries. No noncreature nonland permanents (equipment, sagas, planeswalkers, etc)
- Charge counters on lands, +1/+1 counters on creatures. No other counters
- No searching libraries. It slows down games too much. This includes basic lands
- No double-faced cards. Bad for draft logistics
- No control effects. No effects that exile your card on my side of the table (eg [[Fiend Hunter]]). Easy to accidentally switch cards between decks
- No external minigames: monarch, dungeons, speed, etc
- Maximum of ~6 different types of token (see house rules)
- No morph, manifest, or other face-down cards on the battlefield
- No joke sets or gimmicks (stickers, contraptions, etc)
- No mutate
- No regenerate or protection
- No prepare or omens. Too easy to confuse with adventures
- No retrace. Repetitive gameplay
- Universes Beyond cards *are* allowed

We may tweak this over time. But for the moment, these are hard rules. 

Open question: what about clues, treasures, etc? I'm inclined against them, but could be swayed

### Counterplay

[[Disenchant]] effects are typically not worth main-decking in Limited, but once in a while you'll get blown out by an artifact or enchantment that you can't interact with. This, to me, is bad tension. We avoid this issue entirely via blanket exclusion of noncreature artifacts and noncreature enchantments. 

On a similar note, we need to make sure to include appropriate interaction for the plays that *are* available. If it's possible to go wide, we need sweepers. If it's possible to go big, we need removal that can hit big creatures. If lands are important, we need a (non-oppressive) way to interact with them. If graveyard homework is a theme, we need a way to interact with that too.

### Power Creep

The power level of creatures in MTG has consistently increased over the years. Most uncommon creatures printed 5+ years ago are no longer suitable for the cube. They've just fallen too far behind compared to recent sets. 

This is not a hard rule. There are some old uncommons that were *extremely* overpowered at the time, which now are appropriately powerful.

The goal of the cube is for everything to be in the same ballpark in terms of power level. Some cards will always be better or worse. But we do not want any bombs that will run away with the game on their own, and we do not want any rarely-playable filler.

## House Rules

We tweak a few cards for convenience and to deepen sparse themes. We use small stickers to ensure that modifications are visible on each affected card.

We stick to subtypes. Otherwise it's a *big* can of worms. 

### Token Consolidation

We consolidate tokens based on size:

- All vanilla 1/1 tokens are red Goblins
- All vanilla 2/2 tokens are black Zombies
- All vanilla 3/3 tokens are green Dinosaurs
- All 1/1 flying tokens are blue Thopters

These types are not set in stone. The important thing is that they are all the same. For example, if convenient, we could say that all vanilla 1/1 tokens are green Elves instead. 

Zombie kindred is allowed as a theme, but it is not required. Same for the other token types.

Open question: what about other tokens? There are plenty of ways to produce 2/1, 3/2, tokens with vigilance, tokens with lifelink, etc. In short, we have room for another one or two types of token. But I would be hesitant to add a token type to support just a single card that produces it. 

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

## Scryfall Usage

Scryfall is a tool for searching existing MTG cards. 

- API docs: https://scryfall.com/docs/api
- Query syntax docs: https://scryfall.com/docs/syntax
- Bulk data access: https://scryfall.com/docs/api/bulk-data

### Rate Limiting

Scryfall has a rate limits! Be a good consumer. Be attentive to error messages

### Caching

To reduce duplicate queries, you may cache data locally in `cache/`. Details are up to you, but JSON is probably easiest

## Communication Style

Please be concise and direct. 

### HTML Demos

Sometimes I will ask you to output a bunch of data at once -- for example, a configuration of ten themes with a skeleton for each. That's a lot, especially when it includes cards I'm not familiar with!

For big dumps like that, please follow `template.html` for formatting. It also includes handling for autocards on hover. Do not overwrite the template -- create a new file that follows the rules.