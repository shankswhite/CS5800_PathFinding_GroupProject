import heapq
import random

def dijkstra_with_choices(grid):
    """
    Dijkstra's algorithm for a 20x20 grid with obstacles and intermediate steps logged.

    :param grid: 20x20 2D list where each cell represents the cost of traversing it (0 = obstacle).
    :return: Tuple containing the shortest path from (0, 0) to (19, 19) and the logged steps.
    """
    start = (0, 0)
    end = (19, 19)
    rows, cols = 20, 20
    visited = set()
    distances = {start: 0}
    parent = {}
    priority_queue = [(0, start)]  # (cost, (x, y))
    steps_log = {}  # Dictionary to store logs

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue

        visited.add(current_node)
        x, y = current_node

        # Log all possible paths from the current node
        possible_paths = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if (
                # Stay within grid boundaries
                0 <= nx < rows and 0 <= ny < cols and
                (nx, ny) not in visited and  # Node is not visited
                grid[nx][ny] != 0  # Node is not blocked
            ):
                path_cost = distances[current_node] + grid[nx][ny]
                possible_paths.append(((nx, ny), path_cost))

        # Choose the best path (if any) among possible paths
        if possible_paths:
            best_choice = min(possible_paths, key=lambda x: x[1])  # Smallest cost path
            steps_log[current_node] = {"possible_paths": possible_paths, "choice": best_choice}
        else:
            steps_log[current_node] = {"possible_paths": possible_paths, "choice": None}

        # If we reach the end, reconstruct the path
        if current_node == end:
            path = []
            while current_node in parent:
                path.append(current_node)
                current_node = parent[current_node]
            path.append(start)
            return path[::-1], steps_log  # Return both path and logged steps

        # Explore neighbors and update distances
        for nx, ny in [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
            if (
                0 <= nx < rows and 0 <= ny < cols and  # Stay within grid boundaries
                (nx, ny) not in visited and  # Node is not visited
                grid[nx][ny] != 0  # Node is not blocked
            ):
                new_distance = current_distance + grid[nx][ny]
                if (nx, ny) not in distances or new_distance < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_distance
                    parent[(nx, ny)] = current_node
                    heapq.heappush(priority_queue, (new_distance, (nx, ny)))

    return None, steps_log  # No path found


def generate_grid_with_obstacles(rows, cols, obstacle_fraction=0.1):
    """
    Generates a grid with random costs and fewer obstacles.

    :param rows: Number of rows in the grid.
    :param cols: Number of columns in the grid.
    :param obstacle_fraction: Fraction of grid cells to be obstacles (default = 10%).
    :return: 2D list representing the grid.
    """
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    num_obstacles = int(rows * cols * obstacle_fraction)

    # Place random obstacles (value = 0)
    for _ in range(num_obstacles):
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        grid[x][y] = 0

    # Ensure start and end points are not blocked
    grid[0][0] = 1
    grid[rows - 1][cols - 1] = 1

    return grid


# Example Usage
rows, cols = 20, 20
obstacle_fraction = 0.1  # 10% of the grid cells as obstacles
grid = generate_grid_with_obstacles(rows, cols, obstacle_fraction)

# Run the algorithm
shortest_path, steps_log = dijkstra_with_choices(grid)

# Display the grid
print("Generated Grid:")
for row in grid:
    print(row)

# Display the shortest path
print("\nShortest Path:", shortest_path)

# Display the steps log
print("\nSteps Log:")
for node, log in steps_log.items():
    print(f"Visiting Node {node}:")
    print(f"  Possible Paths -> {log['possible_paths']}")
    print(f"  Chosen Path -> {log['choice']}")
