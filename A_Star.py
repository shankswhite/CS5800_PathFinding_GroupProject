import heapq
import random


class Node:
    def __init__(self, x, y, cost, parent=None):
        self.x = x
        self.y = y
        self.cost = cost  # Cost to reach this node
        self.parent = parent  # Parent node for path reconstruction

    def __lt__(self, other):
        return self.cost < other.cost


def heuristic(a, b):
    """Calculate Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def generate_grid(size, obstacle_fraction=0.1):
    """Generate a grid with random obstacles."""
    grid = [[1 if random.random() > obstacle_fraction else 0 for _ in range(size)] for _ in range(size)]
    grid[0][0] = 1  # Ensure start is walkable
    grid[size - 1][size - 1] = 1  # Ensure end is walkable
    return grid


def a_star(grid, start, end):
    """
    A* algorithm with intermediate step logging.

    :param grid: 2D list representing the grid. 1 = walkable, 0 = obstacle.
    :param start: Tuple (x, y) indicating the start position.
    :param end: Tuple (x, y) indicating the end position.
    :return: List of tuples representing the shortest path from start to end.
    """
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, Node(start[0], start[1], 0)))
    closed_set = set()

    g_cost = {start: 0}
    f_cost = {start: heuristic(start, end)}

    while open_set:
        _, current_node = heapq.heappop(open_set)
        current = (current_node.x, current_node.y)

        if current in closed_set:
            continue

        # Log current node
        print(f"Visiting node: {current}")

        # If we reach the goal, reconstruct the path
        if current == end:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            print("Goal reached!")
            return path[::-1]  # Reverse the path to get start -> end

        closed_set.add(current)

        # Check all neighbors (up, down, left, right)
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current_node.x + dx, current_node.y + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 1:
                neighbors.append(neighbor)

        print(f"Possible neighbors: {neighbors}")

        for neighbor in neighbors:
            tentative_g_cost = g_cost[current] + 1  # All walkable cells have a cost of 1

            if neighbor in closed_set or (neighbor in g_cost and tentative_g_cost >= g_cost[neighbor]):
                continue

            g_cost[neighbor] = tentative_g_cost
            f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, end)

            heapq.heappush(open_set,
                           (f_cost[neighbor], Node(neighbor[0], neighbor[1], tentative_g_cost, current_node)))
            print(f"Adding to open set: {neighbor} with f_cost: {f_cost[neighbor]}")

    print("No path found.")
    return None  # No path found


# Generate a 20x20 grid with random obstacles
grid_size = 20
obstacle_probability = 0.3
grid = generate_grid(grid_size, obstacle_probability)

# Display the grid
print("Generated Grid:")
for row in grid:
    print(row)

# Find the shortest path
start = (0, 0)
end = (19, 19)

path = a_star(grid, start, end)
if path:
    print("Shortest Path:")
    print(path)

else:
    print("No path could be found.")
