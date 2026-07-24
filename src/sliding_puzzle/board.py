from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Iterable, Iterator


State = tuple[int, ...]


MOVE_DELTAS: dict[str, tuple[int, int]] = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


@dataclass(frozen=True)
class Puzzle:
    """Immutable description of an N x N sliding block puzzle."""

    start: State
    target: State
    size: int | None = None

    def __post_init__(self) -> None:
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
        return self._target_positions

    def neighbors(self, state: State) -> Iterator[tuple[State, str]]:
        """Yield all states reachable by sliding one tile into the blank field."""

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
        if len(state) != self.size * self.size:
            raise ValueError(f"State must contain {self.size * self.size} cells.")
        if set(state) != set(self.target):
            raise ValueError("State must contain the same tiles as the target.")
        if state.count(0) != 1:
            raise ValueError("State must contain exactly one blank tile, represented by 0.")


def parse_state(raw: str, size: int) -> State:
    """Parse a state from whitespace/comma separated values.

    The blank tile can be written as 0, _, blank, or x.
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
    """Return a human-readable grid representation."""

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
    """Return whether start can reach target for an N-puzzle.

    For odd board widths, inversion parity must match. For even board widths,
    inversion parity plus blank row-from-bottom parity must match.
    """

    return _solvability_signature(start, size) == _solvability_signature(target, size)


def _solvability_signature(state: State, size: int) -> int:
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
    return tuple(path)

