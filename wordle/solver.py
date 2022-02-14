#!/usr/bin/env python3

import random
import sys

OPENING_GUESS = 'crane'

N = 1000
N_COLS = 10

LENGTH = 5
MAX_GUESSES = 6

GREEN = '\033[92m'
RESET = '\033[0m'
YELLOW = '\033[93m'
BLACK = ''

ALPHABET = [chr(i) for i in range(ord('a'), ord('z')+1)]

with open('words.txt', 'r') as handle:
    WORDS = [line.strip() for line in handle]

with open('solutions.txt', 'r') as handle:
    SOLUTIONS = [line.strip() for line in handle]


def main():
    histogram = {i: 0 for i in range(MAX_GUESSES+1)}
    for _ in range(N):
        result = Result()
        histogram[result.turns] += 1
        print_across(result)
    print_stats(histogram)


def print_stats(histogram):
    whiffs = histogram[0]
    total = sum(histogram.values())
    num = sum(n*histogram[n] for n in range(1, MAX_GUESSES+1))
    denom = sum(histogram[n] for n in range(1, MAX_GUESSES+1))
    avg = "%.2f" % (num/denom)
    print()
    [print(i, histogram[i]) for i in range(MAX_GUESSES+1)]
    print("success rate:", fmt(total - whiffs, total))
    print("average guesses:", avg)


def fmt(num, denom):
    p = (num*100./denom)
    dp = 100./(denom)**0.5
    return "%.0f%% ± %.0f%%" % (p, dp)


PRINT_CACHE = []


def print_across(result):
    global PRINT_CACHE
    PRINT_CACHE.append(result)
    if len(PRINT_CACHE) == N_COLS:
        padding = ' '*2
        for i in range(MAX_GUESSES):
            print('   ', end='')
            for result in PRINT_CACHE:
                line = result[i] if len(result) > i else ' '*LENGTH
                print(padding, line, end='')
            print()
        print()
        PRINT_CACHE = []
    return


class Result(list):

    def __init__(self):
        self.solution = random.choice(SOLUTIONS)
        self.turns = 0
        lines = []
        allowed = SOLUTIONS
        constraints = Constraints()
        for i in range(1, MAX_GUESSES+1):
            # More efficient to shuffle the list then take the first match?
            allowed = [x for x in allowed if constraints.check(x)]
            guess = random.choice(allowed)
            if OPENING_GUESS and not lines:
                guess = OPENING_GUESS
            clues = Clues(guess, self.solution)
            lines.append(clues)
            constraints.update(clues)
            if guess == self.solution:
                self.turns = i
                break
        return list.__init__(self, lines)


class Constraints(list):

    def __init__(self):
        elts = [Constraint(c) for c in ALPHABET]
        return list.__init__(self, elts)

    def update(self, clues):
        [c.update(clues) for c in self]

    def check(self, guess):
        return all(c.check(guess) for c in self)


class Constraint(object):

    def __init__(self, letter):
        assert letter in ALPHABET
        self.letter = letter
        self.hits = set()
        self.misses = set()
        self.min_count = 0
        self.max_count = LENGTH

    def check(self, guess):
        for i in self.hits:
            if guess[i] != self.letter:
                return False
        for i in self.misses:
            if guess[i] == self.letter:
                return False
        return self.min_count <= guess.count(self.letter) <= self.max_count

    def update(self, clues):
        # Only care about clues for this letter
        clues = [c for c in clues if c.letter == self.letter]
        # Suppose we guess GEESE and the solution is EVENT. The middle E would
        # be green, since it's in the right place. One of the other Es would be
        # yellow since there is one more to match. And the third E would be
        # black, indicating that there are no more.
        green_clues = [c for c in clues if c.color == GREEN]
        yellow_clues = [c for c in clues if c.color == YELLOW]
        black_clues = [c for c in clues if c.color == BLACK]
        self.hits.update(c.index for c in green_clues)
        self.misses.update(c.index for c in yellow_clues)
        self.misses.update(c.index for c in black_clues)
        self.min_count = len(green_clues) + len(yellow_clues)
        if black_clues:
            self.max_count = self.min_count
        return


class Clues(list):

    def __init__(self, guess, solution):
        elts = [Clue(guess, solution, i) for i in range(LENGTH)]
        return list.__init__(self, elts)

    def __str__(self):
        return "".join(str(x) for x in self)


class Clue(object):

    def __init__(self, guess, solution, i):
        self.letter = guess[i]
        self.index = i
        if solution[i] == self.letter:
            self.color = GREEN
            return
        # If we guess GEESE and the solution is THERE, the first E will be black
        i_guess = {i for i in range(LENGTH) if guess[i] == self.letter}
        i_solution = {i for i in range(LENGTH) if solution[i] == self.letter}
        i_guess_unmatched = i_guess - i_solution
        i_solution_unmatched = i_solution - i_guess
        n_yellow = len(i_solution_unmatched)
        i_yellow = sorted(i_guess_unmatched)[:n_yellow]
        self.color = YELLOW if i in i_yellow else BLACK

    def __str__(self):
        return self.color + self.letter + RESET


if __name__ == '__main__':
    main()
