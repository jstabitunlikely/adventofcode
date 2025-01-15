import sys
from itertools import permutations

import inputfetcher
from inputparsers import parse_matrix2d
from Coordinate import Coordinate
from utils import is_on_map

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
    return parse_matrix2d(data, str)


def find_antennas(map_: list[list[str]]) -> dict[str, list[Coordinate]]:
    antennas = {}
    for x, row in enumerate(map_):
        for y, c in enumerate(row):
            if c == '.':
                continue
            if c not in antennas.keys():
                antennas[c] = []
            antennas[c].append(Coordinate(x, y))
    return antennas


def solve_1_2(map_: list[list[str]],
              resonant_harmonics: bool = False) -> int:
    antinodes = set()
    for antlist in find_antennas(map_).values():
        for ant1, ant2 in list(permutations(antlist, 2)):
            n = 1 if resonant_harmonics else 2
            while True:
                node = n*ant1 - (n-1)*ant2
                if is_on_map(node, map_):
                    antinodes.add(node)
                else:
                    break
                if not resonant_harmonics:
                    break
                n += 1
    return len(antinodes)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    map_ = parse_input(use_example)
    result_1 = solve_1_2(map_,)
    if use_example:
        assert result_1 == 14, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(map_, resonant_harmonics=True)
    if use_example:
        assert result_2 == 34, result_2
    print(f'Result 2: {result_2}')
