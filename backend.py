import random

from Dijkstra import dijkstra_with_choices
from A_Star import a_star
from Jump_Point_Search import jump_point_search


def get_result(selected_algo, arr):
    """
    input:
        selected_algo:
            1: Dijkstra
            2: A star
            3: Jump Point Search
        arr: 20*20 array
    output: Tuple containing the shortest path from (0, 0) to (19, 19) and the logged steps.
    """
    if selected_algo == 1:
        return dijkstra_with_choices(arr)
    elif selected_algo == 2:
        return a_star(arr, (0, 0), (19, 19))
    elif selected_algo == 3:
        return jump_point_search(arr, (0, 0), (19, 19))


def generate_map():
    # define width and length of grid
    m = 20
    n = 20
    # Create a 20x20 2D array filled with zeros
    map_array = [[0 for _ in range(m)] for _ in range(n)]

    # Randomly generate obstacles
    num_obstacles = random.randint(30, 50)  # Adjust the number of obstacles as needed
    for _ in range(num_obstacles):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        map_array[x][y] = 6  # Mark the position as an obstacle

    map_array[0][0] = 1  # start point
    map_array[m - 1][n - 1] = 2  # end point
    return map_array


# Example usage
map_array = generate_map()

# Print the map in a more readable format
for row in map_array:
    print(row)
