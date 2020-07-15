#!/usr/bin/env python3

import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


TYPES = (
    {"name": "Heart", "color": "C3"},
    {"name": "Fire", "color": "C1"},
    {"name": "Lightning", "color": "C8"},
    {"name": "Plant", "color": "C2"},
    {"name": "Wind", "color": "C9"},
    {"name": "Water", "color": "C0"},
    {"name": "Shadow", "color": "C4"},
    {"name": "Rock", "color": "C5"},
)


RSCALE = 1.3


def main():
    plt.figure(figsize=(10, 10))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.axis("off")
    plt.xlim([-1, 1])
    plt.ylim([-1,1])

    for i, t in enumerate(TYPES):
        theta = 2*math.pi*(i + 0.25)/len(TYPES)
        x = math.sin(theta)/RSCALE
        y = math.cos(theta)/RSCALE

        circle = mpatches.Circle(
            (x, y),
            0.15,
            facecolor=t["color"],
            edgecolor="black",
            linewidth=2,
        )
        plt.gca().add_artist(circle)

        circle = mpatches.Circle(
            (x, y),
            0.12,
            facecolor="white",
            edgecolor="black",
            linewidth=2,
        )
        plt.gca().add_artist(circle)

        plt.text(
            x=x,
            y=y,
            s=t["name"],
            fontsize=14,
            horizontalalignment="center",
            verticalalignment="center",
        )

    return plt.show()


if __name__ == "__main__":
    main()
