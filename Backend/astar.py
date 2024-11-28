import heapq
import random
from collections import defaultdict

class PathResult:
    """
    Container for path finding results.
    
    :param shortest_path: List of coordinates representing the path.
    :param step_info: Dictionary containing step-by-step information of the algorithm.
    """
    def __init__(self, shortest_path, step_info):
        self.shortest_path = shortest_path
        self.step_info = step_info


class Node:
    def __init__(self, x, y, cost, parent=None):
        self.x = x
        self.y = y
        self.cost = cost  # Cost to reach this node
        self.parent = parent  # Parent node for path reconstruction

    def __lt__(self, other):
        return self.cost < other.cost


def generate_grid(size, obstacle_fraction=0.1):
    """Generate a grid with random obstacles."""
    grid = [[1 if random.random() > obstacle_fraction else 0 for _ in range(size)] for _ in range(size)]
    grid[0][0] = 1  # Ensure start is walkable
    grid[size - 1][size - 1] = 1  # Ensure end is walkable
    return grid

def heuristic(a, b):
    """Calculate diagonal distance heuristic."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    # Use diagonal distance: cost of 1 for orthogonal and √2 for diagonal
    return max(dx, dy) + (2**0.5 - 1) * min(dx, dy)

    
def astar_algorithm(grid, start, end):
    """
    A* algorithm with diagonal exploration but orthogonal-only final path.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    f_score = defaultdict(lambda: float('inf'))
    
    g_score[start] = 0
    f_score[start] = heuristic(start, end)
    
    step_info = defaultdict(dict)
    current_level = 0
    
    # Keep diagonal exploration for better pathfinding
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            # Reconstruct path with orthogonal movements only
            path = []
            curr = current
            while curr in came_from:
                path.append(curr)
                prev = came_from[curr]
                
                # If this is a diagonal move, insert an intermediate point
                dx = curr[0] - prev[0]
                dy = curr[1] - prev[1]
                if abs(dx) == 1 and abs(dy) == 1:
                    # Insert intermediate point (either horizontal-first or vertical-first)
                    # Here we choose horizontal-first
                    intermediate = (prev[0], curr[1])
                    path.append(intermediate)
                
                curr = prev
            path.append(start)
            path.reverse()
            return PathResult(path, step_info)

        next_nodes = []
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            
            if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] == 6:
                continue
                
            movement_cost = 2**0.5 if dx != 0 and dy != 0 else 1
            tentative_g_score = g_score[current] + movement_cost
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                next_nodes.append([nx, ny])
        
        if next_nodes:
            step_info[current_level][f"{current[0]},{current[1]}"] = next_nodes
            current_level += 1

    return PathResult([], step_info)