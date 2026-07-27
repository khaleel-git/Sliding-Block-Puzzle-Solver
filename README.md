# Sliding Block Puzzle Search Solver

This repository is a complete implementation of the **Seminar Cognitive
Systems 2: Behavior Control** task **KS2.1 - Sliding Block Puzzle**.

The project solves the required 3x3 sliding puzzle and compares two search algorithms:
- **Breadth-first search (BFS)** as the uninformed search algorithm
- **A\* search** with the admissible **Manhattan distance** heuristic

The code is intentionally small and direct. It does not use any external search
algorithm libraries. All search behavior is implemented in this repository using
Python standard-library data structures (`collections.deque` and `heapq`).

## Assignment Puzzle

**Start Configuration**
```text
8 7 6
5 4 3
2 1 _
```

**Target Configuration**
```text
_ 1 2
3 4 5
6 7 8
```

## How To Run (Web UI)

To launch the interactive game interface and simulation:

```bash
python3 server.py
```
Then open your browser to `http://localhost:8000`. This uses Python's built-in `http.server` and has zero third-party dependencies.

## How To Run (Terminal CLI)

If you prefer the command-line output, you can run the algorithms directly in your terminal:

```bash
# Run both BFS and A* (default)
python3 main.py

# Run ONLY Breadth-First Search
python3 main.py bfs

# Run ONLY A* Search
python3 main.py astar
```

### Expected Output

Running `python3 main.py` will output a comparison table:

```text
Results:
  Algorithm             Heuristic           Expansions  Max memory nodes  Max frontier  Moves  Time
  --------------------  ------------------  ----------  ----------------  ------------  -----  -------
  Breadth-first search  -                   178223      180899            24054         28     ...
  A* search             Manhattan distance  174         266               92            28     ...
```

**Conclusion:** Both algorithms find the same optimal 28-move solution. However, A* expands far fewer nodes because the Manhattan distance heuristic provides an optimistic, admissible estimate that guides the search efficiently.

## Folder Structure

```text
.
|-- main.py           # Terminal CLI entry point
|-- server.py         # Web API server entry point
|-- README.md         # Project documentation
|-- SKS2-01_2026.EN.pdf 
|-- presentation/     # Presentation materials
|-- src/
|   `-- sliding_puzzle/
|       |-- board.py       # Board representation and logic
|       |-- heuristics.py  # Manhattan distance calculation
|       `-- search.py      # BFS and A* algorithm logic
`-- web/              # Frontend HTML/CSS/JS for the simulation
```
