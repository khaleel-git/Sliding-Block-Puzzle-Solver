"""Sliding block puzzle solver for the Seminar Cognitive Systems task."""

from sliding_puzzle.board import Puzzle, State
from sliding_puzzle.heuristics import manhattan_distance, misplaced_tiles
from sliding_puzzle.search import SearchResult, astar_search, breadth_first_search

__all__ = [
    "Puzzle",
    "SearchResult",
    "State",
    "astar_search",
    "breadth_first_search",
    "manhattan_distance",
    "misplaced_tiles",
]

