# Sliding Block Puzzle Search Solver

This repository is a complete implementation of the **Seminar Cognitive
Systems 2: Behavior Control** task **KS2.1 - Sliding Block Puzzle**.

The project solves the required 3x3 sliding puzzle and compares two search
algorithms:

- **Breadth-first search (BFS)** as the uninformed search algorithm
- **A\* search** with the admissible **Manhattan distance** heuristic

The code is intentionally small and direct. It does not use any external search
algorithm library. All search behavior is implemented in this repository using
Python standard-library data structures.

## Table Of Contents

- [Assignment Summary](#assignment-summary)
- [Assignment Puzzle](#assignment-puzzle)
- [Expected Output](#expected-output)
- [How To Run](#how-to-run)
- [Folder Structure](#folder-structure)
- [Code Architecture](#code-architecture)
- [Detailed File And Function Reference](#detailed-file-and-function-reference)
- [How The Algorithms Work](#how-the-algorithms-work)
- [Metrics Explained](#metrics-explained)
- [Assignment Compliance](#assignment-compliance)
- [Troubleshooting](#troubleshooting)
- [Presentation Notes](#presentation-notes)

## Assignment Summary

The assignment asks for a program that solves a 3x3 sliding block puzzle using
at least two search algorithms:

1. An uninformed search algorithm, for example breadth-first search or
   depth-first search.
2. A* search using a permissible, meaning admissible, heuristic.

The program must display:

1. The number of node expansions.
2. The maximum number of nodes held in memory at any point in time.
3. The number of moves needed to solve the puzzle.

This project satisfies those requirements with BFS and A*.

## Assignment Puzzle

The puzzle has 8 numbered tiles and one blank field. The blank is represented
as `0` inside the code and printed as `_` in terminal output.

The state is stored in row-major order:

```text
index:  0 1 2
        3 4 5
        6 7 8
```

So this tuple:

```python
(8, 7, 6, 5, 4, 3, 2, 1, 0)
```

means this board:

```text
8 7 6
5 4 3
2 1 _
```

### Start Configuration

```text
8 7 6
5 4 3
2 1 _
```

Code representation:

```python
(8, 7, 6, 5, 4, 3, 2, 1, 0)
```

### Target Configuration

```text
_ 1 2
3 4 5
6 7 8
```

Code representation:

```python
(0, 1, 2, 3, 4, 5, 6, 7, 8)
```

## Expected Output

Run:

```bash
python3 main.py
```

Typical output:

```text
Sliding Block Puzzle Solver
============================
Board: 3x3
Blank tile: 0, shown as _

Start:
8 7 6
5 4 3
2 1 _

Target:
_ 1 2
3 4 5
6 7 8

Results:
  Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves  Time
  --------------------  ------------------  ----------  ----------------  ------------  -----  -------
  Breadth-first search  -                   178223      180899            24054         28     ...
  A* search             Manhattan distance  174         266               92            28     ...
```

The runtime changes depending on the computer. The important result is:

- BFS finds a 28-move solution.
- A* also finds a 28-move solution.
- A* expands far fewer nodes than BFS.
- A* stores far fewer nodes than BFS.

This is the expected behavior because BFS searches evenly by depth, while A*
uses Manhattan distance to prefer states that look closer to the target.

## How To Run

Open a terminal in the project folder:

```bash
cd /path/to/sliding-puzzle-search-solver-main
```

Check that Python is available:

```bash
python3 --version
```

Python 3.9 or newer is required.

### Run the Web UI (Recommended)

To launch the beautiful, interactive game interface:

```bash
python3 server.py
```

Then open your browser to `http://localhost:8000`. 
This uses Python's built-in `http.server` and has zero third-party dependencies.

### Run the Terminal CLI

If you prefer the command-line output, you can run both algorithms at once, or run them individually:

```bash
# Run both algorithms (default)
python3 main.py

# Run ONLY Breadth-First Search
python3 main.py bfs

# Run ONLY A* Search
python3 main.py astar
```

## Folder Structure

```text
.
|-- README.md
|-- SKS2-01_2026.EN.pdf
|-- main.py
|-- pyproject.toml
|-- server.py
|-- presentation/
|   `-- README.md
|-- src/
|   `-- sliding_puzzle/
|       |-- __init__.py
|       |-- board.py
|       |-- heuristics.py
|       `-- search.py
`-- web/
    |-- game.js
    |-- index.html
    `-- style.css
```

### Root Files

| Path | Purpose |
| --- | --- |
| `README.md` | Full project documentation. |
| `SKS2-01_2026.EN.pdf` | Original assignment PDF. |
| `main.py` | Direct launcher used when running `python3 main.py`. |
| `server.py` | Web API server for the interactive simulation UI. |
| `pyproject.toml` | Python package configuration. |

### `src/sliding_puzzle/`

This is the Python package containing the solver.

| Path | Purpose |
| --- | --- |
| `__init__.py` | Defines the package's public imports. |
| `board.py` | Board representation, validation, parsing, formatting, neighbors, solvability. |
| `heuristics.py` | Heuristic functions used by A*. |
| `search.py` | BFS, A*, path reconstruction, and metric collection. |

### `presentation/`

This folder is reserved for later presentation material. Its README gives a
suggested structure for the 10-minute talk.

### `web/`

The frontend HTML, CSS, and JS files for the interactive web simulation.
It communicates with `server.py` to retrieve paths and metrics, leaving all core algorithm files completely untouched.

## Code Architecture

The code is split into five main responsibilities:

1. `board.py` knows what a puzzle state is and how states connect.
2. `heuristics.py` estimates how far a state is from the target.
3. `search.py` searches through possible states and records metrics.
4. `cli.py` connects user input, puzzle construction, search execution, and printed output.
5. **Web UI & Server (`web/` & `server.py`)**: Provides a beautiful, interactive simulation. The frontend handles animation while `server.py` acts as a bridge, forwarding states directly to the untouched `search.py` algorithms to fetch solutions dynamically.

The normal execution flow is:

```text
main.py
  -> sliding_puzzle.cli.main()
      -> parse command-line arguments
      -> create Puzzle(start, target, size)
      -> check solvability
      -> run BFS and/or A*
      -> print comparison table
      -> optionally print solution path
```

During search, the data flow is:

```text
Puzzle.start
  -> search frontier
  -> Puzzle.neighbors(current_state)
  -> discovered states
  -> parent links and move labels
  -> Puzzle.target found
  -> reconstruct path
  -> SearchResult
  -> CLI output table
```

## Detailed File And Function Reference

This section explains every source file and every function, class, parameter,
and return value.

### `main.py`

Purpose: run the project directly from the repository root.

Important code:

```python
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
```

This adds the local `src/` folder to Python's module search path. That allows
`python3 main.py` to work even when the package has not been installed with
`pip install -e .`.

Then it imports:

```python
from sliding_puzzle.cli import main
```

At the bottom:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

This calls the CLI `main()` function and exits with the return code from that
function.

Return behavior:

- Returns exit code `0` when all selected algorithms find a solution.
- Returns exit code `1` when at least one selected algorithm fails.
- Returns exit code `2` when the puzzle is detected as unsolvable before search.

### `pyproject.toml`

Purpose: package metadata and installation configuration.

Important fields:

| Field | Meaning |
| --- | --- |
| `requires = ["setuptools>=68"]` | Uses setuptools as the build system. |
| `name = "seminar-sliding-puzzle"` | Package distribution name. |
| `version = "0.1.0"` | Project version. |
| `requires-python = ">=3.9"` | Minimum supported Python version. |
| `dependencies = []` | No third-party dependencies. |
| `sliding-puzzle = "sliding_puzzle.cli:main"` | Creates the `sliding-puzzle` console command. |
| `where = ["src"]` | Tells setuptools to find packages inside `src/`. |

### `src/sliding_puzzle/__init__.py`

Purpose: define the public API of the package.

It imports commonly used objects:

```python
Puzzle
State
SearchResult
astar_search
breadth_first_search
manhattan_distance
```

It also defines `__all__`, which lists what should be considered public when
someone imports from the package.

Example:

```python
from sliding_puzzle import Puzzle, astar_search
```

No functions are defined in this file.

### `src/sliding_puzzle/board.py`

Purpose: define puzzle states, validate puzzle objects, generate legal moves,
parse user input, format boards, and check solvability.

#### Imports

```python
from dataclasses import dataclass
from math import isqrt
from typing import Iterable, Iterator
```

- `dataclass` reduces boilerplate for the `Puzzle` class.
- `isqrt` computes an integer square root when inferring board size.
- `Iterable` and `Iterator` are type hints.

#### `State`

```python
State = tuple[int, ...]
```

`State` is a type alias. It means a puzzle state is a tuple of integers.

Example:

```python
(8, 7, 6, 5, 4, 3, 2, 1, 0)
```

There is no return value because this is a type alias, not a function.

#### `MOVE_DELTAS`

```python
MOVE_DELTAS: dict[str, tuple[int, int]] = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}
```

This dictionary maps a move label to a row and column change for the blank.

| Move | Delta | Meaning |
| --- | --- | --- |
| `U` | `(-1, 0)` | Blank moves one row up. |
| `D` | `(1, 0)` | Blank moves one row down. |
| `L` | `(0, -1)` | Blank moves one column left. |
| `R` | `(0, 1)` | Blank moves one column right. |

The move label describes the blank movement, not the numbered tile movement.

#### `Puzzle`

```python
@dataclass(frozen=True)
class Puzzle:
    start: State
    target: State
    size: int | None = None
```

`Puzzle` is an immutable description of a sliding puzzle.

Constructor parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `start` | `State` | Initial board state. |
| `target` | `State` | Desired final board state. |
| `size` | `int | None` | Board width and height. If `None`, it is inferred from `len(start)`. |

For the assignment:

```python
Puzzle(
    start=(8, 7, 6, 5, 4, 3, 2, 1, 0),
    target=(0, 1, 2, 3, 4, 5, 6, 7, 8),
    size=3,
)
```

The class is frozen, so after creation its fields should not be changed. This
helps keep puzzle configuration stable while searches run.

#### `Puzzle.__post_init__(self) -> None`

This method is called automatically after the dataclass is created.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `self` | `Puzzle` | The puzzle object being initialized. |

Return value:

- `None`

What it does:

1. If `size` is not provided, infer it from `len(start)`.
2. Check that the state length is a square number.
3. Check that `start` and `target` both contain `size * size` cells.
4. Check that `start` and `target` contain the same tiles.
5. Check that both states contain exactly one blank tile, represented by `0`.
6. Precompute `_target_positions`, a dictionary from tile value to target
   `(row, column)`.

Possible exceptions:

| Exception | Cause |
| --- | --- |
| `ValueError("Puzzle state length must be a square number.")` | `size` was omitted and `len(start)` is not a square number. |
| `ValueError("Puzzle size could not be determined.")` | Size inference failed. |
| `ValueError("Start and target must contain ... cells.")` | Start or target has the wrong length. |
| `ValueError("Start and target must contain the same tiles.")` | Start and target use different tile values. |
| `ValueError("Each state must contain exactly one blank tile, represented by 0.")` | Missing blank or multiple blanks. |

Why `object.__setattr__` is used:

The dataclass is frozen, so normal assignment is blocked. During initialization,
`object.__setattr__` is used to set inferred or cached values safely.

#### `Puzzle.target_positions(self) -> dict[int, tuple[int, int]]`

This is a read-only property.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `self` | `Puzzle` | The puzzle object. |

Return value:

- A dictionary mapping each tile to its target position as `(row, column)`.

Example for target `_ 1 2 / 3 4 5 / 6 7 8`:

```python
{
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2),
}
```

The heuristic functions use this dictionary to quickly find where each tile
belongs.

#### `Puzzle.neighbors(self, state: State) -> Iterator[tuple[State, str]]`

Generates all states reachable by moving the blank one step.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `self` | `Puzzle` | Puzzle object containing the board size. |
| `state` | `State` | Current state whose legal neighbors should be generated. |

Return value:

- An iterator of `(next_state, move)` pairs.

Each yielded value contains:

| Item | Type | Meaning |
| --- | --- | --- |
| `next_state` | `State` | New board state after one legal blank move. |
| `move` | `str` | Move label: `U`, `D`, `L`, or `R`. |

Example:

```python
puzzle.neighbors((1, 2, 3, 4, 5, 6, 7, 8, 0))
```

The blank is in the bottom-right corner. It can move up or left, so the function
yields:

```python
((1, 2, 3, 4, 5, 0, 7, 8, 6), "U")
((1, 2, 3, 4, 5, 6, 7, 0, 8), "L")
```

Internal steps:

1. Find the blank index with `state.index(0)`.
2. Convert the index to `(row, column)` with `divmod`.
3. Try every move in `MOVE_DELTAS`.
4. Skip moves that would leave the board.
5. Swap the blank with the adjacent tile.
6. Yield the new state and move label.

#### `Puzzle.validate_state(self, state: State) -> None`

Validates that a state can belong to this puzzle.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `self` | `Puzzle` | Puzzle object containing expected size and tiles. |
| `state` | `State` | State to validate. |

Return value:

- `None`

Possible exceptions:

| Exception | Cause |
| --- | --- |
| `ValueError("State must contain ... cells.")` | State has wrong length. |
| `ValueError("State must contain the same tiles as the target.")` | State has wrong tile values. |
| `ValueError("State must contain exactly one blank tile, represented by 0.")` | State has missing or duplicate blank. |

This method is useful when accepting custom states.

#### `parse_state(raw: str, size: int) -> State`

Parses a command-line state string into a `State` tuple.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `raw` | `str` | User-provided state string. |
| `size` | `int` | Board width and height. |

Return value:

- A `State`, meaning `tuple[int, ...]`.

Accepted separators:

- spaces
- commas
- semicolons

Accepted blank values:

- `0`
- `_`
- `blank`
- `x`

Examples:

```python
parse_state("1 2 _ 3 4 5 6 7 8", 3)
# returns (1, 2, 0, 3, 4, 5, 6, 7, 8)

parse_state("1,2,x,3,4,5,6,7,8", 3)
# returns (1, 2, 0, 3, 4, 5, 6, 7, 8)
```

Possible exceptions:

| Exception | Cause |
| --- | --- |
| `ValueError` from `int(token)` | A token is not an integer or accepted blank word. |
| `ValueError("Expected ... values, received ...")` | Wrong number of cells for the selected board size. |

#### `format_state(state: State, size: int, blank: str = "_") -> str`

Converts a tuple state into a printable grid.

Parameters:

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `state` | `State` | required | State to format. |
| `size` | `int` | required | Board width and height. |
| `blank` | `str` | `"_"` | Text used when printing tile `0`. |

Return value:

- A multi-line string.

Example:

```python
format_state((1, 2, 0, 3, 4, 5, 6, 7, 8), 3)
```

returns:

```text
1 2 _
3 4 5
6 7 8
```

Implementation details:

- It computes a cell width so numbers align.
- It walks through rows and columns.
- It replaces tile `0` with the `blank` marker.
- It joins cells with spaces and rows with newline characters.

#### `is_solvable(start: State, target: State, size: int) -> bool`

Checks whether `start` can reach `target`.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `start` | `State` | Initial state. |
| `target` | `State` | Desired target state. |
| `size` | `int` | Board width and height. |

Return value:

- `True` if the start state can reach the target state.
- `False` if it cannot.

How it works:

- For odd board sizes like 3x3, the inversion parity must match.
- For even board sizes, inversion parity plus blank row-from-bottom parity must
  match.

The search functions call this before searching. If a puzzle is not solvable,
they return a not-found result immediately.

#### `_solvability_signature(state: State, size: int) -> int`

Private helper used by `is_solvable`.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `state` | `State` | State to analyze. |
| `size` | `int` | Board width and height. |

Return value:

- `0` or `1`, representing the parity signature of the state.

Details:

1. Remove the blank tile.
2. Count inversions. An inversion is a pair of tiles where a larger number
   appears before a smaller number.
3. For odd board sizes, return `inversions % 2`.
4. For even board sizes, include the blank row counted from the bottom.

The function name starts with `_`, which means it is intended for internal use
inside `board.py`.

#### `states_from_path(path: Iterable[State]) -> tuple[State, ...]`

Converts any iterable of states into a tuple of states.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `path` | `Iterable[State]` | Any iterable producing puzzle states. |

Return value:

- `tuple[State, ...]`

This helper is currently simple. It is useful when code wants an immutable path
representation.

### `src/sliding_puzzle/heuristics.py`

Purpose: provide heuristic functions for A*.

All heuristic functions follow the same signature:

```python
Callable[[Puzzle, State], int]
```

That means each heuristic receives:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `puzzle` | `Puzzle` | Puzzle object containing the target state and board size. |
| `state` | `State` | Current state being estimated. |

and returns:

| Return type | Meaning |
| --- | --- |
| `int` | Estimated number of moves remaining. |

#### `manhattan_distance(puzzle: Puzzle, state: State) -> int`

Default A* heuristic.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `puzzle` | `Puzzle` | Provides `size` and target positions. |
| `state` | `State` | State to estimate. |

Return value:

- Integer sum of each numbered tile's Manhattan distance to its target cell.

Formula for one tile:

```text
abs(current_row - target_row) + abs(current_col - target_col)
```

The blank tile `0` is ignored.

Why it is admissible:

Each legal move can move only one numbered tile by one grid step. Therefore the
total Manhattan distance cannot overestimate the minimum number of moves still
needed.

### `src/sliding_puzzle/search.py`

Purpose: implement BFS, A*, result storage, and path reconstruction.

#### Imports

Important imports:

- `deque`: queue for BFS.
- `dataclass`: result object.
- `heappop`, `heappush`: priority queue operations for A*.
- `count`: increasing sequence number used to break priority queue ties.
- `perf_counter`: runtime measurement.
- `Callable`: type hint for heuristics.

#### `Heuristic`

```python
Heuristic = Callable[[Puzzle, State], int]
```

Type alias for a heuristic function.

It means:

- Input: a `Puzzle` and a `State`
- Output: an integer estimate

#### `SearchResult`

```python
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
```

This immutable dataclass stores everything returned by BFS or A*.

Fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `algorithm` | `str` | Human-readable algorithm name, such as `"Breadth-first search"`. |
| `found` | `bool` | `True` if a solution was found. |
| `path` | `tuple[State, ...]` | Sequence of states from start to target. Empty if not found. |
| `moves` | `tuple[str, ...]` | Move labels from start to target. Empty if not found. |
| `expansions` | `int` | Number of non-goal states expanded. |
| `max_frontier_size` | `int` | Largest number of waiting states in the frontier. |
| `max_nodes_in_memory` | `int` | Largest number of discovered nodes retained. |
| `elapsed_seconds` | `float` | Runtime in seconds. |
| `heuristic` | `str | None` | Heuristic name for A*, or `None` for BFS. |

Relationship between `path` and `moves`:

```text
len(path) = len(moves) + 1
```

For example, if the solution has 28 moves, the path contains 29 states.

#### `SearchResult.move_count(self) -> int`

Property that returns the number of moves.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `self` | `SearchResult` | Result object. |

Return value:

- `len(self.moves)`

This is used by the CLI when printing the `Moves` column.

#### `breadth_first_search(puzzle: Puzzle) -> SearchResult`

Solves the puzzle with BFS graph search.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `puzzle` | `Puzzle` | Puzzle to solve. |

Return value:

- A `SearchResult`.

If a solution is found:

- `found` is `True`
- `path` contains all states from start to target
- `moves` contains all move labels
- metrics are filled with measured values

If the puzzle is unsolvable:

- `found` is `False`
- `path` is empty
- `moves` is empty
- `expansions` is `0` because no search is performed

Important local variables:

| Variable | Type | Meaning |
| --- | --- | --- |
| `start_time` | `float` | Timestamp used to calculate runtime. |
| `frontier` | `deque[State]` | BFS queue of states waiting to be explored. |
| `parents` | `dict[State, State | None]` | Maps each discovered state to its previous state. |
| `move_taken` | `dict[State, str]` | Maps each discovered state to the move used to reach it. |
| `expansions` | `int` | Number of expanded non-goal states. |
| `max_frontier_size` | `int` | Largest queue size seen. |
| `max_nodes_in_memory` | `int` | Largest number of discovered states stored in `parents`. |

BFS process:

1. Check solvability.
2. Put the start state into `frontier`.
3. Store `parents[start] = None`.
4. Repeatedly pop the oldest state with `popleft()`.
5. If it is the target, reconstruct and return the solution.
6. Otherwise, expand it and generate neighbors.
7. Ignore neighbors already present in `parents`.
8. Store new neighbors, parent links, and move labels.
9. Update memory metrics.

Why `parents` also acts as the visited set:

If a state is already in `parents`, it has already been discovered. BFS does
not need to add it again, because the first time BFS discovers a state is always
through a shortest path.

#### `astar_search(puzzle: Puzzle, heuristic: Heuristic = manhattan_distance, heuristic_name: str = "Manhattan distance") -> SearchResult`

Solves the puzzle with A* graph search.

Parameters:

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `puzzle` | `Puzzle` | required | Puzzle to solve. |
| `heuristic` | `Heuristic` | `manhattan_distance` | Function used to estimate distance to target. |
| `heuristic_name` | `str` | `"Manhattan distance"` | Human-readable heuristic name stored in the result. |

Return value:

- A `SearchResult`.

If a solution is found:

- `found` is `True`
- `path` contains the optimal state path
- `moves` contains move labels
- `heuristic` contains the heuristic name
- metrics are filled with measured values

If the puzzle is unsolvable:

- `found` is `False`
- `path` and `moves` are empty
- `expansions` is `0`

Important local variables:

| Variable | Type | Meaning |
| --- | --- | --- |
| `sequence` | counter | Tie-breaker so priority queue entries have stable ordering. |
| `start_h` | `int` | Heuristic value of the start state. |
| `frontier` | `list[tuple[int, int, int, int, State]]` | Heap-based priority queue. |
| `frontier_states` | `set[State]` | Unique states currently waiting in the frontier. |
| `parents` | `dict[State, State | None]` | Parent links for path reconstruction. |
| `move_taken` | `dict[State, str]` | Move labels for path reconstruction. |
| `g_score` | `dict[State, int]` | Best known cost from start to each state. |
| `closed` | `set[State]` | States already expanded. |

Priority queue entry format:

```python
(f_score, h_score, sequence_number, g_score, state)
```

Fields:

| Field | Meaning |
| --- | --- |
| `f_score` | `g_score + h_score`; primary A* priority. |
| `h_score` | Heuristic value; secondary tie-breaker. |
| `sequence_number` | Unique increasing value; prevents tuple comparison from reaching `state`. |
| `g_score` | Cost from start to this state. |
| `state` | Puzzle state. |

A* process:

1. Check solvability.
2. Calculate the start heuristic.
3. Push the start state into the heap.
4. Pop the state with the smallest `f_score`.
5. Skip stale heap entries if a better path was found later.
6. If the current state is the target, reconstruct and return the path.
7. Expand the current state.
8. For each neighbor, calculate `tentative_cost = current_cost + 1`.
9. Ignore the neighbor if the known cost is already better or equal.
10. Otherwise, update parent links, move labels, and `g_score`.
11. Push the improved neighbor into the heap.
12. Update memory metrics.

Why stale heap entries can exist:

Python's `heapq` does not directly update priorities. When a better path to a
state is found, the code pushes a new heap entry. Old entries are skipped later
using:

```python
if current_cost != g_score.get(current):
    continue
```

and:

```python
if current not in frontier_states:
    continue
```

#### `_reconstruct_path(target: State, parents: dict[State, State | None], move_taken: dict[State, str]) -> tuple[tuple[State, ...], tuple[str, ...]]`

Private helper used by BFS and A* after the target is found.

Parameters:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `target` | `State` | Final state where reconstruction starts. |
| `parents` | `dict[State, State | None]` | Parent map from state to previous state. |
| `move_taken` | `dict[State, str]` | Move used to reach each state. |

Return value:

- A pair `(path, moves)`.

Return item details:

| Item | Type | Meaning |
| --- | --- | --- |
| `path` | `tuple[State, ...]` | States from start to target. |
| `moves` | `tuple[str, ...]` | Move labels from start to target. |

How it works:

1. Start at the target state.
2. Follow `parents[current]` backward until reaching `None`.
3. Collect states and moves while moving backward.
4. Reverse both lists so they go from start to target.
5. Return immutable tuples.

#### `_not_found(algorithm: str, heuristic: str | None, start_time: float, expansions: int = 0, max_frontier_size: int = 0, max_nodes_in_memory: int = 0) -> SearchResult`

Private helper for returning a consistent failed search result.

Parameters:

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `algorithm` | `str` | required | Algorithm name. |
| `heuristic` | `str | None` | required | Heuristic name, or `None` for BFS. |
| `start_time` | `float` | required | Timestamp from `perf_counter()`. |
| `expansions` | `int` | `0` | Expansions performed before failure. |
| `max_frontier_size` | `int` | `0` | Maximum frontier size before failure. |
| `max_nodes_in_memory` | `int` | `0` | Maximum memory nodes before failure. |

Return value:

- A `SearchResult` with `found=False`, empty `path`, empty `moves`, and elapsed
  time calculated from `start_time`.

## How The Algorithms Work

### Legal Moves

The solver does not move numbered tiles directly. Instead, it moves the blank.
Moving the blank is equivalent to sliding an adjacent tile into the blank space.

Example:

```text
1 2 3
4 5 6
7 8 _
```

The blank can move up:

```text
1 2 3
4 5 _
7 8 6
```

or left:

```text
1 2 3
4 5 6
7 _ 8
```

### BFS In This Project

BFS uses a queue:

```python
frontier = deque([puzzle.start])
```

It always expands the oldest waiting state. This means it explores all states
at depth `0`, then depth `1`, then depth `2`, and so on.

Because every move costs the same, the first time BFS reaches the target, the
solution is guaranteed to have the minimum number of moves.

The cost is that BFS stores many states. For this assignment puzzle, it expands
178223 states.

### A* In This Project

A* uses a heap priority queue:

```python
heappush(frontier, (f_score, h_score, sequence_number, g_score, state))
```

It chooses states using:

```text
f(n) = g(n) + h(n)
```

For this project:

- `g(n)` is the number of moves already made.
- `h(n)` is the Manhattan distance to the target.

If two states have the same `f(n)`, the implementation uses `h_score` and then
`sequence_number` as tie-breakers.

For the assignment puzzle, A* expands only 174 states with Manhattan distance.

### Why Manhattan Distance Is A Good Heuristic

For each tile, Manhattan distance counts how many grid steps it is away from
its target position:

```text
horizontal distance + vertical distance
```

The blank is ignored. The heuristic is admissible because one move can only
move one tile by one step. Therefore the real remaining number of moves cannot
be smaller than the Manhattan distance estimate for all tiles combined.

## Metrics Explained

The assignment asks for three metrics. The program prints those three plus two
extra useful values.

| Output column | Assignment requirement? | Meaning |
| --- | --- | --- |
| `Expansions` | yes | Number of non-goal states removed from the frontier and expanded. |
| `Max memory nodes` | yes | Maximum number of discovered states retained by the algorithm. |
| `Moves` | yes | Number of moves in the final solution. |
| `Max frontier` | extra | Maximum number of waiting states in the frontier. |
| `Time` | extra | Wall-clock runtime. |

Important detail: `Max memory nodes` counts stored search nodes, not bytes of
RAM used by Python. This matches the assignment wording, which asks for number
of nodes held in memory.

For the assignment puzzle:

```text
Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves
Breadth-first search  -                   178223      180899            24054         28
A* search             Manhattan distance  174         266               92            28
```

Conclusion:

- Both algorithms find the same optimal move count: `28`.
- BFS expands many more states because it has no information about the target.
- A* expands far fewer states because Manhattan distance gives useful guidance.

## Assignment Compliance

| Requirement | Where it is satisfied |
| --- | --- |
| Solve the required 3x3 sliding puzzle | `ASSIGNMENT_START` and `ASSIGNMENT_TARGET` in `src/sliding_puzzle/cli.py` |
| Use an uninformed search algorithm | `breadth_first_search` in `src/sliding_puzzle/search.py` |
| Use A* search | `astar_search` in `src/sliding_puzzle/search.py` |
| Use a permissible/admissible heuristic | `manhattan_distance` in `src/sliding_puzzle/heuristics.py` |
| Count node expansions | `expansions` field in `SearchResult` |
| Count maximum nodes held in memory | `max_nodes_in_memory` field in `SearchResult` |
| Count solution moves | `move_count` property in `SearchResult` |
| Display comparison | `_print_summary` in `src/sliding_puzzle/cli.py` |
| Avoid search-algorithm libraries | BFS and A* are implemented manually using `deque` and `heapq` |

## Troubleshooting

### PowerShell Blocks Virtual Environment Activation

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### BFS Takes A Few Seconds

That is expected for this puzzle. BFS explores a large part of the reachable
state space. A* is much faster because the heuristic guides it.

### Custom Puzzle Says It Is Unsolvable

The program checks inversion parity before searching. If it prints:

```text
This puzzle is not solvable from the given start state.
```

then the selected start state cannot reach the selected target state by legal
sliding moves.

## Presentation Notes

The code is complete without the presentation. For the later 10-minute
presentation, the most important explanation points are:

- The puzzle is represented as a tuple of integers.
- The blank is represented by `0`.
- Legal moves are generated by swapping the blank with an adjacent tile.
- BFS is uninformed and explores by depth.
- BFS is optimal here because all moves cost `1`.
- A* uses `f(n) = g(n) + h(n)`.
- Manhattan distance is admissible.
- Both BFS and A* find a 28-move solution.
- A* expands much fewer nodes than BFS.

Suggested result slide:

```text
Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves
Breadth-first search  -                   178223      180899            24054         28
A* search             Manhattan distance  174         266               92            28
```

Suggested discussion:

BFS is guaranteed to find the shortest path, but it does not know which states
look closer to the target. It therefore expands many states. A* also finds the
shortest path because Manhattan distance is admissible, but it expands far fewer
states because the heuristic gives it useful direction.
