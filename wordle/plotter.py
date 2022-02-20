#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys

TEXT_COLOR = 'white'
BAR_COLOR = 'green'

N_TARGET = 365
X_MAX = N_TARGET*0.5
X_PAD = N_TARGET*(0.07 if N_TARGET > 100 else 0.05)


def main():
    fig, axes = plt.subplots(4, 3)
    fig.set_size_inches(8, 8)

    plt.suptitle('A Year of Wordles by Opening Guess\n', fontsize=16)

    words = [
        'adept',
        'adieu',
        'crane',
        'fluff',
        'geese',
        'jerky',
        'lymph',
        'moist',
        'ratio',
        'slice',
        'soare',
        'xylyl'
    ]

    for ax, word in zip(axes.flatten(), words):
        draw_panel(ax, word)
    if '--save' in sys.argv:
        plt.savefig('wordle-graphs.png', dpi=200)
    else:
        plt.show()


def draw_panel(ax, word):
    filename = 'out/%s.csv' % word
    with open(filename, 'r') as handle:
        data = [int(x.strip()) for x in handle]
    n_data = len(data)
    n_whiffs = data.count(0)
    n_wins = n_data - n_whiffs
    norm = N_TARGET*1./n_data
    yvals = [1, 2, 3, 4, 5, 6]
    xvals = [0]*6
    for d in data:
        if d > 0:
            xvals[d-1] += 1
    xvals = [x*norm for x in xvals]
    xvals_offset = [x+X_PAD for x in xvals]
    for edge in ('top', 'bottom', 'left', 'right'):
        ax.spines[edge].set_visible(False)
    ax.barh(yvals, xvals_offset, align='center', color=BAR_COLOR)
    plt.tight_layout()
    ax.invert_yaxis()
    ax.set_yticks([1, 2, 3, 4, 5, 6])
    ax.set_xticks([])
    ax.set_xlim([0, X_MAX])
    ax.tick_params(axis='both', which='both',length=0)
    # No error bars, but we'll show a range in the label
    dxvals = [x**0.5 for x in xvals]
    xmins = [max(0, x-dx) for x, dx in zip(xvals, dxvals)]
    xmaxs = [x+dx for x, dx in zip(xvals, dxvals)]
    for i, _ in enumerate(yvals):
        lmin, lmax = '%.0f' % xmins[i], '%.0f' % xmaxs[i]
        label = ' %s ' % lmin if lmin == lmax else ' %s-%s ' % (lmin, lmax)
        ax.text(xvals_offset[i], yvals[i], label, color=TEXT_COLOR, ha='right', va='center')
    # Label at the top of each frame
    f = n_whiffs*norm
    df = f**0.5
    fmin, fmax = max(0, f-df), f+df
    fail_count_label = '%.0f-%.0f losses/year' % (fmin, fmax)

    rmax, rmin = (N_TARGET-fmin)*100./N_TARGET, (N_TARGET-fmax)*100./N_TARGET

    win_rate_label = '%.0f%%-%.0f%% Win Rate' % (rmin, rmax)
    label = word.upper() + '\n' + win_rate_label
    ax.text(X_MAX/2, 0, label, ha='center', va='center', linespacing=1.3)


if __name__ == '__main__':
    main()
