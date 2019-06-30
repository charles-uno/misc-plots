#!/usr/bin/env python3


# https://www.holiday-weather.com/lagos/averages/

import matplotlib.pyplot as plt
import numpy as np
import sys

import helpers

def main():

    plt.figure(figsize=(16, 9))
    plt.gcf().text(0.99, 0.01, "charles.uno", fontsize=8, horizontalalignment="right")

    cities = helpers.load_json("data/cities.json")

    xvals, yvals = [], []
    xkey = "latitude"
    ykey = "temperature_january_f"

    skip = {
        "Seattle",
#        "Paris",
#        "Guangzhou",
        "Seoul",
#        "Tehran",
    }


    for city in cities:

        if not city.get(xkey) or not city.get(ykey):
            continue

        if city["latitude"] < 0 or city["name"] in skip:
            continue

        xvals.append(city[xkey])
        yvals.append(city[ykey])
        highlight(city, xkey, ykey)


    # Linear fit
    xfit, yfit = helpers.lin_fit(xvals, yvals)
    plt.plot(xfit, yfit, color="gray", ls=":", lw=0.5, zorder=0)

    # Data points
    plt.scatter(xvals, yvals, zorder=2, alpha=0.8)

    plt.title("Higher Latitude Means Colder Winter in the Northern Hemisphere")
    plt.xlabel("Latitude ($^\circ$N)")
    plt.ylabel("Average January Temperature ($^\circ$F)")

    plt.xlim(0, 80)
    plt.ylim(0, 90)

    plt.tight_layout()

    if "--save" in sys.argv:
        return plt.savefig("out.png")
    else:
        return plt.show()

# ----------------------------------------------------------------------

def highlight(obj, xkey, ykey):
    name, xval, yval = obj["name"], obj[xkey], obj[ykey]
    return plt.text(
        xval,
        yval,
        "  " + name,
        horizontalalignment="left",
        verticalalignment="center",
        fontsize=10,
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
