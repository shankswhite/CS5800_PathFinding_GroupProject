# Dijkstra Algorithm


**Input:** 

grid (2D array), start (node), end (node)
**Output:** 

PathResult containing shortest_path and step_info



1  DISTANCES = ∞ for all nodes, DISTANCES[start] = 0
2  PRIORITY_QUEUE = [(0, start)]
3  VISITED = empty set
4  PARENT = empty map
5  STEP_INFO = empty dictionary
6  CURRENT_LEVEL = 0

7  while PRIORITY_QUEUE is not empty do
8      (distance_current, current) = POP(PRIORITY_QUEUE)
      
9      if current in VISITED then
10         continue
11     VISITED = VISITED ∪ {current}
        
12     if current = end then
13         break

14     for each neighbor in VALID_NEIGHBORS(grid, current) do
15         if neighbor in VISITED then
16             continue
17         tentative_distance = DISTANCES[current] + 1
         
18         if tentative_distance < DISTANCES[neighbor] then
19             DISTANCES[neighbor] = tentative_distance
20             PARENT[neighbor] = current
21             PUSH(PRIORITY_QUEUE, (tentative_distance, neighbor))
22             STEP_INFO[CURRENT_LEVEL][current] = VALID_NEIGHBORS

23     CURRENT_LEVEL = CURRENT_LEVEL + 1

24 shortest_path = RECONSTRUCT_PATH(PARENT, end)
25 return PathResult(shortest_path, STEP_INFO)



# Astar Algorithm


**Input:** 

grid (2D array), start (node), end (node)

**Output:** 

PathResult containing shortest_path and step_info



1  OPEN_SET = priority queue with (0, start)
2  G_SCORE[start] = 0
3  F_SCORE[start] = HEURISTIC(start, end)
4  CAME_FROM = empty map
5  STEP_INFO = empty dictionary
6  CURRENT_LEVEL = 0

7  while OPEN_SET is not empty do
8      (f_current, current) = POP(OPEN_SET) // Node with smallest f_score
      
9      if current = end then
10         shortest_path = RECONSTRUCT_PATH(CAME_FROM, current)
11         ADD_INTERMEDIATE_POINTS(shortest_path)
12         return PathResult(shortest_path, STEP_INFO)
        
13     for each neighbor in NEIGHBORS(grid, current) do
14         if neighbor is out of bounds or grid[neighbor] = obstacle then
15             continue
16         movement_cost = COST(current, neighbor)
17         tentative_g_score = G_SCORE[current] + movement_cost
         
18         if tentative_g_score < G_SCORE[neighbor] then
19             CAME_FROM[neighbor] = current
20             G_SCORE[neighbor] = tentative_g_score
21             F_SCORE[neighbor] = tentative_g_score + HEURISTIC(neighbor, end)
22             PUSH(OPEN_SET, (F_SCORE[neighbor], neighbor))
23             STEP_INFO[CURRENT_LEVEL][current] = NEIGHBORS

24     CURRENT_LEVEL = CURRENT_LEVEL + 1

25 return PathResult([], STEP_INFO)



# Jump Point Search Algorithm

**Input:** 

grid (2D array), start (node), end (node)
**Output:** 

PathResult containing shortest_path and step_info



1  OPEN_SET = [(0, start)]
2  G_SCORE[start] = 0
3  F_SCORE[start] = HEURISTIC(start, end)
4  CAME_FROM = empty map
5  CAME_FROM_PATH = empty map
6  CLOSED_SET = empty set
7  STEP_INFO = empty dictionary
8  CURRENT_LEVEL = 0

9  while OPEN_SET is not empty do
10     (f_current, current) = POP(OPEN_SET)
      
11     if current = end then
12         path = RECONSTRUCT_PATH(CAME_FROM_PATH, start, end)
13         expanded_path = EXPAND_DIAGONAL_MOVES(path)
14         if expanded_path is valid then
15             return PathResult(expanded_path, STEP_INFO)
16         continue

17     if current in CLOSED_SET then
18         continue
19     CLOSED_SET = CLOSED_SET ∪ {current}

20     successors = GET_SUCCESSORS(grid, current, end, CAME_FROM)
21     for each (neighbor, path_segment, move_cost) in successors do
22         if neighbor in CLOSED_SET then
23             continue
24         tentative_g_score = G_SCORE[current] + move_cost
         
25         if neighbor not in G_SCORE or tentative_g_score < G_SCORE[neighbor] then
26             CAME_FROM[neighbor] = current
27             CAME_FROM_PATH[neighbor] = path_segment
28             G_SCORE[neighbor] = tentative_g_score
29             F_SCORE[neighbor] = tentative_g_score + HEURISTIC(neighbor, end)
30             PUSH(OPEN_SET, (F_SCORE[neighbor], neighbor))
31             STEP_INFO[CURRENT_LEVEL][current] = [neighbor]

32     CURRENT_LEVEL = CURRENT_LEVEL + 1

33 return PathResult([], STEP_INFO)