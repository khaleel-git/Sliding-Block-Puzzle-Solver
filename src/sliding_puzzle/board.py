"""<summary>
Board-level primitives for the sliding puzzle solver.
</summary>

<remarks>
This module contains the puzzle state representation, input parsing, display
formatting, legal move generation, and solvability checking. It deliberately
does not contain any search algorithm logic; search algorithms live in
<c>sliding_puzzle.search</c>.
</remarks>
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Iterable, Iterator


# <summary>
# A puzzle board encoded in row-major order.
# </summary>
#
# <remarks>
# For a 3x3 board, the tuple has nine integers. Tile 0 is the blank field.
# Example: (8, 7, 6, 5, 4, 3, 2, 1, 0) represents:
# 8 7 6
# 5 4 3
# 2 1 _
# </remarks>
State = tuple[int, ...]


# <summary>
# Mapping from a move label to the row and column movement of the blank tile.
# </summary>
#
# <remarks>
# The labels describe the blank tile direction:
# U = blank moves up, D = blank moves down, L = blank moves left,
# R = blank moves right.
# </remarks>
MOVE_DELTAS: dict[str, tuple[int, int]] = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


@dataclass(frozen=True)
class Puzzle:
    """<summary>
    Immutable description of an N x N sliding block puzzle.
    </summary>

    <param name="start">
    The initial puzzle state.
    </param>
    <param name="target">
    The desired target puzzle state.
    </param>
    <param name="size">
    The board width and height. When omitted, the size is inferred from the
    start state length.
    </param>

    <remarks>
    The dataclass is frozen so the puzzle definition cannot be accidentally
    changed while a search is running. The private target-position lookup is
    prepared during initialization and used by heuristics.
    </remarks>
    """

    start: State
    target: State
    size: int | None = None

    def __post_init__(self) -> None:
        """<summary>
        Validate the puzzle and prepare cached target positions.
        </summary>

        <returns>
        None.
        </returns>

        <exception cref="ValueError">
        Raised when the puzzle size cannot be inferred, the state lengths are
        invalid, the start and target contain different tiles, or either state
        does not contain exactly one blank tile.
        </exception>

        <remarks>
        Because this dataclass is frozen, <c>object.__setattr__</c> is used for
        initialization-only assignments such as inferred size and cached target
        positions.
        </remarks>
        """

        if self.size is None:
            inferred_size = isqrt(len(self.start))
            if inferred_size * inferred_size != len(self.start):
                raise ValueError("Puzzle state length must be a square number.")
            object.__setattr__(self, "size", inferred_size)

        if self.size is None:
            raise ValueError("Puzzle size could not be determined.")

        expected_length = self.size * self.size
        if len(self.start) != expected_length or len(self.target) != expected_length:
            raise ValueError(f"Start and target must contain {expected_length} cells.")

        if set(self.start) != set(self.target):
            raise ValueError("Start and target must contain the same tiles.")

        if self.start.count(0) != 1 or self.target.count(0) != 1:
            raise ValueError("Each state must contain exactly one blank tile, represented by 0.")

        object.__setattr__(
            self,
            "_target_positions",
            {tile: divmod(index, self.size) for index, tile in enumerate(self.target)},
        )

    @property
    def target_positions(self) -> dict[int, tuple[int, int]]:
        """<summary>
        Return the cached target coordinate for every tile.
        </summary>

        <returns>
        A dictionary mapping tile value to <c>(row, column)</c> in the target
        state.
        </returns>

        <remarks>
        Heuristic functions use this lookup to avoid recomputing target
        coordinates every time they score a state.
        </remarks>
        """

        return self._target_positions

    def neighbors(self, state: State) -> Iterator[tuple[State, str]]:
        """<summary>
        Yield all states reachable by one legal blank move.
        </summary>

        <param name="state">
        The current board state whose legal successors should be generated.
        </param>

        <returns>
        An iterator of <c>(next_state, move)</c> pairs, where <c>next_state</c>
        is the board after the move and <c>move</c> is one of <c>U</c>,
        <c>D</c>, <c>L</c>, or <c>R</c>.
        </returns>

        <remarks>
        The move label describes the movement direction of the blank tile. A
        move is skipped if it would place the blank outside the board.
        </remarks>
        """

        blank_index = state.index(0)
        blank_row, blank_col = divmod(blank_index, self.size)

        for move, (row_delta, col_delta) in MOVE_DELTAS.items():
            next_row = blank_row + row_delta
            next_col = blank_col + col_delta

            if not (0 <= next_row < self.size and 0 <= next_col < self.size):
                continue

            swap_index = next_row * self.size + next_col
            next_state = list(state)
            next_state[blank_index], next_state[swap_index] = (
                next_state[swap_index],
                next_state[blank_index],
            )
            yield tuple(next_state), move

    def validate_state(self, state: State) -> None:
        """<summary>
        Validate that a state belongs to this puzzle.
        </summary>

        <param name="state">
        The state to validate.
        </param>

        <returns>
        None.
        </returns>

        <exception cref="ValueError">
        Raised when the state length is wrong, the tile set differs from the
        target tile set, or the state does not contain exactly one blank tile.
        </exception>
        """

        if len(state) != self.size * self.size:
            raise ValueError(f"State must contain {self.size * self.size} cells.")
        if set(state) != set(self.target):
            raise ValueError("State must contain the same tiles as the target.")
        if state.count(0) != 1:
            raise ValueError("State must contain exactly one blank tile, represented by 0.")


def parse_state(raw: str, size: int) -> State:
    """<summary>
    Parse a user-provided state string into a tuple state.
    </summary>

    <param name="raw">
    Text containing the board cells. Values may be separated by spaces, commas,
    or semicolons.
    </param>
    <param name="size">
    The board width and height. The parser expects <c>size * size</c> values.
    </param>

    <returns>
    A <c>State</c> tuple containing integer tile values.
    </returns>

    <exception cref="ValueError">
    Raised when a token cannot be converted to an integer or the number of
    values does not match the requested board size.
    </exception>

    <remarks>
    The blank tile can be written as <c>0</c>, <c>_</c>, <c>blank</c>, or
    <c>x</c>.
    </remarks>
    """

    normalized = raw.replace(",", " ").replace(";", " ")
    values: list[int] = []

    for token in normalized.split():
        lowered = token.lower()
        if lowered in {"_", "blank", "x"}:
            values.append(0)
        else:
            values.append(int(token))

    expected_length = size * size
    if len(values) != expected_length:
        raise ValueError(f"Expected {expected_length} values, received {len(values)}.")

    return tuple(values)


def format_state(state: State, size: int, blank: str = "_") -> str:
    """<summary>
    Format a tuple state as a human-readable grid.
    </summary>

    <param name="state">
    The state to format.
    </param>
    <param name="size">
    The board width and height.
    </param>
    <param name="blank">
    The text marker to print for tile <c>0</c>.
    </param>

    <returns>
    A multi-line string where each row of the puzzle appears on its own line.
    </returns>

    <remarks>
    Cell width is computed from the largest tile label so wider tile numbers
    still align correctly for larger boards.
    </remarks>
    """

    width = max(len(str(tile)) for tile in state)
    rows: list[str] = []

    for row in range(size):
        cells: list[str] = []
        for col in range(size):
            tile = state[row * size + col]
            label = blank if tile == 0 else str(tile)
            cells.append(label.rjust(width))
        rows.append(" ".join(cells))

    return "\n".join(rows)


def is_solvable(start: State, target: State, size: int) -> bool:
    """<summary>
    Return whether the start state can reach the target state.
    </summary>

    <param name="start">
    The initial state.
    </param>
    <param name="target">
    The desired target state.
    </param>
    <param name="size">
    The board width and height.
    </param>

    <returns>
    <c>True</c> if the target is reachable from the start state; otherwise
    <c>False</c>.
    </returns>

    <remarks>
    For odd board widths, inversion parity must match. For even board widths,
    inversion parity plus blank row-from-bottom parity must match.
    </remarks>
    """

    return _solvability_signature(start, size) == _solvability_signature(target, size)


def _solvability_signature(state: State, size: int) -> int:
    """<summary>
    Compute the parity signature used for solvability comparison.
    </summary>

    <param name="state">
    The state whose parity signature should be computed.
    </param>
    <param name="size">
    The board width and height.
    </param>

    <returns>
    Either <c>0</c> or <c>1</c>, representing the state's solvability parity.
    </returns>

    <remarks>
    The blank is ignored when counting inversions. For even board widths, the
    blank row counted from the bottom is included in the parity signature.
    </remarks>
    """

    without_blank = [tile for tile in state if tile != 0]
    inversions = 0

    for left_index, left in enumerate(without_blank):
        for right in without_blank[left_index + 1 :]:
            if left > right:
                inversions += 1

    if size % 2 == 1:
        return inversions % 2

    blank_row_from_bottom = size - (state.index(0) // size)
    return (inversions + blank_row_from_bottom) % 2


def states_from_path(path: Iterable[State]) -> tuple[State, ...]:
    """<summary>
    Convert an iterable of states into an immutable tuple.
    </summary>

    <param name="path">
    Any iterable that yields puzzle states.
    </param>

    <returns>
    The same states collected into a tuple.
    </returns>
    """

    return tuple(path)
