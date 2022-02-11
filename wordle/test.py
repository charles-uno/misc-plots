import pytest

from solver import Clues, Constraints, BLACK, YELLOW, GREEN, WORDS, SOLUTIONS, LENGTH

def test_all_words_correct_length():
    for word in WORDS:
        assert len(word) == LENGTH

def test_all_solutions_correct_length():
    for solution in SOLUTIONS:
        assert len(solution) == LENGTH

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
