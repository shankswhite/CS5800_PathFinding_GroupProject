import heapq


def heuristic(a, b):
    """Calculate Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_walkable(grid, x, y):
    """Check if a cell is walkable."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1


def jump(grid, x, y, dx, dy, end):
    """
    Attempts to jump in the given direction (dx, dy) until it hits a jump point or the goal.
    """
    nx, ny = x + dx, y + dy
    if not is_walkable(grid, nx, ny):
        return None  # Can't walk further in this direction

    if (nx, ny) == end:
        return nx, ny  # Goal reached

    # Check for forced neighbors
    if dx != 0 and dy != 0:  # Diagonal movement
        if is_walkable(grid, nx - dx, ny) and not is_walkable(grid, nx - dx, ny - dy):
            return nx, ny
        if is_walkable(grid, nx, ny - dy) and not is_walkable(grid, nx - dx, ny - dy):
            return nx, ny
    else:  # Horizontal or vertical movement
        if dx != 0:  # Horizontal
            if (is_walkable(grid, nx, ny - 1) and not is_walkable(grid, nx - dx, ny - 1)) or \
                    (is_walkable(grid, nx, ny + 1) and not is_walkable(grid, nx - dx, ny + 1)):
                return nx, ny
        else:  # Vertical
            if (is_walkable(grid, nx - 1, ny) and not is_walkable(grid, nx - 1, ny - dy)) or \
                    (is_walkable(grid, nx + 1, ny) and not is_walkable(grid, nx + 1, ny - dy)):
                return nx, ny

    # Continue jumping
    if dx != 0 and dy != 0:  # Diagonal movement
        # Check for jump points in horizontal and vertical directions
        if jump(grid, nx, ny, dx, 0, end) or jump(grid, nx, ny, 0, dy, end):
            return nx, ny

    return jump(grid, nx, ny, dx, dy, end)


def find_neighbors(grid, x, y, parent):
    """
    Finds all neighbors for a given node, considering JPS rules.
    """
    neighbors = []
    if parent is not None:
        px, py = parent
        # Direction of movement from parent to current node
        dx, dy = (x - px, y - py)

        # Diagonal movement
        if dx != 0 and dy != 0:
            if is_walkable(grid, x, y + dy):
                neighbors.append((x, y + dy))
            if is_walkable(grid, x + dx, y):
                neighbors.append((x + dx, y))
            if is_walkable(grid, x + dx, y + dy):
                neighbors.append((x + dx, y + dy))

            if not is_walkable(grid, x - dx, y):
                if is_walkable(grid, x - dx, y + dy):
                    neighbors.append((x - dx, y + dy))
            if not is_walkable(grid, x, y - dy):
                if is_walkable(grid, x + dx, y - dy):
                    neighbors.append((x + dx, y - dy))

        # Horizontal/Vertical movement
        elif dx == 0:  # Vertical
            if is_walkable(grid, x, y + dy):
                neighbors.append((x, y + dy))
            if not is_walkable(grid, x + 1, y):
                neighbors.append((x + 1, y + dy))
            if not is_walkable(grid, x - 1, y):
                neighbors.append((x - 1, y + dy))

        elif dy == 0:  # Horizontal
            if is_walkable(grid, x + dx, y):
                neighbors.append((x + dx, y))
            if not is_walkable(grid, x, y + 1):
                neighbors.append((x + dx, y + 1))
            if not is_walkable(grid, x, y - 1):
                neighbors.append((x + dx, y - 1))

    else:  # No parent (start node), add all possible directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            if is_walkable(grid, x + dx, y + dy):
                neighbors.append((x + dx, y + dy))

    return neighbors


def reconstruct_path(came_from, current):
    """Reconstruct the path from start to goal."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def jump_point_search(grid, start, end):
    """
    Jump Point Search algorithm for pathfinding in a 2D grid.

    :param grid: 2D list where 1 represents walkable cells and 0 represents obstacles.
    :param start: Tuple (x, y) for the start position.
    :param end: Tuple (x, y) for the end position.
    :return: List of tuples representing the shortest path, or None if no path is found.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)

        neighbors = find_neighbors(grid, current[0], current[1], came_from.get(current))
        for neighbor in neighbors:
            jump_point = jump(grid, current[0], current[1], neighbor[0] - current[0], neighbor[1] - current[1], end)
            if jump_point:
                tentative_g_cost = g_cost[current] + heuristic(current, jump_point)
                if jump_point not in g_cost or tentative_g_cost < g_cost[jump_point]:
                    g_cost[jump_point] = tentative_g_cost
                    f_cost[jump_point] = tentative_g_cost + heuristic(jump_point, end)
                    came_from[jump_point] = current
                    heapq.heappush(open_set, (f_cost[jump_point], jump_point))

    return None  # No path found


# Example Usage
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]
start = (0, 0)
end = (3, 3)

path = jump_point_search(grid, start, end)
print("Shortest Path:", path)
