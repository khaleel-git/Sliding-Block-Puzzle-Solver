from __future__ import annotations

import unittest

from sliding_puzzle.board import Puzzle, format_state, is_solvable, parse_state


class BoardTests(unittest.TestCase):
    def test_parse_state_accepts_blank_aliases(self) -> None:
        self.assertEqual(parse_state("1 2 _ 3 4 5 6 7 8", 3), (1, 2, 0, 3, 4, 5, 6, 7, 8))
        self.assertEqual(parse_state("1,2,x,3,4,5,6,7,8", 3), (1, 2, 0, 3, 4, 5, 6, 7, 8))

    def test_neighbors_from_corner_blank(self) -> None:
        puzzle = Puzzle(
            start=(1, 2, 3, 4, 5, 6, 7, 8, 0),
            target=(1, 2, 3, 4, 5, 6, 7, 8, 0),
            size=3,
        )

        neighbors = set(puzzle.neighbors(puzzle.start))

        self.assertEqual(
            neighbors,
            {
                ((1, 2, 3, 4, 5, 0, 7, 8, 6), "U"),
                ((1, 2, 3, 4, 5, 6, 7, 0, 8), "L"),
            },
        )

    def test_solvability_matches_assignment_configuration(self) -> None:
        self.assertTrue(
            is_solvable(
                (8, 7, 6, 5, 4, 3, 2, 1, 0),
                (0, 1, 2, 3, 4, 5, 6, 7, 8),
                3,
            )
        )

    def test_format_state_uses_blank_marker(self) -> None:
        self.assertEqual(format_state((1, 2, 0, 3, 4, 5, 6, 7, 8), 3), "1 2 _\n3 4 5\n6 7 8")


if __name__ == "__main__":
    unittest.main()
