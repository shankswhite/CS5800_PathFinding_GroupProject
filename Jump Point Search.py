import heapq
import random


def heuristic(a, b):
    """Calculate Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_walkable(grid, x, y):
    """Check if a cell is walkable."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1

def jump(grid, x, y, dx, dy, end):
    nx, ny = x, y
    path = []  # Record intermediate points

    while 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
        nx += dx
        ny += dy

        # Stop if blocked
        if not is_walkable(grid, nx, ny):
            return None, path

        # Add the current point to the path
        path.append((nx, ny))

        # Stop if goal is reached
        if (nx, ny) == end:
            return (nx, ny), path

        # Check for forced neighbors
        if dx != 0 and dy != 0:  # Diagonal movement
            if (is_walkable(grid, nx - dx, ny) and not is_walkable(grid, nx - dx, ny - dy)) or \
               (is_walkable(grid, nx, ny - dy) and not is_walkable(grid, nx - dx, ny - dy)):
                return (nx, ny), path
        elif dx != 0:  # Horizontal movement
            if (is_walkable(grid, nx, ny + 1) and not is_walkable(grid, x, ny + 1)) or \
               (is_walkable(grid, nx, ny - 1) and not is_walkable(grid, x, ny - 1)):
                return (nx, ny), path
        elif dy != 0:  # Vertical movement
            if (is_walkable(grid, nx + 1, ny) and not is_walkable(grid, nx + 1, y)) or \
               (is_walkable(grid, nx - 1, ny) and not is_walkable(grid, nx - 1, y)):
                return (nx, ny), path

    # Return None if no valid jump point is found
    return None, path

def find_neighbors(grid, x, y, parent):
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    if parent:
        px, py = parent
        dx, dy = x - px, y - py

        # Diagonal movement
        if dx != 0 and dy != 0:
            if is_walkable(grid, x + dx, y):
                neighbors.append((x + dx, y))
            if is_walkable(grid, x, y + dy):
                neighbors.append((x, y + dy))
            if is_walkable(grid, x + dx, y + dy):
                neighbors.append((x + dx, y + dy))
        elif dx != 0:  # Horizontal
            if is_walkable(grid, x + dx, y):
                neighbors.append((x + dx, y))
        elif dy != 0:  # Vertical
            if is_walkable(grid, x, y + dy):
                neighbors.append((x, y + dy))
    else:  # If no parent, consider all directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and is_walkable(grid, nx, ny):
                neighbors.append((nx, ny))

    return neighbors

def jump_point_search(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}  # Track the path
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, end)}

    # Validate start and end points
    if not is_walkable(grid, start[0], start[1]) or not is_walkable(grid, end[0], end[1]):
        print(f"Invalid start or end point. Start: {start}, End: {end}")
        return []  # Return empty list if start or end is invalid

    while open_set:
        _, current = heapq.heappop(open_set)
        print(f"Visiting Node: {current}")

        # Check if we've reached the goal
        if current == end:
            print(f"Goal reached at {end}")
            print(f"Final came_from: {came_from}")
            return reconstruct_path(came_from, current)

        # Get neighbors of the current node
        neighbors = find_neighbors(grid, current[0], current[1], came_from.get(current))
        print(f"Neighbors for {current}: {neighbors}")

        for neighbor in neighbors:
            dx, dy = neighbor[0] - current[0], neighbor[1] - current[1]
            print(f"Attempting jump from {current} towards {neighbor} in direction ({dx}, {dy})")

            # Perform the jump in the given direction
            jump_point, jump_path = jump(grid, current[0], current[1], dx, dy, end)
            if jump_point:
                print(f"Jump successful to: {jump_point} via path {jump_path}")
                # Add all intermediate points to came_from and g_cost
                prev_point = current
                for point in jump_path:
                    if point not in g_cost:
                        g_cost[point] = g_cost[prev_point] + heuristic(prev_point, point)
                        came_from[point] = prev_point
                        print(f"came_from[{point}] = {prev_point}")
                        prev_point = point

                # Update the final jump point
                tentative_g_cost = g_cost[current] + heuristic(current, jump_point)
                if jump_point not in g_cost or tentative_g_cost < g_cost[jump_point]:
                    g_cost[jump_point] = tentative_g_cost
                    f_cost[jump_point] = tentative_g_cost + heuristic(jump_point, end)

                    if jump_path:
                        came_from[jump_point] = jump_path[-1]
                    else:
                        came_from[jump_point] = current
                        print(f"came_from[{jump_point}] = {came_from[jump_point]}")

                    heapq.heappush(open_set, (f_cost[jump_point], jump_point))
                    print(f"Added to open_set: {jump_point} with cost {f_cost[jump_point]}")
                    print(f"Current open_set: {[node[1] for node in open_set]}")

            else:
                print(f"Jump to {neighbor} failed")
    return came_from

def reconstruct_path(came_from, current):
    path = [current]
    print(f"Reconstructing path starting from {current}")  # Debugging
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    print(f"Reconstructed Path: {path}")
    return path


def generate_grid_with_obstacles(rows, cols, obstacle_fraction=0.1):
    """
    Generates a grid with random obstacles.
    :param rows: Number of rows in the grid.
    :param cols: Number of columns in the grid.
    :param obstacle_fraction: Fraction of the grid that will be filled with obstacles.
    :return: 2D grid with obstacles.
    """
    grid = [[1 if random.random() > obstacle_fraction else 0 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = 1  # Ensure the start point is walkable
    grid[rows - 1][cols - 1] = 1  # Ensure the end point is walkable
    return grid


# Test the Algorithm
grid = generate_grid_with_obstacles(20,20,0.1)

# Display the grid
print("Generated Grid:")
for row in grid:
    print(row)
start, end = (0, 0), (19, 19)
path = jump_point_search(grid, start, end)
print("\nShortest Path:", path)