import heapq


def dijkstra(grid, start, end):
    """
    Dijkstra's algorithm for pathfinding in a 2D grid.

    :param grid: 2D list where each cell represents the cost of traversing it.
    :param start: Tuple (x, y) indicating the start position.
    :param end: Tuple (x, y) indicating the end position.
    :return: List of tuples representing the shortest path from start to end.
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    distances = {start: 0}
    parent = {}
    priority_queue = [(0, start)]  # (cost, (x, y))

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue

        visited.add(current_node)
        x, y = current_node

        # If we reach the end, reconstruct the path
        if current_node == end:
            path = []
            while current_node in parent:
                path.append(current_node)
                current_node = parent[current_node]
            path.append(start)
            return path[::-1]  # Reverse the path to get start -> end

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                new_distance = current_distance + grid[nx][ny]

                if (nx, ny) not in distances or new_distance < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_distance
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(priority_queue, (new_distance, (nx, ny)))

    return None  # No path found


# Example Usage
grid = [
    [1, 1, 1, 1],
    [1, 999, 999, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]
start = (0, 0)
end = (3, 3)

path = dijkstra(grid, start, end)
print("Shortest Path:", path)
