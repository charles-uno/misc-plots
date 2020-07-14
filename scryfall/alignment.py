#!/usr/bin/env python3

import json
import os
from PIL import Image
import requests
import time

import numpy as np

import matplotlib.image as mpimg
import matplotlib.pyplot as plt




def main():

    # Lawful: one mana per turn
    # Chaotic: mana is meaningless

    # Good: wins by attacking
    # Evil: wins by concession

    cardnames = [
        "Monastery Swiftspear",
        "Aether Vial",
        "Prized Amalgam",

        "Liliana of the Veil",
        "Primeval Titan",
        "Neoform",

        "Mystic Sanctuary",
        "Expedition Map",
        "Grinding Station",
    ]

    fig, axes = plt.subplots(3, 3, figsize=(8, 6))

    plt.subplots_adjust(
        left=0.05,
        bottom=0.05,
        right=0.95,
        top=0.95,
        wspace=0.6,
        hspace=None,
    )
    for ax in axes.flatten():
        ax.tick_params(bottom=False, left=False, top=False, right=False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    aspect = 0.75

    for ax, cardname in zip(axes.flatten(), cardnames):

        img = get_art(cardname)
        ax.imshow(np.abs(img))
#        ax.set_title("foo")
#        ax.set_xlabel("bar")

        aspect_offset = aspect*img.shape[1]/img.shape[0]
        ax.set_aspect(aspect_offset)


    axes[0, 0].set_title("lawful: one mana per turn")
    axes[0, 1].set_title("neutral: cheats on mana")
    axes[0, 2].set_title("chaotic: mana is meaningless")

    axes[0, 0].set_ylabel("good: wins by attacking")
    axes[1, 0].set_ylabel("neutral: wins with creatures")
    axes[2, 0].set_ylabel("evil: wins by concession")


#    plt.figure(figsize=(wd, ht), dpi=dpi)
#    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
#    plt.imshow(art)

    plt.tight_layout()
    plt.show()




def get_art(cardname):
    save_art(cardname)
    slug = get_slug(cardname)
    png_path = os.path.join(ART_DIR, f"{slug}.png")
    return mpimg.imread(png_path)[:, :, :3]


ART_DIR = "art/"


def save_art(cardname):
    os.makedirs(ART_DIR, exist_ok=True)
    slug = get_slug(cardname)
    png_path = os.path.join(ART_DIR, f"{slug}.png")
    if os.path.exists(png_path):
        print("already have:", png_path)
        return
    try:
        url = get_card(cardname)["image_uris"]["art_crop"]
    except Exception:
        print("CHOKED ON:", cardname)
        raise
    fmt = url.split(".")[-1].split("?")[0]
    raw_path = os.path.join(ART_DIR, f"{slug}.{fmt}")
    # Grab the raw image, regardless of format
    if not os.path.exists(raw_path):
        print("saving:", raw_path)
        with open(raw_path, 'wb') as handle:
            handle.write(get_url(url).content)
    # If it's a JPG, convert to a PNG
    if raw_path != png_path:
        print("converting to:", png_path)
        Image.open(raw_path).save(png_path)
        os.remove(raw_path)
    return


def get_slug(cardname):
    tmp = cardname.lower()
    for c in "',":
        tmp = tmp.replace(c, "")
    for c in " ":
        tmp = tmp.replace(c, "-")
    return tmp


def get_card(cardname):
    return get_url(
        "https://api.scryfall.com/cards/search?",
        q=f"!'{cardname}'",
    ).json()["data"][0]


def get_url(url, **kwargs):
    time.sleep(0.2)
    return requests.get(
        url=url,
        params=kwargs,
    )


if __name__ == '__main__':
    main()
