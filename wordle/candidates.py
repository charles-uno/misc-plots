#!/usr/bin/env python3

import collections

with open('solutions.txt', 'r') as handle:
    SOLUTIONS = [line.strip() for line in handle]


def main():
    letter_counts = collections.defaultdict(int)
    for s in SOLUTIONS:
        for c in s:
            letter_counts[c] += 1
    count_letter = sorted((n, c) for c, n in letter_counts.items())
    top_letters = {c for n, c in count_letter[-10:]}

    for s in SOLUTIONS:
        letters = set(s)
        if len(letters ^ top_letters) != 5:
            continue
        print(s)


if __name__ == '__main__':
    main()
