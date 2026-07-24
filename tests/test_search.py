"""<summary>
Unit tests for heuristics and search algorithms.
</summary>

<remarks>
These tests verify that BFS and A* solve the assignment puzzle, agree on the
optimal move count, and handle unsolvable input without unnecessary search.
</remarks>
"""

from __future__ import annotations

import unittest

from sliding_puzzle.board import Puzzle
from sliding_puzzle.heuristics import manhattan_distance, misplaced_tiles
from sliding_puzzle.search import astar_search, breadth_first_search


# <summary>
# Shared Puzzle object using the exact assignment start and target states.
# </summary>
ASSIGNMENT_PUZZLE = Puzzle(
    start=(8, 7, 6, 5, 4, 3, 2, 1, 0),
    target=(0, 1, 2, 3, 4, 5, 6, 7, 8),
    size=3,
)


class SearchTests(unittest.TestCase):
    """<summary>
    Test suite for search algorithms and heuristic behavior.
    </summary>

    <remarks>
    The tests compare BFS and A* on the assignment puzzle and confirm that the
    heuristics behave correctly at the target state.
    </remarks>
    """

    def test_manhattan_is_zero_for_target(self) -> None:
        """<summary>
        Verify that Manhattan distance is zero at the target state.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        A heuristic must estimate no remaining cost when the puzzle is already
        solved.
        </remarks>
        """

        self.assertEqual(manhattan_distance(ASSIGNMENT_PUZZLE, ASSIGNMENT_PUZZLE.target), 0)

    def test_misplaced_tiles_is_zero_for_target(self) -> None:
        """<summary>
        Verify that misplaced-tiles distance is zero at the target state.
        </summary>

        <returns>
        None.
        </returns>
        """

        self.assertEqual(misplaced_tiles(ASSIGNMENT_PUZZLE, ASSIGNMENT_PUZZLE.target), 0)

    def test_bfs_solves_assignment_puzzle(self) -> None:
        """<summary>
        Verify that BFS finds a valid solution for the assignment puzzle.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        The path should start at the assignment start state, end at the target
        state, and contain exactly one more state than the number of moves.
        </remarks>
        """

        result = breadth_first_search(ASSIGNMENT_PUZZLE)

        self.assertTrue(result.found)
        self.assertEqual(result.path[0], ASSIGNMENT_PUZZLE.start)
        self.assertEqual(result.path[-1], ASSIGNMENT_PUZZLE.target)
        self.assertEqual(len(result.path), result.move_count + 1)

    def test_astar_matches_bfs_solution_length(self) -> None:
        """<summary>
        Verify that A* returns an optimal solution and expands fewer nodes.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        BFS gives a reliable optimal move count for unit-cost moves. A* should
        match that move count while expanding fewer nodes because Manhattan
        distance guides the search.
        </remarks>
        """

        bfs = breadth_first_search(ASSIGNMENT_PUZZLE)
        astar = astar_search(ASSIGNMENT_PUZZLE)

        self.assertTrue(astar.found)
        self.assertEqual(astar.move_count, bfs.move_count)
        self.assertLess(astar.expansions, bfs.expansions)

    def test_unsolvable_puzzle_returns_not_found_without_searching(self) -> None:
        """<summary>
        Verify that an unsolvable puzzle returns immediately.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        The search function performs a solvability check before expanding
        states. For this unsolvable example, expansion count should stay zero.
        </remarks>
        """

        puzzle = Puzzle(
            start=(1, 2, 3, 4, 5, 6, 8, 7, 0),
            target=(1, 2, 3, 4, 5, 6, 7, 8, 0),
            size=3,
        )

        result = breadth_first_search(puzzle)

        self.assertFalse(result.found)
        self.assertEqual(result.expansions, 0)


# <summary>
# Allow this test file to be run directly with python tests/test_search.py.
# </summary>
if __name__ == "__main__":
    unittest.main()
