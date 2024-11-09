"""Basic A* Implementation"""

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


START_STR = bcolors.HEADER + bcolors.BOLD + "S" + bcolors.ENDC
GOAL_STR = bcolors.HEADER + bcolors.BOLD + "E" + bcolors.ENDC
WALL_STR = bcolors.FAIL + bcolors.BOLD + '#' + bcolors.ENDC
PATH_STR = bcolors.OKGREEN + bcolors.BOLD + '*' + bcolors.ENDC
CHECKED_STR = bcolors.BOLD + bcolors.WARNING + "c" + bcolors.ENDC


def a_star(maze: list[list[str]]) -> list[tuple] | None: # pylint: disable=R0914
    """Basic implementation of A* pathfinding algorithm

    Args:
        maze (list[list[str]]): Maze to navigate

    Returns:
        list[tuple]: Path from start to end
    """
    # Locate start and end positions
    start = goal = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == START_STR:
                start = (i, j)
            elif cell == GOAL_STR:
                goal = (i, j)

    def heuristic(a, b) -> int:
        """Basic Manhattan distance calculated between two points

        Args:
            a (tuple): Point A
            b (tuple): Point B

        Returns:
            int: Distance between two points
        """
        if maze[a[0]][a[1]] not in [START_STR, GOAL_STR]:
            maze[a[0]][a[1]] = CHECKED_STR
            print_maze(maze)
            time.sleep(.1)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        # If we are at the goal, return
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path

        neighbors: list[tuple] = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] -1)
        ]

        for neighbor in neighbors:
            x, y = neighbor # pylint: disable=W0621

            # Check if neighbor is in bounds and if not wall
            if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != WALL_STR:
                # Calculate tentativ g score
                tentative_g_score: int = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    # Add neighbor to the open set if not there already
                    if neighbor not in [position for _, position in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))


    return None


def print_maze(maze: list[list[str]]) -> None:
    """Pretty print the maze

    Args:
        maze (list[list[str]]): 2D Array to print
    """
    os.system("cls")
    for row in maze:
        print(" ".join(row))


def generate_maze(x: int, y: int) -> list[list[str]]:
    def _is_valid_cell(x: int, y: int) -> bool:
        if maze[x][y] in [START_STR, GOAL_STR]:
            return False

        neighbors: list = [
            maze[x-1][y] if 0 <= x-1 else "",
            maze[x+1][y] if x+1 < len(maze) else "",
            maze[x][y+1] if y+1 < len(maze[0]) else "",
            maze[x][y-1] if 0 <= y-1 else ""
        ]

        if START_STR in neighbors or GOAL_STR in neighbors:
            return False

        return True


    maze: list[list[str]] = [["o" for _ in range(y)] for _ in range(x)]

    lower_range: int = int(y / 3)
    upper_range: int = int(y - (y / 3))
    start: tuple = (random.randint(0, lower_range), random.randint(0, lower_range))
    end: tuple = (random.randint(upper_range, x-1), random.randint(upper_range, y-1))

    maze[start[0]][start[1]] = START_STR
    maze[end[0]][end[1]] = GOAL_STR

    for i, row in enumerate(maze):
        for j, _ in enumerate(row):
            wall_percent = 35
            wall_chance = random.randint(0, 100)

            place_wall: bool = True if wall_chance <= wall_percent else False
            if place_wall and _is_valid_cell(i, j):
                maze[i][j] = WALL_STR

    return maze


if __name__ == "__main__":
    # print_maze(generate_maze(20, 20))

    example_maze = generate_maze(20, 20)

    result: list[tuple] = a_star(example_maze)
    if result:
        for x, y in result:
            print_maze(example_maze)
            example_maze[x][y] = PATH_STR
            time.sleep(.2)
    else:
        print("No valid path found.")
