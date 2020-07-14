
import glob
import json
import matplotlib.image as mpimg
import os
# Image library (third party) is used to convert JPG to PNG.
from PIL import Image
import requests
import sys
import time
# Just use this to assemble URLs for error messages.
import urllib.parse

# ======================================================================

def get_credits(cardname):

    credits = {}

    for card in search('!"%s"' % cardname, unique='prints'):

        credits[ get_slug(card) ] = '%s (%s) by %s' % (card['name'], card['set_name'], card['artist'])

#        keys = ['name', 'set_name', 'artist', 'frame']
#        print()
#        [ print(x, ':', card[x]) for x in keys ]

#        if len(credits) > 10:
#            break

    return credits




# ======================================================================

LOCAL = '--local' in sys.argv

def get_all_slugs(cardname):
    # Slugs make no sense unless the corresponding image is cached
    # locally. So cache the images as we go.
    if LOCAL:
        return list( get_local_slugs(cardname) )
    else:
        slugs = []
        for card in search('!"%s"' % cardname, unique='prints'):
            save_art(card)
            slugs.append( get_slug(card) )
        return slugs

# ----------------------------------------------------------------------

ART_DIR = '/home/charles/Desktop/scryfall/art/'

def get_local_slugs(cardname):

#    tally = 0

    for path in glob.glob(ART_DIR + cardname + '-*.png'):
        yield path.split('/')[-1].split('.')[0]

#        tally += 1
#        if tally == 12*9:
#            break

# ----------------------------------------------------------------------

def search(query='', **kwargs):
    kwargs['q'] = query
    url = 'https://api.scryfall.com/cards/search?'
    while url:
        scryfall_json = get_json(url, **kwargs)
        for card in scryfall_json['data']:
            yield card
        # If there's another page, get rid of our kwargs and use
        # whatever URL they pass along.
        url = scryfall_json.get('next_page', None)
        # Rate limiting. They say no more than 10 pages per second.
        kwargs = {}

# ----------------------------------------------------------------------

def get_json(url, **kwargs):
    reply = get_url(url, **kwargs).json()
    # If something goes wrong, pass along the reply and bail.
    if 'data' not in reply:
        print(url + urllib.parse.urlencode(kwargs))
        sys.exit( json.dumps(reply, indent=4) )
    return reply

# ----------------------------------------------------------------------

def get_url(url, **kwargs):
    time.sleep(0.2)
    return requests.get(url, params=kwargs)

# ======================================================================

def save_art(card):
    # If we don't have a place to put this art yet, make one.
    if not os.path.isdir(ART_DIR):
        os.mkdir(ART_DIR)
    # Check if we have art for this card already.
    slug = get_slug(card)
    png_path = os.path.join(ART_DIR, slug + '.png')
    # If we have a PNG, we're good.
    if os.path.exists(png_path):
        return
    url = card['image_uris']['art_crop']
    fmt = url.split('.')[-1].split('?')[0]
    raw_path = os.path.join(ART_DIR, slug + '.' + fmt)
    # If we have nothing, grab a raw image.
    if not os.path.exists(raw_path):
        print('Saving:', slug)
        with open(raw_path, 'wb') as handle:
            handle.write(get_url(url).content)
    # If we have only a JPG, turn it into a PNG.
    if raw_path != png_path:
        print('Converting:', slug)
        Image.open(raw_path).save(png_path)
        os.remove(raw_path)
    return

# ----------------------------------------------------------------------

def get_raw_art(slug):
    path = os.path.join(ART_DIR, slug + '.png')
    return mpimg.imread(path)[:, :, :3]

# ======================================================================

def get_slug(card):
    return (
        slugify( card['name'] ) + '-' +
        slugify( card['artist'] ) + '-' +
        card['set'] + '-' +
        card['collector_number']
    )

# ----------------------------------------------------------------------

def slugify(line):
    """Accept a name. Drop it to lowercase, remove the special
    characters, and return it.
    """
    tmp = line.lower()
    for char in '\'- ,!&.':
        tmp = tmp.replace(char, '')
    # Keep an eye out for new special characters.
    if any( not x.isalnum() for x in tmp ):
        print(line)
        raise RuntimeError('Need update to slugify!')
    return tmp
