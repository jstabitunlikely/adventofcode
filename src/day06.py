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


def parse_input(example=False):
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '6')
    return data.split()


def turn_right(dir: str) -> str:
    dir_cnt = DIRECTION.index(dir)
    return DIRECTION[(dir_cnt + 1) % 4]


def turn_left(dir: str) -> str:
    dir_cnt = DIRECTION.index(dir)
    return DIRECTION[(dir_cnt + 3) % 4]


def step(dir: str,
         px: int,
         py: int) -> tuple[int, int]:
    px_next = px + DIR_MAP[dir][0]
    py_next = py + DIR_MAP[dir][1]
    return (px_next, py_next)


def is_obstacle_ahead(dir: str,
                      px: int,
                      py: int,
                      obstacles: list[tuple[int, int]]) -> bool:
    return step(dir, px, py) in obstacles


def walk(guard: tuple[int, int, str],
         obstacles: list[tuple],
         lab_map: list[list]) -> int:
    path = []
    loops = 0
    px, py, dir = guard
    while True:
        path.append((px, py, dir))
        if is_obstacle_ahead(dir, px, py, obstacles):
            dir = turn_right(dir)
        else:
            # px_alt, py_alt, dir_alt = px, py, turn_right(dir)
            # while True:
            #     if (px_alt, py_alt, dir_alt) in path:
            #         loops += 1
            #         break
            #     elif is_obstacle_ahead(dir_alt, px_alt, py_alt, obstacles):
            #         dir_alt = turn_right(dir_alt)
            #     else:
            #         px_alt, py_alt = step(dir_alt, px_alt, py_alt)
            #         try:
            #             lab_map[px_alt][py_alt]
            #         except IndexError:
            #             break
            px, py = step(dir, px, py)
            try:
                lab_map[px][py]
            except IndexError:
                unique_path_len = len(set([(p[0], p[1]) for p in path]))
                return unique_path_len, loops


def solve_1_2(lab_map):
    guard = ()
    obstacles = []
    for x, row in enumerate(lab_map):
        for y, e in enumerate(row):
            if e in ["^", ">", "v", "<"]:
                guard = (x, y, e)
            elif e == '#':
                obstacles.append((x, y))
    return walk(guard, obstacles, lab_map)


if __name__ == "__main__":
    example = "--example" in sys.argv
    lab_map = parse_input(example=example)
    result_1, result_2 = solve_1_2(lab_map)
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
