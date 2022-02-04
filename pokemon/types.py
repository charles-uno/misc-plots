#!/usr/bin/env python3

import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn
import sys


class PokemonType(object):
    def __init__(self, name, color="white"):
        self.name = name
        self.color = color


MODE = 0

YELLOW = seaborn.color_palette("Set2")[5]
GREEN = seaborn.color_palette("Paired")[3]
BLUE = seaborn.color_palette("Paired")[1]
GRAY = seaborn.color_palette("Set2")[7]
BROWN = seaborn.color_palette("tab10")[5]
PURPLE = seaborn.color_palette("Paired")[9]
PINK = seaborn.color_palette("tab10")[6]
ORANGE = seaborn.color_palette("Paired")[7]
RED = seaborn.color_palette("Paired")[5]
CYAN = seaborn.color_palette("Paired")[0]

COSMIC = PokemonType("Cosmic", RED)
FIRE = PokemonType("Fire", ORANGE)
HEART = PokemonType("Heart", PINK)
ICE = PokemonType("Ice", CYAN)
LIGHTNING = PokemonType("Lightning", YELLOW)
PLANT = PokemonType("Plant", GREEN)
ROCK = PokemonType("Rock", BROWN)
SHADOW = PokemonType("Shadow", PURPLE)
TECH = PokemonType("Tech", GRAY)
WATER = PokemonType("Water", BLUE)
WIND = PokemonType("Wind", GRAY)


TYPES_ORDERED = (
    WATER,
    TECH,
    PLANT,
    ROCK,
    FIRE,
    WIND,
    SHADOW,
    LIGHTNING,
    HEART,
)


RADIUS_WHEEL = 0.8
RADIUS_RING = 0.15
THICKNESS = 0.02
RADIUS_CAPTION = RADIUS_RING - THICKNESS
ARROW_TAIL_PAD = 0.02
ARROW_HEAD_PAD = 0.015
ARROW_TAIL_WIDTH = THICKNESS
ARROW_HEAD_LENGTH = 2*ARROW_TAIL_WIDTH
ARROW_HEAD_WIDTH = None


def main():
    plt.figure(figsize=(8, 8))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.axis("off")
    plt.xlim([-1, 1])
    plt.ylim([-1,1])
    # Watch out for duplicates
    assert len(TYPES_ORDERED) == len(set(TYPES_ORDERED))

    # Draw a circle for each type
    for i, t in enumerate(TYPES_ORDERED):
        draw_ring(i, t)

    # Draw the interactions
    draw_arrow(FIRE, PLANT)
    draw_arrow(FIRE, SHADOW)

    draw_arrow(WATER, FIRE)
    draw_arrow(WATER, TECH)

    draw_arrow(PLANT, WATER)
    draw_arrow(PLANT, ROCK)

#    draw_arrow(TECH, PLANT)
    draw_arrow(TECH, HEART)

    draw_arrow(LIGHTNING, WATER)
    draw_arrow(LIGHTNING, WIND)

    draw_arrow(HEART, SHADOW)

    draw_arrow(SHADOW, LIGHTNING)
    draw_arrow(SHADOW, TECH)

    draw_arrow(WIND, ROCK)

    draw_arrow(ROCK, LIGHTNING)

    if "--save" in sys.argv:
        return plt.savefig("pokemon-types.png")
    else:
        return plt.show()


def draw_arrows(*tarr):
    for i, t1 in enumerate(tarr):
        t2 = tarr[(i+1)%len(tarr)]
        draw_arrow(t1, t2)
    return


def draw_arrow(t1, t2):
    i1 = TYPES_ORDERED.index(t1)
    x1, y1 = pos(i1)
    i2 = TYPES_ORDERED.index(t2)
    x2, y2 = pos(i2)
    # Raw distance center to center
    dx_raw, dy_raw = x2 - x1, y2 - y1
    # Normalize to get a unit vector
    ds_raw = (dx_raw**2 + dy_raw**2)**0.5
    dx_hat, dy_hat = dx_raw/ds_raw, dy_raw/ds_raw
    # Chop some padding off each end to avoid overlapping the rings
    x = x1 + dx_hat*(RADIUS_RING + ARROW_TAIL_PAD)
    y = y1 + dy_hat*(RADIUS_RING + ARROW_TAIL_PAD)
    dx = dx_raw - dx_hat*(2*RADIUS_RING + ARROW_TAIL_PAD + ARROW_HEAD_PAD)
    dy = dy_raw - dy_hat*(2*RADIUS_RING + ARROW_TAIL_PAD + ARROW_HEAD_PAD)
    # Color comes from the arrow we point from
    return plt.arrow(
        x,
        y,
        dx,
        dy,
        facecolor=t1.color,
        edgecolor="black",
        width=ARROW_TAIL_WIDTH,
        head_width=ARROW_HEAD_WIDTH,
        head_length=ARROW_HEAD_LENGTH,
        linewidth=2,
        length_includes_head=True
    )


def draw_ring(i, t):
    x, y = pos(i)
    # Colored ring
    shaded_circle = mpatches.Circle(
        (x, y),
        radius=RADIUS_RING,
        facecolor=t.color,
        edgecolor="black",
        linewidth=2,
    )
    plt.gca().add_artist(shaded_circle)
    # White cutout in the middle for legibility
    cutout = mpatches.Circle(
        (x, y),
        radius=RADIUS_CAPTION,
        facecolor="white",
        edgecolor="black",
        linewidth=2,
    )
    plt.gca().add_artist(cutout)
    # Write the name in there
    plt.text(
        x=x,
        y=y,
        s=t.name,
        fontsize=14,
        horizontalalignment="center",
        verticalalignment="center",
    )
    return


def pos(i):
    theta = 2*math.pi*(i + 0.25)/len(TYPES_ORDERED)
    x = math.sin(theta)*RADIUS_WHEEL
    y = math.cos(theta)*RADIUS_WHEEL
    return x, y


if __name__ == "__main__":
    main()
