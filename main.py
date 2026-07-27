import sys
from pathlib import Path

# Add src to python path so it runs without installation
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sliding_puzzle.board import Puzzle, format_state, is_solvable
from sliding_puzzle.heuristics import manhattan_distance
from sliding_puzzle.search import SearchResult, astar_search, breadth_first_search

def _print_summary(results: list[SearchResult]) -> None:
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


def main():
    algorithm = "all"
    if len(sys.argv) > 1:
        algorithm = sys.argv[1].lower()
        if algorithm not in ("bfs", "astar", "all"):
            print("Usage: python3 main.py [bfs|astar|all]")
            return 1

    start_state = (8, 7, 6, 5, 4, 3, 2, 1, 0)
    target_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    puzzle = Puzzle(start=start_state, target=target_state, size=3)

    print("Sliding Block Puzzle Solver")
    print("============================")
    print(f"Board: {puzzle.size}x{puzzle.size}")
    print("Blank tile: 0, shown as _")
    print("\nStart:")
    print(format_state(puzzle.start, puzzle.size))
    print("\nTarget:")
    print(format_state(puzzle.target, puzzle.size))
    print()

    if not is_solvable(puzzle.start, puzzle.target, puzzle.size):
        print("This puzzle is not solvable from the given start state.")
        return 2

    results = []
    
    if algorithm in ("bfs", "all"):
        print("Running Breadth-first search...")
        results.append(breadth_first_search(puzzle))
    
    if algorithm in ("astar", "all"):
        print("Running A* search...")
        results.append(astar_search(puzzle, manhattan_distance, "Manhattan distance"))

    print()
    _print_summary(results)
    return 0

if __name__ == "__main__":
    sys.exit(main())
