import re
import sys
from functools import reduce
from operator import mul

import InputFetcher
from Coordinate import Coordinate

EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""


def parse_input(example: bool) -> list[tuple[Coordinate, Coordinate]]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '14')
    data = data.strip()
    data = data.split('\n')
    numbers_re = re.compile(r'[0-9-]+', flags=re.DOTALL)
    robots = []
    for px, py, vx, vy in [re.findall(numbers_re, m) for m in data]:
        p = Coordinate(int(px), int(py))
        v = Coordinate(int(vx), int(vy))
        robots.append((p, v))
    return robots


def draw(robots: list[Coordinate],
         width: int,
         height: int):
    # Note: swapping x-y for proper visualization
    M = [['.'] * width for _ in range(height)]
    for r in robots:
        M[r.y][r.x] = '*'
    for row in M:
        print(''.join(row))


def solve_1(robots: list[tuple[Coordinate, Coordinate]],
            width: int,
            height: int,
            ticks: int) -> int:
    # Advance the robots for the given number of ticks
    robots_advanced = [
        Coordinate(
            (p.x + v.x * ticks) % width,
            (p.y + v.y * ticks) % height
        ) for p, v in robots
    ]
    # Count the number of robots in each quadrant
    hw = width//2
    hh = height//2
    rpq = [
        [r for r in robots_advanced if r.x > hw and r.y < hh],
        [r for r in robots_advanced if r.x < hw and r.y < hh],
        [r for r in robots_advanced if r.x > hw and r.y > hh],
        [r for r in robots_advanced if r.x < hw and r.y > hh],
    ]
    return reduce(mul, map(len, rpq))


def solve_2(robots: list[tuple[Coordinate, Coordinate]],
            width: int,
            height: int) -> int:
    position, velocity = zip(*robots)
    robots_p = list(position)
    robots_v = list(velocity)
    WINDOW = 50
    THRESHOLD = 0.50 * len(robots)
    tick = 1
    while True:
        robots_p = [
            Coordinate(
                (p.x + robots_v[j].x) % width,
                (p.y + robots_v[j].y) % height
            ) for j, p in enumerate(robots_p)
        ]
        for x in range(height-WINDOW):
            q = [r for r in robots_p if x <= r.x <= x+WINDOW and x <= r.y <= x+WINDOW]
            if len(q) > THRESHOLD:
                # draw(robots_adv, width, height)
                return tick
        tick += 1


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    robots = parse_input(use_example)
    if use_example:
        width = 11
        height = 7
    else:
        width = 101
        height = 103
    result_1 = solve_1(robots, width, height, ticks=100)
    if use_example:
        assert result_1 == 12, result_1
    print(f'Result 1: {result_1}')
    if use_example:
        result_2 = -1
    else:
        result_2 = solve_2(robots, width, height)
    print(f'Result 2: {result_2}')
