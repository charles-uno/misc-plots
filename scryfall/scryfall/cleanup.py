
import collections
import numpy as np
import sys

from . import data

# ======================================================================

RESIZE = 1

def get_art(slug, crop=None):
    img = data.get_raw_art(slug)[::RESIZE, ::RESIZE, :]
    # If we're cropping to a certain size, grab from the middle.
    if crop is not None:
        i0 = (img.shape[0] - crop[1])//2
        j0 = (img.shape[1] - crop[0])//2
        if i0 < 0 or j0 < 0:
            raise ValueError('Failed to crop ' + str(img.shape) + ' to ' + str(crop))
        img = img[i0:i0 + crop[1], j0:j0 + crop[0], :]
    return img

# ----------------------------------------------------------------------

def set_resize(resize):
    global RESIZE
    RESIZE = resize
    return

# ======================================================================

def get_slugs(cardname, unique=False):
    """Accept a card name. Return the slug for each card of that name.
    Optionally, remove duplicate illustrations. Any art not available
    locally will be downloaded from Scryfall.
    """
    slugs = list( data.get_all_slugs(cardname) )
    [ load_metadata(x) for x in slugs ]
    return list( get_unique_slugs(slugs) ) if unique else slugs

# ----------------------------------------------------------------------

def get_unique_slugs(slugs):
    # We're looking for duplicate illustrations. We can make this easier
    # by first clumping by artist.
    slugs_by_artist = collections.defaultdict(set)
    for slug in slugs:
        name, artist = slug.split('-')[:2]
        slugs_by_artist[name, artist].add(slug)
    # For each artist, look for duplicates.
    for artist, slugs in slugs_by_artist.items():
        for slug in _get_unique_slugs(slugs):
            yield slug

# ----------------------------------------------------------------------

def _get_unique_slugs(slugs):
    """This looks at all possible combinations, so make sure to filter
    by card name and artist before calling.
    """
    # Get a list of all pairwise comparisons we can make. We'll check
    # them all. We also want to keep tabs on all the unmatched ones.
    unpaired = set(slugs)
    pairs = { (x, y) for x in slugs for y in slugs if x < y }
    # Find matches by pairwise exhaustive search. Hopefully we've
    # filtered by artist so N is small (dozens?).
    for pair in sorted(pairs):
        if same_art(*pair):
            [ unpaired.discard(x) for x in pair ]
        else:
            pairs.discard(pair)
    # Clump the pairwise matches into groups. Keep going until there's
    # no more overlap.
    while consolidate_groups(pairs):
        pass
    # Keep all the unpaired slugs, plus one from each group.
    return list(unpaired) + [ x[0] for x in pairs ]

# ----------------------------------------------------------------------

def consolidate_groups(groups):
    """Accept a set of tuples. Find a pair of overlapping tuples, pop
    them out, and add their union. Modifications are made in-place.
    Return False if there are no more overlapping groups.
    """
    if not groups:
        return False
    # If each name appears in exactly one group, there's nothing left to
    # combine.
    unique_slugs = set.union( *[ set(x) for x in groups ] )
    listed_slugs = sum(groups, ())
    if len(unique_slugs) == len(listed_slugs):
        return False
    groups_by_slug = {}
    for group in sorted(groups):
        for slug in group:
            # If this name is already listed, we have an intersection.
            if slug in groups_by_slug:
                match = groups_by_slug[slug]
                groups.remove(match)
                groups.remove(group)
                groups.add( tuple( set(group) | set(match) ) )
                return True
            else:
                groups_by_slug[slug] = group
    # Should never get here.
    raise RuntimeError('UH OH')

# ======================================================================

def same_art(slug0, slug1):
    """Accept two card slugs. Check their gray-downs against one
    another. Return True if they seem to be the same illustration, False
    otherwise.
    """
    gray0, gray1 = get_grays(slug0), get_grays(slug1)
    return np.std(gray1 - gray0) < 0.05

# ======================================================================

GRAYS = {}

RGB = {}

SHAPES = {}

def load_metadata(slug):
    global GRAYS, RGB, SHAPES
    if slug not in GRAYS or slug not in RGB or slug not in SHAPES:
        print('Getting metadata:', slug)
        img = data.get_raw_art(slug)
        GRAYS[slug] = _get_grays(img)
        RGB[slug] = _get_rgb(img)
        SHAPES[slug] = img.shape[:3]
    return

# ----------------------------------------------------------------------

def get_grays(slug, n=6, rgb=False):
    """Accept a card slug and a number N (default 6). Partition that
    slug's image into an NxN grid and get the average intensity of each
    partition. Return an NxN array of those values.
    """
    global GRAYS
    if slug not in GRAYS:
        print('Getting grays:', slug)
        GRAYS[slug] = _get_grays(data.get_raw_art(slug), n=n)
    return intensity_to_gray( GRAYS[slug] ) if rgb else GRAYS[slug]

# ----------------------------------------------------------------------

def _get_grays(img, n=6):
    grays = np.zeros( (n, n) )
    wd, ht = img.shape[:2]
    for i in range(n):
        for j in range(n):
            tmp = img[i*wd//n:(i+1)*wd//n, j*ht//n:(j+1)*ht//n]
            grays[i, j] = np.mean(tmp)
    return grays

# ----------------------------------------------------------------------

def get_rgb(slug):
    """Accept a card slug. Return an (R, G, B) tuple corresponding to
    the mean color of that card's art.
    """
    global RGB
    if slug not in RGB:
        print('Getting RGB:', slug)
        RGB[slug] = _get_rgb( data.get_raw_art(slug) )
    return RGB[slug]

# ----------------------------------------------------------------------

def _get_rgb(img):
    return (
        np.mean( img[:, :, 0] ),
        np.mean( img[:, :, 1] ),
        np.mean( img[:, :, 2] ),
    )

# ----------------------------------------------------------------------

def get_shape(slug):
    global SHAPES
    if slug not in SHAPES:
        SHAPES[slug] = data.get_raw_art(slug).shape
    return SHAPES[slug]

# ======================================================================

def intensity_to_gray(arr):
    img = np.ndarray( arr.shape[:2] + (3,) )
    for i in range(3):
        img[:, :, i] = arr
    return img
