"""<summary>
Command-line interface for the sliding puzzle solver.
</summary>

<remarks>
This module owns the assignment's default start and target states, parses user
arguments, runs the selected search algorithms, and prints the comparison table
required by the project.
</remarks>
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from sliding_puzzle.board import Puzzle, format_state, is_solvable, parse_state
from sliding_puzzle.heuristics import manhattan_distance, misplaced_tiles, zero_heuristic
from sliding_puzzle.search import SearchResult, astar_search, breadth_first_search


# <summary>
# Start state specified by the assignment PDF.
# </summary>
ASSIGNMENT_START = (8, 7, 6, 5, 4, 3, 2, 1, 0)

# <summary>
# Target state specified by the assignment PDF.
# </summary>
ASSIGNMENT_TARGET = (0, 1, 2, 3, 4, 5, 6, 7, 8)

# <summary>
# Mapping from CLI heuristic name to the function and label used by A*.
# </summary>
#
# <remarks>
# The first tuple item is the callable heuristic. The second tuple item is the
# readable name displayed in the results table.
# </remarks>
HEURISTICS = {
    "manhattan": (manhattan_distance, "Manhattan distance"),
    "misplaced": (misplaced_tiles, "Misplaced tiles"),
    "zero": (zero_heuristic, "Zero heuristic"),
}


def main(argv: Sequence[str] | None = None) -> int:
    """<summary>
    Run the command-line solver workflow.
    </summary>

    <param name="argv">
    Optional command-line argument sequence. When <c>None</c>, arguments are
    read from the real process command line by <c>argparse</c>.
    </param>

    <returns>
    Process-style exit code: <c>0</c> when all selected algorithms find a
    solution, <c>1</c> when a selected algorithm fails to find a solution, or
    <c>2</c> when the input puzzle is detected as unsolvable before searching.
    </returns>

    <remarks>
    The function is used by <c>main.py</c>, <c>python -m sliding_puzzle</c>, and
    the installed <c>sliding-puzzle</c> console script.
    </remarks>
    """

    args = _parse_args(argv)
    start = parse_state(args.start, args.size) if args.start else ASSIGNMENT_START
    target = parse_state(args.target, args.size) if args.target else ASSIGNMENT_TARGET
    puzzle = Puzzle(start=start, target=target, size=args.size)

    print("Sliding Block Puzzle Solver")
    print("=" * 28)
    print(f"Board: {puzzle.size}x{puzzle.size}")
    print("Blank tile: 0, shown as _")
    print()
    print("Start:")
    print(format_state(puzzle.start, puzzle.size))
    print()
    print("Target:")
    print(format_state(puzzle.target, puzzle.size))
    print()

    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        print("This puzzle is not solvable from the given start state.")
        return 2

    results: list[SearchResult] = []

    if args.algorithm in {"bfs", "all"}:
        results.append(breadth_first_search(puzzle))

    if args.algorithm in {"astar", "all"}:
        heuristic, heuristic_name = HEURISTICS[args.heuristic]
        results.append(astar_search(puzzle, heuristic, heuristic_name))

    _print_summary(results)

    if args.show_path:
        print()
        for result in results:
            _print_path(result, puzzle.size)

    return 0 if all(result.found for result in results) else 1


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """<summary>
    Configure and parse command-line arguments.
    </summary>

    <param name="argv">
    Optional command-line argument sequence. Passing <c>None</c> makes
    <c>argparse</c> read from <c>sys.argv</c>.
    </param>

    <returns>
    An <c>argparse.Namespace</c> containing algorithm, heuristic, size, start,
    target, and show-path options.
    </returns>

    <remarks>
    Invalid choices are handled by <c>argparse</c>, which prints a usage error
    and exits before the solver runs.
    </remarks>
    """

    parser = argparse.ArgumentParser(
        description="Solve and compare search algorithms for a sliding block puzzle.",
    )
    parser.add_argument(
        "--algorithm",
        choices=("bfs", "astar", "all"),
        default="all",
        help="Algorithm to run. Default: all.",
    )
    parser.add_argument(
        "--heuristic",
        choices=tuple(HEURISTICS),
        default="manhattan",
        help="Heuristic for A*. Default: manhattan.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=3,
        help="Puzzle width and height. Default: 3.",
    )
    parser.add_argument(
        "--start",
        help='Custom start state, e.g. "8 7 6 5 4 3 2 1 0".',
    )
    parser.add_argument(
        "--target",
        help='Custom target state, e.g. "0 1 2 3 4 5 6 7 8".',
    )
    parser.add_argument(
        "--show-path",
        action="store_true",
        help="Print every board state in the solution path.",
    )
    return parser.parse_args(argv)


def _print_summary(results: list[SearchResult]) -> None:
    """<summary>
    Print the algorithm comparison table.
    </summary>

    <param name="results">
    Search results to display. Each result becomes one row in the table.
    </param>

    <returns>
    None.
    </returns>

    <remarks>
    Column widths are calculated dynamically so the output stays aligned even
    when algorithm names or numbers change.
    </remarks>
    """

    headers = (
        "Algorithm",
        "Heuristic",
        "Expansions",
        "Max memory nodes",
        "Max frontier",
        "Moves",
        "Time",
    )
    rows = []
    for result in results:
        rows.append(
            (
                result.algorithm,
                result.heuristic or "-",
                str(result.expansions),
                str(result.max_nodes_in_memory),
                str(result.max_frontier_size),
                str(result.move_count if result.found else "-"),
                f"{result.elapsed_seconds:.4f}s",
            )
        )

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]

    print("Results:")
    print("  " + "  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  " + "  ".join("-" * width for width in widths))
    for row in rows:
        print("  " + "  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def _print_path(result: SearchResult, size: int) -> None:
    """<summary>
    Print the full solution path for one search result.
    </summary>

    <param name="result">
    Search result whose path should be printed.
    </param>
    <param name="size">
    Board width and height used to format each state.
    </param>

    <returns>
    None.
    </returns>

    <remarks>
    If no solution was found, the function prints a short message instead of a
    path. Otherwise it prints the move list followed by every board state.
    </remarks>
    """

    print(f"{result.algorithm} path")
    print("-" * len(f"{result.algorithm} path"))

    if not result.found:
        print("No solution found.")
        return

    print(f"Moves ({result.move_count}): {' '.join(result.moves)}")
    for index, state in enumerate(result.path):
        print()
        print(f"Step {index}")
        print(format_state(state, size))
