#!/usr/bin/env python3

import imageio
import numpy as np
import random


N_ROWS = 5
N_COLS = 3

DOT_SIZE = 20

OFFSET = N_ROWS*N_COLS + 1

def main():

    seats = []
    for row in range(N_ROWS):
        for col in range(1, N_COLS+1):
            seats.append((row, col))

    print("number of seats:", len(seats))

    random.shuffle(seats)

    queue = []
    for i, (row, col) in enumerate(seats):
        queue.append({"pos": i, "row": row, "col": col, "seated": False})

    imgs = []
    for _ in range(100):
        queue = next_queue(queue)
        imgs.append(draw_queue(queue))

        if all(q["seated"] for q in queue):
            imgs.append(draw_queue(queue))

            break

    return imageio.mimsave("queue.gif", imgs, "GIF", duration=0.1)


def next_queue(q_old):
    positions = [q["pos"] for q in q_old if not q["seated"]]
    q_new = []
    for qo in q_old:
        qn = qo.copy()
        if qn["pos"] == OFFSET + qn["row"]:
            qn["seated"] = True
        if not qn["seated"] and qn["pos"]+1 not in positions:
            qn["pos"] += 1
        q_new.append(qn)
    return q_new


def draw_queue(queue):
    img = np.zeros((100, (OFFSET + N_ROWS*N_COLS)*DOT_SIZE, 3))

    for q in queue:

        x = 30
        if q["seated"]:
            x += DOT_SIZE*q["col"]

        y = DOT_SIZE*(q["pos"] + 1)

        img = add_dot(img, (x, y))

    return img


def add_dot(img, pos, r=None):
    if not r:
        r = DOT_SIZE//2
    x0, y0 = pos
    for x in range(x0 - r, x0 + r + 1):
        for y in range(y0 - r, y0 + r + 1):

            if not 0 <= x < img.shape[0] or not 0 <= y < img.shape[1]:
                continue

            if (x - x0)**2 + (y - y0)**2 <= r**2:
                img[x, y, :] = 1
    return img





def color(q):
    x = q["row"]/N_ROWS
    return [x, 0, 1-x]


if __name__ == "__main__":
    main()
