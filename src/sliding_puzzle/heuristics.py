"""<summary>
Heuristic functions used by A* search.
</summary>

<remarks>
Each heuristic accepts the current <c>Puzzle</c> and a candidate <c>State</c>,
then returns an integer estimate of the remaining distance to the target. The
default heuristic for the project is Manhattan distance.
</remarks>
"""

from __future__ import annotations

from sliding_puzzle.board import Puzzle, State


def manhattan_distance(puzzle: Puzzle, state: State) -> int:
    """<summary>
    Compute the Manhattan-distance heuristic for a puzzle state.
    </summary>

    <param name="puzzle">
    The puzzle definition, including board size and cached target positions.
    </param>
    <param name="state">
    The state whose estimated distance to the target should be calculated.
    </param>

    <returns>
    The sum of horizontal and vertical distances from each numbered tile to its
    target position.
    </returns>

    <remarks>
    Tile <c>0</c>, the blank, is ignored. The heuristic is admissible because a
    single legal move can reduce the Manhattan distance of only one tile by at
    most one.
    </remarks>
    """

    total = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue

        current_row, current_col = divmod(index, puzzle.size)
        target_row, target_col = puzzle.target_positions[tile]
        total += abs(current_row - target_row) + abs(current_col - target_col)

    return total
