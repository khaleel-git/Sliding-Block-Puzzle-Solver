from __future__ import annotations

import unittest

from sliding_puzzle.board import Puzzle
from sliding_puzzle.heuristics import manhattan_distance, misplaced_tiles
from sliding_puzzle.search import astar_search, breadth_first_search


ASSIGNMENT_PUZZLE = Puzzle(
    start=(8, 7, 6, 5, 4, 3, 2, 1, 0),
    target=(0, 1, 2, 3, 4, 5, 6, 7, 8),
    size=3,
)


class SearchTests(unittest.TestCase):
    def test_manhattan_is_zero_for_target(self) -> None:
        self.assertEqual(manhattan_distance(ASSIGNMENT_PUZZLE, ASSIGNMENT_PUZZLE.target), 0)

    def test_misplaced_tiles_is_zero_for_target(self) -> None:
        self.assertEqual(misplaced_tiles(ASSIGNMENT_PUZZLE, ASSIGNMENT_PUZZLE.target), 0)

    def test_bfs_solves_assignment_puzzle(self) -> None:
        result = breadth_first_search(ASSIGNMENT_PUZZLE)

        self.assertTrue(result.found)
        self.assertEqual(result.path[0], ASSIGNMENT_PUZZLE.start)
        self.assertEqual(result.path[-1], ASSIGNMENT_PUZZLE.target)
        self.assertEqual(len(result.path), result.move_count + 1)

    def test_astar_matches_bfs_solution_length(self) -> None:
        bfs = breadth_first_search(ASSIGNMENT_PUZZLE)
        astar = astar_search(ASSIGNMENT_PUZZLE)

        self.assertTrue(astar.found)
        self.assertEqual(astar.move_count, bfs.move_count)
        self.assertLess(astar.expansions, bfs.expansions)

    def test_unsolvable_puzzle_returns_not_found_without_searching(self) -> None:
        puzzle = Puzzle(
            start=(1, 2, 3, 4, 5, 6, 8, 7, 0),
            target=(1, 2, 3, 4, 5, 6, 7, 8, 0),
            size=3,
        )

        result = breadth_first_search(puzzle)

        self.assertFalse(result.found)
        self.assertEqual(result.expansions, 0)


if __name__ == "__main__":
    unittest.main()
