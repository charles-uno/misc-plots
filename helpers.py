
import json
import math
import numpy as np

def read_lines(filename):
    with open(filename, "r") as handle:
        return [ x.rstrip() for x in handle ]

def dump_json(obj, filename):
    with open(filename, "w") as handle:
        json.dump(obj, handle, indent=4)

def load_json(filename):
    with open(filename, "r") as handle:
        return json.load(handle)

def lin_fit(xin, yin, xlog=False):
    if xlog:
        xin = np.log(xin)
    m, b = np.polyfit(xin, yin, 1)
    dx = max(xin) - min(xin)
    xout = np.linspace(min(xin) - dx, max(xin) + dx, 100)
    yout = m*xout + b
    if xlog:
        xout = np.exp(xout)
    return xout, yout


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
