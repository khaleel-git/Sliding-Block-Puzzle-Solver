# Sliding Block Puzzle Search Solver

This project solves the **Seminar Cognitive Systems 2: Behavior Control**
task **KS2.1 - Sliding Block Puzzle**.

It implements a complete 3x3 sliding puzzle solver using:

- **Breadth-first search (BFS)** as the required uninformed search algorithm
- **A\* search** with the admissible **Manhattan distance** heuristic

The program compares both algorithms using the exact metrics required by the
assignment:

- number of node expansions
- maximum number of nodes held in memory at any point in time
- number of moves needed to solve the puzzle

No third-party search libraries are used. The search algorithms are implemented
directly in this repository with Python standard-library data structures.

## Assignment Puzzle

The blank field is represented as `0` in code and printed as `_` in the output.
States are stored in row-major order from top-left to bottom-right.

Start configuration:

```text
8 7 6
5 4 3
2 1 _
```

Code representation:

```python
(8, 7, 6, 5, 4, 3, 2, 1, 0)
```

Target configuration:

```text
_ 1 2
3 4 5
6 7 8
```

Code representation:

```python
(0, 1, 2, 3, 4, 5, 6, 7, 8)
```

## Expected Result

Running the default command solves the assignment puzzle with BFS and A*:

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

The exact time changes by machine. The important comparison is that both
algorithms find an optimal 28-move solution, while A* expands far fewer nodes
because Manhattan distance guides the search toward states closer to the target.

## Project Structure

```text
.
|-- README.md
|-- SKS2-01_2026.EN.pdf
|-- main.py
|-- pyproject.toml
|-- presentation/
|   `-- README.md
|-- src/
|   `-- sliding_puzzle/
|       |-- __init__.py
|       |-- __main__.py
|       |-- board.py
|       |-- cli.py
|       |-- heuristics.py
|       `-- search.py
`-- tests/
    |-- test_board.py
    `-- test_search.py
```

Main files:

- `main.py`: convenient entry point for running the project from the repository
  root without installing first.
- `src/sliding_puzzle/cli.py`: command-line interface, default assignment
  puzzle, argument parsing, and result printing.
- `src/sliding_puzzle/board.py`: puzzle representation, state parsing,
  formatting, neighbor generation, and solvability checking.
- `src/sliding_puzzle/search.py`: BFS, A*, result object, path reconstruction,
  and metric counting.
- `src/sliding_puzzle/heuristics.py`: admissible heuristic functions.
- `tests/`: unit tests for board behavior, heuristics, BFS, A*, and
  unsolvable puzzle handling.
- `presentation/`: workspace for the later 10-minute presentation.

## Requirements

- Python 3.9 or newer
- No external Python package dependencies
- No search-algorithm libraries

The implementation uses only the Python standard library. Important data
structures:

- `collections.deque` for the BFS queue
- `heapq` for the A* priority queue
- `dict` and `set` for visited states, parent links, and cost tracking

## Quick Start

Open a terminal in the project folder:

```bash
cd /path/to/sliding-puzzle-search-solver-main
```

Check Python:

```bash
python3 --version
```

Run the solver:

```bash
python3 main.py
```

On Windows PowerShell, use:

```powershell
py -3 main.py
```

## Optional Installation

The project can run through `main.py` without installation. Editable
installation is useful if you want the `sliding-puzzle` command and easier test
imports.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```bash
python3 -m pip install -e .
```

Windows PowerShell:

```powershell
py -3 -m pip install -e .
```

After installation, run:

```bash
sliding-puzzle
```

## Command-Line Options

Run both algorithms, which is the default:

```bash
python3 main.py
```

Run only BFS:

```bash
python3 main.py --algorithm bfs
```

Run only A*:

```bash
python3 main.py --algorithm astar
```

Show every state in the solution path:

```bash
python3 main.py --show-path
```

Choose an A* heuristic:

```bash
python3 main.py --algorithm astar --heuristic manhattan
python3 main.py --algorithm astar --heuristic misplaced
python3 main.py --algorithm astar --heuristic zero
```

Available heuristics:

- `manhattan`: default heuristic; sum of each tile's Manhattan distance to its
  target position.
- `misplaced`: counts non-blank tiles that are not in their target position.
- `zero`: always returns `0`; useful for testing because A* behaves like
  uniform-cost search when all moves cost `1`.

Use custom start and target states:

```bash
python3 main.py \
  --start "8 7 6 5 4 3 2 1 0" \
  --target "0 1 2 3 4 5 6 7 8"
```

Custom states may use spaces, commas, or semicolons. The blank can be written as
`0`, `_`, `blank`, or `x`.

Examples:

```bash
python3 main.py --start "8,7,6,5,4,3,2,1,0"
python3 main.py --start "8 7 6 5 4 3 2 1 _"
python3 main.py --start "8;7;6;5;4;3;2;1;x"
```

## How The Solver Works

### State Representation

A puzzle state is an immutable tuple of nine integers. For example:

```python
(8, 7, 6, 5, 4, 3, 2, 1, 0)
```

This means:

```text
8 7 6
5 4 3
2 1 _
```

The blank tile is `0`. A legal move swaps the blank with one horizontally or
vertically adjacent tile. Diagonal moves are not allowed.

Move labels describe the direction the blank moves:

- `U`: blank moves up
- `D`: blank moves down
- `L`: blank moves left
- `R`: blank moves right

### Solvability Check

Before searching, the program checks whether the start state can reach the
target state. For a 3x3 puzzle, this is decided by inversion parity. If the
parity of the start state and target state does not match, the puzzle is
unsolvable and the program stops instead of wasting time searching.

### Breadth-First Search

BFS explores the state space level by level:

1. Put the start state in a queue.
2. Remove the oldest state from the queue.
3. If it is the target, reconstruct the path.
4. Otherwise, generate all legal neighbor states.
5. Add unseen neighbors to the queue.
6. Repeat until the target is found or no states remain.

Because every puzzle move costs `1`, BFS is complete and optimal: the first
solution it finds has the minimum number of moves. The disadvantage is memory
usage, because BFS stores a large number of discovered states.

### A* Search

A* uses a priority queue and chooses the next state with the lowest estimated
total cost:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the number of moves from the start state to state `n`
- `h(n)` is the estimated number of moves from state `n` to the target

This project uses Manhattan distance as the default `h(n)`:

```text
h(n) = sum of each tile's horizontal and vertical distance to its target cell
```

The blank tile is ignored in the heuristic.

Manhattan distance is admissible for the sliding puzzle because one legal move
can reduce the Manhattan distance of one tile by at most one. Therefore the
heuristic never overestimates the real remaining cost. With an admissible
heuristic and unit move costs, A* still finds an optimal solution.

## Metrics Explained

The assignment asks the program to count and display three values. This project
prints those values plus runtime and frontier size.

- `Expansions`: number of non-goal states removed from the frontier and expanded.
- `Max memory nodes`: largest number of unique discovered states retained by
  the algorithm at any point in time. This is the assignment's memory metric.
- `Moves`: number of moves in the final solution path.
- `Max frontier`: largest number of unique states waiting to be explored.
- `Time`: wall-clock runtime for the algorithm.

For the assignment puzzle, the comparison is:

```text
Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves
Breadth-first search  -                   178223      180899            24054         28
A* search             Manhattan distance  174         266               92            28
```

Observation: both algorithms find the same optimal solution length, but A*
expands and stores far fewer nodes. This happens because BFS has no information
about which states are closer to the target, while A* uses the Manhattan
distance heuristic to prioritize more promising states.

## Running Tests

If the project was installed with `pip install -e .`, run:

```bash
python3 -m unittest discover -s tests
```

Without installation, run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Windows PowerShell without installation:

```powershell
$env:PYTHONPATH = "src"
py -3 -m unittest discover -s tests
```

Expected result:

```text
Ran 9 tests

OK
```

## Assignment Compliance

| Requirement | Where it is satisfied |
| --- | --- |
| Solve the required 3x3 sliding puzzle | `src/sliding_puzzle/cli.py` contains the exact assignment start and target states |
| Use an uninformed search algorithm | `breadth_first_search` in `src/sliding_puzzle/search.py` |
| Use A* search | `astar_search` in `src/sliding_puzzle/search.py` |
| Use a permissible/admissible heuristic | `manhattan_distance` in `src/sliding_puzzle/heuristics.py` |
| Count node expansions | `expansions` in `SearchResult` |
| Count maximum nodes held in memory | `max_nodes_in_memory` in `SearchResult` |
| Count solution moves | `move_count` in `SearchResult` |
| Display the comparison | `_print_summary` in `src/sliding_puzzle/cli.py` |
| Avoid search-algorithm libraries | only Python standard-library containers are used |

## Troubleshooting

If `python3 main.py` works but tests fail with `ModuleNotFoundError:
No module named 'sliding_puzzle'`, either install the project:

```bash
python3 -m pip install -e .
```

or run tests with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

If BFS takes a few seconds, that is normal for this puzzle. BFS explores many
more states than A* because it has no heuristic guidance.

## Presentation Notes

The presentation is separate from the code. For the later 10-minute talk, the
most important points to explain are:

- how the puzzle is represented as states and moves
- why BFS is uninformed, complete, and optimal for unit-cost moves
- how A* uses `f(n) = g(n) + h(n)`
- why Manhattan distance is admissible
- why A* expands fewer nodes than BFS on this puzzle
- the final comparison table printed by `python3 main.py`
