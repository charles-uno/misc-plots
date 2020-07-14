#!/usr/bin/env python3

import glob
import imageio
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams["figure.titlesize"] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Roboto Condensed'
matplotlib.rcParams['text.latex.preamble'] = [
    '\\usepackage[sfdefault,condensed]{roboto}',
    '\\usepackage{sansmath}',
    '\\usepackage{amsfonts}',
    '\\usepackage{pifont}',
    '\\sansmath'
]
import numpy as np
import os
import sys

import scryfall

# ======================================================================

N = 4

def main():

    slug_pairs = [

        # Same image, but one is foil.
        [
            'forest-alaynadanner-gk1-127',
            'forest-alaynadanner-prwk-A09'
        ],

        # Same image, but printed more brightly.
        [
            'forest-jimnelson-m10-249',
            'forest-jimnelson-dds-64',
        ],

        # Same image, but difference due to old/new card frame.
        [
            'forest-alanpollack-inv-348',
            'forest-alanpollack-dde-71',
        ],

        # Similar look, with deep green and vertical pine trunks
        [
            'forest-johnavon-8ed-348',
            'forest-johnavon-unh-140',
#            'forest-johnavon-ust-216',
        ],

        # Two in a series, one darker and without a deer. Close!
        [
            'forest-eytanzana-isd-264',
            'forest-eytanzana-avr-244',
        ],

    ]

    for sp in slug_pairs:
        minus_equals(sp)


    assemble('alaynadanner', 'johnavon')


    return


# ----------------------------------------------------------------------


def assemble(*artists):
    imgs = []

    for artist in artists:

        paths = sorted( glob.glob(artist + '*.png') )
        if not paths:
            raise ValueError('No art for ' + artist)

        [ imgs.append( imageio.imread(x) ) for x in paths ]
        # Show the last one for twice as long.
        imgs.append( imgs[-1] )

        # Stick a blank in between artists.
        if len(artists) > 1:
            imgs.append( imageio.imread('blank.png') )

    name = '-'.join(artists) + '.gif'

    return imageio.mimsave(name, imgs, 'GIF', duration=0.4)

# ----------------------------------------------------------------------

def minus_equals(slugs):
    # Get color images and make sure they are the same size.
    color_imgs = [ scryfall.get_art(x) for x in slugs ]
    xmin = min( x.shape[0] for x in color_imgs )
    ymin = min( x.shape[1] for x in color_imgs )
    color_imgs = [ x[:xmin, :ymin, :3] for x in color_imgs ]
    color_imgs.append( np.abs( color_imgs[1] - color_imgs[0] ) )
    # Get black and white versions and make sure they are the same size.
    bw_imgs = [ scryfall.get_art(x, bw=True) for x in slugs ]
    bw_imgs = [ x[:xmin, :ymin, :3] for x in bw_imgs ]
    bw_imgs.append( bw_imgs[1] - bw_imgs[0] )
    # Get the grayscale differences. 4x4 is good for legibility.
    grays = [ scryfall.gray_down(x, rgb=True, n=N) for x in slugs ]
    grays.append( grays[1] - grays[0] )

    artist = slugs[0].split('-')[1]
    tally = 0
    for imgs in [color_imgs, bw_imgs, grays]:
        show_subtraction(imgs, slugs=slugs, filename=artist + '-' + str(tally) + '.png')
        show_subtraction(imgs, slugs=slugs, filename=artist + '-' + str(tally+1) + '.png', check=True)
        tally += 2
    return

# ----------------------------------------------------------------------

def show_subtraction(imgs, slugs, check=False, filename=None):

    aspect = 0.75

    set_names = {
        'gk1': 'GRN Guild Kit',
        'prwk': 'Ravnica Weekend',
        'dds': 'Mind vs Might',
        'dpa': 'Duels of the Planeswalkers',
        'dde': 'Phyrexia vs the Coalition',
        'inv': 'Invasion',
        '8ed': '8th Edition',
        'unh': 'Unhinged',
        'ust': 'Unstable',
        'cma': 'Commander Anthology',
        'isd': 'Innistrad',
        'm10': 'Magic 2010',
        'avr': 'Avacyn Restored',

    }

    artist_names ={
        'alaynadanner': 'Alayna Danner',
        'johnavon': 'John Avon',
        'jimnelson': 'Jim Nelson',
        'alanpollack': 'Alan Pollack',
        'eytanzana': 'Eytan Zana',
    }



    slugs.append('Difference')

    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.6, hspace=None)
    for ax in axes.flatten():
        ax.tick_params(bottom=False, left=False, top=False, right=False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    axes[0].annotate('--', xy=(1.35, 0.7), xycoords='axes fraction', fontsize=128, horizontalalignment='center', verticalalignment='center')
    axes[1].annotate('=', xy=(1.35, 0.6), xycoords='axes fraction', fontsize=128, horizontalalignment='center', verticalalignment='center')
    # Add the art to the plot. Make sure the aspect ratios line up.
    for ax, img, slug in zip(axes, imgs, slugs):
        ax.imshow( np.abs(img) )

        if '-' in slug:

            artist, exp, num = slug.split('-')[1:]
            artist = artist_names.get(artist, artist)
            exp = set_names.get(exp, exp)
            ax.set_title(exp + ' \#' + num)
            ax.set_xlabel(artist)


        else:
            ax.set_title(slug)


        aspect_offset = aspect*img.shape[1]/img.shape[0]
        ax.set_aspect(aspect_offset)
        # If there are only a handful of pixels, label them.
        if img.shape[0] < 10:
            for i in range( img.shape[0] ):
                for j in range( img.shape[1] ):
                    z = img[i, j, 0]
                    txt = ax.text(
                        j,
                        i,
                        s='%.2f' % z,
                        fontsize=16,
                        weight='bold',
                        color='k' if z > 0.2 else 'w',
                        horizontalalignment='center',
                        verticalalignment='center',
                        zorder=1,
                    )

    if not check:
        pass
    elif img.shape[0] > 10:
        axes[-1].text(0.5, 0.5, s='? ? ?', color='white', weight='bold', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=80, zorder=2)
    elif np.std( imgs[-1] ) < 0.05:
        axes[-1].text(0.5, 0.5, s=r'\ding{51}', color='green', weight='bold', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=128, zorder=2)
    else:
        axes[-1].text(0.5, 0.5, s=r'\ding{55}', color='red', weight='bold', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=128, zorder=2)

    if '--save' in sys.argv:
        plt.savefig(filename)
        return plt.close()
    else:
        return plt.show()


# ======================================================================

if __name__ == '__main__':
    main()
