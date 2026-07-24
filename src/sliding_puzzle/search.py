from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
from typing import Callable

from sliding_puzzle.board import Puzzle, State, is_solvable
from sliding_puzzle.heuristics import manhattan_distance


Heuristic = Callable[[Puzzle, State], int]


@dataclass(frozen=True)
class SearchResult:
    algorithm: str
    found: bool
    path: tuple[State, ...]
    moves: tuple[str, ...]
    expansions: int
    max_frontier_size: int
    max_nodes_in_memory: int
    elapsed_seconds: float
    heuristic: str | None = None

    @property
    def move_count(self) -> int:
        return len(self.moves)


def breadth_first_search(puzzle: Puzzle) -> SearchResult:
    """Solve the puzzle with breadth-first graph search."""

    start_time = perf_counter()
    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        return _not_found("Breadth-first search", None, start_time)

    frontier: deque[State] = deque([puzzle.start])
    parents: dict[State, State | None] = {puzzle.start: None}
    move_taken: dict[State, str] = {}

    expansions = 0
    max_frontier_size = 1
    max_nodes_in_memory = 1

    while frontier:
        current = frontier.popleft()

        if current == puzzle.target:
            path, moves = _reconstruct_path(current, parents, move_taken)
            return SearchResult(
                algorithm="Breadth-first search",
                heuristic=None,
                found=True,
                path=path,
                moves=moves,
                expansions=expansions,
                max_frontier_size=max_frontier_size,
                max_nodes_in_memory=max_nodes_in_memory,
                elapsed_seconds=perf_counter() - start_time,
            )

        expansions += 1
        for next_state, move in puzzle.neighbors(current):
            if next_state in parents:
                continue

            parents[next_state] = current
            move_taken[next_state] = move
            frontier.append(next_state)

        max_frontier_size = max(max_frontier_size, len(frontier))
        max_nodes_in_memory = max(max_nodes_in_memory, len(parents))

    return _not_found("Breadth-first search", None, start_time, expansions, max_frontier_size, max_nodes_in_memory)


def astar_search(
    puzzle: Puzzle,
    heuristic: Heuristic = manhattan_distance,
    heuristic_name: str = "Manhattan distance",
) -> SearchResult:
    """Solve the puzzle with A* graph search."""

    start_time = perf_counter()
    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        return _not_found("A* search", heuristic_name, start_time)

    sequence = count()
    start_h = heuristic(puzzle, puzzle.start)
    frontier: list[tuple[int, int, int, int, State]] = []
    heappush(frontier, (start_h, start_h, next(sequence), 0, puzzle.start))

    frontier_states: set[State] = {puzzle.start}
    parents: dict[State, State | None] = {puzzle.start: None}
    move_taken: dict[State, str] = {}
    g_score: dict[State, int] = {puzzle.start: 0}
    closed: set[State] = set()

    expansions = 0
    max_frontier_size = 1
    max_nodes_in_memory = 1

    while frontier:
        _, _, _, current_cost, current = heappop(frontier)

        if current_cost != g_score.get(current):
            continue
        if current not in frontier_states:
            continue

        frontier_states.remove(current)

        if current == puzzle.target:
            path, moves = _reconstruct_path(current, parents, move_taken)
            return SearchResult(
                algorithm="A* search",
                heuristic=heuristic_name,
                found=True,
                path=path,
                moves=moves,
                expansions=expansions,
                max_frontier_size=max_frontier_size,
                max_nodes_in_memory=max_nodes_in_memory,
                elapsed_seconds=perf_counter() - start_time,
            )

        closed.add(current)
        expansions += 1

        for next_state, move in puzzle.neighbors(current):
            tentative_cost = current_cost + 1
            if tentative_cost >= g_score.get(next_state, float("inf")):
                continue

            if next_state in closed:
                closed.remove(next_state)

            parents[next_state] = current
            move_taken[next_state] = move
            g_score[next_state] = tentative_cost
            next_h = heuristic(puzzle, next_state)
            heappush(
                frontier,
                (
                    tentative_cost + next_h,
                    next_h,
                    next(sequence),
                    tentative_cost,
                    next_state,
                ),
            )
            frontier_states.add(next_state)

        max_frontier_size = max(max_frontier_size, len(frontier_states))
        max_nodes_in_memory = max(max_nodes_in_memory, len(g_score))

    return _not_found("A* search", heuristic_name, start_time, expansions, max_frontier_size, max_nodes_in_memory)


def _reconstruct_path(
    target: State,
    parents: dict[State, State | None],
    move_taken: dict[State, str],
) -> tuple[tuple[State, ...], tuple[str, ...]]:
    path: list[State] = []
    moves: list[str] = []
    current: State | None = target

    while current is not None:
        path.append(current)
        if current in move_taken:
            moves.append(move_taken[current])
        current = parents[current]

    path.reverse()
    moves.reverse()
    return tuple(path), tuple(moves)


def _not_found(
    algorithm: str,
    heuristic: str | None,
    start_time: float,
    expansions: int = 0,
    max_frontier_size: int = 0,
    max_nodes_in_memory: int = 0,
) -> SearchResult:
    return SearchResult(
        algorithm=algorithm,
        heuristic=heuristic,
        found=False,
        path=(),
        moves=(),
        expansions=expansions,
        max_frontier_size=max_frontier_size,
        max_nodes_in_memory=max_nodes_in_memory,
        elapsed_seconds=perf_counter() - start_time,
    )

