import os
import time
import random
import heapq


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


START_STR = f"{bcolors.HEADER}{bcolors.BOLD}S{bcolors.ENDC}"
GOAL_STR = f"{bcolors.HEADER}{bcolors.BOLD}E{bcolors.ENDC}"
WALL_STR = f"{bcolors.FAIL}{bcolors.BOLD}#{bcolors.ENDC}"
PATH_STR = f"{bcolors.OKGREEN}{bcolors.BOLD}*{bcolors.ENDC}"
CHECKED_STR = f"{bcolors.BOLD}{bcolors.WARNING}c{bcolors.ENDC}"


def find_positions(maze: list[list[str]], start_marker: tuple, goal_marker: tuple) -> tuple:
    """This function finds the positions of the start and goal markers in a given maze.
    
    Args:
        maze (list[list[str]]): A 2D list representing the maze.
        start_marker (tuple): The marker used to represent the start position in the maze.
        goal_marker (tuple): The marker used to represent the goal position in the maze.
    
    Returns:
        tuple: A tuple containing the coordinates of the start and goal positions in the maze.
    """
    
    start = goal = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == start_marker:
                start = (i, j)
            elif cell == goal_marker:
                goal = (i, j)
    return start, goal


def heuristic(a: tuple, b: tuple) -> int:
    """This function calculates and returns the Manhattan distance between two points.
    
    Args:
        a (tuple): The first point in the form of a tuple (x1, y1).
        b (tuple): The second point in the form of a tuple (x2, y2).
    
    Returns:
        int: The Manhattan distance between the two points.
    """
    
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(maze: list[list[str]], position: tuple) -> list[tuple]:
    """This function gets the neighbors of a given position in a maze.
    
    Args:
        maze (list[list[str]]): A 2D list representing the maze.
        position (tuple): A tuple representing the current position in the maze.
    
    Returns:
        list: A list of tuples representing the valid neighbors of the current position in the maze.
    """
    
    x, y = position
    neighbors = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(maze) and 0 <= ny < len(maze[0])]


def a_star(maze: list[list[str]]) -> list[tuple]:
    """This function implements the A* search algorithm to find the shortest path in a maze from a start position to a goal position. 
    
    Args:
        maze (list[list[str]]): A 2D list representing the maze where each cell can be a wall, start, goal, or an empty cell.
    
    Returns:
        list[tuple]: A list of tuples representing the path from the start position to the goal position. Each tuple represents a position in the maze in the form (row, column). If no path is found, the function returns None.
    
    Raises:
        ValueError: If the start or goal positions are not found in the maze.
    """
    
    start, goal = find_positions(maze, START_STR, GOAL_STR)
    if not start or not goal:
        return None

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in get_neighbors(maze, current):
            if maze[neighbor[0]][neighbor[1]] == WALL_STR:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [pos for _, pos in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

            if maze[neighbor[0]][neighbor[1]] not in [START_STR, GOAL_STR]:
                maze[neighbor[0]][neighbor[1]] = CHECKED_STR
                print_maze(maze)

    return None


def print_maze(maze: list[list[str]]):
    """This function clears the console and prints a given maze.
    
    Args:
        maze (list[list[str]]): A 2D list representing the maze to be printed. Each inner list represents a row in the maze.
    
    Example:
        print_maze([['#', '#', '#'], ['#', ' ', '#'], ['#', '#', '#']])
    
    Note:
        This function is platform independent. It uses 'cls' command for Windows and 'clear' command for Unix/Linux.
    """
    
    os.system("cls" if os.name == "nt" else "clear")
    for row in maze:
        print(" ".join(row))


def generate_maze(x: int, y: int) -> list[list[str]]:
    """Generates a maze of given dimensions with random start and end points and random walls.
    
    Args:
        x (int): The number of rows in the maze.
        y (int): The number of columns in the maze.
    
    Returns:
        list: A 2D list representing the maze. 'o' represents open path, 'START_STR' represents the start point, 
        'GOAL_STR' represents the end point and 'WALL_STR' represents a wall. The start and end points are randomly 
        placed in the first and last third of the maze respectively. Walls are randomly placed throughout the maze 
        with a 35% probability.
    """
    
    maze = [["o" for _ in range(y)] for _ in range(x)]
    start = (random.randint(0, x // 3), random.randint(0, y // 3))
    end = (random.randint(2 * x // 3, x - 1), random.randint(2 * y // 3, y - 1))

    maze[start[0]][start[1]] = START_STR
    maze[end[0]][end[1]] = GOAL_STR

    wall_percentage = 35
    for i in range(x):
        for j in range(y):
            if random.randint(0, 100) < wall_percentage and is_valid_wall_location(maze, i, j):
                maze[i][j] = WALL_STR
    return maze


def is_valid_wall_location(maze: list[list[str]], x: int, y: int):
    """This function checks if a given location in a maze is a valid location for a wall. 
    
    Args:
        maze (list): A 2D list representing the maze.
        x (int): The x-coordinate of the location.
        y (int): The y-coordinate of the location.
    
    Returns:
        bool: False if the location is the start or the goal of the maze, or if any of its neighbors is the start or the goal. True otherwise.
    """
    
    if maze[x][y] in [START_STR, GOAL_STR]:
        return False
    neighbors = [
        maze[x - 1][y] if x > 0 else "",
        maze[x + 1][y] if x < len(maze) - 1 else "",
        maze[x][y - 1] if y > 0 else "",
        maze[x][y + 1] if y < len(maze[0]) - 1 else ""
    ]
    return not (START_STR in neighbors or GOAL_STR in neighbors)


if __name__ == "__main__":
    example_maze = generate_maze(20, 20)
    print_maze(example_maze)
    path = a_star(example_maze)

    if path:
        for x, y in path:
            example_maze[x][y] = PATH_STR
            print_maze(example_maze)
            time.sleep(0.2)
    else:
        print("No valid path found.")
