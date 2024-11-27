import json
import random

from heapq import heappush, heappop
from collections import defaultdict
# from dijkstra import dijkstra_algorithm


def create_empty_grid(size=20):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            # Set start point (0,0) and end point (19,19)
            if i == 0 and j == 0:
                row.append(1)  # Start
            elif i == size-1 and j == size-1:
                row.append(2)  # End
            else:
                row.append(0)  # Empty
        grid.append(row)
    return grid

def is_valid_path_exists(grid):
    size = len(grid)
    visited = [[False] * size for _ in range(size)]
    
    def is_valid_move(x, y):
        return (0 <= x < size and 
                0 <= y < size and 
                not visited[x][y] and 
                grid[x][y] != 6)  # Not an obstacle
    
    def dfs(x, y):
        if x == size-1 and y == size-1:  # Reached end point
            return True
            
        visited[x][y] = True
        
        # Try all 4 directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y):
                if dfs(new_x, new_y):
                    return True
                    
        return False
    
    return dfs(0, 0)  # Start from (0,0)

def add_obstacles(grid, obstacle_count):
    size = len(grid)
    obstacles_added = 0
    max_attempts = obstacle_count * 10  # Prevent infinite loop
    attempts = 0
    
    while obstacles_added < obstacle_count and attempts < max_attempts:
        # Create a copy of the grid
        temp_grid = [row[:] for row in grid]
        
        i = random.randint(0, size-1)
        j = random.randint(0, size-1)
        
        # Don't place obstacles on start, end, or existing obstacles
        if temp_grid[i][j] == 0:
            temp_grid[i][j] = 6  # Add obstacle temporarily
            
            # Check if path still exists
            if is_valid_path_exists(temp_grid):
                grid[i][j] = 6  # Make obstacle permanent
                obstacles_added += 1
                
        attempts += 1
    
    return grid

def get_path_information(grid, algorithm):
    start = (0, 0)
    end = (len(grid)-1, len(grid)-1)
    
    if algorithm == 0:
        return dijkstra_algorithm(grid, start, end)
    elif algorithm == 1:
        return astar_algorithm(grid, start, end)
    elif algorithm == 2:
        return jps_algorithm(grid, start, end)
    else:
        return dijkstra_algorithm(grid, start, end)  # default to Dijkstra

class PathResult:
    def __init__(self, shortest_path, step_info):
        self.shortest_path = shortest_path  # List of tuples [(x,y), ...]
        self.step_info = step_info  # Dict of "x,y": [[next_x, next_y], ...]

def format_path_info(path_result):
    # Convert step_info to the format expected by frontend
    formatted_info = []
    for pos, next_nodes in path_result.step_info.items():
        formatted_info.append({pos: next_nodes})
    return formatted_info



def dijkstra_algorithm(grid, start, end):
    size = len(grid)
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    pq = [(0, start)]
    came_from = {}
    step_info = defaultdict(list)
    
    def get_neighbors(pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < size and 
                0 <= new_y < size and 
                grid[new_x][new_y] != 6):  # not an obstacle
                neighbors.append((new_x, new_y))
        return neighbors
    
    while pq:
        current_dist, current = heappop(pq)
        
        if current == end:
            break
            
        if current_dist > distances[current]:
            continue
            
        neighbors = get_neighbors(current)
        step_info[f"{current[0]},{current[1]}"] = [[n[0], n[1]] for n in neighbors]
        
        for neighbor in neighbors:
            distance = current_dist + 1
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                came_from[neighbor] = current
                heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return PathResult(path, step_info)


def lambda_handler(event, context):    
    # Handle OPTIONS request (preflight)
    # if event.get('httpMethod') == 'OPTIONS':
    #     return {
    #         'statusCode': 200,
    #         'headers': {
    #             'Access-Control-Allow-Origin': '*',
    #             'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    #             'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    #             # 'Access-Control-Allow-Credentials': True
    #         },
    #         'body': ''
    #     }

    try:
        # Parse the body if it's a string
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})
            
        algorithm = body.get('algorithm', 0)
        obstacle_count = body.get('obstacleCount', 20)
        
        # Create grid and add obstacles
        grid = create_empty_grid()
        grid = add_obstacles(grid, obstacle_count)
        
        # Get path information using selected algorithm
        path_result = get_path_information(grid, algorithm)
        path_info = format_path_info(path_result.step_info)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Credentials': True,
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'map': grid,
                'pathInformation': path_info,
                'shortestPath': [[x, y] for x, y in path_result.shortest_path]
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Credentials': True,
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }