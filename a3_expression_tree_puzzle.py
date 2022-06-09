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

This module contains the ExpressionTreePuzzle class.
"""

from __future__ import annotations

from typing import List, Dict

from a3_expression_tree import ExprTree
from puzzle import Puzzle


class ExpressionTreePuzzle(Puzzle):
    """"
    An expression tree puzzle.

    === Public Attributes ===
    variables: the dictionary of variable name (str) - value (int) pairs
               A variable is considered "unassigned" unless it has a
               non-zero value.
    target: the target value for the expression tree to evaluate to

    === Private Attributes ===
    _tree: the expression tree

    === Representation Invariants ===
    - variables contains a key for each variable appearing in _tree

    - all values stored in variables are single digit integers (0-9).
    """
    _tree: ExprTree
    variables: Dict[str, int]
    target: int

    def __init__(self, tree: ExprTree, target: int) -> None:
        """
        Create a new expression tree puzzle given the provided
        expression tree and the target value. The variables are initialized
        using the tree's populate_lookup method.

        >>> puz = ExpressionTreePuzzle(ExprTree('a', []), 4)
        >>> puz.variables == {'a': 0}
        True
        >>> puz.target
        4
        """
        self.variables = {}
        tree.populate_lookup(self.variables)
        self._tree = tree
        self.target = target

    def is_solved(self) -> bool:
        """
        Return True iff ExpressionTreePuzzle self is solved.

        The puzzle is solved if all variables have been assigned a non-zero
        value and the expression tree evaluates to the target value.

        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 7
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 5
        >>> puz.variables['b'] = 2
        >>> puz.is_solved()
        True
        """
        for values in self.variables.values():
            if values == 0:
                return False
        if self._tree.eval(self.variables) == self.target:
            return True
        return False

    def __str__(self) -> str:
        """
        Return a string representation of this ExpressionTreePuzzle.

        The first line should show the dictionary of variables and the
        second line should show the string representation of the algebraic
        equation represented by the puzzle.

        >>> exprt = ExprTree('+', [ExprTree('*', \
                                            [ExprTree('a', []), \
                                             ExprTree('+', [ExprTree('b', []), \
                                                            ExprTree(6, []), \
                                                            ExprTree(6, []), \
                                                           ])]), \
                                   ExprTree(5, [])])
        >>> puz = ExpressionTreePuzzle(exprt, 61)
        >>> print(puz)
        {'a': 0, 'b': 0}
        ((a * (b + 6 + 6)) + 5) = 61
        """
        return f'{self.variables}\n{str(self._tree)} = {self.target}'

    def extensions(self) -> List[ExpressionTreePuzzle]:
        """
        Return the list of legal extensions of this ExpressionTreePuzzle.

        A legal extension is a new ExpressionTreePuzzle equal to this
        ExpressionTreePuzzle, except that it assigns a single currently
        unassigned variable a value in the range 1-9.

        A variable is "unassigned" if it has a value of 0.

        A copy of the expression tree and variables dictionary should be
        used in each extension made to avoid unintended aliasing.

        >>> exp_t = ExprTree('a', [])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz)
        9
        >>> exts_of_an_ext = exts_of_puz[0].extensions()
        >>> len(exts_of_an_ext)
        0
        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 8)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz)
        18
        """
        result = []
        zero_key = []
        for keys, values in self.variables.items():
            if values == 0:
                zero_key.append(keys)
        if len(zero_key) == 0:
            return result
        tree_copy = self._tree.copy()
        variable_copy = self.variables.copy()
        for items in zero_key:
            for i in range(1, 10):
                new_tree_puzzle = ExpressionTreePuzzle(tree_copy, self.target)
                new_tree_puzzle.variables = variable_copy
                another_copy = new_tree_puzzle.variables.copy()
                another_copy[items] = i
                new_tree_puzzle.variables = another_copy
                result.append(new_tree_puzzle)
        return result

    # The specifics of how you implement this are up to you.
    # Hint 1: remember that a puzzle can only be extended by assigning a value
    #         to an unassigned variable.
    # Hint 2: remember that our expression tree only supports addition,
    #         multiplication, and non-negative integers.
    def fail_fast(self) -> bool:
        """
        Return True if this ExpressionTreePuzzle can be quickly determined to
        have no solution, False otherwise.

        """
        count = 0
        if self._tree.is_empty():
            return True
        for values in self.variables.values():
            if values == 0:
                count += 1
        if count == 0 and self._tree.eval(self.variables) != self.target:
            return True
        if self._tree.eval(self.variables) > self.target:
            return True
        if self.target <= 0:
            return True
        another_variables = self.variables.copy()
        for values in another_variables:
            if another_variables[values] == 0:
                another_variables[values] = 1
        if self._tree.eval(another_variables) > self.target:
            return True
        return False


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        # # uncomment to disable openning pyta output in browser
        # 'pyta-reporter': 'ColorReporter',
        'allowed-io': [],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', '__future__',
            'a3_expression_tree', 'puzzle', 'solver'
        ],
        'disable': ['E1136'],
        'max-attributes': 15
    })
