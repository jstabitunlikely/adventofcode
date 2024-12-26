#!/usr/bin/python3

import inputfetcher
from sortedcontainers import SortedKeyList

EXAMPLE1 = """\
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

EXAMPLE2 = """"""

DIRECTION = "^>v<"

DIR_MAP = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_input(example1=False, example2=False):
    if example1:
        data = EXAMPLE1
    elif example2:
        data = EXAMPLE2
    else:
        data = inputfetcher.fetch_input('2024', '6')
    return data.split()


# obsolete solution, works on example but takes too long on the actual input
def walk(position, direction, obstacles, lab_map):
    path = []
    LENGTH = len(lab_map)
    WIDTH = len(lab_map[0])
    px, py = position
    d = direction
    while True:
        if d == '^':
            oxs = sorted([ox for ox, oy in obstacles if ox < px and oy == py])
            ox = oxs[0] if oxs else -1
            for i in range(ox+1, px+1):
                path.append((i, py))
            px, py = [ox+1, py]
            d = '>'
            if not oxs:
                break

        elif d == '>':
            oys = sorted([oy for ox, oy in obstacles if ox == px and oy > py])
            oy = oys[-1] if oys else WIDTH
            for i in range(py, oy):
                path.append((px, i))
            px, py = [px, oy-1]
            d = 'v'
            if not oys:
                break

        elif d == 'v':
            oxs = sorted([ox for ox, oy in obstacles if ox > px and oy == py])
            ox = oxs[-1] if oxs else LENGTH
            for i in range(px, ox):
                path.append((i, py))
            px, py = [ox-1, py]
            d = '<'
            if not oxs:
                break

        elif d == '<':
            oys = sorted([oy for ox, oy in obstacles if ox == px and oy < py])
            oy = oys[0] if oys else -1
            for i in range(oy+1, py+1):
                path.append((px, i))
            px, py = [px, oy+1]
            d = '^'
            if not oys:
                break

    return len(set(path))


def walk2(position: tuple[int, int, int],
          direction: str,
          obstacles: list[tuple],
          lab_map: list[list]):
    path = []
    LENGTH = len(lab_map)
    WIDTH = len(lab_map[0])
    px, py = position
    d = DIRECTION.index(direction)
    while px in range(LENGTH) and py in range(WIDTH):
        path.append((px, py))
        px = px + DIR_MAP[DIRECTION[d]][0]
        py = py + DIR_MAP[DIRECTION[d]][1]
        if (px, py) in obstacles:
            # backtrack from the obstacle
            px = px - DIR_MAP[DIRECTION[d]][0]
            py = py - DIR_MAP[DIRECTION[d]][1]
            d = (d + 1) % 4
    return len(set(path))


def solve_1(lab_map):
    guard_dir = '^'
    guard_pos = ()
    obstacles = []
    for x, row in enumerate(lab_map):
        for y, _ in enumerate(row):
            if lab_map[x][y] == guard_dir:
                guard_pos = (x, y)
            elif lab_map[x][y] == '#':
                obstacles.append((x, y))
    covered = walk2(guard_pos, guard_dir, obstacles, lab_map)
    return covered


def solve_2(lab_map):
    pass


if __name__ == "__main__":
    lab_map = parse_input(example1=False)
    result_1 = solve_1(lab_map)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(lab_map)
    print(f'Result 2: {result_2}')
