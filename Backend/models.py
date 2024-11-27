from pydantic import BaseModel
from enum import Enum
from typing import List, Tuple, Optional

class Algorithm(str, Enum):
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"
    JUMP_POINT = "jump_point"

class MapRequest(BaseModel):
    session_id: str
    algorithm: Algorithm
    obstacle_count: int
    grid_size: Tuple[int, int] = (20, 20)  # default 20x20

class PathStep(BaseModel):
    current_node: Tuple[int, int]
    visited_nodes: List[Tuple[int, int]]
    next_nodes: List[Tuple[int, int]]
    path_so_far: List[Tuple[int, int]] 