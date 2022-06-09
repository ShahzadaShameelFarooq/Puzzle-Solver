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

===== Module Description =====

This module contains sample test cases that you can use to test your code.
These are a very incomplete set of test cases! We will be testing your code on
a much more thorough set of tests.

The self-test on MarkUs runs all of the tests below, along with a few others.
Make sure you run the self-test on MarkUs after submitting your code!

Once you have the entire program completed, that is, after Task 5, your
code should pass all of the tests we've provided. As you develop your code,
test cases for parts that you haven't written yet will fail, of course.

But as you work through the earlier phases of the assignment, you can run the
individual tests below for each method as you complete it. We encourage you to
add further test cases in this file to improve your confidence in your code.

Tip: if you put your mouse inside a pytest function and right click, the "run"
menu will give you the option of running just that test function.
"""
from a3_sudoku_puzzle import SudokuPuzzle
from a3_word_ladder_puzzle import WordLadderPuzzle, EASY, TRIVIAL
from a3_expression_tree import ExprTree, construct_from_list
from a3_expression_tree_puzzle import ExpressionTreePuzzle
from a3_solver import BfsSolver, DfsSolver


# Below is an incomplete set of tests: these tests are mostly the provided
# doctest examples.
#
# We encourage you to write additional test cases and test your own code,
# using the provided test cases as a template!


def test_sudoku_fail_fast_doctest() -> None:
    """Test SudokuPuzzle.fail_fast on the provided doctest."""
    s = SudokuPuzzle(4, [["A", "B", "C", "D"],
                         ["C", "D", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [["B", "D", "A", "C"],
                         ["C", "A", "B", "D"],
                         ["A", "B", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})
    assert s.fail_fast() is True


def test_has_unique_solution_doctest() -> None:
    """Test has_unique_solution on a SudokuPuzzle with a non-unique solution."""
    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is False


def test_dfs_solver_example() -> None:
    """Test DfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    solver = DfsSolver()
    actual = solver.solve(s)[-1]

    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})

    assert actual == expected


def test_bfs_solver_example() -> None:
    """Test BfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    solver = BfsSolver()
    actual = solver.solve(s)[-1]

    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})

    assert actual == expected


def test_word_ladder_eq_doctest() -> None:
    """Test WordLadder.__eq__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    wl3 = WordLadderPuzzle("me", "my", {"ma", "me", "my"})
    assert wl1.__eq__(wl2) is False
    assert wl1.__eq__(wl3) is True


def test_word_ladder_str_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    assert str(wl1) == 'me -> my'
    assert str(wl2) == 'me -> my'


def test_word_ladder_extensions_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "be", "my"})
    wl2 = WordLadderPuzzle("be", "my", {"me", "be", "my"})
    wl3 = WordLadderPuzzle("my", "my", {"me", "be", "my"})

    msg1 = f"{wl1.extensions()} is missing some valid puzzle states"
    msg2 = f"{wl1.extensions()} contains extra invalid puzzle states"

    assert all([wlp in wl1.extensions() for wlp in [wl2, wl3]]), msg1
    assert all([wlp in [wl2, wl3] for wlp in wl1.extensions()]), msg2


def test_word_ladder_is_solved_doctest() -> None:
    """Test WordLadder.is_solved on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "me", {"me", "my"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my"})
    assert wl1.is_solved() is True
    assert wl2.is_solved() is False


def test_word_ladder_get_difficulty() -> None:
    """Test WordLadder.get_difficulty on TRIVIAL and EASY puzzles."""
    wl1 = WordLadderPuzzle("done", "done", {"done"})
    assert wl1.get_difficulty() == TRIVIAL

    wl2 = WordLadderPuzzle("come", "done", {"come", "cone", "done"})
    assert wl2.get_difficulty() == EASY


def test_expression_tree_eval_doctest() -> None:
    """Test ExprTree.eval on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 3

    look_up['x'] = 7
    look_up['y'] = 3
    assert exp_t.eval(look_up) == 31


def test_expression_tree_populate_lookup_doctest() -> None:
    """Test ExprTree.populate_lookup on the provided doctest"""
    expr_t = ExprTree('a', [])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert look_up['a'] == 0
    assert len(look_up) == 1


def test_expression_tree_construct_from_list_doctest() -> None:
    """Test ExprTree.construct_from_list on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    example = [[5]]
    exp_t = construct_from_list(example)
    assert str(exp_t) == '5'

    example = [['+'], [3, 'a']]
    exp_t = construct_from_list(example)
    assert str(exp_t) == '(3 + a)'


def test_expression_tree_substitute_doctest() -> None:
    """Test ExprTree.substitute on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    exp_t = ExprTree('a', [])
    exp_t.substitute({'a': 1})
    assert str(exp_t) == '1'

    exp_t = ExprTree('*', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('a', []),
                                          ExprTree(1, [])])])
    exp_t.substitute({'a': 2, '*': '+'})
    assert str(exp_t) == '(2 + (2 + 1))'


def test_expression_tree_str_doctest() -> None:
    """Test ExprTree.__str__ on the provided doctest"""

    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('b', []),
                           ExprTree(3, [])])
    assert str(exp_t) == '(a + b + 3)'

    exp_t = ExprTree(None, [])
    assert str(exp_t) == '()'

    exp_t = ExprTree(5, [])
    assert str(exp_t) == '5'

    exp_t = ExprTree('+', [ExprTree('*', [ExprTree(7, []),
                                          ExprTree('+',
                                                   [ExprTree(6, []),
                                                    ExprTree(6, [])])]),
                           ExprTree(5, [])])
    assert str(exp_t) == '((7 * (6 + 6)) + 5)'

    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    assert str(exp_t) == '(3 + (x * y) + x)'


def test_expression_tree_eq_doctest() -> None:
    """Test ExprTree.__eq__ on the provided doctest"""
    t1 = ExprTree(5, [])
    assert t1.__eq__(ExprTree(5, []))

    t2 = ExprTree('*', [ExprTree(5, []), ExprTree(2, [])])
    assert t2.__eq__(ExprTree('*', [ExprTree(5, []), ExprTree(2, [])]))
    assert t2.__eq__(ExprTree('*', [])) is False


def test_expression_tree_puzzle_is_solved_doctest() -> None:
    """Test ExpressionTreePuzzle.is_solved on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    assert puz.is_solved() is False
    puz.variables['a'] = 7
    assert puz.is_solved() is False
    puz.variables['a'] = 5
    puz.variables['b'] = 2
    assert puz.is_solved() is True


def test_expression_tree_puzzle_str_doctest() -> None:
    """Test ExpressionTreePuzzle.__str__ on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('*',
                                    [ExprTree('a', []),
                                     ExprTree('+', [ExprTree('b', []),
                                                    ExprTree(6, []),
                                                    ExprTree(6, []),
                                                    ])]),
                           ExprTree(5, [])])
    puz = ExpressionTreePuzzle(exp_t, 61)
    assert str(puz) == "{'a': 0, 'b': 0}\n((a * (b + 6 + 6)) + 5) = 61"


def test_expression_tree_puzzle_extensions_doctest() -> None:
    """Test ExpressionTreePuzzle.extensions on the provided doctest"""
    exp_t = ExprTree('a', [])
    puz = ExpressionTreePuzzle(exp_t, 7)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 9

    exts_of_an_ext = exts_of_puz[0].extensions()
    assert len(exts_of_an_ext) == 0

    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 8)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 18


def test_expression_tree_puzzle_fail_fast_true() -> None:
    """Test ExpressionTreePuzzle.fail_fast on an unsolvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True


def test_expression_tree_puzzle_fail_fast_false() -> None:
    """Test ExpressionTreePuzzle.fail_fast on a solvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 2

    assert puz.fail_fast() is False


def test_unique_solution_not() -> None:
    """Test has_unique_solution on a puzzle with a unique solution."""
    unique_sol_puzzle = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                         ["B", "A", "D", "C"],
                                         ["D", "C", "A", "B"],
                                         ["A", "B", "C", " "]],
                                     {"A", "B", "C", "D"})
    assert unique_sol_puzzle.has_unique_solution() is True


def test_solvers() -> None:
    """Test whether solvers get correct end puzzle state."""
    a1 = SudokuPuzzle(4, [["3", " ", "4", "2"],
                          [" ", " ", " ", " "],
                          [" ", " ", " ", " "],
                          ["2", " ", " ", "3"]],
                      {"1", "2", "3", "4"})

    solver = DfsSolver()
    l_a = solver.solve(a1)

    solver_2 = BfsSolver()
    l2_a = solver_2.solve(a1)

    assert l_a[-1] == SudokuPuzzle(4, [["3", "1", "4", "2"],
                                       ["4", "2", "3", "1"],
                                       ["1", "3", "2", "4"],
                                       ["2", "4", "1", "3"]],
                                   {"1", "2", "3", "4"})

    assert l2_a[-1] == SudokuPuzzle(4, [["3", "1", "4", "2"],
                                        ["4", "2", "3", "1"],
                                        ["1", "3", "2", "4"],
                                        ["2", "4", "1", "3"]],
                                    {"1", "2", "3", "4"})


def test_expression_tree_eval() -> None:
    """Test eval for the expression trees."""
    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('+', [ExprTree(3, []),
                                                         ExprTree(3, [])]),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])

    look_up = {}
    exp_t.populate_lookup(look_up)

    assert exp_t.eval(look_up) == 3

    look_up['x'] = 2
    look_up['y'] = 1

    assert exp_t.eval(look_up) == 11

    exp_t_2 = ExprTree(5, [])

    look_up_2 = {}
    exp_t_2.populate_lookup(look_up_2)

    look_up_2['x'] = 2

    assert exp_t_2.eval(look_up_2) == 5


def test_populate_look_up() -> None:
    """Test ExprTree.populate_lookup"""
    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                         ExprTree('c', [])]),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    look_up = {}
    exp_t.populate_lookup(look_up)

    assert len(look_up) == 5
    assert look_up['a'] == 0
    assert look_up['b'] == 0
    assert look_up['c'] == 0
    assert look_up['x'] == 0
    assert look_up['y'] == 0

    exp_t_2 = ExprTree(5, [])

    look_up_2 = {}
    exp_t_2.populate_lookup(look_up_2)

    assert len(look_up_2) == 0

    exp_t_3 = ExprTree('+', [ExprTree(5, []),
                             ExprTree('*', [ExprTree('+', [ExprTree(5, []),
                                                           ExprTree(1, [])]),
                                            ExprTree(2, [])]),
                             ExprTree(9, [])])

    look_up_3 = {}
    exp_t_3.populate_lookup(look_up_3)

    assert len(look_up_3) == 0

    exp_t_4 = ExprTree(None, [])

    look_up_4 = {}
    exp_t_4.populate_lookup(look_up_4)

    assert len(look_up_4) == 0


def test_eq() -> None:
    """Test ExprTree.__eq__"""
    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                         ExprTree('c', [])]),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    assert exp_t == ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('+', [ExprTree('b', []),
                                                            ExprTree('c', [])]),
                                             ExprTree('y', [])]),
                                   ExprTree('x', [])])

    assert exp_t != ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('+', [ExprTree('b', []),
                                                            ExprTree('d', [])]),
                                             ExprTree('y', [])]),
                                   ExprTree('x', [])])

    assert exp_t != ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('*', [ExprTree('b', []),
                                                            ExprTree('c', [])]),
                                             ExprTree('y', [])]),
                                   ExprTree('x', [])])

    assert exp_t != ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('+', [ExprTree('b', []),
                                                            ExprTree('c', [])]),
                                             ExprTree('a', [])]),
                                   ExprTree('x', [])])

    assert exp_t != ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('+', [ExprTree('b', []),
                                                            ExprTree('c', []),
                                                            ExprTree(5, [])]),
                                             ExprTree('y', [])]),
                                   ExprTree('x', [])])

    assert exp_t != ExprTree('+', [ExprTree('a', []),
                                   ExprTree('*',
                                            [ExprTree('+', [ExprTree('b', [])]),
                                             ExprTree('y', [])]),
                                   ExprTree('x', [])])

    expt_2 = ExprTree(None, [])
    assert expt_2 == ExprTree(None, [])
    assert expt_2 != ExprTree(5, [])
    assert expt_2 != ExprTree('+', [ExprTree('a', []),
                                    ExprTree('*',
                                             [ExprTree('+', [ExprTree('b', []),
                                                             ExprTree('c',
                                                                      [])]),
                                              ExprTree('a', [])]),
                                    ExprTree('x', [])])


def test_substitute() -> None:
    """Test ExprTree.substitute. """
    expt_1 = ExprTree(None, [])
    from_to = {'a': 1}
    expt_1.substitute(from_to)
    assert expt_1 == ExprTree(None, [])

    exp_t_2 = ExprTree('+', [ExprTree('a', []),
                             ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                           ExprTree('c', [])]),
                                            ExprTree('y', [])]),
                             ExprTree('x', [])])
    from_to_2 = {'a': 1}
    exp_t_2.substitute(from_to_2)
    assert exp_t_2 == ExprTree('+', [ExprTree(1, []),
                                     ExprTree('*',
                                              [ExprTree('+', [ExprTree('b', []),
                                                              ExprTree('c',
                                                                       [])]),
                                               ExprTree('y', [])]),
                                     ExprTree('x', [])])

    exp_t_3 = ExprTree('+', [ExprTree('a', []),
                             ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                           ExprTree('c', [])]),
                                            ExprTree('y', [])]),
                             ExprTree('x', [])])
    from_to_3 = {'c': 1, 'b': 3, 'a': 7, 'y': 4, '*': '+', 'x': 'o', 'o': 9}
    exp_t_3.substitute(from_to_3)
    assert exp_t_3 == ExprTree('+', [ExprTree(7, []),
                                     ExprTree('+',
                                              [ExprTree('+', [ExprTree(3, []),
                                                              ExprTree(1,
                                                                       [])]),
                                               ExprTree(4, [])]),
                                     ExprTree('o', [])])
    # Does 'o' need to change to 9?


def test_is_solved() -> None:
    """Test ExpressionTreePuzzle.is_solved"""
    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                         ExprTree('c', [])]),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    expt_puzzle = ExpressionTreePuzzle(exp_t, 7)
    assert expt_puzzle.is_solved() is False

    expt_puzzle.variables['a'] = 1
    expt_puzzle.variables['b'] = 90
    expt_puzzle.variables['c'] = 10
    expt_puzzle.variables['y'] = 2
    expt_puzzle.variables['x'] = 8
    assert expt_puzzle.is_solved() is False

    expt_puzzle.variables['a'] = 1
    expt_puzzle.variables['b'] = 2
    expt_puzzle.variables['c'] = 1
    expt_puzzle.variables['y'] = 2
    expt_puzzle.variables['x'] = 0
    # print(expt_puzzle)
    assert expt_puzzle.is_solved() is False  # 0 to variable x

    expt_puzzle.variables['a'] = 1
    expt_puzzle.variables['b'] = 1
    expt_puzzle.variables['c'] = 1
    expt_puzzle.variables['y'] = 2
    expt_puzzle.variables['x'] = 2
    # print(expt_puzzle)
    assert expt_puzzle.is_solved() is True


def test_extensions() -> None:
    """Test ExpressionTreePuzzle.extensions"""
    exp_t = ExprTree(None, [])
    exp_t_p = ExpressionTreePuzzle(exp_t, 1)
    assert len(exp_t_p.extensions()) == 0

    exp_t_1 = ExprTree(1, [])
    exp_t_p_1 = ExpressionTreePuzzle(exp_t_1, 1)
    assert len(exp_t_p_1.extensions()) == 0

    exp_t_2 = ExprTree('a', [])
    exp_t_p_2 = ExpressionTreePuzzle(exp_t_2, 1)
    l = exp_t_p_2.extensions()
    assert len(l) == 9

    exp_t_3 = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    exp_t_p_3 = ExpressionTreePuzzle(exp_t_3, 1)
    assert len(exp_t_p_3.extensions()) == 18

    exp_t_3 = ExprTree('+', [ExprTree('+', [ExprTree('a', []),
                                            ExprTree('c', [])]),
                             ExprTree('b', [])])
    exp_t_p_3 = ExpressionTreePuzzle(exp_t_3, 1)
    assert len(exp_t_p_3.extensions()) == 27

    exp_t_p_3.variables['a'] = 3
    assert len(exp_t_p_3.extensions()) == 18

    exp_t_p_3.variables['a'] = 0
    assert len(exp_t_p_3.extensions()) == 27

    exp_t_p_3.variables['a'] = 3
    exp_t_p_3.variables['b'] = 2
    exp_t_p_3.variables['c'] = 1
    assert len(exp_t_p_3.extensions()) == 0


def test_fail_fast() -> None:
    """Test ExpressionTreePuzzle.fail_fast"""
    exp_t = ExprTree(None, [])
    exp_t_p = ExpressionTreePuzzle(exp_t, 1)
    assert exp_t_p.fail_fast() is True

    exp_t_2 = ExprTree(5, [])
    exp_t_p_2 = ExpressionTreePuzzle(exp_t_2, 9)
    assert exp_t_p_2.fail_fast() is True

    exp_t_1 = ExprTree('+', [ExprTree('a', []),
                             ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                           ExprTree('c', [])]),
                                            ExprTree('y', [])]),
                             ExprTree('x', [])])
    expt_puzzle_1 = ExpressionTreePuzzle(exp_t_1, 7)
    expt_puzzle_1.variables['a'] = 1
    expt_puzzle_1.variables['b'] = 2
    expt_puzzle_1.variables['c'] = 1
    expt_puzzle_1.variables['y'] = 2
    expt_puzzle_1.variables['x'] = 0

    assert expt_puzzle_1.fail_fast() is True  # Gives False, it should be True
    # since x can only have values# 1-9
    # which would make the puzzle greater than
    # target value.

    exp_t_3 = ExprTree('+', [ExprTree('a', []),
                             ExprTree('*', [ExprTree('+', [ExprTree('b', []),
                                                           ExprTree('c', [])]),
                                            ExprTree('y', [])]),
                             ExprTree('x', [])])
    exp_t_3_puzzle = ExpressionTreePuzzle(exp_t_3, 7)
    assert exp_t_3_puzzle.fail_fast() is False


if __name__ == '__main__':
    import pytest

    pytest.main(['starter_tests_a3.py'])
