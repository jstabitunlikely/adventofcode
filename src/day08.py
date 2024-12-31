import sys
from itertools import permutations

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
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(map_, resonant_harmonics=True)
    print(f'Result 2: {result_2}')
