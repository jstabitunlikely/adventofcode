#!/usr/bin/python3

import inputfetcher
import sys

EXAMPLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""

DIRECTION = "^>v<"

DIR_MAP = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_input(example: bool):
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '6')
    return data.split()


def turn_right(dir: int) -> int:
    return (dir + 1) % 4


def step(dir: int,
         px: int,
         py: int) -> tuple[int, int]:
    px_next = px + DIR_MAP[DIRECTION[dir]][0]
    py_next = py + DIR_MAP[DIRECTION[dir]][1]
    return (px_next, py_next)


def is_obstacle_ahead(dir: int,
                      px: int,
                      py: int,
                      obstacles: list[tuple[int, int]]) -> bool:
    return step(dir, px, py) in obstacles


def find_obstacles(lab_map: list[list]) -> list[tuple[int, int]]:
    obstacles = []
    for x, row in enumerate(lab_map):
        for y, e in enumerate(row):
            if e == '#':
                obstacles.append((x, y))
    return obstacles


def find_guard(lab_map: list[list]):
    for x, row in enumerate(lab_map):
        for y, e in enumerate(row):
            if e in ["^", ">", "v", "<"]:
                return (DIRECTION.index(e), x, y)


def walk(guard: tuple[int, int, int],
         obstacles: list[tuple[int, int]],
         lab_map: list[list]) -> list[tuple[int, int, int]]:
    path = []
    dir, px, py = guard
    while True:
        path.append((dir, px, py))
        # Check if we're running in circles (for Part 2 only)
        if len(path) > 2 and path[-1] == path[0]:
            break
        if is_obstacle_ahead(dir, px, py, obstacles):
            dir = turn_right(dir)
        else:
            px, py = step(dir, px, py)
            # Check if we've walked off the map
            try:
                lab_map[px][py]
            except IndexError:
                break
    return path


def solve_1(lab_map: list[list]) -> int:
    obstacles = find_obstacles(lab_map)
    guard = find_guard(lab_map)
    path = walk(guard, obstacles, lab_map)
    unique_path_len = len(set([(p[1], p[2]) for p in path]))
    return unique_path_len


def solve_2(lab_map: list[list]) -> int:
    obstacles = find_obstacles(lab_map)
    guard = find_guard(lab_map)
    path = walk(guard, obstacles, lab_map)
    loops = 0
    # placeholder for the potential obstacle, so we don't have to re-allocate the array each time
    obstacles.append((-1, -1))
    for dir, px, py in path[1:-1]:
        if not is_obstacle_ahead(dir, px, py, obstacles):
            obstacles[-1] = step(dir, px, py)
            new_path = walk((dir, px, py), obstacles, lab_map)
            if new_path[-1] == new_path[0]:
                loops += 1
    return loops


if __name__ == "__main__":
    example = "--example" in sys.argv
    lab_map = parse_input(example=example)
    result_1 = solve_1(lab_map)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(lab_map)
    print(f'Result 2: {result_2}')
