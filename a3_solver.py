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

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.

        Note: A user of this method may pass a set of puzzle states that
        shouldn't appear in the path to the solution. You should also update
        seen to include states, that you have encountered, which are not the
        solved state of the puzzle.
        """
        # if the puzzle is already solved, return the puzzle itself
        if puzzle.is_solved():
            return [puzzle]
        # otherwise run the helper function
        lst = self._dfs_solve_helper(puzzle, seen)
        # if only the puzzle itself is returned, return empty list
        if len(lst) == 1:
            return []
        # otherwise return the result
        else:
            return lst

    def _dfs_solve_helper(self, puzzle: Puzzle,
                          seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        If the all the solution paths are blocked by seen, return a list with
        only element of <puzzle>. Otherwise, if the puzzle has no solution
        return empty list

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.

        Note: A user of this method may pass a set of puzzle states that
        shouldn't appear in the path to the solution. You should also update
        seen to include states, that you have encountered, which are not the
        solved state of the puzzle.
        """
        # if seen is none, create a set
        if seen is None:
            seen = set()
        # check if puzzle is in seen
        if str(puzzle) in seen:
            # print(f'{str(puzzle)} has been seen already')
            return []
        # check if the puzzle fast fails
        elif puzzle.fail_fast():
            # if fast failed, add it to seen
            seen |= {str(puzzle)}
            # print(f'{str(puzzle)} has fast failed and added to seen')
            return []
        else:
            # get the list of extensions
            extensions = puzzle.extensions()
            # add the puzzle to seen
            seen |= {str(puzzle)}
            # print(f'{str(puzzle)} has been added to seen set')
            result = [puzzle]
            for options in extensions:
                # recurse the extension options
                next_moves = self._dfs_solve_helper(options, seen)
                # include the extension option to seen
                seen |= {str(options)}
                # print(f'{str(options)} has been added to seen set')
                # if we get a result that is solved add it to the list
                if len(next_moves) != 0 and next_moves[-1].is_solved():
                    return result + next_moves
            return result


def _create_extension_path(puzzle_lst: List[Puzzle],
                           seen: Optional[Set[str]] = None
                           ) -> List[List[Puzzle]]:
    """ Helper function that outputs a list of all the possible extension path
    that are not seen previously and could pass fail fast test as a list

    <seen> is either None (default) or a set of puzzle states' string
    representations, whose puzzle states can't be any part of the path to
    the solution.

    Precondition: <puzzle_lst> is not empty
    """
    result = []
    # get extensions for the most recent puzzle move
    extension = puzzle_lst[-1].extensions()
    # if there is no extension, return empty
    if len(extension) == 0:
        return result
    for items in extension:
        # for extension options, if seen is not None, check if it has already
        # been seen. Also, check if the option fast fails
        if seen is not None:
            if str(items) not in seen and not items.fail_fast():
                # not seen and not fast failed, append it to the result since
                # it's a valid option
                result.append(puzzle_lst + [items])
            elif str(items) not in seen and items.fail_fast():
                seen |= {str(items)}
                # print(f'{str(items)} was either seen already or fast failed')
        elif not items.fail_fast():
            # if seen is none, just check if the option fast fails
            # if not, append to the result
            result.append(puzzle_lst + [items])
        # else:
            # print(f'{str(items)} was fast failed')
    # return the results
    return result


class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.

        Note: A user of this method may pass a set of puzzle states that
        shouldn't appear in the path to the solution. You should also update
        seen to include states, that you have encountered, which are not the
        solved state of the puzzle.
        """
        # if seen is not None, and puzzle is already seen, return empty
        if seen is not None and str(puzzle) in seen:
            return []
        # if the puzzle fast fails, return empty
        elif puzzle.fail_fast():
            return []
        # if the puzzle is already solved, return list of the puzzle itself
        elif puzzle.is_solved():
            return [puzzle]
        else:
            # create a queue
            que = Queue()
            # if seen is none, create a set
            if seen is None:
                seen = set()
            # include the puzzle's original state as seen
            seen |= {str(puzzle)}
            # print(f'{str(puzzle)} has been added to seen set')
            # get all the available extension paths for puzzle
            extensions = _create_extension_path([puzzle], seen)
            for path in extensions:
                # add the valid path to the queue
                que.enqueue(path)
                # add the last state of each path that are being visited as seen
                seen |= {str(path[-1])}
                # print(f'{str(path[-1])} has been added to queue')
            while not que.is_empty():
                # while there are options available, we visit all of them
                # visit the first path in the queue
                dequeued = que.dequeue()
                # print(f'{str(dequeued[-1])} is being tested'
                #      f' to see if its the right solution')
                # if the path is the solution return the path
                if dequeued[-1].is_solved():
                    return dequeued
                # otherwise, create more path that are connected to the previous
                # path
                more_extensions = _create_extension_path(dequeued, seen)
                for lst in more_extensions:
                    # add the newly created paths to the queue
                    que.enqueue(lst)
                    # print(f'{str(lst[-1])} has been added to queue')
                    # mark them as seen
                    seen |= {str(lst[-1])}
            return []


if __name__ == "__main__":
    # you may add any code you want to use for testing here
    import python_ta

    python_ta.check_all(config={
        # # uncomment to disable openning pyta output in browser
        # 'pyta-reporter': 'ColorReporter',
        'allowed-io': [],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', '__future__', 'puzzle', 'adts'
        ],
        'disable': ['E1136'],
        'max-attributes': 15
    })
