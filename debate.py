#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

plt.rcParams.update({"font.size": 16})

import helpers

def main():

    names, polls, words = [], [], []
    candidates = helpers.load_json("data/debate.json")

    plt.figure(figsize=(10, 10))

    plt.gcf().text(0.99, 0.01, "charles.uno", fontsize=8, horizontalalignment="right")
    plt.gcf().text(0.01, 0.01, "data per FiveThirtyEight", fontsize=8, horizontalalignment="left")

    # Overall trend line
    polls = [ x["polls"] for x in candidates ]
    words = [ x["words"] for x in candidates ]
    xfit, yfit = helpers.lin_fit(polls, words, log="x")
    plt.plot(xfit, yfit, color="gray", ls=":", lw=0.5, zorder=0)

    # Candidate names
    [ highlight(c) for c in candidates ]

    for i in [1, 2]:
        color = "C" + str(i-1)
        label = "Wednesday" if i == 1 else "Thursday"
        polls = [ x["polls"] for x in candidates if x["night"] == i ]
        words = [ x["words"] for x in candidates if x["night"] == i ]
        plt.scatter(polls, words, label=label, color=color, zorder=2, alpha=0.8)

    plt.legend(loc="upper left")

    plt.xscale("log")
#    plt.minorticks_off()
    ticks, labels = helpers.get_log_ticks(polls, base=10)
    labels = [ x + "%" for x in labels ]
    plt.xlim(min(ticks), max(ticks))
    plt.xticks(ticks, labels)

    plt.ylim(0, 3000)
    plt.yticks([0, 1000, 2000, 3000], ["0", "1k", "2k", "3k"])

    plt.title("How Support Compares to Word Count")
    plt.xlabel("Polling Average")
    plt.ylabel("Word Count")


    plt.tight_layout()

    if "--save" in sys.argv:
        return plt.savefig("out.png")
    else:
        return plt.show()


def highlight(candidate):

    pos = {
        "Biden": "top",
        "Booker": "top",
        "Harris": "top",
        "Buttigieg": "left",
        "O'Rourke": "left",
        "Buttigieg": (16, 2000),
        "Sanders": "top",
        "Warren": "top",
        "Klobuchar": "bottom",
        "Castro": "top",
        "Gabbard": "bottom",
        "Bennet": "left",
        "Gillibrand": (0.3, 1700),
        "Hickenlooper": "right",
        "de Blasio": (0.45, 700),
        "Inslee": (0.7, 800),
        "Delaney": "top",
        "Yang": "bottom",
        "Ryan": "right",
        "Williamson": (0.3, 500),
        "Stalwell": (0.15, 400),
    }

    # Black border around point
#    plt.scatter(
#        [candidate["polls"]],
#        [candidate["words"]],
#        facecolors="none",
#        edgecolors="black",
#    )

    name, polls, words = candidate["name"], candidate["polls"], candidate["words"]


    angle = {
#        "Biden": 30,
#        "Harris": 30,
    }

    if name in angle:
        plt.text(
            polls,
            words,
            name,
            rotation=angle[name],
            horizontalalignment="left",
            verticalalignment="bottom",
            fontsize=10,
        )
        return









    if pos[name] == "top":
        kwargs = {
            "s": name,
            "horizontalalignment": "center",
            "verticalalignment": "bottom",
            "xytext": (polls, words + 25),
        }
    elif pos[name] == "right":
        kwargs = {
            "s": "  " + name,
            "horizontalalignment": "left",
            "verticalalignment": "center",
            "xytext": (polls, words),
        }
    elif pos[name] == "bottom":
        kwargs = {
            "s": name,
            "horizontalalignment": "center",
            "verticalalignment": "top",
            "xytext": (polls, words - 25),
        }
    elif pos[name] == "left":
        kwargs = {
            "s": name + "  ",
            "horizontalalignment": "right",
            "verticalalignment": "center",
            "xytext": (polls, words),
        }
    else:
        kwargs = {
            "s": name,
            "horizontalalignment": "center",
            "verticalalignment": "center",
            "xytext": pos[name],
            "arrowprops": dict(facecolor='black', arrowstyle="-"),
        }

    plt.annotate(
            xy=(polls, words),
            zorder=1,
            **kwargs
        )

    return



# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
