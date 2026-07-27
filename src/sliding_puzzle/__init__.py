"""<summary>
Public package interface for the sliding puzzle solver.
</summary>

<remarks>
The imports in this file expose the main classes, search functions, and
heuristics so users can import them directly from <c>sliding_puzzle</c>.
</remarks>
"""

from sliding_puzzle.board import Puzzle, State
from sliding_puzzle.heuristics import manhattan_distance
from sliding_puzzle.search import SearchResult, astar_search, breadth_first_search

# <summary>
# Explicit public symbols exported by this package.
# </summary>
#
# <remarks>
# This controls what is imported when a caller uses:
# from sliding_puzzle import *
# </remarks>
__all__ = [
    "Puzzle",
    "SearchResult",
    "State",
    "astar_search",
    "breadth_first_search",
    "manhattan_distance",
]
