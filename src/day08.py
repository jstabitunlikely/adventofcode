import sys
from itertools import combinations

import inputfetcher
from Coordinate import Coordinate

EXAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............\
"""


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '8')
    return [list(line) for line in data.split()]


def is_on_map(c: object, map_: list[list[str]]) -> bool:
    return 0 <= c.x < len(map_) and 0 <= c.y < len(map_[0])


def find_antennas(map_: list[list[str]]) -> dict[list[object]]:
    antennas = {}
    for x, row in enumerate(map_):
        for y, c in enumerate(row):
            if c == '.':
                continue
            if c not in antennas.keys():
                antennas[c] = []
            antennas[c].append(Coordinate(x, y))
    return antennas


def solve_1(map_: list[list[str]]) -> int:
    antennas = find_antennas(map_)
    antinodes = set()
    for antlist in antennas.values():
        for ant1, ant2 in list(combinations(antlist, 2)):
            for node in [2*ant1 - ant2, 2*ant2 - ant1]:
                if is_on_map(node, map_):
                    antinodes.add(node)
    return len(antinodes)


def solve_2(map_: list[list[str]]) -> int:
    antennas = find_antennas(map_)
    antinodes = set()
    for antlist in antennas.values():
        for ant1, ant2 in list(combinations(antlist, 2)):
            n = 1
            while True:
                node = n*ant1 - (n-1)*ant2
                if is_on_map(node, map_):
                    antinodes.add(node)
                else:
                    break
                n += 1
            n = 1
            while True:
                node = n*ant2 - (n-1)*ant1
                if is_on_map(node, map_):
                    antinodes.add(node)
                else:
                    break
                n += 1
    return len(antinodes)


if __name__ == "__main__":
    example = "--example" in sys.argv
    map_ = parse_input(example=example)
    result_1 = solve_1(map_)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(map_)
    print(f'Result 2: {result_2}')
