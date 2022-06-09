"""
CSC148, Summer 2021
Assignment 3: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

This module is adapted from the CSC148 Winter 2021 A2 with permission from
the author.

=== Module Description ===

This module contains the word ladder puzzle class.
"""

from __future__ import annotations
from typing import Optional, Set, List
from puzzle import Puzzle
from a3_solver import BfsSolver

# difficulty constants
IMPOSSIBLE = 'impossible'
TRIVIAL = 'trivial'
EASY, MEDIUM, HARD = 'easy', 'medium', 'hard'

# constant for the set of letters used
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# helper function to load a default set of words
def load_words() -> Set[str]:
    """
    Return the set of words stored in the file called words.txt.
    """
    with open("words", "r") as words:
        return set(words.read().split())


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle.

    === Public Attributes ===
    from_word: the initial word the puzzle begins with
    to_word: the goal word the puzzle wants to change to
    word_set: the set of all words that are possible valid words to change into

    === Private Attributes ===
    _chars: a string of all possible characters that a word may consist of

    === Representation Invariants ===
    - len(from_word) == len(to_word)
    - from_word in word_set
    - to_word in word_set
    - all words in word_set are lowercase
    """
    from_word: str
    to_word: str
    word_set: Set[str]
    _chars: str

    def __init__(self, from_word: str, to_word: str,
                 word_set: Optional[Set[str]] = None) -> None:
        """
        Create a new word-ladder puzzle with the aim of stepping
        from <from_word> to <to_word> using words in <word_set>, changing one
        character at each step.

        If <word_set> is None, the words are loaded using load_words.

        Precondition:
        - len(from_word) == len(to_word)
        - from_word and to_word are both in word_set
        - all words in word_set are lowercase
        """
        Puzzle.__init__(self)
        if word_set is None:
            word_set = load_words()

        (self.from_word, self.to_word, self.word_set) = (from_word,
                                                         to_word, word_set)
        # set of characters to use for 1-character changes
        self._chars = LETTERS

    def __eq__(self, other: WordLadderPuzzle) -> bool:
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        Two WordLadderPuzzles are equal if they have equal
        from_word, to_word, and word_set attributes.

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
        >>> wl3 = WordLadderPuzzle("me", "my", {"ma", "me", "my"})
        >>> wl1 == wl2
        False
        >>> wl1 == wl3
        True
        """
        if self.from_word == other.from_word \
                and self.to_word == other.to_word \
                and self.word_set == other.word_set:
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        Return a human-friendly string representing this WordLadderPuzzle's
        state, with the format:

        from_word -> to_word

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
        >>> print(wl1)
        me -> my
        >>> print(wl2)
        me -> my
        """
        return self.from_word + ' -> ' + self.to_word

    # Note: A WordLadderPuzzle is solved when from_word is the same as its
    # to_word
    def is_solved(self) -> bool:
        """
        Return whether this WordLadderPuzzle is solved.

        >>> wl1 = WordLadderPuzzle("me", "me", {"me", "my"})
        >>> wl2 = WordLadderPuzzle("me", "my", {"me", "my"})
        >>> wl1.is_solved()
        True
        >>> wl2.is_solved()
        False
        """
        if self.from_word == self.to_word:
            return True
        else:
            return False

    # legal extensions are valid WordLadderPuzzles that have a from_word that
    # differs from this WordLadderPuzzle's from_word by exactly one character
    def extensions(self) -> List[WordLadderPuzzle]:
        """
        Return a list of WordLadderPuzzles that are one step
        away from this WordLadderPuzzle.

        >>> wl1 = WordLadderPuzzle("me", "my", {"me", "be", "my"})
        >>> wl2 = WordLadderPuzzle("be", "my", {"me", "be", "my"})
        >>> wl3 = WordLadderPuzzle("my", "my", {"me", "be", "my"})

        # ensure wl1.extensions() contains both wl2 and wl3
        >>> wl1_extensions = wl1.extensions()
        >>> wl2 in wl1_extensions and wl3 in wl1_extensions
        True

        # ensure wl1.extensions() contains no other WordLadderPuzzles
        >>> len(wl1_extensions)
        2
        """
        result = []
        # for every options in word_set
        for items in self.word_set:
            differ = 0
            index = 0
            # iterate every character
            # select the ones that have the same length as the original word
            # if difference goes over 1, stop the iteration
            while index < len(self.from_word) \
                    and len(items) == len(self.from_word) and differ < 2:
                # if the characters are different, and the character is a valid
                # character increase the counter differ
                if self.from_word[index] != items[index] \
                        and items[index] in self._chars:
                    differ += 1
                # if the characters are different, but the character is invalid
                # terminate the loop
                elif self.from_word[index] != items[index] \
                        and items[index] not in self._chars:
                    differ += 2
                index += 1
            # if the character difference count is exactly 1
            if differ == 1:
                # create a new puzzle with that word
                temp = WordLadderPuzzle(items, self.to_word, self.word_set)
                # append it as an option
                result.append(temp)
        return result

    # Note: implementing this requires you to have completed Task 2
    # Hint: Think about which of BfsSolver and DfsSolver is the right
    #       solver for the task at hand. (You may add any required
    #       imports at the top of the file.)
    def get_difficulty(self) -> str:
        """
        Return the "difficulty" of this puzzle.

        The difficulty is defined as follows:

        TRIVIAL - a solution can be reached in zero moves or just one move

        EASY - the shortest path to a solution is exactly 2 moves.
            e.g. The puzzle 'cost' -> 'moss' is solved in 2 moves:
                    'cost' -> 'most' and then 'most' -> 'moss'
                (So the result of calling a solver's solve method is a
                list of length 3)

        MEDIUM - the shortest path to a solution is less than 5 moves.

        HARD - a solution exists and it takes at least 5 moves to reach.

        IMPOSSIBLE - a solution does not exist

        Note: Use the defined constants, instead of hard-coding the values
        of the strings.
        """
        # create a solver
        solver = BfsSolver()
        # create a path to the solution
        solved = solver.solve(self)
        # if the path length == 1 (puzzle already solved) or 2
        # return Trivial
        if len(solved) == 1 or len(solved) == 2:
            return TRIVIAL
        # if the path length == 3, return easy and so on
        elif len(solved) == 3:
            return EASY
        elif 3 < len(solved) < 6:
            return MEDIUM
        elif 6 <= len(solved):
            return HARD
        # if none, return impossible
        else:
            return IMPOSSIBLE


if __name__ == '__main__':
    # any code you want to write to test WordLadderPuzzle.
    import python_ta

    python_ta.check_all(config={
        # # uncomment to disable openning pyta output in browser
        # 'pyta-reporter': 'ColorReporter',
        'allowed-io': ['load_words'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', '__future__',
            'puzzle', 'a3_solver'
        ],
        'disable': ['E1136'],
        'max-attributes': 15
    })
