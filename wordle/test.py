import pytest

from solver import Clues, BLACK, YELLOW, GREEN


def test_three_guess_two_match():
    solution = 'event'
    guess = 'geese'
    clues = Clues(guess, solution)
    assert clues[0].color == BLACK
    assert clues[1].color == YELLOW
    assert clues[2].color == GREEN
    assert clues[3].color == BLACK
    assert clues[4].color == BLACK


def test_three_guess_last_two_match():
    solution = 'there'
    guess = 'geese'
    clues = Clues(guess, solution)
    assert clues[0].color == BLACK
    assert clues[1].color == BLACK
    assert clues[2].color == GREEN
    assert clues[3].color == BLACK
    assert clues[4].color == GREEN
