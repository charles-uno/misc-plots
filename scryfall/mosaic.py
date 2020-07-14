#!/usr/bin/env python3

import sys

import scryfall

# ======================================================================

SORT = '--sort' in sys.argv

UNIQUE = '--unique' in sys.argv

THUMB = '--thumb' in sys.argv

def main():

    # TODO -- use argparse to do this right. Also handle SAVE, LOCAL, WIDE?

    cardname = min( x for x in sys.argv[1:] if not x.startswith('-') )

    return scryfall.collage(
        cardname,
        art_ratio=(1, 1) if THUMB else (4, 3),
        canvas_ratio=(1, 1) if THUMB else (4, 3),
        unique=UNIQUE,
        sort=SORT,
        path='mtg-collage-%s%s%s.png' % ('' if UNIQUE else 'all-', cardname, '-thumb' if THUMB else '')

    )

# ======================================================================

if __name__=='__main__':
    main()
