"""Basic A* Implementation"""

import os
import time

import heapq


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
            if cell == "s":
                start = (i, j)
            elif cell == "g":
                goal = (i, j)

    def heuristic(a, b) -> int:
        """Basic Manhattan distance calculated between two points

        Args:
            a (_type_): Point A
            b (_type_): Point B

        Returns:
            int: Distance between two points
        """
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
            if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != "x":
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
    for row in maze:
        print(" ".join(row))


if __name__ == "__main__":
    example_maze = [
        ["x", "x", "s", "o", "x", "o", "o", "x", "o", "o", "x", "x", "o", "o", "x"],
        ["o", "o", "o", "x", "x", "o", "x", "x", "o", "x", "x", "o", "o", "x", "x"],
        ["o", "x", "x", "x", "o", "o", "o", "o", "o", "o", "o", "o", "x", "x", "o"],
        ["o", "o", "o", "o", "o", "x", "x", "x", "x", "o", "x", "o", "o", "o", "o"],
        ["x", "x", "x", "x", "o", "x", "o", "o", "x", "o", "x", "x", "x", "o", "o"],
        ["o", "o", "o", "o", "o", "o", "o", "x", "x", "o", "o", "o", "x", "x", "o"],
        ["o", "x", "x", "x", "x", "x", "o", "o", "o", "x", "o", "o", "o", "o", "o"],
        ["o", "o", "o", "o", "o", "x", "x", "x", "o", "x", "x", "x", "x", "o", "x"],
        ["x", "x", "x", "x", "o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
        ["x", "x", "o", "o", "o", "x", "x", "x", "x", "x", "o", "x", "x", "g", "x"]
    ]

    result: list[tuple] = a_star(example_maze)
    if result:
        for x, y in result:
            os.system("cls")
            print_maze(example_maze)
            example_maze[x][y] = "*"
            time.sleep(.2)
