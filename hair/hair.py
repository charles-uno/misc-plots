#!/usr/bin/env python3


import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


def main():

    day = 86400

    times = []
    lengths = []

    with open("hair.csv", "r") as handle:
        for line in handle:
            date, time, length = line.rstrip().split(",")
            lengths.append(float(length))
            tobj = dt.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            times.append(tobj.timestamp())
    plt.scatter(times, lengths, s=10)

    pfit = np.polyfit(times, lengths, 1)
    tfit = np.linspace(min(times), max(times), 10)
    lfit = pfit[0]*tfit + pfit[1]
    plt.plot(tfit, lfit, color="black", linestyle=":")

    # Raw slope is mm per second
    slope = "%.1f" % (pfit[0]*day*7)
    note = slope + " mm/week"
    plt.text(0.3, 0.8, note, transform=plt.gca().transAxes)

    tmin = int(min(times)//day)*day - day
    tmax = int(max(times)//day + 1)*day
    step = 7*day
    xticks = range(tmin, tmax + step, step)
    xlabels = [pretty_date(t) for t in xticks]
    plt.xlim([min(xticks), max(xticks)])
    plt.xticks(xticks, labels=xlabels, rotation=0)

    plt.title("How Fast Does Hair Grow?")
    plt.ylabel("Length (mm)")
    plt.xlabel("Date")

    plt.tight_layout()
    plt.show()

    return


def pretty_date(t):
    tobj = dt.datetime.fromtimestamp(t)
    return tobj.strftime("%b %d")


if __name__ == "__main__":
    main()
