"""<summary>
Search algorithms and search-result data structures for the puzzle solver.
</summary>

<remarks>
This module contains the assignment's two required algorithms: breadth-first
search as the uninformed algorithm and A* search as the informed algorithm. It
also records the comparison metrics required by the assignment.
</remarks>
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
from typing import Callable

from sliding_puzzle.board import Puzzle, State, is_solvable
from sliding_puzzle.heuristics import manhattan_distance


# <summary>
# Function signature shared by all A* heuristic functions.
# </summary>
#
# <remarks>
# A heuristic receives the puzzle definition and the state being scored, then
# returns an integer estimate of the remaining distance to the target.
# </remarks>
Heuristic = Callable[[Puzzle, State], int]


@dataclass(frozen=True)
class SearchResult:
    """<summary>
    Immutable result returned by a search algorithm.
    </summary>

    <param name="algorithm">
    Human-readable algorithm name.
    </param>
    <param name="found">
    Whether the search found a valid solution.
    </param>
    <param name="path">
    Tuple of states from start to target. Empty when no solution is found.
    </param>
    <param name="moves">
    Tuple of move labels from start to target. Empty when no solution is found.
    </param>
    <param name="expansions">
    Number of non-goal states removed from the frontier and expanded.
    </param>
    <param name="max_frontier_size">
    Largest number of unique states waiting in the frontier at any point.
    </param>
    <param name="max_nodes_in_memory">
    Largest number of discovered states retained by the algorithm at any point.
    </param>
    <param name="elapsed_seconds">
    Wall-clock runtime measured with <c>perf_counter()</c>.
    </param>
    <param name="heuristic">
    Human-readable heuristic name for A*, or <c>None</c> for BFS.
    </param>

    <remarks>
    For successful searches, <c>len(path)</c> is always
    <c>len(moves) + 1</c> because the path includes the start state.
    </remarks>
    """

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
        """<summary>
        Return the number of moves in the solution.
        </summary>

        <returns>
        <c>len(self.moves)</c>.
        </returns>
        """

        return len(self.moves)


def breadth_first_search(puzzle: Puzzle) -> SearchResult:
    """<summary>
    Solve a puzzle using breadth-first graph search.
    </summary>

    <param name="puzzle">
    The puzzle to solve.
    </param>

    <returns>
    A <c>SearchResult</c> containing the solution path, move sequence, required
    assignment metrics, and elapsed runtime. If the puzzle is unsolvable,
    <c>found</c> is <c>False</c> and no nodes are expanded.
    </returns>

    <remarks>
    BFS is uninformed: it does not use a heuristic. Because every puzzle move
    costs one, BFS finds an optimal shortest solution when one exists.
    </remarks>
    """

    start_time = perf_counter()
    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        return _not_found("Breadth-first search", None, start_time)

    # <summary>
    # Queue of states waiting to be explored. BFS pops from the left and appends
    # new states on the right, so states are expanded in discovery order.
    # </summary>
    frontier: deque[State] = deque([puzzle.start])

    # <summary>
    # Parent map used both as a visited set and for reconstructing the final
    # path once the target is reached.
    # </summary>
    parents: dict[State, State | None] = {puzzle.start: None}

    # <summary>
    # Move label used to reach each discovered state from its parent.
    # </summary>
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
    """<summary>
    Solve a puzzle using A* graph search.
    </summary>

    <param name="puzzle">
    The puzzle to solve.
    </param>
    <param name="heuristic">
    Function that estimates the remaining cost from a state to the target.
    </param>
    <param name="heuristic_name">
    Human-readable heuristic name stored in the returned result.
    </param>

    <returns>
    A <c>SearchResult</c> containing the optimal solution path, move sequence,
    required assignment metrics, and elapsed runtime. If the puzzle is
    unsolvable, <c>found</c> is <c>False</c> and no nodes are expanded.
    </returns>

    <remarks>
    A* prioritizes states by <c>f(n) = g(n) + h(n)</c>, where <c>g(n)</c> is
    the known cost from the start and <c>h(n)</c> is the heuristic estimate to
    the target.
    </remarks>
    """

    start_time = perf_counter()
    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        return _not_found("A* search", heuristic_name, start_time)

    # <summary>
    # Monotonic tie-breaker for heap entries. This prevents Python from trying
    # to compare puzzle states when f-score and h-score are equal.
    # </summary>
    sequence = count()
    start_h = heuristic(puzzle, puzzle.start)

    # <summary>
    # Heap entries have the shape:
    # (f_score, h_score, sequence_number, g_score, state).
    # </summary>
    frontier: list[tuple[int, int, int, int, State]] = []
    heappush(frontier, (start_h, start_h, next(sequence), 0, puzzle.start))

    # <summary>
    # Unique states currently represented in the active frontier. This is used
    # for memory metrics and for skipping heap entries that became stale.
    # </summary>
    frontier_states: set[State] = {puzzle.start}

    # <summary>
    # Parent and move maps are used to reconstruct the solution path after the
    # target state is removed from the frontier.
    # </summary>
    parents: dict[State, State | None] = {puzzle.start: None}
    move_taken: dict[State, str] = {}

    # <summary>
    # Best known cost from the start state to each discovered state.
    # </summary>
    g_score: dict[State, int] = {puzzle.start: 0}

    # <summary>
    # States that have already been expanded. A state can be reopened if a
    # better path to it is discovered.
    # </summary>
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
    """<summary>
    Reconstruct the state path and move sequence after a target is found.
    </summary>

    <param name="target">
    The final state where reconstruction starts.
    </param>
    <param name="parents">
    Mapping from each discovered state to the state that came before it.
    </param>
    <param name="move_taken">
    Mapping from each discovered state to the move used to reach it from its
    parent.
    </param>

    <returns>
    A pair <c>(path, moves)</c>. <c>path</c> is ordered from start to target,
    and <c>moves</c> contains the corresponding move labels.
    </returns>

    <remarks>
    Parent links point backward from target to start, so this helper collects
    values backward and reverses them before returning.
    </remarks>
    """

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
    """<summary>
    Build a consistent failed-search result.
    </summary>

    <param name="algorithm">
    Human-readable algorithm name.
    </param>
    <param name="heuristic">
    Human-readable heuristic name, or <c>None</c> for uninformed algorithms.
    </param>
    <param name="start_time">
    Timestamp captured before the algorithm began.
    </param>
    <param name="expansions">
    Number of expansions performed before failure.
    </param>
    <param name="max_frontier_size">
    Maximum frontier size observed before failure.
    </param>
    <param name="max_nodes_in_memory">
    Maximum number of retained nodes observed before failure.
    </param>

    <returns>
    A <c>SearchResult</c> with <c>found=False</c>, empty path, empty moves, and
    elapsed runtime calculated from <c>start_time</c>.
    </returns>
    """

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
