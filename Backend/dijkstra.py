import heapq
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

def dijkstra_algorithm(grid, start, end):
    """
    Dijkstra's algorithm for a 20x20 grid with obstacles and intermediate steps logged.
    
    :param grid: 2D list representing the maze where 6 represents obstacles.
    :param start: Tuple (x, y) representing start position.
    :param end: Tuple (x, y) representing end position.
    :return: PathResult object containing shortest path and step information.
    """
    size = len(grid)
    visited = set()
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    parent = {}
    priority_queue = [(0, start)]  # (distance, (x, y))
    level_nodes = defaultdict(dict)  # Stores nodes by their distance level
    current_level = 0

    def get_valid_neighbors(node):
        """
        Returns valid neighboring coordinates for a given node.
        
        :param node: Tuple (x, y) representing current position.
        :return: List of valid neighboring coordinates.
        """
        x, y = node
        valid_neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < size and 
                0 <= ny < size and 
                grid[nx][ny] != 6  # Not an obstacle
            ):
                valid_neighbors.append((nx, ny))
        return valid_neighbors

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        if current_node == end:
            break
            
        # Log all possible paths from the current node
        neighbors = get_valid_neighbors(current_node)
        next_nodes = []
        
        for neighbor in neighbors:
            if neighbor not in visited:
                new_distance = current_distance + 1
                next_nodes.append(neighbor)
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        
        # Store step information for visualization
        if next_nodes:
            if current_distance not in level_nodes:
                current_level += 1
            level_nodes[current_level][f"{current_node[0]},{current_node[1]}"] = [
                [n[0], n[1]] for n in next_nodes
            ]
    
    # Convert level_nodes to final step_info format
    step_info = {level: node_dict for level, node_dict in level_nodes.items()}
    
    # Reconstruct the shortest path
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    
    return PathResult(path[::-1], step_info)