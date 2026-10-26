#!/usr/bin/env python3

WUBRG = ['w', 'u', 'b', 'r', 'g']


def swap(colors, i, j):
    tmp = list(colors)
    tmp[i % 5], tmp[j % 5] = tmp[j % 5], tmp[i % 5]
    return tuple(tmp)


def rotate(colors, offset):
    tmp = list(colors)
    tmp = tmp[offset:] + tmp[:offset]
    return tuple(tmp)


def sample(colors, n):
    return colors[:n]


def hash(seq):
    return pretty(sorted(seq))


def pretty(seq):
    return "".join([pretty_char(c) for c in seq])


def pretty_char(c):
    return {
        "w": "\033[33mW\033[0m",
        "u": "\033[36mU\033[0m",
        "b": "\033[35mB\033[0m",
        "r": "\033[31mR\033[0m",
        "g": "\033[32mG\033[0m",
    }[c.lower()]


samples = []

colors = rotate(WUBRG, -1)


for i in range(10):

    colors = rotate(colors, 1)
    print(pretty(colors))
    if i % 4 in [1, 2]:
        colors = swap(colors, 2, 3)
        print(pretty(colors))

    s = sample(colors, 3)
    samples.append(s)
    print("sample:", pretty(s))

print("-----")




print("unique combinations:", len(set([hash(s) for s in samples])))

