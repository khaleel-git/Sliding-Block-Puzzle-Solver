# Sliding Block Puzzle Solver

This project solves the Seminar Cognitive Systems 2 task **KS2.1 - Sliding Block Puzzle**.
It implements two search algorithms for the required 3x3 puzzle:

- **Breadth-first search (BFS)** as the uninformed search algorithm
- **A\* search** with the admissible **Manhattan distance** heuristic

The solver reports the metrics required by the assignment:

- number of node expansions
- maximum number of nodes held in memory
- number of moves in the solution

## Assignment Configuration

The blank field is represented as `0` in code and printed as `_`.

Start:

```text
8 7 6
5 4 3
2 1 _
```

Target:

```text
_ 1 2
3 4 5
6 7 8
```

## Project Structure

```text
.
├── README.md
├── main.py
├── pyproject.toml
├── presentation/
│   └── README.md
├── src/
│   └── sliding_puzzle/
│       ├── __init__.py
│       ├── __main__.py
│       ├── board.py
│       ├── cli.py
│       ├── heuristics.py
│       └── search.py
└── tests/
    ├── test_board.py
    └── test_search.py
```

## Requirements

- Python 3.9 or newer
- No third-party Python dependencies
- No search-algorithm libraries are used

Only Python standard-library data structures are used:

- `collections.deque` for BFS
- `heapq` for the A* priority queue

## Installation And Running

The project has no external Python package dependencies. Installing it in editable mode is still recommended because it makes the `src/` package importable from anywhere inside the project.

### 1. Open A Terminal In The Project Folder

macOS/Linux:

```bash
cd "/Users/mohammad/Desktop/Seminar Cognitive Systems"
```

Windows PowerShell:

```powershell
cd "C:\path\to\Seminar Cognitive Systems"
```

Replace the Windows path with the folder where you copied or downloaded this project.

### 2. Check Python

macOS/Linux:

```bash
python3 --version
```

Windows PowerShell:

```powershell
py -3 --version
```

If this prints Python `3.9` or newer, you are ready. If not, install Python from [python.org](https://www.python.org/downloads/) and make sure Python is added to your PATH on Windows.

Common install options:

macOS with Homebrew:

```bash
brew install python
```

Ubuntu/Debian Linux:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Fedora Linux:

```bash
sudo dnf install python3 python3-pip
```

Windows:

Download Python from [python.org](https://www.python.org/downloads/windows/) and enable **Add python.exe to PATH** during installation.

### 3. Create A Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation on Windows, run this once in PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the virtual environment again.

### 4. Install The Project

There are no third-party dependencies to download. This command installs the local project in editable mode.

macOS/Linux:

```bash
python3 -m pip install -e .
```

Windows PowerShell:

```powershell
py -3 -m pip install -e .
```

### 5. Run The Solver

Run the default assignment puzzle.

macOS/Linux:

```bash
python3 main.py
```

Windows PowerShell:

```powershell
py -3 main.py
```

After editable installation, you can also run the package entry point.

macOS/Linux:

```bash
sliding-puzzle
```

Windows PowerShell:

```powershell
sliding-puzzle
```

## Useful Commands

Show the full solution path:

macOS/Linux:

```bash
python3 main.py --show-path
```

Windows PowerShell:

```powershell
py -3 main.py --show-path
```

Run only BFS:

macOS/Linux:

```bash
python3 main.py --algorithm bfs
```

Windows PowerShell:

```powershell
py -3 main.py --algorithm bfs
```

Run only A*:

macOS/Linux:

```bash
python3 main.py --algorithm astar
```

Windows PowerShell:

```powershell
py -3 main.py --algorithm astar
```

Run A* with a different admissible heuristic:

macOS/Linux:

```bash
python3 main.py --algorithm astar --heuristic misplaced
```

Windows PowerShell:

```powershell
py -3 main.py --algorithm astar --heuristic misplaced
```

## Custom Puzzle Input

Pass custom states as whitespace-separated or comma-separated values.
Use `0`, `_`, `blank`, or `x` for the blank field.

macOS/Linux:

```bash
python3 main.py \
  --start "8 7 6 5 4 3 2 1 0" \
  --target "0 1 2 3 4 5 6 7 8"
```

Windows PowerShell:

```powershell
py -3 main.py `
  --start "8 7 6 5 4 3 2 1 0" `
  --target "0 1 2 3 4 5 6 7 8"
```

## Running Tests

If you installed the project with `pip install -e .`, run:

macOS/Linux:

```bash
python3 -m unittest discover -s tests
```

Windows PowerShell:

```powershell
py -3 -m unittest discover -s tests
```

If you skipped editable installation, set `PYTHONPATH` manually.

macOS/Linux:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
py -3 -m unittest discover -s tests
```

## Algorithms

### Breadth-First Search

BFS explores states level by level. In an unweighted puzzle where every move costs `1`, BFS is complete and finds an optimal shortest solution.
The tradeoff is memory: BFS stores many discovered states because it must keep the current search frontier and the states needed for path reconstruction.

### A* Search

A* orders states by:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the number of moves from the start state to state `n`
- `h(n)` is the heuristic estimate from `n` to the target

This implementation uses Manhattan distance:

```text
h(n) = sum of each tile's horizontal and vertical distance to its target cell
```

The blank tile is ignored. Manhattan distance is admissible for the sliding puzzle because each move can reduce a tile's Manhattan distance by at most one, so it never overestimates the true number of moves remaining.

## Metrics

The program prints:

- **Expansions**: how many non-goal states were removed from the frontier and expanded
- **Max memory nodes**: the largest number of unique discovered states retained by the algorithm
- **Max frontier**: the largest number of unique states waiting in the frontier
- **Moves**: the number of moves in the returned solution path
- **Time**: wall-clock runtime for the algorithm

`Max memory nodes` is the metric that corresponds to the assignment requirement "maximum number of nodes held in memory at any point of time."

## Presentation Notes

The `presentation/` folder is reserved for the later 10-minute talk.
For the results slide, run:

```bash
python3 main.py
```

Typical output for the assignment puzzle on this machine:

```text
Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves
Breadth-first search  -                   178223      180899            24054         28
A* search             Manhattan distance  174         266               92            28
```

Then compare BFS and A* using the printed metrics. The expected discussion point is that both algorithms find the same optimal move count, but A* expands significantly fewer nodes because the Manhattan heuristic guides it toward states that are closer to the target.
