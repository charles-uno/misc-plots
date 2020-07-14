
import matplotlib.pyplot as plt
import numpy as np
import sys

from . import data, cleanup

# ======================================================================

SAVE = '--save' in sys.argv

def collage(cardname, sort=False, art_ratio=(1, 1), canvas_ratio=(1, 1), path=None, **kwargs):
    if path is None:
        path = 'mtg-collage-%s.png' % cardname
    slugs = cleanup.get_slugs(cardname, **kwargs)
    # Based on the number of slugs, figure out an appropriate resize
    # factor, and an appropriate crop.
    xpx, ypx = get_art_dims(slugs, art_ratio)
    nx, ny = get_canvas_dims(slugs, canvas_ratio)
    slugs = sorted_slugs(slugs, nx, ny) if sort else slugs[:nx*ny]

#    slugs = list(slugs)
#    credits = data.get_credits(cardname)
#    credits_path = path.replace('.png', '.txt')
#    with open(credits_path, 'w') as handle:
#        [ handle.write(credits[x] + '\n') for x in slugs ]


    # Slap the illustrations, croped and rescaled appropriately, onto a
    # big canvas.
    canvas = np.zeros( (ny*ypx, nx*xpx, 3) )

    print('canvas size:', *canvas.shape)

    for i, slug in enumerate(slugs):
        # Figure out where it's going on the canvas.
        ix = i // ny
        iy = i % ny
        # Stick it on the canvas.
        tmp = cleanup.get_art(slug, crop=(xpx, ypx))
        canvas[ypx*iy:ypx*(iy+1), xpx*ix:xpx*(ix+1), :] = tmp
    return show_canvas(canvas, path=path, save=SAVE)

# ----------------------------------------------------------------------

def show_canvas(canvas, path='mtg-collage.png', save=False):
    height, width = canvas.shape[:2]
    # Constrain the size in square inches. Go bigger if we're saving,
    # smaller if we're showing.
    if save:
        dpi = 40
        wd = 1920*1080*canvas.shape[0]
        ht = 1920*1080*canvas.shape[1]

        wd, ht = 1080*(canvas.shape[1]/canvas.shape[0])/dpi, 1080/dpi

        print('width, height:', wd, ht)

    else:
        dpi = 100
        total_sq_inches = 50
        norm = np.sqrt( total_sq_inches/(height*width) )
        wd, ht = width*norm, height*norm

    plt.figure(figsize=(wd, ht), dpi=dpi)
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
    plt.imshow(canvas)
    if save:
        return plt.savefig(path, dpi=dpi)
    else:
        return plt.show()

# ======================================================================

def get_art_dims(slugs, art_ratio=(1,1)):
    # Make sure we have enough pixels to comfortably support 1920x1080.
    shapes = [ cleanup.get_shape(x) for x in slugs ]
    # We don't know a priori whether we'll be constrained by x or y.
    xmin0 = min( x[0] for x in shapes )//art_ratio[0] * art_ratio[0]
    ymin0 = xmin0//art_ratio[0] * art_ratio[1]
    ymin1 = min( x[1] for x in shapes )//art_ratio[1] * art_ratio[1]
    xmin1 = ymin1//art_ratio[1] * art_ratio[0]
    xmin, ymin = min( (xmin0, ymin0), (xmin1, ymin1) )
    # Shoot to have enough pixels to make a 1920x1080 image. Throw a
    # factor of 2 on there just in case.
    src_pixels = xmin*ymin*len(slugs)
    out_pixels = 1920*1080
    resize = max(int( np.sqrt(src_pixels/out_pixels) ), 1)

    print(xmin, 'x', ymin, '->', xmin//resize, 'x', ymin//resize)

    # From now on, whenever we load an image, we'll downsample by this
    # amount right away.
    cleanup.set_resize(resize)
    return xmin//resize, ymin//resize

# ----------------------------------------------------------------------

def get_canvas_dims(slugs, canvas_ratio=(1, 1), max_blanks=3):
    blocksize = canvas_ratio[0]*canvas_ratio[1]
    blocks = int( np.sqrt((len(slugs) + max_blanks)/blocksize) )
    return canvas_ratio[0]*blocks, canvas_ratio[1]*blocks

# ======================================================================

def sorted_slugs(slugs, nx, ny):
    # First, sort by average color intensity.
    def sortkey(slug):
        return np.mean( cleanup.get_rgb(slug) )

    print(len(slugs), 'slugs ->', nx*ny, 'slugs')

    # TODO -- Right now, we just chop off the final few slugs. There's
    # probably a better way to trim to the appropriate number.
    slugs = sorted(slugs, key=sortkey)[:nx*ny]
    # Then, for each row, sort by relative blueness.
    while slugs:
        def sortkey(slug):
            rgb = cleanup.get_rgb(slug)
            return rgb[0]/rgb[2]
        for slug in sorted(slugs[:ny], key=sortkey):
            yield slug
        slugs = slugs[ny:]
