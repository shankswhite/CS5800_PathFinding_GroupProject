import heapq
import math
from collections import defaultdict
from typing import Tuple, List, Dict, Set, Optional

class PathResult:
    """
    Container for pathfinding results.

    :param shortest_path: List of coordinates representing the path.
    :param step_info: Dictionary containing step-by-step information of the algorithm.
    """
    def __init__(self, shortest_path, step_info):
        self.shortest_path = shortest_path
        self.step_info = step_info

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    Diagonal distance heuristic for grid movement.
    """
    D = 1.0
    D2 = math.sqrt(2)
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

def is_walkable(grid, x, y) -> bool:
    """
    Check if the position is walkable and within the grid bounds.
    """
    return (0 <= x < len(grid) and 
            0 <= y < len(grid[0]) and 
            grid[x][y] != 6)

def forced_neighbors(grid, pos, direction) -> List[Tuple[int, int]]:
    """
    Identify forced neighbors for a given position and movement direction.
    """
    x, y = pos
    dx, dy = direction
    neighbors = []

    if dy == 0:  # moving horizontally
        if not is_walkable(grid, x, y - 1) and is_walkable(grid, x + dx, y - 1):
            neighbors.append((x + dx, y - 1))
        if not is_walkable(grid, x, y + 1) and is_walkable(grid, x + dx, y + 1):
            neighbors.append((x + dx, y + 1))
    elif dx == 0:  # moving vertically
        if not is_walkable(grid, x - 1, y) and is_walkable(grid, x - 1, y + dy):
            neighbors.append((x - 1, y + dy))
        if not is_walkable(grid, x + 1, y) and is_walkable(grid, x + 1, y + dy):
            neighbors.append((x + 1, y + dy))
    else:  # moving diagonally
        if not is_walkable(grid, x - dx, y) and is_walkable(grid, x - dx, y + dy):
            neighbors.append((x - dx, y + dy))
        if not is_walkable(grid, x, y - dy) and is_walkable(grid, x + dx, y - dy):
            neighbors.append((x + dx, y - dy))
    return neighbors

def jump(grid, from_pos, direction, end) -> Tuple[Optional[Tuple[int, int]], List[Tuple[int, int]], float]:
    """
    Jump in the given direction and return the jump point if found.
    """
    x, y = from_pos
    dx, dy = direction
    path = []
    cost = 0.0

    while True:
        x += dx
        y += dy
        current_pos = (x, y)

        if not is_walkable(grid, x, y):
            return None, [], 0.0

        path.append(current_pos)

        # Calculate the movement cost
        if dx != 0 and dy != 0:
            cost += math.sqrt(2)
        else:
            cost += 1.0

        # Found goal
        if current_pos == end:
            return current_pos, path, cost

        # Found forced neighbor
        if forced_neighbors(grid, current_pos, direction):
            return current_pos, path, cost

        # When moving diagonally, check for jump points in orthogonal directions
        if dx != 0 and dy != 0:
            nx, path_x, cost_x = jump(grid, current_pos, (dx, 0), end)
            ny, path_y, cost_y = jump(grid, current_pos, (0, dy), end)
            if nx is not None or ny is not None:
                return current_pos, path, cost

        # If we reach the edge of the grid without finding a jump point
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
            return None, [], 0.0

def prune_directions(grid, current, parent, direction) -> List[Tuple[int, int]]:
    """
    Prune unnecessary directions according to the JPS rules.
    """
    dx, dy = direction
    directions = []

    if dx != 0 and dy != 0:
        # Diagonal movement
        if is_walkable(grid, current[0], current[1] + dy):
            directions.append((0, dy))
        if is_walkable(grid, current[0] + dx, current[1]):
            directions.append((dx, 0))
        if is_walkable(grid, current[0] + dx, current[1] + dy):
            directions.append((dx, dy))
    else:
        if dx == 0:
            # Vertical movement
            if is_walkable(grid, current[0], current[1] + dy):
                directions.append((0, dy))
            if not is_walkable(grid, current[0] + 1, current[1]):
                directions.append((1, dy))
            if not is_walkable(grid, current[0] - 1, current[1]):
                directions.append((-1, dy))
        else:
            # Horizontal movement
            if is_walkable(grid, current[0] + dx, current[1]):
                directions.append((dx, 0))
            if not is_walkable(grid, current[0], current[1] + 1):
                directions.append((dx, 1))
            if not is_walkable(grid, current[0], current[1] - 1):
                directions.append((dx, -1))
    return directions

def get_successors(grid, current, end, came_from) -> List[Tuple[Tuple[int, int], List[Tuple[int, int]], float]]:
    """
    Get successors from the current node according to JPS rules.
    """
    successors = []
    if current in came_from:
        parent = came_from[current]
        dx = current[0] - parent[0]
        dy = current[1] - parent[1]
        # Normalize direction
        dx = (dx > 0) - (dx < 0)
        dy = (dy > 0) - (dy < 0)
        directions = prune_directions(grid, current, parent, (dx, dy))
    else:
        # If no parent, consider all directions
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    for dx, dy in directions:
        jp, path, cost = jump(grid, current, (dx, dy), end)
        if jp:
            successors.append((jp, path, cost))
    return successors

def expand_diagonal_moves(grid, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Expand diagonal moves into orthogonal moves in the path,
    ensuring that intermediate nodes are walkable.
    """
    expanded_path = []
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        x1, y1 = current
        x2, y2 = next_node
        dx = x2 - x1
        dy = y2 - y1

        expanded_path.append(current)

        # If the move is diagonal, expand it
        if abs(dx) == 1 and abs(dy) == 1:
            # Try horizontal first, then vertical
            intermediate_node1 = (x2, y1)
            intermediate_node2 = (x2, y2)
            if is_walkable(grid, *intermediate_node1) and is_walkable(grid, *intermediate_node2):
                expanded_path.append(intermediate_node1)
            else:
                # Try vertical first, then horizontal
                intermediate_node1 = (x1, y2)
                if is_walkable(grid, *intermediate_node1) and is_walkable(grid, *intermediate_node2):
                    expanded_path.append(intermediate_node1)
                else:
                    # No valid expansion possible
                    return []  # Path is invalid
        # For orthogonal moves, no need to expand

    expanded_path.append(path[-1])  # Add the last node
    return expanded_path

def jps_algorithm(grid, start, end) -> PathResult:
    """
    The main function implementing the Jump Point Search algorithm.
    """
    start = tuple(start)
    end = tuple(end)

    open_set = [(0, start)]
    came_from = {}
    came_from_path = {}
    g_score = {start: 0.0}
    f_score = {start: heuristic(start, end)}
    closed_set = set()

    step_info = defaultdict(dict)
    current_level = 0

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == end:
            # Reconstruct path using the paths stored in came_from_path
            path = []
            current_node = current
            while current_node != start:
                path_segment = came_from_path[current_node]
                path = path_segment + path  # Prepend the path segment
                prev_node = came_from[current_node]
                current_node = prev_node
            path = [start] + path

            # Expand diagonal moves into orthogonal moves
            path = expand_diagonal_moves(grid, path)
            if not path:
                # Path cannot be expanded without hitting obstacles
                continue  # Continue searching for alternative paths

            return PathResult(path, step_info)

        if current in closed_set:
            continue

        closed_set.add(current)

        neighbors = get_successors(grid, current, end, came_from)

        if neighbors:
            next_nodes = []
            for neighbor, path_segment, move_cost in neighbors:
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    came_from_path[neighbor] = path_segment
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    next_nodes.append([neighbor[0], neighbor[1]])

            if next_nodes:
                step_info[current_level][f"{current[0]},{current[1]}"] = next_nodes
                current_level += 1

    return PathResult([], step_info)
