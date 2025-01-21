import sys
from itertools import permutations

import inputfetcher
from Map import Map
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


def parse_input(example: bool) -> Map:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '8')
    return Map(data, str)


def find_antennas(grid: Map) -> dict[str, list[Coordinate]]:
    antennas: dict[str, list[Coordinate]] = {}
    for c, v in grid.enumerate_map():
        if v == '.':
            continue
        if v not in antennas.keys():
            antennas[v] = []
        antennas[v].append(c)
    return antennas


def solve_1_2(grid: Map,
              resonant_harmonics: bool = False) -> int:
    antinodes = set()
    for antlist in find_antennas(grid).values():
        for ant1, ant2 in list(permutations(antlist, 2)):
            n = 1 if resonant_harmonics else 2
            while True:
                node = n*ant1 - (n-1)*ant2
                if grid.has_coordinate(node):
                    antinodes.add(node)
                else:
                    break
                if not resonant_harmonics:
                    break
                n += 1
    return len(antinodes)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    grid = parse_input(use_example)
    result_1 = solve_1_2(grid,)
    if use_example:
        assert result_1 == 14, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(grid, resonant_harmonics=True)
    if use_example:
        assert result_2 == 34, result_2
    print(f'Result 2: {result_2}')
