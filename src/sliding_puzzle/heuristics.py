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


def misplaced_tiles(puzzle: Puzzle, state: State) -> int:
    """<summary>
    Count how many numbered tiles are not in their target positions.
    </summary>

    <param name="puzzle">
    The puzzle definition containing the target state.
    </param>
    <param name="state">
    The state whose misplaced tiles should be counted.
    </param>

    <returns>
    The number of non-blank tiles whose current position differs from the
    target state.
    </returns>

    <remarks>
    This heuristic is admissible because every misplaced tile must be moved at
    least once before the puzzle can be solved.
    </remarks>
    """

    return sum(
        1
        for current_tile, target_tile in zip(state, puzzle.target)
        if current_tile != 0 and current_tile != target_tile
    )


def zero_heuristic(puzzle: Puzzle, state: State) -> int:
    """<summary>
    Return a zero estimate for every state.
    </summary>

    <param name="puzzle">
    The puzzle definition. It is accepted to match the common heuristic
    signature but is not used.
    </param>
    <param name="state">
    The state to estimate. It is accepted to match the common heuristic
    signature but is not used.
    </param>

    <returns>
    Always <c>0</c>.
    </returns>

    <remarks>
    This heuristic is admissible because it never overestimates. With unit move
    costs, A* with this heuristic behaves like uniform-cost search.
    </remarks>
    """

    return 0
