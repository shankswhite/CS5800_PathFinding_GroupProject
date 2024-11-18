import heapq


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


def a_star(grid, start, end):
    """
    A* algorithm for pathfinding in a 2D grid.

    :param grid: 2D list representing the grid. Each cell contains the cost of traversing it.
    :param start: Tuple (x, y) indicating the start position.
    :param end: Tuple (x, y) indicating the end position.
    :return: List of tuples representing the shortest path from start to end.
    """
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, Node(start[0], start[1], 0)))
    closed_set = set()
    came_from = {}

    g_cost = {start: 0}
    f_cost = {start: heuristic(start, end)}

    while open_set:
        _, current_node = heapq.heappop(open_set)
        current = (current_node.x, current_node.y)

        if current in closed_set:
            continue

        # If we reach the goal, reconstruct the path
        if current == end:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]  # Reverse the path to get start -> end

        closed_set.add(current)

        # Check all neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current_node.x + dx, current_node.y + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:  # Valid grid cell
                tentative_g_cost = g_cost[current] + grid[neighbor[0]][neighbor[1]]

                if neighbor in closed_set or (neighbor in g_cost and tentative_g_cost >= g_cost[neighbor]):
                    continue

                g_cost[neighbor] = tentative_g_cost
                f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, end)
                heapq.heappush(open_set,
                               (f_cost[neighbor], Node(neighbor[0], neighbor[1], tentative_g_cost, current_node)))

    return None  # No path found


# Example usage
grid = [
    [1, 1, 1, 1],
    [1, 999, 999, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]
start = (0, 0)
end = (3, 3)

path = a_star(grid, start, end)
print("Shortest Path:", path)
