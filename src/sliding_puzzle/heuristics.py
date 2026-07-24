from __future__ import annotations

from sliding_puzzle.board import Puzzle, State


def manhattan_distance(puzzle: Puzzle, state: State) -> int:
    """Admissible heuristic: sum of tile distances from their target positions."""

    total = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue

        current_row, current_col = divmod(index, puzzle.size)
        target_row, target_col = puzzle.target_positions[tile]
        total += abs(current_row - target_row) + abs(current_col - target_col)

    return total


def misplaced_tiles(puzzle: Puzzle, state: State) -> int:
    """Admissible heuristic: count non-blank tiles not yet in target position."""

    return sum(
        1
        for current_tile, target_tile in zip(state, puzzle.target)
        if current_tile != 0 and current_tile != target_tile
    )


def zero_heuristic(puzzle: Puzzle, state: State) -> int:
    """Trivial admissible heuristic, useful for testing A* behavior."""

    return 0

