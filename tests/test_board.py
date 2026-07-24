"""<summary>
Unit tests for board parsing, formatting, neighbor generation, and solvability.
</summary>

<remarks>
These tests verify the foundational puzzle operations used by both BFS and A*.
They use Python's built-in <c>unittest</c> framework.
</remarks>
"""

from __future__ import annotations

import unittest

from sliding_puzzle.board import Puzzle, format_state, is_solvable, parse_state


class BoardTests(unittest.TestCase):
    """<summary>
    Test suite for <c>sliding_puzzle.board</c>.
    </summary>

    <remarks>
    Each test method checks one behavior that the search algorithms depend on:
    parsing input, generating legal moves, checking solvability, or formatting
    states for output.
    </remarks>
    """

    def test_parse_state_accepts_blank_aliases(self) -> None:
        """<summary>
        Verify that the parser accepts supported blank aliases.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        The assignment uses a blank field. The program accepts several textual
        forms for that blank so custom command-line input is easier to type.
        </remarks>
        """

        self.assertEqual(parse_state("1 2 _ 3 4 5 6 7 8", 3), (1, 2, 0, 3, 4, 5, 6, 7, 8))
        self.assertEqual(parse_state("1,2,x,3,4,5,6,7,8", 3), (1, 2, 0, 3, 4, 5, 6, 7, 8))

    def test_neighbors_from_corner_blank(self) -> None:
        """<summary>
        Verify legal neighbor generation when the blank is in a corner.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        A bottom-right blank can only move up or left. This checks that invalid
        moves leaving the board are skipped.
        </remarks>
        """

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
        """<summary>
        Verify that the assignment start and target states are mutually reachable.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        If this test failed, the default puzzle would be impossible and the
        solver would correctly stop before searching.
        </remarks>
        """

        self.assertTrue(
            is_solvable(
                (8, 7, 6, 5, 4, 3, 2, 1, 0),
                (0, 1, 2, 3, 4, 5, 6, 7, 8),
                3,
            )
        )

    def test_format_state_uses_blank_marker(self) -> None:
        """<summary>
        Verify that formatted output displays tile 0 as the blank marker.
        </summary>

        <returns>
        None.
        </returns>

        <remarks>
        The command-line output should be readable for humans, so the blank
        tile is printed as <c>_</c> instead of <c>0</c>.
        </remarks>
        """

        self.assertEqual(format_state((1, 2, 0, 3, 4, 5, 6, 7, 8), 3), "1 2 _\n3 4 5\n6 7 8")


# <summary>
# Allow this test file to be run directly with python tests/test_board.py.
# </summary>
if __name__ == "__main__":
    unittest.main()
