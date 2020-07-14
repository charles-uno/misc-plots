
import json
import matplotlib.pyplot as plt
import math
import numpy as np
import sys

plt.rcParams.update({"font.size": 16})

# ----------------------------------------------------------------------

def scatter(loadfile, xkey, ykey, **kwargs):
    plt.figure(figsize=(10, 10))
    plt.gcf().text(0.99, 0.01, "charles.uno", fontsize=8, horizontalalignment="right")
    # Figure out values, skipping bad ones
    skip = kwargs.get("skip", [])
    xvals, yvals = [], []
    for name, elt in load_json(loadfile).items():
        if not elt.get(xkey) or not elt.get(ykey):
            continue
        if elt["name"] in skip:
            continue
        xvals.append(elt[xkey])
        yvals.append(elt[ykey])
        # Label each point
        highlight(elt, xkey, ykey, **kwargs)
    # Put the data on the plot
    plt.scatter(xvals, yvals, zorder=2, alpha=0.8)
    # Trend line
    log = kwargs.get("log", "")
    if kwargs.get("trend", True):
        xfit, yfit = lin_fit(xvals, yvals, log=log)
        plt.plot(xfit, yfit, color="gray", ls=":", lw=0.5, zorder=0)
    # Title and axis labels
    plt.title(kwargs.get("title", "ADD TITLE HERE"))
    plt.xlabel(kwargs.get("xlabel", "ADD X LABEL HERE"))
    plt.ylabel(kwargs.get("ylabel", "ADD Y LABEL HERE"))
    # Axis finagling
    if "x" in log:
        plt.xscale("log")
    if "y" in log:
        plt.yscale("log")
    # Optionally overwrite default ticks and labels
    xlim = kwargs.get("xlim")
    ylim = kwargs.get("ylim")
    xticks = kwargs.get("xticks")
    yticks = kwargs.get("yticks")
    xticklabels = kwargs.get("xticklabels")
    yticklabels = kwargs.get("yticklabels")
    if xlim:
        plt.xlim(xlim)
    elif xticks:
        plt.xlim(min(xticks), max(xticks))
    if ylim:
        plt.ylim(ylim)
    elif yticks:
        plt.ylim(min(yticks), max(yticks))
    if xticks:
        plt.xticks(xticks, xticklabels)
    if yticks:
        plt.yticks(yticks, yticklabels)
    # Draw the plot!
    plt.tight_layout()
    if "--save" in sys.argv:
        return plt.savefig(kwargs.get("savefile", "out.png"))
    else:
        return plt.show()

# ----------------------------------------------------------------------

def highlight(obj, xkey, ykey, **kwargs):
    name, xval, yval = obj["name"], obj[xkey], obj[ykey]
    return plt.text(
        xval,
        yval,
        "  " + name,
        horizontalalignment="left",
        verticalalignment="center",
        fontsize=kwargs.get("namesize"),
    )

# ----------------------------------------------------------------------

def read_lines(filename):
    with open(filename, "r") as handle:
        return [ x.rstrip() for x in handle ]

# ----------------------------------------------------------------------

def dump_json(obj, filename):
    with open(filename, "w") as handle:
        json.dump(obj, handle, indent=4, sort_keys=True)

# ----------------------------------------------------------------------

def load_json(filename):
    with open(filename, "r") as handle:
        return json.load(handle)

# ----------------------------------------------------------------------

def lin_fit(xin, yin, log=""):
    if "x" in log:
        xin = np.log(xin)
    if "y" in log:
        yin = np.log(yin)
    m, b = np.polyfit(xin, yin, 1)
    dx = max(xin) - min(xin)
    xout = np.linspace(min(xin) - dx, max(xin) + dx, 100)
    yout = m*xout + b
    if "x" in log:
        xout = np.exp(xout)
    if "y" in log:
        yout = np.exp(yout)
    return xout, yout

# ----------------------------------------------------------------------

def get_log_ticks(vals, base=2):
    vmin, vmax = min(vals), max(vals)
    # Round up and down to powers
    pmin = math.floor(np.log(vmin)/np.log(base))
    pmax = math.ceil(np.log(vmax)/np.log(base))
    powers = list(range(pmin, pmax+1))
    while len(powers) > 5 and len(powers) % 2:
        powers = powers [::2]
    ticks = [ base**p for p in powers ]
    labels = []
    for p in powers:
        if p < 0:
            # 1/10 -> "\u2152"
            # Fraction
#            labels.append("1/" + str(base**-p))
            # Round
            labels.append(("%.3f" % base**p).rstrip("0"))
        else:
            labels.append(str(base**p))
    return ticks, labels
